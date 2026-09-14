# -*- coding: utf-8 -*-
"""self_bobine.py -- conception de la self de grave et MODELE DE COUT du cuivre.

Satellite « self optimale » du TIPE (voir REFERENCE-TECHNIQUE.md § 05, et le
contrat d'interface du § 09.4). Le module repond a deux questions distinctes :

  1. DESSINER une bobine a air : combien de spires, quel rayon, quel fil, pour
     obtenir L henrys en perdant au plus r ohms ?  (formule de Wheeler
     multicouche, proportions de Brooks, table de fils normalises)
  2. FOURNIR A optim.py un modele de cout coherent : combien coute -- en cuivre,
     en euros, en watts -- une self de valeur L et de resistance r ?

LE POINT LE PLUS IMPORTANT DU MODULE (defaut signale par la relecture du § 04.5).
La § 04 utilisait deux placeholders :

    dcr(L)    = 1.0 * L/18e-3        # ohm, lineaire en L
    prix_L(L) = 4.0 + 1.2*L/1e-3     # euros, affine en L

Ils sont PHYSIQUEMENT INCOMPATIBLES. « r proportionnel a L » suppose une masse de
cuivre CONSTANTE ; « prix proportionnel a L » suppose une masse PROPORTIONNELLE a
L, auquel cas la DCR devrait etre quasi constante. Chiffre : dcr(18 mH) = 1 ohm
correspond a 4,25 kg de cuivre (106 EUR), tandis que prix_L(18 mH) = 25,6 EUR
n'achete que 1,02 kg, soit 2,58 ohms. Facteur 4,2 en masse, 2,6 en DCR.
Consequence : l'optimiseur croyait acheter une self a la fois bon marche et peu
resistive -- objet qui n'existe pas -- et, les deux fonctions etant monotones de
la seule variable L, elles etaient PARFAITEMENT CORRELEES : le front de Pareto
degenerait en une droite et le satellite n'alimentait aucun arbitrage.

Le bon modele passe par la MASSE de cuivre, seule grandeur devant laquelle les
trois exigences (inductance, pertes, matiere) sont commensurables :

    m = K_CU * (L/r)^(3/2)        avec K_CU ~ 1760 kg.s^-3/2 (+/- 10 %)

Le diametre du fil a DISPARU. La consequence de methode est que r cesse d'etre
une fonction de L : c'est une VARIABLE DE CONCEPTION a part entiere, payee en
cuivre. Diviser la DCR par deux multiplie le cuivre par 2^1,5 = 2,83.
Demonstration et domaine de validite : voir K_cu_analytique() et § 05.6.

Conventions du projet respectees ici :
  - tout en SI (henry, metre, kilogramme, ohm) ; conversions a l'affichage seulement ;
  - docstrings et messages en francais SANS ACCENTS (console cp1252, § 09.4) ;
    le fichier, lui, est en UTF-8 ;
  - numpy SEUL : aucune dependance a scipy (les integrales elliptiques sont
    calculees par la moyenne arithmetico-geometrique). C'est un choix, pas une
    contrainte : scipy est installe (verifie le 2026-09-13) ;
  - AUCUNE MESURE de l'enceinte de Thomas n'existe a ce jour. Tout nombre produit
    ici est CALCULE a partir de constantes tabulees, ou etiquete [[a verifier]].

Lancement de la demonstration complete (tous les nombres de controle du § 05) :
    python analyse/self_bobine.py
"""

import sys

import numpy as np

# --------------------------------------------------------------------------
# 1. CONSTANTES PHYSIQUES ET CONVENTIONS DE FABRICATION
# --------------------------------------------------------------------------

MU0 = 4e-7 * np.pi                 # H/m, permeabilite du vide (exacte a 1e-10 pres)
RHO_CU = 1.72e-8                   # ohm.m, resistivite du cuivre recuit a 20 degC
RHO_M = 8960.0                     # kg/m3, masse volumique du cuivre
CP_CU = 385.0                      # J/kg/K, capacite thermique massique du cuivre
ALPHA_CU = 3.9e-3                  # 1/K, coefficient de temperature de la resistivite

# Coefficient SI de la formule de Wheeler multicouche (§ 05.2) : la formule
# d'origine est en pouces et en microhenrys, elle est homogene de degre 1 en
# longueur, donc le changement d'unite est un simple facteur.
K_WHEELER = 0.8e-6 / 0.0254        # = 3.1496e-5 H/m  (soit 25,06 mu0, PAS un multiple simple)

# Constante de la bobine de Brooks : L = K_BROOKS * N^2 * a  [H, a en metres]
# (Grover 1946 p. 98 ; verifiee ici par sommation de mutuelles, cf. constante_brooks()).
# ATTENTION : la forme « 1,6994 * mu0 * N^2 * a » qui circule est FAUSSE (+26 %) :
# elle multiplie par mu0 un coefficient qui vaut deja 1,6994 microhenry/metre.
K_BROOKS = 1.6994e-6               # H/m
K_BROOKS_ADIM = K_BROOKS / MU0     # = 1,3523 : la bonne ecriture adimensionnee

# Fabrication : surepaisseur d'email grade 2, prise a 0,08 mm pour d ~ 1 a 2 mm.
# [[a verifier : IEC 60317-0-1, tables du fournisseur]]
EMAIL = 0.08e-3                    # m
# Fraction de l'aire de fenetre occupee par les cellules carrees de fil ISOLE.
# Convention gelee (§ 05.4) : b*c*k = N * d_isole^2. Ecrire « b*c*k = N*A » avec A
# la section de cuivre NU serait une autre convention (7 % d'ecart sur r et m).
# 0,85 = bobinage regulier en couches ordonnees ; 0,75-0,80 est realiste a la main.
K_REMPLISSAGE = 0.85

# Prix du cuivre emaille au kilogramme.
# [[A VERIFIER -- ORDRE DE GRANDEUR NON SOURCE, a remplacer par un devis avant achat]]
# Source : les distributeurs francais consultes (E44, ATEC France) ne publient AUCUN
# prix au kg pour ces diametres ; ATEC facture « au cours du cuivre + plus-value de
# transformation » sur devis. 25 EUR/kg = cuivre matiere ~9-10 EUR/kg + transformation.
# Tout montant en euros de ce module lui est STRICTEMENT PROPORTIONNEL.
PRIX_KG_CU = 25.0                  # EUR/kg

# Valeur retenue du coefficient de masse pour le § 04 (§ 05.6).
# +/- 10 %, la contribution dominante etant le remplissage k et non l'email.
K_CU_DEFAUT = 1760.0               # kg.s^-3/2

# Bornes de conception, a geler avec les criteres de la phase 0 (§ 05.8).
J_MAX_DEFAUT = 3.0                 # A/mm2, densite de courant admissible sous ~20 couches
                                   # [[ordre de grandeur a geler avec les criteres]]
D_MAX_DEFAUT = 1.5e-3              # m, plus gros fil approvisionnable [[a verifier par devis]]

# Table des diametres de fil emaille couramment disponibles (m).
DIAMETRES_NORMALISES = (0.80e-3, 1.00e-3, 1.20e-3, 1.40e-3,
                        1.60e-3, 2.00e-3, 2.50e-3)


# --------------------------------------------------------------------------
# 2. LE FIL : SECTION, RESISTANCE LINEIQUE, MASSE LINEIQUE
# --------------------------------------------------------------------------

def section_cuivre(d):
    """Section de CUIVRE NU d'un fil rond de diametre d [m] -> m2.

    C'est cette section-la qui entre dans r = rho*l/A et m = rho_m*l*A ; le
    diametre ISOLE (d + email) ne sert qu'au remplissage de la fenetre.
    """
    return np.pi * np.asarray(d, float) ** 2 / 4.0


def ohm_par_metre(d, rho=RHO_CU):
    """Resistance lineique d'un fil de cuivre de diametre d [m] -> ohm/m."""
    return rho / section_cuivre(d)


def gramme_par_metre(d, rho_m=RHO_M):
    """Masse lineique d'un fil de cuivre de diametre d [m] -> g/m."""
    return 1e3 * rho_m * section_cuivre(d)


def table_fils(diametres=DIAMETRES_NORMALISES, email=EMAIL, prix_kg=PRIX_KG_CU):
    """Table calculee des fils emailles normalises (§ 05.5).

    Retourne une liste de dict : d, d_isole, section [m2], ohm/m, g/m, EUR/m.
    Aucun chiffre n'est recopie d'un catalogue : tout sort de rho_Cu et rho_m.
    """
    lignes = []
    for d in diametres:
        A = float(section_cuivre(d))
        lignes.append(dict(d=d, d_isole=d + email, A=A,
                           ohm_m=float(ohm_par_metre(d)),
                           g_m=float(gramme_par_metre(d)),
                           eur_m=prix_kg * RHO_M * A))
    return lignes


# --------------------------------------------------------------------------
# 3. INDUCTANCE : WHEELER (formule de dessin) ET MUTUELLES (modele arbitre)
# --------------------------------------------------------------------------

def L_wheeler(N, a, b, c):
    """Inductance d'une bobine multicouche a air, formule de Wheeler (1928), en SI.

    N : nombre de spires ; a : rayon MOYEN [m] ; b : longueur axiale [m] ;
    c : epaisseur radiale (rayon externe - rayon interne) [m]. Retourne L en HENRYS.

        L = 3,1496e-5 * N^2 a^2 / (6a + 9b + 10c)

    Origine : L[uH] = 0,8 a^2 N^2/(6a + 9b + 10c) avec a, b, c en POUCES. La
    formule etant homogene de degre 1 en longueur, le passage au SI est le seul
    facteur 0,8e-6/0,0254. Le coefficient n'est pas un multiple simple de mu0
    (il vaut 25,06 mu0) : Wheeler est un ajustement empirique, pas un resultat exact.

    Domaine de validite (enonce par Wheeler lui-meme) : aucune des trois dimensions
    n'ecrase les autres (rapports de 1 a 3 au plus). Exact a mieux de 1 % sur les
    geometries de ce projet -- verifie contre le modele de mutuelles, voir
    comparer_wheeler_mutuelles(). Voir § 05.2.
    """
    N = np.asarray(N, float)
    a = np.asarray(a, float)
    return K_WHEELER * N ** 2 * a ** 2 / (6.0 * a + 9.0 * np.asarray(b, float)
                                          + 10.0 * np.asarray(c, float))


