---
name: feedback-archiver-avant-pivot
description: "Avant un pivot ou une refonte majeure, Thomas veut une copie complète de l'ancienne version « en vrac dans un dossier »"
metadata:
  type: feedback
  modified: 2026-09-02
---

Au moment du pivot v2 (2026-08-04), Thomas a demandé : « garde tout de même de
côté notre ancienne version du TIPE au cas où (mets simplement tout en vrac
dans un dossier) ». Fait : `archive-v1/` = copie intégrale et autonome (slides,
PDF, docs, css, libs, assets, ancien CLAUDE.md) + LISEZMOI + tag git
`v1-sujet-passif-actif` sur le dernier commit v1 (a550061).

**Why:** Il veut pouvoir rouvrir l'ancienne version telle quelle (pas via git),
par sécurité et pour y repêcher du contenu (pré-soutenance déjà présentée aux
profs en juin 2026, Q/R jury, valeurs).

**How to apply:**
- Avant toute refonte majeure (slides, sujet), créer `archive-vN/` autonome
  (copier css/, libs/, assets/ avec, pour que les HTML s'ouvrent) + tag git
  (et le pousser : `git push origin <tag>`).
- Ne jamais modifier le contenu d'une archive ; les fichiers à la racine sont
  les seuls vivants.
- Un simple dossier suffit — pas besoin de mise en forme sophistiquée.
