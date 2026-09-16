# Fiche MCOT (brouillon v2) — Mise en Cohérence des Objectifs du TIPE

> Document de travail pour la fiche MCOT (SCEI), aligné sur le **sujet v2**
> (pivot du 2026-08-04). Les `[[à compléter]]` dépendent de l'étudiant.
> **Rien d'inventé.** L'ancien brouillon (sujet v1) est dans `archive-v1/MCOT.md`.

> **Budget de mots officiel (Attendus 2026 ; limites 2027 [[à vérifier]]).**
> Motivation **50** · Ancrage au thème **50** · Bibliographie commentée **650** ·
> Problématique **50** · Objectifs **100** → **900 mots** au total, hors 5 + 5
> mots-clés et 2 à 10 références. Ces limites sont **des plafonds de saisie** :
> au-delà, le texte est coupé. Chaque rubrique ci-dessous porte sa limite en
> tête, et un commentaire `<!-- ... -->` quand le brouillon la dépasse.
>
> **Fenêtre de saisie : mi-janvier → début février 2027** (étape 1 SCEI, dates
> 2027 [[à vérifier]]), c'est-à-dire pendant la phase 4 — donc **à rédiger dès
> la phase 3 (nov.–déc. 2026)**. Le MCOT décrit des objectifs et une démarche :
> ne pas y promettre de résultats.

## Titre

Optimisation sous contraintes du filtre de raccord d'une enceinte deux voies
sur sa charge réelle.

## Professeur encadrant (étape 1 SCEI)

> **Champ obligatoire du formulaire, pas une rubrique rédigée** : l'étape 1 du
> SCEI (mi-janvier → début février 2027) saisit, à côté du titre, la
> **déclaration du professeur encadrant**. Elle ne consomme aucun des 900 mots
> du MCOT, mais c'est le seul point du cadre SCEI qui peut coûter la note
> entière.

**M. Chevalier** — accord obtenu (confirmé par Thomas le 16 septembre 2026).

`[[à compléter : prénom ou initiale, et discipline, tels qu'ils doivent être saisis]]`

- Vérifier qu'il dispose bien d'un compte sur **lycees.scei-concours.fr**.
- **Étape 3 — validation par l'encadrant, ~mi-juin 2027, fenêtre de 8 jours
  seulement** : la validation atteste d'un travail personnel constaté. En cas de
  refus ou d'absence de validation, le candidat a un entretien avant son passage
  en loge — **note zéro possible**. Le lui rappeler dès la saisie de janvier,
  puis à l'ouverture de la fenêtre.
- À régler dès la rentrée de septembre 2026 (phase 0 de FEUILLE-DE-ROUTE.md) ;
  détail du cadre et des dates : REFERENCE-TECHNIQUE.md § 08.3 et § 08.4
  (dates 2027 [[à vérifier]], données par analogie avec 2025 et 2026).

## Ancrage au thème « Sobriété, efficacité, optimisation »

> **Limite officielle : 50 mots.**

<!-- À CONDENSER : le brouillon ci-dessous fait ≈ 98 mots, soit près du double
     du plafond. Il faut passer de trois paragraphes à ~3 phrases. Piste (à
     trancher par Thomas, pas par Claude) : garder « optimisation » en entier
     puisque c'est le cœur du sujet, et ramener « sobriété » et « efficacité »
     à une demi-phrase chacune, les détails (cuivre, coût système, croisement
     énergétique) étant déjà portés par les Objectifs et la bibliographie. -->

- **Optimisation** (cœur du sujet) : le filtre n'est pas dimensionné par les
  formules catalogues (valables sur 8 Ω résistif) mais par optimisation
  numérique sous contraintes sur l'impédance réelle Z(f) mesurée, après
  identification d'un modèle physique par problème inverse.
- **Sobriété** : contraintes de coût, de matière (cuivre de la bobine, étude
  dédiée) et d'encombrement intégrées à la fonction de coût ; comparaison du
  coût marginal et du coût système avec la solution active.
