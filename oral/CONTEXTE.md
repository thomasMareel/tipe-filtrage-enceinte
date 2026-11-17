# Contexte de l'oral du 18 novembre 2026

> À lire avant de toucher au dossier `oral/`. Ce fichier se suffit à lui-même : il
> résume le projet pour quelqu'un (ou une session de Claude) qui n'a pas suivi les
> échanges. Les sources détaillées restent `CLAUDE.md`, `FEUILLE-DE-ROUTE.md` et
> `DECISIONS-PHASE-0.md`, à la racine du dépôt.

## 1. L'oral en bref

- **Qui** : Thomas Mareel, classe préparatoire PT (après une PTSI), TIPE **individuel**,
  session 2027. Professeur encadrant : M. Chevalier.
- **Quoi** : une **présentation du projet** devant les professeurs du lycée, le mercredi
  18 novembre 2026. Ce n'est pas l'épreuve du concours : les professeurs savent que rien
  n'est encore mesuré. Le but est d'expliquer ce qui va être fait, en insistant sur les
  **expériences**.
- **Format** : environ **8 minutes** d'exposé (script : 8 min 09 au débit de référence),
  suivies de questions, surtout sur la **faisabilité** du sujet.
- **Support** : `oral/presentation.pdf`, 15 pages au format 4:3. Il contient 12 vues
  présentées et 3 annexes gardées pour les questions. Il est projeté depuis un ordinateur
  du lycée. Le support source est `presentation-projet.html`, à la racine.
- **Thème national** du TIPE 2027 : « Sobriété, efficacité, optimisation ».

## 2. La problématique

> « Comment concevoir le filtre de raccord à 100 Hz d'une enceinte deux voies pour qu'il
> tienne sa cible sur la charge réelle — un haut-parleur dont l'impédance varie fortement
> avec la fréquence — au moindre coût en composants, en pertes et en matière ? »

**L'idée en trois phrases :**
1. L'enceinte, construite par Thomas, a un caisson de basses de 18 pouces (en caisse
   bass-reflex à deux évents) et un bloc de médiums.
2. Le filtre qui partage le signal entre les deux à 100 Hz se calcule d'habitude comme si
   chaque haut-parleur était une résistance de 8 Ω. Or l'impédance réelle d'un haut-parleur
   dans sa caisse varie fortement avec la fréquence : deux pics et un creux pour un
   bass-reflex.
3. Le TIPE consiste à mesurer cette impédance réelle, puis à concevoir le filtre pour elle
   au lieu de la résistance idéale, en tenant compte du coût, des pertes et du cuivre.

## 3. La démarche : quatre étapes, quatre expériences

**Les quatre étapes :**
1. **Mesurer** l'impédance Z(f) du caisson et des médiums (expérience).
2. **Identifier** un modèle physique du haut-parleur, le modèle de Thiele-Small à 8
   paramètres, par ajustement aux moindres carrés : c'est un problème inverse (calcul).
3. **Optimiser** les valeurs des bobines et des condensateurs parmi les valeurs
   normalisées (série E12), sous contraintes : l'ampli ne doit jamais voir moins de 4 Ω,
   et on tient compte du coût et des pertes (calcul).
4. **Fabriquer et valider** : bobiner les selfs, puis comparer au banc et au micro
   (expériences).

**Les quatre expériences :**

| Expérience | Ce qu'on fait | Ce qu'elle apporte |
|---|---|---|
| 1. Mesurer Z(f) | Carte son Focusrite Scarlett Solo et logiciel REW ; une résistance connue de 100 Ω en série avec le haut-parleur ; on lit deux tensions et on en déduit Z = R·V_B/(V_A − V_B). Étalonnage d'abord sur une résistance et un condensateur connus, recoupement avec le GBF et l'oscilloscope du lycée. | La charge réelle sur laquelle tout est calculé |
| 2. Bobiner les selfs | Bobines à air, sans noyau, avec une prise intermédiaire ; mesure de l'inductance, de la résistance du fil et de l'échauffement | Le lien entre pertes et masse de cuivre (sobriété) |
| 3. Banc électrique | Le filtre catalogue puis le filtre optimisé, branchés sur les vrais haut-parleurs, un canal d'ampli par voie | Confronter la prédiction du calcul au réel |
| 4. Micro et wattmètre | Mesure en champ proche (membrane et deux évents), test de polarité, comparaison avec un filtre actif à ALI ; consommation au wattmètre | Juger sur ce qu'on entend et ce qu'on consomme |

**La règle :** les critères de comparaison sont écrits et datés **avant** la première
mesure comparative, dans un registre (`DECISIONS-PHASE-0.md`). Les protocoles sont
rédigés dans un livret de 23 manipulations (`protocole/PROTOCOLE-EXPERIENCES.html`).

