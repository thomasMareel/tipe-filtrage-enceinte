# Notes TIPE v2 — questions du jury et réponses préparées

*À relire la veille de l'oral.* Sujet v2 : **optimisation sous contraintes du filtre
de raccord à 100 Hz d'une enceinte deux voies sur sa charge réelle $Z(f)$**.
Jury non spécialiste (deux examinateurs, volontairement non experts du domaine) :
répondre avec des **grandeurs physiques, des ordres de grandeur et des incertitudes**,
jamais « ça sonne mieux ».

> **Mode d'emploi.** Chaque réponse tient en 3 à 6 phrases : c'est ce qui se dit à
> l'oral. Le renvoi « → § NN.n » pointe vers `REFERENCE-TECHNIQUE.md`, où vivent la
> démonstration, le code et les sources ; `FEUILLE-DE-ROUTE.md` dit quoi faire et quand.
> **Aucun chiffre de ce document n'est une mesure faite sur l'enceinte** : les valeurs
> sont calculées, ou tirées d'un modèle illustratif, et étiquetées comme telles. Les
> marques `[[réponse à compléter après la phase N]]` signalent ce qui ne pourra être dit
> qu'après les mesures — tant qu'elles sont là, la phrase n'est pas un résultat.

---

## 0. Le récit en dix lignes, et le message central

1. Une enceinte deux voies DIY doit être coupée en deux bandes autour de **100 Hz** : le
   grave à un 18″ 8 Ω monté en **caisse bass-reflex à deux évents**, le reste à deux médiums
   4 Ω en série, qu'il faut tenir au-dessus de leur résonance. Deux pavillons d'ultra-aigu
   sont **câblés en parallèle des médiums** : hors bande **acoustiquement** (on n'en parle
   pas au raccord), mais **dans la charge électrique** que voit le passe-haut — d'où la règle
   de mesure : on relève le bloc médiums **tel qu'il est câblé**.
2. Les formules de filtrage du cours et des catalogues supposent une charge **résistive de
   8 Ω**. Pour le Butterworth du 2ᵉ ordre : $L=\sqrt2R/\omega_0=18{,}0$ mH et
   $C=1/(\sqrt2R\omega_0)=140{,}7$ µF, soit 18 mH / 150 µF en valeurs normalisées.
3. Or **le haut-parleur n'est pas une résistance de 8 Ω** : c'est un système
   électromécanique dont l'impédance possède une remontée inductive et, **la caisse étant
   bass-reflex, deux pics encadrant un creux à l'accord des évents** (§ 01.10). Sur la bande
   du raccord, son module varie d'un facteur de l'ordre de 20 et sa phase de plus de 100°
   (§ 01.8, modèle typique — **à mesurer**). Aggravation propre au bass-reflex : sur un jeu
   de paramètres plausible pour un 18″ de sonorisation (modèle, **pas une mesure**), le
   **second pic tombe vers 86 Hz**, c'est-à-dire en plein dans la zone de raccord.
4. **Acte 1 — mesurer.** Relever $Z(f)$, module et phase, avec une chaîne étalonnée
   d'abord sur une résistance et un condensateur connus, et des incertitudes chiffrées.
5. **Acte 2 — identifier.** Remonter de la courbe aux paramètres du modèle de Thiele-Small
   par **moindres carrés pondérés** — **cinq** en caisse close, **sept à huit** en
   bass-reflex (les cinq précédents plus l'accord $f_b$, le rapport de compliances $\alpha$
   et une perte de caisse $Q_l$) : c'est un **problème inverse**, validé par le $\chi^2$
   réduit, la structure des résidus et trois estimateurs d'incertitude.
6. **Acte 3 — optimiser.** Concevoir le filtre par **optimisation sous contraintes** sur
   cette charge-là : valeurs normalisées E12, budget, pertes Joule dans la résistance de
   la self, impédance minimale admissible par l'amplificateur, protection des médiums.
7. **Acte 4 — valider.** Comparer filtre catalogue, filtre optimisé et référence active,
   au banc puis au micro, contre des **critères gelés et datés avant les mesures**.
8. Deux satellites nourrissent le récit : la **self** (Wheeler, bobine de Brooks) donne le
   modèle coût–masse–pertes injecté dans la fonction de coût ; le **croisement
   énergétique** compare la consommation au repos de l'actif aux pertes proportionnelles
   du passif.
9. La **référence active Sallen-Key** n'est pas un concurrent : placée avant l'ampli, elle
   ne voit jamais $Z(f)$. C'est l'**étalon immunisé par construction** contre le problème
   étudié.
10. **Conclusion attendue, et assumée d'avance** : si le passif optimisé ne rattrape pas
    l'actif, la limite physique identifiée et mesurée est un résultat — pas un échec.

> **Message central, en une phrase** : *un filtre ne se calcule pas contre une impédance
> nominale mais contre une impédance mesurée ; et une fois qu'on la mesure, le
> dimensionnement cesse d'être une formule pour devenir une optimisation sous contraintes.*

**La formulation qui résiste au jury** : sur l'écart RMS de la somme des deux voies,
passer de 8 Ω résistif à une charge réaliste coûte **+3,8 dB systématiques**, alors que
*toutes* les tolérances de composants et d'identification réunies ne dispersent le
résultat que de **±0,26 dB** (§ 04.9, calcul sur charge typique). Autrement dit :
**$Z(f)$ est un biais, les tolérances sont une dispersion.** Un biais ne s'efface ni en
moyennant ni en resserrant les tolérances — seulement en le mesurant et en optimisant
dessus. C'est exactement le sujet.

---

## 1. Rappels de format (pour ne pas se tromper le jour J)

- **15 min d'exposé + 15 min d'entretien**, deux examinateurs. Support : **PDF 4/3
  paysage, 5 Mo maximum**, projeté depuis l'ordinateur du jury. Ni HTML, ni clé USB, ni
  notes à l'écran, ni objet (donc **ni l'enceinte, ni la self, ni le filtre** : photographier
  avant démontage). Diapositives **numérotées**. → § 08.2
- Les **listings Python** sont à apporter **en double exemplaire papier** et à annexer
  **après la conclusion** du PDF. → § 08.2
- Le détail (self, Monte-Carlo, énergie, code) vit en **annexes appelées pendant
  l'entretien**, pas dans les 15 minutes.

---

## 2. Questions probables, par thème

### 2.1 Modèle et impédance

**« Pourquoi ne peut-on pas traiter le haut-parleur comme une résistance de 8 Ω ? »**
→ Parce qu'il est électromécanique. Vu de ses bornes il vaut $R_e+j\omega L_e$ **plus**
une branche motionnelle : la masse, le ressort et les frottements de l'équipage mobile,
ramenés côté électrique par le facteur de force $Bl$, y apparaissent comme un circuit RLC
parallèle. D'où un **pic de résonance** et une remontée inductive en haut de bande. « 8 Ω »
est une valeur *nominale* de catalogue, pas une mesure. → § 01.2, § 01.3

**« Écrivez $Z(j\omega)$. »**
→ $$Z(j\omega)=R_e+j\omega L_e+\frac{R_{es}}{1+jQ_{ms}\left(\dfrac{f}{f_s}-\dfrac{f_s}{f}\right)}$$
Cinq paramètres, et chacun se **lit sur la courbe** : $R_e$ = plancher basse fréquence,
$f_s$ = position du pic, $R_{es}$ = hauteur du pic au-dessus de $R_e$, $Q_{ms}$ = finesse
du pic, $L_e$ = remontée en haut de bande. C'est ce qui fournit l'initialisation de
l'ajustement. **Attention : cette écriture-là suppose une caisse close.** Mon sub est en
bass-reflex ; il faut donc y ajouter la branche de caisse (question suivante). → § 03.1

**« Votre caisse est à évents : que devient cette formule ? »**
→ Un évent ajoute un **second degré de liberté** : la masse d'air de l'évent résonne avec la
compliance de la caisse. Dans l'impédance mécanique, le terme de raideur $1/(j\omega C_{ms})$
devient $1/(j\omega C_{ms})+S_d^2\underline Z_{ac}$, où $\underline Z_{ac}$ est la compliance
de caisse **en parallèle** avec la masse et les pertes de l'évent. Ramenée aux bornes, cette
branche supplémentaire fait passer le modèle de 5 à **7 ou 8 paramètres** ($f_b$, $\alpha$,
$Q_l$) — et le contrôle qui prouve qu'on n'a pas changé de physique est la limite **« évent
inerte »** : masse d'air infinie ($f_b\to0$) redonne **exactement** la caisse close de même
volume. → § 01.10

