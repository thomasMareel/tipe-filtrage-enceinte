# TIPE — Filtrage fréquentiel d'une enceinte audio

Présentation reveal.js pour le TIPE session 2027 (2e année de prépa).
Thème national : **Sobriété, efficacité, optimisation**.

**Présentation en ligne :** <https://thomasmareel.github.io/tipe-filtrage-enceinte/>

> **Pivot de sujet (2026-08-04) — v2.** Le sujet initial (« passif ou actif ? »)
> a été recentré sur l'**optimisation du filtre sur la charge réelle Z(f)** :
> mesure d'impédance → identification Thiele-Small (problème inverse) →
> optimisation numérique sous contraintes → validation expérimentale.
> Plan complet : [FEUILLE-DE-ROUTE.md](FEUILLE-DE-ROUTE.md) (quoi et quand) ;
> modèles, montages, incertitudes et cadre SCEI :
> [REFERENCE-TECHNIQUE.md](REFERENCE-TECHNIQUE.md) (comment et pourquoi).
> La v1 est gelée
> dans [`archive-v1/`](archive-v1/) ; les slides à la racine sont encore la v1
> en attendant la refonte.

## Objet du projet (v2)

Étude du **raccord fréquentiel à 100 Hz** d'une enceinte fabriquée maison
(un subwoofer pour le grave, deux haut-parleurs médium-aigu).

**Question directrice :** comment concevoir le filtre de raccord pour qu'il
tienne sa cible sur la **charge réelle** — un haut-parleur dont l'impédance
varie fortement avec la fréquence — au moindre coût en composants, en pertes
et en matière ? Le filtre « catalogue » (formules sur 8 Ω résistif) sert de
point de départ à battre ; le filtre **actif** (insensible à Z(f) par
construction) sert de référence.

L'objectif est ramené à des critères objectifs **gelés avant les mesures** :
fidélité de la sommation au raccord, pertes, consommation, coût, matière,
robustesse au niveau d'écoute. Le travail est centré sur l'**électrique** et
l'**expérimental** ; l'acoustique sert de confrontation au réel.

## Deux livrables

| Fichier | Public | Durée | État |
|---|---|---|---|
| `pre-soutenance.html` | Professeurs (annonce du sujet) | ~5 min, 10 vues | rédigé, visuel |
| `presentation-finale.html` | Jury TIPE | **15 min d'exposé + 15 min d'entretien** (format SCEI) | v1 + annexes — à refondre en v2 |

L'épreuve orale dure **30 minutes** : 15 minutes d'exposé par le candidat, puis
15 minutes d'entretien avec le binôme d'examinateurs. Cible de mise en page :
**16 à 18 vues** d'exposé à 50-55 s chacune ; les annexes, placées après la
conclusion, sont hors chronomètre et servent pendant l'entretien. Le code
Python est annexé après la conclusion **et** apporté en double exemplaire
papier. Le support officiel est un **PDF 4/3 paysage de
5 Mo maximum**, téléversé sur le SCEI et projeté depuis l'ordinateur du jury —
le HTML reveal.js reste un outil de travail et ne sera pas utilisé en salle.
Le gabarit actuel est 16:9 : il sera repassé en 4/3 (1024×768) lors de la
refonte v2.

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
├── pre-soutenance.html        Pré-soutenance ~5 min (v1, présentée en juin 2026)
├── presentation-finale.html   Présentation finale (oral 15 min + 15 min) + annexes (v1, à refondre en v2)
├── *.pdf                      PDF vectoriels (sombre) + *-clair.pdf (impression)
├── favicon.svg
├── css/
│   ├── blueprint.css          Thème « Blueprint » (sombre)
│   └── blueprint-light.css    Surcharge palette claire (impression)
├── libs/                      reveal.js, MathJax (SVG), polices — pour le hors-ligne
├── assets/                    Photos de l'enceinte, schémas, courbes de mesure
├── analyse/                   N'EXISTE PAS ENCORE — futur code Python d'analyse
│                              (lecture des mesures → identification Thiele-Small
│                              → optimisation sur séries E12) ; architecture,
│                              modules et tests spécifiés dans
│                              REFERENCE-TECHNIQUE.md § 09
├── archive-v1/                Instantané complet du sujet v1 (gelé, autonome)
├── _gen.py                    Génère les courbes calculées (Bode, impédance)
├── README.md                  Ce fichier
├── CLAUDE.md                  Mémoire de projet entre sessions
├── FEUILLE-DE-ROUTE.md        Plan de travail v2 : phases, critères, calendrier
├── REFERENCE-TECHNIQUE.md     Compagnon « comment et pourquoi » de
│                              FEUILLE-DE-ROUTE.md : modèles et démonstrations,
│                              montages de mesure, incertitudes, cadre SCEI, sources
├── DECISIONS-PHASE-0.md       Décisions de la phase 0 une fois gelées (critères
│                              chiffrés, niveaux d'écoute de référence, conventions)
├── MCOT.md                    Brouillon de la fiche MCOT (v2)
├── EXPORT-PDF.md              Procédure d'export PDF
└── NOTES-TIPE.md              Questions probables du jury + réponses préparées (v2)
```

## Lancer la présentation

reveal.js, MathJax et les polices sont hébergés localement dans `libs/` :
**aucune installation ni connexion** n'est nécessaire. Il faut juste servir le
dossier via un petit serveur local (MathJax et le mode print-pdf fonctionnent
mal en `file://`).

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
