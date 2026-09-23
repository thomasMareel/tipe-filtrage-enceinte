# PARCOURS — TIPE « filtrage d'enceinte », session 2027

*Thomas Mareel — document établi le 16 septembre 2026.*

---

## À quoi sert ce document

C'est **la liste ordonnée de tes actions, de A à Z**, depuis aujourd'hui jusqu'au
matin de l'oral. Pas les phases du projet, pas la méthode, pas la physique :
**les gestes**. Chaque entrée commence par un verbe à l'infinitif, décrit quelque
chose que tu peux faire puis cocher, et porte trois informations :

- une **durée estimée** — ce sont des **estimations**, pas des mesures ;
- ce qu'elle **débloque** ou ce qui la **bloque** ;
- un critère **« fini quand… »** vérifiable, pour que « c'est presque fait » ne
  soit jamais une réponse.

Le *quoi* et le *pourquoi* scientifiques ne sont pas ici : ils vivent dans
`FEUILLE-DE-ROUTE.md` (les phases), `REFERENCE-TECHNIQUE.md` (les modèles, les
protocoles, les budgets d'incertitude) et `DECISIONS-PHASE-0.md` (le registre des
dix décisions à geler). Ce document-ci ne les répète pas : il y renvoie.

## Comment s'en servir

**Le dérouler de haut en bas, et cocher** — avec **une exception, écrite ici parce
qu'elle est structurelle**. La partie RÈGLES TRANSVERSES (`T-A` à `T-E`) est placée
à la fin pour ne pas hacher le fil des périodes, mais **quinze de ses actions sont
des prérequis de la période 1** : toute la sécurité (`T-A1` à `T-A10`), l'ouverture
du cahier au gabarit (`T-B1`, `T-B2`) et trois rappels à poser aujourd'hui (`T-D1`,
`T-D5`, `T-D11`). C'est exactement l'objet de **`1-A0`, la première action du
document** : elle t'y envoie avant la première séance de banc. À part ces
quinze-là, l'ordre est bien celui des dépendances, puis des dates. Et **chaque action
transverse qui en débloque une autre porte désormais son code** (« débloque
`1-D2` », pas « la première séance de paillasse »). Les actions marquées
**(Claude)** sont faites par l'assistant — ta part s'y réduit à fournir la donnée
ou la décision qui les précède, et c'est justement pour ça que ton temps rare doit
aller à la paillasse et aux décisions, pas au traitement.

**Reviens voir Claude aux points indiqués** : après chaque campagne de mesure (avec
le CSV brut et les pages du cahier), après chaque décision gelée (pour la propager
dans tout le dépôt), et tout de suite quand une manip échoue — pas une fois
réparée. La règle d'entrée est dans la section T-E : *on ne vient pas « pour
avancer », on vient avec un livrable.*

**Les durées sont du temps de travail effectif.** Ni les colles, ni les DS, ni les
concours blancs, ni les vacances ne sont dans ce calendrier. Une action « 3 h » se
case en pratique sur deux samedis, et une action « 2 h » peut occuper deux semaines
de calendrier. Compte 4 à 6 heures de TIPE par semaine en moyenne sur l'année de
2ᵉ année, avec des semaines à zéro.

**Les codes d'action, et ils s'écrivent tous pareil.** Chaque action porte un code
du type `2-F3` : avant le tiret, la période (1, 2, 3, ou `T` pour les règles
transverses) ; après, la lettre du bloc puis le rang dans le bloc. Donc `1-A4`,
`3-E12`, `T-A9`, `T-D11` — **jamais de point**, jamais `T1.9`. Ces codes servent à
s'y retrouver et à se citer entre eux ; ils n'ont pas d'autre sens. **À ne pas
confondre avec les décisions du registre**, qui s'écrivent toujours sans préfixe
— `D1` à `D10`, plus les deux entrées que ce parcours propose de créer (`1-C8` et
`2-F6`) — et qui vivent dans `DECISIONS-PHASE-0.md`.

**Quelques décisions reviennent deux ou trois fois, et c'est voulu — mais une
seule fois comme décision.** Le professeur encadrant (`1-A2`/`1-A3`, rappelé en
`2-A3` et `3-A5`), D2 (`2-F1`, rappelée en `3-A1`), D6 (`2-F2`, rappelée en
`3-A2`), D9 et le mode seul/groupe (`1-C5`, rappelés en `2-J6`/`2-J7` puis
`3-A4`/`3-A6`) apparaissent **une** fois comme « à geler », **au plus tôt**, puis
une ou deux fois comme « dernier rappel ».
**Reconnaître un rappel est immédiat : il porte une durée de 2 minutes et aucune
durée de décision.** On y vérifie qu'une date figure au registre ; si oui, on
coche et on passe ; si non, **on ne décide pas là** — on rouvre l'action d'origine,
dont le code est cité. C'est aussi pour cela que le temps d'une décision n'est
compté qu'une fois dans les totaux de période.

**Ce qui porte `[[à vérifier]]`.** Les dates SCEI 2027 données ici sont
extrapolées des sessions précédentes (les clôtures sont stables depuis des
années ; ce sont les ouvertures qui bougent). Elles se confirment à la parution
des *Attendus 2026-2027* sur `scei-concours.fr/tipe.html` — c'est l'action `T-D2`.

## <a id="sommaire"></a>Sommaire

