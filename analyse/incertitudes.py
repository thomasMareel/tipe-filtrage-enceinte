"""incertitudes.py -- propagation des incertitudes au sens du GUM.

TIPE << filtrage enceinte >> (sujet v2), actes 1 a 3.
Voir REFERENCE-TECHNIQUE.md : § 02.7 (budget sur |Z|), § 03.5 (types A
et B sur les parametres de Thiele-Small), § 04.9 (tolerances des composants),
§§ 09.4 et 09.6 (signatures gelees et criteres chiffres des tests).

CE QUE FAIT CE MODULE
---------------------
1. Convertir une TOLERANCE de catalogue (une demi-largeur, loi rectangulaire) en
   INCERTITUDE-TYPE : u = a / racine(3). C'est cette seule conversion qui separe
   les deux chiffres du couple (7,1 % borne au pire cas ; 4,1 % incertitude-type)
   pour des composants a +/- 10 %.
2. Propager, par deux chemins independants qui doivent se confirmer :
   - propagation LINEAIRE (derivees partielles, GUM chapitre 5) ;
   - propagation de MONTE-CARLO (GUM supplement 1).
   Les deux fonctions ont la MEME interface et rendent le meme objet ; leur accord
   valide la linearisation, leur desaccord signale une non-linearite (c'est le cas
   de f0, qui est en (LC)^(-1/2) : le Monte-Carlo est BIAISE de +0,75 % a 10 %/10 %).
3. Separer l'incertitude de TYPE A (aleatoire : repetabilite, bruit de lecture,
   pointe d'un curseur) de celle de TYPE B (systematique : tolerance de R_ref,
   desappariement de gain des deux voies de l'oscilloscope, derive thermique).
   C'est le point le plus important de ce module et le moins intuitif :

       Z = R_ref * |V_d| / |V_R|

   une erreur de +1 % sur R_ref multiplie TOUTES les |Z| de la serie par 1,01, de
   facon parfaitement correlee d'un point a l'autre. Les trois estimateurs
   classiques du § 03.5 (covariance (J^T J)^-1, Monte-Carlo sur le bruit,
   jackknife) ne voient QUE la composante aleatoire : le chi2 reduit ne bouge pas,
   et le biais reste invisible. Or il est ici dominant. La fonction
   budget_parametres_ts() combine les deux composantes et dit, parametre par
   parametre, lequel est immunise (fs et Qms : une position et une forme) et
   lequel herite lineairement de l'erreur de R_ref (Re, Res, Le : des niveaux).

CE QUE CE MODULE NE FAIT PAS
----------------------------
Il ne mesure rien et ne lit aucun fichier. Aucune mesure n'a encore ete faite sur
l'enceinte : toutes les valeurs numeriques citees dans les docstrings et produites
par l'autotest sont SYNTHETIQUES ou des ordres de grandeur etiquetes comme tels.

CONVENTIONS GELEES
------------------
- Incertitudes-types (k = 1) partout, sauf mention explicite ; le resultat final se
  declare elargi avec k = 2 (fonction elargir()), niveau de confiance ~ 95 %.
- Une tolerance de composant << +/- 10 % >> est une loi RECTANGULAIRE : u = a/racine(3)
  = 5,77 %. La combinaison des demi-largeurs en quadrature (7,07 % sur f0) reste
  citable mais TOUJOURS etiquetee << borne au pire cas >>, jamais incertitude-type.
- f0 designe le POLE 1/(2 pi racine(LC)), jamais la frequence de croisement des deux
  voies, qui s'appelle f_x dans tout le code (§ 09.4). La formule de f0 porte
  un facteur 1/2 : u(f0)/f0 = (1/2) racine((u_L/L)^2 + (u_C/C)^2). La meme formule
  SANS le 1/2 est celle d'un RC du premier ordre -- l'architecture abandonnee de la
  v1 -- et elle n'a plus rien a faire dans ce TIPE.
- Dependance : numpy seul (ce module doit tourner sur une machine du lycee).
"""

from collections import OrderedDict, namedtuple

import numpy as np

# --------------------------------------------------------------------------
# Constantes et conventions
# --------------------------------------------------------------------------

RACINE_3 = np.sqrt(3.0)
RACINE_6 = np.sqrt(6.0)

K_ELARGISSEMENT = 2  # facteur d'elargissement gele (§ 02.7)

N_MC_DEFAUT = 400_000  # tirages des chiffres de l'oral (§ 09.8)
N_MC_RAPIDE = 20_000   # tirages de la boucle de developpement (option --rapide)

#: Noms des cinq parametres du modele de Thiele-Small, dans l'ordre de theta.
NOMS_TS = ("Re", "Le", "Res", "fs", "Qms")

#: Sensibilite RELATIVE de chaque parametre T-S a une erreur RELATIVE d'echelle sur
#: R_ref : d(theta_j)/theta_j = c_j * dR_ref/R_ref. Verifie numeriquement par
#: demonstration_biais_Rref() et exactement par l'identite d'echelle du modele :
#: (1+d) * Z_ts(f ; Re, Le, Res, fs, Qms) == Z_ts(f ; (1+d)Re, (1+d)Le, (1+d)Res, fs, Qms).
#: Un << niveau >> herite de l'erreur, une << position >> et une << forme >> n'y voient rien.
SENSIBILITE_RREF = OrderedDict(
    [("Re", 1.0), ("Le", 1.0), ("Res", 1.0), ("fs", 0.0), ("Qms", 0.0)]
)

#: Objet rendu par les DEUX fonctions de propagation (meme interface, meme retour).
Propagation = namedtuple(
    "Propagation", "valeur u u_relative methode detail"
)

#: Objet rendu par u_f0() : jamais un nombre seul, toujours le couple.
CoupleF0 = namedtuple(
    "CoupleF0",
    "borne_pire_cas incertitude_type f0_Hz u_borne_Hz u_type_Hz rho",
)

#: Objet rendu par type_a_repetabilite().
Repetabilite = namedtuple(
    "Repetabilite", "moyenne ecart_type_experimental u_moyenne n"
)


# --------------------------------------------------------------------------
# 1. Types A et B : conversions et combinaisons
# --------------------------------------------------------------------------

def type_b_rectangulaire(demi_largeur):
    """Loi rectangulaire (uniforme) -> incertitude-type : u = a / racine(3).

    PHYSIQUE. Un fabricant qui ecrit << 150 uF +/- 20 % >> n'annonce pas un
    ecart-type : il annonce une BORNE. Le GUM (JCGM 100:2008, § 4.3.7)
    prescrit alors de modeliser la valeur vraie par une loi uniforme sur
    [x - a, x + a], dont l'ecart-type vaut a/racine(3) = 0,577 a. Prendre a pour
    une incertitude-type surestime d'un facteur 1,73 -- c'est exactement l'ecart
    entre les deux lectures du couple de u_f0() (7,1 % et 4,1 %).

    Voir REFERENCE-TECHNIQUE.md § 09.6 (convention gelee) et § 04.9.

    Parametres
    ----------
    demi_largeur : float ou tableau
        Demi-largeur a de la tolerance, en valeur absolue ou en relatif (la
        conversion est lineaire, elle ne change pas d'unite).

    Retour
    ------
    float ou tableau : l'incertitude-type u = a/racine(3), meme unite que a.
    """
    return np.asarray(demi_largeur, float) / RACINE_3


def type_b_triangulaire(demi_largeur):
    """Loi triangulaire -> incertitude-type : u = a / racine(6).

    A utiliser quand on a une raison de croire que les valeurs proches du centre
    sont plus probables que celles du bord -- typiquement un lot de composants
    tries, ou une resistance mesuree au multimetre puis appairee. Sans cette
    raison, on reste sur la loi rectangulaire, qui est le choix prudent.
    """
    return np.asarray(demi_largeur, float) / RACINE_6


