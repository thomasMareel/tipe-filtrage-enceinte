# Notes TIPE — questions probables du jury et pistes de réponse

À relire la veille de l'oral. Sujet : **trois architectures de filtrage** pour le
raccord à 100 Hz d'une enceinte deux voies (sub 18″ 8 Ω + 2 médiums 4 Ω série).
Jury non spécialiste : répondre avec des grandeurs physiques et des ordres de
grandeur, jamais « ça sonne mieux ».

> [P] = surtout utile pour la **pré-soutenance** (démarche) ; les autres pour la **finale**.

## 1. Sujet & problématique

**« En une phrase, qu'optimisez-vous ? »** [P]
→ Le compromis **sobriété / efficacité** du raccord à 100 Hz : à pente et coupure
comparables, quelle architecture coûte le moins (composants, encombrement, complexité)
tout en restant fidèle (coupure réelle proche de 100 Hz, pente effective, pertes faibles).

**« Pourquoi 100 Hz ? »** [P]
→ Garder les médiums **au-dessus de leur résonance** (sinon distorsion/excursion) et
confier le grave au 18″, conçu pour ça.

## 2. Les trois architectures

**« Pourquoi trois architectures ? »**
→ 1) **passif post-ampli** (LC 2ⁿᵈ ordre Butterworth, entre ampli et HP) ;
2) **passif signal faible** (RC 1er ordre, entre pré-ampli et ampli) ;
3) **actif Sallen-Key** (2ⁿᵈ ordre, à AOP, avant l'ampli). Le **duel scientifique** est
**1.B vs 3** (même ordre, 12 dB/oct) ; l'archi 2 (6 dB/oct) est un **contre-exemple**
qui montre les limites de l'approche naïve.

**« La comparaison est-elle équitable ? »** (piège)
→ Honnêtement, l'archi 2 est du **1er ordre** : on ne compare pas sa pente à pied
d'égalité. Je l'assume — c'est justement pour montrer pourquoi on ne filtre pas en RC
au niveau ligne. Le cœur est 1.B vs 3.

**« Si 1.B et 3 sont tous deux du 2ⁿᵈ ordre Butterworth, ne sont-ils pas identiques ? »**
→ En théorie, oui (même \(\underline H\), même pente, même −3 dB à f_c). La différence
est **dans le réel** : le passif voit l'impédance variable du HP, subit les pertes de la
bobine et les tolérances de gros composants ; l'actif garde une réponse idéale et
**ajustable**. L'écart se mesure sur la fidélité réelle et la sobriété.

## 3. Butterworth 2ⁿᵈ ordre & Sallen-Key

**« Fonction de transfert d'un passe-bas 2ⁿᵈ ordre ? »**
→ \( \underline H_{PB}=\dfrac{1}{1+\frac{1}{Q}\frac{j\omega}{\omega_c}+\left(\frac{j\omega}{\omega_c}\right)^2} \).
À f_c : \( |H|=Q \) pour ce passe-bas ; **Butterworth** = \( Q=1/\sqrt2 \) (réponse
maximalement plate), gain −3 dB à f_c, pente asymptotique **−40 dB/décade (−12 dB/oct)**,
déphasage −90° à f_c (−180° en HF).

**« Dimensionnement passif (archi 1.B) ? »**
→ \( L=\dfrac{R\sqrt2}{2\pi f_c}\approx 18{,}0\) mH, \( C=\dfrac{1}{R\sqrt2\,2\pi f_c}\approx 141\) µF
(→ 150 µF normalisé, qui décale f_c à ≈ 96 Hz : à assumer). R = 8 Ω.

**« Dimensionnement actif (archi 3, Sallen-Key gain unité) ? »**
→ Passe-bas (sub) : R₁=R₂=**10 kΩ**, C₁=220 nF, C₂=110 nF (C₁=2C₂ ⇒ Q=1/√2).
Passe-haut (médiums) : C=100 nF, R'₁=**11 kΩ**, R'₂=**22 kΩ** (R'₂=2R'₁ ⇒ Q=1/√2).
AOP NE5532, alim ±15 V. *(Attention : composants tous égaux + gain unité donnent Q=0,5,
pas Butterworth — d'où les ratios C₁=2C₂ et R'₂=2R'₁.)*

## 4. Le haut-parleur réel

**« Vous traitez le HP comme 8 Ω. Justifié ? »**
→ Approximation. Le HP a une inductance L_e (Z monte avec f) et un **pic à la résonance
f_s**. « 8 Ω » est nominal. D'où la méthode : tester d'abord sur **résistance 8 Ω**, puis
sur le **vrai HP** ; l'écart mesure cet effet. L'actif, lui, voit l'entrée de l'AOP → insensible.

**« f_s mesurée vs datasheet ? »** (piège)
→ La datasheet donne f_s en **champ libre** ; mon pic d'impédance est celui du HP **en
caisse** (clos : F_c > f_s ; bass-reflex : deux pics). L'écart n'est **pas une erreur** :
c'est la charge acoustique. Pour le vrai f_s champ libre, mesurer hors caisse.

**« Comment mesurer Z(f) ? »**
→ Résistance de référence R_ref = 100 Ω en série ; mesurer **V_HP et V_Rref** →
\( Z=R_{ref}\,V_{HP}/V_{Rref} \) (exact, sans hypothèse de courant constant — utile car
au pic Z ~ 40–60 Ω). REW sait le faire avec un jig.

## 5. Le raccord (sommation des voies)

**« Que se passe-t-il à la somme des deux voies en 2ⁿᵈ ordre ? »**
→ Les deux voies sont **à 180°** à f_c. Sans rien faire → **trou** (annulation). Il faut
**inverser la polarité** d'une voie → la somme fait une **bosse de +3 dB** (signature
Butterworth). Un **Linkwitz-Riley** (−6 dB à f_c) sommerait **plat** : c'est l'alternative
standard, gardée en perspective.

## 6. Mesure & incertitudes

**« Comment mesurez-vous un Bode ? »** [P]
→ GBF en balayage, oscilloscope : amplitude (→ gain dB) et décalage temporel (→ phase).

**« Pourquoi l'acoustique BF est délicate ? »**
→ λ ≈ 3,4 m à 100 Hz : les **modes de pièce** dominent. Mesure en **champ proche** pour
s'affranchir de la pièce (limite assumée : ce n'est pas la réponse au point d'écoute).

**« Incertitudes ? »**
→ Tolérances R ±5 %, C ±10–20 %, L ±10 % propagées : \( \frac{u(f_c)}{f_c}=\sqrt{(u(R)/R)^2+(u(C)/C)^2} \)
(≈ 11 % pour un RC). Barres d'erreur sur tous les Bode.

## 7. Thème : sobriété / efficacité / optimisation

**« Où sont les trois mots ? »** [P]
→ Sobriété : nombre/taille/coût des composants (passif lourd : bobine 18 mH, condensateur
≥ 100 V). Efficacité : pertes Joule dans la **DCR** de la bobine, pente réelle. Optimisation :
arbitrage pondéré sur l'écart à la cible.

**« Le coût système, c'est l'actif seul ? »**
→ Non : les archis **2 et 3** utilisent toutes deux les 2 canaux du E-800 (bi-amplification).
Le vrai discriminant 1.B vs 3 : gros composants de puissance (DCR, prix, encombrement)
**contre** petits composants + AOP + alim.

## 8. Questions « maths » (un examinateur est mathématicien)

- Module/argument de \( \underline H \) (algébrique ↔ polaire), gain \( 20\log_{10}|H| \), échelle log.
- Démontrer le −3 dB : à \( x=\omega/\omega_c=1 \), pour Butterworth \( |H|=1/\sqrt2 \).
- Facteur de qualité Q : largeur de bande, surtension ; lien avec l'amortissement.
- Comportement asymptotique d'une fraction rationnelle en \( (j\omega)^2 \) (pente −40 dB/déc).

## 9. Limites à reconnaître spontanément

- Comparaison non iso-ordre (archi 2 en 1er ordre).
- HP non résistif (quantifié, pas ignoré) ; f_s en caisse ≠ datasheet.
- Inversion de polarité au raccord ; somme acoustique dépend de la position des HP.
- Acoustique BF limitée par la pièce ; incertitudes des composants.

## 10. Perspectives (slide ouverture)

- **Réseau de Zobel** : linéarise Z(HP) pour fiabiliser le passif.
- **Linkwitz-Riley** : somme plate (cible audio pro).
- **Ordre 4** : encombrant/coûteux en passif (4 gros composants/voie — mais courant en pro),
  trivial en actif (cascade).
- **Correction numérique (DSP)** : autre horizon.

---

### À faire avant la soutenance finale
- Mesurer Z(f) et f_s (REW + jig) ; mesurer Z_s du pré-ampli SX-801.
- Câbler les filtres ; Bode sur résistance puis HP ; somme acoustique au raccord.
- Remplacer les placeholders (courbes mesurées) et la ligne « écart à la cible ».
- Compléter la bibliographie (annexe Sources).
