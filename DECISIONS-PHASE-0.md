# Décisions de phase 0 — registre des choix gelés

> **Registre ouvert le 2026-09-13.** Ce fichier est le seul endroit du dépôt où
> une décision de cadrage est *gelée*. Il est destiné à être rempli, daté et
> signé par Thomas. Tant qu'une décision y porte `[[à remplir]]`, elle n'est pas
> prise — et la porte de validation de la phase 0 reste fermée.

## La règle du jeu

1. **Une décision inscrite ici est gelée.** À partir de sa date de signature,
   elle ne se rediscute plus dans les autres fichiers : `FEUILLE-DE-ROUTE.md`,
   `REFERENCE-TECHNIQUE.md`, `NOTES-TIPE.md`, `MCOT.md` et les supports la
   *citent*, ils ne la *redéfinissent* pas.
2. **Toutes les décisions doivent être gelées avant la première mesure
   comparative** (phase 4, comparaison catalogue / optimisé / actif). Les
   décisions D1, D2, D4, D5 doivent l'être plus tôt encore : elles entrent dans
   la fonction de coût de la phase 3. D7 et D8 doivent l'être avant la première
   figure et avant le premier ajustement.
3. **Une décision peut être changée** — la science n'est pas une promesse. Mais
   tout changement doit être : (a) inscrit dans le *Journal des modifications*
   en fin de fichier, (b) **daté**, (c) **justifié par un argument qui ne soit
   pas le résultat obtenu**, et (d) **mentionné à l'oral**. Un jury valorise un
   candidat qui dit « j'ai changé de critère en novembre parce que j'ai compris
   que le premier ne mesurait pas l'effet étudié » ; c'est de l'esprit critique.
4. **Ce qui ruine la comparaison, c'est de changer une décision après avoir vu
   les mesures.** Déplacer une bande, une pondération ou un critère une fois les
   courbes tracées revient à choisir le vainqueur puis à écrire le règlement.
   C'est la seule faute réellement disqualifiante de ce projet, et elle est
   invisible dans un rapport : d'où ce registre daté.
5. **Aucun chiffre non mesuré n'entre ici sans étiquette.** Les conséquences
   chiffrées ci-dessous proviennent de `REFERENCE-TECHNIQUE.md` (section citée à
   chaque fois) et sont **calculées**, sur 8 Ω résistif ou sur un modèle de
   haut-parleur *typique* jamais mesuré. Rien n'a encore été mesuré sur
   l'enceinte de Thomas.

### Comment remplir

Pour chaque décision : lire l'énoncé, comparer les options, puis écrire la
réponse dans le champ `DÉCISION`, la date du jour dans `date`, et les initiales
dans `signé`. Une décision peut être prise *contre* la recommandation : c'est
même l'intérêt du format, à condition d'écrire pourquoi dans le champ `motif`.

### Tableau de bord

| # | Décision | Ce qu'elle commande | À geler avant | Statut |
|---|---|---|---|---|
| D1 | Définition de $f_c$ | Le critère « précision de $f_c$ », la porte ±5 % de la phase 4 | Phase 3 | `[[ouvert]]` |
| D2 | Cible de sommation (Butterworth 2 / LR2) | **La fonction de coût entière**, le câblage, les valeurs de composants | Phase 3 | `[[ouvert]]` |
| D3 | Les deux niveaux d'écoute | Le critère « robustesse », la tenue en tension, la sécurité | Phase 4 | `[[ouvert]]` |
| D4 | Les 8 critères de comparaison | Toute la conclusion du TIPE | 1ʳᵉ mesure comparative | `[[ouvert]]` |
| D5 | Bande et pondérations de la fonction de coût | Le design optimisé lui-même | Phase 3 | `[[ouvert]]` |
| D6 | $r_{max}$ de la self | Le budget cuivre, les pertes, le critère « robustesse » | Achats phase 4 | `[[ouvert]]` |
| D7 | Gabarit 4/3 des figures et des slides | Toutes les figures des phases 2 à 4 | 1ʳᵉ figure | `[[ouvert]]` |
| D8 | Type de caisse du sub (**constat**) | Le modèle à ajuster en phase 2, la sécurité au niveau fort | Phase 1 | `[[ouvert]]` |
| D9 | Filière et positionnements thématiques | Le binôme d'examinateurs | Étape 1 SCEI | `[[ouvert]]` |
| D10 | Professeur encadrant | **La note elle-même** | Rentrée sept. 2026 | `[[ouvert]]` |

---

## D1 — Définition de $f_c$

### Énoncé

Le même filtre admet **quatre** « fréquences de coupure » qui ne coïncident pas
dès que la self a une DCR ou que la charge n'est pas résistive
(REFERENCE-TECHNIQUE.md § 04.1). Tant qu'une seule n'est pas gelée, le critère
« précision de $f_c$ » de `FEUILLE-DE-ROUTE.md` et la porte de validation de la
phase 4 (±5 %) sont inutilisables. Il faut en outre geler la **convention de
seuil** utilisée pour les repères à $-3$ dB.

### Options et conséquences chiffrées

Filtre de référence pour toute cette comparaison : catalogue E12
$L_1 = 18$ mH, $C_1 = 150$ µF, d'où $f_0 = 96{,}86$ Hz et $Q = 0{,}7303$ sur
8 Ω (§ 04.1).

| Option | $f_c$ désigne | Valeur sur 8 Ω, $r=0$ | Quand la DCR passe de 0 à 2 Ω (§ 04.1) | Sur la charge typique (§ 04.2, § 01.8) |
|---|---|---|---|---|
| **A** | le pôle $f_0 = 1/(2\pi\sqrt{L_1C_1})$ | 96,86 Hz | 96,9 → 108,3 Hz (**+11,8 %**) | non défini : la charge n'est pas résistive |
| **B** | le $-3$ dB du passe-bas, rapporté au **0 dB absolu** | 99,93 Hz | 99,9 → 81,5 Hz (**−18 %**) | 104,1 Hz (+4,2 %, § 01.8) |
| **C** | le $-3$ dB du passe-bas, rapporté au **gain de bande** $K$ | 99,93 Hz | 99,9 → 110,3 Hz (**+10 %**) | — |
| **D** | le **croisement des deux voies** : l'unique $f\in[40;250]$ Hz telle que $\lvert H_{PB}G_{sub}\rvert = \lvert H_{PH}G_{med}\rvert$ | 96,86 Hz | 96,86 → 96,05 Hz (**−0,8 %**) | 96,66 → 102,95 Hz (**+6,5 %**) |

Lecture (§ 04.1) : pour une **même réalité physique** — une DCR de 2 Ω —, les
options B et C annoncent $-18\ \%$ et $+10\ \%$. L'écart n'est pas une erreur de
calcul, c'est la convention. L'option D, elle, ne bouge que de 0,8 % : elle
sépare proprement ce que la DCR fait réellement (une **perte d'insertion** $K$
et un déplacement du pôle) d'un déplacement du raccord qui n'a pas lieu.

**Convention de seuil** — les deux couples de valeurs qui circulent dans le
projet ne diffèrent **pas** par un arrondi mais par la convention (revérifié le
2026-09-13 sur une grille de $1{,}5\cdot10^{7}$ points ; contrôle croisé
$f_{PB}\times f_{PH} = f_0^2 = 9381{,}6$ dans les deux cas) :

| Convention de seuil | $-3$ dB passe-bas | $-3$ dB passe-haut |
|---|---|---|
| **Demi-puissance**, $-3{,}0103$ dB (convention de REW et des logiciels de mesure) | **99,93 Hz** | **93,88 Hz** |
| Seuil littéral $-3{,}000$ dB | 99,82 Hz | 93,99 Hz |

> Note de cohérence documentaire **[soldé le 2026-09-13]** : § 04.1 présentait le
> couple 99,8 / 94,0 comme un « arrondi fautif ». C'était inexact — c'est l'autre
> convention de seuil ; `REFERENCE-TECHNIQUE.md` a été corrigé et porte désormais
> les deux conventions. La conclusion de § 04.1 (geler le croisement) est inchangée.

### Recommandation

