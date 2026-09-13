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

1. Une enceinte deux voies DIY (sub 18″ 8 Ω, deux médiums 4 Ω en série) doit être coupée
   en deux bandes autour de **100 Hz** : le grave au 18″, le reste aux médiums, qu'il faut
   tenir au-dessus de leur résonance.
2. Les formules de filtrage du cours et des catalogues supposent une charge **résistive de
   8 Ω**. Pour le Butterworth du 2ᵉ ordre : $L=\sqrt2R/\omega_0=18{,}0$ mH et
   $C=1/(\sqrt2R\omega_0)=140{,}7$ µF, soit 18 mH / 150 µF en valeurs normalisées.
3. Or **le haut-parleur n'est pas une résistance de 8 Ω** : c'est un système
   électromécanique dont l'impédance possède un pic de résonance et une remontée
   inductive. Sur la bande du raccord, son module varie d'un facteur de l'ordre de 20 et
   sa phase de plus de 100° (§ 01.8, modèle typique — **à mesurer**).
4. **Acte 1 — mesurer.** Relever $Z(f)$, module et phase, avec une chaîne étalonnée
   d'abord sur une résistance et un condensateur connus, et des incertitudes chiffrées.
5. **Acte 2 — identifier.** Remonter de la courbe aux cinq paramètres du modèle de
   Thiele-Small par **moindres carrés pondérés** : c'est un **problème inverse**, validé
   par le $\chi^2$ réduit, la structure des résidus et trois estimateurs d'incertitude.
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
l'ajustement. → § 03.1

**« "Du simple au sextuple", d'où sort ce chiffre ? »**
→ Le rapport pic/plancher vaut $|Z|_{max}/R_e=1+Q_{ms}/Q_{es}$ ; ce n'est donc pas un
accident, c'est le rapport des amortissements mécanique et électrique. Ce chiffre a été
**retiré de la problématique** : il n'était pas mesuré et il était trop bas. Les fiches de
18″ de sonorisation donnent $|Z|_{max}$ entre 60 et 200 Ω (Delta Pro-18A : 172 Ω calculé),
soit ×8 à ×25 face à 8 Ω nominaux ; l'ordre de grandeur 40–60 Ω hérité de la v1 est celui du
**bloc médiums**, pas du 18″. Les pertes de la caisse rabaissent le pic. La problématique dit
donc « varie fortement avec la fréquence », et le rapport sera chiffré après la phase 1.
[[réponse à compléter après la phase 1 : rapport max/min mesuré en caisse]] → § 01.8

**« Votre $f_s$ mesurée ne correspond pas à la datasheet. »** *(piège classique)*
→ C'est attendu, et ce n'est pas une erreur. La datasheet donne $f_s$ en champ libre ; je
mesure le haut-parleur **en caisse**. En caisse close, le ressort d'air s'ajoute à la
suspension et monte la résonance : $f_c=f_s\sqrt{1+V_{as}/V_b}$. En bass-reflex, il y a
**deux pics** et un creux à l'accord de l'évent. Le paramètre utile à mon filtre est celui
**en caisse**, puisque c'est cette impédance-là que le filtre voit. → § 01.9, § 01.10

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
18″ vaut $R_e(1+Q_{ms}/Q_{es})$, soit plusieurs dizaines d'ohms : avec $R_{ref}=100$ Ω, le
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
multimètre, et sa tolérance reportée à part. → § 03.5

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
la **structure des résidus** le trahissent. J'utilise le test des séquences de
Wald-Wolfowitz sur les signes des résidus : $z=+0{,}4$ pour le bon modèle,
$z=-5{,}6$ pour une bobine à pertes ajustée avec $L_e$ constante. → § 03.7

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
réponse qui se déforme. → § 04.1, § 04.2, § 01.8

**« Un résultat qui vous a surpris ? »**
→ Oui : sur la charge typique, la contrainte « impédance vue par l'amplificateur
$\ge4\ \Omega$ » **disqualifie le filtre catalogue avant même la comparaison de fidélité**
(minimum à 3,51 Ω). Et ce n'est pas un cas pathologique isolé : **162 des 576** couples
$(L_1,C_1)$ de la grille violent cette contrainte même sur 8 Ω résistif. Le design optimisé,
lui, remonte ce minimum à 11,3 Ω. C'est une contrainte de sécurité matérielle, gratuite à
calculer, et que la v1 ignorait. → § 04.8

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
(i) le modèle est **petit signal** et à un degré de liberté — il ignore $Bl(x)$, la dérive
thermique et les modes de membrane ;
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
pose problème, je reviens au GBF et à l'oscilloscope point par point ; si l'ajustement à
cinq paramètres échoue au $\chi^2$, je passe au modèle de bobine à pertes à six paramètres,
déjà codé ; si le filtre catalogue viole la contrainte d'impédance, le solveur le signale
avant l'achat. Un échec documenté et diagnostiqué vaut mieux qu'un résultat non vérifié.
→ § 02.8, § 03.7, § 04.7

---

## 4. Check-list « savoir refaire au tableau »

Six gestes à savoir écrire de mémoire, avec leur nombre de contrôle.

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
pourquoi $|Z|\ge R_e$ partout (la branche ajoutée est passive). → § 01.3

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
5. **« ≈ 10 min » et « ± 11 % »** — corrigés le 2026-09-13 dans tous les `.md` et dans
   `index.html`. Il n'en subsiste que dans `presentation-finale.html` (l. 1073 et 1173),
   support v1 en attente de refonte : le format est **15 min + 15 min**, et l'incertitude sur
   $f_0$ s'écrit en couple (7,1 % borne au pire cas / 4,1 % incertitude-type). À corriger
   avant tout réemploi d'une diapositive. → § 08.6
6. **Gabarit 16:9 → 4/3** : à changer **dès la phase 0**, sinon toutes les figures des
   phases 2 à 4 seront à refaire. → § 08.2
7. **Professeur encadrant** : sa déclaration à l'étape 1 et sa validation à l'étape 3 sont
   obligatoires ; sans elles, la note peut être nulle. [[action datée, rentrée septembre]]
   → § 08.3

---

## 7. À faire avant la soutenance

- [ ] Geler les critères, les deux niveaux d'écoute, la définition de $f_c$ et la cible de
      sommation — **datés et signés avant la première mesure comparative**.
- [ ] Franchir les portes de validation dans l'ordre : étalonnage sur résistance et
      condensateur connus → $Z(f)$ en caisse → identification → sanity check 8 Ω → mesures.
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