## 4. Où en est le projet — « résultats clés »

**Il n'y a encore AUCUN résultat expérimental.** Rien n'a été mesuré sur l'enceinte. Ne
jamais présenter un nombre comme mesuré. Ce qui existe au 17/11/2026 :

- **Décisions datées** (registre `DECISIONS-PHASE-0.md`) :
  - **Cible du filtre : Butterworth du second ordre**, voie médium inversée (15/11). Motif
    de Thomas : près de moitié moins de cuivre que l'autre option (Linkwitz-Riley), pour
    que le budget reste cohérent et permette de comparer l'actif et les passifs.
  - **Montage : un canal d'ampli par filtre.** Le pré-ampli a deux sorties, l'ampli deux
    canaux. Le seuil des 4 Ω se vérifie donc voie par voie.
  - **Selfs : résistance de fil maximale de 1,5 Ω** (provisoire, en attente d'un devis),
    densité de courant ≤ 3 A/mm² au niveau fort, et deux selfs à prise intermédiaire.
  - Filière PT, TIPE individuel.
- **Préparation :**
  - le livret de 23 manipulations, avec schémas de câblage et consignes de sécurité ;
  - une chaîne de calcul Python complète, testée sur des données **fictives** (171 tests),
    écrite **avec l'aide d'une IA** (Claude), ce que Thomas déclare.
- **Ordres de grandeur issus d'un modèle** (paramètres plausibles d'un 18 pouces de sono,
  pas des mesures) :
  - deux pics d'impédance vers 16 Hz et 86 Hz, et un creux vers 34 Hz ;
  - sur cette charge modélisée, le filtre « catalogue » (18 mH / 150 µF) ferait descendre
    l'impédance vue par l'ampli sous 4 Ω.
  - Ces nombres ne figurent pas dans le script de l'oral, et c'est voulu.
- **Prochaine étape concrète :** commander les résistances de précision et les
  connecteurs, puis étalonner la chaîne de mesure.

## 5. Termes techniques et prononciation

| Terme | Sens en une ligne | Se prononce |
|---|---|---|
| TIPE | travail d'initiative personnelle encadré | « tipe » (un mot, jamais épelé) |
| MCOT | fiche de mise en cohérence des objectifs du TIPE | « èm-cotte » |
| SCEI | service qui organise les concours | « èss-cé-eu-i » |
| impédance, Z(f) | rapport tension / courant d'un dipôle, qui dépend de la fréquence | « zède de èffe » |
| REW | Room EQ Wizard, logiciel de mesure acoustique et d'impédance | « erre, eu, double-vé » |
| GBF | générateur basses fréquences | « gé, bé, èf » |
| ALI | amplificateur linéaire intégré (le script dit le nom en entier) | « a, èl, i » |
| IA | intelligence artificielle | « i, a » |
| bass-reflex | caisse avec évent(s) accordé(s) | « basse-réflexe » |
| évent | tuyau qui ouvre la caisse | « évan » |
| self | bobine (inductance) | « selfe » ; pluriel « selfs », « selfes » |
| L sur r | inductance divisée par la résistance du fil | « èl sur erre » |
| Thiele-Small | modèle électromécanique du haut-parleur | « tile-smôl » |
| Levenberg-Marquardt | méthode d'ajustement aux moindres carrés | « lévène-bergue markarte » |
| Helmholtz | résonateur qui donne la fréquence d'accord des évents | « elm-holtz » |
| Butterworth | réponse de filtre la plus plate possible | « beu-teur-weurss » |
| Linkwitz-Riley | réponse de filtre dont la somme est plate | « link-vitz raïli » |
| Sallen-Key | structure de filtre actif | « sa-lène ki » |
| E12 | série de 12 valeurs normalisées par décade | « E douze » |
| fréquence d'accord, f_b | fréquence où l'évent résonne | « èffe bé » |
| champ proche | micro à environ 2 cm de la source, pour échapper à la pièce | — |
| unités | Hz, kHz, Ω, mH, µF, A/mm² | « hertz », « kilohertz », « ohm », « millihenry », « microfarad », « ampère par millimètre carré » |
| Focusrite Scarlett | marque et modèle de la carte son | « fo-keuss-raïte scarlette » |

## 6. Questions probables et éléments de réponse

Les questions porteront surtout sur la **faisabilité**. Les réponses ci-dessous sont des
éléments, à dire avec ses mots.

- **« Avez-vous tout le matériel ? »**
  - Oui pour l'essentiel. L'enceinte, l'ampli à deux canaux, la carte son, le micro de
    mesure et le wattmètre sont à moi.
  - Le lycée prête le GBF, l'oscilloscope, le multimètre, une résistance de puissance de
    huit ohms et une de dix ohms.
  - Restent à acheter des petites pièces de précision, puis le fil de cuivre et les
    condensateurs du filtre. Budget plafonné à cinq cents euros. (Annexe 1.)