def type_a_repetabilite(valeurs):
    """Evaluation de TYPE A : dispersion observee sur des lectures repetees.

    PHYSIQUE et piege classique. On refait n fois la lecture complete d'un meme
    point (§ 02.8, etape 5 : 5 fois, en re-reglant les curseurs a chaque
    fois). Deux incertitudes en sortent, et elles ne servent pas au meme usage :

    - l'ECART-TYPE EXPERIMENTAL s : dispersion d'UNE lecture. C'est lui qui
      alimente le budget d'un point de la courbe Z(f), puisque chaque point de la
      courbe n'a ete lu qu'UNE fois. C'est la composante A de epsilon (§ 02.7).
    - u(moyenne) = s / racine(n) : incertitude sur la MOYENNE des n lectures. Ne
      l'utiliser que si le point retenu est effectivement la moyenne des n lectures.

    Confondre les deux divise l'incertitude par racine(5) = 2,2 sans aucune raison.

    Parametres
    ----------
    valeurs : sequence de floats
        Les n lectures repetees (n >= 2), meme grandeur, memes conditions.

    Retour
    ------
    Repetabilite(moyenne, ecart_type_experimental, u_moyenne, n)
    """
    v = np.asarray(valeurs, float).ravel()
    if v.size < 2:
        raise ValueError("type_a_repetabilite : il faut au moins 2 lectures")
    s = float(v.std(ddof=1))  # ddof=1 : estimateur non biaise de la variance
    return Repetabilite(float(v.mean()), s, s / np.sqrt(v.size), int(v.size))


def combiner_types(u_A, u_B):
    """Incertitude-type COMPOSEE : u = racine(u_A^2 + u_B^2).

    Les composantes aleatoire et systematique sont par construction independantes
    (l'une vient du bruit de lecture, l'autre de l'etalonnage de la chaine) : elles
    se combinent en quadrature, jamais en somme. Fonctionne aussi bien sur des
    incertitudes absolues que relatives, pourvu qu'on ne melange pas les deux.
    """
    return np.hypot(np.asarray(u_A, float), np.asarray(u_B, float))


def elargir(u, k=K_ELARGISSEMENT):
    """Incertitude ELARGIE U = k*u (k = 2 par defaut, soit ~ 95 % de confiance).

    C'est sous cette forme que se declare un resultat final (§ 02.7) et que
    s'ecrivent les criteres en ecart normalise E_n <= 2 de la porte de validation
    de la phase 1 (§ 02.8).
    """
    return k * np.asarray(u, float)


# --------------------------------------------------------------------------
# 2. Outils de correlation
# --------------------------------------------------------------------------

def _matrice_correlation(rho, p):
    """Construit la matrice de correlation (p, p) a partir de rho.

    rho accepte trois formes : None ou 0 (variables independantes), un scalaire
    (meme correlation pour toutes les paires -- cas << tous les composants du meme
    lot >>), ou une matrice (p, p) deja complete.
    """
    if rho is None:
        return np.eye(p)
    rho = np.asarray(rho, float)
    if rho.ndim == 0:
        R = np.full((p, p), float(rho))
        np.fill_diagonal(R, 1.0)
        return R
    if rho.shape != (p, p):
        raise ValueError(
            "matrice de correlation de forme %s, attendu (%d, %d)" % (rho.shape, p, p)
        )
    return rho


def _covariance(u, rho):
    """Matrice de covariance a partir des incertitudes-types et de la correlation."""
    u = np.asarray(u, float).ravel()
    R = _matrice_correlation(rho, u.size)
    return (u[:, None] * u[None, :]) * R


def _racine_matricielle(cov):
    """Racine carree symetrique d'une matrice de covariance, par diagonalisation.

    On n'utilise PAS Cholesky : il echoue sur une matrice singuliere, or le cas
    rho = +1 (deux composants du meme lot, parfaitement correles) est justement un
    cas physique qu'il faut savoir traiter. La diagonalisation le supporte, a
    condition de raboter les valeurs propres legerement negatives dues aux arrondis.
    """
    w, V = np.linalg.eigh(np.asarray(cov, float))
    w = np.clip(w, 0.0, None)
    return (V * np.sqrt(w)) @ V.T


# --------------------------------------------------------------------------
# 3. Propagation generique : lineaire et Monte-Carlo, MEME interface
# --------------------------------------------------------------------------

def derivees_partielles(modele, x, pas_relatif=1e-6):
    """Derivees partielles d(modele)/dx_j par differences finies CENTREES.

    Le pas est relatif a chaque variable (pas_relatif * |x_j|) : indispensable ici,
    ou les grandeurs vont de 1e-4 (une self en henry) a 1e2 (une resistance en ohm).
    Un pas absolu unique donnerait une derivee absurde sur l'une des deux.

    Parametres
    ----------
    modele : callable
        modele(x) avec x de forme (p,) -> scalaire. La MEME fonction doit accepter
        x de forme (p, N) -> (N,) pour servir au Monte-Carlo : ecrire le modele avec
        des operations numpy elementaires suffit (voir les exemples de ce module).
    x : sequence de p floats
        Point de fonctionnement (les valeurs nominales).

    Retour
    ------
    tableau (p,) : les p derivees partielles au point x.
    """
    x = np.asarray(x, float).ravel()
    g = np.empty(x.size)
    for j in range(x.size):
        h = pas_relatif * abs(x[j]) if x[j] != 0.0 else pas_relatif
        xp, xm = x.copy(), x.copy()
        xp[j] += h
        xm[j] -= h
        g[j] = (float(modele(xp)) - float(modele(xm))) / (2.0 * h)
    return g


def propager_lineaire(modele, x, u, rho=None, noms=None, pas_relatif=1e-6):
    """Propagation LINEAIRE (GUM chapitre 5) : u_y^2 = g^T Sigma g.

    PHYSIQUE. On linearise le modele autour du point nominal : une variation dx_j
    produit une variation g_j dx_j de la sortie. Les incertitudes se composent alors
    en quadrature, avec les termes croises si les entrees sont correlees :

        u(y)^2 = somme_j (g_j u_j)^2 + 2 somme_{i<j} rho_ij g_i u_i g_j u_j

    Valide tant que le modele est quasi lineaire sur quelques u. Ce n'est PAS le cas
    de f0 = 1/(2 pi racine(LC)) a +/- 10 % : le Monte-Carlo y trouve un ecart-type
    2,3 % plus grand et une moyenne decalee de +0,75 %. D'ou l'obligation de faire
    tourner les deux.

    Parametres
    ----------
    modele : callable, voir derivees_partielles.
    x : sequence de p floats -- valeurs nominales des entrees.
    u : sequence de p floats -- INCERTITUDES-TYPES (k = 1) des entrees, memes unites
        que x. Pour une tolerance de catalogue, passer par type_b_rectangulaire().
    rho : None, scalaire ou matrice (p, p) -- correlations entre entrees.
    noms : sequence de p chaines, pour etiqueter les contributions (facultatif).

    Retour
    ------
    Propagation(valeur, u, u_relative, methode='lineaire', detail)
        detail['sensibilites']  : les g_j
        detail['contributions'] : g_j * u_j, signees (l'unite de y)
        detail['part_variance'] : part de chaque entree dans la variance, en %,
                                  hors termes croises (somme != 100 % si rho != 0)
        detail['terme_croise']  : contribution des termes croises a la variance
    """
    x = np.asarray(x, float).ravel()
    u = np.asarray(u, float).ravel()
    if x.size != u.size:
        raise ValueError("propager_lineaire : x et u de tailles differentes")
    g = derivees_partielles(modele, x, pas_relatif)
    cov = _covariance(u, rho)
    variance = float(g @ cov @ g)
    contributions = g * u
    diag = float(np.sum(contributions ** 2))
    y0 = float(modele(x))
    detail = {
        "sensibilites": g,
        "contributions": contributions,
        "part_variance": 100.0 * contributions ** 2 / diag if diag > 0 else contributions * 0.0,
        "terme_croise": variance - diag,
        "noms": tuple(noms) if noms is not None else tuple("x%d" % j for j in range(x.size)),
    }
    u_y = np.sqrt(max(variance, 0.0))
    return Propagation(y0, u_y, u_y / abs(y0) if y0 != 0 else np.nan, "lineaire", detail)