| Période | Blocs |
|---|---|
| Repères | [Tableau de bord](#bord) · [Vue mois par mois](#mois) · [Où j'en suis](#ouj) · [Les trois actions du moment](#maintenant) |
| [**Période 1** — sept. → fin oct. 2026](#p1) | [1-A Journal, encadrant, cotes](#1a) · [1-B Inventaire et achats](#1b) · [1-C Gel des décisions](#1c) · [1-D Étalonnages](#1d) · [1-E Campagne $Z(f)$](#1e) · [Risques](#p1-risques) · [Récapitulatif](#p1-recap) |
| [**Période 2** — nov. → déc. 2026](#p2) | [2-A Contrôle d'entrée](#2a) · [2-B Sources](#2b) · [2-C Ajustement bass-reflex](#2c) · [2-D $f_b$ par trois voies](#2d) · [2-E Incertitudes](#2e) · [2-F Gel de la fonction de coût](#2f) · [2-G Optimisation](#2g) · [2-H La self](#2h) · [2-I Achats](#2i) · [2-J MCOT](#2j) · [2-K Porte de sortie](#2k) · [Risques](#p2-risques) |
| [**Période 3** — janv. → juin 2027](#p3) | [3-A Solder la saisie](#3a) · [3-B Étape 1 SCEI](#3b) · [3-C Selfs](#3c) · [3-D Montages](#3d) · [3-E Campagnes de mesure](#3e) · [3-F Analyse](#3f) · [3-G Figures et PDF](#3g) · [3-H Étape 2 SCEI](#3h) · [3-I Étape 3 SCEI](#3i) · [3-J Répétitions](#3j) · [Risques](#3k) |
| [**Règles transverses**](#T) | [T-A Sécurité](#ta) · [T-B Journal de bord](#tb) · [T-C Critères gelés](#tc) · [T-D Risques et parades](#td) · [T-E Travailler avec Claude](#te) |
| Fin | [Si tu ne devais retenir que cinq choses](#cinq) |

## <a id="mois"></a>Vue mois par mois

Une page pour savoir, un soir de janvier, ce qui est à faire ce mois-ci. Les
heures sont des **estimations de temps de travail effectif** (ni colles, ni DS, ni
vacances), et elles supposent l'ordre du document respecté.

| Mois | Codes d'action | Heures estimées | Le verrou du mois |
|---|---|---|---|
| **sept. 2026** | `1-A0` à `1-A8`, `1-B1` à `1-B5`, `T-A1` à `T-A10`, `T-B1` à `T-B3`, `T-B8`, `T-C1`, `T-D1`, `T-D5`, `T-D6`, `T-D11`, `T-E1` | 13 à 16 h | l'accord de l'encadrant (`1-A2`, **levé le 16/09/2026** ; reste `1-A3`) |
| **oct. 2026** | `1-C1` à `1-C9`, `1-D1` à `1-D8`, `1-E1` à `1-E8` | 27 à 36 h (selon l'export, `1-B2` ; dont 3 h pour le jig carte son, `1-D8`) | la porte d'étalonnage (`1-D2`/`1-D4`) |
| **nov. 2026** | `2-A1` à `2-A3`, `2-B1` à `2-B7`, `2-C1` à `2-C7`, `2-D1` à `2-D4`, `2-E1` à `2-E4`, `2-F1` à `2-F6` | 17 à 22 h | le gel de D2, D5, D6 avant l'optimisation |
| **déc. 2026** | `2-G1` à `2-G8`, `2-H1` à `2-H3`, `2-I1` à `2-I3`, `2-J1` à `2-J10`, `2-K1` à `2-K6` | 15 à 19 h | la commande avant le 15 décembre (`2-I3`) |
| **janv. 2027** | `3-A1` à `3-A7`, `3-B1` à `3-B4`, `3-C1` à `3-C5` | 10 à 14 h | la saisie de l'étape 1 (`3-B3`) |
| **févr. 2027** | `3-C6` à `3-C8`, `3-D1` à `3-D4`, `3-E1` à `3-E4` | 20 à 26 h | toutes les selfs bobinées avant les vacances |
| **mars 2027** | `3-E5` à `3-E15` | 15 à 19 h | les campagnes acoustiques avant les concours blancs |
| **avril 2027** | `3-F1` à `3-F4`, `3-G1` à `3-G3` | 9 à 12 h | la conclusion écrite, y compris défavorable |
| **mai 2027** | `3-G4` à `3-G7`, `3-H1` à `3-H3`, `3-J1` à `3-J5` | 14 à 18 h | un PDF téléversé même imparfait (`3-H2`) |
| **juin 2027** | `3-I1`, `3-I2`, `3-J6`, `3-J7` | 2 à 3 h | la validation de l'encadrant, 8 jours (`3-I1`/`3-I2`) |

**Ce que ce tableau montre et que les listes cachent** : de janvier à mai, la
charge double par rapport à novembre-décembre, et elle tombe sur le semestre des
concours. C'est le vrai point de rupture du calendrier.

## <a id="ouj"></a>Où j'en suis

> **Dernière revue : 23/09/2026.** Bloc en cours : `1-A` et `1-B`. Prochaine
> échéance ferme : la porte d'étalonnage, mi-octobre 2026 (l'accord de
> l'encadrant est acquis depuis le 16/09/2026 : M. Chevalier, `1-A2` ; reste
> `1-A3`).
>
> *Cette ligne se réécrit à chaque revue mensuelle (`T-D10`) — trois informations,
> pas plus : la date de la revue, le bloc en cours, la prochaine échéance ferme.*

## Où en est le projet au 23 septembre 2026

1. **Tout l'outillage existe déjà** : la documentation complète (feuille de route,
   référence technique, registre de décisions, notes de jury, brouillon de MCOT),
   les deux présentations au gabarit 4/3 imposé par le SCEI avec leurs PDF sous le
   plafond de 5 Mo (régénérés le 23/09/2026 : 1,80 Mo pour la finale), le livret
   de manipulations `protocole/PROTOCOLE-EXPERIENCES.html` et son **PDF A4 à
   imprimer** (relus le 23/09/2026, câblage arbitré du jig), et le dossier
   `analyse/` — **19 319 lignes de Python au 23/09/2026** (15 066 de modules +
   4 253 de tests ; commande de contrôle :
   `wc -l analyse/*.py analyse/tests/*.py`), 171 tests
   au vert, pipeline `tout_refaire.py` exécutable, qui sait déjà lire des mesures,
   ajuster Thiele-Small en caisse close **et** bass-reflex, énumérer les valeurs
   E12, propager les incertitudes et injecter les figures dans les diapositives.
2. **Aucune mesure n'a été faite sur l'enceinte.** Pas une. Tout ce qui tourne
   aujourd'hui tourne sur un fichier étiqueté SYNTHÉTIQUE.
3. **Il ne reste donc que trois choses** : mesurer, décider, et tenir le
   calendrier administratif. C'est exactement ce que liste ce document.

---

## <a id="bord"></a>Tableau de bord — les échéances qui ne se rattrapent pas

Huit lignes. Tout le reste du document peut glisser de deux semaines sans casser
le projet ; celles-ci, non.

| # | Échéance | Date | Ce qui arrive si elle est manquée |
|---|---|---|---|
| 1 | **Obtenir l'accord explicite d'un professeur encadrant** (`1-A2`) — **FAIT le 16/09/2026 : M. Chevalier** ; reste `1-A3` (son compte SCEI, et le prévenir de la fenêtre de 8 jours de mi-juin 2027) | fin septembre 2026 | C'est le seul risque qui annule tout le reste, quelle que soit la qualité du travail. Sans encadrant déclaré à l'étape 1 **et** sans sa validation à l'étape 3, **la note peut être zéro**. Aucun repli n'existe. |
| 2 | **Franchir la porte d'étalonnage de la chaîne de mesure** (`1-D2`/`1-D4`) | mi-octobre 2026 | Rien ne démarre avant : ni la campagne $Z(f)$, ni l'identification, ni l'optimisation, ni la validation. Tant qu'elle n'est pas franchie, **tout le TIPE est de la théorie**. Une chaîne non qualifiée mesurant un objet inconnu ne produit aucune information. |
| 3 | **Geler D2 (cible de sommation) et D6 ($r_{max}$)** (`2-F1`, `2-F2`) | avant le premier achat, **début décembre 2026** | Reportées par décision datée du 13/09/2026 avec une échéance ferme : *avant le premier achat et avant le MCOT*. Acheter avant de trancher, c'est trancher sans le dire — et le choix fait varier la self de 18 à 27 mH et le cuivre de 41 à 291 € l'unité. |
| 4 | **Passer commande du fil et des condensateurs** (`2-I3`) | **avant le 15 décembre 2026** | Décembre-janvier est la pire période de l'année pour les délais. Commander le 20 décembre, c'est recevoir en janvier ; or la période 3 **commence** par le bobinage, qui est le poste le plus long et le plus facile à sous-estimer. |
| 5 | **Saisir l'étape 1 SCEI** (titre, encadrant, MCOT, mots-clés, positionnements) (`3-B3`) | ouverture mi-janvier, **clôture 5-6 février 2027** `[[à vérifier]]` | La saisie est **automatique, sans bouton « valider »**, et la fenêtre se ferme sans préavis. Pas d'étape 1, pas de TIPE. C'est aussi là que se verrouillent le binôme d'examinateurs et la fenêtre d'oraux. |
| 6 | **Avoir toutes les selfs bobinées et mesurées** (`3-C4` à `3-C7`) | **avant les vacances de février 2027** | Après, le semestre des concours compresse tout contre la clôture du 9-10 juin. Le bobinage est l'estimation la moins fiable du projet (1 à 2 h par self avec outillage, une demi-journée sans) : c'est lui qui déborde. |
| 7 | **Téléverser le PDF définitif et saisir le DOT — étape 2** (`3-H3`) | ouverture fin février, **clôture 9-10 juin 2027** `[[à vérifier]]` | Sans PDF téléversé, il n'y a **rien à projeter** : le jury projette depuis son ordinateur, et ni clé USB, ni ordinateur, ni objet ne sont admis en salle. La parade est `3-H2` : téléverser une version imparfaite dès qu'elle est présentable. |
| 8 | **Obtenir la validation de l'encadrant — étape 3** (`3-I1`, `3-I2`) | fenêtre de **8 jours seulement**, mi-juin 2027 (clôture ~19 juin) `[[à vérifier]]` | L'action la plus courte et la plus dangereuse du TIPE. Elle tombe en pleine période de jurys et de corrections, **rien ne te prévient si elle se referme**, et sans validation la note peut être zéro. C'est à toi de relancer, pas à lui d'y penser. |

**Charge totale estimée : ~165 h de travail effectif** (fourchette honnête : 145 à
190 h selon l'export de l'oscilloscope et le temps réel de bobinage — soit 39 à
53 h en période 1, dont 3 h de jig carte son ajoutées le 23/09/2026 (`1-D8`), 35 à 43 h en période 2 et 70 à 95 h en période 3), **dont ~80 h
entre janvier et mai 2027**. Dit autrement : **la période 3 demande à elle seule
plus du double de la période 2, dans une fenêtre plus contrainte** — le semestre
des concours, avec ~15 à 20 h de bobinage à caser avant mi-février et ~20 à 25 h
de campagnes de mesure avant les concours blancs de printemps. Ce sont des
estimations, pas des mesures ; elles sont données parce qu'un calendrier sans
nombre ne se pilote pas.

**Deux règles qui ne figurent dans aucune case du tableau mais qui décident du
reste** : on ne branche jamais le haut-parleur avant que la chaîne soit qualifiée,
et on ne descend jamais sous la fréquence d'accord $f_b$ au niveau fort — c'est le
seul geste du projet qui puisse détruire mécaniquement le 18″.

---

## <a id="maintenant"></a>Les trois actions du moment

*À réécrire à chaque revue mensuelle (`T-D10`) — daté ci-dessous, sinon cette
liste devient trompeuse dès novembre.*

**Au 23/09/2026** (liste du 16/09 mise à jour : `1-A2` est fait, M. Chevalier a
dit oui le 16/09/2026). Elles ne dépendent de rien ni de personne d'autre que toi,
et elles débloquent presque tout le reste.

1. **`1-A3` — Vérifier que M. Chevalier a un compte sur `lycees.scei-concours.fr`,
   et le prévenir dès maintenant de la fenêtre de validation de 8 jours de
   mi-juin 2027** (10 min). C'est ce qui reste de la ligne 1 du tableau de bord :
   l'accord est acquis, le compte et l'avertissement ne le sont pas.
2. **`1-A5` — Photographier l'enceinte, les évents, le câblage et les étiquettes**
   (20 min), **avant d'ouvrir quoi que ce soit**. C'est la seule action
   irréversible du bloc : `1-A4` exige les cotes intérieures, le diamètre
   intérieur des évents et la lecture du condensateur au bornier, c'est-à-dire un
   démontage. Une photo non prise avant ne se rattrape pas en juin.
3. **`1-A4` — Relever toutes les cotes de l'enceinte** (1 h à 1 h 30, à deux si
   possible). Évents, volume net, aires, entraxe, câblage, condensateur des
   pavillons. C'est ce relevé qui permet de **prédire $f_b$ avant de le mesurer** —
   et une prédiction écrite après la mesure ne vaut plus rien.

Dans la foulée, si le temps le permet : `1-A0` (lire la partie sécurité avant tout
branchement), `1-A1` (ouvrir le journal), `1-A7` (remontage et contrôle
d'étanchéité), `1-A6` (Claude calcule la prédiction de $f_b$ dès que tu lui
transmets les cotes) et **`1-B4`** (la commande des résistances du jig, dont la
liste a changé le 23/09/2026 : le délai de livraison est sur le chemin de la porte
d'étalonnage).

---

## <a id="p1"></a>PÉRIODE 1 — de maintenant (16 septembre 2026) à fin octobre 2026

**Ce que cette période doit produire.** À la fin octobre, trois choses doivent
être vraies, et rien d'autre ne compte : (1) tu as un **professeur encadrant** qui
a dit oui et qui a un compte SCEI ; (2) ta **chaîne de mesure d'impédance est
qualifiée** sur des composants dont tu connais la valeur ; (3) tu as les
**premières courbes Z(f)** de ton sub en caisse et de ton bloc médiums. Tout le
reste du TIPE — l'ajustement Thiele-Small, l'optimisation, la validation — est
déjà écrit, codé et testé dans le dépôt. Il attend des nombres.

**Comment lire cette liste.** Elle est ordonnée par dépendance, puis par date. Tu
peux la dérouler de haut en bas sans jamais te bloquer. Les durées sont des
**estimations de temps de travail effectif** : elles ne contiennent ni colles, ni
DS, ni concours blancs, ni vacances. Pour convertir en calendrier, compte à peu
près une action « courte » par soirée et une demi-journée de banc par week-end
utile. Quand une action revient à **Claude** (l'assistant), c'est écrit
explicitement ; dans ce cas, ta part se réduit à fournir la donnée ou la
décision, et c'est justement pour ça que ton temps doit aller au banc et au
mètre ruban, pas au traitement.

**Ce qui n'existe pas encore et qui n'est pas dans cette liste** : aucune mesure
de l'enceinte. C'est tout ce qui manque au projet, avec les décisions et
l'administratif.

> **Périodes ≠ phases.** Les trois périodes de ce document ne recouvrent pas les
> phases 0 à 5 de `FEUILLE-DE-ROUTE.md`, et le calendrier n'y est pas le même :
> ce document replanifie, il ne contredit pas. Table de correspondance :
>
> | Ici | Là-bas | Écart de calendrier |
> |---|---|---|
> | Période 1 (sept.–oct. 2026) | fin de phase 0 + phase 1 (mesure de $Z(f)$) | conforme |
> | Période 2 (nov.–déc. 2026) | phases 2 et 3 (identification, optimisation) | conforme depuis le réalignement du 23/09/2026 (la feuille de route date désormais la phase 1 de sept.–oct. et la phase 2 de novembre, la porte d'étalonnage occupant octobre) |
> | Période 3 (janv.–juin 2027) | phases 4 et 5 (fabrication, validation, oral) | la feuille de route ouvre la phase 4 en **décembre 2026** ; elle démarre ici en **février 2027**, après les selfs |
>
> `FEUILLE-DE-ROUTE.md` a été réalignée le 23/09/2026 pour les phases 1 et 2 ;
> l'écart sur la phase 4 demeure : c'est un écart connu, à traiter dans la même
> passe que `T-E7` (relecture trimestrielle de cohérence).
> En attendant, **pour les dates, c'est ce document qui sert** ; pour le *pourquoi*
> scientifique de chaque phase, c'est la feuille de route.

---

### <a id="1a"></a>1-A. Cette semaine — ouvrir le journal, sécuriser l'encadrant, relever les cotes

Ces neuf actions ne dépendent de rien d'autre que de toi, et elles débloquent
presque tout le reste. Les faire dans cet ordre — et **`1-A5` avant `1-A4`**,
parce que `1-A4` ouvre la caisse et que la photo d'avant ne se refait pas.

- [ ] **1-A0. Lire la partie `T-A` (Sécurité) et les actions `T-B1`–`T-B2`
      (gabarit du cahier) AVANT la première séance de banc.** Elles sont écrites à
      la fin du document pour ne pas couper le fil des périodes, mais ce sont des
      **prérequis de la période 1**, pas des annexes : `T-A2`/`T-A3` (check-list de
      séance) débloquent `1-D2` ; `T-A5` ($X_{max}$, sensibilité, SPL max du micro)
      bloque `1-C4` ; `T-A6` et `T-A7` (borne basse, ordre des campagnes)
      débloquent `1-E2`, `1-E3` et `1-E4` ; `T-A8` (condensateur des pavillons)
      débloque `1-B5` ; `T-A9` (tenue en tension) bloque `2-I1` ; `T-A10` (diode de
      roue libre) bloque `3-C6` ; `T-B1` débloque la séance 1. À poser aussi dès
      aujourd'hui : `T-D1`, `T-D5` et `T-D11`.
      *Durée : 1 h de lecture, une seule fois, avant de brancher quoi que ce soit.*
      *Débloque :* tout le bloc `1-D` et tout le bloc `1-E`.
      *Fini quand :* les actions `T-A1` à `T-A10`, `T-B1`, `T-B2`, `T-D1`, `T-D5`
      et `T-D11` sont **cochées là où elles sont écrites** — quinze cases, pas
      « lues ».

- [ ] **1-A1. Ouvrir un journal de bord daté** (cahier papier, un seul, pas de
      feuilles volantes). Première page : nom, sujet, date d'ouverture. Ensuite,
      une entrée par séance de travail, datée, avec ce qui a été fait, ce qui a
      raté, et le numéro des fichiers produits.
      *Durée : 30 min d'ouverture, puis 5 à 10 min à la fin de chaque séance.*
      *Débloque :* le **DOT** (4 à 8 jalons factuels de 50 mots, à déposer entre
      fin février et début juin 2027) se rédige en une heure si le journal
      existe, et se reconstitue de mémoire — donc mal — s'il n'existe pas. C'est
      aussi le seul document papier réellement admis en salle avec les listings.
      *Fini quand :* le cahier existe, porte une date d'ouverture, et contient
      déjà l'entrée du 16/09/2026 (« constat : caisse bass-reflex, deux évents,
      2 pavillons en parallèle des médiums »).

- [x] **1-A2. Demander à un professeur d'être ton encadrant TIPE**, et obtenir un
      **oui explicite** (pas un « on verra »). **FAIT le 16/09/2026 : M. Chevalier**,
      accord explicite obtenu (décision D10 de `DECISIONS-PHASE-0.md`). La mention
      d'un professeur N. Cavallo dans un commit de juin 2026 est donc caduque.
      *Durée : 10 min de conversation, à provoquer cette semaine.*
      *Débloque :* **la note elle-même**. Sans encadrant déclaré à l'étape 1
      (saisie de mi-janvier 2027) et sans sa validation à l'étape 3 (mi-juin
      2027, fenêtre de **huit jours seulement**), la note peut être zéro. C'est
      le seul point du cadre SCEI qui peut coûter l'épreuve entière, et il ne
      coûte que dix minutes aujourd'hui.
      *Fini quand :* tu as un nom, un accord oral explicite, et l'entrée datée
      dans le journal.

- [ ] **1-A3. Vérifier que cet enseignant dispose d'un compte sur
      `lycees.scei-concours.fr`**, et lui signaler dès maintenant la fenêtre de
      validation de mi-juin 2027 (8 jours) pour qu'il ne la découvre pas en
      pleine période de concours.
      *Durée : 10 min, à la prochaine rencontre avec M. Chevalier (D10 le marque
      encore « reste à vérifier » au 23/09/2026).*
      *Bloqué par :* 1-A2 (fait). *Débloque :* la saisie de l'étape 1.
      *Fini quand :* la réponse (oui / non / « je fais créer le compte ») est
      écrite et datée dans `DECISIONS-PHASE-0.md`, décision **D10**.

- [ ] **1-A5. Photographier l'enceinte, les évents, le câblage interne et les
      étiquettes des haut-parleurs**, **avant** tout démontage — donc **avant
      `1-A4`**, qui ouvre la caisse. C'est la seule action irréversible du bloc.
      *Durée : 20 min.*
      *Débloque :* `1-A4` (qui ne doit pas commencer avant).
      *Débloque :* les planches d'oral. **L'enceinte, le filtre et la self sont
      des objets interdits en salle** : les photos sont la seule façon de les
      montrer. Une photo non prise aujourd'hui ne se rattrape pas en juin.
      *Fini quand :* les images sont dans `assets/`, nommées et datées.

- [ ] **1-A4. Relever au pied à coulisse et au mètre toutes les cotes de
      l'enceinte.** Liste exhaustive, à faire en une fois :
      | Grandeur | Précision visée | Pourquoi |
      |---|---|---|
      | Diamètre **intérieur** de chaque évent | ±1 mm | entre au carré dans $f_b$ |
      | Longueur de chaque évent | ±2 mm | masse d'air |
      | Extrémités : arête vive ou évasées (*flare*) ? intérieure proche d'une paroi ? | description écrite | commande la correction de bout (±3 % sur $f_b$) |
      | Les deux évents sont-ils **identiques** ? | oui/non | si non, la formule change |
      | Cotes intérieures de la caisse → volume **net** ($V_b$ = brut − saladiers − renforts − tubes d'évent) | ±5 % | c'est la grandeur qui **domine** l'incertitude sur $f_b$ |
      | $S_d$ (diamètre effectif de la membrane) et $S_p$ (section d'un évent) | ±2 mm | pondération de la sommation de Keele en phase 4 |
      | Distance entre le centre du 18″ et le centre du bloc médiums | ±1 cm | c'est le $\tau$ de la décision D5 |
      | Câblage réel des deux médiums : série confirmée ? | vérifié à l'ohmmètre | 8 Ω attendus |
      | **Valeur** du condensateur en série avec chaque pavillon (**présent**, constat du 16/09/2026), lue sur le corps | valeur exacte | déplace $|Z|$ du bloc médiums de −10 à −26 % à 100 Hz (29,3 → 26,3 à 21,8 Ω pour 3,3 à 10 µF, deux pavillons ; calculé, pas mesuré) |
      *Durée : 1 h 30 à 2 h 30, une seule fois, **à deux obligatoirement** : un 18″
      pèse lourd, il se dépose et se repose à deux, joint propre et vis serrées en
      croix. Cette manutention n'est pas du temps mort, c'est la moitié de la
      durée.*
      *Bloqué par :* **`1-A5`** — on photographie avant d'ouvrir, jamais après.
      *Débloque :* la prédiction de $f_b$ (1-A6), la grille de mesure de la
      campagne Z(f) (1-E2), la pondération $w_\varphi$ de D5 (via le $\tau$ de la
      dernière ligne — c'est **la seule fois** où ces longueurs se mesurent, 2-F4
      et 3-D4 n'y reviennent que pour un contrôle), les poids de la sommation de
      Keele de 1-E7, et le protocole acoustique de la phase 4.
      *Fini quand :* toutes les lignes du tableau ont un nombre ou une phrase, au
      journal, datées — **aucune case vide, aucun « à peu près »** — et la caisse
      est refermée selon `1-A7`.
      *Note :* la dernière ligne (valeur du condensateur des pavillons) est la
      même action que `T-A8`. Sa **présence** est acquise depuis le 16/09/2026 ;
      seule sa **valeur** reste à relever. Y répondre une fois suffit, coche les
      deux.

- [ ] **1-A6. (CLAUDE) Calculer la prédiction de $f_b$ par le résonateur de
      Helmholtz** à partir des cotes de 1-A4, avec l'encadrement complet des
      conventions de correction de bout et le budget d'incertitude, puis
      l'inscrire **datée** au dépôt et au journal.
      *Durée : quelques minutes côté Claude, une fois 1-A4 transmis.*
      *Bloqué par :* 1-A4. *Débloque :* rien mécaniquement — mais c'est la seule
      façon d'avoir une **prédiction falsifiable**. Écrite après la mesure de
      $f_b$, elle ne vaut plus rien ; écrite avant, elle ferme une
      boucle théorie/expérience indépendante de l'ajustement, et c'est exactement
      ce qu'un jury cherche.
      *Fini quand :* un intervalle (pas un nombre unique) est écrit et daté,
      **avant** la moindre mesure électrique.

- [ ] **1-A7. Refermer la caisse et contrôler son étanchéité**, immédiatement après
      `1-A4`. Joint neuf ou joint d'origine en bon état, vis serrées en croix, puis
      contrôle : à l'oreille et à la main sur les bords pendant un sinus de
      30-40 Hz à faible niveau, ou (mieux) **en refaisant un balayage d'impédance
      grossier après remontage et en vérifiant que le creux n'a pas bougé**.
      *Durée : 45 min, dont le temps de séchage éventuel du joint.*
      *Bloqué par :* 1-A4. *Débloque :* la validité de tout le bloc `2-C`.
      *Pourquoi ça n'est pas du bricolage* : une fuite change $Q_l$ **et** $f_b$,
      c'est-à-dire exactement deux des huit paramètres du modèle bass-reflex et la
      cible du recoupement à trois voies de `2-D`. Ouvrir la caisse sans contrôler
      le remontage, c'est mesurer une autre caisse que celle qu'on a cotée.
      *Fini quand :* le contrôle est fait et son résultat écrit — « pas de fuite
      détectée » est une phrase de cahier, avec la méthode employée.

- [ ] **1-A8. Statuer par écrit sur le crossover actif du commerce actuellement en
      service** dans l'enceinte. Trois questions, trois réponses au registre :
      (a) il se **dépose avant toute mesure** (les $Z(f)$ de `1-E` se mesurent aux
      bornes des haut-parleurs, pas derrière un filtre inconnu) ; (b) constitue-t-il
      déjà la « référence active » du projet, ce qui rendrait le Sallen-Key de
      `3-D2` redondant — ou le montes-tu quand même parce que ses valeurs sont
      connues, calculables et défendables au tableau, ce que l'appareil du commerce
      n'est pas ? (c) sa présence change-t-elle le **critère n° 6 « coût système »**,
      puisqu'un crossover actif déjà acheté ne se recompte pas comme une dépense
      nouvelle ?
      *Durée : 30 min de décision, 20 min de dépose.*
      *Débloque :* `3-D2` (une demi-journée de montage qu'il faut assumer ou
      supprimer en connaissance de cause) et le chiffrage du critère n° 6.
      *Fini quand :* les trois réponses sont écrites et datées — c'est aussi une
      question de jury quasi certaine (« vous aviez déjà un filtre actif : pourquoi
      en refaire un ? »).

---

### <a id="1b"></a>1-B. Fin septembre — inventaire du matériel et achats

- [ ] **1-B1. Faire l'inventaire du matériel de mesure du lycée**, appareil par
      appareil, en notant les **modèles exacts** :
      oscilloscope numérique (nombre de voies — il en faut **deux**, bande
      passante, profondeur mémoire) ; GBF (fréquence minimale atteignable — il
      faut descendre **sous 20 Hz**, impédance de sortie, amplitude max) ;
      multimètre (a-t-il un **capacimètre** ? un mode **REL/zéro** ? une fonction
      **quatre fils** ?) ; sondes (×1/×10, appariées ?) ; té BNC ; résistance de
      puissance 8 ou 10 Ω ; pinces crocodile.
      *Durée : 45 min sur place, avec le professeur ou le technicien.*
      *Débloque :* la liste d'achats 1-B4 (on n'achète que ce qui manque) et le
      choix du montage.
      *Fini quand :* la liste des modèles est au journal, avec pour chaque poste
      « disponible / à emprunter / à acheter ».

- [ ] **1-B2. Vérifier que l'oscilloscope sait EXPORTER ses données** (clé USB,
      CSV, capture d'écran), et faire un export d'essai que tu rapatries
      réellement sur ton ordinateur.
      *Durée : 20 min, pendant 1-B1.*
      *Débloque :* tout le dépouillement automatique. **C'est le point qui décide
      du rythme de tout le projet** : avec export, une campagne Z(f) est une
      séance ; sans export, c'est une lecture de curseurs point par point,
      plusieurs centaines de nombres recopiés à la main, avec les fautes de
      frappe qui vont avec. Si l'export n'existe pas, il faut le savoir
      maintenant pour basculer vers la variante carte son + REW, pas le jour de
      la mesure.
      *État au 23/09/2026 :* cette variante n'est plus hypothétique. L'interface
      est connue (**Focusrite Scarlett Solo 3ᵉ génération**, confirmée le
      16/09/2026, voir `1-B3`) et le câblage de son jig d'impédance est arrêté
      (arbitrage du 23/09/2026, `CLAUDE.md` § Matériel) : si l'oscilloscope
      n'exporte pas, la bascule ne demande que les composants de `1-B4`. L'export
      reste à vérifier pour la chaîne GBF + oscilloscope, qui sert de recoupement.
      *Fini quand :* un fichier issu de l'oscilloscope est ouvert sur ton
      ordinateur.

- [ ] **1-B3. Documenter la carte son et le micro de mesure** : modèles exacts,
      entrées disponibles, **SPL maximal admissible du micro**, présence d'une
      boucle de retour (loopback) pour la mesure de phase.
      *Durée : 30 min (recherche des notices).*
      *Débloque :* la variante rapide REW de la phase 1, tout le protocole
      acoustique, et la décision D3 (le niveau fort est plafonné par le SPL max
      du micro).
      *La vérification à ne pas sauter — et à faire **maintenant**, pas en
      février* : **le micro est-il un micro USB ?** Si oui, tout le protocole
      acoustique s'effondre : le § 07.10 est formel, « le micro et la boucle
      doivent être sur la même interface […] un micro USB est donc exclu de tout ce
      protocole ». Sans référence temporelle commune, il n'y a ni sommation
      complexe en champ proche (1-E7, 3-E5), ni mesure de polarité (3-E8), ni
      phase. C'est une découverte à faire en septembre, quand il reste le temps
      d'emprunter ou d'acheter une interface XLR.
      *Fini quand :* les trois informations sont écrites au dépôt **et** que la
      ligne « micro XLR sur interface à deux entrées avec boucle de retour :
      oui / non » porte une réponse.
      *État au 23/09/2026 — la moitié « carte son » est faite :*
      - [x] **Carte son** : **Focusrite Scarlett Solo 3ᵉ génération** (confirmée
        le 16/09/2026). Deux entrées : **entrée 1 XLR** (préampli micro, 3 kΩ,
        48 V disponible) et **entrée 2 jack 6,35 TRS** (LINE 60 kΩ, ou INST) ;
        sorties ligne arrière (430 Ω) et **sortie casque** (< 1 Ω). Caractéristiques
        et conséquences : `CLAUDE.md` § Matériel.
      - [x] **Boucle de retour** : **pas nécessaire en mode impédance de REW** — la
        voie de référence (entrée 1, XLR) lit directement la sortie casque au
        nœud A du jig, ce qui fournit la référence de niveau et de temps. Pour
        l'acoustique (`1-D6`), l'entrée 2 est libre et reçoit la boucle (sortie
        arrière droite → entrée 2) : micro et boucle sont bien **sur la même
        interface**.
      - [ ] **Micro de mesure** : modèle exact, **XLR ou USB**, et **SPL maximal
        admissible** `[[à documenter]]`. C'est ce qui reste de 1-B3.
      **Réponse à la ligne** : « micro XLR sur interface à deux entrées avec
      boucle de retour » — **interface à deux entrées : oui ; boucle de retour :
      oui (entrée 2) pour l'acoustique, inutile pour l'impédance ; micro XLR :
      `[[à vérifier]]`** tant que le modèle du micro n'est pas écrit.

- [ ] **1-B4. Passer la commande des composants de la phase 1.** Liste minimale
      (**révisée le 23/09/2026** après l'arbitrage sur le jig d'impédance, voir
      `CLAUDE.md` § Matériel) :
      - **deux résistances de 100 Ω à 0,1 %** : l'une est la **R_sense** du jig
        carte son, l'autre la **référence d'étalonnage de REW** (étalonnage
        « reference »). Deux pièces distinctes, obligatoirement : la référence ne
        sert jamais de R_sense ni de dipôle de validation. Puissance : ≥ 0,25 W
        suffit au jig (calcul : 32 mW au pire, sortie casque à pleine échelle).
        **Aucune des deux ne sert à la chaîne GBF + oscilloscope** : si la
        référence de REW y servait aussi d'étalon, les deux chaînes partageraient
        le même facteur d'échelle et le recoupement A7 ne pourrait plus détecter
        une erreur sur cette résistance ;
      - **une troisième 100 Ω, à 1 %, ≥ 1 W, film métallique** : la $R_{ref}$ de
        la chaîne **GBF + oscilloscope** (configuration A, livret A6), distincte
        des deux 0,1 % ;
      - **une résistance de 33 Ω, ≥ 0,25 W**, tolérance indifférente : la
        **protection de la sortie casque**, en tête du jig ;
      - **une 10 Ω, à 0,1 % si possible** (sinon 1 %, mesurée en A1 du livret) :
        ce n'est **plus** une résistance de mesure, c'est le **dipôle de
        validation** de la chaîne carte son, la résistance connue de la manip A5
        (sous 20 Hz) et le recoupement de la chaîne GBF + oscilloscope
        (configuration B) ;
      - *facultatif* : **une 33 Ω à 1 %**, le repli du livret (A1) ;
      - un condensateur **100 µF** et un condensateur **10 µF film MKP** qui
        serviront d'étalons ;
      - **connecteurs du jig** : une **fiche XLR mâle à souder** (ou un cordon XLR
        à couper) pour l'entrée 1, une **fiche jack 6,35 mm TRS** (stéréo) pour
        l'entrée 2, une **fiche jack 6,35 mm TRS** pour la sortie casque — jamais
        de fiche mono TS dans la sortie casque ;
      - **une résistance de ballast 10 Ω / 5 W** (bobinée ou boîtier alu,
        tolérance indifférente, sa valeur exacte sera mesurée) : elle limite le
        courant des mesures quatre fils (livret A1-b et B1-b, 0,1 à 0,2 A). Elle
        est **distincte de la 10 Ω de précision**, qui ne doit jamais chauffer ;
        à ne pas acheter si le lycée en prête une (à vérifier en 1-B1) ;
      - cordons et pinces, wattmètre de prise (~20 €), **bouchons d'oreilles**,
        pied à coulisse si tu n'en as pas, et une résistance de puissance 8 Ω
        **seulement si 1-B1 montre qu'elle manque au lycée**.
      *Plus tard, pour le groupe C du livret (banc électrique), pas maintenant* :
      un **shunt de 1 Ω à 1 %, ≥ 5 W** pour la DCR des selfs à 1 A (C1-b), et, faute
      d'alimentation de laboratoire limitée en courant, un ballast **10 Ω / 20 W**.
      *Ce qui a changé et pourquoi* : l'ancienne liste (une 100 Ω à 1 % et une
      10 Ω « pour le recoupement ») servait un câblage du 16/09/2026 reconnu
      faux le 23/09/2026 (micro aux bornes d'une $R_{ref}$ de 10 Ω : le calcul de
      charge ignorait les jambes de mode commun et la réjection, non publiées, de
      l'entrée XLR, et REW en abandonne l'étalonnage open). Ne pas commander
      d'après une version antérieure de cette liste.
      *Durée : 45 min à 1 h de commande (la liste s'allonge des trois
      connecteurs), puis 3 à 10 jours de livraison. Coût : seul le wattmètre est
      chiffré (~20 €) ; le reste est à relever sur la commande.*
      *Bloqué par :* 1-B1 — **pour la seule résistance de puissance 8 Ω** : les
      résistances et connecteurs du jig ne dépendent pas de l'inventaire du
      lycée et peuvent partir tout de suite. *Débloque :* la séance d'étalonnage
      (1-D2), qui ne peut pas commencer sans étalons.
      *Fini quand :* la commande est passée. **Anticipe le délai** : commande
      fin septembre pour mesurer mi-octobre.
      *Garde-fou :* **n'achète aucune self ni aucun condensateur de filtre pour
      l'instant.** Ces achats dépendent de la décision D2 (18 mH ou 27 mH, 150 µF
      ou 100 µF) et de D6 ($r_{max}$, qui commande la masse de cuivre, donc le
      prix — de 41 € à 291 € la self selon le choix). Acheter avant de trancher,
      c'est trancher sans le dire.

- [ ] **1-B5. Choisir la configuration de masse (A, B ou C du § 02.2) et écrire la
      $R_{ref}$ de la passe 1 (§ 02.4), AVANT la première séance.** Trois
      configurations de masse existent, elles ne donnent pas les mêmes
      incertitudes, et l'une d'elles court-circuite le dipôle si on la câble à
      l'envers. Le choix de $R_{ref}$ dépend en plus de l'excursion attendue de
      $|Z|$ : sur un 18″ bass-reflex dont le pic peut atteindre 60 à 200 Ω, une
      $R_{ref}$ trop petite noie le signal de référence, une trop grande écrase
      celui du dipôle. **Pour la passe 1, la valeur est fixée** : $R_{ref}$ =
      100 Ω à 1 % en configuration A (livret A6, § 02.4), la 10 Ω n'intervenant
      qu'en configuration B, pour le recoupement au pic. Une révision éventuelle
      se fait **après** la passe 1, sur les valeurs mesurées, et se date au
      cahier.
      *Portée (précisée le 23/09/2026) :* ce choix ne concerne que la chaîne
      **GBF + oscilloscope**. Pour le jig **carte son**, il n'y a rien à choisir :
      $R_{sense} = 100$ Ω à 0,1 % et la **masse unique au nœud C** sont arrêtées
      par l'arbitrage du 23/09/2026 (`CLAUDE.md` § Matériel).
      *Durée : 45 min de lecture et de décision.*
      *Bloqué par :* 1-B1 (ce qui existe au lycée).
      *Débloque :* `1-D1`, `1-D2` et tout le budget d'incertitude — la
      configuration est une **ligne d'en-tête obligatoire** du cahier (`T-B1`) :
      elle ne peut pas être « celle qu'on avait ce jour-là ».
      *Fini quand :* une lettre (A, B ou C), la $R_{ref}$ de la passe 1 et les
      deux motifs d'une phrase sont écrits au journal, datés — **avant** la
      séance, pas pendant.

---

### <a id="1c"></a>1-C. Début octobre — geler ce qui peut l'être

Le registre `DECISIONS-PHASE-0.md` contient dix décisions. **Six peuvent être
gelées maintenant, une l'est déjà, une reste volontairement ouverte, et deux
attendent une donnée.** Chaque décision gelée est une chose de moins à
rediscuter, et surtout une chose de moins à pouvoir être accusée d'avoir choisie
après avoir vu les résultats.

- [ ] **1-C1. Geler D7 — gabarit des figures et des slides.** Recommandation du
      dépôt : slides **1024 × 768** (le 4/3 est imposé par le SCEI, pas
      négociable), figures matplotlib `figsize = (8.53, 6.40)` à `dpi = 120`.
      *Durée : 15 min de lecture, la décision est quasi automatique.*
      *Débloque :* **toutes les figures des phases 2 à 4.** À geler **avant la
      première figure**, sinon elles sont toutes à refaire. C'est la décision la
      moins intéressante du registre et la plus coûteuse à oublier.
      *Fini quand :* la ligne DÉCISION de D7 est remplie, datée, signée.

- [ ] **1-C2. Geler D1 — définition de $f_c$.** La recommandation est le
      **croisement des deux voies**, avec la convention de demi-puissance
      (−3,0103 dB) pour les repères. Tu peux décider contre, à condition
      d'écrire pourquoi.
      *Durée : 30 min de lecture attentive de D1.*
      *Débloque :* la porte de validation ±5 % de la phase 4, et le critère n° 2.
      *Fini quand :* la ligne DÉCISION de D1 est remplie, datée, signée.

- [ ] **1-C3. Geler D4 — les huit critères de comparaison**, avec les trois
      amendements proposés (déclasser le critère n° 2, ajouter l'écart maximal au
      critère n° 1, geler la définition complète du critère n° 1 : bande
      40–250 Hz, 24 points/octave, plancher 20 dB, arrondi 0,1 dB, 3 répétitions,
      seuil de départage).
      *Durée : 45 min.*
      *Débloque :* toute la conclusion du TIPE. **C'est le gel qui rend la
      comparaison honnête** : ajouter ou retirer un critère après avoir vu les
      courbes, c'est choisir le vainqueur puis écrire le règlement. Le bon moment
      pour amender la liste, c'est maintenant.
      *Fini quand :* la ligne DÉCISION de D4 est remplie, datée, signée.

- [ ] **1-C4. Geler D3 — les deux niveaux d'écoute.**
      Recommandation : faible = **2 V eff**, fort = **9 V eff** aux bornes du
      haut-parleur, conditionnement 5 min de bruit rose. Contrainte non
      négociable rattachée : au niveau fort, **aucun contenu sous $2f_b$**.
      *Durée : 30 min.*
      *Bloqué par :* 1-B3 et **`T-A5`** (le SPL max du micro plafonne le niveau
      fort, et c'est très probablement lui qui plafonne, pas l'enceinte).
      *Ce que cette décision commande ailleurs* : la tenue en tension des
      condensateurs du filtre. La règle et son chiffre sont en `T-A9`, et ils
      s'appliquent au moment de l'achat, en **`2-I1`** — pas ici. Cette ligne
      n'est qu'un renvoi : ne rien acheter sur sa foi.
      *Débloque :* le critère « robustesse », et surtout la **sécurité** de
      toutes les séances de banc.
      *Fini quand :* les deux tensions, les deux puissances et la durée de
      conditionnement sont écrites, datées, signées.

- [ ] **1-C5. Geler D9 — filière (PT ou PSI), TIPE seul ou en groupe, et
      positionnements thématiques.** Le premier positionnement doit être dans un
      domaine de rattachement de ta filière (Physique ou Sciences industrielles
      pour PT et PSI) : la recommandation est **Électronique** en rang 1, puis
      Mathématiques Appliquées, puis Physique Ondulatoire ou Automatique.
      *Durée : 30 min, mais la partie « filière » est une information, pas une
      décision — tu la connais.*
      *Débloque :* la saisie de l'étape 1 (mi-janvier 2027), la **fenêtre
      d'oraux**, et le **binôme d'examinateurs** qui t'interrogera.
      *Fini quand :* filière, mode (seul/groupe), trois positionnements et titre
      provisoire sont écrits, datés, signés.

- [ ] **1-C6. Demander deux devis de fil de cuivre émaillé** (diamètres 1,0 / 1,25 /
      1,5 mm, prix au kg **et** diamètres réellement vendus au détail) auprès de
      deux distributeurs. **C'est l'unique action « devis » du parcours** :
      `T-D8` en est le rappel, et il n'y en a pas d'autre plus tard.
      *Durée : 45 min d'envoi, réponse sous quelques jours.*
      *Débloque :* la décision **D6** ($r_{max}$ de la self) et le critère n° 5
      « coût marginal », qui se mesure sur factures. Le « 25 €/kg » qui
      circule dans le dépôt n'est **pas une source** : tous les montants en euros
      lui sont strictement proportionnels, donc tous les arbitrages budgétaires
      reposent dessus. Un devis remplace une hypothèse par un fait.
      *Ce que cette action n'autorise PAS :* choisir $r_{max}$ pour tenir un
      budget. Demander un prix au kilo est une **donnée d'entrée** de D6 ;
      laisser le devis fixer $r_{max}$ est la faute que `T-D7` dénonce. Les deux
      gestes se ressemblent et n'ont rien à voir.
      *Fini quand :* deux prix réels, datés et sourcés, sont au dépôt, avec les
      diamètres disponibles — si le diamètre calculé n'est pas vendu au détail, on
      prendra le voisin et on **recalculera $r$** avant de commander (en `2-I1`).

- [ ] **1-C7. Geler le seuil de rejet d'une mesure « niveau fort » sur la distorsion
      (THD), et décider de l'exporter systématiquement.** Le § 07.10 le marque
      `[[à geler en phase 0]]` et n'en propose pas la valeur : c'est à toi de la
      poser, maintenant, avant d'avoir vu la moindre courbe.
      *Durée : 30 min.*
      *Débloque :* le **critère n° 8 « robustesse »**. Sans seuil ni export, un
      écart entre niveau faible et niveau fort ne peut **pas** être attribué à la
      dérive thermique plutôt qu'à la non-linéarité de la suspension, à $Bl(x)$ ou
      à la turbulence des évents — c'est-à-dire que le critère mesure « quelque
      chose », sans qu'on puisse dire quoi. Or c'est tout l'objet du critère.
      *Fini quand :* un nombre (THD en % au-delà duquel un balayage fort est
      écarté et refait plus bas), la bande sur laquelle il se lit, et la consigne
      « exporter la THD de chaque balayage » sont écrits, datés, signés.

- [ ] **1-C8. Geler la règle de réglage de la référence active** (§ 07.6), et la
      consigner comme **entrée complémentaire du registre** (proposition : `D11` —
      le registre en compte dix aujourd'hui, celle-ci est à créer).
      Deux formulations, il faut en choisir une, et elles ne disent pas la même
      chose :
      **(a)** les gains actifs sont réglés pour reproduire le $\Delta S$ mesuré en
      `1-E7`/`1-E8`, sans aucune optimisation du critère → l'actif est un **cas
      comparable**, jugé à armes égales ;
      **(b)** les gains actifs sont optimisés librement → l'actif est présenté
      comme une **borne supérieure**, pas comme un concurrent.
      *Durée : 30 min.*
      *Débloque :* l'honnêteté de toute la comparaison. En passif, l'équilibre
      entre voies est figé par des composants E12 et un éventuel L-pad ; en actif,
      il se règle au potentiomètre. **Laisser l'actif se régler librement sans le
      déclarer lui donne un avantage structurel non déclaré** — c'est-à-dire
      exactement la « comparaison truquée » que tout le projet s'interdit.
      *Fini quand :* (a) ou (b) est écrit, daté, signé, **avant** la première
      mesure acoustique.

- [ ] **1-C9. (CLAUDE) Répercuter les décisions gelées dans tout le dépôt** :
      `analyse/criteres_geles.json`, `FEUILLE-DE-ROUTE.md`,
      `REFERENCE-TECHNIQUE.md`, `NOTES-TIPE.md`, et cocher les cases de la porte
      de validation de la phase 0.
      *Durée : côté Claude, une session.*
      *Bloqué par :* 1-C1 à 1-C8. *Fini quand :*
      `python analyse/tout_refaire.py` passe au vert avec les nouvelles valeurs
      gelées.

> **Ce qui reste délibérément ouvert.** **D2** (cible de sommation : Butterworth
> inversé ou somme plate LR2) a été **reportée après la phase 1 par décision
> datée du 13/09/2026** — la cible sera choisie sur la $Z(f)$ réellement mesurée.
> Ce report est lui-même défendable devant un jury. Mais il a une **échéance
> ferme** : avant le premier achat de composants et avant la rédaction du MCOT
> (novembre-décembre 2026). **D5** attend le $\tau$ mesuré en 1-A4 et **D6** attend
> le devis de 1-C6 : les deux se gèleront en novembre.

---

### <a id="1d"></a>1-D. Mi-octobre — les deux étalonnages : **rien d'autre**

C'est la porte qui dérisque tout le projet. Tant qu'elle n'est
pas franchie, **tout le reste du TIPE est de la théorie** : 19 319 lignes de
Python qui tournent sur un fichier étiqueté SYNTHÉTIQUE, des courbes engendrées
par un modèle, et zéro nombre mesuré. Aucun haut-parleur n'est branché pendant
ces séances.

**Deux chaînes, deux étalonnages.** `1-D1` à `1-D5` qualifient la chaîne
**électrique** (GBF, oscillo, $R_{ref}$) — une demi-journée au lycée. `1-D6` et
`1-D7` qualifient la chaîne **acoustique** (carte son, micro, boucle de retour) —
une soirée chez toi. **Et la mesure d'impédance a elle-même deux chaînes**, qui
doivent se recouper : la chaîne GBF + oscilloscope (`1-D2`, manip A6 du livret
`protocole/PROTOCOLE-EXPERIENCES.html`) et le **jig carte son + REW** sur la
Scarlett Solo (`1-D8`, manips A2, A3 et A5), recoupées en A7. `1-D8` a été
ajoutée le 23/09/2026, avec l'arbitrage sur le câblage du jig ; elle est placée
après `1-D2` parce qu'elle s'exécute là, et numérotée à la suite pour ne casser
aucun renvoi. La maxime du projet, « on ne mesure pas un objet inconnu avec
un instrument inconnu », vaut pour les deux moitiés de l'instrumentation, pas
seulement pour celle qui est la plus facile à étalonner.

- [ ] **1-D1. Préparer la séance sur papier avant d'entrer en salle** : imprimer la
      fiche de relevé, écrire l'ordre des six étapes, préparer le schéma du
      montage (GBF → $R_{ref}$ → dipôle, mesure de **$V_{dipôle}$ ET
      $V_{Rref}$** sur les deux voies, jamais d'hypothèse « courant constant »),
      et repérer où sont les pinces de masse. **Imprimer le livret depuis
      `protocole/PROTOCOLE-EXPERIENCES.html`, jamais depuis
      `protocole/PROTOCOLE-EXPERIENCES.pdf`** tant que ce PDF ne porte pas la
      mention « Relu le 23 septembre 2026 » : le PDF actuel, antérieur à
      l'arbitrage, décrit encore l'ancien câblage du jig ($R_{ref}$ de 10 Ω).
      *Durée : 1 h.*
      *Débloque :* une séance qui tient dans une demi-journée au lieu de deux.
      *Fini quand :* la fiche est imprimée et le schéma dessiné au journal.

- [ ] **1-D2. Faire la séance d'étalonnage, dans cet ordre strict :**
      | # | Étape | Attendu |
      |---|---|---|
      | 0 | Offset de chaque voie (entrées court-circuitées), puis appariement des deux voies sur le même signal (té BNC), à chaque couple de calibres | rapport voie1/voie2 = 1,00 ± 0,01 |
      | 1 | Résistance de puissance, valeur DC relevée au multimètre avec REL (les cordons font ~0,2 Ω) | $|Z|$ **plat**, $\varphi = 0$ |
      | 2 | Condensateur **100 µF sur 10–100 Hz**, puis **10 µF MKP sur 100 Hz–1 kHz** | pente **−1** en log-log, $\varphi = -90°$ |
      | 3 | Recoupement 10 Ω / 100 Ω sur les deux dipôles | écarts compatibles |
      | 4 | Répéter **5 fois** la lecture complète d'un même point, curseurs re-réglés à chaque fois | donne la composante aléatoire du budget d'incertitude |
      *Durée : une demi-journée (4 h), une seule fois si tout va bien.*
      *Bloqué par :* 1-B4 (livraison des étalons), 1-B1 (matériel).
      *Débloque :* **la campagne Z(f), la phase 2, la phase 3, la phase 4.** Rien
      ne démarre avant.
      *Fini quand :* les relevés sont faits et saisis — pas quand ils sont
      « bons » : le verdict, c'est 1-D4.

- [ ] **1-D8. Monter, apparier et étalonner le jig d'impédance carte son + REW,
      puis le valider sur des dipôles connus** — manips **A2, A3 et A5** du livret.
      Le détail geste par geste est là-bas, pas ici ; **le câblage qui fait foi
      est celui de l'arbitrage du 23/09/2026** (`CLAUDE.md` § Matériel, puce
      « Câblage retenu »). Le livret HTML (relu le 23/09/2026) y est conforme ;
      **son PDF antérieur ne l'est pas : ne pas imprimer
      `protocole/PROTOCOLE-EXPERIENCES.pdf` tant qu'il ne porte pas la mention
      « Relu le 23 septembre 2026 »**. Les étapes, dans cet ordre :
      | # | Étape | Attendu |
      |---|---|---|
      | 0 | **Montage standard de REW**, lu en 4 fils : sortie casque (canal gauche) → 33 Ω → nœud A → $R_{sense}$ 100 Ω à 0,1 % → nœud B → dipôle mesuré (plus tard le haut-parleur), au bout du câble du haut-parleur → nœud C → corps du jack casque, **seul retour de masse**. Entrée 1 (XLR) = voie de référence, A–C ; entrée 2 (TRS, LINE) = voie de mesure, B–C. Contrôle à l'ohmmètre **avant** la mise sous tension | câblage conforme au schéma, aucun court-circuit sortie–masse |
      | 1 | Réglages : 48 V, AIR, INST et DIRECT MONITOR éteints ; **sorties ligne arrière débranchées** ; aucun appareil relié à la terre sur le jig ; 15 min de chauffe | voyant 48 V noir, rien d'autre branché |
      | 2 | **Appariement des voies**, fils ouverts, sinus 1 kHz : GAIN 1 au minimum, **GAIN 2 monté d'environ 13 dB** jusqu'à égalité à 1 dB près, **puis bloqué au ruban** | écart ≤ 1 dB (REW abandonne l'étalonnage open au-delà de 2 dB) |
      | 3 | **Trois étalonnages REW, dans l'ordre**, au bout du câble du haut-parleur : **open**, **short**, puis **reference** sur la **seconde 100 Ω à 0,1 %** (valeur certifiée saisie) ; fichier sauvegardé | les trois acceptés par REW |
      | 4 | **Validation** sur la **10 Ω** (A2) puis sur le **100 µF** (A3) — **jamais sur la résistance de référence** | selon les critères de A2 et A3 : 10 Ω plate à sa valeur de A1, phase nulle ; 100 µF en $1/\omega C$ (159 à 15,9 Ω sur 10–100 Hz), phase −90° |
      | 5 | Résistance connue jusqu'à 10 Hz (A5, la 10 Ω) : où la chaîne s'arrête en bas du spectre | bande basse exploitable écrite |
      | 6 | **En fin de séance, relire la 100 Ω de référence** | écart noté au cahier ; repère : 0,23 % d'écart trahit 0,01 dB de dérive de la voie 2, soit 0,19 % au pic de 64 Ω (calcul) |
      *Premier essai à −40 dBFS*, puis premier balayage à $V_A = 0{,}30$ V fils
      ouverts. *Signal d'erreur à connaître* : voies permutées → courbes décalées
      vers le haut d'environ +100 Ω. Toute rotation d'un GAIN, tout changement de
      cordon ou de fréquence d'échantillonnage oblige à refaire les trois
      étalonnages.
      *Durée : 3 h la première fois (dont ~1 h de soudure des trois fiches et
      15 min de chauffe), 45 min à chaque séance ensuite (chauffe, étalonnages,
      validation, relecture) — estimations.*
      *Bloqué par :* 1-B4 (les deux 100 Ω, la 33 Ω, la 10 Ω, les fiches),
      `T-A2`/`T-A3` (check-list de séance). *Débloque :* avec `1-D2`, le verdict de
      la porte (`1-D4`, recoupement des deux chaînes en A7), puis `1-E2` à `1-E4`.
      *Fini quand :* les trois étalonnages sont sauvegardés, les deux validations
      et la relecture de fin de séance sont au cahier avec leurs valeurs — pas
      quand elles sont « bonnes » : le verdict, c'est `1-D4`.

- [ ] **1-D3. Saisir les relevés au format CSV attendu par le dépôt** (une ligne
      d'en-tête commentée par métadonnée : date, dipôle, montage, $R_{ref}$
      nominale et mesurée, niveau, température, opérateur, appareil ; puis les
      colonnes `f_Hz, V_dipole_V, V_Rref_V, dt_s`). Un exemple complet est dans
      `analyse/mesures/exemple_synthetique_sub.csv` : **copier son en-tête et
      remplacer les valeurs**.
      Pour le jig carte son (`1-D8`), pas de saisie : export texte de REW
      (*File > Export > Export measurement as text*), que lit
      `analyse/io_mesures.py::lire_rew` ; joindre le fichier d'étalonnage REW
      sauvegardé et noter au cahier la valeur certifiée des deux 100 Ω.
      *Durée : 30 min à 1 h si l'export de 1-B2 fonctionne ; 2 à 3 h si saisie
      manuelle.*
      *Fini quand :* le fichier est dans `analyse/mesures/` et que son en-tête ne
      contient plus le mot SYNTHÉTIQUE.

- [ ] **1-D4. (CLAUDE) Dépouiller l'étalonnage et rendre le verdict de la porte** :
      $|Z|$ et phase avec barres d'erreur, écart normalisé point par point, biais
      moyen, pente log-log du condensateur, budget d'incertitude complet avec sa
      composante aléatoire enfin mesurée. Le verdict porte sur les **deux**
      chaînes d'impédance : la chaîne GBF + oscilloscope (`1-D2`) et le jig carte
      son (`1-D8` : validations 10 Ω et 100 µF, relecture de la référence), puis
      leur recoupement (manip A7 du livret).
      *Critères, gelés d'avance :* écart normalisé ≤ 2 sur chaque point ; **biais
      moyen ≤ 3 %** sur la résistance ; dispersion du $C$ déduit ≤ 5 % par
      décade ; pente dans −1,00 ± 0,03.
      *Fini quand :* le verdict est écrit — **franchie** ou **non franchie**.

- [ ] **1-D5. Si la porte n'est pas franchie : diagnostiquer, pas contourner.**
      Causes à passer en revue dans l'ordre : pinces de masse, signal sur trop
      peu de divisions, voies non appariées, sondes ×1 et ×10 mélangées, valeur
      de $R_{ref}$ erronée, contact oxydé, couplage AC, offset de voie. Refaire
      une demi-séance. Côté jig carte son (`1-D8`), en plus : **voies permutées**
      (courbes décalées vers le haut d'environ +100 Ω), GAIN 2 tourné après
      étalonnage, DIRECT MONITOR resté actif, 48 V allumé, sortie arrière encore
      branchée, appareil relié à la terre sur le jig, étalonnage « reference »
      fait sur la mauvaise 100 Ω.
      *Durée : 2 à 4 h supplémentaires.*
      *Critère dégradé, gelé d'avance et donc utilisable sans se renier* : biais
      ≤ **5 %** au lieu de 3 %, dispersion ≤ 8 % par décade. Le prix à payer est
      connu : les incertitudes des paramètres Thiele-Small augmentent d'environ
      70 %, ce qui reste exploitable.
      *Règle absolue :* **on ne branche pas le haut-parleur tant que la chaîne
      n'est pas qualifiée**, même dégradée. Mesurer un objet inconnu avec un
      instrument inconnu ne produit aucune information.

- [ ] **1-D6. Étalonner la chaîne ACOUSTIQUE** — c'est l'étalonnage qui manque à la
      plupart des projets, et il coûte une soirée. Quatre gestes, dans l'ordre
      (§ 07.10) :
      | # | Geste | Détail |
      |---|---|---|
      | 1 | Câblage imposé | micro XLR (alim. fantôme) sur l'**entrée 1** ; sortie gauche → ampli ; **sortie droite → entrée 2** (boucle de retour). Micro et boucle sur la **même interface**, sinon rien de ce qui suit ne tient |
      | 2 | *Preferences > Soundcard* | 48 kHz, « Calibrate soundcard » avec la boucle — **à faire une fois, fichier sauvegardé** ; cocher « Use loopback as timing reference » |
      | 3 | *Preferences > Mic/Meter* | charger le **fichier de calibration du micro**. S'il n'existe pas, l'écrire : le critère ne se lira plus qu'en comparaison, jamais en absolu |
      | 4 | *Check levels* | avant **chaque** session, et réglage du gain d'entrée **avant** de monter au niveau fort, jamais pendant |
      *Même interface que le jig d'impédance, réglages incompatibles* : ici le
      48 V est allumé pour le micro et GAIN 1 est monté ; pour le jig (`1-D8`),
      48 V éteint et GAIN 1 au minimum. **Éteindre le 48 V avant de rebrancher le
      jig, et refaire son appariement de GAIN 2 puis ses trois étalonnages** après
      toute séance acoustique : un GAIN touché invalide l'étalonnage.
      *Durée : 2 h la première fois (dont la recherche du fichier de calibration),
      15 min à chaque session ensuite.*
      *Bloqué par :* 1-B3. *Débloque :* `1-E7`, et tout le bloc `3-E.3`.
      *Fini quand :* le fichier de calibration de la carte son existe et est
      rechargé au démarrage, le fichier micro est chargé (ou son absence est
      écrite), et un balayage d'essai revient avec une phase exploitable — donc
      avec la référence temporelle active.

- [ ] **1-D7. Mesurer $Z_s$, l'impédance de sortie du préampli SX-801.** Méthode :
      tension à vide, puis tension sur une charge connue (10 kΩ puis 1 kΩ), et
      $Z_s$ s'en déduit. Aucun haut-parleur dans le circuit.
      *Durée : 30 min, pendant la séance d'étalonnage électrique.*
      *Débloque :* `3-D2`. La référence technique la marque `[[à mesurer]]` avec
      une conséquence chiffrée : **à 1 kΩ, le passe-bas Sallen-Key descend de
      4,6 % et la voie médium subit 0,39 dB de perte d'insertion** — c'est-à-dire
      un **déséquilibre entre voies** sur la référence censée être immunisée. Si
      $Z_s$ dépasse quelques centaines d'ohms, il faut **insérer un étage tampon**
      en entrée de filtre actif : un AOP, un montage et une demi-journée de plus en
      février. Le savoir en octobre coûte 30 min ; le découvrir en février coûte la
      demi-journée **et** le doute sur toutes les mesures actives déjà faites.
      *Fini quand :* $Z_s$ est chiffrée avec son incertitude, et la phrase « tampon
      nécessaire : oui / non » est écrite.

---

### <a id="1e"></a>1-E. Fin octobre — la première campagne $Z(f)$ réelle

- [ ] **1-E1. Relire les règles de sécurité et les appliquer physiquement** :
      bouchons d'oreilles **obligatoires même au niveau faible** (le § 07.11
      prédit **112 dB SPL en champ proche dès 0,5 W** — calcul fait pour une
      sensibilité **supposée** de 95 dB/2,83 V/m, **non mesurée** : c'est un ordre
      de grandeur, et à ces niveaux la question n'est pas de savoir s'il est juste
      à 3 dB près), personne dans l'axe, pas de tête à
      moins d'un mètre, limiteur de l'ampli enclenché, état de la LED de
      limitation consigné à chaque balayage.
      **Pour les balayages d'impédance au jig carte son (`1-E2` à `1-E4`)**,
      l'ampli n'est pas dans le circuit : haut-parleur **débranché de l'ampli et
      de tout filtre**, **sorties ligne arrière de la Scarlett débranchées** (elles
      portent le même signal que le casque, de quoi pousser l'E-800 à pleine
      puissance), 48 V éteint, DIRECT MONITOR sur OFF. L'ampli et son limiteur ne
      reviennent qu'en `1-E7`.
      *Durée : 15 min, à chaque séance.*
      *Fini quand :* les bouchons sont sur place et la consigne est au journal.

- [ ] **1-E2. Faire un balayage grossier au niveau faible pour repérer les
      accidents** : les **deux pics** ($f_L$ puis $f_H$) et le **creux** entre
      eux, qui donne $f_b$. C'est ce repérage qui dit où resserrer la grille.
      Au jig carte son : étalonnages de `1-D8` refaits **au bout du câble du
      haut-parleur** le jour même (open, short, reference), premier essai à
      −40 dBFS, puis **premier balayage à $V_A = 0{,}30$ V fils ouverts** (au plus
      180 mV aux bornes même pour un pic de 200 Ω — calcul) ; manip B2 du livret.
      *Durée : 45 min.*
      *Bloqué par :* la porte 1-D4. *Débloque :* la grille fine de 1-E3.
      *Fini quand :* trois fréquences approximatives sont notées, et que tu as
      vérifié qu'elles ne contredisent pas grossièrement la prédiction de 1-A6.
      *Point de sécurité :* le premier pic tombe **sous l'accord** ; l'explorer
      est nécessaire, mais **au niveau faible uniquement**, avec contrôle visuel
      du débattement de la membrane. Sous $f_b$, la membrane n'est plus chargée
      par les évents et l'excursion devient maximale. **C'est le seul geste du
      projet qui puisse détruire mécaniquement le haut-parleur.**

- [ ] **1-E3. Mesurer $Z(f)$ du sub en caisse, de 10 Hz à 1 kHz**, grille de
      **1/24 d'octave minimum**, **resserrée à 1/48 autour des deux pics et du
      creux**. Relever $R_e$ en continu (quatre fils si le multimètre le permet)
      **avant et après** le balayage.
      **Niveau d'excitation : 100 à 200 mV (régime petits signaux), et rien
      d'autre.** À ce niveau, la descente à 10 Hz est **obligatoire et sans
      risque** — c'est cette zone qui porte le pic bas $f_L$, et l'excursion
      prédite à 10 Hz sous 150 mV vaut **environ 0,09 mm** (modèle recalculé le
      23/09/2026, § 02.6), **plus de cinquante fois moins que le $X_{max}$ de tout
      18″ de sonorisation**. C'est la formulation de `T-A6` : elle est répétée ici parce que
      c'est ici qu'elle s'exécute, et qu'une règle de sécurité écrite à 1 300 lignes
      du geste n'est pas une règle de sécurité.
      **Au jig carte son** (manip B2 du livret, réglages de `1-D8`) : viser
      **environ 200 mV aux bornes au pic**, soit $V_A \approx 0{,}62$ V fils ouverts
      pour un pic de 64 Ω (valeur **modélisée**, à recaler sur le pic lu en
      `1-E2`) ; courant ≤ 4,5 mA. Balayage long, 4 répétitions moyennées. **En fin
      de séance, relire la 100 Ω de référence** : c'est elle qui dit si GAIN 2 a
      dérivé pendant la campagne.
      *Durée : une demi-journée (3 à 4 h) avec export automatique ; une journée
      sans.*
      *Débloque :* toute la phase 2. *Pourquoi monter jusqu'à 1 kHz :* au-dessus
      du pic motionnel, $|Z|$ remonte en $\omega L_e$, et **c'est cette remontée
      qui identifie $L_e$**. Sans elle, l'ajustement n'a aucune prise sur ce
      paramètre — or $L_e$ commande la charge que voit le passe-haut.
      *Fini quand :* le CSV est complet, en-tête renseigné, et que les deux pics
      **et** le creux sont visiblement résolus (plusieurs points sur chaque
      accident, pas un seul).

- [ ] **1-E4. Mesurer $Z(f)$ du bloc médiums TEL QU'IL EST CÂBLÉ, de 10 Hz à
      2 kHz** — les deux pavillons d'ultra-aigu **restent connectés**.
      **Même niveau qu'en `1-E3` : 100 à 200 mV, régime petits signaux.** À ce
      niveau, la mesure est sans risque pour les pavillons, protégés de surcroît
      par leur condensateur série (**présent**, constat du 16/09/2026 ; valeur
      relevée en `T-A8`). Au jig carte son (manip B3 du livret) : le bloc avec ses pavillons
      présente, **sur le modèle du dépôt** (2 pavillons de 8 Ω avec un condensateur de
      6,8 µF, valeur supposée ; aucune mesure), un pic d'environ **112 Ω vers 77 Hz** ; pour 200 mV au pic, $V_A \approx 0{,}44$ V fils
      ouverts. Même relecture de la référence en fin de séance.
      *Durée : 2 à 3 h.*
      *Pourquoi :* les pavillons sont hors périmètre *acoustique*, mais ils sont
      **dans la charge électrique** que voit le passe-haut, et selon la valeur du
      condensateur qui les protège (3,3 à 10 µF), la branche aiguë — 160 à 480 Ω
      par pavillon, 80 à 241 Ω pour les deux en parallèle — fait passer $|Z|$ du
      bloc de 29,3 Ω à 26,3 – 21,8 Ω à 100 Hz, soit −10 à −26 % (−19 % pour
      6,8 µF ; calculé avec `modele_hp.effet_branche_aigu`, pas mesuré). Les débrancher « parce qu'on n'en parle pas » revient à
      mesurer une charge qui n'existe pas dans le montage.
      *Fini quand :* le CSV est complet et que la valeur du condensateur de
      protection (présent depuis le constat du 16/09/2026) est consignée.

- [ ] **1-E5. (CLAUDE) Dépouiller la campagne** : courbes module et phase avec
      barres d'erreur, lecture de $f_L$, du creux et de $f_H$, calcul du rapport
      **$\max|Z|/\min|Z|$** sur la bande utile, et **confrontation des trois
      voies indépendantes vers $f_b$** (prédiction géométrique de 1-A6, creux
      mesuré, puis plus tard l'ajustement de la phase 2).
      *Fini quand :* les figures sont au gabarit gelé en 1-C1 et que le rapport
      $\max|Z|/\min|Z|$ est un nombre mesuré.

- [ ] **1-E6. Inscrire le rapport $\max|Z|/\min|Z|$ dans la problématique.**
      Jusqu'ici, tous les documents du dépôt écrivent « l'impédance varie
      fortement avec la fréquence », **sans chiffre**, parce qu'aucun chiffre
      n'était mesuré. Ce nombre-là est le premier résultat propre du TIPE et il
      remplace la formule vague partout.
      *Durée : 15 min (Claude fait la répercussion dans les fichiers).*
      *Fini quand :* CLAUDE.md, MCOT.md et la feuille de route portent le chiffre
      mesuré, daté, avec son incertitude.

- [ ] **1-E7. Relever les sensibilités des deux voies en champ proche, AU NIVEAU
      FAIBLE GELÉ EN D3 et selon le protocole du bass-reflex** (§ 07.3 et § 07.6),
      haut-parleurs **nus, sans filtre**.
      **Ce n'est pas un relevé au centre du cône.** Un seul micro au centre de la
      membrane est le protocole de la **caisse close** ; ici le sub est
      bass-reflex à deux évents, donc **trois relevés** — membrane, évent 1,
      évent 2 — à sommer en **pression complexe** avec le poids
      $\sqrt{S_{P,i}/S_D}$, les trois partageant la **même référence temporelle**
      (boucle de retour, `1-D6`). Sous l'accord, c'est l'évent qui rayonne
      l'essentiel et la membrane peut être en opposition de phase : le relevé
      unique donne un $G_{sub}$ **faux**, et ce $G_{sub}$ entre ensuite dans la
      fonction de coût (`2-F3`, `2-G2`) **et** dans la définition même de $f_c$
      (D1). C'est le même protocole qu'en `3-E5`, appliqué ici aux voies nues.
      **Niveau : le niveau faible gelé en D3, uniquement.** La voie médium se
      mesure nue, sans passe-haut : `T-D4` l'interdit au niveau fort, sans
      exception.
      *Durée : 2 h (quatre relevés, repositionnement soigné et consigné).*
      *Bloqué par :* 1-B3 (micro et carte son, micro USB exclu), `1-D6` (chaîne
      acoustique étalonnée), `1-A4` ($S_d$ et $S_p$, qui donnent les poids),
      `1-C4` (le niveau faible gelé).
      *Débloque :* la **phase 3**. La fonction de coût porte sur la somme
      $H_{PB}G_{sub} + p\,H_{PH}G_{méd}$, qui n'a aucun sens sans ces deux
      sensibilités, et la définition même de $f_c$ les fait intervenir. Les
      mesurer en phase 4, comme prévu initialement, serait **trop tard** : on
      optimiserait sur deux voies supposées identiques, puis on découvrirait
      l'écart au moment de valider.
      *Fini quand :* les quatre relevés (membrane, évent 1, évent 2, bloc médiums)
      sont enregistrés séparément, avec la position du micro consignée
      ($\le 0{,}11\,a$ de la surface, au centre), et le niveau vérifié au
      multimètre aux bornes.
      *Reportable :* c'est la seule action de la période qui peut glisser en
      novembre sans rien casser — mais pas au-delà, et pas au-delà de `2-F3`.

- [ ] **1-E8. (CLAUDE) Sommer les trois contributions du sub, calculer l'écart de
      sensibilité $\Delta S$ entre voies, et dire s'il impose un L-pad.**
      $\Delta S = L_{1\text{m,sub}} - L_{1\text{m,méd}}$, lu sur la zone de
      recouvrement **80–125 Hz**, chaque voie ramenée à 1 m par $20\log_{10}(a/2)$.
      *Durée : quelques minutes côté Claude, une fois `1-E7` transmis.*
      *Débloque :* **`2-F6`**. Un 18″ et un bloc médium n'ont **aucune raison**
      d'avoir la même sensibilité. Si l'écart n'est pas traité, la somme des deux
      voies est déséquilibrée et le **critère n° 1 mesure ce déséquilibre plutôt
      que le filtre** — et l'optimiseur, lui, le compensera silencieusement par une
      déformation de filtre.
      *Fini quand :* $\Delta S$ est un nombre daté, avec son incertitude, et la
      phrase « L-pad nécessaire : oui / non, et sur quelle voie » est écrite.

---

### <a id="p1-risques"></a>Ce qui peut déraper, et ce qu'on coupe en premier

| Risque | Signe précurseur | Ce qu'on fait |
|---|---|---|
| L'encadrant ne se trouve pas — **écarté le 16/09/2026 (M. Chevalier)** ; le risque résiduel est le compte SCEI et la fenêtre de juin (`1-A3`) | pas de oui explicite fin septembre | **Priorité absolue, rien d'autre ne compte.** Demander à un deuxième, puis à un troisième. C'est le seul risque qui peut annuler la note. |
| L'oscilloscope n'exporte pas | découvert en 1-B2 | Bascule immédiate sur la variante carte son + REW, décidée en septembre et non au banc. Repli ultime : GBF + oscillo point par point au 1/12 d'octave — lent mais infaillible. |
| La porte d'étalonnage échoue deux fois | biais > 5 % après diagnostic | On change de montage (configuration de masse), pas de critère. Si ça persiste : REW. On ne mesure toujours pas le haut-parleur. |
| Le calendrier scolaire mange octobre | une seule séance de banc tenue | **On reporte `1-E7` (sensibilités) en novembre** — le document le prévoit déjà, c'est la seule action reportable de la période. **`1-E4` ne se coupe pas** : le supprimer, c'est supprimer la charge réelle du passe-haut, donc la moitié du sujet, et rendre invérifiable l'argument « la branche aiguë déplace $\lvert Z\rvert$ du bloc de −10 à −26 % à 100 Hz » (calculé) — on optimiserait le passe-haut sur une charge **supposée**. Si tout s'effondre, on le **dégrade** : grille lâche au **1/12 d'octave sur 40–250 Hz** seulement, et on l'écrit. `1-E3` ($Z(f)$ du sub) se garde coûte que coûte : c'est la clé de voûte. |
| La clé USB des mesures est perdue, ou le cahier disparaît | rien — c'est justement le problème | **Parade préventive, `T-B8`** : les pages du cahier sont photographiées à chaque séance, les CSV bruts versionnés dans le dépôt le soir même. Une clé perdue en mai 2027 est au moins aussi probable qu'un haut-parleur grillé, qui a deux pages de parade ; celle-ci en coûte cinq minutes par séance. |
| Tentation d'acheter les composants du filtre maintenant | « autant s'avancer » | Non. D2 et D6 ne sont pas tranchées ; le choix change la self de 18 à 27 mH et le prix de 41 à 291 € l'unité. Acheter avant de décider, c'est décider en cachette. |
| Tentation de descendre en fréquence au niveau fort | « juste pour voir le premier pic » | Non. Sous l'accord, au niveau fort, le 18″ peut être détruit. Le premier pic se relève **au niveau faible**, avec contrôle visuel. C'est le seul geste irréversible du projet. |

---

### <a id="p1-recap"></a>Récapitulatif

| Bloc | Actions | Temps effectif estimé |
|---|---|---|
| Prérequis transverses | `1-A0` → `T-A1`–`T-A10`, `T-B1`–`T-B2`, `T-D1`, `T-D5`, `T-D11` | ~4 h 30 |
| 1-A — Journal, encadrant, cotes, photos, remontage | 1-A0 à 1-A8 | ~5 h 30 + suivi du journal |
| 1-B — Inventaire, achats, montage de mesure | 1-B1 à 1-B5 | ~3 h 15 + délai de livraison |
| 1-C — Gel des décisions | 1-C1 à 1-C9 | ~4 h 30 |
| 1-D — Étalonnages électrique **et** acoustique | 1-D1 à 1-D8 | **7 h 30 à 12 h** (1-D1 1 h + 1-D2 4 h + 1-D3 0,5 à 3 h + 1-D5 0 à 4 h si reprise) **+ 3 h** de jig carte son (`1-D8`, première fois) **+ 2 h 30** de chaîne acoustique et $Z_s$ |
| 1-E — Campagne $Z(f)$ et sensibilités | 1-E1 à 1-E8 | 2 demi-journées + 2 h — **+ 4 h si l'oscillo n'exporte pas** (1-E3 passe d'une demi-journée à une journée) |

**Total : environ 39 à 45 h de travail effectif si l'export de l'oscilloscope
fonctionne ; 45 à 53 h s'il ne fonctionne pas** (3 h de plus qu'au 16/09/2026 :
le jig carte son, `1-D8`). (L'estimation de 25 à 30 h qui
figurait ici comptait un bloc `1-D` à 4-8 h alors que le détail de ses actions en
donne 7 h 30 à 12 h, et ne comptait ni les prérequis transverses, ni les
étalonnages acoustiques, ni les sensibilités au protocole bass-reflex.)
C'est `1-B2` qui tranche entre
les deux, et c'est pour cela qu'il est un verrou : sans export, la saisie devient
manuelle en `1-D3` (2 à 3 h au lieu de 30 min) et `1-E3` passe d'une demi-journée
à une journée entière. Dans les deux cas, **3 à 4 demi-journées de banc**. Ce sont
des estimations, pas des mesures — et elles ne contiennent aucune heure de cours,
de colle ni de DS.

**Les cinq verrous de la période, dans l'ordre :** l'accord de l'encadrant (1-A2,
**levé le 16/09/2026**) →
les cotes de l'enceinte (1-A4) → l'export des données de l'oscilloscope (1-B2) →
la livraison des étalons (1-B4) → **la porte d'étalonnage (1-D2/1-D4)**. Chacun bloque
tout ce qui suit. Aucun ne prend plus d'une demi-journée.

---

## <a id="p2"></a>PÉRIODE 2 — novembre et décembre 2026

### Ce que cette période fait, et ce qu'elle ne fait pas

Tu entres dans cette période avec des courbes $Z(f)$ mesurées et tu en sors avec
**un filtre choisi, justifié, commandé, et un texte de MCOT prêt à coller dans le
formulaire SCEI**. C'est l'acte 2 (identifier) et l'acte 3 (optimiser) du récit,
plus la seule échéance administrative qui ne se rattrape pas.

Deux choses ne se font **pas** ici : aucune mesure acoustique comparative (c'est
la période 3), et aucun achat avant la porte de validation sur 8 Ω résistif. Si
tu achètes une self avant ce test, tu achètes le résultat d'un bug potentiel.

**Les durées sont des estimations, et ce sont des heures de travail effectif.**
Elles ne contiennent ni colles, ni DS, ni concours blancs, ni les vacances de
Noël. Novembre et décembre de 2e année sont chargés : compte que tu ne caseras
pas plus de 4 à 6 heures de TIPE par semaine en moyenne, et que certaines
semaines seront à zéro. Le total ci-dessous est d'environ **35 à 43 heures pour
toi**, plus ce que fait Claude, étalées sur 9 semaines. À comparer aux **70 à
95 heures de la période 3**, qui tiennent dans une fenêtre plus courte et plus
chargée : c'est la période 2 qui doit absorber tout ce qui peut l'être.

**Le partage du travail.** Thomas apporte les données, les décisions et les
lectures ; Claude fait tourner le code, produit les figures, rédige les
brouillons et vérifie les comptes de mots. Une action marquée *(Claude)* ne se
fait pas sans que tu aies fourni l'entrée qui la précède, et une décision n'est
jamais prise par Claude — c'est la règle du registre `DECISIONS-PHASE-0.md`.

---

### <a id="2a"></a>2-A. Contrôle d'entrée (première semaine de novembre)

Ce bloc dure une demi-heure et évite deux mois de travail sur du sable.

- [ ] **2-A1. Vérifier que les cinq entrées de la période 2 existent vraiment**
      (~20 min). Ouvrir `analyse/mesures/` et cocher : $Z(f)$ du sub en caisse
      sur 10 Hz – 1 kHz ; $Z(f)$ du bloc médiums **câblé complet** (pavillons
      d'ultra-aigu en parallèle connectés) sur 10 Hz – 2 kHz — au besoin dégradé au
      1/12 d'octave sur 40–250 Hz, mais **jamais absent** ; $G_{sub}(f)$
      (membrane + deux évents sommés, `1-E7`) et $G_{méd}(f)$ en champ proche, HP
      nus, avec le $\Delta S$ de `1-E8` ; les cotes des deux évents et le
      volume net de la caisse ; la prédiction datée de $f_b$ écrite **avant** le
      dépouillement. *Débloque* : tout le reste de la période.
      *Fini quand* : les cinq fichiers sont dans le dépôt et versionnés.
      **Si l'un manque, il se remesure maintenant** — pas en décembre. C'est ici
      que se rattrape `1-E7` si octobre l'a emporté : c'est la seule entrée qui
      pouvait glisser, et sa date limite est `2-F3`.
- [ ] **2-A2. Vérifier que la chaîne de calcul tourne encore sur ta machine**
      (~10 min) : `python analyse/tout_refaire.py --rapide --sans-figures` puis
      `python -m unittest discover -s analyse/tests -v`. *Fini quand* : code de
      retour 0 et les 171 tests au vert (compte du 23/09/2026). *Si ça échoue* : c'est un problème
      d'environnement, pas de physique — le régler avant d'y mettre des mesures.
- [ ] **2-A3. Dernier rappel — vérifier que D10 (professeur encadrant) porte une
      date** (~2 min). Ce n'est **pas** une nouvelle démarche : c'est un filet de
      sécurité. Si D10 est rempli, daté et signé dans `DECISIONS-PHASE-0.md`,
      tu coches et tu passes. **Sinon, tu reviens à `1-A2` et `1-A3`, et c'est la
      seule chose que tu fais cette semaine** : sans encadrant déclaré à l'étape 1
      et validé à l'étape 3, la note peut être zéro.
      *Fini quand* : D10 porte une date, ou `1-A2` est rouvert.

---

### <a id="2b"></a>2-B. Lire les sources (novembre, en parallèle — créneaux courts)

Ce bloc **ne dépend de rien** et **bloque la rédaction du MCOT**. C'est celui à
glisser dans les trous d'emploi du temps : une référence par soirée. Il démarre
en novembre parce que deux sources se commandent et n'arrivent pas le jour même.

La bibliographie commentée pèse **650 mots sur les 900 du MCOT, soit 72 %**.
C'est la rubrique où le jury lit ton appropriation du contexte, et le brouillon
actuel n'en utilise que ~124. On ne remplit pas 650 mots avec des titres : il
faut une synthèse rédigée où chaque référence est appelée par [1], [2]… et
commentée par **ce qu'on lui emprunte et pourquoi elle ne suffit pas**.

- [ ] **2-B1. Lancer les demandes au CDI dès la première semaine** (~30 min).
      Thiele 1971 (« Loudspeakers in Vented Boxes », *JAES* 19-5 et 19-6) et
      Small 1972 sont des articles AES ; les scans accessibles en ligne sont des
      images sans couche texte. Demander aussi l'édition papier de Dickason,
      *The Loudspeaker Design Cookbook* (7ᵉ éd., pour vérifier la constante de la
      formule de longueur d'évent et ses unités). *Débloque* : les commentaires
      des références [2] et [4]. *Fini quand* : les demandes sont déposées, avec
      une date de réponse annoncée. *Repli si refus ou délai* : s'appuyer sur
      Mateljan & Sikora 2012, en accès libre (voir ci-dessous).
- [ ] **2-B2. Lire Mateljan & Sikora 2012, « Estimation of Loudspeaker Driver
      Parameters »** (~1 h 30, PDF libre : artalabs.hr). *Pourquoi celle-là
      d'abord* : c'est **exactement** ta méthode — moindres carrés non linéaires
      Levenberg-Marquardt sur l'impédance mesurée, initialisation
      semi-analytique, comparaison de modèles de bobine à pertes. Tu peux donc
      écrire honnêtement « la méthode de la phase 2 est celle de [x], que j'ai
      réimplémentée ». *Fini quand* : tu sais dire en trois phrases ce qu'elle
      fait, et ce qu'elle ne fait pas (elle ne traite pas le filtre).
- [ ] **2-B3. Lire Thiele 1971 en diagonale ciblée** (~2 h, dès réception). Ne pas
      tout lire : chercher le circuit équivalent de la caisse à évent, l'origine
      des **deux pics** et la place de $f_b$ et $Q_l$. *Débloque* : le commentaire
      de [2], qui est la référence structurante de ton sujet puisque ta caisse
      **est** le *vented box* de 1971. *Fini quand* : tu peux dire ce que le
      papier apporte et pourquoi il ne suffit pas (il ne dit rien du filtre sur
      charge réelle, ni de l'optimisation sous contraintes).
- [ ] **2-B4. Lire Wheeler 1928 et le § 05 de `REFERENCE-TECHNIQUE.md`** (~1 h).
      Formules géométrie ↔ inductance, et la loi d'échelle $m \propto L^{3/2}$ à
      DCR imposée, qui est **l'argument sobriété le plus direct du sujet**.
      *Débloque* : le commentaire de [3] et le bloc 2-G (self).
      *Fini quand* : tu sais expliquer pourquoi passer de $-2{,}8$ dB à
      $-0{,}5$ dB d'insertion coûte 14 fois plus de cuivre.
- [ ] **2-B5. Récupérer les datasheets réelles du sub 18″ et des médiums** (~45 min,
      recherche + archivage PDF dans `assets/`). *Débloque* : le critère de
      plausibilité physique n° 6 du § 03.7 (comparer $f_s$, $Q_{ms}$, $Q_{es}$
      identifiés aux ordres de grandeur constructeur) **et** la référence [6].
      *Fini quand* : les PDF sont dans le dépôt avec leur URL et leur date de
      consultation. *Si introuvable* : le dire — « datasheet non disponible pour
      ce modèle » est une information, pas un échec, et se dit à l'oral.
- [ ] **2-B6. Trancher le sort de la référence [5] (REW + scipy)** (~15 min de
      réflexion). Les références sont limitées à 2–10 et doivent être
      « scientifiquement fiables » : une doc logicielle consomme un emplacement.
      Deux issues au choix — (a) rendre la place et citer REW et scipy dans le
      texte comme *outillage*, (b) la garder en disant précisément ce qu'on lui
      emprunte. *Fini quand* : le choix est écrit dans `MCOT.md`.
      *C'est ton arbitrage, pas celui de Claude.*
- [ ] **2-B7. (Claude) Rédiger les fiches de lecture à partir de tes notes** (~1 h de
      travail de Claude, après que tu aies lu). Pour chaque référence : 2 à 4
      phrases disant ce que le projet lui emprunte et où elle s'arrête.
      *Fini quand* : six à huit fiches existent, chacune sous 90 mots.
      **Claude ne peut pas écrire ces fiches à ta place sans tes notes** : une
      bibliographie commentée sur des résumés de seconde main s'entend
      immédiatement à l'oral, et c'est exactement ce que l'entretien va sonder.

---

### <a id="2c"></a>2-C. Ajuster le modèle bass-reflex (novembre, semaines 1 et 2)

C'est l'acte 2. La caisse est bass-reflex à deux évents : le modèle par défaut
est `Z_bassreflex8`, huit paramètres ($R_e$, $L_e$, $R_{es}$, $f_s$, $Q_{ms}$,
$\alpha$, $f_b$, $Q_l$), et **pas** les cinq de la caisse close.

- [ ] **2-C1. Faire tourner le diagnostic de caisse sur tes vraies courbes** (~20 min).
      `io_mesures.diagnostiquer_caisse()` compte les maxima locaux de $|Z|$ entre
      10 et 100 Hz sur la courbe **lissée sur 3 points** (le lissage n'est pas
      cosmétique : sur la courbe brute le bruit fabrique des maxima parasites).
      Critère : $\ge 2$ maxima → bass-reflex. *Débloque* : le choix du modèle.
      *Fini quand* : le diagnostic est exécuté et son verdict consigné, avec le
      nombre de pics trouvés. *Si le diagnostic ne voit qu'un pic alors que la
      caisse est bass-reflex* : ta grille de fréquences est trop lâche, ou tu
      n'es pas descendu assez bas — c'est un problème de mesure, retour phase 1.
- [ ] **2-C2. Vérifier D8 dans `DECISIONS-PHASE-0.md`** (~5 min) : D8 est **déjà
      remplie** depuis le 16/09/2026 (type = bass-reflex à deux évents, modèle à
      7-8 paramètres). Il reste à contrôler que `criteres_geles.json` porte les
      mêmes champs ($n$ paramètres du fit = 8).
      *Débloque* : le code refuse d'ajuster 5 paramètres sur une courbe à deux
      pics tant que ce champ n'est pas cohérent. *Fini quand* :
      `criteres_geles.json` est cohérent avec D8.
- [ ] **2-C3. Lancer l'ajustement à 8 paramètres, avec une seule perte globale**
      (~1 h avec les allers-retours). Commencer par **une** perte et n'en ajouter
      une seconde que si le résidu structuré dépasse **0,62 dB RMS** (seuil du
      § 01.10, établi sur un cas où $Q_p$ et $Q_l$ étaient réellement distincts).
      *Fini quand* : le fit converge et `resultats/parametres_ts.json` porte les
      huit valeurs avec leurs incertitudes.
- [ ] **2-C4. Exécuter le multi-départ (50 tirages) et vérifier l'unicité du minimum**
      (~20 min, machine). Le meilleur coût doit être atteint par une nette
      majorité des départs ; un minimum concurrent s'écarte par son $\chi^2$
      (facteur $10^3$ attendu), **jamais par préférence**.
      *Fini quand* : le taux de convergence vers le minimum global est chiffré et
      noté. *C'est une question quasi certaine du jury* : « comment savez-vous
      que c'est le bon minimum ? ».
- [ ] **2-C5. Produire le contre-exemple : ajuster le modèle à 5 paramètres sur les
      mêmes données** (~30 min). Il va **converger en silence** sur des
      paramètres faux — pas d'erreur, juste un résidu un peu moins bon — et le
      test des séquences de Wald-Wolfowitz le trahira ($z \approx -5{,}4$ pour un
      bass-reflex ajusté par le modèle clos, contre $z \approx +0{,}4$ pour le bon
      modèle). *Débloque* : une des meilleures planches de l'oral — « ça a
      convergé » ne veut pas dire « c'est juste ». *Fini quand* : les deux fits
      sont tracés côte à côte avec leurs résidus et leurs $z$.
- [ ] **2-C6. Exécuter le contrôle « évent inerte »** (~20 min). Faire tendre
      l'impédance de la branche d'évent vers l'infini doit redonner **exactement**
      la caisse close de même volume. *Fini quand* : l'écart est chiffré et
      quasi nul. *Ce que ça prouve* : le modèle à 8 paramètres englobe bien celui
      à 5 — c'est ce qui autorise à parler de « paramètres en plus » et non de
      « deux modèles rivaux ». *Piège à ne pas se faire tendre* : un évent
      physiquement bouché ajoute en plus son propre volume à $V_b$.
- [ ] **2-C7. (Claude) Produire la figure d'identification à trois panneaux, gabarit
      4/3** : $|Z|$ mesuré avec barres d'erreur + modèle + bande $\pm 2u$,
      $\varphi$, résidus normalisés. *Fini quand* : la figure est lisible une fois
      réduite à la taille d'une diapo 1024×768 — le panneau des résidus est celui
      qui casse en premier ; si besoin, le basculer en annexe.

---

### <a id="2d"></a>2-D. Le contrôle croisé de $f_b$ par trois voies (novembre, semaine 3)

C'est le plus beau contrôle du projet et il coûte une heure. Trois chemins
indépendants vers la même grandeur, dont **deux ne passent pas par
l'ajustement** : si les trois s'accordent, le modèle de caisse est validé
indépendamment ; si la géométrie et le creux s'accordent mais pas le fit, c'est
le fit qui est en cause.

- [ ] **2-D1. (Claude) Calculer le $f_b$ prédit par la géométrie, sous forme
      d'intervalle** (~30 min de travail de Claude, à partir de tes cotes).
      $f_b = \frac{c}{2\pi}\sqrt{N S_p/(V_b \ell_{\text{eff}})}$, résonateur de
      Helmholtz à $N = 2$ masses d'air en parallèle. Convention retenue :
      $k_a = 1{,}463$ (un bout bridé, un bout libre), encadrement transporté
      $k_a \in [1{,}227\,;1{,}698]$. *Fini quand* : la prédiction est écrite
      **comme un intervalle**, jamais comme un nombre unique — l'incertitude de
      convention (~3 %) dépasse l'incertitude de mesure (~1,5 %), et le dire est
      un point d'honnêteté que le jury attend.
      *Attention* : $V_b$ est le volume **net** — brut moins les saladiers, les
      renforts et les tubes d'évent eux-mêmes. C'est la grandeur la plus facile à
      surestimer sur une caisse DIY, et c'est elle qui domine l'incertitude.
- [ ] **2-D2. Lire $f_b$ directement sur la mesure, au passage par zéro de la phase
      entre les deux pics** (~15 min) — pas à l'argmin du creux, plat et
      indiscernable sous 1 % de bruit (§ 02.6). Lecture directe, sans modèle. *Biais connu à annoncer* : le creux n'est pas
      exactement à $f_b$ quand il y a des pertes — sur le modèle de référence, le
      minimum tombe 2,3 % sous $f_b$ et le passage par zéro de la phase 4,3 %
      sous. *Fini quand* : la valeur lue est notée **avec** ce biais annoncé.
- [ ] **2-D3. Confronter les trois valeurs et trancher** (~30 min, avec Claude pour le
      calcul). Géométrie / lecture directe / ajustement. *Fini quand* : l'écart
      entre $f_b$ ajusté et $f_b$ lu sur la mesure est chiffré et comparé au seuil que tu
      dois **geler maintenant** avec les incertitudes de la phase 1 (le champ
      `[[à geler]]` de la porte de validation de la phase 2).
      *Si les trois divergent de plus de ~5 %* : ne pas avancer. Diagnostiquer
      dans cet ordre — volume net surestimé, puis évents non identiques
      (la formule suppose $N$ évents identiques, sinon remplacer $N S_p /
      \ell_{\text{eff}}$ par $\sum_i S_{p,i}/\ell_{\text{eff},i}$), puis bande
      d'ajustement.
- [ ] **2-D4. Écrire la page « boucle fermée » du cahier** (~30 min). Prédiction datée
      *avant* mesure, mesure, ajustement, écart, explication de l'écart.
      *Fini quand* : la page est datée et signée. *Pourquoi ça compte* : une
      prédiction consignée après coup n'est plus une prédiction, et c'est
      invisible dans un rapport — d'où la date.

---

### <a id="2e"></a>2-E. Incertitudes et porte de validation de l'identification (fin novembre)

La phase 3 ne repart pas de huit incertitudes indépendantes : elle reçoit la
**covariance complète**. C'est tout l'objet de ce bloc.

- [ ] **2-E1. Passer les huit critères de validation du § 03.7 un par un** (~1 h 30).
      $\chi^2$ réduit dans [0,5 ; 2] ; résidu RMS du même ordre que l'incertitude
      de chaîne sur 20–300 Hz ; test des séquences $|z| < 3$ séparément sur
      module et phase ; stabilité sous retrait de 20 % des points (200 tirages) ;
      concordance covariance / Monte-Carlo / jackknife à un facteur 1,5 ;
      plausibilité physique contre datasheet ; test à blanc sur les dipôles
      connus de l'étalonnage ; unicité du minimum.
      *Fini quand* : un tableau à huit lignes dit « passé / échoué » avec le
      chiffre obtenu en face de chacun. *Règle absolue* : si $s^2$ sort de
      [0,5 ; 2], **on diagnostique — on n'ajuste pas les $u$ pour que ça passe**.
- [ ] **2-E2. Séparer les incertitudes de type A et de type B** (~45 min, avec Claude).
      Le point à comprendre et à savoir dire : une erreur sur $R_{ref}$ décale
      $R_e$, $R_{es}$ et $L_e$ du même pourcentage **sans que le $\chi^2$ bouge**,
      tandis que $f_s$ et $Q_{ms}$ y sont immunisés. Les trois estimateurs
      (covariance, Monte-Carlo, jackknife) ne voient que l'aléatoire.
      *Fini quand* : le budget d'incertitude distingue les deux colonnes.
- [ ] **2-E3. (Claude) Écrire les livrables formels pour l'acte 3** : `ts_theta.csv`
      ($\hat\theta$ et $u$), `ts_cov.csv` (la matrice complète) et `ts_mc.csv`
      (les tirages Monte-Carlo). *Débloque* : la propagation des incertitudes
      jusqu'au filtre optimisé. *Fini quand* : les trois fichiers existent et
      sont lus par le code d'optimisation.
- [ ] **2-E4. Franchir (ou non) la porte de validation de la phase 2** (~15 min de
      décision). *Fini quand* : la porte est cochée et datée — résidu faible sur
      20–300 Hz, paramètres stables sous retrait de points, **et** $f_b$ ajusté
      cohérent avec $f_b$ lu sur la mesure. *Si la porte ne passe pas* : le repli
      documenté est `Z_deux_pics`, modèle phénoménologique à 8 paramètres qui
      décrit les deux pics sans prétendre nommer $f_b$ et $Q_l$. Il suffit pour
      l'acte 3 (qui ne voit que $Z(f)$) mais **il coupe la boucle de validation
      géométrique** : c'est un vrai coût narratif, à assumer explicitement si tu
      y viens.

---

### <a id="2f"></a>2-F. Geler ce qui entre dans la fonction de coût (fin novembre)

Trois décisions, et elles doivent être prises **avant** de lancer l'optimisation,
pas après en avoir vu le résultat. Changer une pondération une fois les courbes
tracées, c'est choisir le vainqueur puis écrire le règlement — la seule faute
réellement disqualifiante de ce projet.

- [ ] **2-F1. Trancher D2 : la cible de sommation** (~1 h de réflexion, la décision la
      plus lourde de la période). Reportée le 13/09/2026 « après la phase 1 » :
      l'échéance est **maintenant**, avant le premier achat et avant le MCOT.
      Deux options incompatibles :

      | | Butterworth 2 ($Q = 1/\sqrt2$) | LR2 / somme plate ($Q = 1/2$) |
      |---|---|---|
      | Sur 8 Ω, continu | 18,006 mH / 140,67 µF | 25,465 mH / 99,47 µF |
      | Sur 8 Ω, E12 | 18 mH / 150 µF, $J = 0{,}947$ | 27 mH / 100 µF, $J = 0{,}826$ |
      | Somme après inversion de polarité | **+3,01 dB à $f_c$** (signature, pas défaut) | **0,000 dB partout**, phase nulle partout |
      | Écart RMS d'un filtre parfait à une cible plate | 2,29 dB | 0 |
      | Cuivre, à DCR imposée | référence | **+84 %** par self ($m \propto L^{3/2}$) |
      | Couple de selfs, fil seul, $r_{max} = 2{,}0$ Ω | ~75 € | ~138 € |
      | Couple de selfs, fil seul, $r_{max} = 1{,}5$ Ω | ~116 € | ~213 € |

      **Lecture des deux dernières lignes.** Ces quatre montants dérivent tous
      d'une base de **25 €/kg de cuivre émaillé qui n'est pas sourcée** : ils lui
      sont **strictement proportionnels**. Ce sont donc des **rapports** fiables
      (LR2 coûte 84 % de plus que Butterworth, quel que soit le prix du kilo) et
      des **valeurs absolues fragiles**. Si les devis de `1-C6` sont rentrés, ce
      sont eux qui font foi ici, et Claude recalcule la colonne ; sinon, la
      décision se prend sur les rapports, et on l'écrit.

      *Ce que la décision entraîne mécaniquement* : la cible du critère
      « fidélité » **et** la cible par défaut du code sont la même, et le sanity
      check 8 Ω change de cible attendue. *Fini quand* : D2 est rempli, daté,
      signé, avec un motif d'une phrase qui **ne soit pas un résultat**, et
      `criteres_geles.json` mis à jour. *Argument nouveau depuis le 16/09* : ta
      charge réelle a deux pics dont le haut tombe près de 100 Hz — la robustesse
      de phase de LR2 y gagne en valeur, mais le budget cuivre s'alourdit
      d'autant. C'est ton arbitrage.
- [ ] **2-F2. Trancher D6 : $r_{max}$ de la self et le modèle de DCR/prix** (~30 min).
      Fenêtre praticable 1,5 à 2,0 Ω ; recommandation du registre : **2,0 Ω avec
      $J \le 3$ A/mm²** (fil ~1,24 mm, bobinable à la main, dérive de DCR +3,6 %
      en une minute, sous l'effet thermique du HP lui-même). Passer à 1,5 Ω coûte
      ~41 € de plus par couple pour gagner 0,45 dB d'insertion.
      **Choisir aussi UN modèle de DCR/prix** (A : masse fixée, $r \propto L$ ;
      B : DCR fixée, prix $\propto L$ ; C : fil fixé, $r$ et prix en $\sqrt L$) :
      les placeholders du brouillon pénalisent **deux fois** le cuivre.
      **Et écrire ici le nombre de selfs à bobiner** : 4 pour deux filtres
      complets, 2 avec des **prises intermédiaires** (une seule bobine par voie,
      qui fournit la valeur catalogue *et* la valeur optimisée).
      *Conséquence à assumer si tu choisis les prises intermédiaires* : deux des
      huit critères gelés en D4 **cessent d'être mesurables et deviennent
      calculés**. Le critère n° 7 « encombrement / matière » se mesure à la
      balance — une balance ne sait pas séparer deux filtres qui partagent une
      bobine ; le critère n° 5 « coût marginal » se mesure sur factures — une
      facture ne se coupe pas en deux. Il faut alors **calculer** la masse et le
      prix de la **fraction de bobine réellement utilisée** par chaque design,
      avec une méthode écrite **avant** de basculer, et le dire à l'oral. Ce n'est
      pas rédhibitoire ; c'est un coût, et il doit être inscrit au registre au
      moment du choix, pas découvert en mars.
      *Bloque* : le terme « euros » et le terme « pertes » de la fonction de coût,
      **et la commande de `2-I3`**.
      *Fini quand* : $r_{max}$, $J_{max}$, le modèle, le nombre de selfs et — le
      cas échéant — la méthode de calcul des critères n° 5 et n° 7 sont écrits et
      datés.
- [ ] **2-F3. Trancher D5 : bande et pondérations de $J$** (~45 min). Recommandation
      A3 du registre : plancher dur sur $C_1$, bande **40–1600 Hz** pour le seul
      terme de forme de la voie sub, **40–250 Hz** pour le terme de somme ;
      poids $w_s = 1$, $w_v = 1$, $w_€ = 0{,}04$ dB/€, $w_W = 1$ dB/W à
      $P_{ref} = 10$ W ; $w_\varphi$ **recalibré sur le $\tau$ mesuré** au mètre
      ruban entre le centre du 18″ et celui du bloc médiums (défaut 0,018 dB/°
      pour 0,50 m) ; protection des médiums rendue **unilatérale** sous leur
      $f_s$. *Pourquoi l'unilatéral* : le RMS en dB est à deux côtés et pénalise
      autant « protège trop » que « protège pas assez » — sur l'exemple de
      référence, un design est pénalisé de 5,4 dB pour **mieux** protéger les
      médiums que la cible. Une métrique qui met ces deux cas sur le même plan ne
      peut pas porter la raison d'être d'un raccord.
      *Fini quand* : les champs de D5 sont remplis, datés, et l'hypothèse « bruit
      rose » est **énoncée par écrit** (elle sera redemandée à l'oral).
- [ ] **2-F4. Confirmer $\tau$ au mètre ruban** (~5 min, à ne pas oublier). Distance
      entre le centre du 18″ et celui du bloc médiums — elle a déjà été relevée en
      `1-A4` ; il s'agit ici de la **relire et de la confirmer**, parce que c'est
      elle qui recalibre $w_\varphi$ et qu'une erreur de 10 cm s'y voit.
      *Bloque* : le recalibrage de $w_\varphi$ de `2-F3` — **et rien d'autre, ni
      plus tard** : `3-D4` n'y revient pas.
      *Fini quand* : la valeur est notée en mètres, et l'écart à celle de `1-A4`
      est nul ou expliqué.

- [ ] **2-F6. Décider comment l'écart de sensibilité $\Delta S$ est traité — et
      l'inscrire dans le modèle de l'optimiseur** (~45 min, avec Claude).
      Entrée : le $\Delta S$ chiffré en `1-E8`, et la règle de réglage de l'actif
      gelée en `1-C8`. Trois issues, à trancher
      explicitement (§ 07.6) :
      (a) **L-pad** ($R_1$ série + $R_2$ parallèle) sur la voie la plus sensible —
      a priori les médiums ; (b) gain relatif laissé en **variable de conception**
      de l'optimiseur ; (c) $\Delta S$ jugé négligeable devant le seuil de
      départage du critère n° 1, et on l'écrit.
      *Pourquoi ce n'est pas une retouche de fin de projet* : un L-pad **modifie la
      charge que voit le filtre** — il aplatit même fortement $\lvert Z\rvert$ vue
      par le passe-haut, au prix de pertes. C'est donc **un degré de liberté de
      l'optimisation, pas un réglage** : 6 dB d'atténuation achètent un facteur 5
      sur l'excursion d'impédance contre 75 % de la puissance de la voie. Laissé
      hors du modèle, l'écart de sensibilité sera compensé **silencieusement par
      une déformation de filtre**, et le critère n° 1 mesurera le déséquilibre
      entre voies au lieu de mesurer le filtre.
      *Bloque* : `2-G2` (l'énumération E12 doit énumérer le bon problème) et la
      ligne « résistances de L-pad » de `2-I1`.
      *Fini quand* : (a), (b) ou (c) est écrit, daté, signé, avec les valeurs de
      $R_1$ et $R_2$ si c'est (a), et `criteres_geles.json` en porte la trace.
- [ ] **2-F5. (Claude) Reporter D2, D5, D6 dans `criteres_geles.json` et relancer les
      tests** (~30 min de travail de Claude). *Fini quand* : plus aucune marque
      `[[a geler]]` dans les sections D2, D5, D6, et les 171 tests toujours au
      vert. *Rappel du mécanisme* : tant qu'un champ porte `[[a geler]]`, le code
      **refuse** de s'en servir pour produire un chiffre d'oral. Ce n'est pas une
      formalité, c'est ce qui rend vérifiable l'affirmation « les critères ont
      été gelés avant les mesures ».

---

### <a id="2g"></a>2-G. L'optimisation sur la charge mesurée (décembre, semaines 1 et 2)

- [ ] **2-G1. Faire passer la porte de validation sur 8 Ω résistif — AVANT tout le
      reste** (~30 min). Alimenté d'une charge purement résistive de 8 Ω,
      l'optimiseur continu **doit** retomber sur le second ordre analytique :
      18,006 mH / 140,674 µF en Butterworth, 25,465 mH / 99,472 µF en LR2, à
      $10^{-6}$ près. C'est un **théorème**, pas une tendance.
      *Fini quand* : `sanity_check_continu` et `sanity_check_e12` passent pour la
      cible gelée en D2. **Si ce test échoue, c'est un bug, et on n'achète
      rien** — c'est écrit noir sur blanc dans la feuille de route, et c'est la
      protection la plus utile de tout le projet.
- [ ] **2-G2. Lancer l'énumération exhaustive E12 sur ta charge $Z(f)$ mesurée**
      (~1 h dont l'essentiel en temps machine). 24 valeurs par série, 576 couples
      par voie, **331 776 combinaisons** — l'espace est fini, donc énumérable :
      pas d'optimum local possible, et c'est un argument fort à l'oral.
      *Fini quand* : `resultats/design_optimise.json` porte le classement et le
      gagnant, avec l'étiquette de provenance des mesures.
- [ ] **2-G3. Vérifier que l'optimum n'est pas au bord de la grille** (~15 min).
      `verifier_optimum_interieur()`. *Si l'optimum est au bord*, la grille est
      trop étroite et le « gagnant » est un artefact de cadrage.
      *Fini quand* : le contrôle est exécuté et son résultat noté.
- [ ] **2-G4. Analyser le plateau** (~30 min). Combien de designs sont à moins de 1 %
      du meilleur $J$ ? *Pourquoi c'est important* : si trente designs se tiennent
      dans 1 %, annoncer « le » design optimal est une sur-interprétation, et il
      faut choisir dans le plateau selon un critère secondaire (prix, dispo,
      encombrement) **en le disant**. *Fini quand* : la taille du plateau est
      chiffrée et la règle de départage écrite.
- [ ] **2-G5. Faire le Monte-Carlo des tolérances** (~30 min). Composants à
      $L \pm 10$ %, $C \pm 20$ % : où atterrit vraiment $f_c$ ? Rappel de la
      formule qui fait foi, $u(f_0)/f_0 = \frac12\sqrt{(u_L/L)^2 + (u_C/C)^2}$ —
      le facteur ½ vient de $f_0 \propto (LC)^{-1/2}$. Pour ±10 %/±10 % :
      **7,07 % en borne au pire cas, 4,08 % en incertitude-type GUM**.
      **Toujours écrire le couple, jamais un nombre seul** — les deux ne se
      comparent pas aux mêmes seuils. *Fini quand* : la dispersion de $f_c$ du
      design retenu est chiffrée. *Ne jamais reprendre le « ±11 % »* qui traîne
      dans les supports v1 : c'est la formule d'un RC du 1er ordre abandonné.
- [ ] **2-G6. Recouper par l'optimiseur continu puis arrondi** (~20 min). Deux méthodes
      indépendantes qui tombent sur le même design, c'est une vérification ; si
      elles divergent, c'est le passage à E12 (une projection sur grille) qui
      l'explique, pas un bug — mais il faut le dire.
      *Fini quand* : les deux résultats sont côte à côte.
- [ ] **2-G7. Contre-vérifier le design retenu sous LTspice** (~45 min). Les netlists
      sont exportées par le code (`filtre_optimise.cir`, `filtre_catalogue.cir`).
      *Pourquoi* : un simulateur tiers qui retrouve ta courbe ferme la porte à
      l'objection « votre code se vérifie lui-même ».
      *Fini quand* : les Bode LTspice et Python se superposent.
- [ ] **2-G8. (Claude) Produire la figure « catalogue vs optimisé sur $Z(f)$ réelle »**
      en gabarit 4/3. C'est **la** figure du sujet : elle montre l'écart entre ce
      que promet la formule catalogue sur 8 Ω et ce qu'elle fait sur la vraie
      charge. *Fini quand* : la figure existe, est injectée dans les diapos et
      porte l'étiquette de provenance des mesures.

---

### <a id="2h"></a>2-H. La self : du modèle au plan de bobinage (décembre, semaine 2)

- [ ] **2-H1. Faire tourner l'étude de bobine sur la valeur de $L$ retenue** (~45 min,
      avec Claude). Wheeler, redécouverte numérique de la bobine de Brooks, choix
      du fil, masse de cuivre, DCR, prix, échauffement.
      *Fini quand* : pour la valeur de $L$ du design gagnant, tu as un couple
      (diamètre de fil, nombre de tours) qui respecte $r_{max}$ et $J_{max}$.
- [ ] **2-H2. Décider air ou noyau, et assumer la thèse** (~20 min). À 18 mH, une self
      à noyau est **moins chère et moins résistive** qu'un bobinage à air fait
      maison. On bobine à air pour (a) la **linéarité** — pas de $L(I)$, pas de
      dérive de $f_0$ avec le niveau, ce qui est exactement ton critère de
      robustesse, (b) la **maîtrise métrologique** — $N$, $\ell$, $m$, $r$ tous
      mesurables, (c) la **liberté de valeur**. *Ne pas prétendre que l'argument
      est économique* : le jury le démontera en trente secondes.
      *Fini quand* : la décision et ses trois motifs sont écrits.
- [ ] **2-H3. Écrire le plan de bobinage** (~30 min) : diamètre du mandrin, nombre de
      tours, longueur de fil, masse attendue, DCR attendue, $L$ attendue.
      *Débloque* : la commande de fil, et la vérification de la période 3
      (mesurer $L$ par résonance série avec un $C$ connu — avec 150 µF, pic
      attendu vers 97 Hz au GBF). *Fini quand* : le plan tient sur une page et
      chaque nombre a sa formule en face.

---

### <a id="2i"></a>2-I. Acheter — et seulement maintenant (mi-décembre)

- [ ] **2-I1. Établir la liste d'achats à partir du design gelé** (~45 min).
      Fil de cuivre émaillé au diamètre du plan de bobinage — **au prix réel des
      devis de `1-C6`, pas à 25 €/kg**, et si le diamètre calculé n'est pas vendu
      au détail, on prend le voisin et on **recalcule $r$ avant de commander** —
      mandrins, cosses, bornier, **les résistances du L-pad si `2-F6` a retenu
      l'option (a)** (valeurs $R_1$, $R_2$, et surtout la **puissance** : un L-pad
      dissipe une fraction franche de la voie), et les condensateurs. Prévoir
      **les composants du filtre catalogue aussi** : la comparaison l'exige.
      **Condensateurs — la contrainte qui décide de l'achat, et qu'on ne rattrape
      pas après** : valeurs E12 du design, tolérance **±10–20 %** (le Monte-Carlo
      de `2-G5` dit ce que ça coûte), et surtout **250 V DC / 160 V AC minimum**.
      Ce n'est pas de la marge de confort : le réseau LC **surtensionne** le
      composant shunt d'un facteur qui suit $\lvert Z\rvert$ de la charge (×2,8 à
      30 Ω, ×4,6 à 50 Ω, **×5,5 à 60 Ω** sur 18 mH/150 µF), et à 20 V RMS d'entrée
      sur un pic à 50 Ω cela fait **92 V RMS, soit 130 V crête** aux bornes du
      condensateur. Tant que la surtension réelle n'est pas confirmée sur ta
      $Z(f)$ mesurée : **marge ×6**. Et **vérifier que la spécification lue est la
      tenue alternative permanente** — sur un MKP, un « 100 V » est presque
      toujours du continu, l'alternatif permanent tournant autour de 60–65 V RMS.
      Les « 100 V » hérités de la v1 sont **insuffisants**. Détail du calcul et
      motif : `T-A9`.
      *Bloqué par* : la porte 8 Ω franchie, D2 et D6 gelés, `2-F6`, le plan de
      bobinage.
      *Fini quand* : la liste est chiffrée, fournisseur par fournisseur, et
      **chaque référence de condensateur porte sa tension AC permanente**, pas
      seulement sa capacité.
- [ ] **2-I2. Vérifier le budget cumulé contre les 500 €** (~15 min). Retrancher ce qui
      a déjà été dépensé en phase 1 (résistance étalon, wattmètre, câbles).
      *Si ça dépasse* : le premier levier est $r_{max}$ (2,0 Ω au lieu de 1,5 Ω
      économise ~41 € par couple pour 0,45 dB) ; le second est de ne bobiner que
      les selfs strictement nécessaires à la comparaison.
      *Fini quand* : le total est sous 500 € ou l'arbitrage est écrit.
- [ ] **2-I3. Passer commande** (~30 min). *Fini quand* : les commandes sont passées
      **avec un délai de livraison noté au calendrier**. Décembre-janvier est la
      pire période de l'année pour les délais : commander le 20 décembre, c'est
      recevoir en janvier, et la période 3 commence par le bobinage.
      *Marge à prévoir* : viser une commande **avant le 15 décembre**.

---

### <a id="2j"></a>2-J. Rédiger le texte du MCOT (décembre, en parallèle)

Le texte doit être **prêt avant la saisie de mi-janvier 2027**, qui tombe en
pleine période 3. Il ne dépend d'aucun résultat : il porte sur la problématique,
les objectifs, l'ancrage et la bibliographie, tout est déjà décidé. Le seul
chiffre qu'il pourrait citer — le rapport $\max|Z|/\min|Z|$ — vient de la
phase 1. **Ne rien y promettre comme résultat.**

Budget officiel : motivation **50** · ancrage **50** · problématique **50** ·
objectifs **100** · bibliographie commentée **650** → **900 mots**, hors 5 + 5
mots-clés et 2 à 10 références. Ce sont des **plafonds de saisie** : au-delà, le
texte est coupé.

- [ ] **2-J1. Écrire la Motivation (50 mots)** (~45 min). Rubrique encore **vide**.
      Matière : l'enceinte construite de tes mains, le constat que les formules
      toutes faites supposent un haut-parleur idéal qui n'existe pas, l'envie de
      faire mieux avec des méthodes d'ingénieur. *Fini quand* : 50 mots comptés,
      écrits à la première personne, sans jargon.
      *C'est la rubrique que Claude peut le moins écrire à ta place.*
- [ ] **2-J2. Condenser l'Ancrage au thème de ~98 à 50 mots** (~45 min avec Claude).
      Il fait **le double** du plafond. Piste : garder « optimisation » en entier
      puisque c'est le cœur du sujet, ramener « sobriété » et « efficacité » à
      une demi-phrase chacune — le cuivre, le coût système et le croisement
      énergétique sont déjà portés par les Objectifs et la bibliographie.
      *Fini quand* : 50 mots comptés et les trois mots du thème présents.
- [ ] **2-J3. Condenser les Objectifs de ~126 à 100 mots** (~45 min avec Claude).
      Les quatre verbes — **Mesurer / Identifier / Optimiser / Valider** — sont
      la colonne vertébrale et restent. Couper dans les compléments : candidats
      déjà identifiés — l'énumération des six critères de l'objectif 4 (une
      quinzaine de mots, et l'exposé les détaillera), « avec incertitudes
      propagées » (déjà impliqué par « moindres carrés »), « en caisse ».
      *Arbitrage à faire* : si tu veux nommer « bass-reflex » dans les objectifs,
      il faut **rendre les mots ailleurs**. *Fini quand* : 100 mots comptés.
- [ ] **2-J4. Ne pas toucher à la Problématique** (~5 min de vérification).
      Elle fait ~44 mots pour 50 : elle passe, sans marge. Elle parle d'« un
      haut-parleur dont l'impédance varie fortement avec la fréquence » —
      formulation **renforcée** par le bass-reflex (deux pics, le second près de
      la zone de raccord). Toute reformulation doit être recomptée.
      *Fini quand* : le compte est refait et la phrase laissée telle quelle.
- [ ] **2-J5. Rédiger la bibliographie commentée : viser 600 des 650 mots** (~3 h avec
      Claude, à partir de tes fiches de lecture du bloc 2-B). Ce n'est **pas** une
      liste de titres mais une **synthèse rédigée du contexte** où les références
      sont appelées par [1], [2]… en renvois numérotés progressifs. Chaque
      référence commentée par ce qu'on lui emprunte **et pourquoi elle ne
      suffit pas**. *Bloqué par* : le bloc 2-B.
      *Fini quand* : entre 600 et 650 mots, 2 à 10 références numérotées, plus
      aucun `[[à consulter]]`, et chaque référence effectivement lue.
      **C'est la rubrique décisive : 72 % du budget de mots, et celle où le jury
      lit ton appropriation.**
- [ ] **2-J6. Dernier rappel avant rédaction — vérifier que D9 (filière et
      positionnements) porte une date** (~2 min). Décidé en `1-C5` ; ici on
      contrôle, on ne redécide pas. Si D9 est daté et signé, tu coches et tu
      passes. Sinon, **retour à `1-C5`**, et c'est bloquant pour le MCOT : le
      premier positionnement détermine le binôme d'examinateurs et doit appartenir
      à un domaine de rattachement de ta filière, dans les 24 libellés officiels
      (« Électronique » est classé en **Sciences industrielles**, pas en Physique).
      *Fini quand* : D9 porte une date, ou `1-C5` est rouvert.
- [ ] **2-J7. Dernier rappel — vérifier que le mode (seul ou en groupe) est écrit au
      registre** (~2 min). Décidé en `1-C5`. Le SCEI admet jusqu'à 3
      candidats, avec une part personnelle identifiable pour chacun.
      *Fini quand* : la ligne porte une date, ou `1-C5` est rouvert.
- [ ] **2-J8. Vérifier les 5 + 5 mots-clés** (~15 min). Le brouillon en compte bien 5
      paires, par ordre d'importance décroissante. *Fini quand* : la table est
      relue et cohérente avec le texte final.
- [ ] **2-J9. (Claude) Compter les mots rubrique par rubrique et produire la version
      à coller** (~30 min de travail de Claude). *Fini quand* : un seul fichier
      contient les cinq rubriques, chacune avec son compte exact en tête, et le
      total est **≤ 900**.
- [ ] **2-J10. Vérifier les dates 2027 de l'étape 1 à la parution des Attendus**
      (~15 min, sur scei-concours.fr/tipe.html). Les dates du projet portent
      `[[à vérifier]]` : elles sont données par analogie avec 2025 et 2026
      (clôture historiquement stable au 5-6 février). *Fini quand* : les dates
      réelles 2027 sont notées et les `[[à vérifier]]` levés.

---

### <a id="2k"></a>2-K. Porte de sortie de la période 2

À la fin décembre, les six lignes suivantes doivent être vraies. Si l'une ne
l'est pas, elle se règle avant d'entamer la période 3.

- [ ] **2-K1.** Les huit paramètres Thiele-Small sont identifiés avec leur covariance
      complète, et les huit critères du § 03.7 sont passés en revue.
- [ ] **2-K2.** $f_b$ concorde par les trois voies, ou la divergence est diagnostiquée et
      écrite.
- [ ] **2-K3.** D2, D5, D6, D8, D9, D10 sont remplis, datés et signés dans
      `DECISIONS-PHASE-0.md`, et `criteres_geles.json` ne porte plus de
      `[[a geler]]` sur ces sections.
- [ ] **2-K4.** La porte 8 Ω est franchie pour la cible gelée, et le design optimisé est
      choisi, avec sa taille de plateau et sa dispersion de tolérances.
- [ ] **2-K5.** Les composants sont **commandés** (avant le 15 décembre si possible).
- [ ] **2-K6.** Le texte du MCOT est complet, sous 900 mots, sans placeholder.

---

### <a id="p2-risques"></a>Risques de la période, et ce qu'on coupe en premier

| Ce qui peut déraper | Signe avant-coureur | Ce qu'on fait |
|---|---|---|
| Le fit à 8 paramètres ne converge pas | multi-départ dispersé, $s^2$ hors [0,5 ; 2] | replier sur `Z_deux_pics` (phénoménologique) ; l'acte 3 tient, mais la boucle de validation géométrique est perdue — le dire |
| Les trois $f_b$ divergent | écart > ~5 % | vérifier $V_b$ **net** d'abord (il domine l'incertitude), puis l'hypothèse « deux évents identiques » |
| D2 n'est toujours pas tranchée mi-décembre | la commande est en attente | trancher **par défaut sur la continuité** (Butterworth, déjà dans tous les supports, selfs 2× moins chères) et l'écrire comme un choix motivé par le budget — un choix daté et motivé vaut mieux qu'un blocage |
| Le budget dépasse 500 € | le devis de fil de cuivre | remonter $r_{max}$ à 2,0 Ω, puis renoncer à bobiner la self du passe-haut si le design le permet |
| La bibliographie n'avance pas | les sources ne sont pas arrivées du CDI | s'appuyer sur Mateljan 2012 (accès libre) et Dickason ; commenter honnêtement « consulté via » plutôt que d'inventer une lecture |
| Le temps manque (colles, DS, concours blancs) | deux semaines à zéro | **ordre de sacrifice** : (1) la contre-vérification LTspice, (2) l'analyse de plateau, (3) la figure à trois panneaux réduite à deux. **Jamais** : la porte 8 Ω, le gel des décisions avant l'optimisation, le texte du MCOT |

**La seule chose qui ne se rattrape pas** dans cette période, c'est le MCOT : la
fenêtre de saisie SCEI se ferme début février et la période 3 est déjà pleine.
Tout le reste peut glisser de deux semaines sans casser le projet.

---

## <a id="p3"></a>PÉRIODE 3 — de janvier à juin 2027

> **Comment lire cette liste.** Elle est ordonnée par dépendance, puis par date :
> déroulée de haut en bas, elle ne se bloque jamais. Chaque entrée est une action
> que tu peux cocher, avec une **durée estimée** (estimation, pas une mesure),
> ce qu'elle **débloque ou bloque**, et un critère **« fini quand »** vérifiable.
> Quand l'action revient à **Claude**, c'est écrit en toutes lettres — mais Claude
> ne produit jamais rien sans une donnée ou une décision que tu apportes.
>
> **Les durées sont du temps de travail effectif.** Les colles, les DS, les
> concours blancs et les vacances ne sont pas dans ce calendrier. Une action
> « 3 h » est à caser dans des créneaux réels : en pratique, deux samedis.
>
> **Deux dates ne se négocient pas** : la clôture de l'étape 1 (5-6 février,
> stable depuis des années) et la fenêtre de validation de l'encadrant
> (~8 jours, mi-juin). Tout le reste peut glisser ; ces deux-là, non.

---

### <a id="3a"></a>3-A. Janvier 2027 — solder ce qui bloque la saisie SCEI

Rien de cette section ne dépend d'une mesure de la période 2 : tout est décidable
dès le 2 janvier. En revanche, **tout le reste de la période 3 en dépend**.

> **Les six premières entrées de ce bloc sont des rappels, pas des décisions.**
> D2, D6, D9, le mode seul/groupe et l'encadrant ont été tranchés en période 1 ou
> 2 ; ils reviennent ici parce que la saisie SCEI les verrouille et qu'un oubli
> coûte cher. Aucune ne porte de durée de décision : on vérifie qu'une date figure
> au registre, on coche, on passe. **Si une date manque, on ne la décide pas
> ici** — on rouvre l'action d'origine, et c'est un signal d'alarme.

- [ ] **3-A1. Dernier rappel — vérifier que D2 (cible de sommation) porte une date.**
      **Durée : 2 min.**
      Décidée en **`2-F1`**, fin novembre, avant la commande de `2-I3`. L'ordre du
      projet est : on gèle, **puis** on achète — jamais l'inverse.
      **Fini quand** : le champ `DÉCISION` de D2 porte une option, une date et tes
      initiales. **Sinon** : retour immédiat à `2-F1`, et **on n'ouvre pas les
      cartons de `3-C1` avant** — des composants reçus ne valident pas un choix qui
      n'a pas été fait.

- [ ] **3-A2. Dernier rappel — vérifier que D6 ($r_{max}$, $J_{max}$, nombre de
      selfs) porte une date.** **Durée : 2 min.**
      Décidée en **`2-F2`**, fin novembre. Contrôler en particulier que le
      **nombre de selfs** y figure — 4 pour deux filtres complets, 2 avec des
      **prises intermédiaires** — parce que c'est ce nombre qui commande les 15 à
      20 h du bloc `3-C`.
      **Si le registre porte « prises intermédiaires »** : vérifier aussi qu'y
      figure la **méthode de calcul des critères n° 5 et n° 7**. Une bobine
      partagée entre deux designs ne se pèse pas et ne se facture pas séparément :
      ces deux critères passent alors de « mesurés » à « calculés », et cela doit
      être écrit **avant** le bobinage, pas constaté en mars devant la balance.
      **Fini quand** : D6 porte une date, ou `2-F2` est rouvert.

- [ ] **3-A3. Claude : relancer l'optimisation avec la cible D2 gelée et le
      $r_{max}$ gelé**, produire la liste de composants définitive (valeurs E12,
      tensions de service, DCR visée, nombre de spires, diamètre de fil) et
      vérifier que la **porte 8 Ω** repasse au vert pour la cible retenue.
      **Durée : à la demande** (`python analyse/tout_refaire.py`, ~2 min machine ;
      compter 1 h avec la relecture des résultats).
      **Débloque** : la commande de fil et de condensateurs.
      **Fini quand** : `analyse/resultats/design_optimise.json` porte la cible
      gelée et non plus un `[[a geler]]`, et le sanity check 8 Ω retombe sur le
      filtre catalogue de **cette** cible (18 mH / 141 µF en Butterworth,
      25,5 mH / 99,5 µF en LR2).

- [ ] **3-A4. Dernier rappel — vérifier que D9 (filière et positionnements) porte
      une date**, dans les libellés officiels du SCEI (« Électronique » est
      classé en **Sciences industrielles**, pas en Physique).
      **Durée : 2 min.** Décidée en `1-C5`, contrôlée en `2-J6`.
      **Fini quand** : D9 porte une date et un rang 1, 2, éventuellement 3. Sinon,
      retour à `1-C5` — c'est ce choix qui détermine le binôme d'examinateurs et
      la fenêtre d'oraux, et il se verrouille dans quinze jours.

- [ ] **3-A5. Dernier rappel — relancer l'encadrant et vérifier son nom exact pour
      la saisie.** **Durée : 2 min** de vérification au registre, plus un message
      si nécessaire. Décidé en `1-A2`/`1-A3`, contrôlé en `2-A3`.
      **Fini quand** : D10 porte une date, tu as **l'orthographe exacte du nom**
      pour le formulaire, et il a la fenêtre de 8 jours de mi-juin 2027 dans son
      agenda (c'est le deuxième des trois rappels de `T-D11`). **Si D10 est encore
      vide en janvier, c'est l'urgence n° 1 du projet**, devant toute mesure.

- [ ] **3-A6. Dernier rappel — vérifier que le mode (seul ou en groupe) est au
      registre.** **Durée : 2 min.** Décidé en `1-C5`, contrôlé en `2-J7`.
      En groupe, objectifs et présentation restent individuels.
      **Fini quand** : la ligne porte une date, ou `1-C5` est rouvert.

- [ ] **3-A7. Vérifier les dates 2027 de l'étape 1 sur
      <https://www.scei-concours.fr/tipe.html>** et lever la marque
      `[[à vérifier]]` du calendrier. **Durée : 15 min.**
      **Débloque** : la planification des trois semaines suivantes. Les
      extrapolations du dépôt (mi-janvier → 5-6 février) sont robustes à
      ±2 semaines, pas au jour près.
      **Fini quand** : les vraies dates d'ouverture et de clôture sont notées
      dans `FEUILLE-DE-ROUTE.md`.

---

### <a id="3b"></a>3-B. Mi-janvier → 5-6 février 2027 — ÉTAPE 1 SCEI (saisie en ligne)

Le texte a été rédigé en période 2 ; ici, il s'agit de le relire, le calibrer et
le saisir. **Ne pas repousser au dernier jour : la saisie est automatique, il n'y
a pas de bouton « valider ».**

- [ ] **3-B1. Claude : vérifier le comptage de mots de chaque partie du MCOT**
      (motivation 50, ancrage 50, problématique 50, objectifs 100, bibliographie
      commentée 650) et signaler tout dépassement.
      **Durée : à la demande.**
      **Fini quand** : chaque partie est sous sa limite avec une marge d'au moins
      3 %, et les renvois numérotés de la bibliographie sont progressifs.

- [ ] **3-B2. Relire et arrêter le titre.** **Durée : 30 min.**
      **Bloque** : la saisie. Le titre doit « définir sans ambiguïté le travail
      effectué » — il gagne à porter la **fréquence de raccord** et le fait que la
      charge est **mesurée** (piste du dépôt : « Optimisation sous contraintes
      d'un filtre de raccord à 100 Hz sur l'impédance mesurée d'une enceinte deux
      voies »).
      **Fini quand** : un titre unique est écrit dans `MCOT.md`, sans variante.

- [ ] **3-B3. Saisir l'étape 1 sur SCEI** : titre, encadrant, groupe, motivation,
      ancrage au thème, positionnements + 5 mots-clés français et 5 anglais,
      bibliographie commentée, problématique, objectifs, 2 à 10 références.
      **Durée : 2 h** en une seule session, copier-coller depuis `MCOT.md`.
      **Débloque** : tout le reste de l'année ; c'est la porte administrative du
      TIPE.
      **Fini quand** : tu as **relu chaque champ après saisie** (l'enregistrement
      est automatique, donc silencieux) et pris une capture d'écran de chaque
      page pour ton dossier.

- [ ] **3-B4. Reporter dans `DECISIONS-PHASE-0.md` ce qui vient d'être verrouillé**
      (positionnements, mots-clés, références) : l'étape 2 n'autorisera que des
      « ajustements éventuels ». **Durée : 15 min.**
      **Fini quand** : la ligne D9 du tableau de bord passe de `[[ouvert]]` à la
      valeur saisie, avec la date.

---

### <a id="3c"></a>3-C. Janvier–février 2027 — achats et fabrication des selfs

Le poste le plus long de toute la période, et le plus facile à sous-estimer.

- [ ] **3-C1. Réceptionner et contrôler la commande passée en `2-I3`.** Pointer
      ligne à ligne contre la liste de `2-I1` : diamètre et masse de fil,
      références et **tensions** des condensateurs, mandrins, cosses, résistances
      de L-pad le cas échéant.
      **Durée : 1 h.**
      **Bloque** : le bobinage, donc tout le reste de la période.
      **Fini quand** : tout est arrivé, conforme, et **les factures sont archivées
      dans le dépôt** — elles servent au critère n° 5, qui se mesure sur factures
      et pas sur devis. *Si une référence manque ou n'est pas conforme, c'est
      maintenant qu'on la recommande* : en janvier il reste de la marge, en mars il
      n'y en a plus.

- [ ] **3-C2. Contrôler ce que valent réellement les condensateurs reçus** : lire
      sur chaque corps la **tension alternative permanente** (pas la tension DC —
      sur un MKP, un « 100 V » est presque toujours du continu, l'alternatif
      permanent tournant autour de 60–65 V RMS ; le minimum du projet est
      **250 V DC / 160 V AC**, `T-A9`), et **mesurer la capacité réelle** de chacun
      au capacimètre ou au banc d'impédance de la phase 1.
      **Durée : 45 min.**
      **Débloque** : la porte de validation ±5 % de `3-E2`, qui se juge sur les
      valeurs **mesurées** de $L$ et $C$, jamais sur les valeurs nominales — un
      condensateur donné à ±20 % ne se suppose pas.
      **Fini quand** : chaque condensateur porte une étiquette avec sa capacité
      mesurée et sa tenue AC, et qu'aucun ne se retrouve sous la spécification. *Si
      l'un est sous-dimensionné, il ne se monte pas* : un condensateur qui claque
      en service à 130 V crête emporte la manip et peut-être la voie.

- [ ] **3-C3. Fabriquer le mandrin et le monter sur un axe entraîné**
      (perceuse à vitesse lente ou manivelle), avec un dérouleur libre pour la
      bobine de fil. **Durée : une demi-journée (3 à 4 h).**
      **Débloque** : le bobinage en 1 à 2 h par self au lieu d'une demi-journée.
      C'est le meilleur retour sur temps de toute la période : à 4 selfs, l'écart
      entre outillé et non outillé est de **8 h contre 2 jours**.
      **Fini quand** : le mandrin tourne sans voile, les joues sont démontables,
      et un compteur de spires (mécanique, ou pointage par couche) est en place.

- [ ] **3-C4. Bobiner la première self, avec 2 à 3 % de spires en trop.**
      **Durée : 1 à 2 h avec l'outillage, une demi-journée sans.** C'est la seule
      estimation de tout le projet marquée
      `[[à confirmer par l'expérience sur la première self]]` : chronomètre-la et
      **reporte la vraie durée ici**, les trois suivantes s'en déduisent.
      **Fini quand** : le bobinage est ligaturé ou imprégné (une spire mobile fait
      varier $L$ et vibre à 100 Hz sous les forces de Laplace, $I$ crête ≈ 9,4 A),
      et le nombre de spires est écrit au cahier.

- [ ] **3-C5. Mesurer $L$ au banc d'impédance de la phase 1, puis dérouler spire à
      spire jusqu'à la valeur cible.** **Durée : 45 min par self.**
      **Débloque** : la porte de validation ±5 % de la phase 4, qui n'est tenable
      que si $L$ et $C$ sont **mesurés** et non nominaux.
      **Méthode** : $L = |Z|\sin\varphi/\omega$, lu à 50, 100, 200 et 400 Hz —
      $L$ doit être constant ; c'est en prime le contrôle de linéarité. La
      résonance série avec un $C$ connu sert de **contre-vérification
      indépendante**, pas de méthode principale (elle importerait l'incertitude
      sur $C$).
      **Fini quand** : $L$ est à mieux que 1 % de la cible, et la valeur mesurée
      est consignée avec son incertitude.

- [ ] **3-C6. Mesurer la DCR en quatre fils** (ou en soustrayant la résistance des
      cordons mesurée à part) et **peser la self**.
      **Durée : 20 min par self.**
      **Les trois gestes à faire dans cet ordre, et qui ne se devinent pas**
      (`T-A10`) : **diode 1N4007 en antiparallèle** sur la self pendant toute la
      mesure ; **établissement ET coupure progressifs à l'alimentation**, jamais en
      arrachant un fil ; **le voltmètre se débranche en dernier**. Motif :
      couper 1 A dans 18 mH en quelques microsecondes produit **plusieurs centaines
      de volts** aux bornes de la self. C'est le genre de détail qui coûte un
      multimètre — et le multimètre est celui du lycée.
      **Débloque** : les critères « pertes d'insertion » et « encombrement /
      matière ».
      **Fini quand** : $r$ et $m$ sont au cahier, et l'écart au modèle
      (§ 05.6-05.8) est calculé et **expliqué**, pas seulement constaté.

- [ ] **3-C7. Répéter `3-C4` + `3-C5` + `3-C6` pour les selfs restantes** (3 si tu
      as retenu deux filtres complets, 1 si tu as retenu les prises
      intermédiaires).
      **Durée : aucune durée propre — c'est `3-C4`, `3-C5` et `3-C6` répétés.**
      Compter **3 h 05 par self** avec l'outillage (2 h de bobinage + 45 min de
      mesure de $L$ + 20 min de DCR et pesée), donc **~9 h pour trois selfs** ;
      sans outillage, une demi-journée de bobinage par self suffit à faire passer
      ce poste à deux jours pleins.
      **Fini quand** : toutes les selfs du projet sont mesurées, pesées et
      étiquetées.

- [ ] **3-C8. Claude : comparer les selfs mesurées au modèle Wheeler/Brooks**
      et produire la figure « prédit vs mesuré » du satellite self.
      **Durée : à la demande.**
      **Fini quand** : l'écart est chiffré et un motif physique lui est associé
      (tension de bobinage, papier intercalaire, remplissage réel).

> **Total du bloc `3-C`, compté une seule fois et sans double emploi** — c'est le
> nombre à confronter à l'échéance « toutes les selfs avant les vacances de
> février » :
>
> | Poste | Détail | Avec outillage |
> |---|---|---|
> | Réception et contrôle | `3-C1` + `3-C2` | 1 h 45 |
> | Mandrin et axe entraîné | `3-C3`, une fois | 3 à 4 h |
> | Bobinage | 4 selfs × 1 à 2 h | 4 à 8 h |
> | Mesure de $L$ et ajustement | 4 × 45 min | 3 h |
> | Mesure de DCR et pesée | 4 × 20 min | 1 h 20 |
> | **Total** | | **13 à 18 h**, disons **15 à 20 h** avec les reprises |
>
> **Sans outillage** (bobinage à la main, une demi-journée par self), le même bloc
> passe à **25 à 30 h** : c'est exactement pour cela que `3-C3` est le meilleur
> retour sur temps de la période. Avec les **prises intermédiaires** (2 selfs au
> lieu de 4), retirer ~4 h — mais lire d'abord la conséquence inscrite en `3-A2`
> sur les critères n° 5 et n° 7.
>
> Ces durées portent la seule marque `[[à confirmer par l'expérience]]` du projet
> (`3-C4`) : **chronomètre la première self et reviens corriger ce tableau.**

---

### <a id="3d"></a>3-D. Février 2027 — montage des filtres et de la référence active

- [ ] **3-D1. Monter le filtre catalogue et le filtre optimisé sur planche**, selfs à
      **axes perpendiculaires** ou séparées de plus de deux diamètres.
      **Durée : 3 h les deux.**
      **Bloque** : toutes les mesures électriques. Le couplage mutuel est le piège
      classique : à un diamètre d'écartement il vaut encore **4,6 %** sur $L$,
      soit deux fois l'effet de ±5 spires — il fausserait la comparaison
      prédit/mesuré, et il est **gratuit à éviter**.
      **Fini quand** : les deux filtres sont câblés, repérés, et $L$ a été
      re-mesurée **en place** (pour vérifier qu'aucun couplage résiduel ne l'a
      déplacée).

- [ ] **3-D2. Monter la référence active Sallen-Key** sur alimentation symétrique
      ±15 V, en amont de l'ampli, sur les deux canaux du E-800 (sub :
      R = 10 kΩ, C₁ = 220 nF, C₂ = 110 nF ; médiums : R'₁ = 11 kΩ, R'₂ = 22 kΩ,
      C = 100 nF ; AOP NE5532 ou TL072).
      **Durée : une demi-journée (4 h)**, mise au point comprise.
      **Débloque** : le troisième terme de toute la comparaison, et le satellite
      « croisement énergétique ».
      **Fini quand** : le Bode électrique de chaque voie, relevé au GBF, croise la
      cible à ±5 % — et surtout **sans charge de haut-parleur**, puisque c'est
      tout l'intérêt de l'actif : il ne voit jamais $Z(f)$.

- [ ] **3-D3. Photographier le jig d'impédance, le bobinage en cours, les selfs et les
      filtres montés — avant tout démontage.**
      **Durée : 30 min.**
      **Bloque** : les figures de la présentation. L'enceinte, la self et le
      filtre sont des **objets interdits en salle** : la photo est la seule chose
      qui entrera dans le PDF.
      **Fini quand** : les photos sont dans `assets/`, ré-encodées en JPEG à
      ≤ 200 ko l'unité (le PDF est plafonné à 5 Mo).

- [ ] **3-D4. Relire $S_d$, $S_p$ et l'entraxe avant la première campagne
      acoustique — contrôle de cohérence, pas mesure.** **Durée : 10 min.**
      Ces longueurs ont été relevées une fois pour toutes en **`1-A4`** (septembre)
      et confirmées en **`2-F4`** (novembre) ; elles servent aux poids
      $\sqrt{S_{P,i}/S_D}$ de la sommation de Keele. Il s'agit ici de les **relire
      sur la feuille de manip** avant de placer le micro, pas de ressortir le mètre
      ruban.
      **Ne bloque rien en amont** : le recalibrage du poids de phase $w_\varphi$
      appartient à `2-F4`, fin novembre, et la fonction de coût est gelée depuis
      `2-F3` — une action de février ne peut pas, par construction, bloquer une
      décision de novembre.
      **Fini quand** : les trois valeurs sont recopiées en tête de la feuille de
      manip, avec leur incertitude de lecture.

---

### <a id="3e"></a>3-E. Février–mars 2027 — campagnes de mesure, du moins au plus destructif

**L'ordre de cette section est une règle de sécurité, pas une commodité** :
toujours du faible vers le fort, toujours la résistance avant le haut-parleur.
Aucun test ne commence tant que le précédent n'est pas passé.

> **Convention de durée, valable pour tout le bloc `3-E` et énoncée une fois.**
> Les durées écrites sur `3-E5`, `3-E7`, `3-E12` et `3-E13` sont **par
> configuration de filtre** (catalogue, optimisé, actif). Les actions de reprise
> — `3-E9` et `3-E13` — **ne portent aucune durée propre** : elles disent « ×3 »,
> et le total est calculé une seule fois à la fin de la section. Sans cette
> convention, le même travail se comptait deux fois et le bloc pouvait valoir 4 h
> ou 16 h selon la lecture ; sur un poste placé en pleine période de concours, un
> facteur 4 sur l'estimation n'est pas un détail.

- [ ] **3-E1. Relire à voix haute les consignes de sécurité avant la première session**
      (D3, § 07.11) : bouchons d'oreilles **y compris au niveau faible** (112 dB
      SPL en champ proche dès 0,5 W), personne dans l'axe pendant les balayages
      forts, pas de tête à moins de 1 m du 18″, limiteur du E-800 enclenché mais
      **toute mesure où la LED limit/clip s'allume est écartée et refaite plus
      bas**. **Durée : 10 min, à chaque session.**
      **Fini quand** : la borne basse `Start` $\ge 2f_b$ est écrite en gros sur la
      feuille de manip, avec le $f_b$ **mesuré en phase 1** — pas un chiffre de
      catalogue.

#### <a id="3e1"></a>3-E.1 Électrique sur résistance de puissance 8 Ω — la porte de validation

- [ ] **3-E2. Relever le Bode des deux voies de chaque filtre sur la résistance de
      puissance 8 Ω.** **Durée : 2 h les deux filtres.**
      **Source = l'amplificateur, JAMAIS le GBF (§ 07.7).** Un GBF a **50 Ω de
      sortie** : le filtre LC calculé pour 8 Ω voit alors 50 Ω en série et n'a plus
      rien de Butterworth. C'est le premier point de méthode du § 07.7, et c'est
      celui qui fait échouer cette porte pour une raison qui n'a **rien à voir avec
      le filtre** — on part alors chercher $L$, $C$ et le couplage entre selfs
      pendant une journée, pour une erreur de câblage de trente secondes.
      **Bloque** : tout passage au haut-parleur. C'est la porte de validation de
      la phase 4.
      **Fini quand** : le croisement des deux voies (définition D1 : l'unique
      $f \in [40;250]$ Hz telle que $|H_{PB}G_{sub}| = |H_{PH}G_{méd}|$) est à
      **±5 % de la prédiction faite avec les valeurs mesurées de $L$ et $C$**. Si
      ça ne passe pas : on diagnostique, on ne continue pas. Rappel d'écriture :
      l'incertitude d'un LC se cite **par couple** — 7,1 % en borne au pire cas,
      4,1 % en incertitude-type (GUM) —, jamais en nombre seul.

- [ ] **3-E3. Mesurer les pertes d'insertion en bande passante sur 8 Ω**
      (V et I, à la puissance de référence gelée).
      **Durée : 1 h.**
      **Débloque** : le critère n° 3.
      **Fini quand** : les dB et les W perdus sont chiffrés pour chaque filtre,
      et confrontés au DCR mesuré (contrôle croisé : 1 Ω en série avec 8 Ω →
      −0,51 dB en puissance et −1,02 dB en niveau ; les deux nombres décrivent la
      même chose sous deux conventions, ne pas les mélanger).

#### <a id="3e2"></a>3-E.2 Électrique sur haut-parleur réel — l'écart attendu apparaît

- [ ] **3-E4. Refaire le même Bode, filtres chargés par les haut-parleurs réels, le
      bloc médiums câblé TEL QU'IL EST** (les 2 pavillons d'ultra-aigu restent en
      parallèle avec leur condensateur de série : ils sont hors périmètre
      acoustique mais **dans la charge électrique** du passe-haut).
      **Durée : 2 h les deux filtres.**
      **Source = l'amplificateur, jamais le GBF** — même règle qu'en `3-E2`, et
      elle mord davantage ici : comparer une courbe « sur 8 Ω » relevée à l'ampli
      et une courbe « sur charge réelle » relevée au GBF ferait passer 50 Ω
      d'impédance de source pour l'effet de $Z(f)$, c'est-à-dire fabriquerait le
      résultat central du TIPE.
      **Règle de câblage attachée au critère** : toutes les branches et tous les
      haut-parleurs restent connectés en permanence ; entre deux mesures, **on ne
      déplace que le micro**. Débrancher une voie pour mesurer l'autre
      introduirait une erreur systématique, silencieuse, et portant exactement sur
      l'objet du TIPE.
      **Fini quand** : l'écart entre la courbe sur 8 Ω et la courbe sur charge
      réelle est tracé — c'est **la diapositive centrale de l'oral**, la preuve
      visuelle que le haut-parleur n'est pas une résistance de 8 Ω.

#### <a id="3e3"></a>3-E.3 Acoustique en champ proche, niveau faible

- [ ] **3-E5. Relever le champ proche du sub bass-reflex, filtre inséré : membrane +
      évent 1 + évent 2, trois relevés, trois répétitions chacun.**
      **Durée : ~45 min par configuration de filtre** (3 positions × 3
      répétitions, repositionnement soigné et consigné). Le total des trois
      configurations est compté une seule fois, au récapitulatif de fin de
      section — pas ici.
      **Pourquoi trois relevés** : en caisse close, un seul relevé au centre du
      cône suffirait. En bass-reflex, non — sous l'accord c'est l'évent qui
      rayonne l'essentiel, et la membrane peut être en opposition de phase.
      **Fini quand** : les trois pressions sont enregistrées séparément, avec la
      position du micro consignée, prêtes à être sommées.

- [ ] **3-E6. Claude : sommer les trois contributions en pression complexe, pondérées
      par $\sqrt{S_i/S_d}$** (avec deux évents identiques, le terme évent pèse
      $\sqrt{2S_p/S_d}$), et produire la courbe de la voie grave.
      **Durée : à la demande.**
      **Fini quand** : la somme est tracée et le poids numérique utilisé est écrit
      sur la figure — un jury peut demander d'où sort ce $\sqrt{2}$.

- [ ] **3-E7. Relever le champ proche de la voie médium, filtre inséré, aux mêmes
      conditions.** **Durée : 30 min par configuration.**
      **Fini quand** : les trois répétitions sont faites et la dispersion entre
      répétitions est chiffrée (elle sert au seuil de départage du critère n° 1).

- [ ] **3-E8. Vérifier l'inversion de polarité au micro.**
      **Durée : 15 min.**
      **Pourquoi c'est le test le plus rentable de la période** : au 2ᵉ ordre,
      inversion **obligatoire** — à $f_c$, le bon sens donne une bosse, le mauvais
      un trou profond. C'est immédiat, lisible, et ça vaut une diapositive.
      **Fini quand** : les deux sens ont été essayés et les deux courbes sont
      enregistrées côte à côte.

- [ ] **3-E9. Répéter le bloc 3-E.3 (`3-E5` à `3-E8`) pour les trois
      configurations : filtre catalogue, filtre optimisé, référence active.**
      **Durée : aucune durée propre — « ×3 » sur les durées déjà écrites**
      (45 min de sub + 30 min de médium + 15 min de polarité par configuration),
      **plus ~1 h de dépouillement par configuration**. Voir le récapitulatif en
      fin de section.
      **Bloque** : tout le tableau comparatif.
      **Fini quand** : les trois jeux de courbes existent, mesurés le **même
      jour** si possible (un déplacement de micro entre deux sessions est un biais
      qui ne se rattrape pas).

#### <a id="3e4"></a>3-E.4 Acoustique au niveau fort, et robustesse

- [ ] **3-E10. Claude : simuler AVANT la session l'écart RMS prédit pour $R_e$,
      $1{,}08\,R_e$ et $1{,}20\,R_e$**, à partir du modèle T-S identifié en
      phase 2. **Durée : à la demande.**
      **Pourquoi avant et pas après** : si l'écart prédit est sous le seuil de
      répétabilité, on l'annonce **avant** de mesurer, et la mesure servira à
      poser une **borne supérieure** au lieu de trancher. Dire cela à l'oral vaut
      infiniment mieux que de monter le niveau après coup pour « faire sortir »
      un effet.
      **Fini quand** : le nombre prédit est écrit et daté au cahier, avant la
      première mesure forte.

- [ ] **3-E11. Vérifier visuellement le débattement à faible niveau, puis passer au
      niveau fort gelé (D3), `Start` $\ge 2f_b$ sans exception.**
      **Durée : 15 min de contrôle.**
      **Ce qui arrive si tu sautes cette étape** : sous l'accord, la membrane
      n'est plus chargée par les évents, l'excursion devient maximale, et le 18″
      peut être **détruit mécaniquement**. C'est le seul geste irréversible du
      projet.
      **Fini quand** : la borne basse est saisie dans REW et relue à l'écran avant
      de lancer le balayage, **et** que la valeur du condensateur des pavillons
      (présent, constat du 16/09/2026 ; valeur relevée en `T-A8`) et le contrôle
      de câblage B1 bis du livret (lecture DC du bloc d'environ 6 à 7 Ω) sont
      **relus sur la feuille de manip**. **Si ce contrôle avait lu 2 à 3 Ω**
      (un pavillon sans condensateur, incohérent avec le constat), les pavillons
      recevraient le 100 Hz à pleine puissance, complètement hors de leur bande,
      avec une excursion que leur suspension n'encaisse pas : aucun balayage fort
      sur la voie médium avant d'avoir ouvert le bornier, et on l'écrit au
      cahier. (La mesure d'impédance à 150 mV de `1-E4`, elle, est sans risque —
      c'est le niveau fort qui change tout.)

- [ ] **3-E12. Conditionner thermiquement (bruit rose au niveau fort, durée gelée en D3
      — proposition 5 min), relever $R_e$ en quatre fils avant et après chaque
      balayage, chronomètre déclenché à l'arrêt du signal, trois lectures
      extrapolées à $t = 0$.** **Durée : 1 h par configuration.**
      **Débloque** : le critère n° 8 « robustesse ».
      **Fini quand** : $R_e$ froid, $R_e$ chaud extrapolé et $\tau_v$ sont au
      cahier — et l'écart fait partie du résultat, pas des conditions de mesure.
      Penser à faire de même sur le **bloc médiums** : c'est l'**écart** de
      compression entre voies qui déplace le raccord, pas seulement celle du sub.

- [ ] **3-E13. Refaire le relevé du raccord au niveau fort pour les trois
      configurations.** **Durée : ~1 h 15 par configuration** (le bloc `3-E.3`
      rejoué au niveau fort, borné à $2f_b$), soit **×3** au récapitulatif.
      **Avant chaque balayage** : la relecture de `T-A8` exigée en `3-E11`.
      **Fini quand** : les courbes « faible » et « fort » sont superposables sur
      une même figure pour chaque configuration, et la LED limit/clip est restée
      éteinte (état consigné pour chaque balayage) — toute mesure où elle s'est
      allumée est **écartée et refaite plus bas**, pas « gardée avec une note ».

#### <a id="3e5"></a>3-E.5 Consommation

- [ ] **3-E14. Mesurer au wattmètre de prise la consommation au repos, sans signal**,
      des deux chaînes : passive (préampli + un canal d'ampli) et active
      (Sallen-Key + alimentation ±15 V + deux canaux d'ampli).
      **Durée : 1 h.**
      **Débloque** : le critère n° 4 et le satellite « croisement énergétique ».
      **Fini quand** : les deux puissances au repos sont relevées, ainsi que la
      consommation à la prise aux deux niveaux d'écoute gelés.

> **Récapitulatif chiffré du bloc `3-E`** — le plus gros poste de la période, et
> celui qui tombe en pleine période de concours. Compté une seule fois, selon la
> convention annoncée en tête de section :
>
> | Sous-bloc | Détail | Total |
> |---|---|---|
> | Sécurité (`3-E1`) | 10 min × ~8 sessions | ~1 h 20 |
> | `3-E.1` électrique sur 8 Ω (`3-E2`, `3-E3`) | 2 h + 1 h | 3 h |
> | `3-E.2` électrique sur HP réel (`3-E4`) | 2 h | 2 h |
> | `3-E.3` acoustique faible (`3-E5` à `3-E9`) | (45 + 30 + 15 min + 1 h de dépouillement) × 3 | ~7 h 30 |
> | `3-E.4` niveau fort (`3-E10` à `3-E13`) | 15 min + (1 h de conditionnement + 1 h 15 de relevé) × 3 | ~7 h |
> | `3-E.5` consommation (`3-E14`) | 1 h | 1 h |
> | **Total** | | **~21 à 25 h** selon les reprises |
>
> À caser **avant les concours blancs de printemps**, en séances courtes : c'est
> le bloc qui décide si la conclusion repose sur des mesures ou sur des regrets.

- [ ] **3-E15. Claude : calculer le point de croisement énergétique $P^\star$** — le
      niveau d'écoute au-dessus duquel les pertes proportionnelles du passif
      dépassent la consommation fixe de l'actif — en évaluant les pertes Joule
      **spectralement sur la $Z(f)$ mesurée**, et non sur 8 Ω.
      **Durée : à la demande.**
      **Fini quand** : $P^\star$ est chiffré, avec la bande et l'hypothèse de
      spectre (bruit rose) **énoncées sur la figure** : c'est l'argument
      « sobriété » le plus direct du sujet, il ne doit pas reposer sur une
      hypothèse tacite.

---

### <a id="3f"></a>3-F. Mars–avril 2027 — analyse comparative et conclusion

- [ ] **3-F1. Claude : remplir le tableau brut des huit critères gelés** à partir des
      mesures, avec les incertitudes propagées et le seuil de départage
      ($\approx 2{,}3\,s$ pour 3 répétitions).
      **Durée : à la demande** — mais **seulement une fois toutes les mesures
      déposées** dans `analyse/mesures/`.
      **Fini quand** : chaque case porte une valeur **et** son incertitude, et les
      cases non départagées portent explicitement « non départagés ».

- [ ] **3-F2. Relire le tableau contre `DECISIONS-PHASE-0.md` et vérifier qu'aucun
      critère n'a bougé depuis le gel.** **Durée : 45 min.**
      **Pourquoi c'est la relecture la plus importante de l'année** : changer une
      bande, une pondération ou un critère après avoir vu les courbes revient à
      choisir le vainqueur puis à écrire le règlement. C'est la seule faute
      réellement disqualifiante du projet, et elle est **invisible dans un
      rapport** — d'où le registre daté.
      **Fini quand** : soit rien n'a bougé, soit chaque changement est inscrit au
      *Journal des modifications*, daté, justifié par un argument qui n'est pas le
      résultat obtenu, et noté pour être **dit à l'oral**.

- [ ] **3-F3. Écrire la conclusion, y compris si elle est défavorable.**
      **Durée : 3 h.**
      **Ce qu'on attend** : une limite identifiée est un résultat. Si le passif
      optimisé ne rattrape pas l'actif, le dire ; si deux configurations ne sont
      pas départagées par les mesures, l'écrire au lieu de trancher.
      **Fini quand** : la conclusion tient en une page, ne contient aucun chiffre
      non mesuré, et répond explicitement à la problématique — y compris par
      « pas dans les conditions testées ».

- [ ] **3-F4. Insérer dans la problématique le rapport $\max|Z|/\min|Z|$ mesuré.**
      **Durée : 15 min.**
      **Débloque** : rien, mais c'est la promesse tenue du projet — aucun chiffre
      n'a été écrit avant d'être mesuré, et celui-là attend sa place depuis
      août 2026.
      **Fini quand** : le chiffre figure dans `CLAUDE.md`, `FEUILLE-DE-ROUTE.md`
      et les diapositives, sans marque `[[à mesurer]]` résiduelle.

---

### <a id="3g"></a>3-G. Avril–mai 2027 — figures, diapositives, PDF

- [ ] **3-G1. Déposer tous les CSV de mesure dans `analyse/mesures/` et lancer
      `python analyse/tout_refaire.py`.** **Durée : 1 h.**
      **Débloque** : toutes les figures. Le pipeline est écrit pour ça : le jour
      des vraies mesures, il suffit de déposer les CSV, rien d'autre ne change.
      **Fini quand** : la commande rend 0, `resultats/journal.txt` est daté du
      jour, et **plus aucune figure ne porte l'étiquette SYNTHÉTIQUE**.

- [ ] **3-G2. Claude : refondre les figures et les diapositives avec les vraies
      données**, gabarit 4/3 (1024×768), figures matplotlib au couple
      figsize/dpi gelé en D7, injection par marqueur `<!--FIG:nom-->`.
      **Durée : à la demande.**
      **Fini quand** : aucun bloc `.placeholder` et aucun `<!-- TODO -->` ne
      subsiste dans `presentation-finale.html`, et le « ± 11 % sur f_c » hérité
      de la v1 (l. 1073 et 1173) a disparu — c'était la formule d'un RC du 1ᵉʳ
      ordre abandonné, pas celle d'un LC.

- [ ] **3-G3. Arbitrer le plan de l'exposé : viser 16 à 18 vues.**
      **Durée : 2 h** avec Claude.
      **Le piège** : à ~40 s par vue, 15 min feraient 22 diapositives. La cible
      retenue est 16 à 18 vues à 50-55 s, et le temps gagné sert à **montrer les
      portes de validation** (étalonnage, résidus, sanity check 8 Ω), pas à
      ajouter des planches. Le détail (self, Monte-Carlo, énergie, listings) vit
      en **annexes après la conclusion**, hors chronomètre, appelées pendant les
      15 min d'entretien.
      **Fini quand** : le plan tient sur une feuille, avec une durée cible par
      vue.

- [ ] **3-G4. Vérifier la première vue : nom, prénom, numéro d'inscription ; et la
      numérotation de toutes les diapositives.** **Durée : 20 min.**
      **Fini quand** : c'est vérifié **sur le PDF sorti**, pas dans le HTML — la
      numérotation est une exigence SCEI et elle se contrôle après export.

- [ ] **3-G5. Exporter le PDF vectoriel en 4/3 et contrôler sa taille.**
      **Durée : 1 h** la première fois, 10 min ensuite.
      **Fini quand** : le fichier est en `1024×768`, sous **5 Mo en lecture
      conservatrice** ($5\times10^6$ octets), et s'ouvre correctement sur une
      machine **sans réseau** — formules comprises (MathJax et polices sont
      vendorés, mais ça se vérifie, ça ne se suppose pas). Contrôler la taille
      **à chaque export**, pas seulement au dernier.

- [ ] **3-G6. Préparer le listing papier en deux parties.**
      **Durée : 2 h.**
      **La règle, fixée d'avance** : `analyse/` fait **19 319 lignes** (mesure du
      23/09/2026, `wc -l analyse/*.py analyse/tests/*.py`), soit
      ~360 pages, ~720 en double exemplaire — matériellement indéposable, et une
      annexe illisible donne l'impression d'un travail non maîtrisé. Donc : (1) un
      **noyau imprimé de 10 à 15 pages**, exactement les fonctions que le récit
      cite et sur lesquelles tu dois pouvoir être interrogé au tableau
      (`modele_hp.Z_ts`, `ts_fit.residus_ts` + `ajuster_ts` +
      `moindres_carres_lm`, `filtre.H_pb`/`H_ph`/`cible`, `optim.cout` +
      `enumere_e12`, `incertitudes.u_f0_relative`) ; (2) une **page de garde**
      donnant l'URL du dépôt, le hash court du commit, la commande de
      régénération et l'empreinte SHA-256 de `resultats/journal.txt`.
      **Fini quand** : le noyau est relu ligne à ligne — tu dois pouvoir défendre
      chaque ligne imprimée — et l'empreinte de la page de garde correspond bien
      au journal du dernier export.

- [ ] **3-G7. Imprimer les listings en DOUBLE EXEMPLAIRE PAPIER.**
      **Durée : 1 h** (impression + reliure légère).
      **Bloque** : rien, mais c'est une exigence SCEI et personne ne l'imprime le
      matin de l'oral.
      **Fini quand** : deux jeux identiques, fond blanc, sont rangés avec les
      affaires de concours.

---

### <a id="3h"></a>3-H. Fin février → 9-10 juin 2027 — ÉTAPE 2 SCEI (PDF + DOT)

La fenêtre ouvre fin février mais la **clôture** est ce qui compte. Ne pas
attendre : un PDF téléversable existe dès qu'une version acceptable est prête.

- [ ] **3-H1. Rédiger le DOT : 4 à 8 jalons factuels, 50 mots maximum chacun,
      strictement chronologiques, difficultés comprises.**
      **Durée : 2 h**, matière première = le journal daté du dépôt (commits,
      cahier de laboratoire).
      **Ce que le DOT n'est pas** : un plan, ni des résultats, ni des
      interprétations. Il « doit rester strictement factuel et situer
      chronologiquement les jalons ». Le **pivot v1 → v2 du 04/08/2026** y a toute
      sa place : le SCEI aime lire les « rebonds ou inflexions dans la démarche ».
      **Fini quand** : chaque jalon est sous 50 mots (compté, pas estimé) et
      aucun ne contient le mot « donc ».

- [ ] **3-H2. Téléverser une première version du PDF dès qu'elle est présentable**,
      même imparfaite, puis la remplacer.
      **Durée : 20 min.**
      **Pourquoi** : c'est une assurance contre la panne de la dernière semaine.
      Le remplacement est autorisé pendant toute la fenêtre.
      **Fini quand** : un PDF conforme (4/3, < 5 Mo, numéroté) est en ligne.

- [ ] **3-H3. Téléverser le PDF définitif et saisir le DOT.**
      **Durée : 1 h.**
      **Bloque** : l'étape 3.
      **Fini quand** : tu as **rouvert la page après saisie** pour vérifier que
      tout est enregistré, et téléchargé le PDF depuis le site pour confirmer que
      c'est bien le bon fichier qui est en ligne.

---

### <a id="3i"></a>3-I. Mi-juin 2027 — ÉTAPE 3 : la validation par l'encadrant (8 jours)

**C'est l'action la plus courte et la plus dangereuse de tout le TIPE.**

- [ ] **3-I1. Prévenir l'encadrant trois semaines avant l'ouverture de la fenêtre**,
      avec la date exacte d'ouverture et de clôture.
      **Durée : 10 min.**
      **Bloque** : la note. Sans validation, « le candidat aura un entretien avant
      son passage en loge » — note zéro possible.
      **Fini quand** : il a confirmé par écrit qu'il a la date et l'accès à
      `lycees.scei-concours.fr`.

- [ ] **3-I2. Relancer le jour de l'ouverture, puis tous les deux jours jusqu'à
      confirmation.** **Durée : 5 min par relance.**
      **Pourquoi c'est ta responsabilité et pas la sienne** : la fenêtre fait
      8 jours, elle tombe en pleine période de jurys et de corrections, et rien ne
      te prévient si elle se referme.
      **Fini quand** : il t'a confirmé que la validation est **enregistrée**, pas
      seulement qu'il « va le faire ».

---

### <a id="3j"></a>3-J. Mai–juin 2027 — répétitions chronométrées

À commencer **dès que le PDF est stable**, sans attendre la validation.

- [ ] **3-J1. Première répétition chronométrée, seul, à voix haute, sur le PDF projeté
      (pas sur le HTML).** **Durée : 1 h** (30 min d'exposé raté + reprise).
      **Fini quand** : tu connais ton dépassement réel. Presque tout le monde
      dépasse la première fois ; la question est de combien.

- [ ] **3-J2. Couper jusqu'à tenir 15 min avec 1 min de marge**, en déplaçant en annexe
      ce qui tombe. **Durée : 2 h.**
      **Fini quand** : trois répétitions consécutives passent sous 15 min sans
      accélérer la fin.

- [ ] **3-J3. Préparer les 15 min d'entretien : lister les 20 questions les plus
      probables et la vue d'annexe qui répond à chacune.**
      **Durée : 3 h** avec Claude, en partant de `NOTES-TIPE.md` (déjà écrit en
      v2, avec des placeholders à combler par les chiffres mesurés).
      **Trois questions qui tomberont presque à coup sûr, et dont une n'est
      aujourd'hui traitée nulle part dans ce parcours** :
      (a) **« Pourquoi optimiser le filtre plutôt que linéariser $Z(f)$ par un
      réseau de Zobel ? »** C'est l'objection la plus prévisible du sujet, et elle
      a une réponse chiffrée en § 04.4 : le Zobel annule bien $j\omega L_e$, mais
      **à 100 Hz il ne corrige pas le pic motionnel**, qui est le vrai problème au
      raccord (14,1 → 11,6 Ω seulement) ; la compensation qui, elle, opère demande
      **2,4 mF sous 250 V et une résistance qui dissipe à $f_s$ sept fois ce que
      reçoit le haut-parleur** — l'inverse exact de « sobriété ». Autrement dit :
      le bon marché est inopérant, l'opérant est hors de prix, d'où l'optimisation
      directe sur $Z(f)$. Le balayage de 36 couples $(R_z, C_z)$ confirme que le
      Zobel **n'améliore pas $J$**.
      (b) « Comment savez-vous que c'est le bon minimum ? » (→ `2-C4`).
      (c) « Et si vous aviez trouvé le contraire ? » (→ `T-C6`).
      **Fini quand** : chaque question a un numéro de vue d'annexe en face, les
      trois ci-dessus en ont une chacune, et les
      placeholders de `NOTES-TIPE.md` sont tous remplis par des valeurs mesurées.

- [ ] **3-J4. Répétition devant l'encadrant ou un professeur de physique, avec
      questions.** **Durée : 1 h.**
      **Débloque** : les angles morts que tu ne vois plus.
      **Fini quand** : tu as noté les questions auxquelles tu as mal répondu et
      corrigé soit la diapositive, soit ta réponse.

- [ ] **3-J5. Vérifier ta capacité à défendre trois points au tableau, sans support** :
      (a) pourquoi le modèle à 5 paramètres converge **en silence** sur des
      données bass-reflex, (b) d'où vient le facteur ½ dans
      $u(f_0)/f_0 = \frac12\sqrt{(u_L/L)^2+(u_C/C)^2}$, (c) pourquoi le cuivre
      suit $m \propto (L/r)^{3/2}$ et ce que cet exposant 3/2 dit de la sobriété
      du passif dans le grave.
      **Durée : 2 h.**
      **Fini quand** : tu sais les faire au tableau en 3 min chacun, sans notes.

- [ ] **3-J6. Préparer le sac : deux jeux de listings, convocation, pièce d'identité.**
      **Durée : 20 min.**
      **Rappel** : ni clé USB, ni ordinateur, ni enceinte, ni self, ni filtre. Le
      jury projette le PDF téléversé depuis **son** ordinateur. Tout ce qui n'est
      pas dans ce PDF n'atteindra jamais les examinateurs.
      **Fini quand** : le sac est fait la veille, pas le matin.

- [ ] **3-J7. Suivre la fin de l'épreuve : date de passage, fenêtre d'oraux,
      réclamation éventuelle.** **Durée : 20 min au total, étalées.**
      Trois choses, et elles ne sont écrites nulle part ailleurs :
      1. **La date de passage n'est connue qu'à partir de la mi-juin** (§ 08.4) —
      elle se consulte sur le site de la banque concernée, elle ne t'est pas
      envoyée à l'avance. À vérifier **le jour où elle paraît**, pas la veille.
      2. **La fenêtre d'oraux dépend de la filière déclarée en D9** : elle court
      jusqu'au **11 juillet** en PT et jusqu'au **18 juillet** en PSI `[[à
      vérifier]]` à la parution des Attendus. C'est une raison de plus de ne pas
      traiter D9 comme une formalité.
      3. **En cas de report de note ou d'anomalie, la réclamation se fait avant la
      fin juillet** — après, il n'y a plus de recours. Noter la date limite le jour
      de l'oral, pas en août.
      **Fini quand** : la date de passage est notée dès sa parution, et la date
      limite de réclamation est dans l'agenda.

---

### <a id="3k"></a>3-K. Risques : ce qui dérape, et ce qu'on coupe en premier

| Si… | Alors | Ce qu'on coupe |
|---|---|---|
| Le bobinage prend une demi-journée par self au lieu de 2 h | 4 selfs = 2 jours perdus | Passer aux **prises intermédiaires** : une bobine par voie au lieu de deux, ~4 h économisées, et la comparaison catalogue/optimisé se fait sur le **même objet physique**, donc sans biais de fabrication. **Conséquence à assumer, et à écrire au registre AVANT de basculer** : les critères n° 5 (coût marginal, mesuré sur factures) et n° 7 (encombrement / matière, mesuré à la balance) deviennent **calculés** — masse et prix de la fraction de bobine réellement utilisée par chaque design, selon une méthode écrite d'avance — et ils cessent d'être mesurés. Ce n'est pas rédhibitoire ; c'est un coût sur la conclusion, et il se déclare. |
| Le bobinage échoue, ou le calendrier dérape franchement | Pas de self maison | **Acheter une self à noyau de 18 mH** et faire de la comparaison air/noyau le satellite. Un échec de fabrication devient un résultat expérimental — c'est recevable, à condition de le dire. |
| Le temps manque en phase 4 | Il faut sacrifier quelque chose | **Le satellite « croisement énergétique » en premier** : c'est une seule mesure au wattmètre, réintégrable plus tard. La self, elle, reste : elle alimente le modèle de coût. |
| La porte ±5 % sur 8 Ω ne passe pas | Ne **pas** continuer vers l'acoustique | Diagnostiquer **dans cet ordre** : (1) **impédance de source** — la mesure est-elle bien faite à l'**amplificateur** et non au GBF ? 50 Ω en série détruisent le gabarit à eux seuls (§ 07.7), et c'est de loin la cause la plus fréquente ; (2) $L$ et $C$ sont-ils **mesurés** (`3-C5`, `3-C2`) ou nominaux ? (3) couplage entre selfs (`3-D1`) ? (4) la cible D2 du code est-elle bien celle qui a été gelée ? Une porte qui échoue pour une mauvaise raison coûte plus cher qu'une journée de diagnostic. |
| Les mesures ne départagent pas deux configurations | Ne pas trancher quand même | Écrire « non départagés » dans le tableau et **le dire à l'oral**. Un seuil de répétabilité assumé vaut mieux qu'un classement fabriqué. |
| L'encadrant n'a pas validé à J+6 de la fenêtre | Urgence absolue | Aller le voir physiquement, et prévenir le professeur référent TIPE du lycée. Rien d'autre dans cette liste ne mérite ce niveau d'insistance. |

> **Le vrai risque de cette période n'est aucun de ceux-là.** C'est que janvier à
> juin 2027, c'est aussi le semestre des concours. Le compte, poste par poste :
>
> | Bloc | Estimation |
> |---|---|
> | 3-A rappels + 3-B saisie SCEI | ~4 h |
> | **3-C selfs** | **15 à 20 h** (25 à 30 h sans outillage) |
> | 3-D montages | ~8 h |
> | **3-E campagnes** | **21 à 25 h** |
> | 3-F analyse et conclusion | ~4 h |
> | 3-G figures, PDF, listings | ~9 h 30 |
> | 3-H étape 2 + 3-I étape 3 | ~4 h |
> | 3-J répétitions | ~10 h |
> | **Total** | **~70 à 95 h**, soit **9 à 12 journées pleines** |
>
> C'est **plus du double de la période 2** (35 à 43 h), dans une fenêtre plus
> courte et plus chargée, plus les délais d'approvisionnement. Ça ne tient que si
> les selfs sont bobinées **avant** les vacances de février et si les mesures sont
> faites **avant** les concours blancs de printemps. Tout ce qui glisse après avril
> se retrouve compressé contre une clôture SCEI du 9-10 juin, qui, elle, ne bouge
> pas.

---

## <a id="T"></a>RÈGLES TRANSVERSES — du premier branchement à l'oral

Cette partie ne se range dans aucune période : elle s'applique **du premier
branchement jusqu'à l'oral**. Elle est ordonnée par dépendance, pas par thème.

> **Attention à sa place dans le document.** Elle est écrite ici, à la fin, pour
> ne pas hacher le fil des périodes — mais **onze de ses actions sont des
> prérequis de la période 1**, et elles sont appelées à ce titre par **`1-A0`** :
> `T-A1` à `T-A10`, `T-B1`, `T-B2`, plus `T-D1`, `T-D5` et `T-D11` à poser dès
> aujourd'hui. Chaque action qui en débloque une autre **porte son code** (« bloque
> `1-C4` », « débloque `1-D2` »), pour qu'on sache exactement ce qui attend quoi.
> Les cinq familles, dans leur ordre de morsure :

1. la **sécurité** d'abord, parce qu'elle conditionne la première séance de
   paillasse et qu'une erreur y est irréversible (un 18″ grillé, un multimètre
   détruit, une audition abîmée) ;
2. le **journal de bord** ensuite, parce qu'il doit exister *avant* la première
   mesure, sinon la première séance est perdue pour le DOT ;
3. la **règle des critères gelés**, qui mord à partir de la première mesure
   comparative ;
4. les **risques**, à relire une fois par mois, du premier au dernier jour ;
5. le **rythme de travail avec Claude**, qui court en permanence.

Durées : estimations de temps de travail **effectif**. Ni les colles, ni les DS,
ni les concours blancs, ni les vacances ne sont dans ce calcul. Une action de
« 2 h » peut occuper deux semaines de calendrier.

---

### <a id="ta"></a>T-A. Sécurité — à mettre en place avant la première séance

Rien de ce qui suit n'est un excès de prudence : chaque ligne vient d'un calcul
ou d'un constat déjà écrit dans `REFERENCE-TECHNIQUE.md` (§ 02.6, § 05.14,
§ 07.7, § 07.11). Les chiffres cités sont **calculés sur des modèles**, pas
mesurés sur ton enceinte : ils servent à dimensionner la prudence, pas à
conclure.

- [ ] **T-A1. Lire d'une traite le § 07.11 (Sécurité) et l'encadré « Borne basse du
      balayage » du § 02.6.** — 30 min. **Débloque** tout le reste de cette partie :
      les actions suivantes supposent que tu sais *pourquoi* ces règles existent,
      pas seulement qu'elles existent. *Fini quand* tu peux redire de mémoire les
      trois interdits : jamais sous l'accord au niveau fort, jamais le
      haut-parleur avant la résistance de puissance, jamais les doigts sur un
      condensateur non déchargé.

- [ ] **T-A2. Claude : rédiger la check-list papier de début de séance** (une page,
      recto, cases à cocher, ligne de date et de signature en bas). — action de
      Claude, ~45 min, à demander en une phrase. **Bloqué par** rien. **Débloque**
      **`1-D2`**, la séance d'étalonnage — et toute séance de banc ensuite. *Fini quand* le fichier existe dans le
      dépôt et tient sur **une** page imprimée. Contenu minimal, tiré des sections
      citées ci-dessus :
      - masses vérifiées (borne − de l'ampli ↔ châssis à l'ohmmètre, ampli
        éteint ; puis ≈ 0 V ampli allumé sans signal) — **jamais en mode pont**,
        interrupteur ground/lift sur *ground* ;
      - offset continu du GBF / de la carte son vérifié à zéro ;
      - bouchons d'oreilles en place, **y compris au niveau faible** ;
      - personne dans l'axe, aucune tête à moins de 1 m du 18″ ;
      - borne basse du balayage écrite **à la main** sur la feuille, avant de
        lancer quoi que ce soit ;
      - condensateurs déchargés avant toute manipulation du filtre ;
      - état de la LED limit/clip du E-800 à consigner pour chaque balayage.

- [ ] **T-A3. Imprimer la check-list en 15 exemplaires et la mettre dans le classeur de
      manip.** — 15 min. **Débloque** **`1-D2`**. *Fini quand* les feuilles sont
      physiquement dans le classeur, pas dans un dossier de téléchargement.
      Règle : **une feuille signée par séance**, agrafée au relevé de la séance.
      Une séance sans feuille signée est une séance dont les mesures ne servent à
      rien — tu ne pourras pas dire, six mois plus tard, dans quelles conditions
      elles ont été prises.

- [ ] **T-A4. Acheter les bouchons d'oreilles (atténuation annoncée sur l'emballage) et
      les ranger avec le micro.** — 15 min, quelques euros. **Bloque** **`1-E1`**
      et toute mesure acoustique. *Fini quand* ils sont dans la mallette. Motif chiffré :
      en champ proche, le § 07.11 prédit **112 dB SPL dès le niveau faible de
      0,5 W**, 125 dB à 10 W et 132 dB à 50 W — calcul fait pour une sensibilité
      *supposée* de 95 dB/2,83 V/m, donc un ordre de grandeur ; à ces niveaux, la
      question n'est pas de savoir si le chiffre est exact à 3 dB près.

- [ ] **T-A5. Relever $X_{max}$ et la sensibilité du 18″ sur sa fiche constructeur, et
      le SPL maximal de la capsule du micro de mesure.** — 30 min. **Bloque**
      **`1-C4`** (le gel de D3, les deux niveaux d'écoute) et la borne haute du
      niveau « fort ».
      *Fini quand* les trois nombres sont écrits, avec leur source, dans
      `DECISIONS-PHASE-0.md`. Point important : c'est très probablement **le micro
      qui plafonnera le niveau fort**, pas l'enceinte.

- [ ] **T-A6. Écrire en tête du journal la règle de la borne basse, dans ses deux
      versions, et ne plus jamais la reconstituer de mémoire.** — 20 min.
      **Débloque** **`1-E2`, `1-E3` et `1-E4`** (la campagne d'impédance), et
      **borne `3-E11`/`3-E13`** au niveau fort. Les deux règles sont recopiées **au
      point d'usage**, sur ces actions : une consigne de sécurité écrite à
      1 300 lignes du geste n'est pas une consigne de sécurité. *Fini quand* les
      deux lignes sont au cahier :
      - **mesure d'impédance à 100–200 mV** : le balayage **descend à 10 Hz et il
        le doit** — c'est cette zone qui porte le pic bas $f_L$. Excursion prédite
        à 10 Hz sous 150 mV : environ 0,09 mm (modèle, § 02.6), plus de cinquante
        fois moins que le $X_{max}$ de tout 18″ de sonorisation.
        Aucun risque ;
      - **toute mesure au niveau fort** (acoustique, robustesse, écoute) :
        **interdiction de descendre sous $f_b$**, `Start` $\ge 2f_b$ dans REW,
        avec le $f_b$ **mesuré en phase 1** (passage par zéro de la phase entre
        les deux pics, ou ajustement) — pas une valeur de catalogue, pas une
        estimation. Tant que $f_b$ n'est pas mesuré :
        **aucun balayage lent au niveau fort**, point final. La prédiction de
        Helmholtz (§ 01.10 bis) donne une borne provisoire, pas une autorisation.

- [ ] **T-A7. Geler l'ordre des campagnes, du moins destructif au plus destructif, et
      l'afficher au mur de l'espace de manip.** — 20 min. **Débloque** **`1-E2`**
      et l'ordre de tout le bloc `3-E`. *Fini quand* la liste est écrite et
      qu'aucune séance ne saute une marche :
      1. étalonnage sur composants **connus** (résistance étalon, condensateur,
         self) — rien ne peut casser ;
      2. impédance **petit signal** (150 mV) du sub puis du bloc médiums —
         descente à 10 Hz autorisée ;
      3. filtre **sur résistance de puissance 8 Ω** — le haut-parleur n'est pas
         dans le circuit ;
      4. filtre **sur haut-parleur réel**, mesures électriques ;
      5. acoustique **au niveau faible** ;
      6. acoustique **au niveau fort**, bornée à $2f_b$ ;
      7. robustesse **bobine chaude** — le geste le plus agressif, en dernier.

      Règle transverse : **toujours du faible vers le fort, toujours la
      résistance avant le haut-parleur.**

- [ ] **T-A8. Relever la valeur du condensateur de chaque pavillon, et l'écrire.**
      — 30 min (démontage du bornier compris). Sa **présence** est acquise
      (constat du 16/09/2026) ; sa **valeur** reste `[[à mesurer]]`.
      **Débloque** ce qu'on s'attend à lire sur le bloc médiums en `1-E4`
      (29,3 Ω ramenés à 26,3 – 21,8 Ω à 100 Hz pour 3,3 à 10 µF, calculé) et
      **borne `3-E11`**.
      *C'est la même action que la dernière ligne du tableau de `1-A4`* : y
      répondre une fois suffit — coche les deux.
      *Fini quand* la valeur lue sur chaque composant est notée dans
      `DECISIONS-PHASE-0.md` (D8). Contrôle de câblage à faire en même temps
      (livret, B1 bis) : à l'ohmmètre, le bloc médiums doit lire environ 6 à
      7 Ω en continu ; une lecture de 2 à 3 Ω trahirait un pavillon sans
      condensateur, incohérent avec le constat — ouvrir le bornier avant toute
      suite. La mesure d'impédance à 150 mV, elle, est sans risque.

- [ ] **T-A9. Dimensionner les condensateurs du filtre en tension alternative
      permanente, pas en tension d'ampli.** — 30 min de lecture, puis c'est une
      contrainte d'achat. **Bloque** **`2-I1`** (la liste d'achats, mi-décembre) et
      **`3-C2`** (le contrôle à réception). Le chiffre est recopié en dur dans
      `2-I1` : c'est là qu'il sert, et un condensateur sous-dimensionné acheté en
      décembre se rachète en janvier, dans le meilleur des cas.
      *Fini quand* la règle est écrite dans la liste d'achats. Le calcul du
      § 07.11 : le réseau LC **surtensionne** le composant shunt d'un facteur qui
      suit $|Z|$ de la charge (×2,8 à 30 Ω, ×4,6 à 50 Ω, ×5,5 à 60 Ω, sur
      18 mH/150 µF). À 20 V RMS d'entrée et sur un pic à 50 Ω, cela fait **92 V
      RMS, soit 130 V crête** aux bornes d'un condensateur. Tant que $Z(f)$ n'est
      pas mesurée : marge **×6**, donc condensateurs spécifiés au moins **250 V DC
      / 160 V AC** — et vérifier que la spécification lue est bien la tenue
      **alternative permanente** (sur un MKP, « 100 V » est presque toujours du
      continu ; l'alternatif permanent tourne autour de 60–65 V RMS). Bonus
      d'oral : cette surtension est *la* traduction la plus parlante de « le
      catalogue 8 Ω ne décrit pas la charge réelle ».

- [ ] **T-A10. Prévoir la diode de roue libre (1N4007) avant la première mesure de DCR
      en quatre fils.** — 10 min, quelques centimes. **Bloque** **`3-C6`** (la
      mesure de $r$ des selfs). Les trois gestes sont recopiés dans `3-C6`
      lui-même : c'est là qu'ils s'exécutent, et cette action-ci n'est plus qu'un
      **rappel d'achat**. *Fini quand* la diode est dans la mallette et que la
      consigne est au cahier : couper 1 A dans 18 mH en quelques microsecondes
      produit **plusieurs centaines de volts** aux bornes de la self. On établit et
      on coupe le courant **progressivement à l'alimentation**, diode en
      antiparallèle pendant la mesure, et **le voltmètre se débranche en
      dernier**. C'est le genre de détail qui coûte un multimètre au lycée — et le
      multimètre n'est pas le tien.

---

### <a id="tb"></a>T-B. Le journal de bord — à ouvrir avant la première mesure

Le journal n'est pas de la bureaucratie : c'est **la matière première du DOT**
(4 à 8 jalons factuels de 50 mots maximum, strictement chronologiques,
difficultés comprises) et **la preuve du travail personnel** que ton professeur
encadrant atteste à l'étape 3. Sans lui, tu réécriras en mai 2027, de mémoire,
ce que tu as fait en octobre 2026 — et ça se verra.

- [ ] **T-B1. Ouvrir un cahier papier dédié (pas un carnet partagé avec les DS) et y
      coller la règle d'en-tête de séance.** — 30 min. **Bloqué par** rien.
      **Débloque** **`1-D2`**, la première séance : une mesure prise sans en-tête
      est une mesure inexploitable. La ligne « configuration (A, B ou C) » suppose
      que **`1-B5`** a tranché — l'en-tête ne se remplit pas au fil de l'eau. *Fini quand* la première page porte le gabarit d'en-tête du
      § 02.12 : date · dipôle mesuré · configuration (A, B ou C) · $R_{ref}$
      nominale **et mesurée** · tableau des $\kappa$ par couple de calibres ·
      convention sur la voie voisine · température · $R_e$ continu avant et après ·
      modèle d'oscillo et de GBF avec leurs réglages.

- [ ] **T-B2. Adopter la règle des colonnes brutes : on note ce qu'on lit, jamais ce
      qu'on calcule.** — 15 min pour l'intégrer. **Débloque** la reconstruction
      des incertitudes en phase 2. *Fini quand* le cahier ne contient **aucune**
      colonne $|Z|$, $\varphi$ ou incertitude : rien que fréquence lue avec toute
      sa résolution, calibres, **nombre de divisions occupées par chaque voie**,
      niveau GBF, $V_{CH1}$, $V_{CH2}$, $\Delta t$ **avec son signe**. Le nombre de
      divisions est la colonne qu'on oublie et sans laquelle l'incertitude de gain
      n'est pas reconstructible a posteriori.

- [ ] **T-B3. Ajouter à chaque séance les quatre lignes qui ne sont pas des mesures.** —
      10 min par séance, à vie. **Débloque** la rédaction du DOT en 2027. *Fini
      quand* c'est un réflexe. Les quatre lignes :
      1. **ce que je cherchais à établir aujourd'hui** (une phrase, écrite *avant*
         de brancher) ;
      2. **ce qui n'a pas marché** — panne, résultat aberrant, manip refaite.
         C'est la ligne la plus précieuse : le SCEI demande explicitement les
         « réalisations infructueuses, surmontées ou non » dans le DOT, et un jury
         valorise une difficulté racontée ;
      3. **ce que j'ai décidé et pourquoi** (changement de $R_{ref}$, de grille, de
         niveau) ;
      4. **ce que je fais la prochaine fois.**

- [ ] **T-B4. Instaurer les trois points de contrôle de début de séance.** — 15 min par
      séance. **Débloque** l'affirmation honnête, en phase 4, qu'un écart mesuré
      est un effet et non une dérive de la chaîne. *Fini quand* chaque séance
      commence par refaire **trois points** (un sur le plateau, un au pic, un en
      haut de bande) et les comparer à la séance précédente par $E_n$.

- [ ] **T-B5. Archiver les relevés bruts à côté des CSV dépouillés, sous le même nom.** —
      10 min par séance. **Débloque** la phase 2 : le fit y est pondéré par
      $1/u^2$, donc les colonnes d'incertitude entrent dans le calcul, elles ne
      sont pas décoratives. *Fini quand* chaque CSV dépouillé a son brut jumeau et
      que le nommage suit `AAAA-MM-JJ_...`.

- [ ] **T-B6. Photographier chaque montage avant de le défaire.** — 2 min par montage.
      **Débloque** les planches d'oral et, en cas de désaccord entre deux séances,
      le diagnostic. *Fini quand* la photo est dans `assets/` avec sa date.

- [ ] **T-B8. Sauvegarder : photographier les pages du cahier, et sortir les mesures
      de ta machine le soir même.** — 5 min par séance. **Débloque** ta capacité à
      survivre à l'incident le plus banal du projet. *Fini quand* c'est un réflexe,
      avec **trois copies** : le cahier papier, les photos de ses pages dans
      `assets/journal/` (nommées `AAAA-MM-JJ_pNN.jpg`), et les CSV **poussés dans le
      dépôt Git le soir de la séance**, pas « à la fin de la campagne ».
      *Pourquoi cette ligne existe* : le cahier de bord est **unique** (`T-B1`), et
      ce document en fait à la fois la matière première du DOT et la preuve du
      travail personnel que l'encadrant atteste en juin. Le tableau des risques a
      deux pages de parade pour un haut-parleur grillé ; une clé USB perdue ou un
      cahier oublié dans un train est **au moins aussi probable**, et n'en avait
      aucune. Un dépôt Git poussé, c'est déjà une sauvegarde hors machine :
      l'essentiel est de **pousser**, pas seulement de commiter.

- [ ] **T-B7. Claude : à chaque fin de campagne, transformer les entrées du cahier en
      brouillons de jalons DOT (50 mots max, factuels, chronologiques).** — action
      de Claude, ~30 min par campagne, à partir d'une photo ou d'une recopie de tes
      pages. **Débloque** l'étape 2 SCEI (fin févr. → début juin 2027). *Fini
      quand* le dépôt contient un fichier de jalons candidats, dont tu retiendras 4
      à 8 le moment venu. Le pivot v1 → v2 du 4 août 2026 y a toute sa place :
      c'est un jalon, pas une faute à cacher.

---

### <a id="tc"></a>T-C. La règle des critères gelés

C'est la seule faute réellement disqualifiante de ce projet, et elle est
invisible dans un rapport : **changer une décision après avoir vu les mesures**,
c'est choisir le vainqueur puis écrire le règlement. `DECISIONS-PHASE-0.md`
existe précisément pour rendre cette faute impossible — ou, si elle est commise,
visible et datée.

- [ ] **T-C1. Relire « La règle du jeu » en tête de `DECISIONS-PHASE-0.md` et la
      signer.** — 20 min. **Débloque** la suite de cette section. *Fini quand* ta
      signature et la date sont au bas du paragraphe.

- [ ] **T-C2. Retenir l'échéance de D4 (les huit critères) et D5 (bande et
      pondérations) : avant la première mesure comparative, et de préférence avant
      la phase 3.** — la décision elle-même est traitée dans les lots de phase ;
      ici, seule l'échéance compte. **Bloque** toute la conclusion du TIPE. *Fini
      quand* les deux entrées portent une date et des initiales, et que
      `analyse/criteres_geles.json` ne porte plus la marque `[[a geler]]` sur les
      champs correspondants.

- [ ] **T-C3. Appliquer les quatre interdits, à partir de la première mesure
      comparative.** — 0 min, c'est une discipline. **Débloque** une conclusion
      défendable. *Fini quand* tu peux répondre « non » aux quatre questions :
      - ai-je **ajouté ou retiré un critère** après avoir vu une courbe ?
      - ai-je **déplacé la bande** (40–250 Hz) ou une pondération de la fonction de
        coût après coup ?
      - ai-je **changé un niveau d'écoute** entre deux filtres comparés ?
      - ai-je **changé la cible de sommation** après avoir vu laquelle des deux
        flattait le filtre optimisé ?

- [ ] **T-C4. Si une décision doit vraiment changer : la changer proprement plutôt que
      silencieusement.** — 30 min le jour où le cas se présente. **Débloque** le
      droit d'en parler au jury comme d'une force. *Fini quand* le changement est
      (a) inscrit dans le *Journal des modifications* de `DECISIONS-PHASE-0.md`,
      (b) daté, (c) justifié **par un argument qui n'est pas le résultat obtenu**,
      et (d) noté sur la fiche « à dire à l'oral ». Formulation qui marche : « j'ai
      changé de critère en novembre parce que j'ai compris qu'il ne mesurait pas
      l'effet étudié » — c'est de l'esprit critique. Formulation qui coule : « j'ai
      élargi la bande parce que le résultat était meilleur ».

- [ ] **T-C5. Écrire, dès maintenant et avant toute mesure, la phrase de conclusion
      défavorable.** — 30 min. **Débloque** ta sérénité pour les six mois qui
      suivent, et neutralise la tentation de bricoler les critères. *Fini quand* la
      phrase est au cahier, datée. Quelque chose comme : « si le filtre optimisé ne
      bat pas le filtre catalogue de plus que la dispersion de mes mesures, je le
      dirai, et j'expliquerai pourquoi — un optimum plat est un résultat sur la
      fonction de coût, pas un échec de la méthode. » Le § 07 fixe déjà le
      garde-fou chiffré correspondant : **deux filtres séparés par moins de
      $2{,}3\,s$ (où $s$ est l'écart-type des répétitions) ne sont pas départagés,
      et on le dit.**

- [ ] **T-C6. Préparer la réponse à la question « et si vous aviez trouvé le
      contraire ? ».** — 20 min, au moment des répétitions. **Débloque** les 15 min
      d'entretien. *Fini quand* la réponse tient en trois phrases et s'appuie sur
      le registre daté : la question est un test d'honnêteté, et le registre est la
      preuve matérielle que la réponse n'est pas de circonstance.

---

### <a id="td"></a>T-D. Les risques et leurs parades

Une ligne par risque : le **signe avant-coureur** (ce que tu verras en premier),
la **parade**, et **ce qu'on coupe en premier** si la parade ne suffit pas. À
relire en dix minutes le premier week-end de chaque mois.

#### R1 — Le calendrier glisse et le MCOT arrive avant les résultats

- **Signe avant-coureur** : une phase déclarée « presque finie » depuis plus de
  trois semaines. La phase 0 a déjà glissé d'un mois (août → août-sept. 2026), ce
  qui pousse la phase 3 sur janvier 2027, c'est-à-dire **sur la fenêtre de saisie
  de l'étape 1** (mi-janvier → début février). La marge, d'un bon mois à
  l'origine, tient aujourd'hui en quelques jours.
- **Parade** : le texte du MCOT **ne dépend d'aucun résultat** — problématique,
  objectifs, ancrage et bibliographie sont déjà décidés. Le rédiger **dès décembre
  2026**, en parallèle de l'optimisation, et non à la fin de la phase 3.
- **Ce qu'on coupe en premier** : le satellite « croisement énergétique » (une
  seule mesure, réintégrable plus tard sans rien casser). L'étude de la self, en
  revanche, **ne se coupe pas** : elle alimente le modèle de coût, donc la
  fonction objectif elle-même.

- [ ] **T-D1. Bloquer trois demi-journées « MCOT » dans l'agenda de décembre 2026, dès
      aujourd'hui.** — 10 min maintenant, 3 × 4 h en décembre. **C'est un prérequis
      de la période 1**, appelé par **`1-A0`** : les dix minutes se prennent
      aujourd'hui, pas en décembre. **Débloque** `2-J1` à `2-J9`, donc l'étape 1
      SCEI. *Fini quand* les créneaux sont dans ton agenda avec une alarme, pas
      dans ta tête.
- [ ] **T-D2. Vérifier les dates 2027 réelles à la parution des Attendus 2026-2027 sur
      scei-concours.fr/tipe.html.** — 20 min, à la rentrée puis une fois par mois
      jusqu'à parution. **Débloque** tout le calendrier aval. *Fini quand* les
      trois dates de clôture (étapes 1, 2, 3) sont notées, sourcées et datées dans
      `FEUILLE-DE-ROUTE.md`. Les clôtures sont stables depuis des années (étape 1 :
      5-6 févr. ; étape 2 : 9-10 juin ; étape 3 : ~19 juin) ; ce sont les
      **ouvertures** qui bougent.

#### R2 — L'enceinte est unique et en service : un haut-parleur grillé arrête tout

- **Signe avant-coureur** : un bruit mécanique sec pendant un balayage, une odeur
  de vernis chaud, un $R_e$ continu qui ne revient pas à sa valeur de départ après
  refroidissement, une LED limit/clip qui s'allume.
- **Parade** : c'est **toute la section T-A**. Les trois gestes qui
  comptent : borne basse $\ge 2f_b$ au niveau fort, ordre des campagnes du moins
  au plus destructif, contrôle visuel du débattement avant chaque balayage fort.
  Ajouter : **mesurer $R_e$ avant et après chaque balayage fort** — un balayage de
  5,5 s à 50 W injecte 273 J dans la bobine (calcul du § 07).
- **Ce qu'on coupe en premier** : le **test de robustesse bobine chaude**. C'est le
  seul protocole du projet qui consiste délibérément à échauffer le haut-parleur ;
  s'il faut renoncer à un critère pour ne pas risquer l'enceinte, c'est celui-là,
  et on l'assume à l'oral en expliquant ce qu'il aurait mesuré.

- [ ] **T-D3. Écrire le plan B « si un haut-parleur meurt » avant qu'il meure.** —
      45 min. **Débloque** ta capacité à réagir en une semaine au lieu d'un mois.
      *Fini quand* trois lignes sont au cahier : (i) quelles mesures sont déjà
      archivées et donc sauvées — d'où l'archivage systématique de la section T-B ;
      (ii) le récit de repli, où le TIPE devient « ce que j'ai mesuré avant
      l'incident, plus l'optimisation sur ces données », ce qui reste un sujet
      complet ; (iii) le coût et le délai de remplacement d'un médium (le moins
      cher des trois), à distinguer de ceux du 18″.
- [ ] **T-D4. Traiter les médiums avec plus de précaution que le sub.** — 0 min, c'est
      une règle. *Fini quand* elle est au cahier : **les médiums ne se mesurent
      jamais en pleine bande au niveau fort sans passe-haut**. Leur réponse brute
      se relève au niveau faible, point.

#### R3 — Le matériel du lycée n'est pas disponible quand tu en as besoin

- **Signe avant-coureur** : la salle de TP fermée pour cause de DS, l'oscillo
  réquisitionné, la résistance de puissance introuvable.
- **Parade** : la chaîne de mesure a **deux voies indépendantes** — GBF + oscillo
  (lycée) et carte son + REW (perso). Elles doivent de toute façon se recouper :
  c'est une porte de validation, pas un luxe. Donc *une* voie indisponible
  ralentit, elle ne bloque pas.
- **Ce qu'on coupe en premier** : le recoupement systématique des deux méthodes sur
  **tous** les points. On le garde sur les points clés (plateau, pic, creux,
  100 Hz) et on l'annonce comme tel.

- [ ] **T-D5. Faire l'inventaire du matériel du lycée dès la rentrée, avec un nom en face
      de chaque objet.** — 1 h sur place. **C'est `1-B1` vu sous l'angle du
      risque** : une seule action, deux codes, une seule case à cocher — fais-la
      là-bas, coche ici. **Bloque** **`1-B4`** (la liste d'achats) et **`1-B5`**
      (le choix du montage). *Fini quand* tu sais : modèle de l'oscillo et son nombre de voies,
      modèle du GBF, existence ou non d'une résistance de puissance 8 Ω (sinon elle
      passe sur ta liste d'achats), et **qui** ouvre la salle.
- [ ] **T-D6. Demander, dans le même mouvement, un créneau récurrent plutôt qu'un accès
      au coup par coup.** — 15 min. **Débloque** la régularité des séances, donc la
      répétabilité inter-séances. *Fini quand* un jour et une heure sont convenus
      avec un enseignant.

#### R4 — Le budget part entièrement dans le cuivre

- **Signe avant-coureur** : tu commences à comparer des prix de fil émaillé sans
  avoir gelé $r_{max}$. C'est le symptôme exact du problème : **le prix d'une self
  n'est pas une donnée, c'est une conséquence de $r_{max}$**, via
  $m = K_{Cu}(L/r)^{3/2}$.
- **Chiffres du § 05.10** (cuivre seul, **pour un couple de selfs de 18 mH**, sur
  une base de 25 €/kg encore `[[à confirmer par devis]]`) : **212 € à 1 Ω ; 116 €
  à 1,5 Ω ; 75 € à 2 Ω ; 41 € à 3 Ω**. La fenêtre praticable est 1,5 à 2 Ω, soit
  **75 à 116 € par filtre**, à doubler pour les deux filtres comparés. Sur 500 €,
  ça passe, mais sans place pour une erreur — et si D2 tombe sur la cible plate
  (LR2), les selfs passent de 18 à 27 mH, soit **+84 % de cuivre par self**.
- **Parade** : les **prises intermédiaires** (§ 05.10). Une seule bobine par voie,
  avec une prise, fournit la valeur catalogue *et* la valeur optimisée. Cuivre,
  prix et temps de bobinage divisés par deux — et, argument scientifique bien
  supérieur à l'argument comptable, **la comparaison se fait sur le même objet
  physique**, donc sans biais de fabrication.
- **Ce qu'on coupe en premier** : les condensateurs film, remplacés par des
  électrolytiques bipolaires sur les prototypes ; le film est réservé à la version
  finale si le budget le permet.

- [ ] **T-D7. Ne jamais laisser le devis choisir $r_{max}$.** — la décision est D6
      (`2-F2`) ; ici, seul l'**ordre de causalité** compte, pas la chronologie.
      — 0 min. **Bloque** tout achat de cuivre (`2-I1`).
      *La distinction qui lève l'ambiguïté avec `1-C6`* : **demander un prix au
      kilo est une donnée d'entrée légitime de D6** — il faut bien connaître le
      prix du cuivre pour arbitrer, et `1-C6` le fait dès octobre, à dessein. Ce
      qui est interdit, c'est l'inverse : **partir du budget disponible pour en
      déduire $r_{max}$**. Le prix d'une self n'est pas une donnée, c'est une
      **conséquence** de $r_{max}$, via $m = K_{Cu}(L/r)^{3/2}$ ; le signe que ça
      dérape, c'est une phrase du type « je prendrai ce que le budget permet ».
      *Fini quand* D6 porte une date **et** un motif qui n'est pas un prix. Piège
      documenté : annoncer « 25 € la self »
      revient à acheter 1 kg de cuivre, donc $r \approx 2{,}6\ \Omega$, donc
      **−2,5 dB d'insertion** et une dérive thermique qui fait **échouer le critère
      de robustesse par construction**. Ce n'est pas une économie, c'est un
      résultat négatif acheté d'avance.
- [ ] **T-D8. Rappel — c'est `1-C6`, et il n'y en a qu'un.** Les deux devis réels de
      fil émaillé se demandent **début octobre**, une seule fois ; aucune autre
      action du parcours ne redemande de devis (`3-C1` est devenue la *réception*
      de la commande). — 2 min de vérification. **Débloque** la ligne budgétaire et
      le chiffrage de `2-F1`/`2-F2`. *Fini quand* les deux prix au kilo sont
      notés avec leur date et leur fournisseur, et que la base « 25 €/kg » du
      § 05.10 est confirmée ou corrigée dans le document — **sinon, retour à
      `1-C6`**.

#### R5 — Le résultat est indécidable parce que l'optimum est plat

- **Signe avant-coureur** : en phase 3, plusieurs couples E12 très différents
  donnent des coûts $J$ à quelques pour cent les uns des autres.
- **Ce n'est pas un échec** : c'est une propriété de la fonction de coût, et un
  résultat à part entière. Un jury préfère « l'optimum est plat, voici la carte du
  coût et voici pourquoi » à un vainqueur désigné à 0,2 dB près.
- **Parade** : la préparer en amont, pas le jour où elle arrive. (i) Tracer la
  **carte de $J$** sur la grille E12 plutôt que d'annoncer un point unique ;
  (ii) appliquer la règle des $2{,}3\,s$ — deux filtres plus proches que cela ne
  sont pas départagés ; (iii) si l'optimum est plat, **choisir dans le plateau
  selon un critère secondaire annoncé à l'avance** (le moins de cuivre, par
  exemple) et le dire.
- **Ce qu'on coupe en premier** : rien. Au contraire, c'est le moment d'ajouter une
  planche d'oral — la carte de coût est plus intéressante que le point optimal.

- [ ] **T-D9. Claude : produire la carte de $J$ sur la grille E12 et l'analyse de
      sensibilité en même temps que le design optimisé, pas après.** — action de
      Claude, ~1 h une fois les paramètres Thiele-Small disponibles. **Débloque**
      la planche d'oral « optimum plat ». *Fini quand* la figure existe au gabarit
      4/3 et que le rapport entre le meilleur $J$ et le dixième meilleur est
      chiffré.

#### R6 — La 2e année mange tout le temps disponible

- **Signe avant-coureur** : trois semaines sans une ligne au journal. C'est le seul
  indicateur fiable, et il est objectif — une raison de plus de tenir le journal.
- **Parade** : des séances **courtes et fréquentes** plutôt que des journées
  entières rares (une séance de 2 h qui produit trois points exploitables vaut
  mieux qu'une journée de 8 h reportée quatre fois). Et surtout : **le travail
  d'analyse et de rédaction se délègue à Claude, la mesure non**. Ton temps rare
  doit aller à la paillasse et aux décisions.
- **Ce qu'on coupe en premier**, dans l'ordre : (1) le croisement énergétique ;
  (2) la contre-vérification LTspice systématique — on la garde sur un cas ;
  (3) le second filtre physique, en basculant sur la solution à **prise
  intermédiaire** ; (4) le test de robustesse bobine chaude. On ne coupe **jamais**
  la phase 1 ni sa porte de validation d'étalonnage : sans elles, il n'y a pas de
  sujet.

- [ ] **T-D10. Poser une revue mensuelle de 20 min : relire cette partie, cocher ce qui est
      fait, dire à voix haute ce qui a glissé.** — 20 min par mois. **Débloque** la
      détection précoce de R1 et R6. *Trois gestes d'écriture à chaque revue, et
      ils tiennent en cinq minutes* :
      1. réécrire la ligne **« Où j'en suis »** en tête du document (date de la
         revue, bloc en cours, prochaine échéance ferme) ;
      2. réécrire **« Les trois actions du moment »** — sans quoi elle reste datée
         du 16/09/2026 et devient trompeuse dès novembre ;
      3. reporter dans la **vue mois par mois** ce qui a réellement été fait, et
         corriger les heures si l'estimation s'est révélée fausse (c'est
         explicitement demandé pour le bobinage, `3-C4`).
      *Fini quand* la date de la revue suivante est
      dans l'agenda, chaque fois, avant de refermer le cahier.

#### R7 — Pas d'encadrant validé à la mi-juin 2027

- **Signe avant-coureur** : on est en novembre et personne n'a dit « oui » par
  écrit.
- **Conséquence** : sans encadrant déclaré à l'étape 1 et **sans sa validation à
  l'étape 3 — une fenêtre de huit jours à la mi-juin 2027 — la note peut être
  zéro.** C'est le seul risque du projet qui annule tout le reste, quelle que soit
  la qualité du travail.
- **Parade** : demander **dès la rentrée**, vérifier qu'il a bien un compte sur
  `lycees.scei-concours.fr`, et lui rappeler la fenêtre de juin **deux fois** : en
  janvier à la saisie de l'étape 1, et début juin au téléversement du PDF.
  **État au 23/09/2026 : accord obtenu le 16/09/2026 (M. Chevalier, `1-A2`)** ;
  le compte SCEI et l'avertissement sur la fenêtre de juin restent à faire
  (`1-A3`). La mention de N. Cavallo dans un commit de juin 2026 est caduque.
- **Ce qu'on coupe en premier** : rien. C'est la seule action du projet qui n'a
  aucun repli.

- [ ] **T-D11. Mettre trois rappels d'agenda aujourd'hui : « vérifier le compte
      SCEI de l'encadrant » (prochaine rencontre avec M. Chevalier → `1-A3` ;
      `1-A2` est fait depuis le 16/09/2026), « confirmer son compte SCEI »
      (janvier 2027 → `3-A5`),
      « fenêtre de validation » (1er juin 2027 → `3-I1`).** — 10 min, **à faire
      aujourd'hui** : c'est un prérequis de la période 1, appelé par `1-A0`.
      **Débloque** la sérénité sur R7.
      *Fini quand* les trois alarmes existent.

---

### <a id="te"></a>T-E. Le rythme de travail avec Claude

Le partage est simple et ne bouge pas : **tu mesures et tu décides, Claude calcule
et rédige.** Claude ne peut rien produire d'honnête sans deux choses que toi seul
apportes — des **données** et des **décisions datées**.

- [ ] **T-E1. Adopter la règle d'entrée : ne jamais revenir voir Claude « pour avancer »,
      mais avec un livrable.** — 0 min, c'est une discipline. *Fini quand* tu peux
      nommer, avant d'ouvrir une session, ce que tu apportes : un CSV, une décision
      signée, une photo de montage, une question précise. Une session ouverte sans
      apport produit de la documentation, pas du TIPE — et il y en a déjà beaucoup.

- [ ] **T-E2. Revenir après chaque campagne de mesure, avec le CSV brut et les pages du
      cahier.** — 15 min pour préparer l'envoi. **Débloque** le dépouillement. *Ce
      que Claude fait alors* : lecture et contrôle de format, propagation des
      incertitudes, tracés au gabarit 4/3, contrôles de cohérence (en bas de bande
      $|Z|$ décroît vers $R_e$ **sans l'atteindre** ; $\varphi = 0$ au sommet du
      pic ; recoupement 10 Ω / 100 Ω par $E_n$), puis le brouillon de jalon DOT.
      *Fini quand* les figures sont dans le dépôt et que le journal Python porte la
      date et l'empreinte SHA-256 du run.

- [ ] **T-E3. Revenir après chaque décision gelée, pour la propager.** — 10 min.
      **Débloque** la cohérence du dépôt. *Ce que Claude fait alors* : reporter la
      décision dans `analyse/criteres_geles.json`, retirer les marques
      `[[a geler]]` correspondantes, et **mettre à jour tous les documents qui
      citaient la question comme ouverte**. Règle : une décision se cite, elle ne
      se redéfinit pas. *Fini quand* une recherche sur l'ancienne formulation ne
      renvoie plus rien hors `archive-v1/`.

- [ ] **T-E4. Revenir quand une manip échoue — tout de suite, pas une fois réparée.** —
      20 min. **Débloque** un diagnostic à deux têtes pendant que le montage est
      encore câblé. *Fini quand* la cause probable est écrite au cahier avec ce
      qu'il faudra vérifier à la séance suivante. Un échec raconté le jour même
      vaut un jalon DOT ; un échec reconstitué trois mois plus tard vaut une phrase
      vague.

- [ ] **T-E5. Confier à Claude, pendant que tu révises, tout ce qui ne demande ni mesure
      ni décision.** — 0 min de ton côté, c'est le but. Ce qui est délégable sans
      risque :
      - contrôles et extensions du code d'analyse, tests de non-régression ;
      - figures et leur injection dans les diapositives ;
      - rédaction des textes SCEI (MCOT : 50 + 50 + 50 + 100 + 650 mots ; DOT : 4 à
        8 jalons de 50 mots) — **à partir de tes décisions**, jamais à leur place ;
      - veille sur les dates des Attendus 2027 et mise à jour du calendrier ;
      - refonte des supports et export PDF sous le plafond de 5 Mo ;
      - préparation des questions du jury dans `NOTES-TIPE.md`.

      *Fini quand* tu as pris l'habitude de terminer une session par « pendant que
      je révise, tu peux… ».

- [ ] **T-E6. Interdire à Claude — et t'interdire — de combler un `[[à mesurer]]` par une
      estimation.** — 0 min, c'est la règle fondatrice du projet. *Fini quand* tu
      sais la justifier au jury : le rapport $\max|Z|/\min|Z|$ ne sera écrit nulle
      part avant d'être mesuré, et c'est exactement pour cela que la problématique
      ne porte aujourd'hui aucun chiffre. Un chiffre non mesuré qui traîne dans un
      document finit toujours par être cité à l'oral comme s'il avait été mesuré.

- [ ] **T-E7. Faire relire par Claude, une fois par trimestre, la cohérence du dépôt
      contre `DECISIONS-PHASE-0.md`.** — action de Claude, ~1 h, sur demande.
      **Débloque** la détection des contradictions résiduelles — il en reste : la
      cible de sommation, par exemple, est encore écrite « plate » à un endroit et
      « Butterworth » à un autre, tant que D2 n'est pas gelée. **À traiter dans la
      même passe, dès la première relecture** : le **calendrier de
      `FEUILLE-DE-ROUTE.md` n'est pas celui de ce document** (phase 2 en octobre
      là-bas, en novembre ici ; phase 4 en décembre là-bas, en février ici). La
      table de correspondance est en tête de la période 1 ; la feuille de route,
      elle, n'a pas encore été réalignée. *Fini quand* le
      relevé d'écarts est remis, et chaque écart corrigé ou daté comme
      volontairement ouvert.

---

## <a id="cinq"></a>Si tu ne devais retenir que cinq choses

1. **L'encadrant avant tout le reste.** C'est le seul point du parcours qui peut
   coûter l'épreuve entière quelle que soit la qualité du travail, il n'a aucun
   repli, et il coûte dix minutes aujourd'hui puis deux relances — une en janvier,
   une en juin, dans une fenêtre de huit jours que personne ne te rappellera.
2. **On ne mesure pas un objet inconnu avec un instrument inconnu.** La chaîne se
   qualifie d'abord sur des composants dont tu connais la valeur ; tant que cette
   porte n'est pas franchie, le haut-parleur ne se branche pas, et les
   19 319 lignes de Python du dépôt ne décrivent rien de réel. Et la chaîne
   **acoustique** compte autant que l'électrique : c'est `1-D6`.
3. **Une décision se gèle avant de voir les courbes, et se change au grand jour ou
   pas du tout.** Ajouter un critère, déplacer une bande ou changer la cible de
   sommation après coup, c'est choisir le vainqueur puis écrire le règlement : la
   seule faute réellement disqualifiante du projet, et la seule qui soit invisible
   dans un rapport — d'où le registre daté.
4. **Aucun chiffre n'entre dans un document avant d'être mesuré.** C'est pour cela
   que la problématique ne porte aujourd'hui aucun rapport $\max|Z|/\min|Z|$ ; un
   nombre estimé qui traîne quelque part finit toujours par être cité à l'oral
   comme s'il avait été mesuré.
5. **Ton temps rare va à la paillasse et aux décisions ; le calcul et la rédaction
   se délèguent.** Tiens le journal à chaque séance — c'est le seul indicateur
   objectif que le projet avance, la matière première du DOT, et ce qui fait la
   différence entre un travail raconté et un travail reconstitué de mémoire six
   mois plus tard.

---

*Fin du parcours. Les phases et leur justification scientifique sont dans
`FEUILLE-DE-ROUTE.md` et `REFERENCE-TECHNIQUE.md` ; les décisions à geler dans
`DECISIONS-PHASE-0.md` ; les questions du jury dans `NOTES-TIPE.md`.*

<!--
JOURNAL DES CORRECTIONS — passe du 16/09/2026 sur audit externe.
Ce bloc explique les arbitrages faits quand l'audit laissait le choix, et les
rares points ecartes. Il n'est pas destine a la lecture courante.

1. Ordonnancement des regles transverses. L'audit proposait DEUX solutions :
   deplacer la partie T-A/T-B avant le bloc 1-D, ou ajouter une action de
   renvoi. RETENU : la seconde (1-A0), plus la phrase corrigee dans
   << Comment s'en servir >>. Motif : deplacer la securite au milieu de la
   periode 1 aurait casse la lisibilite de la partie transverse (qui est aussi
   une check-list a relire seule) et duplique dix actions. Chaque action T qui
   debloque une action de periode porte desormais son code, comme demande.

2. Date de commande unique. RETENU : decembre (2-I1/2-I2/2-I3), coherent avec le
   risque de delai du tableau de bord ligne 4. En consequence 3-A1 et 3-A2 sont
   devenues des rappels de 2 min sans duree de decision, et 3-C1/3-C2 ne sont
   plus des achats. ECARTE : la suppression pure de 3-C1 et 3-C2 proposee en
   variante. Motif : la reception se controle (references, tensions, capacites
   reellement mesurees), et supprimer les deux codes aurait oblige a renumeroter
   3-C3..3-C8 et toutes leurs citations, pour un gain nul. Le devis, lui, est
   bien fusionne en une seule action : 1-C6, dont T-D8 n'est plus que le rappel.

3. Volume du code. L'audit annoncait 19 110 lignes. Mesure refaite le 16/09/2026
   sur le depot : 19 134 lignes (14 959 dans analyse/*.py + 4 175 dans
   analyse/tests/*.py), commande de controle
   << wc -l analyse/*.py analyse/tests/*.py >>. C'est ce nombre, mesure et date,
   qui est ecrit aux trois endroits concernes (etat du projet, bloc 1-D,
   3-G6 et les cinq choses a retenir). Il bougera : le recompter a chaque revue
   trimestrielle plutot que de l'arrondir.

4. Calendrier FEUILLE-DE-ROUTE.md. L'audit proposait soit de realigner la feuille
   de route, soit d'ajouter ici une table de correspondance. RETENU : la table de
   correspondance (en tete de periode 1) + inscription de l'ecart dans T-E7.
   Motif : cette passe ne modifie que PARCOURS.md ; toucher au calendrier de la
   feuille de route sans relire ses portes de validation serait pire que l'ecart.

5. Deux entrees de registre a CREER, et signalees comme telles : la regle de
   reglage de la reference active (1-C9, proposee comme D11) et le traitement de
   l'ecart de sensibilite entre voies (2-F6). Le registre en compte dix
   aujourd'hui ; ces deux-la n'y sont pas, et ce document ne peut pas les y
   ajouter — il les nomme et dit ou elles manquent.

6. Non traite ici, faute de pouvoir le verifier : les dates 2027 de la fenetre
   d'oraux (11 juillet en PT, 18 juillet en PSI) restent marquees
   [[a verifier]] dans 3-J7, comme toutes les dates SCEI 2027 du document.
-->
