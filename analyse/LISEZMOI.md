# `analyse/` — la chaîne de calcul du TIPE

> **Tout chiffre montré au jury est régénérable par une commande.** C'est le
> principe 3 de `REFERENCE-TECHNIQUE.md` § 09.1, et c'est la raison d'être de ce
> dossier. La commande, c'est celle-ci :
>
> ```
> python analyse/tout_refaire.py
> ```
>
> Une centaine de secondes plus tard, `analyse/resultats/` contient les deux JSON
> cités à l'oral, les figures, les netlists LTspice et un journal daté portant les
> versions, les graines et les empreintes SHA-256 des fichiers d'entrée.

> ### ⚠ Statut des données au 2026-09-16
>
> **Aucune mesure de l'enceinte n'existe.** La chaîne tourne aujourd'hui sur
> `mesures/exemple_synthetique_sub.csv`, engendré depuis le 2026-09-16 par un
> modèle **bass-reflex à deux évents** (8 paramètres) et **étiqueté SYNTHÉTIQUE
> dans son en-tête**. Cette étiquette est recopiée dans
> chaque résultat produit, jusque dans les JSON et sur les figures. Ce que la
> chaîne prouve aujourd'hui, c'est que **le code est juste** ; elle ne dit
> strictement **rien** du haut-parleur réel. Le jour de la phase 1, il suffit de
> déposer les vrais CSV dans `mesures/` : rien d'autre ne change.

> ### Ce qui a changé le 2026-09-16 — et ce qui n'a pas changé
>
> L'étudiant a constaté que le sub est en **caisse bass-reflex, avec deux
> évents**. Jusque-là, tous les documents disaient « type de caisse à
> documenter » et la chaîne s'exerçait sur un exemple en caisse **close**.
>
> **Ce qui n'a pas changé** : la problématique, le récit en quatre actes, les
> critères, la chaîne de mesure, l'optimisation E12, les portes de validation.
> Le modèle à 7–8 paramètres et le garde-fou de caisse étaient écrits et testés
> **précisément parce que** le type de caisse n'était pas connu : ce n'est pas
> une reprise, c'est une hypothèse qui se lève.
>
> **Ce qui a changé** : le fichier d'exemple est engendré en bass-reflex, donc
> la commande gelée exerce enfin le garde-fou et le modèle à 8 paramètres ; le
> budget d'incertitude de type B porte sur **huit** paramètres au lieu de cinq ;
> la netlist LTspice décrit la **branche évent** au lieu d'une caisse close qui
> lui ressemblerait ; et trois fonctions nouvelles sont arrivées — prédiction de
> f_b par la **géométrie** (Helmholtz), **sommation en champ proche** (Keele),
> et la **charge composite du passe-haut** (les pavillons d'ultra-aigu, hors
> bande acoustique mais bel et bien en parallèle des médiums).
>
> **Et l'argument du TIPE s'en trouve renforcé** : en bass-reflex, le **second
> pic d'impédance tombe en pleine zone de raccord** — 85,9 Hz et 64 Ω sur le
> modèle illustratif, d'où \|Z\|(100 Hz) = 22,4 Ω au lieu des 8 Ω supposés par
> le calcul de catalogue. L'hypothèse « 8 Ω résistifs » y est donc encore plus
> fausse qu'en caisse close ; sur cette charge, le filtre catalogue est
> **disqualifié** avant toute comparaison de fidélité (min\|Z_in\| = 3,29 Ω,
> sous le minimum de 4 Ω du t.amp E-800).

---

## 1. En une commande

| Ce que tu veux | Commande (depuis **la racine du dépôt**) |
|---|---|
| Tout rejouer, chiffres de l'oral | `python analyse/tout_refaire.py` |
| Boucle de mise au point (rapide) | `python analyse/tout_refaire.py --rapide --sans-figures` |
| Les tests seuls | `python -m unittest discover -s analyse/tests -v` |
| Un module seul (auto-test intégré) | `python analyse/optim.py`, `python analyse/filtre.py`, … |
| Les figures seules | `python analyse/figures.py --resultats` |
| Repartir d'une machine neuve | `python -m pip install --user -r analyse/requirements.txt` |

`tout_refaire.py` rend **0** si tout passe, **1** au premier échec, avec le nom de
l'étape sur `stderr`. C'est ce qui permet de l'appeler depuis un script sans lire
sa sortie.

### Le livrable papier est en **deux parties**, et la règle est écrite ici

Ce dossier fait **plus de 16 000 lignes**. À 55 lignes par page cela représente
environ **300 pages**, soit **600 en double exemplaire** : matériellement
indéposable en annexe, et hors de portée de l'oral — aucun jury n'ouvre 300 pages
en 15 minutes, et Thomas ne peut pas soutenir 500 fonctions. Une annexe illisible
produit l'effet inverse de celui recherché : elle donne l'impression d'un travail
non maîtrisé. La règle est donc fixée **maintenant**, pas la veille du dépôt.