def propager_monte_carlo(modele, x, u, rho=None, n=N_MC_DEFAUT, loi="normale",
                         graine=0, noms=None):
    """Propagation de MONTE-CARLO (GUM supplement 1) : meme interface que la lineaire.

    PHYSIQUE. On tire n jeux d'entrees dans leurs lois, on passe chaque jeu dans le
    modele exact, et on lit la moyenne et l'ecart-type de la sortie. Aucune
    hypothese de linearite : c'est la methode de reference quand le modele est une
    racine, un quotient ou une valeur absolue -- tous presents dans ce TIPE.

    PIEGE, ET C'EST LE PIEGE DE CE MODULE :
      - loi='normale'  -> u est un ECART-TYPE ;
      - loi='uniforme' -> u est une DEMI-LARGEUR a (loi rectangulaire), et
        l'ecart-type effectivement tire vaut a/racine(3).

    Le projet ecrit partout « loi rectangulaire » (vocabulaire du GUM) la ou numpy
    dit « uniforme » : les deux noms sont acceptes et designent la meme loi.
    Passer une tolerance de catalogue avec loi='normale' surestime donc la
    dispersion d'un facteur 1,73 ; passer une incertitude-type avec loi='uniforme'
    la sous-estime d'autant.

    La moyenne rendue n'est PAS forcement modele(x) : pour une fonction convexe,
    E[f(X)] > f(E[X]). Le biais est rendu dans detail['biais_relatif'] -- c'est un
    resultat, pas une erreur de tirage (voir biais_relatif_mc_f0).

    Parametres : voir propager_lineaire ; en plus
    n : nombre de tirages (N_MC_DEFAUT pour les chiffres de l'oral).
    loi : 'normale' ou 'uniforme'.
    graine : graine du generateur. TOUJOURS fixee et consignee au journal : un
        Monte-Carlo non reproductible n'est pas un resultat (§ 09.8).

    Retour
    ------
    Propagation(valeur=moyenne, u=ecart-type, u_relative, methode='monte-carlo', detail)
        detail['nominal'], detail['biais_relatif'], detail['quantiles'] (5 %, 95 %),
        detail['n'], detail['loi'], detail['graine'].
    """
    if loi == "rectangulaire":
        loi = "uniforme"   # synonyme GUM, cf. docstring
    x = np.asarray(x, float).ravel()
    u = np.asarray(u, float).ravel()
    if x.size != u.size:
        raise ValueError("propager_monte_carlo : x et u de tailles differentes")
    rng = np.random.default_rng(graine)
    p = x.size

    if loi == "normale":
        z = rng.standard_normal((p, n))
        R = _matrice_correlation(rho, p)
        if not np.allclose(R, np.eye(p)):
            z = _racine_matricielle(R) @ z
        tirages = x[:, None] + u[:, None] * z
    elif loi == "uniforme":
        R = _matrice_correlation(rho, p)
        if np.allclose(R, np.eye(p)):
            s = rng.uniform(-1.0, 1.0, (p, n))
        elif np.allclose(np.abs(R), 1.0):
            # Cas physique << meme lot >> : un seul ecart relatif commun, applique a
            # toutes les entrees avec le signe de leur correlation. Les marginales
            # restent exactement uniformes, ce qu'une copule gaussienne ne garantit pas.
            commun = rng.uniform(-1.0, 1.0, (1, n))
            s = np.sign(R[0])[:, None] * commun
        else:
            raise ValueError(
                "loi='uniforme' : seules les correlations 0 et +/-1 sont traitees "
                "exactement (une correlation intermediaire demanderait une copule). "
                "Utiliser loi='normale' pour un rho quelconque."
            )
        tirages = x[:, None] + u[:, None] * s
    else:
        raise ValueError(
            "loi inconnue : %r (attendu 'normale', 'uniforme' ou son synonyme "
            "'rectangulaire')" % (loi,))

    y = np.asarray(modele(tirages), float).ravel()
    if y.size != n:
        raise ValueError(
            "propager_monte_carlo : le modele doit accepter un tableau (p, n) et "
            "rendre (n,) ; il a rendu %d valeurs pour %d tirages" % (y.size, n)
        )
    moy = float(y.mean())
    ec = float(y.std(ddof=1))
    y0 = float(modele(x))
    detail = {
        "nominal": y0,
        "biais_relatif": moy / y0 - 1.0 if y0 != 0 else np.nan,
        "quantiles": (float(np.quantile(y, 0.05)), float(np.quantile(y, 0.95))),
        "n": int(n),
        "loi": loi,
        "graine": graine,
        "noms": tuple(noms) if noms is not None else tuple("x%d" % j for j in range(p)),
    }
    return Propagation(moy, ec, ec / moy if moy != 0 else np.nan, "monte-carlo", detail)


# --------------------------------------------------------------------------
# 4. Le pole f0 = 1 / (2 pi racine(L C))
# --------------------------------------------------------------------------

def f0_lc(L, C):
    """Frequence propre (le POLE) d'une cellule LC : f0 = 1/(2 pi racine(LC)), en Hz.

    Rappel de nommage gele (§ 09.4) : f0 est un REPERE, la frequence propre.
    La frequence de raccord du TIPE, elle, est f_x, la frequence de CROISEMENT des
    deux voies (|H_PB| = |H_PH|, § 04.1). Les deux ne coincident que sur une
    charge resistive ideale : pour 18 mH / 150 uF sur 8 ohms, f0 = 96,86 Hz.
    """
    return 1.0 / (2.0 * np.pi * np.sqrt(np.asarray(L, float) * np.asarray(C, float)))


def u_f0_relative(uL_rel, uC_rel, rho=0.0):
    """Incertitude-type RELATIVE sur f0, propagation lineaire. Entrees = INCERTITUDES-TYPES.

        u(f0)/f0 = (1/2) racine( (u_L/L)^2 + (u_C/C)^2 + 2 rho (u_L/L)(u_C/C) )

    PHYSIQUE. ln f0 = -ln(2 pi) - (1/2)(ln L + ln C) : les sensibilites relatives
    valent -1/2 pour L comme pour C, d'ou le facteur 1/2 devant la racine. C'est ce
    facteur qui distingue ce LC du RC du premier ordre de la v1 (abandonne), dont la
    formule sans 1/2 donnait le fameux << 11 % >> -- chiffre qui ne doit plus jamais
    etre produit dans ce TIPE (§ 09.6).

    Le terme en rho rend l'hypothese d'independance EXPLICITE au lieu de la laisser
    implicite. Elle ne va pas de soi : deux composants du meme lot derivent ensemble,
    et une self bobinee maison dont on ajuste le nombre de spires APRES avoir mesure
    le condensateur reel est, elle, correlee negativement (c'est d'ailleurs comme cela
    qu'on rattrape une tolerance). A 10 %/10 % : rho = 0 donne 7,07 %, rho = +1 donne
    10,0 %, rho = -1 donne 0.

    ATTENTION aux unites d'entree : ce sont des INCERTITUDES-TYPES relatives. Pour
    une tolerance de catalogue +/- 10 %, passer type_b_rectangulaire(0.10) = 5,77 %,
    ce qui donne 4,08 %. Passer 0.10 directement donne 7,07 %, qui est la BORNE AU
    PIRE CAS. Les deux chiffres sont justes, ils ne repondent pas a la meme question :
    voir u_f0(), qui rend le couple et evite de les confondre.

    Parametres
    ----------
    uL_rel, uC_rel : float -- incertitudes-types RELATIVES sur L et C (0,0577 pour 5,77 %).
    rho : float dans [-1, 1] -- correlation entre L et C.

    Retour
    ------
    float : u(f0)/f0, sans dimension.
    """
    uL = float(uL_rel)
    uC = float(uC_rel)
    rho = float(rho)
    if not -1.0 <= rho <= 1.0:
        raise ValueError("u_f0_relative : rho doit etre dans [-1, 1]")
    variance = uL ** 2 + uC ** 2 + 2.0 * rho * uL * uC
    return 0.5 * np.sqrt(max(variance, 0.0))


