# Fiche MCOT (brouillon v2) — Mise en Cohérence des Objectifs du TIPE

> Document de travail pour la fiche MCOT (SCEI), aligné sur le **sujet v2**
> (pivot du 2026-08-04). Les `[[à compléter]]` dépendent de l'étudiant.
> **Rien d'inventé.** L'ancien brouillon (sujet v1) est dans `archive-v1/MCOT.md`.

## Titre

Optimisation sous contraintes du filtre de raccord d'une enceinte deux voies
sur sa charge réelle.

## Ancrage au thème « Sobriété, efficacité, optimisation »

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

| Français | Anglais |
|---|---|
| Filtre de raccord | Loudspeaker crossover |
| Impédance du haut-parleur | Loudspeaker impedance |
| Modèle de Thiele et Small | Thiele-Small model |
| Problème inverse | Inverse problem |
| Optimisation sous contraintes | Constrained optimization |

## Positionnement thématique (SCEI)

- Physique — **électronique / électrocinétique** (impédance complexe, filtres,
  fonctions de transfert, AOP pour la référence active).
- Mathématiques appliquées — **ajustement de modèle et optimisation** (moindres
  carrés, minimisation sous contraintes, incertitudes).
- Physique — **acoustique** pour la validation au micro.

## Motivation

[[à compléter : enceinte construite de tes mains ; constat que les formules
« toutes faites » supposent un haut-parleur idéal qui n'existe pas ; envie de
faire mieux avec des méthodes d'ingénieur — 2-3 phrases]]

## Problématique

Comment concevoir le filtre de raccord à 100 Hz d'une enceinte deux voies pour
qu'il tienne sa cible sur la charge réelle — un haut-parleur dont l'impédance
varie fortement avec la fréquence — au moindre coût en composants, en pertes et
en matière ?

## Objectifs du TIPE

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

1. Chaîne de mesure d'impédance étalonnée ; Z(f) des deux voies (sept. 2026).
2. Identification Thiele-Small, résidus et incertitudes (oct. 2026).
3. Optimisation numérique sous contraintes + étude de la bobine (nov.–déc. 2026).
4. Fabrication (bobinage, filtres, référence active) et mesures électriques puis
   acoustiques, aux deux niveaux d'écoute de référence (déc. 2026 – févr. 2027).
5. Analyse comparative sur critères gelés, conclusion, supports (2027).

## Matériel

Enceinte deux voies DIY (sub 18″ 8 Ω + 2 médiums 4 Ω en série) · pré-ampli
JB Systems SMX SX-801 · ampli t.amp E-800 (2×350 W/8 Ω, deux canaux → référence
active bi-amplifiée sans achat d'ampli) · GBF, oscilloscope, multimètre (lycée) ·
carte son + micro de mesure · REW, LTspice, Python (numpy/scipy/matplotlib) ·
fil de cuivre émaillé et composants passifs (budget ≤ 500 €).

## Bibliographie commentée (à compléter)

- [1] [[Cours de physique PTSI/PT]] — impédance complexe, filtres, fonctions de
  transfert, AOP. [[réf. exacte]]
- [2] Thiele, A. N., « Loudspeakers in Vented Boxes », *JAES*, 1971 ; Small, R. H.,
  « Direct-Radiator Loudspeaker System Analysis », *JAES*, 1972 — le modèle
  électroacoustique dont les paramètres sont identifiés en phase 2. [[à consulter]]
- [3] Wheeler, H. A., « Simple Inductance Formulas for Radio Coils », *Proc. IRE*,
  1928 — formules géométrie ↔ inductance pour l'étude de la bobine. [[à consulter]]
- [4] Dickason, V., *The Loudspeaker Design Cookbook* — filtres de répartition,
  réseaux de compensation (Zobel). [[édition à préciser]]
- [5] Documentation REW (mesure de réponse et d'impédance) et scipy
  (moindres carrés, optimisation). [[versions/URL]]
- [6] [[Datasheets des HP]] (sub 18″, médiums) — ordres de grandeur pour valider
  l'identification. [[modèles exacts]]

> La fiche MCOT SCEI limite le texte (≈ 650 mots) : condenser à la saisie.
> Le MCOT décrit des objectifs et une démarche — ne pas y promettre de résultats.
