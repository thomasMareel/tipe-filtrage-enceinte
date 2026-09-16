# Feuille de route — TIPE v2 (pivot du 2026-08-04)

> Sujet v2 : **optimisation sous contraintes du filtre de raccord à 100 Hz sur la
> charge réelle Z(f) des haut-parleurs**. La v1 (« passif ou actif ? ») est gelée
> dans `archive-v1/` et survit ici comme référentiel de comparaison.

## Problématique

> « Comment concevoir le filtre de raccord à 100 Hz d'une enceinte deux voies
> pour qu'il tienne sa cible sur la charge réelle — un haut-parleur dont
> l'impédance varie fortement avec la fréquence — au moindre coût en composants,
> en pertes et en matière ? »

> **Pourquoi aucun chiffre dans la problématique (pour l'instant).** Le rapport
> $\max|Z|/\min|Z|$ est un **livrable de la phase 1** `[[à mesurer]]` : il sera
> inséré ici, et seulement là, une fois mesuré. La formule « du simple au
> sextuple » qui figurait dans cette phrase n'a jamais été mesurée et est
> probablement basse — $Z_{pic} = R_e(1 + Q_{ms}/Q_{es})$ donne 60 à 200 Ω pour
> un 18″ de catalogue, soit un rapport bien supérieur à 6. Annoncer un chiffre
> avant la mesure serait précisément la faute que le projet se fait un principe
> d'éviter.

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
| Fidélité du raccord | Écart RMS (dB) de la somme des deux voies à **la cible de sommation gelée en phase 0** (voir l'encadré ci-dessous : **plate** ou **Butterworth** — la contradiction n'est pas tranchée), bande 40–250 Hz | Micro + REW, protocole champ proche fixé en phase 1 |
| Précision de f_c | \|f_c réalisée − 100 Hz\|, f_c = **fréquence de croisement des deux voies** (définition unique du projet, REFERENCE-TECHNIQUE.md § 04.1 fait foi) | Bode électrique puis acoustique |
| Pertes d'insertion | dB et W perdus en bande passante à puissance donnée | V/I au banc, DCR |
| Consommation au repos | W de la chaîne complète sans signal | Wattmètre de prise |
| Coût marginal | € de composants, ampli existant considéré acquis | Factures |
| Coût système | € du système complet équivalent (scénario stéréo) | Devis |
| Encombrement / matière | Masse (kg) et volume (L) du filtre, cuivre utilisé | Balance, mètre |
| Robustesse | Dérive de f_c et de l'écart RMS entre niveau faible et niveau fort | Mesures aux 2 niveaux gelés |

> **Où les décisions sont consignées** : ce tableau est une **proposition**. Dès
> qu'une ligne est validée ou amendée par Thomas, la décision — son libellé
> exact, sa date et sa justification en une phrase — est écrite dans
> **`DECISIONS-PHASE-0.md`**, qui fait foi pour tout ce qui est gelé. Les autres
> documents (celui-ci compris) y renvoient au lieu de recopier. Une décision qui
> n'est pas datée dans ce fichier n'est pas gelée.

Les deux niveaux d'écoute de référence (faible / fort) sont à fixer en phase 0
et à ne plus changer. **Aucun critère ne doit être ajouté ou retiré après les
premières mesures comparatives** — c'est ce qui rend la conclusion honnête.

> ### ⚠ Décision de phase 0 non tranchée : la cible de sommation
>
> **Deux cibles incompatibles cohabitent aujourd'hui dans le projet** et l'une
> des deux doit être abandonnée **avant** le gel des critères.
>
> - **Option A — cible plate (Linkwitz-Riley 2, $Q = 1/2$)**. C'est ce qu'écrit
>   ce document (critère « Fidélité du raccord » ci-dessus, et phase 3). Avec
>   inversion de polarité d'une voie, la somme vaut **0,000 dB partout** et
>   l'écart de phase entre voies est **nul partout** : la cible est atteignable
>   exactement. Prix à payer : sur 8 Ω, LR2 impose $L = 25{,}5$ mH et
>   $C = 99{,}5$ µF (E12 : **27 mH / 100 µF**) au lieu de 18 mH / 150 µF. À DCR
>   imposée, le cuivre suit $m \propto L^{3/2}$ : **+84 % de cuivre par self**
>   (facteur $(27/18)^{3/2} = 1{,}84$), soit un couple de selfs qui passe
>   d'environ 116 à **213 €** de fil à $r_{max} = 1{,}5\ \Omega$ (75 → 138 € à
>   2 Ω). Le budget de 500 € devient tendu.
> - **Option B — cible Butterworth 2 ($Q = 1/\sqrt2$)**. C'est ce qu'utilisent
>   toutes les illustrations, le filtre « catalogue » hérité de la v1 (18 mH /
>   150 µF) et le sanity check 8 Ω de la phase 3. Avec inversion de polarité, la
>   somme fait **+3,01 dB à $f_c$** et +1,68 dB à 50 et 200 Hz : ce n'est pas un
>   défaut, c'est **la signature de l'alignement**. Conséquence directe :
>   l'écart RMS d'un Butterworth *parfait* à une cible plate vaut **2,29 dB** sur
>   40–250 Hz — garder « écart à la cible plate » comme critère reviendrait à
>   noter 2,29 dB un filtre qui fait exactement ce qu'on lui demande.
>
> **Trancher, c'est choisir la cible du critère « Fidélité » ET la cible par
> défaut du code d'optimisation de la phase 3 — les deux ensemble.** Si A : il
> faut amender le filtre de référence (27 mH / 100 µF) et reprendre le budget
> selfs. Si B : il faut réécrire « cible plate » en « cible Butterworth » dans le
> critère ci-dessus et en phase 3. Détail, démonstrations et troisième voie
> (LR4 : plate **sans** inversion, mais 4 gros composants par voie) :
> **REFERENCE-TECHNIQUE.md § 04.3**. **Décision de Thomas, à consigner dans
> `DECISIONS-PHASE-0.md`.**

