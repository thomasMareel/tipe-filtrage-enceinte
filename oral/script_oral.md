# Script de l'oral — présentation du projet, mercredi 18 novembre 2026

> Le texte que Thomas dit, vue par vue. Support : `oral/presentation.pdf` (style clair, celle qui est projetée). Même contenu dans `oral/script_oral.json`, pour un programme. Contexte : `oral/CONTEXTE.md`. Vidéo d'entraînement : `oral/CONSIGNES_VIDEO.md`.

- **Durée visée : 8:15** pour les 12 vues présentées (fourchette acceptée : 7 min 30 à 8 min 30), à 150 mots par minute, une seconde de respiration comprise à chaque changement de vue. Le texte compte 1212 mots.
- **Les 15 pages du PDF** : vues 1 à 12 présentées, puis 3 annexes (pages 13 à 15) qui ne se présentent pas ; elles servent pendant les questions sur la faisabilité.
- **Apparitions successives : aucune.** Chaque vue s'affiche en entier ; on passe à la suivante après la phrase de transition.
- **Aucun chiffre de ce support n'est une mesure** : rien n'a encore été mesuré sur l'enceinte. La seule courbe (vue 2) est une allure calculée sur un modèle, et le texte le dit.
- Le texte est écrit pour être **dit**, pas lu : les nombres sont écrits comme ils se prononcent. Les sigles et leur prononciation sont dans `oral/CONTEXTE.md`.

## Vue 1 — Optimiser le filtre de mon enceinte sur son impédance réelle

- **Temps visé :** 20 s (de 0:00 à 0:20)
- **À montrer :** la photo de l'enceinte ; le titre : « impédance réelle ».
- **Apparitions successives :** aucune.

Bonjour. Voici l'enceinte que j'ai construite. Mon TIPE consiste à calculer son filtre de raccord, à cent hertz, pour le vrai haut-parleur, et pas pour un haut-parleur idéal. Et je vais surtout vous parler des expériences, parce que c'est là que tout se joue. Commençons par le problème.

*Transition vers la vue 2 (dernière phrase ci-dessus) :* « Commençons par le problème. »

## Vue 2 — Le haut-parleur n'est pas une résistance de 8 Ω

- **Temps visé :** 50 s (de 0:20 à 1:10)
- **À montrer :** la ligne pointillée orange : l'hypothèse des huit ohms ; la courbe bleue : le premier pic, le creux, puis le deuxième pic ; la bande « zone de raccord » autour de cent hertz ; la légende du bas : allure attendue, ce n'est pas une mesure.
- **Apparitions successives :** aucune.

Mon enceinte a deux voies : un caisson de basses de dix-huit pouces, et des médiums. Entre les deux, un filtre partage le signal autour de cent hertz. Le calcul classique suppose que le haut-parleur se comporte comme une résistance de huit ohms : c'est cette ligne pointillée orange. Or un haut-parleur dans sa caisse, ce n'est pas ça. Voici l'allure que j'attends pour mon caisson, un bass-reflex à deux évents : deux pics, un creux, et le deuxième pic tombe en pleine zone de raccord. Attention : cette courbe vient d'un modèle, je ne l'ai pas encore mesurée. Mais si elle a cette allure, un filtre calculé pour huit ohms ne fera pas ce qu'on attend de lui. D'où ma question.

*Transition vers la vue 3 (dernière phrase ci-dessus) :* « D'où ma question. »

## Vue 3 — Ma problématique, et la démarche en quatre étapes

- **Temps visé :** 39 s (de 1:10 à 1:49)
- **À montrer :** l'encadré de la problématique ; les quatre cases, de gauche à droite ; les deux cases vertes marquées « expérience ».
- **Apparitions successives :** aucune.

