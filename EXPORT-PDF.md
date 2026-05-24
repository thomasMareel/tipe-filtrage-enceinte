# Export PDF de la présentation

Le livrable final attendu est un PDF. reveal.js sait s'imprimer proprement via un
mode dédié, puis l'impression PDF de Chrome.

## 1. Servir le projet en local

L'export ne marche pas en `file://` (MathJax et les feuilles CDN ne se chargent pas).
Depuis le dossier du projet :

```powershell
python -m http.server 8000
```

## 2. Ouvrir le mode impression

Dans **Google Chrome** (ou Edge), ajouter `?print-pdf` à l'URL de la présentation à exporter :

- Pré-soutenance : <http://localhost:8000/pre-soutenance.html?print-pdf>
- Version finale : <http://localhost:8000/presentation-finale.html?print-pdf>

La page s'affiche alors « à plat », une slide par page. **Attendre** que les formules
MathJax soient rendues (1 à 2 s) avant d'imprimer.

## 3. Imprimer en PDF

`Ctrl + P`, puis régler **exactement** :

| Paramètre | Valeur |
|---|---|
| Destination | **Enregistrer au format PDF** |
| Mise en page / Orientation | **Paysage** |
| Format papier | **A4** (ou « Letter ») |
| Marges | **Aucune** |
| Échelle | **100 %** (ou « par défaut », pas « ajuster ») |
| **Graphiques d'arrière-plan** | **Activé** ← indispensable, sinon fonds et tableaux blancs |
| En-têtes et pieds de page | Désactivés |

Puis **Enregistrer**.

## 4. Vérifier le rendu

Ouvrir le PDF et contrôler :

- [ ] Une slide par page, rien n'est coupé.
- [ ] Les **formules LaTeX** sont nettes (pas de code `\frac{...}` brut → signe que
      MathJax n'avait pas fini : recommencer en laissant plus de temps au chargement).
- [ ] Les **tableaux** ont bien leurs fonds (sinon : « Graphiques d'arrière-plan » oublié).
- [ ] Les **notes du présentateur** n'apparaissent pas (normal, elles sont masquées à l'impression).
- [ ] Les placeholders restants (photo, schéma, Bode) sont à remplacer avant la version définitive.

## Astuces

- Pour inclure les notes dans un PDF séparé (antisèche orale), utiliser la vue
  présentateur (touche `S`) et imprimer cette fenêtre à part.
- Si une slide déborde en hauteur, alléger son contenu : le PDF ne « scrolle » pas,
  ce qui dépasse est perdu.
- `pdfSeparateFragments: false` est déjà réglé : les apparitions progressives ne
  créent pas de pages en double.

## Slides d'annexe (version finale)

La présentation finale se termine sur « Merci de votre attention » ; viennent ensuite
trois **slides d'annexe** (glossaire, incertitude sur f_c, reconstruction des voies).
Ce sont des slides de **secours pour les questions du jury**, pas de la présentation
orale des 10 minutes.

- Si tu veux les **garder** dans le PDF (recommandé, utile en soutenance) : ne touche à rien.
- Si tu veux un PDF **strictement limité** à l'exposé : supprime (ou commente) les
  sections marquées `ANNEXE A/B/C` dans `presentation-finale.html` avant l'export.