## Phases

### Phase 0 — Cadrage (**août – sept. 2026**) — EN COURS

> **Glissement assumé d'un mois.** La phase 0 était calée sur août 2026 ; elle
> n'est pas close à la mi-septembre (critères, niveaux d'écoute, cible de
> sommation, $r_{max}$, encadrant : tous non gelés). Elle est donc re-datée
> **août – sept. 2026** et **recouvre le début de la phase 1**, ce qui est
> acceptable : l'étalonnage de la chaîne de mesure ne dépend d'aucune des
> décisions restantes. Ce qui ne l'est pas, c'est de laisser glisser la suite —
> voir l'encadré « Effet du glissement sur la marge MCOT » en fin de phase 3.

- [x] Archiver la v1 (`archive-v1/`, tag git `v1-sujet-passif-actif`).
- [x] Feuille de route (ce document), MCOT v2, CLAUDE.md v2.
- [ ] Geler les critères ci-dessus + les 2 niveaux d'écoute (décision étudiant),
      **consignés et datés dans `DECISIONS-PHASE-0.md`**.
- [ ] Trancher la **cible de sommation** (plate / Butterworth) — voir l'encadré
      après le tableau des critères. C'est la décision qui bloque la phase 3.
- [ ] Geler **$r_{max}$ de la self** (fenêtre praticable 1,5 à 2 Ω, cf.
      REFERENCE-TECHNIQUE.md § 05.8) : c'est ce choix, et non le budget, qui
      fixe le coût du cuivre.
- [x] **Définition de f_c : décidée, plus à choisir.** C'est la **fréquence de
      croisement des deux voies** — l'unique $f \in [40 ; 250]$ Hz telle que
      $|H_{PB}(f)\,G_{sub}(f)| = |H_{PH}(f)\,G_{méd}(f)|$ — seule définition
      insensible à la perte d'insertion et interprétable sur la charge réelle.
      **REFERENCE-TECHNIQUE.md § 04.1 fait foi.** Les autres nombres restent des **repères**,
      jamais « la » coupure : pour 18 mH + 150 µF sur 8 Ω ($Q = 0{,}730$), pôle
      **96,86 Hz** ; −3 dB passe-bas **99,93 Hz** et passe-haut **93,88 Hz** en
      convention **demi-puissance (−3,0103 dB, celle de REW)**, ou 99,82 et
      93,99 Hz au seuil littéral −3,000 dB — deux **conventions**, pas un
      arrondi fautif. Toujours citer la convention avec le nombre.
- [ ] **Harmoniser l'écriture de f_c dans tous les documents** (slides v1 et
      supports compris) : une seule définition affichée, les repères annoncés
      comme tels, avec leur convention. La décision est prise, la mise en
      cohérence reste à faire.
