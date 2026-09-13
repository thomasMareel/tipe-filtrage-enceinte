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
- **Thème national** : Sobriété, efficacité, optimisation.
- **Enceinte deux voies (DIY)** : 1 subwoofer **8 Ω 18″** + 2 médium-aigu
  **4 Ω câblés en série (= 8 Ω)**. Raccord cible : **100 Hz**. Pavillons d'aigu
  hors périmètre. Type de caisse (clos / bass-reflex) à documenter.

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
  carte son de qualité (modèle à documenter).
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
- Type de caisse (clos/bass-reflex) ; câblage exact des médiums.
- Sensibilités (dB/W/m) pour l'égalisation des niveaux.
- Modèle exact de la carte son ; les 2 niveaux d'écoute de référence à geler.

## Points scientifiques à NE PAS oublier (critique prof 2026-05-25, toujours valides)

- **2ⁿᵈ ordre Butterworth ⇒ inversion de polarité d'une voie OBLIGATOIRE**
  (sinon trou profond à fc ; avec inversion → bosse +3 dB).
- **Fs en caisse ≠ Fs datasheet** : Fc(clos) > Fs ; bass-reflex = deux pics.
  Mesurer le pic en caisse n'est pas une erreur.
- **Z exacte sans approximation courant constant** : mesurer V_HP ET V_Rref →
  Z = Rref·(V_HP/V_Rref). L'hypothèse I≈cst se dégrade au pic : |Z|_max = R_e(1+Q_ms/Q_es)
  vaut **60 à 200 Ω pour un 18″** de catalogue (le « 40–60 Ω » hérité de la v1 est l'ordre
  de grandeur du **bloc médiums**) → voir REFERENCE-TECHNIQUE.md § 02.4.
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
  depuis l'ordinateur du jury (ni HTML, ni notes, ni objets en salle). Le gabarit
  actuel est **16:9 (1280×720) : à repasser en 4/3 (1024×768) lors de la refonte
  v2** — et à figer aussi pour les figures matplotlib produites en phases 2-4,
  sinon elles seront toutes à refaire (détail : REFERENCE-TECHNIQUE.md § 08.2).
- Dépôt : https://github.com/thomasMareel/tipe-filtrage-enceinte
  Site : https://thomasmareel.github.io/tipe-filtrage-enceinte/
  Note : gh.exe est dans "C:\Program Files\GitHub CLI\" (pas dans le PATH).

## Procédure PDF (résumé — détail dans EXPORT-PDF.md)

PDF vectoriels via decktape (Chrome système, PUPPETEER_EXECUTABLE_PATH) ;
variante claire imprimable via css/blueprint-light.css. Repli bitmap :
captures Chrome headless par slide + img2pdf (dossier _pdfbuild/ gitignoré).

## État actuel (2026-09-13)

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
- [ ] Phase 0 à finir : critères + 2 niveaux d'écoute à geler (décision
      étudiant), liste d'achats phase 1, squelette code `analyse/`,
      **désignation du professeur encadrant** (obligatoire pour la saisie SCEI
      de mi-janvier 2027 — voir REFERENCE-TECHNIQUE.md § 08.3).
- [x] **NOTES-TIPE.md réécrit en v2** (13 sept. 2026) : questions du jury sur le
      problème inverse, l'optimisation E12 et les incertitudes ; la v1 portait
      encore les trois architectures (dont le RC 1er ordre abandonné) et le
      « ≈ 11 % pour un RC ». Les placeholders y restent à combler après mesures.
- [ ] Les slides à la racine (pre-soutenance.html, presentation-finale.html)
      sont encore la **v1** — refonte v2 prévue en phase 5 (ou avant sur
      demande), avec passage du gabarit 16:9 au 4/3. Le site Pages reflète donc
      la v1 pour l'instant. `presentation-finale.html` affiche encore
      « ± 11 % sur f_c » (l. 1073 et 1173) : à corriger à la refonte.

## Prochaines étapes

1. Étudiant : valider/amender les critères et les 2 niveaux d'écoute
   (FEUILLE-DE-ROUTE.md § Critères) → les geler, et consigner la décision datée
   dans **DECISIONS-PHASE-0.md**. La définition de f_c, elle, **n'est plus à
   choisir** : c'est le croisement des deux voies (ci-dessus, § 04.1 fait foi).
   Restent à trancher : la **cible de sommation** (Butterworth +3 dB à f_x avec
   inversion de polarité, *ou* somme plate LR2 — les deux ne peuvent pas être
   gelées ensemble, voir FEUILLE-DE-ROUTE.md et REFERENCE-TECHNIQUE.md § 04.3)
   et le **r_max de la self**, qui est le vrai choix caché derrière le budget
   (REFERENCE-TECHNIQUE.md § 05.8 et § 05.10).
2. Étudiant : demander à un professeur d'être **encadrant** et vérifier qu'il a
   un compte sur lycees.scei-concours.fr (échéance : rentrée).
3. Étudiant : acheter R_ref 100 Ω 1 % (+ 10 Ω), pinces, wattmètre de prise ;
   vérifier résistance de puissance 8 Ω au lycée.
4. Claude : squelette `analyse/` (Python : lecture mesures → fit T-S →
   optimisation E12 avec sanity check 8 Ω) dès que demandé — figer d'emblée le
   format de figure 4/3. **Environnement prêt** : scipy 1.18.1 installé et
   vérifié (voir § Matériel) — rien à installer, rien à contourner.
5. Claude (sur demande) : refonte des slides en v2, gabarit 4/3 — c'est le seul
   livrable encore en v1 avec les PDF exportés.
6. Phase 1 dès la rentrée : étalonnage de la chaîne sur composants connus,
   puis Z(f) du sub en caisse. C'est la clé de voûte — rien d'autre avant.

## Historique

Tout le journal de travail v1 (boucle autonome du 2026-05-25, refonte Blueprint,
audit A–D du 2026-05-27, itérations pré-soutenance de juin) est conservé dans
`archive-v1/CLAUDE.md`. Ne pas le recopier ici.