- **Efficacité** : pertes Joule du filtre passif (résistance série de la bobine)
  vs consommation permanente de la chaîne active — recherche du point de
  croisement énergétique selon le niveau d'écoute.

## Mots-clés

> **Limite officielle : 5 mots-clés français + 5 anglais**, par ordre
> d'importance décroissante. Le brouillon en compte bien 5 paires.

| Français | Anglais |
|---|---|
| Filtre de raccord | Loudspeaker crossover |
| Impédance du haut-parleur | Loudspeaker impedance |
| Modèle de Thiele et Small | Thiele-Small model |
| Problème inverse | Inverse problem |
| Optimisation sous contraintes | Constrained optimization |

## Positionnement thématique (SCEI)

> **Limite officielle : 1 à 3 positionnements** choisis dans la liste fermée des
> **24 thèmes**, par ordre d'importance décroissante. Le **premier** détermine le
> binôme d'examinateurs et doit appartenir à un domaine de rattachement de la
> filière (**Physique ou Sciences industrielles** en PT comme en PSI).

<!-- À RÉALIGNER SUR LES LIBELLÉS OFFICIELS. Dans la liste des 24 thèmes,
     « Électronique » est classé en SCIENCES INDUSTRIELLES, pas en Physique
     (avec Traitement du Signal, Génie Électrique, Génie Mécanique, Génie
     Énergétique, Automatique). Les intitulés du brouillon ci-dessous
     (« Physique — électronique/électrocinétique », « Physique — acoustique »)
     n'existent pas tels quels dans la liste SCEI. Correspondances proposées,
     à trancher par Thomas (détail et descripteurs officiels :
     REFERENCE-TECHNIQUE.md § 08.3) :
       1. Électronique (Sciences industrielles)
       2. Mathématiques Appliquées (Mathématiques)
       3. Physique Ondulatoire (acoustique) ou Automatique (identification)
     Ce choix est verrouillé à la saisie de mi-janvier 2027, donc AVANT les
     mesures acoustiques : le choisir sur le récit prévu, pas sur les résultats. -->

- Physique — **électronique / électrocinétique** (impédance complexe, filtres,
  fonctions de transfert, AOP pour la référence active).
- Mathématiques appliquées — **ajustement de modèle et optimisation** (moindres
  carrés, minimisation sous contraintes, incertitudes).
- Physique — **acoustique** pour la validation au micro.

## Motivation