Ma problématique : comment concevoir ce filtre pour qu'il tienne sa cible sur la charge réelle, au moindre coût en composants, en pertes et en cuivre ? Pour y répondre, quatre étapes. Un : je mesure l'impédance réelle. Deux : j'en tire un modèle physique du haut-parleur ; c'est un problème inverse. Trois : je cherche les meilleures valeurs de composants, sous contraintes. Quatre : je fabrique, et je valide. La première et la dernière étape sont des expériences : la première fournit les données, la dernière dit si le calcul avait raison. Voyons ces expériences.

*Transition vers la vue 4 (dernière phrase ci-dessus) :* « Voyons ces expériences. »

## Vue 4 — Quatre expériences

- **Temps visé :** 31 s (de 1:49 à 2:20)
- **À montrer :** les quatre cartes, une par une (la règle et le livret se disent sans support écrit).
- **Apparitions successives :** aucune.

Il y en a quatre. Mesurer l'impédance. Bobiner les inductances et les caractériser. Tester les filtres au banc électrique. Et mesurer le son au micro, avec la consommation au wattmètre. Les protocoles sont déjà rédigés, dans un livret de vingt-trois manipulations. Et une règle vaut pour toutes : les critères de comparaison sont écrits et datés avant la première mesure, pour que je ne puisse pas les ajuster après coup. Je commence par la plus importante.

*Transition vers la vue 5 (dernière phrase ci-dessus) :* « Je commence par la plus importante. »

## Vue 5 — Mesurer l'impédance Z(f) du haut-parleur

- **Temps visé :** 59 s (de 2:20 à 3:19)
- **À montrer :** suivre du doigt le chemin du courant : sortie, résistance, haut-parleur, retour à la masse ; les deux voltmètres, en A puis en B ; la formule : d'abord le courant, puis l'impédance.
- **Apparitions successives :** aucune.

Première expérience, la clé de voûte : mesurer l'impédance du haut-parleur en fonction de la fréquence. Le signal part de la carte son, traverse une résistance connue de cent ohms, puis le haut-parleur, et revient à la masse. Les deux entrées de la carte son servent de voltmètres : l'une mesure la tension en A, avant la résistance, l'autre en B, aux bornes du haut-parleur. Pourquoi cette résistance ? Parce que la carte son ne mesure que des tensions, pas des courants. Le même courant traverse la résistance et le haut-parleur : la tension aux bornes de la résistance, divisée par cent ohms, me donne ce courant. Et l'impédance, c'est la tension du haut-parleur divisée par ce courant. Le logiciel REW fait ce calcul à chaque fréquence, de dix hertz à un kilohertz, en module et en phase. Encore faut-il pouvoir faire confiance à l'appareil.

*Transition vers la vue 6 (dernière phrase ci-dessus) :* « Encore faut-il pouvoir faire confiance à l'appareil. »

## Vue 6 — D'abord, tester l'appareil sur du connu

- **Temps visé :** 59 s (de 3:19 à 4:18)
- **À montrer :** la phrase du haut : sur le haut-parleur, on ne connaît pas la bonne réponse ; la droite horizontale de la résistance de dix ohms ; la droite du condensateur et ses trois valeurs ; les deux chaînes de mesure, à droite ; l'encadré orange : la porte ; l'encadré du bas : ensuite seulement, le haut-parleur.
- **Apparitions successives :** aucune.

Avant de brancher le haut-parleur, il y a un piège : sur lui, je ne connais pas la bonne réponse. Si l'appareil se trompe, je ne le verrai pas. Alors je fais comme avec une balance qu'on vérifie avec un poids connu. Une résistance de dix ohms doit donner une droite horizontale, à dix ohms, à toutes les fréquences. Un condensateur doit donner une impédance divisée par dix quand la fréquence est multipliée par dix. Puis une deuxième chaîne, indépendante, le GBF et l'oscilloscope du lycée, doit donner la même courbe. C'est une porte : si la résistance n'est pas retrouvée à trois pour cent près, je cherche l'erreur avant d'aller plus loin. Ensuite seulement, je mesure le caisson et les médiums, et je compare la courbe à ma prédiction de l'accord des évents, faite d'après leurs dimensions. Une fois la courbe mesurée, place au calcul.