def K_E(m):
    """Integrales elliptiques completes K(m) et E(m), parametre m = k^2.

    Calculees par la moyenne arithmetico-geometrique de Gauss : numpy seul,
    aucun appel a scipy.special. Controle : m = 0,5 -> K = 1,8540746773,
    E = 1,3506438810.
    """
    m = np.asarray(m, float)
    a = np.ones_like(m)
    b = np.sqrt(1.0 - m)
    c = np.sqrt(m)
    somme = 0.5 * c ** 2
    p = 1.0
    for _ in range(30):
        a, b, c = 0.5 * (a + b), np.sqrt(a * b), 0.5 * (a - b)
        p *= 2.0
        somme = somme + 0.5 * p * c ** 2
    K = np.pi / (2.0 * a)
    return K, K * (1.0 - somme)


def mutuelle_spires(r1, r2, dz):
    """Inductance mutuelle de deux spires filiformes circulaires COAXIALES [H].

    Formule de Maxwell : M = mu0 sqrt(r1 r2) [ (2/k - k) K(k) - (2/k) E(k) ],
    avec k^2 = 4 r1 r2 / ((r1 + r2)^2 + dz^2). r1, r2 : rayons [m] ;
    dz : ecart axial [m]. Vectorise (diffusion numpy).
    """
    r1 = np.asarray(r1, float)
    r2 = np.asarray(r2, float)
    m = 4.0 * r1 * r2 / ((r1 + r2) ** 2 + np.asarray(dz, float) ** 2)
    K, E = K_E(m)
    k = np.sqrt(m)
    return MU0 * np.sqrt(r1 * r2) * ((2.0 / k - k) * K - (2.0 / k) * E)


def L_spire_gmd(r, cote):
    """Self-inductance d'une spire circulaire de rayon r dont le conducteur occupe
    une cellule CARREE de cote `cote` [m] :

        L = mu0 r ( ln(8 r / rho_GMD) - 2 ),   rho_GMD = 0,44705 * cote

    rho_GMD est la distance geometrique moyenne de la section carree a elle-meme.
    C'est le terme diagonal du modele de mutuelles.
    """
    return MU0 * np.asarray(r, float) * (np.log(8.0 * np.asarray(r, float)
                                                / (0.44705 * cote)) - 2.0)


def L_filaments(r, z, cote):
    """Inductance d'un bobinage discretise en spires filiformes coaxiales [H].

        L = somme_i somme_{j != i} M_ij + somme_i L_ii

    r, z : rayons et cotes axiales des spires [m] (tableaux de meme longueur) ;
    cote : cote de la cellule carree attribuee a chaque spire [m].

    C'est le MODELE ARBITRE de la section : il ne contient aucun ajustement
    empirique, et il sert a valider la formule de Wheeler et la constante de
    Brooks. Cout memoire : 8 * N^2 octets par tableau intermediaire (2,7 Mo
    pour N = 576).
    """
    r = np.asarray(r, float)
    z = np.asarray(z, float)
    n = r.size
    R1 = r[:, None]
    R2 = r[None, :]
    DZ = z[:, None] - z[None, :]
    # diagonale bidon (dz decale de 1 m) pour eviter la singularite k -> 1 ;
    # elle est ecrasee juste apres par le terme de self-inductance.
    M = mutuelle_spires(R1, R2, DZ + np.eye(n))
    np.fill_diagonal(M, L_spire_gmd(r, cote))
    return float(M.sum())


def grille_bobinage(a, b, c, n_axial, n_radial):
    """Positions (r, z) des spires d'un bobinage rectangulaire regulier, et cote
    equivalent de la cellule.

    a : rayon moyen, b : longueur axiale, c : epaisseur radiale [m].
    Retourne (r, z, cote) avec r et z aplatis (n_axial*n_radial spires).
    La cellule etant rectangulaire (b/n_axial par c/n_radial), on lui substitue
    un carre de meme aire pour le calcul de la distance geometrique moyenne.
    """
    dr = c / n_radial
    dz = b / n_axial
    r_i = (a - c / 2.0) + (np.arange(n_radial) + 0.5) * dr
    z_j = -b / 2.0 + (np.arange(n_axial) + 0.5) * dz
    R, Z = np.meshgrid(r_i, z_j, indexing='ij')
    return R.ravel(), Z.ravel(), float(np.sqrt(dr * dz))


def L_brooks(N, a):
    """Inductance d'une bobine de Brooks : L = 1,6994e-6 * N^2 * a  [H, a en m].

    Bobine de Brooks (1931) = section CARREE c x c, rayon interieur c, rayon
    exterieur 2c, longueur axiale c, donc rayon moyen a = 1,5 c. Ce sont les
    proportions qui maximisent L a longueur de fil donnee (§ 05.3, § 05.4).
    """
    return K_BROOKS * np.asarray(N, float) ** 2 * np.asarray(a, float)


def constante_brooks(n_cotes=(8, 16, 24), c=0.020):
    """Retrouve la constante 1,6994e-6 H/m par sommation de mutuelles (§ 05.3).

    La section carree c x c est discretisee en n x n cellules (N = n^2 spires) ;
    on calcule L/(N^2 a) pour plusieurs finesses, puis on extrapole a n -> infini
    par Richardson (erreur supposee en 1/n) sur les deux grilles les plus fines.

    Retourne (liste de dict par grille, constante extrapolee).
    """
    lignes = []
    for n in n_cotes:
        s = c / n
        a = 1.5 * c
        r, z, cote = grille_bobinage(a, c, c, n, n)
        L = L_filaments(r, z, cote)
        N = n * n
        lignes.append(dict(n=n, N=N, L=L, ratio=L / (N ** 2 * a),
                           ratio_mu0=L / (MU0 * N ** 2 * a), s=s))
    (n1, v1), (n2, v2) = ((lignes[-2]['n'], lignes[-2]['ratio']),
                          (lignes[-1]['n'], lignes[-1]['ratio']))
    extrapole = (n2 * v2 - n1 * v1) / (n2 - n1)
    return lignes, extrapole


def comparer_wheeler_mutuelles():
    """Test numerique de la formule de Wheeler contre le modele de mutuelles (§ 05.2).

    Quatre geometries dans le domaine de validite. Retourne une liste de dict
    (nom, N, a, b, c, L_wheeler, L_mutuelles, ecart_pct).
    """
    cas = []
    # Brooks c = 20 mm, N = 576 (24 x 24) et c = 33 mm, N = 400 (20 x 20)
    for c_mm, n in ((20.0, 24), (33.0, 20)):
        c = c_mm * 1e-3
        cas.append(('Brooks c=%dmm N=%d' % (c_mm, n * n), 1.5 * c, c, c, n, n))
    # bobine aplatie (b = c/2) et bobine allongee (b = 2c), meme nombre de spires
    c = 0.020
    cas.append(('aplatie b=c/2', 1.5 * c, c / 2.0, c, 12, 24))
    cas.append(('allongee b=2c', 1.5 * c, 2.0 * c, c, 48, 12))
    res = []
    for nom, a, b, cc, n_ax, n_rad in cas:
        r, z, cote = grille_bobinage(a, b, cc, n_ax, n_rad)
        N = n_ax * n_rad
        Lw = float(L_wheeler(N, a, b, cc))
        Lm = L_filaments(r, z, cote)
        res.append(dict(nom=nom, N=N, a=a, b=b, c=cc, L_wheeler=Lw,
                        L_mutuelles=Lm, ecart_pct=100.0 * (Lw / Lm - 1.0)))
    return res


# --------------------------------------------------------------------------
# 4. POURQUOI BROOKS : L'OPTIMISATION DE FORME, A LA MAIN PUIS NUMERIQUEMENT
# --------------------------------------------------------------------------

def proportions_optimales_wheeler():
    """Proportions qui maximisent L a longueur de fil ET section de fil donnees,
    dans le modele de Wheeler -- resolution analytique (§ 05.4).

    Avec l = 2 pi a N (longueur de la spire moyenne), N = l/(2 pi a) donne

        L = 3,1496e-5/(4 pi^2) * l^2 / (6a + 9b + 10c)

    A l fixe, maximiser L revient a MINIMISER 6a + 9b + 10c sous la contrainte de
    volume de fenetre a*b*c = cte. Multiplicateurs de Lagrange :

        6 = lam*b*c , 9 = lam*a*c , 10 = lam*a*b   =>   6a = 9b = 10c

    d'ou b/a = 6/9 = 2/3 EXACTEMENT et c/a = 6/10 = 0,600, a comparer a Brooks
    exact : b/a = c/a = 1/1,5 = 0,6667. La longueur axiale est trouvee exactement,
    l'epaisseur radiale a 10 % pres : l'ecart mesure l'imprecision de Wheeler, pas
    une erreur de raisonnement.

    Retourne (beta, gamma) = (b/a, c/a).
    """
    return 6.0 / 9.0, 6.0 / 10.0


def L_relative_forme_wheeler(beta, gamma):
    """Inductance relative d'une bobine de forme (beta, gamma) = (b/a, c/a), a
    LONGUEUR DE FIL et SECTION DE FIL fixees, dans le modele de Wheeler.

    Les contraintes s'enchainent : remplissage b*c*k = N*d_isole^2 avec b = beta*a
    et c = gamma*a donne a^3 = l d_isole^2/(2 pi k beta gamma), donc
    a ~ (beta gamma)^(-1/3) et N = l/(2 pi a) ~ (beta gamma)^(1/3). En reportant
    dans Wheeler (L = K N^2 a/(6 + 9 beta + 10 gamma)) :

        L ~ (beta gamma)^(1/3) / (6 + 9 beta + 10 gamma)

    Grandeur sans dimension, utilisable telle quelle pour comparer des formes.
    """
    beta = np.asarray(beta, float)
    gamma = np.asarray(gamma, float)
    return (beta * gamma) ** (1.0 / 3.0) / (6.0 + 9.0 * beta + 10.0 * gamma)


