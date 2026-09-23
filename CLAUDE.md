# CLAUDE.md — Mémoire de projet (TIPE filtrage enceinte)

Ce fichier est la mémoire entre sessions. À relire en début de session et à
tenir à jour à la fin de chaque session de travail.

> ⚠️ PIVOT DE SUJET v2 — décision étudiant du 2026-08-04 (FAIT FOI).
> L'étudiant jugeait la v1 (« passif ou actif ? ») trop « recette » pour le
> niveau prépa (« il me faut un filtre → j'ai fait un filtre »). Le sujet est
> recentré sur l'**optimisation sur charge réelle**. Le plan opérationnel
> complet est dans **FEUILLE-DE-ROUTE.md** (référence unique pour les phases).
> La v1 est gelée dans `archive-v1/` (autonome, avec son propre CLAUDE.md et
> tout l'historique de travail) + tag git `v1-sujet-passif-actif`.

## Sujet (v2)

- **Auteur** : Thomas Mareel, 2e année de prépa (PTSI → 2e année), TIPE session 2027.
- **Professeur encadrant : M. Chevalier** — accord obtenu, rapporté par Thomas le
  16/09/2026 (D10 de `DECISIONS-PHASE-0.md`). Reste à vérifier son compte sur
  `lycees.scei-concours.fr` et à le prévenir de la fenêtre de validation de
  **8 jours** de mi-juin 2027 (étape 3 SCEI, note zéro possible sans elle).
- **Thème national** : Sobriété, efficacité, optimisation.
- **Enceinte deux voies (DIY)** : 1 subwoofer **8 Ω 18″** + 2 médium-aigu
  **4 Ω câblés en série (= 8 Ω)**. Raccord cible : **100 Hz**.
- **Caisse du sub : BASS-REFLEX, à DEUX ÉVENTS** — constaté par l'étudiant le
  **16/09/2026**. Ce n'est plus une inconnue : la décision D8 de
  `DECISIONS-PHASE-0.md` est **répondue**. Restent à relever : dimensions des
  deux évents (diamètre, longueur) et volume interne $V_b$ `[[à mesurer]]`,
  fréquence d'accord $f_b$ `[[à mesurer]]` en phase 1 — lue au **passage par zéro
  de la phase** entre les deux pics, ou mieux prise de l'**ajustement**, et **pas** à
  l'argmin du creux du module, trop plat pour être localisé sous 1 % de bruit
  (REFERENCE-TECHNIQUE.md § 02.6 ; les deux lectures sont biaisées de quelques
  pour-cent par les pertes).
- **Composition réelle de l'enceinte** : le sub 18″, les 2 médiums en série, et
  **2 haut-parleurs d'ultra-aigu (pavillons) câblés EN PARALLÈLE des médiums**.
  Distinguer les deux plans : les pavillons sont **hors périmètre ACOUSTIQUE**
  (hors bande du raccord à 100 Hz, ils ne seront pas étudiés en rayonnement)
  mais ils sont **DANS la charge ÉLECTRIQUE** que voit le filtre passe-haut,
  puisqu'ils sont en parallèle des médiums. « Pavillons hors périmètre » sans
  cette distinction est faux.
- **Condensateur en série avec les pavillons** (protection classique du 1ᵉʳ
  ordre) : **CONFIRMÉ PRÉSENT** par l'étudiant le **16/09/2026**. Sa *valeur*
  reste `[[à mesurer]]`. Ce que le calcul en dit, pour 3,3 à 10 µF et les **deux**
  pavillons (`analyse/modele_hp.py::effet_branche_aigu`, `n_aigu = 2`) : chaque
  branche présente **160 à 480 Ω vers 100 Hz**, les deux en parallèle **80 à
  241 Ω**, et $|Z|$ du bloc médiums de modèle passe de **29,3 Ω à 26,3 – 21,7 Ω**
  à 100 Hz, soit **−10 à −26 %** (−19 % pour 6,8 µF) — **pas négligeable**, et
  visible sur un ajustement. Deux estimations antérieures étaient fausses :
  « effet négligeable » (le bloc est encore sur le flanc de sa résonance à
  100 Hz, son impédance y est haute), puis « 6 à 16 % » (calcul à **un seul**
  pavillon, sur un autre modèle du bloc).
  **Conséquence pratique** : on mesure le bloc médiums **tel qu'il est câblé,
  pavillons connectés** — c'est ce que le filtre voit, et l'effet est alors inclus
  sans avoir à le modéliser. **Côté sécurité** : à 100 Hz chaque pavillon voit
  ~482 Ω (3,3 µF) contre ~29 Ω pour le bloc, il ne reçoit qu'une fraction infime
  de la puissance — aucun risque pendant les balayages.

## Problématique (v2)

> « Comment concevoir le filtre de raccord à 100 Hz d'une enceinte deux voies
> pour qu'il tienne sa cible sur la charge réelle — un haut-parleur dont
> l'impédance varie fortement avec la fréquence — au moindre coût en composants,
> en pertes et en matière ? »

Le rapport $\max|Z|/\min|Z|$ **n'est pas encore connu** : c'est un livrable de la
phase 1 `[[à mesurer]]`. Tant qu'il n'est pas mesuré, la problématique ne porte
aucun chiffre (l'ancien « du simple au sextuple » était une estimation non
mesurée, et probablement basse : $Z_{pic} = R_e(1+Q_{ms}/Q_{es})$ donne 60 à
200 Ω pour un 18″ de catalogue). Il sera inséré ici une fois mesuré.

**Récit en 4 actes** : mesurer Z(f) → identifier Thiele-Small (problème
inverse, moindres carrés) → optimiser le filtre sous contraintes (E12, coût,
pertes DCR) → valider au banc et au micro contre des critères **gelés avant
les mesures**. Satellites intégrés : **self optimale** (Wheeler/Brooks, alimente
le modèle de coût), **croisement énergétique** (conso au repos de l'actif vs
pertes du passif), **référence active** (immunisée contre Z(f) par construction).

Détail des phases, portes de validation, critères et calendrier :
**FEUILLE-DE-ROUTE.md**. Ne pas dupliquer ici.

## Documents du dépôt (qui dit quoi)

- **CLAUDE.md** (ce fichier) — faits, conventions, état, mémoire entre sessions.
- **FEUILLE-DE-ROUTE.md** — **quoi** faire et **quand** : phases, portes de
  validation, critères à geler, calendrier et échéances SCEI.
- **REFERENCE-TECHNIQUE.md** — **comment** et **pourquoi** : modèles et
  démonstrations (Thiele-Small, filtres, self), montages de mesure, budgets
  d'incertitude, choix numériques, cadre SCEI (§ 08), sources. Document long, à
  consulter par sa table des matières au moment d'exécuter une phase ; aucune
  valeur n'y est une mesure du projet (marques `[[à mesurer]]`/`[[à vérifier]]`).
- **MCOT.md** — brouillon de la fiche MCOT v2 (limites de mots officielles).
- **NOTES-TIPE.md** — questions probables du jury et réponses préparées
  (réécrit en v2 le 13 sept. 2026 ; renvoie à REFERENCE-TECHNIQUE.md par « § NN.n »).
- **DECISIONS-PHASE-0.md** — le **registre daté** des décisions à geler (D1 à D10) :
  énoncé, options, conséquence de chaque option, date du gel. C'est lui qui
  empêche de changer un critère après avoir vu les courbes.
- **PARCOURS.md** — la liste **ordonnée** des actions de Thomas, de A à Z : ce
  qu'il fait, dans quel ordre, avec quoi. C'est le document de terrain.
- **analyse/LISEZMOI.md** — la chaîne de calcul (lecture des mesures →
  ajustement → optimisation → figures), ses garde-fous et sa commande gelée.
- **protocole/PROTOCOLE-EXPERIENCES.html** — le **livret de manipulations** (23
  manips, groupes A étalonnage, B impédances, C banc électrique, D acoustique et
  énergie ; 27 schémas de câblage ; page de sécurité à signer ; fiche de séance).
  **Relu de façon adversariale le 23/09/2026** (câblage et sécurité : 51 corrections
  toutes appliquées ; utilisabilité : 36 sur 38). C'est le HTML qui fait foi : le
  PDF se régénère depuis lui (`chrome --headless --print-to-pdf`, A4).
- **EXPORT-PDF.md** — procédure d'export PDF.

## Ce que la v1 lègue à la v2

- **Filtre passif « catalogue »** (point de départ à battre) : LC 2ⁿᵈ ordre
  Butterworth 100 Hz/8 Ω — PB sub : L₁=18 mH série + C₁=150 µF // ; PH médium :
  C₂=150 µF série + L₂=18 mH //. (C théorique ≈ 141 µF → 150 µF normalisé.)
- **Référence active Sallen-Key** (Q=1/√2), avant l'ampli, bi-amplification sur
  les 2 canaux du E-800. Valeurs corrigées : sub R=10 kΩ, C₁=220 nF/C₂=110 nF ;
  médiums R'₁=11 kΩ, R'₂=22 kΩ, C=100 nF. AOP NE5532 (ou TL072), alim ±15 V.
- L'archi « RC signal faible 1er ordre » de la v1 est **abandonnée** (le
  contre-exemple n'a plus de rôle dans le récit v2).
- Identité visuelle **Blueprint** (css/blueprint.css + blueprint-light.css),
  libs vendorées (hors-ligne), procédure PDF, photos de l'enceinte dans assets/.

## Matériel

- Pré-ampli **JB Systems SMX SX-801** (2 sorties identiques) — Zs à mesurer.
- Ampli **t.amp E-800** : 2×350 W/8 Ω, 2×500 W/4 Ω ; Zin 20 k sym / 10 k asym ;
  sensibilité 0,775 V / 1,4 V (sélectable). Deux canaux → bi-amp sans achat.
- Mesure lycée : GBF, oscillo numérique, multimètre. Perso : micro de mesure +
  interface **Focusrite Scarlett Solo 3ᵉ génération** (confirmée le 16 sept. 2026).
  Caractéristiques du manuel officiel (p. 18) et **ce qu'elles imposent** :
  - Sortie **ligne** : 4,61 V max mais **430 Ω d'impédance de sortie**. **Ne pas
    l'utiliser pour le jig** (REW la réserve à une R_sense de 1 kΩ, au prix du bruit).
  - Sortie **casque** : 1,73 V max, **< 1 Ω**. **C'est elle qui attaque le jig**, et
    avec R_sense = 100 Ω elle ne débite que quelques mA (≤ 4,5 mA en mesure) : aucun
    risque d'écrêtage. Le test à deux niveaux (12 dB d'écart) reste nécessaire, mais
    pour vérifier la **linéarité du haut-parleur**, plus celle de la sortie.
  - Entrée **micro** (XLR) : **3 kΩ**, 2,18 V max, symétrique ; Focusrite ne publie
    ni la structure de ses jambes de mode commun ni sa réjection.
  - Entrée **ligne** (jack TRS, position LINE) : 60 kΩ, 9,75 V max, symétrique.
  - **Câblage retenu (arbitrage du 23 sept. 2026)** : le montage **standard de REW**,
    avec **R_sense = 100 Ω à 0,1 %**, lu en 4 fils. Sortie casque, canal gauche : pointe
    → **33 Ω de protection** → nœud A ; R_sense de A à B ; haut-parleur de B à C ; corps
    du jack → C, **seul retour de masse du jig** ; bague non raccordée. **Entrée 1 (XLR)
    = voie de référence** : broche 2 → A, broche 3 → C, broche 1 non raccordée au jig.
    **Entrée 2 (jack TRS, LINE) = voie de mesure** : pointe → B, bague → C, corps non
    raccordé au jig. L'entrée micro lit un nœud piloté par la source : **ses 3 kΩ ne
    faussent rien**, quelle que soit sa structure interne. La seule charge du
    haut-parleur est l'entrée ligne : −0,11 % au pic de 64 Ω et −0,33 % à 200 Ω, que
    RINPUT = 60 kΩ et les étalonnages retirent. La soustraction logicielle amplifie une
    dérive de voie par |Z + R|/R = 1,64 au pic de 64 Ω (7,4 avec 10 Ω). **GAIN 1 au
    minimum ; GAIN 2 monté d'environ 13 dB** jusqu'à égalité des deux voies à 1 dB près,
    fils ouverts (REW abandonne l'étalonnage open au-delà de 2 dB), **puis bloqué** :
    0,01 dB de rotation coûte 0,19 % au pic. 48 V, AIR, INST et DIRECT MONITOR éteints ;
    **sorties ligne arrière débranchées** (même signal que le casque). REW : sortie
    gauche seule, entrée droite, étalonnages open, short puis reference sur **une seconde
    100 Ω à 0,1 %** ; validation sur la 10 Ω et le 100 µF, jamais sur la référence.
    Niveau (V_A = tension du nœud A, fils ouverts) : 0,30 V au premier balayage, puis
    environ 200 mV aux bornes au pic, soit V_A ≈ 0,62 V pour un pic de 64 Ω. Courant :
    ≤ 4,5 mA en mesure, ≤ 13,3 mA à pleine échelle même en court-circuit. **Le câblage
    du 16 sept. 2026 (micro aux bornes d'une R_ref de 10 Ω) était faux** : son calcul de
    charge ignorait les jambes de mode commun et la réjection, non publiées, de l'entrée
    XLR, et REW en abandonne l'étalonnage open (30 à 76 dB d'écart entre voies). La
    **10 Ω** devient le **dipôle de validation** (A2, A5) ; la chaîne GBF + oscillo garde
    sa R_ref de 100 Ω, désormais la même valeur que R_sense.
  - **Alimentation fantôme 48 V impérativement coupée** avant chaque branchement :
    active, elle injecte 48 V à travers ses résistances de polarisation dans le montage.
  - Réponse garantie **20 Hz – 20 kHz ±0,1 dB** ; **sous 20 Hz : non spécifiée** par le
    constructeur, alors que le premier pic d'impédance du bass-reflex peut y tomber
    → à caractériser en mesurant une résistance connue jusqu'à 10 Hz (manip A5 du livret).
  Protocole complet et schémas : `protocole/PROTOCOLE-EXPERIENCES.html`.
- Logiciels : **REW**, **LTspice**, **Python** (numpy/scipy/matplotlib).
  **Environnement local vérifié le 13 sept. 2026** : Python **3.13.2**,
  numpy **2.4.6**, scipy **1.18.1**, matplotlib **3.11.0** — `scipy` est
  installé et `scipy.optimize.least_squares` a été exécuté avec succès. Rien
  n'est donc à installer pour les phases 2 et 3. (Un repli en numpy pur —
  Gauss-Newton écrit à la main — reste intéressant *pédagogiquement*, pour
  montrer au jury ce que fait l'ajustement ; ce n'est pas une contrainte subie.)
- Budget composants : **≤ 500 €**.
- Enceinte fabriquée et fonctionnelle ; crossover actif réglable du commerce
  actuellement en service (= la référence active existe déjà en pratique).

## Données encore à confirmer par l'étudiant

- **Filière exacte de 2e année (PT ou PSI)** — PTSI mène aux deux. Elle commande
  le **premier positionnement thématique** à déclarer au MCOT et la **fenêtre
  d'oraux** (les banques n'interrogent pas les filières aux mêmes dates) : à
  trancher avant la saisie SCEI de mi-janvier 2027.
