---
name: project-questions-ouvertes-thomas
description: "Où vivent les décisions et questions en attente de Thomas, et la règle : ne jamais geler une décision à sa place"
metadata:
  type: project
  modified: 2026-11-15
---

Le projet attend surtout des **informations et décisions qui n'appartiennent
qu'à Thomas**. Elles vivent dans le dépôt, pas ici :

- `DECISIONS-PHASE-0.md` — le registre des 10 décisions, avec son **tableau de
  bord** (fait foi). État au 30/09/2026 : D8 (type de caisse) et D10
  (encadrant, M. Chevalier) répondues le 16/09 ; D2 (cible de sommation)
  **reportée** le 13/09, à trancher avant le premier achat de composants du
  filtre et avant le MCOT ; D1 (définition de f_c) et D7 (gabarit 4/3)
  **appliquées** dans les documents mais **non signées** ; D3 à D6 et D9
  ouvertes.
- `CLAUDE.md` § Données encore à confirmer et § Prochaines étapes.
- `PARCOURS.md` — l'ordre des actions de Thomas et la ligne « Où j'en suis ».

**Why:** Produire de la théorie sans ces réponses serait du churn ; et une
décision gelée par Claude à la place de Thomas ruinerait l'argument « critères
gelés avant les mesures ».

**How to apply:** À chaque reprise : `git pull`, relire le tableau de bord de
`DECISIONS-PHASE-0.md`, rappeler à Thomas ce qui reste ouvert plutôt que
d'avancer sur des hypothèses. Une décision n'est gelée que **datée et signée
dans le registre** ; une décision prise propage ensuite partout
(`PARCOURS.md` T-E3), y compris dans `analyse/criteres_geles.json` — qui porte
encore D8 à « [[a geler]] » au 15/11/2026 alors que le constat date du 16/09.