*Transition vers la vue 7 (dernière phrase ci-dessus) :* « Une fois la courbe mesurée, place au calcul. »

## Vue 7 — De la courbe mesurée au meilleur filtre

- **Temps visé :** 43 s (de 4:18 à 5:01)
- **À montrer :** à gauche, la boucle du problème inverse ; à droite, l'entonnoir de l'optimisation ; l'encadré « Contrôle », sans le lire : il sert si une question vient sur la validation du code ; la ligne du bas sur l'aide de l'IA : la dire en regardant les professeurs.
- **Apparitions successives :** aucune.

Le calcul, je le résume. À gauche, le problème inverse : j'ajuste un modèle physique du haut-parleur, à huit paramètres, jusqu'à ce que sa courbe colle à la mesure ; c'est la méthode des moindres carrés. À droite, l'optimisation : les composants n'existent qu'en valeurs normalisées, donc je peux tester toutes les combinaisons, plus de trois cent mille, et garder la meilleure. Avec une contrainte : l'ampli ne doit jamais voir moins de quatre ohms. Ce code est déjà écrit et testé, avec l'aide d'une IA, je le dis clairement ; j'en réécrirai moi-même le cœur. Mais un filtre, il faut aussi le fabriquer.

*Transition vers la vue 8 (dernière phrase ci-dessus) :* « Mais un filtre, il faut aussi le fabriquer. »

## Vue 8 — Bobiner les selfs, et mesurer ce qu'elles coûtent

- **Temps visé :** 47 s (de 5:01 à 5:48)
- **À montrer :** la bobine en coupe ; la prise intermédiaire, en orange ; la formule de la masse de cuivre, dans la liste à droite.
- **Apparitions successives :** aucune.

Deuxième expérience : les inductances, qu'on appelle aussi des selfs. Je les bobine moi-même, à air, sans noyau : un noyau peut saturer, et la valeur changerait avec le volume. Le problème, c'est la résistance du fil, qui gaspille de la puissance. Moins de résistance, c'est un fil plus gros, donc beaucoup plus de cuivre : la masse croît comme le rapport L sur r, à la puissance trois demis. C'est là qu'est l'enjeu de sobriété. Je mesure chaque bobine : son inductance, la résistance de son fil, et son échauffement à fort niveau. Et grâce à cette prise intermédiaire, une même bobine sert au filtre du catalogue et au filtre optimisé. Ensuite, je les branche.

*Transition vers la vue 9 (dernière phrase ci-dessus) :* « Ensuite, je les branche. »

## Vue 9 — Les filtres branchés sur les vrais haut-parleurs

- **Temps visé :** 44 s (de 5:48 à 6:32)
- **À montrer :** le pré-ampli et ses deux sorties ; les deux canaux de l'ampli, chacun vers son filtre ; les deux points de mesure en pointillé (la sécurité se dit sans support écrit).
- **Apparitions successives :** aucune.

Troisième expérience : le banc électrique. Le pré-ampli a deux sorties, et l'ampli deux canaux : un canal pour le caisson, un pour les médiums, chacun avec son filtre. Je branche le filtre du catalogue, puis le filtre optimisé, sur les vrais haut-parleurs. Je relève la réponse de chaque voie, la fréquence où elles se croisent, l'impédance que voit l'ampli, et les pertes dans les bobines. C'est là que le calcul est confronté au réel. Et comme ce banc travaille derrière l'ampli, à des tensions élevées, son protocole sera relu par mon professeur avant la première mise sous tension. Reste le plus important : ce qu'on entend.

*Transition vers la vue 10 (dernière phrase ci-dessus) :* « Reste le plus important : ce qu'on entend. »

## Vue 10 — Le micro en champ proche, et le wattmètre

