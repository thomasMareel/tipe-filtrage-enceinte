# Archive v1 — sujet « Filtrage passif ou actif » (gelé le 2026-08-04)

Instantané complet du projet **avant le pivot de sujet** décidé le 2026-08-04.

- **Sujet v1** : comparaison de trois architectures de filtrage (passif LC
  post-ampli, passif RC signal faible, actif Sallen-Key) pour le raccord à
  100 Hz — jugé trop « recette » (« il me faut un filtre → j'ai fait un filtre »).
- **Sujet v2** (à la racine du dépôt) : optimisation sous contraintes du filtre
  de raccord sur la **charge réelle** Z(f) du haut-parleur — mesure d'impédance,
  problème inverse (Thiele-Small), optimisation numérique, validation.
  La comparaison passif/actif de la v1 y survit comme **référentiel**.

> **Attention : à la racine, tout n'est pas encore v2.** Seuls les documents
> `.md` (CLAUDE, FEUILLE-DE-ROUTE, REFERENCE-TECHNIQUE, MCOT, NOTES-TIPE, README)
> et `index.html` ont été réécrits pour le sujet v2. Les deux présentations HTML
> de la racine (`pre-soutenance.html`, `presentation-finale.html`) et les quatre
> PDF exportés (`pre-soutenance.pdf`, `pre-soutenance-clair.pdf`,
> `presentation-finale.pdf`, `presentation-finale-clair.pdf`) sont encore des
> supports **v1** — au gel du 2026-08-04, ce sont les mêmes fichiers que ceux
> archivés ici. Leur refonte en v2 est prévue en phase 5 (voir
> FEUILLE-DE-ROUTE.md) : d'ici là, ne pas les lire comme la v2.

Ce dossier est autonome : `pre-soutenance.html` et `presentation-finale.html`
s'ouvrent avec les `css/`, `libs/` et `assets/` copiés ici. Les PDF sont les
versions générées au moment du gel. La pré-soutenance a été présentée aux
professeurs début juin 2026 sous cette forme.

Rien ne doit être modifié ici — c'est une sauvegarde. L'historique git complet
reste par ailleurs disponible (tag `v1-sujet-passif-actif`).