**(1) Le noyau imprimé — 10 à 15 pages.** Exactement les fonctions que le récit
cite, et sur lesquelles Thomas doit pouvoir être interrogé au tableau :

| Fonction | Acte | Ce qu'elle prouve |
|---|---|---|
| `modele_hp.Z_ts` | 1 | le modèle à 5 paramètres, en quatre lignes |
| `ts_fit.residus_ts` + `ajuster_ts` + `moindres_carres_lm` | 2 | le problème inverse, et le Levenberg-Marquardt écrit à la main |
| `filtre.H_pb` / `H_ph` / `cible` | 3 | les réseaux **sur charge complexe**, sans approximation |
| `optim.cout` (le cœur, hors arguments de cadrage) + `enumere_e12` | 3 | la fonction de coût et l'exhaustivité |
| `incertitudes.u_f0_relative` | transverse | le facteur ½, et pourquoi le 11 % de la v1 est hors sujet |

**(2) Tout le reste — sur le dépôt.** Annoncé par une **page de garde** qui donne
trois choses et rien d'autre :

```
Code d'analyse complet : https://github.com/thomasMareel/tipe-filtrage-enceinte
                         dossier analyse/ , commit <hash court>
Régénération intégrale : python analyse/tout_refaire.py
Empreinte du journal   : SHA-256 de analyse/resultats/journal.txt
                         <empreinte>
```

L'empreinte se lit dans `resultats/journal.txt`, que `tout_refaire.py` date et
signe à chaque exécution. Elle transforme « le code est sur le dépôt » en une
affirmation **vérifiable**, ce qui est tout l'objet du principe 3.

---

## 2. Un module = une étape du récit

Le dossier est organisé comme l'exposé : mesurer → identifier → optimiser →
valider. Chaque module porte en tête une docstring qui explique **la physique**,
pas seulement l'API, et renvoie aux sections de `REFERENCE-TECHNIQUE.md`.

| Module | Acte | À quoi il sert |
|---|---|---|
| `modele_hp.py` | 1 | Modèle électroacoustique du haut-parleur : `Z_ts` (5 paramètres, caisse close), `Z_bassreflex` (7–8 paramètres, deux pics), `Z_charge_passe_haut` (**charge composite** : médiums en série *et* pavillons en parallèle), grilles de fréquences, Zobel, diagnostic du **nombre de pics**. Depuis le 2026-09-16, la section 4 sort de l'impédance et traite la **caisse bass-reflex** : `frequence_accord_helmholtz` (f_b prédite par la géométrie, N évents, correction de bout explicite) et `somme_champ_proche_bassreflex` (méthode de **Keele**, pondération en racine des aires). Porte aussi les jeux de valeurs **typiques** `SUB_TYP` / `SUB_TYP_BR` / `MED_TYP`, chacun avec son avertissement « ordre de grandeur, pas une mesure ». |
| `io_mesures.py` | 1 | Entrées/sorties : lecture et écriture du CSV de mesure (en-tête `# clé: valeur`), dépouillement $Z = R_{ref}V_d/V_R$, lecture des exports **REW** et des CSV **d'oscilloscope**, détection synchrone, validation d'une série, lecture de `criteres_geles.json`, et génération du jeu d'exemple **SYNTHÉTIQUE** (bass-reflex à deux évents depuis le 2026-09-16). *(Renommé : la spécification § 09.2 l'appelle `entrees.py`, et `analyse/entrees.py` est un alias qui redirige ici — voir ci-dessous.)* |
| `ts_fit.py` | 2 | **Problème inverse** : initialisation lue sur la courbe, résidus pondérés, ajustement (SciPy ou repli Levenberg-Marquardt maison), covariance complète, Monte-Carlo, jackknife, diagnostics de résidus, aiguillage automatique clos / bass-reflex et **refus** d'ajuster 5 paramètres sur une courbe à deux pics. |
| `filtre.py` | 3 | Réseaux $H_{PB}$, $H_{PH}$ **sur charge complexe**, cibles (`butterworth`, `lr2`, `plate`), sommation avec polarité et retard, repères à $-3$ dB (convention en paramètre), fréquence de **croisement**, écart RMS en dB, contraintes physiques (tension, courant, $\min|Z_{in}|$), export de **netlist LTspice**. |
| `optim.py` | 3 | Séries E12/E6, fonction de coût $J$ vectorisée par blocs, **énumération exhaustive** des 331 776 combinaisons, recoupement continu, analyse du **plateau**, Monte-Carlo des tolérances, et les **portes de validation 8 Ω** pour les deux cibles. |
| `self_bobine.py` | satellite | Wheeler, bobine de Brooks, DCR, masse de cuivre, prix, perte d'insertion, échauffement. Alimente le terme « euros » et le terme « pertes » de $J$. |
| `incertitudes.py` | transverse | Propagation GUM (analytique et Monte-Carlo), corrélations, budget d'incertitude des paramètres T-S, la formule $u(f_0)/f_0$ **avec son facteur ½**. |
| `blueprint_mpl.py` | figures | Identité visuelle Blueprint pour matplotlib : palettes sombre et claire lues sur `css/blueprint.css`, export SVG à **variables CSS avec repli**, gabarits 4/3. |
| `energie.py` | satellite | **Sobriété** : pertes Joule du passif évaluées **spectralement sur $Z(f)$** (et non sur 8 Ω), consommation au repos de l'actif, et **point de croisement énergétique** $P^\star$ (§ 06.8). C'est le seul satellite qui porte l'argument du thème national. |
| `figures.py` | figures | Les sept figures du dossier, plus `injecter_figures()` qui inline un SVG à la place d'un marqueur `<!--FIG:nom-->`. |
| `tout_refaire.py` | — | **L'orchestrateur.** Il n'y a aucune physique dedans : il enchaîne les huit étapes, vérifie, journalise, et s'arrête au premier échec. |

