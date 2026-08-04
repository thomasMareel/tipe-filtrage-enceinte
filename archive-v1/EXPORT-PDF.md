# Export PDF des présentations

Les PDF sont **pré-générés** et versionnés dans le dépôt :

| Fichier | Thème | Usage |
|---|---|---|
| `pre-soutenance.pdf` | Blueprint (sombre) | écran / projection |
| `presentation-finale.pdf` | Blueprint (sombre) | écran / projection |
| `pre-soutenance-clair.pdf` | clair | **impression papier** (économie d'encre) |
| `presentation-finale-clair.pdf` | clair | impression papier |

Ce sont des PDF **vectoriels** (texte sélectionnable et recherchable), générés avec
**decktape** (qui pilote le Chrome déjà installé). La présentation fonctionne aussi
**hors-ligne** : reveal.js, MathJax (SVG) et les polices sont hébergés en local (`libs/`).

## Régénérer les PDF

1. Servir le dossier : `python -m http.server 8090`
2. Version sombre (vectorielle) :
   ```
   set PUPPETEER_EXECUTABLE_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe
   npx -y decktape@3 reveal http://localhost:8090/pre-soutenance.html pre-soutenance.pdf -s 1280x720 --chrome-arg=--no-sandbox
   npx -y decktape@3 reveal http://localhost:8090/presentation-finale.html presentation-finale.pdf -s 1280x720 --chrome-arg=--no-sandbox
   ```
3. Version claire : créer une copie temporaire du HTML qui ajoute
   `<link rel="stylesheet" href="css/blueprint-light.css">` après `blueprint.css`,
   puis decktape cette copie vers `*-clair.pdf`. (La palette claire se substitue à la
   sombre ; tous les schémas SVG, qui utilisent des variables CSS, se recolorent seuls.)

## Vérifier

- [ ] Une slide par page, rien n'est coupé, grille pleine page.
- [ ] Formules MathJax nettes (SVG), courbes de Bode et d'impédance lisibles, axes gradués.
- [ ] Photos présentes (slide 2). Texte sélectionnable (Ctrl+F dans le PDF).

> Méthode alternative (raster) si decktape indisponible : capturer chaque slide
> avec Chrome `--headless --screenshot` (window 1280×720, scale 2) puis assembler
> avec `img2pdf`. Donne un PDF image (texte non sélectionnable).
