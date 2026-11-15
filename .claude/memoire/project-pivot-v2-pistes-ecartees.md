---
name: project-pivot-v2-pistes-ecartees
description: "Chronologie du pivot v2 (2026-08-04), pistes proposées, lesquelles ont été retenues/écartées et pourquoi — réservoir pour perspectives et annexes"
metadata:
  type: project
  modified: 2026-09-02
---

**Chronologie.** Brief et critique des profs le 2026-05-24/25 ; audit du site
2026-05-27 ; pré-soutenance v1 présentée aux professeurs début juin 2026 ;
dernier commit v1 le 2026-06-04 ; session Claude plantée (rien de perdu) ;
reprise et **pivot v2 le 2026-08-04**.

**Pistes proposées le 2026-08-04 et statut :**
- **Retenue (axe principal)** : optimisation du filtre sur charge réelle —
  mesurer Z(f) → identifier Thiele-Small (problème inverse) → optimiser sous
  contraintes (E12, coût, DCR) → valider contre critères gelés. Thomas : « J'aime
  beaucoup cette idée d'étude de la résistance du sub ».
- **Intégrée comme chapitre/annexe** : self optimale (Wheeler/Brooks, loi
  r×m ≈ cte). Thomas ne l'avait pas comprise au premier passage ; ré-expliquée
  avec schéma. Il la voyait en annexe « réduction des coûts » ; elle a été
  repositionnée comme la brique qui fournit le **modèle de coût** de
  l'optimisation (une slide dans le corps + détails en annexe).
- **Satellites** : croisement énergétique (conso au repos actif vs pertes
  passif) ; référence active Sallen-Key gardée en arrière-plan (immunisée
  contre Z(f)) — question : le passif optimisé rattrape-t-il l'actif, à quel coût ?
- **Écartées, réutilisables en perspectives / questions du jury** :
  - Servo-woofer (asservissement par accéléromètre) : automatique vue tard,
    mise au point expérimentale trop risquée sur un an.
  - Crossover numérique FIR à phase linéaire : cœur = TNS/programmation, hors
    programme PTSI, questions d'échantillonnage non maîtrisables.
  - Non-linéarités Bl(x), k(x) → distorsion (DL, harmoniques) : très riche
    mais Bl(x) difficile à caractériser → semi-quantitatif.
  - Compression thermique (Re(T), modèle 1-2 constantes de temps) : non retenue
    comme axe mais **revient** via le critère de robustesse (mesures à deux
    niveaux) et le croisement énergétique.
  - Directivité / lobes d'interférence au raccord : bon complément possible
    (mesures polaires), non retenu faute de place.
  - Modes de la pièce / placement optimal (sources images) : vrai pivot hors
    filtrage, écarté.
- Abandonnée avec la v1 : l'architecture « RC signal faible 1er ordre »
  (contre-exemple sans rôle en v2).

**Why:** Ne pas reproposer ce qui a été écarté ; savoir quoi citer en
« perspectives » et comment répondre si le jury demande « pourquoi pas … ».

**How to apply:** Pour les slides « limites et perspectives » et NOTES-TIPE.md
(§ 5), puiser dans la liste ci-dessus avec les raisons ; si Thomas veut
réévaluer une piste écartée, rappeler la raison initiale avant d'en discuter.