- **TIPE individuel ou en groupe** (le SCEI admet jusqu'à 3 candidats, avec une
  part personnelle identifiable pour chacun) : à déclarer dès l'étape 1.
- f_s réelle du sub et des médiums (→ phase 1, mesure d'impédance).
- Câblage exact des médiums (série confirmée ?).
- ~~Condensateur en série avec les pavillons ?~~ **CONFIRMÉ PRÉSENT** (Thomas,
  16 sept. 2026). Sa **valeur** reste `[[à mesurer]]` : pour 3,3 à 10 µF, les deux
  branches aiguës abaissent $|Z|$ du bloc médiums de **−10 à −26 %** à 100 Hz
  (calculé, voir § Sujet). Conséquence inchangée : on mesure le bloc **tel qu'il
  est câblé** ; aucun risque pour les pavillons pendant les balayages.
- **Dimensions des deux évents** (diamètre et longueur de chacun) et **volume
  interne de la caisse** $V_b$ `[[à mesurer]]` — ils permettent une prédiction
  falsifiable de $f_b$, à confronter au creux d'impédance mesuré.
- **Fréquence d'accord $f_b$** `[[à mesurer]]` (phase 1 : passage par zéro de la
  phase entre les deux pics de $|Z|$, ou valeur ajustée — pas l'argmin du creux)
  — elle commande la borne basse de sécurité au niveau fort.
- Sensibilités (dB/W/m) pour l'égalisation des niveaux.
- Les 2 niveaux d'écoute de référence à geler (le modèle de carte son est confirmé : voir § Matériel).

## Points scientifiques à NE PAS oublier (critique prof 2026-05-25, toujours valides)

- **2ⁿᵈ ordre Butterworth ⇒ inversion de polarité d'une voie OBLIGATOIRE**
  (sinon trou profond à fc ; avec inversion → bosse +3 dB).
- **Fs en caisse ≠ Fs datasheet** : Fc(clos) > Fs ; bass-reflex = deux pics.
  Mesurer le pic en caisse n'est pas une erreur.
- **La charge est bass-reflex (constat du 16/09/2026) : deux pics et un creux.**
  $|Z|$ présente deux maxima $f_L < f_b < f_H$ séparés par un **creux à
  $f \approx f_b$**, où $|Z|$ retombe près de $R_e$. **Le second pic $f_H$ tombe
  près de la zone de raccord** : à 100 Hz, l'hypothèse « 8 Ω résistifs » est
  **encore plus fausse** qu'en caisse close, et l'argument central du TIPE en
  sort renforcé, pas affaibli. Ordres de grandeur **modélisés** (paramètres
  plausibles pour un 18″ de sono — Re 5,4 Ω, fs 40 Hz, Qms 6,1, fb 35 Hz, Ql 7,
  α 3, ce qui suppose $V_{as} = 330$ L et $V_b = 110$ L — **aucune mesure sur
  l'enceinte**) : pics à **16,3 Hz (54 Ω)** et **85,9 Hz (64 Ω)**, creux à
  **34,2 Hz (6,1 Ω)**, $|Z|(100\ \mathrm{Hz}) = 22{,}4$ Ω à $-57{,}6°$. C'est
  **α, donc le volume de caisse, et non l'accord $f_b$** qui met le pic haut près
  du raccord : à $f_b$ fixé, α de 0,5 à 6 promène $f_H$ de 55 à 111 Hz, tandis
  qu'à α fixé descendre $f_b$ **abaisse les deux pics ensemble**
  (REFERENCE-TECHNIQUE.md § 01.10 — l'énoncé inverse, qui a circulé, est faux).
  Filtre catalogue 18 mH / 150 µF (DCR 1 Ω) **modélisé** sur ces charges : sur
  8 Ω résistif, réponse plate et $\min|Z_{in}| = 8{,}52$ Ω ; sur une **seconde
  charge modélisée, en caisse close** (jeu distinct : $f_s = 55$ Hz,
  $Q_{ms} = 6{,}1$ — ce n'est *pas* le même haut-parleur supposé clos), bosse de
  +12,2 dB et $\min|Z_{in}| = 2{,}49$ Ω ; sur la charge bass-reflex, bosse de
  +12,6 dB et $\min|Z_{in}| = 2{,}66$ Ω — sous le minimum de 4 Ω du t.amp E-800
  dans les deux cas de charge réelle.
  *Définition de la « bosse », sans laquelle le nombre est invérifiable* :
  maximum de $|H|$ du passe-bas sur 10–1000 Hz, **rapporté à la perte
  d'insertion de 1,02 dB** obtenue sur 8 Ω résistifs ($20\log_{10}(8/9)$).
  *Deux familles de chiffres coexistent, et c'est normal* : ceux-ci viennent d'un
  jeu de paramètres posé à la main avec DCR 1 Ω ; les diapositives
  ($\min|Z_{in}|$ = 3,29 Ω pour le catalogue, 5,27 Ω pour l'optimisé) viennent de
  la **chaîne complète** sur le CSV synthétique, avec les selfs de Brooks
  (r = 1,64 Ω). Deux ordres de grandeur indépendants, **pas** deux mesures du
  même nombre : ils ne se comparent pas terme à terme.
- **Un modèle à 5 paramètres ajusté sur des données bass-reflex converge EN
  SILENCE** sur des paramètres faux : aucun message d'erreur, seulement un
  résidu un peu moins bon — et toute la phase 3 serait alors optimisée sur une
  charge qui n'existe pas. Le modèle à **7-8 paramètres** était déjà écrit et
  testé *précisément parce que* le type de caisse n'était pas connu : ce n'est
  pas une reprise, c'est une hypothèse qui se lève. Garde-fou en place :
  `analyse/io_mesures.py::diagnostiquer_caisse()` détecte les deux pics et
  refuse un modèle à 5 paramètres avec un avertissement explicite ;
  `analyse/modele_hp.py` expose `Z_bassreflex`, `Z_bassreflex8` et
  `Z_bassreflex_semi`.
- **Sécurité bass-reflex : interdiction de balayer sous $f_b$ au niveau fort.**
  Sous l'accord, la membrane n'est plus chargée par les évents et l'excursion
  devient maximale — **risque mécanique** pour le 18″. Au niveau fort, borne
  basse du balayage $\ge 2f_b$ ; la descente sous $f_b$, nécessaire pour voir le
  premier pic, se fait **au niveau faible uniquement**, avec contrôle visuel du
  débattement avant chaque balayage.
- **Z exacte sans approximation courant constant** : mesurer V_HP ET V_Rref →
  Z = Rref·(V_HP/V_Rref). L'hypothèse I≈cst se dégrade au pic : |Z|_max = R_e(1+Q_ms/Q_es)
  vaut **60 à 200 Ω pour un 18″** de catalogue ; le « 40–60 Ω » hérité de la v1 ne vaut
  **ni** pour le 18″ **ni** pour le bloc médiums, dont le modèle culmine vers **112 Ω
  à 77 Hz** avec ses pavillons (calcul du 23/09/2026) → REFERENCE-TECHNIQUE.md § 02.4.
  **Incise obligatoire depuis le constat de caisse** : cette formule vaut **en
  champ libre et en caisse close**. En bass-reflex la résonance se **dédouble**
  et elle ne décrit **aucun** des deux pics — sur le modèle ci-dessus elle
  prédirait 105 Ω là où le calcul donne 54 et 64 Ω (−49 % et −40 %). On la garde
  comme **majorant** pour dimensionner R_ref (l'erreur va dans le sens
  conservatif au banc), jamais comme prédiction de la hauteur d'un pic.
- **DCR de la self** : pertes Joule + modifie l'amortissement du grave — en v2
  c'est un élément CENTRAL (fonction de coût + étude self, loi r×m ≈ cte à L fixée).
- **Mesure acoustique à 100 Hz** : modes de pièce (λ ≈ 3,4 m), fenêtrage
  inopérant en BF → champ proche.
- **Égalisation des niveaux** entre voies ; **tolérances** R ±5 %, C ±10–20 %,
  L ±10 % → propagation sur f_c (et argument pour l'énumération E12 en v2).
- **Scope oral : 15 min d'exposé + 15 min d'entretien** (format SCEI officiel ;
  l'ancien « 10 min » était une erreur v1). Le détail vit en annexes, appelées
  pendant les 15 min d'entretien.
- **Incertitude sur f_c d'un LC** : f_0 = 1/(2π√(LC)) ⇒
  u(f_0)/f_0 = ½·√((u_L/L)² + (u_C/C)²). Pour L et C à ±10 %, **toujours écrire
  le couple** : **7,1 % en borne au pire cas, 4,1 % en incertitude-type (loi
  rectangulaire, GUM)**. Jamais un nombre seul : la borne et l'incertitude-type
  ne se comparent pas aux mêmes seuils.
  Le « ±11 % » qui traîne dans les supports v1 est la formule du **RC 1er ordre
  abandonné** (u/f = √((u_R/R)² + (u_C/C)²)) : ne jamais la reprendre.
- **Définition officielle de f_c — UNIQUE dans tout le projet**
  (**REFERENCE-TECHNIQUE.md § 04.1 fait foi**) : f_c est la **fréquence de
  croisement des deux voies**, l'unique f de [40 ; 250] Hz telle que
  \|H_PB(f)·G_sub(f)\| = \|H_PH(f)·G_méd(f)\|. C'est la seule définition
  **insensible à la perte d'insertion** (une atténuation commune aux deux voies
  ne la déplace pas), la seule qui reste interprétable sur la charge réelle où
  \|Z\| culmine, et celle qui gouverne réellement la somme acoustique. Aucune
  autre ne doit être présentée comme « la définition retenue ».

## Nombres de contrôle (vérifiés)

- Butterworth 100 Hz/8 Ω : L = √2·R/(2πf) ≈ 18,0 mH ; C = 1/(√2·R·2πf) ≈ 141 µF.
- DCR 1 Ω **en série avec** 8 Ω → **11 % de la puissance dissipée dans la self**,
  soit **−0,51 dB en puissance** (part de la puissance délivrée qui atteint le HP,
  10·log₁₀(8/9)) **et −1,0 dB de niveau** (tension aux bornes du HP,
  20·log₁₀(8/9) = −1,02 dB) ; valable sur charge 8 Ω résistive. Les trois nombres
  décrivent la même chose sous trois conventions : ne pas les mélanger.
- Résonance série 18 mH + 150 µF ≈ 97 Hz (méthode de mesure de L au GBF).
- Incertitude LC : u(f_0)/f_0 = ½·√((u_L/L)² + (u_C/C)²) pour ±10 %/±10 % →
  **7,1 % en borne au pire cas, 4,1 % en incertitude-type** (loi rectangulaire,
  GUM). Le ½ vient de la racine carrée : f_0 ∝ (LC)^(−1/2).
- **Repères** pour 18 mH + 150 µF sur 8 Ω (Q = 0,730) — ce sont des repères,
  **pas** la définition de f_c (voir ci-dessus) :
  pôle f_0 = **96,86 Hz** ; −3 dB du passe-bas **99,93 Hz** et du passe-haut
  **93,88 Hz** en convention **demi-puissance (−3,0103 dB, celle de REW et des
  logiciels de mesure — convention retenue)**. Au seuil **littéral −3,000 dB**
  les mêmes points valent 99,82 et 93,99 Hz : les deux couples diffèrent par la
  **convention**, pas par un arrondi fautif. Contrôle : f_PB·f_PH = f_0² dans
  les deux cas. Toujours annoncer la convention avec le nombre.
- Sallen-Key : voir valeurs corrigées ci-dessus (fc ≈ 100 Hz, Q = 1/√2).
- Courbes _gen.py (modèle v1) : f_s modèle ≈ 40 Hz, Z(100 Hz) ≈ 14 Ω.

## Conventions du projet

- **Tout en français** : interface, commentaires, commits, notes.
- reveal.js + MathJax + polices **vendorés dans `libs/`** (hors-ligne, pas de
  CDN, pas de npm). Servir via `python -m http.server`.
- **Formules LaTeX** : `$...$` (en ligne) et `$$...$$` (bloc) dans les fichiers
  **.md** ; `\( \)` (en ligne) et `\[ \]` (bloc) dans les **.html** reveal.js
  (MathJax 3). Ne pas transposer une syntaxe dans l'autre format.
- **Pas d'invention de résultats** : tout chiffre non mesuré est un placeholder
  explicite (`<!-- TODO -->` ou bloc `.placeholder`).
- Sobriété visuelle (pas d'emoji, schémas SVG, identité Blueprint).
- Notes du présentateur dans `<aside class="notes">`, ~40 s par slide → 15 min
  d'exposé feraient ~22 vues à ce rythme, mais **viser 16 à 18 vues à 50-55 s**
  (recommandation REFERENCE-TECHNIQUE.md § 08.7 : le temps gagné sur la v1 sert
  à montrer les portes de validation, pas à ajouter des planches). Les annexes
  sont hors chronomètre : elles servent pendant les 15 min d'entretien.
- **Livrable SCEI = un PDF en 4/3 paysage de 5 Mo maximum**, téléversé et projeté
  depuis l'ordinateur du jury (ni HTML, ni notes, ni objets en salle). **Fait
  depuis la refonte v2** : les deux decks sont au gabarit **4/3 (1024×768)** —
  `Reveal.initialize({width: 1024, height: 768})` dans `presentation-finale.html`
  et `pre-soutenance.html` — et les figures matplotlib de `analyse/figures.py`
  sont produites au même format (détail : REFERENCE-TECHNIQUE.md § 08.2). Rien
  n'est donc à refaire de ce côté. Les PDF sont régénérés au 23/09/2026 (finale
  50 pages, **1,80 Mo** après allègement).
- Dépôt : https://github.com/thomasMareel/tipe-filtrage-enceinte
  Site : https://thomasmareel.github.io/tipe-filtrage-enceinte/
  Note : gh.exe est dans "C:\Program Files\GitHub CLI\" (pas dans le PATH).

## Procédure PDF (résumé — détail dans EXPORT-PDF.md)

PDF vectoriels via decktape (Chrome système, PUPPETEER_EXECUTABLE_PATH) sur
l'URL `…html?export` (retire le quadrillage) ; variante claire imprimable via
css/blueprint-light.css ; **puis toujours `python _alleger_pdf.py *.pdf`** —
sans cette étape la finale fait 5,2 Mo (glyphes Type 3 dupliqués vue par vue :
9 643 dessins pour 506 distincts), avec elle 1,80 Mo, rendu identique au pixel.
Piège connu : sans `text-rendering: geometricPrecision` sur le texte SVG
(`css/blueprint.css`), Chrome imprime le texte des SVG en colonnes à ~0,78 de sa
taille et de sa position — invisible à l'écran, flagrant dans le PDF. Toujours
**regarder** quelques pages du PDF sorti, pas seulement le HTML. Repli bitmap :
captures Chrome headless par slide + img2pdf (dossier _pdfbuild/ gitignoré).

## État actuel (2026-09-23)

- [x] **Constat du 16/09/2026 (étudiant) : la caisse du sub est BASS-REFLEX à
      DEUX ÉVENTS**, et 2 pavillons d'ultra-aigu sont câblés en parallèle des
      médiums. D8 de `DECISIONS-PHASE-0.md` est **répondue**. Répercuté ici
      (§ Sujet, § Données à confirmer, § Points scientifiques), dans
      `FEUILLE-DE-ROUTE.md` (phases 1, 2 et 4) et dans `DECISIONS-PHASE-0.md`
      (D3 et D8). **Rien d'autre ne change** : problématique, récit en 4 actes,
      critères, chaîne de mesure, optimisation E12 et portes de validation sont
      inchangés — le modèle à 7-8 paramètres était déjà écrit et testé pour ce
      cas. Propagé depuis dans `REFERENCE-TECHNIQUE.md`, `MCOT.md`,
      `NOTES-TIPE.md`, le code et les deux présentations (16/09/2026).
- [x] **Encadrant désigné : M. Chevalier** (16/09/2026, D10). Restent le contrôle
      de son compte SCEI et l'avertissement sur la fenêtre de mi-juin.
- [x] **Interface de mesure connue** : Focusrite Scarlett Solo 3ᵉ gén. (16/09).
- [x] **Jig d'impédance arbitré le 23/09/2026** par un panel de trois relecteurs
      et un arbitre : montage standard de REW, R_sense = 100 Ω (§ Matériel). Le
      câblage du 16/09 (micro en travers d'une 10 Ω) était faux. Propagé dans le
      livret, REFERENCE-TECHNIQUE.md (§ 02, sous-section Scarlett), PARCOURS.md,
      FEUILLE-DE-ROUTE.md, DECISIONS-PHASE-0.md, NOTES-TIPE.md et les diapositives.
- [x] **PARCOURS.md** (202 actions, A à Z) et **livret de manipulations** écrits ;
      livret relu le 23/09 (voir § Documents).
- [x] **Liste d'achats de la phase 1 établie** (PARCOURS.md, 1-B4) : trois 100 Ω
      (deux à 0,1 % pour le jig, une à 1 % pour l'oscilloscope), une 33 Ω, la 10 Ω
      de validation, un ballast 10 Ω / 5 W, condensateurs étalons, connecteurs.
      **Rien n'est encore commandé.**

- [x] v1 complète (pré-soutenance présentée aux profs début juin 2026 ; finale
      v1 structurée en attente de mesures) — **gelée dans archive-v1/**.
- [x] Pivot v2 acté : FEUILLE-DE-ROUTE.md créée, MCOT.md réécrit (v2),
      CLAUDE.md (ce fichier) réécrit, README mis à jour.
- [x] **REFERENCE-TECHNIQUE.md** rédigée (13 sept. 2026) : compagnon « comment /
      pourquoi » de la feuille de route, dont la section 08 fixe le cadre SCEI
      (oral 15 + 15 min, PDF 4/3 ≤ 5 Mo, limites de mots du MCOT, calendrier).
      C'est elle qui a permis de corriger l'oral « 10 min », le « ±11 % » sur
      f_c et la fenêtre de saisie du MCOT dans les autres documents.
- [x] Documents v2 réalignés sur ce cadre (13 sept. 2026) : CLAUDE.md,
      FEUILLE-DE-ROUTE.md, MCOT.md, README.md, index.html.
- [x] **Dossier `analyse/` écrit et éprouvé** : chaîne complète lecture des
      mesures → ajustement Thiele-Small (5 ou 8 paramètres, aiguillage `auto`) →
      optimisation E12 → figures ; **19 313 lignes de Python dont 4 253 de
      tests**, **171 tests au vert** (`python -m unittest discover -s
      analyse/tests`, 16 sept. 2026) et `python analyse/tout_refaire.py` en
      8 étapes, exit 0.
- [ ] Phase 0 à finir : critères + 2 niveaux d'écoute à geler, cible de sommation
      (D2, reportée), r_max de la self, gabarit D7 à signer — décisions de l'étudiant,
      à dater dans `DECISIONS-PHASE-0.md`.
- [x] **NOTES-TIPE.md réécrit en v2** (13 sept. 2026) : questions du jury sur le
      problème inverse, l'optimisation E12 et les incertitudes ; la v1 portait
      encore les trois architectures (dont le RC 1er ordre abandonné) et le
      « ≈ 11 % pour un RC ». Les placeholders y restent à combler après mesures.
- [x] **Refonte v2 des deux decks faite** (`pre-soutenance.html`,
      `presentation-finale.html`) : récit en 4 actes, gabarit SCEI **4/3
      (1024×768)**, figures injectées par marqueurs `<!--FIG:nom-->` (7 couples
      dans la présentation finale, 2 dans la pré-soutenance). Le « ± 11 % sur
      f_c » n'y figure plus qu'en **annexe A3, comme contre-exemple explicitement
      réfuté**. Le site Pages reflète donc la v2.
- [x] **PDF régénérés le 23/09/2026** après ces corrections : présentation
      finale 50 pages **1,80 Mo**, pré-soutenance 10 pages 0,51 Mo (sombre et
      claire), livret 90 pages A4 1,80 Mo. Deux défauts d'export corrigés au
      passage : poids (glyphes Type 3 dupliqués → `_alleger_pdf.py`, sans perte)
      et libellés SVG décalés dans le PDF (→ `geometricPrecision`). Détail :
      EXPORT-PDF.md § 3.3 et § 4.

## Prochaines étapes

1. Étudiant : **passer la commande de la phase 1** d'après `PARCOURS.md` 1-B4
   (version révisée du 23/09 — ne pas commander d'après une version antérieure).
2. Étudiant : relever au pied à coulisse les cotes des **deux évents** et le
   **volume net** de la caisse, puis faire **calculer et dater la prédiction de
   $f_b$ AVANT** toute mesure de Z(f) — sinon elle n'est plus falsifiable.
3. Étudiant, avec M. Chevalier (1-A3) : compte `lycees.scei-concours.fr`,
   prénom ou initiale et discipline pour le formulaire, fenêtre de 8 jours de
   mi-juin 2027 ; lui faire relire le **groupe C** du livret (tensions élevées)
   avant la première mise sous tension au banc.
4. Étudiant : geler et dater dans `DECISIONS-PHASE-0.md` les critères, les deux
   niveaux d'écoute, la cible de sommation (D2, échéance : avant le premier achat
   de composants du filtre et avant la rédaction du MCOT), le r_max de la self et
   le gabarit D7. La définition de f_c, elle, n'est plus à choisir (§ 04.1).
5. Phase 1, dès réception des composants : étalonnage des deux chaînes sur
   composants connus (livret, groupe A), puis Z(f) du sub en caisse et du bloc
   médiums câblé (groupe B). C'est la clé de voûte — rien d'autre avant.
6. Claude, sur demande : dépouiller les premières mesures avec `analyse/`, puis
   remplacer les données synthétiques des figures par les vraies (marqueurs
   `<!--FIG:nom-->`, injection idempotente) et régénérer les PDF.

## Historique

Tout le journal de travail v1 (boucle autonome du 2026-05-25, refonte Blueprint,
audit A–D du 2026-05-27, itérations pré-soutenance de juin) est conservé dans
`archive-v1/CLAUDE.md`. Ne pas le recopier ici.
