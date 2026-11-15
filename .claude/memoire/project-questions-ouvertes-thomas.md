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
  bord** (fait foi). État au 15/11/2026 :
  - D8 (type de caisse) et D10 (encadrant, M. Chevalier) : répondues le 16/09.
  - **D2 tranchée le 15/11 : Butterworth 2.** Restent le motif et la signature.
  - **D5, option E, gelée le 15/11 : voie par voie** (un canal d'ampli par
    filtre). Le reste de D5 est ouvert.
  - **D6 provisoire le 15/11** : 1,5 Ω, 3 A/mm², 2 selfs à prise. Restent le
    devis, la puissance à laquelle s'applique $J_{max}$, le modèle DCR/prix et la
    méthode de calcul des critères n° 5 et 7.
  - **D9 en partie le 15/11** : PT, TIPE individuel. Restent les positionnements
    et le titre.
  - D1 et D7 : appliquées mais non signées. D3 et D4 : ouvertes.
- `CLAUDE.md` § Données encore à confirmer et § Prochaines étapes.
- `PARCOURS.md` — l'ordre des actions de Thomas et la ligne « Où j'en suis ».

**Why:** Produire de la théorie sans ces réponses serait du churn ; et une
décision gelée par Claude à la place de Thomas ruinerait l'argument « critères
gelés avant les mesures ».

**How to apply:** À chaque reprise : `git pull`, relire le tableau de bord de
`DECISIONS-PHASE-0.md`, rappeler à Thomas ce qui reste ouvert plutôt que
d'avancer sur des hypothèses. Une décision n'est gelée que **datée et signée
dans le registre** ; une décision prise propage ensuite partout
(`PARCOURS.md` T-E3), y compris dans `analyse/criteres_geles.json` (D2 et D8 y
sont reportées depuis le 15/11/2026 ; une décision **provisoire** comme D6 y reste
non gelée). Quand Thomas répond en séance, consigner aussitôt sa réponse au
registre avec la date et « décidée par : Thomas », et laisser **sa** signature et
**son** motif en placeholder : ne jamais les écrire à sa place.