- **Temps visé :** 55 s (de 6:32 à 7:27)
- **À montrer :** le micro devant la membrane, puis devant chaque évent ; les deux courbes de polarité : la bonne en vert, le trou en orange ; les trois étiquettes du bas : catalogue, optimisé, actif.
- **Apparitions successives :** aucune.

Quatrième expérience. À cent hertz, la longueur d'onde fait trois mètres quarante : dans une pièce, les réflexions dominent tout. Je mesure donc en champ proche : le micro à deux centimètres de la membrane, puis de chaque évent, et je fais la somme des trois. Je vérifie aussi la polarité : avec ce filtre, il faut inverser l'une des deux voies, sinon la somme fait un trou au raccord. Je compare trois solutions : le filtre du catalogue, le filtre optimisé, et un filtre actif à amplificateurs linéaires intégrés, placé avant l'ampli, qui ne voit jamais l'impédance du haut-parleur : c'est ma référence. Chaque mesure est faite à deux niveaux d'écoute fixés à l'avance, et le wattmètre mesure ce que consomme chaque solution. Pour que tout cela reste honnête et sûr, j'ai prévu des garde-fous.

*Transition vers la vue 11 (dernière phrase ci-dessus) :* « Pour que tout cela reste honnête et sûr, j'ai prévu des garde-fous. »

## Vue 11 — Garde-fous et calendrier

- **Temps visé :** 41 s (de 7:27 à 8:08)
- **À montrer :** les trois cartes : décider avant, une porte par étape, sécurité ; la frise, de gauche à droite ; les losanges orange des étapes du concours.
- **Apparitions successives :** aucune.

Trois garde-fous. Un : je décide avant de mesurer ; les critères, les niveaux d'écoute et la cible sont datés dans un registre. Deux : chaque étape a sa porte de validation. Trois : la sécurité ; on ne descend jamais sous la fréquence d'accord à fort niveau, parce que la membrane n'y est plus retenue par l'air des évents. Côté calendrier : la commande et l'étalonnage maintenant, la mesure d'impédance en décembre, le calcul et la fiche MCOT en janvier, le bobinage en février, le banc et le micro en mars, puis l'analyse jusqu'au dépôt de juin. Voilà mon projet.

*Transition vers la vue 12 (dernière phrase ci-dessus) :* « Voilà mon projet. »

## Vue 12 — Questions ?

- **Temps visé :** 7 s (de 8:08 à 8:15)
- **À montrer :** laisser la vue affichée pendant les questions ; aller aux annexes si on parle de matériel, de risques ou de critères.
- **Apparitions successives :** aucune.

Merci de votre attention. Je suis prêt pour vos questions, en particulier sur la faisabilité.

## Page 13 — Annexe 1 — Le matériel : l'essentiel est déjà là (hors chrono, pas présentée)

*Si la question vient :* « Avez-vous le matériel ? » Oui pour l'essentiel : l'enceinte, l'ampli à deux canaux, la carte son et le micro sont à moi ; le lycée prête le GBF, l'oscilloscope, le multimètre, une résistance de puissance de huit ohms et une de dix ohms. Il ne reste à acheter que des petites pièces de précision, puis le fil de cuivre et les condensateurs du filtre ; budget plafonné à cinq cents euros.

## Page 14 — Annexe 2 — Ce qui peut mal tourner, et la parade (hors chrono, pas présentée)

*Si la question vient :* « Et si la mesure ne marche pas ? » C'est pour ça que j'étalonne d'abord sur des composants connus, avec une deuxième chaîne de mesure pour recouper. Le champ proche contourne la pièce. Et si le filtre optimisé ne fait pas mieux que le catalogue, mes critères sont fixés avant : je le dirai, c'est un résultat.

## Page 15 — Annexe 3 — Les critères de comparaison (proposition à geler) (hors chrono, pas présentée)

*Si la question vient :* « Comment saurez-vous si c'est mieux ? » Avec ces huit critères, écrits et datés avant la première mesure comparative ; le principal est la fidélité du raccord, l'écart de la somme des deux voies à la cible visée.