**Les noms de modules de la spécification § 09.2 répondent tous à un `import`**, y
compris les deux qui ont été renommés à l'écriture. Le nom de module fait partie du
contrat gelé, contre lequel d'autres modules sont écrits en parallèle : un
`import entrees` qui échoue casse du code, même si les signatures internes sont
respectées à la lettre. Deux alias le rétablissent **sans dupliquer une ligne** :

| Nom du contrat (§ 09.2) | Nom du fichier qui fait foi | Pourquoi le renommage |
|---|---|---|
| `entrees.py` | `io_mesures.py` | le module lit **et** écrit ; et `entrees` est un mot trop commun pour ne pas entrer en collision un jour |
| `injecter_figures.py` | `figures.py` | l'injection a besoin du registre `figures.FIGURES` — un nom de figure **est** le nom de son marqueur HTML. Deux fichiers auraient signifié deux listes, donc un jour deux listes divergentes |

Un test (`tests/test_contrat.py`) vérifie l'**identité** des objets exposés par
l'alias et par le module réel, et pas seulement leur existence : deux
implémentations d'un même lecteur de CSV divergeraient tôt ou tard.

---

## 3. Ce qui n'est pas un module

| Chemin | Rôle |
|---|---|
| `criteres_geles.json` | **Les décisions gelées sont un fichier, pas une intention.** Cibles, poids de $J$, bande, niveaux d'écoute, définition de $f_c$. Tant qu'une valeur porte la marque `[[a geler]]`, le code **refuse** de s'en servir pour un chiffre d'oral. Au 2026-09-14, **42 décisions sont encore ouvertes** — voir `DECISIONS-PHASE-0.md`. Le fichier porte aussi, depuis le 2026-09-14, la section **`tests_non_regression`** : les critères chiffrés du § 09.6 y sont recopiés et **lus par les tests** (`tests/contexte.py`), au lieu de ne vivre que dans leurs docstrings — sans quoi une relecture ne peut confronter un test qu'à lui-même. Le **`journal_des_modifications`** date et motive tout amendement. |
| `mesures/` | **Données brutes, lecture seule, versionnées.** Rien dans la chaîne ne les réécrit. Voir `mesures/LISEZMOI.md`. |
| `resultats/` | **Sorties régénérables**, ignorées par git — *sauf* `parametres_ts.json` et `design_optimise.json`, qui sont les chiffres cités à l'oral et portent donc leur provenance. C'est **le seul** dossier de sortie : `figures.py` lancé seul y écrit comme `tout_refaire.py`. Il y avait auparavant un second dossier `analyse/figures/`, que la règle `.gitignore` du § 09.8 ne couvrait pas — un `git add analyse` y aurait versionné des figures **périmées**, indiscernables des figures à jour une fois dans le dépôt, puis citées à l'oral. |
| `tests/` | Les **neuf** familles de tests de non-régression : les huit du § 09.6 (la famille (h) *figures* comprise) et la famille **(i) bass-reflex**, ajoutée le 2026-09-16. Voir `tests/LISEZMOI.md`. |
| `requirements.txt` | numpy, scipy, matplotlib — et les versions qui ont produit les chiffres. |

---

## 4. Les tests

```
python -m unittest discover -s analyse/tests -v
```

**Depuis la racine du dépôt**, sans `-t .`, et sans créer de `__init__.py` dans
`tests/` (unittest refuserait le dossier de départ). État au 2026-09-16 :
**171 tests, tous au vert, en une cinquantaine de secondes** — dont la famille (h)
*figures*, qui n'était jusqu'ici jouée qu'à l'étape 8 de `tout_refaire.py`, donc
**sautée par `--sans-figures`** et jamais exécutée par la commande gelée. Ce n'était
pas un test de non-régression, c'était un contrôle d'exécution ; il l'est maintenant.

