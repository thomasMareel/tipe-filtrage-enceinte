# Mémoire de travail de Claude — TIPE Thomas (versionnée avec le dépôt)

Cette mémoire **suit le dépôt, pas un compte Claude** : `CLAUDE.md` l'importe à
chaque session, quel que soit le compte, la machine, ou Claude Code sur le web.
Elle complète `CLAUDE.md` (faits, conventions, état) par ce qui n'y est pas : la
façon de travailler avec Thomas, les leçons apprises, les pièges de
l'environnement. Migrée le 15/11/2026 depuis la mémoire locale du premier compte.

**Règles d'usage, pour Claude :**

- Lire la fiche utile avant d'agir dans son domaine. Une fiche reflète ce qui
  était vrai quand elle a été écrite : vérifier ce qu'elle affirme (fichier,
  fonction, décision) avant de s'en servir.
- Toute leçon durable s'écrit **ici**, pas dans la mémoire locale du compte
  (`~/.claude/projects/…/memory/`), puis se commite avec le reste : sinon elle ne
  quitte pas la machine où elle est née.
- Une fiche par fait, avec l'en-tête `name` / `description` / `metadata.type`
  (`user`, `feedback`, `project`, `reference`) ; mettre à jour plutôt que
  dupliquer ; une ligne par fiche dans cet index.
- Le dépôt est **public** (site GitHub Pages ; le dossier `.claude/` n'est pas
  publié sur le site, mais il est lisible sur GitHub) : rien de privé ici, aucun
  identifiant, aucune donnée personnelle au-delà de ce que le projet publie déjà.

## Thomas, et la façon de travailler avec lui

- [Profil de Thomas](user-thomas-profil.md) — étudiant prépa, DIY audio, tutoie, exigeant sur le niveau
- [Pas de sujet « recette »](feedback-niveau-prepa-pas-de-recette.md) — défi niveau prépa : modélisation, problème inverse, optimisation
- [Explorer avant de converger](feedback-explorer-avant-converger.md) — options distinctes, réexpliquer de zéro, confirmer ses reformulations
- [Vérifier avant de recommander du matériel](feedback-verifier-recommandation-materielle.md) — Thomas câble et achète à la lettre : doc constructeur + toutes les branches d'abord
- [Conclusion honnête, critères gelés](feedback-conclusion-honnete-criteres-geles.md) — pas de comparaison truquée, deux comptabilités de coût
- [Archiver avant un pivot](feedback-archiver-avant-pivot.md) — archive-vN/ autonome + tag git, jamais modifiée
- Contribution personnelle déclarée honnêtement — règle dans `CLAUDE.md` § Conventions (« Pas de contribution gonflée »)

## Le projet

- [Pivot v2 et pistes écartées](project-pivot-v2-pistes-ecartees.md) — chronologie, pourquoi chaque piste a été retenue ou écartée
- [Issue attendue passif vs actif](project-issue-attendue-passif-vs-actif.md) — l'argumentaire (dérive thermique, coût marginal vs système, croisement énergétique)
- [Composition de l'enceinte](project-enceinte-composition.md) — résolue le 16/09/2026 ; reste ouvert : le SX-801 marqué « CROSSOVER »
- [Décisions et questions ouvertes](project-questions-ouvertes-thomas.md) — où elles vivent, et la règle : ne jamais geler à la place de Thomas

## Organisation et environnement

- [Travailler depuis plusieurs comptes](project-travail-multi-comptes.md) — GitHub seule source de vérité : pull au début, commit + push à la fin, une session à la fois
- [Environnement Windows d'origine](project-environnement-session.md) — PowerShell 5.1, Python cp1252, fins de ligne, workflows, export PDF
- [Cadre SCEI](reference-scei-tipe.md) — oral 15 + 15 min, PDF 4/3 ≤ 5 Mo, MCOT et DOT ; détail dans REFERENCE-TECHNIQUE.md § 08