**« Pourquoi une caisse bass-reflex donne-t-elle deux pics d'impédance ? »**
→ Parce que le système a **deux degrés de liberté couplés** : la membrane et la colonne d'air
des évents. À l'accord $f_b$, les deux oscillent en opposition et la membrane est **quasi
immobile** — c'est l'**évent** qui rayonne ; la vitesse de la membrane s'effondre, donc la
force contre-électromotrice $Bl\,v$ aussi, donc $|Z|$ **retombe près de $R_e$** : c'est le
**creux**. De part et d'autre, les deux modes du système couplé donnent **deux pics**
$f_L<f_b<f_H$. Ce n'est pas une constatation empirique : le modèle démontre
$f_Lf_H=f_sf_b$ et $f_L^2+f_H^2=f_s^2(1+\alpha)+f_b^2$, d'où $f_L<f_b<f_H$ toujours. Sur un
jeu de paramètres plausible (**modèle, pas mesure** : $f_s=40$ Hz, $f_b=35$ Hz, $Q_l=7$, et
$\alpha=3$, c'est-à-dire $V_{as}=330$ L pour $V_b=110$ L) : pics à 16,3 Hz (54 Ω) et
**85,9 Hz (64 Ω)**, creux à 34,2 Hz (6,1 Ω), $|Z|(100\ \text{Hz})=22{,}4$ Ω.
**Si le jury demande ce qui met le pic haut si près du raccord, la réponse est $\alpha$, pas
$f_b$** : à $f_b$ fixé, $\alpha$ de 0,5 à 6 promène $f_H$ de 55 à 111 Hz ; à $\alpha$ fixé,
descendre $f_b$ **abaisse les deux pics ensemble**. Une caisse *petite devant $V_{as}$* — le
cas ordinaire en sono — remonte $f_H$ vers 100 Hz.
[[réponse à compléter après la phase 1 : $f_L$, $f_b$, $f_H$ mesurés]] → § 01.10

**« Que se passe-t-il sous la fréquence d'accord ? »**
→ **La membrane n'est plus chargée.** Au-dessus de $f_b$, l'air de la caisse fait ressort et
limite le débattement ; en dessous, l'évent devient un court-circuit acoustique, la charge
arrière disparaît et l'**excursion croît très vite** alors que le rayonnement, lui, s'effondre
(les deux sources finissent en opposition de phase). Conséquence pratique, et c'est une
**consigne de sécurité écrite avant les mesures** : les balayages au **niveau fort** partent
de $f_{\text{start}}\ge 2f_b$, $f_b$ étant relevé en phase 1 par le double pic d'impédance ;
en dessous, on ne balaie qu'au **niveau faible**, ou derrière un passe-haut de protection en
amont de l'ampli. → § 01.10, § 07.8

**« Pourquoi ne parlez-vous pas des pavillons d'ultra-aigu ? »**
→ Il faut distinguer deux plans, et c'est exactement la nuance que la question cherche.
**Acoustiquement**, ils sont hors bande : ils ne rayonnent rien autour de 100 Hz et ne
participent pas au raccord étudié — donc hors périmètre. **Électriquement, non** : ils sont
**câblés en parallèle des médiums**, ils font donc partie de la charge que voit le filtre
passe-haut. Je mesure donc le **bloc médiums tel qu'il est câblé, pavillons connectés**,
puisque c'est ce dipôle-là, et pas un médium isolé, que le filtre charge. Un condensateur de
protection est **présent** en série avec les pavillons (constaté le 16/09/2026) ; sa valeur
fixe l'**ampleur** de leur contribution. Pour 3,3 à 10 µF, chaque pavillon présente 160 à
480 Ω vers 100 Hz, soit 80 à 241 Ω pour les deux en parallèle — **pas au point d'être
négligeable** : $|Z|$ du bloc passe de 29,3 Ω à 26,3 – 21,8 Ω, soit −10 à −26 % (−0,9 à
−2,6 dB) au voisinage de sa résonance (calculé sur le modèle, pas mesuré). Sans condensateur,
la branche serait un parallèle direct : $|Z|$ du bloc chuterait de 87 % **et** les pavillons
recevraient du 100 Hz à pleine puissance — c'est pourquoi un contrôle à l'ohmmètre (environ
6 à 7 Ω en continu attendus) vérifie le câblage avant toute mesure.
**La parade est le niveau, jamais le débranchement** : la mesure d'impédance se fait à
100–200 mV, sans risque ; ce sont les seuls **balayages acoustiques forts** qui se limitent
en niveau et en durée. Débrancher les pavillons reviendrait à mesurer une charge qui n'existe
pas dans le montage — c'est-à-dire à défaire exactement ce que je viens d'expliquer.
[[à mesurer sur l'enceinte : valeur du condensateur en série avec les pavillons (sa présence
est constatée depuis le 16/09/2026)]]

**« "Du simple au sextuple", d'où sort ce chiffre ? »**
→ Le rapport pic/plancher vaut $|Z|_{max}/R_e=1+Q_{ms}/Q_{es}$ ; ce n'est donc pas un
accident, c'est le rapport des amortissements mécanique et électrique. Ce chiffre a été
**retiré de la problématique** : il n'était pas mesuré et il était trop bas. Les fiches de
18″ de sonorisation donnent $|Z|_{max}$ entre 60 et 200 Ω (Delta Pro-18A : 172 Ω calculé),
soit ×8 à ×25 face à 8 Ω nominaux ; l'ordre de grandeur 40–60 Ω hérité de la v1 ne vaut
**ni pour le 18″ ni pour le bloc médiums** : modélisé avec ses deux pavillons (2 × 8 Ω avec
6,8 µF), ce bloc culmine lui aussi vers **112 Ω à 77 Hz** (calculé, non mesuré). Les pertes
de la caisse rabaissent le pic. La problématique dit
donc « varie fortement avec la fréquence », et le rapport sera chiffré après la phase 1.
[[réponse à compléter après la phase 1 : rapport max/min mesuré en caisse]] → § 01.8

**« Votre $f_s$ mesurée ne correspond pas à la datasheet. »** *(piège classique)*
→ C'est attendu, et ce n'est pas une erreur. La datasheet donne $f_s$ en champ libre ; je
mesure le haut-parleur **en caisse**. En caisse close, le ressort d'air s'ajoute à la
suspension et monte la résonance : $f_c=f_s\sqrt{1+V_{as}/V_b}$. **Ma caisse est en
bass-reflex, à deux évents** : je n'attends donc pas un pic déplacé mais **deux pics** et un
creux à l'accord des évents. Le paramètre utile à mon filtre est celui **en caisse**,
puisque c'est cette impédance-là que le filtre voit. → § 01.9, § 01.10

**« Que ne peut pas donner votre mesure d'impédance ? »**
→ $Z(f)$ ne détermine que cinq nombres. $Bl$, $M_{ms}$, $C_{ms}$, $R_{ms}$ et donc $V_{as}$
ne sont **pas identifiables** séparément : la famille $(Bl\sqrt k,\;kM_{ms},\;C_{ms}/k,\;
kR_{ms})$ donne rigoureusement la même courbe. Les séparer demanderait une seconde manip
(masse ajoutée ou volume connu). C'est hors périmètre et sans conséquence : **le filtre ne
voit que $Z(f)$**. → § 01.6, § 03.1

---

### 2.2 Mesure et incertitudes

**« Comment mesurez-vous une impédance ? »**
→ Une résistance étalon $R_{ref}$ en série avec le dipôle, et je mesure **les deux
tensions** : $\underline Z=R_{ref}\,\underline V_{d}/\underline V_{R}$. C'est un rapport de
deux tensions parcourues par le **même** courant : la formule est **exacte quelle que soit
$R_{ref}$**, sans aucune hypothèse de « courant constant ». Le module vient du rapport des
amplitudes, la phase du décalage temporel. → § 02.1, § 02.3

**« Pourquoi ne pas supposer le courant constant, avec une grosse résistance série ? »**
→ Parce que l'hypothèse casse là où c'est le plus intéressant. Au pic, l'impédance d'un
18″ vaut $R_e(1+Q_{ms}/Q_{es})$, soit 60 à 200 Ω pour un 18″ de catalogue (majorant : la
formule vaut en caisse close ; en bass-reflex, le pic haut modélisé vaut 64 Ω) : avec
$R_{ref}=100$ Ω, le
courant n'est plus constant du tout et l'erreur sur le pic atteint 50 à 63 % (calculé).
La mesure des deux tensions coûte une voie d'oscilloscope de plus et supprime le problème.
→ § 02.1

**« Comment savez-vous que votre chaîne de mesure est juste ? »**
→ Je l'**étalonne d'abord sur des composants connus** : une résistance de puissance (module
plat, phase nulle) et un condensateur connu ($|Z|=1/\omega C$, phase $-90°$ sur deux
décades). C'est la porte de validation de la phase 1 : tant qu'elle n'est pas franchie, je
ne mesure pas de haut-parleur. Le critère est un **écart normalisé** $E_n\le2$ et un biais
moyen $\le3$ %. Si le code ne retrouve pas une résistance, il ne retrouvera pas un
haut-parleur. → § 02.8, § 03.7 (critère 7)

