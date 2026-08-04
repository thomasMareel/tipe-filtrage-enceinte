# Fiche MCOT (brouillon) — Mise en Cohérence des Objectifs du TIPE

> Document de travail pour la fiche MCOT (SCEI). Pré-rempli avec le cadrage validé ;
> les `[[à compléter]]` dépendent de toi (motivation, références exactes). **Rien d'inventé.**

## Titre

Filtrage fréquentiel d'une enceinte deux voies : passif ou actif pour le raccord à 100 Hz ?

## Ancrage au thème « Sobriété, efficacité, optimisation »

- **Sobriété** : à 100 Hz le filtre passif exige de gros composants (bobine ≈ 18 mH,
  condensateur ≈ 150 µF / ≥ 100 V) ; l'actif n'utilise que de petits R et C.
- **Efficacité** : pertes Joule dans la résistance série de la bobine (DCR), pente réelle
  d'atténuation, rendement.
- **Optimisation** : choix du meilleur compromis entre sobriété et fidélité, sur critères mesurés.

## Mots-clés

| Français | Anglais |
|---|---|
| Filtrage fréquentiel | Frequency filtering |
| Fréquence de coupure | Cutoff frequency |
| Filtre Butterworth 2ⁿᵈ ordre | 2nd-order Butterworth filter |
| Filtre actif / Sallen-Key | Active filter / Sallen-Key |
| Raccord (répartiteur) | Loudspeaker crossover |

## Positionnement thématique (SCEI)

- Physique — **électronique / électrocinétique** (régime sinusoïdal, filtres, AOP, facteur Q).
- (éventuellement) Physique — **acoustique** pour le volet mesure.

## Motivation

[[à compléter : enceinte construite de tes mains, intérêt pour le son / l'électronique — 2-3 phrases]]

## Problématique

Filtrage passif ou filtrage actif : quelle architecture offre le meilleur compromis
sobriété / efficacité pour le raccord à 100 Hz d'une enceinte deux voies subwoofer / médium-aigu ?

## Trois architectures comparées

1. **Passif post-amplification** — LC 2ⁿᵈ ordre Butterworth (12 dB/oct), entre ampli et HP.
2. **Passif signal faible** — RC 1er ordre (6 dB/oct), entre pré-ampli et ampli (contre-exemple).
3. **Actif Sallen-Key** — 2ⁿᵈ ordre Butterworth (Q = 1/√2), à AOP, avant l'ampli (bi-amplification).

Duel central : 1 (passif) vs 3 (actif), à ordre égal.

## Objectifs du TIPE

1. Modéliser les filtres (fonction de transfert, Q, diagrammes de Bode) et dimensionner les composants.
2. Mesurer (Bode électrique au GBF/oscillo, d'abord sur résistance puis sur HP ; somme acoustique au micro/REW).
3. Comparer les architectures sur des critères objectifs (précision de f_c, pente, pertes, coût,
   encombrement, sensibilité à Z(HP)) et conclure.

## Étapes (5 phases)

1. Caractérisation : Z(f) et f_s des HP, Z_s du pré-ampli, réponse initiale.
2. Dimensionnement + simulation (Python, LTspice), d'abord HP = 8 Ω puis Z(f) mesurée.
3. Tests électriques sur résistance de puissance 8 Ω (f_c, pente, pertes).
4. Tests acoustiques sur HP réels (REW), somme des deux voies au raccord.
5. Analyse comparative pondérée + perspectives (Zobel, Linkwitz-Riley, ordre 4, DSP).

## Matériel

Pré-ampli JB Systems SMX SX-801 · ampli t.amp E-800 (2×350 W/8 Ω) · GBF, oscilloscope,
multimètre (lycée) · carte son + micro de mesure · REW, LTspice, Python.

## Bibliographie commentée (à compléter)

- [1] [[Cours d'électronique PTSI]] — impédance complexe, filtres, AOP, facteur Q. [[réf.]]
- [2] [[Datasheets des HP]] (sub 18″, médiums 4 Ω) — Z, f_s, sensibilité. [[modèles]]
- [3] [[Documentation REW]] — mesure de réponse et d'impédance. [[version/URL]]
- [4] [[Électroacoustique]] — filtres de répartition (Butterworth, Linkwitz-Riley). [[réf.]]

> La fiche MCOT SCEI limite le texte (≈ 650 mots) : condenser à la saisie.
