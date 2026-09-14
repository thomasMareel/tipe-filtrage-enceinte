# Export PDF — le support de l'oral

> **Le PDF *est* le livrable.** En salle, le fichier HTML reveal.js n'existe pas :
> le jury projette le **PDF téléversé**, depuis **son propre ordinateur**, au
> clavier. Aucun support personnel n'est admis (clé USB, disque, cloud). Tout ce
> qui n'est pas dans le PDF — notes du présentateur, animations, fichiers
> annexes — n'atteindra jamais les examinateurs.

---

## 1. Le cahier des charges SCEI

| Contrainte officielle | Valeur | Ce qu'elle impose ici |
|---|---|---|
| Format de projection | **4/3 paysage** | `Reveal.initialize({ width: 1024, height: 768 })` **et** `decktape -s 1024x768` |
| Poids du fichier | **5 Mo maximum** | contrôle de la taille à **chaque** export, pas seulement au dernier (§ 4) |
| Numérotation | requise sur **toutes** les diapositives | `slideNumber: 'c/t'` — à vérifier sur le PDF sorti, pas dans le HTML |
| Média | ni vidéo, ni audio, ni animation | aucune transition scénarisée, aucun `data-autoplay` |
| Première vue | nom, prénom et **numéro d'inscription** (recommandation forte) | à contrôler avant l'export |
| Listings de code | **double exemplaire papier** *et* annexés **après la conclusion** ; fond blanc recommandé | § 5 |