**Option D (croisement des deux voies), avec la convention de demi-puissance
$-3{,}0103$ dB pour tous les repères $-3$ dB rapportés.** Quatre raisons, toutes
de § 04.1 : (i) c'est la seule définition **insensible à la perte d'insertion**,
une atténuation commune aux deux voies déplaçant les deux « $-3$ dB absolus »
sans rien changer au raccord ; (ii) c'est la seule qui **reste interprétable sur
la charge réelle**, où $\lvert H\rvert$ culmine à $+10{,}8$ dB et où un seuil à
$-3{,}01$ dB tombe 14 dB sous le pic sans plus rien désigner de physique ;
(iii) c'est **la grandeur qui gouverne la somme acoustique**, donc le critère
« fidélité du raccord » ; (iv) elle **se mesure directement** : deux balayages
de Bode, on lit l'intersection.

Le pôle $f_0$, le $-3$ dB/0 dB et le $-3$ dB/$K$ restent **cités comme repères**
— ils sont utiles, en particulier $f_0$ pour la propagation d'incertitude — mais
aucun n'est « la définition retenue ».

### Ce que la décision déclenche (une fois signée)

- ~~Aligner la convention **C1** de `REFERENCE-TECHNIQUE.md § 07.0`~~ —
  **fait le 2026-09-13** : § 07.0, § 07.7, § 08.5 et le bloc « retenir » de la
  section 07 désignent désormais le croisement, les autres fréquences étant des
  repères nommés. Il reste à **dater et signer** la décision ci-dessous.
- Aligner `FEUILLE-DE-ROUTE.md` (lignes « Définition de $f_c$ » de la phase 0 et
  de la phase 4).
- Reformuler la porte de validation de la phase 4 : ±5 % **sur le croisement**,
  prédit avec les valeurs **mesurées** de $L$ et $C$ (voir D6 et l'incertitude
  ci-dessous).