def L_relative_forme_mutuelles(beta, gamma, N_cible=144):
    """Meme grandeur que L_relative_forme_wheeler, mais calculee par le modele de
    mutuelles -- sans aucune formule empirique.

    On calcule le facteur de forme sans dimension G = L/(mu0 N^2 a) sur une
    bobine a l'echelle unite, puis on applique la meme mise a l'echelle qu'en
    Wheeler : L ~ G(beta, gamma) * (beta gamma)^(1/3).

    N_cible fixe la finesse de discretisation (elle n'est pas la physique : G n'en
    depend que par le terme logarithmique de self-inductance des cellules).
    """
    n_rad = max(1, int(round(np.sqrt(N_cible * gamma / beta))))
    n_ax = max(1, int(round(np.sqrt(N_cible * beta / gamma))))
    N = n_ax * n_rad
    a = 1.0
    r, z, cote = grille_bobinage(a, beta * a, gamma * a, n_ax, n_rad)
    L = L_filaments(r, z, cote)
    G = L / (MU0 * N ** 2 * a)
    return G * (beta * gamma) ** (1.0 / 3.0)


def balayage_forme(betas=(0.50, 0.60, 0.667, 0.75),
                   gammas=(0.40, 0.50, 0.60, 0.667, 0.75, 0.90, 1.10),
                   modele='wheeler', N_cible=144):
    """Balayage numerique de la forme (b/a, c/a) a longueur de fil fixee.

    Retourne (tableau des L relatives normalisees a 1 au maximum, betas, gammas).
    Sert a montrer DEUX choses (§ 05.4) : (i) l'optimum numerique retombe sur les
    proportions de Brooks, (ii) et surtout l'optimum est TRES PLAT -- se tromper de
    10 % sur les proportions coute 0,1 % d'inductance, tandis qu'un solenoide long
    et fin perd pres de 30 %.
    """
    f = (L_relative_forme_wheeler if modele == 'wheeler'
         else (lambda b, g: L_relative_forme_mutuelles(b, g, N_cible)))
    T = np.array([[float(f(b, g)) for g in gammas] for b in betas])
    return T / T.max(), np.asarray(betas, float), np.asarray(gammas, float)


def optimum_forme_wheeler(n=601):
    """Maximum numerique de L_relative_forme_wheeler sur une grille fine.

    Doit retrouver le resultat de Lagrange (2/3 ; 0,600) : c'est le controle que
    le calcul a la main et le calcul numerique parlent bien du meme probleme.
    Retourne (beta*, gamma*).
    """
    b = np.linspace(0.2, 1.6, n)
    g = np.linspace(0.2, 1.6, n)
    T = L_relative_forme_wheeler(b[:, None], g[None, :])
    i, j = np.unravel_index(np.argmax(T), T.shape)
    return float(b[i]), float(g[j])


# --------------------------------------------------------------------------
# 5. DESSIN D'UNE SELF : LA BOBINE DE BROOKS DE VALEUR L
# --------------------------------------------------------------------------

def brooks(L, d=1.4e-3, k=K_REMPLISSAGE, email=EMAIL, prix_kg=PRIX_KG_CU):
    """Dimensionne une bobine de BROOKS de valeur L [H] bobinee en fil de diametre
    d [m] -- c'est la fonction de dessin de la section.

    Chaine de raisonnement (§ 05.7), entierement analytique :
        L = K_BROOKS * N^2 * a   et   a = 1,5 c   et   c^2 k = N d_isole^2
        => L = 1,5 K_BROOKS d_isole N^2,5 / sqrt(k)
        => N = ( L sqrt(k) / (1,5 K_BROOKS d_isole) )^0,4
    puis c = d_isole sqrt(N/k), a = 1,5 c, l = 2 pi a N, r = rho l/A, m = rho_m A l.

    Retourne un dict SI : N, a, b, c, D_ext (= 4c), ell (longueur de fil), A,
    r (DCR), m (masse de cuivre), prix, tau = L/r, n_couches, spires_par_couche,
    et L_verif (relecture de L par L_brooks, controle de coherence interne).

    Validation externe du modele, SANS aucun parametre ajuste (§ 05.7) : la DCR
    predite tombe a +/- 4 % de trois references de catalogue, dont une A LA VALEUR
    CIBLE de 18 mH. Voir valider_catalogue().
    """
    L = np.asarray(L, float)
    di = d + email
    N = (L * np.sqrt(k) / (1.5 * K_BROOKS * di)) ** 0.4
    c = di * np.sqrt(N / k)
    a = 1.5 * c
    A = float(section_cuivre(d))
    ell = 2.0 * np.pi * a * N
    r = RHO_CU * ell / A
    m = RHO_M * A * ell
    return dict(L=L, d=d, d_isole=di, k=k, N=N, a=a, b=c, c=c, D_ext=4.0 * c,
                ell=ell, A=A, r=r, m=m, prix=prix_kg * m, tau=L / r,
                n_couches=c / di, spires_par_couche=c / di,
                L_verif=L_brooks(N, a))


def valider_catalogue():
    """Confronte le modele Brooks a trois fiches produit, sans parametre ajuste.

    Les DCR de catalogue sont des donnees EXTERNES citees (§ 05.7, Sources) ; le
    modele, lui, ne connait que rho_Cu, rho_m et K_BROOKS. Retourne une liste de
    dict (reference, L, d, r_modele, r_catalogue, ecart_pct).
    """
    refs = [('Mundorf BL140    2 mH / 1,4 mm', 2.0e-3, 1.4e-3, 0.43),
            ('Mundorf BL140  1,5 mH / 1,4 mm', 1.5e-3, 1.4e-3, 0.38),
            ('Mundorf serie L 18 mH / 0,71 mm', 18.0e-3, 0.71e-3, 4.77)]
    res = []
    for nom, L, d, r_cat in refs:
        r_mod = float(brooks(L, d)['r'])
        res.append(dict(reference=nom, L=L, d=d, r_modele=r_mod,
                        r_catalogue=r_cat, ecart_pct=100.0 * (r_mod / r_cat - 1.0)))
    return res


# --------------------------------------------------------------------------
# 6. LA LOI r x m, ET SA CORRECTION EXACTE m = K_CU (L/r)^(3/2)
# --------------------------------------------------------------------------

def produit_rm_geometrie_figee(ell):
    """Produit r x m d'une bobine dont la GEOMETRIE est figee (N, a fixes) [ohm.kg].

        r = rho_Cu l/A ,  m = rho_m l A   =>   r x m = rho_Cu rho_m l^2

    La section A a disparu : a longueur de fil fixee, on n'echange la resistance
    contre RIEN D'AUTRE que du cuivre, dans un rapport fixe par la seule longueur.
    Doubler la section divise r par 2 et multiplie m par 2. C'est la version
    « premier ordre » de la loi r x m ~ cte (§ 05.6).
    """
    return RHO_CU * RHO_M * np.asarray(ell, float) ** 2


def longueur_depuis_masse_et_dcr(m, r):
    """Longueur de fil deduite de la masse et de la DCR mesurees, SANS connaitre
    le diametre du fil [m] :

        l = sqrt( m r / (rho_Cu rho_m) )

    C'est la loi r x m relue comme un INSTRUMENT DE MESURE (§ 05.14) : la moyenne
    geometrique des deux estimateurs l = m/(rho_m A) et l = r A/rho_Cu elimine A.
    Verifie sur la Mundorf BL140 : 39,20 m, identique au modele.
    """
    return np.sqrt(np.asarray(m, float) * np.asarray(r, float) / (RHO_CU * RHO_M))


def K_cu_analytique(d=1.4e-3, k=K_REMPLISSAGE, email=EMAIL):
    """Coefficient K_CU de la loi m = K_CU (L/r)^(3/2) [kg.s^-3/2], forme fermee.

        K_CU = (3 pi^2/4) * rho_m * gamma / sqrt(k) * (8 rho_Cu / K_BROOKS)^(3/2)

    avec gamma = d_isole/d. Demonstration (§ 05.6), a forme de Brooks maintenue :
        l = 3 pi d_isole N^1,5 / sqrt(k)   et   L = 1,5 K_B d_isole N^2,5/sqrt(k)
        K_CU = m (r/L)^(3/2) = rho_m rho_Cu^(3/2) l^(5/2) / (A^(1/2) L^(3/2))
    et N s'elimine (l^(5/2) et L^(3/2) sont tous deux en N^3,75). LE DIAMETRE DU
    FIL DISPARAIT AUSSI, via d_isole/sqrt(A) = 2 gamma/sqrt(pi) : c'est le
    resultat central du § 05.

    Il ne subsiste qu'une dependance en gamma (l'email ne se met pas a l'echelle
    du diametre) et en k (remplissage). Dispersion constatee : 1823 kg.s^-3/2 a
    d = 0,8 mm, 1724 a d = 2,0 mm ; et K_CU ~ 1/sqrt(k), donc +10 % en passant de
    k = 0,85 a k = 0,70. D'ou la valeur retenue : K_CU_DEFAUT = 1760 +/- 10 %.
    """
    gamma = (d + email) / d
    return (3.0 * np.pi ** 2 / 4.0) * RHO_M * gamma / np.sqrt(k) \
        * (8.0 * RHO_CU / K_BROOKS) ** 1.5


def K_cu_numerique(L=18e-3, d=1.4e-3, k=K_REMPLISSAGE, email=EMAIL):
    """Meme coefficient, mesure sur le dimensionnement complet : K = m (r/L)^(3/2).

    Doit coincider avec K_cu_analytique() a la precision machine -- c'est le
    controle que la forme fermee n'a pas perdu un facteur en route.
    """
    b = brooks(L, d, k=k, email=email)
    return float(b['m'] * (b['r'] / b['L']) ** 1.5)


# --------------------------------------------------------------------------
# 7. MODELE DE COUT EXPOSE A optim.py  (§ 04.5 contrainte 5, § 05.9)
# --------------------------------------------------------------------------

def masse_pour(L, r, K_cu=K_CU_DEFAUT):
    """Masse de cuivre [kg] d'une self de valeur L [H] et de DCR r [ohm].

        m = K_cu * (L/r)^(3/2)

    C'EST LE MODELE A UTILISER DANS optim.py, et il remplace a lui seul les deux
    placeholders incoherents dcr(L) et prix_L(L) du § 04.6. Lecture physique :
    a L fixe, diviser la DCR par 2 multiplie le cuivre par 2^1,5 = 2,83 ; passer
    de -2,8 dB a -0,5 dB d'insertion coute 14 fois plus de cuivre. L'exposant 3/2
    est ce qui rend le filtre passif structurellement couteux en matiere dans le grave.

    Vectorise (L et r diffusent), pour l'appel par blocs de la fonction de cout.
    """
    return K_cu * (np.asarray(L, float) / np.asarray(r, float)) ** 1.5


