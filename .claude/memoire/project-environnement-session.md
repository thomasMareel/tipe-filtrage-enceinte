---
name: project-environnement-session
description: "Particularités du poste Windows d'origine (PowerShell 5.1, Python cp1252, fins de ligne, workflows, export PDF) et comment les contourner"
metadata:
  type: project
  modified: 2026-11-15
---

Ces pièges ont été relevés sur le **poste Windows 11 d'origine** de Thomas. Sur
une autre machine (ou dans Claude Code sur le web, sous Linux), une partie ne
s'applique pas : vérifier avant d'appliquer un contournement.

- Shell principal **PowerShell 5.1** (pas de `&&`, pas de `??`) ; Git Bash
  disponible aussi. Python 3.13.2.
- **Python affiche en cp1252** : tout script qui imprime des accents ou des
  symboles (Ω, µ, →) doit commencer par
  `import sys; sys.stdout.reconfigure(encoding='utf-8')`, sinon
  UnicodeEncodeError.
- **Fins de ligne** : `core.autocrlf=true` est réglé au niveau système de Git
  pour Windows. Les avertissements « LF will be replaced by CRLF » sont
  inoffensifs. Mais un worktree extrait ainsi avait ses `.py` en CRLF, et le
  test de convention `test_tous_les_sources_sont_utf8_sans_crlf` échouait sur
  24 sous-cas sans aucune régression. Depuis le 15/11/2026, `.gitattributes`
  impose `eol=lf` aux `.py` : toute nouvelle extraction est saine. Python en
  mode texte écrit aussi des CRLF sous Windows : pour patcher un fichier qui doit
  rester en LF, ouvrir avec `newline='\n'` ou écrire en binaire.
- `gh.exe` est dans `C:\Program Files\GitHub CLI\` (hors PATH) ; `git push`
  fonctionne directement (identifiants du compte GitHub `thomasMareel`
  enregistrés sur ce poste — à refaire sur toute autre machine).
- Une session de juin 2026 a planté côté interface ; à la reprise tout était
  commité : **toujours vérifier `git status` + `git log` en début de session**
  avant de supposer du travail perdu.
- `_pdfbuild/` (gitignoré) contient ~9 Mo d'artefacts de capture PDF.
- Le site GitHub Pages sert la racine du dépôt : tout ce qui est à la racine
  est public (archive-v1/ incluse). Jekyll n'y publie pas les dossiers dont le
  nom commence par `.` ou `_` (`.claude/` n'est donc pas sur le site).
- **Workflows multi-agents** : ils meurent si le processus Claude se ferme ou si
  la limite d'utilisation est atteinte ; relancer avec `resumeFromRunId` (même
  session seulement). Toujours mettre un garde-fou `x ? x.champ : repli` sur les
  résultats d'agents (null si échec). Un script de workflow doit être en LF.
- **Heredocs dans le Bash tool** : avec un délimiteur **entre apostrophes**
  (`<<'EOF'`), les backslashes arrivent intacts à Python ; avec les autres formes
  ils sont transformés et cassent les littéraux. En cas de doute, écrire le bloc
  avec l'outil Write dans le scratchpad puis le greffer par un petit script.
- **PowerShell bloque `Remove-Item`** dans une commande composée dès qu'un
  chemin contient une espace : supprimer par une commande séparée, ou par `rm`
  dans le Bash tool.
- **Export PDF des decks** (détail : EXPORT-PDF.md § 3.3 et § 4) : decktape
  produit ~5,2 Mo pour la finale (glyphes Type 3 dupliqués vue par vue) ;
  **toujours** passer `python _alleger_pdf.py *.pdf` ensuite (1,80 Mo, sans
  perte ; dépend de pikepdf, pypdf en option). pikepdf 10.7 n'a pas
  `Pdf.check()` : c'est `check_pdf_syntax()`.
- **Regarder le PDF sorti, pas seulement le HTML** : Chrome imprimait le texte
  des SVG en colonnes à ~0,78 d'échelle (invisible à l'écran, flagrant dans le
  PDF), corrigé par `text-rendering: geometricPrecision`. Contrôle rapide :
  rendre quelques pages avec PyMuPDF (`fitz`) et les ouvrir avec Read.

**Why:** Chaque piège ci-dessus a coûté une itération au moins une fois.

**How to apply:** Sur le poste d'origine, appliquer les contournements d'office ;
ailleurs, vérifier d'abord s'ils s'appliquent.