def u_f0(L, C, tol_L, tol_C, rho=0.0):
    """Budget complet sur f0. Entrees = TOLERANCES (demi-largeurs). Rend LE COUPLE.

    Cette fonction est le garde-fou du module : elle ne rend JAMAIS un nombre seul,
    parce que le nombre seul est precisement ce qui a produit les confusions de la
    v1. Elle rend les deux lectures de la meme tolerance, chacune etiquetee :

    - borne_pire_cas    : demi-largeurs combinees en quadrature. Repond a << de
      combien f0 peut-elle etre fausse au pire ? >>. 7,07 % pour L et C a +/- 10 %.
      A citer TOUJOURS avec l'etiquette << borne au pire cas >>.
    - incertitude_type  : convention GUM retenue pour tout le TIPE. Chaque tolerance
      est lue comme une loi rectangulaire (u = a/racine(3)) avant propagation.
      4,08 % pour L et C a +/- 10 %. C'est ce chiffre qui se compare a un
      Monte-Carlo, qui se combine avec d'autres incertitudes, et qui s'elargit par
      k = 2 pour declarer un resultat.

    Le rapport des deux vaut exactement racine(3) = 1,732 quand les deux tolerances
    sont lues de la meme facon -- ce n'est pas une contradiction entre deux methodes,
    c'est un changement de question.

    Ordre de grandeur a retenir pour l'oral : sur les tolerances de catalogue
    (L +/- 10 %, C +/- 20 %), u(f0)/f0 = 6,5 % ; sur des composants MESURES a 1 %,
    elle tombe sous 1 % (§ 09.8) -- c'est l'argument metrologique en faveur de
    optimiser_sur_stock() plutot que du rachat de composants.

    Parametres
    ----------
    L, C : float -- valeurs nominales en H et F (SI, toujours).
    tol_L, tol_C : float -- tolerances RELATIVES, demi-largeurs (0.10 pour +/- 10 %).
    rho : float -- correlation entre les ecarts de L et de C.

    Retour
    ------
    CoupleF0(borne_pire_cas, incertitude_type, f0_Hz, u_borne_Hz, u_type_Hz, rho)
        Les deux premiers champs sont RELATIFS (sans dimension), les deux suivants
        en Hz. Le deballage naturel << borne, u_type = u_f0(...)[:2] >> rend le couple.
    """
    borne = u_f0_relative(tol_L, tol_C, rho)
    type_gum = u_f0_relative(
        type_b_rectangulaire(tol_L), type_b_rectangulaire(tol_C), rho
    )
    f0 = float(f0_lc(L, C))
    return CoupleF0(borne, type_gum, f0, borne * f0, type_gum * f0, float(rho))


def mc_f0(L, C, uL_rel, uC_rel, n=N_MC_DEFAUT, loi="normale", graine=0, rho=0.0):
    """Monte-Carlo sur f0 = 1/(2 pi racine(LC)). Signature gelee (§ 09.4).

    PIEGE DES UNITES, repete parce que c'est celui de la section :
      - loi='normale'  -> uL_rel et uC_rel sont des ECARTS-TYPES relatifs ;
      - loi='uniforme' -> ce sont des DEMI-LARGEURS relatives, et l'ecart-type
        effectivement tire vaut a/racine(3).
    C'est pour cela que mc_f0(L, C, 0.10, 0.10, loi='uniforme') rend 4,09 % (a
    comparer a la convention GUM, 4,08 %) tandis que loi='normale' rend 7,24 % (a
    comparer a la borne au pire cas, 7,07 %).

    La MOYENNE rendue n'est pas f0(L, C) : f0 est convexe en L et en C, donc
    E[f0] > f0(E[L], E[C]). A 10 %/10 % en loi normale, le biais vaut +0,77 %,
    conforme au developpement limite (3/8)(uL^2 + uC^2) = 0,75 % (voir
    biais_relatif_mc_f0). Ce biais est un RESULTAT : il dit qu'une population de
    filtres construits avec des composants a +/- 10 % a une frequence propre moyenne
    legerement SUPERIEURE a la valeur nominale.

    Correlation : rho quelconque en loi normale ; en loi uniforme, seuls 0 et +/-1
    sont traites exactement (rho = +1 = deux composants du meme lot).

    Retour
    ------
    (moyenne_Hz, ecart_type_relatif) : couple (float, float). L'ecart-type relatif
    est rapporte a la MOYENNE des tirages, pas a la valeur nominale.
    """
    def modele(x):
        return 1.0 / (2.0 * np.pi * np.sqrt(x[0] * x[1]))

    res = propager_monte_carlo(
        modele, (L, C), (uL_rel * L, uC_rel * C), rho=rho, n=n, loi=loi,
        graine=graine, noms=("L", "C"),
    )
    return res.valeur, res.u_relative


def biais_relatif_mc_f0(uL_rel, uC_rel):
    """Biais attendu de E[f0] par rapport a f0 nominale : (3/8)(u_L^2 + u_C^2).

    Developpement limite de (1+x)^(-1/2) = 1 - x/2 + (3/8)x^2 + ... : en esperance,
    le terme lineaire disparait et il reste (3/8)Var(x) par variable. A 10 %/10 %
    cela fait +0,75 %, et le Monte-Carlo mesure +0,77 %. Valable pour une loi
    symetrique quelconque (seule la variance intervient a cet ordre) : en loi
    uniforme a +/- 10 % les variances valent (0,10/racine(3))^2 et le biais tombe a
    +0,25 %.
    """
    return 0.375 * (float(uL_rel) ** 2 + float(uC_rel) ** 2)


# --------------------------------------------------------------------------
# 5. Budget d'incertitude sur le module de l'impedance
# --------------------------------------------------------------------------

def facteur_soustraction(configuration, R_ref, module_Z):
    """Facteur d'amplification de l'incertitude de lecture selon le cablage.

    PHYSIQUE (§ 02.2). Un oscilloscope de lycee a ses deux masses reliees au
    chassis : un seul noeud du montage peut recevoir les pinces, donc l'une des deux
    tensions s'obtient par SOUSTRACTION de phaseurs, et elle herite des incertitudes
    des deux lectures. Pour des erreurs relatives egales epsilon sur les deux voies :

        config A (dipole a la masse, on lit V_d et V_tot) : c = racine(2)(1 + |Z|/R_ref)
        config B (R_ref a la masse, on lit V_R et V_tot)  : c = racine(2)(1 + R_ref/|Z|)
        config C (noeud milieu a la masse, GBF flottant)  : c = racine(2)

    et u(|Z|)/|Z| = racine( (u_Rref/R_ref)^2 + c^2 epsilon^2 ).

    Regle de choix : on met a la masse l'element dont la TENSION est la plus petite ;
    le point de bascule est |Z| = R_ref. La configuration C, quand le GBF est
    flottant, supprime le probleme : c = racine(2) partout, aucune amplification.

    Retour
    ------
    float : le facteur c (sans dimension), a comparer a racine(2) = 1,414 qui est le
    plancher de la methode.
    """
    conf = str(configuration).upper()
    R_ref = float(R_ref)
    Z = float(module_Z)
    if conf == "A":
        return np.sqrt(2.0) * (1.0 + Z / R_ref)
    if conf == "B":
        return np.sqrt(2.0) * (1.0 + R_ref / Z)
    if conf == "C":
        return np.sqrt(2.0)
    raise ValueError("configuration inconnue : %r (attendu 'A', 'B' ou 'C')" % (configuration,))


def epsilon_voie(desappariement=0.010, repetabilite=0.010, divisions=6.0,
                 gain_pleine_echelle=0.03, voies_appariees=True):
    """Incertitude relative de lecture d'UNE voie d'oscilloscope, avec le partage A/B.

    PHYSIQUE (§ 02.7). Quatre sources, et une seule est aleatoire :

    - desappariement des deux voies apres correction par kappa : TYPE B. Seul le
      RAPPORT des deux voies compte dans Z = R_ref V_d/V_R, donc une erreur de gain
      COMMUNE s'elimine exactement ; il ne reste que le desappariement residuel.
      Ordre de grandeur 1 %, a remplacer par la mesure de kappa par couple de calibres.
    - gain vertical : TYPE B. Specifie en pourcentage de la PLEINE ECHELLE (3 % sur
      8 divisions pour un oscilloscope pedagogique courant), donc l'erreur relative
      sur la LECTURE vaut 3 % * 8/divisions : 4 % a 6 divisions, 12 % a 2 divisions.
      C'est l'argument chiffre du << remplir l'ecran >>. N'est comptee que si
      voies_appariees=False (sinon elle s'elimine dans le rapport, voir ci-dessus).
    - quantification 8 bits : TYPE B, loi rectangulaire. Le quantum vaut
      8 divisions/256 = 1/32 de division, soit en relatif q = (8/256)/divisions, et
      l'incertitude-type u = q/racine(12) (demi-largeur q/2 divisee par racine(3)) :
      0,15 % a 6 divisions, 0,45 % a 2 divisions.
    - repetabilite de lecture : TYPE A, la seule. A obtenir par 5 lectures repetees
      (type_a_repetabilite), pas par ce tableau : le << 1 % >> par defaut est un
      ordre de grandeur de travail, pas une mesure.

    Retour
    ------
    dict : {'epsilon', 'epsilon_A', 'epsilon_B', 'contributions'} ou contributions
    est un OrderedDict nom -> (u_relative, 'A' ou 'B').
    """
    q = (8.0 / 256.0) / float(divisions)          # quantum, en relatif de la lecture
    u_quant = q / np.sqrt(12.0)                   # loi rectangulaire de largeur q
    contributions = OrderedDict()
    contributions["repetabilite"] = (float(repetabilite), "A")
    contributions["desappariement"] = (float(desappariement), "B")
    contributions["quantification"] = (float(u_quant), "B")
    if not voies_appariees:
        contributions["gain_vertical"] = (
            float(gain_pleine_echelle) * 8.0 / float(divisions), "B"
        )
    uA = np.sqrt(sum(v ** 2 for v, t in contributions.values() if t == "A"))
    uB = np.sqrt(sum(v ** 2 for v, t in contributions.values() if t == "B"))
    return {
        "epsilon": float(np.hypot(uA, uB)),
        "epsilon_A": float(uA),
        "epsilon_B": float(uB),
        "contributions": contributions,
    }