def prix_pour(L, r, prix_kg=PRIX_KG_CU, K_cu=K_CU_DEFAUT):
    """Prix du CUIVRE d'une self (L [H], r [ohm]) -> EUR.

        prix = prix_kg * K_cu * (L/r)^(3/2)

    `prix_kg` est un parametre, et sa valeur par defaut PRIX_KG_CU = 25 EUR/kg est
    un ORDRE DE GRANDEUR NON SOURCE [[a verifier par devis]] : aucun distributeur
    consulte (E44, ATEC France) ne publie de prix au kg pour ces diametres. Tout
    montant rendu par cette fonction lui est strictement proportionnel : un prix
    reel de 20 ou 35 EUR/kg multiplie le resultat par 0,8 ou 1,4.

    NE COMPTE QUE LE CUIVRE. Mandrin, vernis, colliers, cosses : quelques centaines
    de grammes et quelques euros par self [[a chiffrer sur la facture reelle]].
    """
    return prix_kg * masse_pour(L, r, K_cu)


def dcr_pour(L, r_max=None, masse=None, K_cu=K_CU_DEFAUT):
    """DCR [ohm] retenue pour une self de valeur L [H]. Un seul des deux arguments.

    Deux lectures, toutes deux tirees de m = K_cu (L/r)^(3/2) (§ 05.8, § 05.9) :

    - `r_max` : contrainte DURE de pertes. m etant strictement decroissante en r,
      l'optimum de matiere SATURE la contrainte : r* = r_max, et le cuivre vaut
      alors m* = K_cu (L/r_max)^(3/2). La DCR ne depend donc PAS de L -- c'est
      exactement ce qui remplace le placeholder r(L) ~ L du § 04, et
      c'est la forme a utiliser quand on dimensionne une self sur commande.

    - `masse` : budget de cuivre impose par self [kg]. Alors r = L (K_cu/m)^(2/3),
      soit r PROPORTIONNELLE a L. C'est le jeu (A) « masse de cuivre fixee » du
      § 05.9 -- le placeholder lineaire du § 04.6 EST ce modele, et sa constante
      « 1 ohm a 18 mH » correspond a 4,25 kg de cuivre par self, soit 106 EUR
      (alors que le placeholder de prix n'en facturait que 25,6).

    Vectorise sur L ; retourne un tableau de la forme de L pour se brancher tel
    quel sur `r1 = dcr(L1)` dans la fonction de cout (§ 04.6).
    """
    L = np.asarray(L, float)
    if (r_max is None) == (masse is None):
        raise ValueError('dcr_pour : fournir exactement un argument parmi r_max et masse')
    if r_max is not None:
        return np.full(L.shape, float(r_max)) if L.shape else float(r_max)
    return L * (K_cu / np.asarray(masse, float)) ** (2.0 / 3.0)


def dcr_de_L(L, d_fil=1.4e-3, geometrie='brooks', k=K_REMPLISSAGE, email=EMAIL):
    """DCR [ohm] d'une self de valeur L [H] bobinee en fil de DIAMETRE IMPOSE.

    Signature gelee au § 09.4. C'est le troisieme jeu de modeles du § 05.9 -- le
    jeu (b), « on achete une seule bobine de fil et on bobine tout avec » : a
    diametre fixe et forme de Brooks maintenue, N ~ L^(2/5), a ~ L^(1/5), donc
    l ~ L^(3/5) et

        r ~ L^(3/5)   et   m ~ L^(3/5)

    (ni r ~ L a masse fixee, ni r constant a DCR fixee). C'est le modele realiste
    quand le fil est deja achete ; `dcr_pour(L, r_max=...)` est le modele realiste
    quand on dimensionne la self pour une cible de pertes.

    `geometrie` : seule 'brooks' est implementee (les proportions optimales, § 05.4).
    """
    if geometrie != 'brooks':
        raise ValueError("dcr_de_L : geometrie inconnue %r (seule 'brooks' est "
                         "implementee)" % (geometrie,))
    return brooks(L, d_fil, k=k, email=email)['r']


def masse_cuivre(L, DCR, K_cu=K_CU_DEFAUT):
    """Alias de `masse_pour`, sous la signature gelee du § 09.4 -> kg."""
    return masse_pour(L, DCR, K_cu)


def cout_self(L, r=1.5, prix_kg=PRIX_KG_CU, K_cu=K_CU_DEFAUT):
    """Alias de `prix_pour`, sous la signature gelee du § 09.4 -> EUR.

    `r` a une valeur par defaut (1,5 ohm) parce que la signature du § 09.4 ne
    porte que L ; ce defaut est le HAUT de la fenetre praticable du § 05.8, et il
    doit etre gele avec les criteres de la phase 0, pas subi.
    """
    return prix_pour(L, r, prix_kg=prix_kg, K_cu=K_cu)


def fabrique_dcr(r_max=None, masse=None, d_fil=None, K_cu=K_CU_DEFAUT):
    """Fabrique la fonction `dcr(L)` a passer a `optim.cout(..., dcr=...)`.

    Un seul des trois arguments, ce qui force l'appelant a DIRE quel modele de
    self il achete -- c'est tout l'objet du satellite :
      - r_max=1.5   : self dimensionnee sur commande, DCR plafonnee (recommande) ;
      - masse=2.0   : budget de cuivre impose par self ;
      - d_fil=1.4e-3: fil deja achete, DCR en L^(3/5).

    Exemple :
        import self_bobine as SB
        J = optim.cout(p1, p2, f, Zs, Zm, dcr=SB.fabrique_dcr(r_max=1.5))
    """
    donnes = [x is not None for x in (r_max, masse, d_fil)]
    if sum(donnes) != 1:
        raise ValueError('fabrique_dcr : fournir exactement un argument parmi '
                         'r_max, masse, d_fil')
    if d_fil is not None:
        return lambda L: dcr_de_L(L, d_fil)
    return lambda L: dcr_pour(L, r_max=r_max, masse=masse, K_cu=K_cu)


def fabrique_prix_L(r_max=None, masse=None, d_fil=None, prix_kg=PRIX_KG_CU,
                    K_cu=K_CU_DEFAUT):
    """Fabrique la fonction `prix_L(L)` COHERENTE avec `fabrique_dcr` (memes
    arguments, meme self) -- c'est precisement ce que les placeholders du § 04.6
    ne faisaient pas.
    """
    dcr = fabrique_dcr(r_max=r_max, masse=masse, d_fil=d_fil, K_cu=K_cu)
    if d_fil is not None:
        return lambda L: prix_kg * brooks(L, d_fil)['m']
    return lambda L: prix_kg * masse_pour(L, dcr(L), K_cu)


def insertion_dB(r, Z=8.0):
    """Perte d'insertion [dB, negative] d'une resistance serie r sur une charge Z.

        attenuation = -20 log10(1 + r/|Z|)

    ATTENTION : sur la charge NOMINALE 8 ohm c'est une BORNE SUPERIEURE de la
    perte reelle -- la charge vraie est Z(f), et |Z| > 8 ohm presque partout dans
    la bande du grave (~14 ohm a 100 Hz sur le modele v1), ce qui divise la perte
    par pres de deux. C'est exactement l'hypothese que le sujet v2 se donne pour
    mission de detruire. On garde 8 ohm comme convention de catalogue, donc comme
    point de comparaison honnete avec le filtre du commerce (§ 05.1).
    """
    return -20.0 * np.log10(1.0 + np.asarray(r, float) / np.abs(Z))


def fraction_dissipee(r, Z=8.0):
    """Fraction de la puissance dissipee dans la resistance serie r : r/(r+|Z|).

    Nombre de controle du depot : r = 1 ohm face a 8 ohm -> 11,1 % et -1,02 dB.
    """
    r = np.asarray(r, float)
    return r / (r + np.abs(Z))


# --------------------------------------------------------------------------
# 8. OPTIMISATION : CUIVRE MINIMAL SOUS CONTRAINTES
# --------------------------------------------------------------------------

def diametre_pour_dcr(L, r_cible, k=K_REMPLISSAGE, email=EMAIL,
                      bornes=(0.1e-3, 8.0e-3), tol=1e-9):
    """Diametre de fil [m] realisant la DCR `r_cible` pour une self de Brooks de
    valeur L, par dichotomie (r est strictement decroissante en d).
    """
    lo, hi = bornes
    f = lambda d: float(brooks(L, d, k=k, email=email)['r']) - r_cible
    if f(lo) < 0 or f(hi) > 0:
        raise ValueError('diametre_pour_dcr : r_cible = %.3f ohm hors des bornes '
                         '[%.3f ; %.3f] ohm' % (r_cible, f(hi) + r_cible, f(lo) + r_cible))
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def optimiser_self(L, r_max, P_max=350.0, R_nom=8.0, duree=60.0,
                   J_max=J_MAX_DEFAUT, d_max=D_MAX_DEFAUT,
                   k=K_REMPLISSAGE, email=EMAIL, prix_kg=PRIX_KG_CU):
    """Cuivre minimal sous contrainte d'inductance et de pertes (§ 05.8).

        min  m = rho_m l A    s.c.  L(N,a,b,c) = L_cible , r <= r_max ,
                                    b c k = N d_isole^2 , I_max/A <= J_max ,
                                    d <= d_dispo

    Resolution : la loi m = K_CU (L/r)^(3/2) etant strictement DECROISSANTE en r,
    l'optimum SATURE la contrainte de pertes (r* = r_max) et la forme optimale est
    celle de Brooks (§ 05.4). Il ne reste qu'a trouver par dichotomie le diametre
    de fil qui realise r_max -- puis a VERIFIER les deux contraintes de terrain
    que le programme initial oubliait, et qui ferment la fenetre des deux cotes :

      - en haut (pertes faibles) : l'APPROVISIONNEMENT. d = 1,9 a 2,9 mm de fil
        emaille n'est ni bobinable a la main, ni couramment vendu au detail ;
      - en bas (cuivre econome) : la THERMIQUE. a r_max = 3 ohm on est a 9 A/mm2,
        la self encaisse 131 W et derive de +9,6 % de DCR en une minute au niveau
        fort : le filtre « pas cher » echoue PAR CONSTRUCTION au critere de
        robustesse (f_0 et l'amortissement du grave changent avec le niveau).

    L'echauffement rendu est ADIABATIQUE (dT = P t/(m cp)) : c'est un MAJORANT, il
    neglige toute evacuation vers l'air.

    Retourne un dict : d, N, m, prix, D_ext, ell, insertion_dB (sur R_nom),
    I_max, J (A/mm2), P_joule, dT, derive_dcr_pct, appro_ok, thermique_ok.
    """
    d = diametre_pour_dcr(L, r_max, k=k, email=email)
    b = brooks(L, d, k=k, email=email, prix_kg=prix_kg)
    I = np.sqrt(P_max / R_nom)                       # courant efficace conventionnel
    J = I / (b['A'] * 1e6)                           # A/mm2
    P_j = r_max * I ** 2
    dT = P_j * duree / (b['m'] * CP_CU)
    return dict(L=L, r_max=r_max, d=d, N=float(b['N']), m=float(b['m']),
                prix=float(b['prix']), D_ext=float(b['D_ext']), ell=float(b['ell']),
                insertion_dB=float(insertion_dB(r_max, R_nom)), I_max=float(I),
                J=float(J), P_joule=float(P_j), dT=float(dT),
                derive_dcr_pct=100.0 * ALPHA_CU * float(dT),
                appro_ok=bool(d <= d_max), thermique_ok=bool(J <= J_max))