> **Limite officielle : 50 mots.** (Rubrique saisie à part, avant le MCOT
> proprement dit, avec l'ancrage au thème.)

[[à compléter : enceinte construite de tes mains ; constat que les formules
« toutes faites » supposent un haut-parleur idéal qui n'existe pas ; envie de
faire mieux avec des méthodes d'ingénieur — 2-3 phrases]]

## Problématique

> **Limite officielle : 50 mots.** Le brouillon ci-dessous en fait ≈ 44 : il
> passe, mais sans marge — toute reformulation doit être recomptée.

Comment concevoir le filtre de raccord à 100 Hz d'une enceinte deux voies pour
qu'il tienne sa cible sur la charge réelle — un haut-parleur dont l'impédance
varie fortement avec la fréquence — au moindre coût en composants, en pertes et
en matière ?

## Objectifs du TIPE

> **Limite officielle : 100 mots.** Des **objectifs**, pas des résultats.

<!-- À CONDENSER : le brouillon ci-dessous fait ≈ 126 mots, soit ~26 de trop.
     Les quatre verbes (Mesurer / Identifier / Optimiser / Valider) sont la
     colonne vertébrale du sujet et doivent rester ; c'est dans les
     compléments qu'il faut couper. Candidats au retrait (à trancher par
     Thomas, pas par Claude) : l'énumération des six critères de l'objectif 4,
     qui coûte à elle seule une quinzaine de mots et que l'exposé détaillera ;
     « avec incertitudes propagées » (objectif 2), déjà impliqué par
     « moindres carrés » ; « en caisse » (objectif 1). -->

1. **Mesurer** l'impédance complexe Z(f) du subwoofer (en caisse) et du bloc
   médiums, avec une chaîne de mesure étalonnée sur composants connus et des
   incertitudes chiffrées.
2. **Identifier** les paramètres du modèle de Thiele-Small par ajustement aux
   moindres carrés sur Z(f) (problème inverse), avec incertitudes propagées.
3. **Optimiser** le filtre passif (valeurs L, C contraintes aux séries réelles,
   coût, pertes, encombrement) sur la charge modélisée, pour une sommation des
   deux voies aussi plate que possible autour de 100 Hz ; dimensionner la bobine
   elle-même (compromis cuivre/pertes).
4. **Valider** expérimentalement : comparer filtre catalogue, filtre optimisé et
   référence active (insensible à Z(f) par construction) selon des critères
   chiffrés gelés avant les mesures — fidélité du raccord, pertes, consommation,
   coût, matière, robustesse au niveau d'écoute.

## Étapes (voir FEUILLE-DE-ROUTE.md)

> **Rubrique de travail, pas une rubrique du MCOT** : le formulaire SCEI ne
> comporte que Motivation, Ancrage, Positionnements + mots-clés, Bibliographie
> commentée, Problématique, Objectifs et Liste des références. La chronologie
> se saisit plus tard, dans le **DOT** (4 à 8 jalons de 50 mots max), à
> l'étape 2 — fin févr. → début juin 2027.

1. Chaîne de mesure d'impédance étalonnée ; Z(f) des deux voies (sept. 2026).
2. Identification Thiele-Small, résidus et incertitudes (oct. 2026).
3. Optimisation numérique sous contraintes + étude de la bobine (nov.–déc. 2026).
4. Fabrication (bobinage, filtres, référence active) et mesures électriques puis
   acoustiques, aux deux niveaux d'écoute de référence (déc. 2026 – févr. 2027).
5. Analyse comparative sur critères gelés, conclusion, supports (2027).

## Matériel

> **Rubrique de travail** également : pas de champ « matériel » au SCEI. Ces
> éléments alimentent l'exposé et, le cas échéant, les jalons du DOT.

Enceinte deux voies DIY : sub 18″ 8 Ω **en caisse bass-reflex à deux évents**
+ 2 médiums 4 Ω câblés en série (= 8 Ω), **avec 2 pavillons d'ultra-aigu en
parallèle des médiums** — hors bande **acoustiquement** au raccord de 100 Hz,
mais **dans la charge électrique** que voit le passe-haut, donc mesurés avec le
bloc médiums tel qu'il est câblé · pré-ampli
JB Systems SMX SX-801 · ampli t.amp E-800 (2×350 W/8 Ω, deux canaux → référence
active bi-amplifiée sans achat d'ampli) · GBF, oscilloscope, multimètre (lycée) ·
carte son + micro de mesure · REW, LTspice, Python (numpy/scipy/matplotlib) ·
fil de cuivre émaillé et composants passifs (budget ≤ 500 €).

<!-- Environnement Python vérifié le 2026-09-13 sur la machine du projet :
     Python 3.13.2, numpy 2.4.6, scipy 1.18.1, matplotlib 3.11.0 ; un appel à
     scipy.optimize.least_squares a été exécuté avec succès. Citer scipy dans
     le matériel (et en référence [5]) est donc exact : c'est l'outil réellement
     disponible, pas une intention. Un repli en numpy pur (équations normales ou
     Gauss-Newton écrit à la main) reste intéressant à montrer au jury comme
     preuve de compréhension de l'algorithme, jamais comme une contrainte subie. -->

<!-- COMPOSITION DE L'ENCEINTE — information de l'étudiant du 2026-09-16, qui
     fait foi (décision D8 de DECISIONS-PHASE-0.md, désormais répondue). Le sub
     est en BASS-REFLEX À DEUX ÉVENTS ; l'enceinte porte en outre 2 pavillons
     d'ultra-aigu CÂBLÉS EN PARALLÈLE DES MÉDIUMS. La rubrique Matériel
     ci-dessus est corrigée en conséquence : elle n'a pas de limite de mots.
     Ce que cela change ailleurs dans la fiche, et qu'il faut ARBITRER, pas
     ajouter d'office (rubriques déjà au-dessus de leur plafond) :
       - OBJECTIFS (≈ 126 mots pour 100 autorisés — DÉJÀ TROP LONG, NE PAS
         ALLONGER). L'objectif 1 dit « l'impédance complexe Z(f) du subwoofer
         (en caisse) » : c'est exact et suffisant, le mot « bass-reflex » n'y
         est pas indispensable. L'objectif 2 dit « les paramètres du modèle de
         Thiele-Small » sans en donner le nombre : c'est heureux, puisque le
         compte passe de 5 (caisse close) à 7-8 (bass-reflex : accord f_b,
         rapport de compliances alpha, pertes Q_l). Si Thomas veut nommer le
         bass-reflex dans les Objectifs, il doit RENDRE les mots ailleurs —
         candidats déjà identifiés plus haut : l'énumération des six critères
         de l'objectif 4, et « avec incertitudes propagées » à l'objectif 2.
       - ANCRAGE (≈ 98 mots pour 50 — DÉJÀ TROP LONG, NE PAS ALLONGER).
       - PROBLÉMATIQUE (≈ 44 mots pour 50, sans marge) : elle parle d'« un
         haut-parleur dont l'impédance varie fortement avec la fréquence »,
         formulation qui reste vraie et même RENFORCÉE par le bass-reflex (deux
         pics au lieu d'un, le second tombant près de la zone de raccord).
         Ne rien y changer : le gain d'exactitude serait nul et le coût en mots
         réel.
       - BIBLIOGRAPHIE (≈ 124 mots sur 650 — il reste de la place) : c'est LA
         rubrique où le bass-reflex se dit sans arbitrage, via Thiele 1971,
         « Loudspeakers in Vented Boxes », qui traite précisément des caisses à
         évent. Note ajoutée à la référence [2] ci-dessous. -->

## Bibliographie commentée (à compléter)

> **Limite officielle : 650 mots** — de loin la rubrique la plus généreuse
> (72 % du budget total de 900 mots). Liste des références : **2 à 10**,
> numérotées, avec des « renvois numérotés progressifs » depuis le texte.

<!-- À DÉVELOPPER — c'est LA rubrique à travailler. Le brouillon ci-dessous
     n'utilise qu'environ 124 mots sur 650 : plus de 500 mots sont laissés sur
     la table alors que cette rubrique est celle qui montre au jury
     l'appropriation du contexte scientifique. Ce qui manque : ce n'est pas
     une liste de titres qui est demandée mais une SYNTHÈSE rédigée du contexte,
     dans laquelle les références sont appelées par [1], [2]... Chaque
     référence devrait être commentée par ce qu'elle apporte AU SUJET (ce
     qu'on lui emprunte, et pourquoi elle ne suffit pas). Les six entrées
     actuelles sont par ailleurs encore des placeholders [[à consulter]] :
     les consulter est un préalable, la limite de 2 à 10 références étant
     satisfaite dès maintenant. -->

- [1] [[Cours de physique PTSI/PT]] — impédance complexe, filtres, fonctions de
  transfert, AOP. [[réf. exacte]]
- [2] Thiele, A. N., « Loudspeakers in Vented Boxes », *JAES*, 1971 ; Small, R. H.,
  « Direct-Radiator Loudspeaker System Analysis », *JAES*, 1972 — le modèle
  électroacoustique dont les paramètres sont identifiés en phase 2. Le titre de
  Thiele n'est pas un hasard de bibliographie : le sub étudié est en **caisse
  bass-reflex à deux évents**, c'est-à-dire exactement le *vented box* de 1971 —
  d'où deux pics d'impédance au lieu d'un, et un modèle à identifier à 7-8
  paramètres. [[à consulter]]
- [3] Wheeler, H. A., « Simple Inductance Formulas for Radio Coils », *Proc. IRE*,
  1928 — formules géométrie ↔ inductance pour l'étude de la bobine. [[à consulter]]
- [4] Dickason, V., *The Loudspeaker Design Cookbook* — filtres de répartition,
  réseaux de compensation (Zobel). [[édition à préciser]]
- [5] Documentation REW (mesure de réponse et d'impédance) et scipy
  (moindres carrés, optimisation). [[versions/URL]]
- [6] [[Datasheets des HP]] (sub 18″, médiums) — ordres de grandeur pour valider
  l'identification. [[modèles exacts]]

<!-- ARBITRAGE À TRANCHER PAR THOMAS — recommandation de REFERENCE-TECHNIQUE.md
     § 08.7, signalée ici sans toucher à la liste. Les références sont limitées
     à 2 à 10 et doivent être « scientifiquement fiables et suffisamment précises
     pour être exploitables par les examinateurs » : une documentation de
     logiciel consomme donc l'un de ces emplacements. La référence [5]
     (REW + scipy) occupe une place que pourraient prendre des sources
     scientifiques — Thiele et Small (déjà en [2]), Wheeler (en [3]),
     Dickason (en [4]), et la norme CEI/IEC sur la mesure des haut-parleurs,
     absente de la liste. Deux issues possibles, au choix : (a) rendre
     l'emplacement en rappelant REW et scipy dans le texte de la synthèse
     (outillage, pas source), (b) garder [5] mais l'assumer en disant ce qu'on
     lui emprunte précisément (algorithme de moindres carrés non linéaires ;
     protocole de mesure d'impédance de REW). Ce n'est en aucun cas un problème
     de disponibilité de l'outil : scipy est installé et fonctionnel (voir la
     note de la rubrique Matériel). -->

> **Récapitulatif des écarts au format officiel, à traiter par Thomas :**
> Ancrage ≈ 98 mots pour 50 autorisés (**à condenser**) · Objectifs ≈ 126 pour
> 100 (**à condenser**) · Bibliographie commentée ≈ 124 sur 650 (**à
> développer** — c'est la rubrique décisive) · Positionnements à réaligner sur
> les 24 libellés officiels (« Électronique » est en **Sciences industrielles**,
> pas en Physique) · Motivation encore vide (50 mots) · Problématique à ≈ 44
> mots, sans marge. Le « 650 mots » n'est **pas** la limite de la fiche entière
> mais celle de la seule bibliographie ; le plafond global est de 900 mots.
> Le MCOT décrit des objectifs et une démarche — ne pas y promettre de résultats.
> **Mise à jour du 2026-09-16 (composition de l'enceinte)** : sub en **bass-reflex
> à deux évents**, plus **2 pavillons d'ultra-aigu en parallèle des médiums**.
> Seules les rubriques **sans limite de mots** ont été corrigées (Matériel, et une
> précision à la référence [2], la bibliographie ayant plus de 500 mots de marge).
> **Aucune rubrique plafonnée n'a été allongée** : Ancrage et Objectifs sont déjà
> au-dessus de leur limite, la Problématique est sans marge — ce qu'il faudrait
> éventuellement y dire, et ce qu'il faudrait rendre en échange, est consigné en
> commentaire avant la bibliographie, **à arbitrer par Thomas**.
> **Hors budget de mots, mais bloquant : le professeur encadrant n'est pas encore
> désigné** (rubrique ajoutée en tête de ce fichier) — sans sa déclaration à
> l'étape 1 ni sa validation à l'étape 3, la note peut être zéro.
> Détail du cadre officiel et des citations littérales : REFERENCE-TECHNIQUE.md
> § 08.3.