**« Quelle est votre incertitude sur $|Z|$ ? »**
→ Environ **3 % est un plancher, pas un acquis** : deux voies à 2 % chacune donnent déjà
$\sqrt{u_R^2+2\varepsilon^2}=3{,}0$ %, et la soustraction des tensions coûte un facteur
$\sqrt2\,(1+|Z|/R_{ref})$ — c'est lui, et non la quantification de l'oscilloscope, qui
commande le choix de $R_{ref}$. Je vise 3 % sur le plateau et 3 à 6 % au pic.
[[réponse à compléter après la phase 1 : budget d'incertitude réellement obtenu]] → § 02.7

**« Une erreur sur votre résistance étalon, ça se voit ? »**
→ **Non, et c'est le point le plus subtil.** Une erreur de $+1$ % sur $R_{ref}$ multiplie
toutes les impédances par 1,01 : $R_e$, $R_{es}$ et $L_e$ se décalent d'exactement 1 % et le
$\chi^2$ ne bronche pas. C'est une incertitude **systématique de type B**, invisible pour
les estimateurs statistiques. En revanche $f_s$ et $Q_{ms}$ y sont **immunisés** : ce sont
une position et une forme, pas un niveau. D'où l'achat d'une résistance à 1 %, mesurée au
multimètre, et sa tolérance reportée à part : c'est la $R_{ref}$ de 100 Ω de l'oscilloscope,
**distincte** des deux 100 Ω à 0,1 % de la chaîne carte son (résistance de mesure et
référence de REW) — si les deux chaînes partageaient la même résistance, leur recoupement ne
verrait plus une erreur sur elle. → § 03.5

**« Pourquoi une carte son, et pas seulement l'oscilloscope ? »**
→ Pour la finesse de la grille et la phase. À l'oscilloscope, chaque fréquence demande un
réglage du GBF et une lecture de deux amplitudes et d'un décalage : c'est exact, mais lent,
alors que le premier pic veut un point tous les 0,2 Hz environ. La carte son (Focusrite
Scarlett Solo) pilotée par REW balaie de 5 Hz à 20 kHz en une vingtaine de secondes et rend
module et phase sur une grille serrée. Je ne la crois pas pour autant sur parole : la chaîne
GBF + oscilloscope reste le **recoupement**, justement parce qu'elle ne partage avec la carte
son ni ses entrées, ni son logiciel. → § 02.13 (application à la Scarlett Solo) ; § 02.9
pour le principe de REW

**« Pourquoi 100 Ω, et pas une petite résistance ? »**
→ Parce que REW ne lit pas la tension aux bornes de la résistance : une voie lit la sortie
de la carte, l'autre le haut-parleur, et la soustraction est **logicielle**,
$\underline Z=R\,\underline V_{HP}/(\underline V_{source}-\underline V_{HP})$. Une petite
erreur sur une voie est alors multipliée par le facteur de soustraction $|Z+R|/R$ : au pic
modélisé de 64 Ω, il vaut **1,64 avec 100 Ω** contre **7,4 avec 10 Ω** (calculé). Et avec
100 Ω, le courant reste de quelques milliampères (au plus 4,5 mA au niveau de travail), moins
qu'un casque ordinaire ; une 10 Ω en demanderait 91 à 164 mA à la sortie casque. C'est
d'ailleurs la valeur que l'aide de REW conseille derrière une sortie casque.
→ § 02.13

**« Vos deux entrées ne sont pas identiques : comment le gérez-vous ? »**
→ Elles ne le sont pas : l'entrée micro (XLR, 3 kΩ) et l'entrée ligne (60 kΩ) diffèrent
d'impédance et de 13 dB de pleine échelle. **Un** : je mets chacune là où son défaut ne compte
pas — l'entrée micro lit la sortie de la carte, un nœud piloté à moins de 1 Ω où ses 3 kΩ ne
faussent rien ; l'entrée ligne lit le haut-parleur, qu'elle ne charge que de −0,11 % au pic de
64 Ω (calculé, corrigé ensuite). **Deux** : j'apparie les voies — GAIN 2 monté d'environ
13 dB jusqu'à égalité à 1 dB près, fils ouverts, puis **bloqué au ruban**, car REW abandonne
l'étalonnage open au-delà de 2 dB d'écart. **Trois** : trois étalonnages au bout du câble —
open (écart de gain et de phase entre voies), short (câble), puis reference sur une **seconde**
100 Ω à 0,1 %. Et je ne valide jamais sur la résistance qui a servi de référence : ce contrôle
serait circulaire. → § 02.13

**« Et la chaîne carte son, comment savez-vous qu'elle mesure juste ? »**
→ Par trois contrôles qui ne réutilisent pas l'étalonnage. **Un** : après les étalonnages, je
mesure des dipôles **distincts de la référence** — une 10 Ω (module plat, phase nulle) et un
100 µF ($|Z|$ de 159 à 15,9 Ω sur 10–100 Hz, phase $-90°$). **Deux** : je recoupe avec la
chaîne GBF + oscilloscope ; les deux méthodes doivent coïncider dans leurs incertitudes.
**Trois** : en fin de séance, je relis la 100 Ω de référence — un écart de 0,23 % trahirait
une dérive de 0,01 dB de la voie de mesure, soit 0,19 % sur le pic de 64 Ω (calculé).
[[réponse à compléter après la phase 1 : écarts de validation réellement obtenus]]
→ § 02.13 ; § 02.8

---

### 2.3 Identification et moindres carrés

**« Expliquez votre problème inverse en une phrase. »**
→ Je cherche les cinq nombres qui minimisent la somme des écarts pondérés au carré entre
la courbe mesurée et le modèle ; comme le modèle n'est pas linéaire en ses paramètres, je
le linéarise et j'itère (Gauss-Newton, amorti à la Levenberg-Marquardt) ; l'incertitude
vient de la matrice $(J^{\mathsf T}J)^{-1}$, recoupée par Monte-Carlo et par jackknife.
→ § 03.2, § 03.8

**« Pourquoi pondérer les résidus ? »**
→ Parce que le bruit de ma chaîne est **relatif**, pas absolu. Sans pondération, un point du
pic à 50 Ω pèserait une cinquantaine de fois plus qu'un point du plancher à 7 Ω, alors que
les deux sont mesurés avec la même précision relative. Je pose donc
$r_k=(\text{modèle}-\text{mesure})/u_k$ : chaque point compte selon sa précision réelle, un
point bien ajusté contribue pour $r_k^2\approx1$, et la somme minimale doit valoir environ
le nombre de degrés de liberté. C'est le test du **$\chi^2$ réduit**. → § 03.2

**« Comment savez-vous que c'est le bon minimum ? »**
→ Réponse honnête : **il existe au moins un minimum parasite** ($L_e\to0$, $Q_{ms}$ très
grand). Mais il se reconnaît instantanément à son coût — $\chi^2$ réduit de l'ordre de
$10^3$ contre 1,1. Je fais donc un **multi-départ** (sur données synthétiques : 200 tirages
dans un facteur 0,2 à 5, dont 94 % retrouvent le minimum global) et je garde le coût le
plus bas ; l'initialisation lue sur la courbe évite le piège dès le premier essai.
→ § 03.3, § 03.8

**« Et si votre modèle était faux ? Comment le verriez-vous ? »**
→ C'est la vraie question, parce qu'**un modèle inadapté ne plante pas : il converge et
rend des nombres plausibles**. Sur une charge à deux pics ajustée par le modèle à un pic,
l'ajustement sort $R_e$, $f_s$ et $Q_{ms}$ d'allure crédible — seuls le $\chi^2$ réduit et
la **structure des résidus** le trahissent. **C'est très exactement le piège que ma caisse
bass-reflex me tend** : ajuster ses deux pics avec le modèle clos à cinq paramètres donne
$z=-5{,}4$ au test des séquences. J'utilise donc le test des séquences de Wald-Wolfowitz sur
les signes des résidus : $z=+0{,}4$ pour le bon modèle, $z=-5{,}4$ pour un bass-reflex ajusté
par le modèle clos, $z=-5{,}6$ pour une bobine à pertes ajustée avec $L_e$ constante.
→ § 03.7

**« Comment savez-vous que votre modèle a le bon nombre de paramètres ? »**
→ Je ne le décide pas, je le **constate**, et en trois temps. **Un** : un aiguillage
automatique, avant tout ajustement, compte les **maxima locaux** de $|Z|$ lissé entre 10 et
100 Hz — un seul maximum donne le modèle clos à 5 paramètres, deux ou plus donnent le modèle
bass-reflex ; sur mes données synthétiques il en compte 1 pour la caisse close et 3 pour le
bass-reflex (dont un parasite : le critère est « $\ge2$ », pas « exactement 2 »). **Deux** :
si je mets trop de paramètres, cela se voit aux **incertitudes** — un paramètre non identifié
ressort avec une barre d'erreur énorme et une forte corrélation avec un autre. **Trois**, et
c'est le plus convaincant : **$f_b$ se recoupe par trois voies indépendantes** — la
**géométrie** (formule de Helmholtz avec les sections et longueurs des deux évents et le
volume de la caisse, § 4 check-list), la **lecture directe** sur la courbe (au passage par
zéro de la phase entre les deux pics, plus net que l'argmin du creux, qui est plat),
et la valeur **ajustée** par les moindres carrés. Trois routes qui ne partagent aucune
hypothèse : si elles se recoupent, le modèle a la bonne taille ; sinon, c'est un résultat à
expliquer, pas un paramètre à ajouter. C'est là une **prédiction falsifiable**, faite avant
la mesure. [[réponse à compléter après la phase 1 : les trois estimations de $f_b$ et leur
écart]] → § 01.10, § 03.7

**« Votre modèle vaut-il encore à 1 kHz ? »**
→ Non, et le symptôme n'est pas une grande incertitude, c'est un **biais**. La bobine réelle
a des pertes par courants de Foucault : sa partie réelle croît avec la fréquence, ce que
$L_e$ constante ne sait pas représenter. L'ajustement absorbe cette croissance en gonflant
$R_e$ — jusqu'à $+16$ % sur des données simulées, soit une quinzaine d'écarts-types.
Restreindre la bande n'y suffit pas ; le remède est un modèle à six paramètres
$Z=R_e+K(j\omega)^n+Z_{mot}$, déjà écrit et testé. → § 03.6

**« Vous utilisez une bibliothèque toute faite ? »**
→ `scipy.optimize.least_squares` sert de référence, mais j'ai **réécrit Levenberg-Marquardt
en numpy pur** (vingt-cinq lignes) : mêmes paramètres à $6\cdot10^{-8}$ près en relatif,
mêmes incertitudes. Ce n'était pas une contrainte — scipy 1.18.1 est bien installé sur mon
poste — mais un choix : cela me permet de répondre à « que fait votre boîte noire ? », et le
code reste exécutable sur une machine où scipy manquerait. L'énumération de
l'acte 3 ne demande, elle aussi, que numpy. → § 03.2, § 09.5

---

### 2.4 Optimisation, critères, choix de conception

**« Qu'optimisez-vous, exactement ? »**
→ Quatre composants $(L_1,C_1,C_2,L_2)$, sur une grille de valeurs **réellement
achetables** (série E12), pour minimiser une fonction de coût explicite : écart de la somme
des deux voies à la cible (dB), écart de forme de chaque voie (dB), écart de phase entre
voies (°), prix (€) et pertes Joule (W). Les pondérations sont **affichées et discutées** —
c'est le cahier des charges chiffré, et il est gelé avant les mesures comparatives.
→ § 04.5

**« Quelle est la taille de votre espace de recherche ? »**
→ 24 valeurs de self × 24 de condensateur pour chaque voie, soit
$24^4=\mathbf{331\,776}$ combinaisons. C'est petit : je l'**énumère exhaustivement**, en
environ **2 secondes avec numpy seul**, grâce à une astuce de vectorisation (le passe-bas
ne dépend que de $(L_1,C_1)$, le passe-haut que de $(C_2,L_2)$ : deux tableaux de 576
lignes, puis produit externe). L'énumération est la méthode de référence — pas de minimum
local possible — et un optimiseur continu sert de recoupement. Si j'énumérais aussi le
réseau de Zobel, on passerait à 96 millions de points : je le traite donc comme un
**booléen**, et je l'assume comme une restriction du domaine. → § 04.5, § 04.6

**« Votre optimiseur retrouve-t-il le Butterworth du cours sur une charge de 8 Ω ? »**
→ **Oui, et c'est ma porte de validation de la phase 3** — je n'achète rien tant qu'elle
n'est pas franchie. Alimenté par une charge de 8 Ω résistifs, l'optimiseur **continu**
redonne les valeurs analytiques 18,0063 mH / 140,674 µF à $10^{-6}$ près : c'est un
théorème, pas une coïncidence. L'optimum **E12**, lui, vaut bien 18 mH / 150 µF avec les
pondérations gelées, mais il dépend de la fonction de coût : c'est un test de non-régression,
pas une vérité. → § 04.7, § 09.6

**« Pourquoi le filtre catalogue ne convient-il pas sur la charge réelle ? »**
→ Parce que sur une charge résistive, $Q=R\sqrt{C/L}$ : **le facteur de qualité appartient
à la charge**, pas au filtre. Remplacer $R$ par $Z(f)$ fait donc varier $Q$ avec la
fréquence, et sur un modèle typique la cellule surtend de **+8 à +11 dB** vers 75 Hz.
Résultat contre-intuitif : la fréquence de raccord bouge peu, c'est la **forme** de la
réponse qui se déforme. **Et la caisse bass-reflex aggrave le cas** : son **second pic
d'impédance tombe vers 86 Hz** sur le modèle, donc **dans la zone de raccord elle-même** —
l'hypothèse « 8 Ω résistifs » y est encore plus fausse qu'en caisse close. Sur la charge
bass-reflex modélisée (modèle, **pas une mesure**), le filtre catalogue surtend de
**+12,6 dB**, contre +12,2 dB sur une **seconde charge modélisée, en caisse close** — un jeu
de paramètres distinct, *pas* le même haut-parleur supposé clos — et **0 dB** sur 8 Ω
résistifs. La « surtension » est ici le maximum de $|H|$ du passe-bas sur 10–1000 Hz rapporté
à la perte d'insertion de 1,02 dB obtenue sur 8 Ω résistifs : sans cette définition, le
nombre n'est vérifiable par personne. → § 04.1, § 04.2, § 01.8, § 01.10

**« Un résultat qui vous a surpris ? »**
→ Oui : sur la charge typique, la contrainte « impédance vue par l'amplificateur
$\ge4\ \Omega$ » **disqualifie le filtre catalogue avant même la comparaison de fidélité**
(minimum à **3,29 Ω**, chaîne régénérée le 16/09/2026 sur la charge bass-reflex, avec la DCR
des selfs de Brooks). Et ce n'est pas un cas pathologique isolé : **162 des 576** couples
$(L_1,C_1)$ de la grille violent cette contrainte même sur 8 Ω résistif (recompté le
16/09/2026 : 162/576 exactement). Le design optimisé, lui, remonte ce minimum à **5,27 Ω**.
**Précision de méthode, à donner avant qu'on la demande** : le montage de référence gelé pour
cette contrainte est la lecture **voie par voie** (bi-amplification). Dans l'autre lecture —
les deux cellules en parallèle sur un seul ampli — le catalogue tombe à 1,77 Ω, **mais le
design optimisé y descend aussi sous le seuil, à 3,48 Ω**. Je ne peux donc pas me servir du
montage parallèle contre le catalogue et l'oublier pour mon propre design : dans ce
montage-là, aucun des deux ne passe, et c'est une **limite ouverte** du design candidat. C'est une contrainte de sécurité matérielle, gratuite à
calculer, et que la v1 ignorait. **Le constat ne dépend pas du jeu de paramètres** : recalculé
sur une seconde charge modélisée, plausible pour un 18″ de sonorisation, le même filtre
catalogue descend à **2,66 Ω en bass-reflex** et 2,49 Ω en supposant la caisse close, alors
qu'il reste à 8,52 Ω sur 8 Ω résistifs. Deux modèles indépendants, même verdict — mais ce sont
des **modèles**, et la mesure de la phase 1 tranchera. → § 04.8

**« Pourquoi ne pas simplement linéariser l'impédance avec un réseau de Zobel ? »**
→ Parce que le Zobel corrige la **partie inductive**, pas le pic motionnel — or c'est le pic
qui gêne au raccord : à 100 Hz il ne fait passer l'impédance que de 14,1 à 11,6 Ω sur le
modèle typique. Le réseau qui *corrige vraiment* le pic est un RLC série accordé sur $f_s$ :
il demande **2,4 mF** et une résistance qui, à la résonance et à pleine puissance, dissiperait
**sept fois** ce que reçoit le haut-parleur. Coût, matière et chaleur : exactement ce que le
thème « sobriété » demande d'éviter. D'où le choix v2 : **laisser $Z(f)$ tel quel et optimiser
dessus**. → § 04.4, § 04.8

**« Comment choisissez-vous vos pondérations ? Ce n'est pas arbitraire ? »**
→ Elles sont **conventionnelles et déclarées**, pas arbitraires : chaque poids est une
équivalence explicite (25 € ≡ 1 dB, 1 W de pertes à la puissance de référence ≡ 1 dB), gelée
en phase 0 avec les critères. Deux d'entre elles ont d'ailleurs dû être recalibrées :
la pénalité de phase était sur-pénalisante d'un facteur ≈ 8 au regard de la somme sur l'axe,
et la protection des médiums doit être **unilatérale** (pénaliser la sous-protection, pas la
sur-protection). Je montre la sensibilité de l'optimum à ces choix plutôt que de prétendre
qu'ils n'existent pas. → § 04.5

**« Que vaut votre optimum ? »**
→ **Il est plat** : sur l'illustration, quatre designs se tiennent à 1 % de la fonction de
coût. Cela veut dire que la dernière marche E12 compte moins que les tolérances de
fabrication — et donc qu'il faut présenter un *domaine* de bons designs, pas un point.
[[réponse à compléter après la phase 3 : optimum sur le $Z(f)$ réellement mesuré]]
→ § 04.8, § 04.9

---

### 2.5 La self : cuivre, pertes, matière

**« Pourquoi consacrer une partie du travail à la bobine elle-même ? »**
→ Parce qu'elle est le poste dominant en **prix, en masse et en pertes**, et que sa
résistance série entre directement dans la fonction de coût. À 100 Hz, une self de grave
fait des dizaines de millihenrys : ce n'est plus un composant qu'on choisit sur catalogue,
c'est un objet qu'on **dimensionne**. Le marché ne vend d'ailleurs pas de self à air de
18 mH à faible résistance — parce qu'elle pèserait cinq kilos. → § 05.1, § 05.10

**« Quelle est la loi qui gouverne ce compromis ? »**
→ $L$, $r$ et la masse de cuivre $m$ ne sont pas indépendants :
$$m=K_{Cu}\left(\frac{L}{r}\right)^{3/2},\qquad K_{Cu}\approx1760\ \text{kg}\cdot\text{s}^{-3/2}\ (\pm10\ \%),$$
**indépendamment du diamètre de fil**. Conséquence directe : diviser la résistance par deux
multiplie le cuivre par $2^{3/2}=2{,}83$. La formulation « $r\times m$ = constante » est une
approximation commode ; l'invariant exact du modèle est $m\,r^{3/2}$. → § 05.6

**« Des chiffres ? »**
→ Pour 18 mH, calculés (pas encore bobinés) : 0,91 kg et 2,83 Ω en fil de 1,0 mm ; 2,02 kg
et 1,64 Ω en 1,4 mm ; 4,73 kg et 0,92 Ω en 2,0 mm. Le modèle prédit la résistance de trois
références de catalogue à ±4 % **sans aucun paramètre ajusté**, ce qui est ma validation
externe. La fenêtre praticable est étroite : au-delà de 2 Ω la self encaisse plus de 90 W au
niveau fort, en deçà de 1,5 Ω le fil dépasse 1,5 mm et n'est plus bobinable à la main.
→ § 05.5, § 05.7

**« Qu'est-ce que la bobine de Brooks ? »**
→ La géométrie qui maximise l'inductance **à longueur de fil donnée** : section carrée,
rayon intérieur $c$, rayon extérieur $2c$, longueur axiale $c$, donc rayon moyen $a=1{,}5c$.
Je la **retrouve** en minimisant le dénominateur $6a+9b+10c$ de la formule de Wheeler à
volume de bobinage constant (multiplicateur de Lagrange) : on obtient $b/a=2/3$ exactement,
et $c/a=0{,}600$ contre 0,667 pour le résultat exact. Et l'optimum est **plat** : à 10 % près
sur la forme, on perd 0,1 % d'inductance. → § 05.3, § 05.4

**« L'effet de peau ? »**
→ Négligeable ici : à 100 Hz l'épaisseur de peau dans le cuivre vaut 6,6 mm, très supérieure
au rayon du fil, et $R_{ac}/R_{dc}=1{,}00001$. En revanche l'**effet de proximité** dans un
bobinage à une vingtaine de couches peut atteindre +7 % (majorant) : je mesurerai donc
$\operatorname{Re}(Z)$ à 100 Hz au lieu d'identifier la résistance alternative à la
résistance continue. → § 05.15

---

### 2.6 Énergie, pertes, thermique

**« Où passe l'énergie ? »**
→ Cadrage d'abord, et il est brutal : un haut-parleur convertit de l'ordre de **2,5 % de
l'électricité en son**, tout le reste chauffe. Les pertes du filtre sont donc du second
ordre — mais ce sont les **seules sur lesquelles le concepteur a prise**. Le dire renforce
l'honnêteté du propos au lieu de l'affaiblir. → § 06.9

**« Combien perd-on dans la résistance de la self ? »**
→ Sur charge résistive, la fraction dissipée vaut $r/(R+r)$ : pour 1 Ω face à 8 Ω, **11,1 %
de la puissance**, soit $-0{,}51$ dB en puissance et $-1{,}02$ dB en niveau (tension aux
bornes du haut-parleur) — deux nombres différents qu'il faut nommer à chaque fois. Sur la
charge réelle la fraction n'est pas constante : environ 2 % au pic de résonance, 11 % en
bande passante, **33 % au voisinage du raccord**. D'où une évaluation **spectrale, sur
toutes les branches**, dans la fonction de coût. → § 06.1, § 08.5

**« La résistance de la self, c'est seulement une perte ? »**
→ Non, et c'est une contrepartie inattendue : elle **amortit** la surtension du filtre sur
la charge réelle (+10,8 dB → +8,0 dB sur le modèle typique). DCR et échauffement sont
d'ailleurs **le même levier** : ils s'ajoutent au même endroit du modèle. C'est pourquoi la
résistance de la self est à la fois un terme de pertes et un **paramètre de forme** dans
l'optimisation — elle n'est pas subie, elle est **choisie**. → § 06.4, § 04.1

**« Et quand ça chauffe ? »**
→ Le cuivre gagne $+0{,}39\ \%/\text{K}$. Sur un modèle thermique à une constante de temps
avec rétroaction (sous tension imposée, la puissance dissipée baisse quand $R_e$ monte),
50 W dissipés donnent $+92$ K en régime établi : $-2{,}7$ dB de sensibilité — **pour les
deux architectures** — et un déplacement du raccord de l'ordre de **+20 %** pour le passif.
Mais **au niveau domestique, quelques watts, la dérive n'est que de +2 %**. Il faut donc
toujours dire **à quelle puissance**. → § 06.5

**« Quel est le point de croisement énergétique entre passif et actif ? »**
→ L'actif consomme en permanence (AOP, alimentation, second canal d'ampli), le passif
consomme **proportionnellement au niveau**. En ramenant tout au compteur, avec $\eta$ le
rendement de l'amplificateur :
$$P^\star=\eta\,P_0\,\frac{t_{\text{on}}}{t_{\text{écoute}}}\Big/\left[\frac{r}{R+r}+(1-a^2)\varphi\right]$$
L'ordre de grandeur va de **2 à 18 W** selon $\eta$, l'existence d'un L-pad et le profil
d'usage — c'est-à-dire **à cheval sur la zone d'écoute domestique**. La conclusion est donc
conditionnelle, et elle repose sur trois grandeurs à mesurer : $r$, $P_0$ et $\eta$.
Complication honnête : l'ampli possède une mise en veille automatique, qui change la nature
même de la « consommation au repos ». [[réponse à compléter après la phase 4 : $P_0$, $\eta$
et $r$ mesurés]] → § 06.7, § 06.8

---

### 2.7 Acoustique

**« Pourquoi la mesure acoustique est-elle difficile à 100 Hz ? »**
→ Parce que $\lambda=3{,}4$ m : l'onde a la taille de la pièce. Une salle de 5 × 4 × 2,5 m
compte **33 modes propres sous 150 Hz, dont 13 à moins d'un tiers d'octave du raccord** ;
selon la position du micro, chacun ajoute ou retire plusieurs décibels. Une courbe relevée à
un mètre est celle du couple enceinte + pièce, pas celle du filtre. → § 07.1

**« Pourquoi ne pas fenêtrer temporellement, comme en mesure quasi-anéchoïque ? »**
→ Parce qu'une fenêtre de durée $T$ ne sépare pas deux fréquences plus proches que
$\Delta f=1/T$. Pour couper la première réflexion il faut une fenêtre de quelques
millisecondes, donc une résolution de l'ordre de **280 Hz** : à 100 Hz, le fenêtrage ne
mesure plus rien. → § 07.2

**« Alors comment mesurez-vous ? »**
→ En **champ proche** (Keele, 1974) : micro au ras de la membrane, où le champ direct écrase
le champ réverbéré. C'est valable jusqu'à environ 280 Hz pour un 18″ ($ka=1$), 140 Hz en
lecture prudente — limite « molle » que je **vérifie** par une mesure sur plan de sol plutôt
que de l'affirmer. La somme des deux voies est ensuite **calculée** à partir des deux champs
proches, avec les distances, les retards et la polarité ; à 100 Hz, ±10 cm d'erreur de
position ne coûtent que 0,04 dB. Limite assumée : ce n'est pas la réponse au point d'écoute.
→ § 07.3, § 07.4

**« Votre caisse a deux évents : le champ proche devant la membrane suffit-il ? »**
→ **Non, et c'est une conséquence directe du bass-reflex.** L'évent est une **seconde source**,
qui rayonne précisément là où la membrane ne bouge plus. Il faut donc mesurer aussi son champ
proche (micro au centre de l'embouchure) et le **sommer en complexe**, pondéré par le rapport
des surfaces :
$$p_{\text{tot}}=p_D+\sqrt{\frac{S_P}{S_D}}\,p_P,$$
avec $S_P$ la surface **totale des deux évents**. La somme exige la même référence temporelle
pour les deux mesures (boucle de retour), sans quoi les phases ne sont pas comparables. Deux
précautions : au niveau fort la capsule est dans le **jet d'air** de l'embouchure (bonnette
obligatoire, capsule légèrement décalée), et la mesure du bas du spectre est de toute façon
bornée par la consigne $f_{\text{start}}\ge2f_b$. En caisse close il n'y aurait rien à
corriger — c'est une manip en plus que ma caisse impose. → § 07.3

**« Que se passe-t-il à la somme des deux voies ? »**
→ Au 2ᵉ ordre, les deux voies sont à **180° l'une de l'autre** à la fréquence de raccord.
Sans rien faire, elles s'annulent : **trou profond**. Il faut donc **inverser la polarité
d'une voie** — concrètement, permuter les deux fils d'un haut-parleur — et la somme fait
alors une bosse de **+3,01 dB** (signature Butterworth) ou est **rigoureusement plate** si
l'on vise un alignement Linkwitz-Riley du 2ᵉ ordre. C'est le test le plus rapide et le plus
lisible de toute la phase 4 : bonne polarité → bosse, mauvaise → trou. → § 04.3, § 07.5

**« Quel est votre critère de fidélité, précisément ? »**
→ Un **écart RMS en décibels à la cible, sur 40–250 Hz**, grille logarithmique de 64 points,
niveau moyen retiré, avec un **plancher à 20 dB sous le maximum** — sans ce plancher, le
chiffre varierait de 7 à 1000 dB selon la grille, ce qui n'a pas de sens. Sur des courbes
idéales il vaut 0,6 dB pour un Butterworth inversé, 0 pour un Linkwitz-Riley, et 5,9 dB si
l'on oublie l'inversion de polarité. Tout est gelé avant les mesures : cible, plancher,
bande, seuil d'acceptation. Et **deux filtres séparés par moins de 2,3 fois l'écart-type ne
sont pas départagés** — je le dirai. → § 07.9

---

### 2.8 Comparaison avec la référence active

**« Pourquoi la solution active serait-elle meilleure ? »**
→ Par **construction**, pas par qualité intrinsèque : le filtre actif est placé **avant
l'amplificateur**, il n'est fait que de résistances de quelques kΩ et de condensateurs de
quelques nF, sa sortie est celle d'un amplificateur opérationnel, et le haut-parleur est
alimenté par l'ampli. **Il ne voit jamais $Z(f)$.** C'est donc l'étalon immunisé contre le
problème que j'étudie, et c'est ce qui en fait un point de comparaison utile — pas un
concurrent à battre. → § 04.11

**« Votre référence active est-elle exacte, alors ? »**
→ Non, et c'est une nuance importante : avec les valeurs normalisées, elle tombe à
$f_0=102{,}3$ Hz (+2,3 %), et ses quatre composants à tolérance donnent 4,6 % d'incertitude-type
(7,9 % en borne au pire cas). Elle n'est pas *exacte*, elle est **indépendante de la
charge** — c'est tout ce qu'on lui demande. → § 04.11

**« Elle n'a donc aucun défaut ? »**
→ Si : son talon d'Achille est l'**impédance de sortie du pré-amplificateur**, et il est
identifié et chiffré. Elle s'ajoute à la première résistance du passe-bas et se met en série
avec le condensateur d'entrée du passe-haut. Pour 1 kΩ, le passe-bas descend réellement de
4,6 % tandis que le passe-haut subit surtout une **perte d'insertion de 0,39 dB** — c'est-à-dire
un déséquilibre de niveau entre voies, pas un décalage de raccord (la fréquence de croisement
ne bouge que de 0,3 %). D'où : mesurer cette impédance de sortie, et insérer un étage tampon
si elle dépasse quelques centaines d'ohms — pour le prix d'un amplificateur opérationnel.
[[réponse à compléter après la phase 1 : $Z_s$ du pré-ampli mesurée]] → § 04.11

**« Alors, passif ou actif ? »**
→ Ce n'est pas ma question — c'était celle de ma première version, et je l'ai abandonnée
parce que la réponse était connue d'avance. Ma question est : **de combien un filtre passif
optimisé sur l'impédance mesurée comble-t-il l'écart, et à quel prix en composants, en
pertes et en matière ?** La réponse se lit dans le tableau des critères gelés, avec deux
comptabilités de coût (marginale, l'ampli étant déjà possédé ; système, dans un scénario
stéréo complet) et le point de croisement énergétique.
[[réponse à compléter après la phase 4 : tableau comparatif complet]]

---

### 2.9 Limites et perspectives

**« Quelles sont les limites de votre travail ? »** *(à annoncer spontanément, avant qu'on
ne les demande)*
→ Quatre, et je les cite dans cet ordre :
(i) le modèle est **petit signal** et à deux degrés de liberté seulement — membrane et
colonne d'air des évents — il ignore $Bl(x)$, la dérive thermique, les modes de membrane et
les résonances propres des tubes d'évent ;
(ii) la mesure acoustique est en **champ proche**, ce n'est donc pas la réponse au point
d'écoute ;
(iii) l'optimisation porte sur une charge **identifiée à un instant, à un niveau et à une
température donnés** ;
(iv) les incertitudes de composants (±10 % sur une self, jusqu'à ±20 % sur un condensateur
électrolytique bipolaire) dispersent la fréquence de raccord de quelques pour cent.
→ § 01.12, § 07.3, § 04.9

**« Si c'était à refaire ? »**
→ Je commencerais encore par la chaîne de mesure d'impédance : tout le reste en dépend, et
c'est elle qu'on étalonne sur des composants connus avant de toucher au haut-parleur. La
leçon que je retiens est qu'il faut **geler ses critères et ses définitions avant de
mesurer** — sinon la conclusion se choisit après coup.

---

### 2.10 Ancrage au thème « Sobriété, efficacité, optimisation »

**« En quoi votre sujet répond-il au thème ? »** *(question à laquelle il faut pouvoir
répondre sur demande, en trois grandeurs mesurées)*
→ **Optimisation** : une fonction de coût explicite, des contraintes réelles (valeurs E12,
budget, impédance minimale de l'ampli) et une énumération exhaustive de 331 776 designs.
**Sobriété** : la matière — la masse de cuivre de la self, liée aux pertes par
$m=K_{Cu}(L/r)^{3/2}$ — et le coût, présenté en deux comptabilités.
**Efficacité** : les pertes Joule du passif face à la consommation permanente de l'actif,
et le niveau d'écoute où l'un devient plus sobre que l'autre.
Les trois sont des **grandeurs mesurées** (€, kg, W), jamais un argumentaire d'achat.
→ § 08.5

**« Votre travail est-il "sobre" ou seulement "moins cher" ? »**
→ Les deux comptabilités répondent : en **coût marginal**, l'amplificateur étant déjà
possédé, l'actif est avantagé ; en **coût système**, un scénario stéréo complet demande deux
fois plus de canaux d'amplification en bi-amplification, et le passif reprend l'avantage.
Je présente **les deux**, avec la même frontière de bilan des deux côtés, et je dis ce que
le bilan **ne compte pas** : l'énergie grise du cuivre, les pertes des condensateurs, le
profil d'usage réel. → § 06.9

---

## 3. Questions pièges — à préparer mot à mot

**« Si vous optimisez sur un $Z(f)$ mesuré à faible niveau, que se passe-t-il à fort
niveau ? »**
→ C'est **la** limite du sujet, et je l'ai anticipée : mon filtre optimisé n'est juste que
pour le $Z(f)$ mesuré, c'est-à-dire un niveau et une température. À fort niveau, la bobine
chauffe, $R_e$ monte de $0{,}39\ \%/\text{K}$ — à 50 W dissipés, $+92$ K, soit $+39$ % de
résistance — et l'excursion déplace la résonance par les non-linéarités $Bl(x)$ et $k(x)$.
C'est précisément pourquoi le critère de **robustesse** est gelé dès le départ : je refais la
mesure du raccord **aux deux niveaux d'écoute de référence**, bobine chaude après
conditionnement, avec relevé de $R_e$ avant et après chaque balayage. Si la dérive est
significative, c'est un **résultat**, et c'est même l'argument le plus fort en faveur de
l'architecture active. [[réponse à compléter après la phase 4 : dérive mesurée entre les
deux niveaux]] → § 06.5, § 06.6, § 07.8

**« Pourquoi ne pas simplement prendre la solution active, puisqu'elle est immunisée ? »**
→ Trois raisons, et aucune n'est « parce que c'est plus joli ». **Un** : la question du TIPE
n'est pas de choisir une architecture mais de savoir **de combien on peut corriger un filtre
passif quand on connaît la charge** — c'est un problème de conception sous contraintes, pas
un achat. **Deux** : l'actif a une consommation **permanente**, le passif des pertes
**proportionnelles** ; il existe donc un niveau d'écoute sous lequel le passif est plus
sobre, et ce point de croisement est mesurable. **Trois** : en coût système, l'actif double
le nombre de canaux d'amplification. Et j'ajoute une raison de méthode : l'actif est mon
**étalon**, il faut donc le garder à sa place — comparer contre lui, pas contre son absence.

**« Votre optimiseur retrouve-t-il le Butterworth du cours ? »**
→ Oui, et c'est ma porte de validation avant tout achat : sur 8 Ω résistifs, l'optimiseur
continu redonne 18,0063 mH et 140,674 µF, à $10^{-6}$ près des valeurs analytiques. Je
distingue soigneusement ce théorème du résultat **E12** (18 mH / 150 µF), qui dépend, lui, des
pondérations de la fonction de coût : c'est un test de non-régression, pas une vérité
mathématique. S'il n'y retombait pas, il y aurait un bug — et rien ne s'achèterait.
→ § 04.7, § 09.6

**« Quelle est la taille de votre espace de recherche ? »**
→ $24^4=331\,776$ points sur la grille E12, énumérés en environ 2 secondes avec numpy seul.
Je précise deux choses, parce qu'elles sont honnêtes et qu'elles font la différence : cette
grille est une **idéalisation de catalogue** — une self bobinée maison est une variable
quasi continue, quantifiée par le nombre de spires, et les gros condensateurs bipolaires ne
suivent pas E12 — donc le problème réel est **mixte** ; et si j'énumérais aussi le réseau de
Zobel, on passerait à 96 millions de points, ce qui justifie de le traiter comme un booléen.
→ § 04.5

**« Qu'est-ce qui est de vous dans ce travail ? »**
→ Répondre en gestes concrets, pas en généralités : l'enceinte a été construite et câblée
par moi ; le montage de mesure d'impédance, son étalonnage et les relevés sont de moi ; le
code d'analyse est écrit et testé par moi, y compris l'algorithme de Levenberg-Marquardt
réécrit en numpy pour ne pas dépendre d'une bibliothèque ; le choix, le chiffrage et le gel
des critères sont de moi ; la self est bobinée et mesurée par moi. Et dire aussi ce qui ne
l'est pas : les modèles (Thiele, Small, Wheeler, Brooks) viennent de la littérature citée,
les logiciels utilisés sont REW, LTspice et Python, et l'aide reçue (enseignants, outils de
mise en forme) est mentionnée. **Ne rien surjouer : un jury repère une contribution gonflée
plus vite qu'une contribution modeste.** [[réponse à compléter : liste exacte des gestes
réalisés, à tenir à jour dans le cahier de laboratoire]] → § 08.5 (critère B3)