Les **21 derniers** sont la famille **(i) `test_bassreflex.py`**, ajoutée le
2026-09-16. Elle tient la voie bass-reflex **de bout en bout** : la voie existait
dans le code, elle n'était éprouvée qu'à moitié — l'ajustement à 8 paramètres y
partait des valeurs *vraies*, ce qui ne prouve rien du chemin réel. Elle part
maintenant de la **courbe**, par `init_depuis_courbe` puis par
`identifier(modele='auto')`, exactement comme le fera la phase 1.

Chaque test porte un **critère chiffré** gelé en même temps que la fonction de
coût. Les principaux, tous vérifiés par la dernière exécution :

| Contrôle | Valeur attendue | Obtenue |
|---|---|---|
| Porte 8 Ω, continu, Butterworth | 18,00633 mH / 140,6744 µF à $10^{-6}$ près | écart $10^{-15}$ |
| Porte 8 Ω, continu, Linkwitz-Riley 2 | 25,46479 mH / 99,4718 µF | écart $2\cdot10^{-15}$ |
| Porte 8 Ω, E12, Butterworth | 18 mH / 150 µF, $J = 0{,}947$ | identique |
| Porte 8 Ω, E12, LR2 | 27 mH / 100 µF, $Q = 0{,}487$ | identique |
| Pôle du couple catalogue | $f_0 = 96{,}86$ Hz | 96,86 Hz |
| $u(f_0)/f_0$, convention GUM ($u = a/\sqrt3$) | **4,08 %** | 4,08 % (Monte-Carlo : 4,10 %) |
| $u(f_0)/f_0$, borne au pire cas | **7,07 %** | 7,07 % |
| $u(f_0)/f_0$, même lot ($\rho = +1$) | 10,00 % | 10,00 % |
| Énumération E12 | $24^4 = 331\,776$ combinaisons, sans doublon | identique |
| Ajustement sur l'exemple synthétique | $\chi^2$ réduit dans $[0{,}5\,;2]$ | 0,974 (modèle `bassreflex8`) |
| Bass-reflex, 8 paramètres retrouvés | $< 5\,\%$ et $< 4\sigma$ chacun | max 2,3 % sur le CSV d'exemple (chaîne complète) |
| $f_b$ : géométrie (Helmholtz) contre ajustement | écart $< 5\,\%$ | 35,01 Hz contre 35,04 Hz — *cotes d'évent résolues à l'envers sur ce jeu de test : vérification de code, pas résultat* |
| Garde-fou : 5 paramètres sur deux pics | `UserWarning`, puis `CaisseIncompatible` en mode strict | conforme |
| SVG produits (sombre **et** claire) | 0 couleur `#rrggbb` hors repli `var(--x, #hex)` | 0 |
| Injection HTML | chaque marqueur `<!--FIG:nom-->` encadre son SVG (injection **idempotente**), et échec **bruyant** si un marqueur manque | conforme |

**Les seuils ci-dessus sont lus dans `criteres_geles.json`**, section
`tests_non_regression`, et non écrits en dur dans les tests. Un critère qui ne vit
que dans le test qu'il gouverne se confronte à lui-même : rien n'empêche alors de le
retoucher après avoir vu le résultat, et l'honnêteté du sujet s'effondre. Tout
amendement est daté et motivé dans le `journal_des_modifications` du même fichier —
il y en a un, le critère (a3), et il est instructif : **le seuil de 3 % a été tenu**,
c'est le *nombre* de tirages autorisés à le dépasser qui a été borné, parce
qu'élargir la barre à 4 % après avoir vu un tirage à 3,13 % aurait été déplacer la
référence.

Le **11 %** de la v1 ne doit jamais réapparaître : c'est la formule d'un RC du
premier ordre (sans le facteur ½), abandonné en v2. Un test le vérifie
explicitement.

---

## 5. `tout_refaire.py` — ce qu'il fait, dans l'ordre

L'ordre n'est pas décoratif : **les tests d'abord**, parce que si un test tombe,
aucun chiffre n'est plus garanti et il ne faut pas produire de JSON.

