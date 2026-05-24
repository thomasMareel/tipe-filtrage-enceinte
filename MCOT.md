# Fiche MCOT (brouillon) — Mise en Cohérence des Objectifs du TIPE

> Document de travail pour préparer la fiche MCOT à saisir sur SCEI.
> Pré-rempli avec ce qui est validé ; les `[[à compléter]]` dépendent de toi
> (motivation personnelle, références exactes). **Rien n'est inventé.**

## Titre du TIPE

Filtrage fréquentiel d'une enceinte audio : raccord à 100 Hz, passif ou actif ?

## Ancrage au thème « Sobriété, efficacité, optimisation »

Le filtrage de répartition (raccord grave/médium) illustre directement les trois axes :
- **Sobriété** : à 100 Hz, le filtre passif exige des composants volumineux
  (bobine ≈ 12,7 mH, condensateur ≈ 199 µF pour 8 Ω) ; l'actif n'utilise que de
  petits R et C.
- **Efficacité** : pertes Joule dans la résistance série de la bobine (passif),
  pente d'atténuation réelle, puissance réellement transmise au haut-parleur.
- **Optimisation** : choix du meilleur compromis entre sobriété des composants et
  fidélité de la réponse, sur des critères objectifs mesurés.

## Mots-clés

| Français | Anglais |
|---|---|
| Filtrage fréquentiel | Frequency filtering |
| Fréquence de coupure | Cutoff frequency |
| Filtre passif / actif | Passive / active filter |
| Raccord (répartiteur) | Crossover |
| Diagramme de Bode | Bode plot |

## Positionnement thématique (à cocher sur SCEI)

- Physique — **électronique / électrocinétique** (régime sinusoïdal, filtres, AOP).
- (Éventuellement) Physique — **ondes / acoustique** pour la partie mesure.

## Motivation

[[à compléter : pourquoi ce sujet te tient à cœur — enceinte construite de tes mains,
intérêt pour le son, etc. 2–3 phrases personnelles.]]

## Problématique

À fréquence de coupure fixée à 100 Hz, le filtrage actif permet-il un meilleur
compromis entre sobriété des composants et fidélité de la réponse fréquentielle
que le filtrage passif, et à quel coût système ?

Critère objectif de « qualité » : fidélité de la réponse au raccord (plateau le plus
plat possible autour de 100 Hz + raccord de phase propre), mesurée en dB.

## Objectifs du TIPE

1. Modéliser les filtres passe-bas et passe-haut du 1er ordre à 100 Hz (fonction de
   transfert, fréquence de coupure, diagrammes de Bode) et dimensionner les composants.
2. Mesurer expérimentalement les réponses (Bode électrique au GBF/oscilloscope, d'abord
   sur résistance puis sur le vrai haut-parleur ; confrontation acoustique au micro/REW).
3. Comparer passif et actif sur des critères objectifs (sobriété, pertes, dépendance à
   l'impédance, coût système, écart à la réponse cible) et conclure.

## Étapes et planning

1. Mesure d'impédance des HP (détermination de f_s).
2. Dimensionnement des filtres passif (L, C) et actif (RC + AOP).
3. Tests électriques (Bode) sur résistance équivalente puis sur HP.
4. Tests acoustiques en champ proche.
5. Comparaison théorie/expérience avec incertitudes, puis bilan.

## Bibliographie commentée (à compléter)

- [1] [[Cours d'électronique PTSI]] — fondements : impédance complexe, filtres du
  1er ordre, AOP en régime linéaire. [[réf. exacte]]
- [2] [[Datasheets des haut-parleurs]] — paramètres (impédance, f_s, sensibilité).
  [[marque / modèle]]
- [3] [[Documentation REW (Room EQ Wizard)]] — protocole de mesure de réponse et
  d'impédance. [[version / URL]]
- [4] [[Ouvrage ou ressource d'électroacoustique]] — filtres de répartition d'enceintes.
  [[réf. exacte]]

> Astuce : la fiche MCOT SCEI limite le texte (≈ 650 mots) ; ce brouillon est plus
> long, à condenser au moment de la saisie.