def budget_selfs(L, r_max, n_selfs=2, prix_kg=PRIX_KG_CU, K_cu=K_CU_DEFAUT):
    """Budget CUIVRE d'un jeu de `n_selfs` selfs identiques (L, r_max) -> dict.

    Rappel de cadrage (§ 05.10) : la feuille de route demande d'assembler DEUX
    filtres (catalogue et optimise), c'est-a-dire QUATRE selfs, pas deux -- sauf
    a bobiner une seule bobine par voie munie de PRISES intermediaires, ce qui
    divise par deux le cuivre, le prix et le temps, et permet en prime de comparer
    les deux filtres SUR LE MEME OBJET PHYSIQUE (§ 05.12).
    """
    m = float(masse_pour(L, r_max, K_cu))
    return dict(L=L, r_max=r_max, n_selfs=n_selfs, masse_unitaire=m,
                masse_totale=n_selfs * m, prix_unitaire=prix_kg * m,
                prix_total=n_selfs * prix_kg * m,
                insertion_dB=float(insertion_dB(r_max)))


# --------------------------------------------------------------------------
# 9. MESURE : RESONANCE SERIE, EFFET DE PEAU, EFFET DE PROXIMITE, THERMIQUE
# --------------------------------------------------------------------------

def f0_serie(L, C):
    """Frequence de resonance SERIE d'un couple L-C : f0 = 1/(2 pi sqrt(LC)) [Hz].

    ATTENTION AU VOCABULAIRE (§ 04.1, § 05 en-tete) : f0 est le POLE du couple
    L-C, un REPERE. Ce n'est PAS f_c, qui designe dans tout le TIPE la frequence
    de CROISEMENT des deux voies, ni les reperes a -3 dB du reseau charge. Pour
    18 mH / 150 uF sur 8 ohm : f0 = 96,86 Hz, f3_pb = 99,9 Hz, f3_ph = 93,9 Hz.
    Nombre de controle du depot : 18 mH + 150 uF -> ~97 Hz.
    """
    return 1.0 / (2.0 * np.pi * np.sqrt(np.asarray(L, float) * np.asarray(C, float)))


def L_depuis_f0(f0, C):
    """Inductance relue par la resonance serie : L = 1/(4 pi^2 f0^2 C) [H].

    METHODE DE CONTRE-VERIFICATION SEULEMENT (§ 05.13). La methode principale est
    le banc d'impedance du § 02 sur la self seule : L = Im(Z)/omega, qui
    n'importe AUCUNE incertitude sur C. Ici au contraire

        u(L)/L = sqrt( (2 u(f0)/f0)^2 + (u(C)/C)^2 )

    (le facteur 2 vient de L ~ f0^-2), et l'incertitude est ENTIEREMENT portee par
    C : u(C)/C = 20 % donne u(L)/L = 20 %. Si on emploie cette methode, mesurer
    d'abord C au capacimetre, puis recouper avec deux valeurs de C differentes.

    Piege de protocole (§ 05.13) : NE PAS chercher le maximum de courant. Avec
    R_ref = 100 ohm le Q du montage tombe a 0,108 et il n'y a plus aucun maximum
    a pointer. Le bon observable est la tension aux bornes de la paire L+C, qui
    presente un creux profond (minimum 0,0161 a 96,86 Hz) et dont la phase passe
    par zero avec une pente de 7,8 deg/Hz -- parfaitement lisible a l'oscilloscope.
    """
    f0 = np.asarray(f0, float)
    return 1.0 / (4.0 * np.pi ** 2 * f0 ** 2 * np.asarray(C, float))


def u_L_par_resonance(u_f0_rel, u_C_rel):
    """Incertitude-type relative sur L obtenue par resonance serie (§ 05.13)."""
    return np.hypot(2.0 * np.asarray(u_f0_rel, float), np.asarray(u_C_rel, float))


def epaisseur_peau(f, rho=RHO_CU, mu=MU0):
    """Epaisseur de peau dans un conducteur [m] : delta = sqrt(rho/(pi f mu)).

    Dans le cuivre a 100 Hz : delta = 6,60 mm.
    """
    return np.sqrt(rho / (np.pi * np.asarray(f, float) * mu))


def rapport_rac_rdc(d, f, rho=RHO_CU):
    """Effet de peau dans un fil rond ISOLE : R_ac/R_dc (developpement basse frequence).

        R_ac/R_dc ~ 1 + (1/48) (a/delta)^4 ,  a = d/2 RAYON du fil

    LE RAYON, PAS LE DIAMETRE : l'ecrire avec d surestime l'effet d'un facteur
    2^4 = 16. Le developpement colle a la solution exacte de Bessel au 6e chiffre
    jusqu'a 1 kHz.

    Conclusion a 100 Hz (§ 05.15) : delta = 6,60 mm, soit 6,6 fois le RAYON du plus
    gros fil envisage (2,0 mm) -> R_ac/R_dc = 1,00001. L'EFFET DE PEAU EST
    TOTALEMENT NEGLIGEABLE dans la bande du raccord, et l'argument commercial du
    fil de Litz ou du meplat pour les selfs de grave ne se justifie pas par lui.
    """
    a = np.asarray(d, float) / 2.0
    return 1.0 + (a / epaisseur_peau(f, rho)) ** 4 / 48.0


def rapport_proximite_dowell(d, n_couches, f, email=EMAIL, rho=RHO_CU):
    """Effet de PROXIMITE en bobinage multicouche, majorant de Dowell (1966).

        xi = (d/delta) (sqrt(pi)/2) sqrt(eta) ,  eta = d/d_isole
        R_ac/R_dc ~ 1 + (5 m^2 - 1)/45 * xi^4     (m = nombre de couches)

    Lui n'est PAS negligeable, et il faut le dire : a 100 Hz les selfs de 18 mH de
    la section (22 a 25 couches) donnent +1,9 % (fil 1,0 mm), +6,6 % (1,4 mm) et
    +24,9 % (2,0 mm) -- et l'effet est le plus fort pour le gros fil, celui que
    l'optimisation recommande aux faibles r_max : une part du gain de DCR obtenu
    en grossissant le fil est reprise par la proximite.

    DEUX RESERVES. Dowell est un modele 1-D de fenetre de TRANSFORMATEUR, ou un
    noyau canalise le flux ; pour une bobine A AIR le champ s'echappe par les
    bords et l'effet reel est plus faible : ces chiffres sont un MAJORANT. Mais un
    majorant de +25 % ne se balaie pas d'une phrase.

    CONDUITE A TENIR : en faire une MESURE, pas une affirmation. Comparer
    Re(Z(100 Hz)) au banc du § 02 a la DCR mesuree en continu sur la self
    bobinee est une manip de 20 minutes qui tranche. Si l'ecart depasse quelques %,
    le § 04 doit utiliser r_ac(100 Hz) et non r_dc. [[a mesurer en phase 4]]
    """
    d = np.asarray(d, float)
    eta = d / (d + email)
    xi = (d / epaisseur_peau(f, rho)) * (np.sqrt(np.pi) / 2.0) * np.sqrt(eta)
    mc = np.asarray(n_couches, float)
    return 1.0 + (5.0 * mc ** 2 - 1.0) / 45.0 * xi ** 4


def echauffement_adiabatique(P_joule, masse, duree=60.0, cp=CP_CU):
    """Elevation de temperature ADIABATIQUE du bobinage [K] : dT = P t/(m cp).

    MAJORANT : aucune evacuation vers l'air n'est prise en compte (§ 05.8).
    """
    return np.asarray(P_joule, float) * duree / (np.asarray(masse, float) * cp)


def derive_dcr(dT, alpha=ALPHA_CU):
    """Derive RELATIVE de la DCR pour une elevation dT [K] : alpha * dT.

    alpha_Cu = +0,39 %/K, soit +4 % pour 10 K. C'est directement le critere
    « robustesse » : une self qui derive change f_0 ET l'amortissement du grave
    entre les deux niveaux d'ecoute geles (Q'_es = Q_es (Re + r)/Re).
    """
    return alpha * np.asarray(dT, float)


# --------------------------------------------------------------------------
# 10. VERIFICATION : TOUS LES NOMBRES DE CONTROLE DE LA SECTION 05
# --------------------------------------------------------------------------

