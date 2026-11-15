---
name: feedback-verifier-recommandation-materielle
description: "Thomas exécute les recommandations de câblage et d'achat à la lettre — les vérifier contre la doc constructeur et la pratique standard, et compter toutes les branches, AVANT de les donner"
metadata:
  type: feedback
  modified: 2026-09-23
---

Le 16/09/2026, Thomas a répondu « on fera exactement comme tu me le
recommandes » à un câblage de jig d'impédance sur sa Scarlett Solo que Claude
avait proposé (entrée micro aux bornes d'une R_ref de 10 Ω). Il était **faux** :
il ignorait la topologie standard de REW (R_sense 100 Ω, lecture
différentielle) et la charge de mode commun de l'entrée XLR. Il a fallu un
arbitrage à plusieurs agents le 23/09/2026 et une correction dans tous les
documents (commit c15a3da). Même semaine, même cause : l'effet des pavillons sur
|Z| du bloc médium annoncé « 6 à 16 % » avait été calculé pour **un** pavillon
alors qu'il y en a **deux** (vrai chiffre : −10 à −26 %).

**Why:** Une recommandation matérielle part directement en commande et en
câblage au lycée ; une erreur coûte de l'argent, une séance de manip, voire du
matériel, et elle ne se voit souvent qu'au banc. Le texte déjà vérifié du dépôt
(manuel Focusrite relevé dans CLAUDE.md) contenait de quoi éviter l'erreur.

**How to apply:** Avant toute consigne de câblage, d'achat ou de réglage :
(1) la confronter à la doc constructeur et à la méthode standard de l'outil
(REW, etc.) ; (2) énumérer **toutes** les branches du circuit réel (pavillons,
condensateurs, masses) et vérifier que le calcul les compte ; (3) pour un
montage nouveau, faire relire par un panel d'agents avant de le figer ;
(4) si une consigne donnée se révèle fausse, le dire franchement à Thomas et
corriger partout. Voir [[project-environnement-session]] et
[[feedback-conclusion-honnete-criteres-geles]].
