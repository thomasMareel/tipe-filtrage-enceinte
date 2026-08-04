# Médias à insérer (photos, schémas, courbes)

Dépose tes fichiers dans ce dossier `assets/` avec les noms ci-dessous : les
présentations les attendent à ces emplacements. Pour insérer une image à la place
d'un bloc `placeholder`, remplace le `<div class="placeholder">…</div>` par :

```html
<img src="assets/NOM-DU-FICHIER.png" alt="description" style="max-height:300px;border-radius:4px">
```

## Fichiers attendus

| Fichier suggéré | Où il apparaît | Contenu |
|---|---|---|
| `enceinte.jpg` | finale slide 3, (option pré-soutenance) | photo de l'enceinte fabriquée |
| `reponse-initiale.png` | finale slide 4 | réponse mesurée 40–500 Hz (export REW) |
| `bode-passif.png` | finale slide 10 | Bode mesuré passif (résistance + vrai HP) vs théorie |
| `bode-actif.png` | finale slide 10 | Bode mesuré actif vs théorie |
| `acoustique-raccord.png` | finale slide 11 | somme acoustique des deux voies (champ proche) |
| `impedance.png` | finale slide 5 (option) | courbe d'impédance mesurée avec pic à f_s |

## Conseils

- **Formats** : PNG pour les courbes (net), JPG pour les photos.
- **Exports REW** : capture la courbe sur fond clair pour rester cohérent avec le thème.
- Les schémas (Bode, circuits, impédance) sont déjà dessinés en SVG : tu peux soit
  garder le SVG, soit le remplacer par ta vraie courbe mesurée quand tu l'auras.
- Après insertion, vérifie le rendu PDF (voir `EXPORT-PDF.md`).