| # | Étape | Ce qu'elle écrit |
|---|---|---|
| 1 | Tests de non-régression (sous-processus, interpréteur propre) | — |
| 2 | Décisions gelées, **recopiées intégralement au journal** | — |
| 3 | Inventaire de `mesures/` : SHA-256, validation de chaque série | — |
| 4 | **Portes de validation 8 Ω**, pour les **deux** cibles (décision D2) | — |
| 5 | Acte 2 : identification de Thiele-Small | `resultats/parametres_ts.json` |
| 6 | Acte 3 : énumération E12 **avec et sans DCR**, comparaison des **trois cibles**, plateau, contraintes, netlists | `resultats/design_optimise.json`, `filtre_optimise.cir`, `filtre_catalogue.cir` |
| 7 | Incertitudes : tolérances **et** covariance du fit | `resultats/incertitudes.json` |
| 8 | Figures Blueprint (sombre + claire) et essai d'injection | `resultats/figures/*.svg`, `*.png` |
| — | Journal | `resultats/journal.txt` |

**Options** (interface gelée § 09.8) :

- `--rapide` — Monte-Carlo à 20 000 tirages au lieu de 400 000, ajustement
  allégé. **Pour la mise au point uniquement** : le journal l'écrit en tête, et
  aucun chiffre d'une exécution `--rapide` ne doit être cité à l'oral.
- `--sans-figures` — saute la seule étape qui demande matplotlib.

**Chaque étape vérifie l'existence de sa sortie amont** et échoue en nommant
l'étape fautive, plutôt que de recalculer en silence ce qui manque.

### Trois choses que l'étape 6 dit, et qu'il faut savoir lire

**(a) Les selfs ne sont pas parfaites, et ce n'est pas un détail.** L'énumération
tournait, jusqu'au 2026-09-14, sans modèle de DCR : elle cherchait donc l'optimum
d'un problème où $r_1 = r_2 = 0$, pendant que le même journal chiffrait dix lignes
plus bas « self L₁ : DCR 1,85 Ω ». La DCR n'agit pas seulement par le terme de pertes
$w_W$ (nul ici) : **elle entre dans $H_{PB}$ et $H_{PH}$**, elle amortit la résonance
de la cellule grave et abaisse le niveau de la voie — donc elle pèse dans les termes
*somme* et *voies*, ceux qui valent 1. La chaîne produit maintenant **les deux
énumérations** (selfs idéales / bobine de Brooks) et écrit l'écart : **c'est lui, le
résultat**, et c'est la question de jury la plus prévisible sur ce sujet. D6 n'étant
pas gelée, on ne choisit pas à la place de Thomas — on chiffre.

**(b) Un optimum sur un bord de grille n'est pas un optimum, c'est une contrainte.**
Quand `optimum_interieur` est faux, le mot **CANDIDAT** et la mention **HORS
DOMAINE** remontent jusqu'au récapitulatif, jusqu'au titre de l'étape 7, jusqu'à la
clé `hors_domaine` du JSON et jusqu'à `stderr`. Le diagnostic existait déjà, mais
enterré trente lignes plus haut : or le seul chiffre affiché au terminal est celui
qui sera recopié, cité et retenu.

**(c) Les pavillons d'ultra-aigu sont dans la charge, même s'ils ne rayonnent
rien à 100 Hz.** Ils sont câblés **en parallèle** du bloc médium : hors périmètre
*acoustique*, dans le périmètre *électrique*. Le $Z_m$ de l'étape 6 les ignore
encore — il le faut bien, on ne sait pas s'il y a un condensateur en série avec
eux — mais **taire l'enjeu serait pire que le chiffrer**, alors le journal le
chiffre : sur les ordres de grandeur étiquetés, \|Z\| du bloc à 100 Hz passe de
29,3 Ω à 23,7 Ω (−19 %) **avec** un condensateur de 6,8 µF, et à 3,7 Ω (−87 %)
**sans** — sous le minimum de 4 Ω du t.amp E-800. `[[à vérifier]]` reste ouvert ;
la conséquence de manip, elle, ne dépend pas de la réponse : on mesure le bloc
médium **pavillons connectés**, puisque c'est cela que le filtre voit.

**L'injection de figures est en service** (vérifié le 2026-09-16 ; le paragraphe
qui l'annonçait « pas encore faite » datait d'avant la refonte v2 des deux decks).
`presentation-finale.html` porte **7 couples** de marqueurs `<!--FIG:nom-->` /
`<!--/FIG:nom-->` — `fig-z-sub-mesure`, `fig-fit-ts-sub`,
`fig-catalogue-8ohm-vs-z`, `fig-somme-catalogue-vs-optimise`,
`fig-plateau-optimum`, `fig-self-cout-dcr`, `fig-croisement-energie` — et
`pre-soutenance.html` en porte **2** (`fig-z-sub-mesure`,
`fig-catalogue-8ohm-vs-z`). Les deux decks sont au gabarit SCEI 4/3
(`Reveal.initialize({width: 1024, height: 768})`).