**« Pourquoi avoir changé de sujet en cours de route ? »**
→ Parce que ma première version répondait à la question « passif ou actif ? », dont la
réponse est essentiellement connue d'avance : cela faisait une **recette**, pas un
questionnement. En préparant les mesures, je me suis aperçu que le vrai obstacle n'était pas
le choix d'architecture mais le fait que **toutes les formules de dimensionnement supposent
une charge de 8 Ω qui n'existe pas**. J'ai donc recentré le sujet sur cette difficulté :
mesurer la charge, l'identifier, et optimiser dessus. Le travail de la première version n'est
pas perdu — il fournit le filtre catalogue de référence et la référence active. Ce
changement est de l'esprit critique exercé au bon moment, et c'est aussi ce que le DOT
demande de raconter : les jalons, y compris les réorientations.

**« Votre comparaison est-elle équitable ? »**
→ Je l'ai rendue équitable **avant** de mesurer : mêmes critères pour les trois
architectures, mêmes deux niveaux d'écoute, même bande, même frontière de bilan énergétique,
et aucun critère ajouté ou retiré après les premières mesures comparatives. Le seul biais
que je revendique est structurel et je l'annonce : la référence active est immunisée **par
construction**, ce n'est donc pas un concurrent à armes égales, c'est un étalon.

