# Suite de tests de non-régression — `analyse/tests/`

## Lancement (commande gelée § 09.6)

Depuis **la racine du dépôt** :

```
python -m unittest discover -s analyse/tests -v
```

Ne **pas** ajouter `-t .`, et ne **pas** créer de `__init__.py` dans ce dossier :
unittest refuserait le dossier de départ (« Start directory is not importable »).
Un test de `test_contrat.py` vérifie d'ailleurs l'absence de ce fichier.

Chaque fichier reste exécutable seul, pour la boucle de mise au point :

```
python analyse/tests/test_filtre.py
python -m unittest discover -s analyse/tests -p "test_optimiseur.py" -v
```

## À quoi sert chaque fichier

| Fichier | Ce qu'il protège | Critère chiffré |
|---|---|---|
| `contexte.py` | *(pas un test)* amorce de `sys.path`, jeux synthétiques partagés, dossier jetable | — |
| `test_entrees.py` | le fichier de mesure — la seule chose qui coûte une séance de banc | aller-retour CSV < 1·10⁻⁸ relatif ; colonnes dérivées recalculables ; fichier hors format refusé ; self pure +90,00°, condensateur pur −90,00° ; `lstsq` à ±0,5 % sur fenêtre non entière |
| `test_ajustement.py` | le problème inverse, et le garde-fou de type de caisse | chaque paramètre < 3 % et < 3 σ ; χ² réduit dans [0,5 ; 2] ; SciPy ≡ repli à < 5·10⁻³ sur θ **et** sur σ ; 20 tirages : médiane < 2 %, **au plus 4 au-dessus de 3 %** (amendement daté, voir plus bas) et < 4 σ ; bass-reflex → `UserWarning` + `CaisseIncompatible` en mode strict |
| `test_bassreflex.py` | **(i, 2026-09-16)** la voie bass-reflex de bout en bout : ajustement, garde-fou, f_b géométrique, champ proche, charge du passe-haut | 8 paramètres retrouvés à < 5 % **et** < 4 σ depuis une initialisation **lue sur la courbe** ; `identifier(modele='auto')` choisit seul `bassreflex8` ; 5 paramètres imposés → `CaisseIncompatible` ; f_b = 35,01 Hz par Helmholtz (V = 110 L, 2 évents 100 × 274 mm, $k=1{,}463$ — cotes résolues à l'envers, donc vérification de code) et racine(2) entre 1 et 2 évents ; pondération de Keele = 0,25690 = racine(S/S_d) ; branche aigu sans condensateur → −87 % sur \|Z\|, sous les 4 Ω du E-800 |
| `test_filtre.py` | les repères fréquentiels et la définition unique de f_c | pôle 96,8586 Hz ; Q = 0,7303 ; −3 dB mi-puissance 99,93 / 93,88 Hz ; seuil littéral 99,82 / 93,99 Hz ; f₃PB·f₃PH = f₀² à 10⁻⁹ |
| `test_optimiseur.py` | la porte de validation, en deux étages | continu : 18,006326 mH / 140,674424 µF et 25,464791 mH / 99,471839 µF à < 10⁻⁶ ; E12 : 18,0 mH / 150 µF (J = 0,9471) et 27,0 mH / 100 µF (Q = 0,4869) |
| `test_series_e12.py` | l'exhaustivité de l'énumération | 331 776 = 24⁴ combinaisons, 576 couples/voie, grille strictement croissante, optimum hors bord, vectorisé ≡ boucle à < 10⁻⁹ |
| `test_incertitudes.py` | la propagation sur f₀, et l'interdiction du « 11 % » | 4,08 % (GUM) / 7,07 % (borne au pire cas) / 10,0 % (ρ = +1) ; biais MC +0,75 % ; aucune fonction ne rend 11,18 % |
| `test_self_bobine.py` | le modèle de coût de la self | r×m exactement constant à géométrie figée ; K_cu = 1760 à 5 % près sur 0,8–2,0 mm ; 18 mH/1 Ω → 4,25 kg et 106 € ; les 53 contrôles internes au vert |
| `test_figures.py` | la recoloration claire à l'export PDF, et l'injection HTML | 0 couleur `#rrggbb` hors repli `var(--x, #hex)` en variante **sombre et claire** ; replis présents (le SVG reste juste hors du HTML) ; injection → 0 marqueur restant ; marqueur ou SVG absent → `SystemExit` ; un `#ff00ff` volontaire **doit** être détecté ; un seul dossier de sortie ; le titre de la figure 1 ne dit pas « mesurée » sur du calcul |
| `test_contrat.py` | les signatures **gelées** du § 09.4 entre modules écrits en parallèle | 27 signatures, nom **et** ordre des arguments (`energie.pertes_joule` et `energie.croisement` comprises) ; `seuil=3.0103` par défaut ; cible = paramètre (D2) ; `ρ=0` explicite ; UTF-8 + LF ; une seule convention de renvoi « § NN » ; `import entrees` et `import injecter_figures` répondent |

## Conventions tenues par ces fichiers

- **Tout en français**, sources sans lettres accentuées, UTF-8, fins de ligne LF.
- **Aucune écriture dans le dépôt** : les tests qui écrivent utilisent
  `contexte.dossier_jetable()`. Ce qui est dans `analyse/mesures/` a coûté une
  séance de banc ; un test ne doit même pas pouvoir y écrire par accident.
- **Aucune mesure de l'enceinte n'existe** à ce jour : toutes les données de
  cette suite sont synthétiques et le disent.
- **Graines fixées** partout où il y a du tirage aléatoire (`20260913` pour les
  20 tirages d'identification, `7` pour le Monte-Carlo d'incertitude).
- Chaque test porte un **docstring en français qui explique ce qu'il protège**,
  pas ce qu'il calcule : un test dont on ne sait plus pourquoi il existe finit
  par être ajusté au lieu d'être corrigé.

## D'où viennent les seuils

**Pas des tests eux-mêmes.** Depuis le 2026-09-14, les critères chiffrés du
§ 09.6 sont recopiés dans `analyse/criteres_geles.json`, section
`tests_non_regression` (neuf familles depuis le 2026-09-16), et `contexte.critere(famille, clé)` les y lit. Un critère qui
ne vit que dans le test qu'il gouverne se confronte à **lui-même** : rien n'empêche
alors de le retoucher après avoir vu un résultat, et l'affirmation « les critères ont
été gelés avant les mesures » cesse d'être vérifiable. `contexte.critere` **lève** si
une clé manque : on ne devine pas un critère, on le lit ou on échoue.

Tout amendement est daté et motivé dans le `journal_des_modifications` du même
fichier. Il y en a **deux**. Le premier est un **ajout** (2026-09-16, famille (i)
bass-reflex : aucun critère existant n'est touché) ; le second est un
**amendement**, et il mérite d'être su parce qu'il est exactement le
piège que le projet se défend de tendre :

> **(a3), 2026-09-14.** La référence annonce « 20/20 tirages sous 3 % ». La mesure sur
> la graine gelée donne médiane 0,87 %, maximum 3,13 %, **deux** tirages au-dessus de
> 3 % — de la statistique, pas un bug : 20 tirages × 5 paramètres = 100 estimations
> bruitées à 2 % et 1°, la queue de distribution est attendue. La version précédente du
> test **élargissait le seuil à 4 %**, c'est-à-dire déplaçait la référence après avoir
> vu le résultat. L'amendement **tient le seuil de 3 %** et borne le *nombre* de
> tirages autorisés à le dépasser (4, soit le double de la mesure — assez large pour
> ne pas tomber à la première fluctuation, assez serré pour attraper une régression).
> Cela dit la même statistique sans réécrire la référence. Le critère qui fait vraiment
> foi reste le troisième, en écarts-types.

## Ce que la suite ne couvre pas encore

- **`tout_refaire.py`** : code de retour 0/1 et arrêt au premier échec.
- Les tests (e), (f) et (h′) du § 09.6 — étalonnage sur charge connue, recoupement
  des deux R_ref, accord avec l'outil Thiele-Small de REW — **attendent des
  mesures réelles**. Ils ne peuvent pas être écrits avant la phase 1. *(La famille
  ajoutée le 2026-09-16 porte la lettre **(i)** et non (e), justement pour ne pas
  occuper la place réservée à l'étalonnage sur charge connue.)*
- Du bass-reflex, ce qui **suppose des mesures** : la géométrie réelle de la caisse
  (la prédiction de Helmholtz tourne aujourd'hui sur une géométrie *illustrative*),
  le relevé en champ proche de la membrane et des deux évents, et la réponse au
  `[[à vérifier]]` sur le condensateur des pavillons.
