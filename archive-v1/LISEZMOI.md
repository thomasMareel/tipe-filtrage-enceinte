# Archive v1 — sujet « Filtrage passif ou actif » (gelé le 2026-08-04)

Instantané complet du projet **avant le pivot de sujet** décidé le 2026-08-04.

- **Sujet v1** : comparaison de trois architectures de filtrage (passif LC
  post-ampli, passif RC signal faible, actif Sallen-Key) pour le raccord à
  100 Hz — jugé trop « recette » (« il me faut un filtre → j'ai fait un filtre »).
- **Sujet v2** (à la racine du dépôt) : optimisation sous contraintes du filtre
  de raccord sur la **charge réelle** Z(f) du haut-parleur — mesure d'impédance,
  problème inverse (Thiele-Small), optimisation numérique, validation.
  La comparaison passif/actif de la v1 y survit comme **référentiel**.

Ce dossier est autonome : `pre-soutenance.html` et `presentation-finale.html`
s'ouvrent avec les `css/`, `libs/` et `assets/` copiés ici. Les PDF sont les
versions générées au moment du gel. La pré-soutenance a été présentée aux
professeurs début juin 2026 sous cette forme.

Rien ne doit être modifié ici — c'est une sauvegarde. L'historique git complet
reste par ailleurs disponible (tag `v1-sujet-passif-actif`).