**« Et si vos mesures ne marchent pas ? »**
→ Chaque phase a une **porte de validation** et un repli écrits d'avance : si la carte son
pose problème, je reviens au GBF et à l'oscilloscope point par point ; si l'ajustement
bass-reflex à sept ou huit paramètres échoue au $\chi^2$, je dispose de deux replis **déjà
codés** — un modèle **phénoménologique à deux résonances**, qui décrit les deux pics sans
prétendre nommer $f_b$ ni $Q_l$ (c'est suffisant pour l'acte 3, qui ne voit que $Z(f)$), et un
modèle de bobine à pertes si c'est le haut du spectre qui résiste ; si le filtre catalogue
viole la contrainte d'impédance, le solveur le signale avant l'achat. Un échec documenté et
diagnostiqué vaut mieux qu'un résultat non vérifié.
→ § 02.8, § 03.7, § 04.7

---

## 4. Check-list « savoir refaire au tableau »

Huit gestes à savoir écrire de mémoire, avec leur nombre de contrôle.

**1. Dimensionnement Butterworth 100 Hz sur 8 Ω.**
Cellule LC chargée en parallèle par $R$ : $\omega_0=1/\sqrt{LC}$ et $Q=R\sqrt{C/L}$.
Butterworth $\Rightarrow Q=1/\sqrt2$, donc
$$L=\frac{\sqrt2\,R}{2\pi f_0}=18{,}01\ \text{mH},\qquad C=\frac{1}{\sqrt2\,R\,2\pi f_0}=140{,}7\ \mu\text{F}.$$
Valeurs normalisées retenues : **18 mH / 150 µF**. *(Piège : $Q=\frac1R\sqrt{L/C}$ est celui
du RLC **série** — préciser la topologie.)* → § 04.1