- [ ] **Désigner le professeur encadrant** et obtenir son accord explicite ;
      vérifier qu'il a un compte sur lycees.scei-concours.fr. Sans encadrant
      déclaré à l'étape 1 (mi-janvier 2027) et sans sa validation (mi-juin
      2027), la note peut être zéro. Échéance : rentrée sept. 2026.
- [ ] Trancher le **gabarit 4/3 (1024×768)** avant de produire la moindre figure
      des phases 2-4, sinon elles seront toutes à refaire.
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
- Puis : Z(f) du sub **en caisse** sur **10 Hz – 1 kHz** et du bloc médiums sur
  **10 Hz – 2 kHz** (grille resserrée autour des accidents dans les deux cas).
  La bande ne s'arrête pas à 500 Hz : au-dessus du pic motionnel, $|Z|$ remonte
  en $\omega L_e$, et **c'est cette remontée qui identifie $L_e$**. Sans elle, le
  fit de la phase 2 n'a aucune prise sur ce paramètre — or $L_e$ commande le
  Zobel et la charge vue par le passe-haut. Rappel v1 : F_c en caisse > F_s
  datasheet, c'est normal, ce n'est pas une erreur.
- **La caisse du sub est bass-reflex à deux évents (constat du 16/09/2026,
  D8 de `DECISIONS-PHASE-0.md`) : la grille de fréquences doit résoudre DEUX
  PICS ET LE CREUX intermédiaire.** Une grille calée sur un pic unique passerait
  à côté de la structure même de la charge, et le fit de la phase 2 s'en
  trouverait faux sans le dire. Concrètement (consigne détaillée :
  `REFERENCE-TECHNIQUE.md` § 02.6) : 1/12 d'octave sur toute la plage
  $10$ Hz – $1$ kHz, puis une **grille fine sur les DEUX PICS seulement**,
  $\delta f \le f_{pic}/(10\,Q_{pic})$ — de l'ordre de $0{,}2$ Hz autour de
  $f_L$ et de $1$ Hz autour de $f_H$ — repérés d'abord par un balayage grossier.
  **Le creux, lui, ne se densifie pas** : il est *plat* ($|Z|$ ne remonte de 1 %
  qu'au-delà d'une bande de 5,2 Hz, soit 0,22 octave), donc sous 1 % de bruit
  son argmin est indiscernable et densifier n'y gagnerait que du temps de banc
  perdu. **$f_b$ ne se lit pas sur l'argmin de $|Z|$** (biais $-2{,}3$ % sur le
  modèle) : on le lit au **passage par zéro de la phase** entre les deux pics,
  dont la pente est raide, ou — mieux — on le prend de l'**ajustement** de la
  phase 2.
- **Descendre sous 20 Hz pour voir le premier pic — AU NIVEAU FAIBLE
  UNIQUEMENT.** Le premier pic $f_L$ tombe sous l'accord ; il faut donc explorer
  cette zone, mais sous $f_b$ la membrane n'est plus chargée par les évents et
  l'excursion devient maximale : **risque mécanique** pour le 18″. Règle :
  balayage sous $f_b$ **seulement au niveau faible gelé (D3)**, avec contrôle
  visuel du débattement ; **au niveau fort, borne basse $\ge 2f_b$**, sans
  exception. Un balayage fort descendu sous l'accord peut détruire le
  haut-parleur — c'est le seul geste de la phase 1 qui soit irréversible.
- **Mesurer le bloc médiums TEL QU'IL EST CÂBLÉ, pavillons d'ultra-aigu
  connectés.** Les 2 pavillons sont en **parallèle** des médiums : hors périmètre
  acoustique (hors bande à 100 Hz), mais **dans la charge électrique** que voit
  le passe-haut. Débrancher les pavillons « parce qu'on n'en parle pas »
  mesurerait une charge qui n'existe pas dans le montage. Consigner au passage
  s'il y a ou non un **condensateur en série** avec eux `[[à vérifier]]` : s'il
  existe (3 à 10 µF typiques), la branche aigu pèse plusieurs centaines d'ohms
  vers 100 Hz et n'influe quasiment pas ; sinon elle abaisse $|Z|$ du bloc et
  les pavillons reçoivent du 100 Hz à pleine puissance pendant les balayages
  (prudence sur le niveau). Dans les deux cas la mesure à faire est la même.
