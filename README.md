# TIPE — Filtrage fréquentiel d'une enceinte audio

Présentation reveal.js pour le TIPE 2026–2027 (PTSI).
Thème national : **Sobriété, efficacité, optimisation**.

**Présentation en ligne :** <https://thomasmareel.github.io/tipe-filtrage-enceinte/>

## Objet du projet

Étude du **raccord fréquentiel à 100 Hz** d'une enceinte fabriquée maison
(un subwoofer pour le grave, deux haut-parleurs médium-aigu), au moyen d'un
filtre **passe-bas** (vers le subwoofer) et d'un filtre **passe-haut** (vers les
médium-aigu).

**Question directrice :** à fréquence de coupure fixée à 100 Hz, le filtrage
**actif** permet-il un meilleur compromis entre **sobriété** des composants et
**fidélité** de la réponse fréquentielle que le filtrage **passif**, et à quel
coût système ?

L'objectif final est le **meilleur rendu sonore**, ramené à un critère objectif
et mesurable : la **fidélité de la réponse au raccord** (plateau le plus plat
possible autour de 100 Hz + raccord de phase propre). Le travail est centré sur
l'**électrique** et l'**expérimental** ; l'acoustique sert de confrontation au réel.

## Deux livrables

| Fichier | Public | Durée | État |
|---|---|---|---|
| `pre-soutenance.html` | Professeurs (annonce du sujet) | ~5 min, 9 vues | rédigé, visuel |
| `presentation-finale.html` | Jury TIPE | ~10 min, 16 slides + annexes | structuré, en attente des mesures |

`index.html` est une page d'accueil qui pointe vers les deux. Identité visuelle
**« Blueprint »** (`css/blueprint.css`) ; variante claire pour l'impression
(`css/blueprint-light.css`). Les visuels sont des **schémas SVG** (dont les courbes de
Bode et d'impédance **calculées** via `_gen.py`). Tout fonctionne **hors-ligne** :
reveal.js, MathJax (SVG) et les polices sont hébergés dans `libs/`. Chaque présentation
existe aussi en **PDF vectoriel** (sombre) et **PDF clair** (impression).

## Structure des dossiers

```
TIPE/
├── index.html                 Page d'accueil (liens présentations + PDF + docs)
├── pre-soutenance.html        Pré-soutenance ~5 min
├── presentation-finale.html   Présentation finale ~10 min + annexes
├── *.pdf                      PDF vectoriels (sombre) + *-clair.pdf (impression)
├── favicon.svg
├── css/
│   ├── blueprint.css          Thème « Blueprint » (sombre)
│   └── blueprint-light.css    Surcharge palette claire (impression)
├── libs/                      reveal.js, MathJax (SVG), polices — pour le hors-ligne
├── assets/                    Photos de l'enceinte, schémas, courbes de mesure
├── _gen.py                    Génère les courbes calculées (Bode, impédance)
├── README.md                  Ce fichier
├── CLAUDE.md                  Mémoire de projet entre sessions
├── MCOT.md                    Brouillon de la fiche MCOT
├── EXPORT-PDF.md              Procédure d'export PDF
└── NOTES-TIPE.md              Questions probables du jury + pistes de réponse
```

## Lancer la présentation

reveal.js est chargé depuis un CDN : **aucune installation npm** n'est nécessaire.
Il faut juste servir le dossier via un petit serveur local (le plugin Math et le
mode print-pdf fonctionnent mal en `file://`).

Avec Python (déjà présent sur la plupart des machines) :

```powershell
# depuis le dossier du projet
python -m http.server 8000
```

Puis ouvrir <http://localhost:8000> dans un navigateur (Chrome recommandé).

- Navigation : flèches, `Espace` (suivant), `Échap` (vue d'ensemble).
- Notes du présentateur : touche `S` (ouvre la vue présentateur).

## Export PDF

Ouvrir <http://localhost:8000/?print-pdf> puis imprimer en PDF depuis Chrome.
Procédure détaillée dans `EXPORT-PDF.md`.
