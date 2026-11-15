---
name: project-enceinte-composition
description: "Composition réelle de l'enceinte : question résolue le 16/09/2026 (bass-reflex à deux évents, 2 pavillons en parallèle des médiums) ; reste ouvert le rôle du SX-801 marqué « CROSSOVER »"
metadata:
  type: project
  modified: 2026-11-15
---

Le 13/09/2026, un agent relisant `assets/enceinte-face.jpg` et
`assets/enceinte-banc.jpg` avait compté **plus de haut-parleurs** que l'enceinte
« deux voies » des documents. **Résolu le 16/09/2026 par Thomas** : sub 18″ en
caisse **bass-reflex à deux évents**, 2 médiums 4 Ω en série, et **2 pavillons
d'ultra-aigu câblés en parallèle des médiums**, avec un condensateur série dont
la valeur reste à mesurer. Détail et conséquences : `CLAUDE.md` § Sujet et
`DECISIONS-PHASE-0.md` (D8).

**Encore ouvert** : le pré-ampli JB Systems SMX SX-801 porte une sérigraphie
« CROSSOVER ». Si c'est lui, le « crossover actif réglable du commerce
actuellement en service », la référence active existe déjà et la phase 4 n'a
peut-être pas besoin du montage Sallen-Key. Question jamais posée à Thomas
(reportée dans `CLAUDE.md` § Données encore à confirmer le 15/11/2026).

**Why:** Si la chaîne réelle diffère de celle modélisée, la charge vue par le
filtre et la sommation acoustique du raccord changent de nature.

**How to apply:** Avant la phase 4, demander à Thomas quel appareil filtre
aujourd'hui l'enceinte et avec quels réglages ; corriger ensuite `CLAUDE.md`
§ Matériel et `FEUILLE-DE-ROUTE.md` si besoin.