**2. Ce que valent réellement les fréquences du filtre catalogue 18 mH / 150 µF sur 8 Ω.**
Pôle $f_0=1/(2\pi\sqrt{LC})=\mathbf{96{,}86}$ Hz ; $Q=R\sqrt{C/L}=0{,}7303$ ;
$-3$ dB du passe-bas **99,9 Hz**, du passe-haut **93,9 Hz** ; contrôle :
$f_{-3,PB}\cdot f_{-3,PH}=f_0^2$. *(Le couple « 99,8 / 94,0 » qui a circulé dans le projet
n'est pas fautif : ce sont les valeurs au seuil littéral $-3{,}000$ dB, quand 99,93 / 93,88 Hz
sont celles à mi-puissance $-3{,}0103$ dB. Les deux sont exactes ; la convention retenue ici
est la mi-puissance, celle de REW. Toujours nommer la convention.)* → § 04.1, § 08.5

**3. Définition retenue de $f_c$.** Le même filtre admet **quatre** « fréquences de
coupure » qui ne coïncident pas dès que la self a une résistance ou que la charge n'est pas
résistive : le pôle, le $-3$ dB par rapport à 0 dB absolu, le $-3$ dB par rapport au gain de
bande passante, et la **fréquence de croisement des deux voies**. Pour une résistance de
self de 2 Ω, la même réalité physique se note $-18$ % ou $+10$ % selon la convention, alors
que le croisement ne bouge que de 0,8 %. **Une seule définition doit être gelée et employée
partout — tableaux de critères, diapositives, portes de validation.**
**Tranché le 2026-09-13** : $f_c$ = la **fréquence de croisement des deux voies**
($|H_{PB}|=|H_{PH}|$), seule définition insensible à la perte d'insertion — § 04.1 fait foi et
est le seul passage à porter ce statut. Le pôle (96,86 Hz) et les deux $-3$ dB restent cités
comme **repères nommés**, jamais comme « la » coupure. À confirmer et dater dans
`DECISIONS-PHASE-0.md` (décision D1). → § 04.1, § 07.0, § 08.5

