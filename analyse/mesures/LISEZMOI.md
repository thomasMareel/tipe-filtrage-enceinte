# `analyse/mesures/` — données brutes, en lecture seule

> **Ce qui est dans ce dossier a coûté une séance de banc. Ce qui est dans
> `analyse/resultats/` coûte dix secondes.** Les deux ne se confondent jamais :
> un fichier de `mesures/` est versionné, daté, et **ne se réécrit pas**. Si un
> dépouillement était faux, on rejoue `depouiller()` — on ne corrige pas le
> fichier à la main.
>
> Référence de format : `REFERENCE-TECHNIQUE.md` § 09.3 (format), § 02.11
> (protocole), § 02.12 (tableau de relevé et contrat d'interface avec l'acte 2).
> Le code qui lit et écrit tout cela est `analyse/io_mesures.py`.

---

## 1. Ce que contient le dossier

| Fichier | Statut |
|---|---|
| `exemple_synthetique_sub.csv` | **SYNTHÉTIQUE** — engendré par un modèle, aucune mesure. Sert à éprouver la chaîne avant la première séance. |
| `AAAA-MM-JJ_etalonnage_{R8,C100uF,C10uF,L18mH}.csv` | *[[à mesurer — phase 1]]* porte de validation sur composants connus (§ 02.8) |
| `AAAA-MM-JJ_sub_caisse_Rref{100,10}.csv` | *[[à mesurer — phase 1]]* le relevé clé, et son recoupement avec l'autre étalon (§ 02.4) |
| `AAAA-MM-JJ_mediums_serie.csv` | *[[à mesurer — phase 1]]* les deux médiums **tels qu'ils sont câblés**, jusqu'à 2 kHz |
| `rew/`, `scope/` | *[[à créer]]* exports REW (`.txt`/`.zma`) et acquisitions brutes d'oscilloscope, sous le **même nom** que le CSV dépouillé correspondant |
| `composants.csv` | *[[à créer — avant la phase 3]]* valeur nominale, valeur **mesurée**, incertitude, DCR mesurée, prix, date. Un condensateur ±20 % acheté à 150 µF en fait 163 : le design optimal se recalcule sur les valeurs mesurées. |

**Convention de nom** : `AAAA-MM-JJ_dipole_condition.csv`, en minuscules, sans
accent ni espace. La date est celle de la **manip**, pas celle du fichier.

---

## 2. Le format CSV « maison »

Une ligne de titre, puis **une métadonnée par ligne** au format `# clé: valeur`,
puis la ligne de noms de colonnes, puis les points. Séparateur virgule, point
décimal, encodage **UTF-8**, fins de ligne LF, **9 chiffres significatifs**.

```
# TIPE filtrage enceinte -- mesure d impedance
# version_format: 1
# date: 2026-10-05T14:32
# dipole: sub 18 pouces en caisse
# montage: A (dipole a la masse) -- GBF + oscilloscope 2 voies
# R_ref_nominale_ohm: 100
# R_ref_mesuree_ohm: 99.7
# ... (14 cles au total)
f_Hz,V_dipole_V,V_Rref_V,dt_s,module_Z_ohm,phase_deg,u_module_alea_ohm,u_phase_deg
10,0.145651214,2.35589022,0.00840446206,6.18242786,30.2560634,0.122405827,1.5
```

### 2.1 Les huit colonnes obligatoires

