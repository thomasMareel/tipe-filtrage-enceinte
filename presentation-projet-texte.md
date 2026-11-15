# Texte de l'oral — présentation du projet (18/11/2026)

Support : `presentation-projet.pdf` (sombre) ou `presentation-projet-clair.pdf` (clair, pour une salle éclairée).
Durée visée : **8 min** pour les vues 1 à 12, à environ 150 mots par minute. Les annexes A1 à A3 ne se
présentent pas : elles servent pendant les questions sur la faisabilité.

Aucun chiffre de ce support n'est une mesure : la seule courbe (vue 2) est une **allure attendue**, calculée sur un modèle.

## Vue 1 — Optimiser le filtre de mon enceinte sur son impédance réelle · 15 s

Bonjour. Mon TIPE part de l'enceinte que j'ai construite : comment calculer son filtre de raccord à cent hertz, non pas pour un haut-parleur idéal, mais pour le vrai. Je vais surtout vous parler des expériences, parce que c'est là que tout se joue.

## Vue 2 — Le haut-parleur n'est pas une résistance de 8 Ω · 50 s

Mon enceinte a deux voies : un caisson de basses de dix-huit pouces, et des médiums. Entre les deux, un filtre partage le signal autour de cent hertz. Le calcul classique, celui des catalogues, suppose que le haut-parleur est une résistance de huit ohms : c'est la ligne pointillée. Or un haut-parleur dans sa caisse, ce n'est pas ça. Voici l'allure que j'attends pour mon caisson, qui est un bass-reflex à deux évents : deux pics et un creux, et le second pic tombe en pleine zone de raccord. Attention : cette courbe vient d'un modèle, je ne l'ai pas encore mesurée — c'est justement l'objet de ma première expérience. Mais si elle a cette allure, un filtre calculé pour huit ohms ne fera pas ce qu'on lui demande.

## Vue 3 — Ma problématique, et la démarche en quatre étapes · 40 s

D'où ma question : comment concevoir ce filtre pour qu'il tienne sa cible sur la charge réelle, au moindre coût en composants, en pertes et en cuivre ? Ma démarche a quatre étapes. Je mesure l'impédance réelle. J'en tire un modèle physique du haut-parleur : c'est un problème inverse. Je cherche ensuite les meilleures valeurs de composants, sous contraintes. Enfin je fabrique et je valide. Les expériences encadrent tout : la première fournit les données, les dernières disent si le calcul avait raison.

## Vue 4 — Quatre expériences, une règle · 30 s

Concrètement, il y a quatre expériences : mesurer l'impédance ; bobiner et caractériser les inductances ; tester les filtres au banc électrique ; et mesurer le son au micro, avec la consommation au wattmètre. Elles sont déjà rédigées dans un livret de vingt-trois manipulations, avec les câblages et les consignes de sécurité. Et une règle vaut pour toutes : les critères de comparaison sont écrits et datés avant la première mesure, pour que je ne puisse pas les ajuster après coup.

## Vue 5 — Mesurer l'impédance Z(f) du haut-parleur · 60 s

La première expérience est la clé de voûte : mesurer l'impédance Z en fonction de la fréquence. Le principe : j'envoie un sinus avec ma carte son à travers une résistance connue de cent ohms, en série avec le haut-parleur. Je mesure deux tensions : avant la résistance, et aux bornes du haut-parleur. Leur différence me donne le courant, et le rapport me donne l'impédance, en module et en phase, à chaque fréquence. Le logiciel REW balaie de dix hertz à un kilohertz. Je mesure le caisson dans sa caisse, et le bloc des médiums tel qu'il est câblé, avec les pavillons d'aigu, parce que c'est ce que le filtre voit vraiment. Et avant de mesurer, je fais une prédiction : à partir des dimensions des évents et du volume de la caisse, je calcule la fréquence d'accord. La mesure dira si j'avais raison.

## Vue 6 — Étalonner : la chaîne doit retrouver des valeurs connues · 50 s

Mais une mesure ne vaut que si l'appareil sait retrouver une valeur connue. Donc avant de brancher le haut-parleur, je mesure une résistance connue — je dois trouver une droite horizontale à la bonne valeur — et un condensateur, dont l'impédance doit décroître comme un sur la fréquence. Je recoupe ensuite avec une deuxième chaîne, indépendante : le GBF et l'oscilloscope du lycée. Enfin, la carte son n'est garantie qu'au-dessus de vingt hertz, alors que le premier pic peut tomber en dessous : je vérifie donc sa réponse jusqu'à dix hertz. C'est une porte : si la résistance n'est pas retrouvée à trois pour cent près, je cherche l'erreur avant d'aller plus loin.

## Vue 7 — De la courbe mesurée au meilleur filtre · 45 s

