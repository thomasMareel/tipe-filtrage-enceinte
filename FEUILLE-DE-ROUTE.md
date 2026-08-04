# Feuille de route — TIPE v2 (pivot du 2026-08-04)

> Sujet v2 : **optimisation sous contraintes du filtre de raccord à 100 Hz sur la
> charge réelle Z(f) des haut-parleurs**. La v1 (« passif ou actif ? ») est gelée
> dans `archive-v1/` et survit ici comme référentiel de comparaison.

## Problématique

> « Comment concevoir le filtre de raccord à 100 Hz d'une enceinte deux voies
> pour qu'il tienne sa cible sur la charge réelle — un haut-parleur dont
> l'impédance varie du simple au sextuple — au moindre coût en composants,
> en pertes et en matière ? »

## Le récit en quatre actes

1. **Mesurer** — relever Z(f) (module et phase) du subwoofer en caisse et du
   bloc médiums, avec incertitudes.
2. **Identifier** — remonter de Z(f) aux paramètres du modèle de Thiele-Small
   par ajustement aux moindres carrés (**problème inverse**).
3. **Optimiser** — concevoir le filtre par **optimisation numérique sous
   contraintes** (valeurs normalisées E12, coût, pertes) sur la charge modélisée,
   au lieu des formules catalogues valables seulement sur 8 Ω résistif.
4. **Valider** — comparer au banc puis au micro : filtre « catalogue » vs filtre
   optimisé vs référence active, selon des critères **gelés avant les mesures**.

## Satellites (intégrés, pas digressions)

- **Self optimale (Wheeler / bobine de Brooks)** : fournit le modèle
  coût–masse–DCR ↔ L injecté dans la fonction de coût de l'acte 3, et la self
  réellement bobinée de l'acte 4. Détails en annexe des slides.
- **Croisement énergétique** : consommation au repos de la chaîne active
  (bi-amplification) vs pertes proportionnelles du passif → niveau d'écoute où
  l'un devient plus sobre que l'autre. Argument « sobriété » original.
- **Référence active (Sallen-Key)** : placée avant l'ampli, elle ne voit jamais
  Z(f) — c'est l'étalon « immunisé » contre le problème étudié. Valeurs corrigées
  conservées de la v1 : sub R = 10 kΩ, C₁ = 220 nF / C₂ = 110 nF ; médiums
  R'₁ = 11 kΩ, R'₂ = 22 kΩ, C = 100 nF.

## Critères de comparaison (proposition v0 — à GELER en phase 0, avant toute mesure)

| Critère | Définition | Mesure |
|---|---|---|
| Fidélité du raccord | Écart RMS (dB) de la somme des deux voies à la cible plate, bande 40–250 Hz | Micro + REW, protocole champ proche fixé en phase 1 |
| Précision de f_c | \|f_c réalisée − 100 Hz\| | Bode électrique puis acoustique |
| Pertes d'insertion | dB et W perdus en bande passante à puissance donnée | V/I au banc, DCR |
| Consommation au repos | W de la chaîne complète sans signal | Wattmètre de prise |
| Coût marginal | € de composants, ampli existant considéré acquis | Factures |
| Coût système | € du système complet équivalent (scénario stéréo) | Devis |
| Encombrement / matière | Masse (kg) et volume (L) du filtre, cuivre utilisé | Balance, mètre |
| Robustesse | Dérive de f_c et de l'écart RMS entre niveau faible et niveau fort | Mesures aux 2 niveaux gelés |

Les deux niveaux d'écoute de référence (faible / fort) sont à fixer en phase 0
et à ne plus changer. **Aucun critère ne doit être ajouté ou retiré après les
premières mesures comparatives** — c'est ce qui rend la conclusion honnête.

## Phases

### Phase 0 — Cadrage (août 2026) — EN COURS

- [x] Archiver la v1 (`archive-v1/`, tag git `v1-sujet-passif-actif`).
- [x] Feuille de route (ce document), MCOT v2, CLAUDE.md v2.
- [ ] Geler les critères ci-dessus + les 2 niveaux d'écoute (décision étudiant).
- [ ] Liste d'achats phase 1 (voir ci-dessous) ; vérifier le matériel du lycée.
- [ ] Squelette du code d'analyse Python (`analyse/` : mesure → fit → optimisation).

