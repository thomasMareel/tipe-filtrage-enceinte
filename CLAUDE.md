# CLAUDE.md — Mémoire de projet (TIPE filtrage enceinte)

Ce fichier est la mémoire entre sessions. À relire en début de session et à
tenir à jour à la fin de chaque session de travail.

## Sujet

- **Auteur** : étudiant en PTSI (fin de 1re année), TIPE 2026–2027.
- **Thème national** : Sobriété, efficacité, optimisation.
- **Sujet** : filtrage fréquentiel d'une enceinte fabriquée maison
  (1 subwoofer grave + 2 HP médium-aigu). Raccord à **100 Hz** :
  filtre passe-bas vers le sub, passe-haut vers les médium-aigu.

## Problématique validée

> À fréquence de coupure fixée à 100 Hz, le filtrage **actif** permet-il un
> meilleur compromis entre **sobriété** des composants et **fidélité** de la
> réponse fréquentielle que le filtrage **passif**, et à quel coût système ?

- **Objectif affiché** : meilleur rendu sonore final.
- **Critère scientifique objectif** : fidélité de la réponse au raccord 100 Hz
  = plateau le plus plat possible (écart en dB à une réponse cible) + raccord
  de phase propre. On ne juge PAS le son à l'oreille.

## Décisions cadrantes (validées avec l'étudiant)

1. **Centrage électrique** : la rigueur repose sur la mesure électrique
   (Bode au GBF + oscilloscope : gain et phase). L'acoustique vient en
   confrontation au réel, de façon illustrative, avec ses limites assumées.
2. **Filtres du 1er ordre** : passe-bas / passe-haut 1er ordre.
   - Passif : RC / RL.
   - Actif : RC + AOP (régime linéaire).
   - 2e ordre (Sallen-Key, facteur Q) : hors périmètre pour l'instant.
3. **Thème visuel** : clair sobre (fond blanc cassé, accent bleu-pétrole),
   pour robustesse en salle d'oral et bon export PDF.

## Arguments physiques forts à exploiter (fil rouge)

- À 100 Hz le **passif est coûteux en composants** : L ≈ 12,7 mH et
  C ≈ 199 µF pour 8 Ω → bobine grosse et résistive (pertes Joule, DCR),
  condensateur bipolaire de forte valeur et imprécis. → argument "sobriété".
- Le **HP n'est pas une résistance pure** : inductance de bobine L_e, pic
  d'impédance à la résonance f_s. En passif, la coupure réelle dépend de
  l'impédance du HP qui varie → protocole "d'abord sur résistance, puis sur
  vrai HP" pour isoler l'effet.
- L'**actif filtre en amont de l'ampli** (entrée AOP, impédance élevée et
  constante) → réponse prévisible, indépendante du HP. MAIS impose une
  **bi-amplification** (ampli + alim en plus) → c'est le "coût système".

## Pièges à ne pas oublier

- Mesure acoustique à 100 Hz : modes de pièce (λ ≈ 3,4 m), fenêtrage
  quasi-anéchoïque inopérant en basses fréquences → privilégier le champ proche.
- Phase au raccord : 1er ordre = 90° d'écart entre voies ; somme à surveiller.
- Égalisation des niveaux (sensibilités différentes sub/médium).
- Incertitudes : tolérances R ±5 %, C ±10–20 %, L ±10 % → propagation sur f_c.

## Notions PTSI à mobiliser

Impédance complexe ; fonction de transfert H(jω), module/argument ;
filtres 1er ordre RC/RL ; f_c = 1/(2πRC) ; diagrammes de Bode (asymptotes,
−20 dB/décade) ; AOP idéal en régime linéaire ; incertitudes et propagation.

## Deux livrables

1. **Pré-soutenance** (`pre-soutenance.html`) — ~5 min, 8 slides, **démarche seulement,
   aucun résultat demandé**. À présenter aux professeurs ~2026-06-01 (dans 1 semaine).
   But : annoncer le sujet et la démarche, comme une validation avant de démarrer.