- **Balayage acoustique en champ proche de chaque haut-parleur** (micro à
  quelques centimètres du centre du cône, voie par voie, HP nu sans filtre) :
  il donne les **sensibilités relatives** $G_{sub}(f)$ et $G_{méd}(f)$.
  **Elles sont nécessaires AVANT l'optimisation de la phase 3** : la fonction de
  coût porte sur la somme $S = H_{PB}G_{sub} + p\,H_{PH}G_{méd}$, qui n'a aucun
  sens sans elles, et la définition même de $f_c$ (croisement) les fait
  intervenir. Les mesurer en phase 4, comme initialement prévu, serait **trop
  tard** : on optimiserait sur deux voies supposées de même sensibilité, puis on
  découvrirait l'écart au moment de valider. Un balayage par voie suffit ; le
  protocole complet (niveaux gelés, distance, calibrage) reste en phase 4.

**Livrables** : courbes Z(f) module+phase avec barres d'erreur ; f_s en caisse ;
**la fréquence d'accord $f_b$ lue au creux d'impédance** entre les deux pics
`[[à mesurer]]`, avec les deux fréquences de pic $f_L$ et $f_H$ — $f_b$ commande
à la fois le modèle à ajuster en phase 2 et la borne basse de sécurité au niveau
fort ; **le rapport $\max|Z|/\min|Z|$ sur la bande utile** `[[à mesurer]]` —
c'est le chiffre qui remplacera « varie fortement avec la fréquence » dans la
problématique, et il ne sera écrit nulle part avant d'être mesuré ;
$G_{sub}(f)$ et $G_{méd}(f)$ en champ proche (sensibilités relatives) ;
$Z(f)$ du **bloc médiums câblé complet** (médiums + pavillons en parallèle).
**Prédiction falsifiable à poser AVANT de dépouiller** : à partir des dimensions
des deux évents et du volume interne `[[à mesurer]]`, calculer le $f_b$ attendu
et l'écrire daté au cahier, **puis** le confronter au creux mesuré. Un écart
s'explique (correction d'extrémité, volume occupé par l'aimant et les renforts,
pertes) ; c'est de la démarche scientifique, pas un échec.
**Porte de validation** : la résistance étalon est retrouvée à ±3 % et le
condensateur suit 1/ωC sur deux décades. Sinon on diagnostique avant d'avancer.
**Repli** : si la carte son pose problème (couplage, impédance de sortie),
GBF + oscillo point par point au 1/12 d'octave — lent mais infaillible.
**Achats** : R_ref 100 Ω 1 % (+ une 10 Ω), pinces/câbles, résistance de
puissance 8 Ω si absente au lycée, wattmètre de prise (~20 €).

### Phase 2 — Problème inverse : identification Thiele-Small (oct. 2026)

- **Modèle à ajuster : le modèle BASS-REFLEX à 7-8 paramètres**
  (`analyse/modele_hp.py` : `Z_bassreflex`, `Z_bassreflex8`, variante
  `Z_bassreflex_semi` si la semi-inductance est nécessaire en haut de bande).
  La caisse est bass-reflex à deux évents (constat du 16/09/2026) : ce n'est plus
  une option. Paramètres : $R_e$, $L_e$ (ou $K$, $n$), $R_{es}$, $f_s$, $Q_{ms}$,
  $f_b$, $Q_l$, $\alpha$. Commencer avec **une seule perte globale** et n'en
  ajouter une seconde que si le résidu structuré dépasse le seuil de
  REFERENCE-TECHNIQUE.md § 01.10.
- **Le modèle à 5 paramètres (caisse close, $Z = R_e + j\omega L_e +$ une
  branche motionnelle) n'est plus le modèle du projet : il devient un
  contre-exemple pédagogique.** Ajusté sur des données bass-reflex, il
  **converge en silence** sur des paramètres faux — pas d'erreur, juste un
  résidu un peu moins bon — et la phase 3 optimiserait alors sur une charge qui
  n'existe pas. Montrer ce fit raté à côté du bon est une excellente planche
  d'oral : c'est la démonstration que « ça a convergé » ne veut pas dire « c'est
  juste ». Garde-fou automatique :
  `analyse/io_mesures.py::diagnostiquer_caisse()` compte les pics et refuse le
  modèle à 5 paramètres avec un avertissement explicite.