- **« Et si la mesure d'impédance ne marche pas ? »**
  - Elle est étalonnée d'abord sur des composants connus. Si la résistance n'est pas
    retrouvée à trois pour cent près, on cherche l'erreur avant d'aller plus loin.
  - Une deuxième chaîne, indépendante (GBF et oscilloscope), sert de recoupement.
    (Annexe 2.)
- **« Le calendrier est-il tenable ? »**
  - Le point dur est la mesure d'impédance ; tout le reste en dépend, c'est pourquoi elle
    passe en premier.
  - Le calcul est déjà prêt. Le bobinage est prévu en février, avant le semestre des
    concours.
  - Si le temps manque, on sacrifie d'abord le bilan énergétique, qui ne demande qu'une
    mesure.
- **« Pourquoi pas simplement un filtre actif ? »**
  - Il fait partie de l'étude, comme référence : placé avant l'ampli, il ne voit jamais
    l'impédance du haut-parleur.
  - Le sujet, c'est justement ce qui arrive au filtre passif sur la vraie charge. Et la
    comparaison dira lequel est le plus sobre.
- **« Puisque vous utilisez deux canaux d'ampli, à quoi bon un filtre passif ? »**
  - Bonne question, et elle est ouverte. Le passif ne consomme rien en permanence, l'actif
    oui (ses circuits et leur alimentation).
  - Les deux montages utilisent les mêmes deux canaux : la différence se joue entre les
    pertes dans les selfs et la consommation de l'électronique. C'est ce que mesurera le
    wattmètre.
- **« Pourquoi cent hertz ? »**
  - C'est la fréquence de raccord de cette enceinte : le caisson joue en dessous, les
    médiums au-dessus.
- **« Pourquoi bobiner vous-même ? »**
  - Pour une bobine à air : pas de saturation, donc une valeur qui ne change pas avec le
    volume.
  - Pour une valeur libre, et pour connaître tout ce qui la caractérise (nombre de spires,
    longueur et masse de fil, résistance).
  - Ce n'est pas pour économiser : une self à noyau du commerce coûte moins cher.
- **« Comment mesurer le son à cent hertz dans une pièce ? »**
  - La longueur d'onde fait trois mètres quarante, donc la pièce domine.
  - On mesure en champ proche : le micro à deux centimètres de la membrane, puis de chaque
    évent, et on somme les trois relevés.
- **« Comment saurez-vous que votre filtre est meilleur ? »**
  - Avec huit critères écrits et datés avant les mesures. Le principal est l'écart de la
    somme des deux voies à la cible. (Annexe 3.)
  - Si le filtre optimisé ne fait pas mieux, ce sera dit : c'est un résultat.
- **« Pourquoi un modèle à huit paramètres ? »**
  - Cinq décrivent le haut-parleur, trois la caisse bass-reflex.
  - Un modèle à cinq paramètres, ajusté sur une courbe à deux pics, convergerait sans
    prévenir vers des valeurs fausses.
- **« Pourquoi Butterworth ? »**
  - Près de moitié moins de cuivre que l'autre option, pour garder un budget qui permette
    la comparaison avec l'actif.
  - Avec ce filtre, il faut inverser la polarité d'une des deux voies.
- **« Le haut-parleur risque-t-il quelque chose ? »**
  - Pendant la mesure d'impédance, le courant ne fait que quelques milliampères.
  - À fort niveau, on ne descend jamais sous la fréquence d'accord, où la membrane n'est
    plus retenue par l'air des évents.
- **« Qu'est-ce qui est de vous dans ce travail ? »**
  - De moi : l'enceinte, les mesures, les montages, les décisions datées, le bobinage.
  - Fait avec l'aide d'une IA (Claude) : le code d'analyse et la rédaction des documents.
  - Le noyau du calcul (modèle, moindres carrés, énumération des valeurs), je le
    réécrirai seul.
  - Ne jamais dire « j'ai écrit le code ».
- **« Le sujet est-il original ? »**
  - Le thème est connu, mais l'étude porte sur cette enceinte-là, mesurée, avec des
    critères fixés avant les mesures et une optimisation sous de vraies contraintes de
    coût et de pertes.

## 7. À ne pas dire

- « J'ai mesuré… » : rien n'est mesuré à ce jour.
- « J'ai écrit le code » : il a été écrit avec l'aide d'une IA (voir ci-dessus).
- Une incertitude chiffrée sur la fréquence de coupure : les chiffres qui circulent dans
  le dépôt sont en cours de correction.
- Des nombres de la présentation finale (`presentation-finale.html`) : ils viennent de
  données synthétiques.