**Mise en garde, déjà écrite dans l'en-tête de `pre-soutenance.html` :**
l'injection **réécrit le HTML en place**. On travaille donc sur une copie, ou on
vérifie que le dépôt est propre avant de lancer l'étape. Le mécanisme reste par
ailleurs **éprouvé à chaque exécution** sur un HTML temporaire : c'est le défaut
précis de `_gen.py` (annoncer « OK injecté » sans rien injecter) que ce contrôle
interdit.

---

## 6. Le format des CSV de mesure

Détail complet : `mesures/LISEZMOI.md` et `REFERENCE-TECHNIQUE.md` § 09.3. En
résumé : une ligne de titre, puis **une métadonnée par ligne** au format
`# clé: valeur`, puis la ligne de noms de colonnes, puis les points.

```
# TIPE filtrage enceinte -- mesure d impedance
# version_format: 1
# date: 2026-10-12T14:32
# dipole: sub 18 pouces en caisse
# montage: C (GBF flottant, 2 lectures directes)
# R_ref_nominale_ohm: 100
# R_ref_mesuree_ohm: 99.7
# u_R_ref_relative_pct: 1.0
# u_systematique_relative_pct: 1.2
#   ... (15 clés au total : niveau, température, opérateur, appareil, Re_DC avant/après…)
f_Hz,V_dipole_V,V_Rref_V,dt_s,module_Z_ohm,phase_deg,u_module_alea_ohm,u_phase_deg
10,0.0947589735,0.669779873,0.00115906419,10.0771346,41.7263108,0.201542691,1.5
```

| Colonne | Unité | Contenu | Origine |
|---|---|---|---|
| `f_Hz` | Hz | fréquence **lue à l'oscilloscope**, pas la consigne du GBF | mesure |
| `V_dipole_V`, `V_Rref_V` | V | amplitudes des deux voies (calibres en en-tête) | mesure |
| `dt_s` | s | décalage $\Delta t = t(V_{R_{ref}}) - t(V_{dipole})$, sur deux passages par zéro **montants** | mesure |
| `module_Z_ohm` | Ω | $\lvert Z\rvert = R_{ref}\,V_d/V_R$ | **recalculé** |
| `phase_deg` | ° | $\varphi = 360\,f\,\Delta t$ — avec cette convention, $\varphi > 0$ pour une charge **inductive** | **recalculé** |
| `u_module_alea_ohm` | Ω | incertitude-type **aléatoire** ($k=1$), point par point → poids $1/u^2$ de l'ajustement | calculé |
| `u_phase_deg` | ° | incertitude-type sur la phase, $k=1$ | calculé |

Trois règles qui ont des conséquences :

1. **Le fichier porte les lectures brutes** *et* les grandeurs dérivées. Si l'on
   découvre après coup que $R_{ref}$ valait 99,2 Ω et non 99,7, la série entière
   reste exploitable : on rejoue `depouiller()`. Un test impose que les colonnes
   dérivées soient recalculables à partir des brutes.
2. **L'incertitude est scindée.** Le bruit de lecture est *aléatoire* et varie
   d'un point à l'autre (colonnes `u_*`) ; $u(R_{ref})$ et l'étalonnage de chaîne
   sont *systématiques* et multiplient **tous** les $\lvert Z\rvert$ de la série —
   ils vivent dans l'en-tête et s'appliquent **après** l'ajustement. Les
   mélanger fausse le $\chi^2$, biaise $R_e$ et sous-estime les barres d'erreur.
3. **Métadonnées obligatoires.** Un fichier sans `version_format`, sans
   `R_ref_mesuree_ohm` ou sans date est **refusé**, pas lu à moitié. Sans ses
   conditions, une courbe d'impédance n'est pas une mesure, c'est un dessin.

Deux formats sont importés tels quels : les exports **REW**
(`lire_rew`, séparateur auto-détecté) et les CSV **d'oscilloscope**
(`lire_scope` + `depouiller_scope`). Pour ces derniers, ne pas pointer $\Delta t$
au curseur : la détection synchrone par **moindres carrés** donne amplitude et
phase en une passe, sur une fenêtre quelconque. La projection DFT naïve, elle,
se trompe de **5 %** si la fenêtre ne contient pas un nombre entier de périodes —
et elle se trompe **sans le dire**.

---

## 7. Ce qui est synthétique, et ce qui ne l'est pas