def verifier(verbeux=True):
    """Rejoue les controles chiffres du § 05 et retourne la liste des verdicts.

    Chaque entree : (nom, valeur calculee, valeur attendue, tolerance relative, ok).
    Aucune valeur attendue n'est un resultat de MESURE : ce sont des constantes
    tabulees, des resultats analytiques, ou trois DCR de catalogue citees.
    """
    v = []

    def ctrl(nom, calc, attendu, tol, unite=''):
        ok = abs(calc - attendu) <= tol * max(abs(attendu), 1e-30)
        v.append(dict(nom=nom, calc=calc, attendu=attendu, tol=tol, unite=unite, ok=ok))
        return ok

    # (1) integrales elliptiques
    K, E = K_E(0.5)
    ctrl('K(m=0,5) par AGM', float(K), 1.8540746773, 1e-9)
    ctrl('E(m=0,5) par AGM', float(E), 1.3506438810, 1e-9)

    # (2) Wheeler SI contre le modele de mutuelles
    cw = comparer_wheeler_mutuelles()
    ctrl('Wheeler Brooks c=20mm N=576 (mH)', 1e3 * cw[0]['L_wheeler'], 16.7941, 1e-4, 'mH')
    ctrl('mutuelles Brooks c=20mm N=576 (mH)', 1e3 * cw[0]['L_mutuelles'], 16.9136, 1e-3, 'mH')
    ctrl('ecart Wheeler/mutuelles (%)', cw[0]['ecart_pct'], -0.71, 0.05, '%')

    # (3) constante de Brooks
    lignes, extra = constante_brooks()
    ctrl('constante de Brooks extrapolee (uH/m)', 1e6 * extra, 1.6994, 5e-4, 'uH/m')
    ctrl('constante de Brooks adimensionnee', extra / MU0, 1.3523, 5e-4)

    # (4) recoupement sur un cas publie : Brooks c = 20 mm, N = 200 (QuickField : 2,033 mH)
    a = 1.5 * 0.020
    ctrl('Brooks c=20mm N=200, formule (mH)', 1e3 * float(L_brooks(200, a)), 2.0393, 1e-3, 'mH')
    ctrl('Brooks c=20mm N=200, vs elements finis (mH)',
         1e3 * float(L_brooks(200, a)), 2.033, 5e-3, 'mH')

    # (5) proportions optimales : Lagrange analytique et balayage numerique
    beta_a, gamma_a = proportions_optimales_wheeler()
    beta_n, gamma_n = optimum_forme_wheeler()
    ctrl('optimum Wheeler b/a (numerique vs Lagrange)', beta_n, beta_a, 5e-3)
    ctrl('optimum Wheeler c/a (numerique vs Lagrange)', gamma_n, gamma_a, 5e-3)
    ctrl('Lagrange b/a = 2/3 exact', beta_a, 2.0 / 3.0, 1e-12)
    ctrl('Lagrange c/a = 0,600 exact', gamma_a, 0.600, 1e-12)
    # platitude de l'optimum : Brooks contre l'optimum de Wheeler
    L_bro = float(L_relative_forme_wheeler(2. / 3., 2. / 3.))
    L_opt = float(L_relative_forme_wheeler(beta_a, gamma_a))
    ctrl('Brooks / optimum Wheeler (%)', 100.0 * L_bro / L_opt, 99.9, 2e-3, '%')

    # (6) les trois selfs de 18 mH (§ 05.7)
    for d, N_att, r_att, m_att in ((1.0e-3, 515, 2.828, 0.909),
                                   (1.4e-3, 454, 1.637, 2.021),
                                   (2.0e-3, 396, 0.919, 4.725)):
        b = brooks(18e-3, d)
        ctrl('18 mH / %.1f mm : N' % (1e3 * d), float(b['N']), N_att, 3e-3)
        ctrl('18 mH / %.1f mm : DCR (ohm)' % (1e3 * d), float(b['r']), r_att, 3e-3, 'ohm')
        ctrl('18 mH / %.1f mm : cuivre (kg)' % (1e3 * d), float(b['m']), m_att, 3e-3, 'kg')

    # (7) validation externe sur catalogue
    for c in valider_catalogue():
        ctrl('catalogue %s (ohm)' % ' '.join(c['reference'].split()[1:4]),
             c['r_modele'], c['r_catalogue'], 0.05, 'ohm')

    # (8) loi r x m et invariant m r^1,5
    b1, b2 = brooks(18e-3, 1.0e-3), brooks(18e-3, 2.0e-3)
    ctrl('r x m, rapport 1,0 -> 2,0 mm',
         float(b2['r'] * b2['m']) / float(b1['r'] * b1['m']), 1.689, 5e-3)
    ctrl('invariant m r^1,5, rapport 1,0 -> 2,0 mm',
         float(b2['m'] * b2['r'] ** 1.5) / float(b1['m'] * b1['r'] ** 1.5), 0.963, 5e-3)
    ctrl('r x m geometrie figee = rho_Cu rho_m l^2 (ohm.kg)',
         float(produit_rm_geometrie_figee(b1['ell'])), float(b1['r'] * b1['m']), 1e-12, 'ohm.kg')

    # (9) coefficient K_CU : forme fermee contre dimensionnement complet
    ctrl('K_CU analytique (d=1,4 mm)', K_cu_analytique(1.4e-3), 1752.2, 1e-3, 'kg.s^-3/2')
    ctrl('K_CU numerique = analytique', K_cu_numerique(18e-3, 1.4e-3),
         K_cu_analytique(1.4e-3), 1e-12, 'kg.s^-3/2')
    ctrl('K_CU a k = 0,70 (sensibilite au remplissage)',
         K_cu_analytique(1.4e-3, k=0.70), 1930.8, 1e-3, 'kg.s^-3/2')

    # (10) incoherence des deux placeholders du § 04.6
    ctrl('placeholder dcr(18 mH) = 1 ohm -> cuivre (kg)',
         float(masse_pour(18e-3, 1.0)), 4.25, 5e-3, 'kg')
    ctrl('placeholder dcr(18 mH) = 1 ohm -> prix (EUR)',
         float(prix_pour(18e-3, 1.0)), 106.3, 5e-3, 'EUR')
    r_du_prix = float(dcr_pour(18e-3, masse=25.6 / PRIX_KG_CU))
    ctrl('placeholder prix_L(18 mH) = 25,6 EUR -> DCR (ohm)', r_du_prix, 2.58, 5e-3, 'ohm')

    # (11) budget d'un couple de selfs de 18 mH
    for r_max, att in ((1.0, 212.5), (1.5, 115.7), (2.0, 75.1), (3.0, 40.9)):
        ctrl('couple de selfs 18 mH a r_max = %.1f ohm (EUR)' % r_max,
             budget_selfs(18e-3, r_max)['prix_total'], att, 5e-3, 'EUR')

    # (12) optimisation sous contraintes (§ 05.8)
    o = optimiser_self(18e-3, 1.5)
    ctrl('optim r_max=1,5 : d (mm)', 1e3 * o['d'], 1.477, 5e-3, 'mm')
    ctrl('optim r_max=1,5 : cuivre (kg)', o['m'], 2.297, 5e-3, 'kg')
    ctrl('optim r_max=1,5 : J (A/mm2)', o['J'], 3.86, 5e-3, 'A/mm2')
    ctrl('optim r_max=1,5 : derive DCR 1 min (%)', o['derive_dcr_pct'], 1.7, 0.05, '%')
    o3 = optimiser_self(18e-3, 3.0)
    ctrl('optim r_max=3,0 : J (A/mm2)', o3['J'], 9.05, 5e-3, 'A/mm2')
    ctrl('optim r_max=3,0 : derive DCR 1 min (%)', o3['derive_dcr_pct'], 9.6, 0.02, '%')

    # (13) pertes d'insertion : nombre de controle du depot
    ctrl('r = 1 ohm / 8 ohm : fraction dissipee (%)',
         100.0 * float(fraction_dissipee(1.0)), 11.1, 5e-3, '%')
    ctrl('r = 1 ohm / 8 ohm : attenuation (dB)', float(insertion_dB(1.0)), -1.02, 5e-3, 'dB')

    # (14) mesure : resonance serie
    ctrl('f0(18 mH, 150 uF) (Hz)', float(f0_serie(18e-3, 150e-6)), 96.86, 1e-4, 'Hz')
    ctrl('L relue par resonance (mH)',
         1e3 * float(L_depuis_f0(f0_serie(18e-3, 150e-6), 150e-6)), 18.00, 1e-6, 'mH')
    ctrl('u(L)/L pour u(f0)=0,5 % et u(C)=1 % (%)',
         100.0 * float(u_L_par_resonance(0.005, 0.010)), 1.41, 5e-3, '%')

    # (15) effet de peau et de proximite a 100 Hz
    ctrl('epaisseur de peau du cuivre a 100 Hz (mm)',
         1e3 * float(epaisseur_peau(100.0)), 6.601, 1e-3, 'mm')
    ctrl('R_ac/R_dc, fil 2,0 mm isole a 100 Hz', float(rapport_rac_rdc(2.0e-3, 100.0)),
         1.000011, 1e-4)
    ctrl('Dowell, 2,0 mm 21,6 couches a 100 Hz',
         float(rapport_proximite_dowell(2.0e-3, 21.6, 100.0)), 1.249, 5e-3)

    if verbeux:
        _afficher_verdicts(v)
    return v


def _afficher_verdicts(v):
    n_ok = sum(1 for x in v if x['ok'])
    print('  %-52s %14s %14s   %s' % ('controle', 'calcule', 'attendu', 'verdict'))
    for x in v:
        val = ('%14.6g' % x['calc'])
        att = ('%14.6g' % x['attendu'])
        print('  %-52s %s %s   %s' % (x['nom'][:52], val, att, 'ok' if x['ok'] else 'ECHEC'))
    print('  --> %d/%d controles passes' % (n_ok, len(v)))


# --------------------------------------------------------------------------
# 11. DEMONSTRATION : tout ce que le § 05 apporte, en une commande
# --------------------------------------------------------------------------

def _titre(s):
    print('\n' + s)
    print('-' * max(60, len(s)))