2. **Présentation finale** (`presentation-finale.html`) — ~10 min, 14 slides, version
   complète avec mesures et comparaison. À rédiger après les premières mesures.
3. `index.html` = page d'accueil qui pointe vers les deux. CSS et assets partagés.

## Matériel et caractéristiques (réponses de l'étudiant, 2026-05-24)

- **Subwoofer** : 8 Ω, **18 pouces**, f_s non encore mesurée.
- **Médium-aigu** (×2) : 8 Ω, f_s « vers 50 Hz » (à confirmer), câblage à préciser.
- **Mesure** : carte son de haute qualité (perso), GBF du lycée, micro de mesure
  (compatible carte son/interface). Logiciel recommandé : **REW (gratuit)**.
- **Avancement** : enceinte fabriquée et 100 % fonctionnelle ; utilise actuellement un
  **crossover de fréquence réglable** (= déjà du filtrage actif, à formaliser dans le TIPE).
  **Aucun filtre fabriqué maison, aucune mesure faite.** Projet en cours, tout à venir.
- **Composants** : matériel de base du lycée + achats prévus, **budget max 500 €**
  (à réserver aux composants, pas au logiciel).
- **Actif** : pas encore étudié (programme de 2e année) — sera approfondi pendant le TIPE.
  Décision validée : **on garde l'axe passif vs actif**.

## Conventions du projet

- **Tout en français** : interface, commentaires, commits, notes.
- reveal.js via **CDN** (pas de npm). Servir via `python -m http.server`.
- Formules en **LaTeX** rendu par MathJax 3 (`\( \)` en ligne, `\[ \]` bloc).
- **Pas d'invention de résultats** : tout chiffre non mesuré est un placeholder
  explicite (commentaire HTML `<!-- TODO -->` ou bloc `.placeholder`).
- Sobriété visuelle : pas d'emoji, pas de couleurs criardes, beaucoup de blanc.
- Notes du présentateur dans `<aside class="notes">`, ~40 s par slide.

## État actuel

- [x] Étape 1 — analyse critique du sujet (faite).
- [x] Étape 2 — squelette projet : git, README, CLAUDE.md, index.html
      (reveal.js CDN + MathJax + thème clair), css/custom.css. Premier commit.
- [x] Étape 3 — plans validés : finale 14 slides + pré-version 7 slides.
- [x] Étape 4 — questions de contenu posées et répondues (voir section Matériel).
- [~] Étape 5 — rédaction : **pré-soutenance rédigée** (8 slides), refonte **visuelle**
      (schémas SVG inline, texte minimal, notes orales allégées). Version finale = stub.
      Convention : support PDF → le visuel porte le message, peu de texte à l'écran.
- [x] Étape 6 — EXPORT-PDF.md, NOTES-TIPE.md créés ; dépôt GitHub poussé + Pages actif.
      Dépôt : https://github.com/thomasMareel/tipe-filtrage-enceinte
      Site  : https://thomasmareel.github.io/tipe-filtrage-enceinte/
      Note : gh.exe est dans "C:\Program Files\GitHub CLI\" (pas dans le PATH du shell).

## Prochaines étapes

1. Relecture de la pré-soutenance par l'étudiant ; ajuster nom, schémas, f_s.
2. Insérer les assets (photo enceinte, schéma fonctionnel, Bode théorique).
3. Étape 6 : EXPORT-PDF.md + NOTES-TIPE.md, puis GitHub + Pages.
4. Plus tard : rédiger la version finale une fois les premières mesures faites.

## Données encore à confirmer par l'étudiant

