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
- [ ] Étape 3 — plan détaillé 12–15 slides (à valider).
- [ ] Étape 4 — questions à l'étudiant (matériel, HP, avancement, composants).
- [ ] Étape 5 — rédaction du contenu slide par slide.
- [ ] Étape 6 — EXPORT-PDF.md, NOTES-TIPE.md, push GitHub + Pages.

## Prochaines étapes

1. Proposer le plan détaillé (Étape 3) et le faire valider.
2. Poser les 5–8 questions de contenu (Étape 4).
3. Rédiger les slides après réponses.

## Données à obtenir de l'étudiant (encore manquantes)

- Caractéristiques des HP : impédance nominale, sensibilité, f_s mesurée.
- Matériel de mesure : oscilloscope, GBF, micro de mesure, logiciel (REW ?).
- Avancement des manips et résultats préliminaires.
- Composants disponibles au lycée, budget, référence d'AOP.