Citations littérales et sources : `REFERENCE-TECHNIQUE.md` § 08.1 (cadre de
l'épreuve) et § 08.2 (conséquences pour ce projet).

Convention de taille retenue, faute de précision côté SCEI : lecture
**conservatrice**, 5 Mo = 5 × 10⁶ octets (et non 5 Mio = 5 × 2²⁰). Un fichier
mesuré à 4,9 Mo « décimaux » passe dans les deux lectures ; c'est le seul seuil
qu'on s'autorise.

> Convention de shell dans ce fichier : les blocs marqués `powershell` sont pour
> **PowerShell** (le shell du projet) ; les blocs non marqués passent tels quels
> dans l'**invite de commandes** (`cmd`). Les deux ne sont pas interchangeables —
> `set VAR=...` et le caractère de continuation `^` sont du `cmd`.

---

## 2. Les fichiers

| Fichier | Thème | Usage |
|---|---|---|
| `pre-soutenance.pdf` | Blueprint (sombre) | écran / projection |
| `presentation-finale.pdf` | Blueprint (sombre) | **le livrable SCEI** — à téléverser |
| `pre-soutenance-clair.pdf` | clair | impression papier (économie d'encre) |
| `presentation-finale-clair.pdf` | clair | impression papier, et base des listings (§ 5) |

Ce sont des PDF **vectoriels** : texte sélectionnable et recherchable, figures et
schémas SVG nets à tout zoom. Ils sont produits par **decktape**, qui pilote le
Chrome déjà installé sur la machine. reveal.js 5.1, MathJax (build SVG,
`libs/mathjax/tex-mml-svg.js`) et les polices sont vendorés dans `libs/`.

> ### Correctif du 2026-09-14 — MathJax partait du CDN
>
> Ce paragraphe certifiait un fonctionnement hors-ligne qui n'existait pas. Les
> deux decks configuraient MathJax sous la clé `math:` ; or le plugin vendoré
> `libs/reveal/plugin/math/math.js` ne lit `getConfig().math` que dans sa branche
> **MathJax 2**. Pour MathJax 3 il lit `getConfig().mathjax3` — donc toute la
> configuration était ignorée, chemin local compris, et MathJax était téléchargé
> depuis `cdn.jsdelivr.net` en sortie **CHTML**. Deux conséquences : sans réseau
> (salle d'oral, machine d'export isolée) **toutes les formules disparaissaient**,
> et la sortie CHTML fait dessiner les glyphes par Chrome à l'export, ce qui est
> la piste la plus sérieuse pour les « 446 objets de fonte Type 3 » du § 4.
> `config: 'TeX-AMS_HTML-full'` était de surcroît une option MathJax 2, sans effet.
>
> La clé est désormais `mathjax3:` dans les deux HTML. **À vérifier avant de
> conclure quoi que ce soit sur le poids** : réseau coupé, les formules doivent
> s'afficher, et `MathJax.startup.document.outputJax.constructor.NAME` doit valoir
> `SVG`. Puis rejouer l'export et re-peser : c'est le premier levier à tester,
> avant de toucher aux photos.

> ### Statut au 2026-09-14 — les PDF versionnés sont **périmés**
>
> Les quatre PDF présents dans le dépôt datent du 3–4 juin 2026 : ils portent
> encore la **v1** du sujet, en 1280 × 720 (16:9), c'est-à-dire ni le bon sujet
> ni le bon format. Les deux HTML, eux, sont passés en **v2 / 1024 × 768**.
> Tant que la procédure ci-dessous n'a pas été rejouée, **ne pas diffuser ni
> téléverser ces PDF**.

Nombre de vues attendu après régénération (aucun fragment dans les deux decks,
donc **une vue = une page**, sans exception — **compte vérifié à l'export du
2026-09-14**) :

| Deck | Pages attendues | Détail |
|---|---|---|
| `pre-soutenance` | **10** | 10 vues, ≈ 5 min 30 |
| `presentation-finale` | **49** | 18 vues d'exposé (30 à 60 s pièce, 14 min 45 au total) + 1 sommaire d'annexes + 14 annexes `A1`–`A14` + 16 vues de listings `L0`–`L9` |

> **Le compte est passé de 46 à 49 le 2026-09-14** : ajout du sommaire d'annexes
> (page 19), de l'annexe `A12` « niveau et température » et de l'annexe `A13`
> « pourquoi pas un Zobel ? », la bibliographie devenant `A14`. **Le sommaire
> d'annexes porte des numéros de page : ils sont à revérifier sur le PDF sorti**
> (A1 = 20, A14 = 33, L0 = 34, L9 = 49).

Si le compte diffère, la cause est presque toujours l'ajout de fragments
(`class="fragment"`) : decktape les capture **étape par étape**, une page par
étape. Soit on retire le fragment, soit on désactive la capture des fragments
(`npx decktape --help`, section `reveal`).

---

## 3. Régénérer les PDF

### 3.1 Version sombre (vectorielle)

1. Servir le dossier depuis la **racine du dépôt**, sur le port du projet
   (celui de `.claude/launch.json`) :

   ```
   python -m http.server 8123
   ```

2. Exporter les deux decks au gabarit 4/3 :

   ```
   set PUPPETEER_EXECUTABLE_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe
   npx -y decktape@3 reveal "http://localhost:8123/pre-soutenance.html?export" pre-soutenance.pdf -s 1024x768 --chrome-arg=--no-sandbox
   npx -y decktape@3 reveal "http://localhost:8123/presentation-finale.html?export" presentation-finale.pdf -s 1024x768 --chrome-arg=--no-sandbox
   ```

   Le même enchaînement en PowerShell (seule la ligne d'environnement change) :

   ```powershell
   $env:PUPPETEER_EXECUTABLE_PATH = "C:\Program Files\Google\Chrome\Application\chrome.exe"
   npx -y decktape@3 reveal "http://localhost:8123/presentation-finale.html?export" presentation-finale.pdf -s 1024x768 --chrome-arg=--no-sandbox
   ```

   `-s 1024x768` **doit** reproduire exactement le `width`/`height` du
   `Reveal.initialize` des deux HTML : toute divergence se voit en marges
   asymétriques ou en texte rogné.

   Si MathJax n'a pas fini de composer une formule au moment de la capture (page
   blanche à la place d'une équation), laisser respirer la capture avec l'option
   de pause de decktape (`npx decktape --help`) et relancer.

### 3.2 Version claire (impression)

La palette claire se substitue à la sombre par simple surcharge des variables
CSS ; tous les schémas SVG, écrits en `var(--...)`, se recolorent seuls.

1. Créer une copie temporaire du HTML **à la racine du dépôt** — et pas dans un
   sous-dossier, sinon les chemins relatifs `css/`, `libs/` et `assets/` ne
   résolvent plus — en ajoutant `blueprint-light.css` **après** `blueprint.css` :

   ```powershell
   $src   = "presentation-finale.html"
   $dst   = "_tmp-finale-clair.html"
   $avant = '<link rel="stylesheet" href="css/blueprint.css">'
   $apres = $avant + "`r`n  " + '<link rel="stylesheet" href="css/blueprint-light.css">'
   (Get-Content $src -Raw -Encoding UTF8).Replace($avant, $apres) |
     Set-Content $dst -Encoding UTF8
   ```

   La ligne `$avant` n'apparaît **qu'une fois** dans chacun des deux HTML
   (vérifié) ; `.Replace()` travaille sur la chaîne littérale, sans échappement
   de regex à prévoir.

2. Exporter la copie, puis la supprimer :

   ```
   npx -y decktape@3 reveal "http://localhost:8123/_tmp-finale-clair.html?export" presentation-finale-clair.pdf -s 1024x768 --chrome-arg=--no-sandbox
   ```

   ```powershell
   Remove-Item _tmp-finale-clair.html
   ```

3. Même opération pour `pre-soutenance.html` → `pre-soutenance-clair.pdf`.

> Les vues de listings `L0`–`L9` portent **déjà** leur propre fond clair (fond et
> variables de couleur posés en ligne sur la `<section>`, conformément à la
> recommandation SCEI « listings sur fond blanc »). Elles sortent donc
> identiques dans la version sombre et dans la version claire : c'est normal, il
> n'y a rien à corriger.

---

## 4. Vérifier — la taille d'abord

**Le contrôle de poids est bloquant** : un PDF de plus de 5 Mo n'est pas
téléversable, et on ne s'en aperçoit pas en le regardant.

```powershell
Get-ChildItem *.pdf | Select-Object Name,
  @{n='Mo (10^6)'; e={[math]::Round($_.Length/1e6,2)}},
  @{n='verdict';   e={ if ($_.Length -le 5e6) {'OK'} else {'> 5 Mo - A REDUIRE'} }}
```

### Résultat de l'export d'essai du 2026-09-14 — **la finale ne passe pas**

Procédure du § 3.1 jouée telle quelle sur les deux decks v2, decktape 3 et
Chrome, sortie hors dépôt :

| Deck | Pages | Poids mesuré | Verdict SCEI |
|---|---|---|---|
| `pre-soutenance` | 10 / 10 attendues | **1,38 Mo** | passe, large marge |
| `presentation-finale` | 46 / 46 attendues *(avant les 3 vues ajoutées)* | **5,30 Mo** | **dépasse les 5 Mo** |

> **Mesure périmée sur deux points.** Elle date d'avant (a) le passage de MathJax
> au build SVG vendoré, (b) l'ajout de trois vues. La première change probablement
> le poste dominant du tableau ci-dessous ; la seconde l'augmente un peu. **Re-peser
> avant toute décision, et inscrire la pesée datée au même titre qu'une porte de
> validation : tant qu'elle n'est pas sous 4,9 Mo, le livrable n'existe pas.**

Géométrie vérifiée sur la sortie : page de 768 × 576 pt, soit exactement
1024 × 768 px et un rapport de 1,3333. Le gabarit 4/3 est donc bon ; c'est **le
poids** qui bloque, de 0,30 Mo, soit 6 %.

**Où sont les 5,30 Mo** (analyse du PDF produit) :

| Poste | Poids | Commentaire |
|---|---|---|
| Fontes **Type 3** (glyphes rasterisés, un jeu par vue) | ≈ 3,5 Mo | **446 objets de fonte** pour 46 pages : Chrome n'a pas incorporé les polices vendorées, il a dessiné les glyphes |
| Les deux photos | 0,80 Mo | embarquées **octet pour octet** (377 115 o et 417 917 o : les fichiers d'`assets/` tels quels) |
| Sous-ensembles de polices système réellement incorporés | 0,58 Mo | Arial, Times, Consolas, Segoe UI, Cambria Math |
| Flux de contenu (le dessin vectoriel proprement dit) | 0,19 Mo | négligeable — les schémas SVG ne coûtent rien |
| Structure du fichier (xref, objets compressés, formes) | ≈ 0,3 Mo | incompressible |

L'hypothèse du § 08.2 (« la masse est dans les images ») est donc **fausse pour
ce deck** : les deux photos pèsent 15 % du fichier, les glyphes rasterisés
environ 66 %.

**Si le fichier dépasse, dans cet ordre :**

0. **Re-peser après le correctif MathJax du § 2.** La sortie CHTML faisait dessiner
   les glyphes par Chrome ; le repli sur *Cambria Math* dans la liste des polices
   incorporées en est la signature. C'est la piste « fontes » non testée, et elle
   est gratuite. **Faire ce test avant les deux suivants.**

1. **Les photos — le levier sûr et immédiat.** Elles sont embarquées sans
   recompression, donc tout octet gagné sur le fichier d'`assets/` est un octet
   gagné sur le PDF. Elles sont aujourd'hui **au-dessus** de la règle de 200 ko
   l'unité fixée en § 08.2 : `enceinte-face.jpg` 377 ko, `enceinte-banc.jpg`
   418 ko. Les ramener à 200 ko (largeur ≈ 1200 px, qualité ≈ 80) fait gagner
   ≈ 0,40 Mo et ramène la finale à **≈ 4,9 Mo** : sous la limite, mais avec 2 %
   de marge seulement. C'est un correctif, pas un confort.
2. **Les fontes Type 3 — le vrai gisement, non résolu.** Essais déjà faits, tous
   sans effet sur le poids : `--chrome-arg=--font-render-hinting=none`, et
   l'allongement des pauses de chargement (`--load-pause`, `-p`). La piste la plus
   sérieuse est le point 0 ci-dessus (MathJax CHTML → SVG). Ensuite, si le poids
   n'a pas bougé : export par le mode `?print-pdf` natif de
   reveal.js avec `chrome --headless --print-to-pdf` ; ou passage des polices
   vendorées en formats non subsettés. **À traiter en phase 5**, pas la veille.
3. **Les figures** doivent rester en **SVG inline**, jamais en PNG : c'est ce que
   produisent `python analyse/figures.py` puis
   `python analyse/injecter_figures.py`. Un PNG glissé dans une vue se paie en
   mégaoctets, et les flux vectoriels, eux, ne coûtent rien (0,19 Mo pour
   46 vues).
4. **En dernier recours**, ré-écrire le PDF en abaissant la résolution des seules
   images, le texte restant vectoriel (si Ghostscript est installé — il ne l'est
   pas sur cette machine, donc **non vérifié ici**) :

   ```
   gswin64c -sDEVICE=pdfwrite -dPDFSETTINGS=/ebook -dNOPAUSE -dBATCH -sOutputFile=finale-5mo.pdf presentation-finale.pdf
   ```

   Relire le fichier produit : le texte doit rester sélectionnable.

### Liste de contrôle du PDF sorti

- [ ] **Réseau coupé** : ouvrir les deux HTML et vérifier que *toutes* les formules
      s'affichent (vues 3, 12 et annexes A3, A7, A8, A10). Test ajouté le
      2026-09-14 : c'est précisément celui qui aurait fait tomber le défaut
      MathJax/CDN du § 2. Contrôle complémentaire en console :
      `MathJax.startup.document.outputJax.constructor.NAME` → `SVG`, et aucune
      requête sortante dans l'onglet réseau.
- [ ] **Poids ≤ 5 Mo** (commande ci-dessus) — exigence SCEI.
- [ ] **Sommaire d'annexes** (page 19) : les numéros de page qu'il annonce
      correspondent aux pages réelles du PDF.
- [ ] **Pas de LaTeX dans un `<svg>`** : `grep '\\\\(' *.html` ne doit rien ramener
      à l'intérieur d'un `<text>`. MathJax y insère un `<mjx-container>` HTML que le
      SVG ne rend pas (défaut constaté en vue 5 le 2026-09-14). Notation `<tspan>`.
- [ ] **Format 4/3** : le lecteur PDF annonce 1024 × 768 px (ou 4:3) ; pas de
      bandes noires en haut et en bas.
- [ ] **Compte de pages** conforme au tableau du § 2 (10 / 46).
- [ ] **Numéro de vue visible sur chaque page**, y compris les annexes.
- [ ] Nom, prénom et numéro d'inscription sur la **première** vue.
- [ ] Une vue par page, rien n'est coupé, aucune barre de défilement figée.
- [ ] Formules MathJax nettes (SVG) ; courbes d'impédance et de Bode lisibles,
      axes gradués et légendés.
- [ ] Photos présentes ; **texte sélectionnable** (Ctrl+F dans le PDF sur un mot
      d'une vue de listing : c'est le meilleur test du caractère vectoriel).
- [ ] Les vues de listings sont sur fond clair et le code n'est pas rogné à
      droite (≈ 100 colonnes utiles au maximum).
- [ ] **Les libellés centrés des schémas SVG sont bien dans leur cadre** — voir
      l'anomalie ci-dessous, constatée le 2026-09-14. **Comparer la page du PDF à
      la vue à l'écran**, ce n'est pas la même chose.
- [ ] Aucun placeholder de figure resté visible (`<!--FIG:...-->` non rempli, ou
      bloc `.placeholder` là où une mesure était attendue).

> ### Anomalie ouverte — les libellés `text-anchor="middle"` des SVG dérivent
>
> Mesuré sur l'export d'essai du 2026-09-14, vue 3 de la finale : le libellé
> « R = 8 Ω ? » occupe 262,3 → 304,9 pt alors que le cadre pointillé qui doit le
> contenir va de 307,9 à 405,4 pt. **Le texte tombe entièrement hors de son
> cadre**, et il sort à 10,0 pt au lieu des 12,8 pt attendus. À l'écran, dans le
> navigateur, la même vue est **correcte** : l'anomalie naît à l'export.
>
> Cause : le texte est mesuré avec une police et dessiné avec une autre (les
> fontes Type 3 du § 4), donc le décalage d'ancrage calculé par Chrome ne
> correspond plus aux glyphes tracés. Tous les textes `text-anchor="middle"` des
> SVG sont touchés, proportionnellement à leur longueur ; les textes non ancrés
> (`text-anchor` absent) sont, eux, à leur place.
>
> Reproduit à l'identique avec `--load-pause 4000 -p 1500` : ce **n'est pas** une
> course au chargement des polices. Le correctif est du côté des vues, pas de la
> commande d'export.
>
> **Correctif appliqué le 2026-09-14** : les 63 déclarations `font-family` sans
> pile de repli des SVG de la finale (44 `JetBrains Mono`, 19 `Space Grotesk`) et
> les 20 de la pré-soutenance ont été remplacées par des piles complètes —
> `font-family="'JetBrains Mono', monospace"` et
> `font-family="'Space Grotesk', Inter, sans-serif"`. **Reste à vérifier** :
> ré-exporter et comparer la page 3 du PDF à la vue à l'écran (libellé
> « R = 8 Ω ? » dans son cadre pointillé). À faire dans le même passage que le
> re-test MathJax du § 2, dont le défaut avait la même cause probable.

> **Rappel de fond** : tant que la phase 1 n'a pas eu lieu, les placeholders sont
> **voulus** et doivent rester lisibles comme tels. Ce qu'on vérifie ici, c'est
> qu'aucun marqueur brut ne traîne, pas qu'il n'y a plus de placeholder.

---


### Le plafond de 5 Mo, et comment on le tient

Le paramètre `?export` de l'URL n'est pas décoratif : il retire le fond
quadrillé avant la capture. Chrome rastérise ce fond **page par page**, et
c'est le poste le plus lourd du fichier. Mesures faites le 14/09/2026 sur les
49 vues de la présentation finale :

| Variante | Taille | Verdict |
|---|---|---|
| avec le quadrillage | 5,88 Mo | **dépasse** |
| `?export` (sans quadrillage) | **4,81 Mo** | passe |
| quadrillage élargi à 64 px | 6,32 Mo | pire — voir ci-dessous |

Élargir la grille **n'aide pas** : Chrome ne la carrelle pas, il rastérise le
fond entier, et une image plus contrastée se comprime moins bien. La seule
solution qui marche est de la retirer. Une règle `@media print` ne suffit pas
non plus : decktape pilote Chrome en média **écran**. D'où l'interrupteur
explicite (`?export` → classe `export` sur `<html>` → règle dans
`css/blueprint.css`).

**La marge est mince : 4,81 Mo pour 5 Mo, soit 4 %.** Toute figure ajoutée peut
faire repasser au-dessus. Donc : mesurer la taille **à chaque export**, pas
seulement avant le téléversement. Les deux leviers, dans l'ordre de
préférence :

1. **Les photos.** Elles étaient en 1280×960 pour un affichage à ~450 px :
   ramenées à 900 px et qualité 82, elles sont passées de 776 ko à 187 ko, soit
   0,6 Mo gagnés sur le PDF. Les originaux restent dans `archive-v1/assets/`.
2. **Le nombre d'objets tracés**, et non le poids des SVG. La factorisation des
   styles répétés (`blueprint_mpl._factoriser_styles`) a allégé les SVG de 26 %
   — excellent pour le HTML — sans changer le PDF d'un octet : ce qui compte à
   l'export, c'est le nombre de marqueurs dessinés. Pour alléger vraiment,
   réduire la densité de points affichés ou rastériser la couche de données.

Si malgré tout le fichier dépasse, la coupe la moins coûteuse est de sortir les
vues de listings (16 vues, ~1,1 Mo) dans un PDF séparé — elles doivent de toute
façon être apportées en double exemplaire papier.

## 5. Le papier : les listings en double exemplaire

Obligation SCEI, citée littéralement en `REFERENCE-TECHNIQUE.md` § 08.1 : les
listings des programmes développés sont **apportés en double exemplaire sur
support papier**, *et* inclus en documents annexes à la présentation, **en aval
de la conclusion**. Ils ne sont pas présentés pendant l'exposé mais peuvent faire
l'objet de questions pendant l'entretien. Fond blanc fortement recommandé.

Ce sont donc **deux livrables distincts**, et il faut les deux :

| Livrable | Ce que c'est | Comment on le produit |
|---|---|---|
| Annexes du PDF | les vues `L0`–`L9`, après la conclusion, dans `presentation-finale.pdf` | elles sortent avec le deck (§ 3.1) |
| **Papier ×2** | les mêmes pages, imprimées, en **deux jeux** | imprimer les pages `L0`–`L9` de `presentation-finale-clair.pdf`, ou le noyau imprimé décrit dans `analyse/LISEZMOI.md` |

Le noyau imprimé tient en 10 à 15 pages : seulement les fonctions que le récit
cite et sur lesquelles Thomas doit pouvoir être interrogé. Le reste du dossier
`analyse/` (**18 002 lignes**, dont 3 637 de tests — comptage du 2026-09-14, à
reprendre par `tout_refaire.py` plutôt qu'à retaper) n'est **pas** imprimable et
ne doit pas l'être ; il est annoncé par une page de garde donnant l'URL du dépôt, le commit,
la commande de régénération (`python analyse/tout_refaire.py`) et l'empreinte
SHA-256 du journal. Règle et gabarit de la page de garde : `analyse/LISEZMOI.md`.

À imprimer aussi, comme document papier personnel (autorisé, mais le jury n'est
pas tenu d'en tenir compte) : les **notes du présentateur**. Elles vivent dans
les `<aside class="notes">` et **n'existent pas** sur l'ordinateur du jury.

---

## 6. Repli bitmap (si decktape est indisponible)

Méthode de secours, à n'employer que si `npx decktape` échoue : capturer chaque
vue avec Chrome en mode headless, puis assembler.

```powershell
$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
& $chrome --headless --screenshot=_pdfbuild\vue-01.png --window-size=1024,768 `
          --force-device-scale-factor=1.5 --hide-scrollbars `
          "http://localhost:8123/presentation-finale.html?export#/0"
```

puis assembler avec `img2pdf`. Le dossier de travail est `_pdfbuild/`
(déjà ignoré par git).

Trois avertissements, dans l'ordre d'importance :

1. **Le texte n'est plus sélectionnable** : le PDF devient une suite d'images. On
   perd le Ctrl+F, et surtout la lisibilité des listings à l'impression.
2. **Le poids explose.** 46 pages bitmap tiennent très mal sous 5 Mo :
   convertir les captures en JPEG (qualité ≈ 85) avant `img2pdf`, et rester à
   `--force-device-scale-factor=1.5` (1536 × 1152 px) plutôt que 2. Mesurer
   après chaque essai, avec la commande du § 4 — l'ordre de grandeur donné ici
   n'a pas été vérifié sur la v2.
3. La page finale doit conserver le **rapport 4/3** : si `img2pdf` impose un
   format de page (A4), le fixer explicitement en paysage, sinon le jury projette
   un document aux mauvaises marges.

---

## 7. Divergences connues

- `README.md` donne `python -m http.server 8000`, `.claude/launch.json` donne
  **8123** (et l'ancienne version de ce fichier donnait 8090). Le port qui fait
  foi est celui de `launch.json` — **8123** — repris partout ci-dessus. Le
  `README.md` reste à aligner : il n'est pas modifié ici.
- Le port n'a aucune importance fonctionnelle : n'importe quel port libre
  convient, à condition qu'il soit le même dans la commande `http.server` et
  dans l'URL passée à decktape.