- f_s réelle du médium et du subwoofer (à mesurer à l'impédancemètre / REW).
- Câblage des deux médiums (série / parallèle / voies séparées).
- Sensibilités (dB/W/m) pour l'égalisation des niveaux.
- Référence d'AOP et alimentation symétrique pour le filtre actif (2e année).

## Journal de la boucle autonome (lancée 2026-05-25 01:01, fin visée ~05:01)

Boucle auto-rythmée : à chaque réveil, NOUVELLES idées dans le périmètre
(pré-soutenance / version finale / docs), implémenter, vérifier, commit+push,
journaliser. Pas de scope creep, pas d'invention de résultats.

### Backlog d'idées (cocher quand fait, ajouter au fil de l'eau)
- [x] Mutualiser le CSS des visuels (.viz/.deux-viz/.cle/.chip) dans custom.css.
- [x] Construire la version finale (15 slides) avec visuels SVG + placeholders data.
- [x] Bode finale enrichi : gain ET phase.
- [x] SVG courbe d'impédance d'un HP (pic à f_s) pour la slide « HP ≠ résistance ».
- [x] SVG architecture bi-amplification (actif) vs mono-ampli (passif).
- [~] Dimensionnement chiffré (fait passif) + propagation d'incertitude (exemple à détailler).
- [x] Tableau comparatif final (critères × passif/actif) — version de base.
- [x] Enrichir NOTES-TIPE.md (plus de Q/R, surtout maths + déphasage + choix mesure).
- [x] Page d'accueil : petit visuel/motif de raccord.
- [ ] Vérif qualité : rendu PDF (print-pdf), liens, lisibilité.
- [x] Slide annexe / glossaire pour le jury non spécialiste.
- [x] Exemple travaillé de propagation d'incertitude sur f_c (annexe B).
- [ ] Sélecteur de thème clair/sombre (au cas où la salle est sombre).
- [x] Illustrer la somme des deux voies (1er ordre) : reconstruction plate (annexe C).
- [x] Détailler le dimensionnement actif (valeurs R, C concrètes + AOP exemple).
- [x] README : section sur les deux livrables et la structure SVG.

### Itérations
- Itération 1 (01:01–) : CSS mutualisé dans custom.css ; pré-soutenance nettoyée
  (style inline retiré) ; **version finale construite** (15 slides : contexte, enceinte,
  réponse initiale [placeholder], HP≠résistance [courbe Z avec pic f_s], Bode gain+phase,
  passif dimensionné, actif + bi-amp, protocole, résultats [placeholders], acoustique,
  tableau comparatif, limites, conclusion). Vérifié : 15 sections, 13 SVG, 0 débordement.
- Itération 2 (~01:18) : cadence ramenée au minimum (réveil 60 s, enchaînement).
  NOTES-TIPE.md enrichi (sections 8 maths détaillée, 9 déphasage/somme des voies,
  10 choix expérimentaux REW + mesure d'impédance). Motif visuel « raccord 100 Hz »
  ajouté à la page d'accueil.
- Itérations 3-4 (~01:15, en continu dans le même tour) : dimensionnement actif
  concret sur slide 8 (C=100 nF ⇒ R≈16 kΩ, AOP TL072 ±15 V) ; deux slides d'annexe
  ajoutées à la version finale (glossaire pour jury non spécialiste + propagation
  d'incertitude sur f_c, ±11 % avec R±5 %/C±10 %).
  Note : passage en mode multi-itérations par tour (pas d'attente entre itérations).
- Itérations 5-6 (~01:16, même tour) : README enrichi (tableau des deux livrables +
  structure SVG) ; annexe C ajoutée à la version finale (somme des voies au 1er ordre
  H_PB+H_PH=1 → reconstruction plate, avec SVG). Version finale = 18 sections (15 + 3 annexes).
- Itération 7 (~01:18, même tour) : guide assets/LISEZMOI.md (quels fichiers déposer,
  où ils apparaissent, comment remplacer un placeholder par <img>). Placeholders de la
  finale rendus explicites (noms de fichiers attendus). NB : l'outil de preview
  (screenshot/eval) time out de façon répétée pendant le chargement MathJax — souci
  d'environnement, vérifier le rendu via rechargement manuel ou export PDF.
- Itération 8 (~01:22, même tour) : EXPORT-PDF.md complété (note sur les 3 slides
  d'annexe : secours questions, comment les exclure pour un PDF strict 10 min).
  Vérification numérique des valeurs clés (toutes exactes) : L≈12,7 mH ; C≈199 µF ;
  actif R≈15,9 kΩ pour C=100 nF ; u(f_c)/f_c≈11 %.
- Itération 9 (~01:23) : QA balises (<section> équilibrées 18/18 finale, 9/9 pré-version).
  Tableau comparatif enrichi (ajout encombrement + réglage fin de f_c, critères de la
  démarche initiale) ; police table réduite à .66em pour tenir la slide.
- Itération 10 (~01:25) : correction d'incohérence — l'accueil affichait encore
  « en construction » pour la finale (désormais bâtie). Libellés alignés sur les
  compteurs reveal : pré-soutenance 9 vues, finale 15 slides + 3 annexes (accueil + README).
- Itération 11 (~01:26) : ajout d'une Q/R jury à forte valeur dans NOTES-TIPE.md
  (« si les deux sont du 1er ordre, le filtrage n'est-il pas identique ? ») — point
  subtil : théorie identique, l'écart est dans le réel (Z(f), pertes, tolérances).
- Itération 12 (~01:27) : annexe D « Sources » ajoutée à la finale (gabarit de
  bibliographie à compléter — le TIPE exige des sources ; rien d'inventé, des TODO).
  Finale = 19 sections (15 + 4 annexes : glossaire, incertitude, reconstruction, sources).
- Backlog restant : sélecteur thème clair/sombre (optionnel, différé car le livrable
  est le PDF clair) ; passe finale de relecture PDF quand des assets réels seront là.

### Bilan final de la boucle (arrêt ~01:28 le 2026-05-25, après itération 12)

Boucle arrêtée volontairement : tout le travail à valeur réelle réalisable **sans
les données de l'étudiant** est fait. Continuer aurait été du churn. État livré :

- **Pré-soutenance** (`pre-soutenance.html`) : 9 vues, visuelle, prête pour l'oral ~5 min.
- **Présentation finale** (`presentation-finale.html`) : 15 slides + 4 annexes
  (glossaire, incertitude, reconstruction des voies, sources), à dominante SVG.
- **Docs** : README (livrables + structure), EXPORT-PDF (procédure + annexes),
  NOTES-TIPE (Q/R jury étoffées : maths, déphasage, équivalence des ordres, mesure),
  assets/LISEZMOI (guide d'insertion des médias).
- Tout est commité et poussé ; site Pages à jour.

### Ce qui reste à faire par l'étudiant (nécessite ses données)
1. Renseigner le nom (slides de titre).
2. Mesurer/confirmer f_s du médium et du sub (REW + jig d'impédance).
3. Faire les manips et insérer les courbes (cf. assets/LISEZMOI.md) : réponse
   initiale, Bode passif (résistance + HP), Bode actif, somme acoustique.
4. Remplir le tableau comparatif (ligne « écart à la cible ») et la conclusion.
5. Compléter la bibliographie (annexe Sources) avec les références exactes.
6. Photo de l'enceinte (slide 3).
7. Relire le rendu PDF une fois les médias insérés (EXPORT-PDF.md).

Pour reprendre une boucle plus tard : relancer /loop avec un prompt similaire.

### Reprise de boucle
- Itération 13 (~01:30) : boucle relancée par l'étudiant. Création de **MCOT.md**
  (brouillon de la fiche MCOT SCEI : titre, ancrage au thème, mots-clés FR/EN,
  positionnement, problématique, objectifs, étapes, bibliographie commentée — avec
  placeholders [[à compléter]] pour motivation/sources, rien d'inventé). Référencé
  dans le README. Nouveau doc TIPE requis, hors slides.