| Origine | Exemples | Comment c'est signalé |
|---|---|---|
| **Aucune mesure de l'enceinte** | — | Il n'y en a pas. Aucune. |
| **Synthétique** (engendré par un modèle) | `mesures/exemple_synthetique_sub.csv` et tout ce qui en descend : `parametres_ts.json`, `design_optimise.json`, les figures | En-tête du CSV, clé `statut_donnees` recopiée dans chaque JSON, mention portée sur les figures, bandeau en tête du journal |
| **Ordre de grandeur étiqueté** (datasheet publique) | `modele_hp.SUB_TYP` (B&C 18PS76), `MED_TYP` (FaitalPRO 8FE200-4) | Clé `avertissement` dans le dictionnaire, contrôlée par un test |
| **Placeholder assumé** (modèle à choisir) | prix du cuivre, modèle de DCR, poids de $J$ | Décisions D5 et D6 encore `[[a geler]]` ; tant qu'elles le sont, $w_{euro} = w_W = 0$ et **aucun euro n'entre dans le classement** |
| **Constat, ni mesure ni choix** | le sub est en **bass-reflex à deux évents** (2026-09-16) ; les pavillons d'ultra-aigu sont **en parallèle des médiums** | Décision **D8** de `DECISIONS-PHASE-0.md` : un constat se fait à l'œil, il ne se choisit pas. Ses **nombres** (α, f_b, Q_l, volume, cotes des évents) restent `[[à mesurer]]` |
| **Question ouverte, pas hypothèse** | y a-t-il un condensateur en série avec les pavillons ? | `[[à vérifier]]` dans `Z_charge_passe_haut` ; `effet_branche_aigu` chiffre les **deux** cas au lieu d'en supposer un |
| **Calculé, donc vrai** | portes 8 Ω, $u(f_0)/f_0$, 331 776 combinaisons, $f_b$ de Helmholtz | Ce sont des théorèmes ou de l'arithmétique, pas des mesures. $f_b$ géométrique est un **modèle** : il est fait pour être **contredit** par l'ajustement, pas pour le remplacer |

Tant que D5 n'est pas gelée, la chaîne optimise sur un critère **purement
acoustique**, sans modèle de prix ni de DCR. C'est le réglage le plus
**défavorable au design optimisé** : la comparaison avec le filtre catalogue
n'est donc pas truquée en sa faveur.

---

## 8. Ce code sera **imprimé en double** et annexé au PDF de l'oral

C'est une contrainte de rédaction, pas une remarque de confort. Le jury lira ces
pages **sur papier**, sans exécuter quoi que ce soit, et sans pouvoir chercher.
D'où les conventions que tout ajout doit respecter :

- **Un en-tête de module qui tient seul.** La docstring de tête dit ce que le
  module calcule, **pourquoi la physique impose de le calculer ainsi**, et renvoie
  aux sections de `REFERENCE-TECHNIQUE.md` (« voir § 04.5 »). Un lecteur qui
  ouvre la page 7 de l'annexe doit savoir où il est.
- **Tout en français**, y compris les noms de fonctions et de variables — mais
  **sans lettres accentuées dans les huit modules du contrat**, et sans aucun
  caractère hors cp1252 dans le code exécutable : un `Ω` passé à `print()` fait
  tomber la chaîne sur une console Windows. Les étiquettes d'axes de `figures.py`
  et `blueprint_mpl.py` sont exemptées (matplotlib les rend, il ne les imprime
  pas), et deux tests tiennent ces règles.
- **UTF-8, fins de ligne LF**, partout, testé.
- **Lisible par un élève de prépa** : pas d'astuce numpy pour l'astuce, pas de
  ligne de 200 caractères, pas d'abréviation obscure. Le cœur physique de chaque
  module tient en quelques lignes, et c'est voulu — c'est ce qui se montre.
- **Les commentaires disent *pourquoi*, jamais *quoi*.** « On tronque à $N$
  périodes entières, sinon la fuite spectrale biaise le module de 5 % » vaut dix
  lignes de paraphrase.
- **Le détail vit en annexe, l'oral dure 15 minutes.** Ce qui se dit à l'oral, ce
  sont les portes de validation, le plateau de l'optimum et la convention
  d'incertitude ; le reste est là pour être feuilleté et pour résister aux
  questions.

- **Une seule convention de renvoi : « § NN »**, jamais « section NN ». Le signe
  s'encode en cp1252, il est plus court, et le mot *paragraphe* étant masculin les
  articles retombent juste (« du § 03.7 », « au § 09.4 »). Un remplacement mécanique
  en sens inverse avait laissé 27 fautes d'accord du type « du section 03.7 » ; un
  test tient désormais la règle.
- **Une seule convention de nommage dans les résultats** : les grandeurs en décibels
  portent le suffixe `_dB`, les tensions et les courants gardent leur nom électrique.
  La clé `V_grave` valait des **décibels** à côté de `V_C1_crete` qui vaut des
  **volts** : elle s'appelle maintenant `voie_grave_dB`.
- **Un seul sens pour le mot « gelé ».** `optim.W_SANITY` (ex-`W_GELE`) désigne les
  poids **fixes du sanity check** du § 04.7, celui qui rend $J = 0{,}947$ ; la
  décision **D5** du projet, elle, est encore ouverte. Deux sens du même mot dans un
  dossier dont l'argument d'honnêteté est « les critères ont été gelés avant les
  mesures », c'est la contradiction la plus facile à exploiter par un jury — et elle
  était imprimée sur une figure.

