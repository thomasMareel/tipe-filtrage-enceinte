# CLAUDE.md — Mémoire de projet (TIPE filtrage enceinte)

Ce fichier est la mémoire entre sessions. À relire en début de session et à
tenir à jour à la fin de chaque session de travail.

> ⚠️ PIVOT DE SUJET v2 — décision étudiant du 2026-08-04 (FAIT FOI).
> L'étudiant jugeait la v1 (« passif ou actif ? ») trop « recette » pour le
> niveau prépa (« il me faut un filtre → j'ai fait un filtre »). Le sujet est
> recentré sur l'**optimisation sur charge réelle**. Le plan opérationnel
> complet est dans **FEUILLE-DE-ROUTE.md** (référence unique pour les phases).
> La v1 est gelée dans `archive-v1/` (autonome, avec son propre CLAUDE.md et
> tout l'historique de travail) + tag git `v1-sujet-passif-actif`.

## Sujet (v2)

- **Auteur** : Thomas Mareel, 2e année de prépa (PTSI → 2e année), TIPE session 2027.
- **Thème national** : Sobriété, efficacité, optimisation.
- **Enceinte deux voies (DIY)** : 1 subwoofer **8 Ω 18″** + 2 médium-aigu
  **4 Ω câblés en série (= 8 Ω)**. Raccord cible : **100 Hz**. Pavillons d'aigu
  hors périmètre. Type de caisse (clos / bass-reflex) à documenter.

## Problématique (v2)

> « Comment concevoir le filtre de raccord à 100 Hz d'une enceinte deux voies
> pour qu'il tienne sa cible sur la charge réelle — un haut-parleur dont
> l'impédance varie du simple au sextuple — au moindre coût en composants,
> en pertes et en matière ? »

**Récit en 4 actes** : mesurer Z(f) → identifier Thiele-Small (problème
inverse, moindres carrés) → optimiser le filtre sous contraintes (E12, coût,
pertes DCR) → valider au banc et au micro contre des critères **gelés avant
les mesures**. Satellites intégrés : **self optimale** (Wheeler/Brooks, alimente
le modèle de coût), **croisement énergétique** (conso au repos de l'actif vs
pertes du passif), **référence active** (immunisée contre Z(f) par construction).

Détail des phases, portes de validation, critères et calendrier :
**FEUILLE-DE-ROUTE.md**. Ne pas dupliquer ici.

## Ce que la v1 lègue à la v2

- **Filtre passif « catalogue »** (point de départ à battre) : LC 2ⁿᵈ ordre
  Butterworth 100 Hz/8 Ω — PB sub : L₁=18 mH série + C₁=150 µF // ; PH médium :
  C₂=150 µF série + L₂=18 mH //. (C théorique ≈ 141 µF → 150 µF normalisé.)
- **Référence active Sallen-Key** (Q=1/√2), avant l'ampli, bi-amplification sur
  les 2 canaux du E-800. Valeurs corrigées : sub R=10 kΩ, C₁=220 nF/C₂=110 nF ;
  médiums R'₁=11 kΩ, R'₂=22 kΩ, C=100 nF. AOP NE5532 (ou TL072), alim ±15 V.
- L'archi « RC signal faible 1er ordre » de la v1 est **abandonnée** (le
  contre-exemple n'a plus de rôle dans le récit v2).
- Identité visuelle **Blueprint** (css/blueprint.css + blueprint-light.css),
  libs vendorées (hors-ligne), procédure PDF, photos de l'enceinte dans assets/.

## Matériel

- Pré-ampli **JB Systems SMX SX-801** (2 sorties identiques) — Zs à mesurer.
- Ampli **t.amp E-800** : 2×350 W/8 Ω, 2×500 W/4 Ω ; Zin 20 k sym / 10 k asym ;
  sensibilité 0,775 V / 1,4 V (sélectable). Deux canaux → bi-amp sans achat.
- Mesure lycée : GBF, oscillo numérique, multimètre. Perso : micro de mesure +
  carte son de qualité (modèle à documenter).
- Logiciels : **REW**, **LTspice**, **Python** (numpy/scipy/matplotlib).
- Budget composants : **≤ 500 €**.
- Enceinte fabriquée et fonctionnelle ; crossover actif réglable du commerce
  actuellement en service (= la référence active existe déjà en pratique).

## Données encore à confirmer par l'étudiant

- f_s réelle du sub et des médiums (→ phase 1, mesure d'impédance).
- Type de caisse (clos/bass-reflex) ; câblage exact des médiums.
- Sensibilités (dB/W/m) pour l'égalisation des niveaux.
- Modèle exact de la carte son ; les 2 niveaux d'écoute de référence à geler.

## Points scientifiques à NE PAS oublier (critique prof 2026-05-25, toujours valides)

- **2ⁿᵈ ordre Butterworth ⇒ inversion de polarité d'une voie OBLIGATOIRE**
  (sinon trou profond à fc ; avec inversion → bosse +3 dB).
- **Fs en caisse ≠ Fs datasheet** : Fc(clos) > Fs ; bass-reflex = deux pics.
  Mesurer le pic en caisse n'est pas une erreur.
- **Z exacte sans approximation courant constant** : mesurer V_HP ET V_Rref →
  Z = Rref·(V_HP/V_Rref). À 100 Ω, I≈cst se dégrade au pic (Z ~ 40–60 Ω).
- **DCR de la self** : pertes Joule + modifie l'amortissement du grave — en v2
  c'est un élément CENTRAL (fonction de coût + étude self, loi r×m ≈ cte à L fixée).
- **Mesure acoustique à 100 Hz** : modes de pièce (λ ≈ 3,4 m), fenêtrage
  inopérant en BF → champ proche.
- **Égalisation des niveaux** entre voies ; **tolérances** R ±5 %, C ±10–20 %,
  L ±10 % → propagation sur f_c (et argument pour l'énumération E12 en v2).
- **Scope oral 10 min** : le détail vit en annexes.

## Nombres de contrôle (vérifiés)

- Butterworth 100 Hz/8 Ω : L = √2·R/(2πf) ≈ 18,0 mH ; C = 1/(√2·R·2πf) ≈ 141 µF.
- DCR 1 Ω face à 8 Ω → ~11 % de la puissance en chaleur, ≈ −1 dB.
- Résonance série 18 mH + 150 µF ≈ 97 Hz (méthode de mesure de L au GBF).
- Sallen-Key : voir valeurs corrigées ci-dessus (fc ≈ 100 Hz, Q = 1/√2).
- Courbes _gen.py (modèle v1) : f_s modèle ≈ 40 Hz, Z(100 Hz) ≈ 14 Ω.

## Conventions du projet

- **Tout en français** : interface, commentaires, commits, notes.
- reveal.js + MathJax + polices **vendorés dans `libs/`** (hors-ligne, pas de
  CDN, pas de npm). Servir via `python -m http.server`.
- Formules en LaTeX via MathJax 3 (`\( \)` en ligne, `\[ \]` bloc).
- **Pas d'invention de résultats** : tout chiffre non mesuré est un placeholder
  explicite (`<!-- TODO -->` ou bloc `.placeholder`).
- Sobriété visuelle (pas d'emoji, schémas SVG, identité Blueprint).
- Notes du présentateur dans `<aside class="notes">`, ~40 s par slide.
- Dépôt : https://github.com/thomasMareel/tipe-filtrage-enceinte
  Site : https://thomasmareel.github.io/tipe-filtrage-enceinte/
  Note : gh.exe est dans "C:\Program Files\GitHub CLI\" (pas dans le PATH).

## Procédure PDF (résumé — détail dans EXPORT-PDF.md)

PDF vectoriels via decktape (Chrome système, PUPPETEER_EXECUTABLE_PATH) ;
variante claire imprimable via css/blueprint-light.css. Repli bitmap :
captures Chrome headless par slide + img2pdf (dossier _pdfbuild/ gitignoré).

## État actuel (2026-08-04)

- [x] v1 complète (pré-soutenance présentée aux profs début juin 2026 ; finale
      v1 structurée en attente de mesures) — **gelée dans archive-v1/**.
- [x] Pivot v2 acté : FEUILLE-DE-ROUTE.md créée, MCOT.md réécrit (v2),
      CLAUDE.md (ce fichier) réécrit, README mis à jour.
- [ ] Phase 0 à finir : critères + 2 niveaux d'écoute à geler (décision
      étudiant), liste d'achats phase 1, squelette code `analyse/`.
- [ ] Les slides à la racine (pre-soutenance.html, presentation-finale.html,
      index.html) sont encore la **v1** — refonte v2 prévue en phase 5 (ou
      avant sur demande). Le site Pages reflète donc la v1 pour l'instant.

## Prochaines étapes

1. Étudiant : valider/amender les critères et les 2 niveaux d'écoute
   (FEUILLE-DE-ROUTE.md § Critères) → les geler.
2. Étudiant : acheter R_ref 100 Ω 1 % (+ 10 Ω), pinces, wattmètre de prise ;
   vérifier résistance de puissance 8 Ω au lycée.
3. Claude : squelette `analyse/` (Python : lecture mesures → fit T-S →
   optimisation E12 avec sanity check 8 Ω) dès que demandé.
4. Phase 1 dès la rentrée : étalonnage de la chaîne sur composants connus,
   puis Z(f) du sub en caisse. C'est la clé de voûte — rien d'autre avant.

## Historique

Tout le journal de travail v1 (boucle autonome du 2026-05-25, refonte Blueprint,
audit A–D du 2026-05-27, itérations pré-soutenance de juin) est conservé dans
`archive-v1/CLAUDE.md`. Ne pas le recopier ici.
