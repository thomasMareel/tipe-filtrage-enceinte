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