**Rappel d'incertitude à écrire par couple, jamais en nombre seul** (§ 04.9) :
$u(f_0)/f_0 = \tfrac12\sqrt{(u_L/L)^2 + (u_C/C)^2}$, soit pour $L$ et $C$ à
±10 % : **7,1 % en borne au pire cas** et **4,1 % en incertitude-type** (loi
rectangulaire, convention GUM — c'est celle qui se compare au Monte-Carlo).

> **DÉCISION : [[à remplir]]** — date : `[[JJ/MM/AAAA]]` — signé : `[[TM]]`
> — motif si l'option retenue diffère de la recommandation : `[[...]]`

---

## D2 — Cible de sommation : Butterworth 2 ou somme plate (Linkwitz-Riley 2) ?

### Énoncé

**C'est la décision la plus structurante du registre : elle commande la fonction
de coût, donc le design optimisé lui-même, donc les composants achetés.** Il
existe aujourd'hui une **incohérence à lever** dans le dépôt (§ 04.3) :
`FEUILLE-DE-ROUTE.md` écrit « écart RMS de la somme des deux voies **à la cible
plate** » (critère « fidélité du raccord ») et « cible : somme des deux voies
**plate** » (phase 3) — ce qui désigne LR2. Mais le *sanity check* de la phase 3
et toutes les illustrations de `REFERENCE-TECHNIQUE.md` utilisent la cible
**Butterworth**, héritée de la v1. Les deux ne peuvent pas être gelées ensemble.

### Options et conséquences chiffrées (§ 04.3, `verif_sommation.py`)

| | **Butterworth 2** ($Q = 1/\sqrt2$) | **Linkwitz-Riley 2** ($Q = 1/2$) |
|---|---|---|
| $\lvert H\rvert$ de chaque voie à $f_c$ | $-3{,}01$ dB | $-6{,}02$ dB |
| Somme, même polarité | $\lvert S\rvert = 0$ : **trou** | trou |
| Somme, **une voie inversée** | $\sqrt2$ → **+3,01 dB** à $f_c$, +1,68 dB à 50 et 200 Hz | $S = \dfrac{1+x^2}{(1+jx)^2}$ → **0,000 dB partout** |
| Écart de phase entre voies | 0° **à $f_c$ seulement** | 0° **partout** ($H_{PB}$ et $-H_{PH}$ colinéaires) |
| Écart RMS de la somme inversée à une cible **plate**, 40–250 Hz | **2,29 dB** — ce n'est pas un défaut, c'est sa signature | 0 dB par construction |
| Valeurs sur 8 Ω | $L = \sqrt2R/\omega_0 = 18{,}01$ mH, $C = 140{,}7$ µF → E12 **18 mH / 150 µF** | $L = R/(Q\omega_0) = 25{,}5$ mH, $C = Q/(\omega_0R) = 99{,}5$ µF → E12 **27 mH / 100 µF** |
| Inversion de polarité | **obligatoire** | **obligatoire** |

Deux remarques qui pèsent dans le choix :

- Les deux couples E12 ont **le même produit $LC$** (18 × 150 = 27 × 100), donc
  le **même pôle** $f_0 = 96{,}9$ Hz : passer de l'un à l'autre ne déplace pas
  le raccord, cela change le **$Q$**, c'est-à-dire la forme.
- Une cible LR2 vaut aussi **plus de cuivre** : 27 mH au lieu de 18 mH sur la
  voie grave, dans un régime où la masse de cuivre suit
  $m^\star = K_{Cu}(L/r_{max})^{3/2}$ (§ 05.8). Le lien avec D6 est direct.
- **Perspective écartée** : LR4 (= B2²) somme à plat **sans** inversion, mais
  demande 4 gros composants par voie en passif — trivial en actif par cascade.
  C'est un argument d'oral, pas un design à construire (§ 04.3).

**Mise en œuvre de l'inversion**, pour l'expérimentateur : permuter les deux
fils d'un des deux haut-parleurs. Obligatoire au 2ᵉ ordre, **interdite** en LR4.
À re-vérifier au micro après câblage : à $f_c$, le bon sens donne une bosse, le
mauvais un trou profond — c'est le test le plus rapide et le plus lisible de
toute la phase 4 (§ 04.3, § 07.5).

### Recommandation

**Option LR2 (somme plate), et amender `REFERENCE-TECHNIQUE.md` et le squelette
Python en conséquence.** Motifs : (a) c'est déjà ce qu'écrivent les deux lignes
de `FEUILLE-DE-ROUTE.md` qui portent le critère n° 1, donc le moins de fichiers
à corriger ; (b) une cible **plate** rend le critère « fidélité du raccord »
directement lisible — un écart RMS à une cible plate se compare à zéro, sans
avoir à retrancher une bosse de +3 dB théorique ; (c) l'écart de phase nul
**partout** (et pas seulement à $f_c$) rend le résultat beaucoup plus robuste au
retard $\tau$ entre haut-parleurs non colocalisés, qui est une inconnue du
projet ([[à mesurer]] au mètre ruban, § 04.2).

**Réserve à assumer si LR2 est retenu** : le *sanity check* de la phase 3 (« sur
8 Ω résistif, l'optimiseur doit retomber sur le filtre catalogue ») change de
cible. Il devra vérifier le retour sur **27 mH / 100 µF**, et non sur
18 mH / 150 µF. C'est une ligne de code et une ligne de feuille de route, mais
l'oublier ferait échouer la porte de validation pour une mauvaise raison.

Si au contraire **Butterworth** est retenu (continuité avec la v1, filtre déjà
décrit dans tous les supports), alors il faut *amender* les deux lignes de
`FEUILLE-DE-ROUTE.md` citées plus haut **avant** le gel, et écrire partout que
la cible de la somme est « Butterworth inversé, +3,01 dB à $f_c$ », dont l'écart
RMS à plat de 2,29 dB est la **signature attendue**, pas une erreur.

> **DÉCISION : REPORTÉE APRÈS LA PHASE 1** — date : `13/09/2026` — décidée par : Thomas
> — motif : la cible sera choisie au vu de la $Z(f)$ réellement mesurée plutôt que sur le
> modèle typique. Ce report est lui-même une décision datée, et il est recevable devant le
> jury : on ne fige pas un cahier des charges sur une charge supposée.
>
> **Conséquence technique, à respecter dès maintenant.** Le report ne doit pas bloquer la
> phase 3 : la cible est donc un **paramètre** du code, pas une constante. `analyse/optim.py`
> expose `cible_nom={'butterworth'|'lr2'|'plate'}` (nom retenu dans le code ; un garde-fou
> refuse explicitement `cible=` avec le bon nom en message) et la fonction de coût est
> évaluable sur chacune ; le *sanity check* sur charge $8\ \Omega$ résistive est exécuté pour les deux cibles
> (retour attendu : 18 mH / 141 µF en Butterworth, 25,5 mH / 99,5 µF en LR2).
>
> **Échéance ferme.** La décision doit être prise et datée ici **avant le premier achat de
> composants** (le choix change la self : 18 mH contre 27 mH, donc la masse de cuivre et le
> prix) et **avant la rédaction du MCOT** (nov.-déc. 2026), qui décrit la démarche.
>
> **À vérifier au passage** : l'incohérence de `FEUILLE-DE-ROUTE.md` (critère « fidélité »
> et phase 3 écrivent « cible plate ») reste ouverte tant que D2 n'est pas tranchée — les
> deux occurrences portent désormais un renvoi explicite vers cette décision.

---

## D3 — Les deux niveaux d'écoute de référence

### Énoncé

Fixer un niveau « faible » et un niveau « fort », qui serviront au critère
« robustesse » (dérive thermique entre les deux) et à toutes les mesures des
phases 1 et 4. Il faut fixer **où** se définit un niveau, **sa valeur en
tension**, et **la puissance moyenne correspondante**.

### Où se définit un niveau (convention C5, § 07.0 et § 07.8)

**Tension efficace mesurée au multimètre, sur une sinusoïde à 100 Hz,
directement aux bornes du haut-parleur** — *pas* à la sortie de l'ampli. Ce
point n'est pas cosmétique : en passif, la tension de sortie de l'ampli est **en
amont du filtre** et le haut-parleur en voit moins ($-3$ dB au raccord, plus les
pertes DCR) ; en bi-amplification, la sortie de l'ampli **est** la tension aux
bornes du haut-parleur. Définir le niveau à la sortie de l'ampli donnerait donc
moins de puissance au passif qu'à l'actif — biais direct sur un critère qui
mesure précisément un effet thermique. La tension de commande de l'ampli
devient une **conséquence**, différente pour chaque filtre, et on la consigne.

*Alternative acceptable si elle est écrite ici* : égaliser sur le niveau
acoustique en champ proche à 100 Hz.

### Options et conséquences chiffrées (§ 07.8, § 07.11, § 04.2, § 04.5)

| Niveau | Tension aux bornes du HP | $P$ sur 8 Ω | SPL en champ proche¹ | Énergie d'un balayage de 5,46 s | Remarque |
|---|---|---|---|---|---|
| **faible** | 2 V eff | 0,5 W | **112 dB** | 2,7 J → **< 1 K** : la bobine ne chauffe pas | Bouchons **déjà obligatoires** |
| **fort (a)** | 9 V eff | 10 W | 125 dB | ~55 J | = le $P_{ref}$ de la fonction de coût (§ 04.5) |
| **fort (b)** | 20 V eff | 50 W | 132 dB | **273 J** → +11 K (bobine 60 g) à +68 K (bobine 10 g) | Plafonné par le SPL max du micro [[à vérifier]] |

¹ Sensibilité supposée 95 dB/2,83 V/m — **ordre de grandeur typique, non mesuré**.

**Ce que le niveau fort décide.** Le cuivre suit
$R_e(T) = R_e(T_0)[1 + \alpha(T-T_0)]$ avec $\alpha = 3{,}93\cdot10^{-3}$ K⁻¹ :
+4 % pour +11 K, +8 % pour +20 K, +20 % pour +50 K (§ 07.8). Un niveau fort trop
bas rend le critère « robustesse » **non discriminant** ; un niveau fort trop
haut fait que **le balayage lui-même fait dériver $Z(f)$** pendant qu'on le
mesure. D'où le protocole obligatoire : $R_e$ relevée en **quatre fils** avant
et après chaque balayage fort, chronomètre déclenché à l'arrêt du signal, trois
lectures extrapolées à $t = 0$ ; l'écart fait partie du résultat.

### Contraintes de sécurité — non négociables (§ 07.11, § 04.2)

- **Surtension du LC sur la charge réelle.** Le composant shunt voit
  $\lvert V\rvert/V_{in}$ croissant avec $\lvert Z\rvert$ : ×1,00 sur 8 Ω, ×1,39
  sur 14 Ω, ×2,79 sur 30 Ω, ×4,59 sur 50 Ω, **×5,50 sur 60 Ω** (maximum sur
  20–300 Hz, calculé sur 18 mH / 150 µF). Au niveau fort de **20 V eff sur
  $\lvert Z\rvert = 50$ Ω, cela fait 92 V eff, soit 130 V crête** aux bornes
  d'un composant. À pleine puissance ampli, le majorant monte à **218 V crête**
  sur $C_1$ (§ 04.2). Règle : tant que $Z(f)$ n'est pas mesurée, marge ×6 →
  condensateurs **250 V DC / 160 V AC minimum**, et vérifier que la
  spécification lue est bien la tension **alternative permanente** (sur un MKP,
  un « 100 V » est presque toujours du continu ; la tenue en alternatif
  permanent est typiquement 60 à 65 V eff). **Les « 100 V » de la v1 sont
  insuffisants.**
- **Bass-reflex** (voir D8) : au niveau fort, **aucun contenu sous l'accord** —
  `Start` REW $\ge 2f_B$. Sous $f_B$ la membrane n'est plus chargée et le
  débattement explose ; un 18″ est typiquement accordé vers 30–40 Hz.
  Vérification visuelle du débattement avant chaque balayage fort.
- **Oreilles** : bouchons obligatoires **y compris au niveau faible** (112 dB
  SPL en champ proche dès 0,5 W), personne dans l'axe pendant les balayages
  forts, pas de tête à moins de 1 m du 18″.
- **Limiteur du E-800** : il reste enclenché comme filet de sécurité, **mais un
  limiteur qui agit rend la chaîne non linéaire et invalide la mesure de
  fonction de transfert**. Toute mesure pendant laquelle la LED limit/clip
  s'allume est écartée et refaite plus bas ; l'état de la LED est consigné pour
  chaque balayage. Idéalement, régler le niveau « fort » 3 dB sous le seuil
  d'action constaté.
- **Ordre des amplitudes** : toujours du faible vers le fort, et toujours le
  test sur résistance 8 Ω avant le haut-parleur.

### Recommandation

**Faible = 2 V eff (0,5 W/8 Ω) ; fort = 9 V eff (10 W/8 Ω)**, aux bornes du
haut-parleur, sinus 100 Hz. Motif : 9 V aligne le niveau fort sur le
$P_{ref} = 10$ W déjà utilisé par le terme de pertes de la fonction de coût
(§ 04.5), ce qui évite d'avoir deux puissances de référence dans le mémoire ;
et 125 dB en champ proche reste sous le SPL maximal d'un micro de mesure
courant, là où 132 dB ne l'est probablement pas.

**Conditionnement thermique associé, à geler avec** : bruit rose au niveau fort
pendant une durée fixée — proposition **5 min** — avant les balayages « bobine
chaude », $R_e$ relevée avant et après (§ 07.8, étapes 2b/2c).

**Honnêteté à préparer dès maintenant** (§ 07.8) : 10 W sur un 18″ professionnel
est une fraction faible de sa puissance admissible, et la dérive attendue peut
produire sur le critère un écart **plus petit que le seuil de répétabilité**. On
simule donc **avant la session**, avec le modèle T-S de la phase 2, l'écart RMS
prédit pour $R_e$, $1{,}08\,R_e$ et $1{,}20\,R_e$ ; si l'écart prédit est sous le
seuil de départage, on l'annonce **avant** de mesurer et la mesure servira à
poser une **borne supérieure**, pas à trancher. Dire cela à l'oral vaut mieux
que de monter le niveau après coup pour « faire sortir » un effet.

> **DÉCISION — niveau faible : [[à remplir]] V eff ([[...]] W)**
> **niveau fort : [[à remplir]] V eff ([[...]] W)**
> **conditionnement : [[...]] min de bruit rose**
> date : `[[JJ/MM/AAAA]]` — signé : `[[TM]]`

---

## D4 — Les huit critères de comparaison

### Énoncé

Geler la liste des critères, leur définition et leur poids relatif. **Aucun
critère ne doit être ajouté ou retiré après les premières mesures
comparatives** : c'est ce qui rend la conclusion honnête. Le bon moment pour
amender la liste, c'est **maintenant**.

### La liste à geler (reprise de `FEUILLE-DE-ROUTE.md`)

| # | Critère | Définition | Moyen de mesure | Statut proposé |
|---|---|---|---|---|
| 1 | **Fidélité du raccord** | Écart RMS (dB) de la somme des deux voies à la cible (D2), bande 40–250 Hz, protocole § 07.9 | Micro + REW, champ proche | **Principal** |
| 2 | Précision de $f_c$ | $\lvert f_c$ réalisée $- 100$ Hz$\rvert$, $f_c$ au sens de D1 | Bode électrique puis acoustique | **Déclassé** (voir ci-dessous) |
| 3 | Pertes d'insertion | dB et W perdus en bande passante à puissance donnée | $V$/$I$ au banc, DCR | Principal |
| 4 | Consommation au repos | W de la chaîne complète sans signal | Wattmètre de prise | Principal |
| 5 | Coût marginal | € de composants, ampli existant considéré acquis | Factures | Principal |
| 6 | Coût système | € du système complet équivalent (scénario stéréo) | Devis | Principal |
| 7 | Encombrement / matière | Masse (kg) et volume (L) du filtre, cuivre utilisé | Balance, mètre | Principal |
| 8 | Robustesse | Dérive de $f_c$ et de l'écart RMS entre les deux niveaux gelés (D3) | Mesures aux 2 niveaux | Principal |

### Le point établi par l'audit : le critère n° 2 ne mesure presque pas l'effet étudié

Sur la charge réelle, la grandeur sensible **n'est pas $f_c$, c'est la forme de
la réponse**. Chiffres (§ 01.8, filtre catalogue E12, charge en caisse close
$\alpha = 1$, pic d'impédance dans la bande) :

| Grandeur | Sur 8 Ω résistifs | Sur la charge réelle |
|---|---|---|
| $-3$ dB du passe-bas | 99,9 Hz | 104,1 Hz (**+4,2 %**) |
| $f_c$ au sens du croisement (§ 04.2, charge typique, $r = 1$ Ω) | 96,66 Hz | 102,95 Hz (**+6,5 %**) |
| Gain maximal en bande | 0 dB | **+14,4 dB à 73 Hz** |
| Écart RMS sur 40–250 Hz | — | **4,7 dB** |

Autrement dit : le critère n° 2 bouge de **quelques pour cent** là où le critère
n° 1 bouge de **plusieurs décibels**. **L'effet étudié vit dans le critère
n° 1.** Et le résultat est encore plus net en incertitude (§ 04.9) : sur $f_c$,
la charge (+6,5 %) et les tolérances de composants (7,1 %) pèsent **du même
ordre** — il est donc **faux** de dire que $Z(f)$ domine sur ce critère-là. Sur
la forme, en revanche, l'écart RMS passe de 0,46 dB (8 Ω) à 4,29 dB (charge
typique), soit +3,8 dB, quand *toutes* les sources d'incertitude réunies ne le
dispersent que de ±0,26 dB : un facteur 15. La formulation qui résiste à un jury
est celle-là : **$Z(f)$ est un biais, les tolérances sont une dispersion** — un
biais ne s'annule pas en moyenne et ne se corrige qu'en le mesurant puis en
optimisant dessus.

**Mais le critère n° 2 ne doit pas être supprimé** : § 01.8 établit qu'il garde
tout son sens **comme révélateur de la DCR**, et non de $Z(f)$. Sur 8 Ω, une DCR
de 1 Ω déplace le $-3$ dB rapporté à la bande passante de $+5{,}5$ %, pour une
perte d'insertion de $-1{,}02$ dB.

### Recommandation

Geler les **huit** critères, avec **trois amendements**, tous inscrits
maintenant :

1. **Déclasser le critère n° 2** en indicateur secondaire, et le renommer pour
   dire ce qu'il mesure vraiment : « précision de $f_c$ — **révélateur de la
   résistance série**, non de $Z(f)$ ».
2. **Ajouter au critère n° 1 l'écart maximal à la cible (dB)** :
   $\max_k \lvert \tilde L(f_k) - \bar{\tilde L}\rvert$. Coût nul — § 07.9
   prescrit déjà de le rapporter — et il capte ce qu'un RMS dilue : *« un trou
   étroit au raccord pèse peu dans un RMS »*. C'est la grandeur qui, sur charge
   réelle, passe à +14,4 dB.
3. **Geler la définition complète du critère n° 1** telle que § 07.9 l'écrit,
   sans y revenir ensuite :

| Élément du critère n° 1 | Valeur gelée (§ 07.9, § 07.0) |
|---|---|
| Bande | **40–250 Hz** (C3) |
| Grille | logarithmique, **24 points/octave**, soit $N = 64$ |
| Niveau de référence | $L_0$ = moyenne sur la bande (le niveau absolu est libre, **la forme seule est jugée**) |
| **Plancher** $\Lambda$ | **20 dB** sous le maximum de bande, appliqué **avant** tout calcul |
| Arrondi | **0,1 dB** (C4) |
| Répétitions | **3** par configuration |
| Seuil de départage | $t_{0{,}975;4}\,s\sqrt{2/n} \approx 2{,}3\,s$ ; en deçà, on écrit « non départagés » **et on le dit à l'oral** |

Le plancher $\Lambda$ n'est pas un détail : sans lui, un zéro de transmission
dans la bande rend l'estimateur discret erratique — la même courbe analytique
donne **1027 dB** à 12 pts/octave, 7,3 dB à 24 pts/octave et **375 dB** à
96 pts/octave, contre 6,0 / 5,9 / 5,9 dB avec le plancher. Le choix de $\Lambda$
n'est pas neutre non plus (15 dB → 5,0 dB ; 20 dB → 5,9 dB ; 30 dB → 7,0 dB),
d'où le gel. **À vérifier en phase 0** : que le plancher de bruit effectif de la
mesure soit bien à plus de 20 dB sous le niveau de bande ; sinon le critère est
déclaré « saturé » et on le dit.

**Règle de câblage attachée au critère** (§ 07.8, la plus importante de la
section) : dans un filtre passif parallèle du 2ᵉ ordre, les deux branches se
chargent mutuellement et forment ensemble la charge réelle. **Toutes les
branches et tous les haut-parleurs restent connectés en permanence ; entre deux
mesures, on ne déplace que le micro.** Débrancher la voie médium pour mesurer le
sub introduirait une erreur systématique, silencieuse, et portant exactement sur
l'objet du TIPE.

> **DÉCISION : [[à remplir]]** (liste des 8 critères gelée telle quelle / avec
> les amendements 1-2-3 / autre : préciser)
> date : `[[JJ/MM/AAAA]]` — signé : `[[TM]]`

---

## D5 — Bande et pondérations de la fonction de coût

### Énoncé

La fonction de coût de la phase 3 (§ 04.5) s'écrit

$$
J(\mathbf{x}) = w_s\,\mathrm{RMS}_{dB}(S, S^c) + w_v\,\big[\mathrm{RMS}_{dB}(H_{PB},H^c_{PB}) + \mathrm{RMS}_{dB}(H_{PH},H^c_{PH})\big] + w_\varphi\,\mathrm{RMS}_{deg}(\Delta\varphi,\Delta\varphi^c) + w_€\,\text{Prix} + w_W\,P_{Joule}
$$

Il faut geler : la **bande** d'évaluation, la **grille**, l'**hypothèse
implicite de pondération**, et les **cinq pondérations**.

### Option A — la bande

La bande proposée est 40–250 Hz, grille log-espacée de 64 points (≈ 1/24
d'octave), sous-bande 70–140 Hz pour le terme de phase. **§ 04.8 montre que
l'optimum dépend directement de cette borne haute** :

| Bande de coût | Optimum trouvé | $J$ |
|---|---|---|
| **40–250 Hz** | 27 mH / 10 µF \| 120 µF / 12 mH | 11,04 |
| 40–400 Hz | 33 mH / 10 µF \| 120 µF / 12 mH | 10,43 |
| 40–800 Hz | 33 mH / 10 µF \| 120 µF / 12 mH | 11,59 |
| 40–1600 Hz | **22 mH / 82 µF** \| 120 µF / 15 mH | 11,49 |

Sur 40–250 Hz, $C_1$ **tombe sur la borne basse de la grille** (10 µF ≈ absence
de condensateur) : l'optimiseur signale que sur cette charge la cellule sub tend
vers un **1ᵉʳ ordre**, et viole donc la contrainte « ordre 2 ». L'enjeu n'est pas
cosmétique : 27 mH + 10 µF donne $-15{,}3$ dB à 250 Hz (contre $-15{,}1$ dB pour
27 mH seul) mais **$-22{,}6$ dB à 1 kHz contre $-39{,}8$ dB pour le catalogue**.
Un 18″ qui rayonne encore à $-23$ dB dans sa zone de rupture est un défaut
acoustique réel, **invisible** pour une bande de coût arrêtée à 250 Hz. $C_1$ ne
quitte la butée qu'à partir d'une bande étendue à 1,6 kHz.

Trois remèdes possibles, à trancher :

| Option | Conséquence |
|---|---|
| **A1** — garder 40–250 Hz et **imposer un plancher dur sur $C_1$** (contrainte « ordre 2 » explicite) | Le plus simple ; la bande de coût reste identique à la bande du critère mesuré (C3, § 07.0), qui est elle-même bornée par la validité du champ proche ($\le 280$ Hz pour le 18″) |
| **A2** — élargir la bande de coût à **40–1600 Hz** | L'optimiseur trouve tout seul un vrai 2ᵉ ordre ; mais on **optimise sur une bande plus large que celle où l'on juge**, ce qui doit être déclaré à l'oral |
| **A3** — A1 **et** A2 | Ceinture et bretelles ; l'optimum ne dépend plus d'un choix implicite |

### Option B — les cinq pondérations (§ 04.5)

| Poids | Valeur proposée | Équivalence lisible | Réserve documentée |
|---|---|---|---|
| $w_s$ | **1 dB/dB** | fidélité de la somme (critère n° 1) | — |
| $w_v$ | **1 dB/dB** | forme de chaque voie (protection des médiums, pente du sub) | **Indispensable** : sans lui ($w_v = 0$), la somme seule est dégénérée — une somme plate s'obtient par un LR2 à *n'importe quelle* fréquence, et sur charge réelle par « tout au sub » |
| $w_\varphi$ | 0,05 dB/° (20° ≡ 1 dB) | robustesse hors axe / HP non colocalisés | **Sur-pénalisant d'un facteur ≈ 8** : sur l'axe, 20° entre deux voies d'amplitude égale ne coûtent que 0,13 dB (45° → 0,69 dB ; 90° → 3,01 dB). Le bon calibrage se dérive du décalage acoustique **mesuré** : 0,50 m entre centres → 52° à 100 Hz → 0,93 dB → $w_\varphi \approx 0{,}018$ dB/° |
| $w_€$ | **0,04 dB/€** (25 € ≡ 1 dB) | critère « coût marginal » | — |
| $w_W$ | **1 dB/W** à $P_{ref} = 10$ W | critère « pertes d'insertion » | $P_{ref} = 10$ W est une **puissance conventionnelle sur 8 Ω** ($V_{ref} = 8{,}94$ V), pas la puissance réellement délivrée. Sur la charge réelle, le filtre catalogue dissipe 2,20 W pour ce $P_{ref}$, soit 22 % — cohérent avec l'ordre de grandeur du phénomène |

### Option C — l'hypothèse implicite à énoncer (§ 04.5)

La grille $f_k$ est **log-espacée** : moyenner dessus revient à supposer une
excitation à **énergie constante par fraction d'octave** (bruit rose), et non
par hertz (bruit blanc). Ce choix pondère lourdement le grave et **change le
classement des designs**. Il est défendable — le contenu musical réel est plus
proche du rose que du blanc — mais il doit être **énoncé**, ici et à l'oral.

### Recommandation

- **Bande : option A3.** Plancher dur sur $C_1$ (contrainte « ordre 2 »
  explicite, qui est de toute façon une contrainte du cahier des charges et pas
  une préférence) **et** bande de coût élargie à **40–1600 Hz pour le seul terme
  de forme de la voie sub** $w_v$, en gardant 40–250 Hz pour le terme de somme
  $w_s$ (qui est la bande du critère mesuré). Coût : trois lignes de code.
  Bénéfice : l'optimum ne dépend plus d'un choix de bande non justifié, et le
  défaut acoustique à 1 kHz devient visible pour l'optimiseur.
- **Pondérations** : $w_s = 1$, $w_v = 1$, $w_€ = 0{,}04$ dB/€, $w_W = 1$ dB/W à
  $P_{ref} = 10$ W ; **$w_\varphi$ recalibré sur le $\tau$ mesuré** — à mesurer
  au mètre ruban entre le centre du 18″ et celui du bloc médiums
  ([[à mesurer — cinq minutes, à faire dès maintenant]]), valeur par défaut
  0,018 dB/° si $\tau$ correspond à 0,50 m.
- **Énoncer l'hypothèse « bruit rose »** dans le mémoire et dans les notes de
  l'oral.
- **Protection des médiums : rendre le terme unilatéral sous $f_s$ des
  médiums** (§ 04.5). Le $\mathrm{RMS}_{dB}$ est une métrique à deux côtés qui
  pénalise autant « protège trop » que « protège pas assez » : l'optimum
  120 µF / 12 mH est **pénalisé de 5,4 dB pour mieux protéger les médiums que la
  cible** ($-21{,}4$ dB à 40 Hz contre $-16{,}0$ visés), tandis que le catalogue
  est pénalisé de 4,4 dB pour les sous-protéger. Une métrique qui met ces deux
  cas sur le même plan ne peut pas porter la raison d'être du raccord. Correction
  (trois lignes) : contrainte dure $\lvert H_{PH}\rvert \le \lvert H^c_{PH}\rvert$
  sous $f_s$, RMS à deux côtés conservé en bande passante.

> **DÉCISION — bande : [[à remplir]]** · **pondérations : [[à remplir]]**
> · **hypothèse bruit rose énoncée : [[oui/non]]** · **protection unilatérale :
> [[oui/non]]** — date : `[[JJ/MM/AAAA]]` — signé : `[[TM]]`

---

## D6 — $r_{max}$ de la self

### Énoncé

Choisir la résistance série maximale admissible d'une self de grave. Ce seul
nombre commande **la masse de cuivre, le prix, les pertes, l'échauffement et le
critère « robustesse »** — et, comme le montre § 05.10, une « enveloppe
budgétaire » est en réalité un choix de DCR déguisé.

### Conséquences chiffrées (§ 05.8, § 05.10)

À $L$ fixé, l'optimum sature toujours la contrainte de pertes ($r^\star = r_{max}$)
et la masse minimale vaut $m^\star = K_{Cu}(L/r_{max})^{3/2}$. Pour une self de
**18 mH**, forme de Brooks, cuivre à **25 €/kg** — *ordre de grandeur non sourcé*,
les distributeurs français consultés ne publiant aucun prix au kg
([[à remplacer par un devis avant l'achat de la phase 4]] ; tous les montants en
€ lui sont **strictement proportionnels**) :

| $r_{max}$ (Ω) | $d$ fil (mm) | masse (kg) | prix/self (€) | prix d'un **couple** (€) | insertion /8 Ω | $J$ (A/mm²) | $\Delta T$ 1 min à 350 W | dérive de DCR |
|---|---|---|---|---|---|---|---|---|
| 0,50 | 2,92 | 11,63 | 291 | — ¹ | $-0{,}53$ dB | 0,99 | +0,3 K | +0,1 % |
| 0,75 | 2,27 | 6,38 | 160 | — ¹ | $-0{,}78$ dB | 1,64 | +0,8 K | +0,3 % |
| 1,00 | 1,90 | 4,17 | 104 | **212** | $-1{,}02$ dB | 2,34 | +1,6 K | +0,6 % |
| **1,50** | 1,48 | 2,30 | 57 | **116** | $-1{,}49$ dB | 3,86 | +4,5 K | +1,7 % |
| **2,00** | 1,24 | 1,51 | 38 | **75** | $-1{,}94$ dB | 5,50 | +9,1 K | +3,6 % |
| 3,00 | 0,96 | 0,83 | 21 | **41** | $-2{,}77$ dB | 9,05 | **+24,5 K** | **+9,6 %** |

¹ La colonne « couple » reprend les quatre montants que § 05.10 donne
explicitement pour **deux** selfs de 18 mH ($r_{max}$ = 1 ; 1,5 ; 2 et 3 Ω) ;
les lignes 0,50 et 0,75 Ω n'y figurent pas et ne sont pas extrapolées ici.
Échauffement **adiabatique** sur 1 min
($\Delta T = P_Jt/(mc_p)$, $c_p = 385$ J/kg/K) : c'est un **majorant**, il
néglige toute évacuation vers l'air.

**Attention au nombre de selfs.** La feuille de route demande d'assembler
**deux** filtres (catalogue et optimisé) : c'est **4 selfs**, pas 2. Scénarios
complets à diamètre de fil fixé (§ 05.10) : **92 €** tout en 1,0 mm (3,69 kg,
DCR 2,83 Ω à 18 mH), **205 €** tout en 1,4 mm (8,20 kg, 1,64 Ω), **480 €** tout
en 2,0 mm (19,18 kg, 0,92 Ω) — ce dernier consomme à lui seul la quasi-totalité
du budget de 500 €, avant condensateurs, $R_{ref}$, wattmètre et carte son.

### Les deux contraintes qui bornent la fenêtre (§ 05.8)

- **En haut** (pertes faibles), c'est l'**approvisionnement** qui bloque :
  $d = 1{,}9$ à 2,9 mm de fil émaillé n'est ni bobinable à la main, ni couramment
  vendu au détail [[à vérifier par devis]]. Ces lignes ne sont pas des designs,
  ce sont des bornes théoriques.
- **En bas** (cuivre économe), c'est la **thermique** qui bloque : à
  $r_{max} = 3$ Ω on est à 9 A/mm², la self encaisse 131 W et dérive de **+9,6 %
  de DCR en une minute** au niveau fort. Le filtre « pas cher » **échoue par
  construction au critère de robustesse** : $f_0$ et l'amortissement du grave ne
  sont plus les mêmes à faible et à fort niveau. C'est le seul endroit du projet
  où la dérive thermique se **prédit** avant de se mesurer.
- Densité de courant admissible pour un conducteur enterré sous ~20 couches :
  **2 à 3 A/mm²** en régime permanent — [[ordre de grandeur à geler ici]].

**Le piège budgétaire, à ne pas reproduire** : la ligne « selfs bobinées maison
≈ 25 €/pièce » de `FEUILLE-DE-ROUTE.md` correspond à 1 kg de cuivre, soit
$r = 2{,}6$ Ω et $-2{,}5$ dB — c'est-à-dire **exactement la self que § 05.8
disqualifie sur la thermique**. Et l'enveloppe « 60 à 150 € » correspond à
$r_{max} \approx 1{,}5$–2,5 Ω. Ce ne sont pas des choix de budget, ce sont des
choix de DCR.

### Recommandation

**$r_{max} = 2{,}0$ Ω**, avec $J \le 3$ A/mm² comme contrainte compagne.
Motifs : c'est la borne haute de la fenêtre praticable établie par § 05.8
($r_{max} \approx 1{,}5$ à 2 Ω), elle tient dans le budget (75 € le couple, ou
~150 € les quatre selfs à 18 mH), le fil de 1,24 mm est bobinable à la main, et
la dérive de DCR de +3,6 % en une minute reste **sous** l'effet thermique du
haut-parleur lui-même (+8 % sur $R_e$ pour +20 K, § 07.8), donc n'écrase pas le
critère de robustesse. Passer à 1,5 Ω coûte 41 € de plus par couple pour gagner
0,45 dB d'insertion — arbitrage défendable si le budget le permet après les
achats de la phase 1.

**Loi d'échelle à retenir et à citer à l'oral** : passer de $-2{,}8$ dB à
$-0{,}5$ dB d'insertion coûte **14 fois plus de cuivre** (0,83 → 11,6 kg).
L'exposant $3/2$ est **ce qui rend le passif structurellement coûteux en matière
dans le grave** — c'est l'argument « sobriété » le plus direct du sujet.

**Thèse à assumer** (§ 05.10) : on bobine à air non pas pour économiser — face à
une self à **noyau** à 18 mH, le DIY à air est plus cher *et* plus résistif —
mais pour (a) la **linéarité** (pas de $L(I)$, pas de dérive de $f_0$ avec le
niveau : c'est précisément le critère « robustesse »), (b) la **maîtrise
métrologique** ($N$, $\ell$, $m$, $r$ tous connus et mesurables), (c) la
**liberté de valeur**. Ne pas prétendre que l'argument est économique.

> **DÉCISION — $r_{max}$ = [[à remplir]] Ω** · **$J_{max}$ = [[à remplir]] A/mm²**
> · **nombre de selfs à bobiner : [[à remplir]]** — date : `[[JJ/MM/AAAA]]`
> — signé : `[[TM]]`

---

## D7 — Gabarit 4/3 des figures et des slides

### Énoncé

Trancher le format de sortie **avant de produire la moindre figure des phases 2
à 4**, sinon elles seront toutes à refaire.

### Ce qui est imposé, et ce qui reste à décider (§ 08.2)

Le SCEI **impose** : diapositives « projetées en **format 4/3 paysage** », PDF
de **5 Mo maximum**, ni vidéo ni audio ni animation, **numérotation de toutes
les diapositives requise**. Aucune marge de manœuvre sur ces points.

| Conséquence | Chiffre |
|---|---|
| Un PDF 16:9 ajusté en largeur sur un écran 4/3 occupe $(9/16)/(3/4)$ de la hauteur | **25 % de hauteur utile perdue** |
| Gabarit de remplacement | **1024 × 768** |
| Emplacements à corriger dans le dépôt | `pre-soutenance.html` l. 784 et `presentation-finale.html` l. 1206 (`width: 1280, height: 720`), `EXPORT-PDF.md` l. 22, 23 et 37 |
| Poids des PDF v1 actuels | 1,88 à 3,01 Mo ; marge restante en lecture conservatrice (5 Mo $= 5\cdot10^6$ o) : **1,99 Mo** |
| Listings Python annexés | ≈ 42 lignes × 131 colonnes en 12 px, ≈ 36 × 112 en 14 px, ≈ 31 × 98 en 16 px ; à ~33 lignes utiles/vue, **250 lignes = 8 vues d'annexe** (hors chronomètre) |

Ce qui **reste à décider ici** : le format de sortie matplotlib du squelette
`analyse/` — § 08.2 demande de « figer dès le squelette le format de sortie
matplotlib (taille en pouces et dpi cohérents avec une zone utile 4/3) » mais ne
fixe pas les valeurs.

### Recommandation

- **Slides : 1024 × 768**, numérotées, export PDF vectoriel via
  `css/blueprint-light.css`, contrôle de la taille du fichier **à chaque
  export** et non seulement au dernier ; figures en vectoriel (PDF/SVG) et non
  en PNG ; photos ré-encodées en JPEG à ≤ 200 ko l'unité.
- **Figures matplotlib : `figsize = (8.53, 6.40)` à `dpi = 120`** pour une
  figure pleine page ($8{,}53 \times 120 = 1024$ ; $6{,}40 \times 120 = 768$),
  et `figsize = (8.53, 3.20)` pour une demi-page. Ce sont des valeurs
  **proposées**, pas des valeurs de référence tirées d'une source : l'exigence
  documentée est seulement « zone utile 4/3 » ; l'essentiel est de figer un
  couple et de ne plus en changer.
- **Couleurs : variables CSS avec repli dans chaque `var()`**, par exemple
  `var(--accent, #5fd0e0)`, faute de quoi un SVG appelé par `<img>` ou
  `background-image` perd toutes ses couleurs (les propriétés personnalisées CSS
  sont propres à un **document**). Injection par marqueur unique et non ambigu
  (`<!--FIG:fig-z-sub-mesure-->`), **jamais** par une regex sur un `aria-label`
  — c'est la panne silencieuse diagnostiquée sur `_gen.py` (§ 09.7).

**Conséquence de terrain à ne pas oublier** (§ 08.2) : l'enceinte, le filtre
bobiné et la self sont des **objets interdits en salle**. Photographier le jig
d'impédance, le bobinage en cours et le filtre monté **avant tout démontage**,
et tenir le cahier de laboratoire daté dès la première mesure — il est à la fois
la matière première du DOT et le seul document papier réellement admis.

> **DÉCISION — gabarit slides : [[à remplir]]** · **figsize/dpi matplotlib :
> [[à remplir]]** — date : `[[JJ/MM/AAAA]]` — signé : `[[TM]]`

---

## D8 — Type de caisse du sub : **un constat, pas un choix**

### Énoncé

**Ce n'est pas une décision de conception : c'est une observation à faire.**
Ouvrir, regarder si l'enceinte a un **évent**, et l'écrire. Trente secondes.
Tant que ce n'est pas fait, la phase 2 ne peut pas démarrer.

### Pourquoi c'est bloquant (§ 01.6, § 01.10, § 04.2, § 07.11)

| | Caisse **close** | **Bass-reflex** |
|---|---|---|
| Allure de $\lvert Z\rvert$ | **un** pic | **deux** pics $f_L < f_b < f_H$, et un **creux à $f \approx f_b$** où $\lvert Z\rvert$ retombe près de $R_e$ |
| Paramètres libres du fit (phase 2) | **5** | **8** (9 si l'on sépare les pertes de caisse) |
| Ce que voit le filtre sur 40–250 Hz | un pic | le **second** pic $f_H$, plus le creux : la charge est **encore moins « 8 Ω »** qu'en clos |
| Sécurité au niveau fort | seuil usuel | **aucun contenu sous l'accord** : `Start` REW $\ge 2f_B$, sous $f_B$ la membrane n'est plus chargée et le débattement explose |

**Le danger précis, et c'est pour cela que le constat passe avant tout le
reste** : un modèle à 5 paramètres ajusté sur des données bass-reflex
**converge en silence** et rend des paramètres faux. Il n'émet aucun message
d'erreur ; le résidu est simplement un peu moins bon. Toute la phase 3 serait
alors optimisée sur une charge qui n'existe pas.

Bonne nouvelle côté code : un **seul** modèle suffit. Le contrôle « évent
inerte » (faire tendre l'impédance de la branche d'évent vers l'infini) redonne
**exactement** la caisse close de même volume — écart maximal
$2{,}5\cdot10^{-7}$ Ω. C'est la bonne façon de coder le fit : un modèle, des
paramètres en plus. *Nuance à ne pas se faire prendre* : un évent
**physiquement bouché** ajoute en outre son propre volume à $V_b$.

Sur les pertes : une courbe engendrée avec deux pertes ($Q_p = 20$, $Q_l = 7$)
est ajustée au mieux par une **perte d'évent seule** $Q_p = 7{,}1$, avec un
résidu de **0,62 dB RMS (2,9 dB au pire)**. Donc : commencer avec **une seule
perte globale**, et n'en ajouter une seconde que si le résidu structuré dépasse
ce seuil.

### À constater et à écrire ici

| Point | Réponse |
|---|---|
| Le sub a-t-il un évent ? | `[[oui / non]]` |
| Si oui : nombre, diamètre, longueur de l'évent | `[[à mesurer]]` |
| Volume interne estimé $V_b$ | `[[à mesurer]]` |
| Câblage exact des deux médiums (série confirmée ?) | `[[à vérifier]]` |
| Écart entre le centre du 18″ et celui du bloc médiums (pour $\tau$, D5) | `[[à mesurer — mètre ruban]]` |
| Modèle du micro de mesure et de la carte son ; SPL max du micro | `[[à documenter]]` |
| Sensibilités des deux voies (dB/W/m) | `[[à mesurer en phase 1]]` |

### Sur « du simple au sextuple »

La problématique du dépôt avançait, jusqu'au 2026-09-13, que l'impédance
« varie du simple au sextuple ». **Ce chiffre n'était pas mesuré et il était
probablement bas** ; il a été retiré au profit de « varie fortement avec la
fréquence » dans CLAUDE.md, FEUILLE-DE-ROUTE.md, MCOT.md et README.md. En effet :
$\lvert Z\rvert_{max}/R_e = 1 + Q_{ms}/Q_{es}$, ce qui donne 21,6 à 23,2 sur les
18″ de datasheet du § 01.13, et le modèle typique donne un rapport max/min de
**19,9** sur 40–250 Hz (§ 01.8). Tant que la phase 1 n'a pas mesuré, écrire
partout « **varie fortement avec la fréquence** », sans chiffre.

> **CONSTAT : [[à remplir]]** — date : `[[JJ/MM/AAAA]]` — signé : `[[TM]]`

---

## D9 — Filière et positionnements thématiques SCEI

### Énoncé

Déclarer la filière exacte (Thomas vient de PTSI : la 2ᵉ année est **PT** ou
**PSI**) et arrêter un premier positionnement thématique. **Le choix est
verrouillé à l'étape 1 SCEI, mi-janvier 2027 — c'est-à-dire en pleine phase 4,
avant les mesures acoustiques. Il doit donc être fait sur le récit prévu, pas
sur les résultats obtenus** (§ 08.3).

### Ce que la règle impose (§ 08.3)

- 1 à 3 positionnements parmi **24 thèmes officiels**, par ordre d'importance
  décroissante, plus **5 mots-clés français + 5 anglais**.
- « Le premier positionnement thématique doit impérativement se situer dans un
  des domaines de rattachement disciplinaire de la filière » : **Physique et
  Sciences industrielles pour PSI et PT**. Le premier positionnement « a une
  importance majeure » : **il détermine le binôme d'examinateurs**.
- Ne pas déclarer « Informatique » en 3ᵉ position « pour avoir utilisé un
  programme de tracé de courbes ».
- L'étape 2 n'autorise que des « ajustements éventuels ».

### Positionnements proposés (§ 08.3)

| Rang | Thème officiel (domaine) | Pourquoi | Remarque |
|---|---|---|---|
| 1 | **Électronique** (Sciences industrielles) | « Électronique analogique (instrumentation, électroacoustique...) [...] filtres, amplificateurs » | Domaine de rattachement PT/PSI : satisfait la règle du premier positionnement |
| 2 | **Mathématiques Appliquées** (Mathématiques) | « Mathématiques de l'optimisation, méthodes locales, heuristiques, globales » | Amène un examinateur compétent sur moindres carrés et optimisation discrète. Alternative : **Autres** (« statistiques [...] erreurs en physique, méthodes monte carlo ») si le Monte-Carlo d'incertitudes prend du poids |
| 3 | **Physique Ondulatoire** — « Acoustique » — **ou Automatique** (SI) — « Identification, Estimation » | Validation au micro / problème inverse | Facultatif : « deux d'entre eux suffisent bien souvent » |

**Attention au piège de classement** : « Électronique » et « Automatique » sont
classés en **Sciences industrielles**, pas en Physique. Le brouillon `MCOT.md`
écrit « Physique — électronique/électrocinétique » : à réaligner sur les
libellés officiels **avant** la saisie.

**Risque à écrire noir sur blanc** : choisir « Électronique » en rang 1 et se
retrouver en juin avec un travail devenu majoritairement acoustique, devant un
binôme d'électroniciens. C'est un argument pour que le récit d'oral garde son
centre de gravité sur le **filtre et sa charge**, l'acoustique n'étant que la
validation.

**Titre** — livrable à part entière, « choisi avec soin et permettant de définir
sans ambiguïté le travail effectué ». Le brouillon `MCOT.md` propose
« Optimisation sous contraintes du filtre de raccord d'une enceinte deux voies
sur sa charge réelle » (15 mots) ; § 08.3 suggère d'y faire entrer les deux
éléments qui font le sujet — la fréquence (100 Hz) et le fait que la charge est
**mesurée** : « Optimisation sous contraintes d'un filtre de raccord à 100 Hz
sur l'impédance mesurée d'une enceinte deux voies ».

**Budgets de mots** (§ 08.3) : MCOT $= 50 + 50 + 50 + 100 + 650 = \mathbf{900}$
mots au total, hors mots-clés et références ; DOT $= 4$ à 8 jalons de 50 mots,
soit **200 à 400** mots.

> **DÉCISION — filière : [[PT / PSI]]** · **positionnement 1 : [[à remplir]]** ·
> **2 : [[à remplir]]** · **3 : [[à remplir]]** · **titre retenu :
> [[à remplir]]** — date : `[[JJ/MM/AAAA]]` — signé : `[[TM]]`

---

## D10 — Professeur encadrant

### Énoncé

Désigner un enseignant encadrant, obtenir son **accord explicite**, et vérifier
qu'il dispose d'un compte sur `lycees.scei-concours.fr`.

### Pourquoi c'est la ligne la plus urgente du registre (§ 08.3, `FEUILLE-DE-ROUTE.md`)

C'est **le seul point du cadre SCEI qui peut coûter la note entière**. Le
professeur encadrant est déclaré à l'**étape 1** (mi-janvier 2027) et doit
valider le travail à l'**étape 3** (~mi-juin 2027, **fenêtre de 8 jours
seulement**), sur son propre compte. Sa validation atteste « un travail
personnel constaté ». En cas de refus ou d'absence de validation : « Le candidat
aura alors un entretien avant son passage en loge » — **note zéro possible**.

Au moment de l'audit, le mot « encadrant » n'apparaissait **dans aucun document
v2 du dépôt** hors `archive-v1/`. Échéance fixée par la feuille de route :
**rentrée septembre 2026** — c'est-à-dire maintenant.

### Les quatre actions, dans l'ordre

| # | Action | État |
|---|---|---|
| 1 | Identifier un enseignant encadrant et obtenir son **accord explicite** | `[[à faire]]` |
| 2 | Vérifier qu'il dispose d'un compte sur `lycees.scei-concours.fr` | `[[à faire]]` |
| 3 | Noter son nom pour la saisie de l'étape 1 (mi-janvier 2027) | `[[à faire]]` |
| 4 | Lui rappeler la fenêtre de validation de l'étape 3 (~mi-juin 2027, 8 jours) | `[[à faire]]` |

**Note de discrétion** (§ 08.2) : les Attendus recommandent de ne pas mentionner
le **nom du lycée** ; rien n'y concerne le nom d'un enseignant, et l'encadrant
est de toute façon déclaré au SCEI. Neutraliser le nom d'un enseignant cité en
source est une **interprétation prudente**, pas une exigence.

> **DÉCISION — encadrant : [[nom à remplir]]** · **accord obtenu le :
> [[JJ/MM/AAAA]]** · **compte SCEI vérifié : [[oui/non]]**
> — date : `[[JJ/MM/AAAA]]` — signé : `[[TM]]`

---

## Porte de validation de la phase 0

> **Règle** : la première mesure **comparative** (phase 4 : catalogue vs optimisé
> vs actif) ne peut pas commencer tant qu'une case reste décochée. Les mesures
> d'**étalonnage** de la phase 1, elles, peuvent et doivent commencer dès que D8
> et D10 sont faits — elles ne comparent rien, elles qualifient la chaîne.

### Cases à cocher

- [ ] **D1** — Définition de $f_c$ gelée, avec sa convention de seuil ; répercutée
      dans `FEUILLE-DE-ROUTE.md` et dans la convention C1 de
      `REFERENCE-TECHNIQUE.md § 07.0`.
- [ ] **D2** — Cible de sommation gelée ; l'incohérence entre
      `FEUILLE-DE-ROUTE.md` (cible plate) et `REFERENCE-TECHNIQUE.md`
      (illustrations Butterworth) est **levée**, dans un sens ou dans l'autre ;
      le *sanity check* de la phase 3 vise la bonne cible.
- [ ] **D3** — Deux niveaux d'écoute gelés (tension aux bornes du HP, puissance
      correspondante, durée de conditionnement) ; tenue en tension des
      condensateurs vérifiée pour ces niveaux ; protections auditives présentes.
- [ ] **D4** — Les huit critères gelés, avec la définition complète du critère
      n° 1 (bande, grille, plancher $\Lambda$, arrondi, répétitions, seuil de
      départage).
- [ ] **D5** — Bande, grille, hypothèse « bruit rose » et cinq pondérations
      gelées ; $\tau$ mesuré au mètre ruban et $w_\varphi$ recalibré dessus.
- [ ] **D6** — $r_{max}$ et $J_{max}$ gelés ; nombre de selfs arrêté ; devis de
      fil demandé (le 25 €/kg n'est **pas** une source).
- [ ] **D7** — Gabarit 1024 × 768 acté ; `figsize`/`dpi` matplotlib figés dans le
      squelette `analyse/` **avant** la première figure.
- [ ] **D8** — Type de caisse **constaté** (évent : oui/non) ; le modèle de la
      phase 2 est dimensionné en conséquence (5 ou 8 paramètres).
- [ ] **D9** — Filière déclarée ; positionnements et titre arrêtés sur le récit
      prévu.
- [ ] **D10** — Encadrant désigné, accord explicite obtenu, compte
      `lycees.scei-concours.fr` vérifié.
- [ ] Porte de la **phase 1** connue et acceptée : la résistance étalon est
      retrouvée à ±3 % et le condensateur suit $1/\omega C$ sur deux décades,
      sinon on diagnostique avant d'avancer.
- [ ] Achats de la phase 1 passés : $R_{ref}$ 100 Ω 1 % (+ une 10 Ω), pinces et
      câbles, résistance de puissance 8 Ω (si absente au lycée), wattmètre de
      prise.
- [ ] Cahier de laboratoire ouvert et daté ; appareil photo prêt (les objets
      sont interdits en salle d'oral).

### Phrase de clôture — à dater et signer

> Je soussigné **[[Thomas Mareel]]** atteste que les décisions D1 à D10 du
> présent registre sont arrêtées à la date ci-dessous, **avant toute mesure
> comparative**, et que toute modification ultérieure sera inscrite, datée et
> justifiée dans le journal ci-après, puis mentionnée à l'oral.
>
> Fait le `[[JJ/MM/AAAA]]` — signature : `[[..............]]`
>
> Visa du professeur encadrant (facultatif mais recommandé) :
> `[[..............]]`

---

## Journal des modifications après gel

Toute décision changée après signature s'inscrit ici, **sans jamais effacer la
ligne d'origine**. C'est ce tableau qui alimentera le DOT (4 à 8 jalons de
50 mots, « y compris les difficultés rencontrées, réalisations infructueuses,
surmontées ou non ») et qui permettra de répondre sereinement à la question
« avez-vous changé quelque chose en cours de route ? ».

| Date | Décision | Ancienne valeur | Nouvelle valeur | Justification (qui ne peut pas être « le résultat obtenu ») | Mentionné à l'oral |
|---|---|---|---|---|---|
| `[[...]]` | `[[Dn]]` | `[[...]]` | `[[...]]` | `[[...]]` | `[[oui/non]]` |

---

### Provenance des chiffres cités

Toutes les valeurs numériques de ce registre proviennent de
`REFERENCE-TECHNIQUE.md`, section indiquée à chaque fois : § 01.6, § 01.8,
§ 01.10, § 01.13, § 04.1, § 04.2, § 04.3, § 04.5, § 04.8, § 04.9, § 05.8,
§ 05.10, § 07.0, § 07.8, § 07.9, § 07.11, § 08.2, § 08.3, § 09.7. Elles sont
**calculées**, sur 8 Ω résistif ou sur un modèle de haut-parleur *typique* issu
de datasheets publiques. **Aucune n'est une mesure sur l'enceinte de Thomas.**
Les valeurs des $-3$ dB sous les deux conventions de seuil (D1) ont été
revérifiées le 2026-09-13 par calcul direct. Tout ce qui reste à établir porte
la marque `[[à mesurer]]` ou `[[à vérifier]]`.