| Colonne | Unité | Contenu | Origine |
|---|---|---|---|
| `f_Hz` | Hz | fréquence **lue à l'oscilloscope**, avec toute sa résolution — pas la consigne du GBF | mesure |
| `V_dipole_V` | V | amplitude voie 1 (aux bornes du dipôle) | mesure |
| `V_Rref_V` | V | amplitude voie 2 (aux bornes de l'étalon) | mesure |
| `dt_s` | s | Δt = t(V_Rref) − t(V_dipole), deux passages par zéro **montants** successifs, **avec son signe** | mesure |
| `module_Z_ohm` | Ω | \|Z\| = R_ref · V_d / V_R | **recalculé** |
| `phase_deg` | ° | φ = 360 · f · Δt ; **φ > 0 = charge inductive** | **recalculé** |
| `u_module_alea_ohm` | Ω | incertitude-type **aléatoire** (k = 1), point par point → poids `1/u²` de l'ajustement | calculé |
| `u_phase_deg` | ° | incertitude-type (k = 1) | calculé |

Toute colonne **supplémentaire** est acceptée et conservée : en montage A ou B,
ajouter `V_tot_V`, et — recommandé par le § 02.12 — le **nombre de divisions
occupées** et le **calibre** de chaque voie, sans quoi l'incertitude de gain
n'est pas reconstructible après coup.

### 2.2 Pourquoi les lectures brutes ET les grandeurs dérivées

Si l'on découvre après coup que `R_ref` valait 99,2 Ω et non 99,7, ou qu'une
sonde était en ×10, **la série entière reste exploitable** : on rejoue
`io_mesures.depouiller()`. Un fichier qui ne porterait que \|Z\| n'est pas une
mesure, c'est un dessin. Un test de non-régression impose que les colonnes
dérivées se recalculent depuis les colonnes brutes.

### 2.3 Pourquoi l'incertitude est scindée en deux

Le bruit de lecture est **aléatoire** et varie d'un point à l'autre : il va dans
la colonne `u_module_alea_ohm`. La tolérance de `R_ref` et l'étalonnage de
chaîne sont **systématiques** — ils multiplient *tous* les \|Z\| de la série :
ils vont dans l'en-tête (`u_R_ref_relative_pct`, `u_systematique_relative_pct`)
et s'appliquent **après** l'ajustement, en propagation sur les paramètres
(§ 03.5). Les mélanger fausse le χ², biaise Rₑ et sous-estime les barres
d'erreur des paramètres de Thiele-Small.

### 2.4 Les quatorze métadonnées obligatoires

`version_format`, `date`, `dipole`, `montage`, `R_ref_nominale_ohm`,
`R_ref_mesuree_ohm`, `u_R_ref_relative_pct`, `u_systematique_relative_pct`,
`niveau_Vd_RMS_V`, `temperature_C`, `operateur`, `appareil`,
`Re_DC_avant_ohm`, `Re_DC_apres_ohm`.

Elles sont **refusées si absentes** (`io_mesures.verifier_metadonnees`) : sans
elles, une courbe d'impédance n'est pas reproductible. L'écart `Re_DC` avant /
après mesure le seul échauffement, et c'est lui qui alimente l'étude de dérive
thermique de la phase 4.

---

## 3. Utilisation depuis Python

```python
import io_mesures as E                       # depuis le dossier analyse/

d, meta = E.lire_mesure('mesures/2026-10-05_sub_caisse_Rref100.csv')
erreurs, avertissements = E.valider_mesure(d, meta)

d = E.depouiller(d, meta)                    # rejouer |Z| et phi (R_ref corrigé)
E.ecrire_mesure('mesures/2026-10-05_sub_caisse_Rref100.csv', d, meta)

print(E.diagnostiquer_caisse(d['f_Hz'], d['module_Z_ohm'])['modele'])
print(E.diagnostiquer_grille(d['f_Hz'], d['module_Z_ohm'])['n_points_pic'])
```

`valider_mesure` rend **deux listes**. Les *erreurs* (colonne absente, NaN,
fréquences non croissantes, incertitude ≤ 0, tension ≤ 0, métadonnée manquante)
disqualifient le fichier ; les *avertissements* le laissent lisible mais
signalent : colonnes dérivées incohérentes, grille trop lâche au pic, **deux
pics détectés**, fichier synthétique.

### 3.1 Le diagnostic « deux pics » n'est pas cosmétique

`diagnostiquer_caisse` compte les pics de \|Z\| :

- **un pic** → caisse **close**, modèle de Thiele-Small à **5 paramètres** ;
- **deux pics** encadrant un creux → **bass-reflex** (f_L < f_b < f_H est un
  résultat démontré, § 01.10), et il faut **8 paramètres**.

Ajuster un modèle à 5 paramètres sur une courbe à deux pics **converge** et
donne des valeurs **fausses, sans message d'erreur** : c'est exactement le genre
de piège que le jury cherche. Le type de caisse du sub est la décision **D8**
de `DECISIONS-PHASE-0.md` : un **constat** à faire en phase 1, pas un choix.

---

## 4. Formats importés

### 4.1 Export texte REW — `lire_rew(chemin)`

En-tête préfixée par `*`, puis trois colonnes fréquence / module / phase. Le
séparateur dépend de la version et des réglages régionaux : il est
**auto-détecté** (`,` `;` tabulation, espaces), et la virgule décimale n'est
convertie que si le séparateur de colonnes n'est pas la virgule.
**[[à vérifier sur un export réel]]** — séparateur exact, unité de la colonne 2
(ohm et non dB SPL), convention de signe de la phase.

REW donne des centaines de points **sans incertitude** : on leur *affecte*
l'incertitude de chaîne issue des calibrations, jamais une valeur inventée.
Un import REW **n'est pas** convertible en fichier maison — il n'a pas de
lectures brutes. Il se range dans `rew/` et sert de **vérification
indépendante** de la série à l'oscilloscope.

### 4.2 CSV d'oscilloscope — `lire_scope(chemin)` puis `depouiller_scope(...)`

Convention imposée : **CH1 = V_dipole, CH2 = V_Rref**.
**[[format du modèle du lycée à relever]]** — le lecteur est tolérant (en-tête
quelconque, séparateur auto-détecté, temps reconstruit depuis un `Increment` si
l'appareil n'exporte pas de colonne de temps) et consigne ses hypothèses dans
`meta`.

Le dépouillement se fait par **détection synchrone**, pas au curseur :

| Estimateur | Fenêtre de 10 périodes | Fenêtre de 10,37 périodes |
|---|---|---|
| DFT brute | +0,03 % | **+2,1 %** |
| DFT tronquée à N périodes entières | +0,04 % | +0,03 % |
| **Moindres carrés (`lstsq`, défaut)** | +0,03 % | +0,03 % |

*(valeurs produites par l'auto-test de `io_mesures.py` sur une acquisition
simulée avec bruit et offset ; ordres de grandeur conformes au § 09.3)*

La projection sur un seul point de DFT n'est exacte que si la fenêtre contient
un **nombre entier de périodes** ; sinon la fuite spectrale biaise le résultat
et l'offset continu ne se projette plus à zéro. Une erreur de quelques pour
cent sur \|Z\| ruine l'ajustement de l'acte 2 — **et ne se signale pas**. D'où
le défaut `methode='lstsq'`, valable pour une fenêtre quelconque, qui absorbe
l'offset au passage.

---

## 5. Le fichier `exemple_synthetique_sub.csv`

**DONNÉES SYNTHÉTIQUES — aucune mesure de l'enceinte du projet.** Il est
engendré par `python analyse/io_mesures.py --exemple` à partir du modèle de
Thiele-Small à 5 paramètres de `modele_hp`, avec des paramètres **typiques de
datasheet** (§ 01.13) : Rₑ = 5,4 Ω, Lₑ = 1,9 mH, R_es = 100 Ω, f_s = 55 Hz,
Q_ms = 6,1. Bruit gaussien de 1,4 % par voie, **graine fixée** (un tirage non
reproductible n'est pas un résultat).

Il sert à éprouver toute la chaîne — lecture, validation, ajustement,
optimisation, figures — **avant** la première séance de banc. Aucun chiffre
qui en sort n'est citable comme résultat, et `valider_mesure` le rappelle par
un avertissement à chaque lecture.

---

## 6. Avant de quitter la salle de TP

1. `R_ref` **mesurée** au multimètre (REL), et la température notée.
2. Tableau des κ d'appariement CH1/CH2 **par couple de calibres**.
3. Pour chaque point : fréquence avec toute sa résolution, calibres, nombre de
   divisions occupées, niveau GBF, les deux amplitudes, Δt **avec son signe**.
4. **Type A** : 5 répétitions complètes d'un point de plateau et d'un point de
   pic — c'est la seule source honnête de l'incertitude aléatoire.
5. `Re` DC au multimètre **avant et après**.
6. Trois contrôles de cohérence immédiats : \|Z\|(f_min) > R_e,DC ; φ = 0 au
   sommet du pic ; \|Z\| et φ décroissants vers R_e quand f baisse.
   (Le contrôle v1 « \|Z\| → R_e à 10 Hz » est **faux** : la branche
   motionnelle n'est pas éteinte une octave et demie sous la résonance.)
7. Exporter les acquisitions brutes dans `scope/` **avant** de débrancher.