def budget_module_Z(R_ref, module_Z, epsilon, u_rel_R_ref=0.01, configuration="A",
                    u_rel_f=0.0, pente_log=0.0):
    """Budget d'incertitude complet sur |Z| = R_ref |V_d| / |V_R|, contributions nommees.

    PHYSIQUE (§ 02.7). La formule produit/quotient naive

        u(|Z|)/|Z| = racine( (u_R/R)^2 + (u_Vd/Vd)^2 + (u_VR/VR)^2 )

    est FAUSSE en configuration A ou B : elle suppose V_d et V_R independantes, alors
    que l'une des deux vient d'une soustraction de l'autre. Le calcul correct, mene
    sur les grandeurs REELLEMENT LUES, fait apparaitre le facteur d'amplification c
    de facteur_soustraction() :

        u(|Z|)/|Z| = racine( (u_Rref/R_ref)^2 + c^2 epsilon^2 + (pente * u_f/f)^2 )

    Sur le plateau la formule naive est optimiste de 0,2 point ; au pic elle l'est de
    plus de 2 points.

    PARTAGE A/B, qui est l'objet du module. La tolerance de R_ref est de TYPE B et
    totalement correlee d'un point a l'autre : elle ne disperse pas la courbe Z(f),
    elle la MULTIPLIE en bloc. Consequence a retenir : elle ne se moyenne pas sur les
    69 points, elle ne se voit pas dans le chi2 de l'ajustement de l'acte 2, et elle
    se propage telle quelle sur Re, Res et Le (voir budget_parametres_ts).

    Parametres
    ----------
    R_ref : float -- resistance etalon, en ohms.
    module_Z : float -- |Z| du point considere, en ohms (le budget en depend : au pic
        l'amplification de la soustraction est maximale en configuration A).
    epsilon : float OU dict rendu par epsilon_voie()
        Incertitude relative de lecture par voie. Passer le dict permet de separer
        les composantes A et B ; passer un float les regroupe sous l'etiquette 'A+B'.
    u_rel_R_ref : float -- incertitude-type relative sur R_ref (0,01 pour 1 %).
    configuration : 'A', 'B' ou 'C' (voir facteur_soustraction).
    u_rel_f : float -- incertitude-type relative sur la frequence lue (1e-5 avec un
        frequencemetre 6 chiffres ; 2,5e-3 a 40 Hz si on se contente de 0,1 Hz).
    pente_log : float -- pente locale d ln|Z| / d ln f. Sur le flanc d'un pic elle
        vaut environ le facteur de qualite mecanique (jusqu'a 17 pour un 18 pouces) :
        c'est ce qui transforme une lecture de frequence bacle en 4 % sur |Z|.

    Retour
    ------
    dict : {'u_relative', 'u_relative_A', 'u_relative_B', 'facteur_soustraction',
            'configuration', 'contributions'} ou contributions est un OrderedDict
            nom -> (u_relative, type).
    """
    c = facteur_soustraction(configuration, R_ref, module_Z)
    contributions = OrderedDict()
    contributions["R_ref"] = (float(u_rel_R_ref), "B")

    if isinstance(epsilon, dict):
        eps_A, eps_B = epsilon["epsilon_A"], epsilon["epsilon_B"]
        if eps_A > 0:
            contributions["lecture_aleatoire"] = (c * eps_A, "A")
        if eps_B > 0:
            contributions["lecture_systematique"] = (c * eps_B, "B")
    else:
        contributions["lecture"] = (c * float(epsilon), "A+B")

    if u_rel_f != 0.0 and pente_log != 0.0:
        contributions["frequence"] = (abs(float(pente_log) * float(u_rel_f)), "B")

    def _somme(types):
        return np.sqrt(sum(v ** 2 for v, t in contributions.values() if t in types))

    return {
        "u_relative": float(_somme(("A", "B", "A+B"))),
        "u_relative_A": float(_somme(("A",))),
        "u_relative_B": float(_somme(("B",))),
        "facteur_soustraction": float(c),
        "configuration": str(configuration).upper(),
        "contributions": contributions,
    }


def u_phase_degres(f, u_dt):
    """Incertitude sur la phase lue par decalage temporel : u(phi) = 360 f u(dt), en degres.

    PHYSIQUE (§ 02.3). phi[deg] = 360 f dt : l'incertitude de pointe se
    convertit en degres avec un facteur proportionnel a la FREQUENCE. Un pointe a
    50 us coute 0,18 degre a 10 Hz, 1,8 degre a 100 Hz et 9 degres a 500 Hz : c'est
    la raison pour laquelle il faut resserrer la base de temps quand la frequence
    monte, ou passer a une detection synchrone sur une acquisition exportee.
    """
    return 360.0 * np.asarray(f, float) * np.asarray(u_dt, float)


def budget_point_Z_mc(R_ref, u_R_ref, V_d, u_V_d, V_ref, u_V_ref, theta_deg,
                      u_theta_deg, configuration="A", n=200_000, graine=0):
    """Monte-Carlo sur un point de mesure complet : rend |Z|, u(|Z|), phi, u(phi).

    PHYSIQUE. Contrairement a la forme close de budget_module_Z(), qui suppose Z
    reelle, ce Monte-Carlo travaille sur les PHASEURS : il tire les deux amplitudes,
    la resistance etalon et le dephasage lu, fait la soustraction complexe quand il y
    a lieu, et lit la dispersion du module ET de la phase du resultat. C'est le seul
    moyen simple d'obtenir u(phi) A TRAVERS une soustraction de phaseurs.

    Configurations (§ 02.2) :
      'A' : on lit V_d (bornes du dipole) et V_ref = V_tot (chaud du GBF) ;
            V_R = V_tot - V_d est reconstruite par soustraction complexe.
            theta = arg(V_d) - arg(V_tot).
      'C' : on lit les deux tensions directement, V_ref = V_R, aucune soustraction.
            theta = arg(V_d) - arg(V_R) = phi directement.

    Controle croise attendu (donnees ILLUSTRATIVES, § 02.7) : pour R_ref = 100
    ohms +/- 1 %, epsilon = 1,4 % par voie et Z = 14,1 ohms a -47,5 degres, le
    Monte-Carlo rend 2,4 % et la forme close 2,5 % : l'ecart vient de ce que la forme
    close suppose Z reelle. Les deux methodes reposent sur le meme modele statistique,
    leur accord valide la propagation.

    Retour
    ------
    dict : {'module', 'u_module', 'u_module_relative', 'phase_deg', 'u_phase_deg',
            'configuration', 'n', 'graine'}.
    """
    conf = str(configuration).upper()
    rng = np.random.default_rng(graine)
    R = rng.normal(R_ref, u_R_ref, n)
    A = rng.normal(V_d, u_V_d, n)
    T = rng.normal(V_ref, u_V_ref, n)
    th = np.radians(rng.normal(theta_deg, u_theta_deg, n))

    Vd_c = V_d * np.exp(1j * np.radians(theta_deg))
    if conf == "A":
        Z_tirages = R * (A * np.exp(1j * th)) / (T - A * np.exp(1j * th))
        Z_nominal = R_ref * Vd_c / (V_ref - Vd_c)
    elif conf == "C":
        Z_tirages = R * (A * np.exp(1j * th)) / T
        Z_nominal = R_ref * Vd_c / V_ref
    else:
        raise ValueError(
            "budget_point_Z_mc : configuration %r non traitee (A ou C ; la B est la A "
            "avec les roles de R_ref et du dipole echanges)" % (configuration,)
        )

    module = float(abs(Z_nominal))
    u_module = float(np.abs(Z_tirages).std(ddof=1))
    return {
        "module": module,
        "u_module": u_module,
        "u_module_relative": u_module / module,
        "phase_deg": float(np.degrees(np.angle(Z_nominal))),
        "u_phase_deg": float(np.degrees(np.angle(Z_tirages)).std(ddof=1)),
        "configuration": conf,
        "n": int(n),
        "graine": graine,
    }