**Porte de validation** : critères datés et signés avant la première mesure comparative.

### Phase 1 — La clé de voûte : chaîne de mesure d'impédance (sept. 2026)

Tout le sujet repose sur la capacité à mesurer Z(f) proprement. On ne passe pas
à la suite tant que cette capacité n'est pas démontrée.

- Montage (méthode validée par la critique prof de mai) : GBF → résistance étalon
  R_ref → dipôle testé ; on mesure **V_dipôle ET V_Rref** (2 voies oscillo) →
  \|Z\| = R_ref·(V_dipôle/V_Rref), phase par décalage temporel. Pas d'hypothèse
  « courant constant ».
- Variante rapide : jig d'impédance sur carte son + REW (balayage automatique).
  Les deux méthodes doivent se recouper.
- **Étalonnage sur composants CONNUS d'abord** : une résistance de puissance
  (courbe plate attendue), un condensateur connu (\|Z\| = 1/ωC, phase −90°).
  → incertitudes de la chaîne chiffrées.
- Puis : Z(f) du sub **en caisse** (10–500 Hz, resserré autour du pic) et du bloc
  médiums. Rappel v1 : F_c en caisse > F_s datasheet, c'est normal, ce n'est pas
  une erreur.

**Livrables** : courbes Z(f) module+phase avec barres d'erreur ; f_s en caisse.
**Porte de validation** : la résistance étalon est retrouvée à ±3 % et le
condensateur suit 1/ωC sur deux décades. Sinon on diagnostique avant d'avancer.
**Repli** : si la carte son pose problème (couplage, impédance de sortie),
GBF + oscillo point par point au 1/12 d'octave — lent mais infaillible.
**Achats** : R_ref 100 Ω 1 % (+ une 10 Ω), pinces/câbles, résistance de
puissance 8 Ω si absente au lycée, wattmètre de prise (~20 €).

### Phase 2 — Problème inverse : identification Thiele-Small (oct. 2026)

