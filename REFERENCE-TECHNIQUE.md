# Référence technique — TIPE v2 (optimisation du filtre sur charge réelle)

*Assemblé le 13 septembre 2026. Thomas Mareel, TIPE session 2027, thème « Sobriété, efficacité, optimisation ».*

> **Avertissement — à lire avant d'utiliser le moindre chiffre de ce document.**
> Ceci est un **document de référence théorique et méthodologique**. **Aucune valeur
> qui y figure n'est une mesure faite sur l'enceinte du projet.** Les nombres sont soit
> des identités vérifiées par le calcul, soit des sorties de scripts exécutés sur des
> données **synthétiques**, soit des **ordres de grandeur** tirés de datasheets ou de
> fiches produit publiques — auquel cas ils sont étiquetés comme tels sur place.
> Les marques `[[à mesurer]]` et `[[à vérifier]]` signalent les trous à combler : elles
> sont toutes recensées, avec leur section d'origine, dans l'[index final](#index-marques),
> et elles sont à traiter. Tant qu'une marque n'est pas levée, la phrase qui la porte
> n'est **pas** un résultat et ne doit être présentée ni au jury ni dans le MCOT.

## <a id="role"></a>Rôle de ce document

`FEUILLE-DE-ROUTE.md` dit **quoi** faire et **quand** : les phases, les portes de
validation, les critères gelés, le calendrier. Ce document-ci en est le compagnon et dit
**comment** et **pourquoi** : les modèles et leurs démonstrations, les montages de mesure,
les budgets d'incertitude, les choix numériques, les pièges connus et les sources. Les deux
se lisent ensemble — la feuille de route reste la référence unique pour l'ordonnancement
des phases, et cette référence technique ne la duplique pas.

Il n'est pas fait pour être lu d'un bout à l'autre : on y entre par la table des matières,
au moment d'exécuter une phase. Chaque section se termine par un bloc **« Ce qu'il faut
retenir pour l'oral »** — la version courte, celle qui tient dans les 15 minutes d'exposé —
et par ses **« Sources »**. Le détail vit ici ; l'exposé, lui, reste court.

Conventions : tout en français ; formules en LaTeX (`$…$` en ligne, `$$…$$` en bloc) ;
aucun résultat inventé ; les renvois internes s'écrivent « § 04.5 » et pointent vers la
sous-section correspondante de ce document.

## <a id="sommaire"></a>Table des matières


**[01. Modèle électroacoustique du haut-parleur et impédance Z(f)](#s01)**

- [01.1 Ce que « voit » le filtre — et ce que « $f_x$ » veut dire](#s01-1)
- [01.2 Les trois étages du haut-parleur électrodynamique](#s01-2)
- [01.3 Impédance aux bornes : la branche motionnelle](#s01-3)
- [01.4 Facteurs de qualité et formules de passage](#s01-4)
- [01.5 Vérification numérique du modèle](#s01-5)
- [01.6 Ce que $Z(f)$ détermine — et ce qu'elle ne détermine pas](#s01-6)
- [01.7 Allure de $|Z|$ et de la phase](#s01-7)
- [01.8 « Du simple au sextuple » — et ce que la charge fait vraiment au filtre](#s01-8)
- [01.9 Effet de la caisse close](#s01-9)
- [01.10 Effet du bass-reflex — le cas réel du projet](#s01-10)
- [01.10 bis Prédire $f_b$ au pied à coulisse : résonateur de Helmholtz à $N$ évents](#s01-10bis)
- [01.11 Du modèle électrique à la réponse acoustique](#s01-11)
- [01.12 Limites du modèle](#s01-12)
- [01.13 Ordres de grandeur typiques (datasheets publiques, NON mesurés sur l'enceinte)](#s01-13)
- [01.14 Ce que la section engage pour les phases 1 et 2](#s01-14)

**[02. Mesure de l'impédance Z(f) : montage, formules, incertitudes](#s02)**

- [02.1 Principe : diviseur de tension à résistance étalon, sans hypothèse de courant constant](#s02-1)
- [02.2 Câblage : le problème de la masse et les trois configurations](#s02-2)
- [02.3 Phase : décalage temporel ou figure de Lissajous](#s02-3)
- [02.4 Choix de $R_{ref}$ et de la configuration](#s02-4)
- [02.5 Niveau de signal : régime petits signaux](#s02-5)
- [02.6 Bande, grille de fréquences et répartition des rôles](#s02-6)
- [02.7 Propagation des incertitudes](#s02-7)
- [02.8 Étalonnage sur composants connus et porte de validation](#s02-8)
- [02.9 Variante rapide : carte son + REW, et jig derrière l'amplificateur](#s02-9)
- [02.10 Pièges](#s02-10)
- [02.11 Protocole reproductible](#s02-11)
- [02.12 Tableau de relevé et contrat d'interface avec l'acte 2](#s02-12)

**[03. Problème inverse : identification des paramètres de Thiele-Small](#s03)**

- [03.1 Le modèle direct : du haut-parleur au dipôle électrique](#s03-1)
- [03.2 Du problème direct au problème inverse : les moindres carrés](#s03-2)
- [03.3 Initialisation lue sur la courbe, et multi-départ](#s03-3)
- [03.4 Le code, exécuté sur données synthétiques](#s03-4)
- [03.5 Incertitudes des paramètres : ce que chaque estimateur teste, et ce qu'il ne teste pas](#s03-5)
- [03.6 Bande d'ajustement : le vrai risque n'est pas la variance sur $L_e$, c'est un biais sur $R_e$](#s03-6)
- [03.7 Critères de validation de l'identification (à geler avant l'ajustement sur les vraies mesures)](#s03-7)
- [03.8 Ce qu'il faut présenter au jury, et ce qu'il faut livrer à l'acte 3](#s03-8)

**[04. Filtre de raccord sur charge réelle et formulation de l'optimisation](#s04)**

- [04.1 Cellules passives du second ordre chargées par une impédance quelconque](#s04-1)
- [04.2 La même cellule sur une charge $Z(f)$ réaliste](#s04-2)
- [04.3 Cible de sommation : Butterworth 2 ou somme plate ?](#s04-3)
- [04.4 Réseau de Zobel et compensation de résonance](#s04-4)
- [04.5 Formulation du problème d'optimisation](#s04-5)
- [04.6 Squelette Python exécuté](#s04-6)
- [04.7 Sanity check (porte de validation de la phase 3) et recoupement scipy](#s04-7)
- [04.8 Illustration sur la charge typique (synthétique — à refaire sur $Z(f)$ mesurée)](#s04-8)
- [04.9 Propagation des incertitudes](#s04-9)
- [04.10 Contre-vérification LTspice (phase 3)](#s04-10)
- [04.11 Référence active Sallen-Key : pourquoi elle ne voit pas $Z(f)$](#s04-11)

**[05. Conception de la self : inductance, cuivre, pertes, fabrication](#s05)**

- [05.1 Ce qu'on demande à la self de grave](#s05-1)
- [05.2 Inductance d'une bobine à air : la formule de Wheeler multicouche, en SI](#s05-2)
- [05.3 La bobine de Brooks : la constante, vérifiée (et une erreur à ne pas propager)](#s05-3)
- [05.4 Pourquoi Brooks maximise $L$ à longueur de fil donnée](#s05-4)
- [05.5 Le fil : table calculée](#s05-5)
- [05.6 La loi $r\times m$ : démonstration, puis sa correction exacte](#s05-6)
- [05.7 Trois selfs de 18 mH, et une validation externe](#s05-7)
- [05.8 Formulation de l'optimisation : minimiser le cuivre sous contraintes](#s05-8)
- [05.9 Ce que la section 04 doit reprendre : `dcr(L)` et `prix_L(L)`](#s05-9)
- [05.10 Coût du fil, budget réel, et ce que le marché vend vraiment à 18 mH](#s05-10)
- [05.11 Alternative noyau ferrite/fer : ce qu'on gagne, ce qu'on risque](#s05-11)
- [05.12 Fabrication pratique](#s05-12)
- [05.13 Mesure de $L$ : d'abord le banc d'impédance, la résonance en contre-vérification](#s05-13)
- [05.14 Mesure de $r$ : quatre fils, cordons, cosses, et budget d'incertitude](#s05-14)
- [05.15 Effet de peau et effet de proximité à 100 Hz](#s05-15)

**[06. Pertes, compression thermique et croisement énergétique passif / actif](#s06)**

- [06.1 Pertes Joule dans la self série du passe-bas](#s06-1)
- [06.2 Les autres résistances du filtre](#s06-2)
- [06.3 L-pad d'égalisation : une perte qui achète de l'immunité à $\underline Z(f)$](#s06-3)
- [06.4 Résistance série totale et amortissement : DCR et échauffement sont le même levier](#s06-4)
- [06.5 Compression thermique et dérive du raccord](#s06-5)
- [06.6 Mesurer la dérive de $R_e$ sans démonter le haut-parleur](#s06-6)
- [06.7 Côté actif : consommation au repos et rendement de l'ampli](#s06-7)
- [06.8 Point de croisement énergétique](#s06-8)
- [06.9 Présenter l'argument « sobriété » honnêtement](#s06-9)

**[07. Validation acoustique : protocole de mesure au micro à 100 Hz](#s07)**

- [Conventions gelées avant toute mesure](#s07-0)
- [07.1 Pourquoi la pièce domine sous 150 Hz](#s07-1)
- [07.2 Pourquoi le fenêtrage temporel (gating) est inopérant en basses fréquences](#s07-2)
- [07.3 Mesure en champ proche (Keele, 1974)](#s07-3)
- [07.4 Mesurer la somme des deux voies alors que les sources sont séparées](#s07-4)
- [07.5 Inversion de polarité et vérification de la phase relative](#s07-5)
- [07.6 Égalisation des niveaux entre voies](#s07-6)
- [07.7 Mesures électriques préalables (Bode)](#s07-7)
- [07.8 Protocole reproductible aux deux niveaux d'écoute de référence](#s07-8)
- [07.9 Critère « écart RMS à la cible en dB sur 40–250 Hz »](#s07-9)
- [07.10 REW en pratique](#s07-10)
- [07.11 Sécurité](#s07-11)

**[08. Cadre du TIPE (SCEI, session 2027) et attentes du jury](#s08)**

- [08.1 Le thème 2026-2027 : source officielle](#s08-1)
- [08.2 Format de l'épreuve orale (règlement session 2026, à reconfirmer pour 2027)](#s08-2)
- [08.3 Les livrables : titre, MCOT et DOT](#s08-3)
- [08.4 Calendrier : sessions passées (vérifiées) et session 2027 (à confirmer)](#s08-4)
- [08.5 Les six critères officiels et la réponse du sujet v2](#s08-5)
- [08.6 Erreurs classiques relevées par le jury, et points de vigilance propres au projet](#s08-6)
- [08.7 Vérifications numériques : le budget temps, le budget mots et le budget taille](#s08-7)

**[09. Architecture du code d'analyse Python (dossier `analyse/`)](#s09)**

- [09.1 Quatre principes de conception](#s09-1)
- [09.2 Arborescence proposée](#s09-2)
- [09.3 Formats de données](#s09-3)
- [09.4 Fonctions clés (signatures à geler)](#s09-4)
- [09.5 Dépendances, et repli sans SciPy](#s09-5)
- [09.6 Tests de non-régression](#s09-6)
- [09.7 Figures : identité Blueprint](#s09-7)
- [09.8 Reproductibilité](#s09-8)

**[Index des points `[[à vérifier]]` et `[[à mesurer]]`](#index-marques)**

## <a id="s01"></a>01. Modèle électroacoustique du haut-parleur et impédance Z(f)

> Objet de la section : établir le modèle **direct** $Z(j\omega)$ que la phase 2 ajustera sur les mesures de la phase 1, dire **ce que ce modèle permet d'identifier et ce qu'il ne permet pas**, et comprendre pourquoi un haut-parleur « 8 Ω » n'est 8 Ω à peu près nulle part. **Aucune valeur de cette section n'est mesurée sur l'enceinte de Thomas** : les chiffres sont soit des identités vérifiées numériquement, soit des ordres de grandeur issus de datasheets publiques, clairement étiquetés.

### <a id="s01-1"></a>01.1 Ce que « voit » le filtre — et ce que « $f_x$ » veut dire

Le filtre passif de raccord est un diviseur d'impédance : sa fonction de transfert dépend de la charge. Pour le passe-bas $L_1$ série / $C_1$ parallèle chargé par $Z$ :

$$
\underline{H}_{PB}(j\omega)=\frac{1}{1-L_1C_1\omega^2+\dfrac{j\omega L_1}{Z(j\omega)}}
$$

Sur une résistance $R$, le terme $j\omega L_1/R$ fixe le facteur de qualité $Q=R\sqrt{C_1/L_1}$ ; c'est ainsi qu'on obtient les valeurs « catalogue » pour $R=8\ \Omega$. Si $Z$ dépend de la fréquence, $Q$ en dépend aussi, en module **et** en phase : en écrivant $Z=R_p+jX$, le terme devient $\dfrac{\omega L_1 X}{|Z|^2}+j\dfrac{\omega L_1R_p}{|Z|^2}$, dont la **partie réelle s'ajoute à $1-L_1C_1\omega^2$** — une charge réactive ($X\neq0$) déplace donc l'annulation du dénominateur, c'est-à-dire le pôle lui-même. Tout le sujet v2 tient dans cette ligne : il faut connaître $Z(j\omega)$, puis concevoir le filtre pour cette charge-là. Le § 01.8 chiffre l'effet ; il est loin d'être uniforme sur toute la bande.

**Convention de nommage, à tenir dans tout le mémoire.** Deux fréquences différentes ont porté le nom « $f_c$ » dans les brouillons v1, ce qui est intenable à l'oral. On fixe :

| Symbole | Désigne | Ordre de grandeur ici |
|---|---|---|
| $f_x$ | fréquence de **raccord** du filtre = **croisement des deux voies**, $\lvert H_{PB}G_{sub}\rvert=\lvert H_{PH}G_{med}\rvert$ (**définition unique du TIPE, posée au § 04.1**) | 100 Hz (cible) |
| $f_0$ | **repère**, pas une définition de $f_x$ : le **pôle** du couple $L_1C_1$, $1/(2\pi\sqrt{L_1C_1})$ | 96,9 Hz (E12 réalisé) |
| $f_s$ | résonance du haut-parleur **en champ libre** | 30–40 Hz (18″) |
| $f_c$ | résonance du haut-parleur **en caisse close** (notation de Small) | 45–70 Hz |
| $f_b$ | fréquence d'**accord** de l'évent (bass-reflex) | 30–40 Hz |

> **Piège de notation, à dire une fois et à tenir.** Le symbole $f_c$ est **surchargé** : dans la notation de Small (ligne 3 du tableau) il désigne la résonance du haut-parleur **en caisse close**, alors que les sections 04 à 09 l'emploient couramment pour la **fréquence de raccord du filtre**. Les deux usages sont légitimes dans leur littérature d'origine, mais ils ne doivent jamais se croiser dans une même phrase. Règle : **quand il y a le moindre risque, écrire $f_x$ pour le raccord** (croisement des deux voies, § 04.1) et réserver $f_c$ à la caisse close ; quand le contexte est sans ambiguïté — toute la section 04, par exemple, où il n'est question que du filtre — « $f_c$ » signifie le raccord, c'est-à-dire **le croisement**, et jamais le pôle ni un $-3$ dB.

Le choix de définition n'est pas neutre, et il faut le dire : quatre candidates circulent (croisement des deux voies, pôle, $-3$ dB du passe-bas, $-3$ dB du passe-haut) et elles ne coïncident que sur une charge résistive sans DCR **et** pour $Q=1/\sqrt2$ **exact**. Le § 04.1 tranche — $f_x$ est **le croisement**, parce que c'est la seule grandeur insensible à la perte d'insertion et la seule qui reste interprétable sur la charge réelle — et les trois autres restent des **repères nommés**. Sortie de `filtre_sur_charge.py` (charge 8 Ω résistifs ; seuil « −3 dB » = mi-puissance $-3{,}0103$ dB, § 04.1) :

```
--- Butterworth theorique : L = 18.0063 mH, C = 140.67 uF ---
    pole 1/(2 pi sqrt(LC)) = 100.00 Hz ; Q = R sqrt(C/L) = 0.7071 ; -3 dB PB = 100.00 Hz
    pole 1/(2 pi sqrt(LC)) = 100.00 Hz ; Q = R sqrt(C/L) = 0.7071 ; -3 dB PH = 100.00 Hz
--- E12 realise : L = 18.0000 mH, C = 150.00 uF ---
    pole 1/(2 pi sqrt(LC)) = 96.86 Hz ; Q = R sqrt(C/L) = 0.7303 ; -3 dB PB = 99.93 Hz
    pole 1/(2 pi sqrt(LC)) = 96.86 Hz ; Q = R sqrt(C/L) = 0.7303 ; -3 dB PH = 93.88 Hz
```

Il faut donc distinguer deux filtres « catalogue », et ne jamais les confondre :

- **catalogue théorique** : $L_1=\sqrt2\,R/\omega_x=18{,}006$ mH, $C_1=1/(\sqrt2R\omega_x)=140{,}67$ µF — les quatre candidates donnent 100,00 Hz ;
- **catalogue réalisé (E12)** : $L_1=18$ mH, $C_1=150$ µF — $Q=0{,}730$, et les trois **repères** donnent 96,9 / 99,9 / 93,9 Hz, soit **6 % d'écart entre eux** ; sur cette charge idéale le **croisement** $f_x$ tombe sur le pôle, à 96,9 Hz. C'est ce filtre-là qui sera construit et mesuré, et c'est de son **croisement** que l'on parlera — le pôle n'étant cité que comme repère, et comme la seule des quatre grandeurs qui soit fonction directe de $L_1$ et $C_1$.

**Incertitude de composants : elle se propage sur le pôle $f_0$.** Comme $f_0=1/(2\pi\sqrt{L_1C_1})$, la propagation logarithmique donne

$$
\frac{u(f_0)}{f_0}=\frac12\sqrt{\left(\frac{u_L}{L_1}\right)^2+\left(\frac{u_C}{C_1}\right)^2}
$$

soit, pour $L$ et $C$ à ±10 %, **7,1 % en borne au pire cas** et **4,1 % en incertitude-type** (loi rectangulaire, GUM : $u=10/\sqrt3=5{,}8$ % par composant) — les deux chiffres se citent **toujours en couple**, jamais l'un seul ; 11,2 % en borne au pire cas si $C$ est à ±20 % (électrolytique bipolaire). Le facteur $\tfrac12$ vient de la racine carrée : c'est la différence avec un premier ordre $RC$, où l'exposant vaut 1 et où l'on trouverait 14 % au lieu de 7 %. Le report sur $f_x$ (le croisement) n'est exact que sur charge résistive sans DCR, où $f_x=f_0$ ; sur la charge réelle il passe par le Monte-Carlo du § 04.9.

<!-- Le "11 %" de la v1 était la formule du RC 1er ordre (architecture abandonnée) : la coïncidence numérique avec le cas "C à +-20 %" ci-dessus est fortuite, elle ne doit jamais servir d'argument. -->

### <a id="s01-2"></a>01.2 Les trois étages du haut-parleur électrodynamique

Un haut-parleur à bobine mobile couple trois domaines :

| Étage | Grandeurs | Équation (petit signal, régime linéaire) |
|---|---|---|
| Électrique | tension $u$, courant $i$ | $u = R_e\,i + L_e\,\dfrac{di}{dt} + Bl\,v$ |
| Mécanique | vitesse $v$, position $x$ | $M_{ms}\dfrac{dv}{dt} = Bl\,i - R_{ms}\,v - \dfrac{x}{C_{ms}}$ |
| Acoustique | pression, débit $S_d\,v$ | charge de rayonnement et de caisse, renvoyée côté mécanique |

avec :

- $R_e$ : résistance de la bobine (Ω) ;
- $L_e$ : inductance de la bobine (H), idéalisée ici comme constante ;
- $Bl$ : facteur de force (T·m, ou N/A) — la même constante sert à la force de Laplace $F=Bl\,i$ et à la f.é.m. induite $e=Bl\,v$ ;
- $M_{ms}$ : masse mobile (kg), membrane + bobine + charge d'air ;
- $C_{ms}$ : compliance de la suspension (m/N), inverse d'une raideur ;
- $R_{ms}$ : résistance mécanique de pertes (kg/s ou N·s/m).

**$R_e$ mérite un paragraphe à lui seul**, parce que c'est le paramètre le plus sensible de toute la chaîne : il entre linéairement dans $Q_{es}=R_e\sqrt{C_{mes}/L_{ces}}$, dans $r_0=|Z|_{max}/R_e$ et dans $R_{es}=R_eQ_{ms}/Q_{es}$. Or les cordons d'un multimètre de lycée valent couramment 0,2 à 0,5 Ω [[à vérifier sur l'appareil du lycée, cordons court-circuités]], soit **4 à 10 % de $R_e\approx5$ Ω** — et comme $Q_{es}\propto R_e$, on a directement $u(Q_{es})/Q_{es}=u(R_e)/R_e$ : une erreur de 0,3 Ω non compensée biaise $Q_{es}$ de 6 % en silence. En pratique : compenser les cordons (fonction REL/zéro), ou mieux, mesurer $R_e$ **par la même méthode à deux voltmètres à très basse fréquence** (5–10 Hz), où la branche motionnelle est encore petite (§ 01.7 : $|Z|=5{,}45$ Ω à 5 Hz pour $R_e=5{,}00$ Ω, soit +9 % — donc extrapoler, pas lire brut).

Les paramètres $Bl$, $M_{ms}$, $C_{ms}$, $R_{ms}$, complétés par $f_s$, $Q_{ms}$, $Q_{es}$, $Q_{ts}$ et $V_{as}$, sont les **paramètres de Thiele-Small** (Thiele 1961/1971, Small 1972). Ce sont des paramètres **petit signal** : ils supposent $Bl$, $C_{ms}$ et $R_e$ indépendants de l'excursion et de la température (voir § 01.12).

### <a id="s01-3"></a>01.3 Impédance aux bornes : la branche motionnelle

En régime sinusoïdal, l'équation mécanique donne l'impédance mécanique

$$
\underline{Z}_m(j\omega)=R_{ms}+j\omega M_{ms}+\frac{1}{j\omega C_{ms}},\qquad \underline{v}=\frac{Bl\,\underline{i}}{\underline{Z}_m}.
$$

La f.é.m. induite $Bl\,\underline{v}=\dfrac{(Bl)^2}{\underline{Z}_m}\,\underline{i}$ apparaît côté électrique comme une impédance supplémentaire, dite **motionnelle** :

$$
\boxed{\;\underline{Z}(j\omega)=R_e+j\omega L_e+\underline{Z}_{mot}(j\omega),\qquad \underline{Z}_{mot}=\frac{(Bl)^2}{\underline{Z}_m}\;}
$$

Inverser $\underline{Z}_m$ transforme la série mécanique $R_{ms}$–$M_{ms}$–$C_{ms}$ en un **RLC parallèle** électrique :

$$
\underline{Z}_{mot}=\left(\frac{1}{R_{es}}+\frac{1}{j\omega L_{ces}}+j\omega C_{mes}\right)^{-1}
$$

| Élément électrique équivalent | Expression | Origine mécanique | Contrôle dimensionnel |
|---|---|---|---|
| $R_{es}$ (Ω) | $\dfrac{(Bl)^2}{R_{ms}}$ | pertes mécaniques | $\mathrm{(N/A)^2/(N{\cdot}s/m)=W/A^2=\Omega}$ |
| $L_{ces}$ (H) | $(Bl)^2\,C_{ms}$ | compliance (ressort) | $\mathrm{(N/A)^2{\cdot}(m/N)=J/A^2=H}$ |
| $C_{mes}$ (F) | $\dfrac{M_{ms}}{(Bl)^2}$ | masse mobile | $\mathrm{kg{\cdot}A^2/N^2=A^2s^4/(kg{\cdot}m^2)=F}$ |

Le couplage $Bl$ est un **gyrateur** : une masse devient une capacité, un ressort devient une inductance, et un circuit série devient un circuit parallèle. C'est pour cela que la résonance mécanique se manifeste par un **maximum** d'impédance (résonance parallèle), et non un minimum.

Conséquence immédiate, et utile au banc : $\underline{Z}_{mot}$ est l'impédance d'un **RLC parallèle passif**, donc $\mathrm{Re}(\underline{Z}_{mot})\ge0$ et par suite $|Z|\ge|\mathrm{Re}(Z)|\ge R_e$ **à toute fréquence**. Toute mesure donnant $|Z|<R_e$ signale un défaut de la chaîne de mesure, pas un haut-parleur.

### <a id="s01-4"></a>01.4 Facteurs de qualité et formules de passage

Fréquence de résonance (identique dans les deux domaines puisque $L_{ces}C_{mes}=M_{ms}C_{ms}$) :

$$
f_s=\frac{1}{2\pi\sqrt{M_{ms}C_{ms}}}=\frac{1}{2\pi\sqrt{L_{ces}C_{mes}}}
$$

Facteurs de qualité à $f_s$ :

$$
Q_{ms}=\frac{\omega_s M_{ms}}{R_{ms}}=R_{es}\sqrt{\frac{C_{mes}}{L_{ces}}},\qquad
Q_{es}=\frac{\omega_s M_{ms}R_e}{(Bl)^2}=R_e\sqrt{\frac{C_{mes}}{L_{ces}}},\qquad
\frac{1}{Q_{ts}}=\frac{1}{Q_{ms}}+\frac{1}{Q_{es}}
$$

$Q_{ms}$ ne contient que les pertes mécaniques ; $Q_{es}$ décrit l'amortissement **électrique** apporté par $R_e$ (la f.é.m. induite débite dans $R_e$ **et dans tout ce qui est en série** : impédance de sortie de l'ampli, câble, DCR de la self). $Q_{ts}$ combine les deux comme des résistances en parallèle vues de la branche motionnelle.

**Ce que « en série » coûte, chiffré** (jeu du § 01.5) — c'est l'argument physique derrière le terme « DCR » de la fonction de coût de la phase 3 :

```
=== Resistance serie R_add : Qes proportionnel a (Re + R_add) ===
  R_add = 0.0 ohm : Qes = 0.321 (+0.0 %)  Qts = 0.305 (+0.0 %)
  R_add = 0.2 ohm : Qes = 0.333 (+4.0 %)  Qts = 0.316 (+3.8 %)
  R_add = 0.5 ohm : Qes = 0.353 (+10.0 %)  Qts = 0.333 (+9.5 %)
  R_add = 1.0 ohm : Qes = 0.385 (+20.0 %)  Qts = 0.362 (+18.8 %)
```

Une self de 18 mH bobinée maison aura une DCR de l'ordre de l'ohm : elle relâche donc l'amortissement du grave de près de 20 %, **en plus** de dissiper 11 % de la puissance (§ 01.8). Ce qui est en série *avant* le haut-parleur compte, et ce qui l'est *dans* la chaîne aussi : le t.amp E-800 annonce un facteur d'amortissement > 160 (constructeur, référencé à 8 Ω), soit $Z_{out}<8/160=50$ mΩ — négligeable ; le câble HP, lui, vaut 0,041 Ω en 2,5 mm² sur 3 m et 0,115 Ω en 1,5 mm² sur 5 m, soit 0,8 % à 2,3 % de $R_e$ — négligeable aussi, mais à mentionner plutôt qu'à supposer.

Trois relations de passage utiles au fit et à l'oral :

$$
\frac{R_{es}}{R_e}=\frac{Q_{ms}}{Q_{es}},\qquad
|Z|_{max}=R_e+R_{es}=R_e\left(1+\frac{Q_{ms}}{Q_{es}}\right)\ \text{(à } f_s\text{, si } \omega_sL_e\ll R_e+R_{es}\text{)},\qquad
V_{as}=\rho_0c^2S_d^2C_{ms}
$$

La condition porte bien sur $R_e+R_{es}$ et non sur $R_e$ seul : à $f_s$ la branche motionnelle vaut $R_{es}$ (réelle), donc $|Z(f_s)|=\sqrt{(R_e+R_{es})^2+(\omega_sL_e)^2}$. Sur le jeu du § 01.5, $\omega_sL_e=0{,}37$ Ω contre $R_e+R_{es}=101$ Ω : l'erreur relative vaut $(\omega_sL_e)^2/2(R_e+R_{es})^2\approx7\cdot10^{-6}$. Écrire la condition sur $R_e$ seul (0,37 Ω contre 5 Ω) ferait rejeter à tort l'identité pour un haut-parleur à fort $L_e$. En revanche, $L_e$ décale légèrement la **fréquence** du maximum de $|Z|$ par rapport à $f_s$ — décalage invisible ici à la résolution du script, à vérifier sur la mesure réelle.

$V_{as}$ est le volume d'air dont la compliance acoustique égale celle de la suspension ; il n'intervient pas dans $Z(f)$ en champ libre mais gouverne l'effet de la caisse (§ 01.9).

**Méthode « $r_0$ » (Small 1972) — extraire $Q_{ms}$, $Q_{es}$ d'une courbe $|Z|$ sans fit.** On lit $r_0=|Z|_{max}/R_e$ et les deux fréquences $f_1<f_s<f_2$ où $|Z|=\sqrt{r_0}\,R_e=\sqrt{R_e|Z|_{max}}$ ; alors

$$
f_s\approx\sqrt{f_1f_2},\qquad Q_{ms}=\frac{f_s\sqrt{r_0}}{f_2-f_1},\qquad Q_{es}=\frac{Q_{ms}}{r_0-1}.
$$

C'est la méthode historique, et elle reste précieuse comme **calcul de tête, valeur initiale et recoupement** du fit de la phase 2. Il faut en revanche cesser de dire que « c'est ce que fait REW » : la documentation de REW indique explicitement qu'il procède par *« least squares fit of an electrical model of the drive unit impedance »*, sur un modèle à composants $R_E$ + $dR$ + $L_{EB}$ série + ($L_E$ // $K_E$ // $R_{SS}$) — donc **semi-inductance comprise** (§ 01.12) — et qu'il offre quatre protocoles (champ libre, masse ajoutée, caisse close, double masse ajoutée). Le fit maison de la phase 2 n'est donc pas original par son principe ; il l'est par ce qu'il rend **explicite** : le choix du modèle, la bande d'ajustement, les résidus et les incertitudes des paramètres, que REW ne publie pas. Les deux résultats doivent se recouper — c'est un contrôle croisé gratuit, et c'est la réponse à l'objection « le logiciel gratuit le fait déjà ».

### <a id="s01-5"></a>01.5 Vérification numérique du modèle

Script exécuté (`scratchpad/sec01/modele_ts.py`, numpy seul). Le jeu de paramètres est un **ordre de grandeur « 18 pouces sono 8 Ω » recalé sur les fiches du § 01.13** ($M_{ms}\approx150$ g, $Bl\approx24$ T·m, $S_d\approx1190$ cm², $R_e\approx5$ Ω, $L_e\approx1{,}5$ mH) : les cinq grandeurs tombent dans les fourchettes annoncées plus loin. **Il n'est mesuré sur rien** et ne décrit aucun produit existant.

<!-- Le jeu du brouillon (Mms = 250 g, fs = 26 Hz, Qms = 5,10) était HORS des fourchettes que la section revendique elle-meme : trois grandeurs sur cinq. Recalage retenu plutot que simple ré-étiquetage, pour rendre les § 01.5, 01.8 et 01.13 mutuellement cohérents. Tous les chiffres aval ont été recalculés. -->

```python
import numpy as np

def Z_ts(f, Re, Le, Res, Lces, Cmes):
    """Impédance aux bornes : Re + jwLe + branche motionnelle RLC parallèle."""
    w = 2*np.pi*f
    Ymot = 1/Res + 1/(1j*w*Lces) + 1j*w*Cmes
    return Re + 1j*w*Le + 1/Ymot

def meca_vers_elec(Bl, Mms, Cms, Rms):
    return Bl**2/Rms, Bl**2*Cms, Mms/Bl**2          # Res, Lces, Cmes

def facteurs_qualite(Re, Bl, Mms, Cms, Rms):
    ws = 1/np.sqrt(Mms*Cms)
    Qms = ws*Mms/Rms; Qes = ws*Mms*Re/Bl**2
    return ws/(2*np.pi), Qms, Qes, Qms*Qes/(Qms+Qes)

Re, Le = 5.0, 1.5e-3                                # ohm, H   (ordre de grandeur)
Bl, Mms, Cms, Rms = 24.0, 0.150, 1.1e-4, 6.0        # T.m, kg, m/N, kg/s
Res, Lces, Cmes = meca_vers_elec(Bl, Mms, Cms, Rms)
fs, Qms, Qes, Qts = facteurs_qualite(Re, Bl, Mms, Cms, Rms)
```

Sortie (extraits) :

```
Res = 96.0 ohm   Lces = 63.4 mH   Cmes = 260 uF
fs = 39.2 Hz   Qms = 6.15   Qes = 0.321   Qts = 0.305
controle : fs(elec) = 39.2 Hz ; Qms(elec) = 6.15 ; Qes(elec) = 0.321
controle : Res = Re*Qms/Qes = 96.0 ohm ; |Z|max attendu = Re+Res = 101.0 ohm
controle : Zmax/Re = 1 + Qms/Qes = 20.2
|Z| max = 101.0 ohm a 39.2 Hz ; phase au pic = -0.0 deg
|Z| min au-dessus du pic = 5.06 ohm a 264 Hz
  approximation 1/(2 pi sqrt(Le Cmes)) = 255 Hz
  f =    20 Hz : |Z| =  12.47 ohm, phase =   60.2 deg
  f =    50 Hz : |Z| =  31.58 ohm, phase =  -62.8 deg
  f =   100 Hz : |Z| =   8.34 ohm, phase =  -48.4 deg
  f =   200 Hz : |Z| =   5.27 ohm, phase =  -14.2 deg
  f =   500 Hz : |Z| =   6.11 ohm, phase =   34.8 deg
  f =  1000 Hz : |Z| =  10.13 ohm, phase =   60.4 deg
methode r0 : Zmax/Re = 20.20, f1 = 27.3 Hz, f2 = 55.6 Hz, sqrt(f1 f2) = 39.0 Hz
  Qms(r0) = fs*sqrt(r0)/(f2-f1) = 6.23 (theorie 6.15, ecart +1.16 %)
  Qes(r0) = Qms/(r0-1) = 0.324 (theorie 0.321)
  memes lectures avec Le = 0 : Qms(r0) = 6.1546 (theorie 6.1546) -> l'ecart venait bien de Le
```

Les identités du § 01.4 sont retrouvées à mieux que 1,2 %. Le dernier contrôle est un test de réfutation : en refaisant les mêmes lectures graphiques sur un modèle où $L_e=0$ **exactement**, l'écart de la méthode $r_0$ tombe à zéro à la précision machine. L'écart résiduel vient donc bien de $L_e$ (négligé dans la dérivation de Small), et non d'un artefact de grille — vérifié sur 4 000 puis 400 000 points avec interpolation linéaire.

### <a id="s01-6"></a>01.6 Ce que $Z(f)$ détermine — et ce qu'elle ne détermine pas

C'est le point le plus important de la section pour la phase 2, et un jury de prépa peut le demander directement.

Vue de ses bornes, une caisse close est décrite par **cinq nombres et cinq seulement** : $R_e$, $L_e$, $R_{es}$, $L_{ces}$, $C_{mes}$ — ou, de façon équivalente, $R_e$, $L_e$, $f_c$, $Q_{mc}$, $Q_{ec}$. Or les trois éléments motionnels dépendent de **quatre** paramètres mécaniques :

$$
R_{es}=\frac{(Bl)^2}{R_{ms}},\qquad L_{ces}=(Bl)^2C_{ms},\qquad C_{mes}=\frac{M_{ms}}{(Bl)^2}
$$

Trois équations, quatre inconnues : le système est **sous-déterminé**. La démonstration est constructive — la famille à un paramètre $Bl\to Bl\sqrt{k}$, $M_{ms}\to kM_{ms}$, $C_{ms}\to C_{ms}/k$, $R_{ms}\to kR_{ms}$ laisse $R_{es}$, $L_{ces}$, $C_{mes}$ **exactement** inchangés, donc la même $Z(f)$ à la précision machine :

```
=== Non-identifiabilite de (Bl, Mms, Cms, Rms) a partir de Z(f) seule ===
  k = 0.5 : Bl = 16.97  Mms =  75.0 g  Cms = 0.2200 mm/N  Rms =  3.00
            ->  Res = 96.000  Lces = 63.360 mH  Cmes = 260.4 uF  fs = 39.18  Qms = 6.155  Qes = 0.3206  Vas = 440 L
  k = 1.0 : Bl = 24.00  Mms = 150.0 g  Cms = 0.1100 mm/N  Rms =  6.00
            ->  Res = 96.000  Lces = 63.360 mH  Cmes = 260.4 uF  fs = 39.18  Qms = 6.155  Qes = 0.3206  Vas = 220 L
  k = 2.0 : Bl = 33.94  Mms = 300.0 g  Cms = 0.0550 mm/N  Rms = 12.00
            ->  Res = 96.000  Lces = 63.360 mH  Cmes = 260.4 uF  fs = 39.18  Qms = 6.155  Qes = 0.3206  Vas = 110 L
```

Trois haut-parleurs dont le $V_{as}$ va de 110 L à 440 L donnent la **même courbe d'impédance**. D'où le tableau à afficher avant tout fit :

| Identifiable par $Z(f)$ seule | Non identifiable sans manip supplémentaire |
|---|---|
| $R_e$, $L_e$ | $Bl$, $M_{ms}$, $C_{ms}$, $R_{ms}$ |
| $f_c$ (ou $f_s$), $Q_{mc}$, $Q_{ec}$, donc $Q_{tc}$ et $R_{es}$ | $S_d$, $V_{as}$ |

**Lever la dégénérescence** demande une seconde mesure, et deux voies s'offrent :

1. **Masse ajoutée** : coller une masse connue $\Delta M$ sur la membrane (pâte à modeler + balance de cuisine, coût nul), relever le nouveau $f_s'$ ; alors $M_{ms}=\Delta M/\big((f_s/f_s')^2-1\big)$, d'où $C_{ms}$, puis $Bl$ et $R_{ms}$.
2. **Volume clos connu** : mesurer $f_c$ dans une caisse de volume $V_b$ connu ; le § 01.9 donne $\alpha=(f_c/f_s)^2-1$, donc $V_{as}=\alpha V_b$, donc $C_{ms}$ via $V_{as}=\rho_0c^2S_d^2C_{ms}$ si $S_d$ est mesuré au mètre.

Ce sont exactement les protocoles « added mass » et « sealed box » de REW (§ 01.4). **À planifier dès la phase 1** : sans l'un des deux, la confrontation aux datasheets promise en phase 2 est impossible sur $Bl$, $M_{ms}$ et $V_{as}$ — elle ne portera que sur $f_c$, $Q_{mc}$, $Q_{ec}$.

**Nombre de paramètres libres du fit** — information indispensable pour discuter sur-ajustement et incertitudes : **5 en caisse close**, et **8 en bass-reflex** (les cinq précédents plus les trois éléments de la branche caisse + évent, re-paramétrables en $\alpha$, $f_b$ et une perte). Le § 01.10 montre qu'une seule perte globale suffit en première approche.

### <a id="s01-7"></a>01.7 Allure de $|Z|$ et de la phase

![Module et phase de l'impédance : jeu d'illustration NON MESURÉ du § 01.5, champ libre et caisse close α = 1](../sec01/fig_impedance.png)

Quatre zones se lisent sur la figure, et se retrouveront sur toute mesure :

| Zone | Ce qui domine | $\lvert Z\rvert$ | Phase |
|---|---|---|---|
| $f\ll f_s$ | $L_{ces}$ (ressort) | part de $R_e$ (asymptote basse **atteinte par au-dessus**) et monte vers le pic | positive (inductif) |
| $f=f_s$ | résonance parallèle | **maximum** $R_e+R_{es}$ | **0°** (passage +→−) |
| $f_s<f<f_{min}$ | $C_{mes}$ (masse) | redescend vers $R_e$ | **négative (capacitif)** |
| $f>f_{min}$ | $L_e$ | remonte comme $\omega L_e$ | positive, tend vers +90° |

<!-- Le brouillon écrivait "remonte vers Re par en dessous" : faux, et facilement réfuté par un jury sur la première courbe projetée. La branche motionnelle est un RLC parallèle PASSIF, donc |Z| >= Re partout (§ 01.3). Corrigé et vérifié numériquement ci-dessous. -->

Vérification numérique du sens de l'asymptote, sur 0,1 Hz – 10 kHz :

```
min |Z| sur toute la bande = 5.0002 ohm  (Re = 5.00 ohm)
  f =   0.5 Hz : |Z| =   5.0046 ohm, phase =  +2.33 deg
  f =   1.0 Hz : |Z| =   5.0182 ohm, phase =  +4.66 deg
  f =   5.0 Hz : |Z| =   5.4508 ohm, phase = +22.32 deg
  f =  10.0 Hz : |Z| =   6.7671 ohm, phase = +39.94 deg
  f =  20.0 Hz : |Z| =  12.4689 ohm, phase = +60.22 deg
```

À basse fréquence $\underline{Z}\approx R_e+j\omega(L_e+L_{ces})$ et $\mathrm{Re}(\underline{Z})=R_e+\omega^2L_{ces}^2/R_{es}>R_e$ : le module tend vers $R_e$ **par valeurs supérieures**, et le seul minimum de la courbe est celui situé au-dessus du pic.

Ce **minimum** (5,06 Ω à 264 Hz ici, à peine au-dessus de $R_e$) est le seul endroit où le haut-parleur ressemble à sa valeur nominale ; il correspond approximativement à la résonance série de $L_e$ avec $C_{mes}$ : $f_{min}\approx\dfrac{1}{2\pi\sqrt{L_eC_{mes}}}=255$ Hz pour ce jeu, soit 3,4 % en dessous de la valeur exacte — l'approximation néglige $L_{ces}$ et $R_{es}$.

**L'étiquette « 8 Ω » n'est pas une mesure.** Sur les trois fiches du § 01.13, $R_e/Z_{nom}$ vaut 0,625 / 0,634 / 0,750 : c'est un constat, pas une norme. La norme, elle, existe et dit autre chose — la CEI 60268-5 demande que le **minimum du module** dans la bande nominale ne descende pas sous 80 % de $Z_{nom}$. Or le modèle donne $|Z|_{min}/Z_{nom}=0{,}635$ / 0,638 / 0,758 pour ces trois haut-parleurs : **aucun des trois ne satisfait le critère**. L'écart entre la norme et la pratique du matériel de sono est un argument de plus pour mesurer plutôt que de croire l'étiquette.

Point capital pour le raccord : **entre $f_s$ (ou $f_c$) et $f_{min}$, c'est-à-dire précisément autour de 100 Hz pour un 18″, la charge est capacitive** (phase −48° à 100 Hz en champ libre, −53° en caisse close). Le § 01.8 chiffre ce que cela fait au filtre.

### <a id="s01-8"></a>01.8 « Du simple au sextuple » — et ce que la charge fait vraiment au filtre

Le rapport pic/résistance est fixé par les facteurs de qualité : $|Z|_{max}/R_e=1+Q_{ms}/Q_{es}$. Deux lectures honnêtes de la phrase de la problématique :

1. **Rapportée à l'impédance nominale**, un pic de 40–60 Ω (ordre de grandeur donné par le professeur en mai 2026, non mesuré) fait ×5 à ×7,5 par rapport à 8 Ω : « du simple au sextuple ».
2. **Rapportée aux datasheets** du § 01.13, le modèle donne $|Z|_{max}/R_e$ = 23,2 et 21,6 pour les deux 18″, 19,5 pour le 8″ médium, soit **×20 en champ libre**. Il faut se garder de déduire ce ×20 des fourchettes prises isolément : avec $Q_{ms}\in[6;10]$ et $Q_{es}\in[0{,}3;0{,}5]$, $1+Q_{ms}/Q_{es}$ irait de **13,0 à 34,3** — ce qui rappelle surtout que $Q_{ms}$ et $Q_{es}$ ne sont pas indépendants dans un vrai haut-parleur. Les pertes de caisse (fuites, absorbant) abaissent $Q_{mc}$ et donc le pic réel (§ 01.10). Le « sextuple » est à lire comme une **borne basse plausible**, à remplacer par le rapport mesuré en caisse [[à mesurer]].

**Ce que le filtre voit dans sa propre bande.** Le bloc ci-dessous traite la **caisse close**, qui est désormais le cas de comparaison et non le cas du projet (§ 01.9). Le cas réel — **bass-reflex à deux évents** — est chiffré au § 01.10 et il est **pire** : $\lvert Z\rvert(100\ \text{Hz})=22{,}4$ Ω contre 9,7 Ω ici. Sur le jeu typique mis en caisse close $\alpha=1$ ($f_c=55{,}4$ Hz, donc pic **à l'intérieur** de la bande de raccord) :

```
clos alpha=1 (Vb = Vas = 220 L) : fc = 55.4 Hz
  f =    40 Hz : |Z| =   18.27 ohm, phase =  +64.7 deg, |Z|/8 = 2.28
  f =    60 Hz : |Z| =   58.78 ohm, phase =  -49.9 deg, |Z|/8 = 7.35
  f =    80 Hz : |Z| =   15.38 ohm, phase =  -62.1 deg, |Z|/8 = 1.92
  f =   100 Hz : |Z| =    9.72 ohm, phase =  -53.4 deg, |Z|/8 = 1.22
  f =   150 Hz : |Z| =    6.18 ohm, phase =  -32.2 deg, |Z|/8 = 0.77
  f =   250 Hz : |Z| =    5.07 ohm, phase =   -2.4 deg, |Z|/8 = 0.63
  rapport max/min de |Z| sur 40-250 Hz = 19.9
  phase : de -64.2 deg (a 70.9 Hz) a +65.3 deg (a 43 Hz), excursion 129.5 deg
```

La charge du passe-bas varie donc d'un facteur ~20 en module et de ~130° en phase **à l'intérieur de la bande de raccord**, sans même regarder au-delà.

**Chiffrage de l'effet sur le filtre catalogue E12 (18 mH / 150 µF)** — c'est le calcul qui doit précéder le gel des critères, parce qu'il dit *quelle grandeur est sensible* :

| Grandeur | Charge 8 Ω résistifs | Charge réelle (clos $\alpha=1$) |
|---|---|---|
| $-3$ dB du passe-bas | 99,9 Hz | 104,1 Hz (**+4,2 %**) |
| gain max en bande | 0 dB | **+14,4 dB à 73 Hz** |
| écart de gain sur 40–250 Hz | — | de $-3{,}3$ dB (163 Hz) à $+15{,}4$ dB (73 Hz), **RMS 4,7 dB** |
| écart de phase sur 40–250 Hz | — | de $-59°$ à $+46°$ |

Le message est net et il faut le dire tel quel : **la grandeur sensible n'est pas $f_x$, c'est la forme de la réponse.** Le pic d'impédance se comporte comme une charge presque à vide pour le diviseur, et la partie capacitive de $Z$ s'ajoute à $C_1$ : le $Q$ effectif explose localement. Un critère « précision de $f_x$ » bougerait de 4 % là où le critère « fidélité du raccord » bouge de près de 5 dB RMS.

Ce qui déplace vraiment $f_x$, en revanche, c'est la **résistance série** :

```
=== effet d'une DCR de self (charge 8 ohm resistifs) ===
  (le -3 dB est compte par rapport a la bande passante ATTENUEE : c'est la f_x realisee,
   la perte d'insertion plate etant comptee separement comme pertes)
  DCR = 0.0 ohm : perte d'insertion = +0.00 dB ; -3 dB =  99.9 Hz (+0.0 %) ; pole =  96.9 Hz, Q = 0.730
  DCR = 0.5 ohm : perte d'insertion = -0.53 dB ; -3 dB = 102.8 Hz (+2.8 %) ; pole =  99.8 Hz, Q = 0.728
  DCR = 1.0 ohm : perte d'insertion = -1.02 dB ; -3 dB = 105.4 Hz (+5.5 %) ; pole = 102.7 Hz, Q = 0.726
```

Le mécanisme est analytique et se démontre en trois lignes : avec une DCR $R_d$ en série, la fonction de transfert normalisée à sa valeur continue a pour pôle $\omega_0'=\omega_0\sqrt{(R_d+R)/R}$ — soit $+6{,}1$ % pour $R_d=1$ Ω sur $R=8$ Ω — tandis que $Q$ bouge à peine (0,730 → 0,726). **Attention à la convention** : rapporté au 0 dB absolu, le $-3$ dB semble au contraire *descendre* (à 92,8 Hz), simplement parce que toute la courbe a perdu 1 dB. Le repère utile est celui **normalisé à la bande passante atténuée** ; la perte plate se compte séparément, dans le critère « pertes d'insertion ».

> **À lire avec le § 04.1, qui tranche et qui complète.** Tout ce que déplace ici la DCR, ce sont des **repères** — le pôle et les deux $-3$ dB — et non $f_x$ au sens gelé du TIPE (le **croisement des deux voies**). Le § 04.1 refait le même calcul sur les deux voies simultanément et montre que le croisement, lui, ne bouge que de **0,8 % pour 2 Ω de DCR**, quand les deux repères $-3$ dB bougent de $-18$ % et $+10$ %. Autrement dit : la DCR agit en **perte d'insertion** et en déplacement du pôle, pas en déplacement du raccord. Les chiffres du bloc ci-dessus restent exacts pour ce qu'ils mesurent, à condition de les nommer.

Le critère « précision de $f_x$ » de la feuille de route garde donc tout son sens — **mais comme révélateur de la DCR à travers les repères $-3$ dB, pas comme révélateur de $Z(f)$**. C'est une remarque à remonter en phase 0, avant le gel.

<!-- Le verificateur "terrain" trouvait -2 % de deplacement du -3 dB et une bosse de +9 dB ; je trouve +4 % et +14,4 dB. L'ecart vient de la charge : son jeu placait le pic a 39 Hz (hors bande), le mien recale le place a 55 Hz (dans la bande). La CONCLUSION est la meme et c'est elle qui compte (f_x peu sensible, forme tres sensible) ; la magnitude, elle, depend de la position du pic et sera donc [[à recalculer]] sur le jeu identifie en phase 2. -->

Enfin, les deux **nombres de contrôle** du projet, revérifiés, car la section filtre les réutilisera et ils ne mesurent pas la même chose :

```
fraction de puissance dissipee dans une DCR de 1 ohm en serie sur 8 ohm = 1/9 = 11.1 %
baisse de TENSION aux bornes du HP  = 20 log10(8/9) = -1.02 dB
baisse de PUISSANCE delivree au HP  = 10 log10(8/9) = -0.51 dB
```

Le « −1 dB » du projet est un rapport de **tensions** ; la puissance, elle, ne perd que 0,51 dB. À préciser à chaque emploi.

### <a id="s01-9"></a>01.9 Effet de la caisse close

> **Statut de cette sous-section depuis le 16 septembre 2026 : cas de comparaison, pas cas du
> projet.** Le sub de l'enceinte est **bass-reflex à deux évents** (constat de l'étudiant,
> 16 sept. 2026 — voir § 01.10). La caisse close reste traitée ici parce qu'elle est le cas
> *simple* : un seul pic, cinq paramètres, la formule $f_c=f_s\sqrt{1+\alpha}$ démontrée en
> trois lignes. C'est le repère par rapport auquel on lit le cas réel — et c'est la limite que
> le modèle bass-reflex doit redonner quand l'évent est inerte (contrôle exécuté au § 01.10).
> Rien dans cette sous-section n'est un résultat sur l'enceinte de Thomas.

Une caisse close de volume $V_b$ ajoute un ressort d'air en série avec la suspension. En notant $\alpha=V_{as}/V_b$ (Small 1972, « Closed-Box Loudspeaker Systems »), la compliance totale devient $C_{ms}/(1+\alpha)$ et, en négligeant les pertes de la caisse :

$$
f_c=f_s\sqrt{1+\alpha},\qquad Q_{tc}=Q_{ts}\sqrt{1+\alpha},\qquad Q_{mc}=Q_{ms}\sqrt{1+\alpha},\qquad Q_{ec}=Q_{es}\sqrt{1+\alpha}
$$

Sur le modèle électrique, cela revient à diviser $L_{ces}$ par $(1+\alpha)$ : le pic **monte en fréquence** mais **garde sa hauteur** $R_e+R_{es}$ (les deux $Q$ sont multipliés par le même facteur, leur rapport est inchangé — et $R_{es}=(Bl)^2/R_{ms}$ ne dépend pas de $C_{ms}$). En pratique l'absorbant et les fuites ajoutent des pertes mécaniques : $Q_{mc}$ réel est plus bas que la formule, et le pic mesuré est plus bas et plus large.

```
Sd = 1190 cm2 -> Vas = 220 L (avec Cms = 0.110 mm/N)
  Vb =  100 L : alpha = 2.20 ; fc = 70.1 Hz ; Qtc = 0.545 ; Qmc = 11.01 ; Qec = 0.573
  Vb =  150 L : alpha = 1.47 ; fc = 61.5 Hz ; Qtc = 0.478 ; Qmc =  9.67 ; Qec = 0.503
  Vb =  220 L : alpha = 1.00 ; fc = 55.4 Hz ; Qtc = 0.431 ; Qmc =  8.70 ; Qec = 0.453
  Vb =  400 L : alpha = 0.55 ; fc = 48.8 Hz ; Qtc = 0.379 ; Qmc =  7.66 ; Qec = 0.399
Vb = Vas (220 L, alpha = 1) : |Z| max = 101.0 ohm a 55.4 Hz (hauteur inchangee = Re+Res)
  largeur a mi-hauteur du pic en caisse ~ fc/Qmc = 6.4 Hz
```

Conséquences pour le projet :

- **$f_s$ datasheet (champ libre) $\neq$ $f_c$ en caisse** : mesurer un pic plus haut que la datasheet n'est pas une erreur, c'est $\sqrt{1+\alpha}$. Le rapport $(f_c/f_s)^2-1$ donne même une estimation de $\alpha$, donc de $V_{as}$ si $V_b$ est connu — c'est l'une des deux voies pour lever la dégénérescence du § 01.6.
- Le fit de la phase 2 se fait **sur le haut-parleur en caisse** : les paramètres identifiés sont $f_c$, $Q_{mc}$, $Q_{ec}$ (ceux qui chargent réellement le filtre), et non les paramètres champ libre. La confrontation à la datasheet passe par les formules ci-dessus.
- **La largeur à mi-hauteur du pic vaut $f_c/Q_{mc}\approx6{,}4$ Hz.** Pour que $Q_{mc}$ soit mesurable à mieux que 10 %, il faut au moins une dizaine de points dans cet intervalle, soit un **pas ≤ 0,6 Hz autour du pic** — pas un balayage au 1/12 d'octave, qui donnerait 3,3 Hz par pas à 55 Hz. C'est une contrainte de protocole, à écrire dans la phase 1.

### <a id="s01-10"></a>01.10 Effet du bass-reflex — le cas réel du projet

> **Fait établi le 16 septembre 2026 (constat de l'étudiant, il fait foi).** Le sub 18″ est
> monté en **bass-reflex, avec DEUX évents**. Ce n'était pas su à la rédaction initiale : tous
> les documents portaient « type de caisse (clos / bass-reflex) à documenter », et le modèle à
> 7-8 paramètres avait été écrit et testé **précisément parce que** la question n'était pas
> tranchée. Elle l'est maintenant : ce n'est pas une reprise, c'est une hypothèse qui se lève,
> et le code n'a pas une ligne à changer (`modele_hp.Z_bassreflex`, `Z_bassreflex8`,
> `Z_bassreflex_semi` existent et sont testés). Ce qui change, c'est le **statut** des deux
> sous-sections : le § 01.9 devient le cas de comparaison, celui-ci devient le cas du projet.
> Restent à relever : **dimensions des deux évents et volume de la caisse** [[à mesurer]], et
> donc $f_b$ [[à mesurer]] — ce sont les entrées de la prédiction du § 01.10 bis.

Un évent ajoute un second degré de liberté : la masse d'air de l'évent $M_{ap}$ résonne avec la compliance de la caisse $C_{ab}=V_b/(\rho_0c^2)$ à la fréquence d'accord $f_b=\dfrac{1}{2\pi\sqrt{M_{ap}C_{ab}}}$. Côté mécanique, la charge vue par la membrane devient $S_d^2\,\underline{Z}_{ac}$ avec $\underline{Z}_{ac}=\left(j\omega C_{ab}\right)^{-1}\,\|\,\left(j\omega M_{ap}+R_{ap}\right)$ ; on remplace donc dans $\underline{Z}_m$ le seul terme $1/(j\omega C_{ms})$ par $1/(j\omega C_{ms})+S_d^2\underline{Z}_{ac}$ (contrôle dimensionnel : $\mathrm{m^4\cdot Pa\,s/m^3=N\,s/m}$, bien une impédance mécanique). L'impédance électrique montre alors **deux pics** $f_L<f_b<f_H$ et un **creux à $f\approx f_b$** : à l'accord, la membrane bouge peu (c'est l'évent qui rayonne), la f.é.m. induite s'effondre et $|Z|$ retombe près de $R_e$.

Relations sans pertes (Thiele 1961, Small 1973), **redémontrées** : en posant $x=\omega^2/\omega_s^2$ et $\beta=(f_b/f_s)^2$, l'annulation de $\underline{Z}_m$ donne $x^2-(1+\alpha+\beta)x+\beta=0$, d'où par les relations racines–coefficients

$$
f_L\,f_H=f_s\,f_b,\qquad f_L^2+f_H^2=f_s^2(1+\alpha)+f_b^2
$$

et, en évaluant le polynôme en $x=\beta$, $p(\beta)=-\alpha\beta<0$ : $\beta$ est **toujours** entre les deux racines, donc $f_L<f_b<f_H$ est un résultat démontré, pas une constatation.

```
REGENERE le 2026-09-16 par modele_hp.Z_bassreflex8 sur SUB_TYP_BR -- MODELE, pas une mesure.
Vas = 207 L, Vb = 230 L (alpha = 0.9), fs = 39 Hz, fb = 35.0 Hz, Ql = 7 :
  pics a  22.6 Hz (55.5 ohm), 60.2 Hz (67.8 ohm)
  creux a 35.0 Hz (7.41 ohm)
  fL*fH = 1362  vs  fs*fb = 1365   (ecart -0.23 %)
  fL^2+fH^2 = 4131  vs  fs^2(1+alpha)+fb^2 = 4115   (ecart +0.39 %)
  controle fL < fb < fH : 22.6 < 35.0 < 60.2
  controle event inerte : ecart max |Zbr - Zclos| = 2.2e-13 ohm
```

Les deux identités ne sont **exactes que sur les racines sans pertes** : les maxima de $|Z|$
d'une caisse à $Q_l$ fini sont légèrement déplacés, d'où les écarts de 0,2 à 0,4 % ci-dessus.
Un bloc qui afficherait « exacts » sur des pics numériques se réfuterait lui-même.

Le contrôle « évent inerte » consiste à faire tendre l'impédance de la branche d'évent vers l'infini (masse ou pertes infinies, c'est équivalent ici) : le modèle redonne **exactement** la caisse close de même volume, ce qui est la bonne façon de coder le fit (un seul modèle, des paramètres en plus). Nuance à ne pas se faire prendre : un évent *physiquement* bouché ajoute en outre son propre volume à $V_b$.

**Les pertes de caisse — et pourquoi le pic mesuré est toujours plus bas.** Small distingue trois pertes : fuites $Q_l$, absorption $Q_a$, évent $Q_p$. Le brouillon n'en modélisait qu'une. Leur effet est massif :

```
REGENERE le 2026-09-16 -- meme jeu SUB_TYP_BR, seule Ql change.
Re + Res = 110.2 ohm  (hauteur des DEUX pics a Ql infini : c'est un resultat EXACT,
                       la partie reactive de l'admittance s'annule en fL comme en fH)
effet d'une fuite de caisse (Ql fini) sur la hauteur des pics :
    Ql = infini : 22.8 Hz (110.2 ohm), 60.0 Hz (110.2 ohm)
    Ql =     15 : 22.7 Hz ( 74.5 ohm), 60.1 Hz ( 84.8 ohm)
    Ql =      7 : 22.6 Hz ( 55.5 ohm), 60.2 Hz ( 67.8 ohm)
```

**Une seule perte est implémentée**, et c'est $Q_l$ — les **fuites** de caisse, qui tombent en
résistance **série** dans la branche d'évent ($R_p=\omega_b L_{ceb}/Q_l$ dans le dual
électrique). Une perte d'**évent** $R_{ap}$, elle, tomberait *en parallèle* de $C_{peb}$ : elle
est **absente du modèle**, et c'est assumé. Ne pas écrire « $Q_p$ » là où le code calcule $Q_l$.

Peut-on les séparer sur $Z(f)$ ? Test : une courbe engendrée avec ($Q_p=20$, $Q_l=7$) est ajustée au mieux par une **perte d'évent seule** $Q_p=7{,}1$, avec un résidu de **0,62 dB RMS (2,9 dB au pire)**. Ce n'est donc ni indiscernable ni facile : commencer le fit avec **une seule perte globale** est raisonnable, et n'en ajouter une seconde que si le résidu structuré dépasse ce seuil. Cela porte le compte de la phase 2 à 8 paramètres en bass-reflex (§ 01.6), 9 si l'on sépare les pertes.

**Ce que le bass-reflex fait à la charge du raccord — chiffré sur un jeu plausible.** Le jeu ci-dessus (grosse caisse : $V_{as}=207$ L, $V_b=230$ L, soit $\alpha=0{,}9$ ; accord $f_b=35$ Hz) laissait le second pic à 60 Hz. Avec un jeu plus représentatif d'un 18″ de sonorisation en caisse **petite devant $V_{as}$** ($\alpha=3$, ce qui est le cas courant en sono), le second pic remonte en plein dans la zone de raccord. Calcul exécuté le 16 sept. 2026 avec `modele_hp.Z_bassreflex` — **c'est un MODÈLE, pas une mesure** : $R_e=5{,}4$ Ω, $L_e=1{,}9$ mH, $R_{es}=100$ Ω, $f_s=40$ Hz, $Q_{ms}=6{,}1$, $f_b=35$ Hz, $Q_l=7$, et $\alpha=3$ **écrit comme un couple de volumes** — $V_{as}=330$ L (haut de la fourchette 207–331 L du § 01.13) et $V_b=110$ L — pour qu'aucune incohérence ne puisse se reformer entre ce jeu et la géométrie d'évents du § 01.10 bis. C'est le jeu `io_mesures.SUB_TYPIQUE_BR`, celui qui engendre le fichier d'exemple.

```
MODELE (aucune mesure) -- REGENERE le 2026-09-16 par modele_hp.Z_bassreflex8.
sub 18" bass-reflex : Vas = 330 L, Vb = 110 L (alpha = 3), fs = 40 Hz, fb = 35 Hz, Ql = 7
  pic bas   f_L =  16.3 Hz   |Z| = 54 ohm
  creux            34.2 Hz   |Z| =  6.1 ohm     (~ Re : la membrane est quasi immobile)
  pic haut  f_H =  85.9 Hz   |Z| = 64 ohm       <-- EN PLEIN DANS LA ZONE DE RACCORD
  |Z|(100 Hz) = 22.4 ohm, phase -57.6 deg       (soit 2.8 fois les "8 ohms" supposes)
  rapport max/min de |Z| sur 40-250 Hz = 11.6 ; excursion de phase 113 deg
  racines SANS PERTES (exactes)   : f_L = 16.32 Hz, f_H = 85.78 Hz
  controles sur les pics NUMERIQUES (deplaces par Ql = 7, donc approches) :
      fL.fH = 1398 vs fs.fb = 1400 (-0.13 %)
      fL^2+fH^2 = 7638 vs fs^2(1+alpha)+fb^2 = 7625 (+0.17 %)
```

**Trois conséquences, dans l'ordre d'importance.**

1. **Le second pic tombe près de 100 Hz, et c'est le VOLUME de caisse qui l'y met.** C'est le point capital de tout ce qui a été appris le 16 septembre — et il faut l'énoncer juste, parce que le jury tirera ce fil en premier. Les deux identités sont $f_Lf_H=f_sf_b$ et $f_L^2+f_H^2=f_s^2(1+\alpha)+f_b^2$. Le produit **n'est fixé que si $f_b$ l'est** : il ne dit donc rien de ce que fait un changement d'accord. Les deux paramètres agissent de façon opposée, et c'est vérifié numériquement (`modele_hp.Z_bassreflex8`, $f_s=40$ Hz, $Q_l=7$) :

   - **L'accord $f_b$ déplace les deux pics dans le MÊME sens.** À $\alpha=3$ fixé, descendre $f_b$ de 50 à 25 Hz fait passer $f_L$ de 21,7 à 12,0 Hz **et** $f_H$ de 91,9 à 83,0 Hz. Descendre l'accord **abaisse** le pic haut, elle ne le remonte pas. (C'est cohérent avec les identités : à $\alpha$ fixé, la somme des carrés diminue avec $f_b$ en même temps que le produit.)
   - **Ce qui écarte les deux pics, c'est $\alpha=V_{as}/V_b$**, par $f_L^2+f_H^2=f_s^2(1+\alpha)+f_b^2$ à produit constant. À $f_b=35$ Hz fixé : $\alpha=0{,}5\Rightarrow f_H=54{,}6$ Hz ; $\alpha=0{,}9\Rightarrow61{,}3$ ; $\alpha=2\Rightarrow75{,}5$ ; $\alpha=3\Rightarrow85{,}9$ ; $\alpha=6\Rightarrow110{,}8$ Hz. **Une caisse petite devant $V_{as}$ remonte $f_H$ vers le raccord** — et une caisse petite devant $V_{as}$ est précisément ce que la sono fait, pour des raisons d'encombrement et de transport.

   Le pic haut ne peut donc pas être éloigné du raccord en jouant sur l'accord : il faudrait **grossir la caisse**, ce qui n'est pas une variable de ce TIPE (l'enceinte est faite). À 100 Hz le modèle donne $\lvert Z\rvert=22{,}4$ Ω à $-57{,}6°$ : **l'hypothèse « 8 Ω résistifs » y est encore plus fausse qu'en caisse close** ($9{,}7$ Ω à $-53°$ au § 01.8). L'argument central du TIPE en sort **renforcé**, pas affaibli — et c'est ainsi qu'il faut le présenter au jury. Réserve d'honnêteté à porter avec le chiffre : $\alpha$ est [[à mesurer]] ; c'est lui, et non $f_b$, qui décide si $f_H$ tombe à 60 Hz ou à 86 Hz.
2. **Le creux à $f_b$ est un second point bas.** À l'accord la membrane est quasi immobile — c'est l'évent qui rayonne, la vitesse $v$ s'effondre, donc la f.é.m. $Bl\,v$ et l'impédance motionnelle avec elle — et $\lvert Z\rvert$ retombe à 6,1 Ω, c'est-à-dire **sous l'impédance nominale**. Le filtre y ajoute son propre point bas (§ 04.2) : la charge vue par l'ampli a donc **deux** minima au lieu d'un.
3. **Le compte de paramètres est fixé** : 8 (`Z_bassreflex8`), 9 si l'on sépare les pertes. Le § 03 en fait le modèle **par défaut**, et non un repli.

**Ce qui ne change pas.** La problématique, le récit en 4 actes, les critères, la chaîne de mesure, l'optimisation E12, les portes de validation : rien de tout cela n'est touché. Le bass-reflex change la *charge*, pas la *méthode*. Le seul document de travail qui change de forme est le protocole de mesure (grille et sécurité, § 02.6) et le protocole acoustique (deux évents à sommer, § 07.3).

### <a id="s01-10bis"></a>01.10 bis Prédire $f_b$ au pied à coulisse : résonateur de Helmholtz à $N$ évents

Tout ce qui précède **lit** $f_b$ sur une courbe. On peut aussi le **prédire** à partir de la seule géométrie de la caisse, sans brancher quoi que ce soit — et c'est une occasion rare, dans ce projet, de fermer une boucle théorie/expérience qui ne doit rien à l'ajustement de l'acte 2.

**Mise en équation.** L'air de la caisse est un ressort, l'air des évents une masse. Côté acoustique (variables : pression $p$ en Pa, débit volumique $q$ en m³/s) :

$$C_{ab}=\frac{V_b}{\rho_0c^2}\quad[\mathrm{m^5/N}],\qquad M_{ap}=\frac{\rho_0\,\ell_{\text{eff}}}{S_p}\quad[\mathrm{kg/m^4}]$$

pour **un** évent de section $S_p$ et de longueur acoustique $\ell_{\text{eff}}$. $N$ évents identiques sont $N$ masses **en parallèle** (elles voient la même pression de caisse et leurs débits s'ajoutent), donc $M_{ap,tot}=M_{ap}/N$. D'où

$$\boxed{\;f_b=\frac{1}{2\pi\sqrt{M_{ap,tot}\,C_{ab}}}=\frac{c}{2\pi}\sqrt{\frac{N\,S_p}{V_b\,\ell_{\text{eff}}}}\;}\qquad S_p=\frac{\pi d^2}{4},\quad \ell_{\text{eff}}=\ell+\delta_{\text{int}}+\delta_{\text{ext}}$$

Deux remarques que le jury peut demander et qui se lisent sur la formule : **$\rho_0$ disparaît** (la masse et le ressort sont tous deux proportionnels à la densité de l'air) — $f_b$ ne dépend donc pas de la pression atmosphérique, seulement de $c$, donc de la température ($c=331{,}3\sqrt{1+\theta/273{,}15}$, soit $+0{,}17$ %/K, +1,7 % pour 10 K) ; et **$f_b\propto\sqrt{N}$ à géométrie d'évent fixée**, ce qui rend le comptage des évents dimensionnant, pas décoratif.

**La correction de bout, et la convention retenue.** $\ell$ est la longueur du tube au pied à coulisse ; $\ell_{\text{eff}}$ est plus grande, parce que l'air rayonne de part et d'autre et entraîne un peu d'air au-delà des ouvertures. La correction par extrémité s'écrit $\delta=k_a\,a$ avec $a=d/2$, et **les sources ne donnent pas le même $k_a$ parce qu'elles ne décrivent pas la même extrémité** :

| Extrémité | $k_a$ | Source |
|---|---|---|
| ouverte **libre** (tube débouchant dans le vide) | **0,6133** | Levine & Schwinger (1948), limite basse fréquence exacte |
| ouverte **bridée** (affleurant un grand plan) | **0,8216** | Rayleigh, valeur variationnelle |
| idem, approximation courante | **0,8488** $=8/(3\pi)$ | réactance de rayonnement du piston bafflé |

Un évent de caisse est **bridé à l'extérieur** (il affleure le baffle) et **libre à l'intérieur** (il débouche dans le volume) : $k_a=0{,}61+0{,}82$ à $0{,}61+0{,}85$, soit $k_a\in[1{,}435\,;1{,}462]$, c'est-à-dire $\ell_{\text{eff}}=\ell+(0{,}72\ \text{à}\ 0{,}73)\,d$. **Convention retenue : $k_a=1{,}463$** — c'est la **borne haute** de cet intervalle (son centre vaut 1,4485), et on la retient non pour sa position mais parce que c'est exactement le coefficient de la formule de longueur d'évent utilisée dans toute la littérature haut-parleur (Small 1973 ; Dickason, *Loudspeaker Design Cookbook*), ce qui rend nos chiffres comparables aux leurs. C'est aussi, **depuis le 16 sept. 2026, le défaut du code** (`modele_hp.K_BOUT_DEFAUT`) : un seul $k_a$ dans tout le projet, document et code compris — l'ancien défaut 1,7 du code contredisait cette page. On **transporte néanmoins l'encadrement complet** $k_a\in[1{,}227\,;1{,}698]$ (deux bouts libres → deux bouts bridés) comme incertitude de modèle, parce que l'extrémité intérieure d'un tube peut être proche d'une paroi ou de l'autre évent, ce qui la bride en pratique.

**Vérification numérique** (script `helmholtz.py`, exécuté). En inversant la formule on retrouve la « formule de longueur d'évent » classique :

```
CELERITE RETENUE : c = 343 m/s (20 degres C). C'est la SEULE valeur du projet,
celle de modele_hp.C_SON ; les blocs ci-dessous sont recalcules avec elle.

Leff[cm] = 93622 * N * R[cm]^2 / (fb[Hz]^2 * Vb[L])     avec c = 343 m/s
  (c = 340 -> 91992 ; c = 344 -> 94169 ; c = 345 -> 94717 -- pour lire la litterature)
donc  Lv = 93622 N R^2/(fb^2 Vb) - 1.463 R     (R rayon en cm, Vb en litres, Lv en cm)

Controle : N=1, d=10 cm, Vb=250 L, Leff=7.73 cm -> fb = 34.80 Hz  (coherent)

Cas d'ecole : DEUX events d=10 cm, l=15 cm, Vb=250 L
  sans aucune correction de bout .......... fb = 35.33 Hz
  2 bouts libres      (ka = 1.227) ........ fb = 29.76 Hz
  1 bride + 1 libre   (ka = 1.435-1.463) .. fb = 28.97 a 29.06 Hz   <-- convention retenue
  2 bouts brides      (ka = 1.643-1.698) .. fb = 28.23 a 28.40 Hz
  -> encadrement toutes conventions : 28.2 a 29.8 Hz

Meme aire totale, meme longueur, mais UN SEUL event (d = 14.14 cm) : fb = 27.18 Hz
  -> N petits events accordent 6.6 % PLUS HAUT qu'un gros de meme aire
     (chaque event porte sa propre correction de bout, proportionnelle a son rayon)
```

**Attention aux constantes trouvées en ligne** : elles diffèrent d'un facteur 100 ou 1000 selon les unités (cm/litres, pouces/pieds cubes) et selon $c$. Ne jamais reprendre une constante sans redémontrer ses unités — celle ci-dessus l'est.

**Budget d'incertitude de la prédiction.** $f_b\propto d\,(\ell+k_ad/2)^{-1/2}V_b^{-1/2}$, d'où par dérivation logarithmique et sommation quadratique (GUM, lois rectangulaires) :

```
meme cas d'ecole, c = 343 m/s, k = 1.463 -> fb = 28.97 Hz
d a +- 1 mm, l a +- 2 mm, Vb a +- 5 % :
  u(fb)/fb = 1.55 %  (contributions : Vb 1.45 %, d 0.48 %, l 0.26 %)
  -> fb = 29.0 Hz +- 0.45 Hz (k=1), soit +- 0.90 Hz elargi (k=2)
Sensibilites unitaires : d +1 mm -> +0.83 % ; l +1 cm -> -2.17 % ; Vb +10 L -> -1.94 %
```

Deux enseignements. (i) **C'est $V_b$ qui domine**, et $V_b$ est le *volume net* : volume intérieur brut moins le volume occupé par les saladiers, les renforts et **les tubes d'évent eux-mêmes**. Sur une caisse DIY, c'est la grandeur la plus facile à surestimer. (ii) **L'incertitude de convention (1,53 Hz d'amplitude : 28,23 à 29,76 Hz) dépasse l'incertitude de mesure (0,90 Hz élargie)** : la prédiction doit donc être annoncée comme un **intervalle**, jamais comme un nombre unique. C'est un point d'honnêteté, et c'est aussi exactement le genre de remarque que le jury attend d'un candidat qui a compris ce qu'il calcule.

**Trois voies indépendantes vers $f_b$, et c'est là tout l'intérêt.**

| Voie | Instrument | Statut | Biais connu |
|---|---|---|---|
| **géométrie** (cette sous-section) | pied à coulisse, mètre, volume net | **prédiction**, formulée *avant* la mesure | convention de correction de bout (± 3 %) |
| **creux d'impédance** | banc du § 02 | lecture directe, sans modèle | le creux n'est pas *exactement* à $f_b$ quand il y a des pertes : sur le modèle du § 01.10 le minimum tombe à **34,2 Hz pour $f_b=35$ Hz** ($-2{,}3$ %), et le passage par zéro de la phase à 33,5 Hz ($-4{,}3$ %) |
| **ajustement** (§ 03) | `Z_bassreflex8` | estimateur non biaisé, avec sa covariance | dépend du modèle et de la bande d'ajustement |

Les faire concorder, c'est **fermer une boucle théorie/expérience qui ne passe pas par l'ajustement** : si les trois s'accordent à quelques pour-cent, le modèle de caisse est validé indépendamment ; si la géométrie et le creux s'accordent mais pas l'ajustement, c'est l'ajustement qui est en cause. Le contrôle est formalisé comme critère de validation au § 03.7. **Coût : dix minutes de pied à coulisse et un relevé de cotes intérieures.** À faire *avant* la première mesure d'impédance, et à consigner daté, sinon la prédiction n'en est plus une.

**Limites à énoncer.** (i) Le modèle de Helmholtz suppose $\ell_{\text{eff}}\ll\lambda$ (largement vrai : 22 cm contre 10 m à 35 Hz) et une section constante ; un évent évasé (*flare*) n'a pas de $\ell_{\text{eff}}$ simple. (ii) Deux évents **proches l'un de l'autre** interagissent : leurs corrections de bout se recouvrent, la masse effective augmente et $f_b$ descend — effet non chiffré ici, borné par la ligne « 2 bouts bridés » du tableau. (iii) La formule ignore les pertes ($Q_l$), qui ne déplacent pas $f_b$ mais déplacent le **creux mesuré**, d'où la colonne « biais connu ». (iv) Elle suppose les deux évents **identiques** : s'ils ne le sont pas, $N\,S_p/\ell_{\text{eff}}$ se remplace par $\sum_i S_{p,i}/\ell_{\text{eff},i}$ [[à vérifier : les deux évents de l'enceinte ont-ils les mêmes cotes ?]].

### <a id="s01-11"></a>01.11 Du modèle électrique à la réponse acoustique

Le § 01.1 dit que « tout le sujet tient » dans une fonction de transfert **électrique**. Or le critère gelé de la feuille de route (« écart RMS de la somme des deux voies à la cible plate, 40–250 Hz ») est **acoustique**. Le pont entre les deux doit être posé ici, sinon la phase 3 optimisera la mauvaise grandeur.

La pression rayonnée par une voie s'écrit, en champ proche et à un facteur près,

$$
\underline{p}(j\omega)\;\propto\;\underline{H}_{\text{filtre}}(j\omega)\times\underline{H}_{\text{HP}}(j\omega)
$$

où $\underline{H}_{\text{HP}}$ est la réponse propre du haut-parleur **en tension**, elle-même un **passe-haut du 2ᵉ ordre** de fréquence $f_c$ et de facteur $Q_{tc}$. Trois conséquences, à écrire noir sur blanc :

1. **Un filtre électrique parfaitement Butterworth ne donne pas un raccord acoustique Butterworth.** Le sub apporte déjà $f_c\approx48$–70 Hz avec $Q_{tc}\approx0{,}38$–0,55 (§ 01.9) : la voie grave est un passe-bande, pas un passe-bas.
2. **Les médiums apportent eux aussi une pente acoustique du 2ᵉ ordre au voisinage de 100 Hz** (§ 01.13) : le passe-haut électrique peut donc être **moins raide** que le catalogue ne le suggère. C'est une piste d'économie de composants, donc directement dans le thème « sobriété ».
3. **Une partie de la bosse de +14 dB du § 01.8 tombe là où le sub roule déjà** : les deux défauts se compensent partiellement, et l'écart acoustique sera plus faible que l'écart électrique. Le chiffrer sans le mesurer serait inventer — c'est précisément l'objet des phases 1 et 4.

Autrement dit : l'optimisation de la phase 3 doit porter sur le **produit** filtre × haut-parleur, pas sur le filtre seul. Le sanity check « charge 8 Ω résistive → retour au Butterworth catalogue » de la feuille de route reste valide, mais il teste l'optimiseur, pas la cible.

### <a id="s01-12"></a>01.12 Limites du modèle

1. **Inductance non idéale (courants de Foucault).** La bobine est bobinée sur un noyau ferromagnétique conducteur ; les courants de Foucault induits dans le pôle rendent l'inductance apparente décroissante avec la fréquence et ajoutent des pertes. **Vanderkooy (1989)** dérive *physiquement* un terme en $\sqrt{j\omega}$ — c'est-à-dire $n=1/2$ exactement, d'où le nom de « semi-inductance ». **Leach (2002)** généralise en $K(j\omega)^n$ avec $n$ **identifié par régression**, typiquement 0,6–0,7 sur des moteurs réels : module en $\omega^n$ et phase constante $n\cdot90°$. Comparaison à $L_e$ constant, avec $K$ **calibré sur le même haut-parleur** ($K=\omega_{ref}L_e/\omega_{ref}^{\,n}$ à $\omega_{ref}=2\pi\cdot1000$ rad/s, fréquence à laquelle les datasheets donnent $L_e$) :

```
  Le = 1.5 mH  ->  K = wref*Le/wref^n = 0.0320 ohm.s^0.65
  f =   100 Hz : jwLe =  0.94 ohm (90 deg) ; K(jw)^n =  2.11 ohm (58 deg) ; Re(K(jw)^n) =  1.10 ohm ; rapport = 2.24
  f =  1000 Hz : jwLe =  9.42 ohm (90 deg) ; K(jw)^n =  9.42 ohm (58 deg) ; Re(K(jw)^n) =  4.92 ohm ; rapport = 1.00
  f = 10000 Hz : jwLe = 94.25 ohm (90 deg) ; K(jw)^n = 42.10 ohm (58 deg) ; Re(K(jw)^n) = 22.00 ohm ; rapport = 0.45
  a 100 Hz : part de jwLe dans |Z| = 11 % ; part de K(jw)^n = 25 %
```

   <!-- Le brouillon comparait Le = 1,5 mH a K = 0,05 declare "valeur d'illustration" : les deux colonnes ne decrivaient pas le meme haut-parleur, la comparaison n'avait pas de sens quantitatif. Recalibre a 1 kHz. -->

   La conclusion honnête n'est **pas** « le modèle à $L_e$ constant suffit » — les deux modèles diffèrent encore d'un facteur 2,24 à 100 Hz. Elle est : dans la bande 20–300 Hz, un $L_e$ **constant mais ajusté sur cette bande** suffit ; le $L_e$ identifié est alors une **valeur effective de raccord**, pas le « $L_e$ à 1 kHz » de la datasheet, et les deux ne doivent pas être confondus dans la confrontation de la phase 2. Le prix à payer est un **résidu structuré en haut de bande**, parce que la semi-inductance apporte une **partie réelle** (1,10 Ω à 100 Hz) qu'un $j\omega L_e$ pur ne sait pas rendre : un fit à $L_e$ constant reportera ce surplus sur $R_e$. Si le résidu dépasse quelques pour cent, on passe à $K(j\omega)^n$ — deux paramètres au lieu d'un. **Ce n'est pas un bug, c'est le modèle** : à ne pas chercher pendant une soirée de phase 2.

2. **Petit signal — et « trop petit signal ».** $Bl(x)$, $C_{ms}(x)$ et $L_e(x)$ varient avec l'excursion ; à fort niveau, $Z(f)$ mesurée à faible amplitude ne décrit plus exactement la charge. Le modèle ne prédit ni la distorsion ni la compression : c'est la raison du critère « robustesse » mesuré aux deux niveaux d'écoute gelés. Mais le piège de la phase 1 est **l'autre sens**. Avec un GBF à 10 V crête-à-crête :

```
  Rref = 100 ohm, |Z| =   5 ohm (au minimum) : V_HP =  476 mVcc, I = 95.2 mAcc, P =   5.7 mW
  Rref = 100 ohm, |Z| = 100 ohm (au pic)     : V_HP = 5000 mVcc, I = 50.0 mAcc, P =  31.3 mW
  Rref =  10 ohm, |Z| =   5 ohm (au minimum) : V_HP = 3333 mVcc, I =  667 mAcc, P = 277.8 mW
  Rref =  10 ohm, |Z| = 100 ohm (au pic)     : V_HP = 9091 mVcc, I = 90.9 mAcc, P = 103.3 mW
```

   Trois recommandations directement actionnables : (a) la méthode à deux voltmètres **n'exige pas** le courant constant, donc utiliser plutôt la **$R_{ref}$ de 10 Ω** déjà prévue à l'achat — on gagne un facteur 7 en tension sur le haut-parleur au point le plus défavorable, donc en rapport signal/bruit, tout en restant à moins de 0,3 W ; (b) **noter et geler** le niveau d'excitation, et vérifier l'absence de ronflement 50 Hz capté par une bobine de 18 pouces (moyennage, ou points de mesure décalés hors de 50 et 100 Hz) ; (c) mesurer $f_s$ **deux fois à quelques minutes d'intervalle** — une dérive de quelques pour cent est un effet de rodage et de niveau sur la compliance, pas une erreur de manip.

3. **Dérive thermique de $R_e$.** Le cuivre a un coefficient de température d'environ $+0{,}39\ \%/\mathrm{K}$ (constante physique) : une bobine qui chauffe de 50 K voit $R_e$ augmenter d'environ 20 %, ce qui décale $Q_{es}$ (proportionnel à $R_e$), la sensibilité et le $Q$ du filtre passif. La référence active, qui ne voit pas $Z(f)$, y est insensible par construction.

4. **Modes de membrane (*break-up*).** Le modèle n'a qu'**un** degré de liberté mécanique : il suppose la membrane rigide. Un 18″ cesse d'être un piston bien avant 1 kHz, et ces modes se voient sur $Z(f)$ sous forme d'accidents locaux que le modèle ne peut pas reproduire. C'est une limite **mécanique**, indépendante des courants de Foucault du point 1, et c'est la seconde raison de borner le fit à la bande utile : **20–300 Hz** (feuille de route, phase 2).

5. **Bloc médiums = deux dipôles en série.** Si les deux 4 Ω sont identiques, $Z$ double sans changer de forme ; s'ils ne sont pas appariés, la somme montre deux pics distincts.

```
--- Bloc 2 x 8FE200-4 en serie (identiques, champ libre) ---
  Re serie = 6 ohm ; |Z|max = 117 ohm a 80 Hz ; |Z|(100 Hz) = 29.2 ohm
  largeur a mi-hauteur du pic ~ fs/Qms = 9.2 Hz
  si fs different de +-10 % : pics a 72 Hz (67 ohm), 89 Hz (69 ohm) -> ecart 17 Hz
  si fs different de +-5 %  : pics a 76 Hz (78 ohm), 84 Hz (81 ohm) -> ecart  8 Hz
  pas de mesure autour de 80 Hz : 1/12 oct = 4.8 Hz ; 1/24 oct = 2.3 Hz
```

   Le modèle du bloc doit donc prévoir **deux branches motionnelles** en série. Sur la résolution : au 1/12 d'octave, deux pics distants de 17 Hz ne sont couverts que par ~3,5 pas, et une dispersion de ±5 % (8 Hz) ne serait **plus résolue du tout**. Il faut resserrer à **1/24 d'octave, ou mieux un balayage linéaire au pas de 1 Hz sur 60–110 Hz**.

6. **Charge de rayonnement et environnement.** La masse d'air rayonnée fait partie de $M_{ms}$ et dépend du baffle ; une mesure en caisse, dans la pièce, est la bonne (c'est la charge que verra le filtre), mais elle n'est pas transposable à un autre montage.

### <a id="s01-13"></a>01.13 Ordres de grandeur typiques (datasheets publiques, NON mesurés sur l'enceinte)

Les trois fiches ci-dessous sont des produits du commerce choisis comme **repères de plausibilité** ; les haut-parleurs de Thomas sont d'un modèle non documenté. Après la phase 2, les colonnes $f_s$, $Q_{ms}$, $Q_{es}$, $R_e$, $L_e$ seront remplacées par les valeurs identifiées [[à mesurer]] ; $M_{ms}$, $Bl$, $S_d$ et $V_{as}$ **resteront des ordres de grandeur** tant qu'une manip de masse ajoutée ou de volume connu n'aura pas été faite (§ 01.6).

| Paramètre | 18″ 8 Ω sono — B&C 18PS76 | 18″ 8 Ω sono — Eminence Kilomax Pro-18A | 8″ 4 Ω pro — FaitalPRO 8FE200-4 |
|---|---|---|---|
| $R_e$ | 5,0 Ω | 5,07 Ω | 3,0 Ω |
| $L_e$ (à 1 kHz, valeur constructeur) | 1,9 mH | 1,59 mH | 0,25 mH |
| $f_s$ (champ libre) | 39 Hz | 32 Hz | 80 Hz |
| $Q_{ms}$ / $Q_{es}$ / $Q_{ts}$ | 6,1 / 0,29 / 0,27 | 10,15 / 0,49 / 0,47 | 8,7 / 0,47 / 0,45 |
| $M_{ms}$ | 149 g | 143 g | 15,3 g |
| $Bl$ | 25,8 T·m | 17,2 T·m | 7,0 T·m |
| $S_d$ | 1210 cm² | 1159 cm² | 209 cm² |
| $V_{as}$ (datasheet) | 207 L | 331,5 L | 15,8 L |

Grandeurs dérivées par `ordres_de_grandeur.py` (modèle sans pertes de caisse, champ libre) :

```
--- B&C 18PS76 (18", 8 ohm) ---
  Cms = 0.112 mm/N  Rms = 5.99 kg/s
  Qes : datasheet 0.290 | recalcule depuis Bl,Re,Mms,fs 0.274  (ecart -5.4 %)
  Qts : datasheet 0.277 | recalcule 0.262  (ecart -5.2 %)
  Vas : datasheet 207.0 L | recalcule rho0 c^2 Sd^2 Cms = 231.0 L  (ecart +11.6 %)
  Res = 111 ohm  Lces = 74 mH  Cmes = 224 uF
  |Z|max (modele, Qes recalcule) = 116 ohm a 39.0 Hz  ->  |Z|max/Re = 23.2
  a comparer a Re(1+Qms/Qes,datasheet) = 110 ohm  ->  1+Qms/Qes = 22.0  (ecart +5.5 %)
  |Z|(100 Hz) = 9.1 ohm, phase -52 deg ; |Z|min sur 20-500 Hz = 5.1 ohm
  impedance nominale : Re/Znom = 0.625 ; |Z|min/Znom = 0.635  (CEI 60268-5 : attendu >= 0.80)
--- Eminence Kilomax Pro-18A (18", 8 ohm) ---
  Qes : datasheet 0.490 | recalcule 0.493 (+0.6 %) ; Vas : 331.5 L | 328.1 L (-1.0 %)
  Res = 104 ohm  Lces = 51 mH  Cmes = 483 uF
  |Z|max = 110 ohm a 32.0 Hz -> |Z|max/Re = 21.6 ; 1+Qms/Qes(datasheet) = 21.7  (ecart -0.5 %)
  |Z|(100 Hz) = 5.8 ohm, phase -27 deg ; Re/Znom = 0.634 ; |Z|min/Znom = 0.638
--- FaitalPRO 8FE200-4 (8", 4 ohm) ---
  Qes : datasheet 0.470 | recalcule 0.471 (+0.2 %) ; Vas : 15.8 L | 16.0 L (+1.0 %)
  Res = 55 ohm  Lces = 13 mH  Cmes = 312 uF
  |Z|max = 58 ohm a 80.0 Hz -> |Z|max/Re = 19.5 ; 1+Qms/Qes(datasheet) = 19.5  (ecart -0.2 %)
  |Z|(100 Hz) = 14.6 ohm, phase -64 deg ; Re/Znom = 0.750 ; |Z|min/Znom = 0.758
```

Lecture (fourchettes, pas valeurs) :

- **18″ 8 Ω de sono** : $R_e\approx5$ Ω, $L_e\approx1{,}5$–2 mH, $f_s\approx30$–40 Hz en champ libre (donc $f_c\approx45$–70 Hz en caisse close de volume comparable à $V_{as}$), $Q_{ms}\approx6$–10, $Q_{es}\approx0{,}3$–0,5, $M_{ms}\approx150$ g, $Bl\approx17$–26 T·m, $V_{as}\approx200$–330 L. Branche motionnelle : $R_{es}\approx100$ Ω, $L_{ces}\approx50$–75 mH, $C_{mes}\approx200$–500 µF — des valeurs du **même ordre que les composants du filtre** (18 mH, 150 µF), ce qui explique que le filtre et le haut-parleur « se parlent ».
- **Médium 4 Ω** (un seul) : $R_e\approx3$ Ω, $L_e$ de quelques dixièmes de mH, $f_s$ de 50 à 100 Hz selon le diamètre et la suspension, $M_{ms}$ de 10 à 30 g, $Bl$ de 5 à 10 T·m. **Deux en série** : $R_e\approx6$ Ω, pic doublé.
- **Une datasheet n'est pas auto-cohérente.** Le test $Q_{es}$ recalculé depuis $Bl,R_e,M_{ms},f_s$ passe pour l'Eminence (+0,6 %) et la FaitalPRO (+0,2 %), mais **échoue de −5,4 % sur la B&C** ; le test $V_{as}=\rho_0c^2S_d^2C_{ms}$ retombe à −1,0 % et +1,0 % pour les deux premières mais à **+11,6 % pour la B&C**. Et sur cette même fiche, $|Z|_{max}/R_e$ vaut 23,2 selon le modèle nourri au $Q_{es}$ recalculé contre 22,0 selon $1+Q_{ms}/Q_{es}$ datasheet — **le signe « = » de l'identité du § 01.4 n'est vrai que si l'on injecte le même $Q_{es}$ des deux côtés**. Trois écarts concordants d'environ 5 à 12 % : ce n'est pas $\rho_0$ ni un arrondi, c'est la fiche qui n'est pas cohérente avec elle-même. **Ordre de grandeur de la confiance à accorder à une datasheet : 5 à 12 %** — et c'est le meilleur argument de la section pour justifier la mesure. Le même test d'auto-cohérence, avec le même seuil d'alerte, sera appliqué aux paramètres identifiés en phase 2.
- **Point de vigilance majeur pour le raccord.** Le $f_s$ des médiums en champ libre est déjà proche de 100 Hz (le « vers 50 Hz » de l'étudiant n'est pas confirmé ; les 8″ pro sont plutôt vers 80 Hz). Or **leur $f_s$ se décale aussi en $\sqrt{1+\alpha}$ dans leur propre chambre** :

```
--- Mediums en chambre close : fc = fs sqrt(1 + Vas/Vb) ---
  Vb =  5 L : alpha = 3.16 ; fc = 163 Hz      Vb = 20 L : alpha = 0.79 ; fc = 107 Hz
  Vb = 10 L : alpha = 1.58 ; fc = 128 Hz      Vb = 40 L : alpha = 0.40 ; fc =  94 Hz
```

  **Prédiction testable, formulée avant la mesure** : si les médiums occupent un volume clos de l'ordre de 20 à 40 L, leur $f_c$ tombe entre 94 et 107 Hz, c'est-à-dire **en plein sur la fréquence de raccord**. Le bloc présenterait alors à 100 Hz son pic d'impédance (plusieurs dizaines d'ohms, fortement réactif : 29 Ω à −64° en champ libre) — le pire cas possible pour le passe-haut $C_2$ série / $L_2$ parallèle calculé pour 8 Ω. Cela ne se saura qu'après la mesure [[à mesurer]], mais le volume de la chambre médium est à relever au mètre dès maintenant.

- Le modèle illustratif de la v1 (`archive-v1/_gen.py` : $R_e=6{,}5$ Ω, $R_{es}=44$ Ω, $f_s=40$ Hz, $L_{es}=0{,}1$ H, soit $C_{es}=158$ µF, $Q_{ms}=1{,}75$, $Q_{es}=0{,}259$, pic 50,5 Ω, $Z(100\ \mathrm{Hz})=14$ Ω — valeurs relues dans le fichier source) a un $Q_{ms}$ **trois à six fois plus faible** que les fiches ci-dessus : il est plausible en forme, pas en valeurs. Ne jamais le citer comme représentatif du sub.

### <a id="s01-14"></a>01.14 Ce que la section engage pour les phases 1 et 2

Récapitulatif actionnable, tout ce qui suit découlant des paragraphes ci-dessus :

| Point | Décision / contrainte | § |
|---|---|---|
| Bande d'ajustement | **20–300 Hz** (bornée en haut par la semi-inductance et les modes de membrane) | 01.12 |
| Type de caisse | **Tranché le 16 sept. 2026 : bass-reflex à DEUX évents** (constat de l'étudiant). Le cas clos reste au dossier comme comparaison pédagogique | 01.9, 01.10 |
| Nombre de paramètres | **8 par défaut** (`Z_bassreflex8`), 9 si l'on sépare les pertes. Les 5 paramètres du cas clos ne servent plus qu'à la vérification de routine du § 03.7 | 01.6, 01.10 |
| Prédiction géométrique | relever **cotes des 2 évents + volume net** au pied à coulisse **avant** la première mesure, et consigner la prédiction datée de $f_b$ sous forme d'**intervalle** | 01.10 bis |
| Outil d'optimisation | **Environnement vérifié le 2026-09-13 : Python 3.13.2, numpy 2.4.6, scipy 1.18.1, matplotlib 3.11.0 — tous installés et fonctionnels.** À 5 paramètres, avec les valeurs initiales de la méthode $r_0$, un Gauss-Newton ou un Nelder-Mead écrit en numpy suffirait ; à 8, `scipy.optimize.least_squares` est nettement préférable (matrice de covariance quasi gratuite pour les incertitudes) — et il est disponible. Le Levenberg-Marquardt réécrit en numpy pur (§ 03.3) reste au dossier comme **exercice de robustesse** et comme secours si les calculs sont refaits sur une machine du lycée : y **vérifier la présence de scipy** le cas échéant |  |
| Résolution en fréquence | pas **≤ 0,6 Hz** autour du pic (largeur à mi-hauteur $f_c/Q_{mc}\approx6{,}4$ Hz, il faut ≥ 10 points) ; **1/24 d'octave ou 1 Hz linéaire** sur 60–110 Hz pour le bloc médiums | 01.9, 01.12 |
| Durée de la manip | 10–500 Hz au 1/12 d'octave = **68 points × 2 voies ≈ 2,3 h** ; +25 points pour le resserrement 40–80 Hz au 1/24 d'octave. **Deux séances de TP, pas une** — à savoir avant de réserver la salle |  |
| Niveau d'excitation | préférer $R_{ref}=10\ \Omega$ à 100 Ω (facteur 7 sur le signal au minimum d'impédance) ; geler le niveau ; contrôler le ronflement 50 Hz ; deux relevés de $f_s$ espacés | 01.12 |
| Mesure de $R_e$ | compenser les cordons, ou extrapoler la méthode à deux voltmètres vers 5–10 Hz ; **$u(Q_{es})/Q_{es}=u(R_e)/R_e$** | 01.2 |
| Manip supplémentaire | **masse ajoutée** (ou volume clos connu) — sinon $Bl$, $M_{ms}$, $C_{ms}$, $R_{ms}$, $V_{as}$ resteront inconnus | 01.6 |
| Sensibilités pour le Monte-Carlo | $Q_{es}\propto R_e$ ; $r_0=\lvert Z\rvert_{max}/R_e$ ; $Q_{ms}=f_s\sqrt{r_0}/(f_2-f_1)$, donc très sensible à la résolution autour du pic | 01.4, 01.9 |
| Remontée en phase 0 | le critère « précision de $f_x$ » mesure la **DCR**, pas l'effet de $Z(f)$ ; l'effet de $Z(f)$ vit dans le critère « fidélité du raccord » | 01.8 |

### Ce qu'il faut retenir pour l'oral

- Le haut-parleur vu de ses bornes, c'est $R_e+j\omega L_e$ **plus** une branche RLC parallèle image de la mécanique (masse → $C_{mes}$, ressort → $L_{ces}$, frottements → $R_{es}$) via le gyrateur $Bl$ ; le pic d'impédance est une résonance **parallèle**, et comme la branche est passive, $|Z|\ge R_e$ partout.
- $|Z|_{max}=R_e(1+Q_{ms}/Q_{es})$ **à condition d'injecter le même $Q_{es}$ des deux côtés** : le « simple au sextuple » n'est pas un accident, c'est le rapport des amortissements mécanique et électrique. Les fiches de 18″ de sono donnent plutôt ×20 en champ libre ; la caisse et ses pertes ramènent le pic vers le bas — la mesure tranchera.
- **$Z(f)$ ne détermine que cinq nombres** ($R_e$, $L_e$, $f_c$, $Q_{mc}$, $Q_{ec}$). $Bl$, $M_{ms}$, $C_{ms}$, $R_{ms}$, $V_{as}$ ne sont **pas identifiables** sans une seconde manip (masse ajoutée ou volume connu) : la famille $Bl\sqrt{k}$, $kM_{ms}$, $C_{ms}/k$, $kR_{ms}$ donne exactement la même courbe. C'est la réponse à préparer pour le jury.
- Autour de 100 Hz la charge est **capacitive** ; sur 40–250 Hz elle varie d'un facteur ~20 en module et de ~130° en phase. Le filtre catalogue E12 sur cette charge garde son repère $-3$ dB à 4 % près mais **prend +14 dB de bosse** (4,7 dB RMS d'écart) : la grandeur sensible est la **forme**, pas une fréquence. Ce qui déplace les repères $-3$ dB, c'est la DCR (+5,5 % pour 1 Ω, pour $-1$ dB de perte plate) — le croisement $f_x$, lui, ne bouge presque pas (§ 04.1).
- La caisse close monte $f_s$ en $f_c=f_s\sqrt{1+V_{as}/V_b}$ sans changer la hauteur théorique du pic ; le bass-reflex donne deux pics et un creux à $f_b$, avec $f_Lf_H=f_sf_b$ et $f_L<f_b<f_H$ démontré. La datasheet ne remplace jamais la mesure en caisse — d'autant que sur les trois fiches consultées, l'une n'est pas auto-cohérente à mieux que 5–12 %.
- **La caisse de l'enceinte est bass-reflex, à deux évents** (constat du 16 sept. 2026). Conséquence qu'il faut dire en une phrase, et la dire **juste** : ce qui écarte les deux pics, c'est $\alpha=V_{as}/V_b$ ($f_L^2+f_H^2=f_s^2(1+\alpha)+f_b^2$ à produit $f_Lf_H=f_sf_b$ constant), de sorte qu'une **caisse petite devant $V_{as}$ remonte le pic haut vers le raccord** ; l'accord $f_b$, lui, déplace les deux pics dans le même sens. Sur un jeu plausible de sono ($\alpha=3$) le pic haut tombe à **86 Hz, c'est-à-dire dans la zone de raccord**, avec $\lvert Z\rvert(100\ \text{Hz})=22{,}4$ Ω au lieu de 8. L'hypothèse « 8 Ω » y est donc *plus* fausse qu'en caisse close (9,7 Ω) : la découverte renforce le sujet au lieu de l'affaiblir. À l'accord même, la membrane est quasi immobile — c'est l'évent qui rayonne — donc la f.é.m. induite s'effondre et $\lvert Z\rvert$ retombe à $R_e$.
- **$f_b$ se prédit au pied à coulisse**, sans rien brancher : $f_b=\frac{c}{2\pi}\sqrt{N S_p/(V_b\ell_{\text{eff}})}$, résonateur de Helmholtz à $N$ masses d'air en parallèle. La seule subtilité est la correction de bout, dont les conventions ne s'accordent qu'à ±3 % : la prédiction s'annonce donc en **intervalle**. Confrontée au creux d'impédance *mesuré* et au $f_b$ *ajusté*, elle donne trois voies indépendantes vers la même grandeur — une boucle théorie/expérience fermée qui ne doit rien à l'ajustement (§ 01.10 bis).
- Le modèle est petit signal, à un degré de liberté et à $L_e$ constant : dérive thermique de $R_e$ (≈ +0,4 %/K), non-linéarités $Bl(x)$, semi-inductance et modes de membrane en haut de bande — quatre limites à annoncer avant que le jury ne les demande, et qui justifient de borner le fit à 20–300 Hz.

### Sources

- A. N. Thiele, « Loudspeakers in Vented Boxes », *Proceedings of the IRE Australia*, vol. 22, n° 8, p. 487–508 (août 1961) — communication présentée à la convention IRE de Sydney, 1961. Réimprimé en deux parties dans le *Journal of the Audio Engineering Society*, vol. 19, n° 5, p. 382–392 (mai 1971) et n° 6, p. 471–483 (juin 1971).
- R. H. Small, « Direct Radiator Loudspeaker System Analysis », *JAES*, vol. 20, n° 5, p. 383–395 (juin 1972). Définit $Q_{ms}$, $Q_{es}$, $Q_{ts}$, $V_{as}$ et la méthode de mesure par le pic d'impédance (méthode $r_0$).
- R. H. Small, « Closed-Box Loudspeaker Systems, Part I: Analysis », *JAES*, vol. 20, n° 10, p. 798–808 (décembre 1972). Formules $f_c=f_s\sqrt{1+\alpha}$, $Q_{tc}=Q_{ts}\sqrt{1+\alpha}$.
- R. H. Small, « Vented-Box Loudspeaker Systems, Part I: Small-Signal Analysis », *JAES*, vol. 21, n° 5, p. 363–372 (juin 1973). Deux pics d'impédance, accord $f_b$, et les trois pertes de caisse $Q_l$, $Q_a$, $Q_p$.
- J. Vanderkooy, « A Model of Loudspeaker Driver Impedance Incorporating Eddy Currents in the Pole Structure », *JAES*, vol. 37, n° 3, p. 119–128 (mars 1989). Origine physique de la semi-inductance ($n=1/2$).
- W. M. Leach, « Loudspeaker Voice-Coil Inductance Losses: Circuit Models, Parameter Estimation, and Effect on Frequency Response », *JAES*, vol. 50, n° 6, p. 442–450 (juin 2002). Modèle $K(j\omega)^n$ et son identification par régression ($n\approx0{,}6$–0,7).
- V. Dickason, *The Loudspeaker Design Cookbook*, 7ᵉ édition, Audio Amateur Press, 2005 (réimpressions ultérieures), ISBN 978-1-882580-47-7. Chapitres sur les paramètres T-S, la caisse close et le bass-reflex ; référence de vulgarisation la plus citée pour le DIY. C'est aussi la source usuelle de la **formule de longueur d'évent** avec la correction de bout $1{,}463\,R$ par tube, reprise au § 01.10 bis — **la constante numérique y est donnée dans un système d'unités particulier** (rayon en cm, volume en litres) : la nôtre est redémontrée depuis $f_b=\frac{c}{2\pi}\sqrt{NS_p/(V_b\ell_{\text{eff}})}$ et vaut 94 169 pour $c=344$ m/s [[à recouper sur l'édition papier au CDI si le jury demande la référence de la constante]].
- **Correction de bout d'un tube ouvert**, deux régimes à ne pas confondre (§ 01.10 bis) : extrémité **libre**, $\delta=0{,}6133\,a$ — H. Levine et J. Schwinger, « On the Radiation of Sound from an Unflanged Circular Pipe », *Physical Review*, vol. 73, n° 4, p. 383–406 (février 1948), solution exacte par factorisation de Wiener-Hopf, limite basse fréquence ; extrémité **bridée** (affleurant un plan infini), $\delta=0{,}8216\,a$ — Lord Rayleigh, *The Theory of Sound*, vol. II, § 307, souvent approchée par $8a/(3\pi)=0{,}8488\,a$, valeur issue de la réactance de rayonnement du piston bafflé (Beranek, *Acoustics*, ch. 5). Les deux nombres circulent dans la littérature haut-parleur sans que l'extrémité décrite soit toujours précisée : d'où l'encadrement explicite retenu ici plutôt qu'une valeur unique.
- Documentation de **REW** (Room EQ Wizard), pages « Impedance Measurement » et « Thiele-Small Parameters », roomeqwizard.com. Décrit l'ajustement aux moindres carrés d'un modèle à composants ($R_E$, $dR$, $L_{EB}$, $L_E$ // $K_E$ // $R_{SS}$) et les quatre protocoles (champ libre, masse ajoutée, caisse close, double masse ajoutée, ce dernier d'après Candy & Futtrup 2017). Consultée le 2026-09-09.
- **CEI 60268-5** (*Équipements pour systèmes électroacoustiques — Partie 5 : haut-parleurs*) : définition de l'impédance nominale par le minimum du module (≥ 80 % de $Z_{nom}$). Citée de seconde main [[à vérifier sur le texte de la norme si le jury le demande]].
- Datasheets constructeurs utilisées pour les ordres de grandeur du § 01.13 : B&C Speakers, fiche 18PS76 (bcspeakers.com) ; Eminence, fiche Kilomax Pro-18A (eminence.com) ; FaitalPRO, fiche 8FE200 4 Ω (faitalpro.com). Consultées le 2026-09-02.
- Scripts de vérification (numpy 2.4, Python 3.13, hors dépôt) : `scratchpad/sec01/modele_ts.py`, `ordres_de_grandeur.py`, `verif_br.py`, `filtre_sur_charge.py`, `degen_pertes.py`, `divers.py`, `fig_impedance.py`. Ajouts du 16 sept. 2026 : `helmholtz.py` (formule de $f_b$ à $N$ évents, encadrement des corrections de bout, budget d'incertitude), `br2.py` (caractérisation du jeu bass-reflex : pics, creux, largeurs, pentes, contrôles analytiques), `br3.py` (déplacement de membrane et règle de sécurité du § 02.6), `br4.py` (filtre catalogue sur les trois charges, branche des pavillons), `keele.py` (pondération de sommation à $N$ évents, § 07.3).

## <a id="s02"></a>02. Mesure de l'impédance Z(f) : montage, formules, incertitudes

> Acte 1 du récit v2. Tout le sujet repose sur cette capacité : relever
> $\underline{Z}(f) = |Z|\,e^{j\varphi}$ (module **et** phase) du subwoofer en caisse et du
> bloc médiums, avec des incertitudes chiffrées. La chaîne est d'abord validée sur des
> composants connus (porte de validation de la phase 1). Rien n'a encore été mesuré sur
> l'enceinte : tous les chiffres ci-dessous sont des calculs, des spécifications citées ou
> des ordres de grandeur explicitement étiquetés.

**Bande retenue : 10 Hz – 1 kHz pour le sub, 10 Hz – 2 kHz pour le bloc médiums.**
FEUILLE-DE-ROUTE.md écrit « 10–500 Hz » : cette borne est trop basse pour deux raisons
chiffrées au § 02.6 — l'identification de $L_e$ à l'acte 2 et le dimensionnement du
passe-haut (et d'un éventuel Zobel) à l'acte 3 ont besoin de la remontée inductive, qui
commence à peine à 500 Hz. **Correction à reporter dans FEUILLE-DE-ROUTE.md § phase 1.**

### <a id="s02-1"></a>02.1 Principe : diviseur de tension à résistance étalon, sans hypothèse de courant constant

Montage : GBF → résistance étalon $R_{ref}$ → dipôle testé (haut-parleur, ou composant
d'étalonnage). Le **même courant** $\underline{I}$ traverse $R_{ref}$ et le dipôle. En régime
sinusoïdal (notation complexe, programme PTSI) :

$$\underline{V}_R = R_{ref}\,\underline{I}, \qquad \underline{V}_d = \underline{Z}\,\underline{I}
\quad\Longrightarrow\quad
\boxed{\;\underline{Z} = R_{ref}\,\frac{\underline{V}_d}{\underline{V}_R}\;}$$

soit, en module et en argument :

$$|Z| = R_{ref}\,\frac{|V_d|}{|V_R|}, \qquad
\varphi = \arg\underline{V}_d - \arg\underline{V}_R, \qquad
\varphi\,[\mathrm{rad}] = 2\pi f\,\Delta t \;\Longleftrightarrow\; \varphi\,[^\circ] = 360\,f\,\Delta t$$

où $\Delta t$ est le décalage temporel de $v_d(t)$ par rapport à $v_R(t)$ (image du courant),
**compté positivement si $v_d$ est en avance sur $v_R$** ($\varphi > 0$ : inductif).

Cette formule est **exacte quelles que soient** la valeur de $R_{ref}$, l'impédance de sortie
du GBF (50 Ω typiquement), la résistance des câbles côté GBF et l'amplitude : on mesure le
rapport de deux tensions prises **au même instant** sur le même courant. C'est une identité
algébrique — il n'y a rien à « vérifier numériquement », et le contrôle utile porte sur la
propagation des erreurs de lecture (§ 02.7). Attention : $\underline{V}_{tot} = \underline{V}_R + \underline{V}_d$
est une somme de **phaseurs**, pas d'amplitudes ; pour $R_{ref} = 100\ \Omega$ et
$\underline{Z} = 14{,}1\,e^{-j47{,}5°}$, $|V_d| + |V_R|$ dépasse $|V_{tot}|$ de 3,7 % (calculé).

C'est ce qui distingue la méthode de l'approximation « courant constant »
($I \approx V_{GBF}/R_{ref}$, valable seulement si $R_{ref} \gg |Z|$), dont l'erreur vaut
$I_{réel}/I_{supposé} - 1 = R_{ref}/|R_{ref} + \underline{Z}| - 1$ :

| $R_{ref}$ | $\lvert Z\rvert = 8\ \Omega$ | $50\ \Omega$ | $100\ \Omega$ | $172\ \Omega$ |
|---|---|---|---|---|
| 10 Ω | −44 % | −83 % | −91 % | −94 % |
| 100 Ω | −7,4 % | −33 % | −50 % | −63 % |
| 1 kΩ | −0,8 % | −4,8 % | −9,1 % | −15 % |

*Sous-estimation de $\lvert Z\rvert$ si l'on suppose $I$ constant (calculé, impédance de sortie
du GBF ignorée). Évalué pour $\underline{Z}$ **réelle** : exact au sommet du pic ($\varphi = 0$) et
sur le plateau, et majorant sur les flancs — par exemple −9,1 % au lieu de −12,4 % pour
$|Z| = 14{,}1\ \Omega$ à $\varphi = -47{,}5°$, −23,9 % au lieu de −28,6 % pour $40\ \Omega$ à
$-45°$ (calculé).*

**Quelle est la hauteur réelle du pic ?** C'est le chiffre qui pilote tout le
dimensionnement, et l'ordre de grandeur « 40–60 Ω » hérité de la v1 est faux pour un 18″ de
sonorisation. La hauteur du pic d'impédance vaut

$$Z_{pic} = R_e\left(1 + \frac{Q_{ms}}{Q_{es}}\right)$$

et elle est **invariante en caisse close** ($Q_{mc}$ et $Q_{ec}$ sont multipliés par le même
facteur $F_c/F_s$ : le pic se déplace en fréquence, pas en hauteur). Pour un 18″ de catalogue
(Eminence Delta Pro-18A, valeurs constructeur : $R_e = 5{,}3\ \Omega$, $F_s = 28$ Hz,
$Q_{ms} = 10{,}38$, $Q_{es} = 0{,}33$, $L_e = 3{,}43$ mH), on obtient **172 Ω** ; avec un rapport
$Q_{ms}/Q_{es}$ plus modeste (10), 58 Ω. **Ordre de grandeur à retenir : 60 à 200 Ω pour le
sub**, souvent un peu moins en caisse réelle (fuites, absorption). En revanche 40–60 Ω est
bien l'ordre de grandeur du **bloc médiums** (2 × 4 Ω en série : $R_e \approx 6{,}4\ \Omega$,
$Z_{pic} \approx 45$–60 Ω, calculé). La valeur réelle sera fixée par la passe 1 [[à mesurer]].

Deux conséquences à assumer publiquement :

- **La formulation « l'impédance varie du simple au sextuple » de la problématique est
  probablement fausse** : la dynamique $|Z|_{max}/|Z|_{min}$ calculée sur des jeux de
  paramètres plausibles va de **13 à 32**, pas 6. C'est un **résultat de la phase 1**
  [[à mesurer]] ; la problématique devra être ajustée après la mesure.
  **Formulation de remplacement à adopter dès maintenant, et à reporter dans CLAUDE.md,
  FEUILLE-DE-ROUTE.md et MCOT.md : « un haut-parleur dont l'impédance varie fortement avec la
  fréquence »** — sans aucun chiffre tant que la phase 1 n'a pas mesuré $Z(f)$.
- L'argument « courant constant » en sort **renforcé** : avec $R_{ref} = 100\ \Omega$,
  l'approximation fausserait le pic non pas de 30 % mais de 50 à 63 %.

Avec 1 kΩ l'approximation serait acceptable, mais $V_d$ tomberait à quelques millivolts
(bruit, quantification). La mesure du rapport $V_d/V_R$ **supprime ce dilemme** : on peut
choisir $R_{ref}$ du même ordre que $|Z|$ pour avoir des tensions confortables, sans perdre
l'exactitude.

### <a id="s02-2"></a>02.2 Câblage : le problème de la masse et les trois configurations

Un oscilloscope de lycée a des entrées **asymétriques** : les pinces de masse de toutes les
voies sont reliées entre elles et au châssis, lui-même relié à la **terre** du secteur. Si la
borne froide (blindage BNC) du GBF est elle aussi à la terre, **un seul nœud** du circuit peut
recevoir des pinces de masse, et l'une des deux tensions doit s'obtenir par soustraction.

> **Étape 0 du protocole, trois minutes à l'ohmmètre** : mesurer entre la borne froide du BNC
> de sortie du GBF et la terre du secteur (broche de terre d'une prise). **Continuité →
> sortie référencée, configuration A ou B. Isolement → sortie flottante, configuration C.**
> Ce test conditionne tout le reste du paragraphe et une bonne moitié du bilan d'incertitude.

```
Configuration A (dipôle à la masse) — sortie GBF référencée à la terre

 GBF (chaud) ----[ R_ref ]----+---- dipôle Z ----+
      |                       |                  |
    CH2 = V_tot             CH1 = V_d          masse commune (GBF froid + les 2 pinces)
                              V_R = V_tot - V_d  (soustraction)

Configuration B (R_ref à la masse) — idem, quand |Z| > R_ref

 GBF (chaud) ----[ dipôle Z ]----+---- R_ref ----+
      |                          |               |
    CH2 = V_tot                CH1 = V_R       masse commune
                               V_d = V_tot - V_R  (soustraction)

Configuration C (nœud milieu à la masse) — SI ET SEULEMENT SI la sortie du GBF est flottante

 GBF (chaud) ----[ R_ref ]----+----[ dipôle Z ]---- GBF (froid)
                              |
                       masse commune  ;  CH1 = +V_R  et  CH2 = -V_d, LUES DIRECTEMENT
                       (inverser CH2, ou fonction Invert ; phi = arg(-V_CH2) - arg(V_CH1))
```

**La configuration C est strictement meilleure et doit être essayée en premier.** Les deux
tensions sont lues directement : plus de voie MATH, plus de soustraction, plus de facteur
d'amplification, et le déphasage se lit directement entre les deux voies. Un ordinateur
portable **sur batterie** avec une carte son en générateur donne également une source
flottante, tout comme un GBF alimenté par un transformateur d'isolement.

**Règle du choix A/B** : la tension obtenue par soustraction hérite des incertitudes des deux
autres ; si elle est petite, son incertitude relative explose. On met donc **à la masse
l'élément dont la tension est la plus petite**. Le point de bascule est exactement
$|Z| = R_{ref}$. Le facteur d'amplification de l'incertitude relative admet une forme close
(démontrée et vérifiée numériquement, erreurs relatives égales sur les deux lectures) :

$$c_A = \sqrt{2}\left(1 + \frac{|Z|}{R_{ref}}\right) \quad\text{(config. A)}, \qquad
c_B = \sqrt{2}\left(1 + \frac{R_{ref}}{|Z|}\right) \quad\text{(config. B)}$$

| $R_{ref}$ | $\lvert Z\rvert = 5{,}3\ \Omega$ | $8\ \Omega$ | $50\ \Omega$ | $100\ \Omega$ | $172\ \Omega$ |
|---|---|---|---|---|---|
| 100 Ω — config. A | ×1,49 | ×1,53 | ×2,12 | ×2,83 | ×3,85 |
| 100 Ω — config. B | ×28 | ×19 | ×4,24 | ×2,83 | ×2,24 |
| 10 Ω — config. A | ×2,16 | ×2,55 | ×8,49 | ×15,6 | ×25,7 |
| 10 Ω — config. B | ×4,08 | ×3,18 | ×1,70 | ×1,56 | ×1,50 |

Lecture : avec $R_{ref} = 100\ \Omega$, la configuration A est la meilleure tant que
$|Z| < 100\ \Omega$ et son facteur ne dépasse pas ×3,9 même à un pic de 172 Ω — **on la garde
sur toute la bande** plutôt que de recâbler en cours de série (un recâblage change les
impédances de contact et casse la traçabilité), en sachant qu'au pic elle coûte un facteur
près de 4 sur $u(V_R)$. Avec $R_{ref} = 10\ \Omega$, c'est la configuration B qui s'impose dès
$|Z| > 10\ \Omega$, donc partout : le recoupement 10 Ω se fait en configuration B.

**Méthode de lecture principale : les deux voies brutes, la soustraction en Python.** On
relève $|V_{CH1}|$, $|V_{CH2}|$ et leur déphasage $\theta$, on corrige chaque voie de son
facteur d'appariement, puis on soustrait **les phaseurs** dans le code de dépouillement
(§ 02.7). La voie **MATH = CH2 − CH1** est reléguée au **contrôle visuel en direct** (vérifier
que la tension déduite a bien l'allure et l'ordre de grandeur attendus). Deux raisons :

1. MATH calcule CH2 − CH1 sur les voies **brutes**. Or la correction exacte est
   $V_{CH2}/\kappa_2 - V_{CH1}/\kappa_1$, et $(\text{CH2} - \text{CH1})/\kappa \ne
   \text{CH2}/\kappa_2 - \text{CH1}/\kappa_1$ dès que $\kappa_1 \ne \kappa_2$ : **le facteur
   d'appariement ne peut pas être appliqué a posteriori sur la sortie de MATH**, c'est-à-dire
   précisément sur la tension qui porte l'amplification d'incertitude.
2. [[à vérifier sur l'oscilloscope du lycée : la voie MATH est-elle acceptée comme **source**
   des mesures automatiques de délai/phase ? Sur beaucoup d'appareils d'entrée de gamme, non.]]

**Où entre le facteur d'appariement.** Seul le **rapport** des deux voies compte : une erreur
de gain commune s'élimine, seul le désappariement subsiste. On applique le même signal aux deux
voies au couple de calibres utilisé et on note $\kappa = V_{CH1}^{lu}/V_{CH2}^{lu}$ (attendu
1,00 ± 0,01). La formule de dépouillement devient, en configuration A :

$$\underline{Z} = R_{ref}\;\frac{\underline{V}_{CH1}/\kappa}{\underline{V}_{CH2} - \underline{V}_{CH1}/\kappa}
\qquad\text{(config. C : } \underline{Z} = R_{ref}\,\dfrac{-\underline{V}_{CH2}}{\underline{V}_{CH1}/\kappa}\text{)}$$

CH1 et CH2 ne sont **jamais** sur le même calibre en pratique ($V_d \approx 0{,}15$ V et
$V_R \approx 1{,}9$ V) : $\kappa$ doit donc être relevé **pour chaque couple de calibres
réellement utilisé** et consigné dans l'en-tête de série. Astuce pour chaîner les calibres :
lire un même signal stable sur **une seule voie** à deux calibres adjacents (par exemple 1 V
lu à 0,2 V/div puis à 0,5 V/div) donne directement le rapport de ces deux calibres ; de
proche en proche on rapporte tous les calibres à un calibre de référence.

**Faute classique** : pince de masse de CH1 sur le nœud intermédiaire et pince de masse de
CH2 sur le froid du GBF. L'élément situé entre les deux pinces est **court-circuité par le
châssis de l'oscilloscope** : mesure fausse, GBF éventuellement en court-circuit. Avant de
mettre sous tension, vérifier à l'ohmmètre que les deux pinces de masse sont sur le même
nœud, ou n'utiliser qu'une seule pince de masse.

**Liaisons** : préférer des **cordons coaxiaux BNC–bananes** aux sondes ×1, dont le fil de
masse volant de 15 cm forme une boucle qui capte le secteur — c'est le remède le plus
efficace au piège « secteur » du § 02.10. À défaut, sondes en position **×1** identiques sur
les deux voies (signal faible, 8 bits), couplage **DC** (le couplage AC ajoute un déphasage de
type passe-haut sensible sous 20–30 Hz). Charge des entrées : 1 MΩ // ~100 pF en parallèle sur
100 Ω → erreur 0,010 % ; 100 pF à 500 Hz ≈ 3,2 MΩ → négligeable (calculé).

### <a id="s02-3"></a>02.3 Phase : décalage temporel ou figure de Lissajous

**Décalage temporel (méthode principale).** Base de temps réglée pour qu'une période occupe
l'écran ; curseurs (ou mesure automatique « phase / delay ») entre les passages par zéro
montants ; convention $\Delta t > 0$ si $v_d$ est en avance ($\varphi > 0$, inductif).
Réglages qui décident du résultat :

- **déclencher sur la voie de plus grande amplitude** (CH2 = $V_{tot}$ en configuration A),
  jamais sur la voie faible : sinon le moyennage lisse le signal lui-même au lieu du bruit ;
- couplage de déclenchement en DC (pas de *LF reject*, qui déphase sous 30 Hz) ;
- mode moyennage 16 à 64 acquisitions, **réarmé après chaque changement de fréquence**, en
  attendant sa convergence avant de lire.

$$u(\varphi)\,[^\circ] = 360\, f\, u(\Delta t)$$

| $f$ | $u(\Delta t) = 10\ \mu s$ | $50\ \mu s$ | $100\ \mu s$ | $\Delta t$ pour 1° |
|---|---|---|---|---|
| 10 Hz | 0,04° | 0,18° | 0,36° | 278 µs |
| 40 Hz | 0,14° | 0,72° | 1,4° | 69 µs |
| 100 Hz | 0,36° | 1,8° | 3,6° | 28 µs |
| 500 Hz | 1,8° | 9,0° | 18° | 5,6 µs |

À 500 Hz, il faut placer les curseurs à quelques microsecondes près : resserrer la base de
temps (une demi-période à l'écran) ou utiliser la mesure automatique moyennée. La base de
temps elle-même (±25 ppm sur un DS1054Z) est négligeable ; c'est le pointé qui domine.

**Fréquence.** Relever la fréquence **lue par le fréquencemètre de l'oscilloscope**, pas la
consigne du GBF, et l'enregistrer **avec toute sa résolution** (6 chiffres sur un DS1054Z, soit
$u(f)/f \sim 10^{-5}$). Ne pas se contenter de 0,1 Hz : à 40 Hz cela ferait 0,25 %, ce qui
coûterait 4,3 % sur $|Z|$ sur le flanc d'un pic de $Q = 17$ (§ 02.6).

**Lissajous (contrôle visuel).** Mode XY, $x = v_R$, $y = v_d$ : $\sin\varphi = A/B$ avec $A$
l'ordonnée à $x = 0$ et $B$ l'amplitude maximale de $y$. Incertitude
$u(\varphi) = u(A/B)/\cos\varphi$ : pour $u(A/B) = 0{,}02$ — **incertitude absolue sur le
rapport sans dimension**, soit environ 2 % de la hauteur de l'écran — on obtient 1,2° à 0°,
2,3° à 60°, 13° à 85° (calculé). Inutilisable près de ±90° (condensateur, self) et sans signe.
Usage recommandé : **trouver la fréquence où l'ellipse se referme en segment** ($\varphi = 0$),
c'est-à-dire le sommet du pic d'impédance, à mieux que 1 % [ordre de grandeur].

### <a id="s02-4"></a>02.4 Choix de $R_{ref}$ et de la configuration

**Ce choix se fait APRÈS la passe 1**, pas avant : il dépend de $Z_{pic}$, qui est justement
ce que la passe 1 mesure. Passe 1 exploratoire à $R_{ref} = 100\ \Omega$ en configuration A →
lecture de $f_{pic}$, $Z_{pic}$ et $Q$ → choix définitif de $R_{ref}$, de la configuration et
des calibres → passes 2 et 3.

Quatre contraintes, la première étant dominante :

1. **Conditionnement de la soustraction.** C'est la contrainte dominante : $c_A$ impose
   $R_{ref} \gtrsim 3\,|Z|$ (§ 02.2). Elle pousse $R_{ref}$ vers le haut.
2. **Conditionnement 8 bits.** Le rapport $V_d/V_R = |Z|/R_{ref}$ ; la valeur qui équilibre
   les deux extrémités est la moyenne géométrique. Avec la vraie dynamique
   (5,3 à 172 Ω, facteur 32) : $\sqrt{5{,}3 \times 172} = 30\ \Omega$, soit **33 Ω en E12**
   (calculé) — et non les 17 Ω obtenus en supposant un pic à 50 Ω. Mais cette contrainte est
   largement levée par le réajustement du niveau à chaque point (§ 02.5), qui permet de garder
   les deux tensions dans une fenêtre confortable quel que soit $R_{ref}$.
3. **Niveau et courant.** Un GBF de laboratoire a ~50 Ω de sortie et fournit typiquement 10 V
   crête au maximum [[à vérifier sur le GBF du lycée]]. Courants et puissances (RMS) :

   | $V_{GBF}$ crête (f.é.m. à vide) | $R_{ref}$ | $\lvert Z\rvert$ | $I$ | $V_d$ | $V_R$ | $P_{HP}$ | $P_{R_{ref}}$ |
   |---|---|---|---|---|---|---|---|
   | 1 V | 100 Ω | 8 Ω | 4,5 mA | 36 mV | 0,45 V | 0,16 mW | 2,0 mW |
   | 5 V | 100 Ω | 8 Ω | 22 mA | 0,18 V | 2,24 V | 4,0 mW | 50 mW |
   | 5 V | 100 Ω | 50 Ω | 18 mA | 0,88 V | 1,77 V | 16 mW | 31 mW |
   | 5 V | 100 Ω | 172 Ω | 11 mA | 1,89 V | 1,10 V | 21 mW | 12 mW |
   | 5 V | 10 Ω | 8 Ω | 52 mA | 0,42 V | 0,52 V | 22 mW | 27 mW |
   | 10 V | 10 Ω | 8 Ω | 104 mA | 0,83 V | 1,04 V | 87 mW | 108 mW |

   *Calculé avec $I = (V_{GBF}/\sqrt2)/(Z_s + R_{ref} + |Z|)$ et $Z_s = 50\ \Omega$
   d'impédance de sortie du GBF ; valeurs RMS. Sans ces 50 Ω, la dernière ligne donnerait
   393 mA et **1,2 W** dans le haut-parleur, hors régime petits signaux : l'hypothèse compte.
   Attention aussi à la convention d'affichage — beaucoup de GBF affichent l'amplitude en
   supposant une charge adaptée de 50 Ω et délivrent le double à vide. **Vérifier le réglage
   High-Z / 50 Ω et mesurer à l'oscilloscope la tension réellement délivrée, ne jamais se fier
   à l'afficheur** [[à vérifier]].*

   Une résistance étalon de 1 W (ou 2 W) suffit ; le haut-parleur reçoit au plus ~0,1 W.
4. **Exactitude de $R_{ref}$.** Tolérance 1 % ; mieux : mesurer sa valeur DC au multimètre
   (fonction REL pour annuler les cordons, ou 4 fils) et utiliser **la valeur mesurée**. Non
   inductive de préférence (film métallique) ; une bobinée de 10 µH à 500 Hz sur 100 Ω donne
   $X = 0{,}031\ \Omega$, soit $X/R = 0{,}03\ \%$ → **erreur de phase 0,02° et erreur sur le
   module $5\cdot10^{-6}\ \%$** : négligeable sur les deux (calculé).

**Décision.** $R_{ref} = 100\ \Omega$ 1 % en configuration A comme étalon principal ; $10\ \Omega$
en configuration B pour le recoupement au pic ; **ajouter une $33\ \Omega$ 1 %** à la liste
d'achats (≈ 1 €, négligeable devant le budget de 500 €) au cas où la passe 1 révélerait un pic
modeste. L'arbitrage est assumé : le conditionnement 8 bits désignerait 33 Ω, mais on retient
100 Ω parce qu'il minimise le facteur d'amplification de la soustraction (≤ ×3,9 partout) et
parce que c'est la valeur recommandée par REW sur une sortie casque, ce qui rend les deux
méthodes directement comparables. Les deux jeux (10 Ω et 100 Ω) doivent coïncider : c'est un
**contrôle de cohérence interne** gratuit, chiffré au § 02.8.

### <a id="s02-5"></a>02.5 Niveau de signal : régime petits signaux

Le modèle de Thiele-Small à identifier (acte 2) est un modèle **linéaire petits signaux**.
REW recommande une tension aux bornes du haut-parleur « de l'ordre de 100 mV à 200 mV au
plus » ; c'est un **plafond**, pas une consigne.

**Décision gelée : le niveau du GBF est réajusté à chaque point pour maintenir
$V_d$ entre 100 et 200 mV RMS, et la valeur retenue est consignée** (colonne du tableau
§ 02.12). Trois raisons, toutes vérifiables :

- La mesure de $Z$ est un **rapport** : elle est insensible au niveau tant qu'on reste
  linéaire. On est donc libre du niveau, et on s'en sert pour garder l'écran rempli sur les
  deux voies — ce qui maintient $\varepsilon$ constant sur toute la bande (§ 02.7).
- À amplitude GBF **fixe**, $V_d$ suit $|Z|$ : avec $R_{ref} = 100\ \Omega$ et
  $V_{tot} = 3$ V RMS, $V_d$ passerait de 151 mV sur le plateau à 1,9 V au pic de 172 Ω
  (facteur 12,6, calculé). Soit on cale le pic à 150 mV et le plateau tombe à 12 mV
  (≈ 1 division → 24 % d'erreur de gain), soit on remplit l'écran sur le plateau et le pic
  reçoit douze fois plus.
- **C'est au pic que l'hypothèse petits signaux est la plus fragile.** Avec
  $R_{ref} \gg |Z|$ on attaque quasiment à **courant constant** : l'amortissement n'est plus
  qu'électrique côté mécanique, et l'excursion est **maximale à la résonance**. À tension aux
  bornes constante en revanche, l'excursion près de $f_s$ vaut $x \approx V_d/(Bl\,\omega)$,
  indépendante de l'amortissement : ≈ 30 µm pour $V_d = 150$ mV, $Bl \approx 20$ N/A et
  $f = 40$ Hz [ordre de grandeur, $Bl$ [[à confirmer]]]. Le réajustement du niveau **est** la
  protection contre la non-linéarité.

À $V_d = 150$ mV constants et $R_{ref} = 100\ \Omega$ : le courant vaut 19 mA sur le plateau
(2,8 mW) et seulement 0,9 mA au pic de 172 Ω (0,13 mW), et $V_{tot}$ va de 2,0 V à 0,24 V
(calculé) — tout tient dans la plage du GBF. Sur le plateau, 100–200 mV correspondent à
12–25 mA (1 à 5 mW) ; au pic, à 0,6–1,2 mA seulement.

> **Différence de méthode à garder en tête** : REW balaie à **niveau de sortie fixe**. Le
> réglage REW doit donc être fait de sorte que la tension aux bornes **au sommet du pic**
> reste ≤ 200 mV — sur le plateau elle sera alors bien plus faible. Les deux méthodes ne
> mesurent donc pas au même niveau : c'est une cause légitime d'écart au § 02.9.

Autres conséquences du régime petits signaux :

- **Pas d'échauffement** : $R_e$ suit le cuivre, $\alpha_{Cu} = 3{,}93\cdot10^{-3}\ \mathrm{K^{-1}}$
  à 20 °C → **+0,393 %/K, +2,0 % pour 5 K, +3,9 % pour 10 K** (calculé). Mesurer $R_e$ au
  multimètre **avant et après** chaque série ; noter la température ambiante.
- **Contrôle de non-linéarité au pic, AVANT la passe 2** : refaire le point de pic (et 100 Hz,
  300 Hz) à amplitude moitié et double ; $|Z|$ et $\varphi$ ne doivent pas bouger au-delà de
  $u$. Si le pic s'affaisse quand le niveau monte, on est sorti du régime linéaire (la
  robustesse en grand signal est l'affaire de l'acte 4, aux deux niveaux gelés).
- **Offset DC du GBF à zéro** (un courant continu décale la membrane et fausse $R_e$).
- **Distorsion et bruit** : la valeur RMS affichée par un oscilloscope intègre les harmoniques
  et le bruit, alors que $\underline{Z} = \underline{V}/\underline{I}$ suppose un fondamental pur.
  REW, qui extrait le fondamental du balayage, n'a pas ce biais : c'est une cause
  **systématique** d'écart entre les deux méthodes. Remèdes : lire l'**amplitude
  crête-à-crête sur une base de temps d'une période** avec moyennage synchrone (le bruit non
  cohérent s'efface), et vérifier à l'œil que la sinusoïde n'est pas écrêtée.

### <a id="s02-6"></a>02.6 Bande, grille de fréquences et répartition des rôles

**Bande.** 10 Hz – 1 kHz pour le sub, 10 Hz – 2 kHz pour le bloc médiums. Justification
chiffrée : avec $L_e = 3{,}43$ mH (valeur catalogue du 18″ pris en exemple), $\omega L_e$ vaut
4,3 Ω à 200 Hz, 10,8 Ω à 500 Hz et 21,6 Ω à 1 kHz — à 500 Hz la remontée inductive **commence
à peine**, et un ajustement de $L_e$ sur des données arrêtées là serait mal contraint (le repli
« courants de Foucault » de la phase 2 masquerait alors un simple manque de données). Le
passe-haut du filtre, lui, travaille sur $Z_{médium}$ dans toute sa bande passante : l'acte 3
(et un éventuel réseau de Zobel) a besoin de 1 à 2 kHz. Bonus : **10 Hz – 1 kHz font exactement
deux décades**, ce qu'exige la porte de validation de la feuille de route (§ 02.8).

**Grille logarithmique** $f_n = f_{min}\cdot 2^{n/N}$ : le comportement du dipôle est régulier
en $\log f$ et l'identification pondère également les octaves. Trois passes, **avec une
répartition des rôles explicite** :

| Passe | Pas | Points | Porté par | Rôle |
|---|---|---|---|---|
| 1 | 1/3 d'octave, 10 Hz–1 kHz | 21 | oscilloscope | repérer $f_{pic}$, $Z_{pic}$, $Q$ ; régler calibres et niveau |
| 2 | 1/12 d'octave, 10 Hz–1 kHz | 81 | **REW + carte son** | grille de référence, module et phase |
| 2′ | 15 à 25 points **choisis** | 20 | oscilloscope | budget d'incertitude complet, traçable |
| 3 | grille **linéaire** autour du pic, pas $\propto 1/Q$ | 15 | les deux | flancs raides du pic |

**Pourquoi resserrer autour du pic, et de combien.** L'affirmation v1 « la pente
$\mathrm{d}\ln|Z|/\mathrm{d}\ln f$ atteint ±1,7 » est fausse : sur un résonateur, la pente
maximale vaut approximativement le **facteur de qualité mécanique**. Recalculé sur le modèle
T-S : ±5,0 pour $Q_{ms} = 5$, ±7,0 pour $Q_{ms} = 7$, **±17** pour le 18″ de catalogue en caisse
close. Conséquence : la largeur à $Z_{pic}/\sqrt2$ vaut $\Delta f/f \approx 1/Q$, soit
0,082 octave pour $Q = 17$ — une grille au 1/24 d'octave n'y placerait que **2 points**, et
$|Z|$ varierait de moitié d'un point au suivant. Or c'est le pic qui porte toute l'information
sur $f_s$, $Q_{ms}$ et $Q_{es}$ pour l'acte 2. D'où la règle : **le pas de la passe 3 est fixé
par le $Q$ mesuré en passe 1**, de façon à placer au moins 15 points dans la largeur à
−3 dB élargie ×2 ; une grille **linéaire** est plus simple à piloter au GBF qu'une grille log
très fine. C'est aussi le meilleur argument pour confier le pic au balayage continu de REW.

**Budget de temps, honnête.** À 2–3 min par point (changer la fréquence, réajuster le niveau et
deux calibres, réarmer le moyennage, lire deux amplitudes et placer deux curseurs, recopier),
la grille complète de 80 points × 2 $R_{ref}$ × 2 dipôles représenterait **11 à 16 h de
paillasse** — impossible dans les créneaux de TP de septembre. Avec la répartition ci-dessus :
≈ 20 points à l'oscilloscope par dipôle, plus 3 points de linéarité et 5 répétitions du type A,
soit **environ 1 h par dipôle et par $R_{ref}$** — un créneau. La comparaison REW / oscilloscope
devient alors un vrai recoupement métrologique au lieu d'une redondance coûteuse.

**Divers.** Éviter 50 Hz et 100 Hz exacts (résidu secteur) : la grille 1/12 issue de 10 Hz tombe
à 50,4 et 100,8 Hz, ce qui convient.

#### La grille doit résoudre DEUX pics et UN creux

Le type de caisse n'est plus une inconnue : le sub est **bass-reflex à deux évents** (§ 01.10).
La grille n'a donc plus à résoudre un pic, mais trois accidents, **de largeurs très
différentes**. Mesuré sur le modèle du § 01.10 (script `br2.py` — modèle, pas mesure) :

```
accident            position   |Z|      largeur a facteur racine(2)   en octave   pts d'une grille 1/12   pente max |dln|Z|/dln f|
pic bas   f_L        16.3 Hz   54 ohm        1.8 Hz  [15.4 ; 17.2]      0.163           2.0                     9.2
creux     ~ f_b      34.2 Hz   6.1 ohm      30.7 Hz  [23.2 ; 53.9]      1.216          14.6                     1.0
pic haut  f_H        85.9 Hz   63 ohm        9.8 Hz  [81.1 ; 90.9]      0.164           2.0                     8.8
```

**Règle de densification, à appliquer telle quelle.** Les deux pics ont la même largeur
*relative* (0,16 octave, soit $\Delta f/f\approx1/Q$ avec $Q\approx9$) mais des largeurs
*absolues* dans un rapport 5. Une grille au 1/12 d'octave n'y place que **2 points**, et comme
la pente atteint $\lvert\mathrm{d}\ln\lvert Z\rvert/\mathrm{d}\ln f\rvert\approx9$, un pas de
1/12 d'octave (5,95 % en fréquence) fait varier $\lvert Z\rvert$ d'un facteur
$1{,}0595^{9}\approx1{,}7$ **d'un point au suivant** : c'est inexploitable pour l'ajustement.

1. **Passe 1** (1/3 d'octave, 10 Hz–1 kHz) : repérer les **trois** accidents, pas un seul.
   Le critère d'aiguillage du § 03.7 se lit dès cette passe.
2. **Passes 3a et 3c — les deux pics** : grille **linéaire**, pas $\le \Delta f_{\sqrt2}/10$,
   soit **$\le 0{,}2$ Hz autour de $f_L$** et **$\le 1$ Hz autour de $f_H$**, sur $\pm2$ largeurs
   de part et d'autre. Formulation générale, indépendante du jeu de paramètres :
   $$\delta f \le \frac{f_{pic}}{10\,Q_{pic}},\qquad Q_{pic}\ \text{lu en passe 1 par}\ Q=\frac{f_{pic}}{\Delta f_{\sqrt2}} .$$
   C'est **la même règle qu'en caisse close** (§ 01.9), appliquée deux fois.
3. **Passe 3b — le creux** : c'est le cas *inverse*, et c'est un piège. Le creux est **plat** :
   $|Z|$ ne remonte de 1 % qu'à $\pm2{,}6$ Hz du minimum ($[31{,}76\,;36{,}94]$ Hz, soit
   5,2 Hz — **0,22 octave** — de bande à 1 %). Densifier ne sert donc **pas** à le résoudre — il l'est déjà par la
   grille au 1/12 — mais à **localiser son minimum** malgré le bruit. Avec 1 % de bruit sur
   $|Z|$, l'argmin est indiscernable sur toute cette bande de 5 Hz. **Conséquence de méthode** :
   on ne lit pas $f_b$ sur l'argmin. On le lit sur le **passage par zéro de la phase** entre les
   deux pics, dont la pente est raide (**0,93° par pour-cent de fréquence** sur le modèle), ou
   mieux, on le prend de l'**ajustement** (§ 03). Sur le modèle, l'argmin tombe à 34,2 Hz et le
   zéro de phase à 33,5 Hz pour $f_b=35$ Hz vrai : **les deux sont biaisés de quelques pour-cent
   par les pertes** — à savoir avant de comparer à la prédiction géométrique du § 01.10 bis.
4. **Choix de $R_{ref}$ à refaire.** La dynamique n'est plus celle du cas clos : $|Z|$ va de
   **6,1 Ω au creux à 64 Ω au pic haut** (rapport 10,5) sur le modèle, alors que le cas clos
   donnait un pic unique bien plus haut. Le compromis du § 02.4 doit être rejoué sur cette
   dynamique-là, et il est possible qu'un seul $R_{ref}$ suffise désormais — à trancher sur les
   valeurs réelles [[à mesurer]].

#### Borne basse du balayage : règle de sécurité

**La borne basse n'est pas la même pour la mesure d'impédance et pour les mesures acoustiques,
et confondre les deux peut détruire le haut-parleur.**

En bass-reflex, l'évent **décharge** la membrane sous $f_b$ : le ressort d'air ne la retient plus,
l'excursion croît vite et rien ne l'arrête. Sur le modèle électro-mécano-acoustique complet
(script `br3.py` ; $M_{ms}=149$ g, $Bl=25{,}8$ T·m, $S_d=1210$ cm², $f_b=35$ Hz, $Q_l=7$ —
**MODÈLE, pas une mesure**), le déplacement crête par volt vaut :

```
  f = 100 Hz : 0.050 mm/V     f = 35 Hz (= fb) : 0.146 mm/V  (reference)
  f =  50 Hz : 0.104 mm/V     f = 25 Hz        : 0.199 mm/V   (x1.36)
  f =  40 Hz : 0.129 mm/V     f = 17.5 Hz      : 0.267 mm/V   (x1.83)
                              f = 10 Hz        : 0.383 mm/V   (x2.34)

sous V = 0.15 V (mesure d'impedance) : x(10 Hz) = 0.057 mm   -- sans objet
sous V = 8.94 V (10 W dans 8 ohm)    : x(10 Hz) = 3.42 mm
sous V = 52.9 V (350 W dans 8 ohm)   : x(10 Hz) = 20.3 mm    -- au-dela de tout X_max de 18"
```

**Règle gelée.**

- **Mesure d'impédance (§ 02.5, 100–200 mV aux bornes)** : le balayage **descend librement à
  10 Hz**, et il le doit — le pic bas $f_L$ est à 16 Hz et l'initialisation de $Q$ exige une
  octave sous le pic (§ 03.3). À 150 mV l'excursion prédite à 10 Hz est de 57 µm : trois ordres
  de grandeur sous $X_{max}$. **Il n'y a aucun risque, et il ne faut pas s'interdire cette
  zone** — c'est elle qui porte $f_L$, donc $\alpha$.
- **Toute mesure au niveau fort** (les deux niveaux d'écoute gelés, mesures acoustiques du
  § 07, rodage, essais d'écoute) : **interdiction de balayer sous $f_b$**. Borne basse
  $f_{min}=f_b$, et $1{,}2\,f_b$ si l'on veut une marge sur l'incertitude de $f_b$ lui-même.
  Sous cette borne, soit on n'excite pas, soit on insère un **passe-haut de protection
  (« subsonique ») du 2ᵉ ordre accordé à $f_b$** — c'est ce que fait tout système de sono, et
  c'est une remarque à faire au jury plutôt qu'à subir.
- **Aucun balayage lent au niveau fort tant que $f_b$ n'est pas connu.** L'ordre des phases le
  garantit déjà : l'impédance (petit signal) vient **avant** l'acoustique (fort signal), et c'est
  elle qui donne $f_b$. La prédiction géométrique du § 01.10 bis, faite encore avant, fournit une
  borne basse provisoire dès le premier jour.
- **Contrôle visuel obligatoire** avant tout balayage au niveau fort : membrane à l'arrêt,
  offset DC du GBF/de la carte son vérifié à zéro (un continu décentre la membrane et ajoute son
  excursion à celle du signal), et un doigt léger sur le saladier pour sentir une excursion
  anormale. [[$X_{max}$ du 18″ à lire sur la datasheet — la règle ci-dessus est qualitative tant
  qu'on ne l'a pas]]

#### Le bloc médiums se mesure TEL QU'IL EST CÂBLÉ, pavillons compris

L'enceinte comporte, outre le 18″ et les deux médiums, **deux haut-parleurs d'ultra-aigu
(pavillons) câblés en parallèle des médiums** (constat de l'étudiant, 16 sept. 2026). Il faut
distinguer deux plans, et ne pas les confondre :

- **Acoustiquement**, les pavillons sont **hors périmètre** : ils travaillent des kilohertz
  au-dessus du raccord à 100 Hz, ils ne participent pas à la somme des deux voies dans la bande
  40–250 Hz, et le TIPE n'en parle pas.
- **Électriquement**, ils sont **dans la charge** : étant en parallèle des médiums, ils font
  partie du dipôle que le passe-haut voit. Un filtre calculé sur le bloc médiums *seul* serait
  calculé sur une charge qui n'existe pas.

**Conséquence de protocole, non négociable : on mesure $\underline{Z}(f)$ du bloc
médium+pavillons tel qu'il est câblé, sans rien débrancher.** C'est cette impédance-là, et
elle seule, qui entre dans l'acte 3. Ce n'est pas une approximation, c'est la définition de la
charge.

**Question ouverte, à trancher par l'observation et non par hypothèse : y a-t-il un
condensateur en série avec les pavillons ?** [[à vérifier auprès de l'étudiant / en ouvrant le
bornier]] C'est la protection classique du premier ordre. Les deux cas ont des conséquences
opposées — et c'est pour cela qu'il faut regarder :

| | avec condensateur (3,3 à 10 µF **par pavillon**) | sans condensateur |
|---|---|---|
| $\lvert Z_{aigu}\rvert$ à 100 Hz, **les DEUX pavillons en parallèle** | **80 à 241 Ω** (241 Ω pour 3,3 µF, 117 Ω pour 6,8 µF, 80 Ω pour 10 µF) | **4 Ω** (deux 8 Ω en parallèle) |
| effet sur $\lvert Z\rvert$ du bloc médiums à 100 Hz | 29,3 Ω → 26,3 à 21,8 Ω, soit **$-0{,}9$ à $-2{,}6$ dB** ($-10$ à $-26$ %) : **pas négligeable** | 29,3 Ω → **3,7 Ω**, soit **$-17{,}9$ dB** ($-87$ %) : sous le minimum de 4 Ω du E-800 |
| risque matériel pendant les balayages | faible : les pavillons ne reçoivent presque rien à 100 Hz | **réel** : les pavillons reçoivent le 100 Hz à pleine puissance, hors de leur bande, avec une excursion que leur suspension n'encaisse pas |

*(Chiffres **recalculés le 16 sept. 2026** avec `modele_hp.effet_branche_aigu` sur le jeu
`MED_TYP` — deux 8″ de 4 Ω en série, $R_e=6{,}0$ Ω, $f_s=80$ Hz, d'où
$\lvert Z\rvert(100\ \text{Hz})=29{,}3$ Ω — et **$n_{aigu}=2$** pavillons résistifs de 8 Ω.
Ordres de grandeur, pas des mesures.)*

**Pourquoi « négligeable » était faux, et à quelle condition il redevient vrai.** Une version
antérieure de ce tableau calculait **un seul** pavillon et le confrontait au bloc illustratif du
§ 04.2 ($\lvert Z\rvert=12{,}2$ Ω à 100 Hz) : deux erreurs qui allaient dans le même sens et
donnaient « $-0{,}15$ à $-0{,}47$ dB, négligeable ». Deux pavillons en parallèle **divisent par
deux** l'impédance de la branche aiguë, et le bloc médiums vaut 29 Ω — et non 12 — au voisinage
de sa propre résonance, donc la branche pèse bien plus lourd relativement. L'énoncé correct est
**conditionnel** : *négligeable devant un bloc à 12 Ω, pas devant un bloc à 29 Ω au voisinage de
sa résonance.* Le mot « négligeable » sans cette condition est indéfendable. Les trois documents
qui chiffrent cet enjeu (`analyse/modele_hp.py`, `PARCOURS.md`, cette section) sont depuis alignés
sur le **seul** jeu `MED_TYP` et sur $n_{aigu}=2$ ; c'est `effet_branche_aigu` qui fait foi.

**La conséquence pratique est la même dans les deux cas** : on mesure le bloc tel qu'il est
câblé. Ce qui change, c'est (i) ce qu'on **s'attend** à lire — un bloc à ~25 Ω ou à ~4 Ω vers
100 Hz — donc le choix de $R_{ref}$ ; et (ii) s'il faut **limiter la durée et le niveau** des
balayages au fort niveau pour ne pas maltraiter les pavillons. La mesure d'impédance, elle,
se fait à 150 mV : elle ne présente de risque dans aucun des deux cas. Si l'inspection révèle
qu'il n'y a pas de condensateur, c'est en outre un **résultat de conception à commenter** : le
passe-haut du raccord ne protège pas les pavillons, puisqu'il les laisse passer avec les
médiums.

### <a id="s02-7"></a>02.7 Propagation des incertitudes

Incertitudes-types ($k = 1$), sommation quadratique des contributions indépendantes (GUM).
**Le résultat final est déclaré élargi, $U = k\,u$ avec $k = 2$** (niveau de confiance ≈ 95 %),
comme le veut le GUM ; les critères du § 02.8 sont exprimés de façon cohérente avec ce choix.

**La formule produit/quotient naïve est fausse ici.** Écrire
$u(|Z|)/|Z| = \sqrt{(u_R/R)^2 + (u_{V_d}/V_d)^2 + (u_{V_R}/V_R)^2}$ suppose $V_d$ et $V_R$
**indépendantes** ; or le § 02.2 montre qu'en configuration A ou B l'une des deux vient d'une
soustraction, donc est **corrélée** à l'autre. Avec les grandeurs réellement lues
($V_d$ et $V_{tot}$ en configuration A, $Z = R_{ref}V_d/(V_{tot}-V_d)$), les dérivées
logarithmiques sont $\partial\ln Z/\partial V_d = 1/V_d + 1/V_R$ et
$\partial\ln Z/\partial V_{tot} = -1/V_R$, d'où, pour des erreurs relatives $\varepsilon$
égales sur les deux lectures et $\underline{Z}$ réelle :

$$\frac{u(|Z|)}{|Z|} = \sqrt{\left(\frac{u(R_{ref})}{R_{ref}}\right)^2
+ 2\left(1 + \frac{|Z|}{R_{ref}}\right)^2\varepsilon^2}
\qquad\text{(config. B : remplacer } |Z|/R_{ref} \text{ par } R_{ref}/|Z| \text{)}$$

En **configuration C**, les deux tensions sont lues indépendamment et le facteur disparaît :
$u(|Z|)/|Z| = \sqrt{(u_R/R)^2 + 2\varepsilon^2}$, constant sur toute la bande.

**De quoi est fait $\varepsilon$.** Sources, avec en référence un oscilloscope pédagogique
courant (Rigol DS1054Z : CAN 8 bits, précision de gain DC **±3 % de la pleine échelle** pour
les calibres ≥ 10 mV/div, ±4 % en dessous, base de temps ±25 ppm) [[reporter les
spécifications de l'oscilloscope du lycée]] :

| Source | Valeur | Remède / commentaire |
|---|---|---|
| Tolérance $R_{ref}$ | 1 % (0,5 % ou mieux si mesurée) | mesurer au multimètre, REL / 4 fils |
| Gain vertical, **% de la pleine échelle** | 3 % de la lecture à 8 div ; 4 % à 6 div ; 6 % à 4 div ; **12 % à 2 div** (calculé) | remplir l'écran (≥ 6 div) ; **s'élimine dans le rapport** si les voies sont appariées |
| Désappariement résiduel après correction par $\kappa$ | ≈ 1 % [ordre de grandeur, à remplacer par le type A] | $\kappa$ par **couple de calibres** (§ 02.2) |
| Quantification 8 bits | $u = q/\sqrt{12}$ avec $q = $ calibre × 8/256 : **0,11 % à 8 div, 0,15 % à 6 div, 0,23 % à 4 div, 0,45 % à 2 div** (calculé, loi rectangulaire GUM) | remplir l'écran ; moyennage |
| Répétabilité de lecture (bruit, pointé) | ≈ 1 % [**type A** : 5 lectures répétées → écart-type expérimental] | moyennage, cordons coaxiaux courts |
| **Fréquence** | $u(f)/f \sim 10^{-5}$ avec le fréquencemètre 6 chiffres → contribution = pente × $u(f)/f$, négligeable. Avec seulement 0,1 Hz : 1,0 % à 10 Hz et **4,3 % sur $\lvert Z\rvert$ à 40 Hz si $Q = 17$** (calculé) | **enregistrer $f$ avec toute la résolution** |
| Tension issue de la soustraction | facteur $c_A$ ou $c_B$, ×1,5 à ×26 (§ 02.2) | règle « le petit à la masse », ou config. C |
| Pointé de $\Delta t$ | 20–50 µs typiques → 0,7–1,8° à 100 Hz, 4–9° à 500 Hz (calculé) | base de temps resserrée, moyennage, type A |
| Distorsion / bruit dans la valeur RMS | biais **systématique**, non aléatoire (§ 02.5) | crête-à-crête sur une période, moyennage |

Somme quadratique des trois composantes de lecture (désappariement 1 %, quantification 0,15 %
à 6 div, répétabilité 1 %) : **$\varepsilon \approx 1{,}4\ \%$ par voie** (calculé). C'est
l'objectif ; la valeur définitive doit venir du **type A mesuré**, pas de ce tableau.

Fonction de dépouillement, exécutée (valeurs de lecture **illustratives**, pas une mesure) :

```python
import numpy as np

def point_z_configA(Rref, u_Rref, Vd, u_Vd, Vtot, u_Vtot, theta_deg, u_theta_deg,
                    N=200_000, seed=0):
    """Configuration A : on lit DIRECTEMENT V_d (bornes du dipole) et V_tot (chaud du GBF),
    et theta = arg(V_d) - arg(V_tot) par decalage temporel (V_tot = reference de phase).
    V_R = V_tot - V_d est une SOUSTRACTION DE PHASEURS : V_d et V_R sont correlees, la formule
    produit/quotient appliquee au couple (V_d, V_R) est donc FAUSSE. Propagation Monte-Carlo.
    Convention : theta > 0 si v_d est en avance sur v_tot. Sortie : |Z|, u(|Z|), phi, u(phi) en deg."""
    rng = np.random.default_rng(seed)
    R  = rng.normal(Rref, u_Rref, N)
    A  = rng.normal(Vd,   u_Vd,   N)
    T  = rng.normal(Vtot, u_Vtot, N)
    th = np.radians(rng.normal(theta_deg, u_theta_deg, N))
    Zc = R*(A*np.exp(1j*th))/(T - A*np.exp(1j*th))
    Vd0 = Vd*np.exp(1j*np.radians(theta_deg))
    Zc0 = Rref*Vd0/(Vtot - Vd0)                       # valeur centrale, sans tirage
    return abs(Zc0), np.abs(Zc).std(), np.degrees(np.angle(Zc0)), np.degrees(np.angle(Zc)).std()

def u_rel_close(Rref, Zmod, eps, u_rel_Rref=0.01):
    """Forme close pour Z reelle : dlnZ/dV_d = 1/V_d + 1/V_R et dlnZ/dV_tot = -1/V_R
    donnent u(|Z|)/|Z| = sqrt( (u_R/R)^2 + 2 (1+|Z|/Rref)^2 eps^2 )."""
    return np.sqrt(u_rel_Rref**2 + 2*(1 + Zmod/Rref)**2*eps**2)

# --- Point ILLUSTRATIF (lectures plausibles, PAS une mesure sur l'enceinte)
Rref, u_Rref, eps = 100.0, 1.0, 0.014      # 100 ohm +/- 1 % ; 1,4 % par voie apres appariement
Ztest = 14.1*np.exp(-1j*np.radians(47.5))  # dipole d'essai (modele illustratif v1 a 100 Hz)
Vtot  = 2.000                              # V RMS lus sur CH2
Vd_c  = Vtot*Ztest/(Rref+Ztest)            # ce que lirait CH1
Vd, theta = abs(Vd_c), np.degrees(np.angle(Vd_c))
print(f"lectures simulees : Vd = {Vd:.4f} V, Vtot = {Vtot:.3f} V, theta = {theta:+.2f} deg")
Z, uZ, phi, uphi = point_z_configA(Rref, u_Rref, Vd, eps*Vd, Vtot, eps*Vtot, theta, 1.5)
print(f"|Z| = {Z:.2f} +/- {uZ:.2f} ohm ({100*uZ/Z:.1f} %) ; phi = {phi:+.1f} +/- {uphi:.1f} deg")
print(f"  forme close (Z reelle de meme module)      : {100*u_rel_close(Rref, abs(Ztest), eps):.1f} %")
print(f"  formule NAIVE (V_d et V_R independantes)   : {100*np.sqrt(0.01**2+2*eps**2):.1f} %  <- optimiste")

# --- Le meme point au sommet du pic, ou |Z| > Rref
for Zpic in (50.0, 120.0):
    Vd_c = Vtot*Zpic/(Rref+Zpic)
    Z, uZ, phi, uphi = point_z_configA(Rref, u_Rref, abs(Vd_c), eps*abs(Vd_c), Vtot, eps*Vtot, 0.0, 1.5, seed=1)
    print(f"pic |Z| = {Zpic:5.0f} ohm : {Z:6.1f} +/- {uZ:4.1f} ohm ({100*uZ/Z:.1f} %) ; "
          f"forme close {100*u_rel_close(Rref, Zpic, eps):.1f} %")

# --- Table de synthese : u(|Z|)/|Z| en % (k = 1), config A, Rref = 100 ohm
print("\n u(|Z|)/|Z| en % (k=1), config A, Rref = 100 ohm, u(Rref)/Rref = 1 %")
print(" eps/voie |  |Z| = 5     8    20    50   120   172 ohm")
for e in (0.020, 0.014, 0.010):
    print(f"   {100*e:4.1f} %  |     " + "  ".join(f"{100*u_rel_close(100,z,e):4.1f}" for z in (5,8,20,50,120,172)))
print(" config C (2 lectures directes, aucune soustraction) : "
      + ", ".join(f"{100*e:.1f} % -> {100*np.sqrt(0.01**2+2*e**2):.2f} %" for e in (0.020,0.014,0.010)) + " a tout |Z|")
```

Sortie :

```
lectures simulees : Vd = 0.2563 V, Vtot = 2.000 V, theta = -42.08 deg
|Z| = 14.10 +/- 0.34 ohm (2.4 %) ; phi = -47.5 +/- 1.6 deg
  forme close (Z reelle de meme module)      : 2.5 %
  formule NAIVE (V_d et V_R independantes)   : 2.2 %  <- optimiste
pic |Z| =    50 ohm :   50.0 +/-  1.6 ohm (3.1 %) ; forme close 3.1 %
pic |Z| =   120 ohm :  120.0 +/-  5.4 ohm (4.5 %) ; forme close 4.5 %

 u(|Z|)/|Z| en % (k=1), config A, Rref = 100 ohm, u(Rref)/Rref = 1 %
 eps/voie |  |Z| = 5     8    20    50   120   172 ohm
    2.0 %  |      3.1   3.2   3.5   4.4   6.3   7.8
    1.4 %  |      2.3   2.4   2.6   3.1   4.5   5.5
    1.0 %  |      1.8   1.8   2.0   2.3   3.3   4.0
 config C (2 lectures directes, aucune soustraction) : 2.0 % -> 3.00 %, 1.4 % -> 2.22 %, 1.0 % -> 1.73 % a tout |Z|
```

Le Monte-Carlo et la forme close coïncident (à 0,1 % près), ce qui valide la propagation ; ils
reposent tous deux sur le **bon** modèle statistique, celui des grandeurs réellement lues.
La méthode donne aussi $u(\varphi)$ **à travers la soustraction** : ici 1,6° pour un pointé de
1,5° sur $\theta$.

**Conclusion honnête, à graver avant les mesures.** Le plancher de la méthode est
$\sqrt{u_R^2 + 2\varepsilon^2}$, soit **3,0 % pour $\varepsilon = 2\ \%$** et 2,2 % pour
$\varepsilon = 1{,}4\ \%$ : **±3 % à $k = 1$ n'est pas atteignable partout**. Avec
$\varepsilon = 2\ \%$ il faudrait descendre à $\varepsilon \le 1{,}85\ \%$ pour tenir 3 % sur le
plateau, ≤ 1,33 % à un pic de 50 Ω et ≤ 0,74 % à un pic de 172 Ω (calculé). Formulation
retenue : **±3 % est tenu sur le plateau si l'écart de gain résiduel après appariement descend
sous ~1,5 % par voie ; au pic l'incertitude est de 3 à 6 % selon sa hauteur.** D'où la
reformulation des critères au § 02.8.

### <a id="s02-8"></a>02.8 Étalonnage sur composants connus et porte de validation

**Forme des critères.** Un critère « ±3 % » comparé à une incertitude-type de 3 % est
statistiquement absurde : $P(|\text{écart}| \le 1\sigma) = 0{,}683$, donc sur 80 points on
attendrait **25 points hors critère par pur hasard** sur une chaîne parfaitement saine
(calculé ; 3,6 points seulement avec $k = 2$). Tous les critères sont donc énoncés en
**écart normalisé**

$$E_n = \frac{|x_{mesuré} - x_{référence}|}{\sqrt{u_{mesuré}^2 + u_{référence}^2}} \le 2
\qquad (\text{soit } \pm 2u,\ k = 2)$$

**doublé d'un critère global sur le biais**, qui teste les composantes systématiques (valeur de
$R_{ref}$, appariement, câblage) et bénéficie du moyennage sur tous les points. C'est le critère
de biais qui porte le « ±3 % » de la feuille de route.

Ordre imposé, avant tout haut-parleur :

0. **Offset et appariement.** Entrées court-circuitées : vérifier la position zéro de chaque
   voie à chaque calibre utilisé (un offset propre fausse une amplitude à petit calibre).
   Puis même signal sur CH1 et CH2 (té BNC) à chaque **couple de calibres** ; noter
   $\kappa = V_{CH1}/V_{CH2}$ (attendu 1,00 ± 0,01) et chaîner les calibres (§ 02.2).
1. **Résistance de puissance** (8 ou 10 Ω, la tolérance nominale importe peu) : mesurer sa
   valeur DC $R_{DC}$ au multimètre avec REL (les cordons font ~0,2 Ω, soit 2,5 % de 8 Ω,
   calculé). Attendu : $|Z| = R_{DC}$ **plat**, $\varphi = 0$.
   **Critères** : (a) $E_n \le 2$ sur chaque point ; (b) **biais moyen $|\langle |Z|/R_{DC}\rangle - 1| \le 3\ \%$** ;
   (c) $|\varphi| \le 2°$ ; (d) aucune dérive systématique de $|Z|/R_{DC}$ avec $f$.
2. **Condensateur, sur DEUX DÉCADES EXACTES (10 Hz – 1 kHz)** — c'est l'exigence de la feuille
   de route, et elle ne coûte rien puisque l'étalonnage d'un condensateur n'a aucune raison
   d'être borné à la bande du haut-parleur. **Deux valeurs pour rester bien conditionné** avec
   un seul $R_{ref} = 100\ \Omega$ et une seule configuration : **100 µF sur 10–100 Hz** puis
   **10 µF (film MKP) sur 100 Hz – 1 kHz** — dans les deux cas $|Z|$ balaie 159 → 15,9 Ω,
   donc $c_A$ va de 3,67 à 1,64 (calculé). Attendu : pente **−1** en log-log,
   $\varphi = -90°$.
   **Critères** : (a) $E_n \le 2$ sur $C_{déduit} = 1/(2\pi f |Z|)$ par rapport à la moyenne ;
   (b) dispersion relative de $C_{déduit}$ sur chaque décade **≤ 5 %** ; (c) pente log-log de
   $|Z|$ dans $-1{,}00 \pm 0{,}03$ ; (d) valeur absolue compatible avec le capacimètre du
   multimètre [[précision à vérifier]] ou la tolérance nominale (±10–20 %). Un électrolytique
   a une ESR : 0,3 Ω sur 150 µF décale la phase de 1,6° à 100 Hz et **8° à 500 Hz** (calculé) —
   ce n'est pas un défaut de la chaîne mais une propriété du composant, que l'on ajuste avec un
   modèle $ESR + 1/(j\omega C)$ ; cette ESR compte dans les pertes du filtre (acte 3).
3. **Petite self** (la 18 mH du filtre catalogue) : attendu
   $|Z| = \sqrt{r^2 + (2\pi f L)^2}$, $\varphi = \arctan(2\pi f L/r)$. Pour 18 mH et
   $r = 1\ \Omega$ (ordre de grandeur) : 1,51 Ω / +48,5° à 10 Hz, 11,35 Ω / +84,9° à 100 Hz,
   56,56 Ω / +89,0° à 500 Hz (calculé). Ce test **vérifie le signe de la phase** (inductif > 0)
   et fournit $L$ et $r$ par ajustement.
   **Point directement lié au sujet du TIPE** : le $r$ issu de l'ajustement est une résistance
   **alternative**, majorée par l'effet de peau, les pertes de proximité et les pertes fer,
   alors que la **DCR** qui entre dans la fonction de coût de l'acte 3 est la résistance
   continue. Mesurer les deux — $r_{DC}$ au multimètre en 4 fils et $r_{AC}(f)$ par ajustement
   sur plusieurs sous-bandes — et **commenter l'écart** : c'est un résultat, pas une anomalie.
   Recoupement de $L$ par la **résonance série** avec 150 µF : à
   $f_0 = 1/(2\pi\sqrt{LC}) = 96{,}9$ Hz, une self **en série** avec un condensateur présente un
   **MINIMUM d'impédance** $|Z| = r \approx 1\ \Omega$ (donc un maximum de courant, $\varphi$
   changeant de signe), **pas un pic** (calculé : minimum de 1,000 Ω à 96,86 Hz). Ne pas
   confondre ce creux avec le pic d'impédance du haut-parleur.
4. **Recoupement 10 Ω / 100 Ω** sur la résistance et le condensateur :
   $E_n = |Z_{100} - Z_{10}|/\sqrt{u_{100}^2 + u_{10}^2} \le 2$, calculé point par point et
   **tracé** en fonction de $f$ (un $E_n$ qui dérive avec $f$ signe un problème de bande
   passante ou de couplage, pas un aléa).
5. **Évaluation de type A** : refaire **5 fois** la lecture complète d'un même point (sur le
   plateau, et un second au pic), en re-réglant les curseurs à chaque fois ; l'écart-type
   expérimental donne la composante A de $\varepsilon$ et **remplace** le « ≈ 1 % » du tableau
   du § 02.7. Sans cette étape, le bilan d'incertitude n'a pas de composante A du tout.

**Stratégie si la porte de validation échoue** — à décider et geler **avant** les mesures,
comme le veut la feuille de route :

- Causes à diagnostiquer d'abord : pinces de masse (§ 02.2), signal sur trop peu de divisions,
  voies non appariées, sondes ×1/×10 différentes, valeur de $R_{ref}$ erronée, contact oxydé,
  couplage AC, offset de voie.
- **Critère dégradé acceptable, gelé** : biais moyen ≤ **5 %** au lieu de 3 % sur la résistance,
  et dispersion de $C_{déduit}$ ≤ 8 % par décade. Coût pour l'acte 2 : les incertitudes des
  paramètres T-S issues du fit pondéré par $1/u^2$ augmentent dans le même rapport (≈ ×1,7),
  ce qui reste compatible avec l'objectif « paramètres stables quand on retire aléatoirement
  des points ». **En dessous, on ne passe pas à l'acte 2 : on répare la chaîne.**

Script de grille et de valeurs attendues, exécuté :

```python
import numpy as np

def grille_log(fmin, fmax, n_par_octave):
    """Grille log de fmin a fmax INCLUS (log2(fmax/fmin) n'est pas entier : fmax est ajoute)."""
    n = int(np.ceil(n_par_octave*np.log2(fmax/fmin))) + 1
    f = fmin*2.0**(np.arange(n)/n_par_octave)
    return np.append(f[f < fmax], fmax)

def grille_pic(f_pic, Q, n_pts=15, elargissement=2.0):
    """Passe 3 : grille LINEAIRE centree sur le pic. Largeur relative a -3 dB d'un
    resonateur : Delta f/f = 1/Q. Le pas s'adapte donc au Q MESURE en passe 1."""
    demi = elargissement*f_pic/(2*Q)
    return np.linspace(f_pic - demi, f_pic + demi, n_pts)

g1 = grille_log(10, 1000, 3)          # passe 1 : exploration (1/3 d'octave)
g2 = grille_log(10, 1000, 12)         # passe 2 : grille de reference, portee par REW
print(f"passe 1 : {len(g1)} pts (10 -> {g1[-1]:.0f} Hz) ; passe 2 (REW) : {len(g2)} pts ; "
      f"1/3 d'octave 10 Hz - 2 kHz (mediums) : {len(grille_log(10,2000,3))} pts")
for f_pic, Q in ((40.0, 5.0), (45.0, 17.0)):      # [[a mesurer]] : f_pic et Q lus en passe 1
    g3 = grille_pic(f_pic, Q)
    print(f"  passe 3 : f_pic={f_pic:.0f} Hz, Q={Q:4.1f} -> largeur a -3 dB = {f_pic/Q:5.2f} Hz ; "
          f"15 pts de {g3[0]:.2f} a {g3[-1]:.2f} Hz (pas {g3[1]-g3[0]:.2f} Hz = {100*(g3[1]-g3[0])/f_pic:.2f} %)")
    print(f"     une grille au 1/24 d'octave (+2,93 %) n'y placerait que {np.log2(1+1/Q)*24:.1f} points")

print("\nHauteur du pic : Zpic = Re (1 + Qms/Qes)  [ordres de grandeur catalogue, [[a mesurer]]]")
for nom, Re, Qms, Qes in (("18\" pro, Qms/Qes = 10",  5.3,  3.30, 0.33),
                          ("18\" pro, Qms/Qes = 31",  5.3, 10.38, 0.33),
                          ("bloc mediums 2x4 serie",  6.4,  3.50, 0.50)):
    print(f"  {nom:24s} Re = {Re:4.1f} ohm -> Zpic = {Re*(1+Qms/Qes):5.0f} ohm, dynamique |Z|max/Re = {1+Qms/Qes:5.1f}")

print("\nEtalonnage condensateur : deux decades exactes (10 Hz - 1 kHz), deux valeurs")
for C, f1, f2 in ((100e-6, 10, 100), (10e-6, 100, 1000)):
    Z1, Z2 = 1/(2*np.pi*f1*C), 1/(2*np.pi*f2*C)
    print(f"  C = {C*1e6:5.0f} uF sur {f1:4d}-{f2:4d} Hz : |Z| = {Z1:7.2f} -> {Z2:6.2f} ohm ; "
          f"c_A = sqrt(2)(1+|Z|/100) = {np.sqrt(2)*(1+Z1/100):.2f} -> {np.sqrt(2)*(1+Z2/100):.2f}")
print("Etalonnage self 18 mH, r = 1 ohm :")
for f in (10, 100, 500):
    Z = 1 + 1j*2*np.pi*f*18e-3
    print(f"  f = {f:4d} Hz : |Z| = {abs(Z):6.2f} ohm, phi = {np.degrees(np.angle(Z)):+5.1f} deg")
f = np.linspace(50, 150, 200001)
Zs = np.abs(1 + 1j*2*np.pi*f*18e-3 + 1/(1j*2*np.pi*f*150e-6))
print(f"  18 mH EN SERIE avec 150 uF : f0 = {1/(2*np.pi*np.sqrt(18e-3*150e-6)):.2f} Hz ; le balayage donne un "
      f"MINIMUM |Z| = {Zs.min():.3f} ohm a {f[np.argmin(Zs)]:.2f} Hz (un creux, pas un pic)")

print("\nRemplissage de l'ecran (gain specifie en % de la PLEINE ECHELLE sur 8 divisions) :")
for nd in (8, 6, 4, 2):
    q = 100*(8/256)/nd
    print(f"  {nd} div : gain 3 % PE = {3*8/nd:5.1f} % de la lecture ; quantification q = {q:.3f} %, "
          f"u = q/sqrt(12) = {q/np.sqrt(12):.3f} %")
```

Sortie :

```
passe 1 : 21 pts (10 -> 1000 Hz) ; passe 2 (REW) : 81 pts ; 1/3 d'octave 10 Hz - 2 kHz (mediums) : 24 pts
  passe 3 : f_pic=40 Hz, Q= 5.0 -> largeur a -3 dB =  8.00 Hz ; 15 pts de 32.00 a 48.00 Hz (pas 1.14 Hz = 2.86 %)
     une grille au 1/24 d'octave (+2,93 %) n'y placerait que 6.3 points
  passe 3 : f_pic=45 Hz, Q=17.0 -> largeur a -3 dB =  2.65 Hz ; 15 pts de 42.35 a 47.65 Hz (pas 0.38 Hz = 0.84 %)
     une grille au 1/24 d'octave (+2,93 %) n'y placerait que 2.0 points

Hauteur du pic : Zpic = Re (1 + Qms/Qes)  [ordres de grandeur catalogue, [[a mesurer]]]
  18" pro, Qms/Qes = 10    Re =  5.3 ohm -> Zpic =    58 ohm, dynamique |Z|max/Re =  11.0
  18" pro, Qms/Qes = 31    Re =  5.3 ohm -> Zpic =   172 ohm, dynamique |Z|max/Re =  32.5
  bloc mediums 2x4 serie   Re =  6.4 ohm -> Zpic =    51 ohm, dynamique |Z|max/Re =   8.0

Etalonnage condensateur : deux decades exactes (10 Hz - 1 kHz), deux valeurs
  C =   100 uF sur   10- 100 Hz : |Z| =  159.15 ->  15.92 ohm ; c_A = sqrt(2)(1+|Z|/100) = 3.67 -> 1.64
  C =    10 uF sur  100-1000 Hz : |Z| =  159.15 ->  15.92 ohm ; c_A = sqrt(2)(1+|Z|/100) = 3.67 -> 1.64
Etalonnage self 18 mH, r = 1 ohm :
  f =   10 Hz : |Z| =   1.51 ohm, phi = +48.5 deg
  f =  100 Hz : |Z| =  11.35 ohm, phi = +84.9 deg
  f =  500 Hz : |Z| =  56.56 ohm, phi = +89.0 deg
  18 mH EN SERIE avec 150 uF : f0 = 96.86 Hz ; le balayage donne un MINIMUM |Z| = 1.000 ohm a 96.86 Hz (un creux, pas un pic)

Remplissage de l'ecran (gain specifie en % de la PLEINE ECHELLE sur 8 divisions) :
  8 div : gain 3 % PE =   3.0 % de la lecture ; quantification q = 0.391 %, u = q/sqrt(12) = 0.113 %
  6 div : gain 3 % PE =   4.0 % de la lecture ; quantification q = 0.521 %, u = q/sqrt(12) = 0.150 %
  4 div : gain 3 % PE =   6.0 % de la lecture ; quantification q = 0.781 %, u = q/sqrt(12) = 0.226 %
  2 div : gain 3 % PE =  12.0 % de la lecture ; quantification q = 1.562 %, u = q/sqrt(12) = 0.451 %
```

### <a id="s02-9"></a>02.9 Variante rapide : carte son + REW, et jig derrière l'amplificateur

**Principe** (documentation REW, page *Impedance Measurement*) : la sortie de la carte son
attaque la charge à travers une résistance de détection $R_{sense}$ ; une entrée (gauche)
mesure la tension de sortie, l'autre (droite) la tension aux bornes de la charge ; REW calcule
$Z = R_{sense}\,V_{droite}/(V_{gauche} - V_{droite})$ — exactement la configuration A du
§ 02.2, la soustraction étant faite par le logiciel. Le balayage sinusoïdal logarithmique
fournit module et phase en quelques secondes, avec un export texte (f, |Z|, φ) directement
exploitable par le code d'identification.

**Réglages et calibration REW** : valeur exacte de $R_{sense}$ saisie ; *Open circuit cal*
(fils déconnectés : compense l'écart de gain entre voies — l'équivalent de notre appariement),
*Short circuit cal* (compense l'impédance série des cordons), *Reference cal* sur une
résistance connue non inductive ≤ 100 Ω. Niveau ≤ −3 dBFS (plafond), 256 k échantillons,
moyennage synchrone, filtre de bruit.

**Valeur de $R_{sense}$ selon la source** (REW) : 100 Ω sur une sortie casque ; 1 kΩ sur une
sortie ligne (résultats plus bruités, car une sortie ligne ne débite pas dans 100 Ω) ;
≤ 33 Ω derrière un amplificateur de puissance.

**Mesurer l'impédance de sortie réelle de la carte son** (cinq minutes, et cela tranche entre
100 Ω et 1 kΩ) : relever la tension de sortie à vide $V_0$, puis sur une charge connue
$R_c = 100\ \Omega$ ; alors $Z_s = R_c\,(V_0/V_c - 1)$. [[à faire dès réception, modèle de carte
son à documenter.]]

**Jig derrière l'amplificateur E-800** — seule voie pour mesurer $Z(f)$ à niveau réaliste
(utile à l'acte 4 et à l'argument de dérive thermique). Dimensionnement proposé, à valider :

- $R_{sense} = 1\ \Omega$ non inductive, **10 à 25 W** : sous 20 V RMS aux bornes d'une charge
  de 8 Ω, $I = 2{,}5$ A, $V_{sense} = 2{,}5$ V et $P_{sense} = 6{,}2$ W (calculé). Ne jamais
  monter en pleine puissance : à 53 V RMS (350 W/8 Ω) il faudrait 44 W dans $R_{sense}$.
- **Deux diviseurs IDENTIQUES**, un par voie : $R_1 = 47\ \mathrm{k}\Omega$, $R_2 = 1\ \mathrm{k}\Omega$
  (rapport 1/48). Étant identiques, leur rapport **s'élimine dans $V_d/V_R$** : il n'a même pas
  besoin d'être connu, seulement apparié. Charge de 48 kΩ sur les nœuds mesurés : négligeable ;
  $P(R_1) = 0{,}06$ W même à pleine puissance ; sortie 1,10 V RMS pour 53 V d'entrée (calculé),
  compatible avec une entrée ligne.
- **Protection** : diodes Zener 5,1 V tête-bêche (ou TVS bidirectionnelle) **après** le diviseur,
  sur chaque entrée de carte son ; elles ne conduisent jamais en fonctionnement normal et
  clampent en cas d'erreur de câblage. [[à vérifier sur l'E-800 : sortie en pont ou masse
  commune ? Si pont, aucune borne n'est à la masse et le diviseur doit être flottant.]]

**Limites** : impédance de sortie et courant maximal de la carte son ; impédance d'entrée en
parallèle sur la charge (≥ 10 kΩ, négligeable sur 10–200 Ω) ; couplage capacitif des
entrées/sorties → atténuation et déphasage sous 10–20 Hz [[à vérifier]] ; **le bruit dominant
est acoustique et vibratoire** (la membrane fonctionne en microphone, § 02.10) ; un ordinateur
portable sur secteur peut créer une boucle de masse avec le GBF ou l'oscilloscope si les deux
chaînes sont branchées en même temps — ne pas les cumuler.

**Comment comparer les deux méthodes.** REW ne fournit **aucune incertitude** : la phrase « les
deux doivent coïncider dans les incertitudes » n'est pas décidable telle quelle. Procédure
retenue : répéter **5 balayages REW** (en débranchant et rebranchant le jig entre deux) →
$u_{REW}$ par écart-type expérimental (type A), auquel on ajoute quadratiquement la tolérance
de $R_{sense}$ ; puis comparer point à point sur la grille commune par
$E_n = |Z_{REW} - Z_{oscillo}|/\sqrt{u_{REW}^2 + u_{oscillo}^2} \le 2$, **tracé en fonction de
$f$**. Un $E_n$ qui explose systématiquement en bas de bande accuse le couplage capacitif de la
carte son ; un biais constant accuse $R_{sense}$ ou l'appariement ; un écart concentré au pic
accuse la différence de niveau d'excitation (§ 02.5).

### <a id="s02-10"></a>02.10 Pièges

- **Câbles et contacts** : une pince crocodile oxydée fait 10–100 mΩ, soit jusqu'à ~1 % de 8 Ω.
  Prendre $V_d$ **directement sur les bornes** du haut-parleur (esprit « 4 fils »), pas au bout
  du cordon ; bornier vissé ou soudure plutôt que pinces sur le trajet du courant.
- **Dipôle nu** : déconnecter le filtre existant (crossover actif ou passif) et l'ampli. Une
  sortie d'amplificateur **en fonctionnement** présente une impédance très faible qui
  court-circuiterait la mesure ; **hors tension**, le comportement dépend du modèle (relais de
  sortie ouvert, transistors bloqués, réseau de Zobel) et n'est pas garanti — on débranche
  systématiquement plutôt que de parier.
- **En caisse, pas en l'air** : le filtre passif voit l'impédance du haut-parleur **monté**.
  Caisse close : $F_c > F_s$ (raideur de l'air ajoutée), $Z_{pic}$ **inchangé** ; bass-reflex :
  deux pics et un minimum à $f_b$. Ce décalage par rapport à la datasheet n'est pas une erreur.
- **Autre haut-parleur dans le même volume** [[médiums en chambre séparée ?]] : un haut-parleur
  voisin en circuit ouvert ou court-circuité ne charge pas l'air de la même façon (freinage
  électrique). **Convention gelée : l'autre voie est TOUJOURS laissée en circuit ouvert**, et
  c'est écrit dans l'en-tête de chaque série. Sans convention figée, la comparaison des séries
  n'a pas de sens.
- **Dérive thermique** : +0,393 %/K sur $R_e$ ; $R_e$ DC avant/après, température notée.
- **Vibrations et bruit acoustique** : à faible niveau, la f.é.m. induite par le bruit ambiant
  s'ajoute à $V_d$, surtout près de $f_s$. Pièce silencieuse, portes fermées, ne pas toucher
  l'enceinte, moyennage.
- **Secteur** : 50 Hz et harmoniques visibles à petit niveau ; **cordons coaxiaux** plutôt que
  sondes ×1 à fil de masse volant, cordons courts et torsadés côté puissance, éviter les
  fréquences exactes 50/100/150 Hz, moyennage.
- **Oscilloscope** : couplage DC sur les deux voies, liaisons identiques, écran rempli, voies
  appariées par couple de calibres, déclenchement sur la voie forte, pinces de masse sur un
  seul nœud (§ 02.2).
- **Enceinte en position normale**, évent dégagé, rien posé sur la membrane.

### <a id="s02-11"></a>02.11 Protocole reproductible

0. **Test de la masse du GBF** : ohmmètre entre la borne froide du BNC et la terre du secteur.
   Continuité → configuration A/B. Isolement → **configuration C**, et la moitié des
   difficultés du § 02.2 disparaît.
1. Mesurer $R_{ref}$ (100 Ω, 10 Ω, éventuellement 33 Ω) au multimètre en REL ; noter valeurs et
   température.
2. Vérifier l'offset de voie (entrées court-circuitées) puis apparier CH1/CH2 par **couple de
   calibres** ; noter le tableau des $\kappa$.
3. Câbler la configuration retenue à l'étape 0 ; vérifier à l'ohmmètre que les pinces de masse
   sont sur un seul nœud ; liaisons ×1 identiques ou coaxiales, couplage DC, GBF offset nul,
   affichage High-Z vérifié.
4. **Étalonnage** : résistance (plat, φ = 0), condensateur sur deux décades (deux valeurs),
   self (+90°, $r_{DC}$ et $r_{AC}$) — critères § 02.8, **type A inclus**. Ne pas passer au
   haut-parleur avant validation.
5. Haut-parleur : filtre et ampli déconnectés, autre voie en circuit ouvert ; $R_e$ DC au
   multimètre ; **passe 1** (1/3 d'octave, 10 Hz–1 kHz) à $V_d \approx 150$ mV RMS réajustés à
   chaque point ; relever $f_{pic}$, $Z_{pic}$ et la largeur à −3 dB → $Q$.
6. **Choix définitif** de $R_{ref}$, de la configuration et du plan de calibres, à la lumière de
   $Z_{pic}$ (§ 02.4). **Contrôle de linéarité au pic** (×0,5 et ×2) **avant** d'aller plus loin.
7. Passe 2′ (15 à 25 points choisis : bas de bande, plateau, deux flancs, pic, 100 Hz, 300 Hz,
   500 Hz, 1 kHz) puis passe 3 (grille linéaire autour du ou des pics, pas $\propto 1/Q$).
   À chaque point : fréquence lue **avec toute sa résolution**, calibres, niveau GBF, $V_{CH1}$,
   $V_{CH2}$, $\Delta t$ **avec son signe**, moyennage actif, écran rempli.
8. **Type A** : 5 répétitions complètes d'un point de plateau et d'un point de pic.
9. Refaire le pic avec l'autre $R_{ref}$ (10 Ω, configuration B) ; refaire $R_e$ DC ; noter la
   température.
10. Dépouiller (`point_z_configA`) ; tracer $|Z|$ et $\varphi$ avec barres d'erreur ; **contrôles
    de cohérence** :
    - **En bas de bande, $|Z|$ DÉCROÎT vers $R_e$ sans l'atteindre.** Le contrôle v1
      « $|Z| \to R_e$ à 10 Hz » est faux et ferait diagnostiquer une panne inexistante : la
      branche motionnelle n'est pas éteinte une octave et demie sous la résonance. Calculé sur
      des jeux de paramètres plausibles, à 10 Hz on attend encore
      $|Z| \approx 1{,}1$ à $1{,}6 \times R_e$ avec $\varphi = +24°$ à $+50°$. Les vrais
      contrôles sont : (a) $|Z|(f_{min}) > R_{e,DC}$ ; (b) $|Z|$ et $\varphi$ décroissants vers
      $R_e$ et 0 quand $f$ baisse ; (c) $R_{e,DC}$ mesuré au multimètre **sous** toute la courbe ;
      (d) le $R_e$ issu de l'ajustement de l'acte 2 compatible avec $R_{e,DC}$ à mieux que
      l'incertitude combinée ($E_n \le 2$).
    - **$\varphi = 0$ au sommet du pic** : ce contrôle-là est valide. Vérifié sur le modèle T-S,
      le maximum de $|Z|$ et le passage $\varphi = 0$ coïncident exactement sans $L_e$, et à
      0,03 % près avec $L_e = 3{,}43$ mH (calculé).
    - Recoupement 10 Ω / 100 Ω par $E_n$ (§ 02.8).
11. Mesure REW + jig sur le même dipôle ; superposer ; $E_n(f)$ tracé et écarts commentés.
12. Même séquence pour le bloc médiums (les deux HP en série, tels que câblés), jusqu'à 2 kHz.
13. **Répétabilité inter-séances** : au début de chaque nouvelle séance, refaire **3 points de
    contrôle** (plateau, pic, haut de bande) et les comparer à la séance précédente par $E_n$.
    C'est ce qui permettra, en phase 4, d'affirmer honnêtement qu'un écart mesuré est un effet
    et non une dérive de la chaîne.
14. Archiver les relevés bruts (CSV) et les conditions.

### <a id="s02-12"></a>02.12 Tableau de relevé et contrat d'interface avec l'acte 2

**En-tête de série** : date · opérateur · dipôle (sub en caisse / bloc médiums / R étalon / C /
L) · **configuration (A, B ou C)** · $R_{ref}$ nominale et **mesurée** · **tableau des $\kappa$
par couple de calibres** · convention sur la voie voisine (circuit ouvert) · température ·
$R_e$ DC avant / après · oscilloscope (modèle, liaisons, couplage, moyennage) · GBF (modèle,
réglage High-Z/50 Ω).

| n° | $f$ lue (Hz) | $R_{ref}$ | conf. | niveau GBF (V) | cal. CH1 | div. CH1 | cal. CH2 | div. CH2 | $V_{CH1}$ (V) | $V_{CH2}$ (V) | $\Delta t$ (µs, signe) | remarques |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [[à mesurer]] | 100,3 | A | | | | | | | | | |
| … | | | | | | | | | | | | |

Colonnes ajoutées par rapport au brouillon v1, chacune indispensable : **$R_{ref}$ et
configuration** (on bascule entre deux étalons et deux câblages), **niveau GBF** (réajusté à
chaque point, § 02.5), et surtout **le nombre de divisions occupées par chaque voie** — c'est
la grandeur qui fixe l'incertitude de gain (3 % de pleine échelle → 3 à 12 % de la lecture).
Sans elle, l'incertitude n'est pas reconstructible a posteriori. Quelle lecture est directe et
laquelle vient d'une soustraction se déduit de la colonne « conf. ».

$|Z|$, $u(|Z|)$, $\varphi$, $u(\varphi)$ ne figurent **pas** dans le tableau de paillasse : ce
sont des grandeurs **calculées**, jamais saisies à la main ; les colonnes de lecture restent
brutes (traçabilité).

**Contrat d'interface avec l'acte 2** (à respecter par le squelette `analyse/` de la phase 0,
sinon la phase 2 recommencera le dépouillement) :

- **CSV dépouillé** : `f_Hz, Z_mod_ohm, u_Z_mod_ohm, phi_deg, u_phi_deg, Rref_ohm, config, methode, date`
  — une ligne par point, séparateur virgule, point décimal, encodage UTF-8.
- **Convention de signe de $\varphi$** : positif = inductif (§ 02.1). REW exporte avec la même
  convention [[à vérifier au premier export]].
- **Le fit de l'acte 2 est pondéré par $1/u^2$**, séparément sur le module et sur la phase : les
  colonnes d'incertitude ne sont pas décoratives, elles entrent dans le calcul. Les points de
  flanc de pic, mal conditionnés, y pèseront naturellement moins.
- Les fichiers **bruts** (le tableau ci-dessus) sont archivés à côté, sous le même nom.

### Ce qu'il faut retenir pour l'oral

- $\underline{Z} = R_{ref}\,\underline{V}_d/\underline{V}_R$ : un rapport de deux tensions sur le
  même courant, **exact quel que soit $R_{ref}$**. L'hypothèse « courant constant » avec 100 Ω
  fausserait le pic de 50 à 63 % (calculé), pas de 30 % : le pic d'un 18″ vaut
  $R_e(1+Q_{ms}/Q_{es})$, soit 60 à 200 Ω et non 40–60 Ω.
- La masse de l'oscilloscope impose un seul nœud de référence : une tension se lit, l'autre se
  déduit — sauf si la sortie du GBF est **flottante**, auquel cas on met le **nœud milieu** à la
  masse et les deux tensions se lisent directement. Trois minutes d'ohmmètre décident.
- Le prix de la soustraction est un facteur $\sqrt2\,(1+|Z|/R_{ref})$ sur l'incertitude : c'est
  lui, et non le conditionnement 8 bits, qui commande le choix de $R_{ref}$ et de la configuration.
- **±3 % sur $|Z|$ est un plancher, pas un acquis** : $\sqrt{u_R^2+2\varepsilon^2} = 3{,}0\ \%$
  pour 2 % par voie. Tenu sur le plateau avec voies appariées et écran rempli, 3 à 6 % au pic.
  Les critères sont donc écrits en écart normalisé $E_n \le 2$ plus un biais moyen ≤ 3 %.
- Le pic est **étroit** (largeur relative $1/Q$, $Q$ jusqu'à ~17) : la grille y est linéaire et
  son pas est fixé par le $Q$ mesuré, pas décidé à l'avance.
- Petits signaux à **tension aux bornes constante** (150 mV réajustés à chaque point), en caisse,
  dipôle nu, pièce silencieuse ; deux $R_{ref}$ et deux méthodes (oscilloscope / REW) recoupées
  par $E_n$.

### Sources

- Room EQ Wizard, aide en ligne, page « Impedance Measurement » (jig, résistance de détection,
  calibrations, niveaux « 100 mV to 200 mV at most », bruit) :
  https://www.roomeqwizard.com/help/help_en-GB/html/impedancemeasurement.html
  (consultée le 2026-09-02) ; page « Thiele Small Parameters » de la même aide.
- R. Elliott (Elliott Sound Products), « Measuring Loudspeaker Parameters » :
  https://sound-au.com/tsp.htm — méthode de la résistance série, mesure de $f_s$ et des $Q$
  au générateur ; référence libre, vérifiée en ligne le 2026-09-09, adaptée au niveau prépa.
- Rigol, *DS1000Z Series Specifications* (DS1054Z) : résolution 8 bits, « DC Gain Accuracy
  ≥ 10 mV : ±3 % full scale ; < 10 mV : ±4 % full scale », base de temps ±25 ppm :
  https://assets.testequity.com/te1/Documents/pdf/rigol/Rigol-DS1054Z-Specification.pdf
  (spécification prise comme oscilloscope pédagogique de référence ; celui du lycée
  [[à vérifier]]).
- JCGM 100:2008, *Évaluation des données de mesure — Guide pour l'expression de l'incertitude
  de mesure* (GUM) : incertitudes-types, propagation au premier ordre, types A et B,
  distribution rectangulaire ($u = q/\sqrt{12}$), incertitude élargie $U = k\,u$.
- Eminence, fiche technique **Delta Pro-18A** ($R_e = 5{,}3\ \Omega$, $F_s = 28$ Hz,
  $Q_{ms} = 10{,}38$, $Q_{es} = 0{,}33$, $Q_{ts} = 0{,}32$, $L_e = 3{,}43$ mH,
  $V_{as} = 493$ L) : utilisée **uniquement** comme jeu de paramètres catalogue plausible pour
  un 18″ 8 Ω de sonorisation, pas comme description du haut-parleur du projet
  [[paramètres du HP réel à confirmer]].
- Coefficient de température du cuivre recuit, $\alpha = 3{,}93\cdot10^{-3}\ \mathrm{K^{-1}}$ à
  20 °C : valeur tabulée usuelle (tables de physique / norme IEC 60287) [[référence exacte à
  citer]].
- V. Dickason, *The Loudspeaker Design Cookbook* : mesure d'impédance par résistance série,
  paramètres de Thiele-Small [[édition et chapitre à préciser — référence payante, citée pour
  mémoire ; les deux sources libres ci-dessus la remplacent pour le lecteur]].
- Programme de physique PTSI/PT : régime sinusoïdal forcé, impédance complexe, propagation des
  incertitudes (cours N. Cavallo).
- Vérifications numériques : `scratchpad/sec02f/verif_a.py`, `verif_b.py`, `verif_c.py`,
  `final1.py`, `final2.py` (numpy seul — ces scripts n'ont besoin que de numpy ; Python 3.13,
  Windows), exécutées le 2026-09-09. Environnement du poste vérifié le 2026-09-13 : Python
  3.13.2, numpy 2.4.6, scipy 1.18.1, matplotlib 3.11.0 installés et fonctionnels.

<!-- NOTES DE RÉDACTION — arbitrages entre les deux vérificateurs (ne pas publier) -->
<!-- Pente du pic : le vérificateur « rigueur » n'a pas contesté le ±1,7 de la v1 ; recalcul
     indépendant (verif_a.py) confirme le vérificateur « terrain » : la pente max vaut ≈ Q
     (5,0 / 7,0 / 16,7 sur trois jeux). Le ±1,7 est supprimé, et les contributions de u(f)
     qui en découlaient sont recalculées avec la pente = Q. -->
<!-- Étalon du condensateur : proposition « changer de Rref selon la bande (1 kΩ sous 30 Hz) »
     non retenue — changer de Rref en cours de série casse la traçabilité et impose un second
     appariement. On change de CONDENSATEUR (100 µF puis 10 µF), ce qui donne la même plage de
     |Z| sur les deux décades avec un seul Rref et une seule configuration. -->
<!-- Niveau d'excitation : désaccord entre les deux vérificateurs (réajustement par point vs
     amplitude fixe par passe). Retenu : réajustement par point. Il satisfait aussi l'objection
     « terrain » (excursion maximale à la résonance sous attaque à courant quasi constant), car
     à tension aux bornes constante l'excursion près de f_s vaut V_d/(Bl·ω), bornée. -->
<!-- Self parasite 10 µH sur 100 Ω : les deux vérificateurs donnent des chiffres différents pour
     l'erreur de module (5e-8 « en fraction » vs 3e-6 %). Recalcul : sqrt(1+x²)-1 avec
     x = 3,14e-4 donne 4,9e-8 en fraction, soit 5e-6 %. C'est cette valeur qui est écrite. -->
<!-- Critère « ±3 % » : la feuille de route l'impose. Non supprimé, mais scindé — biais moyen
     ≤ 3 % (composantes systématiques, moyennées sur tous les points) + E_n ≤ 2 point par point.
     Cela satisfait l'objection statistique sans affaiblir la porte de validation. -->

## <a id="s03"></a>03. Problème inverse : identification des paramètres de Thiele-Small

**Place dans le récit.** Acte 2. En entrée : la courbe $Z(f)$ du haut-parleur *en caisse*, module et phase, avec ses incertitudes (livrable de l'acte 1). En sortie : les paramètres du modèle électrique de Thiele-Small, chacun avec son incertitude, **la matrice de covariance complète** et la courbe « mesure vs modèle ». Ces paramètres sont la charge sur laquelle l'acte 3 optimisera le filtre.

**Pourquoi un modèle plutôt que les points mesurés ?** Trois raisons : (1) le modèle *lisse* le bruit de mesure et *interpole* entre les points ; (2) il donne un *sens physique* aux nombres (résonance, amortissement, inductance de bobine) et permet la confrontation à la datasheet ; (3) il permet de *propager les incertitudes* jusqu'au filtre optimisé (acte 3) au lieu de traîner 70 points bruités. Le prix à payer : un modèle a un domaine de validité, qu'il faut vérifier — c'est tout l'objet des critères de validation du § 03.7.

**Rien n'a encore été mesuré sur l'enceinte.** Tous les nombres de cette section sortent de tests de la méthode sur des impédances *synthétiques* dont les paramètres sont arbitraires (modèle illustratif v1, `archive-v1/_gen.py`, ligne 68 : `Re=6.5; Le=1.2e-3; Res=44.0; fsr=40.0; Les=0.1`). Ils prouvent que le code retrouve ce qu'on y a mis, et surtout *comment il échoue* quand le modèle est faux ; ils ne disent rien du sub 18″.

> **Question tranchée le 16 septembre 2026 : la caisse est BASS-REFLEX, à deux évents.**
> Le choix du modèle direct n'est donc plus en suspens. **Le modèle à ajuster par défaut est
> celui du bass-reflex, à 7 ou 8 paramètres** : `Z_bassreflex8`, de vecteur
> $(R_e, L_e, R_{es}, f_s, Q_{ms}, \alpha, f_b, Q_l)$ — 8 paramètres, $\alpha$ **libre**, parce
> que c'est l'écartement des deux pics qui le porte ($f_L^2+f_H^2=f_s^2(1+\alpha)+f_b^2$) et que
> le figer serait s'interdire de lire ce que la courbe dit. On descend à 7 (`Z_bassreflex`,
> $\alpha$ figé) seulement si la covariance montre $\alpha$ non identifiable ; on monte à 9 (deux
> pertes séparées) seulement si les résidus le réclament (§ 01.10).
>
> **Ce n'était pas une reprise.** Le modèle à 7-8 paramètres était écrit et testé *avant* qu'on
> sache, précisément parce qu'on ne savait pas. Ce qui se lève, c'est une hypothèse, pas une
> erreur : le code n'a pas une ligne à changer, et la seule modification de cette section est de
> **permuter le défaut et le repli**.
>
> **Le modèle à 5 paramètres reste au dossier, mais comme vérification de routine.** Le test D
> du § 03.4 garde donc tout son intérêt, à un statut près : appliqué à une charge à deux pics, le
> modèle à 5 paramètres **converge sans lever la moindre erreur** et rend des nombres d'allure
> plausible ($R_e = 6{,}17 \pm 0{,}20\ \Omega$, $f_s = 39{,}0 \pm 0{,}7$ Hz,
> $Q_{ms} = 2{,}11 \pm 0{,}22$) qui ne veulent rien dire. Seuls le $\chi^2$ réduit ($s^2 = 93$)
> et la structure des résidus le trahissent. **On l'exécute désormais systématiquement, sur
> chaque jeu de mesures, comme contrôle de cohérence** : il *doit* échouer, et de façon
> spectaculaire. S'il ne le fait pas — si $s^2$ reste raisonnable avec cinq paramètres — alors
> ce n'est pas le modèle qui est en cause, c'est la mesure : la grille n'a probablement pas
> résolu les pics (§ 02.6), ou l'un des deux est hors de la bande balayée. Un garde-fou qui ne
> se déclenche jamais n'est pas un garde-fou ; celui-ci se déclenche à chaque passage et c'est
> ce qui le rend informatif.

### <a id="s03-1"></a>03.1 Le modèle direct : du haut-parleur au dipôle électrique

Un haut-parleur électrodynamique vu de ses bornes, en petit signal, c'est :

- la bobine mobile : résistance $R_e$ en série avec une inductance $L_e$ ;
- l'équipage mobile (masse $M_{ms}$, souplesse $C_{ms}$, frottements $R_{ms}$), couplé au circuit par le facteur de force $Bl$. La force de Laplace $Bl\cdot i$ met la membrane en mouvement ; la vitesse $v$ induit en retour une f.é.m. $Bl\cdot v$. Ramenée côté électrique, la mécanique apparaît comme une impédance *motionnelle* $Z_{mot} = (Bl)^2 / Z_{mec}$ ; comme $Z_{mec}$ est un RLC **série** ($R_{ms}$, $M_{ms}$, $C_{ms}$), son inverse est un RLC **parallèle** :

$$R_{es} = \frac{(Bl)^2}{R_{ms}},\qquad C_{mes} = \frac{M_{ms}}{(Bl)^2},\qquad L_{ces} = C_{ms}\,(Bl)^2 .$$

*(Contrôle dimensionnel, exposants SI $(\mathrm{m},\mathrm{kg},\mathrm{s},\mathrm{A})$ : $R_{es} \to (2,1,-3,-2) = \Omega$ ; $C_{mes} \to (-2,-1,4,2) = \mathrm{F}$ ; $L_{ces} \to (2,1,-2,-2) = \mathrm{H}$. Les trois conversions sont homogènes.)*

D'où le modèle direct, écrit avec les paramètres que l'on va identifier, $\theta = (R_e,\ L_e,\ R_{es},\ f_s,\ Q_{ms})$ :

$$\boxed{\,Z(j\omega;\theta) = R_e + j\omega L_e + \frac{R_{es}}{1 + jQ_{ms}\left(\dfrac{f}{f_s} - \dfrac{f_s}{f}\right)}\,}
\qquad f_s = \frac{1}{2\pi\sqrt{L_{ces}C_{mes}}},\quad Q_{ms} = \frac{R_{es}}{\omega_s L_{ces}} = R_{es}\,\omega_s C_{mes}.$$

Le passage du RLC parallèle explicite $(R_{es}, L_{ces}, C_{mes})$ à la forme $(R_{es}, f_s, Q_{ms})$ est une identité algébrique : la branche parallèle a pour admittance $\frac{1}{R_{es}}\left[1 + jR_{es}\left(\omega C_{mes} - \frac{1}{\omega L_{ces}}\right)\right]$, et le crochet vaut $1 + jQ_{ms}(f/f_s - f_s/f)$. Vérifié numériquement sur les paramètres du modèle v1 ($R_{es} = 44\ \Omega$, $f_s = 40$ Hz, $L_{ces} = 0{,}1$ H $\Rightarrow C_{mes} = 158{,}3\ \mu$F, $Q_{ms} = 1{,}7507$) : écart maximal entre les deux écritures $2{,}8\times10^{-14}\ \Omega$.

**Pourquoi cette paramétrisation ?** Chaque paramètre se *lit* sur la courbe (§ 03.3) et se *nomme* devant un jury : $R_e$ = plancher basse fréquence, $f_s$ = position du pic, $R_{es}$ = hauteur du pic au-dessus de $R_e$, $Q_{ms}$ = finesse du pic, $L_e$ = remontée en haut de bande. Le triplet $(R_{es}, L_{ces}, C_{mes})$ ferait la même chose mais avec des ordres de grandeur ($10^{-4}$ F, $10^{-1}$ H, $10^{1}$ Ω) qui dégradent le conditionnement (§ 03.5).

**Ce que $Z(f)$ seule ne peut PAS donner.** La courbe d'impédance fixe trois nombres motionnels ($R_{es}$, $f_s$, $Q_{ms}$), pas les cinq grandeurs mécaniques ($Bl$, $M_{ms}$, $C_{ms}$, $R_{ms}$, donc $V_{as}$). Les séparer exige une seconde mesure (masse ajoutée, ou volume connu). C'est *hors périmètre* et c'est *sans conséquence* pour le sujet : le filtre ne voit que $Z(f)$. On en déduit tout de même les facteurs de qualité classiques :

$$Q_{es} = Q_{ms}\frac{R_e}{R_{es}},\qquad Q_{ts} = \frac{Q_{ms}Q_{es}}{Q_{ms}+Q_{es}}.$$

| Paramètre | Signature sur la courbe | Ordre de grandeur typique (HP 8 Ω nominal) | Sub de Thomas |
|---|---|---|---|
| $R_e$ | plancher de $\lvert Z\rvert$ sous le pic ; = résistance DC | 5 à 7 Ω | [[à mesurer]] (multimètre) |
| $L_e$ | remontée de $\lvert Z\rvert$ et phase $> 0$ en haut de bande | 0,5 à 3 mH (gros woofers) | [[à mesurer]] |
| $R_{es}$ | $Z_{max} - R_e$ | dizaines d'ohms | [[à mesurer]] |
| $f_s$ | position du pic (en caisse : $> f_s$ datasheet) | 20 à 50 Hz (18″) | [[à mesurer]] en caisse |
| $Q_{ms}$ | finesse du pic | 2 à 10 | [[à mesurer]] |

Les ordres de grandeur sont des valeurs usuelles de catalogue, pas des données du projet. **Attention à une incohérence assumée** : le modèle illustratif v1 a $Q_{ms} = 1{,}75$, *sous* la fourchette usuelle. Son pic est donc plus large que le pic réel attendu, et mieux échantillonné. Le test E du § 03.4 rejoue tout à $Q_{ms} = 8$ pour vérifier que la méthode tient et pour en déduire le pas de la grille de mesure de la phase 1.

**Limites du modèle, à connaître avant d'ajuster.**

1. *Petit signal, linéaire.* Le modèle ignore $Bl(x)$, la compression thermique de $R_e$, etc. Vérification gratuite à ajouter au protocole de la phase 1 : refaire cinq points autour du pic à **deux amplitudes d'excitation** dans un rapport 3 environ et vérifier que $Z$ ne bouge pas plus que $u$. C'est le protocole des « deux niveaux d'écoute gelés » de la feuille de route, appliqué à la mesure d'impédance.
2. *$L_e$ constante est faux au-delà de quelques centaines de hertz.* Les courants de Foucault dans la pièce polaire dissipent de l'énergie : l'impédance de bobine devient $Z_{bob} = K(j\omega)^n$ avec $n \in [0{,}5\,;\,0{,}8]$ selon le moteur (« semi-inductance » ; $n = 1$ serait l'inductance pure, $n = 1/2$ l'effet de peau idéalisé). Ce terme a une **partie réelle** croissante, que le modèle $L_e$ = constante n'a pas : l'ajustement l'absorbe en gonflant $R_e$. C'est le risque n° 2 de la phase 2, quantifié au § 03.6 — et le repli à 6 paramètres est écrit et testé (§ 03.4, test C). Sources : Vanderkooy (1989), Leach (2002).
3. *Caisse.* **C'est le cas du projet, et il est tranché : bass-reflex à deux évents.** Le modèle à cinq paramètres écrit ci-dessus est donc le modèle du **cas de comparaison** (caisse close : un seul pic, déplacé vers le haut, $Q$ modifié, paramètres identifiés *en caisse*). Le modèle **par défaut** est `Z_bassreflex8`, huit paramètres $(R_e, L_e, R_{es}, f_s, Q_{ms}, \alpha, f_b, Q_l)$, **physique** : $f_b$ et $Q_l$ y sont des grandeurs de caisse nommées, ce qui permet le contrôle croisé du § 03.7 contre la géométrie (§ 01.10 bis) — un modèle phénoménologique l'interdirait. Repli, si `Z_bassreflex8` ne converge pas : `Z_deux_pics` (nom du dépôt, `analyse/modele_hp.py` ; le script de démonstration du § 03.4 l'appelle `Z_2pics` — même modèle, deux noms, à unifier [[à faire en phase 2]]), huit paramètres $(R_e, L_e, R_1, f_1, Q_1, R_2, f_2, Q_2)$, deux résonances en série sur la branche motionnelle — modèle *phénoménologique* (il décrit les deux pics sans prétendre nommer $f_b$ et $Q_l$ ; suffisant pour l'acte 3, qui ne voit que $Z(f)$, mais il coupe la boucle de validation géométrique). Critère d'aiguillage objectif au § 03.7.
4. *Bloc médiums* = deux HP 4 Ω en série. **Stratégie tranchée maintenant** : on l'identifie comme **un seul dipôle à 5 paramètres**, car c'est tout ce dont l'acte 3 a besoin — le passe-haut ne voit que la somme. On ne passe au modèle à deux dipôles (7 paramètres si l'on impose $R_e$ et $L_e$ communs) *que si* les résidus le réclament : $s^2 > 2$ **et** structure des résidus autour du pic. Test de cohérence gratuit : $R_e$ et $L_e$ du bloc série doivent valoir environ le double de ceux d'un médium seul.

**Généraliser le code.** Le modèle est passé en *argument* aux fonctions d'ajustement (`ajuster(Z_ts, …)`, `ajuster(Z_semi, …)`, `ajuster(Z_RC, …)`) : changer de modèle ne demande donc que d'écrire la fonction $Z(\theta, f)$ et de fournir une initialisation. Seule `init_ts` est spécifique aux cinq paramètres de Thiele-Small et à l'existence d'un pic ; les modèles génériques (résistance, condensateur) s'initialisent en deux lignes, ce qui rend le test à blanc du critère 7 réellement exécutable — il est exécuté au § 03.4.

### <a id="s03-2"></a>03.2 Du problème direct au problème inverse : les moindres carrés

*Problème direct* : $\theta$ connu $\to$ courbe $Z(f)$. *Problème inverse* : $N$ mesures $(f_k, \lvert Z_k\rvert, \varphi_k)$ connues $\to$ retrouver $\theta$. On a $2N$ équations (module et phase à chaque fréquence, ici $2\times69 = 138$) pour 5 inconnues, et les équations sont bruitées : aucun $\theta$ ne les satisfait toutes. On choisit donc le $\theta$ qui les viole *le moins*, au sens d'une somme de carrés d'écarts pondérés. **Convention de signe** : on pose $r = (\text{modèle} - \text{mesure})/u$ ; le signe est sans effet sur $S$ ni sur $\operatorname{Cov}$, mais il fixe celui de la jacobienne $J$ et donc celui de la formule du § 03.5.

$$S(\theta) = \sum_{k=1}^{2N} r_k(\theta)^2,\qquad
r_k = \frac{\ln\lvert Z(f_k;\theta)\rvert - \ln\lvert Z_k\rvert}{u(\lvert Z_k\rvert)/\lvert Z_k\rvert}\ \ (k\le N),\qquad
r_{N+k} = \frac{\arg Z(f_k;\theta) - \varphi_k}{u(\varphi_k)} .$$

**Pourquoi pondérer.** Sans division par l'incertitude, et avec un bruit *relatif* de 2 %, un point du pic (écart typique $50 \times 0{,}02 = 1\ \Omega$) contribuerait à $S$ environ $(50/7)^2 \approx 50$ fois plus qu'un point du plancher (écart typique $7 \times 0{,}02 = 0{,}14\ \Omega$) : le pic écraserait tout, alors que les deux points sont mesurés avec la *même* précision relative. Avec la normalisation, chaque point compte selon sa précision réelle, un point « bien ajusté » contribue $r_k^2 \approx 1$ et, si les $u$ sont réalistes, $S_{min} \approx 2N - p$ (nombre de degrés de liberté) : c'est le test du **$\chi^2$ réduit** $s^2 = S_{min}/(2N-p) \approx 1$.

**Hypothèse d'indépendance, à énoncer.** La matrice de poids est *diagonale* : on suppose les erreurs sur $\lvert Z\rvert$ et sur $\varphi$ indépendantes entre elles et d'un point à l'autre. Ce n'est pas évident, puisque les deux sortent des **mêmes** deux tensions ($Z = R_{ref}\,V_{HP}/V_{Rref}$, § 02) : une erreur de gain d'une voie affecte surtout le module, un défaut de synchronisation surtout la phase, mais un défaut commun de la carte d'acquisition les corrèle. Décision : garder la matrice diagonale, et si l'étalonnage de la phase 1 révèle une corrélation module/phase, passer à une matrice de poids pleine (résidus $\operatorname{Cov}^{-1/2}\!\Delta$). Les erreurs *systématiques*, elles, ne relèvent pas du tout de cette matrice : voir le § 03.5, « incertitude de type B ».

**Points aberrants, règle gelée AVANT les mesures.** Sur une mesure au lycée, un point franchement faux est quasi certain (ronflement 50 Hz, décrochage du GBF). Écarter un point *après coup* serait indéfendable. Règle : on ajuste d'abord avec la perte quadratique ; si $s^2 > 2$ **et** qu'un seul résidu dépasse $\lvert r\rvert = 5$, on relance avec une perte robuste (`loss='soft_l1'`) et on **rapporte les deux résultats**, le point suspect restant dans les données et sur la figure. Test synthétique (§ 03.4, test H) : un seul point faussé de +50 % à 50 Hz déplace $f_s$ de $+0{,}34$ Hz ($5\,u$) et $Q_{ms}$ de $+2{,}5$ % avec la perte quadratique ; avec `soft_l1`, $f_s = 40{,}034$ Hz et $Q_{ms} = 1{,}748$, soit les valeurs vraies. Attention : sous `soft_l1`, $s^2$ n'est plus un $\chi^2$ (le coût est transformé) et sert seulement de comparaison relative.

**Variante « résidu complexe ».** On peut aussi écrire $r = (Z_{mod} - Z_{mes})/u_k$ et empiler parties réelle et imaginaire, avec $u_k = \sqrt{u(\lvert Z\rvert)^2 + (\lvert Z\rvert\,u(\varphi))^2}$ le rayon d'incertitude dans le plan complexe. Sur le jeu synthétique, les deux formulations donnent les mêmes paramètres à moins de 0,3 σ (script `variante_complexe.py`, écart/u : $-0{,}29 ; -0{,}10 ; -0{,}12 ; +0{,}24 ; -0{,}06$). Le choix (log-module, phase) est retenu parce qu'il colle aux deux grandeurs *réellement mesurées* à l'oscilloscope, chacune avec son incertitude propre.

**Lien avec le programme.** La capacité exigible du programme de physique-chimie 2021 (formulation identique en PT et en PSI, annexe « Mesures et incertitudes ») est : « *Utiliser un logiciel de régression linéaire afin d'obtenir les valeurs des paramètres du modèle. Analyser les résultats obtenus à l'aide d'une procédure de validation : analyse graphique intégrant les barres d'incertitude ou analyse des écarts normalisés.* » Les « écarts normalisés », ce sont exactement les $r_k$ ci-dessus : les § 03.7 et 03.8 ne font qu'appliquer cette procédure de validation à un modèle non linéaire.

La régression linéaire du cours est le cas où $Z$ dépend *linéairement* de $\theta$ : $S$ est alors un polynôme du second degré en $\theta$, son gradient s'annule pour la solution des *équations normales* $J^{\mathsf T}J\,\theta = J^{\mathsf T}y$ — géométriquement, la projection orthogonale du vecteur des mesures sur le sous-espace engendré par les colonnes de $J$. Ici le modèle est *non linéaire* en $f_s$, $Q_{ms}$ (et $R_{es}$ n'apparaît pas linéairement dans le log-module). **Méthode de Gauss-Newton en une phrase** : on linéarise le modèle autour de l'estimation courante, $r(\theta + \delta) \approx r(\theta) + J\delta$ avec $J_{kj} = \partial r_k/\partial\theta_j$, on résout le problème *linéaire* $J^{\mathsf T}J\,\delta = -J^{\mathsf T}r$, on pose $\theta \leftarrow \theta + \delta$ et on recommence — c'est la méthode de Newton du programme d'informatique (résolution de $\nabla S = 0$, avec la hessienne de $S$ approchée par $2J^{\mathsf T}J$). Levenberg-Marquardt ajoute un amortissement $\lambda$ sur la diagonale, $(J^{\mathsf T}J + \lambda D)\delta = -J^{\mathsf T}r$, qui rend l'itération robuste loin de la solution. C'est ce que fait `scipy.optimize.least_squares` (qui minimise $\tfrac12\sum r_k^2$ ; méthode `'trf'` acceptant des bornes, ou `'lm'` = MINPACK sans bornes).

**On ne se contente pas d'appeler la boîte noire.** Levenberg-Marquardt est réimplémenté en numpy pur (25 lignes utiles, fonction `lm_numpy`), ce qui donne à la fois un repli si `scipy` manque sur la machine du lycée et une réponse à la question « et que fait-il, votre `least_squares` ? ». Vérification (§ 03.4, test G) : les cinq paramètres coïncident avec `scipy` à $6\times10^{-8}$ près en relatif, même $s^2 = 1{,}1094$, incertitudes identiques au rapport $1{,}0000$.

### <a id="s03-3"></a>03.3 Initialisation lue sur la courbe, et multi-départ

Gauss-Newton converge vers le minimum *le plus proche* du point de départ. Le point de départ doit donc venir de la courbe elle-même, pas d'une datasheet :

| Paramètre | Recette | Remarque |
|---|---|---|
| $R_e$ | multimètre en DC (à la seconde décimale) | ou $\min\lvert Z\rvert$ en bas de bande ; valeur *libre* dans l'ajustement, le multimètre ne sert qu'à démarrer et à contrôler (critère 6) |
| $f_s$ | **passage par zéro de la phase**, interpolé, dans un voisinage du maximum de $\lvert Z\rvert$ | le sommet de $\lvert Z\rvert$ est *plat* : sur une grille au 1/12 d'octave bruitée à 2 %, l'argmax tombe à un pas de grille (42,4 Hz pour 40 Hz vrais) alors que le zéro de phase donne 39,79 Hz. Repli sur l'argmax si la phase est trop bruitée. **Ni l'un ni l'autre ne vaut $f_s$** : $L_e$ les décale en sens *opposés* (sur le modèle non bruité, $\lvert Z\rvert_{max}$ à 39,940 Hz et $\varphi = 0$ à 40,079 Hz pour $f_s = 40{,}000$) ; seul l'ajustement rend $f_s$ |
| $R_{es}$ | $Z_{max} - R_e$ | hauteur du pic |
| $Q_{ms}$ | $Q_{ms} = \dfrac{f_s\sqrt{r_0}}{f_2 - f_1}$ avec $r_0 = Z_{max}/R_e$ et $f_1 < f_s < f_2$ tels que $\lvert Z\rvert = \sqrt{R_e Z_{max}}$ | méthode classique de Small (1972). **Exacte** si $L_e = 0$ (et non approchée : en posant $u = Q_{ms}x$, la condition $\lvert Z\rvert = \sqrt{R_e Z_{max}}$ donne $u^2 = 1 + R_{es}/R_e = r_0$ ; vérifié, 1,7500 pour 1,75). Avec $L_e = 1{,}2$ mH : $+2{,}4$ % sur courbe non bruitée, $+11$ % sur la grille bruitée. Suffisant pour démarrer, pas pour conclure |
| $L_e$ | $\dfrac{\operatorname{Im} Z_{mes}(f_{\text{haut}}) - \operatorname{Im} Z_{mot,0}(f_{\text{haut}})}{2\pi f_{\text{haut}}}$ | $f_{\text{haut}}$ = fréquence la plus **élevée** de la grille (500 Hz), *et non* la fréquence du maximum de $\lvert Z\rvert$. Partie imaginaire en haut de bande, *corrigée de la queue de la branche motionnelle* (§ 03.6) |

**Garde-fou sur la bande de balayage.** La recherche de $f_1$ et $f_2$ suppose que les *deux* flancs du pic redescendent sous le seuil $\sqrt{R_e Z_{max}}$ à l'intérieur de la bande mesurée. Si le balayage ne descend pas assez bas, la recherche échoue : le code lève alors un avertissement explicite et se replie sur $Q_{ms,0} = 3$ (les moindres carrés corrigent), au lieu de planter sur un `IndexError` nu. Testé pour plusieurs $Q_{ms}$ (§ 03.4, test F) : à $Q_{ms} = 1{,}75$ le repli s'enclenche dès $f_{min} = 20$ Hz, à $Q_{ms} = 4$ dès 30 Hz. **Consigne pour la phase 1** : commencer le balayage au moins une octave sous le pic attendu (donc à 10–15 Hz pour un pic vers 40 Hz), sinon $Q_{ms}$ n'est pas initialisable — et c'est justement la zone où le jig d'impédance sur carte son décroche (couplage AC).

**Multi-départ.** L'initialisation lue sur la courbe est bonne, mais elle n'est pas une *preuve* d'unicité du minimum. Le test honnête consiste à repartir de points volontairement mauvais sur **les mêmes** données : 200 départs tirés au hasard dans un facteur 0,2 à 5 sur chaque paramètre retrouvent le minimum global dans **94 %** des cas ; les 6 % restants tombent sur un minimum de bord ($L_e \to 0$, $Q_{ms}$ très grand) immédiatement reconnaissable à son coût — $\chi^2$ réduit de l'ordre de $1{,}3\times10^3$ contre 1,11. Des minima parasites existent donc bel et bien ; la parade est double : initialiser sur la courbe, et faire tourner un multi-départ (fonction `multistart`, une cinquantaine de tirages) en gardant le coût le plus bas. C'est ce que fait le code, et c'est ce qu'il faut répondre au jury (§ 03.8).

### <a id="s03-4"></a>03.4 Le code, exécuté sur données synthétiques

Fichiers `fit_ts.py` (bibliothèque) et `main_ts.py` / `diag_ts.py` (programmes). Environnement vérifié : Python 3.13.2, numpy 2.4.6, scipy 1.18.1, matplotlib 3.11.0. Hypothèses de ce *test de méthode* : paramètres « vrais » arbitraires (modèle v1) ; bruit de 2 % sur $\lvert Z\rvert$ et 1° sur $\varphi$ (**hypothèse**, à remplacer par les incertitudes réellement étalonnées en phase 1) ; grille de 10 à 500 Hz au 1/12 d'octave (69 points). En phase 2, `simuler` est remplacé par la lecture du CSV de mesure (colonnes $f$, $\lvert Z\rvert$, $\varphi$, $u_{\lvert Z\rvert}$, $u_\varphi$) ; rien d'autre ne change.

```python
# ---------- 1. Modèles directs : Z(jω ; θ) ----------
def Z_ts(theta, f):
    """Modèle 5 paramètres, caisse close. theta = (R_e, L_e, R_es, f_s, Q_ms) SI."""
    Re, Le, Res, fs, Qms = theta
    return Re + 2j*np.pi*f*Le + Res/(1 + 1j*Qms*(f/fs - fs/f))

def Z_semi(theta, f):
    """Repli 6 paramètres : bobine à pertes Z = K(jω)^n (courants de Foucault)."""
    Re, K, n, Res, fs, Qms = theta
    return Re + K*(1j*2*np.pi*f)**n + Res/(1 + 1j*Qms*(f/fs - fs/f))

def Z_2pics(theta, f):
    """Repli bass-reflex (phénoménologique) : deux résonances en série."""
    Re, Le, R1, f1, Q1, R2, f2, Q2 = theta
    return (Re + 2j*np.pi*f*Le + R1/(1 + 1j*Q1*(f/f1 - f1/f))
                               + R2/(1 + 1j*Q2*(f/f2 - f2/f)))

def Z_RL(theta, f):                      # test à blanc : résistance étalon
    R, L = theta;  return R + 2j*np.pi*f*L

# ---------- 2. Grille et données synthétiques (remplacées par le CSV en phase 2) ----------
def grille_freq(f1, f2, n_par_octave=12):
    """Grille géométrique dont les DEUX bornes sont exactement f1 et f2 : on
    arrondit le nombre d'intervalles, le pas vaut donc environ 1/n_par_octave."""
    n = max(1, round(np.log2(f2/f1)*n_par_octave))
    return f1*(f2/f1)**(np.arange(n + 1)/n)

def simuler(Zfun, theta, f, u_rel, u_deg, rng):
    Z = Zfun(theta, f)
    mod = np.abs(Z)*(1 + u_rel*rng.standard_normal(f.size))
    phi = np.angle(Z) + np.radians(u_deg)*rng.standard_normal(f.size)
    return mod, phi, u_rel*mod, np.full(f.size, np.radians(u_deg))

# ---------- 3. Initialisation lue sur la courbe ----------
def init_ts(f, mod, phi, Re_dmm, bavard=True):
    k = int(np.argmax(mod)); Zmax = mod[k]
    # f_s : passage par zéro de la phase autour du pic (plus net que l'argmax plat)
    vois = np.where((f > f[k]/2) & (f < 2*f[k]))[0]
    chg = [i for i in vois[:-1] if phi[i] > 0 >= phi[i+1]]
    fs0 = (np.interp(0.0, [phi[chg[0]+1], phi[chg[0]]], [f[chg[0]+1], f[chg[0]]])
           if chg else f[k])
    Res0 = Zmax - Re_dmm
    seuil = np.sqrt(Re_dmm*Zmax)                  # méthode de Small (1972)
    g = np.where(mod[:k] < seuil)[0]; d = np.where(mod[k:] < seuil)[0]
    if g.size and d.size:                         # les deux flancs sont dans la bande
        i1, i2 = g[-1], k + d[0]
        f1 = np.interp(seuil, [mod[i1], mod[i1+1]], [f[i1], f[i1+1]])
        f2 = np.interp(seuil, [mod[i2], mod[i2-1]], [f[i2], f[i2-1]])
        Qms0 = fs0*np.sqrt(Zmax/Re_dmm)/(f2 - f1)
    else:
        if bavard:
            print("  AVERTISSEMENT : un flanc du pic sort de la bande mesurée "
                  "(balayer au moins une octave sous f_s) ; Q_ms initialisé à 3.")
        Qms0 = 3.0
    f_haut = f[-1]                                # fréquence la plus HAUTE de la grille
    im_mot = np.imag(Z_ts(np.array([Re_dmm, 0.0, Res0, fs0, Qms0]), f_haut))
    Le0 = max((mod[-1]*np.sin(phi[-1]) - im_mot)/(2*np.pi*f_haut), 1e-5)
    return np.array([Re_dmm, Le0, Res0, fs0, Qms0])
```

```python
# ---------- 4. Résidus pondérés, ajustement, multi-départ ----------
def residus(theta, f, mod, phi, u_mod, u_phi, Zfun):
    """Convention : r = (modèle - mesure)/u."""
    Z = Zfun(theta, f)
    return np.concatenate([np.log(np.abs(Z)/mod)/(u_mod/mod),
                           (np.angle(Z) - phi)/u_phi])

def ajuster(Zfun, theta0, f, mod, phi, u_mod, u_phi, loss='linear', bavard=True):
    res = least_squares(residus, theta0, args=(f, mod, phi, u_mod, u_phi, Zfun),
                        bounds=(1e-12, np.inf), x_scale=np.abs(theta0),
                        method='trf', loss=loss)
    n_res, p = 2*f.size, theta0.size
    s2 = 2*res.cost/(n_res - p)                   # χ² réduit (≈ 1 si les u sont justes)
    J = res.jac
    cond = np.linalg.cond(J*res.x)
    if bavard and (np.any(res.active_mask != 0) or cond > 1e6):
        print("  ALERTE : paramètre en butée ou jacobienne mal conditionnée "
              "(cond = %.1e) -> covariance NON exploitable." % cond)
    cov = s2*np.linalg.inv(J.T @ J)               # convention absolute_sigma=False
    return res.x, cov, s2, res

def multistart(Zfun, theta0, f, mod, phi, u_mod, u_phi, n=50, fac=3.0, graine=0):
    """Départ multiple : garde le coût le plus bas. Teste l'unicité du minimum."""
    rg = np.random.default_rng(graine); best = None; couts = []
    for i in range(n):
        t0 = theta0 if i == 0 else theta0*np.exp(
            rg.uniform(-np.log(fac), np.log(fac), theta0.size))
        try: sol = ajuster(Zfun, t0, f, mod, phi, u_mod, u_phi, bavard=False)
        except Exception: continue
        couts.append(sol[3].cost)
        if best is None or sol[3].cost < best[3].cost: best = sol
    couts = np.array(couts)
    return best, float(np.mean(couts < best[3].cost*1.001)), couts
```

```python
# ---------- 5. Incertitudes et diagnostics ----------
def monte_carlo(Zfun, th, f, u_mod, u_phi, n, rng):      # bootstrap paramétrique
    Zh = Zfun(th, f); out = []
    for _ in range(n):
        mod = np.abs(Zh) + u_mod*rng.standard_normal(f.size)
        phi = np.angle(Zh) + u_phi*rng.standard_normal(f.size)
        try: t0 = init_ts(f, mod, phi, th[0], bavard=False)
        except Exception: t0 = th
        out.append(ajuster(Zfun, t0, f, mod, phi, u_mod, u_phi, bavard=False)[0])
    return np.array(out)

def jackknife(Zfun, th, f, mod, phi, u_mod, u_phi):
    """On retire une FRÉQUENCE (donc ses 2 résidus) à la fois : N ajustements."""
    N = f.size; ths = []
    for i in range(N):
        m = np.ones(N, bool); m[i] = False
        ths.append(ajuster(Zfun, th, f[m], mod[m], phi[m], u_mod[m], u_phi[m],
                           bavard=False)[0])
    ths = np.array(ths)
    return np.sqrt((N-1)/N*np.sum((ths - ths.mean(0))**2, axis=0)), ths

def test_sequences(r):
    """Wald-Wolfowitz sur les signes des résidus : R runs, E[R], sd, z."""
    s = np.sign(r); a = int((s > 0).sum()); b = int((s < 0).sum()); N = a + b
    R = 1 + int(np.sum(s[1:] != s[:-1]))
    E = 1 + 2*a*b/N
    sd = np.sqrt(2*a*b*(2*a*b - N)/(N**2*(N - 1)))
    return R, E, sd, (R - E)/sd

def leviers(J):
    """Diagonale de la matrice chapeau H = J(JᵀJ)⁻¹Jᵀ : influence de chaque résidu."""
    Q, _ = np.linalg.qr(J);  return np.sum(Q**2, axis=1)

def bande_Z(Zfun, th, cov, ff, h=1e-6):
    """Incertitude sur |Z(f)| par propagation de la covariance COMPLÈTE."""
    base = np.abs(Zfun(th, ff)); G = np.empty((ff.size, th.size))
    for j in range(th.size):
        t = th.copy(); t[j] *= 1 + h
        G[:, j] = (np.abs(Zfun(t, ff)) - base)/(th[j]*h)
    return base, np.sqrt(np.einsum('ij,jk,ik->i', G, cov, G))

# ---------- 6. Repli sans scipy : Levenberg-Marquardt en numpy pur ----------
def lm_numpy(fres, x0, args=(), tol=1e-12, itmax=200):
    x = np.array(x0, float); lam = 1e-3
    r = fres(x, *args); S = r @ r
    for _ in range(itmax):
        J = np.empty((r.size, x.size))
        for j in range(x.size):                   # jacobienne par différences finies
            h = 1e-7*max(abs(x[j]), 1e-12); xp = x.copy(); xp[j] += h
            J[:, j] = (fres(xp, *args) - r)/h
        A = J.T @ J; g = J.T @ r
        for _ in range(60):        # pas amorti : lambda /3 si le coût baisse, x5 sinon
            d = np.linalg.solve(A + lam*np.diag(np.diag(A)), -g)
            xn = np.maximum(x + d, 1e-12); rn = fres(xn, *args); Sn = rn @ rn
            if Sn < S:
                fini = abs(S - Sn) < tol*S
                x, r, S, lam = xn, rn, Sn, max(lam/3, 1e-12)
                if fini: return x, J, S
                break
            lam *= 5
        else: break
    return x, J, S
```

Sortie obtenue (`main_ts.py`, exécution du 2026-09-09) :

```text
grille : 69 frequences de 10.0 a 500.0 Hz (138 residus), 5 parametres
parametre        vrai      init    ajuste    u_cov  ecart/u
R_e [Ohm]       6.500     6.436     6.499    0.029    -0.04
L_e [mH]        1.200     1.232     1.214    0.016     0.89
R_es [Ohm]     44.000    45.026    44.010    0.287     0.04
f_s [Hz]       40.000    39.787    39.987    0.067    -0.19
Q_ms [-]        1.750     1.833     1.741    0.014    -0.62
chi2 reduit s2 = 1.11 (sd statistique 0.123) ; statut 2
cout : 8 evaluations du vecteur residu, 48 appels au modele direct (jacobienne numerique comprise)
multistart 200 departs (facteur 0,2 a 5) : 94 % retrouvent le minimum global ; 12 minima parasites, chi2 reduit median 1256
residu relatif RMS sur |Z| = 1.97 % ; sur phi = 1.08 deg
  idem sur 20-300 Hz (porte de validation) : 2.03 % ; 1.00 deg
conditionnement de J : brut = 2.1e+04 ; apres mise a l'echelle par theta = 8.2e+00
matrice de correlation (R_e, L_e, R_es, f_s, Q_ms) :
[[ 1.   -0.15  0.22 -0.02  0.35]
 [-0.15  1.    0.01  0.18 -0.24]
 [ 0.22  0.01  1.   -0.    0.83]
 [-0.02  0.18 -0.    1.    0.01]
 [ 0.35 -0.24  0.83  0.01  1.  ]]
sequences module : R = 37 runs pour E = 35.3 +- 4.1 -> z = +0.41
sequences phase  : R = 35 runs pour E = 35.4 +- 4.1 -> z = -0.11
max|r| = 2.98 ; 0 residu(s) au-dela de 3 sur 138
parametre      u_cov     u_MC   u_jack  sd_ret20%  /(0,50 u)
R_e [Ohm]      0.029    0.027    0.034      0.017       1.15
L_e [mH]       0.016    0.015    0.019      0.010       1.21
R_es [Ohm]     0.287    0.264    0.309      0.153       1.07
f_s [Hz]       0.067    0.062    0.068      0.037       1.11
Q_ms [-]       0.014    0.013    0.015      0.007       1.06
levier max = 0.134 (moyenne 0.036) au residu 137 -> phase a 500.0 Hz
Q_es = 0.257 +- 0.002 (vrai 0.259) ; Q_ts = 0.224 +- 0.001 (vrai 0.225)
|Z( 40 Hz)| =  50.51 Ohm  u = 0.294 Ohm (0.58 %)  [covariance complete]
|Z(100 Hz)| =  14.15 Ohm  u = 0.049 Ohm (0.35 %)  [covariance complete]
|Z(200 Hz)| =   8.01 Ohm  u = 0.026 Ohm (0.32 %)  [covariance complete]
R_ref +1 % : ecart relatif [ 1.  1.  1. -0.  0.] %, soit [ 2.25  0.76  1.54 -0.    0.  ] u_cov ; s2 = 1.11
R_ref +3 % : ecart relatif [ 3.  3.  3. -0.  0.] %, soit [ 6.76  2.29  4.61 -0.    0.  ] u_cov ; s2 = 1.11

bande         u(L_e) [mH]  corr(L_e,Q_ms)  corr(L_e,R_es)  L_e ajuste [mH]
10- 150 Hz        0.085           -0.26            0.08          1.212
10- 300 Hz        0.027           -0.30            0.02          1.162
10- 500 Hz        0.014           -0.24            0.01          1.183
10-2000 Hz        0.005           -0.12            0.02          1.193
figure : fit_synthetique.png
livrable acte 3 : ts_theta.csv, ts_cov.csv (5x5), ts_mc.csv (300 tirages)
```

**Lecture.** Le $\chi^2$ réduit vaut 1,11 (les résidus ont bien l'amplitude du bruit injecté : 1,97 % en module pour 2 % injectés, 1,08° pour 1°), les résidus normalisés ne présentent aucune structure ($z = +0{,}41$ et $-0{,}11$ au test des séquences) et le multi-départ retrouve le minimum global dans 94 % des cas. Sur ce tirage-ci, les cinq paramètres tombent à moins de $1\,u$ de leur valeur vraie — mais **ce n'est pas la preuve que la méthode marche** : cinq paramètres simultanément sous $1\,\sigma$ n'a qu'une probabilité $0{,}68^5 \approx 15$ % même quand tout va bien. La preuve, c'est la statistique de couverture du test B ci-dessous. Le statut 2 de scipy signifie « critère `ftol` atteint ».

Sortie obtenue (`diag_ts.py`, mêmes conditions ; huit tests indépendants) :

```text
=== A. TEST A BLANC (critere 7) : dipoles connus, on ne change que le modele ===
  ALERTE : parametre en butee ou jacobienne mal conditionnee (cond = 7.6e+10) -> covariance NON exploitable.
  resistance etalon 100 Ohm : R = 99.82 +- 0.22 Ohm (ecart -0.8 u) ; s2 = 0.81
    -> le garde-fou se declenche a juste titre : a 100 Ohm, une inductance de cordon de 1 uH est
       invisible (0.0018 deg a 500 Hz), donc NON identifiable ; on lit R, on ignore u(L).
  condensateur 150 uF (ESR 0,30 Ohm) : C = 150.13 +- 0.35 uF (ecart +0.4 u) ;
       ESR = 0.282 +- 0.012 Ohm (-1.5 u) ; s2 = 0.96
=== B. COUVERTURE : 300 realisations de bruit independantes ===
  |ecart| < u  : [71. 71. 65. 65. 67.] % (68 attendus)
  |ecart| < 2u : [96. 96. 95. 95. 95.] % (95 attendus)
  les cinq simultanement sous 1u : 21 % des tirages
  s2 : moyenne 1.005, min 0.59, max 1.31 (jamais hors de [0,5 ; 2])
=== C. SEMI-INDUCTANCE : donnees K(jw)^0,7, R_e vrai 6,500 Ohm, Q_ms 4,0 ===
  ajuste 5 param sur 10- 200 Hz : R_e = 6.945 +- 0.043 (+6.8 %, +10.3 u) ; s2 = 2.28 ; z = -1.3
  ajuste 5 param sur 10- 300 Hz : R_e = 7.076 +- 0.046 (+8.9 %, +12.5 u) ; s2 = 3.28 ; z = -3.1
  ajuste 5 param sur 10- 500 Hz : R_e = 7.267 +- 0.053 (+11.8 %, +14.4 u) ; s2 = 5.37 ; z = -5.6
  ajuste 5 param sur 10-1000 Hz : R_e = 7.560 +- 0.068 (+16.3 %, +15.5 u) ; s2 = 10.41 ; z = -6.5
  REMEDE, modele 6 param sur 10-2000 Hz : R_e = 6.475 +- 0.031 ; n = 0.696 +- 0.005 (vrai 0,700) ; s2 = 0.86
  (memes donnees, modele 5 param L_e = cte : R_e = 7.871, s2 = 21.8)
  ATTENTION : sur ce modele FAUX (s2 = 5.4), le critere de stabilite passe quand meme
       -> sd/(0,50 u) = [1.44 1.02 0.85 0.72 0.91], max|D|/u = [2.5 2.4 1.8 1.7 1.8]
=== D. BASS-REFLEX (deux pics) ajuste par le modele 5 parametres ===
  courbe vraie : pics a [32.8 46.2] Hz (|Z| = [33.6 33.5] Ohm), creux 11.7 Ohm
  aiguillage (maxima locaux de |Z| lisse sur 3 points, 10-100 Hz) : bass-reflex -> 3 ; caisse close -> 1
  ajustement 5 param : R_e = 6.169 +- 0.196 ; f_s = 39.03 +- 0.71 ; Q_ms = 2.105 +- 0.223
  -> il CONVERGE sans erreur, mais s2 = 93, RMS = 17.8 %, z(sequences) = -5.4
=== E. Q_ms ELEVE : largeur du pic et pas de grille ===
  Q_ms =  1.75 : f2 - f1 =  63.7 Hz -> 35 point(s) au 1/12 d'octave dans la largeur
  Q_ms =  4.00 : f2 - f1 =  27.9 Hz -> 13 point(s) au 1/12 d'octave dans la largeur
  Q_ms =  8.00 : f2 - f1 =  13.9 Hz ->  6 point(s) au 1/12 d'octave dans la largeur
  Q_ms = 12.00 : f2 - f1 =   9.3 Hz ->  5 point(s) au 1/12 d'octave dans la largeur
  1/12 oct, 10-500 Hz       69 points : Q_ms = 7.929 +- 0.102 (vrai 8,0) ; f_s = 40.000 +- 0.029 Hz
  + 1/48 oct sur 20-80 Hz  166 points : Q_ms = 8.034 +- 0.046 (vrai 8,0) ; f_s = 40.006 +- 0.012 Hz
=== F. INITIALISATION : jusqu'ou faut-il descendre en frequence ? ===
  Q_ms = 1.75 : 10 Hz:OK  15 Hz:OK  20 Hz:repli  25 Hz:repli  30 Hz:repli
  Q_ms = 4.00 : 10 Hz:OK  15 Hz:OK  20 Hz:OK  25 Hz:OK  30 Hz:repli
  Q_ms = 8.00 : 10 Hz:OK  15 Hz:OK  20 Hz:OK  25 Hz:OK  30 Hz:OK
=== G. REPLI SANS SCIPY : Levenberg-Marquardt en numpy pur ===
  ecart relatif max sur les cinq parametres = 6.1e-08 ; s2 : 1.1094 (LM) vs 1.1094 (scipy) ;
  rapport des u = [1. 1. 1. 1. 1.]
=== H. POINT ABERRANT (ronflement 50 Hz sur un point : |Z| x 1,5) ===
  loss = linear   : f_s = 40.341 Hz (vrai 40,000) ; Q_ms = 1.794 (vrai 1,750) ; s2 = 6.52
  loss = soft_l1  : f_s = 40.034 Hz (vrai 40,000) ; Q_ms = 1.748 (vrai 1,750) ; s2 = 1.19
```

**Ce que ces huit tests établissent, dans l'ordre d'importance pour la phase 2 :**

- **(B) Les incertitudes annoncées sont calibrées.** Sur 300 réalisations de bruit indépendantes, l'écart à la valeur vraie reste sous $u$ dans 65 à 71 % des cas selon le paramètre (68 % attendus) et sous $2u$ dans 95 à 96 % (95 % attendus), avec un biais moyen inférieur à $0{,}15\,u$. C'est l'argument fort, et c'est celui qu'il faut montrer au jury — pas le tirage favorable du § 03.4.
- **(D) Un modèle inadapté ne se signale pas par une erreur, mais par $s^2$.** D'où le critère d'aiguillage 0 du § 03.7.
- **(C) La semi-inductance produit un *biais* sur $R_e$, pas une variance** : voir § 03.6.
- **(A) Le test à blanc du critère 7 est exécutable et il passe** : condensateur de 150 µF retrouvé à $150{,}13 \pm 0{,}35$ µF ($+0{,}4\,u$) avec $s^2 = 0{,}96$, résistance étalon à $99{,}82 \pm 0{,}22$ Ω ($-0{,}8\,u$). Le garde-fou de `ajuster` se déclenche sur la résistance : c'est correct, l'inductance des cordons n'y est pas identifiable — un exemple concret de covariance à ne pas publier.
- **(E) Conception de la mesure de la phase 1.** À $Q_{ms} = 8$ (valeur plausible pour un 18″), la largeur de Small $f_2 - f_1 = f_s\sqrt{r_0}/Q_{ms}$ tombe à 14 Hz, soit 6 points seulement au 1/12 d'octave. Une grille mixte (1/12 d'octave sur 10–500 Hz **+** 1/48 d'octave sur 20–80 Hz, 166 points au lieu de 69) fait passer $u(Q_{ms})$ de 0,102 à 0,046 et $u(f_s)$ de 0,029 à 0,012 Hz. C'est le calcul qui justifie quantitativement le « balayage resserré autour du pic » de la feuille de route : deux fois plus de points, mais placés là où ils informent — argument « efficacité » directement dans le thème du TIPE.
- **(F)** Balayer au moins une octave sous le pic. **(G)** Le repli sans scipy est démontré équivalent. **(H)** La perte robuste sauve l'ajustement en présence d'un point aberrant.

<!-- Divergence entre les deux vérificateurs sur la largeur du pic à Q_ms = 8 (5,0 Hz contre 13,9 Hz) : il s'agit de deux définitions différentes, f_s/Q_ms d'une part, f_2 - f_1 = f_s*sqrt(r_0)/Q_ms (définition de Small) d'autre part. La section utilise partout la seconde, qui est celle de sa propre formule d'initialisation ; les comptages de points en découlent (6 et non 3). -->
<!-- Divergence sur le coût du minimum parasite (620 contre 1250) : le premier chiffre divise le coût scipy (= S/2) par 2N-p au lieu de S. Valeur recalculée ici : chi2 réduit médian 1256. -->

### <a id="s03-5"></a>03.5 Incertitudes des paramètres : ce que chaque estimateur teste, et ce qu'il ne teste pas

**1. Covariance par la jacobienne (la formule).** Au voisinage du minimum, $r(\theta) \approx r(\hat\theta) + J(\theta - \hat\theta)$. Avec la convention $r = (\text{modèle} - \text{mesure})/u$ du § 03.2, perturber la mesure de $u\varepsilon$ change $r$ en $r - \varepsilon$, et l'annulation de $J^{\mathsf T}r$ donne $\hat\theta - \theta_{vrai} \approx (J^{\mathsf T}J)^{-1}J^{\mathsf T}\varepsilon$, d'où

$$\operatorname{Cov}(\hat\theta) \approx s^2\,(J^{\mathsf T}J)^{-1},\qquad s^2 = \frac{S_{min}}{2N - p},\qquad u(\theta_j) = \sqrt{\operatorname{Cov}_{jj}},\qquad \rho_{ij} = \frac{\operatorname{Cov}_{ij}}{u_i u_j}.$$

Le facteur $s^2$ corrige une éventuelle sur- ou sous-estimation *globale* des $u_k$. Coût : nul (la jacobienne est déjà calculée). Limite : formule *linéarisée*.

**Convention à geler pour la phase 2.** `curve_fit` propose $s^2(J^{\mathsf T}J)^{-1}$ (`absolute_sigma=False`, défaut) ou $(J^{\mathsf T}J)^{-1}$ (`absolute_sigma=True`). Après étalonnage de la chaîne en phase 1, les $u_k$ sont *connus* : la convention cohérente est donc **sans le facteur $s^2$**, sinon un défaut de modèle est blanchi en incertitude ($s^2 = 5$ multiplierait toutes les barres par 2,2 et ferait disparaître le symptôme). **Décision : reporter $(J^{\mathsf T}J)^{-1}$, et traiter $s^2$ comme un *diagnostic* (critère 1) et non comme un correctif.** Ici $\sqrt{s^2} = 1{,}05$, la différence est de 5 %.

**2. Monte-Carlo sur le bruit de mesure (bootstrap paramétrique).** On rejoue 300 fois le bruit de la chaîne autour du modèle ajusté, on ré-initialise *depuis la courbe bruitée* et on réajuste ; l'écart-type des 300 solutions est $u_{MC}$. Ne suppose rien de linéaire ; teste au passage la robustesse de l'initialisation. Coût : 300 ajustements (quelques secondes).

**3. Jackknife (retrait d'un point).** On refait l'ajustement $N = 69$ fois en retirant à chaque fois **une fréquence**, donc les *deux* résidus (module et phase) qui lui correspondent ; $u_{jack}^2 = \frac{N-1}{N}\sum_i (\hat\theta_{(i)} - \bar\theta_{(\cdot)})^2$. Ne suppose rien sur le bruit : il mesure ce que *ces* données, avec *leur* dispersion réelle, laissent comme liberté aux paramètres.

| Paramètre | $u_{cov}$ | $u_{MC}$ | $u_{jack}$ | écart-type sous retrait de 20 % | rapport à la valeur attendue $0{,}50\,u_{cov}$ |
|---|---|---|---|---|---|
| $R_e$ (Ω) | 0,029 | 0,027 | 0,034 | 0,017 | 1,15 |
| $L_e$ (mH) | 0,016 | 0,015 | 0,019 | 0,010 | 1,21 |
| $R_{es}$ (Ω) | 0,287 | 0,264 | 0,309 | 0,153 | 1,07 |
| $f_s$ (Hz) | 0,067 | 0,062 | 0,068 | 0,037 | 1,11 |
| $Q_{ms}$ | 0,014 | 0,013 | 0,015 | 0,007 | 1,06 |

**Ce que leur accord prouve — et ce qu'il ne prouve pas.** Attention à ne pas surinterpréter : le Monte-Carlo *rejoue* le bruit avec les $u_k$ postulés, il ne peut donc rien dire de leur réalisme. Vérification numérique : $u_{MC}$ reproduit $(J^{\mathsf T}J)^{-1}$ *sans* le facteur $s^2$ à 3–10 % près ; $u_{cov}$ et $u_{MC}$ sont donc **le même estimateur au facteur $\sqrt{s^2} = 1{,}05$ près**, et leur accord valide la *linéarisation*, rien d'autre. Le réalisme des $u_k$ est jugé par (i) $s^2 \approx 1$, (ii) l'accord avec le **jackknife**, seul des trois à n'utiliser que la dispersion réellement observée, et (iii) la couverture du test B. Les trois concordent ici à ±14 % autour de leur moyenne (rapport max/min de 1,27, sur $R_e$).

**Le retrait de 20 % ne teste pas ce qu'on croit.** Pour un sous-échantillonnage sans remise de fraction $d/n$, l'écart-type des estimations vaut asymptotiquement $u\sqrt{d/(n-d)} = 0{,}50\,u$ pour $d/n = 0{,}2$. Un critère « écart-type $< u_{cov}$ » est donc satisfait *par construction* — et il l'est même sur les données semi-inductives où le modèle est démontrablement faux ($s^2 = 5{,}4$, test C). Ce test mesure le **conditionnement**, pas l'adéquation ; il n'est informatif que *normalisé* (colonne de droite du tableau : on attend 1, on observe 1,06 à 1,21). L'adéquation, c'est $s^2$ et la structure des résidus.

**Diagnostic d'influence.** La dispersion globale ne dit pas *quel* point porte l'ajustement. Le levier $h_{kk}$ (diagonale de la matrice chapeau $H = J(J^{\mathsf T}J)^{-1}J^{\mathsf T}$, de trace $p$, donc de moyenne $p/2N = 0{,}036$) le dit : ici le levier maximal vaut 0,134, sur le résidu de **phase à 500 Hz** — le point qui, à lui seul, fixe $L_e$. Conséquence pratique pour la phase 2 : si un paramètre bouge trop sous retrait, on regarde les leviers pour savoir quel point re-mesurer, au lieu de re-mesurer les 69.

**Grandeurs dérivées.** $Q_{es}$ et $Q_{ts}$ ne s'obtiennent pas en additionnant des incertitudes relatives (les paramètres sont corrélés) : on les calcule *sur chaque tirage Monte-Carlo* et on prend l'écart-type des résultats — $Q_{es} = 0{,}257 \pm 0{,}002$, $Q_{ts} = 0{,}224 \pm 0{,}001$ (valeurs vraies 0,259 et 0,225).

**Corrélations et conditionnement.** La corrélation dominante est $\rho(R_{es}, Q_{ms}) = 0{,}83$ : les points des flancs du pic vérifient $\lvert Z_{mot}\rvert = R_{es}/\sqrt{1 + Q_{ms}^2 x^2}$, donc un pic un peu plus haut *et* un peu plus étroit passe par les mêmes points de flanc — seul le sommet, plat et donc peu contraignant, les départage. Conséquences pratiques :

- (a) toujours *afficher* la matrice de corrélation à côté des $u$ ;
- (b) une incertitude sur $Q_{ms}$ seul sous-estime ce que l'on sait du *couple* — pour l'acte 3, propager la covariance complète (ou les tirages Monte-Carlo), pas cinq $u$ indépendants ;
- (c) **on ne peut pas s'en débarrasser à bon compte** avec le multimètre. Ajouter un sixième résidu $(R_e - R_{e,DMM})/u_{DMM}$ ne change ni $\rho(R_{es},Q_{ms})$ (0,831 → 0,830) ni vraiment $\rho(R_e,Q_{ms})$ (0,343 → 0,319) : la corrélation dominante vient de la géométrie des flancs, pas de $R_e$. *Figer* $R_e$ à la lecture du multimètre la supprime formellement mais transfère l'erreur du multimètre en **biais** sur $Q_{ms}$ (avec une lecture fausse de 1 %, $Q_{ms} = 1{,}731$ au lieu de 1,742, soit $-0{,}8\,u$) et fait disparaître $u(R_e)$ du bilan. **Décision : garder $R_e$ libre**, n'utiliser le multimètre que comme contrôle de plausibilité (critère 6), et propager la covariance complète.

Le **conditionnement** de la jacobienne passe de $2{,}1\times10^4$ (paramètres en unités SI, $L_e$ en henry contre $R_{es}$ en dizaines d'ohms) à $8{,}2$ une fois chaque colonne multipliée par son paramètre : c'est le rôle de `x_scale`. Honnêteté sur ce point : sur *ce* problème, la convergence est strictement identique avec `x_scale`, sans, et avec `method='lm'` (même coût 73,80, même nombre d'itérations, même $\theta$) — $2\times10^4$ reste trivial en double précision. Le bénéfice de la mise à l'échelle est une garantie de robustesse si l'initialisation devient plus lointaine ; ce n'est pas un besoin démontré ici, et il ne faut pas prétendre le contraire devant un jury qui peut demander « montrez-moi ».

**Incertitude systématique (type B) : la composante que les trois estimateurs ne voient pas.** Les trois estimateurs ci-dessus mesurent la même chose, la composante **aléatoire** $u_A$. Or $Z = R_{ref}\,V_{HP}/V_{Rref}$ : une erreur de $+1$ % sur $R_{ref}$ multiplie **toutes** les $\lvert Z\rvert$ par 1,01, de façon parfaitement corrélée d'un point à l'autre. Vérifié numériquement :

| Erreur sur $R_{ref}$ | $R_e$ | $L_e$ | $R_{es}$ | $f_s$ | $Q_{ms}$ | $s^2$ |
|---|---|---|---|---|---|---|
| $+1$ % | $+1{,}00$ % ($+2{,}25\,u_{cov}$) | $+1{,}00$ % ($+0{,}76\,u$) | $+1{,}00$ % ($+1{,}54\,u$) | $+0{,}00$ % | $+0{,}00$ % | 1,11 (inchangé) |
| $+3$ % | $+3{,}00$ % ($+6{,}76\,u$) | $+3{,}00$ % ($+2{,}29\,u$) | $+3{,}00$ % ($+4{,}61\,u$) | $+0{,}00$ % | $+0{,}00$ % | 1,11 (inchangé) |

Deux enseignements. (i) $f_s$ et $Q_{ms}$ sont **immunisés** : ce sont une position et une forme, pas un niveau. (ii) $R_e$, $R_{es}$ et $L_e$ héritent *linéairement* de l'erreur de $R_{ref}$, et le $\chi^2$ ne bronche pas — l'erreur est invisible pour les trois estimateurs. Avec une résistance ordinaire à 3 %, le biais sur $R_e$ vaut près de $7\,u_{cov}$ : l'incertitude dominante ne serait pas celle qu'on affiche. **Prescriptions** : acheter la $R_{ref}$ à 1 % (déjà dans la liste d'achats de la phase 1), la mesurer au multimètre (4 fils si possible) et reporter $u(R_{ref})/R_{ref}$ en quadrature sur $R_e$, $R_{es}$, $L_e$ ; relever $R_e$ au multimètre **avant et après** le balayage — 69 points relevés à la main prennent une à deux heures et le cuivre gagne 0,4 %/K, l'écart avant/après est une composante $u_B$ de dérive thermique à comptabiliser, pas à ignorer ; retrancher la résistance des cordons de la lecture de $R_e$ [[valeur à mesurer en phase 1]].

**Ce que l'acte 3 reçoit vraiment.** L'objet livré n'est pas $\theta$ mais la courbe $Z(f;\hat\theta)$ *avec son incertitude*. En propageant la covariance complète, $u(\lvert Z\rvert)^2 = G\operatorname{Cov}G^{\mathsf T}$ avec $G_j = \partial\lvert Z\rvert/\partial\theta_j$ :

| $f$ | 40 Hz (pic) | **100 Hz (raccord)** | 200 Hz |
|---|---|---|---|
| $\lvert Z\rvert$ | 50,51 Ω | **14,15 Ω** | 8,01 Ω |
| $u(\lvert Z\rvert)$ | 0,294 Ω (0,58 %) | **0,049 Ω (0,35 %)** | 0,026 Ω (0,32 %) |

C'est la figure la plus utile de l'acte 2 : elle dit *à la fréquence du raccord* combien on connaît réellement la charge — 0,35 % en $u_A$, à comparer au 1 % de $u_B$ apporté par $R_{ref}$, qui domine donc largement. Le contrôle croise le nombre de la mémoire projet : $\lvert Z(100\ \text{Hz})\rvert \approx 14\ \Omega$ pour le modèle v1.

### <a id="s03-6"></a>03.6 Bande d'ajustement : le vrai risque n'est pas la variance sur $L_e$, c'est un biais sur $R_e$

Le tableau « bande » de la sortie montre que $u(L_e)$ passe de 0,085 mH (7 %) pour une mesure arrêtée à 150 Hz, à 0,014 mH (1 %) à 500 Hz. La raison est visible dans les nombres du modèle à 500 Hz : $Z_{mot} = 0{,}09 - 2{,}02j\ \Omega$ (la branche motionnelle, au-dessus de sa résonance, est *capacitive*) contre $j\omega L_e = +3{,}77j\ \Omega$. Les deux termes imaginaires se compensent à 54 % : $L_e$ n'est bien visible que là où $\omega L_e$ domine la queue motionnelle, c'est-à-dire *au-dessus* de la bande du raccord — et c'est pour cela que l'initialisation de $L_e$ (§ 03.3) retranche la queue motionnelle avant de diviser par $\omega$.

Mais **ce n'est pas là le vrai danger**. Le modèle $L_e$ = constante n'a pas de partie réelle croissante, alors que la bobine réelle en a une (pertes par courants de Foucault : la résistance apparente croît avec la fréquence). L'ajustement, forcé de rendre compte d'un $\operatorname{Re}Z$ qui monte, **absorbe cette croissance en gonflant $R_e$** — le paramètre en apparence le mieux déterminé, et en réalité le plus faux. Test C sur des données $K(j\omega)^{0{,}7}$ avec $R_e$ vrai $= 6{,}500\ \Omega$ :

| Bande d'ajustement | $R_e$ obtenu | biais | en $u_{cov}$ | $s^2$ | $z$ (séquences) |
|---|---|---|---|---|---|
| 10–200 Hz | $6{,}945 \pm 0{,}043$ | $+6{,}8$ % | $+10{,}3$ | 2,28 | $-1{,}3$ |
| 10–300 Hz | $7{,}076 \pm 0{,}046$ | $+8{,}9$ % | $+12{,}5$ | 3,28 | $-3{,}1$ |
| 10–500 Hz | $7{,}267 \pm 0{,}053$ | $+11{,}8$ % | $+14{,}4$ | 5,37 | $-5{,}6$ |
| 10–1000 Hz | $7{,}560 \pm 0{,}068$ | $+16{,}3$ % | $+15{,}5$ | 10,41 | $-6{,}5$ |

Trois conclusions. (i) **Restreindre la bande ne guérit pas** : même à 10–200 Hz, le biais vaut $+7$ % et dix écarts-types. Le repli « réduire la bande d'ajustement » envisagé en v1 est donc insuffisant — il faut le dire. (ii) Le biais est invisible dans $u_{cov}$ mais parfaitement visible dans $s^2$ et dans le test des séquences. (iii) Le remède qui marche est le **modèle à 6 paramètres** $Z = R_e + K(j\omega)^n + Z_{mot}$ : sur les mêmes données étendues à 2 kHz, il rend $R_e = 6{,}475 \pm 0{,}031$ et $n = 0{,}696 \pm 0{,}005$ (valeur vraie 0,700) avec $s^2 = 0{,}86$ — l'exposant *est* identifiable et le biais disparaît. Il est déjà écrit (`Z_semi`).

**Règle retenue pour la phase 2.** Mesurer 10–1000 Hz (pour *voir* la dérive), ajuster d'abord le modèle à 5 paramètres sur 10–500 Hz, puis lire $s^2$ et le test des séquences. **Il faut s'attendre à ce que ce premier ajustement échoue aux critères 1 et 6** — et ce n'est pas un échec, c'est un résultat : c'est la mesure qui dit que la bobine a des pertes. On bascule alors sur `Z_semi`, on rapporte les deux ajustements côte à côte, et on discute $n$. C'est un bon moment d'oral : on part d'un modèle de cours, on montre qu'il ne passe pas le test, et on en tire de la physique.

Pour l'acte 3, la question utile n'est d'ailleurs pas « $L_e$ à 1 % ou à 7 % » mais « de combien la réponse du filtre optimisé bouge-t-elle quand $\theta$ bouge de $u$ ». C'est à cela que sert le livrable Monte-Carlo du § 03.8 : on repasse les 300 tirages dans l'optimiseur de l'acte 3 et on regarde la dispersion de la réponse à 100 Hz. Le tableau « précision nécessaire par paramètre » qui en sortira est le chaînon qui ferme la boucle entre l'acte 2 et l'acte 3, et il justifiera *a posteriori* la bande 10–500 Hz [[à produire en phase 3]].

### <a id="s03-7"></a>03.7 Critères de validation de l'identification (à geler avant l'ajustement sur les vraies mesures)

**0. Aiguillage du modèle — désormais une VÉRIFICATION, plus un aiguillage** (avant tout ajustement). Le type de caisse est connu : **bass-reflex à deux évents**, donc modèle `Z_bassreflex8` par défaut. Le comptage automatique reste en place, mais il change de rôle : il ne choisit plus, il **confirme**. Compter les maxima locaux de $\lvert Z\rvert$ entre 10 et 100 Hz sur la courbe mesurée **lissée par moyenne glissante sur 3 points** (le lissage est indispensable : sur la courbe brute, le bruit crée des maxima parasites — `modele_hp.diagnostic_caisse` le fait et lève un avertissement explicite si l'on présente des données à deux pics à un modèle à cinq paramètres). Sur le jeu synthétique : 1 pour la caisse close, 3 pour le bass-reflex (dont un parasite : le critère est « $\ge 2$ », pas « exactement 2 »).

> **Que faire si le comptage rend 1 alors qu'on attend 2 ?** Ce n'est alors *pas* une raison de basculer sur le modèle à 5 paramètres : c'est un **défaut de mesure**, à traiter comme tel. Trois causes, dans l'ordre de probabilité : (i) la grille n'est pas descendue assez bas et $f_L$ (≈ 16 Hz sur le modèle) est hors bande ; (ii) la grille est trop lâche autour des pics — ils font 0,16 octave, une grille au 1/12 n'y place que 2 points (§ 02.6) ; (iii) le niveau d'excitation a écrasé le pic (sortie du régime petits signaux, § 02.5). **On refait la mesure, on ne change pas de modèle.** Passer à 5 paramètres pour faire converger un ajustement serait exactement l'erreur que le test D du § 03.4 sert à rendre visible.

**0 bis. Exécution systématique du modèle à 5 paramètres, en contrôle.** Sur chaque jeu de mesures du sub, ajuster *aussi* `Z_ts` et rapporter son $s^2$ à côté de celui de `Z_bassreflex8`. Attendu : un rapport de deux ordres de grandeur (93 contre ≈ 1 sur le jeu synthétique). C'est gratuit, cela se met sur une seule figure, et c'est la démonstration la plus lisible qu'un jury puisse recevoir de ce que veut dire « le modèle est faux » : deux courbes également « jolies », deux $\chi^2$ qui n'ont rien à voir.

1. **$\chi^2$ réduit** $s^2 \in [0{,}5\,;\,2]$ avec les $u_k$ étalonnés en phase 1. Fourchette volontairement large : pour $2N - p = 133$ degrés de liberté, la dispersion purement statistique de $s^2$ n'est que de $\sqrt{2/133} = 0{,}12$ (intervalle à 3 σ : $[0{,}63\,;\,1{,}37]$), et sur 300 réalisations $s^2$ n'est jamais sorti de $[0{,}59\,;\,1{,}31]$. Sortir de $[0{,}5\,;\,2]$ ne peut donc **pas** venir du hasard de la mesure : c'est un défaut de modèle ou une erreur d'un facteur sur les $u_k$ — diagnostiquer, ne pas « ajuster les $u$ pour que ça passe ». Signal d'alerte non bloquant : $\lvert s^2 - 1\rvert > 3\sqrt{2/(2N-p)}$.
2. **Résidu relatif** RMS sur $\lvert Z\rvert$ et sur $\varphi$ du même ordre que l'incertitude de chaîne, **calculé sur 20–300 Hz** (la bande de la porte de validation de la feuille de route, à ne pas confondre avec la bande d'ajustement 10–500 Hz). Sur le jeu synthétique : 2,03 % et 1,00° pour un bruit injecté de 2 % et 1°.
3. **Absence de structure dans les résidus**, chiffrée par le test des séquences de Wald-Wolfowitz sur les signes : le nombre de suites $R$ doit être compatible avec $E[R] = 1 + 2n_+n_-/N$ à $\pm 3$ écarts-types ($\lvert z\rvert < 3$), **séparément sur le module et sur la phase**. Et moyenne des résidus normalisés compatible avec 0 sur chacune des trois sous-bandes (sous le pic, autour du pic, au-dessus de 200 Hz). Ce critère est le plus discriminant de tous : sur le bon modèle $z = +0{,}41$ et $-0{,}11$ ; sur des données semi-inductives ajustées avec $L_e$ constante, $z = -5{,}6$ ; sur un bass-reflex ajusté par le modèle clos, $z = -5{,}4$. *(Le critère qualitatif « pas de suite de signes identiques sur plusieurs points » serait piégeux : la plus longue suite vaut 6 sur le jeu synthétique, pour $\log_2 69 \approx 6$ attendus par pur hasard.)*
4. **Stabilité (conditionnement, pas adéquation).** Sous retrait aléatoire de 20 % des fréquences (200 tirages), l'écart-type des estimations doit être compris entre **0,7 et 1,4 fois** la valeur attendue $u_{cov}\sqrt{d/(n-d)} = 0{,}50\,u_{cov}$ (observé sur le jeu synthétique : rapports 1,06 à 1,21), et la moyenne des 200 sous-échantillons doit rester à moins de $0{,}2\,u$ de l'ajustement complet. Un rapport nettement supérieur à 1 signale un ou deux points à fort levier qui portent seuls l'ajustement : on identifie alors le coupable par $h_{kk}$. **À écrire noir sur blanc : ce critère ne teste pas l'adéquation du modèle** — il passe sur des données où le modèle est démontrablement faux (test C).
5. **Concordance** $u_{cov} \approx u_{MC} \approx u_{jack}$ (à un facteur 1,5 près). Rappel du § 03.5 : cela valide la linéarisation, pas le réalisme des $u_k$.
6. **Plausibilité physique** : $R_e$ ajusté compatible avec le multimètre à $2\,u$ **après retrait de la résistance des cordons et compte tenu de $u_B(R_{ref})$** ; $f_s$ en caisse close supérieure au $f_s$ datasheet ; $Q_{ms}$, $Q_{es}$ dans les ordres de grandeur du constructeur [[datasheet à obtenir]].
7. **Test à blanc du code**, exécuté sur données synthétiques (test A) et à refaire sur les dipôles réels de l'étalonnage de la phase 1 : pour $Z = R + j\omega L$, retrouver la résistance étalon à $2\,u$ avec $s^2 \approx 1$ ; pour $Z = R_s + 1/(j\omega C)$, retrouver le condensateur connu à $2\,u$ sur deux décades. Si le code ne retrouve pas une résistance, il ne retrouvera pas un haut-parleur.
8. **Unicité du minimum** : multi-départ de 50 tirages autour de l'initialisation ; le meilleur coût doit être atteint par une nette majorité des départs, et tout minimum concurrent doit être écarté par son $\chi^2$ (facteur $10^3$ ici), pas par une préférence.
9. **Contrôle croisé de $f_b$ : trois voies indépendantes vers la même grandeur.** C'est le critère le plus convaincant que le bass-reflex ait apporté au projet, et il ne coûte que dix minutes de pied à coulisse. On compare :
   - $f_b^{\text{géo}}$, **prédit** avant toute mesure à partir des cotes des deux évents et du volume net (§ 01.10 bis), sous forme d'**intervalle** (la convention de correction de bout vaut ±3 %, davantage que l'incertitude de mesure) ;
   - $f_b^{\text{creux}}$, **lu** sur la courbe mesurée, au passage par zéro de la phase entre les deux pics plutôt qu'à l'argmin du module (§ 02.6 : le creux est plat, la phase est raide) ;
   - $f_b^{\text{ajusté}}$, **estimé** par `Z_bassreflex8`, avec son $u$ issu de la covariance.

   **Seuil, et biais connus à corriger avant de comparer.** Les deux dernières voies ne visent pas exactement la même chose : sur le modèle du § 01.10 ($f_b = 35{,}0$ Hz vrai, $Q_l = 7$), l'argmin du module tombe à 34,2 Hz ($-2{,}3$ %) et le zéro de phase à 33,5 Hz ($-4{,}3$ %). **Le creux est donc un estimateur biaisé de quelques pour-cent**, d'autant plus que les pertes sont fortes ; seul l'ajustement rend $f_b$ sans biais. Critère gelé : $\lvert f_b^{\text{ajusté}} - f_b^{\text{creux}}\rvert / f_b \le 6\ \%$ (le biais de modèle, doublé pour la marge), et $f_b^{\text{ajusté}}$ **à l'intérieur de l'intervalle géométrique élargi de 5 %**.
   **Interprétation des désaccords — c'est là que le critère devient utile** :
   | Constat | Diagnostic |
   |---|---|
   | les trois concordent | modèle de caisse validé **indépendamment de l'ajustement** : c'est le résultat à montrer |
   | géométrie et creux d'accord, ajustement à l'écart | **l'ajustement est en cause** (minimum parasite, bande mal choisie, $\alpha$ mal contraint) — relancer un multi-départ |
   | ajustement et creux d'accord, géométrie à l'écart | **le relevé géométrique est en cause** : volume net surestimé (le terme dominant, § 01.10 bis), évents non identiques, ou correction de bout mal choisie (les deux évents sont-ils proches l'un de l'autre ?) |
   | rien ne concorde | avant tout, refaire la mesure : c'est le symptôme d'une grille qui ne résout pas les accidents (§ 02.6) |

   Trois voies indépendantes vers une même grandeur, chacune avec son incertitude et ses biais énoncés, c'est **exactement la structure qu'un jury de TIPE attend** — bien plus qu'un ajustement isolé, si beau soit son $\chi^2$.

Critères associés déjà gelés ailleurs : la règle de traitement des points aberrants (§ 03.2) et la convention `absolute_sigma` (§ 03.5).

### <a id="s03-8"></a>03.8 Ce qu'il faut présenter au jury, et ce qu'il faut livrer à l'acte 3

- **Une figure** à trois panneaux, axe des fréquences logarithmique : $\lvert Z\rvert$ (points mesurés avec barres d'erreur + courbe du modèle + bande $\pm 2u$ issue de la covariance complète), $\varphi$ (idem), résidus normalisés $r_k$. Annoter $f_s$ et $Z_{max}$. La figure `fit_synthetique.png` produite par le script est le gabarit — mais telle quelle elle est en **portrait** ($840 \times 960$ px, 67 ko) : pour une diapo 4/3 il faudra la recomposer en deux colonnes (module et phase à gauche, résidus à droite) ou n'en projeter qu'un panneau, le troisième restant en annexe. Vérifier la lisibilité du panneau des résidus une fois réduit.
- **Lecture des résidus, avec le bon seuil.** Les $r_k$ doivent rester dans $\pm 3$ **à un ou deux points près** : pour 138 résidus, on attend $138 \times 0{,}0027 = 0{,}4$ dépassement en moyenne, et un ajustement *parfait* sort de $\pm 3$ dans 31 % des cas (sur 300 réalisations, $\max\lvert r\rvert$ est monté jusqu'à 4,3). Alerte à partir de $\lvert r\rvert > 4$, ou de plusieurs dépassements groupés dans la même zone de fréquence. Sur le jeu synthétique : $\max\lvert r\rvert = 2{,}98$, zéro dépassement.
- **Un tableau** paramètres $\pm u$ (deux chiffres significatifs sur $u$), avec $Q_{es}$ et $Q_{ts}$ dérivés des tirages Monte-Carlo, une colonne « datasheet » pour la confrontation, la séparation $u_A$ / $u_B$, et la matrice de corrélation en annexe.
- **Un livrable formel pour l'acte 3**, écrit par le script : `ts_theta.csv` ($\hat\theta$ et $u$), `ts_cov.csv` (la matrice $5\times5$ complète) et `ts_mc.csv` (les 300 tirages Monte-Carlo). Sans cet artefact, la phase 3 repartirait de cinq $u$ indépendants — exactement l'erreur que cette section dénonce.
- **Une phrase de méthode** : « je cherche les cinq nombres qui minimisent la somme des écarts pondérés au carré entre la courbe mesurée et le modèle ; comme le modèle n'est pas linéaire, je le linéarise et j'itère (Gauss-Newton, amorti à la Levenberg-Marquardt) ; l'incertitude vient de la matrice $(J^{\mathsf T}J)^{-1}$, recoupée par Monte-Carlo et par jackknife ».
- **Questions à anticiper.**
  - *« Comment savez-vous que c'est le bon minimum ? »* — Réponse honnête : il existe au moins un minimum parasite ($L_e \to 0$, $Q_{ms}$ très grand). Mais il se reconnaît instantanément à son coût, $\chi^2$ réduit de l'ordre de $10^3$ contre 1,1. Je fais donc un multi-départ (200 tirages dans un facteur 0,2 à 5 : 94 % retrouvent le minimum global) et je garde le coût le plus bas ; l'initialisation lue sur la courbe évite le piège dès le premier essai.
  - *« Pourquoi $R_{es}$ et $Q_{ms}$ sont-ils corrélés à 0,83 ? »* — Flancs du pic, § 03.5 ; et non, fixer $R_e$ au multimètre n'y change rien.
  - *« Pourquoi ne pas utiliser les points mesurés directement ? »* — Lissage, interpolation, propagation des incertitudes.
  - *« Que vaut votre modèle à 1 kHz ? »* — $L_e$ constante y est faux ; le symptôme n'est pas une grande incertitude, c'est un biais de $+16$ % sur $R_e$ (§ 03.6), d'où le modèle de repli à 6 paramètres.
  - *« Retrouvez-vous $V_{as}$ ? »* — Non : $Z(f)$ seule ne sépare pas $Bl$, $M_{ms}$, $C_{ms}$ ; inutile pour le filtre.
  - *« Et si votre résistance de référence est fausse ? »* — $f_s$ et $Q_{ms}$ n'y voient rien, $R_e$, $R_{es}$ et $L_e$ se décalent du même pourcentage sans que le $\chi^2$ bouge : c'est une incertitude de type B, comptabilisée à part.

**Perspective de sobriété numérique.** L'ajustement coûte 8 évaluations du vecteur résidu, soit **48 appels au modèle direct** — car scipy calcule la jacobienne par différences finies (5 appels supplémentaires par évaluation jacobienne). Les dérivées de $Z$ se calculent pourtant à la main en trois lignes ($\partial Z/\partial R_e = 1$, $\partial Z/\partial L_e = j\omega$, $\partial Z/\partial R_{es} = Z_{mot}/R_{es}$, etc.) ; les fournir via l'argument `jac=` ferait tomber les 40 appels de différences finies à 8. C'est un exercice de niveau prépa, et un argument cohérent avec le thème du TIPE [[à faire si le temps le permet]].

> **Ce qu'il faut retenir pour l'oral**
> - Le modèle direct tient en une formule : $Z = R_e + j\omega L_e + R_{es}/[1 + jQ_{ms}(f/f_s - f_s/f)]$ ; chacun des cinq paramètres se lit sur la courbe, ce qui fournit l'initialisation. Mais cette formule décrit une caisse **close** : la nôtre est **bass-reflex à deux évents**, donc le modèle par défaut a **huit** paramètres (`Z_bassreflex8`), la branche d'évent shuntant la branche motionnelle. Les cinq paramètres restent au dossier comme contrôle : ajustés sur des données à deux pics, ils convergent sans broncher vers des nombres plausibles et faux ($s^2 = 93$ contre ≈ 1) — c'est la meilleure démonstration de ce que vaut un « ça a convergé ».
> - **$f_b$ se recoupe par trois voies indépendantes** : prédiction géométrique au pied à coulisse (Helmholtz, § 01.10 bis), lecture du creux d'impédance, et paramètre ajusté. Chacune a son biais, que j'annonce : le creux est décalé de quelques pour-cent par les pertes, la prédiction géométrique est un intervalle à ±3 % à cause de la correction de bout. Les faire concorder valide le modèle de caisse **sans passer par l'ajustement**.
> - Le problème inverse est un problème de moindres carrés *pondérés* : on minimise $\sum r_k^2$ avec $r_k$ = écart / incertitude, et le $\chi^2$ réduit ≈ 1 valide à la fois le modèle et les incertitudes de chaîne. C'est la « procédure de validation par les écarts normalisés » du programme.
> - Non linéaire ⇒ Gauss-Newton amorti (Levenberg-Marquardt) ; je l'ai réécrit en numpy pur pour ne pas dépendre d'une boîte noire, et il retrouve scipy à $6\times10^{-8}$ près.
> - Les incertitudes sont **calibrées** : sur 300 réalisations de bruit, l'écart à la valeur vraie reste sous $u$ dans 65 à 71 % des cas (68 % attendus) et sous $2u$ dans 95 à 96 %. $R_{es}$ et $Q_{ms}$ sont corrélés à 0,83 : on propage la covariance complète, pas cinq $u$ indépendants.
> - Trois estimateurs (covariance, Monte-Carlo, jackknife) concordent — mais ils ne mesurent que l'aléatoire. L'incertitude **systématique** (tolérance de $R_{ref}$, dérive thermique) est invisible pour eux et déplace $R_e$, $R_{es}$, $L_e$ d'autant de pour-cent que $R_{ref}$ est fausse, sans que le $\chi^2$ bouge. $f_s$ et $Q_{ms}$, eux, y sont immunisés.
> - Un modèle inadapté ne plante pas : il converge et rend des nombres plausibles. Ce qui le trahit, c'est $s^2$ et le test des séquences sur les signes des résidus ($z = -5{,}6$ pour une bobine à pertes ajustée avec $L_e$ constante, contre $+0{,}4$ pour le bon modèle).
> - À 100 Hz — la fréquence du raccord — le modèle donne $\lvert Z\rvert$ à 0,35 % près en aléatoire ; c'est cette bande, pas les cinq paramètres, que reçoit l'acte 3.

### Sources

- A. N. Thiele, « Loudspeakers in Vented Boxes: Part 1 », *J. Audio Eng. Soc.*, vol. 19, n° 5, p. 382–392, mai 1971 ; « Part 2 », vol. 19, n° 6, p. 471–483, juin 1971 — modèle électrique équivalent du haut-parleur en caisse.
- R. H. Small, « Direct-Radiator Loudspeaker System Analysis », *J. Audio Eng. Soc.*, vol. 20, n° 5, p. 383–395, juin 1972 — définition de $Q_{ms}$, $Q_{es}$, $Q_{ts}$.
- R. H. Small, « Closed-Box Loudspeaker Systems, Part 1: Analysis », *J. Audio Eng. Soc.*, vol. 20, n° 10, p. 798–808, déc. 1972 — décalage de la résonance en caisse close, **et** détermination des paramètres à partir de la mesure d'impédance de bobine (c'est le résumé de *cet* article, et non de « Direct-Radiator », qui annonce la méthode ; d'où l'attribution corrigée). La formule $Q_{ms} = f_s\sqrt{r_0}/(f_2 - f_1)$ avec $Z_0 = \sqrt{R_e Z_{max}}$, $Q_{es} = Q_{ms}/(r_0 - 1)$, $Q_{ts} = Q_{ms}Q_{es}/(Q_{ms}+Q_{es})$ est par ailleurs confirmée par une source industrielle indépendante et redémontrée exactement au § 03.3. [[attribution à confirmer sur le texte original : les scans AES accessibles en ligne sont des images sans couche texte — à demander au CDI]]
- J. Vanderkooy, « A Model of Loudspeaker Driver Impedance Incorporating Eddy Currents in the Pole Structure », *J. Audio Eng. Soc.*, vol. 37, n° 3, p. 119–128, mars 1989 — origine physique de la semi-inductance.
- W. M. Leach Jr., « Loudspeaker Voice-Coil Inductance Losses: Circuit Models, Parameter Estimation, and Effect on Frequency Response », *J. Audio Eng. Soc.*, vol. 50, n° 6, p. 442–450, juin 2002 — modèle $K(j\omega)^n$ et estimation de ses paramètres. *(Certaines bibliographies citent par erreur le n° 3 ; la fiche AES donne le n° 6, p. 442–450.)*
- I. Mateljan et M. Sikora, « Estimation of Loudspeaker Driver Parameters », 6ᵉ congrès de l'Alps Adria Acoustics Association, Petrčane (Croatie), 12–14 septembre 2012, communication ELA-02, 6 p. — **exactement la méthode de cette section** : ajustement par moindres carrés non linéaires (Levenberg-Marquardt, MINPACK) de l'impédance mesurée, avec initialisation semi-analytique et comparaison des modèles de bobine à pertes ($L_2R$, $L_3R$, $L_2RK$ de Thorborg). Implémentée dans le logiciel LIMP/ARTA. https://artalabs.hr/papers/Mateljan-ELA-02.pdf
- SciPy 1.18, documentation de `scipy.optimize.least_squares` (fonction de coût $\tfrac12\sum\rho(f_i^2)$, méthodes `trf`/`dogbox`/`lm`, `x_scale`, `loss`, `active_mask`, attribut `jac` : « $J^{\mathsf T}J$ is a Gauss-Newton approximation of the Hessian of the cost function ») et de `scipy.optimize.curve_fit` (option `absolute_sigma`) : https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html
- Programme de physique-chimie 2021 des CPGE, annexe « Mesures et incertitudes », capacité exigible citée au § 03.2 — formulation **identique en PT et en PSI** (vérifié dans les deux PDF, page 6) : voie PT https://prepas.org/ups.php?document=96 , voie PSI https://prepas.org/ups.php?document=94 . [[filière à confirmer : PT ou PSI]] *(L'URL upsti.fr utilisée en v1 renvoie une erreur 404 : remplacée.)* Programme d'informatique du tronc commun PTSI-PT (2021), méthode de Newton : https://sti.eduscol.education.fr/textes/programme-dinformatique-du-tronc-commun-cpge-ptsi-pt-2021 (URL vérifiée) [[semestre exact à vérifier]].
- `archive-v1/_gen.py` (dépôt du projet, ligne 68) — modèle d'impédance illustratif dont les paramètres arbitraires ($R_e = 6{,}5\ \Omega$, $L_e = 1{,}2$ mH, $R_{es} = 44\ \Omega$, $f_s = 40$ Hz, $L_{ces} = 0{,}1$ H) servent de « vérité » aux tests synthétiques.
- Scripts exécutés pour cette section (scratchpad de session, à verser dans `analyse/` en phase 1) : `fit_ts.py` (bibliothèque), `main_ts.py` (test de méthode), `diag_ts.py` (huit tests de diagnostic), `verif_formules.py`, `variante_complexe.py`.

## <a id="s04"></a>04. Filtre de raccord sur charge réelle et formulation de l'optimisation

> **Statut.** Section de référence rédigée en phase 0 (septembre 2026). Tous les chiffres sont **calculés**, soit sur 8 Ω résistif, soit sur un modèle de haut-parleur **typique** (paramètres illustratifs hérités de `archive-v1/_gen.py`, jamais mesurés). **Rien n'a été mesuré sur l'enceinte de Thomas** : toute valeur marquée [[à mesurer]] sera remplacée par les résultats des phases 1–2. Scripts exécutés (scratchpad `sec04/`) : `verif_cellules.py`, `verif_sommation.py`, `verif_zobel.py`, `optim_e12_squelette.py`, `verif_sallen_key.py` ; contrôles croisés de la présente rédaction dans `sec04f/` (`v1_fc.py`, `v2_sk.py`, `v3_puissance.py`, `v4_divers.py`, `v5_optim.py`, `v6_ltspice.py`, `v7_sensib.py`). Python 3.13.2, numpy 2.4.6, scipy 1.18.1. **L'énumération exhaustive — la méthode de référence — ne demande que numpy** ; `scipy` n'intervient que pour le recoupement continu du § 04.7, qui est facultatif.

### <a id="s04-1"></a>04.1 Cellules passives du second ordre chargées par une impédance quelconque

Le filtre « catalogue » (§ 03) est constitué de deux cellules LC. La self réelle a une résistance série $r$ (DCR) que l'on garde dans toutes les expressions.

| Voie | Topologie | Composants (catalogue) |
|---|---|---|
| Passe-bas (sub) | $L_1$ (+ $r_1$) **en série**, puis $C_1$ **en parallèle** sur la charge $Z$ | 18 mH, 150 µF |
| Passe-haut (médiums) | $C_2$ **en série**, puis $L_2$ (+ $r_2$) **en parallèle** sur la charge $Z$ | 150 µF, 18 mH |

Les fonctions de transfert **exactes** (tension aux bornes du HP / tension d'entrée), pour une charge $Z(j\omega)$ quelconque, s'obtiennent par deux diviseurs de tension :

$$
H_{PB}(j\omega)=\frac{Z_\parallel}{j\omega L_1+r_1+Z_\parallel},\qquad Z_\parallel = Z \parallel \frac{1}{j\omega C_1}=\frac{Z}{1+j\omega C_1 Z}
$$

$$
H_{PH}(j\omega)=\frac{Z'_\parallel}{\dfrac{1}{j\omega C_2}+Z'_\parallel},\qquad Z'_\parallel=(j\omega L_2+r_2)\parallel Z=\frac{(j\omega L_2+r_2)\,Z}{j\omega L_2+r_2+Z}
$$

**Cas d'une charge résistive $Z=R$, $r=0$.** Les deux cellules partagent le même dénominateur :

$$
H_{PB}=\frac{1}{1+j\omega\frac{L}{R}+(j\omega)^2LC},\qquad H_{PH}=\frac{(j\omega)^2LC}{1+j\omega\frac{L}{R}+(j\omega)^2LC},\qquad
\omega_0=\frac{1}{\sqrt{LC}},\quad Q=R\sqrt{\frac{C}{L}}
$$

Le facteur de qualité est fixé par la **charge**, pas par le filtre seul : c'est la racine du problème v2. Pour Butterworth ($Q=1/\sqrt2$) à 100 Hz sur 8 Ω : $L=\sqrt2R/\omega_0=18{,}01$ mH, $C=1/(\sqrt2R\omega_0)=140{,}7$ µF.

**Vérification numérique** (`verif_cellules.py`, cellules chargées par $Z=8$ Ω, $r=0$) :

```
Butterworth 100 Hz / 8 ohm : L = 18.01 mH, C = 140.7 uF
  f =    50 Hz : PB   -0.26 dB /   -43.3 deg   PH  -12.30 dB /   136.7 deg
  f =   100 Hz : PB   -3.01 dB /   -90.0 deg   PH   -3.01 dB /    90.0 deg
  f =   200 Hz : PB  -12.30 dB /  -136.7 deg   PH   -0.26 dB /    43.3 deg
  f =  1000 Hz : PB  -40.00 dB /  -171.9 deg   PH   -0.00 dB /     8.1 deg
  ecart max |H_pb charge 8 ohm - H_Butterworth| = 4.0e-16
```

Les expressions exactes redonnent donc la forme normalisée $1/(1+\sqrt2\,jx+(jx)^2)$ à la précision machine.

**Avec les valeurs normalisées 18 mH / 150 µF sur 8 Ω** : $f_0=96{,}86$ Hz, $Q=0{,}7303$, point à mi-puissance (**−3,0103 dB**, cf. la convention de seuil ci-dessous) à **99,93 Hz** (PB) et **93,88 Hz** (PH). Contrôle croisé : $f_{PB}\times f_{PH}=9381{,}6=f_0^2$ exactement.

> <!-- ANCIENNE NOTE, CORRIGÉE LE 2026-09-13 : elle qualifiait « 99,8 / 94,0 » d'arrondis fautifs. C'est faux. Recalcul : au seuil LITTÉRAL de −3,000 dB on trouve 99,820 et 93,985 Hz (arrondis : 99,8 / 94,0) ; à la MI-PUISSANCE (−3,0103 dB) on trouve 99,931 et 93,881 Hz (arrondis : 99,9 / 93,9). Les deux couples vérifient f_PB × f_PH = f0² = 9381,59 Hz². Les deux couples sont exacts, chacun dans sa convention ; l'écart de 0,11 % est un écart de CONVENTION, pas une erreur d'arrondi. -->
> **Harmonisation des deux couples qui circulent dans le projet.** « 99,82 / 93,99 Hz » (arrondis : 99,8 / 94,0) est le seuil **littéral −3,000 dB** ; « 99,93 / 93,88 Hz » (arrondis : 99,9 / 93,9) est la **mi-puissance −3,0103 dB**. Ce sont **deux conventions différentes appliquées au même filtre**, toutes deux correctement calculées — et non un arrondi fautif : l'écart, 0,11 Hz sur 100, est exactement celui qu'impose le passage de $10^{-3{,}000/10}=0{,}50119$ à $\tfrac12$ sur $\lvert H\rvert^2$. La **convention de seuil** retenue pour tout le TIPE est la **mi-puissance** (cf. l'encadré suivant), donc **99,9 / 93,9 Hz** ; l'autre couple reste citable à condition d'être nommé « seuil littéral −3,000 dB ». Dans les deux cas, ce sont des **repères**, pas la définition de $f_c$.

#### <a id="s04-1-def"></a>Définition gelée de $f_c$ — la décision la plus importante de cette section

Le même filtre admet **quatre** « fréquences de coupure » qui ne coïncident pas dès que la self a une DCR ou que la charge n'est pas résistive. Le critère de FEUILLE-DE-ROUTE (« Précision de $f_c$ = $\lvert f_c$ réalisée $-100$ Hz$\rvert$ ») et la porte de validation de la phase 4 (±5 %) sont **inutilisables** tant que l'une d'elles n'est pas gelée.

> **Définition retenue pour tout le TIPE — unique, et seule à porter ce statut** (à reporter dans FEUILLE-DE-ROUTE.md ; tout autre passage du présent document qui semblerait « geler » une autre valeur est un **repère**, pas une définition) :
> $$\boxed{\;f_c \;=\; \text{l'unique } f\in[40;250]\text{ Hz telle que }\bigl\lvert H_{PB}(f)\,G_{sub}(f)\bigr\rvert=\bigl\lvert H_{PH}(f)\,G_{med}(f)\bigr\rvert\;}$$
> c'est-à-dire la **fréquence de croisement des deux voies** — notée aussi $f_x$ quand il faut lever toute ambiguïté. Les trois autres candidates ($f_0=1/2\pi\sqrt{LC}$, le −3 dB par rapport à 0 dB absolu, le −3 dB par rapport au gain de bande passante $K$) restent **citées comme repères explicitement nommés** (« le **pôle** », « le **−3 dB du passe-bas** », « le **−3 dB du passe-haut** ») dans le tableau ci-dessous et dans les sections suivantes — jamais sous le nom nu de « $f_c$ ».

**Convention de seuil, gelée avec la définition.** Partout où le document écrit « −3 dB », il faut lire **mi-puissance**, c'est-à-dire $\lvert H\rvert^2 = \tfrac12$, soit $-10\log_{10}2 = \mathbf{-3{,}0103}$ **dB** — la convention de REW et des logiciels de mesure, celle qu'il faut donc retenir pour que le calcul et la mesure soient comparables sans retouche. Le seuil **littéral** $-3{,}000$ dB correspond à $\lvert H\rvert^2 = 10^{-0{,}3} = 0{,}50119$, ce qui n'est pas tout à fait la moitié.

> **Conséquence à connaître, et à ne pas prendre pour une faute de calcul.** Sur le filtre catalogue 18 mH / 150 µF sur 8 Ω ($f_0 = 96{,}86$ Hz, $Q = 0{,}7303$), les deux couples de valeurs qui circulent dans le projet sont **tous deux exacts** :
>
> | Convention de seuil | $\lvert H\rvert^2$ visé | $-3$ dB du passe-bas | $-3$ dB du passe-haut |
> |---|---|---|---|
> | **Mi-puissance, $-3{,}0103$ dB (retenue)** | $1/2$ | **99,93 Hz** | **93,88 Hz** |
> | Seuil littéral, $-3{,}000$ dB | $0{,}50119$ | 99,82 Hz | 93,99 Hz |
>
> L'écart — 0,11 Hz, soit 0,11 % — est un écart de **convention**, pas un arrondi fautif : c'est exactement ce que produit le passage de $0{,}50119$ à $0{,}5$. Les deux couples vérifient d'ailleurs le même contrôle croisé $f_{PB}\times f_{PH}=f_0^2=9381{,}6$ Hz². Il est donc sans portée devant la porte de validation à ±5 % — mais il faut **choisir et s'y tenir**, sans quoi deux relevés du même filtre semblent se contredire.

Pourquoi celle-là. (i) C'est la seule qui soit **insensible à la perte d'insertion** : une atténuation commune aux deux voies déplace les deux « −3 dB absolus » sans rien changer au raccord. (ii) C'est la seule qui **reste interprétable sur la charge réelle**, où $\lvert H\rvert$ culmine à $+10{,}8$ dB : le croisement de $-3{,}01$ dB y tombe 14 dB sous le pic et ne désigne plus rien de physique. (iii) C'est **la grandeur qui gouverne la somme acoustique**, donc le critère « fidélité du raccord ». (iv) Elle se mesure directement : deux balayages de Bode, on lit l'intersection.

**Effet de la DCR sur charge résistive** (dérivation exacte, vérifiée à $5\cdot10^{-16}$ près) :

$$
H_{PB}=\frac{K}{1+\dfrac{jx}{Q}+(jx)^2},\quad K=\frac{R}{R+r},\quad \omega_0=\sqrt{\frac{R+r}{LCR}},\quad Q=\frac{R+r}{\omega_0\,(L+rRC)},\quad x=\frac{\omega}{\omega_0}
$$

| $r$ (Ω) | $K$ (dB) | pôle $f_0$ (Hz) | $Q$ | $f$ à −3 dB / **0 dB** (Hz) | $f$ à −3 dB / **$K$** (Hz) | **$f_c$ croisement** (Hz) | chaleur $r/(R+r)$ |
|---|---|---|---|---|---|---|---|
| 0 | 0,00 | 96,9 | 0,730 | 99,9 | 99,9 | **96,86** | 0 % |
| 0,5 | −0,53 | 99,8 | 0,728 | 96,7 | 102,8 | **96,81** | 5,9 % |
| 1,0 | −1,02 | 102,7 | 0,726 | 92,8 | 105,4 | **96,66** | 11,1 % |
| 2,0 | −1,94 | 108,3 | 0,720 | 81,5 | 110,3 | **96,05** | 20,0 % |

Ce tableau est l'argument. Quand la DCR passe de 0 à 2 Ω, le « −3 dB absolu » **descend** de 18 % (99,9 → 81,5 Hz) et le « −3 dB relatif à $K$ » **monte** de 10 % (99,9 → 110,3 Hz) — la même réalité physique, notée $-18\,\%$ ou $+10\,\%$ selon la convention. Le croisement, lui, ne bouge que de **0,8 %** : il sépare proprement ce que la DCR fait vraiment, c'est-à-dire une **perte d'insertion** $K$ et un déplacement du pôle, d'un déplacement du raccord qui n'a pas lieu.

La DCR agit donc trois fois : perte d'insertion $K$, léger déplacement du pôle, et (sur charge réelle, § 04.2) amortissement du pic. C'est pourquoi elle est à la fois un **terme de pertes** et un **paramètre de forme** dans la fonction de coût.

### <a id="s04-2"></a>04.2 La même cellule sur une charge $Z(f)$ réaliste

**Modèle T-S électrique** (celui que la phase 2 ajustera) : $Z(j\omega)=R_e+j\omega L_e+\left(\frac{1}{R_{es}}+\frac{1}{j\omega L_{es}}+j\omega C_{es}\right)^{-1}$, reparamétré en $(R_e,L_e,R_{es},f_s,Q_{ms})$ avec $L_{es}=R_{es}/(\omega_sQ_{ms})$ et $C_{es}=Q_{ms}/(\omega_sR_{es})$.

| Paramètres **typiques** (ordre de grandeur, PAS une mesure) | $R_e$ | $L_e$ | $R_{es}$ | $f_s$ | $Q_{ms}$ | pic $\lvert Z\rvert$ | $Z(100\text{ Hz})$ | max/min 20–500 Hz |
|---|---|---|---|---|---|---|---|---|
| Sub 18″ (modèle v1) | 6,5 Ω | 1,2 mH | 44 Ω | 40 Hz | 1,75 | 50,5 Ω à 39,9 Hz | 14,1 Ω ∠−47,5° | 7,6 |
| Bloc médiums 2×4 Ω série | 6,4 Ω | 0,5 mH | 30 Ω | 60 Hz | 3,0 | 36,4 Ω à 60 Hz | 12,2 Ω ∠−42,2° | 5,6 |

Valeurs réelles du sub et des médiums : [[à mesurer]] (phase 1) ; le « simple au sextuple » de la problématique est cohérent avec ce modèle (7,6) mais n'est étayé par aucune mesure. **Ce modèle n'a qu'une branche motionnelle, donc un seul pic : il suppose la caisse close, ce qui n'est PAS le cas de l'enceinte.**

> **Ce que le constat du 16 septembre 2026 change ici.** Le sub est **bass-reflex à deux évents** (§ 01.10) : la charge du passe-bas a **deux pics et un creux**, et sur un jeu plausible le **second pic tombe à 86 Hz**, c'est-à-dire dans la zone de raccord. Les tableaux ci-dessous, établis sur une charge à un seul pic, restent valables comme **illustration de méthode** — ils montrent *comment* une charge non résistive déforme un filtre — mais ils **sous-estiment le cas réel** : à 100 Hz le modèle bass-reflex donne $\lvert Z\rvert = 22{,}4$ Ω contre 14,1 Ω pour le modèle typique à un pic. Ce qui suit est donc à lire comme une borne basse de l'effet. Les valeurs définitives viendront de $\underline{Z}(f)$ mesurée puis ajustée par `Z_bassreflex8`.
>
> **Et la charge du passe-haut n'est pas le bloc médiums seul.** Deux pavillons d'ultra-aigu sont câblés **en parallèle** des médiums (§ 02.6). Acoustiquement ils sont hors périmètre ; **électriquement ils sont dans la charge**. Selon qu'un condensateur de protection les découple ou non [[à vérifier]], et **les deux pavillons comptés en parallèle** (§ 02.6, jeu `MED_TYP`), $\lvert Z\rvert$ du bloc à 100 Hz passe de 29,3 Ω à 26,3–21,8 Ω (avec condensateur de 3,3 à 10 µF : $-0{,}9$ à $-2{,}6$ dB, **pas négligeable**) ou à **3,7 Ω** (sans : $-17{,}9$ dB, sous le minimum de 4 Ω du E-800). *Les chiffres de ce paragraphe sont donnés sur `MED_TYP` et non sur le jeu illustratif à 12,2 Ω du présent §, pour qu'il n'y ait qu'un seul jeu dans tout le projet : un effet négligeable devant un bloc à 12 Ω ne l'est plus devant un bloc à 29 Ω au voisinage de sa résonance.* Dans les deux cas l'optimiseur doit recevoir l'impédance du bloc **tel qu'il est câblé**, pavillons connectés.

**Premier ordre de grandeur** — si $Z$ était résistive de module $\lvert Z\rvert$ : $Q_{eff}=\lvert Z\rvert\sqrt{C/L}$ = 0,73 (8 Ω), **1,28** (14 Ω), **4,38** (48 Ω). Le calcul exact avec la phase de $Z$ est pire, car au-dessus de $f_s$ la branche motionnelle est capacitive et s'ajoute à $C_1$ :

```
Filtre catalogue 18 mH / 150 uF sur la charge typique :
  r = 0.0 ohm | PB : max +10.8 dB a  75.0 Hz, gain a 100 Hz  +1.4 dB, f(-3 dB / 0 dB) = 115.7 Hz
              | PH : max  +5.7 dB a  78.5 Hz, gain a 100 Hz  +0.8 dB, f(-3 dB / 0 dB) =  62.3 Hz
  r = 1.0 ohm | PB : max  +8.0 dB a  74.0 Hz, gain a 100 Hz  +0.7 dB, f(-3 dB / 0 dB) = 114.3 Hz
              | PH : max  +3.3 dB a  79.4 Hz, gain a 100 Hz  +0.2 dB, f(-3 dB / 0 dB) =  63.3 Hz
  f_c (croisement, definition gelee) : 8 ohm r=1 -> 96.66 Hz | charge typique r=1 -> 102.95 Hz  (+6.5 %)
```

| $f$ (Hz) | 40 | 50 | 70 | 100 | 140 | 200 | 250 |
|---|---|---|---|---|---|---|---|
| cible PB Butterworth (dB) | −0,1 | −0,3 | −0,9 | −3,0 | −6,8 | −12,3 | −16,0 |
| PB catalogue sur 8 Ω, $r=0$ | 0,0 | −0,2 | −0,8 | −3,0 | −7,1 | −12,7 | −16,5 |
| PB catalogue sur $Z$ typique, $r=1$ Ω | +1,3 | +3,1 | **+7,7** | +0,7 | −7,7 | −14,4 | −17,9 |
| PH catalogue sur $Z$ typique, $r=1$ Ω | −16,1 | −10,7 | **+0,8** | +0,2 | −2,0 | −1,9 | −1,4 |
| somme (voie inversée), cible | 1,2 | 1,7 | 2,5 | 3,0 | 2,6 | 1,7 | 1,2 |
| somme (voie inversée), $Z$ typique | 2,4 | 4,7 | **10,9** | 6,5 | 1,6 | 0,0 | −0,2 |

Ordre de grandeur de l'écart (calculé sur le modèle typique) : **≈ +8 à +11 dB de surtension vers 75 Hz** sur le passe-bas, et un raccord déplacé de 96,7 à **103,0 Hz** (définition gelée, $r=1$ Ω), soit **+6,5 %**.

**Ce que la DCR coûte vraiment sur la charge réelle.** Une DCR de 1 Ω amortit ≈ 3 dB du pic (10,85 → 7,99 dB). Mais son prix énergétique n'est plus les 11 % du tableau 4.1, qui valent pour 8 Ω **résistifs** : la part de $r_1$ dans la puissance **active** fournie à la voie grave vaut **33 % à 100 Hz**, 28 % à 75 Hz, et **≈ 30 % en moyenne** sur 40–250 Hz (27,6 % si l'on pondère par l'énergie ; jusqu'à 42 % à 250 Hz). La charge réelle aggrave donc aussi la facture énergétique de la DCR — c'est un renfort de l'argumentaire v2, pas un affaiblissement.

**Tenue en tension des condensateurs : c'est la crête qui compte.** *Hypothèse* : l'ampli est assimilé à une **source de tension** limitée par ses rails, $V_{in,max}$ estimée par la puissance nominale sur 8 Ω, soit $V_{in}=\sqrt{350\times8}=52{,}9$ V efficaces, **$V_{in,crête}=\sqrt2\times52{,}9=74{,}8$ V**. Sur 8 Ω, $\lvert V_{C_1}\rvert\le V_{in}$ ; sur le modèle typique ($r=0{,}5$ Ω), $\max_f\lvert V_{C_1}/V_{in}\rvert=2{,}92$ et $\max_f\lvert V_{C_2}/V_{in}\rvert=2{,}16$, soit **154 V efficaces ≡ 218 V crête** sur $C_1$ et **114 V efficaces ≡ 162 V crête** sur $C_2$. Un condensateur est spécifié en tension **continue ou de crête**, jamais en valeur efficace : la contrainte s'écrit

$$V_{C,nom}\;\ge\;k\,\max_f\left\lvert \frac{V_C}{V_{in}}\right\rvert\cdot V_{in,cr\hat{e}te},\qquad V_{in,cr\hat{e}te}=\sqrt2\,\sqrt{P_{nom}R_{nom}} = 74{,}8\text{ V}$$

soit **250 V DC au catalogue, marge comprise** — et non les « 100 V » de la v1, ni même 160 V. Acheter un 160 V sur la foi du « 154 V » le détruirait. *Réserve d'honnêteté* : ce 218 V est un **majorant d'un majorant**. À 75 Hz l'impédance d'entrée du filtre tombe à 3,5 Ω (ci-dessous) et le montage tirerait 15 A ; un E-800 (500 W/4 Ω, soit ≈ 11 A) écrête bien avant. La limite réelle est fixée par l'enveloppe tension/courant de l'ampli et sera plus basse. La conclusion — les 100 V de la v1 sont insuffisants — survit intacte.

**Le filtre ne déforme pas seulement la réponse : il déforme la charge.** Grandeur absente de la v1 et pourtant dimensionnante, l'impédance vue par l'amplificateur $Z_{in}=j\omega L_1+r_1+(Z\parallel 1/j\omega C_1)$ :

| Design (charge typique, $r_1$ du modèle) | $\min_f\lvert Z_{in}\rvert$ | $\max_f\lvert I_{L_1}\rvert$ à 52,9 V | $\max_f\lvert I_{C_1}\rvert$ |
|---|---|---|---|
| HP seul (pas de filtre) | 6,7 Ω (20–500 Hz) | — | — |
| catalogue 18 mH / 150 µF | **3,51 Ω à 77 Hz** | 15,1 A → **228 W** dans $r_1=1$ Ω | 9,4 A |
| optimisé 27 mH / 10 µF (§ 04.8) | 11,3 Ω à 90 Hz | 4,7 A | — |

> **Ne pas confondre ce tableau avec les chiffres de la chaîne.** Il est calculé sur la
> **charge typique en caisse close**, avec des **selfs idéales** et le design 27 mH / 10 µF :
> 3,51 et 11,3 Ω. La chaîne `analyse/tout_refaire.py`, elle, travaille sur la **charge
> bass-reflex** du CSV synthétique, avec les **selfs de Brooks** (r = 1,64 Ω) et le design
> 18 mH / 27 µF : elle donne **3,29 Ω** (catalogue) et **5,27 Ω** (optimisé), en lecture
> **voie par voie** — le montage de référence proposé au D5, option E. Ce sont deux ordres de
> grandeur indépendants du **même phénomène**, pas deux mesures du même nombre : ils ne se
> comparent pas terme à terme, et ce sont les chiffres de la chaîne qui sont projetés au jury.
> Dans la lecture **parallèle** (les deux cellules sur un seul ampli), la chaîne donne 1,77 Ω
> pour le catalogue et **3,48 Ω pour le design optimisé** — donc **aucun des deux** ne satisfait
> la contrainte dans ce montage-là, et cela se dit pour les deux ou pour aucun.

**Le même calcul sur la charge bass-reflex — c'est-à-dire sur le cas réel.** Repris le 16 sept. 2026 avec le code du dépôt, filtre catalogue 18 mH / 150 µF, DCR 1 Ω (**MODÈLES, aucune mesure**) :

| Charge du passe-bas | bosse max de $\lvert H_{PB}\rvert$ | $\min_f\lvert Z_{in}\rvert$ |
|---|---|---|
| 8 Ω résistifs | réponse plate (référence) | **8,52 Ω** |
| **seconde** charge modélisée, en caisse close | $+12{,}2$ dB | **2,49 Ω** |
| **bass-reflex modélisé** (le cas réel) | $+12{,}6$ dB | **2,66 Ω** |

*« Bosse » = maximum de $\lvert H_{PB}\rvert$ sur 10–1000 Hz **rapporté à la perte d'insertion de 1,02 dB** obtenue sur 8 Ω résistifs ($20\log_{10}(8/9)$ pour $r=1$ Ω) : sans cette définition, le nombre n'est vérifiable par personne. La ligne « caisse close » est un **jeu de paramètres distinct** ($f_s=55$ Hz, $Q_{ms}=6{,}1$), et non le même haut-parleur supposé clos — c'est une seconde charge modélisée, pas une variante de la première.*

Deux lectures, et il faut les donner toutes les deux. (i) **Le verdict est le même dans les deux cas de charge réelle, et il tombe avant toute comparaison de fidélité** : $\min\lvert Z_{in}\rvert$ passe **sous le minimum de 4 Ω du t.amp E-800**. Le filtre catalogue est donc **disqualifié par une contrainte**, pas par un critère de qualité — c'est un résultat plus fort et plus simple à défendre qu'un écart de quelques dB. (ii) **Le bass-reflex n'améliore rien** : 2,66 Ω au lieu de 2,49 Ω, la différence est dans l'épaisseur du trait, et la bosse est même légèrement pire (+12,6 contre +12,2 dB — maximum de $|H|$ du passe-bas sur 10–1000 Hz rapporté à la perte d'insertion de 1,02 dB sur 8 Ω résistifs ; et la « charge close » citée ici est une **seconde charge modélisée**, un jeu de paramètres distinct, non le même haut-parleur supposé clos).

**Mais le bass-reflex ajoute un SECOND point bas, d'origine différente.** Sur 20–500 Hz, $\lvert Z_{in}\rvert$ du montage complet présente deux minima locaux là où la caisse close n'en a qu'un (calcul `br4.py`, jeu du § 01.10) :

```
REGENERE le 2026-09-16 (minima LOCAUX de |Zin| sur 20-500 Hz, filtre 18 mH/150 uF, r = 1 ohm).
ATTENTION : trois charges distinctes circulent dans cette section, il faut les NOMMER.
  (a) 8 ohm resistif                          : un seul minimum,  58.2 Hz -> 8.52 ohm
  (b) SECONDE charge modelisee, close         : un seul minimum,  77.8 Hz -> 2.49 ohm
      (fs = 55 Hz, Qms = 6,1 -- celle du tableau ci-dessus, bosse +12,2 dB)
  (c) LE MEME 18" suppose clos a alpha = 3    : un seul minimum,  87.2 Hz -> 2.16 ohm
      (fs = 40 x racine(4) = 80 Hz, Qms = 6,1 x 2 = 12,2 ; bosse +14,3 dB)
  (d) bass-reflex modelise (LE CAS REEL)      : DEUX minima,      26.7 Hz -> 6.50 ohm
                                                                  90.6 Hz -> 2.66 ohm
      26.7 Hz = creux d'impedance du HP, pres de fb (il appartient au HAUT-PARLEUR)
      90.6 Hz = point bas du FILTRE, entre le pic et le raccord
```

**(b) et (c) ne sont pas la même chose, et il faut le dire.** (b) est une *seconde charge
modélisée*, un jeu de paramètres plausible en caisse close ; (c) est le **même haut-parleur
que le bass-reflex**, mis en caisse close de même $\alpha$ (évent bouché). (c) est la vraie
comparaison « à charge identique » — et elle est **moins favorable encore** au filtre catalogue
(2,16 Ω, +14,3 dB). Parler de « la même charge supposée close » en montrant (b) serait une
confusion que le jury défera en une question.

Les deux n'ont pas la même cause et n'appellent pas le même remède. Celui de **90,6 Hz** est fabriqué par le filtre : le condensateur $C_1$ shunte la charge juste au-dessus du pic, là où $\underline{Z}$ est capacitive, et l'ensemble tombe bien sous $R_e$ — c'est sur lui qu'agit l'optimisation de l'acte 3. Celui de **26,7 Hz** appartient au haut-parleur : c'est le creux à $f_b$, où la membrane est immobile et où seule $R_e$ subsiste ; **aucun choix de $L_1,C_1$ ne le supprime**, on ne peut que ne pas l'aggraver. D'où une conséquence directe sur la **contrainte** du § 04.5 : le minimum d'impédance d'entrée doit être évalué sur **toute la bande utile, pas seulement sur 40–250 Hz** — le creux d'accord est en dessous, et l'amplificateur, lui, ne sait pas que le critère s'arrête à 40 Hz.

Le filtre passif **divise par deux l'impédance minimale** du haut-parleur et passe sous le minimum de 4 Ω admis par le E-800 : risque de protection, d'écrêtage, d'ampli en défaut. Au niveau d'écoute gelé ($P_{ref}=10$ W dans 8 Ω) les chiffres restent parlants : 2,55 A de pointe et **6,5 W de pointe** dans $r_1$, contre 2,20 W de moyenne de bande pour $r_1+r_2$. Une self bobinée maison dimensionnée sur la moyenne chauffe trois fois trop au pic. D'où deux contraintes nouvelles au § 04.5 — et un argument d'oral sans équivalent en actif : **la référence active n'a aucun de ces problèmes, parce que son filtre ne voit jamais le haut-parleur.**

**Hypothèse « réponse acoustique = tension HP × réponse du HP ».** La pression rayonnée s'écrit $p(f)=V_{in}\,H(f)\,G_{HP}(f)$ où $G_{HP}$ est la réponse en pression du HP **attaqué en tension** — c'est ainsi qu'elle est définie (ampli = source de tension, $Z_s\approx0$) et mesurée en champ proche. Cette factorisation suppose : (i) linéarité petit signal (le modèle T-S ignore $Bl(x)$, d'où le critère « robustesse » à deux niveaux) ; (ii) que $G_{HP}$ ne dépende pas du filtre — vrai puisque le HP ne « sait » pas d'où vient sa tension. Le filtre agit donc **exactement** par $H(f)$, et la cible acoustique de la somme est

$$S(f)=H_{PB}(f)\,G_{sub}(f)\;+\;p\,H_{PH}(f)\,G_{med}(f)\,e^{-j\omega\tau},\qquad p=\pm1 .$$

Trois choses que le squelette pose à 1 et qu'il ne faut **pas** laisser à 1 :

- **$\tau$, la différence de trajet entre haut-parleurs non colocalisés.** À 100 Hz, $\lambda=3{,}43$ m : un écart de **0,50 m** entre centres acoustiques vaut **52°** de déphasage, ce qui coûte 0,93 dB sur la somme sur l'axe (20° coûtent 0,13 dB, 45° 0,69 dB, 90° annulent). C'est largement de quoi transformer la bosse Butterworth de +3,01 dB en creux partiel. **Mesurer l'écart au mètre ruban dès maintenant** (cinq minutes) et mettre $e^{-j\omega\tau}$ avec ce $\tau$ dans la fonction de coût : [[à mesurer — écart entre le centre du 18″ et celui du bloc médiums]]. Attention : une mesure en **champ proche**, protocole imposé à 100 Hz, mesure chaque HP séparément et **ne capte pas** cette différence de trajet — il faut l'ajouter à la main. (C'est exactement le sujet de Linkwitz 1976, cité en bibliographie.)
- **$G_{sub}$ et $G_{med}$, les réponses des HP.** Les poser égales à 1 revient à optimiser la somme **électrique** alors que le critère gelé est **acoustique**. L'écart entre les deux peut dépasser l'effet étudié : le 18″ chute de 12 à 24 dB/oct sous $F_c$, les médiums sous leur propre $f_s$. **Conséquence de calendrier** : il faut déplacer un balayage champ proche de chaque HP **en phase 1** (le micro, la carte son et REW sont déjà dans la liste de matériel ; c'est une demi-heure) pour disposer de $G_{sub}$ et $G_{med}$ **avant** la phase 3. Sinon la phase 3 optimise la mauvaise grandeur et la phase 4 le découvre trop tard.
- **Le niveau relatif des deux voies.** $G_{sub}=G_{med}=1$ suppose les deux voies de même sensibilité. Un 18″ et un bloc médium n'ont aucune raison d'avoir le même dB/W/m : si l'écart n'est pas modélisé, l'optimiseur le compensera **silencieusement par une déformation de filtre**. Il faut soit un gain relatif en variable, soit un L-pad sur la voie la plus sensible. Sensibilités : [[à mesurer]] (phase 1) — conséquence énoncée, à ne pas oublier.

### <a id="s04-3"></a>04.3 Cible de sommation : Butterworth 2 ou somme plate ?

Sur charge résistive, avec $x=f/f_c$ réel et $D=1+jx/Q+(jx)^2$ : $H_{PB}=1/D$, $H_{PH}=(jx)^2/D$. À $f_c$ : $H_{PB}=-j/\sqrt2$, $H_{PH}=+j/\sqrt2$ (Butterworth) → phases **−90° et +90°, soit 180° d'écart**.

| Alignement | $\lvert H(f_c)\rvert$ | même polarité à $f_c$ | une voie inversée | phase entre voies |
|---|---|---|---|---|
| Butterworth 2 ($Q=1/\sqrt2$) | −3,01 dB | $\lvert S\rvert=0$ (**trou**), −2,77 dB à 50 et 200 Hz | $\lvert -j/\sqrt2-j/\sqrt2\rvert=\sqrt2$ → **+3,01 dB**, +1,68 dB à 50/200 Hz | 0° à $f_c$ seulement |
| Linkwitz-Riley 2 ($Q=1/2$) | −6,02 dB | trou | $S=\frac{1+x^2}{(1+jx)^2}$ → **0,000 dB partout** | 0° **partout** ($H_{PB}$ et $-H_{PH}$ colinéaires) |
| Linkwitz-Riley 4 ($=$ B2²) | −6,02 dB | **0,000 dB partout** (passe-tout) | trou | 0° partout, **sans inversion** |

Chiffres issus de `verif_sommation.py` (écart de phase LR2 : $6\cdot10^{-15}$°, platitude à $10^{-15}$ dB). L'écart RMS de la somme Butterworth inversée à une cible plate sur 40–250 Hz vaut **2,29 dB** : ce n'est pas un défaut, c'est sa signature. Sur 8 Ω, LR2 correspond à $L=R/(Q\omega_0)=25{,}5$ mH et $C=Q/(\omega_0R)=99{,}5$ µF (E12 : 27 mH / 100 µF, dont le produit $LC$ est identique à celui de 18 mH × 150 µF, d'où le même $f_0=96{,}9$ Hz).

**Mise en œuvre de l'inversion de polarité**, pour l'expérimentateur : elle consiste simplement à **permuter les deux fils d'un des deux haut-parleurs**. Elle est **obligatoire** au 2ᵉ ordre (Butterworth comme LR2) et **interdite** en LR4 (qui somme à plat sans elle). Elle doit être re-vérifiée au micro après câblage : à $f_c$ le bon sens donne une bosse, le mauvais un trou profond — c'est le test le plus rapide et le plus lisible de toute la phase 4.

> **Décision à geler en phase 0, et incohérence à lever avant.** FEUILLE-DE-ROUTE écrit déjà « écart RMS de la somme des deux voies **à la cible plate** » (ligne 43) et « cible : somme des deux voies **plate** » (ligne 109), ce qui désigne LR2 ($Q=1/2$, 27 mH / 100 µF). Mais le sanity check du § 04.7 et l'ensemble des illustrations utilisent la cible **Butterworth** (forme catalogue, +3 dB à $f_c$), qui est l'héritage v1. **Les deux ne peuvent pas être gelées ensemble.** Si l'on retient Butterworth, il faut *amender* les lignes 43 et 109 de FEUILLE-DE-ROUTE avant le gel ; si l'on retient la cible plate, il faut changer la cible par défaut du squelette. LR4 reste en perspective : somme plate sans inversion, mais 4 gros composants par voie en passif (trivial en actif par cascade).

### <a id="s04-4"></a>04.4 Réseau de Zobel et compensation de résonance

**Zobel** ($R_z+C_z$ série, en parallèle sur le HP) : annule la partie inductive $j\omega L_e$. Condition exacte $R_z=R_e$, $C_z=L_e/R_e^2$ : alors $(R_e+j\omega L_e)\parallel(R_z+1/j\omega C_z)=R_e$ à toute fréquence (vérifié : écart $2{,}7\cdot10^{-15}$ Ω sur 10 Hz–10 kHz). Sub typique : $R_z=6{,}5$ Ω, $C_z=28{,}4$ µF ; médiums : 6,4 Ω, 12,2 µF. Effet à 1 kHz sur le sub : 9,2 Ω ∠45° → 6,1 Ω ∠0°. Mais **à 100 Hz** : 14,1 Ω → 11,6 Ω seulement, phase −47° → −54° : le Zobel ne corrige pas le pic motionnel, qui est le vrai problème au raccord.

**Compensation de résonance** : on cherche $Z_c$ tel que $(R_e+Z_{mot})\parallel Z_c=R_e$, soit $Z_c=R_e+R_e^2/Z_{mot}=R_e+R_e^2Y_{mot}$. Comme $Y_{mot}=1/R_{es}+1/(j\omega L_{es})+j\omega C_{es}$, $Z_c$ est un **RLC série** accordé sur $f_s$ :

$$
R_c=R_e+\frac{R_e^2}{R_{es}},\qquad L_c=C_{es}R_e^2,\qquad C_c=\frac{L_{es}}{R_e^2},\qquad \frac{1}{2\pi\sqrt{L_cC_c}}=f_s
$$

*(Homogénéité : $\mathrm{F}\cdot\Omega^2=\mathrm{H}$ et $\mathrm{H}/\Omega^2=\mathrm{F}$ — les deux conversions sont dimensionnellement correctes.)*

| HP typique | $R_c$ | $L_c$ | $C_c$ | $\lvert Z\rvert$ 20–500 Hz brut → +RLC → +RLC+Zobel | à $f_s$ sous 53 V : $I$ / $P$ dans $R_c$ | $P$ reçue par le HP |
|---|---|---|---|---|---|---|
| Sub | 7,46 Ω | 6,69 mH | **2 368 µF** | 6,7–50,5 → 5,4–6,5 → 5,0–6,5 Ω | 7,1 A / **375 W** | 55 W |
| Médiums | 7,77 Ω | 10,9 mH | **648 µF** | 6,5–36,4 → 6,0–6,4 → 5,9–6,4 Ω | 6,8 A / 361 W | 77 W |

Le réseau linéarise parfaitement (vérifié à $7\cdot10^{-15}$ Ω hors $L_e$) mais à 100 Hz les valeurs sont énormes : 2,4 mF sous ≥ 250 V crête (§ 04.2), une self de 6,7 mH à faible DCR, et une résistance qui, à la résonance, dissipe **375 W, soit près de sept fois les 55 W simultanément reçus par le haut-parleur** — l'équivalent de la puissance nominale de l'ampli, dans une résistance. Ce n'est pas un paradoxe : le réseau linéarise l'impédance en **absorbant précisément ce que le HP cesse d'absorber** quand il résonne. (Chiffre majorant : sinus permanent à pleine puissance exactement à $f_s$.) Coût et matière multipliés par deux ou trois (ordre de grandeur, [[à vérifier]] sur devis) — exactement ce que le thème « sobriété » demande d'éviter. C'est la réponse au jury « pourquoi pas simplement un Zobel ? » : le Zobel est bon marché mais inopérant au raccord ; ce qui opère est hors de prix. D'où la voie v2 : **laisser $Z(f)$ tel quel et optimiser $L_1,C_1,C_2,L_2$ dessus**, Zobel en option.

### <a id="s04-5"></a>04.5 Formulation du problème d'optimisation

**Variables** : $\mathbf{x}=(L_1,C_1,C_2,L_2)$, option Zobel sur le sub $(R_z,C_z)$.

<!-- Remarque des deux relecteurs retenue : les valeurs Rz = Re, Cz = Le/Re^2 sont optimales pour ANNULER l'inductance, pas pour minimiser J. La justification du brouillon était un raccourci logique. -->
*Statut du Zobel* : les valeurs $R_z=R_e$, $C_z=L_e/R_e^2$ sont celles qui **annulent l'inductance** (§ 04.4) — rien ne prouve qu'elles minimisent $J$. On les fige à ces valeurs (arrondies E12) et on traite le Zobel comme un **booléen**, faute de quoi l'espace passe à 96 millions de points. C'est une **restriction assumée du domaine**, contrôlée a posteriori par le balayage du § 04.8.

**Cible** : $H^{c}_{PB},H^{c}_{PH}$ (Butterworth ou LR2, § 04.3) et somme cible $S^c=H^c_{PB}G_{sub}+p\,H^c_{PH}G_{med}$, **avec la même polarité $p$ que la solution évaluée**.

**Fonction de coût** (grille $f_k$ log-espacée, 64 points ≈ 1/24 d'octave sur 40–250 Hz ; $m_\varphi$ = sous-bande 70–140 Hz) :

$$
J(\mathbf{x})=w_s\,\underbrace{\sqrt{\left\langle\left(20\log\lvert S\rvert-20\log\lvert S^c\rvert\right)^2\right\rangle_{40\text{–}250}}}_{\text{somme (dB)}}
+w_v\,\underbrace{\Big(\mathrm{RMS}_{dB}(H_{PB},H^c_{PB})+\mathrm{RMS}_{dB}(H_{PH},H^c_{PH})\Big)}_{\text{forme de chaque voie (dB)}}
+w_\varphi\,\underbrace{\sqrt{\left\langle\left(\Delta\varphi-\Delta\varphi^c\right)^2\right\rangle_{70\text{–}140}}}_{\text{phase entre voies (°)}}
+w_€\,\text{Prix}(\mathbf{x})+w_W\,P_{Joule}(\mathbf{x})
$$

avec $S=H_{PB}G_{sub}+p\,H_{PH}G_{med}$, $\Delta\varphi=\arg\!\big(H_{PB}\,\overline{p\,H_{PH}}\big)$ (replié dans $]-180°,180°]$), $\text{Prix}=\sum(\text{prix}_L+\text{prix}_C)$ et $P_{Joule}=\langle r_1\lvert I_{L_1}\rvert^2+r_2\lvert I_{L_2}\rvert^2\rangle_{40\text{–}250}$ sous $V_{ref}=\sqrt{8P_{ref}}$.

> **Hypothèse implicite de la moyenne $\langle\cdot\rangle$.** La grille $f_k$ est **log-espacée** : moyenner dessus revient à supposer une excitation à **énergie constante par fraction d'octave** (bruit rose), et non par hertz (bruit blanc). Ce choix pondère lourdement le grave et **change le classement des designs**. Il est défendable — le contenu musical réel est plus proche du rose que du blanc — mais il doit être énoncé, et il fait partie des conventions à geler en phase 0.

| Pondération | Valeur proposée | Signification | Statut |
|---|---|---|---|
| $w_s$ | 1 dB/dB | fidélité de la somme (critère « fidélité du raccord ») | à geler phase 0 |
| $w_v$ | 1 dB/dB | forme de chaque voie (protection des médiums, pente du sub) | à geler phase 0 |
| $w_\varphi$ | 0,05 dB/° (20° ≡ 1 dB) | robustesse hors axe / HP non colocalisés | **justification à revoir** (ci-dessous) |
| $w_€$ | 0,04 dB/€ (25 € ≡ 1 dB) | critère « coût marginal » | à geler phase 0 |
| $w_W$ | 1 dB/W à $P_{ref}=10$ W | critère « pertes d'insertion » | $P_{ref}$ = niveau gelé |

*Sur $w_W$* : $P_{ref}=10$ W est une **puissance de référence conventionnelle sur 8 Ω** ($V_{ref}=\sqrt{8P_{ref}}=8{,}94$ V), pas la puissance réellement délivrée à la charge. L'équivalence « 1 W ≡ 1 dB » se lit donc « 10 % de $P_{ref}$ ≡ 1 dB » ; sur la charge réelle le filtre catalogue dissipe 2,20 W pour ce $P_{ref}$, soit 22 % — le poids est cohérent avec l'ordre de grandeur du phénomène, pas avec les 11 % de la ligne 8 Ω résistive.

*Sur $w_\varphi$* : l'équivalence « 20° ≡ 1 dB » est **sur-pénalisante d'un facteur ≈ 8** au regard de la somme sur l'axe, où 20° d'écart entre deux voies d'amplitude égale ne coûtent que **0,13 dB** (45° → 0,69 dB, 90° → 3,01 dB). Elle n'est défendable que si elle représente la robustesse **hors axe**. Le bon calibrage se dérive du décalage acoustique réel : si les centres sont écartés de 0,50 m, l'écart de trajet vaut 52° à 100 Hz et coûte 0,93 dB → $w_\varphi\approx 0{,}018$ dB/°. **À recalibrer sur le $\tau$ mesuré** (§ 04.2).

**Contraintes.**

1. **Séries normalisées IEC 60063** — E12 : {1,0 ; 1,2 ; 1,5 ; 1,8 ; 2,2 ; 2,7 ; 3,3 ; 3,9 ; 4,7 ; 5,6 ; 6,8 ; 8,2} × 10ⁿ ; E6 = un terme sur deux. Grilles retenues : $L\in$ E12 × {1 mH, 10 mH} (1–82 mH, 24 valeurs), $C\in$ E12 × {10 µF, 100 µF} (10–820 µF, 24 valeurs). ⚠ **Cette grille est une idéalisation de catalogue.** Une self **bobinée maison** (option de FEUILLE-DE-ROUTE, ~25 €/pièce) est une variable quasi **continue**, quantifiée par le nombre de spires : la contrainte E12 n'y a aucun sens. Et les chimiques bipolaires de crossover ne suivent pas E12 au-delà de 100 µF. Le problème réel est donc **mixte** : $L$ continu, $C$ discret sur le **catalogue effectif du fournisseur** [[à relever avant la phase 3]]. Les 331 776 combinaisons restent la borne pédagogique et le banc d'essai de la méthode ; c'est aussi ce qui donne son vrai rôle au recoupement par optimiseur continu.
2. **Tension des condensateurs, en crête** : $V_{C,nom}\ge k\,\max_f\lvert V_C/V_{in}\rvert\cdot 74{,}8$ V (§ 04.2).
3. **Courant** — la contrainte que la v1 ignorait et qui décide si l'objet tient physiquement. (a) *Courant d'ondulation* admissible de chaque condensateur : $\max_f\lvert I_C\rvert\le I_{ripple,max}$ ; un chimique bipolaire de 150 µF n'est pas garanti aux 9,4 A calculés au § 04.2 [[à vérifier sur datasheet]]. (b) *Section de fil / échauffement* de chaque self : la perte de **pointe** $\max_f r\lvert I_L\rvert^2$ (228 W à pleine puissance, 6,5 W à $P_{ref}$) et non la moyenne de bande dimensionne le fil — c'est le satellite « self optimale » qui fournit cette contrainte.
4. **Impédance vue par l'ampli** : $\min_f\lvert Z_{in}(f)\rvert\ge 4\ \Omega$ (minimum du E-800), implémentée comme pénalité dure. Coût de calcul **nul** : $Z_{in}$ est déjà au dénominateur de $H_{PB}$ dans le code. Loin d'être théorique, elle **disqualifie le filtre catalogue** (3,51 Ω, § 04.8) et **162 des 576 couples $(L_1,C_1)$ de la grille** même sur 8 Ω résistif.
5. **DCR et prix issus d'un seul modèle de bobinage.** <!-- Les deux relecteurs convergent : r ∝ L (masse fixée) et prix ∝ L (masse ∝ L) sont physiquement incompatibles ; la fonction de coût pénalise deux fois le cuivre. --> À géométrie donnée, $R=\rho\,(N\ell_{spire})^2/V_{cuivre}$ et $L\propto N^2$ : $r\propto L$ suppose la **masse de cuivre constante**, alors qu'un prix $\propto L$ suppose une masse $\propto L$ — auquel cas la DCR devrait être quasi constante. Les placeholders du brouillon ($r(L)=1\,\Omega\times L/18$ mH et $4+1{,}2\,L[\mathrm{mH}]$ €) **pénalisent donc deux fois la même grandeur physique** et faussent l'arbitrage cuivre ↔ pertes ↔ prix, qui est le cœur du satellite. Pire : ces deux fonctions étant monotones de la seule variable $L$, elles sont **parfaitement corrélées** et le front de Pareto dégénère en une droite — **le satellite, branché ainsi, n'alimente aucun arbitrage**. La correction de fond est d'ajouter la **masse de cuivre $m$ en cinquième variable** : $m(L,r)$ par Wheeler, puis $\text{prix}=a+b\,m$ et $r=f(L,m)$ avec $r\propto 1/m$ à $L$ fixé (la loi $r\times m\approx$ cte de FEUILLE-DE-ROUTE). En attendant, on retient **un** jeu cohérent et on le dit. Les trois jeux possibles et leur effet sur l'optimum (§ 04.8) : (A) masse fixée, $r\propto L$, prix constant → 33 mH ; (B) DCR fixée, $r$ constant, prix $\propto L$ → 27 mH ; (C) fil fixé, $r$ et prix $\propto\sqrt L$ → 33 mH. **L'illustration tient, la contrainte telle qu'écrite dans le brouillon est indéfendable devant un jury.**
6. **Ordre 2** : contrainte **dure**, pas une hypothèse par défaut — donc un plancher explicite sur $C_1$ (ou un drapeau « ordre 2 »), sans quoi l'optimiseur la viole en rabattant $C_1$ sur la borne basse (§ 04.8).
7. **ESR des condensateurs** : $C_2$ est **en série** sur la voie médium, son ESR s'ajoute exactement comme une DCR. Négligée dans le squelette ; ordre de grandeur recalculé : 0,13 W à $P_{ref}$ et **−0,17 dB à 250 Hz** pour 0,2 Ω, 0,31 W et −0,43 dB pour 0,5 Ω — second ordre devant les 2,20 W de DCR, mais non nul dans un critère gelé « pertes d'insertion ». Elle est **mesurable gratuitement** avec le jig d'impédance de la phase 1 : [[à mesurer]], puis à ajouter comme paramètre de $H_{PH}$ et de $P_{Joule}$ (deux caractères de code).
8. **Résistances parasites de la chaîne** : impédance de sortie de l'ampli (facteur d'amortissement) et résistance des câbles et connexions s'ajoutent directement à $r_1$ et $r_2$ et sont du même ordre (quelques dixièmes d'ohm). [[à mesurer]] — un fil de 2,5 mm² de 3 m aller-retour, c'est déjà ~0,04 Ω.

**Protection des médiums : une contrainte, pas un terme quadratique.** Le terme $w_v$ est fondé sur $\mathrm{RMS}_{dB}$, métrique à **deux côtés** qui pénalise autant la sur-atténuation que la sous-atténuation. Recalculé : l'optimum 120 µF / 12 mH atténue les médiums à **−21,4 dB à 40 Hz** contre une cible de −16,0 dB — il est donc **pénalisé de 5,4 dB pour mieux protéger les médiums que la cible**. Symétriquement, le catalogue laisse −5,0 dB à 60 Hz (le $f_s$ des médiums) contre −9,4 dB visés : sous-protection de 4,4 dB, qui coûte exactement pareil. Une métrique qui met sur le même plan « protège trop » et « protège pas assez » ne peut pas porter la raison d'être du raccord. **Correction (trois lignes de code, et l'optimum change)** : rendre la protection **unilatérale** sous $f_s$ des médiums — contrainte dure $\lvert H_{PH}(f)\rvert\le \lvert H^c_{PH}(f)\rvert$, ou pénalité sur le seul excès $\max(0,\lvert H\rvert-\lvert H^c\rvert)$ — et garder le RMS à deux côtés pour la seule bande passante.

**Taille de l'espace discret.** $24^4=331\,776$ combinaisons ; $24^2\times12^2=82\,944$ si les condensateurs sont en E6 ; $\times(12\times24)=96$ millions si l'on énumérait aussi $(R_z,C_z)$. **Astuce de vectorisation** : $H_{PB}$ ne dépend que de $(L_1,C_1)$ et $H_{PH}$ que de $(C_2,L_2)$ → on calcule deux tableaux $576\times N_f$, et la somme par produit externe $576\times576\times N_f$ (par blocs pour la mémoire). Mesuré : **331 776 combinaisons en ≈ 2 s** (médiane 1,84 s sur 5 exécutions ; 1,8 à 3,3 s selon l'appel et la machine, le premier appel incluant l'allocation des tableaux). L'énumération exhaustive est donc la méthode de référence (robuste, sans minimum local, **numpy seul**) ; l'optimiseur continu (`scipy.optimize`) sert de recoupement, puis on arrondit — et l'on vérifie que l'arrondi est bien l'optimum discret.

**Dégénérescence découverte en testant.** Avec la somme seule ($w_v=0$), la cible « plate » retourne **10 mH / 39 µF**, c'est-à-dire un LR2 à 254,9 Hz ($Q=0{,}50$, $J=0{,}004$) : une somme plate est obtenue par un LR2 à *n'importe quelle* fréquence, et sur charge réelle par « tout au sub » (1 mH / 10 µF, testé). La somme ne contraint ni $f_c$ ni la protection des médiums. **Le terme par voie $w_v$ est donc indispensable** — et il correspond physiquement à la raison d'être du raccord (§ 03 : tenir les médiums au-dessus de $f_s$), sous réserve de le rendre unilatéral en basse fréquence comme dit ci-dessus.

### <a id="s04-6"></a>04.6 Squelette Python exécuté

Extrait de `optim_e12_squelette.py` (fonctions ; le bloc principal enchaîne les tests des § 04.7–04.9). Données synthétiques ; modèles économiques = placeholders. **Ces fonctions n'utilisent que numpy.**

```python
import numpy as np
# scipy n'est requis QUE pour le recoupement continu du bloc principal (§ 04.7) :
# from scipy.optimize import minimize, differential_evolution

# ---------- 1. Charge : modele electrique de Thiele-Small (Re, Le, Res, fs, Qms) ----------
def Z_ts(f, Re, Le, Res, fs, Qms):
    w = 2*np.pi*f; ws = 2*np.pi*fs
    Les = Res/(ws*Qms); Ces = Qms/(ws*Res)                    # branche motionnelle RLC parallele
    return Re + 1j*w*Le + 1/(1/Res + 1/(1j*w*Les) + 1j*w*Ces)

SUB_TYP = dict(Re=6.5, Le=1.2e-3, Res=44., fs=40., Qms=1.75)  # typique (modele v1), PAS une mesure
MED_TYP = dict(Re=6.4, Le=0.5e-3, Res=30., fs=60., Qms=3.0)   # typique, bloc 2 x 4 ohm en serie

def zobel(Z, f, Rz, Cz):
    """Impedance vue par le filtre quand un Zobel (Rz + Cz en serie) est en parallele sur le HP."""
    Zz = Rz + 1/(2j*np.pi*f*Cz)
    return Z*Zz/(Z + Zz)

# ---------- 2. Cellules chargees (L, C de forme (n,1) ; f, Z de forme (Nf,) -> (n, Nf)) ----------
def H_pb(f, L, C, Z, r=0.):
    w = 2*np.pi*f; Zp = Z/(1 + 1j*w*C*Z)                      # Z // (1/jwC)
    return Zp/(1j*w*L + r + Zp)
def H_ph(f, C, L, Z, r=0.):
    w = 2*np.pi*f; ZL = 1j*w*L + r; Zp = ZL*Z/(ZL + Z)       # (jwL + r) // Z
    return Zp/(1/(1j*w*C) + Zp)

# ---------- 3. Cibles : forme de chaque voie ----------
def cible(f, nom, fc=100.):
    s = 1j*f/fc                                              # s : variable de Laplace NORMALISEE (s = jf/fc)
    Q = {'butterworth': 1/np.sqrt(2), 'plat': 0.5}[nom]       # 'plat' = Linkwitz-Riley 2
    D = 1 + s/Q + s**2                                       # <-> 1 + jx/Q + (jx)^2 du texte, avec x = f/fc reel
    return 1/D, s**2/D

# ---------- 4. Series normalisees et modeles economiques (PLACEHOLDERS explicites) ----------
E12 = np.array([1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2])
E6  = E12[::2]
serie = lambda base, decades: np.concatenate([base*10.**d for d in decades])
L_VALS = serie(E12, [-3, -2])          # 1,0 mH ... 82 mH   (24 valeurs)
C_VALS = serie(E12, [-5, -4])          # 10 uF ... 820 uF   (24 valeurs)

# JEU (A) "masse de cuivre fixee" : r ~ L et prix constant. A remplacer par le modele a 2 variables
# (masse m en 5e variable, Wheeler : prix = a + b.m et r = f(L, m) avec r.m ~ cte) -- cf. contrainte 5.
def dcr(L):    return 1.0*L/18e-3          # ohm : 1 ohm a 18 mH, lineaire en L a MASSE FIXEE [ordre de grandeur]
def prix_L(L): return 4.0 + 1.2*L/1e-3     # euros -- INCOHERENT avec dcr() ci-dessus  [[a corriger, cf. 04.5]]
def prix_C(C): return 1.0 + 0.05*C/1e-6    # euros, electrolytique bipolaire            [[a verifier]]

# ---------- 5. Fonction de cout ----------
W_DEF = dict(s=1.0, v=1.0, phi=0.05, eur=0.04, W=1.0)   # dB/dB, dB/dB, dB/deg, dB/euro, dB/W -- a geler en phase 0
def cout(p1, p2, f, Zs, Zm, cible_nom='butterworth', w=W_DEF, P_ref=10., pol=-1,
         Gs=1., Gm=1., avec_dcr=True, detail=False, bloc=48):
    """p1 : tableau (n1, 2) de couples (L1, C1) ; p2 : tableau (n2, 2) de couples (C2, L2).
    Gs, Gm : reponses complexes des HP (=1 : hypothese 'HP plats, colocalises et de meme
    sensibilite', a remplacer par les reponses champ proche + exp(-jwt)). Retourne J (n1, n2)."""
    f = np.asarray(f); m_phi = (f >= 70) & (f <= 140)          # f = grille de la bande de cout 40-250 Hz
    Hc_pb, Hc_ph = cible(f, cible_nom)
    S_c = Hc_pb*Gs + pol*Hc_ph*Gm                              # la CIBLE suit la meme polarite que la solution
    dphi_c = np.angle(Hc_pb*np.conj(pol*Hc_ph))
    L1, C1 = p1[:, :1], p1[:, 1:]; C2, L2 = p2[:, :1], p2[:, 1:]
    r1 = dcr(L1) if avec_dcr else 0.*L1; r2 = dcr(L2) if avec_dcr else 0.*L2
    Hpb = H_pb(f, L1, C1, Zs, r1)*Gs                            # (n1, Nf)
    Hph = H_ph(f, C2, L2, Zm, r2)*Gm                            # (n2, Nf)
    dB = lambda h: 20*np.log10(np.abs(h))
    V1 = np.sqrt(np.mean((dB(Hpb) - dB(Hc_pb*Gs))**2, axis=1))  # forme de chaque voie vs sa cible
    V2 = np.sqrt(np.mean((dB(Hph) - dB(Hc_ph*Gm))**2, axis=1))  # [[a rendre UNILATERAL sous fs -- cf. 04.5]]
    V_ref = np.sqrt(P_ref*8.)                                   # P_ref = puissance de REFERENCE dans 8 ohm
    Zp1 = Zs/(1 + 2j*np.pi*f*C1*Zs)
    Zin = 2j*np.pi*f*L1 + r1 + Zp1                              # impedance vue par l'ampli (voie grave)
    P1 = np.mean(abs(V_ref/Zin)**2*r1, axis=1)                  # Joule dans r1 (serie) -- moyenne de bande
    P2 = np.mean(abs(V_ref*Hph/(2j*np.pi*f*L2 + r2))**2*r2, axis=1)         # Joule dans r2 (shunt)
    ZIN_MIN = np.min(abs(Zin), axis=1)                          # contrainte 4 : >= 4 ohm (E-800)
    EUR = (prix_L(L1[:, 0]) + prix_C(C1[:, 0]))[:, None] + (prix_C(C2[:, 0]) + prix_L(L2[:, 0]))[None, :]
    G = np.empty((len(p1), len(p2))); PHI = np.empty_like(G)
    for a in range(0, len(p1), bloc):                                         # par blocs (memoire)
        S = Hpb[a:a+bloc, None, :] + pol*Hph[None, :, :]
        G[a:a+bloc] = np.sqrt(np.mean((dB(S) - dB(S_c))**2, axis=-1))         # somme vs somme cible
        dphi = np.angle(Hpb[a:a+bloc, None, :]*np.conj(pol*Hph[None, :, :])) - dphi_c
        dphi = np.degrees((dphi + np.pi) % (2*np.pi) - np.pi)
        PHI[a:a+bloc] = np.sqrt(np.mean(dphi[..., m_phi]**2, axis=-1))        # ecart de phase entre voies
    V = V1[:, None] + V2[None, :]; PW = P1[:, None] + P2[None, :]
    J = w['s']*G + w['v']*V + w['phi']*PHI + w['eur']*EUR + w['W']*PW
    J = J + np.where(ZIN_MIN[:, None] < 4.0, 1e3, 0.)                         # contrainte dure Z_in >= 4 ohm
    return (J, G, V, PHI, EUR, PW) if detail else J

# ---------- 6. Enumeration exhaustive E12 ----------
def enumere(f, Zs, Zm, L_vals=L_VALS, C_vals=C_VALS, **kw):
    p1 = np.array([(L, C) for L in L_vals for C in C_vals])    # (L1, C1) : 576 couples
    p2 = np.array([(C, L) for C in C_vals for L in L_vals])    # (C2, L2) : 576 couples
    J = cout(p1, p2, f, Zs, Zm, **kw)
    i, j = np.unravel_index(np.argmin(J), J.shape)
    return dict(L1=p1[i, 0], C1=p1[i, 1], C2=p2[j, 0], L2=p2[j, 1], J=J[i, j], J_all=J, p1=p1, p2=p2)
```

> **Deux corrections apportées au brouillon**, toutes deux silencieuses et donc dangereuses. (a) La cible codait en dur l'inversion de polarité (`S_c = Hc_pb*Gs - Hc_ph*Gm`) alors que la signature expose un paramètre `pol` : un appel avec `pol=+1` aurait comparé une somme non inversée à une cible inversée et renvoyé un coût **faux sans lever d'erreur** (l'écart à $f_c$ valant l'infini plutôt que zéro). (b) Le nom `x` était utilisé pour $jf/f_c$ dans le code et pour $f/f_c$ réel dans le texte : renommé `s`, avec la correspondance en commentaire. Les sorties des § 04.7–04.9 sont **inchangées** (le défaut `pol=-1` était le seul cas testé).
>
> Restent **non corrigées et signalées comme telles** dans le squelette : le couple `dcr`/`prix_L` (contrainte 5), le caractère bilatéral de `V1`/`V2` (§ 04.5), l'absence d'ESR et de contrainte de courant. Ce sont les chantiers de la phase 3 ; les inscrire en commentaire dans le code plutôt que de les corriger à la hâte évite de casser la traçabilité des résultats ci-dessous.

Bloc principal : `f = np.logspace(log10(40), log10(250), 64)` ; sanity checks sur `Z8 = 8 + 0j` avec `avec_dcr=False` et `w = dict(s=1, v=1, phi=0.05, eur=0, W=0)` ; recoupement continu par `minimize(J, log10(x0), method='Nelder-Mead')` **borné sur le domaine de la grille** et `differential_evolution` ; puis charge typique, option Zobel, Monte-Carlo.

### <a id="s04-7"></a>04.7 Sanity check (porte de validation de la phase 3) et recoupement scipy

```
Espace discret : 24 L x 24 C, 4 composants -> 331,776 combinaisons ; C en E6 : 82,944 ; + Zobel enumere : 96 millions
Sanity 8 ohm, cible butterworth, somme seule : L1 = 18.0 mH, C1 = 150 uF | C2 = 150 uF, L2 = 18.0 mH ; J = 0.211 ; f0 =  96.9 Hz, Q = 0.73 ; 331,776 combinaisons en 1.88 s
Sanity 8 ohm, cible butterworth, somme+voies : L1 = 18.0 mH, C1 = 150 uF | C2 = 150 uF, L2 = 18.0 mH ; J = 0.947 ; f0 =  96.9 Hz, Q = 0.73
Sanity 8 ohm, cible plat       , somme seule : L1 = 10.0 mH, C1 =  39 uF | C2 =  39 uF, L2 = 10.0 mH ; J = 0.004 ; f0 = 254.9 Hz, Q = 0.50   <- degenere
Sanity 8 ohm, cible plat       , somme+voies : L1 = 27.0 mH, C1 = 100 uF | C2 = 100 uF, L2 = 27.0 mH ; J = 0.826 ; f0 =  96.9 Hz, Q = 0.49   [attendu 27 mH / 100 uF]
scipy Nelder-Mead (8 ohm)            : L1 = 18.01 mH, C1 = 140.7 uF | C2 = 140.7 uF, L2 = 18.01 mH ; J = 4.5e-10 [attendu 18,01 mH / 140,7 uF]
scipy differential_evolution (8 ohm) : L1 = 18.01 mH, C1 = 140.7 uF | C2 = 140.7 uF, L2 = 18.01 mH ; J = 9.1e-15
```

Sur 8 Ω pur, sans DCR ni pénalités, **l'énumération retombe sur 18 mH / 150 µF** (le catalogue normalisé) et l'optimiseur continu sur **18,01 mH / 140,7 µF** (le catalogue théorique) : le code reproduit les formules qu'il est censé généraliser. Avec la cible LR2 il retrouve 27 mH / 100 µF (analytique 25,5 / 99,5). Contrôle croisé supplémentaire : une **énumération indépendante par boucles explicites** (35 s au lieu de 2 s) donne exactement le même optimum et le même $J = 0{,}947$ — la version vectorisée ne cache pas de bug d'indice. Ces tests sont à rejouer **à chaque modification** de la fonction de coût, avant tout achat (FEUILLE-DE-ROUTE, phase 3).

### <a id="s04-8"></a>04.8 Illustration sur la charge typique (synthétique — à refaire sur $Z(f)$ mesurée)

> ⚠ **Ce paragraphe démontre la MÉTHODE. Ce n'est pas un design à fabriquer.** Les paramètres de charge sont typiques et non mesurés ; le modèle de self est incohérent (contrainte 5) ; la protection des médiums est bilatérale (§ 04.5) ; la contrainte d'ordre 2 n'est pas imposée. **Ne rien acheter sur la foi de ces valeurs** — c'est précisément l'objet de la porte de validation de la phase 3.

```
Charge typique (illustratif), cible Butterworth, DCR = 1 ohm a 18 mH :
  catalogue 18.0 mH/150 uF | 150 uF/18.0 mH : J = 1017.63 (somme 4.26 dB, voies 8.35 dB, phase 1.9 deg, 68 euros, pertes 2.20 W)
                                               ^^^^ 17.63 + penalite 1000 : min|Z_in| = 3.51 ohm < 4 ohm -> DISQUALIFIE
  optimise E12, fidelite seule (eur = W = 0) : 33.0 mH/ 10 uF | 120 uF/12.0 mH : J = 7.58 (somme 1.88 dB, voies 4.90 dB, phase 15.9 deg, 70 euros, pertes 0.71 W)
  optimise E12, poids par defaut            : 27.0 mH/ 10 uF | 120 uF/12.0 mH : J = 11.04 (somme 2.06 dB, voies 5.15 dB, phase 11.5 deg, 63 euros, pertes 0.72 W)
     4 meilleurs : 11.04 -> 27 mH/10 uF | 120 uF/12 mH ; 11.08 -> 27/12 | 120/12 ; 11.11 -> 33/10 | 120/12 ; 11.16 -> 27/15 | 120/12
  continu (Nelder-Mead BORNE sur le domaine de la grille) : 29.5 mH / 10.0 uF | 115.7 uF / 12.4 mH ; J = 10.92
  continu (Nelder-Mead NON borne)  : C1 -> 2.7e-14 uF (log10 C1 = -19.6) ; J = 10.59   <- DIVERGENCE, point non admissible
  + Zobel sub 6,8 ohm + 27 uF (prix non compte) : 27.0 mH/ 10 uF | 100 uF/15.0 mH : J = 11.89
  balayage de 36 couples (Rz, Cz) autour des valeurs analytiques : meilleur J = 11.27  (sans Zobel : 11.04)
```

**Lecture** (valable pour ce modèle seulement). Premier résultat, et il n'était pas prévu : **la contrainte d'impédance élimine le filtre catalogue avant toute comparaison de fidélité.** Avec $\min\lvert Z_{in}\rvert=3{,}51$ Ω il descend sous le minimum de 4 Ω du E-800 ; le solveur lui ajoute la pénalité de 1000 et il sort du domaine admissible. Ses mérites de fidélité (somme 4,26 dB, $J$ « nu » $=17{,}63$) sont affichés pour mémoire, mais le débat est clos avant d'avoir lieu. Sur les 576 couples $(L_1,C_1)$ de la grille, **162 violent cette contrainte** même sur 8 Ω résistif : ce n'est pas un cas pathologique isolé.

Ensuite seulement, la fidélité : l'écart RMS de la somme passe de **4,3 dB à ≈ 2 dB**, celui des voies de 8,4 à ≈ 5 dB — un passif du 2ᵉ ordre **ne rattrape pas** la forme Butterworth sur une charge qui résonne, ce qui serait déjà un résultat. Le design optimisé remonte au passage $\min\lvert Z_{in}\rvert$ de 3,5 à **11,3 Ω**.

Quatre enseignements méthodologiques, eux, sont généraux.

1. **L'optimum est plat** : quatre designs à 1 % de $J$. La dernière marche E12 compte moins que les tolérances (§ 04.9).
2. **L'optimum continu et l'énumération se recoupent** (29,5 → 27 ou 33 mH ; 115,7 → 120 µF) mais l'arrondi *composant par composant* n'est pas toujours l'optimum discret — d'où la primauté de l'énumération. <!-- Correction retenue : le brouillon affichait « C1 = 0 uF ; J = 10,59 » et un « arrondi E12 » qui n'en était pas un. --> **Attention au piège numérique** : l'optimiseur continu **non borné** minimise sur $\log_{10}C_1$ sans plancher, donc $C_1\to0$ et l'affichage `%.0f` imprime « 0 µF ». Le $J=10{,}59$ correspondant n'appartient pas au domaine admissible : ce n'est **pas** un optimum, c'est une **borne inférieure**. Borné sur le domaine de la grille, l'optimiseur rend $J=10{,}92$, à comparer honnêtement aux $J=11{,}04$ de l'optimum discret.
3. **$C_1$ tombe sur la borne basse** de la grille (10 µF ≈ absence de condensateur) : l'optimiseur signale que sur cette charge la cellule sub tend vers un **1ᵉʳ ordre**, et **viole donc la contrainte 6**. L'enjeu n'est pas cosmétique : 27 mH + 10 µF donne −15,3 dB à 250 Hz (contre −15,1 pour 27 mH seul) mais **−22,6 dB à 1 kHz contre −39,8 dB pour le catalogue**. Un 18″ qui rayonne encore à −23 dB dans sa zone de rupture est un défaut acoustique réel, invisible pour une bande de coût arrêtée à 250 Hz. **Sensibilité à la borne haute de la bande** (balayage fait) :

   | bande de coût | optimum | $J$ |
   |---|---|---|
   | 40–250 Hz | 27 mH / 10 µF \| 120 µF / 12 mH | 11,04 |
   | 40–400 Hz | 33 mH / 10 µF \| 120 µF / 12 mH | 10,43 |
   | 40–800 Hz | 33 mH / 10 µF \| 120 µF / 12 mH | 11,59 |
   | 40–1600 Hz | **22 mH / 82 µF** \| 120 µF / 15 mH | 11,49 |

   $C_1$ ne quitte la butée qu'à partir d'une bande étendue à 1,6 kHz. La conclusion la plus frappante du § 04.8 dépend donc **directement** d'un choix de bande qui n'avait pas été justifié. Deux remèdes, à trancher en phase 0 : imposer le plancher sur $C_1$, ou élargir la bande de coût de la voie sub à au moins 1 kHz.
4. **Le Zobel n'améliore pas $J$** : 11,89 avec les valeurs analytiques, et **11,27 au mieux sur 36 couples $(R_z,C_z)$ balayés** avec énumération complète à chaque fois, contre 11,04 sans Zobel. La conclusion du § 04.4 ne repose donc plus sur un seul essai. Réserve : $R_z$ et $C_z$ dérivent de $R_e$ et $L_e$, tous deux [[à mesurer]].

**Robustesse au modèle de self** (contrainte 5). En remplaçant le couple incohérent par les trois jeux physiquement cohérents :

| Modèle de self | optimum | $J$ |
|---|---|---|
| brouillon ($r\propto L$ **et** prix $\propto L$) — incohérent | 27 mH / 10 µF | 11,04 |
| (A) masse fixée : $r\propto L$, prix constant | 33 mH / 10 µF | 10,68 |
| (B) DCR fixée : $r$ constant, prix $\propto L$ | 27 mH / 10 µF | 11,01 |
| (C) fil fixé : $r$ et prix $\propto\sqrt L$ | 33 mH / 10 µF | 10,88 |

L'optimum ne bouge que d'un cran E12 : l'illustration n'est pas détruite par l'incohérence, mais la formulation doit l'être avant l'oral.

### <a id="s04-9"></a>04.9 Propagation des incertitudes

**Trois lectures de la même tolérance**, à ne pas mélanger. Sur charge résistive, $f_0=1/(2\pi\sqrt{LC})$ donne

$$\frac{u(f_0)}{f_0}=\frac12\sqrt{\left(\frac{u(L)}{L}\right)^2+\left(\frac{u(C)}{C}\right)^2}$$

<!-- La formule du brouillon est juste (elle corrige bien le 11 % du RC 1er ordre de la v1, qui n'a plus rien a faire ici) ; c'est son ALIMENTATION qui melangeait demi-largeurs et incertitudes-types. Les deux relecteurs convergent sur la convention GUM. -->

| lecture | $L\pm10\%$, $C\pm10\%$ | $L\pm10\%$, $C\pm20\%$ |
|---|---|---|
| borne au pire cas (demi-largeurs combinées en quadrature) | 7,1 % | 11,2 % |
| **incertitude-type GUM** (loi uniforme, $u=a/\sqrt3$) — **convention retenue** | **4,1 %** | **6,5 %** |
| Monte-Carlo direct sur $f_0$ ($N=2\cdot10^5$ tirages uniformes) | — | 6,5 % |

Le rapport entre les deux premières lignes est exactement $\sqrt3=1{,}732$ (vérifié). Retenir la convention GUM permet de **comparer directement** l'analytique au Monte-Carlo : c'est un contrôle croisé, pas une contradiction. Toute mention d'un « 11 % » doit porter l'étiquette « borne au pire cas ». Même correction pour le Sallen-Key (§ 04.11) : 7,9 % en borne, **4,6 % en incertitude-type**.

**Monte-Carlo sur le design catalogue** ($N=2000$ tirages uniformes, $L\pm10\%$, $C\pm20\%$, $r=1$ Ω) :

| Charge | $f$ à −3 dB du PB : moyenne, $\sigma$ (5–95 %) | écart RMS de la somme à la cible Butterworth |
|---|---|---|
| 8 Ω résistif | 92,7 Hz, $\sigma=5{,}6$ Hz soit **6,1 %** (84,4–101,8 Hz) | 0,57 dB (0,25–1,07) |
| $Z$ typique | 114,7 Hz, $\sigma=5{,}0$ Hz soit **4,3 %** (106,7–123,3 Hz) | 4,25 dB (3,89–4,59) |

*(Les « ±6 % » du brouillon désignaient un écart-type : écrire $\sigma=6$ %, l'intervalle 5–95 % étant 84–102 Hz, soit −9 %/+10 %.)*

**Ce que le brouillon ne faisait pas : propager l'incertitude sur $Z(f)$ elle-même.** La conclusion « l'incertitude dominante est $Z(f)$ » portait la problématique entière et n'était étayée que par un Monte-Carlo qui ne tirait que sur $L$ et $C$. Sensibilités recalculées sur la définition gelée de $f_c$ (variation de $+1$ % de chaque paramètre, design catalogue, charge typique) :

| paramètre | $\delta f_c/f_c$ | $\delta$(RMS somme) |
|---|---|---|
| $f_s$ du sub | +0,43 % | +0,010 dB |
| $f_s$ des médiums | −0,59 % | +0,009 dB |
| $R_{es}$ sub / médiums | +0,29 % / −0,26 % | +0,015 / +0,009 dB |
| $Q_{ms}$ sub / médiums | −0,32 % / +0,28 % | −0,008 / −0,005 dB |
| $R_e$ sub / médiums | +0,14 % / −0,18 % | −0,001 / −0,002 dB |
| $L_e$ (les deux) | < 0,02 % | < 0,001 dB |
| $L_1$ / $C_1$ / $C_2$ / $L_2$ | −0,80 / −0,42 / −0,16 / +0,24 % | −0,000 / +0,007 / +0,016 / +0,012 dB |
| $r_1$ | −0,04 % | −0,006 dB |

Et le Monte-Carlo correspondant, source par source (incertitudes T-S = **ordres de grandeur** calqués sur l'exemple de la section 03 : $R_e\pm3$ %, $L_e\pm10$ %, $R_{es}\pm5$ %, $f_s\pm2$ %, $Q_{ms}\pm10$ % ; à remplacer par la **covariance du fit** de la phase 2) :

| source tirée | $f_c$ (croisement) | écart RMS de la somme |
|---|---|---|
| composants seuls ($L\pm10$ %, $C\pm20$ %) | 103,7 ± 7,4 Hz (**7,1 %**) | 4,24 ± 0,21 dB |
| paramètres T-S seuls | 102,4 ± 5,4 Hz (5,3 %) | 4,29 ± 0,13 dB |
| DCR seule (±25 %) | 102,9 ± 0,7 Hz (0,7 %) | 4,29 ± 0,10 dB |
| tout | 103,0 ± 8,8 Hz (8,5 %) | 4,25 ± 0,26 dB |

> **Conclusion révisée — et plus solide que celle du brouillon.** Sur $f_c$, la charge et les composants pèsent **du même ordre** (la charge déplace $f_c$ de 96,7 à 103,0 Hz, soit +6,5 % ; les tolérances le dispersent de 7,1 %) : il est **faux** de dire que $Z(f)$ domine sur ce critère-là. En revanche, sur la **forme**, l'écart RMS de la somme passe de 0,46 dB (8 Ω) à 4,29 dB ($Z$ typique), soit **+3,8 dB**, quand *toutes* les sources d'incertitude réunies ne le dispersent que de **±0,26 dB** : un facteur 15. La bonne formulation est donc : **$Z(f)$ est un BIAIS, les tolérances sont une DISPERSION.** Un biais ne s'annule pas en moyenne et ne se réduit pas en resserrant les tolérances — il ne se corrige qu'en le **mesurant** puis en **optimisant dessus**. C'est exactement la thèse du sujet v2, et cette formulation-là résiste à un jury.

Le Monte-Carlo de la phase 3 devra donc tirer sur les trois sources (composants, T-S via la covariance du fit § 03, DCR à ±20–30 % pour une self bobinée maison).

### <a id="s04-10"></a>04.10 Contre-vérification LTspice (phase 3)

FEUILLE-DE-ROUTE impose « LTspice en contre-vérification » et la section 08 s'en prévaut devant le jury (critère A3). Toute la section 04 ne s'appuie pour l'instant que sur son propre code Python : le sanity check prouve qu'il retrouve les formules analytiques sur 8 Ω, pas qu'il traite correctement une charge complexe. Netlist minimale (6 composants) du passe-bas chargé par le modèle T-S du sub :

```spice
* Passe-bas 18 mH / 150 uF charge par le modele T-S du sub 18" (parametres TYPIQUES, non mesures)
V1  in 0  AC 1
L1  in m  18m
Rd  m  hp 1            ; DCR de la self, en serie
C1  hp 0  150u
Re  hp e  6.5          ; bobine mobile
Le  e  n  1.2m
Res n  0  44           ; branche motionnelle : RLC parallele accorde sur fs = 40 Hz
Les n  0  100.04m      ; Les = Res/(2.pi.fs.Qms)
Ces n  0  158.25u      ; Ces = Qms/(2.pi.fs.Res)   -> 1/(2.pi.sqrt(Les.Ces)) = 40,000 Hz, Res.sqrt(Ces/Les) = 1,7500
.ac oct 48 10 10k
.end
```

Valeurs de référence à retrouver (calculées par le code de la section, `v6_ltspice.py`) — **[[à exécuter sous LTspice en phase 3]]**, la superposition des deux courbes fermant la question « comment savez-vous que votre code est juste ? » :

| $f$ (Hz) | 40 | 50 | 70 | 75 | 100 | 140 | 200 | 250 | 1000 |
|---|---|---|---|---|---|---|---|---|---|
| $\lvert Z\rvert$ (Ω) | 50,50 | 39,68 | 22,40 | 20,24 | 14,10 | 10,21 | 8,00 | 7,23 | 9,23 |
| $\lvert H_{PB}\rvert$ (dB) | +1,32 | +3,06 | +7,68 | **+7,97** | +0,73 | −7,74 | −14,37 | −17,87 | −39,76 |
| phase (°) | −8,5 | −14,9 | −54,0 | −73,1 | −131,5 | −145,3 | −148,2 | −149,2 | −174,4 |

### <a id="s04-11"></a>04.11 Référence active Sallen-Key : pourquoi elle ne voit pas $Z(f)$

Topologies (AOP suiveur, gain unité) : PB = $V_{in}$ – $R_1$ – A – $R_2$ – B(+), $C_2$ de B à la masse, $C_1$ de A à la sortie ; PH = mêmes positions avec $C$ en série et $R'_2$ à la masse, $R'_1$ en contre-réaction. Analyse nodale ($V_{out}=V_B$) :

$$
H_{PB}=\frac{1}{1+s\,C_2(R_1+R_2)+s^2R_1R_2C_1C_2},\quad \omega_0=\frac{1}{\sqrt{R_1R_2C_1C_2}},\quad Q=\frac{\sqrt{R_1R_2C_1C_2}}{C_2(R_1+R_2)}\ \xrightarrow{R_1=R_2}\ \frac12\sqrt{\frac{C_1}{C_2}}
$$

$$
H_{PH}=\frac{s^2R'_1R'_2C^2}{1+2sR'_1C+s^2R'_1R'_2C^2},\quad \omega_0=\frac{1}{C\sqrt{R'_1R'_2}},\quad Q=\frac12\sqrt{\frac{R'_2}{R'_1}}
$$

Butterworth ⇒ $C_1=2C_2$ (PB) et $R'_2=2R'_1$ (PH). Piège : composants tous égaux ⇒ $Q=0{,}5$. Vérification (`verif_sallen_key.py`, et résolution nodale indépendante) :

```
SK PB sub  (R = 10 k, C1 = 220 nF, C2 = 110 nF) : f0 = 102.3 Hz, Q = 0.707 ; |H(100 Hz)| = -2.82 dB, phase -88.2 deg
SK PH med  (C = 100 nF, R1' = 11 k, R2' = 22 k)  : f0 = 102.3 Hz, Q = 0.707 ; |H(100 Hz)| = -3.21 dB, phase +91.8 deg
  ecart max |H_SK,pb - Butterworth(102,3 Hz)| = 4.5e-16
```

L'immunité tient à la structure : le filtre n'est fait que de $R$ et $C$ de l'ordre du kΩ et du nF, sa sortie est celle de l'AOP (impédance quasi nulle, chargée par les 10–20 kΩ de l'ampli), et le HP est alimenté par l'ampli — **jamais par le filtre**. Les valeurs E12 donnent $f_0=102{,}3$ Hz (+2,3 %), à afficher tel quel. Avec les tolérances usuelles ($R\pm5$ %, $C\pm10$ %, 4 composants), $u(f_0)/f_0=4{,}6$ % en incertitude-type (7,9 % en borne au pire cas) : la référence active n'est pas « exacte », elle est **indépendante de la charge** — c'est ce qu'on lui demande.

**Son talon d'Achille, identifié et chiffré : l'impédance de sortie du pré-ampli.** $Z_s$ n'agit pas de la même façon sur les deux voies, et le chiffre unique « −4,6 % » du brouillon masquait l'essentiel. Sur le passe-bas, $Z_s$ **s'ajoute à $R_1$** et abaisse $f_0$. Sur le passe-haut, il se met **en série avec le condensateur d'entrée** ; la résolution nodale donne alors

$$H_{PH}=\frac{s^2C^2}{s^2C^2\left(1+\dfrac{Z_s}{R'_2}\right)+sC\left(\dfrac{2}{R'_2}+\dfrac{Z_s}{R'_1R'_2}\right)+\dfrac{1}{R'_1R'_2}}$$

c'est-à-dire une **perte d'insertion** $K_{PH}=1/(1+Z_s/R'_2)$ dans la bande passante, plus une légère baisse de $f_0$ et de $Q$ :

| $Z_s$ | PB : gain / $f$ à −3 dB | PH : gain / $f$ à −3 dB **/ $K$** | PH : $f$ à −3 dB **/ 0 dB** | $f_c$ (croisement) |
|---|---|---|---|---|
| 0 | 0,00 dB / 102,3 Hz | 0,000 dB / 102,31 Hz | 102,3 Hz | 102,31 Hz |
| 100 Ω | 0,00 dB / 101,8 Hz | −0,039 dB / 102,31 Hz | 102,8 Hz | 102,28 Hz |
| 600 Ω | 0,00 dB / 99,3 Hz | −0,234 dB / 102,33 Hz | 105,3 Hz | 102,14 Hz |
| 1 kΩ | 0,00 dB / 97,4 Hz | −0,386 dB / 102,36 Hz | 107,5 Hz | 102,00 Hz |

<!-- Les deux relecteurs se contredisaient ici : l'un annoncait 107,5 Hz sur le passe-haut a 1 kohm, l'autre un effet negligeable (coin a 16 kHz). Recalcul nodal : les DEUX ont raison dans leur convention. 107,5 Hz est le -3 dB ABSOLU (contamine par la perte d'insertion de 0,39 dB) ; le -3 dB relatif a la bande passante ne bouge que de +0,05 %. C'est la meilleure illustration possible de la necessite de geler la definition (04.1). -->

Lecture. À 1 kΩ, **la forme du passe-haut est quasi intacte** (son −3 dB relatif à sa propre bande passante bouge de +0,05 %) : la vraie dégradation est une **perte d'insertion de 0,39 dB** sur la seule voie médium, c'est-à-dire un **déséquilibre de niveau entre voies**, pas un déplacement de coupure. Pendant ce temps le passe-bas, lui, descend réellement de 4,6 %. Résultat : les deux « −3 dB » se désolidarisent de 5 % (97,4 contre 102,4 Hz) alors que la **fréquence de croisement ne bouge que de 0,3 %** (102,31 → 102,00 Hz). C'est un déséquilibre d'amplitude et de pente, pas un décalage de raccord — et c'est exactement ce que la définition gelée du § 04.1 permet de dire sans se tromper : le même phénomène se lit « −4,6 % », « +5 % » ou « −0,3 % » selon la convention. **D'où : mesurer $Z_s$ du SX-801** [[à mesurer]], et si elle dépasse quelques centaines d'ohms, insérer un **étage tampon** en entrée de filtre. Argument fort pour l'oral : même la référence « immunisée » a un talon d'Achille, il est identifié, chiffré, et corrigeable pour le prix d'un AOP.

### Ce qu'il faut retenir pour l'oral

- Sur 8 Ω résistif, $Q=R\sqrt{C/L}$ : **le facteur de qualité appartient à la charge**. Remplacer $R$ par $Z(f)$ fait varier $Q$ avec la fréquence — sur un modèle typique, le filtre catalogue surtend de ≈ +8 à +11 dB vers 75 Hz (calculé, à confronter à la mesure).
- **$f_c$ est gelée comme la fréquence de croisement des deux voies.** Ce n'est pas de la bureaucratie : pour une DCR de 2 Ω, la même réalité physique se note −18 % ou +10 % selon la convention, et le croisement ne bouge que de 0,8 %. Avec cette définition, la charge déplace le raccord de **96,7 à 103,0 Hz (+6,5 %)**.
- Au 2ᵉ ordre les voies sont à 180° à $f_c$ : sans inversion, trou ; avec inversion, +3,01 dB (Butterworth) ou 0 dB (LR2). **La cible se choisit avant, pas après** — et FEUILLE-DE-ROUTE dit « plate » là où les illustrations disent « Butterworth » : à trancher en phase 0.
- Zobel = bon marché mais inopérant à 100 Hz ; compensation RLC = efficace mais 2,4 mF et une résistance qui, à $f_s$, dissipe **sept fois** ce que reçoit le haut-parleur. D'où l'optimisation directe sur $Z(f)$.
- **Le filtre passif ne déforme pas seulement la réponse, il déforme la charge** : $\min\lvert Z_{in}\rvert$ tombe de 6,7 à 3,5 Ω, sous le minimum de 4 Ω de l'ampli — au point que la contrainte **disqualifie le filtre catalogue** avant même la comparaison de fidélité. Aucun équivalent en actif.
- Fonction de coût explicite (somme + forme des voies + phase + € + W), espace E12 de 331 776 combinaisons énuméré en **≈ 2 s avec numpy seul** ; sanity check : sur 8 Ω l'optimiseur redonne 18 mH / 150 µF (continu : 18,01 mH / 140,7 µF).
- **$Z(f)$ est un biais, les tolérances sont une dispersion** : +3,8 dB systématiques sur l'écart RMS de la somme, contre ±0,26 dB toutes sources d'incertitude confondues. Un biais ne s'efface qu'en le mesurant et en optimisant dessus — c'est le sujet.

### Sources

- Thiele, A. N., « Loudspeakers in Vented Boxes », Parts I & II, *J. Audio Eng. Soc.*, vol. 19, n° 5, pp. 382–392 (mai 1971) et n° 6, pp. 471–483 (juin 1971).
- Small, R. H., « Direct-Radiator Loudspeaker System Analysis », *J. Audio Eng. Soc.*, vol. 20, n° 5, pp. 383–395 (juin 1972).
- Linkwitz, S. H., « Active Crossover Networks for Noncoincident Drivers », *J. Audio Eng. Soc.*, vol. 24, n° 1, pp. 2–8 (1976) — la référence sur le terme $e^{-j\omega\tau}$ du § 04.2.
- Sallen, R. P., Key, E. L., « A Practical Method of Designing RC Active Filters », *IRE Trans. Circuit Theory*, vol. CT-2, n° 1, pp. 74–85 (mars 1955).
- Zobel, O. J., « Theory and Design of Uniform and Composite Electric Wave-filters », *Bell System Technical Journal*, vol. 2, n° 1, pp. 1–46 (janv. 1923) — réseau **à résistance constante** en téléphonie ; **il n'y est jamais question de haut-parleur**. Son application au HP est une **analogie**, reprise de Dickason. La « compensation de résonance » du § 04.4 n'est pas de Zobel du tout.
- IEC 60063:2015, *Preferred number series for resistors and capacitors* (séries E6, E12, E24).
- Dickason, V., *The Loudspeaker Design Cookbook*, Audio Amateur Press — formules usuelles du Zobel et de la compensation de résonance [[à vérifier : édition et pages]].
- NumPy 2.4.6 ; SciPy 1.18.1 (`minimize` Nelder-Mead, `differential_evolution`) — **facultatif**, cf. l'en-tête de statut.
- Dépôt : `FEUILLE-DE-ROUTE.md` (phases 0 et 3, critères — lignes 43 et 109 à amender, cf. § 04.3), `CLAUDE.md` (nombres de contrôle), `archive-v1/_gen.py` (modèle T-S illustratif réutilisé comme « typique »), datasheet t.amp E-800 (2 × 350 W / 8 Ω, 500 W / 4 Ω, $Z_{in}$ 10/20 kΩ) telle que consignée dans `CLAUDE.md`.

## <a id="s05"></a>05. Conception de la self : inductance, cuivre, pertes, fabrication

> **Statut.** Section de référence rédigée en phase 0 (septembre 2026). Tous les nombres ci-dessous sont **calculés** à partir de constantes tabulées ($\rho_{Cu}=1{,}72\cdot10^{-8}\ \Omega\cdot$m, $\rho_m=8960$ kg/m³) ou **vérifiés numériquement** ; les seuls chiffres externes sont trois fiches produit, citées et étiquetées. **Rien n'a été bobiné ni mesuré** : toute grandeur de l'enceinte de Thomas reste [[à mesurer]]. Scripts réellement exécutés (scratchpad `sec05/`, Python 3.13.2, **numpy 2.4.6 seul** — aucun appel à scipy, les intégrales elliptiques sont calculées par la moyenne arithmético-géométrique et les fonctions de Bessel par leur série entière) : `verif_brooks.py`, `verif_proportions.py`, `dimensionnement.py`, `noyau_et_fabrication.py`, `optim_contraintes.py`, `peau_et_proximite.py`, `mesure_et_thermique.py`, `budget_et_coherence.py`, `couplage_mutuel.py`.

Cette section est le **satellite qui alimente la section 04**. La fonction de coût de la § 4.5 contient deux modèles laissés en placeholder : `dcr(L)` et `prix_L(L)`. C'est ici qu'on les remplace par des lois démontrées — et l'on verra au passage que **ces deux placeholders se contredisent**, ce qui biaisait l'optimiseur. Résultat central : le triplet $(L, r, m)$ n'a **que deux degrés de liberté** ; on ne choisit pas séparément l'inductance, la résistance et la masse de cuivre.

**Convention de fréquence (rappel ; la définition officielle est au § 04.1).** $f_c$ est **la fréquence de croisement des deux voies**, et rien d'autre — c'est la seule définition gelée du TIPE. Cette section-ci n'en a pas l'usage : elle manipule des **repères** du couple $L$–$C$, qu'elle nomme explicitement. $f_0=1/(2\pi\sqrt{LC})$ désigne le **pôle**, qui est aussi la fréquence de **résonance série** exploitée en § 05.13 pour mesurer $L$ ; pour 18 mH / 150 µF sur 8 Ω, $f_0=96{,}86$ Hz, tandis que le **−3 dB du passe-bas** est à 99,9 Hz et le **−3 dB du passe-haut** à 93,9 Hz ($Q=0{,}73$, seuil mi-puissance $-3{,}0103$ dB, cf. § 04.1). Ces trois nombres sont distincts : la section n'écrit jamais « $f_c$ » pour l'un d'eux.

### <a id="s05-1"></a>05.1 Ce qu'on demande à la self de grave

Dans la cellule passe-bas (§ 4.1), $L_1$ est **en série** avec le haut-parleur : tout le courant du grave la traverse. Trois exigences contradictoires :

| Exigence | Grandeur | Conséquence |
|---|---|---|
| Tenir la fréquence de raccord | $L = 18$ mH (catalogue) à quelques % près | fixe $N^2 a$ |
| Ne pas perdre le signal en chaleur | $r$ faible (§ 4.5 : $r=1\ \Omega$ ⇒ 11,1 % de la puissance, $-1{,}02$ dB — **revérifié** ci-dessous) | impose du cuivre |
| Sobriété : matière, encombrement, prix | $m$ faible | s'oppose au précédent |

S'y ajoute un effet physique rappelé par le professeur en mai 2026 : $r$ **s'ajoute à $R_e$** et augmente le $Q$ électrique total du grave, $Q'_{es}=Q_{es}\,(R_e+r)/R_e$ — la self ne se contente pas de perdre de la puissance, elle **désamortit le grave**. Avec $R_e\approx6{,}5\ \Omega$ [[à mesurer]], $r=1{,}6\ \Omega$ donne $Q'_{es}=1{,}25\,Q_{es}$ : ce n'est pas un détail.

> **Avertissement sur toutes les pertes d'insertion de cette section.** Elles sont calculées par le pont diviseur $r/(r+8)$, c'est-à-dire sur la charge **nominale** 8 Ω. C'est exactement l'hypothèse que le sujet v2 se donne pour mission de détruire : la charge réelle est $Z(f)$, et $|Z|>8\ \Omega$ presque partout dans la bande du grave (≈ 14 Ω à 100 Hz sur le modèle v1). Les chiffres en dB ci-dessous sont donc des **bornes supérieures** :

```
  r = 1.000 ohm : sur 8 ohm  -1.02 dB | sur 14 ohm  -0.60 dB | sur 30 ohm  -0.28 dB
  r = 1.637 ohm : sur 8 ohm  -1.62 dB | sur 14 ohm  -0.96 dB | sur 30 ohm  -0.46 dB
  r = 2.828 ohm : sur 8 ohm  -2.63 dB | sur 14 ohm  -1.60 dB | sur 30 ohm  -0.78 dB
```

Le chiffrage définitif se fera sur le $Z(f)$ mesuré en phase 1. On garde 8 Ω ici parce que c'est la convention du catalogue, donc le point de comparaison honnête avec le filtre « du commerce » qu'on cherche à battre.

### <a id="s05-2"></a>05.2 Inductance d'une bobine à air : la formule de Wheeler multicouche, en SI

Wheeler (1928) donne, pour une bobine multicouche de section rectangulaire, avec **$a$ = rayon moyen, $b$ = longueur axiale, $c$ = épaisseur radiale, toutes en pouces et $L$ en µH** :

$$L\ [\mu\text{H}] = \frac{0{,}8\,a^2N^2}{6a+9b+10c}$$

La formule est **homogène de degré 1** en longueur ($a^2/\text{longueur}$), donc le changement d'unités se fait par un simple facteur. Forme SI **sans ambiguïté** ($a,b,c$ en mètres, $L$ en henrys) :

$$\boxed{\,L=\frac{0{,}8\cdot10^{-6}}{0{,}0254}\cdot\frac{N^2a^2}{6a+9b+10c}=3{,}1496\cdot10^{-5}\ \frac{N^2a^2}{6a+9b+10c}\quad[\text{H, m}]\,}$$

Le coefficient vaut $3{,}1496\cdot10^{-5}$ H/m $=25{,}06\,\mu_0$ : il n'est **pas** un multiple simple de $\mu_0$, parce que la formule est un ajustement empirique et non un résultat exact.

**Test numérique sur un cas connu.** Modèle de référence indépendant : la bobine est discrétisée en spires filiformes circulaires coaxiales et $L=\sum_i\sum_{j\ne i}M_{ij}+\sum_iL_{ii}$, avec la formule de Maxwell $M=\mu_0\sqrt{r_1r_2}\left[(2/k-k)K(k)-(2/k)E(k)\right]$, $k^2=4r_1r_2/((r_1+r_2)^2+d^2)$, et $L_{ii}=\mu_0r(\ln(8r/\rho_{GMD})-2)$ où $\rho_{GMD}=0{,}44705\,s$ est la distance géométrique moyenne d'une cellule carrée de côté $s$.

```python
def K_E(m):                                    # K(m), E(m) par la moyenne arithmetico-geometrique
    a = np.ones_like(m); b = np.sqrt(1.0 - m); c = np.sqrt(m)
    somme = 0.5*c**2; p = 1.0
    for _ in range(30):
        a, b, c = 0.5*(a + b), np.sqrt(a*b), 0.5*(a - b); p *= 2.0
        somme = somme + 0.5*p*c**2
    K = np.pi/(2*a); return K, K*(1.0 - somme)

def mutuelle(r1, r2, dz):                      # formule de Maxwell
    m = 4*r1*r2/((r1 + r2)**2 + dz**2); K, E = K_E(m); k = np.sqrt(m)
    return MU0*np.sqrt(r1*r2)*((2/k - k)*K - (2/k)*E)

def wheeler_SI(N, a, b, c):                    # a, b, c en METRES ; L en HENRYS
    return 0.8e-6/0.0254*N**2*a**2/(6*a + 9*b + 10*c)
```

Sortie (`verif_brooks.py`) :

```
Controle K,E : m=0.5 -> [1.85407468] [1.35064388]   attendu [1.8540746773] [1.3506438810]
  geometrie          | Wheeler (mH) | mutuelles (mH) | ecart
  Brooks c=20mm N=576|     16.7941  |       16.9136  |  -0.71 %
  Brooks c=33mm N=400|     13.3633  |       13.4582  |  -0.71 %
  aplatie b=c/2      |     14.9123  |       15.0596  |  -0.98 %
  allongee b=2c      |      8.8294  |        8.8325  |  -0.04 %
```

**Wheeler est exact à mieux que 1 %** sur les géométries qui nous intéressent — bien en deçà des tolérances de fabrication (§ 05.12). C'est la formule à utiliser pour dessiner ; le modèle de mutuelles sert d'arbitre.

**Domaine de validité.** Wheeler énonce lui-même la restriction : la formule multicouche vaut tant qu'**aucune des trois dimensions $a$, $b$, $c$ n'écrase les autres** (rapports de l'ordre de 1 à 3 au plus). Les quatre cas testés ci-dessus respectent cette condition, et les selfs dimensionnées en § 05.7 sont des bobines de Brooks ($b=c=a/1{,}5$), donc en plein cœur du domaine. Hors domaine — solénoïde très long, ou galette très fine — il faut repasser au modèle de mutuelles.

### <a id="s05-3"></a>05.3 La bobine de Brooks : la constante, vérifiée (et une erreur à ne pas propager)

La **bobine de Brooks** (1931) est la bobine de section carrée dont les proportions maximisent $L$ à longueur de fil donnée : rayon intérieur $c$, rayon extérieur $2c$, longueur axiale $c$, donc **rayon moyen $a=1{,}5\,c$** et section carrée $c\times c$. Son inductance vaut

$$\boxed{\,L = 1{,}6994\cdot10^{-6}\ N^2\,a\quad[\text{H, }a\text{ en mètres}]\,}$$

> ⚠ **Correction importante.** La forme « $L\approx1{,}6994\,\mu_0N^2a$ » qui circule (et qui figurait dans la commande de rédaction de cette section) est **fausse** : elle multiplie par $\mu_0$ un coefficient qui vaut déjà $1{,}6994\ \mu$H/m. Elle surestime $L$ d'un facteur $\mu_0/10^{-6}=1{,}2566$, soit **+26 %**. La bonne écriture adimensionnée est $L = 1{,}3523\,\mu_0N^2a$.

Vérification (sommation de mutuelles, extrapolation de Richardson sur la finesse de grille) :

```
--- Constante de la bobine de Brooks (section carree, a = 1,5 c) ---
  n= 8  N=  64  L=  0.20873 mH   L/(N^2 a) =  1.6987 uH/m   L/(mu0 N^2 a) =  1.3518
  n=16  N= 256  L=  3.34078 mH   L/(N^2 a) =  1.6992 uH/m   L/(mu0 N^2 a) =  1.3522
  n=24  N= 576  L= 16.91365 mH   L/(N^2 a) =  1.6993 uH/m   L/(mu0 N^2 a) =  1.3523
  extrapolation n->infini : L/(N^2 a) = 1.6995 uH/m  => L/(mu0 N^2 a) = 1.3524
```

**Recoupement sur un cas publié** (bobine de Brooks $c=20$ mm, $N=200$, calculée par éléments finis à 2,033 mH par QuickField) :

| Méthode | $L$ |
|---|---|
| Formule de Brooks $1{,}6994\cdot10^{-6}N^2a$ | 2,0393 mH |
| Sommation de mutuelles (ce document) | 2,0392 mH |
| Éléments finis (source externe) | 2,033 mH |
| Wheeler SI | 2,0247 mH ($-0{,}71$ %) |
| Forme erronée $1{,}6994\,\mu_0N^2a$ | 2,5626 mH ($+26$ %) |

Trois méthodes indépendantes se recoupent à 0,3 % : la constante est établie.

### <a id="s05-4"></a>05.4 Pourquoi Brooks maximise $L$ à longueur de fil donnée

C'est un joli problème d'optimisation sous contrainte, faisable **entièrement à la main** avec la formule de Wheeler. Soit $\ell=2\pi aN$ la longueur de fil (spire moyenne).

> **Convention de remplissage, valable dans toute la section.** $A=\pi d^2/4$ est la section de **cuivre nu** (elle sert à $r=\rho_{Cu}\ell/A$ et $m=\rho_m\ell A$). Le remplissage de la fenêtre, lui, se compte en **cellules carrées du fil isolé** de côté $d_{isolé}=\gamma d$ : la fenêtre $b\times c$ contient les spires selon
> $$\boxed{\,b\,c\,k=N\,d_{isolé}^2\,},\qquad k\ \text{= fraction de l'aire de fenêtre occupée par ces cellules.}$$
> C'est ce que le code implémente. Écrire « $bck=NA$ » avec $A$ = cuivre nu serait une **autre** convention : les deux aires de cellule diffèrent de $d_{isolé}^2/(\pi d^2/4)=1{,}423$, et à même $k=0{,}85$ la lecture littérale donnerait $N=487$, $D_{ext}=119$ mm, $r=1{,}53\ \Omega$, $m=1{,}88$ kg au lieu de 454 / 137 mm / 1,64 Ω / 2,02 kg — **7 % d'écart sur la DCR et la masse**. (Les deux conventions se raccordent par $k_{équiv}=k\,\pi/(4\gamma^2)=0{,}60$.)

Seul le produit $abc$ intervient dans ce qui suit, donc le raisonnement de Lagrange est insensible à ce choix ; la reproductibilité des chiffres, elle, ne l'est pas. En reportant $N=\ell/(2\pi a)$ dans Wheeler :

$$L=\frac{3{,}1496\cdot10^{-5}\,a^2}{6a+9b+10c}\cdot\frac{\ell^2}{4\pi^2a^2}=\frac{3{,}1496\cdot10^{-5}}{4\pi^2}\cdot\frac{\ell^2}{6a+9b+10c}$$

À $\ell$ **et** $A$ fixés (donc à masse de cuivre fixée), maximiser $L$ revient donc à **minimiser $6a+9b+10c$**, sous la contrainte $abc=\text{cte}$. Multiplicateurs de Lagrange :

$$\nabla(6a+9b+10c)=\lambda\nabla(abc)\ \Longrightarrow\ 6=\lambda bc,\quad 9=\lambda ac,\quad 10=\lambda ab\ \Longrightarrow\ 6a=9b=10c$$

d'où $b/a = 6/9 = 0{,}667$ et $c/a=6/10=0{,}600$, à comparer à Brooks exact : $b/a=c/a=1/1{,}5=0{,}667$. **La longueur axiale est trouvée exactement ; l'épaisseur radiale à 10 % près** — l'écart mesure l'imprécision de Wheeler, pas une erreur de raisonnement.

Balayage numérique direct (modèle de mutuelles, $L\propto F(\beta,\gamma)(\beta\gamma)^{1/3}$ à $\ell$ et $A$ fixés, avec $\beta=b/a$, $\gamma=c/a$) :

```
    b/a \ c/a    0.400   0.500   0.600   0.667   0.750   0.900   1.100
        0.500    97.2%   98.6%   99.0%   98.9%   98.5%   97.3%   95.2%
        0.600    97.5%   99.1%   99.8%   99.8%   99.6%   98.5%   96.6%
        0.667    97.3%   99.1%   99.9%  100.0%   99.8%   98.9%   97.1%
        0.750    96.8%   98.8%   99.7%   99.9%   99.8%   99.1%   97.5%
    raffinement parabolique : b/a* = 0.689 , c/a* = 0.669   (Brooks : 0,667)
    Brooks           b/a=0.667 c/a=0.667 : L = 100.0 % de l'optimum
    optimum Wheeler  b/a=0.667 c/a=0.600 : L =  99.9 % de l'optimum
    a = b = c        b/a=1.000 c/a=1.000 : L =  97.6 % de l'optimum
    galette fine     b/a=0.300 c/a=0.300 : L =  91.4 % de l'optimum
    solenoide long   b/a=2.000 c/a=0.200 : L =  71.5 % de l'optimum
```

**Deux enseignements, le second plus important que le premier.** (i) Le calcul numérique **retrouve Brooks à 3 % près** ($b/a^\star=0{,}689$ contre 0,667) — et cet écart résiduel n'est pas un défaut, c'est **la signature même de** (ii). (ii) **L'optimum est très plat** : se tromper de 10 % sur les proportions coûte 0,1 % d'inductance, et même une bobine cubique n'en perd que 2,4 %. En revanche un solénoïde long perd 28 % : ce qu'il faut retenir n'est pas « viser 1,5 exactement » mais « ne pas bobiner long et fin ». Le même constat qu'en § 4.8 (l'optimum du filtre est plat) réapparaît ici — c'est un trait de méthode, pas une coïncidence.

### <a id="s05-5"></a>05.5 Le fil : table calculée

$A=\pi d^2/4$, $\Omega/\text{m}=\rho_{Cu}/A$, $\text{g/m}=\rho_m A$. Surépaisseur d'émail grade 2 prise à 0,08 mm pour $d\sim1$–2 mm [[à vérifier : IEC 60317, tables du fournisseur]].

| $d$ nu (mm) | $d$ émaillé (mm) | section (mm²) | Ω/m | g/m | € /m à 25 €/kg |
|---|---|---|---|---|---|
| 0,80 | 0,880 | 0,503 | 0,03422 | 4,50 | 0,113 |
| 1,00 | 1,080 | 0,785 | 0,02190 | 7,04 | 0,176 |
| 1,20 | 1,280 | 1,131 | 0,01521 | 10,13 | 0,253 |
| 1,40 | 1,480 | 1,539 | 0,01117 | 13,79 | 0,345 |
| 1,60 | 1,680 | 2,011 | 0,00855 | 18,02 | 0,450 |
| 2,00 | 2,080 | 3,142 | 0,00547 | 28,15 | 0,704 |
| 2,50 | 2,580 | 4,909 | 0,00350 | 43,98 | 1,100 |

### <a id="s05-6"></a>05.6 La loi $r\times m$ : démonstration, puis sa correction exacte

**Version « premier ordre », à géométrie de bobinage figée.** À forme et nombre de spires fixés, $L=1{,}6994\cdot10^{-6}N^2a$ ne dépend **pas** de la section du fil : $L$ fixé ⇒ $N$ et $a$ fixés ⇒ $\ell=2\pi aN$ **fixé**. Alors

$$r=\frac{\rho_{Cu}\,\ell}{A},\qquad m=\rho_m\,\ell\,A\qquad\Longrightarrow\qquad \boxed{\,r\times m=\rho_{Cu}\,\rho_m\,\ell^2=\text{cte}\,}$$

Le produit ne dépend plus de $A$ : **on n'échange la résistance contre rien d'autre que du cuivre**, dans un rapport fixé par la seule longueur de fil. Doubler la section divise $r$ par 2 et multiplie $m$ par 2.

**Pourquoi « ≈ ».** Grossir le fil grossit la fenêtre de bobinage, donc $a$ : la géométrie ne peut pas rester figée. En imposant la **forme** (proportions de Brooks) et non la taille : $b\,c\,k=N d_{isolé}^2$ avec $b\propto c\propto a$ donne $a\propto\sqrt{NA}$, d'où $L\propto N^2a\propto N^{5/2}A^{1/2}$. À $L$ fixé, $N\propto A^{-1/5}$, puis $\ell\propto Na\propto N^{3/2}A^{1/2}\propto A^{1/5}$ :

$$r\propto \frac{\ell}{A}\propto A^{-4/5},\qquad m\propto \ell A\propto A^{6/5},\qquad r\,m\propto A^{2/5},\qquad \boxed{\,m\,r^{3/2}=\text{cte à }\gamma\text{ constant}\,}$$

Cet invariant est **exact dans le modèle** (forme de Brooks, $k$ et $\gamma=d_{isolé}/d$ constants) ; en pratique il dérive de **±4 % sur la plage 0,8–2,5 mm**, parce que la surépaisseur d'émail (0,08 mm) ne se met pas à l'échelle du diamètre, donc $\gamma$ dépend de $d$. Vérification numérique en passant du fil de 1,0 mm à celui de 2,0 mm ($A\times4$) :

```
  section x4 (1,0 -> 2,0 mm) : r x0.325 [loi A^-4/5 : 0.330] , m x5.199 [A^6/5 : 5.278] ,
                               r*m x1.689 [A^2/5 : 1.741] , m*r^1,5 x0.963 [invariant : 1,000]
```

**$r\times m$ varie donc d'un facteur 1,7 sur cette plage — ce n'est pas une constante, c'est un ordre de grandeur.** En posant $\tau=L/r$ (la constante de temps de la self) :

$$\boxed{\,m = K_{Cu}\,\left(\frac{L}{r}\right)^{3/2}\,}\qquad
K_{Cu}=\frac{3\pi^2}{4}\,\frac{\rho_m\,\gamma}{\sqrt{k}}\left(\frac{8\rho_{Cu}}{K_B}\right)^{3/2}$$

avec $K_B=1{,}6994\cdot10^{-6}$ H/m. **Le diamètre du fil disparaît** : c'est le résultat central de cette section. Vérification (numérique par balayage vs formule analytique) :

```
  d =  0.8 mm : K_cu =  1823.2 kg.s^-3/2      d =  1.4 mm : K_cu =  1752.2 kg.s^-3/2
  d =  1.0 mm : K_cu =  1790.1 kg.s^-3/2      d =  2.0 mm : K_cu =  1723.8 kg.s^-3/2
  forme analytique (gamma pour d = 1,4 mm) : K_cu = 1752.2  [numerique : 1752.2]
```

**Barre d'erreur honnête sur $K_{Cu}$.** La dispersion de ±3 % ci-dessus ne vient que de $\gamma$. Or $K_{Cu}\propto1/\sqrt{k}$, et **le remplissage $k=0{,}85$ est le paramètre le moins maîtrisé du modèle** : il suppose un bobinage régulier en couches ordonnées. À la main, 0,75–0,80 est plus réaliste, et un bobinage désordonné descend à 0,70 :

```
  k = 0.70 : N = 437 , r = 1.702 ohm , m = 2.101 kg , Dext = 148 mm , K_cu = 1930.8
  k = 0.80 : N = 449 , r = 1.657 ohm , m = 2.045 kg , Dext = 140 mm , K_cu = 1806.1
  k = 0.85 : N = 454 , r = 1.637 ohm , m = 2.021 kg , Dext = 137 mm , K_cu = 1752.2
  k = 0.95 : N = 465 , r = 1.601 ohm , m = 1.976 kg , Dext = 131 mm , K_cu = 1657.4
```

**Valeur retenue pour la section 04 : $K_{Cu}\approx1760$ kg·s$^{-3/2}$ à ±10 %** (et non ±3 %), la contribution dominante étant $k$ et non $\gamma$. Deux remarques opposées mais toutes deux vraies : $K_{Cu}$ est sensible à $k$ (**+10 %** de 0,85 à 0,70), tandis qu'à **diamètre de fil donné** $r$ et $m$ ne bougent que de **4 %** sur la même plage — le modèle n'est donc pas fragile là où on l'utilise pour dessiner une bobine, seulement là où on l'utilise pour chiffrer une loi.

### <a id="s05-7"></a>05.7 Trois selfs de 18 mH, et une validation externe

```python
def brooks(L, d, k=0.85, email=0.08e-3):
    """Bobine de Brooks : rayon int. c, ext. 2c, longueur axiale c, rayon moyen a = 1,5c.
    L = 1,5 K_B d_iso N^2,5 / sqrt(k)  en combinant L = K_B N^2 a et c = d_iso sqrt(N/k)."""
    di = d + email
    N = (L*np.sqrt(k)/(1.5*K_B*di))**0.4
    c = di*np.sqrt(N/k); a = 1.5*c; ell = 2*np.pi*a*N
    return dict(N=N, c=c, a=a, ell=ell, r=RHO_E*ell/section(d), m=RHO_M*section(d)*ell)
```

```
 d(mm)| N   | c(mm)| Dext(mm)| fil(m)| DCR(ohm)| cuivre(kg)| prix(EUR)|  r*m  | m*r^1.5| L/r(ms)
  1.0 |  515|  26.6|   106.4 | 129.1 |   2.828 |    0.909  |    22.7  |  2.57 |  4.323 |   6.36
  1.4 |  454|  34.2|   136.9 | 146.5 |   1.637 |    2.021  |    50.5  |  3.31 |  4.231 |  11.00
  2.0 |  396|  44.9|   179.7 | 167.9 |   0.919 |    4.725  |   118.1  |  4.34 |  4.163 |  19.59
```

Pertes d'insertion correspondantes sur charge nominale 8 Ω (borne supérieure, cf. § 05.1), et contrôle du nombre de contrôle du dépôt :

```
  d = 1.0 mm, r = 2.828 ohm : fraction dissipee = 26.1 %, attenuation = -2.63 dB
  d = 1.4 mm, r = 1.637 ohm : fraction dissipee = 17.0 %, attenuation = -1.62 dB
  d = 2.0 mm, r = 0.919 ohm : fraction dissipee = 10.3 %, attenuation = -0.94 dB
  verification du nombre de controle : r = 1,00 ohm -> 11.1 % et -1.02 dB
```

**Validation externe du modèle sur trois références de catalogue**, sans aucun paramètre ajusté :

```
  Mundorf BL140    2 mH / 1,4 mm  : modele 0.438 ohm vs catalogue 0.43 -> +1.9 %
  Mundorf BL140  1,5 mH / 1,4 mm  : modele 0.369 ohm vs catalogue 0.38 -> -3.0 %
  Mundorf serie L 18 mH / 0,71 mm : modele 4.951 ohm vs catalogue 4.77 -> +3.8 %
```

**Le modèle prédit la DCR à ±4 %, dont un point exactement à la valeur cible de 18 mH.** C'est la meilleure preuve disponible que la chaîne Brooks → longueur de fil → DCR est correcte, et elle est validée **là où on va l'utiliser** — un point unique à 2 mH aurait été une validation à 9 fois la valeur d'intérêt. (Les diamètres extérieurs prédits dépassent le catalogue d'environ 20 % — 88 mm contre 70 pour la BL140, 83 contre 70 pour la L71 — parce que le fabricant ne bobine pas exactement en Brooks. Seule la DCR, qui ne dépend que de $\ell$ et $A$ et non de la forme, est prédite finement : c'est bien elle qu'on utilise.)

Ordre de grandeur qui reste : ces trois selfs de 18 mH pèsent **de 0,9 à 4,7 kg de cuivre et mesurent 11 à 18 cm de diamètre** — le filtre passif de grave est un objet lourd, et c'est précisément l'argument « matière » du thème.

### <a id="s05-8"></a>05.8 Formulation de l'optimisation : minimiser le cuivre sous contraintes

$$\min_{d,\,N,\,a,\,b,\,c}\ m=\rho_m\ell A \quad\text{s.c.}\quad
\begin{cases}
L(N,a,b,c)=18\ \text{mH} & \text{(cible)}\\[2pt]
r=\rho_{Cu}\ell/A\le r_{max} & \text{(pertes)}\\[2pt]
b\,c\,k=N\,d_{isolé}^2 & \text{(remplissage)}\\[2pt]
J=I_{max}/A\le J_{max} & \text{(thermique)}\\[2pt]
d\le d_{dispo} & \text{(approvisionnement)}
\end{cases}$$

La § 05.6 **résout le cœur du problème analytiquement** : à $L$ fixé, $m=K_{Cu}(L/r)^{3/2}$ est strictement décroissante en $r$, donc l'optimum sature la contrainte de pertes, $r^\star=r_{max}$, et

$$\boxed{\,m^\star = K_{Cu}\left(\frac{L}{r_{max}}\right)^{3/2}\,}$$

la forme optimale étant celle de Brooks (§ 05.4). Il ne reste qu'à trouver le diamètre de fil qui réalise $r_{max}$ (dichotomie sur `brooks`) — puis à **vérifier les deux contraintes de terrain que le programme initial oubliait**, et qui sont précisément celles qui pilotent le critère « robustesse » de la feuille de route :

```
  I(350 W/8 ohm) = 6.61 A eff ; I(10 W/8 ohm) = 1.12 A eff
 r_max| d(mm) |  N  | m(kg) |prix(EUR)|Dext(mm)| dB/8ohm| J(A/mm2)| P_J 350W | P_J 10W | dT 1min | ddcr
  0.50| 2.917 |  343| 11.632|   290.8 |  240.7 |  -0.53 |    0.99 |    21.9 W|   0.62 W|  +0.3 K | +0.1 %
  0.75| 2.268 |  378|  6.380|   159.5 |  198.0 |  -0.78 |    1.64 |    32.8 W|   0.94 W|  +0.8 K | +0.3 %
  1.00| 1.898 |  405|  4.171|   104.3 |  172.6 |  -1.02 |    2.34 |    43.8 W|   1.25 W|  +1.6 K | +0.6 %
  1.50| 1.477 |  445|  2.297|    57.4 |  142.6 |  -1.49 |    3.86 |    65.6 W|   1.88 W|  +4.5 K | +1.7 %
  2.00| 1.237 |  476|  1.507|    37.7 |  124.7 |  -1.94 |    5.50 |    87.5 W|   2.50 W|  +9.1 K | +3.6 %
  3.00| 0.964 |  522|  0.834|    20.9 |  103.6 |  -2.77 |    9.05 |   131.3 W|   3.75 W| +24.5 K | +9.6 %
```

(Échauffement **adiabatique** sur 1 min, $\Delta T=P_J t/(mc_p)$ avec $c_p=385$ J/kg/K : c'est un **majorant**, il néglige toute évacuation vers l'air. Densité de courant admissible pour un conducteur enterré sous ~20 couches : **2 à 3 A/mm²** en régime permanent [[ordre de grandeur à geler avec les critères]]. Les deux niveaux d'écoute restant à geler, 350 W et 10 W sont ici des bornes, pas les niveaux de l'expérience.)

**Lecture — et c'est le résultat le plus utile de la section.** Les deux contraintes ajoutées **mordent aux deux extrémités du tableau** :

- **En haut** (pertes faibles), c'est l'**approvisionnement** qui bloque : $d=1{,}9$ à 2,9 mm de fil émaillé n'est ni bobinable à la main, ni couramment vendu au détail [[à vérifier par devis : les distributeurs consultés ne publient pas leur gamme de diamètres]]. Ces lignes ne sont pas des designs, ce sont des bornes théoriques.
- **En bas** (cuivre économe), c'est la **thermique** qui bloque : à $r_{max}=3\ \Omega$ on est à 9 A/mm², la self encaisse 131 W et dérive de **+9,6 % de DCR en une minute** au niveau fort. C'est-à-dire que le filtre « pas cher » **échoue par construction au critère de robustesse** : $f_0$ et l'amortissement du grave ne sont plus les mêmes à faible et à fort niveau. On peut *prédire* la dérive thermique avant de la mesurer — c'est le seul endroit du projet où c'est possible.
- **La fenêtre praticable est donc $r_{max}\approx1{,}5$ à 2 Ω**, soit 1,5 à 1,9 dB d'insertion sur 8 Ω (0,9 à 1,1 dB sur la charge réelle), 1,5 à 2,3 kg de cuivre par self et un fil de 1,2 à 1,5 mm. C'est l'arbitrage à geler avec les autres critères.

Enfin, la loi d'échelle reste le chiffre à retenir : passer de $-2{,}8$ dB à $-0{,}5$ dB coûte **14 fois plus de cuivre** (0,83 → 11,6 kg). **L'exposant $3/2$ est ce qui rend le passif structurellement coûteux en matière dans le grave.**

### <a id="s05-9"></a>05.9 Ce que la section 04 doit reprendre : `dcr(L)` et `prix_L(L)`

La § 4.5 utilise deux placeholders : `dcr(L) = 1.0*L/18e-3` (linéaire) et `prix_L(L) = 4.0 + 1.2*L/1e-3`. Avant de les remplacer, **il faut voir ce qu'ils disaient sans le dire — et qu'ils se contredisent.**

- **À masse de cuivre imposée** $m$ : $r(L)=L\,(K_{Cu}/m)^{2/3}$, donc $r\propto L$ — **le placeholder linéaire est exactement ce modèle**, et il correspond à $m = K_{Cu}(18\text{ mH}/1\,\Omega)^{3/2} = \mathbf{4{,}25}$ **kg de cuivre par self, soit 106 € de fil.**
- **Mais** `prix_L(18 mH)` $= 4{,}0 + 1{,}2\times18 = \mathbf{25{,}6}$ **€**, ce qui achète 1,02 kg de cuivre, soit $r=2{,}58\ \Omega$.

> ⚠ **Les deux placeholders sont mutuellement incohérents d'un facteur 4,2 en masse et 2,6 en DCR.** L'optimiseur de la phase 3 achète actuellement une self au prix d'une bobine de 1 kg tout en lui prêtant la DCR d'une bobine de 4,25 kg : il croit obtenir un filtre passif à la fois **bon marché et peu résistif**, ce qui n'existe pas. Ce n'est pas une imprécision d'ordre de grandeur, c'est un **bug de modélisation** qui biaise structurellement l'arbitrage passif/actif en faveur du passif, et qui pousse en prime vers les fortes inductances. C'est le résultat que cette section doit remonter en priorité à la § 04.

- **À diamètre de fil imposé** $d$ : $N\propto L^{2/5}$, $a\propto L^{1/5}$, $\ell\propto L^{3/5}$, donc **$r$ et $m$ varient en $L^{3/5}$** — c'est le modèle réaliste quand on achète une seule bobine de fil.

```
  (a) m = 2.0 kg/self : r(10 mH) =  0.92 ohm ; r(18 mH) =  1.65 ohm ; r(27 mH) =  2.48 ohm
  (b) d = 1,4 mm :  L(mH) | N   | r(ohm)| m(kg) | (L/18)^0,6 | r/r(18 mH)
                      4.7 |  265| 0.731 | 0.903 |    0.447   |    0.447
                     10.0 |  359| 1.150 | 1.420 |    0.703   |    0.703
                     18.0 |  454| 1.637 | 2.021 |    1.000   |    1.000
                     27.0 |  534| 2.088 | 2.577 |    1.275   |    1.275
                     47.0 |  667| 2.911 | 3.594 |    1.779   |    1.779
```

**Livrable exécutable pour la § 4.5** — un seul modèle cohérent, où $r$ cesse d'être une fonction de $L$ pour devenir une **variable de conception à part entière** :

```python
K_CU    = 1760.0      # kg.s^-3/2, section 05.6 (+/- 10 %, dominee par le remplissage k)
PRIX_KG = 25.0        # EUR/kg  [[ordre de grandeur NON SOURCE, a remplacer par un devis]]
J_MAX   = 3.0         # A/mm2   [[a geler avec les criteres]]
D_MAX   = 1.5e-3      # m, plus gros fil approvisionnable [[a verifier par devis]]

masse_L      = lambda L, r: K_CU*(L/r)**1.5                    # kg de cuivre
prix_L       = lambda L, r: PRIX_KG*masse_L(L, r)              # EUR
insertion_dB = lambda r, Z: 20*np.log10(1 + r/np.abs(Z))       # sur la charge REELLE Z(f)
# contraintes : brooks(L, d)["r"] == r  avec  d <= D_MAX  et  I_max/section(d) <= J_MAX
```

**Pondérations : le pont qu'il faut faire.** La § 4.5 exprime les pertes en $w_W$ = 1 dB/W à $P_{ref}=10$ W, alors que le tableau ci-dessous les exprime en $w_{dB}$ (dB par dB d'insertion). Les deux se raccordent : à 10 W dans 8 Ω, $P_{Joule}\simeq10\,r/(r+8)$, et le rapport $P_{Joule}/\text{insertion(dB)}$ vaut 1,117 / 1,086 / 1,020 / 0,986 pour $r=0{,}5$ / 1 / 2,24 / 3 Ω. **Donc $w_W=1$ dB/W équivaut à $w_{dB}=1$ dB/dB à 2 % près** sur toute la plage utile : la ligne $w_{dB}=1$ **est** la réponse de la § 4.5.

| $w_€$ (dB/€) | $w_{dB}$ | $r^\star$ (Ω) | cuivre (kg) | prix (€) | insertion /8 Ω (dB) |
|---|---|---|---|---|---|
| 0,04 | 0,5 | 3,05 | 0,80 | 20 | −2,80 |
| **0,04** | **1,0** ← § 4.5 | **2,24** | **1,27** | **32** | **−2,15** |
| 0,04 | 2,0 | 1,66 | 1,99 | 50 | −1,64 |
| 0,04 | 4,0 | 1,23 | 3,10 | 77 | −1,25 |

**Conclusion à porter en § 4.5** : avec « 25 € ≡ 1 dB » et « 1 W ≡ 1 dB », l'optimiseur achèterait une self à 2,2 Ω, soit **2,1 dB de pertes d'insertion** et — d'après la § 05.8 — 5,5 A/mm² et une dérive thermique de plusieurs pour-cent. Vraisemblablement inacceptable. Il faut soit alourdir $w_{dB}$, soit ajouter la **contrainte dure** $r\le r_{max}\approx1{,}5$–2 Ω (décision étudiant, à geler avec les autres critères). Les pondérations ne sont pas un détail de calcul : **elles choisissent la self**.

**Le cas de $L_2$, en dérivation.** $L_2$ est en parallèle (§ 4.1) : sa DCR **ne coûte pas de pertes d'insertion dans la bande passante du médium**. Mais « à moindre conséquence » serait faux, car elle agit sur deux autres critères gelés :

```
  cellule passe-haut C2 = 150 uF, L2 = 18 mH, charge 8 ohm
  f =   100 Hz :   r2=0.200 ->  -2.57 dB   r2=1.637 ->  -3.30 dB   r2=3.000 ->  -3.88 dB
  f =    10 Hz :   r2=0.200 -> -39.52 dB   r2=1.637 -> -36.15 dB   r2=3.000 -> -33.16 dB
```

Entre $r_2=0{,}2$ et 3 Ω, la réponse des médiums **au raccord** se déplace de **1,3 dB** — du même ordre que l'écart RMS de 1 à 2 dB visé par le critère « fidélité du raccord », et avec un effet sur la phase qui compte directement pour la sommation des deux voies (inversion de polarité obligatoire du 2ⁿᵈ ordre Butterworth). Et en bande coupée profonde, la DCR fixe un **plancher de réjection** : $-33$ dB au lieu de $-40$ dB à 10 Hz, soit **6 dB de protection en excursion perdue** pour les médiums — c'est-à-dire une part de la raison d'être du filtre. $L_2$ doit donc rester une **variable d'optimisation à part entière**, avec son propre diamètre de fil, mais **pas un paramètre libre**. (Le code de la § 4.6 modélise déjà correctement `r2 = dcr(L2)` ; c'est seulement la prose qu'il fallait corriger.)

### <a id="s05-10"></a>05.10 Coût du fil, budget réel, et ce que le marché vend vraiment à 18 mH

**Prix du fil.** Les distributeurs français consultés (E44, ATEC France) **ne publient aucun prix au kg** pour les diamètres qui nous intéressent : ATEC facture « au cours du cuivre + plus-value de transformation » sur devis, E44 affiche « à partir de 4,90 € » sans masse associée. La valeur **25 €/kg** retenue dans toute cette section est donc un **ordre de grandeur NON SOURCÉ** (cuivre matière ≈ 9–10 €/kg + transformation), [[à remplacer par un devis avant l'achat de la phase 4]]. **Tous les montants en € de cette section lui sont strictement proportionnels** : un prix réel de 20 ou 35 €/kg les multiplie par 0,8 ou 1,4.

**Budget réel, pour le bon nombre de selfs.** La feuille de route demande d'assembler **deux** filtres (catalogue 18/18 mH et optimisé, typiquement 27/12 mH en § 4.8) : c'est **4 selfs**, pas 2.

```
  tout en 1.0 mm :  524 m de fil,   3.69 kg,    ~92 EUR ; DCR(18 mH) = 2.828 ohm (-2.63 dB)
  tout en 1.4 mm :  595 m de fil,   8.20 kg,   ~205 EUR ; DCR(18 mH) = 1.637 ohm (-1.62 dB)
  tout en 2.0 mm :  681 m de fil,  19.18 kg,   ~480 EUR ; DCR(18 mH) = 0.919 ohm (-0.94 dB)
```

Le scénario 2,0 mm consomme **à lui seul la quasi-totalité du budget de 500 €**, avant condensateurs, $R_{ref}$, wattmètre et carte son : il est hors de portée. Et pour un **couple** de selfs de 18 mH, le cuivre seul coûte 212 € à $r_{max}=1\ \Omega$, 116 € à 1,5 Ω, 75 € à 2 Ω, 41 € à 3 Ω.

> ⚠ **L'enveloppe « 60 à 150 € » et la ligne « selfs bobinées maison ≈ 25 €/pièce » de FEUILLE-DE-ROUTE.md ne sont pas des choix techniques : ce sont des choix de DCR déguisés.** 25 €/self = 1 kg de cuivre = **$r=2{,}6\ \Omega$ = $-2{,}5$ dB**, c'est-à-dire exactement la self que la § 05.8 vient de disqualifier sur la thermique. L'enveloppe 60–150 € correspond à $r_{max}\approx1{,}5$–2,5 Ω. **C'est le premier arbitrage à geler avec les critères**, et il faut l'écrire comme tel dans la feuille de route.

**Ce que le marché vend réellement à 18 mH** — et c'est l'argument le plus direct dont dispose le sujet :

| Référence | Type | DCR | insertion /8 Ω | masse | prix |
|---|---|---|---|---|---|
| Mundorf série L, 18 mH, fil 0,71 mm | **à air** | 4,77 Ω | $-4{,}1$ dB | ~0,4 kg Cu | — |
| Jantzen 6595, 18 mH, 14 AWG | **noyau torique fer** | 0,174 Ω | $-0{,}19$ dB | 1,29 kg total | ≈ 80 £ |
| DIY à air, 18 mH, fil 2,0 mm (§ 05.7) | à air | 0,919 Ω | $-0{,}94$ dB | 4,73 kg Cu | ≈ 118 € de cuivre |

**Trois conclusions, toutes honnêtes.** (i) **Le marché ne vend pas de self à air de 18 mH à faible DCR** : la seule référence à air de Mundorf à cette valeur est bobinée en 0,71 mm et fait 4,77 Ω, inutilisable ; Jantzen ne monte pas au-delà de 15 mH en 14 AWG à air. Ce fait de catalogue, vérifiable, démontre mieux qu'un calcul que « le filtre passif de grave est un objet lourd » : **l'objet n'existe pas parce qu'il pèserait 5 kg**. (ii) Face au vrai concurrent à 18 mH — la self **à noyau** —, le DIY à air est **plus cher et plus résistif** : l'argument du DIY n'est **pas** économique, et il ne faut pas prétendre le contraire. (iii) La comparaison « Mundorf BL140 2 mH à 48,90 € pour 13,5 € de cuivre, rapport 3,6 » doit rester **une validation du modèle** (§ 05.7) et **jamais un argument de budget** : elle est établie sur une self 9 fois plus petite que la cible, dans un régime où le concurrent à air existe encore.

**La vraie thèse à assumer** : on bobine à air non pas pour économiser, mais pour (a) la **linéarité** — pas de $L(I)$, pas de dérive de $f_0$ avec le niveau, ce qui est précisément le critère « robustesse » ; (b) la **maîtrise métrologique** — on connaît $N$, $\ell$, $m$, $r$, et on peut tous les mesurer ; (c) la **liberté de valeur** — une inductance E12 non cataloguée est accessible sans surcoût.

### <a id="s05-11"></a>05.11 Alternative noyau ferrite/fer : ce qu'on gagne, ce qu'on risque

Un noyau de perméabilité relative $\mu_r$ multiplie $L$ à $N$ donné, donc permet **moins de spires, moins de fil, moins de cuivre et moins de DCR** pour la même inductance. Ordre de grandeur mesurable sur catalogue : la self torique à noyau de fer 18 mH bobinée en 14 AWG (1,63 mm) est annoncée à **0,174 Ω** et **1,29 kg au total**, quand le modèle Brooks donne **1,282 Ω** et **2,89 kg de cuivre seul** avec le même fil à l'air (155 m, Ø 153 mm). Soit un **facteur 7,4 sur la DCR** et un gain de matière **établi** (et non plus supposé) d'un facteur > 2.

> **Note de source à retenir pour l'oral.** Certains revendeurs étiquettent cette référence « Air Core » ; c'est **faux**, et le calcul ci-dessus le prouve : une self à air de 18 mH en 1,6 mm demande 2,89 kg de cuivre et 153 mm de diamètre, pas 1,29 kg dans une enveloppe Ø105 × 36 mm. Ne citer que le revendeur qui écrit correctement « toroidal iron core ». Un désaccord de catalogue tranché par un modèle de prépa : c'est une bonne anecdote de soutenance.

**Le prix à payer est la saturation.** Argument énergétique, quantitatif et de niveau prépa : la self doit stocker $W=\tfrac12LI^2$, et un matériau ne peut stocker que $w=B^2/2\mu$ par unité de volume, plafonnée par $B_{sat}$.

```
  P =  350.0 W dans 8 ohm : V = 52.92 V RMS, I = 6.61 A RMS (9.35 A crete),
                            energie stockee 0,5 L I_crete^2 = 0.7875 J
  self A AIR 18 mH / 1,4 mm : volume englobant = 503 cm3 -> w = 1565 J/m3
  poudre de fer, mu_r ~ 60             : B_sat = 1.00 T, w_max =   6631 J/m3 -> V_mini =  118.75 cm3
  ferrite entrefer, mu_r,eff ~ 100     : B_sat = 0.35 T, w_max =    487 J/m3 -> V_mini = 1615.68 cm3
  tole Fe-Si non entrefere, mu_r ~ 4000: B_sat = 1.60 T, w_max =    255 J/m3 -> V_mini = 3092.51 cm3
```

**Lecture du champ, avec les bonnes étiquettes.** $\sqrt{2\mu_0\langle w\rangle}=63$ mT est un **champ moyen au sens énergétique** sur le volume englobant, donc un **minorant** du champ réel : au cœur du bobinage, l'ordre de grandeur solénoïdal $\mu_0NI_{crête}/b=1{,}257\cdot10^{-6}\times454\times9{,}35/0{,}0342$ vaut **0,16 T**, deux fois et demie plus. Dans les deux cas on est trois ordres de grandeur sous tout $B_{sat}$ — mais surtout **l'argument vrai est qualitatif** : $\mu_r=1$, la relation $B(H)$ de l'air est **rigoureusement linéaire**, elle ne sature à aucun champ. Le calcul ne sert qu'à situer l'ordre de grandeur face aux $B_{sat}$ des noyaux.

Avec un noyau, il faut au minimum **~120 cm³ de poudre de fer** pour stocker 0,79 J sans saturer ; en dessous, $L$ chute avec le courant, $f_0$ dérive avec le niveau et le noyau engendre de la distorsion harmonique. **Et la marge du produit du commerce est faible** : l'enveloppe de la Jantzen 6595 fait 312 cm³ **cuivre compris**, pour un minimum calculé de 119 cm³ de poudre de fer. Le [[à mesurer]] ci-dessous n'est donc pas une curiosité, c'est une manip **à forte probabilité de résultat positif**.

**Position retenue** : self à air pour le filtre de référence et le filtre optimisé. Le noyau reste une **perspective** — et le meilleur satellite disponible de cette section : [[à mesurer]] **$L$ à 0,1 A et à 5 A sur une self à noyau du commerce**, au banc d'impédance de la § 02. Si $L$ bouge, on a mesuré de ses propres mains le compromis matière/linéarité que tout le sujet met en évidence.

### <a id="s05-12"></a>05.12 Fabrication pratique

- **Mandrin** : tube rigide de diamètre extérieur $2c$ (68 mm pour la version 1,4 mm, puisque le rayon intérieur du bobinage vaut $c=34{,}2$ mm), joues en contreplaqué espacées de $c$ (34 mm), démontable. Axe traversant pour une perceuse à vitesse lente ou une manivelle — **indispensable**, pas optionnel (voir le temps de bobinage ci-dessous).
- **Comptage des spires** : $N\approx454$ pour la version 1,4 mm. La sensibilité $\mathrm{d}L/L=2\,\mathrm{d}N/N$ vaut **à rayon moyen figé** ; en pratique les spires supplémentaires s'empilent vers l'extérieur, $a$ croît avec $N$, et la sensibilité réelle est plus forte :

```
  dN | 2dN/N  | mandrin fixe (joues figees, Wheeler) | forme de Brooks maintenue (L ~ N^2,5)
   1 |  0.44 % |                0.49 %                |                0.55 %
   5 |  2.20 % |                2.44 %                |                2.77 %
  20 |  8.80 % |                9.97 %                |               11.37 %
```

  Retenir $\mathrm{d}L/L\approx2{,}2$ à $2{,}5\,\mathrm{d}N/N$, soit **2,4 à 2,8 % pour ±5 spires**. La conclusion est inchangée : 5 spires sont sans conséquence devant la tolérance des condensateurs (±10–20 %, § 4.5), 20 spires ne le sont plus. Compteur mécanique, ou comptage par couche (spires par couche $=c/d_{isolé}\approx23$) avec pointage écrit.
- **Ajustement final de $L$ — on n'atteint jamais 18,00 mH en comptant.** Procédure : bobiner **2 à 3 % de spires en trop**, mesurer $L$ au banc de la § 02 (§ 05.13), puis **dérouler spire à spire jusqu'à la cible**, en remesurant. C'est ce que le tableau de sensibilité ci-dessus appelle, et c'est la seule façon de tenir une valeur à mieux que 1 %.
- **Prises intermédiaires : l'économie que le projet ne doit pas manquer.** Puisque $L\propto N^2a$, une **prise** soudée en cours de bobinage donne une inductance plus faible **sur la même bobine**, sans rebobiner. Une seule bobine par voie, munie de deux ou trois prises, fournit à la fois la valeur « catalogue » (18 mH) et la valeur « optimisée » (12 ou 27 mH selon la voie) : cela **divise par deux le cuivre, le prix et le temps de bobinage**, et surtout cela permet de comparer le filtre catalogue et le filtre optimisé **sur le même objet physique**, donc sans biais de fabrication. [[à vérifier]] : la prise doit être prise sur la couche, pas au milieu d'une couche, et le tronçon inutilisé reste couplé — il faut le laisser **en circuit ouvert** et vérifier au banc que $L$ mesurée sur la prise est bien la valeur voulue.
- **Couplage mutuel entre $L_1$ et $L_2$ : le piège classique du filtre passif.** Deux bobines à air de 14 cm de diamètre posées côte à côte sur la même planche se couplent. Le coefficient $k=M/L$ ne dépend que de l'entraxe rapporté au diamètre (grandeur purement géométrique), cas **coaxial = pire cas** :

```
   D (mm) | D/Dext | k = M/L | effet sur L
       70 |   0.51 |  0.1854 |  +18.5 %
      137 |   1.00 |  0.0458 |   +4.6 %
      274 |   2.00 |  0.0074 |   +0.7 %
      400 |   2.92 |  0.0025 |   +0.3 %
```

  **À un diamètre d'écartement, le couplage vaut encore 4,6 % — deux fois l'effet de ±5 spires.** Il fausserait la comparaison prédit/mesuré de la phase 4, et il est **gratuit à éviter** : axes **perpendiculaires** (le flux croisé s'annule par symétrie), ou à défaut **écartement supérieur à deux diamètres**. À traiter avec la même autorité que les forces de Laplace.
- **Tension du fil** : régulière et modérée — trop faible, le bobinage gonfle, $a$ augmente et $L$ dépasse la cible ; trop forte, l'émail se fend (court-circuit entre spires ⇒ spire en court-circuit, $L$ s'effondre). Fil déroulé depuis une bobine libre en rotation, jamais tiré latéralement.
- **Isolation entre couches** : 23 couches de fil émaillé grade 2 mettent quelques dizaines de volts entre couches adjacentes en régime normal, et davantage sur un transitoire ou à la coupure d'un courant continu. Un papier isolant intercalaire est prudent — mais il **dégrade $k$**, donc majore $r$ et $m$ de quelques pour-cent (§ 05.6) : c'est un compromis à assumer, pas un détail gratuit.
- **Vernis / immobilisation** : imprégner ou ligaturer (colliers, ruban de lin) — une spire mobile fait varier $L$ et **vibre** à 100 Hz sous les forces de Laplace ($I$ crête ≈ 9,4 A).
- **Temps de bobinage réaliste** : 454 spires de fil de 1,4 mm, c'est **2 kg de fil raide**. À la main, sans mandrin monté sur perceuse lente et sans dérouleur, compter **une demi-journée par self** ; avec l'outillage, **1 à 2 h**. Rapporté aux 4 selfs du projet (ou 2 avec prises), l'écart entre 8 h et 2 jours de travail n'est pas un détail de planning en phase 4 (déc. 2026 – fév. 2027). [[à confirmer par l'expérience sur la première self]]
- **Comptabilité matière honnête** : le tableau ne compte que le **cuivre**. Mandrin (contreplaqué + tube), vernis, colliers, cosses : **quelques centaines de grammes et quelques euros par self**, [[à chiffrer sur la facture réelle]]. Pour le tableau comparatif final du critère « encombrement/matière », c'est le **filtre complet** qu'il faut porter : 2 selfs de 1,4 mm + 2 condensateurs + support ≈ **4,5 kg et ~3 L** — à comparer au boîtier du filtre actif.
- **Repli si le bobinage échoue ou si le calendrier dérape** (la feuille de route en a un pour chaque phase sauf celle-ci) : **acheter la self à noyau de 18 mH** (0,174 Ω, ≈ 80 £) comme self de grave, et faire de la **comparaison air/noyau** le sujet du satellite (§ 05.11). Un échec de fabrication devient alors un résultat expérimental.

### <a id="s05-13"></a>05.13 Mesure de $L$ : d'abord le banc d'impédance, la résonance en contre-vérification

**Méthode principale — le banc de la § 02, sur la self seule.** C'est la clé de voûte du projet, déjà étalonnée en phase 1 : il mesure $Z(f)$ en module et en phase. Sur une self, il suffit de lire

$$L=\frac{\Im\mathrm{m}(Z)}{\omega}=\frac{|Z|\sin\varphi}{\omega}$$

**Aucun condensateur n'intervient, donc aucune incertitude sur $C$ n'est importée.** L'incertitude est portée par l'étalonnage du module et de la phase :

```
  f =    50 Hz : |Z| =   5.89 ohm, phi = 73.86 deg     f =   200 Hz : |Z| =  22.68 ohm, phi = 85.86 deg
  f =   100 Hz : |Z| =  11.43 ohm, phi = 81.76 deg     f =   400 Hz : |Z| =  45.27 ohm, phi = 87.93 deg
  u|Z| = 2 %, u(phi) = 0.5 deg -> u(L)/L = 2.00 %   (a 100 Hz)
  u|Z| = 3 %, u(phi) = 1.0 deg -> u(L)/L = 3.01 %
```

Faire la lecture à **plusieurs fréquences** (50 / 100 / 200 / 400 Hz) : $L$ doit être constant. C'est en prime le **contrôle de linéarité** de la self, et à fort courant le test $L(I)$ de la § 05.11.

**Contre-vérification indépendante — la résonance série avec un $C$ connu.** On met la self en série avec un condensateur connu et une résistance étalon, et on balaie au GBF :

$$f_0=\frac{1}{2\pi\sqrt{LC}}\qquad\Longrightarrow\qquad L=\frac{1}{4\pi^2f_0^2C}$$

```
  L = 18.0 mH , C = 150.0 uF -> f0 =  96.86 Hz ; L relu = 1/(4 pi^2 f0^2 C) = 18.00 mH
  L = 18.0 mH , C = 100.0 uF -> f0 = 118.63 Hz ; L relu = 18.00 mH
  L = 27.0 mH , C = 100.0 uF -> f0 =  96.86 Hz ; L relu = 27.00 mH
```

**Le nombre de contrôle du dépôt (« 18 mH + 150 µF ⇒ ≈ 97 Hz ») est confirmé : 96,86 Hz** — et c'est bien le **pôle** du couple $L$–$C$, distinct des repères $-3$ dB à 99,9 et 93,9 Hz (mi-puissance $-3{,}0103$ dB ; 99,8 et 94,0 Hz au seuil littéral $-3{,}000$ dB — différence de convention, § 04.1), et distinct de $f_c$, qui est le croisement des deux voies (cf. l'encadré de convention en tête de section).

> ⚠ **Correction de protocole : ne pas chercher le maximum de courant.** Le $Q=\sqrt{L/C}/r=6{,}7$ est celui de la **branche $L$–$C$–$r$ seule**. Le montage réel ajoute $R_{ref}$ **et** l'impédance de sortie du GBF (~50 Ω) :
>
> ```
>   branche seule    : Q_montage =  6.692        GBF 50 ohm seul : Q_montage = 0.212
>   avec R_ref =   1 : Q_montage =  4.154        R_ref = 100 ohm : Q_montage = 0.108
> ```
>
> **À $Q<0{,}5$ il n'y a plus aucun maximum de courant à pointer** : avec le montage de la § 02.1 tel quel ($R_{ref}=100\ \Omega$), la tension aux bornes de $R_{ref}$ ne varie pas de façon mesurable sur ±0,5 % autour de $f_0$. Le bon observable existe, et il est excellent : **la tension aux bornes de la paire $L+C$**, qui présente un **creux profond** indépendant de l'impédance de source.
>
> ```
>   |V_LC|/|V| avec R_ref = 100 ohm : minimum = 0.0161 exactement a 96.859 Hz
>   le creux double de profondeur en +/- 12.5 Hz
>   pente de phase de V_LC : 7.79 deg/Hz  ->  3.8 deg pour 0,5 % de f0
> ```
>
> Le **passage de la phase de $V_{LC}$ par zéro**, à 7,8 °/Hz, est parfaitement lisible à l'oscilloscope : c'est la même technique qu'en § 02.3. (Variante acceptable si l'on tient au maximum de courant : $R_{ref}\le1\ \Omega$ **et** une source de faible impédance — attaquer par l'ampli E-800, $Z_s<0{,}1\ \Omega$ — ce qui remonte $Q$ à 4,2.)

**Incertitude de la méthode par résonance** : $u(L)/L=\sqrt{(2\,u(f_0)/f_0)^2+(u(C)/C)^2}$ — le facteur 2 vient de $L\propto f_0^{-2}$.

```
    u(f0)/f0 =  0.5 % , u(C)/C =   1.0 %  ->  u(L)/L =   1.4 %
    u(f0)/f0 =  0.5 % , u(C)/C =   5.0 %  ->  u(L)/L =   5.1 %
    u(f0)/f0 =  0.5 % , u(C)/C =  20.0 %  ->  u(L)/L =  20.0 %
```

**L'incertitude est entièrement portée par $C$** — c'est la raison pour laquelle cette méthode est reléguée au rang de contre-vérification. Si on l'emploie : mesurer d'abord $C$ au capacimètre du multimètre (typiquement ±1–2 % [[à vérifier sur la notice du multimètre du lycée]]), *puis* en déduire $L$, et recouper avec deux valeurs de $C$ différentes.

**Et voici pourquoi tout cela compte — la propagation vers $f_0$.** Le sens inverse du calcul précédent (§ 4.9) :

$$\frac{u(f_0)}{f_0}=\frac12\sqrt{\left(\frac{u_L}{L}\right)^2+\left(\frac{u_C}{C}\right)^2}$$

```
  u(L)/L= 2.4 % , u(C)/C= 20.0 % -> u(f0)/f0 = 10.07 %  (part de L : 1.20 %, part de C : 10.00 %)
  u(L)/L= 2.4 % , u(C)/C= 10.0 % -> u(f0)/f0 =  5.14 %  (part de L : 1.20 %, part de C :  5.00 %)
  u(L)/L=10.0 % , u(C)/C= 10.0 % -> u(f0)/f0 =  7.07 %  (part de L : 5.00 %, part de C :  5.00 %)
```

Deux lectures. (i) Le fait établi du projet — **$L$ et $C$ à ±10 % donnent $u(f_0)/f_0\approx7$ %** — est retrouvé. (ii) Surtout : une erreur de **±5 spires** (2,4 % sur $L$) ne pèse que **1,2 %** sur $f_0$, contre **10 %** pour un condensateur à ±20 %. **C'est l'argument qui justifie de bobiner soi-même** : on maîtrise l'élément dont on maîtrise la fabrication, et le maillon faible reste le condensateur, qu'il faut donc mesurer et trier (§ 4.5).

### <a id="s05-14"></a>05.14 Mesure de $r$ : quatre fils, cordons, cosses, et budget d'incertitude

$r\approx1{,}6\ \Omega$ est du même ordre que les cordons d'un multimètre (~0,2 Ω, § 02.8) : une mesure deux fils naïve donnerait **+12 %**. Trois remèdes, par ordre de préférence :

1. **Quatre fils (Kelvin)** : injecter un courant continu connu $I$ avec une **alimentation de laboratoire limitée en courant + résistance de ballast** par deux fils, et mesurer la tension aux bornes de la self par **deux autres fils** au voltmètre. $r=U/I$. La chute dans les fils d'injection n'est pas vue par le voltmètre, et le courant dans les fils de mesure est nul (impédance d'entrée ≈ 10 MΩ). À $I=1$ A, $U\approx1{,}6$ V : facile et précis.
   > **Pas de GBF en continu** : avec 50 Ω d'impédance de sortie et ~10 V max, un GBF ne débite que $10/(50+1{,}64)\approx0{,}19$ A dans la self, soit 0,32 V à mesurer — dix fois moins confortable.
   >
   > ⚠ **Surtension inductive.** Couper 1 A dans 18 mH en quelques microsecondes produit une pointe de **plusieurs centaines de volts** aux bornes de la self : sur le voltmètre, sur l'alimentation, et en arc aux pinces. **Établir et couper le courant en faisant varier progressivement la consigne de l'alimentation**, ou laisser une diode de roue libre (1N4007) en antiparallèle sur la self pendant la mesure, et débrancher le voltmètre **en dernier**. C'est le genre de détail qui coûte un multimètre au lycée.
2. **Fonction REL / relative du multimètre** : court-circuiter les pointes, mémoriser, puis mesurer. Retire les cordons mais pas les résistances de contact.
3. **Substitution** : comparer à une résistance étalon 1 Ω 1 % dans le même montage.

**Budget d'incertitude, et quelle précision est nécessaire.** En quatre fils, $u(r)/r=\sqrt{(u_I/I)^2+(u_U/U)^2}$ ; avec un multimètre de lycée à ±(0,5 % + quelques digits) sur les deux, on obtient **$u(r)/r\approx1$ %**, à condition de mesurer **à froid** et à température notée. Est-ce nécessaire ? La fonction de coût de la § 4.5 arbitre sur $r$ avec une pente de l'ordre de 1 dB/Ω, et la § 05.8 montre que la décision se joue entre 1,5 et 2 Ω : **une précision de 2 à 3 % suffit largement** pour l'optimisation. Le 1 % devient utile pour l'autre usage de $r$ — mesurer la **dérive thermique** entre les deux niveaux d'écoute, qui vaut quelques pour-cent (§ 05.8).

**Deux contrôles indépendants a posteriori** de la longueur de fil : la **pesée** ($\ell=m/(\rho_mA)$, ±5 g ⇒ ±0,25 %) **et** la **DCR** ($\ell=rA/\rho_{Cu}$, ±1 % ⇒ ±1 %). Si les deux ne concordent pas, **c'est une erreur sur le diamètre du fil, et elle seule** : si la section supposée $A_s$ diffère de la vraie $A_v$, les deux estimateurs divergent en sens opposés d'un facteur $(A_v/A_s)^2$, tandis qu'une **erreur de comptage laisse les deux d'accord** (et justes), puisque $N$ n'intervient dans ni l'une ni l'autre. Pour détecter une erreur de comptage il faut comparer $\ell$ à $2\pi aN$ avec $a$ mesuré au pied à coulisse.

> **Bonus : l'estimateur sans diamètre.** La moyenne géométrique des deux élimine $A$ :
> $$\boxed{\,\ell=\sqrt{\frac{m\,r}{\rho_{Cu}\,\rho_m}}\,}$$
> Vérifié sur le cas Mundorf BL140 : 39,20 m, identique au modèle, **sans jamais utiliser le diamètre du fil**. C'est directement la loi $r\times m=\rho_{Cu}\rho_m\ell^2$ de la § 05.6, relue comme un instrument de mesure.

**Résistances de contact et longueurs parasites.** $\ell$ ne compte que la spire moyenne ; les **amenées** (quelques dizaines de centimètres de fil), les **cosses** et les **soudures du filtre** ajoutent typiquement **0,05 à 0,2 Ω**, soit 3 à 12 % de $r$ — et contrairement aux cordons du multimètre, **elles restent dans le circuit en permanence** : elles s'ajoutent à la DCR vue par le haut-parleur (0,1 Ω de plus sur 1,64 Ω ⇒ $-0{,}09$ dB supplémentaires sur 8 Ω, $-0{,}06$ dB sur 14 Ω, et surtout $Q'_{es}$ qui monte encore). Souder, pas visser ; mesurer $r$ **cosses comprises**. [[à chiffrer sur le filtre réel]]

**Précautions** : mesurer à froid, noter la température ($+0{,}39$ %/K, § 02.5, donc $+4$ % pour 10 K) ; refaire la mesure **après** les essais en puissance. L'écart donne l'échauffement du bobinage — et la § 05.8 dit combien de watts y passent : **65 à 130 W à 350 W de programme**, soit une dérive prédite de +1,7 à +9,6 % selon le fil. C'est directement le critère « robustesse ».

### <a id="s05-15"></a>05.15 Effet de peau et effet de proximité à 100 Hz

$$\delta=\sqrt{\frac{2\rho_{Cu}}{\omega\mu_0}}=\sqrt{\frac{\rho_{Cu}}{\pi f\mu_0}}$$

**(a) Effet de peau, fil isolé : totalement négligeable.** Le développement basse fréquence pour un fil rond s'écrit avec le **rayon** $a=d/2$, pas avec le diamètre :

$$\boxed{\,\frac{R_{ac}}{R_{dc}}\simeq1+\frac{1}{48}\left(\frac{a}{\delta}\right)^4=1+\frac{1}{768}\left(\frac{d}{\delta}\right)^4\,}$$

L'écrire avec $d$ surestime l'effet d'un facteur $2^4=16$. Valeur **exacte** calculée par la solution de Bessel $R_{ac}/R_{dc}=\Re\!\left[\frac{ka}{2}\,J_0(ka)/J_1(ka)\right]$ avec $k=(1-j)/\delta$ (série entière, numpy seul), pour le plus gros fil envisagé ($d=2{,}0$ mm) :

```
  f(Hz) | delta(mm) | a/delta | EXACT Bessel | 1+(a/delta)^4/48 | (FAUX) 1+(d/delta)^4/48
     100 |    6.601  |  0.152  |     1.000011 |     1.000011     |      1.00018
     250 |    4.175  |  0.240  |     1.000069 |     1.000069     |      1.00110
    1000 |    2.087  |  0.479  |     1.001097 |     1.001098     |      1.01756
   10000 |    0.660  |  1.515  |     1.100969 |     1.109754     |      2.75607
  controle de l'asymptote HF  a/delta = 10 : exact = 5.2593 , q/(2 sqrt2)+1/4 = 5.2500
```

Le développement en $a$ colle à l'exact **au 6ᵉ chiffre** jusqu'à 1 kHz, et à 0,8 % encore à 10 kHz. À **100 Hz, $\delta=6{,}60$ mm**, soit 6,6 fois le rayon du plus gros fil : $R_{ac}/R_{dc}=\mathbf{1{,}00001}$. **L'effet de peau est totalement négligeable dans la bande du raccord**, et l'argument commercial du « fil de Litz » ou du méplat pour les selfs de grave **ne se justifie pas** par l'effet de peau à 100 Hz. C'est une bonne réponse à une question de jury : le calcul, pas l'argument d'autorité.

**(b) Effet de proximité : lui n'est PAS négligeable, et il faut le dire.** Le champ des spires voisines dans une bobine **multicouche** crée des courants induits qui croissent non pas seulement en $(d/\delta)^4$, mais en $m^2$ où $m$ est le **nombre de couches**. Or nos selfs en ont 22 à 25. Développement basse fréquence de Dowell (1966), $\xi=\frac{d}{\delta}\frac{\sqrt\pi}{2}\sqrt\eta$ avec $\eta=d/d_{isolé}$ :

$$\frac{R_{ac}}{R_{dc}}\simeq1+\frac{5m^2-1}{45}\,\xi^4$$

```
  a 100 Hz, selfs de 18 mH de la section :
   d=1.0 mm : couches m = 24.6 , xi = 0.129 -> R_ac/R_dc = 1.019   (une seule couche : 1.00002)
   d=1.4 mm : couches m = 23.1 , xi = 0.183 -> R_ac/R_dc = 1.066   (une seule couche : 1.00010)
   d=2.0 mm : couches m = 21.6 , xi = 0.263 -> R_ac/R_dc = 1.249   (une seule couche : 1.00043)
```

**Soit +2 % à +25 %, pas « le pour-mille ».** Et l'effet est le plus fort pour le gros fil — celui que la § 05.8 recommande pour les faibles $r_{max}$ : une partie du gain de DCR obtenu en grossissant le fil est reprise par la proximité.

**Deux réserves, puis la bonne conduite à tenir.** Dowell est un modèle **1-D de fenêtre de transformateur**, où un noyau canalise le flux et impose un champ parallèle aux couches ; pour une bobine **à air**, le champ s'échappe par les bords et l'effet réel est plus faible : ces chiffres sont un **majorant**. Mais un majorant de +25 % ne se balaie pas d'une phrase.

> **Donc : en faire une mesure, pas une affirmation.** Le banc de la § 02 mesure $\Re\mathrm{e}(Z)$ à 100 Hz. **Comparer $\Re\mathrm{e}(Z(100\ \text{Hz}))$ à la DCR mesurée en continu (§ 05.14) sur la self bobinée est une manip de 20 minutes, gratuite, qui tranche.** Si l'écart est de quelques %, on peut identifier $r_{ac}\simeq r_{dc}$ et tout l'usage de $r$ fait en section 04 est légitime. **Si l'écart dépasse quelques %, la section 04 doit utiliser $r_{ac}(100\ \text{Hz})$ et non $r_{dc}$** — et c'est alors un excellent résultat expérimental, et une excellente réponse de jury. [[à mesurer en phase 4 — c'est un point dur du modèle, pas un détail]]

**Perspective** (une ligne, si le jury pose la question) : la capacité parasite inter-spires d'un bobinage de 454 spires multicouche place l'**auto-résonance** vers quelques centaines de kHz [[ordre de grandeur, à mesurer si besoin]] — sans objet à 100 Hz, mais c'est la limite haute du modèle « self pure + $r$ ».

### Ce qu'il faut retenir pour l'oral

- La bobine de Brooks maximise $L$ à longueur de fil donnée ; on **retrouve ses proportions** en minimisant $6a+9b+10c$ à $abc$ constant (Lagrange sur la formule de Wheeler) : $b/a=2/3$ exactement, $c/a=0{,}600$ contre 0,667 pour le résultat exact. Et l'optimum est **plat** : à 10 % près sur la forme, on perd 0,1 % d'inductance.
- $L$, $r$ et $m$ ne sont pas indépendants : **$m=K_{Cu}(L/r)^{3/2}$ avec $K_{Cu}\approx1760$ kg·s$^{-3/2}$ (±10 %), indépendamment du diamètre de fil**. Diviser la DCR par 2 multiplie le cuivre par $2^{3/2}=2{,}83$. « $r\times m$ = cte » n'est qu'une approximation (facteur 1,7 entre 1,0 et 2,0 mm) ; l'invariant est $m\,r^{3/2}$, exact dans le modèle, à ±4 % en pratique.
- Chiffres calculés pour 18 mH (pertes sur 8 Ω, borne supérieure) : 0,91 kg et 2,83 Ω ($-2{,}6$ dB) en 1,0 mm ; 2,02 kg et 1,64 Ω ($-1{,}6$ dB) en 1,4 mm ; 4,73 kg et 0,92 Ω ($-0{,}9$ dB) en 2,0 mm. Le modèle prédit la DCR de **trois** références de catalogue à **±4 %**, dont une **à la valeur cible**, sans paramètre ajusté.
- **La fenêtre praticable est étroite et les deux contraintes de terrain la ferment des deux côtés** : **en deçà** de $r_{max}\approx1{,}5\ \Omega$ le fil dépasse 1,5 mm (introuvable au détail, non bobinable à la main) ; **au-delà** de 2 Ω on passe 3 A/mm², la self encaisse plus de 90 W et dérive de plusieurs % de DCR au niveau fort — **le critère « robustesse » est décidé ici, avant toute mesure**.
- Cette section **remplace deux placeholders de la section 04 — et montre qu'ils se contredisaient d'un facteur 4,2** : `dcr(L)` supposait 4,25 kg de cuivre par self (106 €), `prix_L(L)` en facturait 1,02 kg (25,6 €). L'optimiseur croyait acheter un filtre passif à la fois bon marché et peu résistif. Le bon modèle : $r$ est une **variable de conception**, payée $\text{prix}_{kg}K_{Cu}(L/r)^{3/2}$. Les pondérations choisissent la self : avec celles de la § 4.5, l'optimiseur accepterait 2,1 dB.
- À 100 Hz, $\delta_{Cu}=6{,}6$ mm : **effet de peau négligeable ($R_{ac}/R_{dc}=1{,}00001$)** — mais l'**effet de proximité** en bobinage à 23 couches peut atteindre **+7 % (majorant Dowell)**, et il faut donc **mesurer** $\Re\mathrm{e}(Z)$ à 100 Hz avant d'identifier $r_{ac}$ à $r_{dc}$.
- L'air ne sature **jamais** ($\mu_r=1$, $B(H)$ rigoureusement linéaire ; $B$ moyen énergétique 63 mT, champ au cœur ≈ 0,16 T à 350 W). Un noyau divise la DCR par ~7 et la matière par > 2, mais **impose de vérifier $L(I)$** : il faut au moins ~120 cm³ de poudre de fer pour stocker 0,79 J, et l'enveloppe du produit du commerce n'en fait que 312 cm³ cuivre compris. La marge est faible — l'essai $L(I)$ est le meilleur satellite de la section.
- **Argument de catalogue, vérifiable, qui vaut mieux qu'un calcul** : le marché **ne vend pas** de self à air de 18 mH à faible DCR. L'objet n'existe pas parce qu'il pèserait 5 kg.

### Sources

- Wheeler, H. A., « Simple Inductance Formulas for Radio Coils », *Proceedings of the I.R.E.*, vol. 16, n° 10, oct. 1928, pp. 1398–1400 — formule multicouche $L[\mu\text{H}]=0{,}8a^2N^2/(6a+9b+10c)$, $a$ = rayon moyen, $b$ = longueur, $c$ = différence des rayons externe et interne, dimensions en pouces ; domaine de validité (aucune dimension n'écrasant les autres) ; transposée en SI et testée numériquement en § 05.2.
- Brooks, H. B., « Design of Standards of Inductance, and the Proposed Use of Model Reactors in the Design of Air-Core and Iron-Core Reactors », *Bureau of Standards Journal of Research*, vol. 7, 1931, à partir de la p. 289 — tiré à part NIST `jresv7n2p289` : <https://nvlpubs.nist.gov/nistpubs/jres/7/jresv7n2p289_A2b.pdf> (pagination de début vérifiée ; page de fin [[à vérifier]]).
- Grover, F. W., *Inductance Calculations: Working Formulas and Tables*, Van Nostrand, 1946 (rééd. Dover) — **référence primaire de la constante $1{,}6994\cdot10^{-6}$ H/m (p. 98)**, formule de Maxwell pour la mutuelle de deux spires coaxiales, distance géométrique moyenne, tables de la bobine de Brooks.
- QuickField (Tera Analysis), *Brooks coil* — note d'application donnant $L=1{,}6994\cdot10^{-6}\cdot(3c/2)\cdot N^2$ [H, m] et un calcul par éléments finis (2,033 mH pour $c=20$ mm, $N=200$) : <https://quickfield.com/advanced/brooks_inductor.htm>. Cas test utilisé en § 05.3.
- Dowell, P. L., « Effects of eddy currents in transformer windings », *Proc. IEE*, vol. 113, n° 8, 1966, pp. 1387–1394, DOI 10.1049/piee.1966.0236 — effet de proximité en bobinage multicouche (§ 05.15). Modèle 1-D de fenêtre de transformateur : **majorant** pour une bobine à air.
- Fiche produit Mundorf BL140 2 mH / Ø 1,4 mm (Audiophonics) : DCR 0,43 Ω, 48,90 € TTC : <https://www.audiophonics.fr/en/mundorf-mcoil-bl/mundorf-bl140-air-core-self-14mm-2mh-p-4211.html>. Point de validation du modèle de DCR (§ 05.7). Variante 1,5 mH / 1,4 mm : DCR 0,38 Ω.
- Fiche produit Mundorf MCoil L (L71), **self à air** 18 mH / fil 0,71 mm : DCR **4,77 Ω** — la seule self à air de 18 mH trouvée au catalogue, et elle est inutilisable en grave ($-4{,}1$ dB). Troisième point de validation, **à la valeur cible** (§ 05.7), et argument de marché (§ 05.10). Dimensions annoncées [[à vérifier sur la fiche constructeur]].
- Fiche produit Jantzen Audio 6595, 18 mH / 14 AWG : DCR 0,174 Ω, 700 W RMS, Ø 105 × 36 mm, **1,29 kg**, ≈ 80 £. Parts-Express décrit correctement un **noyau torique de fer** : <https://www.parts-express.com/Jantzen-6595-18mH-14-AWG-C-Coil-Toroidal-Inductor-255-844> ; HiFi Collective l'étiquette « Air Core », ce que le calcul de la § 05.11 réfute : <https://www.hificollective.co.uk/catalog/000-6595-18mh-jantzen-c-coil.html>. Point de comparaison air / noyau (§ 05.10, § 05.11).
- Prix du fil émaillé : distributeurs français de fil de bobinage (E44 <https://www.e44.com/>, ATEC France <https://www.atecfrance.fr/merchant/category/fils-cuivre>). **Aucun ne publie de prix au kg pour ces diamètres** (ATEC : « au cours du cuivre + plus-value de transformation », sur devis) : les **25 €/kg** de cette section sont un ordre de grandeur **non sourcé**, [[à remplacer par un devis]]. Vérifier au passage que **le fil existe au détail dans la masse voulue** (2 kg en 1,4 mm, 4,7 kg en 2,0 mm ne s'achètent pas en bobine de 100 g) et que le conditionnement disponible ne fasse pas exploser le coût réel.
- Petoin, D., « Résistance des selfs pour filtre passif » <https://www.petoindominique.fr/php/self.php> — $Q'_{es}=Q_{es}(R_e+R_F)/R_e$ (§ 05.1) et ordres de grandeur de DCR du commerce.
- IEC 60317-0-1, *Specifications for particular types of winding wires* — dimensions et surépaisseur d'émail grade 1/grade 2 [[à vérifier : valeurs exactes pour 1,0 / 1,4 / 2,0 mm]].
- Dépôt : `FEUILLE-DE-ROUTE.md` (phases 3 et 4, critères « pertes d'insertion », « encombrement/matière », « robustesse » ; **la ligne « selfs bobinées maison ≈ 25 €/pièce » est à corriger**, cf. § 05.10), `CLAUDE.md` (nombres de contrôle : 18 mH, 150 µF, 97 Hz, DCR 1 Ω ⇒ 11 % / −1 dB), section 02 (chaîne de mesure, incertitudes, coefficient de température du cuivre), section 04 (fonction de coût, séries E12, Monte-Carlo, définition gelée de $f_c$).

<!-- NON RETENU — remarque sur `mutuelle(R1, R2, DZ + np.eye(len(r_i)))` dans verif_brooks.py : le code porte deja le commentaire « # diagonale bidon, ecrasee juste apres », suivi de np.fill_diagonal. Rien a ajouter. -->
<!-- NON RETENU (partiellement) — le verificateur 1 proposait de garder R_ref = 100 ohm en mesurant V_LC comme methode PRINCIPALE de mesure de L. Sa correction du Q est reprise integralement, mais la methode principale retenue est le banc d'impedance de la section 02 (L = Im(Z)/omega, propose par le verificateur 2), qui elimine entierement l'incertitude sur C — dominante ici. La resonance serie avec lecture du creux de V_LC est conservee comme contre-verification independante, ce qui satisfait les deux verdicts. -->
<!-- NON RETENU — l'affirmation « E44 ne vend que jusqu'a 1,5 mm » n'a pas pu etre confirmee : les distributeurs consultes ne publient pas leur gamme de diametres. La contrainte d <= d_dispo est donc posee avec un [[a verifier par devis]] plutot qu'avec une borne chiffree presentee comme un fait. -->
<!-- Nombres confirmes par recalcul independant (scratchpad/sec05/, numpy 2.4.6 seul, Python 3.13.2) : effet de peau exact par serie entiere de Bessel (1.000011 / 1.000069 / 1.001097 / 1.100969, asymptote HF verifiee a a/delta=10) ; Dowell (1.019 / 1.066 / 1.249) ; Q du montage de mesure (6.69 / 0.212 / 0.108) et creux de V_LC (0.0161 a 96.859 Hz, 7.79 deg/Hz) ; couplage mutuel coaxial (k = 0.046 a un diametre d'entraxe) ; J, P_Joule et derive thermique de la table 05.8 ; budget 4 selfs ; incoherence des placeholders (4.25 kg vs 1.02 kg) ; lecture litterale bck=NA (487 spires, -7 % sur r) ; sensibilite a k ; 3 validations catalogue ; pont w_W/w_dB. Fiches Jantzen 6595 et Mundorf L71 verifiees en ligne le 2026-09-13. -->

## <a id="s06"></a>06. Pertes, compression thermique et croisement énergétique passif / actif

Cette section chiffre trois lignes du tableau des critères gelés (FEUILLE-DE-ROUTE.md) : **pertes d'insertion**, **consommation au repos** et **robustesse** (dérive entre les deux niveaux d'écoute). Elle fournit aussi le terme « pertes » de la fonction de coût de l'acte 3. Rien n'a encore été mesuré sur l'enceinte de Thomas : toutes les valeurs numériques ci-dessous sont soit calculées à partir d'hypothèses explicites, soit des ordres de grandeur étiquetés, soit des placeholders `[[à mesurer]]`. Les scripts cités ont été exécutés avec **numpy seul** — non par contrainte (l'environnement du poste, vérifié le 2026-09-13, comporte Python 3.13.2, numpy 2.4.6, **scipy 1.18.1** et matplotlib 3.11.0, tous fonctionnels) mais par **choix de méthode** : les calculs de cette section sont des balayages et des moindres carrés linéaires que numpy fait aussi bien, et qui restent exécutables tels quels sur une machine du lycée. Python 3.13 ; ils sont dans le scratchpad `sec06/` : `pertes_dcr.py`, `thermique_croisement.py`, `mesure_Re_coupure.py` et `corrections_verif.py` (ce dernier porte les calculs ajoutés après vérification : rétroaction thermique, référence analytique du point −3 dB, L-pad sur charge complexe, DCR de $L_2$, Monte-Carlo de la méthode A).

**Cadrage préalable : l'ordre de grandeur qui domine tout le bilan.** Un haut-parleur de grave à rayonnement direct convertit en son quelques pour cent de la puissance électrique qu'il reçoit ; tout le reste chauffe la bobine. Le rendement de référence se calcule gratuitement à partir des paramètres identifiés en phase 2 :

$$\eta_0=\frac{4\pi^2}{c^3}\,\frac{f_s^{\,3}\,V_{as}}{Q_{es}}
\;\simeq\;9{,}61\times10^{-10}\;\frac{f_s^{\,3}\,V_{as}[\text{L}]}{Q_{es}}\qquad(c=345\ \text{m/s}).$$

Pour des paramètres plausibles d'un 18″ de sonorisation (`[[à identifier en phase 2]]` — ici $f_s=40$ Hz, $V_{as}=200$ L, $Q_{es}=0{,}5$), $\eta_0\approx2{,}5\ \%$ ; la fourchette sur des jeux voisins reste 2 à 3 %. Autrement dit **plus de 97 % de la puissance envoyée à la voie grave finit en chaleur dans $R_e$, quelle que soit l'architecture de filtrage**. Ce que compare cette section — 11 % dans une self, quelques watts au repos — est du second ordre. Mais c'est le seul ordre sur lequel le concepteur du filtre a prise, et c'est aussi ce qui rend l'échauffement de 06.5 inévitable. Le dire d'entrée est plus honnête que de le laisser découvrir au jury.

### <a id="s06-1"></a>06.1 Pertes Joule dans la self série du passe-bas

La self $L_1$ du passe-bas est en série avec le haut-parleur ; sa résistance de bobinage $r$ (DCR) est traversée par tout le courant de la voie grave. Sur une charge résistive $R$, le même courant $I$ traverse $r$ et $R$ :

$$\frac{P_r}{P_{\text{totale}}}=\frac{r\,I^2}{(R+r)\,I^2}=\frac{r}{R+r},\qquad
\text{atténuation en tension : } 20\log_{10}\frac{R}{R+r}.$$

| $r$ (Ω) | fraction dissipée dans $r$ | atténuation |
|---|---|---|
| 0,25 | 3,0 % | −0,27 dB |
| 0,5 | 5,9 % | −0,53 dB |
| **1** | **11,1 %** | **−1,02 dB** |
| 2 | 20,0 % | −1,94 dB |

Le nombre de contrôle du projet (1 Ω face à 8 Ω → 11 % en chaleur, ≈ −1 dB) est retrouvé. **Attention : cette fraction est une borne inférieure**, valable en bande passante sur charge résistive ; la suite montre qu'elle triple près du raccord.

**Dépendance à la charge réelle.** Avec une charge complexe $\underline Z(f)$, la puissance active reçue par le HP est $\operatorname{Re}\{\underline Z\}\,|I|^2$, donc

$$\frac{P_r}{P_r+P_{HP}}=\frac{r}{r+\operatorname{Re}\{\underline Z(f)\}}.$$

Au pic de résonance, $\operatorname{Re}\{\underline Z\}$ est grand (le HP « refuse » le courant) et la self dissipe peu ; en haut de bande $\operatorname{Re}\{\underline Z\}\to R_e$ et la fraction est maximale. Illustration sur le modèle Z(f) **illustratif v1** (paramètres arbitraires de `_gen.py` : $R_e=6{,}5$ Ω, $L_e=1{,}2$ mH, $R_{es}=44$ Ω, $f_s=40$ Hz, $L_{es}=0{,}1$ H — **ce n'est pas le sub de Thomas**), HP seul en série avec $r=1$ Ω :

| $f$ (Hz) | $\lvert\underline Z\rvert$ (Ω) | $\operatorname{Re}\{\underline Z\}$ (Ω) | fraction dans $r$ |
|---|---|---|---|
| 20 | 19,1 | 12,1 | 7,6 % |
| 40 ($f_s$) | 50,5 | 50,5 | 1,9 % |
| 100 | 14,1 | 9,5 | 9,5 % |
| 400 | 6,7 | 6,6 | 13,1 % |

**Dans le filtre complet, le courant de la self n'est pas celui du HP** : $C_1$ en parallèle absorbe un courant réactif qui traverse aussi $L_1$ et $r$. Bilan de puissance exact (source idéale 1 V → $r + j\omega L_1$ → $C_1 \,\|\, \underline Z$), code exécuté (convention : amplitudes complexes, $V=1$ V réel, donc $P=\operatorname{Re}\{V\,I^*\}$ — pas de facteur 1/2, ce qui est sans effet sur les rapports publiés) :

```python
L1, C1 = 18e-3, 150e-6
def bilan(f, r, charge):
    w = 2*np.pi*f
    Zl = charge(f)
    Zpar = 1/(1j*w*C1 + 1/Zl)          # C1 // charge
    Ztot = r + 1j*w*L1 + Zpar
    I_L = 1/Ztot                        # V = 1 V
    V_hp = I_L*Zpar
    I_hp = V_hp/Zl
    P_in = (I_L.conjugate()*1).real     # V=1 reel : P = Re(V I*)
    P_r = r*abs(I_L)**2
    P_hp = Zl.real*abs(I_hp)**2
    return P_in, P_r, P_hp, abs(V_hp)
```

Sortie (extrait) :

```
  charge      f (Hz) | P_r/P_in | P_hp/P_in | |V_hp| (V)
  8 ohm pur     20   |   11.3 % |   88.7 %  | 0.890
  8 ohm pur     70   |   13.8 % |   86.2 %  | 0.823
  8 ohm pur    100   |   16.4 % |   83.6 %  | 0.663
  8 ohm pur    200   |   29.0 % |   71.0 %  | 0.230
  modele Z(f)   40   |    8.4 % |   91.6 %  | 1.164
  modele Z(f)   70   |   26.6 % |   73.4 %  | 2.420
  modele Z(f)  100   |   33.1 % |   66.9 %  | 1.088
```

Lecture : en bande passante (20 Hz) on retrouve $r/(R+r)$ ; près de $f_c$ la fraction dissipée monte (16 % à 100 Hz sur 8 Ω) parce que le courant réactif de $C_1$ passe dans la self ; sur le modèle Z(f) le filtre catalogue **résonne** et un tiers de la puissance part dans $r$ à 100 Hz. Précision sur cette résonance : le pic vaut **+10,8 dB à 74,9 Hz sans DCR, ramené à +8,0 dB à 74,0 Hz par $r=1$ Ω** (à 70 Hz : $|V_{hp}|=3{,}15$ V soit +10,0 dB sans DCR, 2,42 V soit +7,7 dB avec). Autrement dit **la DCR amortit la résonance parasite du filtre catalogue sur la charge réelle** : c'est le seul effet bénéfique de $r$ de toute la section, et l'optimiseur de l'acte 3 ne doit donc pas traiter $r$ comme un pur handicap.

**Conséquence pour la fonction de coût.** Le terme « pertes » doit être évalué sur le spectre du programme, pas sur le seul $r/(R+r)$. Avec $S_{I_L}(f)$ la densité spectrale de puissance du courant de self (en A²/Hz), obtenue en filtrant le spectre du programme par $|\underline Y(f)|^2$ :

$$P_r=r\int_0^{\infty} S_{I_L}(f)\,\mathrm{d}f\;=\;r\,I_{L,\text{RMS}}^2 .$$

<!-- L'écriture "P_r = r ∫ |I_L(f)|² df" du brouillon était dimensionnellement fausse (W·Hz) : corrigée en DSP, avec la forme RMS équivalente pour l'oral et la mesure. -->

La seconde forme est celle qu'on mesure : $I_{L,\text{RMS}}$ à la pince ou aux bornes d'un shunt, aux deux niveaux gelés, avec un bruit rose 40–250 Hz. **Bande à retenir** : selon la fréquence et la charge, la fraction perdue va de 2 % (au pic de résonance) à 33 % (au raccord sur le modèle Z(f)), en passant par 11 % en bande passante sur 8 Ω. Toute conclusion énergétique doit être donnée comme une bande, pas comme une ligne.

### <a id="s06-2"></a>06.2 Les autres résistances du filtre

La self $L_1$ n'est pas la seule branche dissipative, et le budget de pertes de l'acte 3 doit porter sur **toutes** les branches résistives :

$$P_{\text{pertes}}=\sum_k R_k\int_0^{\infty} S_{I_k}(f)\,\mathrm{d}f
\qquad\text{avec } R_k\in\{r_{L_1},\;r_{L_2},\;\mathrm{ESR}(C_1),\;\mathrm{ESR}(C_2),\;R_{\text{L-pad}},\;R_{\text{câble}}\}.$$

**DCR de $L_2$, la self en parallèle du passe-haut.** Elle shunte en permanence l'entrée de la voie médium : elle dissipe *et* plafonne la réjection en bas de bande. Calcul sur le passe-haut catalogue ($L_2=18$ mH, $C_2=150$ µF, $r_{L_2}=1$ Ω, médiums 8 Ω), fraction de la puissance entrant dans la voie médium qui est dissipée dans $r_{L_2}$ :

| $f$ (Hz) | 40 | 70 | 100 | 200 |
|---|---|---|---|---|
| $P_{r_{L_2}}/P_{\text{entrée méd.}}$ | 27,2 % | 11,2 % | 5,8 % | 1,5 % |

En bas de bande c'est **plus** que le poste $L_1$ mis en avant en 06.1 : la self parallèle est la branche la plus dissipative du filtre là où le passe-haut est censé ne rien laisser passer.

**ESR des condensateurs.** Le budget prévoit des électrolytiques bipolaires de 150 µF, dont l'ESR est de l'ordre de 0,1 à 0,5 Ω à 100 Hz `[[à mesurer]]` — non négligeable devant $r$, croissante à basse fréquence, dépendante de la température et dégradée par le vieillissement. Or 06.1 montre que $C_1$ véhicule un courant réactif important près de $f_c$ : ce courant traverse aussi son ESR. **La mesure est gratuite** : c'est $\operatorname{Re}\{\underline Z\}$ du condensateur seul, avec le jig d'impédance de la phase 1, déjà prévu pour l'étalonnage sur composants connus.

**Résistance série alternative de la self.** Seule la résistance continue (DCR) est comptée ci-dessus. À 100 Hz sur du fil de 1 à 2 mm, effet de peau et effet de proximité restent faibles, mais si la self est **à noyau**, les pertes fer et la saturation ajoutent une résistance série qui croît avec la fréquence *et avec le niveau*. C'est une réserve importante pour le satellite « self optimale », dont la loi $r\times m\approx$ cte à $L$ fixée n'est établie que pour la DCR : elle ne vaut telle quelle que pour une self **à air** `[[à trancher en phase 3]]`.

**Câble et impédance de sortie de l'ampli.** Ils s'ajoutent au même endroit du circuit :
$R_{\text{série,tot}}=r_{L_1}+R_g+R_{\text{câble}}$, avec $R_{\text{câble}}=2\ell\rho/S\approx0{,}05$ à $0{,}15$ Ω pour quelques mètres de 1,5 mm² `[[à calculer sur le câblage réel]]` et $R_g$ l'impédance de sortie du E-800 (facteur d'amortissement **non publié dans le manuel**, vérifié ; ordre de grandeur $R_g<0{,}1$ Ω pour un ampli de scène). $R_g$ se mesure en phase 1 avec le même jig, par la méthode des deux charges. Conséquence pratique : **le $r$ injecté dans la fonction de coût doit être mesuré aux bornes où le filtre sera réellement inséré, câblage compris**, sinon le budget de pertes est sous-estimé dès le départ.

### <a id="s06-3"></a>06.3 L-pad d'égalisation : une perte qui achète de l'immunité à $\underline Z(f)$

Les deux voies n'ont pas la même sensibilité (dB/W/m `[[à documenter]]`). En passif, la voie la plus sensible (a priori les médiums) est atténuée par un L-pad : $R_1$ en série, $R_2$ en parallèle sur la charge $R_L$. Pour un rapport de tension $a=10^{-A_{\text{dB}}/20}$ :

$$R_1=R_L\,(1-a),\qquad R_2=R_L\,\frac{a}{1-a},\qquad
\frac{P_{\text{perdue}}}{P_{\text{entrée}}}=1-a^2 .$$

```python
RL = 8.0
for att in (1, 2, 3, 6, 10):
    a = 10**(-att/20)
    R1 = RL*(1-a)
    R2 = RL*a/(1-a)
    Zin = R1 + 1/(1/R2 + 1/RL)   # verification sur charge NOMINALE
    assert abs(Zin-RL) < 1e-9
```

**L-pad sur charge nominale $R_L=8\ \Omega$** (mêmes valeurs pour la voie médiums, 2 × 4 Ω en série) :

| atténuation | $a$ | $R_1$ (Ω) | $R_2$ (Ω) | puissance perdue | dont $R_1$ / $R_2$ |
|---|---|---|---|---|---|
| 1 dB | 0,891 | 0,87 | 65,6 | 20,6 % | — |
| 2 dB | 0,794 | 1,65 | 30,9 | 36,9 % | — |
| 3 dB | 0,708 | 2,34 | 19,4 | 49,9 % | 29,2 % / 20,7 % |
| 6 dB | 0,501 | 3,99 | 8,04 | 74,9 % | 49,9 % / 25,0 % |
| 10 dB | 0,316 | 5,47 | 3,70 | 90,0 % | — |

<!-- Ligne 2 dB rétablie pour que le tableau corresponde exactement à la boucle du code, et R_L = 8 Ω explicité dans le titre. -->

**Dimensionnement en puissance** (le brouillon disait « plusieurs W » sans formule) : la puissance perdue vaut $(1-a^2)\,P_{\text{méd}}$, répartie en $P(R_1)=(1-a)^2\,P_{\text{méd}}\cdot$… — plus simplement, avec $V_{in}$ imposé sur $Z_{in}=R_L$ : $P(R_1)=R_1/R_L$ et $P(R_2)=a^2 R_L/R_2$ en fraction de $P_{\text{entrée}}$, soit pour un pad de 3 dB **29 % dans $R_1$ et 21 % dans $R_2$** de la puissance de la voie. À dimensionner sur le niveau fort gelé, avec la marge d'usage : des résistances bobinées de 10 à 20 W.

**Correction importante — $Z_{in}=R_L$ n'est vrai que sur la charge nominale.** Sur la charge réelle, $Z_{in}(f)=R_1+\bigl(R_2\parallel\underline Z(f)\bigr)$ varie encore avec $f$. Mais le fait sous-jacent est plus intéressant que l'erreur : **le L-pad aplatit fortement l'impédance vue par le passe-haut**. Sur le modèle Z(f) illustratif, bande 20–300 Hz :

| | excursion de $\lvert Z\rvert$ | à 50 Hz | à 100 Hz | à 200 Hz |
|---|---|---|---|---|
| sans pad | ×7,4 (6,9 → 50,5 Ω) | 39,7 Ω | 14,1 Ω | 8,0 Ω |
| pad 3 dB | ×2,2 (7,4 → 16,4 Ω) | 15,8 Ω | 11,0 Ω | 8,0 Ω |
| pad 6 dB | ×1,4 (7,7 → 10,9 Ω) | 10,8 Ω | 9,4 Ω | 8,1 Ω |

Le L-pad est donc **le seul composant du filtre qui échange des pertes contre une réduction de la sensibilité du filtre à $\underline Z(f)$** — c'est-à-dire contre une immunité partielle au problème central du TIPE. Ce n'est pas un simple poste de perte, c'est un **degré de liberté de l'optimisation de l'acte 3**, avec sa propre courbe d'arbitrage : 6 dB d'atténuation achètent un facteur 5 sur l'excursion d'impédance au prix de 75 % de la puissance de la voie. En actif, l'égalisation est un réglage de gain avant l'ampli : perte nulle, et immunité totale par construction.

### <a id="s06-4"></a>06.4 Résistance série totale et amortissement : DCR et échauffement sont le même levier

Le facteur de qualité électrique de Thiele-Small est proportionnel à la résistance **série totale** du circuit électrique vu par la force contre-électromotrice (Small, 1972, avec résistance de générateur $R_g$) :

$$Q_{es}'=Q_{es}\,\frac{R_e+r}{R_e},\qquad
Q_{ts}'=\frac{Q_{ms}\,Q_{es}'}{Q_{ms}+Q_{es}'},\qquad
Q_{tc}'=Q_{ts}'\sqrt{1+V_{as}/V_b}\ \text{(caisse close)} .$$

**Peu importe d'où vient cette résistance** : DCR de la self, câble, impédance de sortie de l'ampli — ou échauffement de la bobine. Chauffer la bobine de $\Delta T$ équivaut exactement à insérer $R_{e0}\,\alpha\,\Delta T$ en série. C'est la phrase-clé qui relie cette sous-section à la suivante. Sur le modèle illustratif ($Q_{ms}=1{,}75$, $Q_{es}=0{,}259$, $Q_{ts}=0{,}225$) :

| origine de la résistance série | valeur (Ω) | $Q_{es}'$ | $Q_{ts}'$ | variation de $Q_{ts}$ |
|---|---|---|---|---|
| — | 0 | 0,259 | 0,225 | — |
| DCR self | 0,5 | 0,279 | 0,240 | +6,6 % |
| DCR self | 1 | 0,298 | 0,255 | +13,1 % |
| DCR self | 2 | 0,338 | 0,283 | +25,8 % |
| **échauffement +20 K** | **+0,51** | 0,279 | 0,241 | +6,8 % |
| **échauffement +50 K** | **+1,28** | 0,309 | 0,263 | +16,7 % |
| **échauffement +100 K** | **+2,55** | 0,360 | 0,299 | +32,6 % |
| **échauffement +150 K** | **+3,83** | 0,411 | 0,333 | +47,7 % |

Un ohm de DCR relève le $Q$ total de ~13 % : le grave est un peu moins amorti (bosse et traînage à la résonance en caisse). Mais **+100 K sur la bobine équivaut à +2,55 Ω, davantage que la pire self envisagée** — et cette résistance-là, contrairement à la DCR, n'est pas choisie : elle apparaît en cours d'écoute. Conséquence directe sur le critère « robustesse » : l'échauffement ne décale pas seulement $f_c$ du filtre (06.5), il **désaligne la caisse** en faisant monter $Q_{tc}$ dans les mêmes proportions. Le critère doit donc surveiller **la forme du bas du spectre**, pas seulement $f_c$.

Nuance : autour de $f_s$ la self présente aussi une réactance ($2\pi\cdot40\ \text{Hz}\cdot18\ \text{mH}\approx4{,}5$ Ω) et $C_1$ est en parallèle ; l'amortissement réel dépend du filtre entier, ce que la simulation complète de l'acte 3 capture. Les formules ci-dessus servent à l'oral et à l'intuition ; le code fait le calcul exact.

### <a id="s06-5"></a>06.5 Compression thermique et dérive du raccord

**Loi de résistance du cuivre.** $R_e(T)=R_{e0}\,[1+\alpha\,(T-T_0)]$ avec $\alpha=3{,}93\times10^{-3}\ \text{K}^{-1}$ pour le cuivre recuit (IEC 60028, référence 20 °C ; Klippel utilise la même valeur $\delta=0{,}00393\ \text{K}^{-1}$).

**Notations.** Deux puissances différentes interviennent et le brouillon les confondait sous la lettre $P$ ; on distingue désormais :

- $P_{R_e}$ : puissance **dissipée dans la bobine**, celle qui pilote le modèle thermique ;
- $P_{\text{voie}}$ : puissance **envoyée à la voie grave** à l'entrée du filtre, celle du bilan énergétique de 06.8 ;
- $P_{\text{secteur}}$ : puissance **absorbée au compteur**, celle que lit le wattmètre de prise.

Elles sont reliées par $P_{R_e}\approx P_{\text{voie}}\cdot\dfrac{R_e}{R_e+r}\,(1-\eta_0)$ avec $\eta_0\approx2{,}5\ \%$ (cadrage), et $P_{\text{voie}}=\eta\,P_{\text{secteur}}$ avec $\eta$ le rendement de l'ampli (06.7).

**Conséquence sur la sensibilité.** Hors résonance, le courant est fixé par $R_e$ (source de tension) : la force $Bl\,I$ et donc la pression chutent comme $1/R_e(T)$. Avec une résistance série $r$, le dénominateur est $R_e(T)+r$ : la compression est légèrement moindre.

| $\Delta T$ (K) | $R_e/R_{e0}$ | compression HP seul | avec $r=1$ Ω ($R_{e0}=6{,}5$ Ω) |
|---|---|---|---|
| 20 | 1,079 | −0,66 dB | −0,57 dB |
| 50 | 1,196 | −1,56 dB | −1,37 dB |
| 100 | 1,393 | −2,88 dB | −2,55 dB |
| 150 | 1,590 | −4,03 dB | −3,58 dB |

−1 dB est atteint dès $\Delta T\approx31$ K, −3 dB vers $\Delta T\approx105$ K — ce qui correspond au « −3 dB à puissance nominale » de la littérature pro (Button, 1992). **Ce que la colonne « avec $r$ » ne dit pas** : le passif comprime bien 0,3 dB de moins, mais depuis un niveau déjà inférieur de 1,2 dB (perte d'insertion sur $R_{e0}=6{,}5$ Ω). Relativement à l'attaque directe à froid, le passif est à −1,24 dB quand il est froid et à −3,79 dB à +100 K, contre −2,88 dB pour l'attaque directe : **il reste toujours en dessous, à toute température**. La « moindre compression » n'est pas un avantage, seulement un écart qui se resserre — et il faut le présenter ainsi.

**Modèle thermique.** À une constante de temps : la bobine (capacité thermique $C_{tv}$) évacue vers l'aimant à travers $R_{tv}$, aimant supposé à l'ambiante :

$$\Delta T_v(t)=P_{R_e}\,R_{tv}\left(1-e^{-t/\tau_v}\right),\qquad \tau_v=R_{tv}C_{tv}.$$

À deux constantes de temps (modèle linéaire classique, Klippel 2004, fig. 2) : l'aimant/châssis ($C_{tm}$, $R_{tm}$ vers l'ambiante) s'échauffe à son tour, beaucoup plus lentement :

$$C_{tv}\frac{\mathrm{d}\Delta T_v}{\mathrm{d}t}=P_{R_e}-\frac{\Delta T_v-\Delta T_m}{R_{tv}},\qquad
C_{tm}\frac{\mathrm{d}\Delta T_m}{\mathrm{d}t}=\frac{\Delta T_v-\Delta T_m}{R_{tv}}-\frac{\Delta T_m}{R_{tm}} .$$

**Rétroaction indispensable.** Sous tension imposée — l'hypothèse « source de tension » posée juste au-dessus — la puissance dissipée n'est pas constante : $P_{R_e}=U^2/R_e\propto1/R_e(T)$. Quand $R_e$ monte de 39 %, la puissance dissipée **baisse** d'autant, et c'est un mécanisme stabilisant du premier ordre. Klippel fonde d'ailleurs la compression exactement là-dessus (*« less drive from a constant voltage source into a rising impedance »*). Dans la boucle d'Euler, `P` devient donc `P0/(1 + alpha*T1[k])`, où $P_0$ est la puissance dissipée **à froid** :

```python
Rth1, tau1 = 2.0, 10.0        # bobine -> aimant : K/W, s   [[ordres de grandeur]]
Rth2, tau2 = 0.5, 20*60.0     # aimant -> ambiant : K/W, s  [[ordres de grandeur]]
C1, C2 = tau1/Rth1, tau2/Rth2 # capacites thermiques J/K
P0 = 50.0                     # puissance dissipee A FROID (W) -- hypothese, cf. tableau ci-dessous
for k in range(n):
    P   = P0/(1 + alpha*T1[k])        # retroaction source de tension
    q12 = (T1[k]-T2[k])/Rth1
    q2a = T2[k]/Rth2
    T1[k+1] = T1[k] + dt*(P - q12)/C1
    T2[k+1] = T2[k] + dt*(q12 - q2a)/C2
```

Le régime permanent auto-cohérent s'obtient analytiquement en résolvant $\alpha\,\Delta T^2+\Delta T-P_0(R_{tv}+R_{tm})=0$ :

$$\Delta T_\infty=\frac{-1+\sqrt{1+4\alpha P_0 (R_{tv}+R_{tm})}}{2\alpha}
\;=\;92\ \text{K pour } P_0=50\ \text{W},\ \text{au lieu de }125\ \text{K à } P\ \text{constante.}$$

```
  t (s) | P constante        | avec retroaction    (dT bobine / compression)
      1 |   9.5 K / -0.32 dB |   9.4 K / -0.31 dB
     10 |  63.3 K / -1.93 dB |  55.3 K / -1.71 dB
     60 | 100.6 K / -2.89 dB |  77.3 K / -2.30 dB
    600 | 109.6 K / -3.11 dB |  82.8 K / -2.45 dB
   3600 | 123.7 K / -3.44 dB |  91.2 K / -2.66 dB   (aimant : +23.7 K vs +17.6 K)
```

Toute la colonne de droite est **auto-cohérente** et c'est elle qu'on retient ; l'écart avec la colonne de gauche (−27 % sur l'échauffement permanent) mesure exactement ce que la rétroaction stabilise.

**Constantes de temps : le chiffre de Klippel n'est pas celui d'un 18″.** Les valeurs **publiées** (Klippel 2004, table 2, « driver A », petit HP : $R_e=1{,}88$ Ω, 9,7 g de cuivre, 545 g d'acier) sont $R_{tv}=5{,}9$ K/W, $C_{tv}=3{,}6$ J/K → $\tau_v\approx21$ s ; $R_{tm}=4{,}1$ K/W, $C_{tm}=272$ J/K → $\tau_m\approx19$ min. Le couple $(R_{tv}=2$ K/W, $\tau_v=10$ s$)$ utilisé ci-dessus impose $C_{tv}=5$ J/K, soit **13 g de cuivre** : encore un petit haut-parleur. Une bobine de 18″ de sonorisation pèse plutôt 50 à 150 g de cuivre, soit $C_{tv}\approx20$ à 60 J/K et, à $R_{tv}=2$ K/W, **$\tau_v$ de l'ordre de 40 s à 2 min**. On retient donc : $\tau_v=$ `[[à mesurer en phase 4]]`, ordre de grandeur 10 s (petit HP, Klippel) à ~1 min (18″), et **la mesure de $\tau_v$ est le premier geste de la phase 4 énergie** puisque c'est elle qui dimensionne les deux protocoles de 06.6.

**Indexation sur les deux niveaux d'écoute gelés.** Le $P_0=50$ W ci-dessus est une hypothèse de sonorisation, pas un résultat. Les chiffres qui comptent sont ceux des **deux niveaux gelés en phase 0** — $P_{\text{faible}}$ et $P_{\text{fort}}$, `[[à geler avant toute mesure]]`. En attendant, voici le même modèle balayé en puissance (régime permanent auto-cohérent, $R_{tv}+R_{tm}=2{,}5$ K/W, $f_c$ définie plus bas) :

| $P_{R_e}$ | $\Delta T_\infty$ | $R_e/R_{e0}$ | $f(-3\ \text{dB})$ | dérive | compression | bosse |
|---|---|---|---|---|---|---|
| 3 W (écoute domestique) | 7 K | 1,029 | 102,1 Hz | +2,1 % | −0,25 dB | +0,05 dB |
| 11 W (crête 15 dB sous 350 W) | 25 K | 1,098 | 106,8 Hz | +6,8 % | −0,82 dB | +0,17 dB |
| 35 W (crête 10 dB) | 69 K | 1,271 | 116,1 Hz | +16,2 % | −2,08 dB | +0,64 dB |
| 50 W (hypothèse sonorisation) | 92 K | 1,361 | 119,9 Hz | +20,0 % | −2,68 dB | +0,93 dB |

**Au niveau faible la dérive thermique est négligeable (~+2 % sur $f_c$) ; c'est au niveau fort qu'elle dépasse la porte de validation ±5 %.** C'est précisément ce que le critère « robustesse » est fait pour attraper, et c'est la formulation à tenir devant le jury — pas « +20 % » sans dire à quelle puissance.

**Dérive thermique : quel repère de fréquence on suit ici, et pourquoi ce n'est pas $f_c$.** La seule définition gelée du TIPE est celle du § 04.1 : **$f_c$ = fréquence de croisement des deux voies**. Elle n'est pas l'outil adapté ici, parce qu'on veut voir la déformation de **la seule voie grave** quand $R_e$ monte. La grandeur suivie dans tout ce paragraphe est donc un **repère explicitement nommé**, le **−3 dB du passe-bas**, noté $f_{-3,PB}$ : la fréquence où le module descend du seuil retenu **sous le gain continu** $|H(f\to0)|=R/(R+r)$ — et non sous 0 dB absolu, ce qui mélangerait la perte d'insertion à la dérive. Rappel des trois repères du filtre 18 mH / 150 µF sur 8 Ω, tous distincts (§ 04.1) : **pôle** $f_0=1/(2\pi\sqrt{L_1C_1})=96{,}9$ Hz, **−3 dB du passe-bas** 99,9 Hz, **−3 dB du passe-haut** 93,9 Hz ($Q=0{,}730$, mi-puissance). Le code ne prend plus le premier point de la grille comme référence — ce qui rendait le résultat dépendant du choix de `np.logspace` — mais la valeur analytique, avec interpolation du croisement (il est ici appelé avec `seuil=3.0`, cf. la note de convention après le tableau) :

```python
def f_m3dB(R, r=0.0, seuil=3.0):
    g  = 20*np.log10(np.abs(H_pb(f, R, r)))
    g0 = 20*np.log10(R/(R+r))          # gain continu EXACT, pas g[0]
    i  = np.where(g < g0-seuil)[0][0]
    fc = np.interp(g0-seuil, [g[i], g[i-1]], [f[i], f[i-1]])   # croisement interpole
    return fc, g.max()-g0
```

| cas | $\Delta T$ (K) | $R$ (Ω) | $Q$ | $f_{-3,PB}$ (seuil 3,00 dB) | bosse |
|---|---|---|---|---|---|
| 8 Ω, $r=0$ | 0 | 8,00 | 0,730 | **99,8 Hz** | +0,02 dB |
| 8 Ω, $r=0$ | 50 | 9,28 | 0,847 | 112,3 Hz | +0,42 dB |
| 8 Ω, $r=0$ | 100 | 10,55 | 0,963 | 121,0 Hz | +1,04 dB |
| 8 Ω, $r=1$ Ω | 0 | 8,00 | — | 105,3 Hz | +0,01 dB |
| 8 Ω, $r=1$ Ω | 100 | 10,55 | — | 124,1 Hz | +0,83 dB |

<!-- Ancien tableau (99,7 / 111,4 / 119,7 Hz et 0 / +0,31 / +0,87 dB) : la référence était g[0], prise à 20 Hz, donc déjà sur la bosse dès que Q > 1/racine(2) ; en faisant varier le seul début de grille (10/20/30/40 Hz) la valeur chaude oscillait entre 116,1 et 120,6 Hz, soit 4 % d'artefact pur. -->

Les deux colonnes sont maintenant reproductibles et confirmées analytiquement : $f_{-3}=f_0\sqrt{x+\sqrt{x^2+1}}$ avec $x=1-1/(2Q^2)$, et $|H|_{\max}=Q/\sqrt{1-1/(4Q^2)}$ (+1,040 dB pour $Q=0{,}963$). La ligne froide retombe sur **99,8 Hz**, c'est-à-dire le repère « −3 dB du passe-bas » au seuil **littéral** 3,00 dB.

> **Note de convention (à lire avec le tableau).** La convention **de seuil** gelée pour tout le TIPE est la **mi-puissance, $-3{,}0103$ dB** (celle de REW, § 04.1) ; le tableau ci-dessus a été calculé au seuil **littéral 3,00 dB**. À la mi-puissance, la même colonne donne **99,9 / 112,4 / 121,1 Hz**. L'écart de 0,1 % entre les deux lectures est un écart de **convention**, pas un arrondi fautif, et il est sans portée devant la dérive de +21 % qui fait l'objet du paragraphe — mais c'est bien **99,9 Hz** qui est la valeur de référence du repère froid, et 99,8 Hz sa variante au seuil littéral. Les conclusions du paragraphe sont inchangées.

**Comparaison honnête des deux sources d'incertitude.** Une bobine à +100 K décale le repère $f_{-3,PB}$ de **+21 %** (99,8 → 121,0 Hz) et fait apparaître une bosse de 1,0 dB. C'est environ **trois fois** la dispersion due aux tolérances sur le **pôle** $f_0$ — $u(f_0)/f_0=\frac12\sqrt{(u_L/L)^2+(u_C/C)^2}$, soit, pour $L$ et $C$ à ±10 %, **7,1 % en borne au pire cas** et **4,1 % en incertitude-type** (loi rectangulaire, GUM ; toujours citer le couple, jamais un nombre seul, cf. § 04.9) — et **quatre fois** la porte de validation ±5 %. Deux réserves à énoncer dans la même phrase : les deux pourcentages ne portent pas sur le même repère ($f_0$, le pôle, pour les tolérances ; $f_{-3,PB}$ pour la dérive — et ni l'un ni l'autre n'est $f_c$, qui est le croisement des voies), et le +21 % suppose 50 W dissipés en continu. Sous ces réserves, **la dérive thermique est le premier poste d'erreur sur le raccord passif, devant les composants**.

Sur le modèle Z(f) illustratif, le gain du passe-bas à 100 Hz passe de +1,83 dB (froid) à +2,77 dB (+100 K) : la dérive est d'environ **+1 dB au raccord**, ce qui se voit directement sur la somme des voies. La référence active Sallen-Key ne voit jamais $R_e$ : **sa $f_c$ ne bouge pas**. La compression de sensibilité, elle, est une propriété du HP et frappe les deux architectures — avec une nuance : les −2,9 dB valent dans la zone contrôlée par la masse ; près de $F_c$ de la caisse la montée de $Q_{tc}$ (06.4) compense partiellement la chute en $1/R_e$, donc **la compression thermique déforme la réponse autant qu'elle la baisse**. L'optimiseur de l'acte 3 intègre ce point en évaluant la fonction de coût pour deux valeurs de $R_e$ (froid / niveau fort) et en pénalisant l'écart : c'est le critère « robustesse » transposé en contrainte de conception.

**Trois effets du second ordre, à citer sans les chiffrer faussement.**

1. **La self chauffe aussi**, et son cuivre a le même $\alpha$ : $r(T)=r_0[1+\alpha(T-T_0)]$, avec un effet auto-amplifiant ($r$ monte → les pertes montent → $r$ monte). Ordre de grandeur : 2 W dissipés dans une self à l'air libre ($R_{th}\approx20$ K/W `[[à mesurer]]`) → +40 K → $r$ +16 %. **Le modèle de coût du satellite self doit donc porter sur $r$ à chaud, pas sur la DCR mesurée à froid au multimètre** — et un fil plus fin donne un $r$ plus grand *et* une masse thermique plus faible, donc une double pénalité.
2. **L'aimant chauffe et perd du $Bl$** : une ferrite perd typiquement 0,2 %/K de $B_r$ de façon réversible ; le modèle prévoit +18 à +24 K sur l'aimant en régime permanent, soit quelques pour cent de $Bl$ en moins — ce qui ajoute de la compression **et** fait monter $Q_{es}\propto1/(Bl)^2$, donc désaligne encore la caisse.
3. **La voie médiums comprime aussi**, avec des bobines plus petites donc des $\tau$ plus courts. Comme le critère porte sur le **raccord** (la somme des deux voies), c'est l'**écart** de compression entre voies qui compte, pas seulement celle du sub. À ajouter au protocole de la phase 4 : $R_e$ du bloc médiums par la même méthode A.

### <a id="s06-6"></a>06.6 Mesurer la dérive de $R_e$ sans démonter le haut-parleur

**Méthode A — résistance DC juste après coupure (recommandée au lycée).** Un commutateur bipolaire bascule les bornes du HP de l'ampli vers un multimètre déjà en mode Ω (4 fils si possible, sinon soustraire la résistance des cordons mesurée à part). Jamais le multimètre sur un ampli en marche. Comme la bobine refroidit avec $\tau_v$, la première lecture est déjà fausse de ~9 % de l'échauffement ; on **extrapole** à $t=0$ par un ajustement exponentiel, ce qui donne en prime $\tau_v$. La fenêtre de relevé doit couvrir **au moins 3 $\tau_v$** : 30 s si $\tau_v\approx10$ s, 3 min si $\tau_v\approx1$ min (d'où l'importance de mesurer $\tau_v$ en premier, 06.5).

L'ajustement se fait en moindres carrés **linéaires à $\tau$ donné**, avec balayage sur $\tau$. `scipy.optimize.curve_fit` est disponible (scipy 1.18.1 installé) et aurait fait l'affaire : le balayage est un **choix**, pas un pis-aller — on voit le paysage du résidu, donc on voit si le minimum est franc ou plat, ce que `curve_fit` cacherait, et le calcul tourne sur n'importe quelle machine du lycée avec numpy seul.

```python
for tau in np.linspace(3, 40, 371):
    X = np.column_stack([np.ones_like(t), np.exp(-t/tau)])
    coef, res, *_ = np.linalg.lstsq(X, R, rcond=None)
    r2 = np.sum((X@coef - R)**2)
    if best is None or r2 < best[0]:
        best = (r2, tau, coef)
```

```
A la coupure (apres 600 s a 50 W) : dT_bobine = 109.6 K, dT_aimant = 9.7 K, R_e = 9.299 ohm
  t apres coupure (s) | R_DC lue (ohm)
    1.0               | 9.056
    3.0               | 8.637
    5.0               | 8.295
  erreur si on prend la lecture a 1 s : -8.7 % de l'echauffement
  ajustement R(t) = R_inf + A exp(-t/tau) : tau = 10.0 s (vrai tau1 = 10.0 s), R(0) extrapole = 9.298 ohm (vrai 9.299)
```

**Incertitude chiffrée dès maintenant** (Monte-Carlo, 300 tirages, 6 lectures espacées de 2 s, gigue temporelle ±0,2 s sur l'instant de lecture, quantification à la résolution du multimètre) :

| résolution du multimètre | $R(0)$ estimé (vrai 9,299 Ω) | $\Delta T$ (vrai 109,6 K) | $\tau_v$ (vrai 10,0 s) |
|---|---|---|---|
| 0,01 Ω (calibre 20 Ω) | 9,298 ± 0,004 Ω | 109,5 ± 0,2 K | 10,0 ± 0,2 s |
| 0,05 Ω | 9,298 ± 0,021 Ω | 109,6 ± 0,8 K | 9,8 ± 0,8 s |
| **0,1 Ω (calibre 200 Ω)** | 9,303 ± 0,042 Ω | **109,7 ± 1,6 K** | 9,8 ± 1,2 s |

Le biais est nul et la méthode reste utilisable **même avec un multimètre 3½ digits sans calibre 20 Ω** (le plus bas calibre étant alors 200 Ω, soit 0,1 Ω de résolution sur une lecture de 6,5 Ω) : ±1,6 K sur $\Delta T$, largement suffisant pour comparer à la prédiction de 06.5. `[[à vérifier sur le multimètre du lycée : calibre le plus bas et résolution]]`. **Repli sans achat** : injecter un courant continu ou à 1–2 Hz à travers la $R_{\text{ref}}$ 10 Ω et lire $V_{HP}$ et $V_{R_{\text{ref}}}$ à l'oscilloscope — c'est exactement le montage de la phase 1, avec une meilleure résolution et l'enregistrement automatique de la décroissance.

**Deux précautions pratiques** (absentes du brouillon, elles coûtent une manip ou un commutateur) : (i) **couper le signal et attendre ~1 s l'arrêt du cône avant de basculer** — la bobine encore en mouvement génère une f.é.m. qui fausse la mesure ohmique ; (ii) **commutateur à coupure avant fermeture**, jamais l'inverse, sinon la source de courant du multimètre débite dans la sortie de l'ampli, et l'ouverture d'une charge inductive sur un ampli en marche produit une surtension.

**Méthode B — pilote basse fréquence en régime établi.** Klippel superpose au signal un pilote à $f_p=1$ Hz et mesure $R_e$ par le rapport $V/I$ à cette fréquence (*« plus commode qu'une composante continue »*). Il faut $f_p\ll f_s$ pour que la partie motionnelle soit négligeable ; erreur sur le modèle illustratif ($f_s=40$ Hz) :

| $f_p$ (Hz) | $\operatorname{Re}\{\underline Z\}$ (Ω) | écart à $R_e$ | équivalent en $\Delta T$ |
|---|---|---|---|
| 1 | 6,509 | +0,1 % | +0,4 K |
| 2 | 6,536 | +0,6 % | +1,4 K |
| 5 | 6,730 | +3,5 % | +9 K |
| 10 | 7,498 | +15 % | +39 K |

À 1–2 Hz l'erreur est négligeable, mais le E-800 est spécifié 20 Hz–20 kHz : un pilote à 1 Hz sera probablement atténué par le couplage d'entrée `[[à vérifier]]`. On peut contourner en n'exploitant que la **variation** de $\operatorname{Re}\{\underline Z(f_p)\}$ entre froid et chaud (l'écart motionnel se compense au premier ordre), avec extraction du pilote par FFT (oscillo ou REW) sur $V_{HP}$ et $V_{R_{\text{ref}}}$ — c'est le montage de la phase 1 avec deux composantes spectrales. Méthode B = perspective ; méthode A = protocole de base.

**Protocole « robustesse » (phase 4).**

1. Mesure du raccord au **niveau faible**, HP froid, $R_{DC}$ relevée. **Deux rappels non négociables** : la somme des deux voies se mesure **avec inversion de polarité d'une voie** (2ⁿᵈ ordre Butterworth : sans inversion on mesurerait la dérive d'un trou, pas celle du raccord) ; et la mesure acoustique à 100 Hz se fait **en champ proche** ($\lambda\approx3{,}4$ m, modes de pièce, fenêtrage inopérant en BF) — la tentation d'écouter de loin est d'autant plus forte au niveau fort.
2. Bruit rose 40–250 Hz au **niveau fort** pendant une durée **fixée** (10 min, ou 3 $\tau_v$ si $\tau_v$ mesuré est plus long), sinon le résultat dépend de l'horloge.
3. Mesure du raccord au niveau fort, même protocole champ proche, même inversion.
4. Coupure et méthode A → $R_e$, $\Delta T$, $\tau_v$, avec l'incertitude du tableau ci-dessus.
5. Comparaison de la dérive de $f_c$ mesurée à la prédiction de 06.5 pour ce $\Delta T$.

Le même cycle sur la référence active isole la part « compression du HP » de la part « dérive du filtre ». **Sous-ensemble minimal** si le temps manque (FEUILLE-DE-ROUTE prévoit de couper ce satellite en premier) : $P_0$ marginal au multimètre sur les rails ±15 V, plus **une seule** mesure de $R_e$ après coupure au niveau fort — une demi-heure de banc, et le satellite reste quantitatif.

### <a id="s06-7"></a>06.7 Côté actif : consommation au repos et rendement de l'ampli

Ce que consomme la chaîne active sans signal, poste par poste :

| poste | ordre de grandeur | statut |
|---|---|---|
| AOP NE5532 (2 canaux) sous ±15 V | $I_{CC}\approx8$ mA typ (16 mA max) → $\approx0{,}24$ W typ | datasheet TI |
| variante TL072 | 1,4 mA/ampli typ (2,5 mA max) → $\approx0{,}08$ W | datasheet ST/TI |
| alimentation symétrique ±15 V (transfo + régulateurs) | pertes à vide souvent supérieures à l'AOP lui-même (quelques dixièmes de W à ~2 W) | ordre de grandeur, `[[à mesurer]]` |
| pré-ampli SX-801 | présent dans les deux scénarios → s'annule dans la comparaison | `[[à mesurer]]` pour info |
| t.amp E-800, **veille activée**, sans signal depuis > 15 min | l'ampli bascule seul en veille : c'est l'état le plus probable en usage réel | `[[à mesurer]]` — poste décisif |
| t.amp E-800, **veille désactivée**, allumé au repos | typiquement quelques dizaines de W pour un ampli de scène de cette taille | `[[à mesurer]]` — borne supérieure |
| t.amp E-800 éteint mais branché | consommation résiduelle du transfo | `[[à mesurer]]` |
| crossover actif du commerce actuellement en service | — | `[[à mesurer]]` (point de comparaison gratuit) |

**Le E-800 possède une mise en veille automatique débrayable** (manuel, ch. 5 : commutateur [ON]/[OFF]/[STANDBY], *« If the standby function is enabled, the device automatically switches to standby mode after fifteen minutes without any input signal »*, et *« In standby mode, the LED lights red. As soon as the unit receives a signal, it switches back to normal »*). Il y a donc **trois** états au secteur, pas deux, et « la consommation au repos » n'a pas de sens tant que la position du commutateur n'est pas gelée. Cette veille est en soi un dispositif de sobriété, qui joue en faveur des deux architectures et qui **écrase le terme $t_{\text{on}}/t_{\text{écoute}}$ de 06.8**.

**Deux comptabilités, comme pour le coût** (FEUILLE-DE-ROUTE, « coût marginal » vs « coût système ») :

- *Marginale* (enceinte de Thomas, un seul E-800 possédé) : l'ampli stéréo est allumé dans les deux scénarios et sa consommation au repos ne devrait pas dépendre du nombre de canaux utilisés — hypothèse **à tester** au wattmètre (un canal chargé / deux canaux chargés, sans signal). Alors $P_0^{\text{marg}}=$ carte AOP + son alimentation, de l'ordre du watt.
- *Système* (scénario stéréo équivalent : deux enceintes, donc deux amplis stéréo en bi-amplification contre un seul en passif) : $P_0^{\text{syst}}=$ consommation au repos d'un E-800 entier + **les deux cartes AOP** (2 × NE5532 ≈ 0,48 W typ, une par enceinte) + leur(s) alimentation(s). Compter une seule carte, comme le faisait le brouillon, sous-estimait le poste actif dans la comptabilité qui lui est justement la plus défavorable.

**Protocole wattmètre de prise** (résolution typique 0,1–1 W, imprécis sous quelques W — lire la notice de l'appareil acheté ; lire la puissance **active** en W, pas les VA) :

1. E-800 seul derrière le wattmètre, quatre états à distinguer : (a) éteint mais branché ; (a bis) **allumé, veille activée, sans signal depuis > 15 min** ; (a ter) **allumé, veille désactivée, sans signal** ; (b) allumé, un canal chargé 8 Ω ; (c) deux canaux chargés — lecture après 15 min de stabilisation thermique (le courant de repos d'un étage classe AB/H dérive avec la température). Utiliser le compteur kWh sur 1 h pour moyenner si l'affichage fluctue. **Geler la configuration de veille retenue pour toutes les mesures de la phase 4.**
2. **Sur le haut-parleur réel** (pas sur la résistance de charge), signal aux deux niveaux gelés (bruit rose 40–250 Hz) : donne $P_{\text{secteur}}$ à chaque niveau. Combinée à $P_{\text{voie}}$ mesurée à l'entrée du filtre ($V_{\text{RMS}}$ et $I_{\text{RMS}}$), elle donne **gratuitement le rendement de l'amplificateur** $\eta=P_{\text{voie}}/(P_{\text{secteur}}-P_{\text{repos}})$ aux deux niveaux — grandeur indispensable au bilan de 06.8. `[[à vérifier : puissance admissible de la résistance 8 Ω du lycée]]` — une résistance de labo fait 10 à 50 W, elle serait détruite ou hors tolérance si le niveau fort y était appliqué en continu ; sur résistance, ne dépasser que quelques watts et vérifier au multimètre que sa valeur n'a pas dérivé entre le début et la fin (ironie utile : elle subit exactement le phénomène étudié en 06.5).
3. Carte AOP : le wattmètre de prise n'a pas la résolution ; mesurer au multimètre les courants continus sur les rails $+15$ V et $-15$ V, $P_0=(I_++I_-)\times15$ V (équivalent à $30\ \text{V}\times I_q$ pour une alimentation symétrique équilibrée), puis la consommation secteur du bloc d'alimentation seul.
4. Pré-ampli et crossover actif existant : une lecture chacun, pour le tableau.

Point de comparaison gratuit pour l'étape 2 : le manuel donne un **courant typique absorbé** (A RMS, sous 230 V, sinus 1 kHz) par palier de puissance de sortie — la mesure au wattmètre doit s'en approcher. Toutes ces valeurs sont des lignes du tableau brut de la phase 4, avec la résolution de l'appareil comme incertitude, et **$\eta$ y figure au même titre que $r$ et $P_0$**.

### <a id="s06-8"></a>06.8 Point de croisement énergétique

**La frontière du bilan doit être la même pour les deux architectures.** C'était la faute centrale du brouillon : $P_0$ est mesuré **au compteur**, tandis que $P\,r/(R+r)$ est une chaleur dissipée **en sortie d'amplificateur**. Pour délivrer 1 W de plus en sortie il faut tirer $1/\eta$ W au secteur, avec $\eta$ le rendement de l'ampli au point de fonctionnement — médiocre à faible puissance (quelques watts moyens sur un ampli de 350 W en classe H : $\eta$ de l'ordre de 15 à 40 %). On ramène donc **tout au compteur**.

Soit $P_{\text{voie}}$ la puissance électrique moyenne délivrée à la voie grave pendant l'écoute, $a$ le rapport de tension du L-pad éventuel et $\varphi$ la fraction de la puissance dirigée vers la voie atténuée. L'égalité des énergies au secteur s'écrit

$$\underbrace{P_0\,t_{\text{on}}}_{\text{actif}}
=\underbrace{\frac{1}{\eta}\left[\frac{r}{R+r}+(1-a^2)\,\varphi\right]P_{\text{voie}}\,t_{\text{écoute}}}_{\text{passif}}
\;\Longrightarrow\;
\boxed{\;P^\star=\eta\,P_0\,\frac{t_{\text{on}}}{t_{\text{écoute}}}\Big/\left[\frac{r}{R+r}+(1-a^2)\,\varphi\right]\;}$$

Sans L-pad ($a=1$) on retrouve la forme simple $P^\star=\eta\,P_0\,\frac{R+r}{r}\cdot\frac{t_{\text{on}}}{t_{\text{écoute}}}$ ; à $\eta=1$ et $t_{\text{on}}=t_{\text{écoute}}$, la formule du brouillon, $P^\star=9\,P_0$ pour $r=1$ Ω. **Les deux corrections vont dans le même sens et se cumulent** :

| $\eta$ | sans L-pad | avec L-pad 3 dB sur 30 % de la puissance |
|---|---|---|
| 1,00 (référence du brouillon) | 18,0 W | 7,7 W |
| 0,60 | 10,8 W | 4,6 W |
| 0,40 | 7,2 W | 3,1 W |
| 0,25 | 4,5 W | 1,9 W |

($P_0=2$ W, $r=1$ Ω, $t_{\text{on}}=t_{\text{écoute}}$.) Le $P^\star$ annoncé par le brouillon était donc **surestimé d'un facteur 2 à 9**, et la conclusion « le passif gagne en écoute domestique » n'est **pas acquise** : elle est conditionnelle à $\eta$, à l'existence d'un L-pad (que 06.3 laisse ouverte tant que les sensibilités sont `[[à documenter]]`) et à la fraction de pertes réellement pondérée par le spectre — qui, rappel de 06.1, va de 2 % à 33 % et non 11 %. **$P^\star$ doit être donné comme un intervalle, ordre de grandeur 2 à 18 W**, c'est-à-dire à cheval sur la zone d'écoute domestique.

**Ordre de grandeur de $P_{\text{voie}}$.** La musique a un facteur de crête de 10 à 20 dB : si les crêtes atteignent la puissance sinus de l'ampli (350 W / 8 Ω), la moyenne n'est que de 35 W (10 dB), 11 W (15 dB) ou 3,5 W (20 dB). En écoute domestique la moyenne est de quelques watts ; en sonorisation, plusieurs dizaines. Les **deux niveaux gelés en phase 0** donneront les deux valeurs à utiliser, mesurées au banc ($V_{\text{RMS}}$ et $I_{\text{RMS}}$ à l'entrée du filtre).

**Profil d'usage.** Le surcoût actif court tant que la chaîne est allumée ($t_{\text{on}}$), les pertes passives seulement pendant l'écoute ($t_{\text{écoute}}$) : une chaîne laissée allumée 5 fois plus longtemps qu'elle ne joue multiplie $P^\star$ par 5. Mais **la veille automatique du E-800 (06.7) coupe ce raisonnement** : au bout de 15 min sans signal l'ampli quitte de lui-même l'état consommateur. Le profil doit donc distinguer trois états — allumé au repos, veille, éteint — et le scénario « allumé 24 h/j » n'est légitime que **veille désactivée**, comme borne supérieure explicitement étiquetée.

**Exemple chiffré, hypothèses explicites** (2 h/j d'écoute, $P_{\text{voie}}=3$ W, $r=1$ Ω, pas de L-pad ; les pertes passives sont ramenées au compteur en divisant par $\eta$) :

```
                                E_actif      E_passif au secteur       facteur
  P0 =  2 W allume  2 h/j :    1.46 kWh/an   0.24 (eta=1) a 1.62 (eta=0,15)     0.9 a 6
  P0 =  2 W allume 24 h/j :   17.52 kWh/an   0.24            a 1.62            10.8 a 72
  P0 = 20 W allume  2 h/j :   14.60 kWh/an   0.24            a 1.62             9.0 a 60
  P0 = 20 W allume 24 h/j :  175.20 kWh/an   0.24            a 1.62           108   a 720
```

Avec ces hypothèses (qui ne sont **pas** des mesures), le passif est plus sobre **d'un facteur compris entre ~1 et ~700** selon $P_0$, le profil d'usage et le rendement de l'ampli. La borne basse mérite d'être dite : dans le cas le plus favorable à l'actif ($P_0=2$ W, 2 h/j) et avec un ampli à $\eta=15\ \%$, **l'actif repasse devant**. Le brouillon annonçait « un facteur 6 à 700 » parce qu'il comptait les pertes passives en sortie d'ampli et le repos actif au compteur. **Ce sont les mesures de $P_0$, de $\eta$ et de $r$ qui tranchent**, pas le raisonnement.

### <a id="s06-9"></a>06.9 Présenter l'argument « sobriété » honnêtement

- **Cadrer d'abord** : le haut-parleur dissipe lui-même plus de 97 % de ce qu'on lui envoie ($\eta_0\approx2{,}5\ \%$). Ce que compare cette section est du second ordre — mais c'est le seul ordre sur lequel le concepteur du filtre a prise. Le dire renforce l'honnêteté au lieu de l'affaiblir, et relie le TIPE au thème national sur un chiffre marquant.
- Annoncer que la comparaison **dépend du profil d'usage** ($P_{\text{voie}}$, $t_{\text{on}}/t_{\text{écoute}}$, état de veille) et de **trois** grandeurs mesurées : $r$, $P_0$ et **$\eta$** — le rendement de l'ampli est le facteur qui déplace le plus $P^\star$, et le protocole 06.7 le fournit gratuitement. Donner $P^\star$ comme un **intervalle**, pas « le passif gagne ».
- Montrer les **deux comptabilités** (marginale : cartes AOP seules ; système : second ampli) sur le même graphique $E$ en fonction de $P$ : deux droites actives horizontales, une bande passive de pente $\left[\frac{r}{R+r}+(1-a^2)\varphi\right]/\eta$, les deux niveaux gelés en repères verticaux.
- Propager les incertitudes : résolution du wattmètre sur $P_0$, tolérance de $r$ (±2 % au multimètre 4 fils, ordre de grandeur), dérive de $r$ à chaud (+16 % pour 2 W dissipés, 06.5), et dépendance de la fraction de pertes à $\underline Z(f)$ (2 % au pic, 11 % en bande passante, 33 % au raccord) — **une bande, pas une ligne**.
- Dire ce que le bilan **ne compte pas** : l'énergie grise du cuivre de la self (traitée dans le satellite self par la masse, pas en kWh), l'ESR des condensateurs et les pertes fer d'une éventuelle self à noyau (06.2, `[[à mesurer]]`), et l'asymétrie de répartition spectrale entre canaux en bi-amplification. Le rendement de l'ampli, lui, **est** compté désormais : il ne s'annule pas entre les deux scénarios, puisqu'en actif l'ampli ne délivre pas $P_r$ et qu'en passif si.
- Relier au thème : *efficacité* = $r/(R+r)$, $P_0$ et $\eta$ **mesurés** ; *sobriété* = matière et composants ; *optimisation* = $r$ n'est pas subi mais **choisi** par la fonction de coût (pertes contre masse de cuivre, loi $r\times m\approx$ cte à $L$ fixée pour une self à air), et le L-pad n'est pas qu'une perte : c'est un achat d'immunité à $\underline Z(f)$. Le croisement énergétique est un satellite : une mesure de $P_0$ et une de $\eta$ suffisent à le rendre quantitatif, et il se coupe en premier si le temps manque (sous-ensemble minimal en 06.6).

### Ce qu'il faut retenir pour l'oral

- **Cadrage** : le HP convertit ~2,5 % de l'électricité en son ; tout le reste chauffe. Les pertes du filtre sont du second ordre — mais ce sont les seules qu'on choisit.
- **Pertes passives** : $r/(R+r)$ → 11 % et −1 dB pour 1 Ω / 8 Ω en bande passante, mais 2 % au pic de résonance et 33 % au raccord sur la charge réelle, plus la DCR de la self parallèle du passe-haut (27 % de la voie médium à 40 Hz) et l'ESR des condensateurs. D'où une évaluation **spectrale, sur toutes les branches**, dans la fonction de coût. Contrepartie inattendue : la DCR amortit la résonance parasite du filtre catalogue (+10,8 → +8,0 dB).
- **Un seul levier, deux noms** : DCR et échauffement s'ajoutent au même endroit du modèle. +100 K ≡ +2,55 Ω en série ⇒ $Q_{ts}$ +33 % : l'échauffement désaligne la caisse autant qu'il décale le filtre.
- **Thermique** : le cuivre prend +0,39 %/K. À 50 W dissipés, +92 K en régime auto-cohérent (et non 125 K : sous tension imposée la puissance dissipée baisse quand $R_e$ monte) → −2,7 dB de sensibilité (les deux architectures) et **le repère « −3 dB du passe-bas » du passif de 99,8 à 120 Hz, soit +20 %** (repère, pas $f_c$ : cf. § 06.5) — mais **au niveau d'écoute domestique (3 W) la dérive n'est que de +2 %**. Toujours dire à quelle puissance. $\tau_v$ : 10 s pour un petit HP, ~1 min attendue pour un 18″, à mesurer en premier.
- **$R_e$ chaud se mesure sans démonter** : $R_{DC}$ après coupure extrapolée à $t=0$ (donne aussi $\tau_v$) ; ±1,6 K même avec un multimètre au calibre 200 Ω. Klippel utilise un pilote à 1 Hz.
- **Croisement énergétique** : $P^\star=\eta\,P_0\,\frac{t_{\text{on}}}{t_{\text{écoute}}}\big/\bigl[\frac{r}{R+r}+(1-a^2)\varphi\bigr]$. Avec $P_0\approx2$ W et $r=1$ Ω, $P^\star$ va de ~2 W à ~18 W selon le rendement de l'ampli et l'existence d'un L-pad : **à cheval sur l'écoute domestique**, donc conclusion conditionnelle. Tout repose sur $P_0$, $\eta$ et $r$ **mesurés**, valeurs encore inconnues. La veille automatique du E-800 change la nature même de la « consommation au repos ».
- **Argument sobriété honnête** = deux comptabilités (marginale / système), même frontière de bilan des deux côtés, profil d'usage explicite, incertitudes et postes non comptés annoncés.

### Sources

- Klippel, W., « Nonlinear Modeling of the Heat Transfer in Loudspeakers », *J. Audio Eng. Soc.*, vol. 52, n° 1/2, 2004, p. 3–25 (manuscrit soumis, klippel.de) — modèle à deux constantes de temps (fig. 2) ; **table 2** (driver A : $R_{tv}=5{,}9$ K/W, $C_{tv}=3{,}6$ J/K, $R_{tm}=4{,}1$ K/W, $C_{tm}=272$ J/K, $\delta=0{,}00393$ K⁻¹, 9,7 g de cuivre, 545 g d'acier) ; **table 1** : *« Significant variation (60 %) are found in the measured thermal resistance depending on the properties of the signal »* — les paramètres thermiques ne valent que pour un stimulus donné ; **table 3** : $\Delta T_{on}=138$ K à 1 kHz pour $P_{Re}=14$ W contre 52 K à 80 Hz pour 13 W, avec $\gamma=60\ \%$ à 80 Hz, soit une résistance thermique effective qui tombe de 9,9 à 4,0 K/W — près de la résonance, le déplacement de la bobine crée une convection forcée qui emporte ~60 % du flux. Le modèle linéaire **surestime** donc l'échauffement d'un sub joué autour de $f_s$ : nos chiffres restent des majorants, la rétroaction de 06.5 mise à part. Compression fondée sur *« less drive from a constant voltage source into a rising impedance »* ; pilote à 1 Hz pour $R_e$, *« more convenient than using an additional dc-component »*.
  <!-- Vérifié dans le texte source (sec06/klippel.txt) : les 60 % existent DEUX fois et désignent deux choses différentes. Table 1 = dispersion de R_th selon le programme ; table 3 = gamma = 60 %, part du flux détournée vers la convection à 80 Hz. La formulation du brouillon (« convection forcée qui court-circuite jusqu'à 60 % du flux ») correspond bien à gamma en table 3 : elle est donc conservée, et la statistique de table 1 est ajoutée comme argument distinct. -->
- Button, D. J., « Heat Dissipation and Power Compression in Loudspeakers », *J. Audio Eng. Soc.*, vol. 40, n° 1/2, janv./févr. 1992, p. 32–41 (AES paper 2981) — rendements typiquement inférieurs à 5 %, −3 dB de compression à puissance nominale.
- Henricksen, C. A., « Heat Transfer Mechanisms in Loudspeakers: Analysis, Measurement and Design », *J. Audio Eng. Soc.*, vol. 35, n° 10, oct. 1987 ; Zuccatti, C., « Thermal Parameters and Power Ratings of Loudspeakers », *J. Audio Eng. Soc.*, vol. 38, n° 1/2, janv./févr. 1990 (cités par Klippel).
- Small, R. H., « Direct-Radiator Loudspeaker System Analysis », *J. Audio Eng. Soc.*, vol. 20, n° 5, juin 1972, p. 383–395 (AES e-library id 2066) — $Q_{es}$ avec résistance de générateur, et $\eta_0=4\pi^2f_s^3V_{as}/(c^3Q_{es})$.
- IEC 60028, *International standard of resistance for copper* (IACS) : $\alpha=0{,}00393$ K⁻¹ à 20 °C pour le cuivre recuit.
- Texas Instruments, NE5532 (8 mA typ / 16 mA max par boîtier sous ±15 V ; révisions récentes 6 mA typ `[[à vérifier sur la datasheet du lot acheté]]`) ; STMicroelectronics / TI, TL072 (1,4 mA/ampli typ, 2,5 mA max).
- Thomann, *the t.amp E-400 / E-800 / E-1200 / E-1500 – User Manual* (27.05.2020, ID 173888_173889_460282_460283), **ch. 6 « Technical specifications », p. 29–31** : classe H 2 paliers, 2 × 350 W RMS / 8 Ω, 2 × 500 W RMS / 4 Ω, 20 kΩ sym / 10 kΩ asym, 20 Hz–20 kHz (0/−3 dB) ±1 dB, sensibilité 0,77 V / 1,4 V, gain 36 dB / 31 dB ; rubrique « Power consumption » = **table de courant typique absorbé (A RMS, 230 V, sinus 1 kHz) par palier de puissance de sortie**, aucune valeur au repos publiée, aucun facteur d'amortissement publié. **Ch. 5, p. 21** : commutateur [ON]/[OFF]/[STANDBY], veille débrayable basculant après 15 min sans signal. Le chiffre de 1500 W provient de la **page produit** Thomann, pas du manuel.
  <!-- Le brouillon citait « p. 25 Technical Data » et attribuait les 1500 W au manuel : les deux points étaient faux, vérifiés sur sec06/e800.txt. -->
- Scripts exécutés (scratchpad `sec06/`) : `pertes_dcr.py` (06.1, 06.3, 06.4), `thermique_croisement.py` (06.5, 06.6-B, 06.8), `mesure_Re_coupure.py` (06.6-A), `corrections_verif.py` (rétroaction thermique, référence analytique du point −3 dB, indexation en puissance, L-pad sur charge complexe, DCR de $L_2$, Monte-Carlo de la méthode A, croisement corrigé). numpy seul (par choix de méthode : scipy 1.18.1 est installé, cf. préambule de section). Modèle Z(f) illustratif : `archive-v1/_gen.py` (paramètres arbitraires, **pas une mesure du sub de Thomas**).

## <a id="s07"></a>07. Validation acoustique : protocole de mesure au micro à 100 Hz

> Place dans le récit : acte 4 (phase 4 de FEUILLE-DE-ROUTE.md), tests 3 et 4, après le Bode électrique sur résistance 8 Ω puis sur haut-parleur. Cette section fixe le protocole **avant** toute mesure. Aucun chiffre ci-dessous n'a été mesuré sur l'enceinte de Thomas : les valeurs sont soit calculées (scripts reproduits, sorties reportées telles quelles), soit des ordres de grandeur typiques étiquetés comme tels, soit des placeholders [[à mesurer]].
>
> Les deux scripts d'appui — `scratchpad/sec07v/calc_sec07.py` et `scratchpad/sec07v/critere_rms.py` — n'utilisent **que numpy**. Ce n'est pas une contrainte subie : l'environnement du poste (vérifié le 2026-09-13) comporte Python 3.13.2, numpy 2.4.6, **scipy 1.18.1** et matplotlib 3.11.0, tous fonctionnels. C'est un choix de portabilité — ces calculs, comme la phase 3 (énumération exhaustive E12), tournent sur n'importe quelle machine du lycée avec numpy seul. Tous les extraits de code reproduits ci-dessous supposent en tête `import io, os, re` et `import numpy as np`, ainsi que `c = 343.0` ; sans ces lignes ils lèvent un `NameError`.

### <a id="s07-0"></a>Conventions gelées avant toute mesure

Six conventions de forme, anodines prises une par une, mais dont l'absence rend les chiffres incomparables d'une sous-section à l'autre — c'est le défaut qui saute aux yeux d'un correcteur. Elles font partie des critères à geler en phase 0.

| # | Convention | Valeur gelée |
|---|---|---|
| C1 | **Ce que désigne $f_c$** | La **fréquence de croisement des deux voies** ($\lvert H_{PB}G_{sub}\rvert = \lvert H_{PH}G_{med}\rvert$) — **définition unique du TIPE, posée au § 04.1**, et la seule utilisée dans les critères et les portes de validation. Les trois autres fréquences du filtre catalogue sont des **repères** portant chacun son nom propre, jamais « $f_c$ » : le **pôle** $f_0 = 1/(2\pi\sqrt{LC}) = 96{,}86$ Hz, le **−3 dB du passe-bas** (99,9 Hz) et le **−3 dB du passe-haut** (93,9 Hz), rapportés séparément en 07.7. **Seuil « −3 dB » = mi-puissance, $-3{,}0103$ dB** (convention de REW). |
| C2 | **Convention de phase** | $p(t) = \operatorname{Re}\{\underline{p}\,e^{+j\omega t}\}$ : un retard $\tau$ multiplie par $e^{-j\omega\tau}$ et la phase **décroît** avec la fréquence (c'est la convention de REW). À l'oscilloscope, $\Delta t$ étant le retard de $V_{\text{out}}$ sur $V_{\text{in}}$ : $\varphi = -360\,f\,\Delta t$ (deg), ramené dans $\,]-180°,180°]$. |
| C3 | **Quatre bandes distinctes** | Balayée : Start 10 Hz – End 1 kHz au niveau faible, Start $\ge 2f_B$ au niveau fort (07.10, 07.11). Exportée : 10–1000 Hz. **Bande du critère : 40–250 Hz.** Validité du champ proche : $\le 280$ Hz ($ka = 1$) ou $\le 140$ Hz en lecture prudente ($ka = 1/2$) pour le 18″ (07.3). |
| C4 | **Arrondi** | Critères et écarts-types à **0,1 dB** (l'incertitude-type sur un critère moyenné sur 3 répétitions vaut ~0,1 dB) ; fréquences à 0,1 Hz. |
| C5 | **Où se définit un niveau** | Tension RMS **aux bornes du haut-parleur**, sur une sinusoïde à 100 Hz (07.8) — pas à la sortie de l'ampli. |
| C6 | **Célérité** | $c = 343$ m/s partout. Entre 15 et 25 °C, $c = 331{,}3\sqrt{1+T/273{,}15}$ varie de 1,7 % : modes et retards se décalent d'autant, sous le bruit de mesure. La température de la pièce est consignée à chaque session, sans correction. |

### <a id="s07-1"></a>07.1 Pourquoi la pièce domine sous 150 Hz

Une pièce parallélépipédique $L_x \times L_y \times L_z$ à parois rigides possède des ondes stationnaires (modes propres) aux fréquences

$$f_{lmn} = \frac{c}{2}\sqrt{\left(\frac{l}{L_x}\right)^2+\left(\frac{m}{L_y}\right)^2+\left(\frac{n}{L_z}\right)^2},\qquad l,m,n \in \mathbb{N},$$

avec $c = 343$ m/s (air à 20 °C). À 100 Hz, $\lambda = c/f = 3{,}43$ m : l'onde est de la taille de la pièce et chaque paroi est à moins d'une longueur d'onde du micro. Exemple pour une pièce de 5 × 4 × 2,5 m (ordre de grandeur typique d'une salle de classe, $V = 50$ m³) :

| Mode $(l,m,n)$ | $f_{lmn}$ (Hz) | Type |
|---|---|---|
| (1,0,0) | 34,3 | axial |
| (0,1,0) | 42,9 | axial |
| (1,1,0) | 54,9 | tangentiel |
| (0,0,1) et (2,0,0) | 68,6 | axiaux |
| (1,0,1) | 76,7 | tangentiel |
| (0,1,1) et (2,1,0) | 80,9 | tangentiels |
| (0,2,0) | 85,8 | axial |
| (1,1,1) | 87,9 | oblique |
| (1,2,0) | 92,4 | tangentiel |
| (2,0,1) | 97,0 | tangentiel |

Le dénombrement donne **33 modes sous 150 Hz, dont 13 à ± 1/3 d'octave du raccord, soit dans $[79\,;126]$ Hz**. (Ne pas confondre avec la bande normalisée de tiers d'octave centrée sur 100 Hz, qui est $[89\,;112]$ Hz : deux objets différents aux noms voisins.) Selon la position du micro, chaque mode produit un renforcement ou une extinction de plusieurs dB : une courbe relevée à 1 m est celle du couple enceinte + pièce, pas celle du filtre.

La fréquence de Schroeder $f_S \approx 2000\sqrt{T_{60}/V}$ (Hz ; s ; m³), au-dessous de laquelle le champ est modal, vaut ici 179 Hz ($T_{60} = 0{,}4$ s) à 253 Hz ($T_{60} = 0{,}8$ s). Autrement dit : **selon l'amortissement de la pièce, 82 % (cas le plus favorable) à 100 % de l'étendue logarithmique de la bande du critère est en régime modal**. Même dans le cas favorable, seule la tranche 179–250 Hz — 0,48 octave sur 2,64 — échappe au régime modal.

```python
import numpy as np
c = 343.0
Lx, Ly, Lz = 5.0, 4.0, 2.5   # ordre de grandeur typique (salle de classe / chambre)
V = Lx*Ly*Lz
modes = []
for l in range(0, 8):
    for m in range(0, 8):
        for n in range(0, 8):
            if (l, m, n) == (0, 0, 0):
                continue
            f = c/2*np.sqrt((l/Lx)**2 + (m/Ly)**2 + (n/Lz)**2)
            if f <= 150:
                modes.append((f, l, m, n))
modes.sort()
f_lo, f_hi = 100*2**(-1/3), 100*2**(1/3)
n_tiers = sum(1 for f, *_ in modes if f_lo <= f <= f_hi)
```

Sortie (extrait de `calc_sec07.py`) : `Pièce 5.0 x 4.0 x 2.5 m (V = 50 m3) : 33 modes propres sous 150 Hz` ; `Modes à ± 1/3 d'octave du raccord, soit dans [79 ; 126] Hz : 13` ; `f_S = 179 Hz pour T60 = 0.4 s -> 82 % de l'étendue log de 40-250 Hz est en régime modal` ; `f_S = 253 Hz pour T60 = 0.8 s -> 100 %`.

### <a id="s07-2"></a>07.2 Pourquoi le fenêtrage temporel (gating) est inopérant en basses fréquences

La mesure « quasi anéchoïque » de REW tronque la réponse impulsionnelle avant l'arrivée de la première réflexion (fenêtre de durée $T$). Une fenêtre de durée $T$ ne peut pas séparer deux fréquences plus proches que

$$\Delta f = \frac{1}{T}.$$

Scénario réaliste : source et micro à 1 m du sol, micro à 1 m de l'enceinte. Le trajet réfléchi par le sol vaut $\sqrt{1^2 + 2^2} = 2{,}24$ m, soit un retard de $(2{,}24 - 1)/343 = 3{,}60$ ms → $T \le 3{,}6$ ms → $\Delta f \ge 277$ Hz. **Sous 280 Hz, la réponse fenêtrée ne contient pas un seul point de fréquence indépendant.** Inversement, pour obtenir une résolution donnée à 100 Hz (largeur d'une bande de $1/n$ d'octave : $\Delta f = 100\,(2^{1/2n} - 2^{-1/2n})$) :

| Résolution voulue à 100 Hz | $\Delta f$ (Hz) | $T = 1/\Delta f$ | Différence de marche minimale $c\,T$ (première réflexion) |
|---|---|---|---|
| 1/3 d'octave | 23,2 | 43 ms | 14,8 m |
| 1/6 d'octave | 11,6 | 87 ms | 29,7 m |
| 1/12 d'octave | 5,8 | 173 ms | 59,4 m |

$c\,T$ est une **différence** de trajet entre le son direct et la première réflexion, pas un dégagement : 14,8 m de différence de marche correspond à des parois à environ $cT/2 \approx 7{,}4$ m du couple source-micro dans toutes les directions. Aucune pièce (pas même un gymnase) n'offre cela, et encore moins sous plafond. Conclusion : en dessous de ~300 Hz, on renonce au fenêtrage et on **change de méthode** : champ proche (07.3) ou plan de sol en extérieur (07.4).

### <a id="s07-3"></a>07.3 Mesure en champ proche (Keele, 1974)

**Principe.** Pour un piston circulaire bafflé de rayon $a$ et de vitesse $u$, la pression sur l'axe à la distance $z$ s'écrit (Beranek) $p(z) = \rho c\,u\left(e^{-jkz} - e^{-jk\sqrt{z^2+a^2}}\right)$. Au ras de la membrane ($z \to 0$) et en basses fréquences ($ka \ll 1$, $k = 2\pi f/c$) : $|p_{NF}| \approx \rho c\,u\,ka = \rho\,\omega\,u\,a$. En champ lointain demi-espace : $|p_{FF}(r)| = \rho\,\omega\,u\,S_d/(2\pi r) = \rho\,\omega\,u\,a^2/(2r)$. D'où la relation de Keele, **en module** :

$$\left|\frac{p_{FF}(r)}{p_{NF}}\right| = \frac{a}{2r} \qquad\Longrightarrow\qquad L_{FF}(1\ \text{m}) = L_{NF} + 20\log_{10}\frac{a}{2}\quad(\text{dB, demi-espace}).$$

En grandeurs complexes, le retard de propagation subsiste : $p_{FF}(r) = p_{NF}\,\dfrac{a}{2r}\,e^{-jkr}$ (convention C2). C'est ce facteur $e^{-jkr}$ qui est appliqué **séparément** dans `somme_champ_proche` (07.9) ; l'écrire ici en module évite de laisser croire que la sommation complexe de 07.4 pourrait se faire sans retard — ce qui serait exactement l'erreur que 07.4 cherche à éviter.

La pression en champ proche est proportionnelle à l'accélération volumique de la membrane : elle ne dépend ni de la pièce (le son direct domine de 20 à 30 dB) ni de la diffraction du coffret. Conditions de validité (Keele 1974 ; D'Appolito 2012) :

- **limite haute « molle »** : $ka \lesssim 1$, soit $f_{\max} \approx \dfrac{c}{2\pi a} = \dfrac{c}{\pi d}$ ($d$ = diamètre **effectif**, $d = 2\sqrt{S_d/\pi}$) ; formule rapide $f_{\max} \approx 10\,900/d_{\text{cm}}$ Hz. La littérature n'est pas unanime : certains auteurs retiennent $ka = 1/2$, deux fois plus bas ;
- **distance micro** $\le 0{,}11\,a$ de la membrane (erreur < 1 dB), au centre du cache-noyau.

```python
def nf(nom, Sd_cm2):
    a = np.sqrt(Sd_cm2*1e-4/np.pi)
    print(f"  {nom:22s} Sd={Sd_cm2:5.0f} cm2  a={a*100:5.2f} cm  f(ka=1)={c/(2*np.pi*a):4.0f} Hz  "
          f"f(ka=1/2)={c/(4*np.pi*a):4.0f} Hz  0,11a={0.11*a*100:4.2f} cm  NF->1 m : {20*np.log10(a/2):+.2f} dB")
```

| Haut-parleur | $S_d$ supposée (cm², ordre de grandeur typique) | $a$ (cm) | $f_{\max}$ ($ka = 1$) | $f_{\max}$ ($ka = 1/2$) | $0{,}11a$ | $L_{FF}(1\text{ m}) - L_{NF}$ |
|---|---|---|---|---|---|---|
| Sub 18″ | 1100 / 1200 / 1250 | 18,71 / 19,54 / 19,95 | 292 / 279 / 274 Hz | 146 / 140 / 137 Hz | 2,06 / 2,15 / 2,19 cm | −20,58 / −20,20 / −20,02 dB |
| Médium si 12″ | 530 | 12,99 | 420 Hz | 210 Hz | 1,43 cm | −23,75 dB |
| Médium si 10″ | 330 | 10,25 | 533 Hz | 266 Hz | 1,13 cm | −25,81 dB |
| Médium si 8″ | 220 | 8,37 | 652 Hz | 326 Hz | 0,92 cm | −27,57 dB |

D'après la photo `assets/enceinte-face.jpg`, les médiums latéraux semblent être des 12″ environ [[à vérifier : référence et $S_d$ datasheet]] ; la $S_d$ réelle du 18″ est [[à lire sur la datasheet]].

**La borne haute du critère est donc une décision à geler, pas un fait.** En lecture $ka = 1$, la bande 40–250 Hz est couverte de justesse (280 Hz pour le 18″, 420 Hz pour un 12″). En lecture prudente $ka = 1/2$, elle ne l'est pas (140 et 210 Hz). Deux issues, à trancher en phase 0 :

- soit abaisser la borne haute du critère à 200 Hz : cela suffit face à un médium 12″ ($ka = 1/2$ à 210 Hz), mais **pas** face au 18″, dont la lecture prudente plafonne à 140 Hz. Cette option ne règle donc le problème qu'à moitié, et coûte 0,32 octave sur 2,64 ;
- soit **justifier $ka = 1$ par un contrôle expérimental** : au niveau faible, comparer le champ proche ramené à 1 m et une mesure sur plan de sol (option B, 07.4) dans la zone 150–400 Hz ; si les deux se superposent à mieux que 1 dB, $ka = 1$ est validé sur ce haut-parleur-là. Contrôle peu coûteux et très convaincant à l'oral. C'est l'option recommandée.

Deux chiffres à connaître : l'approximation $|p_{NF}| \approx \rho\omega u a$ **surestime** la pression de 0,05 dB à 100 Hz, 0,19 dB à 200 Hz et **0,30 dB à 250 Hz** ($ka = 0{,}91$, $S_d = 1250$ cm²). C'est un biais systématique, identique pour les trois filtres, mais qui n'est pas négligeable devant les 0,6 dB que le critère doit départager : raison supplémentaire de ne lire le critère qu'en comparaison. Le retard de propagation sur 1,2 cm vaut 0,035 ms, soit 1,3° à 100 Hz : la phase mesurée en champ proche est, à cette précision, celle de la membrane elle-même.

#### Champ proche d'un bass-reflex à DEUX évents

**Ce n'est plus une variante conditionnelle : c'est le protocole du projet.** Le sub est
bass-reflex à deux évents (§ 01.10). La membrane **et** les deux évents rayonnent, et la réponse
du sub n'est ni l'une ni les autres : c'est leur somme, qu'aucun micro ne peut capter d'un seul
placement en champ proche. Il faut **trois** relevés et une reconstruction.

**Établissement de la pondération.** La relation de Keele dit qu'en champ lointain une source
de débit volumique $\underline U$ rayonne $\propto \underline U$, et qu'en champ proche on lit
$\lvert p_{NF}\rvert = \rho\omega u\,a$ avec $u=U/S$ et $a=\sqrt{S/\pi}$. Donc

$$\underline p_{NF}\;\propto\;\rho\omega\,\frac{\underline U}{S}\sqrt{\frac{S}{\pi}}=\frac{\rho\omega}{\sqrt\pi}\,\frac{\underline U}{\sqrt S}\qquad\Longleftrightarrow\qquad \underline U\;\propto\;\sqrt S\;\underline p_{NF}.$$

**Convention de signe, posée une fois pour toutes** : tous les débits sont comptés **positifs vers l'extérieur de la caisse**, membrane et évents. Avec cette convention et cette convention seule, le débit total rayonné est une **somme** : $\underline U_{tot}=\underline U_D+\sum_i\underline U_{P,i}$. (Si l'on comptait plutôt le débit *entrant* dans les évents depuis l'intérieur, il faudrait un signe moins — c'est la source d'erreur la plus fréquente, et la raison pour laquelle il vaut mieux figer la convention avant d'écrire la formule qu'après.) En normalisant par $\sqrt{S_D}$ pour exprimer le tout « en équivalent membrane » :

$$\boxed{\;\underline p_{\Sigma}(f)=\underline p_D(f)+\sum_{i=1}^{N}\sqrt{\frac{S_{P,i}}{S_D}}\;\underline p_{P,i}(f)\;}$$

somme **complexe**, tous les relevés partageant la **même référence temporelle** (boucle de
retour REW, 07.10) et le **même signal d'entrée**. Pour $N$ évents **identiques** dont on ne
mesurerait qu'un seul en supposant la symétrie, le poids devient $N\sqrt{S_P/S_D}$.

> **Le piège dans lequel il ne faut pas tomber, et il coûte exactement 3 dB.** Avec deux évents, il est
> tentant d'écrire $\sqrt{S_{P,tot}/S_D}$ en mettant l'**aire totale** sous la racine. C'est
> faux : le bon poids est $N\sqrt{S_P/S_D}=\sqrt N\cdot\sqrt{S_{P,tot}/S_D}$. Vérifié
> numériquement (`keele.py`) — deux évents de 10 cm sur une membrane de 1210 cm² : poids juste
> **0,5095**, poids fautif 0,3603, écart **$+3{,}01$ dB $=20\log_{10}\sqrt2$ exactement**, quelle
> que soit la taille des évents. L'identité elle-même a été revérifiée sur un cas jouet en
> reconstruisant $\underline U_D+\underline U_P$ à partir des trois pressions de champ proche :
> écart $10^{-16}$ en relatif.

**Signe et déphasage : ce qu'il ne faut pas « corriger » à la main.** La question revient à
chaque fois et elle a une réponse nette : **on n'applique aucune inversion de signe.** Chaque
$\underline p_{P,i}$ est mesuré avec la capsule dehors, orientée vers l'ouverture, exactement
comme pour la membrane, et avec la même référence temporelle : c'est exactement la convention
« tout positif vers l'extérieur » posée ci-dessus, et la phase relative *physique*
entre évent et membrane est donc **déjà contenue dans les relevés**. Elle vaut ce qu'elle vaut —
proche de l'opposition sous $f_b$, en quadrature vers $f_b$ — et c'est précisément ce qu'on veut
mesurer, pas ce qu'on veut imposer. Ajouter un $-1$ « parce que l'évent est alimenté par
l'arrière du cône » reviendrait à compter deux fois le même effet.

**Contrôle de signature, à faire avant d'exploiter quoi que ce soit** (il coûte une figure et il
attrape toutes les erreurs de signe, de poids et de référence temporelle) :

1. sous $f_b$, $\underline p_\Sigma$ doit **chuter à environ 24 dB/octave** (les deux sources
   s'opposent) alors que $\underline p_D$ seule ne chute qu'à 12 dB/oct — si la somme ne chute
   pas plus vite que la membrane seule, le signe ou la référence temporelle est fausse ;
2. autour de $f_b$, $\lvert \underline p_D\rvert$ passe par un **minimum** (la membrane est
   immobile) tandis que la contribution des évents passe par son maximum — c'est la signature
   acoustique du même phénomène que le creux d'impédance, et **la faire apparaître sur la même
   figure que $\lvert Z\rvert$ est l'un des plus beaux visuels que ce TIPE puisse produire** ;
3. le $f_b$ lu sur ce minimum doit recouper les trois voies du § 03.7 (critère 9).

**Distances et précautions, chiffrées.** Les évents ne se traitent pas comme la membrane :

| | membrane 18″ | un évent Ø 10 cm | un évent Ø 12,5 cm |
|---|---|---|---|
| $S$ | 1210 cm² | 78,5 cm² | 122,7 cm² |
| $a=\sqrt{S/\pi}$ | 19,63 cm | 5,00 cm | 6,25 cm |
| **distance micro max $0{,}11\,a$** | 2,16 cm | **0,55 cm** | **0,69 cm** |
| $f_{\max}$ ($ka=1$) | 279 Hz | 1095 Hz | 876 Hz |

Deux conséquences pratiques. (i) **La tolérance de placement est quatre fois plus serrée sur un
évent que sur la membrane** : 5 mm, pas 2 cm. Capsule dans le **plan de l'ouverture**, centrée,
jamais enfoncée dans le tube (à l'intérieur on ne mesure plus un champ proche mais une onde
guidée). (ii) **La limite haute $ka=1$ n'est pas contraignante pour un évent** (près de 1 kHz) :
c'est la membrane qui plafonne le critère, comme avant.

**Bruit de jet au niveau fort.** La capsule est placée dans le souffle de l'évent, où la vitesse
particulaire est maximale : bruit large bande, risque de saturation, et distorsion du balayage.
**Bonnette anti-vent obligatoire**, capsule légèrement décalée du centre, et **contrôle de la
cohérence du balayage dans REW avant exploitation** (une cohérence dégradée en bas de bande sur
la voie évent, et elle seule, signe le jet). C'est au niveau fort que la mesure d'évent est la
plus fragile, et c'est justement l'un des deux niveaux gelés : prévoir de la refaire.

**Contamination croisée : le chiffre honnête.** Les trois sources rayonnent en même temps ; le
micro placé à l'embouchure d'un évent entend aussi la membrane, à environ son niveau de champ
lointain à cette distance, soit $a_D/(2r)$ de son propre champ proche :

```
membrane 18" (aD = 19.6 cm) vue depuis le micro d'event :
  r = 20 cm :  -6.2 dB     r = 30 cm :  -9.7 dB     r = 40 cm : -12.2 dB     r = 50 cm : -14.1 dB
erreur relative sur le relevé d'un event = (1/rho) . N.sqrt(Sp/Sd) . aD/(2r)
  avec rho = (contribution des events)/(contribution de la membrane) a la frequence consideree
  rho = 10 -> +0.14 dB     rho = 3 -> +0.47 dB     rho = 1 -> +1.34 dB     rho = 0.3 -> +3.84 dB
  (N = 2, d_P = 10 cm, Sd = 1210 cm2, r = 30 cm)
```

Lecture : l'erreur est **faible là où elle compte**. Près de $f_b$, les évents portent presque
tout le débit ($\rho\gg1$) et la contamination reste sous 0,2 dB ; elle ne devient grande
($\rho<1$) qu'au-dessus, là où la contribution des évents est déjà négligeable dans la somme.
**On n'y peut d'ailleurs rien** : éloigner le micro pour fuir la membrane fait sortir du champ
proche. La parade est de *borner* l'erreur et de la déclarer, ce que la formule ci-dessus
permet ; et de **relever au mètre ruban la distance $r$ entre le centre de la membrane et chaque
embouchure** [[à mesurer]], sans quoi elle n'est même pas bornable.

**Temps de manip supplémentaire, à budgéter maintenant.** Le bass-reflex fait passer le sub de
**un** à **trois** relevés en champ proche : membrane, évent 1, évent 2. À chaque fois il faut
repositionner la capsule au millimètre, relancer un balayage avec référence temporelle et
vérifier la cohérence — compter **10 à 15 min par relevé supplémentaire**, soit **+20 à 30 min
par configuration** (une configuration = un filtre à un niveau). Sur la campagne de la phase 4
(3 filtres × 2 niveaux, plus les relevés bruts $G_{sub}$, $G_{med}$ de la phase 1), cela
représente **2 à 3 heures** de paillasse en plus. Ce n'est pas rédhibitoire, mais ce n'est pas
gratuit : c'est une séance de plus, à réserver. En caisse close, il n'y aurait eu rien à faire —
c'est le seul poste où le bass-reflex coûte vraiment quelque chose au projet.

**Limites assumées du champ proche.** (i) Il ne voit pas la diffraction du coffret : l'« étape de baffle » (transition +6 dB entre rayonnement en espace entier et demi-espace) tombe vers $f_3 \approx 115/W$ Hz avec $W$ la largeur du baffle en m (règle issue d'Olson [[à vérifier]]) : 230 Hz pour $W = 0{,}5$ m, 192 Hz pour $W = 0{,}6$ m, 144 Hz pour $W = 0{,}8$ m — dans tous les cas **dans la bande du critère**. La largeur réelle est [[à mesurer]]. (ii) Il ne voit pas la directivité ni la géométrie réelle des trois sources. (iii) Il n'est pas la réponse au point d'écoute.

**Budget d'incertitude de la mesure acoustique.** Aux trois limites ci-dessus s'ajoutent la planéité du micro en BF ([[à lire sur son fichier de calibration]]), la réponse résiduelle de la carte son après calibration, l'incertitude de positionnement du micro et la dérive entre sessions. Tous ces termes **entrent à l'identique dans les trois valeurs du critère** (catalogue, optimisé, actif) et se compensent donc dans la **comparaison** ; ils ne se compensent pas dans la **valeur absolue** du critère. D'où la règle : on ne publie jamais $\varepsilon_{RMS}$ comme une qualité absolue de l'enceinte, seulement des différences. La seule incertitude réellement propagée est celle de la répétabilité intra-session (07.8) et celle des tolérances de composants (07.9).

### <a id="s07-4"></a>07.4 Mesurer la somme des deux voies alors que les sources sont séparées

Géométrie (photo) : 18″ en façade du caisson central, deux médiums dans des boîtes latérales inclinées d'environ 45°, centres distants de l'ordre de 0,5 m [[à mesurer]]. Un micro unique en champ proche ne peut pas « voir » la somme : trois options, à discuter honnêtement.

**Option A — champ proche voie par voie + sommation complexe en post-traitement (retenue pour le critère).** On mesure séparément $p_{\text{sub}}(f)$, $p_{\text{med,G}}(f)$ et $p_{\text{med,D}}(f)$ (module et phase) avec la **même référence temporelle** (boucle de retour REW, 07.10) et le **même signal d'entrée**. Chaque source est ramenée en champ lointain par $a_i/(2d_i)$, retardée du trajet $d_i$ jusqu'à un point d'écoute virtuel (gelé : par exemple sur l'axe à 2 m [[à geler en phase 0]]), affectée de sa polarité, puis on somme :

$$p_{\Sigma}(f) = \sum_i \sigma_i\, \frac{a_i}{2 d_i}\, p_{NF,i}(f)\, e^{-j 2\pi f d_i / c},\qquad \sigma_i = \pm 1.$$

> **Le bass-reflex ajoute deux sources à cette somme, il ne la complique pas.** La voie grave
> n'est pas une source mais **trois** : membrane + évent 1 + évent 2 (§ 07.3). Deux façons
> équivalentes de les faire entrer, et il faut en choisir une et s'y tenir : (a) les traiter
> comme trois termes de plus dans la somme ci-dessus, avec leurs $a_i$ et leurs $d_i$ propres —
> c'est le plus rigoureux, puisque les évents ne sont pas au même endroit que la membrane ;
> (b) reconstruire d'abord $\underline p_\Sigma^{\,sub}$ « en équivalent membrane » par la
> pondération $\sqrt{S_P/S_D}$ du § 07.3, puis n'injecter qu'un seul terme sub dans la somme
> ci-dessus. La (b) est plus simple et suffit ici : à 100 Hz, un écart de trajet de 30 cm entre
> membrane et évent vaut 31,5°, soit 0,33 dB sur la somme de contributions égales — or la
> contribution des évents à 100 Hz est très inférieure à celle de la membrane (on est deux
> octaves et demie au-dessus de $f_b$), donc l'erreur réelle est bien plus faible. **Décision
> retenue : (b)**, avec cette justification, et la distance membrane-évent relevée au mètre pour
> pouvoir borner l'erreur [[à mesurer]]. En cas de doute, (a) est disponible sans travail
> supplémentaire — ce sont les mêmes trois relevés.

Les deux médiums en série reçoivent chacun $V/2$, mais rien ne garantit que leurs impédances — donc le partage de tension — ni leurs charges arrière soient rigoureusement identiques : ils sont dans **deux boîtes latérales distinctes**. On ne mesure donc pas l'un pour le doubler ; **on mesure les deux et on les somme**, $p_{\text{med}} = p_G + p_D$. Cela ne coûte rien (les deux sont déjà au programme des étapes 2 à 4) et transforme une hypothèse de symétrie en **donnée rapportée** : l'écart G/D est la dispersion entre haut-parleurs, un résultat en soi.

Sensibilité à l'incertitude de position (script, section D) :

| Écart de trajet $\Delta d$ | $\Delta\varphi$ à 100 Hz | Erreur sur la somme de deux contributions égales |
|---|---|---|
| 0,05 m | 5,2° | −0,01 dB |
| 0,10 m | 10,5° | −0,04 dB |
| 0,30 m | 31,5° | −0,33 dB |
| 0,50 m | 52,5° | −0,94 dB |
| 1,00 m | 105,0° | −4,31 dB |
| 1,72 m ($\lambda/2$) | 180,0° | extinction ($-\infty$) |

Une incertitude de ±10 cm sur les centres acoustiques coûte < 0,05 dB : à 100 Hz, la sommation est robuste. De même, deux médiums à ±0,25 m de l'axe vus depuis un point à 2 m sur l'axe diffèrent de trajet de 1,6 cm, soit 1,6° et 0,001 dB : les traiter comme équidistants est quantitativement inoffensif **sur l'axe**. Limites : la somme est **calculée, pas mesurée** ; elle dépend du point virtuel choisi (07.9 : passer de 2,00 m à 2,50 m pour les médiums change le critère de 0,6 à 1,6 dB sur une somme idéale) ; elle ignore la diffraction et la directivité. Le point virtuel doit donc être gelé et identique pour les trois filtres.

**Option B — mesure en extérieur sur plan de sol (Gander, 1982).** Enceinte et micro posés sur une grande surface dure (parking) : le sol devient un miroir acoustique sans réflexion retardée (le micro est dessus), la pièce disparaît, on mesure la **vraie somme** en un point (+6 dB de gain d'image). Limites : logistique (enceinte lourde, alimentation, météo, bruit ambiant), réflexions des bâtiments proches (peigne résiduel), un seul point, et difficulté de répéter aux deux niveaux et pour trois filtres. Rôle proposé : **une** campagne de contrôle, qui sert en même temps à valider l'hypothèse $ka = 1$ du 07.3.

**Option C — au point d'écoute dans la pièce (moyenne spatiale).** Mesure la réalité perçue mais mélange filtre et pièce : hors critère, éventuellement une illustration de fin d'oral.

### <a id="s07-5"></a>07.5 Inversion de polarité et vérification de la phase relative

Pour un couple LC du 2ᵉ ordre, passe-bas et passe-haut partagent le **même dénominateur** et ont pour numérateurs $1$ et $-x^2$ ($x = f/f_0$) : leur rapport vaut $-1/x^2$, réel négatif. Ils sont donc à **180° l'un de l'autre à toute fréquence**, et pas seulement au raccord. Au pôle $f_0 = 96{,}86$ Hz ils valent respectivement −90° et +90° et ont le même module (−2,73 dB). Conséquence : même polarité → annulation à $f_0$ ; une voie inversée → bosse de $20\log\sqrt2 = +3{,}0$ dB pour Butterworth ($Q = 1/\sqrt2$), somme plate pour Linkwitz-Riley ($Q = 0{,}5$, qui exige aussi l'inversion).

C'est un argument de **robustesse** exploitable : l'écart de phase entre voies pouvant se lire à n'importe quelle fréquence de la zone de recouvrement, l'étape 2 ci-dessous ne dépend pas d'avoir identifié précisément le raccord.

1. **Polarité mécanique de chaque HP** : pile 1,5 V brièvement sur les bornes, la membrane doit sortir quand le + est sur le +. Consigner le sens de câblage des deux médiums en série [[à vérifier]].
2. **Phase relative mesurée** : sur les relevés champ proche (même référence temporelle), lire $\varphi_{\text{sub}}(f) - \varphi_{\text{med}}(f)$ en plusieurs points de 80 à 125 Hz. Après inversion physique de la voie médium, l'écart attendu est proche de 0° et **constant** (± 30° tolérés : −0,33 dB sur la somme, tableau du 07.4). Un écart qui **dérive** avec la fréquence signale un retard résiduel, pas une erreur de polarité.
3. **Test de signature** : calculer la somme avec et sans inversion ; le trou profond sans inversion et la bosse avec inversion sont la preuve expérimentale de l'ordre 2 (sur sommes idéales, avec le plancher gelé du 07.9 : critère 5,9 dB contre 0,6 dB).

En **option A la somme est calculée** : inverser physiquement la voie ou changer $\sigma_i$ dans le script donnent rigoureusement le même résultat, puisque permuter les fils d'un haut-parleur ne modifie ni son impédance, ni le point de fonctionnement électrique du filtre, ni le module de sa réponse — seulement le signe de la pression. On inverse quand même **physiquement** pour l'enceinte livrée, et obligatoirement pour les options B et C où la somme est réellement acoustique.

### <a id="s07-6"></a>07.6 Égalisation des niveaux entre voies

Les sensibilités (dB/2,83 V/m) du 18″ et des médiums sont [[à documenter]]. Mesure de la sensibilité relative : réponse brute (sans filtre) de chaque voie en champ proche sous la même tension $V_{\text{ref}}$ aux bornes (par exemple 2 V RMS, 0,5 W/8 Ω), ramenée à 1 m par $20\log(a/2)$, puis $\Delta S = L_{1\text{m,sub}} - L_{1\text{m,med}}$ lu sur la zone de recouvrement (80–125 Hz).

Conséquence sur les trois filtres : la référence active égalise par le gain de chaque canal ; en passif, un atténuateur (L-pad) sur la voie la plus sensible **modifie la charge vue par le filtre** et doit entrer dans le modèle de l'optimiseur (phase 3) — c'est une variable de conception, pas une retouche.

**Règle de réglage de la référence active, à geler avant les mesures.** En passif, l'équilibre entre voies est figé par des composants E12 et un L-pad ; en actif, il est continûment réglable au potentiomètre. Laisser l'actif se régler librement lui donnerait un avantage structurel non déclaré. Deux formulations acceptables, il faut en choisir une :

- **(a)** les gains actifs sont réglés pour reproduire le $\Delta S$ mesuré ci-dessus, sans aucune optimisation du critère → l'actif est un **cas comparable** ;
- **(b)** les gains actifs sont optimisés → l'actif est présenté comme un **meilleur cas** (borne supérieure), pas comme un concurrent à armes égales.

Règle d'honnêteté pour le critère lui-même : aucun décalage de niveau entre voies n'est appliqué en post-traitement ; seul le niveau global (moyenne sur la bande) est libre (07.9).

### <a id="s07-7"></a>07.7 Mesures électriques préalables (Bode)

Ordre imposé par la feuille de route : (1) filtre sur **résistance de puissance 8 Ω**, (2) filtre sur **haut-parleur réel**, (3) acoustique. Points de méthode :

- **La source doit être l'amplificateur, pas le GBF.** Un GBF a 50 Ω de sortie ; le filtre LC calculé pour 8 Ω voit alors 50 Ω en série et n'a plus rien de Butterworth (calcul sur 18 mH / 150 µF / 8 Ω, script section H) :

| $R_s$ (Ω) | $\lvert H\rvert$ à 10 Hz | à 100 Hz | à 200 Hz |
|---|---|---|---|
| 0 | +0,01 dB | −3,02 dB | −12,71 dB |
| 1 (≈ DCR d'une self) | −1,02 dB | −3,57 dB | −12,78 dB |
| 50 (GBF direct) | −17,22 dB | −18,80 dB | −22,01 dB |

  Chaîne : GBF (ou REW) → E-800 à bas niveau → filtre → charge. Le E-800 a un gain de 36,7 dB en position 0,77 V (1 V en sortie pour 15 mV en entrée) ou 31,5 dB en position 1,4 V (26 mV) ; le sélecteur a aussi une position « 26 dB » (manuel Thomann), soit 50 mV pour 1 V. On règle le niveau au potentiomètre du canal et on le **mesure** au multimètre RMS.

- **Méthode principale : REW à deux canaux via la carte son** (un balayage donne gain *et* phase). Diviseurs résistifs **50:1** sur chaque tension — pas 20:1 : face à une entrée ligne limitée à ~1,2 V RMS [[à vérifier selon la carte]], un 20:1 ne laisse que 1,6 dB de marge au niveau fort (20 V → 1,00 V) et sature dès 24 V, alors qu'un 50:1 laisse 9,5 dB au niveau fort et ne sature pas avant 60 V.
- **Oscilloscope 2 voies : contre-vérification, pas méthode principale.** Au 1/12 d'octave de 20 à 500 Hz il y a 56 fréquences, soit plus de 650 relevés manuels (deux lectures × deux voies × trois filtres), à refaire sur résistance puis sur haut-parleur : plusieurs séances entières, dans une phase 4 qui tient de décembre à février. On garde l'oscilloscope pour ~10 fréquences bien choisies — 20, 50, 80, 94, 97, 100, 125, 200, 315, 500 Hz — ce qui suffit à valider la chaîne REW et reste infaillible si la carte son pose problème. C'est déjà la logique de repli de la phase 1. On y mesure $V_{\text{in}}$ (sortie ampli) et $V_{\text{out}}$ (aux bornes de la charge) : $|H| = V_{\text{out}}/V_{\text{in}}$ en dB, $\varphi = -360\,f\,\Delta t$ (convention C2).
- **Masses : oscilloscope ET carte son.** Les masses des sondes d'oscilloscope sont reliées à la terre ; **les deux entrées d'une interface audio partagent leur masse, elle-même reliée au châssis du PC donc à la terre** — c'est exactement le même risque, en pire : si la borne − de l'ampli n'est pas au potentiel de masse, y brancher un diviseur la met à la terre, c'est-à-dire un court-circuit partiel d'une sortie de 350 W et la destruction probable de l'interface. Le manuel du E-800 décrit trois modes (stéréo / parallèle / pont) et un interrupteur ground/lift, mais ne dit pas si la borne − HP est au potentiel de masse. **Avant tout branchement** : ampli éteint, continuité borne − ↔ châssis au multimètre ; ampli allumé sans signal, tension borne − ↔ terre ≈ 0 V. Si la sortie est flottante : à l'oscilloscope, deux sondes et fonction A − B ; à la carte son, entrées symétriques réellement flottantes, ou transformateurs de ligne 1:1 (~15 € pièce), ou l'on renonce et l'on reste à l'oscilloscope. **Jamais en mode pont, dans les deux cas.** [[à vérifier au multimètre]]
- **Attendu sur 8 Ω** (filtre catalogue 18 mH / 150 µF). Convention C1 : **$f_c$ est le croisement des deux voies** (§ 04.1) ; sur 8 Ω résistif et sans DCR il tombe à $f_0 = 96{,}86$ Hz, où les deux branches valent −2,73 dB et sont à ∓90° — coïncidence propre au cas idéal, qui cesse dès qu'il y a une DCR ou une charge réelle (§ 04.1, tableau des DCR). Les autres fréquences sont des **repères** distincts, rapportés à part :

| Repère (ce n'est pas $f_c$) | Passe-bas | Passe-haut |
|---|---|---|
| Pôle $f_0 = 1/(2\pi\sqrt{LC})$ | 96,86 Hz | 96,86 Hz |
| **Mi-puissance, −3,0103 dB (convention retenue)** sous le niveau de bande passante | **99,93 Hz** | **93,88 Hz** |
| Seuil littéral −3,000 dB sous le niveau de bande passante | 99,82 Hz | 93,99 Hz |

  Les deux couples sont exacts ; ils diffèrent par la **convention de seuil** (0,11 Hz, soit 0,11 %), pas par un arrondi fautif — voir l'encadré du § 04.1. Le couple gelé est celui de la **mi-puissance** (celui de REW), donc **99,9 / 93,9 Hz** en arrondi à 0,1 Hz (convention C4).

  Les deux branches **ne se croisent ni à 100 Hz ni à −3 dB** : à 100 Hz elles valent −3,02 dB (PB) et −2,46 dB (PH). Le $Q$ pertinent ici est $Q = R\sqrt{C/L} = 0{,}730$ (et non le $Q$ série $\frac1R\sqrt{L/C} = 1{,}369$).

<!-- Recalculé analytiquement (scratchpad, 2026-09-13) : les 99,8 / 94,0 Hz cités dans les sections précédentes sont le seuil LITTÉRAL de -3,000 dB (99,820 / 93,985 Hz) ; la mi-puissance (-3,0103 dB) donne 99,931 / 93,881 Hz. Ce n'est NI un arrondi fautif NI la convention « -3 dB sous le maximum de bande passante » (qui donnerait 99,75 / 94,16 Hz) : c'est une différence de convention de seuil. Les trois repères figurent dans le tableau ci-dessus ; l'écart de 0,1 Hz est sans portée, mais la convention est désormais écrite et gelée (mi-puissance). -->

- **Porte de validation, contre quoi ?** Deux portes distinctes, à ne pas confondre :
  1. **contre le calcul** : $f_0$ mesurée à ±5 % de $1/(2\pi\sqrt{LC})$ calculée avec les valeurs de **L et C mesurées individuellement** (self au GBF par résonance série, capacité au RLC-mètre). C'est la porte qui teste la chaîne de mesure ;
  2. **contre le nominal** (18 mH / 150 µF de catalogue) : la tolérance attendue est de ±7 % à 1σ, donc la porte est portée à **±15 %** (2σ). Une porte à ±5 % face au nominal recalerait 48 % de filtres pourtant conformes (Monte Carlo, 400 000 tirages gaussiens à $\sigma = 10$ %).

  Justification du 7 % : $f_0 = 1/(2\pi\sqrt{LC})$ donne $u(f_0)/f_0 = \frac12\sqrt{(u_L/L)^2 + (u_C/C)^2}$, soit, pour $L$ et $C$ à ±10 %, **7,1 % en borne au pire cas** et **4,1 % en incertitude-type** (loi rectangulaire, GUM : une tolérance ±10 % vaut $u = 10/\sqrt3 = 5{,}8$ %) — les deux chiffres se citent **toujours en couple**, jamais l'un seul ; 11,2 % en borne au pire cas si $C$ est à ±20 %. La porte à ±15 % ci-dessus est dimensionnée sur la borne au pire cas, donc conservative. <!-- Ce 11,2 % est numériquement voisin du « 11 % » de la v1, mais il n'a RIEN à voir : le 11 % v1 venait de la formule du RC 1er ordre abandonné, u(f_c)/f_c = sqrt((u_R/R)^2+(u_C/C)^2). Le facteur 1/2 est la signature du LC. Ne jamais réimporter la formule v1. --> Le facteur $\tfrac12$ est la signature du LC : il n'existe pas dans la formule d'un RC du 1er ordre.

- Sur le haut-parleur, l'écart aux valeurs ci-dessus n'est pas un défaut de mesure : **c'est l'objet de l'étude**.
- **Test de cohérence de bout en bout (gratuit, et le meilleur argument devant un jury).** La réponse acoustique d'une voie filtrée doit être égale, à la précision de mesure près, au **produit** de la réponse électrique $|H(f)|$ mesurée ici par la réponse brute du même haut-parleur mesurée à l'étape 1 du 07.8. Si les deux coïncident sur 40–250 Hz, la chaîne (électrique, acoustique, post-traitement) est validée dans le même esprit que la porte « étalonner sur composants connus » de la phase 1. Si elles ne coïncident pas, on sait où chercher avant d'avoir dépensé trois sessions.
- **Résistance de puissance** : valeur contrôlée au multimètre ; bobinée, son inductance parasite de quelques µH est négligeable à 250 Hz ; dissipation ≥ 50 W sur radiateur pour le niveau fort.

### <a id="s07-8"></a>07.8 Protocole reproductible aux deux niveaux d'écoute de référence

**Définition électrique des niveaux (convention C5) : tension RMS mesurée au multimètre, sur une sinusoïde à 100 Hz, directement aux bornes du haut-parleur.** Ce point n'est pas cosmétique : en passif, la tension à la sortie de l'ampli est **en amont du filtre**, et le haut-parleur en voit moins (−3 dB au raccord, plus les pertes DCR) ; en bi-amplification, la sortie de l'ampli **est** la tension aux bornes du haut-parleur. Définir le niveau à la sortie de l'ampli reviendrait donc à donner moins de puissance au passif qu'à l'actif — biais direct sur le critère « robustesse », qui mesure précisément un effet thermique. La tension de commande de l'ampli devient une **conséquence**, différente pour chaque filtre, et on la consigne. (Alternative acceptable si elle est écrite en phase 0 : égaliser sur le niveau acoustique en champ proche à 100 Hz.)

Ordres de grandeur pour la décision de phase 0 [[à geler]] : « faible » 2 V (0,5 W/8 Ω), « fort » entre 9 V (10 W) et 20 V (50 W). Contrainte : en champ proche d'un 18″ de sensibilité supposée 95 dB/2,83 V/m (ordre de grandeur typique), le script donne **112 dB SPL au niveau faible, 125 dB à 10 W et 132 dB à 50 W** — à comparer au SPL maximal du micro de mesure [[à vérifier sur sa fiche]] ; le niveau « fort » sera plafonné par le micro plus que par l'enceinte.

**Positions du micro.** La règle de Keele se compte depuis la **membrane**, pas depuis la grille : avec une grille en place, une cale de 2 cm laisse la capsule à 4–6 cm du cône, soit 2 à 3 fois la limite. **Grille déposée**, distance mesurée du cache-noyau **au repos** à la capsule. Il faut de plus tenir compte du débattement : à 40 Hz et au niveau fort (50 W, soit 112 dB **à 1 m** en demi-espace avec la sensibilité supposée — c'est le même point de fonctionnement que les 132 dB en champ proche ci-dessus), l'excursion crête du 18″ est de l'ordre de **7,8 mm** (5,5 mm en valeur RMS), si bien que la distance instantanée oscille de ±8 mm autour de la consigne. Pour que la distance **instantanée** reste sous $0{,}11a = 21{,}5$ mm, la consigne doit être d'environ 12 mm :

| | Limite Keele $0{,}11a$ | Excursion crête au niveau fort | Consigne retenue |
|---|---|---|---|
| Sub 18″ (1200 cm²) | 21,5 mm | ~8 mm à 40 Hz (ordre de grandeur) | **12 mm** |
| Médium 12″ (530 cm²) | 14,3 mm | faible (voie passe-haut) | **10 mm** |

<!-- Une relecture donnait 5,5 mm : c'est le déplacement RMS (u_RMS/omega). La grandeur qui limite la distance du micro est le déplacement CRÊTE, u_RMS*racine(2)/omega = 7,8 mm. Recalculé : p(1 m) = 7,96 Pa ; u_RMS = 1,38 m/s ; omega = 251,3 rad/s. -->
<!-- 12 mm et non 10 mm comme le proposait une relecture : la contrainte est que la distance INSTANTANÉE reste sous 0,11a, soit consigne <= 21,5 - 7,8 = 13,7 mm ; 12 mm garde la marge tout en laissant 4 mm de garde au débattement crête. Descendre à 10 mm réduirait cette garde sans bénéfice. -->

Contrôle de non-linéarité : refaire une mesure à 18 mm sur le sub — volontairement au-delà de la consigne, mais encore sous $0{,}11a$ au repos — et vérifier que l'écart reste < 0,3 dB sur 40–250 Hz ; sinon la distance est trop grande, ou le niveau trop fort. Vérifier visuellement l'absence de contact avant chaque balayage fort. Micro sur pied fixé au sol par ruban, repères sur le cache-noyau (sub, médium gauche, médium droit, évent le cas échéant), photos des positions, température de la pièce notée. En champ proche la position de l'enceinte dans la pièce n'importe pas ; on la laisse pourtant fixe.

**Règle de câblage — la plus importante de la section.** Dans un filtre passif parallèle du 2ᵉ ordre, les deux branches sont en parallèle sur la sortie de l'ampli : **elles se chargent mutuellement et forment ensemble la charge réelle**. Débrancher la voie médium pour mesurer le sub modifierait l'impédance vue par la branche passe-bas, donc sa fonction de transfert — erreur systématique, silencieuse, et portant exactement sur l'objet du TIPE. Donc : **toutes les branches du filtre et tous les haut-parleurs restent connectés en permanence ; entre deux mesures, on ne déplace que le micro.** Une mesure de contrôle chiffre l'effet (voie sub, niveau faible, branche médium déconnectée puis connectée) : c'est à la fois la justification de la règle et un résultat intéressant. En bi-amplification, les deux voies sont découplées par construction — une différence physique de plus à porter au débat passif / actif.

**Ordre d'une session** (une ligne = une mesure REW exportée) :

| Étape | Objet | Niveau | Répétitions |
|---|---|---|---|
| 0 | Calibrations REW (carte son en boucle, fichier micro), « Check levels » | — | 1 |
| 1 | Réponses brutes sans filtre : sub, médium G, médium D, évent | faible | 3 |
| 1b | Contrôle de cohérence : acoustique filtrée ?= brute × $\lvert H\rvert$ électrique (07.7) | faible | 1 |
| 1c | Contrôle de charge mutuelle : voie sub, branche médium déconnectée puis connectée | faible | 1 |
| 2 | Filtre catalogue : sub, médium G, médium D, évent | faible | 3 |
| 2b | **Conditionnement** : bruit rose au niveau fort, durée fixée [[à geler, ex. 5 min]] ; $R_e$ au multimètre avant et après | fort | 1 |
| 2c | Filtre catalogue, bobine chaude : balayage immédiat après 2b ; $R_e$ relevée à nouveau après | fort | 3 |
| 3 / 3b / 3c | Filtre optimisé : idem 2 / 2b / 2c | faible puis fort | 3 + 1 + 3 |
| 4 / 4b / 4c | Référence active : idem 2 / 2b / 2c | faible puis fort | 3 + 1 + 3 |
| 5 | Test de polarité (somme avec / sans inversion) sur le filtre catalogue | faible | 1 |
| 6 | Ordre inverse 4 → 2 pour détecter une dérive de session | faible | 1 |

**Dérive thermique (critère « robustesse »).** Un balayage de 256 k échantillons dure $262144/48000 = 5{,}46$ s. Au niveau **faible** (0,5 W), il injecte 2,7 J : moins de 1 K, la bobine ne chauffe pas. Au niveau **fort** en revanche, un balayage sinus est à amplitude constante et plus de 98 % de l'énergie électrique finit en chaleur dans $R_e$ (le rendement électroacoustique d'un 18″ est de quelques pour cent) : 5,5 s à 50 W, c'est **273 J**, soit un échauffement adiabatique de 11 K (bobine de 60 g) à 68 K (bobine de 10 g) [[masse de bobine à documenter]] — c'est-à-dire du même ordre que l'effet que l'on cherche à mesurer. **Le balayage fort fait donc lui-même dériver $Z(f)$.** D'où le protocole ci-dessus : chaque balayage fort est encadré par une mesure de $R_e$ avant et après, et l'écart fait partie du résultat.

Le cuivre suit $R_e(T) = R_e(T_0)\,[1 + \alpha\,(T - T_0)]$ avec $\alpha = 3{,}93\times10^{-3}$ K⁻¹ : +4 % pour +11 K, +8 % pour +20 K, +20 % pour +50 K, +39 % pour +100 K. Thermomètre : $\Delta T = (R_e/R_{e,0} - 1)/\alpha$. Trois précautions, sans quoi la mesure de $R_e$ ne vaut rien : mesure **quatre fils** (ou soustraction d'un court-circuit de cordons — la résistance des cordons est du même ordre que la dérive cherchée) ; chronomètre déclenché à l'arrêt du signal (le refroidissement se compte en secondes) ; trois lectures successives extrapolées à $t = 0$.

Un filtre passif voit cette dérive de $Z(f)$ ; la référence active ne la voit pas. **Mais il faut le dire avant de mesurer** : 50 W sur un 18″ professionnel, c'est quelques pour cent de sa puissance admissible, et la dérive attendue (+8 % sur $R_e$) peut produire sur le critère un écart plus petit que le seuil de répétabilité. On simule donc **avant la session**, avec le modèle T-S de la phase 2, l'écart RMS prédit pour $R_e$, $1{,}08\,R_e$ et $1{,}20\,R_e$ ; si l'écart prédit est sous le seuil de départage, on l'annonce et la mesure servira à poser une **borne supérieure**, pas à trancher.

**Lien DCR ↔ amortissement du grave — prédiction à écrire avant la mesure.** Le filtre passif ajoute en série la DCR de la self : la résistance de source vue par le haut-parleur augmente, son facteur de qualité total monte,
$$Q_{ts}' = Q_{ts}\left(1 + \frac{R_{DCR} + R_s}{R_e}\right),$$
soit +8 % pour 0,5 Ω et +17 % pour 1 Ω face à $R_e = 6$ Ω (ordres de grandeur). L'alignement basse-fréquence du grave change donc, et **le champ proche va le mesurer**. C'est calculable dès la phase 2 : il faut le prédire, sinon l'effet sera découvert dans les courbes et confondu avec un défaut de raccord. C'est aussi une différence passif / actif qui n'a rien à voir avec la fonction de transfert du filtre — CLAUDE.md classe ce point comme central pour la v2.

**Répétabilité et départage.** Trois répétitions par configuration ; on rapporte l'écart-type point à point sur la bande et l'écart-type du critère, $s = \sqrt{\frac{1}{n-1}\sum_i(\varepsilon_i - \bar\varepsilon)^2}$. Deux filtres ne sont départagés que si leurs critères **moyens** diffèrent de plus de
$$t_{0{,}975;\,2(n-1)}\;s\sqrt{\tfrac{2}{n}} \;\approx\; 2{,}3\,s \quad (n = 3),$$
car l'écart-type de la différence de deux moyennes de $n$ répétitions vaut $s\sqrt{2/n} = 0{,}816\,s$ et $t_{0{,}975;4} = 2{,}776$. La règle « $2s$ » serait légèrement trop permissive. De plus, $s$ estimé sur 3 répétitions est biaisé de −11 % (facteur $c_4 = 0{,}886$) : on l'annonce comme ordre de grandeur. Enfin l'incertitude-type sur un critère moyenné vaut $s/\sqrt3$, soit ~0,1 dB pour un $s$ de 0,2 dB : **tous les critères de cette section sont arrondis à 0,1 dB** (convention C4). En dessous du seuil, on écrit « non départagés » — et on le dit à l'oral.

### <a id="s07-9"></a>07.9 Critère « écart RMS à la cible en dB sur 40–250 Hz »

**Définition (à geler telle quelle).** Soit $L(f)$ le niveau (dB) de la somme des voies au point virtuel gelé, sur la bande $[f_1, f_2] = [40, 250]$ Hz. On **plafonne d'abord par le bas** :

$$\tilde L(f) = \max\!\big(L(f),\; L_{\max} - \Lambda\big),\qquad L_{\max} = \max_{[f_1,f_2]} L,\qquad \boxed{\Lambda = 20\ \text{dB}}$$

puis, avec un poids égal par octave (mesure $df/f$) :

$$\varepsilon_{RMS}^2 = \frac{1}{\ln(f_2/f_1)}\int_{f_1}^{f_2}\big(\tilde L(f) - L_0\big)^2\,\frac{df}{f},\qquad L_0 = \frac{1}{\ln(f_2/f_1)}\int_{f_1}^{f_2} \tilde L(f)\,\frac{df}{f}.$$

$L_0$ est la constante qui minimise $\varepsilon_{RMS}$ (moindres carrés) : le niveau absolu est libre, la forme seule est jugée. Discrétisation sur une grille logarithmique à 24 points par octave :

$$f_k = f_1\left(\frac{f_2}{f_1}\right)^{\frac{k-1}{N-1}},\quad N = \operatorname{round}\!\big(24\log_2(f_2/f_1)\big) + 1 = 64,\qquad \varepsilon_{RMS} = \sqrt{\frac{1}{N}\sum_{k=1}^{N}\big(\tilde L(f_k) - \bar{\tilde L}\big)^2}.$$

On rapporte aussi l'écart maximal $\max_k |\tilde L(f_k) - \bar{\tilde L}|$ (un trou étroit au raccord pèse peu dans un RMS).

**Pourquoi le plancher $\Lambda$ — et pourquoi il fait partie du critère gelé.** Quand une somme présente un **zéro de transmission** dans la bande (c'est exactement le cas du Butterworth non inversé, qui s'annule à 100 Hz), $L \to -\infty$ en ce point. L'intégrale continue, elle, reste finie — $(\ln|f - f_0|)^2$ est intégrable — et vaut 7,77 dB. Mais l'**estimateur discret** devient erratique : sa valeur ne dépend plus que de la distance entre 100 Hz et le point de grille le plus proche. Calculé sur la courbe analytique :

| Grille | sans plancher | avec plancher 20 dB |
|---|---|---|
| 12 pts/octave ($N = 33$) | **1027 dB** | 6,0 dB |
| 24 pts/octave ($N = 64$) | 7,3 dB | 5,9 dB |
| 48 pts/octave ($N = 128$) | 7,5 dB | 5,9 dB |
| 96 pts/octave ($N = 255$) | **375 dB** | 5,9 dB |
| 384 pts/octave ($N = 1016$) | 7,7 dB | 5,9 dB |
| intégrale continue | 7,77 dB | 5,93 dB |

Le 24 points/octave « marche » sans plancher **par coïncidence** : $\sqrt{40 \times 250} = 100{,}000$ Hz exactement, donc 100 Hz est le milieu géométrique de la bande et seul un $N$ pair l'évite ($N = 63 \to 749$ dB, $N = 64 \to 7{,}3$ dB, $N = 65 \to 738$ dB). Un critère gelé pour toute l'étude ne peut pas dépendre de la parité du nombre de points. Le plancher de 20 dB supprime le problème sans changer la nature du critère, et il est **physiquement fondé** : sur une mesure réelle, aucune annulation n'est infinie — elle est bornée par les tolérances des composants (±7 % sur $f_0$) et par le plancher de bruit. Le choix de $\Lambda$ n'est pas neutre (15 dB → 5,0 dB ; 20 dB → 5,9 dB ; 30 dB → 7,0 dB), d'où le gel. 20 dB parce qu'un creux de 20 dB est déjà disqualifiant : aller chercher plus profond n'ajoute rien à la décision. À vérifier en phase 0 : que le plancher de bruit effectif de la mesure soit bien à plus de 20 dB sous le niveau de bande, sinon le critère est déclaré « saturé » et on le dit.

<!-- Λ = 20 dB et non 30 dB (autre valeur proposée en relecture) : les deux stabilisent l'estimateur (30 dB donne 7,0 dB au lieu de 5,9 dB), mais 20 dB reste franchement au-dessus du plancher de bruit d'une mesure en champ proche ET franchement au-dessous de toute profondeur de creux qui aurait besoin d'être résolue pour trancher entre deux filtres. Le seul point qui compte est que la valeur soit gelée. -->

<!-- Les deux relecteurs donnaient des chiffres différents pour la sensibilité de grille (37/50 dB contre 375/1027 dB) : les deux sont reproductibles, l'écart vient de la source — courbe analytique (valeurs retenues ici) contre courbe interpolée depuis un fichier de 500 points, dont la résolution finie borne déjà la profondeur du creux. Ce désaccord illustre le défaut qu'on corrige : sans plancher, le chiffre dépend autant de la résolution du fichier que de la grille. -->
<!-- Non retenu : « le critère n'a pas de valeur limite quand N croît ». L'intégrale continue converge (log² est intégrable) et vaut 7,77 dB ; c'est l'estimateur discret qui est erratique aux N utilisables. La formulation retenue ci-dessus est la formulation exacte. -->

```python
def lire_rew_txt(chemin):
    """Lit un export texte REW (File > Export > Export measurement as text).
    Colonnes : Freq(Hz)  SPL(dB)  Phase(deg). Ne garde que les lignes commençant par
    un chiffre ou un signe (l'en-tête '*' ET une éventuelle ligne de titres de colonnes
    sont écartées). Convertit la virgule DÉCIMALE (entre deux chiffres) seulement :
    un fichier à séparateur virgule n'est donc pas corrompu silencieusement."""
    with open(chemin, encoding="utf-8", errors="replace") as fh:
        lignes = [re.sub(r'(?<=\d),(?=\d)', '.', l) for l in fh if re.match(r'\s*[-+.0-9]', l)]
    if not lignes:
        raise ValueError(f"{os.path.basename(chemin)} : aucune ligne de données reconnue")
    data = np.loadtxt(io.StringIO("".join(lignes)), ndmin=2)
    if data.shape[1] < 2:
        raise ValueError(f"{os.path.basename(chemin)} : {data.shape[1]} colonne(s), "
                         "2 au minimum attendues (séparateur décimal ? séparateur de colonnes ?)")
    f, L = data[:, 0], data[:, 1]
    phi = data[:, 2] if data.shape[1] > 2 else np.zeros_like(f)
    return f, L, phi


def ecart_rms(f, L, f1=40.0, f2=250.0, n_par_octave=24, cible=None, plancher=20.0):
    """Écart RMS (dB) de la courbe L(f) à la cible sur [f1, f2].
    Grille log à n_par_octave points par octave (poids égal par octave).
    plancher : on remplace L par max(L, max(L) - plancher) AVANT tout calcul. Sans lui,
    un zéro de transmission dans la bande rend l'estimateur discret erratique.
    cible=None : cible plate de niveau libre (le niveau moyen sur la bande est retiré :
    c'est la constante qui minimise l'écart RMS). Sinon cible = fonction f -> dB.
    Retourne (rms, ecart_max_abs, fk, ek)."""
    N = int(round(np.log2(f2/f1)*n_par_octave)) + 1
    fk = np.geomspace(f1, f2, N)
    Lk = np.interp(np.log(fk), np.log(f), L)          # interpolation en log f
    if plancher is not None:
        Lk = np.maximum(Lk, Lk.max() - plancher)
    ref = np.mean(Lk) if cible is None else cible(fk)
    ek = Lk - ref
    return float(np.sqrt(np.mean(ek**2))), float(np.max(np.abs(ek))), fk, ek


def somme_champ_proche(f, sources):
    """Somme complexe de N mesures en champ proche (même référence temporelle REW).
    sources : liste de dict {L, phi, a, d, sigma} —
      L, phi : SPL (dB) et phase (deg) mesurés au ras de la membrane ;
      a      : rayon effectif du HP (m), a = sqrt(Sd/pi) ;
      d      : distance du HP au point d'écoute virtuel (m) ;
      sigma  : +1 / -1 (polarité de câblage de la voie).
    Convention C2 : p(t) = Re{p e^{+j omega t}} ; un retard tau multiplie par e^{-j omega tau}.
    Keele : p_FF(d) = p_NF . a/(2d) en module, avec le retard e^{-j 2 pi f d/c} en plus.
    Retourne le niveau (dB) et la phase (deg) de la somme au point d'écoute virtuel."""
    p = np.zeros_like(np.asarray(f), dtype=complex)
    for s in sources:
        pi_ = 10**(np.asarray(s["L"])/20) * np.exp(1j*np.deg2rad(s["phi"]))
        pi_ = pi_ * (s["a"]/(2*s["d"])) * np.exp(-1j*2*np.pi*np.asarray(f)*s["d"]/c)
        p = p + s.get("sigma", 1)*pi_
    return 20*np.log10(np.abs(p) + 1e-300), np.rad2deg(np.angle(p))


def repetabilite(courbes, f, f1=40.0, f2=250.0):
    """courbes : liste de tableaux L(f) (dB) issus de n répétitions.
    Retourne (ecart-type moyen point à point sur la bande, critère moyen, ecart-type du critère,
    seuil de départage à 95 % entre deux configurations de n répétitions).
    s estimé sur n = 3 est biaisé de -11 % (facteur c4 = 0,886) : ordre de grandeur."""
    M = np.vstack(courbes)
    masque = (f >= f1) & (f <= f2)
    sigma_pt = np.std(M[:, masque], axis=0, ddof=1).mean()
    rms_i = [ecart_rms(f, Li, f1, f2)[0] for Li in courbes]
    n = len(courbes)
    t = {3: 2.776, 4: 2.447, 5: 2.306}.get(n, 2.0)     # t(0,975 ; 2(n-1))
    s = float(np.std(rms_i, ddof=1))
    return float(sigma_pt), float(np.mean(rms_i)), s, t*np.sqrt(2/n)*s
```

Sortie de `critere_rms.py` (données **synthétiques** : fonctions de transfert idéales, HP supposés plats, sans pièce) :

```
Grille du critère : 64 points de 40 à 250 Hz (24 points/octave, 2.644 octaves)
Plancher gelé : 20 dB sous le maximum de la bande.
Critère RMS 40-250 Hz sur des sommes IDÉALES (HP supposés plats, sans pièce) :
  Butterworth 2e ordre, une voie inversée      RMS =  0.60 dB ; écart max =  1.03 dB
  Butterworth 2e ordre, même polarité          RMS =  5.91 dB ; écart max = 14.33 dB
  Linkwitz-Riley 2e ordre, une voie inversée   RMS =  0.00 dB ; écart max =  0.00 dB
  1er ordre, même polarité                     RMS =  0.00 dB ; écart max =  0.00 dB
  Butterworth inversé, cible fixée à 0 dB (sans retrait du niveau moyen) : RMS = 2.29 dB

Pourquoi le plancher : cas « même polarité » (zéro de transmission exact à 100 Hz),
courbe ANALYTIQUE échantillonnée sur la grille du critère :
    12 pts/oct (N =    33) : sans plancher   1027.36 dB | avec plancher   6.01 dB
    24 pts/oct (N =    64) : sans plancher      7.26 dB | avec plancher   5.91 dB
    48 pts/oct (N =   128) : sans plancher      7.48 dB | avec plancher   5.92 dB
    96 pts/oct (N =   255) : sans plancher    374.58 dB | avec plancher   5.93 dB
   384 pts/oct (N =  1016) : sans plancher      7.72 dB | avec plancher   5.93 dB
  (l'intégrale continue vaut 7,77 dB sans plancher et 5,93 dB avec : le plancher ne change
   pas la nature du critère, il rend son estimateur discret stable.)

Lecture : 5000 et 5000 points ; ligne de titres sans '*' ignorée : True ; virgule décimale gérée : True
  fichier à séparateur virgule : refusé proprement -> could not convert string '10.0.100.0.0.0' to float64 at row 0, column 1.

Somme au point d'écoute virtuel (sub à 2,00 m ; les DEUX médiums à d2, sigma commun).
Démonstration : les deux voies sont volontairement égalisées (la pondération a_i/2d_i est
neutralisée sur la voie médium) pour isoler l'effet du trajet et de la polarité.
  d2 = 2.00 m, sigma_medium = -1 : RMS =  0.60 dB ; écart max =  1.03 dB ; creux à 100 Hz =   0.00 dB sous le maximum de bande
  d2 = 2.15 m, sigma_medium = -1 : RMS =  0.66 dB ; écart max =  1.41 dB ; creux à 100 Hz =   0.01 dB sous le maximum de bande
  d2 = 2.50 m, sigma_medium = -1 : RMS =  1.60 dB ; écart max =  3.23 dB ; creux à 100 Hz =   0.43 dB sous le maximum de bande
  d2 = 2.00 m, sigma_medium = +1 : RMS =  5.91 dB ; écart max = 14.33 dB ; creux à 100 Hz =  63.64 dB sous le maximum de bande
  (le « creux » du cas sigma = +1 est une annulation exacte : sa profondeur n'est bornée
   que par la résolution du fichier — sur une mesure réelle, par les tolérances et le bruit.)

Répétabilité (3 répétitions synthétiques, bruit 0,2 dB) : écart-type point à point = 0.17 dB ; critère RMS moyen = 0.60 dB (arrondi gelé : 0.6 dB) ; s = 0.011 dB
  seuil de départage à 95 % entre deux filtres (t x s x sqrt(2/n)) = 0.026 dB, soit 2.3 s
```

Dans cette démonstration, les deux voies sont **volontairement égalisées** (pondération $a_i/2d_i$ neutralisée sur la voie médium) pour isoler l'effet du trajet et de la polarité ; la pondération réelle n'entre qu'avec les mesures de la phase 4. Le « creux à 100 Hz » du dernier cas est une annulation **exacte** : sa profondeur de 63,6 dB n'est bornée que par la résolution du fichier synthétique, pas par la physique — d'où le plancher.

Quatre enseignements pour le gel des critères (phase 0) :

1. **Cible plate ⇒ le Butterworth catalogue est pénalisé de 0,6 dB par construction** (sa bosse de +3 dB), alors qu'un alignement Linkwitz-Riley ($Q = 0{,}5$) donne 0. Si la cible gelée est « somme plate », l'optimiseur de la phase 3 tendra vers $Q \approx 0{,}5$ et le catalogue est bien « à battre » ; si la cible est « Butterworth idéal », il faut le dire avant. Décision à écrire noir sur blanc.
2. **Retirer le niveau moyen n'est pas un choix cosmétique** : avec une cible fixée à 0 dB, le même Butterworth donne 2,3 dB au lieu de 0,6 dB. La définition retenue (niveau libre, forme jugée) doit figurer dans les critères gelés.
3. **Le point virtuel fait partie du critère** (0,6 → 1,6 dB entre 2,00 et 2,50 m sur la voie médium) : à geler et à garder identique pour les trois filtres.
4. **Le plancher $\Lambda$ fait partie du critère** au même titre que la bande, la grille et la cible.

**Quelle cible, au juste ?** Les réponses brutes des haut-parleurs ne sont pas plates sur 40–250 Hz (coupure basse du sub en caisse [[à mesurer en phase 1]]). Si cette non-planéité domine le critère, elle noie ce qu'on veut mesurer. Deux solutions, à trancher en phase 0 :

- relever la borne basse de la bande **après la phase 1 et avant toute mesure comparative** (conforme à la règle « critères gelés avant les mesures comparatives ») ;
- ou, mieux, définir la cible non comme une droite plate mais comme **la somme idéale des réponses brutes mesurées à l'étape 1, pondérées par un passe-bas et un passe-haut idéaux**. L'argument `cible` d'`ecart_rms` le permet sans une ligne de code supplémentaire. Le critère juge alors le **filtre** et non les haut-parleurs, et la question de la borne basse disparaît.

**Barre d'erreur du côté conception.** La répétabilité (07.8) ne couvre que la mesure. Les tolérances $L$ ±10 % et $C$ ±10–20 % donnent $u(f_0)/f_0 \approx 7$ % : le filtre « catalogue » réellement bobiné n'est pas à 96,9 Hz mais quelque part dans $96{,}9 \pm 7$ Hz. Il faut afficher cette barre-là aussi, sinon un écart de 0,2 dB entre deux filtres pourra provenir uniquement de la tolérance des composants. Pratique : mesurer $L$ et $C$ des exemplaires réellement montés (07.7) et recalculer le critère prédit avec ces valeurs-là, pas avec le nominal.

**Seuil d'acceptation — ce que « le filtre optimisé gagne » veut dire.** La phase 0 doit geler non seulement *comment* on mesure, mais *quelle valeur constitue un succès*. Proposition à valider par l'étudiant [[à geler]] :

| Critère | Succès déclaré si… |
|---|---|
| Fidélité du raccord | $\varepsilon_{RMS}(\text{optimisé}) < \varepsilon_{RMS}(\text{catalogue}) - \max(2{,}3\,s\;;\;0{,}5\ \text{dB})$ |
| Précision de $f_c$ | $\lvert f_0^{\text{mes}} - 100\ \text{Hz}\rvert \le 5\,\%$ de $f_0$ **calculée avec les L et C mesurés** (07.7) |
| Robustesse | $\lvert\varepsilon_{RMS}(\text{fort}) - \varepsilon_{RMS}(\text{faible})\rvert$ rapporté avec son seuil ; si l'écart est sous $2{,}3\,s$, on conclut « non départagé », pas « pas de dérive » |

La référence active sert de **borne** (ce que ferait un filtre qui ne voit jamais $Z(f)$), pas de concurrent : un passif qui s'en approche à moins de $2{,}3\,s$ est un succès complet.

### <a id="s07-10"></a>07.10 REW en pratique

- **Matériel et câblage exact** : micro de mesure XLR (alimentation fantôme) sur l'**entrée 1** d'une interface à deux entrées ; **sortie gauche → ampli** ; **sortie droite → entrée 2** (boucle de retour). Le micro et la boucle doivent être sur **la même interface** : l'aide REW n'autorise les balayages multiples qu'en l'absence de référence temporelle **ou** avec boucle de retour, et les interdit si entrée et sortie sont sur des appareils différents. **Un micro USB est donc exclu de tout ce protocole** — à dire au moment de documenter le modèle de carte son [[à documenter]].
- **Preferences > Soundcard** : 48 kHz ; « Calibrate soundcard » avec la boucle (compense la réponse de la carte, à faire une fois, fichier sauvegardé) ; référence temporelle « Use loopback as timing reference » — indispensable pour comparer les phases de deux mesures (sommation 07.4, évent 07.3, polarité 07.5).
- **Preferences > Mic/Meter** : charger systématiquement le fichier de calibration du micro. S'il n'existe pas [[à vérifier]] : la réponse basse-fréquence du micro entre **à l'identique** dans les trois valeurs du critère et se simplifie donc dans la comparaison ; elle ne se simplifie pas si l'on veut lire le critère comme une qualité absolue — ce qu'on s'interdit (07.3). Ne pas affirmer « les micros de mesure sont plats à ±0,5 dB » : à 40 Hz, sur une capsule d'entrée de gamme, l'écart dépasse souvent ±1 dB et certaines sont filtrées vers 20–30 Hz.
- **Measure — deux jeux de réglages distincts** (voir 07.11) : REW balaie en réalité **de la moitié du Start au double du End**.
  - *Niveau faible* : Start 10 Hz (le contenu descend donc à 5 Hz — c'est justement ce qu'on veut pour caractériser le comportement sous l'accord), End 1 kHz. **Uniquement au niveau faible**, et en surveillant visuellement le débattement au premier balayage de chaque session.
  - *Niveau fort* : **Start $\ge 2f_B$** ($f_B$ = fréquence d'accord de l'évent, mesurée en phase 1 par le double pic d'impédance [[à mesurer]]), pour que le contenu réel reste au-dessus de $f_B$ ; en caisse close, Start $\ge 2 f_c(\text{caisse})$. À défaut, passe-haut de protection en amont de l'ampli.
  - Commun : Length 256 k (5,46 s à 48 kHz ; chaque doublement gagne ~3 dB de rapport signal/bruit) ; Level −12 dBFS par défaut (ce niveau est **numérique** : la tension aux bornes se **mesure** au multimètre, 07.8) ; « Check levels » avant chaque session ; Repetitions 2 à 4 (pré-moyennage synchrone, autorisé car entrée et sortie sont sur la même carte).
- **Distorsion** : exporter la **THD** de chaque balayage (REW la fournit dans le même balayage). Sans elle, un écart entre niveau faible et niveau fort ne peut pas être attribué à la dérive thermique plutôt qu'à la non-linéarité de la suspension, de $Bl(x)$ ou à la turbulence de l'évent. Seuil de rejet d'une mesure « fort » [[à geler en phase 0]].
- **Moyennage des répétitions** : All SPL > « Vector average » (module et phase, mesures avec référence temporelle) ; « RMS average » ignore la phase. Lissage : aucun (ou 1/48) pour l'export ; le lissage 1/12 n'est qu'un confort d'affichage.
- **Export** : File > Export > « Export measurement as text » : lignes d'en-tête commençant par `*`, puis trois colonnes fréquence / SPL (dB) / phase (°) ; point décimal par défaut (ne pas cocher « Use computer's number format » — le lecteur Python tolère la virgule décimale, mais **pas** un fichier où la virgule sert de séparateur de colonnes : il le refuse alors explicitement). Plage exportée 10–1000 Hz, résolution logarithmique (96 points/octave). Nommage : `AAAA-MM-JJ_filtre_voie_niveau_repN.txt`. Export optionnel de la réponse impulsionnelle en WAV pour archivage.
- REW propose aussi une arithmétique de traces (A + B, A − B) ; on préfère Python pour garder la trace exacte du calcul (pondérations $a_i/2d_i$, retards, polarités).

### <a id="s07-11"></a>07.11 Sécurité

- **Oreilles** : en champ proche, **112 dB SPL dès le niveau faible gelé** (0,5 W), 125 dB à 10 W et 132 dB à 50 W (sensibilité 95 dB/2,83 V/m supposée). Bouchons obligatoires **y compris au niveau faible**, personne dans l'axe pendant les balayages forts, balayages courts, pas de tête à moins de 1 m du 18″.
- **Micro** : SPL maximal de la capsule [[à vérifier]] ; réduire le gain d'entrée avant le niveau fort ; surveiller l'écrêtage dans « Check levels » ; bonnette au champ proche de l'évent (jet d'air, 07.3).
- **Haut-parleurs** : médiums jamais en pleine bande au niveau fort sans passe-haut (leur réponse brute se mesure au niveau faible seulement). **Le sub est bass-reflex à deux évents** (§ 01.10) : le seuil pertinent n'est **pas** 20 Hz mais la fréquence d'accord $f_b$, car sous $f_b$ la membrane n'est plus chargée par le ressort d'air et le débattement croît sans butée. Chiffré sur le modèle du § 02.6 : $\times1{,}8$ à $f_b/2$ et $\times2{,}3$ à 10 Hz par rapport à $f_b$, soit **20 mm crête à 52,9 V et 10 Hz** — au-delà du $X_{max}$ de tout 18″. Règle : **au niveau fort, aucun contenu sous l'accord — Start REW $\ge 2f_b$** (07.10), jamais de pleine puissance, et vérification visuelle du débattement avant chaque balayage fort. La règle complète, avec la distinction petit signal / fort signal, est au § 02.6 (« Borne basse du balayage ») : **la mesure d'impédance à 150 mV, elle, descend librement à 10 Hz et le doit** — c'est là que se trouve le pic bas $f_L$.
  - **Et les pavillons.** Deux haut-parleurs d'ultra-aigu sont câblés en parallèle des médiums (§ 02.6). S'il n'y a **pas** de condensateur en série avec eux [[à vérifier]], ils reçoivent le 100 Hz à pleine puissance pendant les balayages de la voie médium : hors de leur bande, avec une excursion que leur suspension n'est pas faite pour encaisser. **Vérifier la présence du condensateur avant le premier balayage au niveau fort** ; à défaut, limiter durée et niveau, et surveiller l'odeur de colle chaude.
- **Limiteur du E-800** : il reste enclenché comme filet de sécurité (le manuel le décrit comme limiteur à 5 % de distorsion), **mais un limiteur qui agit rend la chaîne non linéaire et invalide la mesure de fonction de transfert par balayage**. Toute mesure pendant laquelle la LED limit/clip s'allume est écartée et refaite à niveau réduit ; l'état de la LED est consigné pour chaque balayage. Idéalement, régler le niveau « fort » 3 dB sous le seuil d'action constaté.
- **Électricité — le dimensionnement des composants ne se fait pas sur la tension de l'ampli.** À pleine puissance sur 8 Ω : 52,9 V RMS, 74,8 V crête. Mais le réseau LC **surtensionne** : le composant shunt (le condensateur du passe-bas, la self du passe-haut) voit la tension de charge, amplifiée d'un facteur $Q \approx \lvert Z\rvert\sqrt{C/L}$ (en assimilant la charge à une résistance égale à $\lvert Z\rvert$) qui croît avec l'impédance réelle du haut-parleur — or $\lvert Z\rvert$ atteint 40 à 60 Ω au pic de résonance, c'est-à-dire justement vers 95–100 Hz si $F_c$(caisse) y tombe. Maximum sur 20–300 Hz, calculé sur 18 mH / 150 µF :

| $\lvert Z\rvert$ de la charge | $\lvert V\rvert$ du composant **shunt** / $V_{\text{in}}$ | $\lvert V\rvert$ du composant **série** / $V_{\text{in}}$ |
|---|---|---|
| 8 Ω (résistif) | 1,00 (à 24 Hz) | 1,29 |
| 14 Ω | 1,39 (à 81 Hz) | 1,68 |
| 30 Ω | 2,79 (à 94 Hz) | 2,95 |
| 50 Ω | 4,59 (à 96 Hz) | 4,70 |
| 60 Ω | 5,50 (à 96 Hz) | 5,59 |

  Au niveau « fort » de 20 V RMS et sur $\lvert Z\rvert = 50$ Ω, cela fait **92 V RMS, soit 130 V crête** aux bornes d'un composant. Règle : tension de service = $V_{\text{ampli}} \times$ facteur de surtension calculé sur la $Z(f)$ **mesurée en phase 1** ; tant que $Z(f)$ n'est pas connue, prendre une marge $\times 6$ → condensateurs film spécifiés au moins **250 V DC / 160 V AC**, et vérifier que la spécification lue est bien la tension **alternative permanente** (sur un MKP, un « 100 V » est presque toujours une tension continue ; la tenue en alternatif permanent est typiquement de 60 à 65 V RMS). Ce point mérite mieux qu'une ligne de sécurité : **la surtension $Q \approx \lvert Z\rvert\sqrt{C/L}$ est la traduction la plus parlante de « le catalogue 8 Ω ne décrit pas la charge réelle »** — c'est un résultat de l'exposé.
- **Autres précautions électriques** : résistance de puissance chaude ; décharger les condensateurs avant de toucher ; ne jamais court-circuiter une sortie ; interrupteur ground/lift en position ground ; masses d'oscilloscope **et de carte son** vérifiées (07.7) ; **jamais en mode pont**.
- **Ordre des amplitudes** : toujours du faible vers le fort, et toujours le test sur résistance 8 Ω avant le HP.

### Ce qu'il faut retenir pour l'oral

- À 100 Hz, $\lambda = 3{,}4$ m : une pièce de classe a 33 modes sous 150 Hz et une fenêtre temporelle ne peut donner que $\Delta f = 1/T \approx 280$ Hz de résolution ; on ne mesure donc pas à 1 m, on mesure au ras de la membrane (Keele 1974), valable jusqu'à $f \approx c/(\pi d) \approx 280$ Hz pour un 18″ — limite « molle » que l'on **vérifie** par une mesure sur plan de sol plutôt que de l'affirmer.
- La somme des deux voies est **calculée** à partir des champs proches (phases conservées par la boucle de retour REW, pondération $a/2d$, retard $e^{-j2\pi f d/c}$, polarité) ; à 100 Hz, ±10 cm sur les positions ne coûtent que 0,04 dB.
- **Le sub est bass-reflex à deux évents : la voie grave n'est pas une source, c'est trois.** On relève la membrane et chaque évent, puis on somme en complexe avec la pondération de Keele $\underline p_\Sigma=\underline p_D+\sum_i\sqrt{S_{P,i}/S_D}\,\underline p_{P,i}$. Avec $N$ évents identiques le poids est $N\sqrt{S_P/S_D}$ et **non** $\sqrt{N S_P/S_D}$ : mettre l'aire totale sous la racine coûte exactement $20\log\sqrt N$, soit 3,01 dB pour deux évents. Aucune inversion de signe à la main — la phase physique est déjà dans les relevés ; le contrôle est la chute à 24 dB/oct sous $f_b$ et le minimum de la membrane à $f_b$, qui est l'exact pendant acoustique du creux d'impédance. Coût : trois relevés au lieu d'un, soit 2 à 3 h sur la campagne.
- Le critère est un écart RMS en dB sur 40–250 Hz, grille logarithmique de 64 points, niveau moyen retiré, **plancher à 20 dB sous le maximum** ; sur des courbes idéales il vaut 0,6 dB pour Butterworth inversé, 0 pour Linkwitz-Riley, 5,9 dB sans inversion (critère saturé au plancher — sans ce plancher, le chiffre varie de 7 à 1000 dB selon la grille). Cible, point virtuel, plancher et seuil d'acceptation sont gelés avant les mesures.
- $f_c$ désigne **le croisement des deux voies** (définition unique, § 04.1) ; le **pôle** $f_0 = 1/(2\pi\sqrt{LC}) = 96{,}9$ Hz et les **−3 dB** (99,9 Hz au passe-bas, 93,9 Hz au passe-haut, seuil mi-puissance $-3{,}0103$ dB) sont des repères différents, à nommer comme tels. La tolérance des composants place $f_0$ à **7,1 % en borne au pire cas / 4,1 % en incertitude-type** ($\frac12\sqrt{(u_L/L)^2+(u_C/C)^2}$, le facteur $\frac12$ étant la signature du LC).
- Les niveaux « faible » et « fort » sont définis par une tension RMS **aux bornes du haut-parleur**, mesurée. La robustesse se mesure bobine chaude après conditionnement (cuivre : +20 % de $R_e$ pour +50 K) — et le balayage fort lui-même chauffe (273 J en 5,5 s à 50 W), d'où un $R_e$ relevé avant et après chaque balayage.
- Sur la charge réelle, le LC surtensionne : jusqu'à ×5,5 sur un pic d'impédance de 60 Ω. C'est la démonstration la plus directe que le calcul « 8 Ω » ne décrit pas l'enceinte.
- Trois répétitions, écart-type rapporté, tout arrondi à 0,1 dB ; deux filtres à moins de $2{,}3\,s$ ne sont pas départagés, et on le dit.

### Sources

- Keele, D. B., Jr., « Low-Frequency Loudspeaker Assessment by Nearfield Sound-Pressure Measurement », *J. Audio Eng. Soc.*, vol. 22, n° 3, p. 154–162, avril 1974 — https://www.aes.org/e-lib/browse.cfm?elib=2774
- D'Appolito, J., « Measuring Loudspeaker Low-Frequency Response », *audioXpress*, juin 2012 (republié le 14 novembre 2018) — https://audioxpress.com/article/measuring-loudspeaker-low-frequency-response — règle $0{,}11\,a$ (erreur < 1 dB) et pondération de l'évent. Note : sa forme $f_{\max} = 4311/D$ (Hz, $D$ en pouces) est identique à $c/(\pi d)$ **à condition d'y mettre le diamètre effectif** $d = 2\sqrt{S_d/\pi}$ — 15,4″ pour un 18″ de 1200 cm², soit 280 Hz, contre 239 Hz si l'on y met le diamètre nominal. D'Appolito attribue de plus ce plafond au début de rupture du cône, et non à $ka = 1$ : deux justifications physiques différentes qui tombent numériquement au même endroit.
- **Pondération de sommation membrane + évents, $N$ évents** (§ 07.3) : le résultat $\underline p_\Sigma=\underline p_D+\sum_i\sqrt{S_{P,i}/S_D}\,\underline p_{P,i}$ est une conséquence directe de la relation de Keele ci-dessus ($p_{FF}\propto\sqrt S\,p_{NF}$), redémontrée ici en trois lignes depuis $\lvert p_{NF}\rvert=\rho\omega u a$ et $U=Su$, puis **revérifiée numériquement** sur un cas jouet (`keele.py`, écart $10^{-16}$). Keele (1974) la donne pour **un** évent ; D'Appolito (2012) la reprend sous la forme « pondérer par le rapport des diamètres ». **Aucune des deux sources n'explicite le cas $N>1$**, où le poids est $N\sqrt{S_P/S_D}$ et non $\sqrt{N S_P/S_D}$ (écart $20\log\sqrt N$, soit 3,01 dB pour deux évents) : c'est pourquoi la démonstration est écrite au § 07.3 plutôt que citée. [[à recouper sur le texte intégral de Keele 1974 si le jury demande une source pour le cas à deux évents — article AES payant, à demander au CDI]]
- Gander, M. R., « Ground-Plane Acoustic Measurement of Loudspeaker Systems », *J. Audio Eng. Soc.*, vol. 30, n° 10, p. 723–731, octobre 1982 (correction *JAES* vol. 34, n° 1/2, 1986).
- Linkwitz, S. H., « Active Crossover Networks for Noncoincident Drivers », *J. Audio Eng. Soc.*, vol. 24, n° 1, p. 2–8, février 1976.
- Olson, H. F., « Direct Radiator Loudspeaker Enclosures », *J. Audio Eng. Soc.*, vol. 17, n° 1, 1969 (diffraction du coffret) [[à vérifier]].
- Kuttruff, H., *Room Acoustics*, CRC Press (modes propres, fréquence de Schroeder) [[édition à préciser]].
- Beranek, L. L., Mellow, T., *Acoustics: Sound Fields and Transducers*, Academic Press, 2012 (rayonnement du piston bafflé).
- REW (J. Mulcahy), aide en ligne : « Making Measurements » https://www.roomeqwizard.com/help/help_en-GB/html/makingmeasurements.html ; « File Menu » (export texte) https://www.roomeqwizard.com/help/help_en-GB/html/file.html ; « All SPL Graph » (moyennages) https://www.roomeqwizard.com/help/help_en-GB/html/graph_allspl.html ; « Getting set up for measuring » https://www.roomeqwizard.com/help/help_en-GB/html/calsoundcard.html
- Thomann, *the t.amp E-400/E-800/E-1200/E-1500 Power Amplifier User Manual* (modes, sensibilité 0,77 V / 26 dB / 1,4 V, classe H, limiteur, ground/lift) — https://images.thomann.de/pics/prod/173889_manual.pdf
- Coefficient de température du cuivre $\alpha = 3{,}93\times10^{-3}$ K⁻¹ : valeur tabulée usuelle (CRC Handbook).
- Scripts exécutés : `scratchpad/sec07v/calc_sec07.py` et `scratchpad/sec07v/critere_rms.py` (Python 3.13, numpy seul par choix de portabilité — l'environnement du poste, vérifié le 2026-09-13, comporte Python 3.13.2, numpy 2.4.6, scipy 1.18.1, matplotlib 3.11.0).

## <a id="s08"></a>08. Cadre du TIPE (SCEI, session 2027) et attentes du jury

> Section vérifiée le **2026-09-03** sur les sources officielles (scei-concours.fr, Bulletin officiel de l'ESR) ; contrôles numériques et audit du dépôt refaits le **2026-09-09**. Convention : ce qui est écrit sans marque a été lu dans une source citée en fin de section ; ce qui n'a pas pu l'être porte la marque **[[à vérifier]]**. Au 2026-09-03, la page TIPE du SCEI affiche encore « INFORMATIONS SESSION 2026 », et les *Attendus pédagogiques 2026-2027* n'ont **pas été trouvés aux URL testées** — le nommage des fichiers change chaque année (`AttendusPedagogiques_2023.pdf`, `2024_Attendus_Pedagogiques_Final.pdf`, `2025_Attendus_Pedagogiques.pdf`, `TIPE_2026_Attendus_Pedagogiques.pdf`), donc l'absence d'un fichier deviné ne prouve rien. **Seule la page https://www.scei-concours.fr/tipe.html fait foi ; la consulter à la rentrée.** En attendant, tout ce qui concerne la session 2027 est déduit de la session 2026 et devra être reconfirmé (le rapport 2021 indique que les Attendus sont « publiés annuellement au tout début de chaque année scolaire » ; l'édition 2026 est datée du 21 novembre 2025, l'édition 2025 du 17 septembre 2024).

<!-- Correction retenue (vérificateur « terrain ») : l'inférence « 404 sur une URL devinée donc document non publié » n'était pas valide ; remplacée par « non trouvé aux URL testées ». Même correction appliquée à la source n° 5. -->

### <a id="s08-1"></a>08.1 Le thème 2026-2027 : source officielle

Le thème est fixé par **l'arrêté du 9 janvier 2026 (NOR : ESRS2600935A)**, publié au **Bulletin officiel de l'enseignement supérieur et de la recherche n° 5 du 29 janvier 2026**. Article 1 : le thème des TIPE « dans les classes préparatoires de seconde année [...] des voies MP, MPI, PC, PSI, PT, TSI, TPC, BCPST, TB est fixé pour l'année scolaire 2026-2027 conformément à l'annexe ». Annexe, point 2 : « Pour l'année 2026-2027, le thème Tipe commun aux filières MP, MPI, PC, PSI, PT, TSI, TPC, BCPST et TB est intitulé : **Sobriété, efficacité, optimisation**. » L'arrêté abroge celui du 17 mars 2025 (thème 2025-2026 : « Cycles, boucles », celui qu'affiche encore la page SCEI de la session 2026).

L'annexe de l'arrêté dit aussi ce que le jury attend, et c'est directement exploitable pour le sujet v2 :

| Annexe de l'arrêté (formulation officielle) | Ce que cela impose au sujet v2 |
|---|---|
| « dégager une problématique en relation explicite avec le thème proposé » | L'ancrage n'est pas décoratif : les trois mots du thème doivent être reliés à des grandeurs (voir 08.5). |
| investigation par « observations, réalisation pratique d'expériences, modélisations, formulation d'hypothèses, simulations, **validation ou invalidation de modèles par comparaison au réel** » | C'est le récit en 4 actes (mesurer → identifier → optimiser → valider). Le sanity check 8 Ω et la validation au banc sont exactement des « validations de modèle ». |
| « découvrir par lui-même, **sans ambition excessive** » | Périmètre à tenir : ordre 2, une fréquence de raccord, deux dipôles mesurés. Les satellites (self, énergie) restent en annexe. |
| la production « ne peut en aucun cas se limiter à une simple synthèse d'informations collectées, mais doit faire ressortir une **"valeur ajoutée"** apportée par le candidat » | Le filtre « catalogue » est la synthèse ; la valeur ajoutée est l'optimisation sur Z(f) mesurée. C'est la réponse officielle à la crainte « sujet recette ». |
| travaux « en petits groupes d'au maximum trois étudiants [...] ou de façon individuelle » | Thomas travaille seul : pas de déclaration de groupe à l'étape 1. |
| compétences : « identifier, s'approprier et traiter une problématique explicitement reliée au thème ; collecter des informations pertinentes [...] ; réaliser une production ou une expérimentation personnelle et en exploiter les résultats ; **construire et valider une modélisation** ; communiquer » | Le fit Thiele-Small (problème inverse) est la « modélisation construite et validée » ; la bibliographie commentée du MCOT couvre « collecter, analyser, synthétiser ». |

### <a id="s08-2"></a>08.2 Format de l'épreuve orale (règlement session 2026, à reconfirmer pour 2027)

L'épreuve commune est organisée par le **Concours Centrale-Supélec**, le **Concours Commun INP**, le **Concours Commun Mines-Ponts** et la **Banque filière PT**. D'autres concours (e3a-Polytech, etc.) en reprennent les résultats **[[à vérifier]]**. Pour un élève issu de PTSI, la Banque PT comme les concours de la filière PSI utilisent cette épreuve.

<!-- Correction retenue : « le réseau Polytech » était présenté comme organisateur sans source ; ramené à quatre organisateurs vérifiés, le reste marqué [[à vérifier]]. -->

| Élément | Règle (SCEI, session 2026) |
|---|---|
| Durée totale | **30 minutes** en deux parties |
| Exposé | **15 minutes** de « présentation par le candidat de son travail de l'année » |
| Entretien | **15 minutes** d'« échange avec le binôme d'examinateurs » |
| Jury | Deux examinateurs, constitués en binôme par un algorithme d'appariement à partir des 24 positionnements thématiques (bilan 2019 : couplage optimal + affectation des candidats par « mariages stables »). Le bilan 2019 précise : « examinateurs compétents mais volontairement non choisis pour leur niveau d'expertise dans un domaine donné » — pas de présentation d'expert à expert. |
| Support — **règles** | Diapositives « projetées en **format 4/3 paysage** » ; PDF de **5 Mo maximum** ; ni vidéo, ni audio, ni animation ; la présentation « doit illustrer le discours du candidat et être **focalisée sur les aspects scientifiques du projet** » ; **la numérotation de toutes les diapositives est requise**. |
| Support — **recommandations** | Pas de limite de pages ni de mots, mais « il est conseillé de ne pas mettre trop de texte (**au grand maximum 10 lignes par diapositive**) », d'éviter les phrases, d'adjoindre une iconographie référencée. « En première page, il est **fortement recommandé** aux candidats de placer leur Nom, Prénom et numéro d'inscription. » |
| En salle | La présentation téléversée est « projetée et calée sur la première diapositive », pilotée « via le clavier d'un ordinateur résident ». Aucun support numérique personnel (clé USB, disque, cloud) ; pointeur laser personnel de classe 1 ou 2 toléré. |
| Documents papier | Autorisés (« photos, cahier de laboratoire, ... ») ; les examinateurs « ne sont en aucun cas tenus de les prendre en compte ». |
| Programmes | Citation littérale : « **Si le candidat a développé des programmes informatiques, il devra apporter en double exemplaire les listings correspondants sur support papier. Ces listings seront également inclus en documents annexes à la présentation (en aval de la conclusion) mais ne seront pas présentés formellement durant l'exposé du candidat. Ils pourront faire l'objet de questions spécifiques lors de la phase d'échange avec les examinateurs. Il est fortement recommandé d'afficher ces listings sur fond blanc pour être plus lisibles.** » Commentaire propre au projet : le TIPE v2 développe du code Python (`analyse/`), donc cette obligation s'applique. |
| Interdits | Présentation « de tout produit et de tout objet » ; calculatrice, ordinateur, téléphone, montre connectée. |
| Évaluation | « L'évaluation finale tient également compte de la présentation, de l'échange avec les examinateurs ainsi que des éléments saisis en ligne durant les différentes étapes » (MCOT, DOT). |

<!-- Corrections retenues : (a) « nom, prénom, n° d'inscription » était donné comme règle — c'est une recommandation forte, séparée ici de la numérotation qui, elle, est requise ; (b) la citation sur les listings contenait le mot « obligatoirement », absent du texte officiel : citation littérale rétablie. -->

Conséquences pratiques pour ce projet :

- **Le fichier HTML reveal.js ne sera jamais utilisé en salle** : seul le PDF téléversé compte. Les notes du présentateur (`<aside class="notes">`) n'existent pas sur l'ordinateur résident — les imprimer et les apporter comme document papier.
- **Le gabarit actuel est 16:9 alors que le SCEI projette en 4/3.** Un PDF 16:9 ajusté en largeur sur un écran 4/3 occupe $(9/16)/(3/4) = 0{,}75$ de la hauteur, soit **exactement 25 % de hauteur utile perdue**. Emplacements exacts à corriger (relevés dans le dépôt) : `pre-soutenance.html` l. 784 et `presentation-finale.html` l. 1206 (`width: 1280, height: 720`), `EXPORT-PDF.md` l. 22 et 23 (`-s 1280x720`) et l. 37 (repli bitmap, « window 1280×720 »). Gabarit de remplacement : **1024×768**.
  **Quand trancher : en phase 0, pas en phase 5.** Toutes les figures des phases 2 à 4 (module et phase de $Z(f)$, résidus du fit, Bode, comparatifs) seront produites avant la refonte des slides ; il faut donc figer dès le squelette `analyse/` le format de sortie matplotlib (taille en pouces et dpi cohérents avec une zone utile 4/3), sinon chaque figure sera à refaire.
- **Taille du PDF.** Les PDF v1 pèsent 1 877 821 à 3 006 617 octets, soit **1,88 à 3,01 Mo** ($10^6$ o) ou 1,79 à 2,87 Mio ($2^{20}$ o) — la convention n'était pas déclarée dans le brouillon, et celle du plafond « 5 Mo » ne l'est pas non plus côté SCEI. En lecture conservatrice (5 Mo $= 5\times10^6$ o), la **marge restante est de 1,99 Mo**, soit 66 % de la taille du plus gros PDF actuel. Règle d'export associée (voir le budget chiffré en 08.7) : figures en vectoriel (PDF/SVG) et non en PNG ; photos ré-encodées en JPEG à ≤ 200 ko l'unité ; contrôle de la taille à **chaque** export, pas seulement au dernier.
- Le code Python `analyse/` doit être **imprimé en double exemplaire et annexé après la conclusion** du PDF. La variante claire `blueprint-light.css` est la bonne base (fond blanc recommandé). Ordre de grandeur de mise en page, calculé pour une vue 1024×768 avec 40 px de marge : **≈ 42 lignes × 131 colonnes** en police monospace 12 px, ≈ 36 × 112 en 14 px, ≈ 31 × 98 en 16 px. En retenant ~33 lignes utiles par vue (en-tête et respiration comprises), 250 lignes de code occupent **8 vues d'annexe**. Ces vues sont hors des 15 minutes ; en poids elles sont du texte vectoriel, donc négligeables devant les images [[à vérifier à l'export]].
- **L'enceinte, le filtre bobiné, la self : objets interdits en salle.** Conséquence de terrain, à inscrire dans les phases 1 et 4 : **photographier le jig d'impédance, le bobinage en cours et le filtre monté AVANT tout démontage ou remontage**, et tenir le cahier de laboratoire daté dès la première mesure. Ce cahier est à la fois la matière première du DOT et le seul document papier réellement admis en salle.
- Les Attendus recommandent de **ne pas mentionner le nom du lycée** (« cette précision n'amène rien ») et de mentionner sa spécialité le cas échéant. La consigne officielle vise le **nom du lycée** ; rien n'y concerne le nom d'un enseignant, et le professeur encadrant est de toute façon déclaré au SCEI. Par prudence, on peut neutraliser aussi le nom de l'enseignant cité dans les sources v1 (`pre-soutenance.html` l. 753, « N. Cavallo, Cours de physique — PTSI ») en « cours de physique de PTSI » : c'est une **interprétation**, non une exigence.

<!-- Correction retenue : le brouillon écrivait « l'enseignante » — le genre n'est pas établi par la source ; et il présentait l'extension de la consigne comme la consigne elle-même. -->

Conseil non officiel mais répandu (document de lycée, MPI Faidherbe) : structurer les 15 min en 1 min d'introduction, 13 min de développement, 1 min de conclusion.

### <a id="s08-3"></a>08.3 Les livrables : titre, MCOT et DOT

**Étape 1 — Titre et MCOT.** Saisie en ligne (« SCEI > Mon dossier > TIPE ») de : titre ; **déclaration du professeur encadrant** ; **motivation du choix de l'étude (au maximum 50 mots)** ; **ancrage au thème de l'année (au maximum 50 mots)** ; MCOT en cinq parties saisies dans cet ordre :

| Partie du MCOT | Limite officielle | Règles (Attendus 2026) |
|---|---|---|
| 1. Positionnements thématiques et mots-clés | 1 à 3 positionnements parmi **24 thèmes** ; **5 mots-clés français + 5 anglais** | Par ordre d'importance décroissante. « Le premier positionnement thématique doit impérativement se situer dans un des domaines de rattachement disciplinaire de la filière » : **Physique et Sciences industrielles pour PSI et PT**. Le premier positionnement « a une importance majeure » (il détermine le binôme d'examinateurs) ; ne pas déclarer « Informatique » en 3e position « pour avoir utilisé un programme de tracé de courbes ». |
| 2. Bibliographie commentée | **650 mots max** | Synthèse du contexte scientifique avec « renvois numérotés progressifs » vers la liste de références. Vise « un premier niveau d'appropriation ». |
| 3. Problématique retenue | **50 mots max** | « questionnement scientifique (phénomène à étudier, propriété à mesurer, à établir ou démontrer...) » offrant « une approche et un regard personnels ». |
| 4. Objectifs du TIPE | **100 mots max** | Énoncer « les objectifs qu'il se propose d'atteindre » — des objectifs, pas des résultats (cohérent avec la règle du projet « ne pas promettre de résultats »). |
| 5. Liste des références | **2 à 10 références** numérotées | « scientifiquement fiables et suffisamment précises pour être exploitables par les examinateurs » ; pas de contacts (rencontres, visites) ici — ils vont dans le DOT. |

**Budgets de mots consolidés** (utiles pour planifier la rédaction) : le MCOT plafonne à $50 + 50 + 50 + 100 + 650 = \mathbf{900}$ **mots**, hors 5 + 5 mots-clés et 2 à 10 références ; le DOT à $4 \times 50 = 200$ à $8 \times 50 = \mathbf{400}$ **mots**.

**Le titre est un livrable à part entière** : « choisi avec soin et permettant de définir sans ambiguïté le travail effectué ». Le brouillon `MCOT.md` propose « Optimisation sous contraintes du filtre de raccord d'une enceinte deux voies sur sa charge réelle » (15 mots). Il est correct mais tait deux éléments qui font le sujet : la **fréquence de raccord** (100 Hz) et le fait que la charge est **mesurée**, pas postulée. Piste à arbitrer par Thomas : « Optimisation sous contraintes d'un filtre de raccord à 100 Hz sur l'impédance mesurée d'une enceinte deux voies ».

**Étape 2 — Présentation et DOT.** Téléversement du PDF ; saisie du **DOT (Déroulé Opérationnel du TIPE)** : « une séquence de **4 à 8** faits marquants (jalons) [...] (y compris les difficultés rencontrées, réalisations infructueuses, surmontées ou non) », chacun « dans la limite de **50 mots** ». Le DOT « ne doit pas être analogue à un plan, ni fournir des résultats ou des interprétations. Il doit, avant tout, rester strictement factuel et situer chronologiquement les différents jalons. » Cette étape n'autorise que des « **ajustements éventuels** » des positionnements, mots-clés et références.

**Étape 3 — Validation par le professeur encadrant.** Sur son propre compte, sur **lycees.scei-concours.fr**. La validation atteste « un travail personnel constaté » et, pour un 5/2, que le travail de 3/2 n'a pas été repris. En cas de refus ou d'absence de validation : « Le candidat aura alors un entretien avant son passage en loge » — note zéro possible. Il n'y a « pas de bouton pour valider ou enregistrer la MCOT » : la saisie est automatique — vérifier en relisant.

> **Action la plus urgente de toute cette section.** Le mot « encadrant » n'apparaît **dans aucun document v2 du dépôt** (vérifié par grep hors `archive-v1/`, 0 occurrence). C'est le seul point du cadre SCEI qui peut coûter la note entière. À inscrire en phase 0 de `FEUILLE-DE-ROUTE.md`, avec échéance **rentrée septembre 2026** : (1) identifier un enseignant encadrant et obtenir son accord explicite ; (2) vérifier qu'il dispose bien d'un compte sur `lycees.scei-concours.fr` ; (3) noter son nom pour la saisie de l'étape 1 (mi-janvier 2027) ; (4) lui rappeler la fenêtre de validation de l'étape 3 (mi-juin 2027, 8 jours seulement).

**Les 24 positionnements thématiques officiels** (liste des Attendus 2026, regroupée par domaine ; la liste 2027 est [[à vérifier]]) :

| Domaine | Thèmes (libellés officiels) |
|---|---|
| **Chimie** (5) | Chimie Analytique · Chimie Théorique-Générale · Chimie Organique · Chimie Inorganique · Génie Chimique |
| **Informatique** (3) | Informatique pratique · Informatique Théorique · Technologies informatiques |
| **Sciences industrielles** (6) | Traitement du Signal · Génie Électrique · Génie Mécanique · Génie Énergétique · **Automatique** · **Électronique** |
| **Mathématiques** (5) | Géométrie · Algèbre · Analyse · **Mathématiques Appliquées** · **Autres** |
| **Physique** (5) | Physique Théorique · Mécanique · Physique de la Matière · **Physique Ondulatoire** · Physique Interdisciplinaire |

Total : $5+3+6+5+5 = 24$. Les libellés en gras sont ceux qui touchent le sujet v2 ; noter que « Électronique » et « Automatique » sont classés en **Sciences industrielles**, et que « Traitement du Signal » et « Génie Électrique » sont des voisins écartés (le sujet ne fait ni analyse spectrale pour elle-même, ni électrotechnique de puissance).

**Positionnements proposés pour le sujet v2** :

| Rang | Thème officiel (domaine) | Descripteurs officiels qui collent au sujet | Remarque |
|---|---|---|---|
| 1 | **Électronique** (Sciences industrielles) | « Électronique analogique (instrumentation, électroacoustique...) [...] Électronique (filtres, amplificateurs, électronique analogique, micro-électronique) » | Domaine de rattachement PT/PSI : satisfait la règle du premier positionnement. |
| 2 | **Mathématiques Appliquées** (Mathématiques) | « Mathématiques de l'optimisation, méthodes locales, heuristiques, globales » | Amène un examinateur compétent sur moindres carrés et optimisation discrète. Alternative : **Autres** (« statistiques [...] Applications : erreurs en physique, [...] méthodes monte carlo ») si le Monte-Carlo d'incertitudes prend du poids. |
| 3 | **Physique Ondulatoire** (Physique) — « Acoustique (son, spectre harmonique, phonons) » ou **Automatique** (SI) — « Identification, Estimation » | Validation au micro / problème inverse | Facultatif : « deux d'entre eux suffisent bien souvent ». |

Le brouillon `MCOT.md` v2 écrit « Physique — électronique/électrocinétique », « Mathématiques appliquées — ajustement de modèle », « Physique — acoustique » : à **réaligner sur les libellés officiels** ci-dessus (en particulier, « Électronique » est classé en Sciences industrielles, pas en Physique).

> **Le choix est verrouillé en janvier 2027, avant les mesures acoustiques.** Positionnements et mots-clés se saisissent à l'étape 1 (mi-janvier), c'est-à-dire pendant la phase 4 ; l'étape 2 n'autorise que des « ajustements éventuels ». Le premier positionnement « Électronique » doit donc être choisi **sur le récit prévu, pas sur les résultats obtenus**. À écrire noir sur blanc dans la feuille de route, pour ne pas se retrouver en juin avec un sujet devenu majoritairement acoustique et un binôme d'examinateurs électroniciens.

**Travail individuel ou en groupe.** L'arrêté autorise des groupes de trois au plus (quatre en BCPST/TB) ou le travail individuel. En groupe, bibliographie et problématique sont communes, les **objectifs et la présentation sont individuels** ; le préambule des Attendus demande de « clairement faire apparaître l'originalité de sa contribution ». Le rapport 2021 : 47,1 % de candidats en groupe (binômes majoritaires) ; tout écart de note supérieur à 5 points entre membres d'un groupe est instruit et « dans tous les cas [...] pleinement justifié », le plus souvent par une « polarité moteur – suiveur(s) ». Thomas est seul : cette source d'écart disparaît, mais l'exigence d'expliciter « sa propre plus-value » demeure — notamment vis-à-vis de l'aide reçue (enseignants, outils logiciels, assistant IA cité dans les sources v1 pour « la mise en forme »). Dire ce qui a été fait soi-même, mesuré soi-même, codé soi-même.

### <a id="s08-4"></a>08.4 Calendrier : sessions passées (vérifiées) et session 2027 (à confirmer)

| Étape | Session 2025 (Attendus 2025) | **Session 2026 (règlement SCEI)** ¹ | Session 2027 |
|---|---|---|---|
| 1 — Titre, ancrage, motivation, MCOT, encadrant, groupe | 16 janv. 2025 9h → 6 févr. 2025 14h | **15 janv. 2026 9h → 5 févr. 2026 14h** | **[[à vérifier]]** — par analogie : mi-janvier → début février 2027 |
| 2 — PDF de présentation, DOT, ajustements | 25 févr. 2025 9h → 10 juin 2025 14h | **25 févr. 2026 9h → 9 juin 2026 14h** | **[[à vérifier]]** — clôture ≈ début juin 2027 ; **date d'ouverture non fiable** (voir ci-dessous) |
| 3 — Validation par l'encadrant | 12 juin → 19 juin 2025 | **11 juin 2026 9h → 19 juin 2026 14h** | **[[à vérifier]]** — mi-juin 2027 |
| Jour de passage connu | — | à partir du 16 juin 2026 14h | [[à vérifier]] |
| Oraux | — | **22 juin → 18 juillet 2026** (MP, MPI, PC, PSI) ; **22 juin → 11 juillet 2026 (PT)** ; 22 juin → 4 juillet (TSI) | **[[à vérifier]]** — fin juin → juillet 2027 |
| Réclamation sur report de note | — | avant le 24 juillet 2026 14h | [[à vérifier]] |

¹ Note officielle des Attendus 2026, à reporter telle quelle : « **Dates en cours de validation et susceptibles de changer. Se reporter https://www.scei-concours.fr/tipe.html** ». Les dates ci-dessus, y compris pour 2026, ne sont donc **pas** fermes au jour près ; l'extrapolation 2027 doit être tenue pour robuste à **±2 semaines**.

**Ce qui est stable et ce qui ne l'est pas.** Pour mémoire, session 2020 : étape 1 du 15 janv. au 6 févr., étape 2 du **2 avril** au 9 juin, étape 3 du 10 au 19 juin. Les **clôtures** sont stables depuis des années (étape 1 : 5-6 février ; étape 2 : 9-10 juin ; étape 3 : ~19 juin), mais **l'ouverture de l'étape 2 a avancé de 37 jours** entre 2020 (2 avril, jour 93) et 2025-2026 (25 février, jour 56). L'extrapolation 2027 est donc fiable sur les **échéances**, pas sur les dates d'ouverture. (L'« abstract » en anglais a été supprimé en 2021.) Les dates 2027 seront publiées sur https://www.scei-concours.fr/tipe.html ; le site tipefacile.com (non officiel) confirme au 2026-09 que « SCEI n'a pas publié les dates de la session 2027 » et ne propose que des estimations.

<!-- Correction retenue : le brouillon écrivait « le rythme est stable depuis des années » alors que les données citées dans la même phrase montrent 37 jours d'écart sur l'ouverture de l'étape 2. -->

**Variable ouverte : la filière.** Thomas vient de PTSI ; le passage en **PT** ou en **PSI** n'est pas tranché, et cela change la fenêtre d'oraux : PT du 22 juin au 11 juillet 2026 (20 jours), PSI du 22 juin au 18 juillet 2026 (27 jours). Conséquence pratique : la date de passage n'est connue qu'à partir de mi-juin, et la borne haute de la fenêtre diffère d'une semaine selon la filière — à ne pas noyer dans un « pour un élève issu de PTSI ». Le premier positionnement thématique, lui, est indifférent au choix (Physique **et** Sciences industrielles sont domaines de rattachement pour PT comme pour PSI).

**Conséquence sur la feuille de route.** Le MCOT se saisit **fin janvier 2027**, donc pendant la phase 4 (fabrication/mesures) : la bibliographie commentée (650 mots), la problématique et les objectifs doivent être **rédigés dès la phase 3** (nov.–déc. 2026), pas en phase 5. Le PDF final et le DOT sont dus **début juin 2027** ; les oraux commencent **fin juin** — la phase 5 doit donc être bouclée **fin mai**, pas « juin ». Ligne de remplacement à appliquer telle quelle dans le « Calendrier synthétique » de `FEUILLE-DE-ROUTE.md` (l. 168) :

```
| Déc. 2026 – janv. 2027 | 3-4 | Rédaction MCOT (biblio 650 mots, problématique, objectifs) |
| Mi-janv. → début févr. 2027 | — | ÉTAPE 1 SCEI : titre, encadrant, ancrage, motivation, MCOT |
| Févr. – mai 2027 | 5 — Analyse/supports | Slides v2 en 4/3, DOT, listings imprimés, répétitions ; clôture fin mai |
| Début juin 2027 | — | ÉTAPE 2 SCEI : téléversement PDF + DOT ; puis ÉTAPE 3 : validation encadrant |
```

Le journal daté du dépôt (commits, notes) est la matière première du DOT : le pivot v1 → v2 du 2026-08-04 est typiquement un jalon que le SCEI aime lire (« rebonds ou inflexions dans la démarche »).

### <a id="s08-5"></a>08.5 Les six critères officiels et la réponse du sujet v2

Depuis le format 2015-2017, l'évaluation « repose sur une approche par compétences, structurée autour de 6 critères répartis en deux groupes » (Attendus 2026 ; détail dans le document « Critères d'évaluation et compétences associées », SCEI 2014). Le bilan 2019 les rattache à « 36 compétences CTI et EUR-ACE ». Un document de lycée (MP, sept. 2025) annonce un barème « Présentation : 80 % de la note / Livrables (MCOT, DOT) : 20 % » — **[[à vérifier]] : cette pondération n'apparaît dans aucun document SCEI consulté** ; le règlement dit seulement que l'évaluation « tient également compte [...] des éléments saisis en ligne ».

| Critère officiel | Ce que les examinateurs attendent (texte SCEI) | Où le sujet v2 y répond |
|---|---|---|
| **A1. Pertinence et justesse scientifiques** | « place son travail au niveau CPGE » ; « interprète les concepts, propriétés ou formules utilisées (faire le lien entre la modélisation et l'observation) » ; attention à « la compréhension des termes cités, **la rigueur des définitions énoncées**, la précision des résultats, la maîtrise des ordres de grandeur et des unités ». « Les examinateurs n'évaluent pas un master, une thèse ou une agrégation. » | Formules catalogue démontrées puis mises en défaut sur $Z(f)$ ; **définition de $f_c$ gelée** (encadré ci-dessous) ; ordres de grandeur affichés, écrits sous forme désambiguïsée (encadré ci-dessous). Thiele-Small, moindres carrés et E12 dépassent le programme mais sont introduits pas à pas — c'est autorisé si c'est expliqué. |
| **A2. Appropriation et capacité à apprendre** | « présenter, s'approprier, analyser, exploiter et critiquer un dossier scientifique relevant des disciplines de rattachement de sa filière » | Bibliographie commentée sur Thiele (1971), Small (1972), Wheeler (1928), Dickason ; confrontation des paramètres identifiés aux datasheets. **Réserve de terrain** : ces sources doivent être réellement lisibles par Thomas (articles JAES en bibliothèque électronique AES ; Dickason est un livre). À vérifier **dès la rentrée** (accès AES, bibliothèque universitaire, ou achat sur le budget), faute de quoi la bibliographie commentée sera un habillage — ce que le jury repère précisément (« viser un premier niveau d'appropriation »). [[à vérifier par l'étudiant]] |
| **A3. Ouverture et curiosité** | « décloisonner les disciplines ou varier les points de vue [...] les approches théoriques et expérimentales, mathématiques et applicatives, les performances simulées et les performances réelles d'un système technique » ; situer dans des « contextes sociaux, économiques, environnementaux » | Électronique + mathématiques appliquées + acoustique ; simulé (LTspice, Python) vs réel (banc, micro) ; contexte : coût, cuivre, énergie au repos. Attention : le PDF devant être « focalisé sur les aspects scientifiques », les volets coût et matière se présentent comme des **grandeurs mesurées** (€, kg de cuivre, W au repos), jamais comme un argumentaire d'achat. |
| **B1. Questionnement et méthode** | parcourir le cycle « choix de la problématique → orienter l'enquête → mener l'enquête → interpréter → analyse critique », « en faisant preuve d'initiative, d'esprit critique et de rigueur de raisonnement à chaque étape » | Portes de validation de chaque phase (étalonnage sur $R$ et $C$ connus, sanity check 8 Ω, **porte $f_c$ électrique à ±5 %** — référentiel précisé ci-dessous) ; critères gelés et datés avant les mesures. |
| **B2. Résolution de problème** | faire « émerger des problèmes dont les objectifs sont précis, et dont la résolution est à la portée du candidat » ; « choisir une méthode de résolution et l'appliquer » | Problème inverse (fit T-S) puis optimisation sous contraintes (énumération E12 recoupée par optimiseur continu) : deux méthodes nommées, choisies, appliquées, contrôlées. |
| **B3. Communication – présentation – échange** | « exposé clair et structuré », « précise sa contribution personnelle », « écoute des questions posées », « dialogue constructif et progressif » | Slides 15 min + annexes appelées pendant l'échange ; NOTES-TIPE v2 (Q/R) ; réponses en grandeurs physiques, jamais « ça sonne mieux ». |

> **Rappel de la définition de $f_c$ — convention valable dans tous les tableaux de critères et sur toutes les diapositives. La définition officielle est posée au § 04.1 ; le présent encadré la rappelle et la chiffre, il ne la redéfinit pas.**
> $$f_c \;=\; \text{la fréquence de \textbf{croisement des deux voies} :}\quad \bigl\lvert H_{PB}(f_c)\,G_{sub}(f_c)\bigr\rvert = \bigl\lvert H_{PH}(f_c)\,G_{med}(f_c)\bigr\rvert$$
> et **non** le pôle, **ni** une fréquence à −3 dB — ces trois-là sont des **repères**, qu'on nomme toujours explicitement. Pour la cellule normalisée $L = 18$ mH, $C = 150$ µF, $R = 8$ Ω (calcul reproduit ci-dessous) :
> - **repère « pôle »** : $f_0 = 1/(2\pi\sqrt{LC}) = 96{,}86$ Hz ; $Q = R\sqrt{C/L} = 0{,}7303$, recoupé par $Q = R/(\omega_0 L) = 0{,}7303$. Sur cette charge idéale (8 Ω résistif, DCR nulle) le croisement tombe justement sur le pôle, donc $f_c = 96{,}86$ Hz **ici** — égalité fortuite qui disparaît dès qu'il y a une DCR ou une charge réelle (§ 04.1) ;
> - **repère « −3 dB du passe-bas »** : **99,93 Hz** ; **repère « −3 dB du passe-haut »** : **93,88 Hz** (seuil **mi-puissance, $-3{,}0103$ dB**, convention de REW, gelée au § 04.1) ;
> - contrôle de cohérence : $f_{-3\,\mathrm{dB,PB}} \cdot f_{-3\,\mathrm{dB,PH}} = f_0^2$ (symétrie géométrique, vérifiée à $10^{-9}$ près).
>
> Les trois repères s'écartent de **6,05 Hz, soit 6,25 %** — davantage que la porte de validation à ±5 %. Laisser le terme flottant, c'est offrir au jury une question à laquelle on ne peut pas répondre.
>
> *Note de réconciliation* : les valeurs de contrôle qui circulaient dans le projet (99,8 Hz et 94,0 Hz) **ne sont pas des arrondis fautifs** — ce sont les mêmes repères calculés au seuil **littéral $-3{,}000$ dB** (99,820 et 93,985 Hz), alors que 99,93 et 93,88 Hz correspondent à la **mi-puissance** $-3{,}0103$ dB ($\lvert H\rvert^2 = \tfrac12$). L'écart de 0,11 % est un écart de **convention**, et c'est la mi-puissance qui fait foi. Résolution exacte dans les deux cas : $x^2 + x(1/Q^2 - 2) + (1 - 1/t) = 0$ avec $x = (f/f_0)^2$ pour le passe-bas et $t$ le seuil visé sur $\lvert H\rvert^2$ ($t = \tfrac12$ à la mi-puissance, $t = 10^{-0{,}3} = 0{,}50119$ au seuil littéral) ; symétriquement $(1-1/t)\,x^2 + x(1/Q^2 - 2) + 1 = 0$ pour le passe-haut.

> **Formule de $Q$ : préciser la topologie.** $Q = R\sqrt{C/L}$ vaut **pour la cellule LC chargée par la résistance $R$ en parallèle** — c'est le cas des deux voies de ce filtre (passe-bas : $L$ série puis $C$ en parallèle sur $R$, $H = 1/(1 + sL/R + s^2LC)$ ; passe-haut : $C$ série puis $L$ en parallèle sur $R$, **même** $Q$). À ne pas confondre avec $Q = \tfrac{1}{R}\sqrt{L/C}$ du RLC **série**. Analyse dimensionnelle : $\sqrt{\mathrm{F/H}} = \sqrt{(\mathrm{s}/\Omega)/(\Omega\,\mathrm{s})} = \Omega^{-1}$, donc $R\sqrt{C/L}$ est bien sans dimension. Ici $Q = 0{,}730$ : légèrement sous-amorti par rapport à Butterworth, conséquence directe de l'arrondi E12 (Butterworth exige $C = 140{,}7$ µF et $Q = 0{,}707$ ; la valeur normalisée est 150 µF).

> **Ordre de grandeur du DCR : toujours écrire la grandeur.** « DCR 1 Ω en série avec 8 Ω » se dit sous **deux** formes, qu'un examinateur confondra si on ne les distingue pas :
> - **puissance** : $1/(1+8) = 11{,}1\ \%$ de la puissance dissipée dans la self, soit $10\log_{10}(8/9) = -0{,}51$ dB ;
> - **niveau** (tension aux bornes du HP, donc SPL) : $20\log_{10}(8/9) = \mathbf{-1{,}02}$ **dB**.
>
> Le « ≈ −1 dB » du projet est le **niveau**, pas la puissance. Formulation à propager dans `CLAUDE.md` § Nombres de contrôle : « DCR 1 Ω en série avec 8 Ω → 11 % de la puissance dissipée dans la self, soit −1,0 dB de niveau (tension aux bornes du HP) ».

> **Référentiel de la porte à ±5 %.** La porte s'entend **entre la $f_c$ mesurée et la $f_c$ prédite à partir des valeurs de $L$ et $C$ effectivement mesurées** (self au GBF par résonance série avec un $C$ connu ; capacité au multimètre) — **pas** des valeurs nominales du catalogue. Comparée aux valeurs nominales, l'écart admissible est bien plus large : $u(f_0)/f_0 = \tfrac12\sqrt{(u_L/L)^2+(u_C/C)^2}$ vaut **7,1 %** à ±10/±10, **11,2 %** si $C$ est un électrolytique bipolaire à ±20 %, et le pire cas déterministe (tolérances de même sens, ±10/±10) va de **−9,1 %** à **+11,1 %**. Sans cette précision, la porte échouerait statistiquement une fois sur deux sans qu'aucun défaut de conception n'existe — et le critère B1 (« ne pas négliger les incertitudes ») transforme la faiblesse méthodologique en question d'entretien.

Trois points transversaux que le jury cite explicitement et que le récit v2 doit rendre visibles :

- **Ancrage au thème** : le rapport 2021 note que « le degré d'adéquation au thème est à l'appréciation des examinateurs, mais a en général un impact sur la note finale » et recommande de « pouvoir justifier l'adéquation au thème sur demande ». Réponse v2 en trois grandeurs : *optimisation* = optimisation numérique sous contraintes (fonction de coût explicite, pondérations affichées) ; *sobriété* = matière et coût (cuivre de la self via Wheeler/Brooks, coût marginal vs coût système) ; *efficacité* = pertes DCR du passif vs consommation au repos de l'actif.
- **Esprit critique et échecs** : « Se questionner/se remettre en cause — par exemple rendre compte des leçons que l'on a tiré d'une expérience qui a échoué (dans le DOT, et même dans certains cas, dans la présentation elle-même) » ; « Ne pas négliger les incertitudes expérimentales et la connaissance des appareils de mesure utilisés ». Le pivot v1 → v2, l'étalonnage de la chaîne de mesure et les barres d'erreur sur $Z(f)$ sont exactement cela. Une conclusion « le passif optimisé ne rattrape pas l'actif » est, aux yeux de ces critères, un résultat recevable — à condition d'être mesurée contre les critères gelés.
- **Réponse à la problématique** : le MCOT lie « problématique retenue » et « objectifs » ; l'oral doit revenir explicitement sur la question posée (« le filtre tient-il sa cible sur $Z(f)$, à quel coût ? ») avec les chiffres du tableau des critères gelés.

### <a id="s08-6"></a>08.6 Erreurs classiques relevées par le jury, et points de vigilance propres au projet

Relevées dans les Attendus 2026 (« Retour d'expérience », « Retour des examinateurs »), le rapport 2021 et le bilan 2019 :

1. **Téléverser au dernier moment** : « quelques centaines de candidats » en difficulté chaque année ; en 2021, « plus de 50 % des téléversements se font dans les deux dernières heures ». Aucune modification après la clôture d'une étape.
2. **Ne pas vérifier le fichier téléversé** (présentations illisibles, mauvais fichier — le bilan 2019 cite même des « tickets cinéma ») : « présenter oralement sans support » et pas de clé USB de secours.
3. **Diapositives non numérotées**, texte trop dense, phrases au lieu de mots-clés, illustrations sans crédit (« indiquer l'URL [...] en tout petits caractères au bas de la diapositive »).
4. **Positionnements thématiques imprécis** : mauvais binôme d'examinateurs ; le premier positionnement est déterminant.
5. **Adéquation au thème non mentionnée** ou « parfois un peu limite ».
6. **Présentation chronologique** (« nous avons fait ceci, puis cela... » est « à réserver au DOT ») ; à l'inverse, un DOT rédigé comme un plan ou contenant des résultats.
7. **« Tourisme industriel »** : contact avec un professionnel sans contenu scientifique.
8. **Incertitudes ignorées**, appareils de mesure non maîtrisés, ordres de grandeur et unités flous, termes employés sans les comprendre.
9. **Supposer que les examinateurs connaissent le projet** : « être explicite (efforts sur un programme ou une manip, échecs...) ».
10. **Sujet mal calibré** : « ni trop élémentaire, ni trop ambitieux », « motivé, motivant, maîtrisable », s'inscrivant « dans la durée d'une année complète ».
11. **Ne pas répéter** « devant un public critique, avec si possible un "candide" du sujet ».
12. En groupe : objectifs et présentations identiques (« anormal ») — sans objet ici.

**Audit du 2026-09-03/09 — état au moment du relevé.** Points de vigilance propres à ce projet, relevés par audit du dépôt en lecture seule les 2026-09-03 et 2026-09-09. La liste est conservée telle quelle : c'est la trace de la méthode (grep systématique, fichier et ligne cités, aucun constat sans preuve), et c'est elle qui rend les corrections vérifiables. Les items **vérifiés par grep le 2026-09-13** et effectivement corrigés depuis portent la mention **[soldé le 2026-09-13]** ; ceux qui subsistent restent écrits au présent.

- **Formule d'incertitude périmée, encore en ligne — priorité 1.** La propagation du **RC 1er ordre**, architecture abandonnée en v2, survit à trois endroits hors `archive-v1/` (relevés par grep) :
  - `presentation-finale.html` l. 1151-1179, **Annexe B « Propagation d'incertitudes sur f_c »** : « f_c = 1 / (2π · R · C) », « u(f_c) / f_c = √[ (u(R)/R)² + (u(C)/C)² ] », « ≈ ± 11 % », légende « f_c ∈ [89 ; 111] Hz » ;
  - `presentation-finale.html` l. 1073, slide « Limites assumées » : « incertitudes propagées (± 11 % sur f_c) » ;
  - `NOTES-TIPE.md` l. 94-95 : la même formule, « (≈ 11 % pour un RC) ». **[soldé le 2026-09-13]** — `NOTES-TIPE.md` a été réécrit en v2 ; vérifié par grep : la formule du RC a disparu, et le § 6 des notes (« Propagation d'incertitude sur $f_0$ — formule du LC, PAS celle du RC ») porte désormais le couple **7,1 % en borne au pire cas / 4,1 % en incertitude-type**, avec la consigne explicite « ne jamais reprendre le 11 % de la version 1 ».

  Pire : le **même fichier** affiche l. 668 « f_c = 1 / (2π√LC) » — deux définitions incompatibles de $f_c$ coexistent dans un PDF qui serait remis au jury, sans le dire. C'est exactement ce que sanctionnent le critère A1 (« rigueur des définitions énoncées ») et l'erreur classique n° 8. **À corriger avant toute réutilisation d'une diapositive v1.** *(Non soldé : vérifié par grep le 2026-09-13, les trois passages de `presentation-finale.html` — l. 1073, l. 1153-1173 et l. 668 — sont **toujours en place**. C'est attendu : les supports de la racine sont encore la v1 et leur refonte est prévue en phase 5. Le point reste donc au présent, et redevient bloquant au moment de cette refonte.)*
  (Un quatrième « 11 % » existe, `CLAUDE.md` l. 90 : « DCR 1 Ω face à 8 Ω → ~11 % de la puissance en chaleur ». Celui-là est **légitime et vérifié** — $1/(1+8) = 11{,}1\ \%$ — il demande seulement la désambiguïsation puissance/niveau donnée en 08.5.)

- **Contenu de remplacement pour l'annexe B** (à mettre tel quel sur la diapositive v2, puisque les incertitudes sont un critère explicite) :
  $$f_0 = \frac{1}{2\pi\sqrt{LC}} \quad\Longrightarrow\quad \frac{u(f_0)}{f_0} = \frac{1}{2}\sqrt{\left(\frac{u_L}{L}\right)^{\!2} + \left(\frac{u_C}{C}\right)^{\!2}}$$
  avec $u_L/L = \pm10\ \%$ et $u_C/C = \pm10\ \%$ : **7,1 % en borne au pire cas** — soit $f_0 \in [90{,}0\ ;\ 103{,}7]$ Hz autour de 96,86 Hz — et **4,1 % en incertitude-type** (loi rectangulaire, GUM : $u = 10/\sqrt3 = 5{,}8$ % par composant). **Les deux chiffres se citent toujours en couple, jamais l'un seul** : la borne dimensionne une porte de validation, l'incertitude-type se compare à d'autres incertitudes. Si le condensateur est un électrolytique bipolaire à ±20 % : 11,2 % en borne au pire cas. Le facteur $\tfrac12$ vient de la racine carrée : c'est lui que la formule RC ignorait (elle aurait donné 14,1 % à ±10/±10). **Ne jamais reprendre le 11 % comme incertitude sur $f_0$** — ni, a fortiori, sur $f_c$, qui est le croisement des deux voies (§ 04.1) et non le pôle.

- **Durée de l'exposé** : « ~10 min » est reconduit dans **4 fichiers et 6 endroits** — `CLAUDE.md` l. 85 ; `FEUILLE-DE-ROUTE.md` l. 153 et l. 187 ; `README.md` l. 38 et l. 53 ; `index.html` l. 67 (qui affiche « ≈ 10 min · 16 slides + annexes », donc **deux** chiffres faux sur la même ligne). Seul `presentation-finale.html` l. 27 affiche « ~15 min ». Le format officiel est **15 min** (voir 08.7).
  **[soldé le 2026-09-13]** — vérifié par grep : les quatre fichiers `.md`/`.html` de la racine affichent désormais « 15 min d'exposé + 15 min d'entretien », et le compte « 16 slides » a disparu de `README.md` comme d'`index.html`. Les seules occurrences restantes de « 10 min » sont des **mentions de la correction elle-même** (`CLAUDE.md`, `NOTES-TIPE.md`), ce qui est le comportement voulu.
- **Format 4/3** : gabarit 16:9 à revoir, emplacements exacts en 08.2 — dont **`EXPORT-PDF.md` l. 22, 23 et 37**, jamais nommé jusqu'ici. Décision à prendre en **phase 0** pour que les figures Python soient produites au bon format dès la phase 2. *(Non soldé : vérifié par grep le 2026-09-13, `EXPORT-PDF.md` l. 22, 23 et 37 portent toujours `1280x720`, soit 16:9.)*
- **Objets** : l'enceinte et le filtre ne peuvent pas entrer en salle → photographier avant démontage, tenir le cahier de laboratoire daté (voir 08.2).
- **Listings** : le code Python devra être imprimé en double exemplaire et annexé après la conclusion ; ordre de grandeur de pagination en 08.2.
- **Professeur encadrant** : absent de tous les documents v2 → action datée en phase 0 (voir 08.3).
  **[soldé le 2026-09-13]** *(pour la partie documentaire seulement)* — vérifié par grep : le point figure maintenant dans `CLAUDE.md` (§ Prochaines étapes), dans `FEUILLE-DE-ROUTE.md` (case de phase 0, étapes 1 et 3 du calendrier SCEI) et dans `MCOT.md` (rubrique dédiée en tête de fichier). **La désignation elle-même reste à faire** : `MCOT.md` porte encore `[[à compléter : nom du professeur encadrant + accord obtenu le …]]`, et c'est une action de l'étudiant, pas une correction de document.
- **MCOT v2** : deux rubriques dépassent déjà les limites officielles, une est vide (voir 08.7) ; les positionnements sont à réécrire avec les libellés officiels ; le titre est à réexaminer. *(Non soldé : vérifié le 2026-09-13, « Motivation » est toujours un placeholder, « Ancrage au thème » porte toujours sa note « À CONDENSER : ≈ 98 mots », et la bibliographie commentée est toujours très en dessous des 650 mots.)*
- **Risque « recette »** : le jury ne demande pas un résultat spectaculaire mais une « valeur ajoutée » et un « questionnement scientifique sur toute la durée ». Le récit v2 (mesure → problème inverse → optimisation → validation contre critères gelés) est conçu pour cela ; ne pas le réduire, à l'oral, à « j'ai calculé un filtre ».
- **Ne pas conclure « l'actif gagne »** : la référence active est un étalon immunisé par construction, pas un concurrent ; conclure sur le passif optimisé face aux critères gelés.

### <a id="s08-7"></a>08.7 Vérifications numériques : le budget temps, le budget mots et le budget taille

Script exécuté le 2026-09-09 (lecture seule du dépôt ; `scratchpad/verif_mcot_v2.py`). Trois différences avec la version du brouillon : le script **lève une erreur** si un titre de rubrique est introuvable dans `MCOT.md` (sans quoi il ne pouvait pas détecter sa propre panne, une regex en échec produisant le même « 0 mot / OK » qu'une rubrique vide) ; il distingue **VIDE** de **OK** ; et il **compte les diapositives depuis le fichier** au lieu de coder « 16 » en dur. Aucune dépendance externe (ni numpy ni scipy).

```python
import sys; sys.stdout.reconfigure(encoding='utf-8')
import re, pathlib

DEPOT = pathlib.Path(r"C:\Claude\TIPE Thomas")

# --- 1. Comptage de mots du brouillon MCOT v2 face aux limites SCEI (Attendus 2026) ---
src = (DEPOT / "MCOT.md").read_text(encoding="utf-8")
def section(titre):
    m = re.search(r"^## " + re.escape(titre) + r".*?$\n(.*?)(?=^## |\Z)", src, re.S | re.M)
    assert m, f"titre introuvable dans MCOT.md : {titre}"   # le script doit signaler sa propre panne
    return m.group(1)
def mots(txt):
    txt = re.sub(r"\[\[.*?\]\]", "", txt, flags=re.S)   # retire les placeholders (multi-lignes)
    txt = re.sub(r"[#*>|`\-]", " ", txt)
    return len(re.findall(r"[\wÀ-ÿ'’]+", txt))
limites = {"Ancrage au thème": 50, "Motivation": 50, "Problématique": 50,
           "Objectifs du TIPE": 100, "Bibliographie commentée": 650}
print(f"{'Rubrique MCOT':28s} {'mots':>5s} {'limite':>6s}  verdict")
for titre, lim in limites.items():
    n = mots(section(titre))
    verdict = "VIDE - a ecrire" if n == 0 else ("OK" if n <= lim else "A CONDENSER")
    print(f"{titre:28s} {n:5d} {lim:6d}  {verdict}")
refs = re.findall(r"^- \[\d+\]", section("Bibliographie commentée"), re.M)
print(f"References numerotees : {len(refs)} (SCEI : 2 a 10)")
lignes = [l for l in section("Mots-clés").splitlines() if l.startswith("|")]
mc = [l for l in lignes[1:] if "---" not in l]       # saute l'en-tete et la ligne separatrice
print(f"Mots-cles : {len(mc)} paires FR/EN -> {len(mc)} FR + {len(mc)} EN (SCEI : 5 + 5) : "
      f"{'conforme' if len(mc) == 5 else 'A CORRIGER'}")
print(f"Budget total MCOT : {sum(limites.values())} mots max, hors mots-cles et references")

# --- 2. Budget temps : 15 min officielles vs gabarit du deck v1 (compte depuis le fichier) ---
html = (DEPOT / "presentation-finale.html").read_text(encoding="utf-8")
n_sections = len(re.findall(r"^      <section", html, re.M))   # sections de premier niveau
n_annexes  = len(re.findall(r'class="kicker">Annexe', html))
n_vues     = n_sections - n_annexes                            # annexes hors des 15 min
print(f"\nDeck v1 : {n_sections} sections dont {n_annexes} annexes -> {n_vues} vues projetees dans l'expose")
expose_s = 15 * 60
for par_vue in (40, 45, 50, 60):
    print(f"{par_vue:2d} s/vue -> {expose_s/par_vue:4.1f} vues pour 15 min")
print(f"Gabarit v1 a 40 s/vue : {n_vues} x 40 s = {n_vues*40/60:.1f} min  (officiel : 15,0 min)")
print(f"Le meme deck tenu sur 15 min : {expose_s/n_vues:.1f} s/vue")
print(f"Ecart '10 min' (docs projet) vs 15 min : {15-10} min = {(15-10)/15*100:.0f} % du temps d'expose")

# --- 3. Marge sur la limite de 5 Mo ---
tailles = {p.name: p.stat().st_size for p in sorted(DEPOT.glob("*.pdf"))}
for nom, o in tailles.items():
    print(f"{nom:32s} {o:>9d} o = {o/1e6:5.2f} Mo (10^6) = {o/2**20:5.2f} Mio (2^20)")
plus_gros = max(tailles.values())
print(f"Marge sur 5 Mo = 5e6 o : {(5e6-plus_gros)/1e6:.2f} Mo, soit {100*(5e6-plus_gros)/plus_gros:.0f} %"
      f" de la taille du plus gros PDF actuel")

# --- 4. Extrapolation de taille (2 points, ordre de grandeur seulement) ---
n1 = len(re.findall(r"^      <section", (DEPOT/"pre-soutenance.html").read_text(encoding="utf-8"), re.M))
o1 = (DEPOT/"pre-soutenance.pdf").stat().st_size
n2, o2 = n_sections, (DEPOT/"presentation-finale.pdf").stat().st_size
pente = (o2-o1)/(n2-n1); socle = o1 - n1*pente
print(f"\nRegression a 2 points : {socle/1e6:.2f} Mo de socle + {pente/1e3:.0f} ko par vue")
for n in (26, 30):
    print(f"  {n} vues (expose + annexes) -> {(socle+n*pente)/1e6:.2f} Mo avant photos et courbes v2")
```

Sortie :

```
Rubrique MCOT                 mots limite  verdict
Ancrage au thème                98     50  A CONDENSER
Motivation                       0     50  VIDE - a ecrire
Problématique                   42     50  OK
Objectifs du TIPE              126    100  A CONDENSER
Bibliographie commentée        124    650  OK
References numerotees : 6 (SCEI : 2 a 10)
Mots-cles : 5 paires FR/EN -> 5 FR + 5 EN (SCEI : 5 + 5) : conforme
Budget total MCOT : 900 mots max, hors mots-cles et references

Deck v1 : 21 sections dont 3 annexes -> 18 vues projetees dans l'expose
40 s/vue -> 22.5 vues pour 15 min
45 s/vue -> 20.0 vues pour 15 min
50 s/vue -> 18.0 vues pour 15 min
60 s/vue -> 15.0 vues pour 15 min
Gabarit v1 a 40 s/vue : 18 x 40 s = 12.0 min  (officiel : 15,0 min)
Le meme deck tenu sur 15 min : 50.0 s/vue
Ecart '10 min' (docs projet) vs 15 min : 5 min = 33 % du temps d'expose
pre-soutenance-clair.pdf           1892945 o =  1.89 Mo (10^6) =  1.81 Mio (2^20)
pre-soutenance.pdf                 1877821 o =  1.88 Mo (10^6) =  1.79 Mio (2^20)
presentation-finale-clair.pdf      3006617 o =  3.01 Mo (10^6) =  2.87 Mio (2^20)
presentation-finale.pdf            2974906 o =  2.97 Mo (10^6) =  2.84 Mio (2^20)
Marge sur 5 Mo = 5e6 o : 1.99 Mo, soit 66 % de la taille du plus gros PDF actuel

Regression a 2 points : 0.88 Mo de socle + 100 ko par vue
  26 vues (expose + annexes) -> 3.47 Mo avant photos et courbes v2
  30 vues (expose + annexes) -> 3.87 Mo avant photos et courbes v2
```

**Lecture — Audit du 2026-09-03/09, état au moment du relevé.** Les chiffres du bloc ci-dessus sont ceux mesurés à la date de l'audit ; ils sont conservés parce qu'ils documentent l'ampleur des écarts et la méthode de calcul. Les items **vérifiés par grep le 2026-09-13** et corrigés depuis portent la mention **[soldé le 2026-09-13]** ; les autres restent au présent.

- **Budget temps. [soldé le 2026-09-13]** — la correction est faite dans les quatre fichiers ; le constat ci-dessous est conservé tel qu'il était au moment du relevé, et la **recommandation de format (16-18 vues à 50-55 s) reste valide**, elle. L'écart relevé était réel : **10 min affichées contre 15 min officielles, soit un tiers du temps d'exposé.** Le « ~10 min » vient de la pré-soutenance de juin 2026 (format interne au lycée) et avait été reconduit dans 4 fichiers et 6 endroits (liste exacte en 08.6) ; il a été remplacé par « 15 min d'exposé + 15 min d'entretien » le 2026-09-13, ce que confirme un grep de `CLAUDE.md`, `FEUILLE-DE-ROUTE.md`, `README.md` et `index.html`. Le compte de « 16 slides » qui circulait dans `README.md` et `index.html` était également faux — **il a disparu des deux fichiers, vérifié le 2026-09-13** : `presentation-finale.html` contient **21 sections de premier niveau** — 17 de contenu, 1 « Merci », 3 annexes — soit **18 vues projetées** dans l'exposé, les annexes étant hors chronomètre. À 40 s la vue, ce deck fait **12,0 min**, pas 10,7.
  Arithmétique exacte du budget : $900\ \mathrm{s}/40\ \mathrm{s} = 22{,}5$, donc **22 vues à 40 s (880 s)** ou **20 vues à 45 s (900 s)** ; le gabarit v1 (18 vues) tiendrait 15 min à $900/18 = 50{,}0$ s par vue.
  **Recommandation : viser 16 à 18 vues d'exposé, à 50-55 s chacune** — et non 22. Augmenter le nombre de planches va contre le « Retour des examinateurs » (soigner le nombre de planches, éviter le texte dense) et contre le budget de taille (ci-dessous). Le temps supplémentaire par rapport à la v1 sert à **montrer la porte de validation de chaque acte** (étalonnage, résidus du fit, sanity check 8 Ω, écart mesuré), pas à ajouter des vues. L'action « remplacer "~10 min" par "15 min + 15 min d'échange" dans les 6 endroits recensés » est **faite** ; reste à faire, et toujours d'actualité : calibrer les répétitions sur 14-15 min (couper à 15 min est le rôle du jury, pas une tolérance).
- **Budget taille.** La marge disponible est de **1,99 Mo** (66 % du plus gros PDF actuel). L'extrapolation à deux points — 10 vues → 1,88 Mo, 21 vues → 2,97 Mo, soit **0,88 Mo de socle + ~100 ko par vue**, *ordre de grandeur seulement, hors changement de gabarit* — donne **≈ 3,5 Mo à 26 vues** et **≈ 3,9 Mo à 30 vues** (exposé + annexes de listings) **avant** toute photo ni courbe de mesure. C'est un argument de plus pour 16-18 vues d'exposé, et pour la règle d'export de 08.2 (figures vectorielles, photos JPEG ≤ 200 ko).
- **Budget mots (MCOT).** *(Non soldé — vérifié le 2026-09-13 : « Motivation » est toujours un placeholder `[[à compléter]]`, « Ancrage au thème » porte toujours sa note interne « À CONDENSER : ≈ 98 mots », et la bibliographie commentée reste très en dessous des 650 mots. Seule la sous-réserve sur scipy est soldée, cf. ci-dessous.)* « Ancrage au thème » (98 mots, limite 50) et « Objectifs » (126, limite 100) sont à condenser — la note en bas de `MCOT.md` (« condenser à la saisie ») sous-estime l'ampleur : il faut **diviser l'ancrage par deux**. « Motivation » est **vide** (placeholder à écrire par Thomas, 2-3 phrases, ≤ 50 mots). Les 5 lignes du tableau de mots-clés sont **5 paires FR/EN**, donc 5 + 5 : **conforme** (le brouillon affichait « 5 » face à « 5 FR + 5 EN », ce qui se lisait comme un déficit). La bibliographie commentée n'utilise que 124 des 650 mots : c'est la rubrique où le jury lit « l'appropriation » — à développer avec des références **exactes** (titres, revue, année, pages), car les références actuelles portent des marques `[[à consulter]]` / `[[édition à préciser]]`.
  Deux réserves sur l'étoffement de cette bibliographie : (1) une **documentation logicielle consomme un des 10 emplacements** de références « scientifiquement fiables et suffisamment précises pour être exploitables par les examinateurs » — arbitrage à expliciter, les articles fondateurs passent avant ; (2) **ne pas citer dans le MCOT un outil qui ne serait pas réellement utilisé** — au 2026-09-13, numpy 2.4.6, **scipy 1.18.1** et matplotlib 3.11.0 sont installés et fonctionnels sur la machine du projet, et `scipy.optimize.least_squares` est effectivement employé (acte 2, § 03.3) : la citer est donc légitime, sous la réserve (1). *[la réserve « scipy n'est pas installé » qui figurait ici au moment du relevé est **[soldé le 2026-09-13]** : l'environnement a été vérifié, cf. l'en-tête de statut de la section 09 et le § 09.5]*
  *Précision de méthode* : le comptage ci-dessus est **indicatif à quelques pour cent près** — le script scinde les mots composés (« Thiele-Small » compte pour 2) et compte les nombres (« 1971 » compte pour 1). Testé sur trois conventions de découpage, l'ancrage donne 97 à 103 mots et les objectifs 122 à 128 : **les deux dépassements sont confirmés quelle que soit la convention**, et la problématique (42-45) comme la bibliographie (124-127) restent conformes. Le compteur qui fait foi est celui de l'interface SCEI, à revérifier à la saisie.

<!-- Non retenu tel quel : le brouillon proposait 18-22 vues ; recommandation ramenée à 16-18 vues, arbitrée par le budget de taille et le « Retour des examinateurs », les deux vérificateurs étant en désaccord sur ce point. -->

### Ce qu'il faut retenir pour l'oral

- **15 min d'exposé + 15 min d'échange avec deux examinateurs**, sur un **PDF 4/3 de 5 Mo max** projeté depuis un ordinateur résident : ni HTML, ni notes, ni objets, ni USB. Les 6 endroits du dépôt qui disaient « 10 min » ont été corrigés [soldé le 2026-09-13] ; il n'en subsiste que dans `presentation-finale.html` (support v1). Le gabarit 16:9 est à repasser en 4/3 **dès la phase 0** (sinon toutes les figures des phases 2-4 seront à refaire) ; le code Python s'imprime en double et s'annexe après la conclusion.
- **Action prioritaire, hors science : le professeur encadrant.** Il figure désormais dans CLAUDE.md, FEUILLE-DE-ROUTE.md (phase 0), MCOT.md et DECISIONS-PHASE-0.md (D10) [soldé le 2026-09-13 pour la partie documentaire], mais **la désignation elle-même reste à faire**. Sans sa déclaration à l'étape 1 et sa validation à l'étape 3, la note peut être zéro. À régler à la rentrée de septembre 2026.
- Le thème 2026-2027 est bien **« Sobriété, efficacité, optimisation »** (arrêté du 9 janvier 2026, BO ESR n° 5 du 29 janvier 2026) ; le jury veut une « valeur ajoutée » validée « par comparaison au réel » et un ancrage justifiable sur demande — répondre en trois grandeurs (fonction de coût, cuivre/coût, pertes/consommation), présentées comme des grandeurs mesurées, le PDF devant rester « focalisé sur les aspects scientifiques ».
- Six critères, deux blocs : **potentiel scientifique** (justesse, appropriation, ouverture) et **démarche** (questionnement, résolution, communication). Le jury n'attend pas un master : il attend des **définitions rigoureuses** — d'où le gel d'une définition unique de $f_c$ (la **fréquence de croisement des deux voies**, § 04.1 ; le pôle $f_0 = 1/(2\pi\sqrt{LC}) = 96{,}9$ Hz et les $-3$ dB à 99,9 / 93,9 Hz restant des repères nommés) — des ordres de grandeur désambiguïsés, des incertitudes justes ($7{,}1\ \%$ et non 11 %), et l'aveu des échecs.
- **MCOT mi-janvier → début février 2027** (900 mots au total : ancrage 50, motivation 50, biblio 650, problématique 50, objectifs 100 ; 2-10 références ; 5+5 mots-clés ; 1er positionnement en Physique/SI → « Électronique », **verrouillé avant les mesures acoustiques**) ; **DOT + PDF au plus tard début juin 2027** (4-8 jalons factuels de 50 mots, soit 200-400 mots) ; oraux à partir de fin juin — dates 2027 [[à vérifier]] sur scei-concours.fr, robustes à ±2 semaines, et l'ouverture de l'étape 2 est la date la moins prévisible.
- Tenir la ligne « critères gelés avant les mesures » : c'est la réponse directe aux critères « questionnement et méthode » et « esprit critique », et ce qui rend recevable une conclusion défavorable au filtre optimisé.

### Sources

Officielles (consultées le 2026-09-03) :

1. SCEI, « Épreuve d'évaluation des TIPE — Informations session 2026 » (règlement : durées, étapes, dates, consignes en salle) : https://www.scei-concours.fr/tipe.html
2. SCEI, *TIPE 2025-2026 — Attendus pédagogiques* (mise à jour du 21 novembre 2025 ; MCOT, DOT, présentation, retour d'expérience, liste des 24 positionnements thématiques) : https://www.scei-concours.fr/pdf/TIPE_2026_Attendus_Pedagogiques.pdf
3. SCEI, *TIPE 2024-2025 — Attendus pédagogiques* (mise à jour du 17 septembre 2024 ; calendrier session 2025) : https://www.scei-concours.fr/pdf/2025_Attendus_Pedagogiques.pdf
4. SCEI, *Critères d'évaluation et compétences associées* (document de 2014, six critères en deux blocs) : https://www.scei-concours.fr/tipe/criteres/CRITERES_TIPE_2015.pdf
5. SCEI, *Rapport annuel TIPE 2020-2021* (format 15 + 15 min, travail de groupe, écarts de notes, conseils aux candidats) : https://www.scei-concours.fr/tipe/Rapport_TIPE_2021.pdf — les fichiers `Rapport_TIPE_2022/2023/2024/2025.pdf` **n'ont pas été trouvés à cette adresse** le 2026-09-03 ; le nommage variant d'une année sur l'autre, cela ne prouve pas qu'ils n'existent pas.
6. SCEI, *Réunion bilan TIPE session 2019* (constitution des binômes d'examinateurs, évaluation des livrables, conseils) : https://www.scei-concours.fr/tipe/REUNION-BILAN-TIPE-2019-V1.pdf
7. SCEI, exemples de MCOT/DOT de candidats : https://www.scei-concours.fr/tipe/mcot/
8. Arrêté du 9 janvier 2026 fixant le thème des TIPE pour l'année scolaire 2026-2027, NOR ESRS2600935A, *Bulletin officiel de l'enseignement supérieur et de la recherche* n° 5 du 29 janvier 2026 : https://www.enseignementsup-recherche.gouv.fr/fr/bo/2026/Hebdo5/ESRS2600935A (PDF du BO : https://www.enseignementsup-recherche.gouv.fr/sites/default/files/bulletin-officiel-n-5-du-29-janvier-2026-39268.pdf)

Non officielles (documents de lycées et sites de préparation ; utilisées seulement pour les points marqués comme tels) :

9. Lycée (classe MP), « Présentation de l'épreuve de TIPE 2026 », 9 septembre 2025 — source du barème « 80 % présentation / 20 % livrables » [[à vérifier]] : https://cahier-de-prepa.fr/mp-ism/download?id=4026
10. Lycée Faidherbe (MPI), « Épreuve de TIPE au tétra-concours » — découpage conseillé 1 / 13 / 1 min : https://cahier-de-prepa.fr/mpi-faidherbe/download?id=926
11. tipefacile.com, « Calendrier TIPE 2027 » — confirme l'absence de dates officielles 2027 au 2026-09 et propose des estimations : https://tipefacile.com/blog/calendrier-tipe-2027/

Documents du projet (lecture seule, audit du 2026-09-09) : `CLAUDE.md`, `FEUILLE-DE-ROUTE.md`, `MCOT.md`, `NOTES-TIPE.md`, `README.md`, `index.html`, `presentation-finale.html`, `pre-soutenance.html`, `EXPORT-PDF.md`, `archive-v1/NOTES-TIPE.md`, `archive-v1/MCOT.md`, `archive-v1/CLAUDE.md`.

<!-- Vérification non faite, signalée par un vérificateur : le format 16:9 des PDF v1 est *déduit* du gabarit reveal.js et de la ligne decktape, il n'a pas été lu dans les /MediaBox des PDF (flux compressés ; il faudrait pdfinfo ou pypdf, non installés). L'affirmation est donc déductive, non mesurée à la source. -->

## <a id="s09"></a>09. Architecture du code d'analyse Python (dossier `analyse/`)

> **Statut.** Cette section est une **spécification** : le dossier `analyse/` n'existe pas encore
> dans le dépôt (phase 0, dernière case à cocher de la feuille de route). Les extraits ci-dessous
> ont néanmoins été écrits et **exécutés** dans un bac à sable de session sur des données
> **synthétiques** — paramètres illustratifs hérités de `archive-v1/_gen.py` et du § 04.6.
> **Aucune mesure n'a été faite sur l'enceinte de Thomas** : tout nombre est calculé ou marqué
> `[[à mesurer]]`. Environnement revérifié le **2026-09-13** : Python 3.13.2, numpy 2.4.6,
> matplotlib 3.11.0, **scipy 1.18.1 présent et importable**, `pytest` absent.
> ⚠ **Fait de référence pour tout le TIPE** : au 2026-09-13, scipy **est** installé et
> fonctionnel (`scipy.optimize.least_squares` exécuté avec succès). Toute phrase du type
> « scipy n'est pas installé » / « repli sans scipy obligatoire » est **périmée** — elle a été
> corrigée dans la présente section de référence ; il en subsiste au 2026-09-13 dans
> `CLAUDE.md` et `NOTES-TIPE.md`, à reprendre. Le repli sans SciPy garde toute sa raison d'être
> comme **exercice de robustesse** (répondre à « et que fait-il, votre `least_squares` ? ») et
> comme **secours** si l'analyse est refaite sur une machine du lycée — où il faudra
> **vérifier la présence de scipy** — mais ce n'est pas une contrainte subie.

**Où tourne quoi.** L'acquisition se fait au lycée — réglage du GBF, lecture de l'oscilloscope,
export CSV — et ne demande **aucun Python**. Le dépouillement, l'ajustement, l'optimisation et les
figures tournent sur le poste personnel, où numpy / scipy / matplotlib sont installés. Le repli
Levenberg-Marquardt du § 09.5 existe pour le cas où l'analyse doit être refaite sur une machine
qui n'a que numpy ; rien dans la chaîne ne fonctionne sans numpy.

### <a id="s09-1"></a>09.1 Quatre principes de conception

1. **Les données brutes ne sont jamais réécrites — et le fichier de mesure les contient.** Le CSV
   versionné porte les **lectures** ($V_d$, $V_R$, $\Delta t$, calibres) *et* les grandeurs
   dérivées ($\lvert Z\rvert$, $\varphi$). Si l'on découvre après coup que $R_{ref}$ valait 99,2 Ω
   et non 99,7, ou qu'une sonde était en ×10, la série entière reste exploitable : on rejoue
   `depouiller()`. Un `*_brut.csv` « en option » se traduit par « jamais fait » un soir de manip —
   d'où l'obligation, contrôlée par un test (§ 09.6, test g).
2. **Aucun résultat en dur.** Les valeurs typiques (`SUB_TYP`, `MED_TYP`) portent la mention
   « TYPIQUE, PAS une mesure » dans le source ; les modèles de prix et de DCR sont des fonctions
   isolées, documentées comme placeholders (§ 04.5) : quand le prix réel arrive, une ligne change.
3. **Tout chiffre montré au jury est régénérable par une commande** — d'où `tout_refaire.py`
   (§ 09.8) et la suite de tests (§ 09.6) : si un test tombe, aucun chiffre n'est plus garanti.
4. **Les décisions gelées sont un fichier, pas une intention.** Critères, définition de $f_0$,
   pondérations $w$ de $J$, bande de coût, deux niveaux d'écoute : tout vit dans
   `analyse/criteres_geles.json`, daté, versionné, lu par `optim.py` et recopié dans le journal.
   C'est ce qui rend **vérifiable** l'affirmation « critères gelés avant les mesures », socle
   d'honnêteté du sujet (§ 08) — sinon rien n'empêche de retoucher les poids après coup.

### <a id="s09-2"></a>09.2 Arborescence proposée

```
analyse/
├── README.md                  # comment relancer, quelle version a produit quelle figure
├── criteres_geles.json        # DECISIONS gelees en phase 0 (date + commit) -- principe 4
├── mesures/                   # DONNEES BRUTES, lecture seule, versionnees
│   ├── 2026-09-xx_etalonnage_{R8,C100uF,L18mH}.csv   # porte de validation phase 1
│   ├── 2026-10-xx_sub_caisse_Rref{100,10}.csv        # releve cle + recoupement (§ 02.4)
│   ├── 2026-10-xx_mediums_serie.csv ; rew/ ; scope/  # + exports REW et captures brutes
│   └── composants.csv         # valeur nominale, valeur MESUREE, u, DCR mesuree, prix, date
├── modele_hp.py               # Z_ts, caisse close, Zobel, grilles de frequences (§ 01)
├── io_mesures.py              # lire_mesure, ecrire_mesure, lire_rew, lire_scope, depouiller
├── entrees.py                 # alias de compatibilite vers io_mesures (nom du contrat ci-dessus)
├── ts_fit.py                  # probleme inverse : init, residus, ajustement, covariance (§ 03)
├── filtre.py                  # H_pb, H_ph, cibles, sommation, contraintes, netlist LTspice (§ 04)
├── optim.py                   # series E12/E6, fonction de cout, enumeration exhaustive (§ 04.5)
├── self_bobine.py             # Wheeler, Brooks, DCR(L, fil), masse de cuivre, cout (satellite)
├── incertitudes.py            # propagation analytique + Monte-Carlo, correlations
├── energie.py                 # pertes Joule, conso au repos, croisement energetique (§ 06)
├── figures.py                 # style Blueprint + export SVG a variables CSS (§ 09.7)
├── injecter_figures.py        # inline les SVG dans le HTML aux marqueurs <!--FIG:nom-->
├── tout_refaire.py            # rejoue toute la chaine dans l'ordre (§ 09.8)
├── resultats/                 # SORTIES regenerables, ignorees par git -- sauf les 2 JSON
│   └── figures/*.svg ; parametres_ts.json ; design_optimise.json ; journal.txt
└── tests/                     # test_{entrees,ajustement,optimiseur,incertitudes,series_e12,
                               #        figures,self_bobine}.py
```

Un module = une étape du récit. `mesures/` et `resultats/` ne se confondent jamais : **ce qui est
dans `mesures/` a coûté une séance de banc, ce qui est dans `resultats/` coûte dix secondes.**

### <a id="s09-3"></a>09.3 Formats de données

**CSV de mesure d'impédance** (format « maison », référence) : une ligne de titre, puis une
métadonnée **par ligne** au format `# clé: valeur` — les conditions exigées au § 02.11, étape 12 —
puis la ligne de noms de colonnes, puis les points. Extrait **réellement produit** par
`ecrire_mesure` (données **synthétiques**), tronqué après la sixième clé :

```
# TIPE filtrage enceinte -- mesure d'impedance
# version_format: 1
# date: 2026-09-15T14:32
# dipole: SYNTHETIQUE (demo, pas une mesure)
# montage: A (dipole a la masse) -- GBF + oscilloscope 2 voies
# R_ref_nominale_ohm: 100
# R_ref_mesuree_ohm: 99.7
# u_R_ref_relative_pct: 0.5
# u_systematique_relative_pct: 1.2
#   ... (14 cles au total : niveau, temperature, operateur, appareil, Re_DC avant/apres)
f_Hz,V_dipole_V,V_Rref_V,dt_s,module_Z_ohm,phase_deg,u_module_alea_ohm,u_phase_deg
10,0.0947589735,0.669779873,0.00115906419,10.0771346,41.7263108,0.201542691,1
10.5946,0.0993141244,0.669089268,0.00115297158,10.5682462,43.9694157,0.211364924,1
```

| Colonne | Unité | Contenu | Origine |
|---|---|---|---|
| `f_Hz` | Hz | fréquence **lue à l'oscilloscope**, pas la consigne du GBF (§ 02.6) | mesure |
| `V_dipole_V`, `V_Rref_V` | V | amplitudes des deux voies, **calibres consignés en en-tête** | mesure |
| `dt_s` | s | décalage $\Delta t = t(V_{R_{ref}}) - t(V_{dipole})$, sur deux passages par zéro **montants** successifs | mesure |
| `module_Z_ohm` | Ω | $\lvert Z\rvert = R_{ref}\,V_d/V_R$ | recalculé |
| `phase_deg` | ° | $\varphi = 360\,f\,\Delta t$ ; avec la convention de $\Delta t$ ci-dessus, **$\varphi>0$ pour une charge inductive** | recalculé |
| `u_module_alea_ohm` | Ω | incertitude-type **aléatoire** ($k=1$), point par point → **poids de l'ajustement** | calculé |
| `u_phase_deg` | ° | incertitude-type, $k=1$ | calculé |

**Pourquoi l'incertitude est scindée.** Le bruit de lecture est aléatoire et varie d'un point à
l'autre ; $u(R_{ref})$ et l'étalonnage de chaîne sont **systématiques** et multiplient *tous* les
$\lvert Z\rvert$ de la série. Les mettre dans la même colonne fausse le $\chi^2$, biaise $R_e$ et
sous-estime les barres d'erreur des paramètres T-S. Le systématique vit donc dans l'en-tête
(`u_systematique_relative_pct`) et s'applique **après** l'ajustement, en propagation sur $\theta$
(§ 03.5). Les colonnes dérivées sont régénérables à partir des colonnes brutes — un test l'impose.

Autres choix explicites : séparateur virgule, point décimal, **9 chiffres significatifs**
(aller-retour écriture/lecture exact à $4\cdot10^{-9}$ **en relatif** ; le fichier grossit de 15 %
et il n'y a plus rien à justifier) ; métadonnées obligatoires refusées si absentes ;
`version_format` pour changer d'avis sans casser les anciens fichiers.

<!-- Les deux relecteurs avaient raison : l'extrait compacte avec des « | » etait une mise en page presentee comme une sortie, et il cassait le parseur (8 cles lues sur 13, version_format et R_ref_mesuree_ohm perdues). Verifie : le format ci-dessus donne bien 14 cles. -->

Deux formats sont importés tels quels, chacun avec sa fonction de lecture gelée :

- **export REW** — `lire_rew(chemin) -> (f, mod, phi, meta)`. En-tête préfixée par `*`, puis trois
  colonnes (fréquence, module, phase). Le séparateur dépend de la version et des réglages
  régionaux [[à vérifier sur un export réel]] : le lecteur l'auto-détecte parmi `,` `;`
  tabulation ou espaces. REW donne des centaines de points sans incertitude : la fonction leur
  **affecte** l'incertitude de chaîne issue de ses calibrations (§ 02.9). REW calcule aussi
  lui-même les paramètres de Thiele-Small : cette sortie n'est pas un concurrent de l'ajustement
  maison, c'est sa **vérification indépendante** (test h).
- **CSV d'oscilloscope** — `lire_scope(chemin) -> (t, v1, v2, meta)` (temps, CH1, CH2 ; en-tête
  propre à l'appareil [[format du modèle du lycée à relever]]). Au lieu de pointer $\Delta t$ au
  curseur, faire une **détection synchrone** : projeter chaque voie sur $e^{-2j\pi f_0t}$ donne
  amplitude *et* phase en une passe et rejette tout ce qui n'est pas à $f_0$.

**Condition de validité, et elle n'est pas cosmétique.** La projection sur un seul point de DFT
n'est exacte que si la fenêtre contient un **nombre entier de périodes** de $f_0$ ; sinon la fuite
spectrale biaise le résultat, et l'offset continu ne se projette plus à zéro. Mesuré sur le même
modèle synthétique : sur 100 ms à 100 Hz (10 périodes **exactement**, et 5 périodes du ronflement
50 Hz — deux coïncidences, pas une propriété) l'erreur sur $\lvert Z\rvert$ vaut **+0,05 %** ; sur
103,7 ms elle passe à **+1,9 %** ; au deuxième point de la grille (10,5946 Hz) sur 100 ms elle
atteint **−5,5 %** et 2,6° sur la phase. Une erreur de 5 % sur $Z$ ruine l'ajustement de l'acte 2
et dépasse à elle seule la porte de validation à ±3 % de la phase 1. On impose donc la condition
dans le code — ou, mieux, on utilise l'estimateur par moindres carrés, valable pour une fenêtre
**quelconque** et qui retire l'offset au passage :

```python
def depouiller_scope(t, v1, v2, f0, R_ref, methode='lstsq'):
    """Depouillement d'une acquisition 2 voies a la frequence f0.
    Convention section 02 : CH1 = V_dipole, CH2 = V_Rref ; Z = R_ref*A1/A2, donc arg(Z) > 0
    pour une charge inductive. Retourne (|Z|, phase_deg, |A1|, |A2|).
    methode='dft'   : projection sur exp(-2j.pi.f0.t) -- EXACTE seulement si la fenetre
                      contient un nombre ENTIER de periodes de f0 ; on la tronque donc.
    methode='lstsq' : moindres carres sur [cos, sin, 1] -- valable pour une fenetre
                      quelconque, la colonne constante absorbant l'offset continu."""
    t = np.asarray(t, float); w = 2*np.pi*f0
    if methode == 'dft':
        N = int(np.floor((t[-1] - t[0])*f0))                 # periodes entieres disponibles
        if N < 1: raise ValueError('fenetre plus courte qu une periode de f0')
        m = t <= t[0] + N/f0 - 0.5*(t[1] - t[0])             # on tronque a N periodes
        e = np.exp(-1j*w*t[m])
        A1, A2 = 2*np.mean(v1[m]*e), 2*np.mean(v2[m]*e)      # phaseurs (amplitude crete)
    else:
        M = np.c_[np.cos(w*t), np.sin(w*t), np.ones_like(t)]
        a1 = np.linalg.lstsq(M, v1, rcond=None)[0]
        a2 = np.linalg.lstsq(M, v2, rcond=None)[0]
        A1, A2 = a1[0] - 1j*a1[1], a2[0] - 1j*a2[1]
    Z = R_ref*A1/A2
    return abs(Z), np.degrees(np.angle(Z)), abs(A1), abs(A2)
```

Sortie de `demo_io.py` (acquisitions **simulées** à 50 kéch/s, bruit + offset + résidu 50 Hz) :

```
CSV ecrit : demo_sub_synthetique.csv | 69 points, 14 cles de metadonnees
  aller-retour |Z| exact a 4e-9 pres EN RELATIF (%.9g) : True
  colonnes derivees recalculees depuis le brut : ecart max 9.2e-08 ohm
Garde-fou metadonnees : metadonnees manquantes : R_ref_mesuree_ohm
                                        |Z| vrai     dft brut      dft tronque   lstsq
  100 Hz, 100.0 ms (10 periodes)        14.1034      +0.053 %      +0.086 %      +0.053 %
  100 Hz, 103.7 ms (10,37 periodes)     14.1034      +1.921 %      +0.058 %      +0.106 %
  10.5946 Hz, 100 ms (1,06 periode)     10.3973      -5.506 %      +0.024 %      -0.007 %
Controle de signe : self pure 10 mH -> phi = +90.00 deg ; condo pur 100 uF -> phi = -90.00 deg
```

Module et phase sont retrouvés à mieux de 0,1 % malgré le bruit, **à condition d'utiliser un
estimateur non biaisé** : c'est l'argument pour exporter les acquisitions plutôt que pointer des
curseurs, **si** l'export CSV de l'oscilloscope du lycée est accessible [[à vérifier]]. Le contrôle
de signe (self pure → +90°, condensateur pur → −90°) coûte trois lignes de test et attrape une fois
pour toutes l'erreur de convention qui, sinon, rend un $Q_{ms}$ négatif ou une phase miroir à
l'acte 2, **sans aucun message d'erreur**.

Un piège numpy mérite d'être connu : `np.genfromtxt(..., names=True, comments='#')` prend comme
ligne de noms **la première ligne du fichier, commentée ou non**. Avec un en-tête `# clé: valeur`
l'appel **échoue bruyamment** (`ValueError: got N columns instead of 1`) — le diagnostic est
immédiat, mais le contournement reste le même : découper l'en-tête du corps à la main, ce qui a de
toute façon l'avantage de **rendre les métadonnées**.

<!-- Le brouillon parlait de « faux positif silencieux » et d'« une demi-heure perdue » : verifie, genfromtxt leve une exception. Le mot « silencieux » ne vaut que pour _gen.py (§ 09.7), pas ici. -->

```python
CLE = re.compile(r'#\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)')   # une cle = un identifiant, point

def lire_mesure(chemin):
    """Lit un CSV de mesure -> (d, meta) : d = tableau structure numpy (toujours 1-D),
    meta = dict des lignes '# cle: valeur'. Les lignes '#' qui ne sont pas de cette forme
    (titre, commentaire libre) sont IGNOREES. Erreur explicite si une colonne ou une
    metadonnee obligatoire manque."""
    meta, corps = {}, []
    with open(chemin, encoding='utf-8') as fh:
        for ligne in fh:
            if ligne.startswith('#'):
                m = CLE.fullmatch(ligne.strip())
                if m: meta[m.group(1)] = m.group(2).strip()
            elif ligne.strip(): corps.append(ligne)
    d = np.atleast_1d(np.genfromtxt(io.StringIO(''.join(corps)),      # atleast_1d : un fichier a
                                    delimiter=',', names=True, dtype=float))   # 1 ligne reste 1-D
    absentes = [c for c in COLONNES if c not in d.dtype.names]
    if absentes: raise ValueError('colonnes absentes : ' + ', '.join(absentes))
    if 'version_format' not in meta: raise ValueError('version_format absent : fichier hors format')
    return d, meta
```

Le `re.fullmatch` neutralise à la fois la ligne de titre et les commentaires libres : aucune clé
fantaisiste ne peut plus entrer dans `meta`. Le `np.atleast_1d` règle en un mot le cas — réaliste —
du fichier d'étalonnage à une seule ligne de données, qui sinon rend un tableau 0-d sur lequel
`len(d)` lève `TypeError`. Le `with` ferme le fichier sans dépendre du compteur de références.

**Coût en temps de banc, à savoir avant de choisir la grille.** 69 points × (régler le GBF, lire
deux amplitudes et un $\Delta t$) représentent **2 à 3 h** de manip point par point, à multiplier
par deux $R_{ref}$ et deux haut-parleurs. D'où le partage : le relevé **fin** se fait à la carte
son + REW (des centaines de points en quelques minutes), le relevé GBF/oscillo sert
d'**étalonnage** sur ~20 points et de **recoupement** — c'est exactement ce que la porte de
validation de la phase 1 demande, et cela tient dans une séance.

### <a id="s09-4"></a>09.4 Fonctions clés (signatures à geler)

**Convention de nommage dans le code (la définition de $f_c$, elle, est celle du § 04.1).**
Rappel : **$f_c$ = fréquence de croisement des deux voies**, seule définition du TIPE ; dans le
code elle porte le nom `f_x` (jamais `f0`). La variable `f0` désigne un **repère**, la
**fréquence propre (le pôle)** $f_0 = 1/(2\pi\sqrt{LC})$ : c'est elle que rapportent l'optimiseur,
les tests et la propagation d'incertitude, parce qu'elle est la grandeur directement fonction de
$L$ et $C$. Les repères à $-3$ dB des réseaux **réels chargés** en diffèrent — pour 18 mH / 150 µF
sur 8 Ω : $f_0 = 96{,}86$ Hz, et, au seuil **mi-puissance** $-3{,}0103$ dB gelé au § 04.1,
$f_{3,PB} = 99{,}93$ Hz et $f_{3,PH} = 93{,}88$ Hz ($Q = 0{,}730$) — soit 6 % entre extrêmes,
l'ordre de grandeur de l'incertitude elle-même. *(Les sorties de test reproduites plus bas
affichent 99,82 et 93,99 Hz : ce sont les mêmes repères au seuil **littéral** $-3{,}000$ dB, écart
de convention de 0,11 %, sans portée sur les critères — cf. § 04.1. **Spécification** : dans
`analyse/`, la fonction qui calcule un repère à $-3$ dB prend la convention en paramètre nommé et
la valeur par défaut est `seuil=3.0103` ; le prototype du § 06.5, écrit avant le gel, utilise
encore `seuil=3.0`.)* Ces
repères sont nommés `f3_pb` et `f3_ph` et ne sont cités que comme grandeurs dérivées (§ 04.1).
L'argument de `cible()` s'appelle donc `f0_cible` : pour la cible canonique, $f_0 = f_{cible}$ par
construction.

| Module | Signature | Retour |
|---|---|---|
| `modele_hp` | `Z_ts(f, Re, Le, Res, fs, Qms)` ; `grille_log(f1, f2, n_par_octave=12, densifier=(fs/2, 2*fs, 24))` ; `zobel(Z, f, Rz, Cz)` | $Z$ complexe (§ 01) ; grille de fréquences (§ 02.6) ; $Z$ avec Zobel (§ 04.4) |
| `entrees` | `lire_mesure(chemin)` / `ecrire_mesure(chemin, d, meta)` ; `lire_rew(chemin)` ; `lire_scope(chemin)` ; `depouiller_scope(t, v1, v2, f0, R_ref, methode)` | `(d, meta)` ; `(f, mod, phi, meta)` ; `(t, v1, v2, meta)` ; `(mod, phi, A1, A2)` |
| `ts_fit` | `init_depuis_courbe(f, mod, phi=None, Re0=None)` ; `residus_ts(theta, f, mod, phi, u_mod, u_phi)` | $\theta_0$ lu sur la courbe (§ 03.3) ; résidus pondérés empilés |
| | `ajuster_ts(f, mod, phi, u_mod, u_phi, theta0, forcer_repli=False)` | `(theta, cov, chi2_reduit, moteur)` |
| `filtre` | `H_pb(f, L, C, Z, r=0.)` / `H_ph(f, C, L, Z, r=0.)` ; `cible(f, nom, f0_cible=100.)` ; `verifier_contraintes(design, P_max, Z)` ; `exporter_netlist(design, Z_rlc, chemin)` | $H$ complexe, diffusion `(n,1)×(Nf,)` ; $(H^c_{PB}, H^c_{PH})$ ; `(V_C_crete, I_L_crete, Zin_min, ok)` ; `.cir` LTspice (§ 04.10) |
| `optim` | `cout(p1, p2, f, Zs, Zm, H_ac_sub, H_ac_med, g_med, cible_nom, w, pol, dcr)` ; `enumere_e12(f, Zs, Zm, L_vals=L_VALS, C_vals=C_VALS, **kw)` ; `optimiser_sur_stock(stock, ...)` | $J$ de forme `(n1, n2)` (§ 04.5) ; meilleur design + `n_combinaisons` |
| `self_bobine` | `L_wheeler(N, a, b, c)` ; `dcr_de_L(L, d_fil, geometrie)` ; `masse_cuivre(L, DCR)` ; `brooks(L)` ; `cout_self(L)` | $L$ [H] ; DCR [Ω] ; masse [kg] ; géométrie optimale ; € |
| `incertitudes` | `u_f0_relative(uL_rel, uC_rel, rho=0.)` (**incertitudes-types**, $L$ et $C$ indépendants si `rho=0`) ; `mc_f0(L, C, uL_rel, uC_rel, n, loi, graine, rho)` (`loi='normale'` → **écarts-types** ; `loi='uniforme'` → **demi-largeurs**, $u=a/\sqrt3$ — la docstring l'écrit, c'est le piège de la section) | $u(f_0)/f_0$ analytique ; `(moyenne, écart-type relatif)` |
| `energie` | `pertes_joule(design, Z, P_ref)` ; `croisement(P_repos_actif, design, Z)` | W ; niveau d'écoute de croisement (§ 06) |
| `figures` | `style_blueprint()` / `enregistrer_svg(fig, chemin)` ; `injecter_figures(html, dossier, noms)` | SVG à variables CSS (§ 09.7) ; nombre d'injections |

Conventions : **tout en SI** (henry, farad, hertz), conversion en mH/µF à l'affichage seulement ;
les jeux de composants sont des tableaux `(n, 2)` pour que la fonction de coût vectorise sur toutes
les combinaisons d'un coup ; docstrings et messages **en français sans accents**, pour rester
lisibles si un script est lancé dans une console cp1252 — les **fichiers**, eux, sont en UTF-8
explicite (§ 09.8).

**Ce que `cout` reçoit, et pourquoi la signature est plus longue que prévu.** Le critère n° 1 gelé
dans FEUILLE-DE-ROUTE est **acoustique** (« écart RMS (dB) de la somme des deux voies à la cible
plate, 40–250 Hz, micro + REW »). Une fonction de coût purement électrique optimiserait donc en
phase 3 une grandeur qu'on ne mesure pas en phase 4, et la comparaison contre critères gelés
perdrait son sens. D'où `H_ac_sub`, `H_ac_med` (réponses acoustiques par voie, mesurées en champ
proche — ou, tant qu'elles n'existent pas, un modèle de caisse close paramétré par le fit T-S) et
`g_med` (gain d'égalisation entre le 18″ et le bloc médium, piège explicitement gelé dans
`CLAUDE.md`). **Ordre logique assumé** : la phase 3 optimise sur l'électrique seul, faute de mesure
acoustique disponible à cette date ($H_{ac}=1$, hypothèse « HP plats et colocalisés » du § 04.6) ;
la phase 4 **referme la boucle** en réoptimisant avec les $H_{ac}$ mesurées, et l'écart entre les
deux designs est lui-même un résultat. L'argument `dcr` vient de `self_bobine.dcr_de_L` : c'est ce
couplage — et lui seul — qui fait du satellite « self optimale » une pièce du récit plutôt qu'une
annexe décorative.

**Les grilles, écrites noir sur blanc** (§ 04.5) : `L_VALS` = E12 × {1 mH, 10 mH} → **1,0 à 82 mH**
(24 valeurs), `C_VALS` = E12 × {10 µF, 100 µF} → **10 à 820 µF** (24 valeurs). Deux décades
suffisent parce qu'à 8 Ω et 100 Hz les valeurs catalogue (18 mH, 141 µF) sont **au centre** de la
grille, à plus d'une décade de chaque borne — mais c'est une hypothèse, pas un théorème, d'où
l'assertion anti-optimum-de-bord du test (d). Rappel du § 04.5 : la contrainte E12 est légitime
pour les **condensateurs** (on les achète) et **discutable pour les selfs bobinées maison**, dont
la valeur est quasi continue (quantifiée par le nombre de spires). Les 331 776 combinaisons restent
la borne pédagogique ; le recoupement continu, lui, traite $L$ comme une variable réelle.

Le cœur physique tient en quelques lignes, et c'est voulu :

```python
def Z_ts(f, Re, Le, Res, fs, Qms):
    """Impedance electrique du HP (modele de Thiele-Small a 5 parametres, SI).
    theta = (Re [ohm], Le [H], Res [ohm], fs [Hz], Qms [-]) ; retourne Z complexe.
    Domaine : f > 0 strictement (le modele est en f/fs - fs/f) et validite 10-500 Hz ;
    au-dela, la semi-inductance (courants de Foucault) fait devier Le -- cf. repli § 03."""
    f = np.asarray(f, float)
    if np.any(f <= 0): raise ValueError('Z_ts : f doit etre > 0 (modele en f/fs - fs/f)')
    x = f/fs - fs/f                                    # x = desaccord reduit
    return Re + 2j*np.pi*f*Le + Res/(1 + 1j*Qms*x)

def enumere_e12(f, Zs, Zm, L_vals=L_VALS, C_vals=C_VALS, bloc=48, **kw):
    """Recherche EXHAUSTIVE sur la grille E12 : le minimum trouve est le minimum GLOBAL
    sur la grille, sans hypothese sur la regularite de J ni sensibilite a l'initialisation
    -- contrairement a un optimiseur continu, qui peut converger vers un minimum local.
    J (somme + forme des voies + phase + euros + watts) est detaillee au § 04.5.
    Memoire : le tableau intermediaire des sommes pese 16*bloc*n2*Nf octets (28 Mo pour
    bloc = 48, n2 = 576, Nf = 64) ; J final, float64 (576, 576), pese 2,7 Mo."""
    p1, p2 = couples(L_vals, C_vals), couples(C_vals, L_vals)
    J = cout(p1, p2, f, Zs, Zm, bloc=bloc, **kw)       # (576, 576), produit externe PAR BLOCS
    i, j = np.unravel_index(np.argmin(J), J.shape)
    return dict(L1=p1[i, 0], C1=p1[i, 1], C2=p2[j, 0], L2=p2[j, 1],
                J=J[i, j], n_combinaisons=J.size)
```

<!-- Le « aucun minimum local possible » du brouillon etait faux : l'exhaustivite ne supprime pas les minima locaux, elle garantit d'atteindre le minimum global malgre eux. Docstring corrigee. -->

**La mémoire est le point qui fait planter un PC de lycée**, et le mot « par blocs » ne suffit pas :
sans découpage, le tableau des sommes des deux voies pèse $16\,n_1n_2N_f$ octets, soit **340 Mo**
à $N_f=64$ et **1,06 Go** à $N_f=200$. Avec `bloc = 48`, la crête retombe à **28 Mo** (88 Mo à
$N_f=200$). $N_f = 64$ points log sur 40–250 Hz suffisent pour un écart RMS en dB [[à contrôler en
doublant $N_f$ : l'optimum ne doit pas bouger]].

**L'énumération jointe est-elle une inflation ?** Question de jury légitime : si $J$ se sépare en
$J_1(\text{voie 1}) + J_2(\text{voie 2})$, il n'y a que $576+576 = 1152$ évaluations à faire, pas
331 776. Réponse vérifiée : **les termes de somme et de phase couplent les deux voies**, et le
couplage change le résultat. Sur 8 Ω, avec le seul terme « forme de chaque voie » (séparable), le
passe-haut choisit **15,0 mH** ; avec le $J$ gelé (somme + voies + phase), il choisit **18,0 mH**.
L'énumération jointe n'est donc pas décorative — mais il faut savoir dire quels termes couplent
(somme, phase, budget total, encombrement) et lesquels ne couplent pas (forme par voie, prix par
voie, pertes par voie).

### <a id="s09-5"></a>09.5 Dépendances, et repli sans SciPy

| Paquet | Version vérifiée (2026-09-13) | Rôle | Indispensable ? |
|---|---|---|---|
| `numpy` | 2.4.6 | tout le calcul vectoriel | **oui** |
| `matplotlib` | 3.11.0 | figures SVG | oui (figures seulement) |
| `scipy` | 1.18.1 (installé) | `optimize.least_squares` (acte 2), recoupement continu (acte 3) | non — **repli fourni** |
| `unittest` | bibliothèque standard | tests de non-régression | oui, rien à installer |

**Rien n'est à installer sur le poste de travail** : numpy 2.4.6, scipy 1.18.1 et matplotlib
3.11.0 y sont présents et fonctionnels (vérifié le 2026-09-13, `least_squares` exécuté). La ligne
`python -m pip install --user numpy scipy matplotlib` ne sert que si l'on repart d'une machine
neuve ; **si les calculs sont refaits sur une machine du lycée, y vérifier la présence de scipy** —
c'est le seul cas où le repli ci-dessous est utilisé par nécessité. Partout ailleurs il est un
**exercice de robustesse**, pas une contrainte subie. `pytest` n'est installé nulle part — d'où
`unittest`, qui est dans la bibliothèque standard.

```python
try:
    from scipy.optimize import least_squares
    SCIPY = True
except ImportError:            # repli : le poste du lycee peut ne pas avoir SciPy
    SCIPY = False

def moindres_carres_lm(residus, theta0, args=(), n_iter=80, lam=1e-3):
    """Levenberg-Marquardt maison (REPLI sans SciPy) : jacobienne par differences
    finies, pas amorti, parametres contraints positifs.
    Retourne (theta ajuste, jacobienne au point final) -- la jacobienne est NECESSAIRE
    pour que ajuster_ts() rende une covariance dans les deux branches."""
    th = np.asarray(theta0, float).copy(); J = None
    S = lambda t: float(np.sum(residus(t, *args)**2)); s = S(th)
    for _ in range(n_iter):
        r = residus(th, *args); J = np.empty((r.size, th.size))
        for j in range(th.size):                        # jacobienne numerique, pas relatif
            d = 1e-6*max(abs(th[j]), 1e-12); tp = th.copy(); tp[j] += d
            J[:, j] = (residus(tp, *args) - r)/d
        A, g = J.T @ J, J.T @ r
        for _ in range(40):                             # recherche du pas amorti
            try: pas = np.linalg.solve(A + lam*np.diag(np.diag(A)), -g)
            except np.linalg.LinAlgError: lam *= 10.; continue
            if np.all(th + pas > 0) and S(th + pas) < s:
                th, s, lam = th + pas, S(th + pas), max(lam/10., 1e-12); break
            lam *= 10.
        else: break
    return th, J
```

`ajuster_ts` calcule ensuite `cov = np.linalg.inv(J.T @ J)` **dans les deux branches** (`sol.jac`
côté SciPy) : c'est légitime ici parce que les résidus sont déjà pondérés par $u_{mod}$ et
$u_{\varphi}$, donc $J^{\mathsf T}J$ est la matrice d'information. Sans cela, la signature gelée
promettrait une covariance que le repli ne rendrait pas — et le critère « < 3 σ » du test (a)
serait intestable sur un poste sans SciPy, pour une raison d'interface et non de physique.

C'est exactement l'algorithme du § 03.2 (linéariser, résoudre les équations normales amorties,
itérer) : le repli n'est pas un pis-aller, c'est **la même méthode écrite à la main**, et l'avoir
écrite est un bon argument d'oral. Un test vérifie qu'il donne la même réponse que SciPy,
**paramètres et écarts-types** ; l'énumération E12 de l'acte 3, elle, ne dépend **que** de numpy.

### <a id="s09-6"></a>09.6 Tests de non-régression

Huit familles, chacune avec un critère chiffré **gelé en même temps que la fonction de coût** et
recopié dans `criteres_geles.json`. Lancement **depuis la racine du dépôt** :
`python -m unittest discover -s analyse/tests -v` (ne pas ajouter `-t .` ni de `__init__.py` dans
`tests/` : « Start directory is not importable »).

| Test | Ce qu'il vérifie | Critère chiffré |
|---|---|---|
| (a) `test_ajustement` | le fit retrouve $\theta$ d'une $Z(f)$ synthétique bruitée (2 % / 1°), **sur deux jeux : $Q_{ms}\approx2$ (pic large) et $Q_{ms}\approx8$ (pic étroit)** ; le repli sans SciPy donne les mêmes $\theta$ **et les mêmes σ** ; `init_depuis_courbe` converge sur **20 tirages** aléatoires ($f_s$ 25–60 Hz, $Q_{ms}$ 1–6) | chaque paramètre à **< 3 %** et **< 3 σ** ; $\chi^2$ réduit dans [0,5 ; 2] ; écart SciPy/repli **< 5·10⁻³** sur θ et sur σ ; 20/20 tirages sous 3 % |
| (b1) `test_optimiseur_continu` | **porte de validation, version théorème** : sans contrainte E12, sur 8 Ω résistif, l'optimiseur continu **doit** rendre le Butterworth analytique | $L = 18{,}0063$ mH, $C = 140{,}674$ µF, écart relatif **< 10⁻⁶** |
| (b2) `test_optimiseur_e12` | **non-régression, version discrète** : le gagnant E12 produit par le $J$ **gelé** sur 8 Ω | 18,0 mH / 150 µF \| 150 µF / 18,0 mH, $J = 0{,}947$, $f_0 = 96{,}86 \pm 0{,}01$ Hz ; variante LR2 → 27 mH / 100 µF ($Q=0{,}487$ ; analytique 25,465 / 99,472) |
| (b3) `test_degenerescence` | le terme de **somme seul** ne définit pas un raccord (§ 04.5) : il faut le terme par voie | cible plate, somme seule → 10 mH / 39 µF, c.-à-d. un LR2 à **254,9 Hz** ($J=0{,}004$) ; cible Butterworth, somme seule → 15 mH / 120 µF \| 120 µF / 22 mH ($J=0{,}056 < 0{,}211$ du catalogue) : dans les deux cas l'optimum n'est pas le raccord voulu |
| (c) `test_incertitudes` | propagation sur $f_0=1/(2\pi\sqrt{LC})$, convention GUM, corrélation, biais du Monte-Carlo | voir ci-dessous : **4,08 %** (GUM), 7,07 % (borne au pire cas), 10,0 % ($\rho=+1$), biais MC $+0{,}75\pm0{,}15$ % |
| (d) `test_series_e12` | énumération exhaustive, sans doublon, **et optimum pas au bord** | **331 776 = 24⁴** combinaisons, 576 couples/voie, 0 doublon, grille strictement croissante ; $1{,}0 < L_{opt} < 82$ mH et $10 < C_{opt} < 820$ µF |
| (g) `test_entrees` | aller-retour CSV ; colonnes dérivées recalculables ; dépouillement sur fenêtre **non entière** ; signe de la phase | aller-retour **4·10⁻⁹ relatif** ; recalcul à 10⁻⁷ Ω ; `lstsq` à **±0,5 %** sur fenêtre quelconque ; self pure +90,00°, condensateur pur −90,00° |
| (h) `test_figures` | aucune couleur `#rrggbb` résiduelle dans les SVG produits ; injection HTML | 0 hexadécimal hors repli `var(--x, #hex)` ; après injection, **0 marqueur restant** et `<svg` augmenté du nombre de figures |

**Pourquoi la porte de validation est scindée en (b1) et (b2).** Sur une charge 8 Ω résistive pure,
sans DCR ni pénalités, le problème d'optimisation **continu** *est* celui du catalogue : c'est un
théorème, et un Nelder-Mead sur $(\log L, \log C)$ y retombe à $3\cdot10^{-14}$ près, quelle que
soit la bande. Voilà ce qui mérite « si ça échoue, c'est un bug, et on n'achète rien ».
Le passage à **E12**, lui, n'est pas un théorème : c'est une **projection sur une grille**, et la
grille n'est pas stable par les symétries du problème. Le gagnant discret dépend donc légitimement
de $J$ et de la bande. Vérifié sur 8 Ω, même grille, même bande 40–250 Hz :

| $J$ utilisé | gagnant E12 |
|---|---|
| forme de chaque voie **seule** (séparable) | PB 18,0 mH / 150 µF — PH 150 µF / **15,0 mH** |
| somme **seule** | 15,0 mH / 120 µF \| 120 µF / 22,0 mH |
| **$J$ gelé** (somme + voies + phase) | **18,0 mH / 150 µF \| 150 µF / 18,0 mH**, $J = 0{,}947$ |

Le deuxième meilleur du $J$ gelé est d'ailleurs 18 mH / 150 µF \| 150 µF / **15,0 mH**
($J = 1{,}351$) : le voisin E12 est à portée. (b2) est donc un test de **non-régression** — il
protège contre une modification involontaire de $J$ — et non une vérité mathématique. Formulation à
tenir devant le jury : *« sur 8 Ω le problème continu est celui du catalogue ; le passage à E12
peut légitimement choisir un voisin différent d'une voie à l'autre, ce n'est pas un bug mais une
propriété de la grille. »* FEUILLE-DE-ROUTE § Phase 3 est à amender dans le même sens.

<!-- Le verificateur « rigueur » annoncait que le sanity check E12 ECHOUE (PH = 15 mH). Verifie sur machine : c'est vrai pour un J par voie seule, FAUX pour le J gele du § 04.5, qui redonne bien 18/150|150/18 (J = 0,9471, conforme au § 04.7). Le fond de l'objection est retenu -- l'E12 n'est pas un theoreme -- mais le contre-exemple est reattribue a son vrai J. -->

**Convention d'incertitude, gelée ici et cohérente avec le § 04.9.** Une tolérance de composant
« ±10 % » est une **loi rectangulaire** : l'incertitude-type vaut $u = a/\sqrt3 = 5{,}77$ %
(GUM, JCGM 100:2008). C'est cette lecture qui est **retenue**. La combinaison des demi-largeurs en
quadrature (7,07 %) reste citable, mais **étiquetée « borne au pire cas »** — jamais comme
incertitude-type. Sans cette convention écrite, on remplace une erreur de facteur 2 (le 11 % de la
v1) par une erreur de facteur $\sqrt3$ restée implicite, ce qu'un correcteur voit immédiatement.

$$\frac{u(f_0)}{f_0}=\frac12\sqrt{\left(\frac{u_L}{L}\right)^2+\left(\frac{u_C}{C}\right)^2
+2\rho\,\frac{u_L}{L}\frac{u_C}{C}}$$

Le facteur $\tfrac12$ vient de $\ln f_0 = -\tfrac12(\ln L + \ln C)$ ; le terme en $\rho$ est
**l'hypothèse d'indépendance rendue explicite** : elle vaut jusqu'à 3 points de pourcentage, et le
cas $\rho\neq0$ n'est pas académique (deux composants du même lot ; une self bobinée dont $L$ est
ajusté *après* mesure du $C$ réel). Réponse toute prête à « et si vos composants viennent du même
lot ? » : $\rho=+1$ donne 10,0 % au lieu de 7,07 %.

```python
class TestIncertitudeF0(unittest.TestCase):
    """(c) Propagation sur f0 = 1/(2 pi racine(LC)) : le facteur 1/2 doit y etre.
    La formule SANS 1/2 est celle du RC du 1er ordre ABANDONNE de la v1."""
    def test_c_convention_gum_et_borne(self):
        a = 0.10                                        # tolerance catalogue, DEMI-LARGEUR
        u = a/np.sqrt(3.)                               # incertitude-type GUM (loi uniforme)
        self.assertAlmostEqual(N.u_f0_relative(u, u), 0.0408, delta=5e-4)      # convention retenue
        self.assertAlmostEqual(N.u_f0_relative(a, a), 0.0707, delta=5e-4)      # borne au pire cas
        _, u_mc = N.mc_f0(18e-3, 150e-6, a, a, n=400_000, loi='uniforme', graine=7)
        self.assertAlmostEqual(u_mc, 0.0409, delta=1e-3)                       # MC <-> GUM

    def test_c_correlation_et_biais(self):
        _, u_rho1 = N.mc_f0(18e-3, 150e-6, .10, .10, n=400_000, loi='normale', graine=7, rho=1.)
        self.assertAlmostEqual(N.u_f0_relative(.10, .10, rho=1.), 0.10, delta=1e-6)
        self.assertAlmostEqual(u_rho1, 0.10, delta=0.01)          # meme lot -> 10 %, pas 7 %
        f0_nom = 1/(2*np.pi*np.sqrt(18e-3*150e-6))
        moy, _ = N.mc_f0(18e-3, 150e-6, .10, .10, n=400_000, loi='normale', graine=7)
        self.assertAlmostEqual(moy/f0_nom - 1, 0.0075, delta=0.0015)   # E[f0] != f0(E[L], E[C])

    def test_c_garde_fou_anti_v1(self):
        """La v1 annoncait 11,2 % avec u_R/R = 5 % et u_C/C = 10 % ; la MEME formule a
        10 %/10 % donne 14,1 %. Dans les deux cas elle est hors sujet : elle decrit un RC
        du 1er ordre, pas un LC. Ce qui la refute, c'est le Monte-Carlo, pas un rapport a 2."""
        for uL, uC in [(.10, .10), (.05, .20), (.20, .05)]:
            ana = N.u_f0_relative(uL, uC)
            _, mc = N.mc_f0(18e-3, 150e-6, uL, uC, n=400_000, loi='normale', graine=7)
            self.assertLess(abs(mc/ana - 1), 0.15)                  # accord analytique <-> MC
            formule_rc_1er_ordre_interdite = np.hypot(uL, uC)
            self.assertGreater(abs(formule_rc_1er_ordre_interdite/mc - 1), 0.5)   # elle, non
```

Sortie **agrégée** des vérifications effectivement exécutées dans le bac à sable (chaque ligne a été
produite par un script ; la suite `unittest` reprendra ces mêmes critères, son décompte de tests et
son chronométrage n'existeront qu'une fois `analyse/tests/` écrit) :

```
  (a1) Qms=1.75  69 pts  chi2red = 0.903 ; ecart scipy/repli 2.0e-09 (theta), 8.8e-07 (sigma)
       Re 0.23 % 0.54 s | Le 0.98 % 0.78 s | Res 0.90 % 1.47 s | fs 0.00 % 0.01 s | Qms 1.14 % 1.52 s
  (a2) Qms=8.00  69 pts  chi2red = 0.885 ; Res 2.58 % 2.12 sigma ; Qms 2.51 % 1.88 sigma  <- limite
  (a2) Qms=8.00 118 pts (1/24 d'octave sur 20-80 Hz) : Res 0.82 %, Qms 0.97 %              <- corrige
  (a3) init_depuis_courbe, 20 tirages : ecart max 1.86 %, mediane 0.70 %, 0 echec
  (b1) continu 8 ohm : L = 18.00633 mH, C = 140.6744 uF ; ecart a l'analytique 3.4e-15
  (b2) E12 8 ohm, J gele : 18.0 mH/150 uF | 150 uF/18.0 mH ; J = 0.9471 ; 331,776 comb en 1.88 s
       f0 = 96.859 Hz ; Q = R*sqrt(C/L) = 0.7303 ; f3_pb = 99.82 Hz ; f3_ph = 93.99 Hz
       2e meilleur : 18.0 mH/150 uF | 150 uF/15.0 mH (J = 1.3507)     LR2 : 27.0/100 ; Q = 0.487
  (c)  GUM (u = a/racine 3) : analytique 4.082 %  MC uniforme 4.087 %
       borne au pire cas    : 7.071 %            MC normal    7.235 %  (f0 moyen 97.60 Hz)
       correlation rho = +1 : 10.000 %           MC          10.306 %
       biais du MC : +0.77 % (attendu (3/8)(uL^2+uC^2) = 0.75 %)
       formule RC 1er ordre (INTERDITE) : 14.14 % a 10/10 ; 11.18 % a 5/10 (le « 11 % » de la v1)
  (d)  E12 : 24 L (1.0-82 mH), 24 C (10-820 uF) -> 576 couples/voie, 331,776 combinaisons
       pas de la grille L : min 1.182, max 1.250 (E12 ideal 10^(1/12) = 1.212) ; optimum hors bord
  (g)  aller-retour CSV 4.0e-09 relatif ; derivees recalculees a 9.2e-08 ohm
       dft brut sur 1.06 periode : -5.51 %   |   lstsq : -0.01 %   |   dft tronquee : +0.02 %
  (h)  SVG 60 ko ; substitutions {bg 1, bg-card 3, ink 6, ink-soft 137, accent 212, trait 55, ...}
       couleurs hexadecimales non substituees : aucune ; injection : 1 marqueur -> 0, <svg> 0 -> 1
```

Quatre remarques. Le $\chi^2$ réduit vaut **0,90**, donc les incertitudes injectées sont cohérentes
avec le bruit présent — c'est le test qui valide *à la fois* le modèle et les incertitudes (§ 03.7).
Le repli maison et SciPy diffèrent de **2·10⁻⁹** sur $\theta$ et **9·10⁻⁷** sur les σ, soit la
seule tolérance d'arrêt. La grille E12 n'est **pas exactement géométrique** (pas de 1,182 à 1,250
pour un idéal $10^{1/12}=1{,}212$), propriété de la norme IEC 60063 et non un bug — le test la
borne. Enfin, **le cas $Q_{ms}=8$ est le vrai cas** : un 18″ professionnel a un $Q_{ms}$ de 3 à 10,
donc un pic étroit ($\Delta f \approx f_s/Q_{ms}$), et au 1/12 d'octave à 40 Hz il ne reste que
**2,1 points** dans la largeur du pic contre 9,6 pour $Q_{ms}=1{,}75$. Le test passe encore (2,6 %
< 3 %), mais sans marge : d'où le défaut `densifier=(fs/2, 2fs, 24)` de `grille_log`, qui ramène
l'écart à 0,9 % pour **une vingtaine de points de plus**, soit dix minutes de banc.

**Deux fragilités connues et non résolues, à dire plutôt qu'à cacher.** (i) L'initialisation :
depuis un départ à ×1,8 des vraies valeurs les deux moteurs convergent encore, mais à ×3,0 **les
deux divergent** ($\chi^2_{red}$ = 987). C'est `init_depuis_courbe` qui protège, d'où le test (a3)
sur 20 tirages ; le multi-départ du § 03.3 reste le filet. (ii) Les σ du test (a) sont calculés sur
données synthétiques **sans systématique** ; sur données réelles, ajouter 1 % de systématique commun
ne change pas $\chi^2_{red}$ mais gonfle $u(R_e)$ — variante à ajouter au test (a) le jour où la
séparation aléatoire/systématique du § 09.3 sera exercée sur un vrai fichier.

**Tests à ajouter dès que des mesures existeront** : (e) le dépouillement du CSV d'étalonnage sur la
résistance de puissance rend $\lvert Z\rvert$ plat à ±3 % et $\varphi$ à ±2° — le § 02.8 transformé
en test ; (f) les séries $R_{ref}$ = 10 Ω et 100 Ω se recoupent dans leurs incertitudes ;
(h′) l'ajustement maison et l'outil « Thiele-Small Parameters » de REW s'accordent à **< 5 %** sur
$f_s$ et $Q_{ms}$ — une objection de jury (« pourquoi le refaire ? ») transformée en preuve ;
(i) `self_bobine` : Wheeler vérifiée contre un cas tabulé, et la **bobine de Brooks** retrouvée par
optimisation numérique du rapport géométrique, avec la loi $r\times m \approx$ cte à $L$ fixé
(tolérance [[à chiffrer sur le modèle retenu au § 05]]).

### <a id="s09-7"></a>09.7 Figures : identité Blueprint

**État des lieux.** `_gen.py` (racine du dépôt) calcule deux SVG en pur Python et les injecte
dans `presentation-finale.html`. Deux limites constatées : il n'a **aucune entrée de données**
(paramètres du haut-parleur écrits en dur, ce que la v2 interdit), et **son injection ne
fonctionne plus** — il cherche le marqueur `<!--BODE_SVG-->`, absent du HTML, puis à défaut les
motifs `aria-label="Bode Butterworth…"` et `aria-label="Impedance HP…"`, alors que le fichier
contient `…(DESACTIVE pour _gen.py)` et `aria-label="Impédance HP modèle"` **accentué** : les
deux regex rendent **0 correspondance**, le script réécrit le fichier à l'identique et affiche quand
même `OK injecté`. Faux positif silencieux, à ne pas relancer tel quel.

**Décision : ne pas étendre `_gen.py`, produire les SVG avec matplotlib — mais garder son
mécanisme d'injection, corrigé.** Écrire des `polyline` à la main était tenable pour deux courbes
illustratives, pas pour une douzaine de figures avec barres d'erreur, résidus et axes
logarithmiques. La seule chose qui faisait la valeur de `_gen.py` doit être conservée : **les
couleurs restent des variables CSS**, sinon la variante claire `css/blueprint-light.css` (export
PDF) ne recolore plus rien.

**Le piège, et il est fatal si on le rate.** Les propriétés personnalisées CSS sont propres à un
**document** : un SVG appelé par `<img src="fig-z-sub.svg">`, `<object>` ou `background-image` est
un document indépendant où `--accent` n'est défini nulle part ; la déclaration devient invalide
*at computed-value time* et la courbe disparaît (fill noir, stroke `none`). Vérifié : le SVG produit
ne contient **aucune définition** des variables. Deux corrections, cumulées :

1. **Repli dans chaque `var()`** : on écrit `var(--accent, #5fd0e0)`. Le fichier est alors
   **autonome** (juste à l'écran, en `<img>`, dans un lecteur SVG) *et* recolorable une fois
   inliné ;
2. **Inlining** : `injecter_figures.py` remplace un marqueur unique et non ambigu
   `<!--FIG:fig-z-sub-mesure-->` par le contenu du SVG — jamais par une regex sur un `aria-label`,
   qui est exactement la panne diagnostiquée ci-dessus. **L'injection échoue bruyamment** si un
   marqueur manque, et le message de succès n'est imprimé qu'après un remplacement effectif.
   (`presentation-finale.html` contient aujourd'hui 15 `<svg` inline et **zéro** `<img …svg>` : le
   HTML est déjà dans le bon format, il ne manque que les marqueurs.)

```python
BLUEPRINT = {'--bg': '#0e2230', '--bg-card': '#0c1e2b', '--ink': '#e6f1f4', '--ink-soft': '#8fb2bf',
             '--accent': '#5fd0e0', '--accent2': '#9ad6a0', '--warn': '#e0a84e',
             '--wire': '#b8d4dc', '--trait': '#28485a'}          # = css/blueprint.css (--grid exclu :
                                                                 # rgba(), jamais emis par matplotlib)
def enregistrer_svg(fig, chemin):
    """Enregistre la figure en SVG puis remplace les couleurs sentinelles par des variables
    CSS Blueprint AVEC REPLI -- var(--accent, #5fd0e0) -- pour que le fichier reste juste
    hors du document HTML. Retourne (compte par variable, hexadecimaux NON substitues)."""
    fig.savefig(chemin, format='svg', bbox_inches='tight')
    svg = open(chemin, encoding='utf-8').read(); compte = {}
    for var, hexa in BLUEPRINT.items():
        svg, n = re.compile(re.escape(hexa), re.IGNORECASE).subn('var(%s, %s)' % (var, hexa), svg)
        compte[var] = n
    open(chemin, 'w', encoding='utf-8').write(svg)
    nu = re.sub(r'var\(--[a-z0-9-]+, (#[0-9a-fA-F]{6})\)', '', svg)       # on retire les replis
    return compte, sorted(set(re.findall(r'#[0-9a-fA-F]{6}(?![0-9a-fA-F])', nu)))

def injecter_figures(chemin_html, dossier, noms):
    """Inline chaque SVG a la place de son marqueur <!--FIG:nom-->. ECHEC FATAL si un
    marqueur est absent : c'est le defaut de _gen.py (« OK injecte » sans rien injecter)."""
    html = open(chemin_html, encoding='utf-8').read(); n_avant = html.count('<svg')
    for nom in noms:
        marqueur = '<!--FIG:%s-->' % nom
        if marqueur not in html:
            raise SystemExit('injecter_figures : marqueur %s absent de %s' % (marqueur, chemin_html))
        svg = open(os.path.join(dossier, nom + '.svg'), encoding='utf-8').read()
        html = html.replace(marqueur, svg[svg.index('<svg'):])            # on jette l'en-tete XML
    open(chemin_html, 'w', encoding='utf-8').write(html)
    n_apres = html.count('<svg')
    assert n_apres - n_avant == len(noms) and '<!--FIG:' not in html
    print('injecte %d figure(s) ; <svg> : %d -> %d' % (len(noms), n_avant, n_apres))
    return n_apres - n_avant
```

**« Aucune couleur figée » n'est vrai que si `style_blueprint()` couvre tous les rcParams** : par
défaut, matplotlib écrit `#000000` pour le texte, les bords d'axes et les graduations, et cette
couleur-là échappe à la substitution. La liste à fixer, vérifiée exhaustive sur une figure
$\lvert Z\rvert$ + phase avec barres d'erreur et axes log : `figure.facecolor`, `savefig.facecolor`,
`figure.edgecolor`, `savefig.edgecolor`, `axes.facecolor`, `axes.edgecolor`, `axes.labelcolor`,
`axes.titlecolor`, `text.color`, `xtick.color`, `ytick.color`, `xtick.labelcolor`,
`ytick.labelcolor`, `grid.color`, `legend.edgecolor`, `legend.facecolor`, `legend.labelcolor`,
`patch.edgecolor`, `hatch.color`, `lines.color`, `axes.prop_cycle`, et `svg.fonttype='none'`.
C'est le test (h) qui garantit qu'on ne l'a pas oubliée — seul garde-fou contre une figure
illisible dans la variante claire à l'export PDF.

Deux autres réglages comptent. `svg.fonttype='none'` garde le texte comme texte (léger, rendu avec
les polices vendorées dans `libs/fonts/`), au prix d'un avertissement `findfont: Font family 'Inter'
not found` **par élément de texte** si la police n'est pas installée sur la machine de rendu : sans
effet sur le fichier produit, mais la métrique de placement est celle d'une police de repli, donc à
vérifier à l'œil sur les étiquettes longues. `bbox_inches='tight'` évite que les marges mangent la
diapositive. Poids typique 30–80 ko par figure (60 ko pour la figure de démonstration), compatible
avec la limite **PDF ≤ 5 Mo** du dépôt SCEI (§ 08).

**Nommage des figures**, à figer maintenant pour que le code écrive le nom que le marqueur HTML
appellera :

| Fichier `resultats/figures/` | Contenu | Acte |
|---|---|---|
| `fig-etalonnage-chaine.svg` | R, C, L connus : mesuré vs attendu, bande ±3 % | 1 |
| `fig-z-sub-mesure.svg` / `fig-z-mediums-mesure.svg` | $\lvert Z\rvert$ et $\varphi$ avec barres d'erreur, deux $R_{ref}$ | 1 |
| `fig-fit-ts-sub.svg` | 3 panneaux : module, phase, **résidus normalisés** | 2 |
| `fig-correlations-ts.svg` | matrice de corrélation des 5 paramètres (annexe) | 2 |
| `fig-catalogue-8ohm-vs-z.svg` | le filtre catalogue sur 8 Ω puis sur $Z(f)$ mesurée | 3 |
| `fig-somme-catalogue-vs-optimise.svg` / `fig-plateau-optimum.svg` | sommes prédites (cible gelée) ; coupe de $J$ : l'optimum est plat (§ 04.8) | 3 |
| `fig-self-cout-dcr.svg` | DCR, masse de cuivre et coût en fonction de $L$ ; Brooks | satellite |
| `fig-bode-electrique.svg` | banc électrique : mesuré vs prédit | 4 |
| `fig-acoustique-champ-proche.svg` | voies et somme, aux **deux niveaux gelés** | 4 |
| `fig-monte-carlo-f0.svg` | histogramme de $f_0$ (**le pôle**, § 09.4) et de l'écart RMS sous tolérances | 4/5 |
| `fig-croisement-energie.svg` | conso au repos (actif) vs pertes (passif) vs niveau | satellite |

### <a id="s09-8"></a>09.8 Reproductibilité

`analyse/tout_refaire.py` enchaîne, dans l'ordre du récit, et s'arrête au premier échec. Interface
gelée : `python analyse/tout_refaire.py [--rapide] [--sans-figures]` ; **code de retour 0** si tout
passe, **1** au premier échec, avec le nom de l'étape sur `stderr`. `--rapide` réduit le
Monte-Carlo de 400 000 à 20 000 tirages (et le dit au journal) pour la boucle de développement ;
les chiffres de l'oral se produisent **sans** `--rapide`.

1. `python -m unittest discover -s analyse/tests` — si un test tombe, **on ne va pas plus loin** ;
2. lecture de `criteres_geles.json` (recopié intégralement au journal) puis de tous les CSV de
   `mesures/`, empreinte **SHA-256** de chacun consignée ;
3. ajustement T-S → `resultats/parametres_ts.json` (θ, covariance, $\chi^2$ réduit) ;
4. énumération E12 sur $Z(f)$ identifiée → `resultats/design_optimise.json` (design + termes de $J$),
   puis `verifier_contraintes` et export de la netlist LTspice du design **et** du catalogue (§ 04.10) ;
5. Monte-Carlo sur les tolérances **et** sur la covariance des paramètres T-S (§ 04.9), puis
   génération des figures et `injecter_figures` dans les HTML de présentation ;
6. `resultats/journal.txt` : date, `sys.version`, versions des paquets, graines, empreintes des
   entrées, temps de calcul.

Chaque étape dépend de la précédente ; chacune vérifie l'existence de sa sortie amont et
échoue explicitement si elle manque, plutôt que de recalculer en silence.

**Les deux JSON versionnés portent leur provenance** : SHA-256 de leurs fichiers d'entrée, hash du
commit git, graine du générateur, date. Sans cela, un JSON périmé dans le dépôt est indiscernable
d'un JSON à jour — et ce sont les chiffres cités à l'oral.

**Règle `.gitignore`, à écrire exactement ainsi** (piège git classique : une négation est inopérante
si le **dossier** entier est exclu — vérifié) :

```gitignore
analyse/resultats/*
!analyse/resultats/parametres_ts.json
!analyse/resultats/design_optimise.json
```

Avec `analyse/resultats/` (barre oblique finale) au lieu de `analyse/resultats/*`, git n'entre
jamais dans le dossier et les deux `!` ne servent à rien : les fichiers cités à l'oral seraient
perdus.

Autres règles : **graine fixée** (`np.random.default_rng(graine)`) et écrite au journal — un
Monte-Carlo non reproductible n'est pas un résultat ; `mesures/` versionné et jamais réécrit.
Durée de la chaîne complète sur données synthétiques : **une dizaine de secondes** (ordre de
grandeur mesuré sur la machine de développement, dont ~2 s pour les onze figures et 1,9 s pour
l'énumération des 331 776 combinaisons) — l'analyse entière tient dans le temps d'une pause,
condition pour la relancer souvent. Vigilance Windows : la console
est en cp1252, donc tout script qui affiche des accents commence par
`import sys; sys.stdout.reconfigure(encoding='utf-8')`, et tous les fichiers sont lus et écrits avec
`encoding='utf-8'` explicite.

**Ce qui manque encore, et qu'il faut coder avant la phase 3** : `mesures/composants.csv` et
`optimiser_sur_stock(stock)`. Un condensateur ±20 % acheté à 150 µF en fait 163 ; le design optimal
doit être recalculé **sur les valeurs mesurées**, et l'optimisation vraiment sobre consiste à trier
et apparier le stock plutôt qu'à racheter. Bénéfice collatéral sur les incertitudes : mesurés à
1 %, $L$ et $C$ font tomber $u(f_0)/f_0$ **sous 1 %**, contre 4,1 % sur les tolérances catalogue.
De même, le critère « robustesse » suppose de lire **deux jeux de mesures par configuration** (les
deux niveaux d'écoute gelés) et de produire la comparaison : à prévoir dans le format et dans
`tout_refaire.py`, faute de quoi ce critère restera un tableau rempli à la main.

### Ce qu'il faut retenir pour l'oral

- Le code est organisé comme le récit : un module par acte (`ts_fit.py` → problème inverse,
  `optim.py` → optimisation), données brutes en lecture seule, résultats régénérables en une commande.
- Le CSV de mesure porte ses **lectures brutes** ($V_d$, $V_R$, $\Delta t$) *et* ses **conditions**
  (date, montage, $R_{ref}$ mesurée, niveau, température) : sans elles, une courbe d'impédance n'est
  pas une mesure, c'est un dessin — et sans les brutes, une erreur de $R_{ref}$ détruit la série.
- La porte de validation est **en deux étages** : sur 8 Ω résistif, l'optimiseur **continu** *doit*
  redonner le Butterworth analytique (18,0063 mH / 140,674 µF, à $10^{-6}$ près) — c'est un
  théorème, et rien ne s'achète tant qu'il échoue. Le gagnant **E12**, lui, dépend de $J$ : avec le
  $J$ gelé c'est bien 18 mH / 150 µF, mais ce n'est qu'un test de non-régression, pas une vérité.
- **Convention d'incertitude gelée** : une tolérance ±10 % est une loi rectangulaire, donc
  $u = 5{,}8$ %, donc $u(f_0)/f_0 = \frac12\sqrt{(u_L/L)^2+(u_C/C)^2} = \mathbf{4{,}1\ \%}$ (GUM) ;
  7,1 % est la **borne au pire cas**, et 11 % venait d'un RC du premier ordre hors sujet en v2. Le
  Monte-Carlo confirme les trois lectures, et $\rho=+1$ (même lot) porterait le chiffre à 10 %.
- Un estimateur mal conditionné se trompe **sans le dire** : la détection synchrone sur une fenêtre
  qui ne contient pas un nombre entier de périodes se trompe de 5 % sur $\lvert Z\rvert$. Trois
  lignes de moindres carrés suffisent à l'en empêcher — et un test le prouve.
- Le seul paquet indispensable est numpy : SciPy accélère l'ajustement, mais un
  Levenberg-Marquardt de vingt lignes le remplace — mêmes $\theta$ à $2\cdot10^{-9}$ près et mêmes
  écarts-types à $10^{-6}$ près.

### Sources

- NumPy 2.4, `numpy.genfromtxt` (option `names`, lignes commentées) : https://numpy.org/doc/stable/reference/generated/numpy.genfromtxt.html
- SciPy 1.18, `scipy.optimize.least_squares` (`trf`, `x_scale`, jacobienne au minimum) : https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html
- Matplotlib 3.11, backend SVG, paramètre `svg.fonttype` : https://matplotlib.org/stable/users/explain/text/fonts.html
- MDN, *Using CSS custom properties* — portée par document, repli `var(--x, valeur)`, invalidité
  *at computed-value time* : https://developer.mozilla.org/docs/Web/CSS/Using_CSS_custom_properties
- Python 3.13, bibliothèque standard, module `unittest` (retenu parce que `pytest` n'est installé
  ni sur le poste de travail ni, a fortiori, sur celui du lycée).
- JCGM 100:2008 (*GUM*), § 4.3.7 : tolérance de composant → loi rectangulaire, $u=a/\sqrt3$.
- IEC 60063:2015, Edition 3.0 (2015-03), *Preferred number series for resistors and capacitors*
  (séries E6, E12).
- Room EQ Wizard, aide en ligne, « Impedance Measurement » et « Thiele-Small Parameters » — export
  par *File > Export > Export measurement as text* (`.txt`/`.zma`, colonnes Freq / Z / Phase,
  en-tête commentée) [[séparateur exact à vérifier sur un export réel]].
- Dépôt : `_gen.py`, `css/blueprint.css`, `css/blueprint-light.css`, `presentation-finale.html`,
  `EXPORT-PDF.md`, `FEUILLE-DE-ROUTE.md` (phase 0 : squelette du code ; phase 3 : porte de
  validation 8 Ω) ; et les sections 01, 02, 03, 04, 05, 06 et 08 du présent document.
- Scripts exécutés pour cette section (bac à sable, non versionnés) : `sec09/noyau.py`,
  `demo_io.py`, `test_non_regression.py`, `demo_figure.py`, `injecter_demo.py` — Python 3.13.2,
  numpy 2.4.6, scipy 1.18.1, matplotlib 3.11.0, exécutés les 2026-09-09 et 2026-09-13.

## <a id="index-marques"></a>Index des points `[[à vérifier]]` et `[[à mesurer]]`

Recensement exhaustif des **163 marques** présentes dans les neuf sections, dans leur ordre
d'apparition et avec leur section d'origine. C'est la liste des trous à combler avant que ce
document cesse d'être purement théorique : tant qu'une ligne y figure, la phrase
correspondante n'est pas un résultat. Répartition : environ 58 marques de vérification, 53 marques
de mesure, le reste étant des marques d'arbitrage (« à geler », « à documenter »,
« à confirmer », « à trancher », « à chiffrer »).

> **Mise à jour du 16 septembre 2026 — le bass-reflex à deux évents.** Le constat de l'étudiant
> (sub bass-reflex à **deux évents** ; deux pavillons d'ultra-aigu **en parallèle des médiums**)
> **lève 4 marques** et **en ouvre 13**. Bilan : 154 → 163.
>
> **Levées** (la question est tranchée, le texte n'est plus conditionnel) : « type de caisse à
> confirmer » (§ 02.6), « à documenter : clos ou bass-reflex » (§ 03, préambule), « à documenter
> — trente secondes, regarder s'il y a un évent » (§ 04.2), « si bass-reflex, type de caisse à
> documenter » (§ 07.3).
>
> **Ouvertes** — ce sont les quatre relevés qui bloquent désormais le plus de choses, par ordre
> d'urgence :
>
> | À faire | Ce que cela débloque | Coût |
> |---|---|---|
> | **Cotes des deux évents** (diamètre au pied à coulisse, longueur, entraxe) [[à mesurer]] | la prédiction géométrique de $f_b$ (§ 01.10 bis) et la pondération de sommation acoustique (§ 07.3) | 10 min |
> | **Volume net de la caisse** [[à mesurer]] | la même prédiction — et c'est le **terme dominant** de son incertitude (1,44 % sur 1,5 %) | 20 min |
> | **$f_b$** [[à mesurer]] | la borne basse de sécurité au niveau fort (§ 02.6, § 07.11), le paramètre de départ de `Z_bassreflex8`, et le contrôle croisé du § 03.7 | mesure d'impédance (phase 1) |
> | **Condensateur en série avec les pavillons : oui ou non ?** [[à vérifier]] | la charge réelle du passe-haut (12 Ω ou 5 Ω à 100 Hz, § 02.6 et § 04.2) et le risque matériel pendant les balayages (§ 07.11) | ouvrir le bornier, 5 min |
>
> Les trois premiers se font **avant** la première mesure d'impédance, sinon la prédiction
> géométrique cesse d'en être une. Le quatrième se fait **avant** le premier balayage au niveau
> fort.

**11 de ces marques se trouvent à l'intérieur d'un extrait de code** : ce sont des
commentaires Python laissés volontairement sans accents, pour ne pas dépendre de l'encodage
du poste. Elles portent la mention *(code)* et se lèvent dans le script, pas dans le texte.
3 autres sont dans un commentaire HTML — une note de rédaction invisible au rendu, qui
garde la trace d'un arbitrage ; elles portent la mention *(note)* et ne bloquent aucun
résultat.

| Section | Marques |
|---|---:|
| [01. Modèle électroacoustique du haut-parleur et impédance Z(f)](#s01) | [10](#idx-01) *(+4)* |
| [02. Mesure de l'impédance Z(f) : montage, formules, incertitudes](#s02) | [24](#idx-02) *(+2)* |
| [03. Problème inverse : identification des paramètres de Thiele-Small](#s03) | [13](#idx-03) *(1 levée, 1 ouverte)* |
| [04. Filtre de raccord sur charge réelle et formulation de l'optimisation](#s04) | [17](#idx-04) *(inchangé : 1 levée, 1 ouverte)* |
| [05. Conception de la self : inductance, cuivre, pertes, fabrication](#s05) | [23](#idx-05) |
| [06. Pertes, compression thermique et croisement énergétique passif / actif](#s06) | [23](#idx-06) |
| [07. Validation acoustique : protocole de mesure au micro à 100 Hz](#s07) | [29](#idx-07) *(+3)* |
| [08. Cadre du TIPE (SCEI, session 2027) et attentes du jury](#s08) | [17](#idx-08) |
| [09. Architecture du code d'analyse Python (dossier `analyse/`)](#s09) | [7](#idx-09) |
| **Total** | **163** |

### <a id="idx-01"></a>Marques de la section 01

| Sous-section | Marque | Contexte |
|---|---|---|
| [§ 01.2](#s01-2) | `[[à vérifier sur l'appareil du lycée, cordons court-circuités]]` | `…R_e$ et dans $R_{es}=R_eQ_{ms}/Q_{es}$. Or les cordons d'un multimètre de lycée valent co… (…) , soit **4 à 10 % de $R_e\approx5$ Ω** — et…` |
| [§ 01.8](#s01-8) | `[[à mesurer]]` | `…. Le « sextuple » est à lire comme une **borne basse plausible**, à remplacer par le rapp… (…) . **Ce que le filtre voit dans sa propre ban…` |
| [§ 01.8](#s01-8) | `[[à recalculer]]` *(note)* | `…ompte (f_x peu sensible, forme tres sensible) ; la magnitude, elle, depend de la position… (…) sur le jeu identifie en phase 2. --> Enfin,…` |
| [§ 01.10](#s01-10) | `[[à mesurer]]` **(nouvelle, 16 sept. 2026)** | `…Restent à relever : **dimensions des deux évents et volume de la caisse** (…) , et donc $f_b$…` — entrée de la prédiction du § 01.10 bis, à relever **avant** la première mesure d'impédance |
| [§ 01.10](#s01-10) | `[[à mesurer]]` **(nouvelle, 16 sept. 2026)** | `…dimensions des deux évents et volume de la caisse [[à mesurer]], et donc $f_b$ (…) — ce sont les entrées de la prédiction du § 01.10 bis.` — $f_b$ vient de la mesure d'impédance (creux) et de l'ajustement, et se recoupe avec la géométrie (§ 03.7, critère 9) |
| [§ 01.10 bis](#s01-10bis) | `[[à vérifier : les deux évents de l'enceinte ont-ils les mêmes cotes ?]]` **(nouvelle)** | `…(iv) Elle suppose les deux évents **identiques** : s'ils ne le sont pas, $N\,S_p/\ell_{\text{eff}}$ se remplace par $\sum_i S_{p,i}/\ell_{\text{eff},i}$ (…)` |
| Sources | `[[à recouper sur l'édition papier au CDI si le jury demande la référence de la constante]]` **(nouvelle)** | `…la constante numérique y est donnée dans un système d'unités particulier (…) : la nôtre est redémontrée depuis $f_b=\frac{c}{2\pi}\sqrt{NS_p/(V_b\ell_{\text{eff}})}$ et vaut 94 169 pour $c=344$ m/s…` |
| [§ 01.13](#s01-13) | `[[à mesurer]]` | `…a phase 2, les colonnes $f_s$, $Q_{ms}$, $Q_{es}$, $R_e$, $L_e$ seront remplacées par les… (…) ; $M_{ms}$, $Bl$, $S_d$ et $V_{as}$ **rester…` |
| [§ 01.13](#s01-13) | `[[à mesurer]]` | `…ssible pour le passe-haut $C_2$ série / $L_2$ parallèle calculé pour 8 Ω. Cela ne se saur… (…) , mais le volume de la chambre médium est à…` |
| Sources | `[[à vérifier sur le texte de la norme si le jury le demande]]` | `…*) : définition de l'impédance nominale par le minimum du module (≥ 80 % de $Z_{nom}$). C… (…) . - Datasheets constructeurs utilisées pour…` |

### <a id="idx-02"></a>Marques de la section 02

| Sous-section | Marque | Contexte |
|---|---|---|
| [§ 02.1](#s02-1) | `[[à mesurer]]` | `…$R_e \approx 6{,}4\ \Omega$, $Z_{pic} \approx 45$–60 Ω, calculé). La valeur réelle sera f… (…) . Deux conséquences à assumer publiquement :…` |
| [§ 02.1](#s02-1) | `[[à mesurer]]` | `…culée sur des jeux de paramètres plausibles va de **13 à 32**, pas 6. C'est un **résultat… (…) ; la problématique devra être ajustée après…` |
| [§ 02.2](#s02-2) | `[[à vérifier sur l'oscilloscope du lycée : la voie MATH est-elle acceptée comme **source** des mesures automatiques de délai/phase ? Sur beaucoup d'appareils d'entrée de…` | `…r la sortie de MATH**, c'est-à-dire précisément sur la tension qui porte l'amplification… (…) **Où entre le facteur d'appariement.** Seul…` |
| [§ 02.4](#s02-4) | `[[à vérifier sur le GBF du lycée]]` | `…*Niveau et courant.** Un GBF de laboratoire a ~50 Ω de sortie et fournit typiquement 10 V… (…) . Courants et puissances (RMS) : \| $V_{GBF}$…` |
| [§ 02.4](#s02-4) | `[[à vérifier]]` | `…igh-Z / 50 Ω et mesurer à l'oscilloscope la tension réellement délivrée, ne jamais se fie… (…) .* Une résistance étalon de 1 W (ou 2 W) suf…` |
| [§ 02.5](#s02-5) | `[[à confirmer]]` | `…l'amortissement : ≈ 30 µm pour $V_d = 150$ mV, $Bl \approx 20$ N/A et $f = 40$ Hz [ordre… (…) ]. Le réajustement du niveau **est** la prot…` |
| [§ 02.6](#s02-6) | ~~`[[type de caisse à confirmer — donnée manquante identifiée dans CLAUDE.md]]`~~ **LEVÉE le 16 sept. 2026** | tranchée : bass-reflex à deux évents. Le § 02.6 porte désormais la règle de densification à deux pics et un creux, et non plus une alternative conditionnelle |
| [§ 02.6](#s02-6) | `[[à mesurer]]` **(nouvelle)** | `…il est possible qu'un seul $R_{ref}$ suffise désormais — à trancher sur les valeurs réelles (…)` — la dynamique de $\lvert Z\rvert$ en bass-reflex (6 à 64 Ω sur le modèle) n'est pas celle du cas clos, le compromis du § 02.4 est à rejouer |
| [§ 02.6](#s02-6) | `[[$X_{max}$ du 18″ à lire sur la datasheet — la règle ci-dessus est qualitative tant qu'on ne l'a pas]]` **(nouvelle)** | `…**Contrôle visuel obligatoire** avant tout balayage au niveau fort (…)` — borne basse de sécurité sous $f_b$ |
| [§ 02.6](#s02-6) | `[[à vérifier auprès de l'étudiant / en ouvrant le bornier]]` **(nouvelle)** | `…**y a-t-il un condensateur en série avec les pavillons ?** (…) C'est la protection classique du premier ordre.` — avec : $-0{,}9$ à $-2{,}6$ dB sur $\lvert Z\rvert$ du bloc, **pas négligeable** ; sans : $-17{,}9$ dB, sous les 4 Ω du E-800, **et** risque matériel au niveau fort |
| [§ 02.7](#s02-7) | `[[reporter les spécifications de l'oscilloscope du lycée]]` | `…gain DC **±3 % de la pleine échelle** pour les calibres ≥ 10 mV/div, ±4 % en dessous, bas… (…) : \| Source \| Valeur \| Remède / commentaire \|…` |
| [§ 02.8](#s02-8) | `[[précision à vérifier]]` | `…og de $\|Z\|$ dans $-1{,}00 \pm 0{,}03$ ; (d) valeur absolue compatible avec le capacimètre… (…) ou la tolérance nominale (±10–20 %). Un élec…` |
| [§ 02.8](#s02-8) | `[[a mesurer]]` *(code)* | `…Hz - 2 kHz (mediums) : {len(grille_log(10,2000,3))} pts") for f_pic, Q in ((40.0, 5.0), (… (…) : f_pic et Q lus en passe 1 g3 = grille_pic(…` |
| [§ 02.8](#s02-8) | `[[a mesurer]]` *(code)* | `…g2(1+1/Q)*24:.1f} points") print("\nHauteur du pic : Zpic = Re (1 + Qms/Qes) [ordres de g… (…) ]") for nom, Re, Qms, Qes in (("18\" pro, Qm…` |
| [§ 02.8](#s02-8) | `[[a mesurer]]` *(code)* | `…,93 %) n'y placerait que 2.0 points Hauteur du pic : Zpic = Re (1 + Qms/Qes) [ordres de g… (…) ] 18" pro, Qms/Qes = 10 Re = 5.3 ohm -> Zpic…` |
| [§ 02.9](#s02-9) | `[[à faire dès réception, modèle de carte son à documenter.]]` | `…on de sortie à vide $V_0$, puis sur une charge connue $R_c = 100\ \Omega$ ; alors $Z_s =… (…) **Jig derrière l'amplificateur E-800** — seu…` |
| [§ 02.9](#s02-9) | `[[à vérifier sur l'E-800 : sortie en pont ou masse commune ? Si pont, aucune borne n'est à la masse et le diviseur doit être flottant.]]` | `…de carte son ; elles ne conduisent jamais en fonctionnement normal et clampent en cas d'e… (…) **Limites** : impédance de sortie et courant…` |
| [§ 02.9](#s02-9) | `[[à vérifier]]` | `…, négligeable sur 10–200 Ω) ; couplage capacitif des entrées/sorties → atténuation et dép… (…) ; **le bruit dominant est acoustique et vibr…` |
| [§ 02.10](#s02-10) | `[[médiums en chambre séparée ?]]` | `…b$. Ce décalage par rapport à la datasheet n'est pas une erreur. - **Autre haut-parleur d… (…) : un haut-parleur voisin en circuit ouvert o…` |
| [§ 02.12](#s02-12) | `[[à mesurer]]` | `…{CH2}$ (V) \| $\Delta t$ (µs, signe) \| remarques \| \|---\|---\|---\|---\|---\|---\|---\|---\|---\|--… (…) \| 100,3 \| A \| \| \| \| \| \| \| \| \| \| \| … \| \| \| \|…` |
| [§ 02.12](#s02-12) | `[[à vérifier au premier export]]` | `…. - **Convention de signe de $\varphi$** : positif = inductif (§ 02.1). REW exporte avec… (…) . - **Le fit de l'acte 2 est pondéré par $1/…` |
| Sources | `[[à vérifier]]` | `…1054Z-Specification.pdf (spécification prise comme oscilloscope pédagogique de référence… (…) ). - JCGM 100:2008, *Évaluation des données…` |
| Sources | `[[paramètres du HP réel à confirmer]]` | `…tres catalogue plausible pour un 18″ 8 Ω de sonorisation, pas comme description du haut-p… (…) . - Coefficient de température du cuivre rec…` |
| Sources | `[[référence exacte à citer]]` | `…{,}93\cdot10^{-3}\ \mathrm{K^{-1}}$ à 20 °C : valeur tabulée usuelle (tables de physique… (…) . - V. Dickason, *The Loudspeaker Design Coo…` |
| Sources | `[[édition et chapitre à préciser — référence payante, citée pour mémoire ; les deux sources libres ci-dessus la remplacent pour le lecteur]]` | `…on, *The Loudspeaker Design Cookbook* : mesure d'impédance par résistance série, paramètr… (…) . - Programme de physique PTSI/PT : régime s…` |

### <a id="idx-03"></a>Marques de la section 03

| Sous-section | Marque | Contexte |
|---|---|---|
| préambule | ~~`[[à documenter : clos ou bass-reflex]]`~~ **LEVÉE le 16 sept. 2026** | tranchée : **bass-reflex à deux évents**. Le modèle par défaut devient `Z_bassreflex8` (8 paramètres, $\alpha$ libre) ; le modèle à 5 paramètres reste au dossier comme **contrôle de routine** (critère 0 bis du § 03.7), et le test D du § 03.4 devient une exécution systématique et non un cas exotique |
| [§ 03.1](#s03-1) | `[[à faire en phase 2]]` **(nouvelle)** | `…Repli, si 'Z_bassreflex8' ne converge pas : 'Z_deux_pics' (nom du dépôt (…) ; le script de démonstration du § 03.4 l'appelle 'Z_2pics' — même modèle, deux noms, à unifier (…)` |
| [§ 03.1](#s03-1) | `[[à mesurer]]` | `…e Thomas \| \|---\|---\|---\|---\| \| $R_e$ \| plancher de $\lvert Z\rvert$ sous le pic ; = résis… (…) (multimètre) \| \| $L_e$ \| remontée de $\lvert…` |
| [§ 03.1](#s03-1) | `[[à mesurer]]` | `…mètre) \| \| $L_e$ \| remontée de $\lvert Z\rvert$ et phase $> 0$ en haut de bande \| 0,5 à 3… (…) \| \| $R_{es}$ \| $Z_{max} - R_e$ \| dizaines d'…` |
| [§ 03.1](#s03-1) | `[[à mesurer]]` | `…haut de bande \| 0,5 à 3 mH (gros woofers) \| [[à mesurer]] \| \| $R_{es}$ \| $Z_{max} - R_e$… (…) \| \| $f_s$ \| position du pic (en caisse : $>…` |
| [§ 03.1](#s03-1) | `[[à mesurer]]` | `…aines d'ohms \| [[à mesurer]] \| \| $f_s$ \| position du pic (en caisse : $> f_s$ datasheet)… (…) en caisse \| \| $Q_{ms}$ \| finesse du pic \| 2…` |
| [§ 03.1](#s03-1) | `[[à mesurer]]` | `…se : $> f_s$ datasheet) \| 20 à 50 Hz (18″) \| [[à mesurer]] en caisse \| \| $Q_{ms}$ \| fines… (…) \| Les ordres de grandeur sont des valeurs us…` |
| [§ 03.5](#s03-5) | `[[valeur à mesurer en phase 1]]` | `…dérive thermique à comptabiliser, pas à ignorer ; retrancher la résistance des cordons de… (…) . **Ce que l'acte 3 reçoit vraiment.** L'obj…` |
| [§ 03.6](#s03-6) | `[[à produire en phase 3]]` | `…le chaînon qui ferme la boucle entre l'acte 2 et l'acte 3, et il justifiera *a posteriori… (…) . ### <a id="s03-7"></a>03.7 Critères de val…` |
| [§ 03.7](#s03-7) | `[[datasheet à obtenir]]` | `…n caisse close supérieure au $f_s$ datasheet ; $Q_{ms}$, $Q_{es}$ dans les ordres de gran… (…) . 7. **Test à blanc du code**, exécuté sur d…` |
| [§ 03.8](#s03-8) | `[[à faire si le temps le permet]]` | `…s de différences finies à 8. C'est un exercice de niveau prépa, et un argument cohérent a… (…) . > **Ce qu'il faut retenir pour l'oral** >…` |
| Sources | `[[attribution à confirmer sur le texte original : les scans AES accessibles en ligne sont des images sans couche texte — à demander au CDI]]` | `…s})$ est par ailleurs confirmée par une source industrielle indépendante et redémontrée e… (…) - J. Vanderkooy, « A Model of Loudspeaker Dr…` |
| Sources | `[[filière à confirmer : PT ou PSI]]` | `…page 6) : voie PT https://prepas.org/ups.php?document=96 , voie PSI https://prepas.org/up… (…) *(L'URL upsti.fr utilisée en v1 renvoie une…` |
| Sources | `[[semestre exact à vérifier]]` | `…ps://sti.eduscol.education.fr/textes/programme-dinformatique-du-tronc-commun-cpge-ptsi-pt… (…) . - 'archive-v1/_gen.py' (dépôt du projet, l…` |

### <a id="idx-04"></a>Marques de la section 04

| Sous-section | Marque | Contexte |
|---|---|---|
| préambule | `[[à mesurer]]` | `…archive-v1/_gen.py', jamais mesurés). **Rien n'a été mesuré sur l'enceinte de Thomas** :… (…) sera remplacée par les résultats des phases…` |
| [§ 04.2](#s04-2) | `[[à mesurer]]` | `…,5 mH \| 30 Ω \| 60 Hz \| 3,0 \| 36,4 Ω à 60 Hz \| 12,2 Ω ∠−42,2° \| 5,6 \| Valeurs réelles du s… (…) (phase 1) ; le « simple au sextuple » de la…` |
| [§ 04.2](#s04-2) | ~~`[[à documenter — trente secondes, regarder s'il y a un évent]]`~~ **LEVÉE le 16 sept. 2026** | il y en a **deux**. Le § 04.2 porte désormais le chiffrage sur charge bass-reflex : bosse $+12{,}6$ dB, $\min\lvert Z_{in}\rvert = 2{,}66$ Ω (contre 8,52 Ω sur 8 Ω résistifs), et **deux** points bas de $\lvert Z_{in}\rvert$ au lieu d'un |
| [§ 04.2](#s04-2) | `[[à vérifier]]` **(nouvelle)** | `…Deux pavillons d'ultra-aigu sont câblés **en parallèle** des médiums (…) Selon qu'un condensateur de protection les découple ou non (…), $\lvert Z\rvert$ du bloc à 100 Hz passe de 29,3 Ω à 26,3–21,8 Ω ou à **3,7 Ω**…` — même marque qu'au § 02.6 et au § 07.11, à lever une fois pour toutes en ouvrant le bornier |
| [§ 04.2](#s04-2) | `[[à mesurer — écart entre le centre du 18″ et celui du bloc médiums]]` | `…ruban dès maintenant** (cinq minutes) et mettre $e^{-j\omega\tau}$ avec ce $\tau$ dans la… (…) . Attention : une mesure en **champ proche**…` |
| [§ 04.2](#s04-2) | `[[à mesurer]]` | `…iltre**. Il faut soit un gain relatif en variable, soit un L-pad sur la voie la plus sens… (…) (phase 1) — conséquence énoncée, à ne pas ou…` |
| [§ 04.4](#s04-4) | `[[à vérifier]]` | `…nent à pleine puissance exactement à $f_s$.) Coût et matière multipliés par deux ou trois… (…) sur devis) — exactement ce que le thème « so…` |
| [§ 04.5](#s04-5) | `[[à relever avant la phase 3]]` | `…. Le problème réel est donc **mixte** : $L$ continu, $C$ discret sur le **catalogue effec… (…) . Les 331 776 combinaisons restent la borne…` |
| [§ 04.5](#s04-5) | `[[à vérifier sur datasheet]]` | `…I_C\rvert\le I_{ripple,max}$ ; un chimique bipolaire de 150 µF n'est pas garanti aux 9,4… (…) . (b) *Section de fil / échauffement* de cha…` |
| [§ 04.5](#s04-5) | `[[à mesurer]]` | `…tère gelé « pertes d'insertion ». Elle est **mesurable gratuitement** avec le jig d'impéd… (…) , puis à ajouter comme paramètre de $H_{PH}$…` |
| [§ 04.5](#s04-5) | `[[à mesurer]]` | `…câbles et connexions s'ajoutent directement à $r_1$ et $r_2$ et sont du même ordre (quelq… (…) — un fil de 2,5 mm² de 3 m aller-retour, c'e…` |
| [§ 04.6](#s04-6) | `[[a corriger, cf. 04.5]]` *(code)* | `…EE [ordre de grandeur] def prix_L(L): return 4.0 + 1.2*L/1e-3 # euros -- INCOHERENT avec… (…) def prix_C(C): return 1.0 + 0.05*C/1e-6 # eu…` |
| [§ 04.6](#s04-6) | `[[a verifier]]` *(code)* | `…corriger, cf. 04.5]] def prix_C(C): return 1.0 + 0.05*C/1e-6 # euros, electrolytique bipo… (…) # ---------- 5. Fonction de cout ----------…` |
| [§ 04.6](#s04-6) | `[[a rendre UNILATERAL sous fs -- cf. 04.5]]` *(code)* | `…xis=1)) # forme de chaque voie vs sa cible V2 = np.sqrt(np.mean((dB(Hph) - dB(Hc_ph*Gm))*… (…) V_ref = np.sqrt(P_ref*8.)…` |
| [§ 04.8](#s04-8) | `[[à mesurer]]` | `…§ 04.4 ne repose donc plus sur un seul essai. Réserve : $R_z$ et $C_z$ dérivent de $R_e$… (…) . **Robustesse au modèle de self** (contrain…` |
| [§ 04.10](#s04-10) | `[[à exécuter sous LTspice en phase 3]]` | `…10 10k .end ''' Valeurs de référence à retrouver (calculées par le code de la section, 'v… (…) **, la superposition des deux courbes ferman…` |
| [§ 04.11](#s04-11) | `[[à mesurer]]` | `…e phénomène se lit « −4,6 % », « +5 % » ou « −0,3 % » selon la convention. **D'où : mesur… (…) , et si elle dépasse quelques centaines d'oh…` |
| Sources | `[[à vérifier : édition et pages]]` | `…speaker Design Cookbook*, Audio Amateur Press — formules usuelles du Zobel et de la compe… (…) . - NumPy 2.4.6 ; SciPy 1.18.1 ('minimize' N…` |

### <a id="idx-05"></a>Marques de la section 05

| Sous-section | Marque | Contexte |
|---|---|---|
| préambule | `[[à mesurer]]` | `…oduit, citées et étiquetées. **Rien n'a été bobiné ni mesuré** : toute grandeur de l'ence… (…) . Scripts réellement exécutés (scratchpad 's…` |
| [§ 05.1](#s05-1) | `[[à mesurer]]` | `…lf ne se contente pas de perdre de la puissance, elle **désamortit le grave**. Avec $R_e\… (…) , $r=1{,}6\ \Omega$ donne $Q'_{es}=1{,}25\,Q…` |
| [§ 05.5](#s05-5) | `[[à vérifier : IEC 60317, tables du fournisseur]]` | `…\text{m}=\rho_{Cu}/A$, $\text{g/m}=\rho_m A$. Surépaisseur d'émail grade 2 prise à 0,08 m… (…) . \| $d$ nu (mm) \| $d$ émaillé (mm) \| section…` |
| [§ 05.8](#s05-8) | `[[ordre de grandeur à geler avec les critères]]` | `…nsité de courant admissible pour un conducteur enterré sous ~20 couches : **2 à 3 A/mm²**… (…) . Les deux niveaux d'écoute restant à geler,…` |
| [§ 05.8](#s05-8) | `[[à vérifier par devis : les distributeurs consultés ne publient pas leur gamme de diamètres]]` | `…** qui bloque : $d=1{,}9$ à 2,9 mm de fil émaillé n'est ni bobinable à la main, ni couram… (…) . Ces lignes ne sont pas des designs, ce son…` |
| [§ 05.9](#s05-9) | `[[ordre de grandeur NON SOURCE, a remplacer par un devis]]` *(code)* | `…760.0 # kg.s^-3/2, section 05.6 (+/- 10 %, dominee par le remplissage k) PRIX_KG = 25.0 #… (…) J_MAX = 3.0 # A/mm2 [[a geler avec les crite…` |
| [§ 05.9](#s05-9) | `[[a geler avec les criteres]]` *(code)* | `…0 # EUR/kg [[ordre de grandeur NON SOURCE, a remplacer par un devis]] J_MAX = 3.0 # A/mm2 (…) D_MAX = 1.5e-3 # m, plus gros fil approvisio…` |
| [§ 05.9](#s05-9) | `[[a verifier par devis]]` *(code)* | `…3.0 # A/mm2 [[a geler avec les criteres]] D_MAX = 1.5e-3 # m, plus gros fil approvisionna… (…) masse_L = lambda L, r: K_CU*(L/r)**1.5…` |
| [§ 05.10](#s05-10) | `[[à remplacer par un devis avant l'achat de la phase 4]]` | `…ute cette section est donc un **ordre de grandeur NON SOURCÉ** (cuivre matière ≈ 9–10 €/k… (…) . **Tous les montants en € de cette section…` |
| [§ 05.11](#s05-11) | `[[à mesurer]]` | `…e de la Jantzen 6595 fait 312 cm³ **cuivre compris**, pour un minimum calculé de 119 cm³… (…) ci-dessous n'est donc pas une curiosité, c'e…` |
| [§ 05.11](#s05-11) | `[[à mesurer]]` | `…filtre optimisé. Le noyau reste une **perspective** — et le meilleur satellite disponible… (…) **$L$ à 0,1 A et à 5 A sur une self à noyau…` |
| [§ 05.12](#s05-12) | `[[à vérifier]]` | `…rer le filtre catalogue et le filtre optimisé **sur le même objet physique**, donc sans b… (…) : la prise doit être prise sur la couche, pa…` |
| [§ 05.12](#s05-12) | `[[à confirmer par l'expérience sur la première self]]` | `…, l'écart entre 8 h et 2 jours de travail n'est pas un détail de planning en phase 4 (déc… (…) - **Comptabilité matière honnête** : le tabl…` |
| [§ 05.12](#s05-12) | `[[à chiffrer sur la facture réelle]]` | `…ontreplaqué + tube), vernis, colliers, cosses : **quelques centaines de grammes et quelqu… (…) . Pour le tableau comparatif final du critèr…` |
| [§ 05.13](#s05-13) | `[[à vérifier sur la notice du multimètre du lycée]]` | `…e contre-vérification. Si on l'emploie : mesurer d'abord $C$ au capacimètre du multimètre… (…) ), *puis* en déduire $L$, et recouper avec d…` |
| [§ 05.14](#s05-14) | `[[à chiffrer sur le filtre réel]]` | `…$ dB sur 14 Ω, et surtout $Q'_{es}$ qui monte encore). Souder, pas visser ; mesurer $r$ *… (…) **Précautions** : mesurer à froid, noter la…` |
| [§ 05.15](#s05-15) | `[[à mesurer en phase 4 — c'est un point dur du modèle, pas un détail]]` | `…})$ et non $r_{dc}$** — et c'est alors un excellent résultat expérimental, et une excelle… (…) **Perspective** (une ligne, si le jury pose…` |
| [§ 05.15](#s05-15) | `[[ordre de grandeur, à mesurer si besoin]]` | `…nter-spires d'un bobinage de 454 spires multicouche place l'**auto-résonance** vers quelq… (…) — sans objet à 100 Hz, mais c'est la limite…` |
| Sources | `[[à vérifier]]` | `…: <https://nvlpubs.nist.gov/nistpubs/jres/7/jresv7n2p289_A2b.pdf> (pagination de début vé… (…) ). - Grover, F. W., *Inductance Calculations…` |
| Sources | `[[à vérifier sur la fiche constructeur]]` | `…me point de validation, **à la valeur cible** (§ 05.7), et argument de marché (§ 05.10).… (…) . - Fiche produit Jantzen Audio 6595, 18 mH…` |
| Sources | `[[à remplacer par un devis]]` | `…de transformation », sur devis) : les **25 €/kg** de cette section sont un ordre de grand… (…) . Vérifier au passage que **le fil existe au…` |
| Sources | `[[à vérifier : valeurs exactes pour 1,0 / 1,4 / 2,0 mm]]` | `…, *Specifications for particular types of winding wires* — dimensions et surépaisseur d'é… (…) . - Dépôt : 'FEUILLE-DE-ROUTE.md' (phases 3…` |
| Sources | `[[a verifier par devis]]` *(note)* | `…ibuteurs consultes ne publient pas leur gamme de diametres. La contrainte d <= d_dispo es… (…) plutot qu'avec une borne chiffree presentee…` |

### <a id="idx-06"></a>Marques de la section 06

| Sous-section | Marque | Contexte |
|---|---|---|
| préambule | `[[à mesurer]]` | `…oit calculées à partir d'hypothèses explicites, soit des ordres de grandeur étiquetés, so… (…) '. Les scripts cités ont été exécutés (numpy…` |
| préambule | `[[à identifier en phase 2]]` | `…as}[\text{L}]}{Q_{es}}\qquad(c=345\ \text{m/s}).$$ Pour des paramètres plausibles d'un 18… (…) ' — ici $f_s=40$ Hz, $V_{as}=200$ L, $Q_{es}…` |
| [§ 06.2](#s06-2) | `[[à mesurer]]` | `…e budget prévoit des électrolytiques bipolaires de 150 µF, dont l'ESR est de l'ordre de 0… (…) ' — non négligeable devant $r$, croissante à…` |
| [§ 06.2](#s06-2) | `[[à trancher en phase 3]]` | `…pprox$ cte à $L$ fixée n'est établie que pour la DCR : elle ne vaut telle quelle que pour… (…) '. **Câble et impédance de sortie de l'ampli…` |
| [§ 06.2](#s06-2) | `[[à calculer sur le câblage réel]]` | `…text{câble}}$, avec $R_{\text{câble}}=2\ell\rho/S\approx0{,}05$ à $0{,}15$ Ω pour quelque… (…) ' et $R_g$ l'impédance de sortie du E-800 (f…` |
| [§ 06.3](#s06-3) | `[[à documenter]]` | `…une perte qui achète de l'immunité à $\underline Z(f)$ Les deux voies n'ont pas la même s… (…) '). En passif, la voie la plus sensible (a p…` |
| [§ 06.5](#s06-5) | `[[ordres de grandeur]]` *(code)* | `…st la puissance dissipée **à froid** : '''python Rth1, tau1 = 2.0, 10.0 # bobine -> aiman… (…) Rth2, tau2 = 0.5, 20*60.0 # aimant -> ambian…` |
| [§ 06.5](#s06-5) | `[[ordres de grandeur]]` *(code)* | `…obine -> aimant : K/W, s [[ordres de grandeur]] Rth2, tau2 = 0.5, 20*60.0 # aimant -> amb… (…) C1, C2 = tau1/Rth1, tau2/Rth2 # capacites th…` |
| [§ 06.5](#s06-5) | `[[à mesurer en phase 4]]` | `…pprox20$ à 60 J/K et, à $R_{tv}=2$ K/W, **$\tau_v$ de l'ordre de 40 s à 2 min**. On retie… (…) ', ordre de grandeur 10 s (petit HP, Klippel…` |
| [§ 06.5](#s06-5) | `[[à geler avant toute mesure]]` | `…res qui comptent sont ceux des **deux niveaux gelés en phase 0** — $P_{\text{faible}}$ et… (…) '. En attendant, voici le même modèle balayé…` |
| [§ 06.5](#s06-5) | `[[à mesurer]]` | `…es montent → $r$ monte). Ordre de grandeur : 2 W dissipés dans une self à l'air libre ($R… (…) ') → +40 K → $r$ +16 %. **Le modèle de coût…` |
| [§ 06.6](#s06-6) | `[[à vérifier sur le multimètre du lycée : calibre le plus bas et résolution]]` | `…ur une lecture de 6,5 Ω) : ±1,6 K sur $\Delta T$, largement suffisant pour comparer à la… (…) '. **Repli sans achat** : injecter un couran…` |
| [§ 06.6](#s06-6) | `[[à vérifier]]` | `…ais le E-800 est spécifié 20 Hz–20 kHz : un pilote à 1 Hz sera probablement atténué par l… (…) '. On peut contourner en n'exploitant que la…` |
| [§ 06.7](#s06-7) | `[[à mesurer]]` | `…s) \| pertes à vide souvent supérieures à l'AOP lui-même (quelques dixièmes de W à ~2 W) \|… (…) ' \| \| pré-ampli SX-801 \| présent dans les de…` |
| [§ 06.7](#s06-7) | `[[à mesurer]]` | `…eur, '[[à mesurer]]' \| \| pré-ampli SX-801 \| présent dans les deux scénarios → s'annule da… (…) ' pour info \| \| t.amp E-800, **veille activé…` |
| [§ 06.7](#s06-7) | `[[à mesurer]]` | `…sans signal depuis > 15 min \| l'ampli bascule seul en veille : c'est l'état le plus proba… (…) ' — poste décisif \| \| t.amp E-800, **veille…` |
| [§ 06.7](#s06-7) | `[[à mesurer]]` | `…désactivée**, allumé au repos \| typiquement quelques dizaines de W pour un ampli de scène… (…) ' — borne supérieure \| \| t.amp E-800 éteint…` |
| [§ 06.7](#s06-7) | `[[à mesurer]]` | `…[[à mesurer]]' — borne supérieure \| \| t.amp E-800 éteint mais branché \| consommation rési… (…) ' \| \| crossover actif du commerce actuelleme…` |
| [§ 06.7](#s06-7) | `[[à mesurer]]` | `…mation résiduelle du transfo \| '[[à mesurer]]' \| \| crossover actif du commerce actuelleme… (…) ' (point de comparaison gratuit) \| **Le E-80…` |
| [§ 06.7](#s06-7) | `[[à vérifier : puissance admissible de la résistance 8 Ω du lycée]]` | `…xt{voie}}/(P_{\text{secteur}}-P_{\text{repos}})$ aux deux niveaux — grandeur indispensabl… (…) ' — une résistance de labo fait 10 à 50 W, e…` |
| [§ 06.8](#s06-8) | `[[à documenter]]` | `…st conditionnelle à $\eta$, à l'existence d'un L-pad (que 06.3 laisse ouverte tant que le… (…) ') et à la fraction de pertes réellement pon…` |
| [§ 06.9](#s06-9) | `[[à mesurer]]` | `…lf par la masse, pas en kWh), l'ESR des condensateurs et les pertes fer d'une éventuelle… (…) '), et l'asymétrie de répartition spectrale…` |
| Sources | `[[à vérifier sur la datasheet du lot acheté]]` | `…cuit. - Texas Instruments, NE5532 (8 mA typ / 16 mA max par boîtier sous ±15 V ; révision… (…) ') ; STMicroelectronics / TI, TL072 (1,4 mA/…` |

### <a id="idx-07"></a>Marques de la section 07

| Sous-section | Marque | Contexte |
|---|---|---|
| préambule | `[[à mesurer]]` | `…s reportées telles quelles), soit des ordres de grandeur typiques étiquetés comme tels, s… (…) . > > Les deux scripts d'appui — 'scratchpad…` |
| [§ 07.3](#s07-3) | `[[à vérifier : référence et $S_d$ datasheet]]` | `…−27,57 dB \| D'après la photo 'assets/enceinte-face.jpg', les médiums latéraux semblent êt… (…) ; la $S_d$ réelle du 18″ est [[à lire sur la…` |
| [§ 07.3](#s07-3) | `[[à lire sur la datasheet]]` | `…raux semblent être des 12″ environ [[à vérifier : référence et $S_d$ datasheet]] ; la $S_… (…) . **La borne haute du critère est donc une d…` |
| [§ 07.3](#s07-3) | ~~`[[à documenter]]`~~ (type de caisse, dans « Correction évent ») **LEVÉE le 16 sept. 2026** | remplacée par le protocole complet « Champ proche d'un bass-reflex à DEUX évents » : pondération $\sum_i\sqrt{S_{P,i}/S_D}$, piège du $\sqrt N$ (3,01 dB), contrôle de signature à 24 dB/oct sous $f_b$, distance micro $0{,}11\,a_P = 5{,}5$ mm, et +2 à 3 h de manip sur la campagne |
| [§ 07.3](#s07-3) | `[[à mesurer]]` **(nouvelle)** | `…relever au mètre ruban la distance $r$ entre le centre de la membrane et chaque embouchure (…), sans quoi elle n'est même pas bornable.` — $r$ borne la contamination croisée du champ proche des évents par la membrane, via $(1/\rho)\,N\sqrt{S_p/S_d}\,a_D/(2r)$ |
| [§ 07.3](#s07-3) | `[[à vérifier]]` | `…ier et demi-espace) tombe vers $f_3 \approx 115/W$ Hz avec $W$ la largeur du baffle en m… (…) ) : 230 Hz pour $W = 0{,}5$ m, 192 Hz pour $…` |
| [§ 07.3](#s07-3) | `[[à mesurer]]` | `…= 0{,}6$ m, 144 Hz pour $W = 0{,}8$ m — dans tous les cas **dans la bande du critère**. L… (…) . (ii) Il ne voit pas la directivité ni la g…` |
| [§ 07.3](#s07-3) | `[[à lire sur son fichier de calibration]]` | `…t d'incertitude de la mesure acoustique.** Aux trois limites ci-dessus s'ajoutent la plan… (…) ), la réponse résiduelle de la carte son apr…` |
| [§ 07.4](#s07-4) | `[[à mesurer]]` | `…central, deux médiums dans des boîtes latérales inclinées d'environ 45°, centres distants… (…) . Un micro unique en champ proche ne peut pa…` |
| [§ 07.4](#s07-4) | `[[à geler en phase 0]]` | `…$a_i/(2d_i)$, retardée du trajet $d_i$ jusqu'à un point d'écoute virtuel (gelé : par exem… (…) ), affectée de sa polarité, puis on somme :…` |
| [§ 07.4](#s07-4) | `[[à mesurer]]` **(nouvelle)** | `…**Décision retenue : (b)**, avec cette justification, et la distance membrane-évent relevée au mètre pour pouvoir borner l'erreur (…)` — choix entre traiter les trois sources du sub séparément (a) ou les recombiner d'abord « en équivalent membrane » (b) |
| [§ 07.5](#s07-5) | `[[à vérifier]]` | `…rnes, la membrane doit sortir quand le + est sur le +. Consigner le sens de câblage des d… (…) . 2. **Phase relative mesurée** : sur les re…` |
| [§ 07.6](#s07-6) | `[[à documenter]]` | `…07-6"></a>07.6 Égalisation des niveaux entre voies Les sensibilités (dB/2,83 V/m) du 18″… (…) . Mesure de la sensibilité relative : répons…` |
| [§ 07.7](#s07-7) | `[[à vérifier selon la carte]]` | `…e). Diviseurs résistifs **50:1** sur chaque tension — pas 20:1 : face à une entrée ligne… (…) , un 20:1 ne laisse que 1,6 dB de marge au n…` |
| [§ 07.7](#s07-7) | `[[à vérifier au multimètre]]` | `…:1 (~15 € pièce), ou l'on renonce et l'on reste à l'oscilloscope. **Jamais en mode pont,… (…) - **Attendu sur 8 Ω** (filtre catalogue 18 m…` |
| [§ 07.8](#s07-8) | `[[à geler]]` | `…égaliser sur le niveau acoustique en champ proche à 100 Hz.) Ordres de grandeur pour la d… (…) : « faible » 2 V (0,5 W/8 Ω), « fort » entre…` |
| [§ 07.8](#s07-8) | `[[à vérifier sur sa fiche]]` | `…*112 dB SPL au niveau faible, 125 dB à 10 W et 132 dB à 50 W** — à comparer au SPL maxima… (…) ; le niveau « fort » sera plafonné par le mi…` |
| [§ 07.8](#s07-8) | `[[à geler, ex. 5 min]]` | `…médium G, médium D, évent \| faible \| 3 \| \| 2b \| **Conditionnement** : bruit rose au nivea… (…) ; $R_e$ au multimètre avant et après \| fort…` |
| [§ 07.8](#s07-8) | `[[masse de bobine à documenter]]` | `…s à 50 W, c'est **273 J**, soit un échauffement adiabatique de 11 K (bobine de 60 g) à 68… (…) — c'est-à-dire du même ordre que l'effet que…` |
| [§ 07.9](#s07-9) | `[[à mesurer en phase 1]]` | `…te ?** Les réponses brutes des haut-parleurs ne sont pas plates sur 40–250 Hz (coupure ba… (…) ). Si cette non-planéité domine le critère,…` |
| [§ 07.9](#s07-9) | `[[à geler]]` | `…seulement *comment* on mesure, mais *quelle valeur constitue un succès*. Proposition à va… (…) : \| Critère \| Succès déclaré si… \| \|---\|---\|…` |
| [§ 07.10](#s07-10) | `[[à documenter]]` | `…**Un micro USB est donc exclu de tout ce protocole** — à dire au moment de documenter le… (…) . - **Preferences > Soundcard** : 48 kHz ; «…` |
| [§ 07.10](#s07-10) | `[[à vérifier]]` | `…**Preferences > Mic/Meter** : charger systématiquement le fichier de calibration du micro… (…) : la réponse basse-fréquence du micro entre…` |
| [§ 07.10](#s07-10) | `[[à mesurer]]` | `…**Start $\ge 2f_B$** ($f_B$ = fréquence d'accord de l'évent, mesurée en phase 1 par le do… (…) ), pour que le contenu réel reste au-dessus…` |
| [§ 07.10](#s07-10) | `[[à geler en phase 0]]` | `…on-linéarité de la suspension, de $Bl(x)$ ou à la turbulence de l'évent. Seuil de rejet d… (…) . - **Moyennage des répétitions** : All SPL…` |
| [§ 07.11](#s07-11) | `[[à vérifier]]` | `…balayages forts, balayages courts, pas de tête à moins de 1 m du 18″. - **Micro** : SPL m… (…) ; réduire le gain d'entrée avant le niveau f…` |
| [§ 07.11](#s07-11) | `[[à vérifier]]` **(nouvelle)** | `…**Et les pavillons.** (…) S'il n'y a **pas** de condensateur en série avec eux (…), ils reçoivent le 100 Hz à pleine puissance pendant les balayages de la voie médium…` — **à lever avant le premier balayage au niveau fort** ; même marque qu'aux § 02.6 et § 04.2 |
| Sources | `[[à recouper sur le texte intégral de Keele 1974 si le jury demande une source pour le cas à deux évents — article AES payant, à demander au CDI]]` **(nouvelle)** | `…Keele (1974) la donne pour **un** évent ; D'Appolito (2012) la reprend sous la forme « pondérer par le rapport des diamètres ». **Aucune des deux sources n'explicite le cas $N>1$** (…)` — la démonstration est donc écrite au § 07.3 et vérifiée numériquement, plutôt que citée |
| Sources | `[[à vérifier]]` | `…Direct Radiator Loudspeaker Enclosures », *J. Audio Eng. Soc.*, vol. 17, n° 1, 1969 (diff… (…) . - Kuttruff, H., *Room Acoustics*, CRC Pres…` |
| Sources | `[[édition à préciser]]` | `…coffret) [[à vérifier]]. - Kuttruff, H., *Room Acoustics*, CRC Press (modes propres, fréq… (…) . - Beranek, L. L., Mellow, T., *Acoustics:…` |

### <a id="idx-08"></a>Marques de la section 08

| Sous-section | Marque | Contexte |
|---|---|---|
| préambule | `[[à vérifier]]` | `…rit sans marque a été lu dans une source citée en fin de section ; ce qui n'a pas pu l'êt… (…) **. Au 2026-09-03, la page TIPE du SCEI affi…` |
| [§ 08.2](#s08-2) | `[[à vérifier]]` | `…nes-Ponts** et la **Banque filière PT**. D'autres concours (e3a-Polytech, etc.) en repren… (…) **. Pour un élève issu de PTSI, la Banque PT…` |
| [§ 08.2](#s08-2) | `[[à vérifier]]` *(note)* | `…ech » était présenté comme organisateur sans source ; ramené à quatre organisateurs vérif… (…) . --> \| Élément \| Règle (SCEI, session 2026)…` |
| [§ 08.2](#s08-2) | `[[à vérifier à l'export]]` | `…s vues sont hors des 15 minutes ; en poids elles sont du texte vectoriel, donc négligeabl… (…) . - **L'enceinte, le filtre bobiné, la self…` |
| [§ 08.3](#s08-3) | `[[à vérifier]]` | `…4 positionnements thématiques officiels** (liste des Attendus 2026, regroupée par domaine… (…) ) : \| Domaine \| Thèmes (libellés officiels)…` |
| [§ 08.4](#s08-4) | `[[à vérifier]]` | `…, MCOT, encadrant, groupe \| 16 janv. 2025 9h → 6 févr. 2025 14h \| **15 janv. 2026 9h → 5… (…) ** — par analogie : mi-janvier → début févri…` |
| [§ 08.4](#s08-4) | `[[à vérifier]]` | `…entation, DOT, ajustements \| 25 févr. 2025 9h → 10 juin 2025 14h \| **25 févr. 2026 9h → 9… (…) ** — clôture ≈ début juin 2027 ; **date d'ou…` |
| [§ 08.4](#s08-4) | `[[à vérifier]]` | `…ous) \| \| 3 — Validation par l'encadrant \| 12 juin → 19 juin 2025 \| **11 juin 2026 9h → 19… (…) ** — mi-juin 2027 \| \| Jour de passage connu…` |
| [§ 08.4](#s08-4) | `[[à vérifier]]` | `…2026 14h** \| **[[à vérifier]]** — mi-juin 2027 \| \| Jour de passage connu \| — \| à partir d… (…) \| \| Oraux \| — \| **22 juin → 18 juillet 2026*…` |
| [§ 08.4](#s08-4) | `[[à vérifier]]` | `…n → 18 juillet 2026** (MP, MPI, PC, PSI) ; **22 juin → 11 juillet 2026 (PT)** ; 22 juin →… (…) ** — fin juin → juillet 2027 \| \| Réclamation…` |
| [§ 08.4](#s08-4) | `[[à vérifier]]` | `…érifier]]** — fin juin → juillet 2027 \| \| Réclamation sur report de note \| — \| avant le 2… (…) \| ¹ Note officielle des Attendus 2026, à rep…` |
| [§ 08.5](#s08-5) | `[[à vérifier]]` | `…ycée (MP, sept. 2025) annonce un barème « Présentation : 80 % de la note / Livrables (MCO… (…) : cette pondération n'apparaît dans aucun do…` |
| [§ 08.5](#s08-5) | `[[à vérifier par l'étudiant]]` | `…ommentée sera un habillage — ce que le jury repère précisément (« viser un premier niveau… (…) \| \| **A3. Ouverture et curiosité** \| « déclo…` |
| [§ 08.7](#s08-7) | `[[à consulter]]` | `…c des références **exactes** (titres, revue, année, pages), car les références actuelles… (…) ' / '[[édition à préciser]]'. Deux réserves…` |
| [§ 08.7](#s08-7) | `[[édition à préciser]]` | `…xactes** (titres, revue, année, pages), car les références actuelles portent des marques… (…) '. Deux réserves sur l'étoffement de cette b…` |
| Ce qu'il faut retenir pour l'oral | `[[à vérifier]]` | `…but juin 2027** (4-8 jalons factuels de 50 mots, soit 200-400 mots) ; oraux à partir de f… (…) sur scei-concours.fr, robustes à ±2 semaines…` |
| Sources | `[[à vérifier]]` | `…ation de l'épreuve de TIPE 2026 », 9 septembre 2025 — source du barème « 80 % présentatio… (…) : https://cahier-de-prepa.fr/mp-ism/download…` |

### <a id="idx-09"></a>Marques de la section 09

| Sous-section | Marque | Contexte |
|---|---|---|
| préambule | `[[à mesurer]]` | `…du § 04.6. > **Aucune mesure n'a été faite sur l'enceinte de Thomas** : tout nombre est c… (…) '. Environnement revérifié le **2026-09-13**…` |
| [§ 09.3](#s09-3) | `[[à vérifier sur un export réel]]` | `…s trois colonnes (fréquence, module, phase). Le séparateur dépend de la version et des ré… (…) : le lecteur l'auto-détecte parmi ',' ';' ta…` |
| [§ 09.3](#s09-3) | `[[format du modèle du lycée à relever]]` | `…d'oscilloscope** — 'lire_scope(chemin) -> (t, v1, v2, meta)' (temps, CH1, CH2 ; en-tête p… (…) ). Au lieu de pointer $\Delta t$ au curseur,…` |
| [§ 09.3](#s09-3) | `[[à vérifier]]` | `…s acquisitions plutôt que pointer des curseurs, **si** l'export CSV de l'oscilloscope du… (…) . Le contrôle de signe (self pure → +90°, co…` |
| [§ 09.4](#s09-4) | `[[à contrôler en doublant $N_f$ : l'optimum ne doit pas bouger]]` | `…etombe à **28 Mo** (88 Mo à $N_f=200$). $N_f = 64$ points log sur 40–250 Hz suffisent pou… (…) . **L'énumération jointe est-elle une inflat…` |
| [§ 09.6](#s09-6) | `[[à chiffrer sur le modèle retenu au § 05]]` | `…par optimisation numérique du rapport géométrique, avec la loi $r\times m \approx$ cte à… (…) ). ### <a id="s09-7"></a>09.7 Figures : iden…` |
| Sources | `[[séparateur exact à vérifier sur un export réel]]` | `…*File > Export > Export measurement as text* ('.txt'/'.zma', colonnes Freq / Z / Phase, e… (…) . - Dépôt : '_gen.py', 'css/blueprint.css',…` |
