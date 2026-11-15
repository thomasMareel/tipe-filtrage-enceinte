---
name: project-issue-attendue-passif-vs-actif
description: "L'argumentaire partagé avec Thomas sur l'issue probable (pas de victoire nette du passif optimisé) et comment le TIPE en tire parti"
metadata:
  type: project
  modified: 2026-09-02
---

Prédiction donnée à Thomas le 2026-08-04 (acceptée par lui) :

- **Forme de la réponse** : à niveau fixé et modéré, le passif optimisé sur
  Z(f) mesurée peut se rapprocher très près de la cible. Mais l'actif est
  structurellement exact (avant l'ampli, il ne voit jamais le HP).
- **Limite fondamentale** : Z(f) n'est pas fixe — R_e monte avec la chaleur
  (≈ +0,4 %/°C), la résonance bouge avec l'excursion. Le passif optimisé n'est
  juste que pour le Z(f) mesuré (un niveau, une température) ; l'actif s'en
  moque. À **démontrer par des mesures à deux niveaux** — c'est un résultat.
- **Pertes** : plancher irréductible côté passif (DCR ~0,5 Ω minimum
  raisonnable, loi r×m ≈ cte ; L-pads d'égalisation qui chauffent) ; mais
  l'actif a une consommation **fixe** au repos (AOP + second canal d'ampli) →
  il existe un niveau d'écoute sous lequel le passif gaspille moins :
  **point de croisement énergétique**, mesurable au wattmètre de prise.
- **Coût** : dépend de la frontière du système. Marginal (E-800 à 2 canaux
  déjà possédé) → actif gagne (~40 € d'électronique vs ~80-100 € de selfs et
  gros condensateurs, le passif à 100 Hz est dans sa pire zone). Système /
  scénario stéréo → passif gagne (divise par deux les canaux d'ampli).
  Présenter les deux comptabilités.
- **Méthode** : critères gelés avant les mesures ; conclusion attendue du type
  « le passif optimisé comble X % de l'écart pour Y €, mais bute sur une limite
  physique identifiée et mesurée » — plus forte qu'une victoire.

**Why:** C'est l'argument qui a convaincu Thomas que le sujet v2 est au niveau
et honnête ; il structure la fin du récit et les réponses au jury.

**How to apply:** Concevoir les manips de phase 4 pour capturer ces effets
(deux niveaux, wattmètre, coût marginal ET système) ; garder la problématique
ouverte ; reprendre cet argumentaire dans NOTES-TIPE.md et la slide de conclusion.