- Ajustement moindres carrés (scipy) sur module ET phase ; analyse des résidus ;
  incertitudes des paramètres (covariance, Monte-Carlo sur les barres d'erreur).
- Confrontation aux ordres de grandeur datasheet ; explication du décalage en caisse.
- **Contrôle « évent inerte »** : faire tendre l'impédance de la branche d'évent
  vers l'infini doit redonner exactement la caisse close de même volume — c'est
  le test qui prouve que le modèle à 7-8 paramètres englobe bien celui à 5.

**Livrables** : paramètres identifiés ± incertitudes, **dont $f_b$ ajusté** ;
courbe mesure vs modèle ; le fit à 5 paramètres tracé **en contre-exemple**, avec
son résidu.
**Porte de validation** : résidu relatif faible sur 20–300 Hz, paramètres
stables quand on retire aléatoirement des points de mesure, **ET cohérence entre
le $f_b$ ajusté par le modèle et le $f_b$ lu directement au creux d'impédance en
phase 1** (deux chemins indépendants vers la même grandeur : s'ils divergent, le
fit est suspect, on diagnostique avant d'avancer). Écart toléré à fixer avec les
incertitudes de la phase 1 `[[à geler]]`.
**Repli** : si le fit bute en haut de bande (courants de Foucault), restreindre
la bande utile au raccord ou mentionner le modèle de semi-inductance en perspective.

### Phase 3 — Optimisation numérique du filtre (nov.–déc. 2026)

- Cible : somme des deux voies sur 40–250 Hz (gain et phase cohérente), **selon
  la cible de sommation gelée en phase 0**. ⚠ **Contradiction non tranchée** :
  cette ligne dit « plate » (= Linkwitz-Riley 2, $Q = 1/2$, 27 mH / 100 µF sur
  8 Ω, somme à 0,000 dB partout après inversion de polarité), alors que le
  sanity check ci-dessous et toutes les illustrations utilisent **Butterworth**
  ($Q = 1/\sqrt2$, 18 mH / 150 µF, **+3,01 dB à $f_c$** après inversion, soit
  **2,29 dB** d'écart RMS à une cible plate — sa signature, pas un défaut).
  **Les deux ne peuvent pas être gelées ensemble** : la cible du critère
  « Fidélité » et la cible par défaut du code doivent être la même. Conséquence
  chiffrée du choix de LR2 : +84 % de cuivre par self à DCR imposée
  ($m \propto L^{3/2}$), soit ~213 € de fil pour un couple à $r_{max} = 1{,}5\
  \Omega$ au lieu de ~116 €. Voir l'encadré après le tableau des critères et
  **REFERENCE-TECHNIQUE.md § 04.3**. Décision de phase 0, à consigner dans
  `DECISIONS-PHASE-0.md`.
- Variables : L₁, C₁ (passe-bas), C₂, L₂ (passe-haut), option réseau de Zobel (R, C).
- Contraintes : valeurs des séries E12/E6 réelles, budget, DCR(L) issu de
  l'étude self (satellite intégré ici), encombrement.
- Fonction de coût : écart RMS à la cible + pénalités coût/pertes (pondérations
  affichées et discutées — c'est le « cahier des charges » chiffré).
- Méthode : l'espace discret E12 est énumérable → recherche exhaustive (robuste),
  recoupée par un optimiseur continu arrondi ensuite. LTspice en contre-vérification.
- Étude self en parallèle : formules de Wheeler, redécouverte numérique de la
  bobine de Brooks, choix du fil (loi r×m ≈ constante à L fixée).
- **Rédaction du texte du MCOT** (bibliographie commentée 650 mots,
  problématique 50, objectifs 100, ancrage 50, motivation 50) : la saisie SCEI
  tombe mi-janvier 2027, en pleine phase 4 — le texte doit être prêt avant.
  Verrouiller aussi à cette date les **positionnements thématiques** et les
  mots-clés, sur le récit prévu et non sur des résultats pas encore obtenus.

**Livrables** : design optimisé + courbes prédites catalogue vs optimisé sur Z(f)
réelle ; modèle de coût de la self ; plan de bobinage ; **texte du MCOT prêt à
saisir**.
**Porte de validation (sanity check clé)** : alimenté avec une charge 8 Ω
résistive pure, l'optimiseur doit retomber sur le filtre catalogue de la cible
gelée (Butterworth 18 mH / 150 µF, ou LR2 27 mH / 100 µF si c'est l'option A qui
est retenue). S'il n'y retombe pas, il y a un bug — ne rien acheter avant ce test.

> **Effet du glissement de la phase 0 sur la marge MCOT.** La phase 0 re-datée
> « août – sept. 2026 » pousse mécaniquement la suite d'environ un mois :
> phase 1 sept. → **sept.-oct.**, phase 2 oct. → **oct.-nov.**, phase 3
> nov.-déc. → **nov. 2026 – janv. 2027**. Or la saisie SCEI de l'étape 1 ouvre
> **mi-janvier 2027** et le **texte du MCOT est un livrable de la phase 3** : la
> marge, d'un bon mois à l'origine, tombe à **quelques jours**. Deux garde-fous,
> à appliquer sans attendre de constater le retard :
> 1. **Le texte du MCOT ne dépend d'aucun résultat.** Il porte sur la
>    problématique, les objectifs, l'ancrage et la bibliographie — tout est déjà
>    décidé. Il est donc à rédiger **dès décembre 2026, en parallèle** de
>    l'optimisation, et non à la fin de la phase 3. Le seul chiffre qu'il
>    pourrait vouloir citer (le rapport $\max|Z|/\min|Z|$) vient de la phase 1,
>    donc bien en amont.
> 2. **Aucune décision de phase 0 ne doit plus glisser.** Chaque semaine de
>    retard sur le gel des critères et de la cible de sommation se reporte
>    intégralement sur cette marge, et la date de clôture SCEI, elle, ne bouge
>    pas (5-6 février, stable depuis des années).

### Phase 4 — Fabrication et validation expérimentale (déc. 2026 – fév. 2027)

- Bobiner la/les selfs ; mesurer L (résonance série avec C connu : avec 150 µF,
  pic attendu vers 97 Hz au GBF+oscillo) et DCR ; écart au modèle expliqué.
- Assembler filtre catalogue ET filtre optimisé ; monter la référence active
  Sallen-Key (valeurs ci-dessus) sur alimentation symétrique.
- Ordre des tests, chacun conditionnant le suivant :
  1. électrique sur résistance de puissance 8 Ω (f_c, pente, pertes) ;
  2. électrique sur HP réel (l'écart attendu apparaît) ;
  3. acoustique REW en champ proche (20–500 Hz), voie par voie — **filtre
     inséré** cette fois : les sensibilités $G_{sub}$, $G_{méd}$ des HP nus ont
     déjà été relevées en phase 1, puisque la phase 3 en avait besoin ;
  4. **sommation champ proche du sub bass-reflex (méthode de Keele) — ÉTAPE
     NOUVELLE, issue du constat du 16/09/2026.** En caisse close, un seul
     relevé au centre du cône suffit. **En bass-reflex, non** : sous l'accord
     c'est l'évent qui rayonne l'essentiel, et la membrane peut être en
     opposition. Il faut donc **trois relevés en champ proche — la membrane et
     CHACUN des deux évents** — puis les sommer **en pression complexe avec une
     pondération par la racine des aires** : chaque contribution est multipliée
     par $\sqrt{S_i/S_{membrane}}$ avant addition (la pression de champ proche
     rapportée à un rayonnement équivalent est proportionnelle à $\sqrt{S}$).
     Avec deux évents identiques d'aire $S_p$ chacun, le terme évent pèse
     $\sqrt{2S_p/S_d}$. **Temps de manip à prévoir : ~45 min par configuration**
     (3 positions de micro × 3 répétitions, repositionnement soigné et consigné,
     à refaire pour chaque filtre comparé) — c'est le poste le plus coûteux en
     temps de la phase 4, à inscrire au planning et non à découvrir le jour même.
     Mesurer les aires $S_d$ (membrane, diamètre effectif) et $S_p$ (évent) au
     mètre ruban, et les consigner : elles entrent dans le calcul.
  5. somme des deux voies au raccord — **avec inversion de polarité d'une voie**
     (2ⁿᵈ ordre : sans inversion → trou, avec → bosse +3 dB).
- **Borne basse de sécurité au niveau fort : `Start` $\ge 2f_b$, sans
  exception.** Le $f_b$ à utiliser est celui **mesuré en phase 1** (creux
  d'impédance), pas une valeur de catalogue. Sous l'accord, la membrane n'est
  plus chargée par les évents, l'excursion devient maximale et le 18″ peut être
  détruit mécaniquement. Toute descente sous $f_b$ se fait **au niveau faible
  uniquement**, avec contrôle visuel du débattement avant le balayage. Cette
  borne s'applique aussi aux balayages « bobine chaude » du test de robustesse.
- Robustesse : refaire la mesure du raccord aux 2 niveaux gelés (dérive thermique).
- Énergie : consommation au repos actif vs pertes passif → point de croisement.

**Livrables** : toutes les courbes de la présentation finale ; tableau brut des critères.
**Porte de validation** : f_c électrique sur résistance conforme à la prédiction
à ±5 % avant de passer à l'acoustique — la prédiction étant faite avec les
valeurs **mesurées** de L et C, pas avec les valeurs nominales. Avec des
composants à ±10 %, un filtre LC a en effet
$u(f_0)/f_0 = \tfrac12\sqrt{(u_L/L)^2 + (u_C/C)^2}$, soit **7,1 % en borne au
pire cas et 4,1 % en incertitude-type** (loi rectangulaire, GUM) — **toujours
écrire le couple, jamais un nombre seul** : la borne au pire cas dépasse la
porte à ±5 %, l'incertitude-type non. Conclusion inchangée : la porte n'est
tenable que si L et C sont mesurés d'abord.
**Définition de f_c** : c'est le **croisement des deux voies**
($|H_{PB}G_{sub}| = |H_{PH}G_{méd}|$), définition unique du projet —
REFERENCE-TECHNIQUE.md § 04.1 fait foi. Les autres nombres ne sont que des
**repères** : pour 18 mH + 150 µF sur 8 Ω ($Q = 0{,}730$), pôle 96,86 Hz ;
−3 dB passe-bas 99,93 Hz et passe-haut 93,88 Hz en convention demi-puissance
(−3,0103 dB, celle de REW), 99,82 et 93,99 Hz au seuil littéral −3,000 dB.
**Pièges connus (hérités v1)** : modes de pièce à 100 Hz (λ ≈ 3,4 m) → champ
proche ; égalisation des niveaux entre voies ; petites amplitudes d'abord.

### Phase 5 — Analyse, supports, échéances SCEI (fév. – **fin mai** 2027)

- Tableau comparatif final selon les critères gelés ; incertitudes propagées ;
  conclusion honnête (y compris si le passif optimisé ne rattrape pas l'actif :
  la limite identifiée est un résultat).
- Refonte des livrables en v2 : presentation-finale.html, accueil, PDF (les
  NOTES-TIPE.md v2 existent depuis sept. 2026 — il restera à y injecter les
  chiffres mesurés) ; répétitions de l'exposé (**15 min**) et de l'entretien
  (**15 min** de questions : c'est là que servent les annexes).
- **Format du support** : le SCEI projette un **PDF 4/3 paysage de 5 Mo max**
  depuis l'ordinateur du jury (ni HTML, ni notes du présentateur, ni objet, ni
  clé USB). Le gabarit actuel est 16:9 → passage en **1024×768** ; diapositives
  **numérotées** ; listings Python annexés après la conclusion **et** apportés
  en double exemplaire papier. Détail : REFERENCE-TECHNIQUE.md § 08.2.
- **DOT** (Déroulé Opérationnel du TIPE) : **4 à 8 jalons factuels de 50 mots
  max chacun**, strictement chronologiques, difficultés comprises — le pivot
  v1 → v2 du 2026-08-04 y a toute sa place. Saisi à l'étape 2 SCEI, **fin
  févr. → début juin 2027** (dates 2027 [[à vérifier]]), en même temps que le
  téléversement du PDF. Matière première : le journal daté du dépôt.
- **Validation par le professeur encadrant** (étape 3, ~mi-juin 2027, fenêtre
  de 8 jours) : sans elle, note zéro possible. L'encadrant doit être désigné
  **dès la phase 0**.

> **Attention au calendrier** : le MCOT ne se saisit **pas** en phase 5 mais à
> l'**étape 1 SCEI, mi-janvier → début février 2027** (dates 2027
> [[à vérifier]] à la parution des Attendus 2026-2027 sur
> scei-concours.fr/tipe.html ; clôtures historiquement stables au 5-6 février).
> Son **texte doit donc être rédigé dès la phase 3 (nov.–déc. 2026)**, avant
> les mesures acoustiques. Les oraux commencent **fin juin 2027** et le PDF est
> dû **début juin** : la phase 5 doit être bouclée **fin mai**, pas « en juin ».

## Calendrier synthétique

| Période | Phase | Jalon |
|---|---|---|
| **Août – sept. 2026** | 0 — Cadrage | Critères, cible de sommation et $r_{max}$ gelés (`DECISIONS-PHASE-0.md`), achats listés — **glissement d'un mois assumé** |
| Sept. 2026 (recouvre la phase 0) | 1 — Mesure Z(f) | Chaîne validée sur composants connus ; $\max\|Z\|/\min\|Z\|$ mesuré ; sensibilités champ proche ; **encadrant désigné** |
| Oct. 2026 | 2 — Problème inverse | Paramètres T-S ± incertitudes |
| Nov.–déc. 2026 | 3 — Optimisation | Design validé par le sanity check 8 Ω |
| Déc. 2026 – févr. 2027 | 4 — Fabrication/mesures | Courbes finales, tableau brut |
| Déc. 2026 – janv. 2027 | 3-4 (en parallèle) | **Rédaction du MCOT** (biblio 650 mots, problématique, objectifs) |
| **Mi-janv. → début févr. 2027** | — | **ÉTAPE 1 SCEI** : titre, encadrant, ancrage, motivation, MCOT |
| Févr. – **mai** 2027 | 5 — Analyse/supports | Slides v2 **en 4/3**, DOT, listings imprimés, répétitions ; clôture fin mai |
| **Début juin 2027** | — | **ÉTAPE 2 SCEI** : téléversement du PDF + DOT ; puis **ÉTAPE 3** : validation par l'encadrant (~mi-juin) |
| Fin juin – juillet 2027 | — | Oraux (15 min d'exposé + 15 min d'entretien) |

> Dates 2027 **[[à vérifier]]** : elles sont extrapolées des sessions 2025 et
> 2026 et ne seront fermes qu'à la parution des Attendus 2026-2027 sur
> <https://www.scei-concours.fr/tipe.html>. Les **clôtures** sont stables depuis
> des années (étape 1 : 5-6 févr. ; étape 2 : 9-10 juin ; étape 3 : ~19 juin) ;
> les **ouvertures** le sont moins (celle de l'étape 2 a avancé de 37 jours
> entre 2020 et 2026). Tenir l'extrapolation pour robuste à ±2 semaines.

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
- **Budget** (≤ 500 €) : la ligne « selfs bobinées maison ~25 €/pièce » de la
  version initiale de ce document était fausse sur deux points. (i) **Il faut
  4 selfs**, pas une : chaque filtre en compte deux ($L_1$ série au passe-bas,
  $L_2$ parallèle au passe-haut) et le projet en construit **deux** (catalogue
  et optimisé). (ii) Surtout, **le prix d'une self n'est pas une donnée : c'est
  le $r_{max}$ qu'on choisit**, via $m = K_{Cu}(L/r)^{3/2}$ — annoncer 25 €/self,
  c'est acheter 1 kg de cuivre, donc $r \approx 2{,}6\ \Omega$ et **−2,5 dB**
  d'insertion, exactement la self que l'étude thermique disqualifie
  (REFERENCE-TECHNIQUE.md § 05.8 : dérive de +9,6 % de DCR en une minute au
  niveau fort ⇒ échec du critère « robustesse » par construction).
  Chiffres à retenir (§ 05.10, cuivre seul, **pour un couple de selfs de
  18 mH**, sur la base non sourcée de 25 €/kg de fil `[[devis à obtenir]]`) :
  **212 € à $r_{max} = 1\ \Omega$ ; 116 € à 1,5 Ω ; 75 € à 2 Ω ; 41 € à 3 Ω.**
  La fenêtre praticable étant $r_{max} \approx 1{,}5$ à 2 Ω, **compter 75 à
  116 € de cuivre par filtre**, à doubler pour les deux filtres — sauf à
  exploiter les **prises intermédiaires** (§ 05.10 : une seule bobine par voie,
  avec prise, fournit la valeur catalogue *et* la valeur optimisée ; cuivre,
  prix et temps de bobinage divisés par deux, et comparaison sur le **même objet
  physique**, donc sans biais de fabrication). **Le budget ne se fixe donc pas
  avant $r_{max}$** : c'est une décision de phase 0, pas une ligne comptable.
  Reste : condensateurs électrolytiques bipolaires (film réservé à la version
  finale si budget OK).
- **Scope de l'oral (15 min d'exposé + 15 min d'entretien)** : à ~40 s par vue,
  15 min feraient ~22 diapositives, mais la cible retenue est **16 à 18 vues à
  50-55 s** — les 5 min gagnées sur le format v1 servent à montrer les portes de
  validation (étalonnage, résidus, sanity check 8 Ω), pas à ajouter des planches.
  Le détail (self, Monte-Carlo, énergie, listings Python) vit en annexes placées
  après la conclusion et appelées pendant les 15 min d'entretien — elles sont
  hors chronomètre.
- **Pas d'invention de résultats** : tout chiffre non mesuré reste un placeholder
  explicite, comme en v1.