**4. Pertes dans la résistance de la self.** Fraction dissipée $=r/(R+r)$. Pour $r=1$ Ω et
$R=8$ Ω : **11,1 % de la puissance**, soit $10\log_{10}(8/9)=-0{,}51$ dB en **puissance** et
$20\log_{10}(8/9)=-1{,}02$ dB en **niveau** (tension aux bornes du haut-parleur). Toujours
dire laquelle des deux. Sur charge réelle, remplacer $R$ par $\operatorname{Re}\{Z(f)\}$ :
la fraction va d'environ 2 % au pic à 33 % près du raccord. → § 06.1, § 08.5

**5. Résonance LC (méthode de mesure de la self).** En série,
$f_{rés}=1/(2\pi\sqrt{LC})$ : avec 18 mH et un condensateur connu de 150 µF, on attend un
pic vers **97 Hz** au GBF et à l'oscilloscope. C'est la contre-vérification de la mesure
d'inductance faite au banc d'impédance. → § 05.13

**6. Propagation d'incertitude sur $f_0$ — formule du LC, PAS celle du RC.**
$$f_0=\frac{1}{2\pi\sqrt{LC}}\quad\Longrightarrow\quad
\frac{u(f_0)}{f_0}=\frac12\sqrt{\left(\frac{u_L}{L}\right)^2+\left(\frac{u_C}{C}\right)^2}$$
Le facteur $\frac12$ est la **signature de la racine carrée** : c'est lui que la formule du
RC du premier ordre ignorait. Pour $u_L/L=u_C/C=\pm10$ % : **7,1 % en borne au pire cas**,
**4,1 % en incertitude-type** (loi rectangulaire, $u=a/\sqrt3$, convention GUM retenue) ;
avec un condensateur électrolytique à ±20 % : 11,2 % en borne, 6,5 % en incertitude-type.
**Ne jamais reprendre le « 11 % » de la version 1** : il venait d'un filtre RC du premier
ordre abandonné, et il traîne encore dans les diapositives v1 — à purger avant tout
réemploi. → § 04.9, § 08.6, § 09.5

**7. Écrire $Z(j\omega)$ et nommer ses cinq paramètres** — voir § 2.1 ci-dessus. Savoir dire
d'où vient la branche motionnelle (mécanique série $\to$ électrique parallèle par $Bl$) et
pourquoi $|Z|\ge R_e$ partout (la branche ajoutée est passive). Et **enchaîner sur le
bass-reflex** : ce modèle-là suppose la caisse close, ma caisse ne l'est pas. → § 01.3

**8. Accord d'un résonateur de Helmholtz à $N$ évents, et pourquoi il y a deux pics.**
*La caisse est en bass-reflex, à **deux** évents : c'est le geste qui manquait à la v1.*