# --------------------------------------------------------------------------
# 6. Types A et B sur les parametres de Thiele-Small identifies
# --------------------------------------------------------------------------

def parametres_immunises(noms=NOMS_TS):
    """Parametres T-S insensibles a une erreur d'ECHELLE sur R_ref : ('fs', 'Qms').

    PHYSIQUE (§ 03.5). fs est une POSITION sur l'axe des frequences et Qms une
    FORME (une largeur relative de pic) : multiplier toute la courbe |Z(f)| par 1,01
    ne deplace pas le sommet du pic et ne change pas sa largeur relative. Re, Res et
    Le sont au contraire des NIVEAUX, homogenes a des ohms lus sur l'axe vertical :
    ils sont multiplies par le meme 1,01.

    A ne pas surinterpreter : cette immunite vaut contre une erreur d'echelle
    verticale, PAS contre une erreur sur la frequence lue, qui deplacerait fs.
    """
    return tuple(n for n in noms if SENSIBILITE_RREF.get(n, 1.0) == 0.0)


def parametres_herites(noms=NOMS_TS):
    """Parametres T-S qui heritent lineairement de l'erreur de R_ref : ('Re', 'Le', 'Res')."""
    return tuple(n for n in noms if SENSIBILITE_RREF.get(n, 1.0) != 0.0)


def budget_parametres_ts(theta, u_A, u_rel_R_ref=0.01, u_B_relatives_sup=None,
                         noms=NOMS_TS):
    """Combine type A (ajustement) et type B (chaine de mesure) sur les parametres T-S.

    POURQUOI CETTE FONCTION EXISTE (§ 03.5, le point central du module). Les
    trois estimateurs disponibles apres l'ajustement -- covariance s^2 (J^T J)^-1,
    Monte-Carlo sur le bruit, jackknife -- concordent a +/- 14 % sur le jeu
    synthetique. Cet accord est rassurant et trompeur : ils mesurent TOUS LES TROIS
    la meme chose, la dispersion due au bruit ALEATOIRE. Aucun ne voit qu'une erreur
    d'echelle sur R_ref decale Re de 1 % sans que le chi2 bronche. Avec une
    resistance etalon ordinaire a 3 %, le biais sur Re vaut pres de 7 u_cov :
    l'incertitude dominante ne serait pas celle qu'on affiche.

    D'ou le tableau produit ici : pour chaque parametre, u_A (ce que l'ajustement
    sait), u_B (ce que la chaine impose), leur composee, et la mention explicite
    << immunise >> ou non.

    Parametres
    ----------
    theta : dict nom -> valeur, ou sequence de len(noms) valeurs
        Les parametres identifies, en SI (Re et Res en ohms, Le en henry, fs en Hz).
    u_A : dict ou sequence -- incertitudes-types ABSOLUES de type A, typiquement
        racine(diag(cov)) rendu par ajuster_ts (convention gelee : (J^T J)^-1 SANS le
        facteur s^2, § 03.5 -- s^2 est un diagnostic, pas un correctif).
    u_rel_R_ref : float -- incertitude-type RELATIVE sur R_ref (0,01 pour une 1 %
        mesuree au multimetre ; 0,03 pour une resistance ordinaire).
    u_B_relatives_sup : dict nom -> u_relative, facultatif
        Autres composantes systematiques, propres a un parametre. Cas reel prevu :
        la derive thermique de la bobine mobile sur Re (le cuivre gagne 0,393 %/K,
        soit 2 % pour 5 K), obtenue en relevant Re au multimetre avant et apres le
        balayage -- une a deux heures de manip a la main (§ 03.5).

    Retour
    ------
    OrderedDict nom -> dict(valeur, u_A, u_B, u_composee, u_relative_composee,
                            U_k2, immunise, sensibilite_R_ref, part_B_pourcent)
        part_B_pourcent est la part de la VARIANCE apportee par le type B : au-dessus
        de 50 %, l'incertitude affichee par l'ajustement seul est trompeuse.
    """
    def _en_dict(x, quoi):
        if isinstance(x, dict):
            manquants = [n for n in noms if n not in x]
            if manquants:
                raise ValueError("%s : parametres absents : %s" % (quoi, ", ".join(manquants)))
            return {n: float(x[n]) for n in noms}
        x = np.asarray(x, float).ravel()
        if x.size != len(noms):
            raise ValueError("%s : %d valeurs attendues, %d recues" % (quoi, len(noms), x.size))
        return {n: float(v) for n, v in zip(noms, x)}

    th = _en_dict(theta, "budget_parametres_ts (theta)")
    ua = _en_dict(u_A, "budget_parametres_ts (u_A)")
    sup = dict(u_B_relatives_sup or {})
    inconnus = [n for n in sup if n not in noms]
    if inconnus:
        raise ValueError("u_B_relatives_sup : noms inconnus : %s" % ", ".join(inconnus))

    budget = OrderedDict()
    for nom in noms:
        c = SENSIBILITE_RREF.get(nom, 1.0)
        u_b_rel = np.hypot(c * float(u_rel_R_ref), float(sup.get(nom, 0.0)))
        u_b = u_b_rel * abs(th[nom])
        u_c = float(np.hypot(ua[nom], u_b))
        budget[nom] = {
            "valeur": th[nom],
            "u_A": ua[nom],
            "u_B": float(u_b),
            "u_composee": u_c,
            "u_relative_composee": u_c / abs(th[nom]) if th[nom] != 0 else np.nan,
            "U_k2": float(elargir(u_c)),
            "immunise": c == 0.0,
            "sensibilite_R_ref": float(c),
            "part_B_pourcent": 100.0 * u_b ** 2 / u_c ** 2 if u_c > 0 else 0.0,
        }
    return budget


def tableau_budget_ts(budget, titre="Budget d'incertitude des parametres T-S"):
    """Met en forme le retour de budget_parametres_ts() en tableau texte (ASCII).

    Destine au journal de tout_refaire.py et a l'annexe du dossier : le jury doit
    pouvoir lire d'un coup d'oeil quelle part de l'incertitude vient de l'ajustement
    et quelle part vient de la chaine de mesure.
    """
    lignes = [titre, "-" * len(titre)]
    lignes.append(
        "%-5s %12s %11s %11s %11s %7s  %s"
        % ("param", "valeur", "u_A", "u_B", "u_composee", "part B", "immunise / R_ref")
    )
    for nom, b in budget.items():
        lignes.append(
            "%-5s %12.6g %11.4g %11.4g %11.4g %6.1f %%  %s"
            % (
                nom, b["valeur"], b["u_A"], b["u_B"], b["u_composee"],
                b["part_B_pourcent"],
                "OUI (immunise)" if b["immunise"] else "non (herite x%.0f)" % b["sensibilite_R_ref"],
            )
        )
    lignes.append(
        "u_A : ajustement (covariance) -- u_B : chaine de mesure (R_ref, derive thermique)."
    )
    lignes.append(
        "Immunises : %s -- une position et une forme ne suivent pas une erreur d'echelle."
        % ", ".join(parametres_immunises())
    )
    return "\n".join(lignes)


# -- outils internes de la demonstration (voir demonstration_biais_Rref) ---------

def _Z_ts_local(f, Re, Le, Res, fs, Qms):
    """Modele T-S a 5 parametres, copie LOCALE pour que ce module reste autonome.

    La version de production est modele_hp.Z_ts (§ 01) : c'est elle qui fait
    foi. Celle-ci n'existe que pour la demonstration ci-dessous, afin que
    incertitudes.py n'importe aucun module voisin -- il doit rester executable seul,
    y compris sur une machine du lycee.
    """
    f = np.asarray(f, float)
    x = f / fs - fs / f
    return Re + 2j * np.pi * f * Le + Res / (1.0 + 1j * Qms * x)


def _lm_local(residus, theta0, args=(), n_iter=120, lam=1e-3):
    """Levenberg-Marquardt minimal (numpy seul), pour la demonstration uniquement.

    Meme algorithme que le repli du § 09.5 : jacobienne par differences
    finies, equations normales amorties, pas contraint positif. L'ajustement de
    production est ts_fit.ajuster_ts.
    """
    th = np.asarray(theta0, float).copy()
    J = None
    cout = lambda t: float(np.sum(residus(t, *args) ** 2))
    s = cout(th)
    for _ in range(n_iter):
        r = residus(th, *args)
        J = np.empty((r.size, th.size))
        for j in range(th.size):
            d = 1e-6 * max(abs(th[j]), 1e-12)
            tp = th.copy()
            tp[j] += d
            J[:, j] = (residus(tp, *args) - r) / d
        A, g = J.T @ J, J.T @ r
        for _ in range(40):
            try:
                pas = np.linalg.solve(A + lam * np.diag(np.diag(A)), -g)
            except np.linalg.LinAlgError:
                lam *= 10.0
                continue
            if np.all(th + pas > 0) and cout(th + pas) < s:
                th, s, lam = th + pas, cout(th + pas), max(lam / 10.0, 1e-12)
                break
            lam *= 10.0
        else:
            break
    return th, J, s


