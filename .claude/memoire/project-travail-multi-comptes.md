---
name: project-travail-multi-comptes
description: "Le projet se travaille depuis plusieurs comptes Claude et machines : GitHub est la seule source de vérité — pull au début, commit et push à la fin, une session à la fois"
metadata:
  type: project
  modified: 2026-11-15
---

Le 15/11/2026, Thomas a demandé d'organiser le dépôt pour pouvoir travailler
depuis **un autre compte Claude**. Jusque-là, une partie du travail n'existait
qu'en local : les corrections du 30/09 dans un worktree non fusionné, le dossier
`dissertation/` jamais versionné, et la mémoire de Claude dans le profil Windows
du premier compte. Tout a été fusionné sur `main` et poussé ; la mémoire est
désormais versionnée dans `.claude/memoire/` et importée par `CLAUDE.md`.

**Why:** Un autre compte, une autre machine ou Claude Code sur le web ne voient
que ce qui est sur GitHub. Un worktree, une modification non commitée ou une
mémoire locale leur sont invisibles ; et deux sessions qui modifient les mêmes
fichiers sans se synchroniser produisent des conflits.

**How to apply:**
- **Début de session** : `git status`, puis `git pull` (ou `git fetch` et
  comparer `main` à `origin/main`) avant toute modification. Signaler à Thomas
  toute modification locale non commitée trouvée, sans l'écraser.
- **Fin de session** : proposer de commiter et de pousser sur `main` — c'est ce
  qui rend le travail visible à l'autre compte. Un travail fait dans une branche
  `claude/*` ou un worktree se fusionne dans `main` avant de partir ; ne jamais
  laisser du travail seulement local sans le dire.
- **Une seule session à la fois** sur le dépôt. Si deux comptes ont travaillé en
  parallèle, fusionner avant de continuer, jamais écraser (`git push --force`
  interdit sur `main`).
- Leçons durables → `.claude/memoire/`, pas la mémoire locale du compte.
- Les PDF à la racine sont des **livrables régénérés** : après une modification
  visible des decks, les régénérer (`EXPORT-PDF.md`) ou dire qu'ils sont en
  retard sur le HTML.
- Procédure de reprise côté Thomas : `README.md` § « Reprendre le projet sur un
  autre compte Claude ».