Entre les expériences, il y a le calcul, que je résume. D'abord le problème inverse : j'ajuste un modèle physique du haut-parleur, à huit paramètres pour un bass-reflex, jusqu'à ce que sa courbe colle à la mesure, par moindres carrés. Ensuite l'optimisation : les composants n'existent qu'en valeurs normalisées, donc je peux tester toutes les combinaisons, plus de trois cent mille, et garder la meilleure, avec une contrainte : l'ampli ne doit jamais voir moins de quatre ohms. Ce code est déjà écrit et testé sur des données fictives, avec l'aide d'une IA, je le dis clairement ; j'en réécrirai moi-même le cœur.

## Vue 8 — Bobiner les selfs, et mesurer ce qu'elles coûtent · 45 s

Deuxième expérience : les inductances. Je les bobine moi-même, à air, sans noyau : un noyau sature, et la valeur changerait avec le volume. Mais le fil a une résistance, qui gaspille de la puissance. Moins de résistance, c'est un fil plus gros, donc beaucoup plus de cuivre : la masse croît comme la puissance trois demis du rapport L sur r. C'est le cœur de l'aspect sobriété. Je mesurerai chaque bobine : son inductance par résonance avec un condensateur connu, la résistance de son fil en quatre fils, et son échauffement au niveau fort. Et grâce à une prise intermédiaire, une même bobine servira au filtre du catalogue et au filtre optimisé.

## Vue 9 — Les filtres branchés sur les vrais haut-parleurs · 45 s

Troisième expérience : le banc électrique. Le pré-ampli a deux sorties et l'ampli deux canaux : un pour le caisson, un pour les médiums, chacun avec son filtre. Je branche le filtre du catalogue, puis le filtre optimisé, sur les vrais haut-parleurs, dans le même montage. Je relève la réponse de chaque voie, la fréquence où elles se croisent, l'impédance que voit l'ampli, et les pertes dans les bobines. C'est ici que la prédiction du calcul est confrontée au réel. Ce banc travaille derrière l'ampli, à des tensions élevées : son protocole sera relu par mon professeur avant la première mise sous tension.

## Vue 10 — Le micro en champ proche, et le wattmètre · 60 s

Quatrième expérience : ce qu'on entend vraiment. À cent hertz, la longueur d'onde fait trois mètres quarante : dans une pièce, les réflexions dominent tout. Je mesure donc en champ proche, le micro à deux centimètres de la membrane, puis de chaque évent, et je somme les trois relevés. Je vérifie aussi la polarité : avec ce type de filtre, il faut inverser une des voies, sinon la somme fait un trou au raccord — c'est un test très lisible. Je compare trois solutions : le filtre du catalogue, le filtre optimisé, et un filtre actif à amplificateurs linéaires intégrés, placé avant l'ampli, qui ne voit jamais l'impédance du haut-parleur : c'est ma référence. Chaque mesure est faite à deux niveaux d'écoute fixés à l'avance, et un wattmètre mesure la consommation de chaque solution.

## Vue 11 — Garde-fous et calendrier · 40 s

Pour que tout cela reste honnête et sûr, trois garde-fous. Je décide avant de mesurer : critères, niveaux et cible sont datés dans un registre. Chaque étape a sa porte de validation. Et la sécurité : on ne descend jamais sous la fréquence d'accord à fort niveau, parce que la membrane du dix-huit pouces n'y est plus retenue par l'air des évents. Côté calendrier : commande et étalonnage maintenant, mesure d'impédance en décembre, calcul et MCOT en janvier, bobinage en février, banc et micro en mars, puis l'analyse jusqu'au dépôt de juin.

## Vue 12 — Questions ? · 5 s

Merci. Je suis prêt pour vos questions, en particulier sur la faisabilité.

## Vue A1 — Le matériel : l'essentiel est déjà là · Annexe

Si on me demande si j'ai le matériel : oui pour l'essentiel. La chaîne de mesure d'impédance repose sur ma carte son, recoupée par le GBF et l'oscilloscope du lycée. Les achats immédiats sont des petites pièces de précision. Le gros poste, c'est le cuivre des selfs, et je l'ai borné par un choix de résistance de fil, pas par un chiffre au hasard.

## Vue A2 — Ce qui peut mal tourner, et la parade · Annexe

Le point dur, c'est la mesure d'impédance, et c'est pour ça que je l'étalonne d'abord sur des composants connus : réussir cette étape lève l'essentiel du risque. Pour l'acoustique, le champ proche contourne la pièce. Et si le filtre optimisé ne fait pas mieux, mes critères sont fixés avant : je le dirai, c'est un résultat.

## Vue A3 — Les critères de comparaison (proposition à geler) · Annexe

Ces huit critères sont une proposition : je les gèlerai et les daterai avant la première mesure comparative, et je n'en ajouterai ni n'en retirerai ensuite. C'est ce qui rend la conclusion recevable, même si elle est défavorable au filtre que j'ai optimisé.