- Modèle : Z(jω) = R_e + jωL_e + branche motionnelle (RLC parallèle équivalent).
- Ajustement moindres carrés (scipy) sur module ET phase ; analyse des résidus ;
  incertitudes des paramètres (covariance, Monte-Carlo sur les barres d'erreur).
- Confrontation aux ordres de grandeur datasheet ; explication du décalage en caisse.

**Livrables** : paramètres identifiés ± incertitudes ; courbe mesure vs modèle.
**Porte de validation** : résidu relatif faible sur 20–300 Hz ET paramètres
stables quand on retire aléatoirement des points de mesure.
**Repli** : si le fit bute en haut de bande (courants de Foucault), restreindre
la bande utile au raccord ou mentionner le modèle de semi-inductance en perspective.

### Phase 3 — Optimisation numérique du filtre (nov.–déc. 2026)

- Cible : somme des deux voies plate (gain et phase cohérente), bande 40–250 Hz.
- Variables : L₁, C₁ (passe-bas), C₂, L₂ (passe-haut), option réseau de Zobel (R, C).
- Contraintes : valeurs des séries E12/E6 réelles, budget, DCR(L) issu de
  l'étude self (satellite intégré ici), encombrement.
- Fonction de coût : écart RMS à la cible + pénalités coût/pertes (pondérations
  affichées et discutées — c'est le « cahier des charges » chiffré).
- Méthode : l'espace discret E12 est énumérable → recherche exhaustive (robuste),
  recoupée par un optimiseur continu arrondi ensuite. LTspice en contre-vérification.
- Étude self en parallèle : formules de Wheeler, redécouverte numérique de la
  bobine de Brooks, choix du fil (loi r×m ≈ constante à L fixée).

**Livrables** : design optimisé + courbes prédites catalogue vs optimisé sur Z(f)
réelle ; modèle de coût de la self ; plan de bobinage.
**Porte de validation (sanity check clé)** : alimenté avec une charge 8 Ω
résistive pure, l'optimiseur doit retomber sur le Butterworth catalogue.
S'il n'y retombe pas, il y a un bug — ne rien acheter avant ce test.

### Phase 4 — Fabrication et validation expérimentale (déc. 2026 – fév. 2027)

- Bobiner la/les selfs ; mesurer L (résonance série avec C connu : avec 150 µF,
  pic attendu vers 97 Hz au GBF+oscillo) et DCR ; écart au modèle expliqué.
- Assembler filtre catalogue ET filtre optimisé ; monter la référence active
  Sallen-Key (valeurs ci-dessus) sur alimentation symétrique.
- Ordre des tests, chacun conditionnant le suivant :
  1. électrique sur résistance de puissance 8 Ω (f_c, pente, pertes) ;
  2. électrique sur HP réel (l'écart attendu apparaît) ;
  3. acoustique REW en champ proche (20–500 Hz), voie par voie ;
  4. somme des deux voies au raccord — **avec inversion de polarité d'une voie**
     (2ⁿᵈ ordre : sans inversion → trou, avec → bosse +3 dB).
- Robustesse : refaire la mesure du raccord aux 2 niveaux gelés (dérive thermique).
- Énergie : consommation au repos actif vs pertes passif → point de croisement.

**Livrables** : toutes les courbes de la présentation finale ; tableau brut des critères.
**Porte de validation** : f_c électrique sur résistance conforme à la prédiction
à ±5 % avant de passer à l'acoustique.
**Pièges connus (hérités v1)** : modes de pièce à 100 Hz (λ ≈ 3,4 m) → champ
proche ; égalisation des niveaux entre voies ; petites amplitudes d'abord.

### Phase 5 — Analyse, supports, échéances SCEI (fév. – juin 2027)

- Tableau comparatif final selon les critères gelés ; incertitudes propagées ;
  conclusion honnête (y compris si le passif optimisé ne rattrape pas l'actif :
  la limite identifiée est un résultat).
- Refonte des livrables en v2 : presentation-finale.html, accueil, NOTES-TIPE.md,
  PDF ; répétitions oral (~10 min).
- **MCOT définitif** à saisir sur SCEI — fenêtre exacte à vérifier sur
  scei-concours.fr (historiquement déc.–févr.). Le MCOT se rédige comme
  objectifs/démarche : ne pas y promettre de résultats.
- **DOT** (déroulé opérationnel) en fin d'année — date à vérifier également.

## Calendrier synthétique

| Période | Phase | Jalon |
|---|---|---|
| Août 2026 | 0 — Cadrage | Critères gelés, achats listés |
| Sept. 2026 | 1 — Mesure Z(f) | Chaîne validée sur composants connus |
| Oct. 2026 | 2 — Problème inverse | Paramètres T-S ± incertitudes |
| Nov.–déc. 2026 | 3 — Optimisation | Design validé par le sanity check 8 Ω |
| Déc. 2026 – févr. 2027 | 4 — Fabrication/mesures | Courbes finales, tableau brut |
| Févr.– juin 2027 | 5 — Analyse/supports | Slides v2, MCOT, DOT, répétitions |

## Par où commencer (réponse courte)

**Par la phase 1, et rien d'autre.** La totalité du sujet repose sur une seule
capacité expérimentale : mesurer Z(f) avec des incertitudes maîtrisées. C'est
pour cela qu'on l'étalonne d'abord sur des composants connus — si la chaîne
retrouve une résistance et un condensateur, elle saura mesurer un haut-parleur.
Réussir ces deux manips dérisque ~80 % du projet ; les rater tout de suite
coûterait une semaine au lieu d'un semestre. Premier geste concret : acheter la
R_ref 1 % et monter le jig.

## Gestion des risques transverses

- **Temps** : si retard en phase 4, couper d'abord le satellite « croisement
  énergétique » (1 mesure, réintégrable). La self reste : elle alimente le
  modèle de coût.
- **Budget** (≤ 500 €) : selfs bobinées maison (~25 €/pièce), condensateurs
  électrolytiques bipolaires (film réservé à la version finale si budget OK).
- **Scope oral 10 min** : le détail (self, Monte-Carlo, énergie) vit en annexes,
  appelées pendant les questions.
- **Pas d'invention de résultats** : tout chiffre non mesuré reste un placeholder
  explicite, comme en v1.