def demonstration_biais_Rref(erreurs=(0.01, 0.03), theta_vrai=(6.5, 1.2e-3, 44.0, 40.0, 1.75),
                             n_points=69, bruit_module=0.02, bruit_phase_deg=1.0, graine=3):
    """Verifie NUMERIQUEMENT que +1 % sur R_ref decale Re de +1 % et laisse fs intact.

    PROTOCOLE. On fabrique une courbe Z(f) SYNTHETIQUE (parametres typiques herites
    de archive-v1/_gen.py, JAMAIS mesures), on la bruite, on l'ajuste ; puis on
    multiplie tous les modules par (1 + d) -- ce que fait exactement une erreur
    relative d sur R_ref, puisque Z = R_ref |V_d|/|V_R| -- et on refait l'ajustement.

    Deux resultats, et le second est le plus instructif :
    1. les parametres de niveau (Re, Le, Res) se decalent de +d exactement, les
       parametres de position et de forme (fs, Qms) ne bougent pas ;
    2. le chi2 reduit est RIGOUREUSEMENT INCHANGE : l'erreur est invisible pour tous
       les diagnostics d'ajustement. C'est la definition meme d'une incertitude de
       type B, et la raison d'etre de budget_parametres_ts().

    Le fait que ce soit exact et non approche tient a une identite d'echelle du
    modele : (1+d) Z_ts(f ; Re, Le, Res, fs, Qms) = Z_ts(f ; (1+d)Re, (1+d)Le,
    (1+d)Res, fs, Qms), et a ce que les poids de l'ajustement sont RELATIFS (u
    proportionnelle a |Z|), donc eux aussi invariants d'echelle. L'identite est
    verifiee ici a la precision machine, avant tout ajustement.

    Retour
    ------
    dict : {'ecart_identite', 'reference', 'u_cov', 'resultats'} ou resultats est une
    liste de dicts (un par erreur testee) contenant les ecarts relatifs par parametre,
    le chi2 reduit et le decalage exprime en nombre de u_cov.
    """
    vrai = np.asarray(theta_vrai, float)
    f = np.geomspace(10.0, 500.0, int(n_points))
    Z = _Z_ts_local(f, *vrai)

    # 1. identite d'echelle du modele, verifiee AVANT tout ajustement
    d0 = 0.01
    ecart_identite = float(
        np.max(np.abs((1 + d0) * Z - _Z_ts_local(f, vrai[0] * (1 + d0), vrai[1] * (1 + d0),
                                                 vrai[2] * (1 + d0), vrai[3], vrai[4])))
    )

    # 2. courbe synthetique bruitee (SYNTHETIQUE : aucune mesure de l'enceinte)
    rng = np.random.default_rng(graine)
    module = np.abs(Z) * (1.0 + bruit_module * rng.standard_normal(f.size))
    phase = np.degrees(np.angle(Z)) + bruit_phase_deg * rng.standard_normal(f.size)

    def residus(th, f, mod, phi, u_mod, u_phi):
        Zm = _Z_ts_local(f, *th)
        return np.concatenate([(np.abs(Zm) - mod) / u_mod,
                               (np.degrees(np.angle(Zm)) - phi) / u_phi])

    theta0 = vrai * 1.3  # depart volontairement decale de 30 %, identique pour tous les cas
    resultats = []
    reference = None
    u_cov = None
    for d in (0.0,) + tuple(erreurs):
        mod_d = module * (1.0 + d)
        u_mod = bruit_module * mod_d          # ponderation RELATIVE : invariante d'echelle
        u_phi = np.full(f.size, bruit_phase_deg)
        th, J, s = _lm_local(residus, theta0, args=(f, mod_d, phase, u_mod, u_phi))
        chi2_reduit = s / (2 * f.size - th.size)
        if d == 0.0:
            reference = th.copy()
            u_cov = np.sqrt(np.diag(np.linalg.inv(J.T @ J)))
            continue
        ecarts = th / reference - 1.0
        resultats.append({
            "erreur_R_ref": float(d),
            "ecarts_relatifs": OrderedDict(zip(NOMS_TS, ecarts)),
            "decalage_en_u_cov": OrderedDict(
                zip(NOMS_TS, (th - reference) / u_cov)),
            "chi2_reduit": float(chi2_reduit),
        })
    return {
        "ecart_identite": ecart_identite,
        "reference": OrderedDict(zip(NOMS_TS, reference)),
        "u_cov": OrderedDict(zip(NOMS_TS, u_cov)),
        "resultats": resultats,
    }


# --------------------------------------------------------------------------
# 7. Autotest : reproduit les nombres de controle du § 09.6, test (c)
# --------------------------------------------------------------------------