*(a) La formule.* Un évent est une **masse d'air** (la colonne du tube) sur un **ressort**
(l'air de la caisse). Pour $N$ évents identiques de section $S_v$ et de longueur $L_v$, montés
en parallèle sur le même volume $V_b$, les masses acoustiques se composent **en parallèle**
(la masse totale est divisée par $N$) :
$$M_{ap}=\frac{\rho_0\,L_{\text{eff}}}{N\,S_v},\qquad
C_{ab}=\frac{V_b}{\rho_0c^2},\qquad
f_b=\frac{1}{2\pi\sqrt{M_{ap}C_{ab}}}
=\frac{c}{2\pi}\sqrt{\frac{N\,S_v}{V_b\,L_{\text{eff}}}}.$$
$L_{\text{eff}}=L_v+\delta$ est la longueur **corrigée des effets de bout** : le tube entraîne
un peu d'air au-delà de ses extrémités. Correction classique $\delta\approx0{,}85a$ par
extrémité bridée (débouchant dans le baffle) et $\approx0{,}61a$ par extrémité libre, soit
$\delta\approx1{,}46a$ pour un évent classique ($a$ = rayon). *(Contrôle dimensionnel :
$c\sqrt{\text{m}^2/(\text{m}^3\cdot\text{m})}=\text{s}^{-1}$. Deux réflexes : **doubler le
nombre d'évents à section donnée monte $f_b$ de $\sqrt2$**, et **allonger l'évent baisse
$f_b$** — c'est ainsi qu'on accorde une caisse.)* Les dimensions des deux évents et le volume
interne sont **[[à mesurer]]** : c'est ce qui rend la prédiction de $f_b$ **falsifiable**
avant même de brancher le banc d'impédance.

*(b) Pourquoi deux pics.* Deux oscillateurs couplés $\Rightarrow$ deux modes. À l'accord, la
membrane est **quasi immobile** (c'est l'évent qui rayonne), donc $Bl\,v\to0$, donc la branche
motionnelle s'efface et **$|Z|$ retombe près de $R_e$** : c'est le **creux**, situé en
$f\approx f_b$. Il est encadré par deux pics $f_L<f_b<f_H$, et le modèle donne deux identités
à savoir citer :
$$f_L\,f_H=f_s\,f_b,\qquad f_L^2+f_H^2=f_s^2(1+\alpha)+f_b^2,$$
avec $\alpha=V_{as}/V_b$. La première est le **contrôle de cohérence** le plus rapide sur une
courbe mesurée : le produit des deux pics doit valoir le produit $f_sf_b$. *(Piège à éviter :
le creux ne descend pas jusqu'à $R_e$ — les pertes de caisse $Q_l$ le relèvent ; et un pic
mesuré plus bas que la théorie n'est pas une erreur de mesure, ce sont ces mêmes pertes.)*
→ § 01.10

---

## 5. Perspectives et pistes écartées

Réserve de réponses pour « pourquoi n'avez-vous pas fait … ? ». Chaque piste a été
**envisagée** et **écartée pour une raison**, pas ignorée.

| Piste | Ce que c'est | Pourquoi écartée |
|---|---|---|
| **Servo-woofer** (asservissement par accéléromètre sur la membrane) | Boucle de contre-réaction qui impose l'accélération, donc la pression | Relève de l'automatique, vue trop tard dans le cursus ; mise au point expérimentale trop risquée sur une année |
| **Filtrage numérique FIR à phase linéaire** | Correction en amont par traitement du signal, phase et amplitude découplées | Le cœur du travail deviendrait du traitement du signal (échantillonnage, fenêtrage, latence), hors programme et hors du questionnement choisi |
| **Non-linéarités $Bl(x)$ et $k(x)$** | Origine de la distorsion et de la dérive de la résonance avec l'excursion | Très riche, mais $Bl(x)$ est difficile à caractériser avec le matériel disponible : resterait semi-quantitatif. **Revient par la bande** dans le critère de robustesse |
| **Compression thermique comme axe principal** | Modèle $R_e(T)$ à une ou deux constantes de temps, mesure de la dérive | Non retenue comme axe, mais **intégrée** comme critère de robustesse (mesures aux deux niveaux gelés) et dans le croisement énergétique — § 06.5 |
| **Directivité et lobes d'interférence au raccord** | Deux sources non colocalisées interfèrent différemment selon l'angle | Bon complément (mesures polaires), écarté faute de place dans 15 minutes ; le décalage acoustique entre voies est néanmoins pris en compte dans la pondération de phase — § 04.5 |
| **Modes de pièce et placement optimal** | Sources images, position enceinte/auditeur | Vrai sujet, mais c'est un **autre** sujet : il porte sur la pièce, pas sur le filtre. La mesure en champ proche est justement là pour s'en affranchir — § 07.1 |
| **Réseau de compensation RLC du pic** | Linéariser $Z(f)$ au lieu d'optimiser dessus | Efficace mais hors de prix en matière et en chaleur (2,4 mF, résistance dissipant sept fois la puissance reçue par le HP à la résonance) — § 04.4 |
| **Alignement Linkwitz-Riley d'ordre 4** | Somme plate **sans** inversion de polarité | Quatre gros composants par voie en passif ; trivial en actif par cascade. Reste en perspective légitime — § 04.3 |
| **Self à noyau ferrite ou fer** | Divise la résistance par ~7 et la matière par plus de 2 | Impose de vérifier $L(I)$ (saturation) ; la marge est faible à 350 W. Excellent satellite si le temps le permet — § 05.11 |
| **Architecture « RC signal faible du 1ᵉʳ ordre »** | Contre-exemple de la version 1 | **Abandonnée avec la v1** : elle n'a plus de rôle dans le récit v2. Ne pas la mentionner |

---

## 6. Incohérences encore ouvertes — à trancher **avant** de figer les supports

Les nommer ici évite d'être pris en défaut sur le critère « rigueur des définitions ».

1. ~~**Définition de $f_c$**~~ — **résolu le 2026-09-13** : fréquence de croisement des deux
   voies (§ 04.1, seul passage à porter ce statut) ; § 07.0 et § 08.5 sont alignés, les autres
   fréquences sont des repères nommés. Reste à dater dans `DECISIONS-PHASE-0.md` (D1).
2. **Cible de sommation** : `FEUILLE-DE-ROUTE.md` écrit « cible plate » (= Linkwitz-Riley 2,
   27 mH / 100 µF) là où les illustrations utilisent la cible Butterworth (+3 dB à $f_c$).
   Les deux ne peuvent pas être gelées ensemble. [[à geler en phase 0]] → § 04.3
3. **Bande de la fonction de coût** : arrêtée à 250 Hz, l'optimiseur rabat $C_1$ sur la
   borne basse (le passe-bas tend vers un 1ᵉʳ ordre) ; il faut soit imposer un plancher sur
   $C_1$, soit élargir la bande à au moins 1 kHz. [[à trancher en phase 0]] → § 04.8
4. **Modèle économique de la self** : les deux placeholders de la version brouillon se
   contredisaient d'un facteur 4,2 et pénalisaient deux fois le cuivre. Le bon modèle passe
   par la masse ($m=K_{Cu}(L/r)^{3/2}$). [[à intégrer avant la phase 3]] → § 04.5, § 05.9
5. ~~**« ≈ 10 min » et « ± 11 % »**~~ — **résolu** : corrigés le 2026-09-13 dans tous les
   `.md` et dans `index.html`, puis dans les deux présentations lors de leur refonte v2. Le
   « ± 11 % » ne subsiste plus qu'en **annexe A3** de `presentation-finale.html`, comme
   contre-exemple explicitement réfuté. Le format est **15 min + 15 min**, et l'incertitude
   sur $f_0$ s'écrit en couple (7,1 % borne au pire cas / 4,1 % incertitude-type). → § 08.6
6. ~~**Gabarit 16:9 → 4/3**~~ — **fait** : les deux présentations et les figures de
   `analyse/figures.py` sont en 1024×768 depuis la refonte v2 ; reste seulement à signer D7.
   → § 08.2
7. **Professeur encadrant** : sa déclaration à l'étape 1 et sa validation à l'étape 3 sont
   obligatoires ; sans elles, la note peut être nulle. **M. Chevalier, accord obtenu le
   16/09/2026 (D10)** ; restent le compte lycees.scei-concours.fr et l'avertissement sur la
   fenêtre de 8 jours de mi-juin 2027 (`PARCOURS.md` 1-A3). → § 08.3
8. ~~**Type de caisse du sub**~~ — **résolu le 2026-09-16** (constat de l'étudiant, décision
   D8) : la caisse est **bass-reflex, à deux évents**. Ce n'était pas une inconnue de
   modélisation mais le **choix du modèle direct** : le modèle à 7-8 paramètres était déjà
   écrit et testé **parce que** le type de caisse n'était pas établi — ce n'est donc pas une
   reprise, c'est une hypothèse qui se lève. Purger de tout support la formulation « clos ou
   bass-reflex, à documenter ». **Reste ouvert** : dimensions des deux évents et volume
   interne [[à mesurer]], nécessaires au recoupement géométrique de $f_b$.
9. **Condensateur en série avec les pavillons d'ultra-aigu** : **présent** (constat du
   16/09/2026) ; valeur [[à mesurer]] au bornier. Elle ne change **ni** le protocole (on
   mesure le bloc médiums tel qu'il est câblé) **ni** le modèle du filtre, seulement
   l'ampleur de la contribution de la branche aigu à la charge du passe-haut (−10 à −26 % sur
   $|Z|$ du bloc à 100 Hz pour 3,3 à 10 µF, calculé). → § 2.1

---

## 7. À faire avant la soutenance

- [ ] Geler les critères, les deux niveaux d'écoute, la définition de $f_c$ et la cible de
      sommation — **datés et signés avant la première mesure comparative**.
- [ ] Franchir les portes de validation dans l'ordre : étalonnage sur résistance et
      condensateur connus → $Z(f)$ en caisse → identification → sanity check 8 Ω → mesures.
- [ ] **Relever la géométrie du bass-reflex avant la phase 1** : diamètre et longueur des
      **deux** évents, volume interne de la caisse — pour prédire $f_b$ par Helmholtz
      **avant** de le lire sur la mesure (passage par zéro de la phase entre les deux pics,
      ou ajustement). Une prédiction publiée avant la mesure
      vaut beaucoup plus qu'un accord constaté après.
- [ ] **Relever la valeur du condensateur des pavillons** (présent depuis le constat du
      16/09/2026), contrôler le câblage à l'ohmmètre (environ 6 à 7 Ω en continu) et
      photographier le bornier ; consigner la valeur, ne pas la supposer.
- [ ] Remplacer chaque `[[réponse à compléter]]` de ce document par le chiffre mesuré, ou
      l'assumer à voix haute comme non mesuré.
- [ ] Tenir le **cahier de laboratoire daté** dès la première mesure : c'est la matière du
      DOT et le seul document papier réellement admis en salle.
- [ ] Photographier le jig, le bobinage et le filtre monté **avant tout démontage** — aucun
      objet n'entre en salle.
- [ ] Imprimer les listings Python en **double exemplaire** et les annexer après la
      conclusion du PDF.
- [ ] Répéter devant un « candide » : si la première minute ne fait pas comprendre pourquoi
      un haut-parleur n'est pas une résistance de 8 Ω, l'exposé est à reprendre.