**Ce qui s'imprime, et ce qui ne s'imprime pas : voir la règle du § 1**, « Le livrable
papier est en deux parties ». Ordre de grandeur : **16 400 lignes** au total, dont
13 300 de modules et 3 100 de tests. Tout imprimer serait illisible ; le noyau
imprimé fait 10 à 15 pages, le reste se cite par la page de garde (URL, commande de
régénération, SHA-256 du journal).

---

## 9. Ce qui reste à écrire

- **Ce qui vient d'être écrit** (2026-09-16, après le constat « bass-reflex à deux
  évents ») : `modele_hp.frequence_accord_helmholtz` (f_b prédite par la géométrie),
  `modele_hp.somme_champ_proche_bassreflex` (méthode de Keele, N évents),
  `modele_hp.Z_charge_passe_haut` et `effet_branche_aigu` (les pavillons dans la
  charge du passe-haut), la famille de tests **(e) `test_bassreflex.py`**, et
  l'exemple synthétique passé en bass-reflex. Trois corrections que ce passage a
  fait apparaître, toutes réelles et aucune cosmétique : le budget d'incertitude de
  type B s'arrêtait au modèle à 5 paramètres (la chaîne tombait sur
  `iteration over a 0-d array` à l'étape 7) ; la netlist LTspice décrivait une caisse
  **close** en prétendant décrire la charge identifiée ; et l'auto-test de
  `figures.py` exigeait « 0 marqueur restant » après une injection **idempotente**
  qui, par construction, conserve ses marqueurs — un contrôle qui ne pouvait donc
  jamais passer.
- **Ce qui reste à faire quand les vrais nombres seront là** : la géométrie de la
  caisse (volume et cotes des deux évents) relevée au mètre-ruban, pour que la
  prédiction de f_b par Helmholtz cesse d'être illustrative ; la réponse au
  `[[à vérifier]]` sur le condensateur des pavillons ; et le relevé en **champ
  proche** de la membrane *et* de chaque évent, seule entrée de la sommation de
  Keele. Le code les attend, aucun n'existe.
- **Ce qui avait été écrit le 2026-09-14** (après relecture) et qui manquait :
  `energie.py` et sa figure `fig-croisement-energie` ; la famille de tests (h)
  *figures* ; la section `tests_non_regression` de `criteres_geles.json` ; les alias
  de module `entrees.py` et `injecter_figures.py`. Le couplage **DCR → énumération**,
  surtout, qui faisait du satellite « self optimale » une annexe décorative alors que
  le § 09.4 en fait une pièce du récit.
- `mesures/composants.csv` et `optim.optimiser_sur_stock` **sur des valeurs
  mesurées** : un condensateur ±20 % acheté à 150 µF en fait 163, et
  l'optimisation vraiment sobre consiste à **trier et apparier le stock** plutôt
  qu'à racheter. Bénéfice collatéral : mesurés à 1 %, $L$ et $C$ font tomber
  $u(f_0)/f_0$ **sous 1 %**, contre 4,1 % sur les tolérances catalogue.
- Les tests qui n'existeront que le jour où des mesures existeront : étalonnage
  sur composants connus à ±3 %, recoupement des deux $R_{ref}$, accord à moins de
  5 % entre l'ajustement maison et l'outil Thiele-Small de REW.
- La lecture de **deux jeux de mesures par configuration** (les deux niveaux
  d'écoute gelés), sans quoi le critère de robustesse restera un tableau rempli à
  la main.
- **Le regroupement des arguments de cadrage de `optim.cout`.** Les 12 premiers sont
  ceux gelés au § 09.4, dans l'ordre : le contrat est tenu. Les 26 suivants, tous
  optionnels et tous documentés, font néanmoins une fonction qu'on ne lit pas d'un
  trait — et « montrez-moi votre fonction de coût » est une question de jury
  certaine. Le regroupement dans un objet de réglages **n'a pas été fait ici**, et
  volontairement : c'est une modification d'interface, elle touche tous les appelants
  — y compris des modules écrits en parallèle contre le même contrat — et elle ne
  corrige aucune erreur. À faire d'un seul geste, avec les tests, avant la phase 3.
  En attendant, l'entrée en matière reste simple : un appel typique ne passe que
  `cout(p1, p2, f, Zs, Zm)`, tout le reste a une valeur par défaut.
- **La largeur des lignes**, ramenée à 88 colonnes. Environ 225 lignes dépassent 90
  colonnes aujourd'hui, ce qui force soit le repli, soit une police trop petite sur un
  PDF 4/3. À reprendre au moment de préparer le noyau imprimé, pas avant : un
  reformatage massif du code juste avant une échéance est le meilleur moyen d'y
  introduire une faute que les tests ne verront pas.