def _autotest(n=N_MC_DEFAUT):
    """Rejoue les controles chiffres du module et affiche le detail.

    Les criteres sont ceux de REFERENCE-TECHNIQUE.md § 09.6, test (c) ; la
    suite unittest de analyse/tests/test_incertitudes.py les reprend formellement.
    """
    ok = True

    def verifier(libelle, valeur, attendu, tolerance):
        nonlocal ok
        passe = abs(valeur - attendu) <= tolerance
        ok = ok and passe
        print("  [%s] %-46s %10.5f  (attendu %.5f +/- %.5f)"
              % ("OK " if passe else "NON", libelle, valeur, attendu, tolerance))

    print("=" * 78)
    print("incertitudes.py -- autotest (donnees SYNTHETIQUES, aucune mesure)")
    print("=" * 78)

    # --- (c1) convention GUM contre borne au pire cas -------------------------
    a = 0.10
    u = type_b_rectangulaire(a)
    print("\n1. Tolerance +/- 10 %% -> incertitude-type %.4f %% (a/racine(3))" % (100 * u))
    verifier("u_f0_relative (incertitudes-types, GUM)", u_f0_relative(u, u), 0.0408, 5e-4)
    verifier("u_f0_relative (demi-largeurs, pire cas)", u_f0_relative(a, a), 0.0707, 5e-4)
    verifier("u_f0_relative, rho = +1 (meme lot)", u_f0_relative(a, a, rho=1.0), 0.1000, 1e-6)
    verifier("u_f0_relative, rho = -1 (compensation)", u_f0_relative(a, a, rho=-1.0), 0.0, 1e-9)

    c = u_f0(18e-3, 150e-6, 0.10, 0.10)
    print("\n2. u_f0(18 mH, 150 uF, +/-10 %, +/-10 %) : le COUPLE, jamais un nombre seul")
    print("   f0 = %.3f Hz ; borne au pire cas %.2f %% (%.2f Hz) ; "
          "incertitude-type %.2f %% (%.2f Hz)"
          % (c.f0_Hz, 100 * c.borne_pire_cas, c.u_borne_Hz,
             100 * c.incertitude_type, c.u_type_Hz))
    verifier("rapport borne / incertitude-type = racine(3)",
             c.borne_pire_cas / c.incertitude_type, RACINE_3, 1e-9)
    verifier("f0 du filtre catalogue (18 mH, 150 uF)", c.f0_Hz, 96.859, 1e-2)

    # --- (c2) Monte-Carlo contre propagation lineaire -------------------------
    print("\n3. Monte-Carlo (n = %d) contre propagation lineaire" % n)
    moy_u, u_mc_u = mc_f0(18e-3, 150e-6, a, a, n=n, loi="uniforme", graine=7)
    verifier("MC loi uniforme (demi-largeurs) <-> GUM", u_mc_u, 0.0409, 1e-3)
    moy_n, u_mc_n = mc_f0(18e-3, 150e-6, a, a, n=n, loi="normale", graine=7)
    verifier("MC loi normale (ecarts-types) <-> pire cas", u_mc_n, 0.0724, 3e-3)
    _, u_mc_r = mc_f0(18e-3, 150e-6, a, a, n=n, loi="normale", graine=7, rho=1.0)
    verifier("MC rho = +1 (meme lot)", u_mc_r, 0.1000, 1e-2)
    f0_nom = float(f0_lc(18e-3, 150e-6))
    verifier("biais du MC : E[f0] > f0(E[L], E[C])", moy_n / f0_nom - 1.0, 0.0075, 1.5e-3)
    print("   biais attendu au 2e ordre (3/8)(uL^2+uC^2) = %.4f %% ; observe %.4f %%"
          % (100 * biais_relatif_mc_f0(a, a), 100 * (moy_n / f0_nom - 1.0)))
    print("   f0 moyen : %.2f Hz (uniforme) / %.2f Hz (normale) pour %.2f Hz nominal"
          % (moy_u, moy_n, f0_nom))

    # --- interface commune des deux propagations ------------------------------
    modele_f0 = lambda x: 1.0 / (2.0 * np.pi * np.sqrt(x[0] * x[1]))
    lin = propager_lineaire(modele_f0, (18e-3, 150e-6),
                            (u * 18e-3, u * 150e-6), noms=("L", "C"))
    mc = propager_monte_carlo(modele_f0, (18e-3, 150e-6),
                              (u * 18e-3, u * 150e-6), n=n, graine=7, noms=("L", "C"))
    print("\n4. Meme interface, deux methodes (entrees = incertitudes-types) :")
    print("   lineaire    : f0 = %.3f Hz, u = %.3f Hz (%.3f %%)"
          % (lin.valeur, lin.u, 100 * lin.u_relative))
    print("   monte-carlo : f0 = %.3f Hz, u = %.3f Hz (%.3f %%), biais %+.3f %%"
          % (mc.valeur, mc.u, 100 * mc.u_relative, 100 * mc.detail["biais_relatif"]))
    print("   parts de variance (lineaire) : " + ", ".join(
        "%s %.1f %%" % (nom, part)
        for nom, part in zip(lin.detail["noms"], lin.detail["part_variance"])))
    verifier("accord lineaire / MC sur u(f0) (< 3 %)",
             mc.u_relative / lin.u_relative, 1.0, 0.03)

    # --- (5) budget sur |Z| ---------------------------------------------------
    print("\n5. Budget sur |Z| = R_ref |V_d|/|V_R| (§ 02.7), R_ref = 100 ohms a 1 %")
    eps = epsilon_voie()
    print("   epsilon par voie = %.3f %% (type A %.3f %%, type B %.3f %%) ; detail :"
          % (100 * eps["epsilon"], 100 * eps["epsilon_A"], 100 * eps["epsilon_B"]))
    for nom, (v, t) in eps["contributions"].items():
        print("     %-16s %6.3f %%   type %s" % (nom, 100 * v, t))
    print("   u(|Z|)/|Z| en % (k=1), configuration A :")
    print("     eps/voie |  |Z| =     5      8     20     50    120    172 ohms")
    for e in (0.020, 0.014, 0.010):
        ligne = "  ".join("%5.1f" % (100 * budget_module_Z(100.0, z, e)["u_relative"])
                          for z in (5, 8, 20, 50, 120, 172))
        print("       %.1f %%  |          %s" % (100 * e, ligne))
    verifier("plateau 8 ohms, eps = 1,4 %",
             budget_module_Z(100.0, 8.0, 0.014)["u_relative"], 0.024, 5e-4)
    verifier("pic 172 ohms, eps = 1,4 % (config A)",
             budget_module_Z(100.0, 172.0, 0.014)["u_relative"], 0.055, 5e-4)
    verifier("config C (GBF flottant), 172 ohms",
             budget_module_Z(100.0, 172.0, 0.014, configuration="C")["u_relative"],
             0.0222, 5e-4)
    b = budget_module_Z(100.0, 14.1, eps, u_rel_f=1e-5, pente_log=17.0)
    print("   detail au point 14,1 ohms (c = %.3f) : total %.2f %% "
          "= type A %.2f %% + type B %.2f %%"
          % (b["facteur_soustraction"], 100 * b["u_relative"],
             100 * b["u_relative_A"], 100 * b["u_relative_B"]))
    for nom, (v, t) in b["contributions"].items():
        print("     %-22s %6.3f %%   type %s" % (nom, 100 * v, t))

    print("\n6. Monte-Carlo sur un point complet (phaseurs) contre la forme close")
    Z_essai = 14.1 * np.exp(-1j * np.radians(47.5))
    V_tot = 2.0
    Vd_c = V_tot * Z_essai / (100.0 + Z_essai)
    pt = budget_point_Z_mc(100.0, 1.0, abs(Vd_c), 0.014 * abs(Vd_c), V_tot,
                           0.014 * V_tot, float(np.degrees(np.angle(Vd_c))), 1.5,
                           n=200_000, graine=0)
    print("   |Z| = %.2f +/- %.2f ohm (%.1f %%) ; phi = %+.1f +/- %.1f deg"
          % (pt["module"], pt["u_module"], 100 * pt["u_module_relative"],
             pt["phase_deg"], pt["u_phase_deg"]))
    print("   forme close (Z reelle de meme module) : %.1f %% ; "
          "formule naive (V_d, V_R independantes) : %.1f %%  <- optimiste"
          % (100 * budget_module_Z(100.0, 14.1, 0.014)["u_relative"],
             100 * np.sqrt(0.01 ** 2 + 2 * 0.014 ** 2)))
    verifier("MC phaseurs <-> forme close (< 0,3 point)",
             100 * pt["u_module_relative"],
             100 * budget_module_Z(100.0, 14.1, 0.014)["u_relative"], 0.3)
    print("   u(phi) = 360 f u(dt) : %.2f deg a 100 Hz pour un pointe a 50 us"
          % u_phase_degres(100.0, 50e-6))

    # --- (6) types A et B sur les parametres T-S ------------------------------
    print("\n7. Type A / type B sur les parametres T-S (§ 03.5)")
    demo = demonstration_biais_Rref()
    print("   identite d'echelle du modele verifiee a %.1e ohm (precision machine)"
          % demo["ecart_identite"])
    print("   ajustement de reference : " + ", ".join(
        "%s = %.5g" % (k, v) for k, v in demo["reference"].items()))
    for r in demo["resultats"]:
        print("   erreur R_ref %+.0f %% -> " % (100 * r["erreur_R_ref"]) + ", ".join(
            "%s %+.3f %%" % (k, 100 * v) for k, v in r["ecarts_relatifs"].items())
            + " ; chi2 reduit %.4f" % r["chi2_reduit"])
    r1 = demo["resultats"][0]
    verifier("Re suit R_ref (+1 % -> +1 %)", r1["ecarts_relatifs"]["Re"], 0.01, 1e-4)
    verifier("Le suit R_ref (+1 % -> +1 %)", r1["ecarts_relatifs"]["Le"], 0.01, 1e-4)
    verifier("Res suit R_ref (+1 % -> +1 %)", r1["ecarts_relatifs"]["Res"], 0.01, 1e-4)
    verifier("fs immunise (+1 % -> 0 %)", r1["ecarts_relatifs"]["fs"], 0.0, 1e-4)
    verifier("Qms immunise (+1 % -> 0 %)", r1["ecarts_relatifs"]["Qms"], 0.0, 1e-4)
    verifier("chi2 reduit inchange (l'erreur est invisible)",
             r1["chi2_reduit"], demo["resultats"][-1]["chi2_reduit"], 1e-9)
    print("   decalage de +1 % exprime en u_cov : " + ", ".join(
        "%s %+.2f u" % (k, v) for k, v in r1["decalage_en_u_cov"].items()))

    print()
    budget = budget_parametres_ts(demo["reference"], demo["u_cov"], u_rel_R_ref=0.01,
                                  u_B_relatives_sup={"Re": 0.02})
    print(tableau_budget_ts(budget))
    verifier("part du type B sur Re (> 50 % : ajustement seul trompeur)",
             budget["Re"]["part_B_pourcent"], 95.0, 5.0)
    verifier("part du type B sur fs (nulle : parametre immunise)",
             budget["fs"]["part_B_pourcent"], 0.0, 1e-9)
    print("  (la composante supplementaire de 2 % sur Re est la derive thermique de la "
          "bobine mobile,\n   ordre de grandeur pour 5 K -- a remplacer par l'ecart Re "
          "avant/apres balayage mesure en phase 1)")

    print("\n" + "=" * 78)
    print("AUTOTEST : %s" % ("tous les controles passent" if ok else "AU MOINS UN ECHEC"))
    print("=" * 78)
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if _autotest() else 1)
