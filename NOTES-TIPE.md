# Notes TIPE — questions probables du jury et pistes de réponse

À relire la veille de l'oral. Le jury (un examinateur physique-chimie, un
mathématiques, **non spécialistes** du sujet) cherche à vérifier la rigueur de la
démarche, pas à te piéger sur de l'électroacoustique pointue. Réponds avec des
grandeurs physiques et des ordres de grandeur, jamais « ça sonne mieux ».

> Les questions marquées **[P]** sont surtout utiles pour la **pré-soutenance**
> (annonce du sujet) ; les autres pour la **soutenance finale** (avec résultats).

---

## 1. Sur le sujet et la problématique

**« En une phrase, qu'est-ce que vous cherchez à optimiser ? »** **[P]**
→ La fidélité de la réponse en fréquence au raccord 100 Hz : que la somme des deux
voies soit la plus plate possible (écart minimal en dB à une cible), avec un raccord
de phase propre. C'est mon critère objectif de « qualité ».

**« Pourquoi 100 Hz et pas une autre fréquence ? »** **[P]**
→ Choix dicté par les haut-parleurs : mon médium a une résonance vers f_s ≈ 50 Hz ;
couper à 100 Hz (le double) le maintient au-dessus de sa zone de distorsion, et confie
le grave au subwoofer 18″ qui est conçu pour ça.

**« Pourquoi comparer passif ET actif, est-ce vraiment comparable ? »**
→ Non, pas tout à fait, et c'est justement l'intérêt : le passif filtre après
l'ampli (composants de puissance, lourds) ; l'actif filtre avant (petits composants)
mais impose un ampli par voie. Je compare donc des compromis, pas des équivalents —
d'où le « à quel coût système » de ma problématique.

## 2. Sur la physique des filtres (cœur PTSI)

**« Écrivez la fonction de transfert d'un passe-bas du 1er ordre. »**
→ \( \underline{H}(j\omega) = \dfrac{1}{1 + j\,\omega/\omega_c} \), avec
\( \omega_c = 2\pi f_c \). Module \( |H| = 1/\sqrt{1+(\omega/\omega_c)^2} \),
gain \(-3\) dB et déphasage \(-45°\) à \( f_c \), pente asymptotique \(-20\) dB/décade.

**« Comment fixez-vous la fréquence de coupure ? »**
→ Passe-haut RC : \( f_c = 1/(2\pi RC) \). Passe-bas RL (bobine série + charge R) :
\( f_c = R/(2\pi L) \). Je choisis L ou C pour obtenir 100 Hz avec R = 8 Ω.

**« Donnez les valeurs des composants en passif. »**
→ Pour R = 8 Ω à 100 Hz : \( L = R/(2\pi f_c) \approx 12{,}7 \) mH et
\( C = 1/(2\pi f_c R) \approx 199~\mu\text{F} \). Ce sont de grosses valeurs : c'est mon
argument « sobriété » — le passif est physiquement coûteux à si basse fréquence.

**« Qu'est-ce qu'une décade, une octave ? »**
→ Décade = facteur 10 en fréquence (pente −20 dB/décade au 1er ordre) ;
octave = facteur 2 (soit −6 dB/octave). Même pente, deux unités.

## 3. Sur le haut-parleur réel (LE piège classique)

**« Vous traitez le HP comme une résistance de 8 Ω. Est-ce justifié ? »**
→ Non, c'est une approximation. Un HP a une inductance de bobine (impédance qui monte
avec f) et un pic d'impédance à sa résonance f_s. Le « 8 Ω » est une valeur nominale,
pas l'impédance réelle. C'est pourquoi je teste d'abord sur une **résistance de 8 Ω**
(cas idéal), puis sur le **vrai HP** : l'écart entre les deux mesure précisément cet effet.

**« Conséquence sur le filtre passif ? »**
→ La coupure réelle dépend de l'impédance de charge, qui varie ; donc le f_c effectif
diffère du f_c théorique calculé sur 8 Ω. L'actif, lui, voit l'entrée de l'AOP
(impédance élevée et quasi constante) → réponse prévisible, indépendante du HP. Deuxième
argument fort pour l'actif.

## 4. Sur la mesure

**« Comment mesurez-vous un diagramme de Bode ? »** **[P]**
→ GBF en entrée, balayage en fréquence ; à l'oscilloscope je lis l'amplitude de sortie
(→ gain en dB) et le décalage temporel entre entrée et sortie (→ déphasage). Point par
point ou en balayage.

**« Pourquoi la mesure acoustique est-elle délicate à 100 Hz ? »**
→ À 100 Hz la longueur d'onde vaut ≈ 3,4 m, comparable aux dimensions de la pièce :
les modes propres (ondes stationnaires) dominent et faussent la mesure. Le fenêtrage
quasi-anéchoïque est inopérant si bas. Je mesure donc en **champ proche** (micro à
quelques cm) pour m'affranchir de la pièce, en assumant que ce n'est pas la réponse au
point d'écoute.

**« Et les incertitudes ? »**
→ Tolérances des composants (R ±5 %, C ±10–20 %, L ±10 %) propagées sur
\( f_c \) : par exemple pour un RC, \( u(f_c)/f_c = \sqrt{(u(R)/R)^2 + (u(C)/C)^2} \).
Plus les incertitudes de lecture à l'oscilloscope sur le gain et le déphasage.

## 5. Sur le filtrage actif (2e année — à maîtriser pour la finale)

**« Comment fonctionne votre filtre actif ? »**
→ Un amplificateur opérationnel en régime linéaire (hypothèses : courants d'entrée
nuls, \( V^+ = V^- \)) associé à un réseau RC fixe la fréquence de coupure, en amont
de l'amplification de puissance. Avantage : composants minuscules et réponse
indépendante du HP.

**« Pourquoi une bi-amplification ? »**
→ Comme le filtrage est fait avant l'ampli, chaque voie filtrée a besoin de son propre
amplificateur de puissance. C'est le coût système de l'actif : plus d'électronique et
une alimentation, en échange de la sobriété des composants de filtrage.

## 6. Sur le thème national

**« Où sont sobriété, efficacité, optimisation dans votre travail ? »** **[P]**
→ Sobriété : nombre/taille/coût des composants (le passif est lourd à 100 Hz).
Efficacité : pertes Joule dans la résistance de la bobine, pente réelle d'atténuation.
Optimisation : le compromis chiffré entre les deux, jugé sur l'écart à la réponse cible.

## 7. Limites à reconnaître spontanément (ça rassure le jury)

- Je reste au 1er ordre : pente douce (−6 dB/oct), recouvrement large des deux voies.
- Le HP n'est pas purement résistif ; je le quantifie au lieu de l'ignorer.
- La mesure acoustique en basses fréquences est limitée par la pièce.
- Le raccord de phase entre voies (90° au 1er ordre) influe sur la somme acoustique.
- Les sensibilités des HP diffèrent : il faudra peut-être égaliser les niveaux.

## 8. Questions « maths » possibles

- Lien module/argument d'un complexe \( \underline{H} \) (forme algébrique ↔ polaire).
- Pourquoi le gain en dB : \( G_{dB} = 20\log_{10}|H| \) ; échelle log en fréquence.
- Comportement asymptotique d'une fraction rationnelle en \( j\omega \) (limites 0 et ∞).

---

### À faire avant la soutenance finale
- Remplacer tous les placeholders (photo, schéma, Bode, f_s mesurée).
- Avoir des courbes mesurées : Bode passif et actif, sur résistance et sur HP.
- Préparer le tableau comparatif chiffré (sobriété / efficacité / optimisation).