def demonstration():
    """Rejoue, dans l'ordre du recit, tous les resultats du satellite « self »."""
    _titre('1. INDUCTANCE : Wheeler (formule de dessin) vs mutuelles (modele arbitre)')
    K, E = K_E(0.5)
    print('  controle K,E : m = 0,5 -> K = %.10f , E = %.10f' % (K, E))
    print('                 attendu             1.8540746773   1.3506438810')
    print('  %-22s | %5s | %12s | %14s | %s'
          % ('geometrie', 'N', 'Wheeler (mH)', 'mutuelles (mH)', 'ecart'))
    for c in comparer_wheeler_mutuelles():
        print('  %-22s | %5d | %12.4f | %14.4f | %+6.2f %%'
              % (c['nom'], c['N'], 1e3 * c['L_wheeler'], 1e3 * c['L_mutuelles'],
                 c['ecart_pct']))
    print('  (les valeurs absolues dependent du nombre de spires retenu pour chaque')
    print('   geometrie ; seul l ECART Wheeler/mutuelles est la grandeur testee.)')
    print('  => Wheeler est exact a mieux de 1 % sur le domaine utile : c est la')
    print('     formule a utiliser pour DESSINER ; les mutuelles servent d arbitre.')

    _titre('2. LA BOBINE DE BROOKS : la constante, par sommation de mutuelles')
    lignes, extra = constante_brooks()
    for l in lignes:
        print('  n=%2d  N=%4d  L=%9.5f mH   L/(N^2 a) = %.4f uH/m   L/(mu0 N^2 a) = %.4f'
              % (l['n'], l['N'], 1e3 * l['L'], 1e6 * l['ratio'], l['ratio_mu0']))
    print('  extrapolation de Richardson (n -> infini) : %.4f uH/m  => %.4f mu0'
          % (1e6 * extra, extra / MU0))
    print('  valeur retenue K_BROOKS = %.4f uH/m (Grover 1946 p. 98)' % (1e6 * K_BROOKS))
    a20 = 1.5 * 0.020
    print('  recoupement cas publie (c = 20 mm, N = 200) :')
    print('    formule de Brooks            : %.4f mH' % (1e3 * L_brooks(200, a20)))
    print('    elements finis (QuickField)  : 2.0330 mH  [source externe]')
    print('    Wheeler SI                   : %.4f mH'
          % (1e3 * L_wheeler(200, a20, 0.020, 0.020)))
    faux = 1e3 * 1.6994 * MU0 * 200 ** 2 * a20      # forme qui circule, et qui est FAUSSE
    print('    forme ERRONEE 1,6994*mu0*N^2*a : %.4f mH  (%+.0f %%, a ne pas propager)'
          % (faux, 100.0 * (faux / (1e3 * L_brooks(200, a20)) - 1.0)))

    _titre('3. POURQUOI BROOKS MAXIMISE L A LONGUEUR DE FIL DONNEE')
    b_a, g_a = proportions_optimales_wheeler()
    b_n, g_n = optimum_forme_wheeler()
    print('  Lagrange sur 6a + 9b + 10c a abc = cte : 6a = 9b = 10c')
    print('    => b/a = %.4f (exactement 2/3) , c/a = %.4f  [Brooks exact : 0,6667 / 0,6667]'
          % (b_a, g_a))
    print('  balayage numerique du meme critere      : b/a = %.4f , c/a = %.4f' % (b_n, g_n))
    T, betas, gammas = balayage_forme()
    print('  L relative a longueur de fil et section de fil FIXEES (Wheeler, % de l optimum)')
    print('    b/a \\ c/a ' + ''.join('%8.3f' % g for g in gammas))
    for i, b in enumerate(betas):
        print('    %9.3f ' % b + ''.join('%7.1f%%' % (100 * x) for x in T[i]))
    print('  modele de mutuelles (sans aucune formule empirique) :')
    ref = L_relative_forme_mutuelles(2. / 3., 2. / 3.)
    for nom, bb, gg in (('Brooks          ', 2. / 3., 2. / 3.),
                        ('optimum Wheeler ', b_a, g_a),
                        ('cube a = b = c  ', 1.0, 1.0),
                        ('galette fine    ', 0.30, 0.30),
                        ('solenoide long  ', 2.00, 0.20)):
        print('    %s b/a=%.3f c/a=%.3f : L = %6.1f %% de Brooks'
              % (nom, bb, gg, 100.0 * L_relative_forme_mutuelles(bb, gg) / ref))
    print('  => L OPTIMUM EST TRES PLAT : 10 % d erreur sur la forme coute 0,1 % de L,')
    print('     une bobine cubique 2 % ; mais un solenoide long perd pres de 30 %.')
    print('     A retenir : « ne pas bobiner long et fin », pas « viser 1,5 exactement ».')

    _titre('4. LE FIL : table calculee (rho_Cu = 1,72e-8 ohm.m, rho_m = 8960 kg/m3)')
    print('  %8s | %10s | %11s | %9s | %7s | %s'
          % ('d nu(mm)', 'd emai(mm)', 'section(mm2)', 'ohm/m', 'g/m', 'EUR/m a %.0f EUR/kg' % PRIX_KG_CU))
    for l in table_fils():
        print('  %8.2f | %10.3f | %11.3f | %9.5f | %7.2f | %.3f'
              % (1e3 * l['d'], 1e3 * l['d_isole'], 1e6 * l['A'], l['ohm_m'],
                 l['g_m'], l['eur_m']))

    _titre('5. LA LOI r x m, ET SA CORRECTION EXACTE m = K_CU (L/r)^(3/2)')
    b1, b2 = brooks(18e-3, 1.0e-3), brooks(18e-3, 2.0e-3)
    print('  (a) GEOMETRIE FIGEE (N, a fixes) : r x m = rho_Cu rho_m l^2, EXACTEMENT')
    print('      l = %.1f m -> r x m = %.4f ohm.kg ; recalcul direct r*m = %.4f ohm.kg'
          % (b1['ell'], produit_rm_geometrie_figee(b1['ell']), b1['r'] * b1['m']))
    print('  (b) FORME DE BROOKS MAINTENUE (le cas reel : grossir le fil grossit la fenetre)')
    print('      N ~ A^-1/5, l ~ A^1/5 : r ~ A^-4/5 , m ~ A^6/5 , r*m ~ A^2/5')
    print('      section x4 (1,0 -> 2,0 mm) : r x%.3f [A^-4/5 : %.3f] , m x%.3f [A^6/5 : %.3f]'
          % (b2['r'] / b1['r'], 4 ** -0.8, b2['m'] / b1['m'], 4 ** 1.2))
    print('                                   r*m x%.3f [A^2/5 : %.3f] , m*r^1,5 x%.3f [invariant : 1,000]'
          % ((b2['r'] * b2['m']) / (b1['r'] * b1['m']), 4 ** 0.4,
             (b2['m'] * b2['r'] ** 1.5) / (b1['m'] * b1['r'] ** 1.5)))
    print('  => r x m varie d un facteur 1,7 sur la plage : CE N EST PAS UNE CONSTANTE,')
    print('     c est un ordre de grandeur. L invariant exact du modele est m r^(3/2).')
    print('  K_CU = (3 pi^2/4) rho_m gamma/sqrt(k) (8 rho_Cu/K_B)^(3/2) :')
    for d in (0.8e-3, 1.0e-3, 1.4e-3, 2.0e-3):
        print('    d = %4.1f mm : K_cu = %7.1f kg.s^-3/2  [numerique : %7.1f]'
              % (1e3 * d, K_cu_analytique(d), K_cu_numerique(18e-3, d)))
    print('  sensibilite au remplissage k (le parametre le MOINS maitrise du modele) :')
    for k in (0.70, 0.80, 0.85, 0.95):
        b = brooks(18e-3, 1.4e-3, k=k)
        print('    k = %.2f : N = %3.0f , r = %.3f ohm , m = %.3f kg , Dext = %3.0f mm , K_cu = %.1f'
              % (k, b['N'], b['r'], b['m'], 1e3 * b['D_ext'], K_cu_analytique(1.4e-3, k=k)))
    print('  => VALEUR RETENUE POUR LA SECTION 04 : K_CU = %.0f kg.s^-3/2 a +/- 10 %%'
          % K_CU_DEFAUT)

    _titre('6. TROIS SELFS DE 18 mH, ET LA VALIDATION EXTERNE DU MODELE')
    print('  %5s| %4s| %6s| %8s| %7s| %8s| %10s| %9s| %6s| %8s| %s'
          % ('d(mm)', 'N', 'c(mm)', 'Dext(mm)', 'fil(m)', 'DCR(ohm)', 'cuivre(kg)',
             'prix(EUR)', 'r*m', 'm*r^1.5', 'L/r(ms)'))
    for d in (1.0e-3, 1.4e-3, 2.0e-3):
        b = brooks(18e-3, d)
        print('  %5.1f| %4.0f| %6.1f| %8.1f| %7.1f| %8.3f| %10.3f| %9.1f| %6.2f| %8.3f| %7.2f'
              % (1e3 * d, b['N'], 1e3 * b['c'], 1e3 * b['D_ext'], b['ell'], b['r'],
                 b['m'], b['prix'], b['r'] * b['m'], b['m'] * b['r'] ** 1.5, 1e3 * b['tau']))
    print('  pertes d insertion sur charge NOMINALE 8 ohm (borne superieure, cf. § 05.1) :')
    for d in (1.0e-3, 1.4e-3, 2.0e-3):
        r = float(brooks(18e-3, d)['r'])
        print('    d = %.1f mm, r = %.3f ohm : fraction dissipee = %4.1f %%, attenuation = %+.2f dB'
              % (1e3 * d, r, 100 * fraction_dissipee(r), insertion_dB(r)))
    print('    nombre de controle du depot : r = 1,00 ohm -> %.1f %% et %+.2f dB'
          % (100 * fraction_dissipee(1.0), insertion_dB(1.0)))
    print('  pertes sur la charge REELLE (|Z| > 8 ohm presque partout dans le grave) :')
    for r in (1.0, 1.637, 2.828):
        print('    r = %.3f ohm : sur 8 ohm %+.2f dB | sur 14 ohm %+.2f dB | sur 30 ohm %+.2f dB'
              % (r, insertion_dB(r, 8.), insertion_dB(r, 14.), insertion_dB(r, 30.)))
    print('  validation externe, AUCUN parametre ajuste (DCR de catalogue citees) :')
    for c in valider_catalogue():
        print('    %-32s : modele %.3f ohm vs catalogue %.2f -> %+.1f %%'
              % (c['reference'], c['r_modele'], c['r_catalogue'], c['ecart_pct']))
    print('    (le 3e point est A LA VALEUR CIBLE de 18 mH : la validation porte la ou')
    print('     on utilise le modele, et non a 9 fois la valeur d interet.)')

    _titre('7. OPTIMISATION : CUIVRE MINIMAL SOUS L = 18 mH ET r <= r_max')
    print('  m = K_CU (L/r)^(3/2) est DECROISSANTE en r : l optimum SATURE r = r_max,')
    print('  et la forme optimale est celle de Brooks. Reste a trouver le fil (dichotomie).')
    I350, I10 = np.sqrt(350. / 8.), np.sqrt(10. / 8.)
    print('  I(350 W/8 ohm) = %.2f A eff ; I(10 W/8 ohm) = %.2f A eff' % (I350, I10))
    print('  %5s| %6s| %4s| %7s| %8s| %7s| %7s| %8s| %9s| %8s| %s'
          % ('r_max', 'd(mm)', 'N', 'm(kg)', 'prix(EUR)', 'Dext(mm)', 'dB/8ohm',
             'J(A/mm2)', 'P_J 350W', 'dT 1min', 'ddcr'))
    for r_max in (0.50, 0.75, 1.00, 1.50, 2.00, 3.00):
        o = optimiser_self(18e-3, r_max)
        drapeau = ''
        if not o['appro_ok']:
            drapeau += ' [appro]'
        if not o['thermique_ok']:
            drapeau += ' [thermique]'
        print('  %5.2f| %6.3f| %4.0f| %7.3f| %8.1f| %7.1f| %7.2f| %8.2f| %8.1f W| %+7.1f K| %+5.1f %%%s'
              % (r_max, 1e3 * o['d'], o['N'], o['m'], o['prix'], 1e3 * o['D_ext'],
                 o['insertion_dB'], o['J'], o['P_joule'], o['dT'],
                 o['derive_dcr_pct'], drapeau))
    print('  [appro]     : d > %.1f mm -- ni bobinable a la main ni vendu au detail [[a verifier par devis]]'
          % (1e3 * D_MAX_DEFAUT))
    print('  [thermique] : J > %.1f A/mm2 -- la self derive de plusieurs %% de DCR au niveau fort'
          % J_MAX_DEFAUT)
    print('  => LA FENETRE PRATICABLE EST r_max = 1,5 a 2 ohm. En deca le fil est')
    print('     introuvable ; au-dela le filtre « pas cher » ECHOUE PAR CONSTRUCTION')
    print('     au critere de robustesse. Le critere se decide ici, AVANT toute mesure.')
    print('  loi d echelle a retenir : passer de -2,8 dB a -0,5 dB coute %.0f fois plus de cuivre.'
          % (optimiser_self(18e-3, 0.5)['m'] / optimiser_self(18e-3, 3.0)['m']))

    _titre('8. BUDGET, ET L INCOHERENCE DES DEUX PLACEHOLDERS DE LA SECTION 04')
    print('  cuivre seul, pour un COUPLE de selfs de 18 mH (la feuille de route en demande 4) :')
    for r_max in (1.0, 1.5, 2.0, 3.0):
        b = budget_selfs(18e-3, r_max)
        print('    r_max = %.1f ohm : %5.2f kg/self , %6.1f EUR/self , %6.1f EUR le couple (%+.2f dB)'
              % (r_max, b['masse_unitaire'], b['prix_unitaire'], b['prix_total'],
                 b['insertion_dB']))
    print('  prix du cuivre : %.0f EUR/kg  [[ORDRE DE GRANDEUR NON SOURCE -- a remplacer'
          % PRIX_KG_CU)
    print('    par un devis. E44 et ATEC France ne publient aucun prix au kg.]]')
    print('    Tout montant ci-dessus lui est STRICTEMENT proportionnel.')
    print('  les deux placeholders du § 04.6, mis face a face dans le meme modele :')
    print('    dcr(18 mH) = 1,00 ohm    -> il faut %.2f kg de cuivre, soit %.1f EUR'
          % (masse_pour(18e-3, 1.0), prix_pour(18e-3, 1.0)))
    print('    prix_L(18 mH) = 25,6 EUR -> on achete %.2f kg, soit r = %.2f ohm'
          % (25.6 / PRIX_KG_CU, dcr_pour(18e-3, masse=25.6 / PRIX_KG_CU)))
    print('    => INCOHERENTS d un facteur %.1f en masse et %.1f en DCR. L optimiseur'
          % (masse_pour(18e-3, 1.0) / (25.6 / PRIX_KG_CU),
             float(dcr_pour(18e-3, masse=25.6 / PRIX_KG_CU)) / 1.0))
    print('       croyait acheter une self a la fois bon marche et peu resistive.')
    print('  les trois modeles coherents exposes a optim.py (§ 05.9) :')
    print('    (a) masse imposee m = 2,0 kg/self : r(10 mH) = %.2f ; r(18 mH) = %.2f ; r(27 mH) = %.2f ohm'
          % tuple(dcr_pour(np.array([10e-3, 18e-3, 27e-3]), masse=2.0)))
    print('    (b) fil impose d = 1,4 mm         : r ~ L^(3/5)')
    print('        %6s | %4s | %7s | %7s | %10s | %s'
          % ('L(mH)', 'N', 'r(ohm)', 'm(kg)', '(L/18)^0,6', 'r/r(18 mH)'))
    r18 = float(dcr_de_L(18e-3, 1.4e-3))
    for L in (4.7e-3, 10e-3, 18e-3, 27e-3, 47e-3):
        b = brooks(L, 1.4e-3)
        print('        %6.1f | %4.0f | %7.3f | %7.3f | %10.3f | %.3f'
              % (1e3 * L, b['N'], b['r'], b['m'], (L / 18e-3) ** 0.6, b['r'] / r18))
    print('    (c) r_max impose (recommande)     : r = r_max, INDEPENDANT de L ;')
    print('        c est le prix qui varie : prix(10 mH) = %.0f ; prix(18 mH) = %.0f ;'
          % (prix_pour(10e-3, 1.5), prix_pour(18e-3, 1.5)))
    print('        prix(27 mH) = %.0f EUR a r_max = 1,5 ohm.' % prix_pour(27e-3, 1.5))

    _titre('9. MESURE DE L : RESONANCE SERIE (contre-verification du banc d impedance)')
    for L, C in ((18e-3, 150e-6), (18e-3, 100e-6), (27e-3, 100e-6)):
        f0 = float(f0_serie(L, C))
        print('  L = %4.1f mH , C = %5.1f uF -> f0 = %6.2f Hz ; L relu = 1/(4 pi^2 f0^2 C) = %5.2f mH'
              % (1e3 * L, 1e6 * C, f0, 1e3 * L_depuis_f0(f0, C)))
    print('  => nombre de controle du depot confirme : 18 mH + 150 uF donne 96,86 Hz.')
    print('     C est le POLE du couple L-C, distinct des reperes -3 dB (99,9 et 93,9 Hz)')
    print('     et distinct de f_c, qui est le CROISEMENT des deux voies (§ 04.1).')
    print('  incertitude de la methode : u(L)/L = sqrt( (2 u(f0)/f0)^2 + (u(C)/C)^2 )')
    for uf, uc in ((0.005, 0.01), (0.005, 0.05), (0.005, 0.20)):
        print('    u(f0)/f0 = %4.1f %% , u(C)/C = %5.1f %% -> u(L)/L = %5.1f %%'
              % (100 * uf, 100 * uc, 100 * u_L_par_resonance(uf, uc)))
    print('  => l incertitude est ENTIEREMENT portee par C : d ou le banc d impedance')
    print('     (L = Im(Z)/omega) en methode principale, la resonance en recoupement.')

    _titre('10. EFFET DE PEAU ET EFFET DE PROXIMITE A 100 Hz')
    print('  delta = sqrt(rho_Cu/(pi f mu0)) :')
    for f in (100., 250., 1000., 10000.):
        print('    f = %7.0f Hz : delta = %6.3f mm' % (f, 1e3 * epaisseur_peau(f)))
    print('  fil ISOLE, R_ac/R_dc = 1 + (a/delta)^4/48 avec a = d/2 (LE RAYON) :')
    for d in (1.0e-3, 1.4e-3, 2.0e-3):
        print('    d = %.1f mm a 100 Hz : a/delta = %.3f -> R_ac/R_dc = %.6f'
              % (1e3 * d, (d / 2) / epaisseur_peau(100.), rapport_rac_rdc(d, 100.)))
    print('  CONCLUSION : a 100 Hz, delta = %.2f mm, soit %.1f fois le RAYON du plus gros'
          % (1e3 * epaisseur_peau(100.), epaisseur_peau(100.) / 1e-3))
    print('    fil envisage (2,0 mm). R_ac/R_dc = 1,00001 : L EFFET DE PEAU EST TOTALEMENT')
    print('    NEGLIGEABLE dans la bande du raccord. L argument commercial du fil de Litz')
    print('    ou du meplat pour une self de grave NE SE JUSTIFIE PAS par l effet de peau.')
    print('  MAIS l effet de PROXIMITE (bobinage multicouche) ne l est pas -- majorant de Dowell :')
    for d in (1.0e-3, 1.4e-3, 2.0e-3):
        b = brooks(18e-3, d)
        nc = float(b['n_couches'])
        print('    d = %.1f mm : %4.1f couches -> R_ac/R_dc = %.3f   (une seule couche : %.5f)'
              % (1e3 * d, nc, rapport_proximite_dowell(d, nc, 100.),
                 rapport_proximite_dowell(d, 1, 100.)))
    print('    => +2 a +25 %, et c est le GROS fil qui trinque -- celui que l optimisation')
    print('       recommande aux faibles r_max. Dowell est un modele 1-D de fenetre de')
    print('       TRANSFORMATEUR : pour une bobine a air c est un MAJORANT. Conduite a tenir :')
    print('       comparer Re(Z(100 Hz)) a la DCR continue sur la self bobinee (20 min de banc).')

    _titre('11. CONTROLES CHIFFRES (aucun n est une mesure de l enceinte)')
    v = verifier(verbeux=True)
    return v


if __name__ == '__main__':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    print('self_bobine.py -- satellite « self optimale » (REFERENCE-TECHNIQUE.md § 05)')
    print('AUCUNE MESURE DE L ENCEINTE N EXISTE A CE JOUR : tous les nombres ci-dessous')
    print('sont CALCULES a partir de constantes tabulees, ou etiquetes [[a verifier]].')
    verdicts = demonstration()
    sys.exit(0 if all(x['ok'] for x in verdicts) else 1)
