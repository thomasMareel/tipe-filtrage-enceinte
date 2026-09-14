"""Probleme inverse : identification des parametres de Thiele-Small (acte 2, § 03).

Place dans le recit. En entree : la courbe Z(f) du haut-parleur EN CAISSE, module et
phase, avec leurs incertitudes (livrable de l'acte 1, io_mesures.py). En sortie : les
parametres du modele electrique, chacun avec son incertitude, la MATRICE DE COVARIANCE
COMPLETE, les residus et la courbe "mesure vs modele". Ces parametres sont la charge sur
laquelle l'acte 3 (optim.py) optimisera le filtre.

    io_mesures.py  ->  ts_fit.py  ->  optim.py
     (mesure)         (ce module)     (filtre)
                           |
                       modele_hp.py (le modele direct Z(jw ; theta), partout le meme)
                       incertitudes.py (type A + type B, budget systematique)

Pourquoi un modele plutot que les points mesures (§ 03) : il LISSE le bruit et
INTERPOLE entre les points ; il donne un SENS PHYSIQUE aux nombres (resonance,
amortissement, inductance de bobine) ; il permet de PROPAGER les incertitudes jusqu'au
filtre optimise au lieu de trainer 70 points bruites. Le prix a payer est un domaine de
validite qu'il faut verifier : c'est l'objet des huit criteres du § 03.7, tous
implementes ici (valider_identification).

La methode en une phrase (a dire au jury) : "je cherche les cinq nombres qui minimisent
la somme des ecarts ponderes au carre entre la courbe mesuree et le modele ; comme le
modele n'est pas lineaire, je le linearise et j'itere (Gauss-Newton amorti a la
Levenberg-Marquardt) ; l'incertitude vient de la matrice (J^T J)^-1, recoupee par
Monte-Carlo et par jackknife -- et la composante systematique, elle, est ajoutee a part."

LE GARDE-FOU CENTRAL DE CE MODULE (§ 03.4, test D). Applique a une courbe a DEUX
pics (caisse bass-reflex), le modele a 5 parametres CONVERGE sans lever la moindre erreur
et rend des nombres d'allure parfaitement plausible qui ne veulent rien dire ; seuls le
chi2 reduit et la structure des residus le trahissent. Un modele inadapte ne se signale
donc PAS par une exception. D'ou garde_fou_caisse(), appele AVANT tout ajustement par
ajuster_ts() : il compte les pics, avertit bruyamment (UserWarning + banniere), et
identifier() refuse carrement de poursuivre tant que forcer=True n'est pas ecrit noir sur
blanc par l'appelant.

Conventions du fichier (§ 09.4) :
  * tout en SI (ohm, henry, farad, hertz) -- conversion en mH / uF a l'affichage seulement ;
  * la PHASE est partout en DEGRES, comme dans le CSV de mesure (colonnes phase_deg et
    u_phase_deg) ; le modele, lui, sort des radians : la conversion est faite ici, une
    fois pour toutes. Un garde-fou avertit si la phase recue ressemble a des radians ;
  * convention de signe des residus : r = (modele - mesure)/u (§ 03.2) ;
  * convention de covariance GELEE (§ 03.5) : on rapporte (J^T J)^-1 SANS le facteur
    s^2 (equivalent de absolute_sigma=True). s^2 est un DIAGNOSTIC, jamais un correctif :
    le multiplier par les barres blanchirait un defaut de modele en incertitude ;
  * francais SANS ACCENTS dans le code et les messages (console cp1252) ; fichier UTF-8 ;
  * scipy est utilise s'il est present (verifie le 2026-09-13 : 1.18.1) mais le repli
    Levenberg-Marquardt en numpy pur est ecrit, teste et compare a scipy (test G).

AVERTISSEMENT, a lire avant d'utiliser le moindre nombre produit par ce fichier : AUCUNE
MESURE N'A ENCORE ETE FAITE SUR L'ENCEINTE DE THOMAS. Toutes les donnees manipulees par
l'auto-test sont SYNTHETIQUES (modele illustratif herite de archive-v1/_gen.py, jeu
MH.JEU_SYNTHETIQUE_V1). Elles prouvent que le code retrouve ce qu'on y a mis, et surtout
COMMENT il echoue quand le modele est faux ; elles ne disent rien du sub 18 pouces.

Lancement des huit tests de diagnostic du § 03.4 :
    python analyse/ts_fit.py            (complet, ~23 s : 5 000 ajustements environ)
    python analyse/ts_fit.py --rapide   (moins de tirages, ~5 s)
"""

import hashlib
import json
import os
import sys
import warnings
from collections import OrderedDict
from datetime import datetime

import numpy as np

try:
    from scipy.optimize import least_squares
    SCIPY = True
except ImportError:                      # le poste du lycee peut ne pas avoir SciPy
    SCIPY = False

# Le dossier analyse/ doit etre importable meme si le script est lance d'ailleurs
# (par exemple par unittest discover, qui met analyse/tests/ dans sys.path).
_ICI = os.path.dirname(os.path.abspath(__file__))
if _ICI not in sys.path:
    sys.path.insert(0, _ICI)

import modele_hp as MH          # modele direct Z(jw ; theta), diagnostic de caisse
import io_mesures as IO         # lecture du CSV de mesure, diagnostic de caisse (proeminence)
import incertitudes as INC      # type A / type B, budget systematique


# =====================================================================
# 1. CONSTANTES, MODELES DISPONIBLES, EXCEPTIONS
# =====================================================================

#: bande d'AJUSTEMENT par defaut (§ 03.6 : mesurer 10-1000 Hz pour VOIR la derive
#: de bobine, ajuster d'abord sur 10-500 Hz, puis lire s^2 et le test des sequences).
BANDE_AJUSTEMENT = (10.0, 500.0)

#: bande de la PORTE DE VALIDATION (critere 2), a ne pas confondre avec la precedente.
BANDE_VALIDATION = (20.0, 300.0)

#: bande de l'AIGUILLAGE clos / bass-reflex (critere 0, § 03.7).
BANDE_AIGUILLAGE = (10.0, 100.0)

#: critere 1 : chi2 reduit acceptable. Fourchette volontairement large -- pour
#: 2N - p = 133 degres de liberte la dispersion purement statistique de s^2 n'est que
#: de racine(2/133) = 0,12 : sortir de [0,5 ; 2] ne peut PAS venir du hasard.
SEUIL_S2 = (0.5, 2.0)

#: critere 3 : test des sequences de Wald-Wolfowitz sur les signes des residus.
SEUIL_Z_SEQUENCES = 3.0

#: seuil d'alerte sur un residu isole (§ 03.8 : |r| > 3 arrive dans 31 % des
#: ajustements PARFAITS a 138 residus ; c'est |r| > 4, ou un groupe, qui alerte).
SEUIL_RESIDU = 4.0

#: regle GELEE des points aberrants (§ 03.2) : perte quadratique d'abord ; si
#: s^2 > 2 ET qu'un seul residu depasse |r| = 5, relancer en soft_l1 et RAPPORTER LES
#: DEUX, le point suspect restant dans les donnees et sur la figure.
SEUIL_ABERRANT = 5.0

N_MC_DEFAUT = 300              # bootstrap parametrique (§ 03.5)
N_RETRAIT_DEFAUT = 200         # tirages du critere 4 (§ 03.7 : 200 tirages)
FRACTION_RETRAIT = 0.20        # 20 % des frequences retirees
N_MULTI_DEFAUT = 50            # multi-depart (§ 03.3)
FACTEUR_MULTI = 3.0            # tirage log-uniforme dans [theta0/3 ; 3 theta0]
QMS0_REPLI = 3.0               # repli d'initialisation quand un flanc sort de la bande

#: tolerances d'arret passees a least_squares. Le defaut de SciPy (1e-8) est trop lache
#: ICI pour un usage precis du module : le jackknife et le critere 4 repartent du
#: minimum sur donnees completes, donc la baisse relative de cout attendue est minuscule
#: et l'optimiseur s'arreterait AVANT d'avoir bouge -- ce qui RETRECIRAIT artificiellement
#: la dispersion des sous-echantillons et ferait passer le critere 4 pour de mauvaises
#: raisons. Verifie : avec ftol = 1e-8 les rapports du critere 4 tombent a 0,4, avec
#: 1e-12 ils reviennent autour de 1.
TOLERANCE = 1e-12

#: rapport attendu entre l'ecart-type sous retrait d'une fraction d et u_cov :
#: racine(d/(n-d)) = 0,50 pour d/n = 0,20. Un critere "ecart-type < u_cov" serait
#: satisfait PAR CONSTRUCTION (§ 03.5) : il faut normaliser avant de juger.
RAPPORT_RETRAIT_ATTENDU = np.sqrt(FRACTION_RETRAIT / (1.0 - FRACTION_RETRAIT))


class ErreurAjustement(RuntimeError):
    """L'ajustement n'a pas converge, ou sa covariance n'est pas exploitable."""


class CaisseIncompatible(ValueError):
    """On tente d'ajuster un modele a un seul pic sur une courbe qui en montre deux.

    C'est le garde-fou du § 03.4 (test D) : l'ajustement CONVERGERAIT en silence
    sur des valeurs fausses. Passer forcer=True pour l'exiger quand meme -- ce que fait
    le test de diagnostic D, dont c'est justement le sujet.
    """


def Z_RL(f, R, L):
    """Dipole d'ETALONNAGE : resistance en serie avec une inductance (§ 03.7,
    critere 7). Ce n'est pas un modele de haut-parleur : c'est le "test a blanc" du
    code. Si le code ne retrouve pas une resistance etalon, il ne retrouvera pas un
    haut-parleur."""
    f = np.asarray(f, float)
    return R + 2j * np.pi * f * L


def Z_RC(f, Rs, C):
    """Dipole d'ETALONNAGE : condensateur reel (ESR en serie). Meme role que Z_RL ;
    le condensateur de 150 uF du filtre catalogue est le dipole de reference du
    critere 7, retrouve sur deux decades."""
    f = np.asarray(f, float)
    return Rs + 1.0 / (2j * np.pi * f * C)


#: registre des modeles directs. La cle est le nom court utilise partout dans le
#: projet ('clos', 'semi', 'bassreflex' -- ce sont ceux de modele_hp.Z_depuis_jeu).
MODELES = OrderedDict([
    ('clos', MH.Z_ts),                      # 5 parametres : caisse close (§ 01.9)
    ('semi', MH.Z_semi),                    # 6 : bobine a pertes K(jw)^n (§ 03.6)
    ('bassreflex', MH.Z_bassreflex),        # 7 : alpha fige (hypothese de structure)
    ('bassreflex8', MH.Z_bassreflex8),      # 8 : alpha LIBRE (§ 01.6)
    ('bassreflex_semi', MH.Z_bassreflex_semi),   # 8 : BR + bobine a pertes
    ('deux_pics', MH.Z_deux_pics),          # 8 : repli phenomenologique (§ 03.1)
    ('RL', Z_RL),                           # 2 : etalonnage (critere 7)
    ('RC', Z_RC),                           # 2 : etalonnage (critere 7)
])

#: noms des parametres, dans l'ordre du vecteur theta. Repris de modele_hp pour ne pas
#: les ecrire deux fois (une divergence de nommage serait un bug silencieux).
NOMS_THETA = {
    'clos': MH.NOMS_PARAMETRES['Z_ts'],
    'semi': MH.NOMS_PARAMETRES['Z_semi'],
    'bassreflex': MH.NOMS_PARAMETRES['Z_bassreflex'],
    'bassreflex8': MH.NOMS_PARAMETRES['Z_bassreflex8'],
    'bassreflex_semi': MH.NOMS_PARAMETRES['Z_bassreflex_semi'],
    'deux_pics': MH.NOMS_PARAMETRES['Z_deux_pics'],
    'RL': ('R', 'L'),
    'RC': ('Rs', 'C'),
}

#: nombre de parametres ajustes par modele (derive des noms : une seule source).
N_PARAMETRES = {nom: len(noms) for nom, noms in NOMS_THETA.items()}

#: modeles a UN SEUL pic : les appliquer a une courbe a deux pics est l'erreur que
#: garde_fou_caisse() est charge d'empecher.
MODELES_UN_PIC = ('clos', 'semi', 'RL', 'RC')

#: chaine d'essai de identifier(modele='auto') quand la courbe montre deux pics : le
#: modele PHYSIQUE d'abord (alpha libre, § 01.10), le phenomenologique en dernier
#: recours (il decrit les deux pics sans pretendre nommer f_b ni Q_l).
CHAINE_BASSREFLEX = ('bassreflex8', 'bassreflex', 'deux_pics')

UNITES = {
    'Re': 'ohm', 'Le': 'H', 'Res': 'ohm', 'fs': 'Hz', 'Qms': '-',
    'K': 'ohm.s^n', 'n': '-', 'fb': 'Hz', 'Ql': '-', 'alpha': '-',
    'R1': 'ohm', 'f1': 'Hz', 'Q1': '-', 'R2': 'ohm', 'f2': 'Hz', 'Q2': '-',
    'R': 'ohm', 'L': 'H', 'Rs': 'ohm', 'C': 'F',
}

#: facteur d'affichage (SI -> unite lisible) et son etiquette.
AFFICHAGE = {'Le': (1e3, 'mH'), 'L': (1e3, 'mH'), 'C': (1e6, 'uF')}


def _resoudre_modele(modele):
    """Accepte un nom ('clos'), une fonction (MH.Z_ts) ou None -> (nom, fonction, noms).

    Le modele est un ARGUMENT partout dans ce module (§ 03.1, "generaliser le
    code") : changer de modele ne demande que d'ecrire Z(f, *theta) et de fournir une
    initialisation.
    """
    if modele is None:
        modele = 'clos'
    if isinstance(modele, str):
        nom = modele.strip()
        if nom not in MODELES:
            raise ValueError("modele inconnu : '%s' (connus : %s)"
                             % (nom, ', '.join(MODELES)))
        return nom, MODELES[nom], NOMS_THETA[nom]
    if callable(modele):
        for nom, fonc in MODELES.items():          # reconnu par identite
            if fonc is modele:
                return nom, fonc, NOMS_THETA[nom]
        nom = getattr(modele, '__name__', 'anonyme')
        noms = MH.NOMS_PARAMETRES.get(nom)
        return nom, modele, noms
    raise TypeError('modele : attendu un nom, une fonction ou None')


def _noms(nom_modele, p):
    """Noms des p parametres du modele, ou des etiquettes generiques a defaut."""
    noms = NOMS_THETA.get(nom_modele)
    if noms is None:
        noms = MH.NOMS_PARAMETRES.get(nom_modele)
    if noms is None or len(noms) != p:
        noms = tuple('theta%d' % i for i in range(p))
    return tuple(noms)


def evaluer(modele, f, theta):
    """Z complexe du modele au vecteur theta : evaluer('clos', f, [Re, Le, Res, fs, Qms])."""
    _, fonc, _ = _resoudre_modele(modele)
    return fonc(np.asarray(f, float), *np.asarray(theta, float))


def theta_depuis_jeu(jeu, modele=None):
    """Convertit un dict de parametres (MH.SUB_TYP, IO.SUB_TYPIQUE...) en vecteur theta.

    Le dict porte souvent des cles de documentation ('nom', 'source', 'avertissement') :
    seules les cles du modele sont lues, dans l'ORDRE du vecteur -- c'est tout l'interet
    de passer par NOMS_THETA plutot que par dict.values(), dont l'ordre n'est pas un
    contrat.
    """
    if modele is None:
        modele = jeu.get('modele', 'clos')
        if modele == 'bassreflex' and 'alpha' in jeu:
            modele = 'bassreflex8'
    nom, _, noms = _resoudre_modele(modele)
    manquants = [c for c in noms if c not in jeu]
    if manquants:
        raise ValueError("jeu incomplet pour le modele '%s' : %s"
                         % (nom, ', '.join(manquants)))
    return np.array([float(jeu[c]) for c in noms])


def bornes_modele(nom_modele, p):
    """Bornes passees a least_squares : tout est positif, et l'exposant n est borne.

    Pourquoi borner n dans [0,2 ; 1,0] : n = 1 serait l'inductance pure, n = 1/2
    l'effet de peau idealise ; Leach (2002) mesure 0,6 a 0,7 sur des moteurs reels
    (§ 01.12). Laisser n > 1 donnerait une bobine plus qu'inductive, physiquement
    absurde, et ouvrirait un minimum parasite.
    """
    bas = np.full(p, 1e-12)
    haut = np.full(p, np.inf)
    noms = _noms(nom_modele, p)
    if 'n' in noms:
        i = noms.index('n')
        bas[i], haut[i] = 0.2, 1.0
    return bas, haut


# =====================================================================
# 2. INITIALISATION LUE SUR LA COURBE (§ 03.3)
# =====================================================================

def _bande(f, bande):
    """Masque booleen d'une bande [f1, f2] (None = tout garder)."""
    f = np.asarray(f, float)
    if bande is None:
        return np.ones(f.size, bool)
    return (f >= float(bande[0])) & (f <= float(bande[1]))


def _verifier_unite_phase(phi, bavard=True):
    """Garde-fou : une phase en RADIANS passee pour des degres est indetectable par
    l'ajustement (il converge sur des valeurs fausses). Le modele, lui, sort des
    radians : la conversion est faite ici. Un pic de haut-parleur fait passer la phase
    par +-30 a +-60 degres ; rester sous 3,2 en valeur absolue est donc suspect."""
    if phi is None:
        return
    phi = np.asarray(phi, float)
    if phi.size >= 5 and np.nanmax(np.abs(phi)) < 3.2 and np.nanstd(phi) > 1e-9:
        msg = ("phase comprise entre %+.2f et %+.2f : est-elle en RADIANS ? "
               "ts_fit attend des DEGRES (colonne phase_deg du CSV)."
               % (np.nanmin(phi), np.nanmax(phi)))
        warnings.warn(msg, UserWarning, stacklevel=3)
        if bavard:
            print('  AVERTISSEMENT : ' + msg)


def init_depuis_courbe(f, mod, phi=None, Re0=None, modele='clos', bavard=True):
    """Initialisation LUE SUR LA COURBE, jamais sur une datasheet (§ 03.3).

    Gauss-Newton converge vers le minimum LE PLUS PROCHE du point de depart : le point
    de depart doit donc venir de la courbe mesuree. Recettes, parametre par parametre :

      R_e   : minimum de |Z| en bas de bande (ou la lecture au multimetre, Re0) ;
      f_s   : PASSAGE PAR ZERO DE LA PHASE, interpole, au voisinage du pic. Le sommet
              de |Z| est PLAT : sur une grille au 1/12 d'octave bruitee a 2 % l'argmax
              tombe a un pas de grille (42,4 Hz pour 40 Hz vrais) alors que le zero de
              phase donne 39,79 Hz. Repli sur le pic raffine (MH.pic_principal) si la
              phase manque ou est trop bruitee. Ni l'un ni l'autre ne VAUT f_s : L_e
              les decale en sens OPPOSES ; seul l'ajustement rend f_s ;
      R_es  : Z_max - R_e (hauteur du pic) ;
      Q_ms  : methode de Small (1972), Q = f_s racine(r_0)/(f_2 - f_1) avec
              r_0 = Z_max/R_e et |Z(f_1)| = |Z(f_2)| = racine(R_e Z_max). EXACTE si
              L_e = 0 (et non approchee : en posant u = Q x, la condition donne
              u^2 = 1 + R_es/R_e = r_0) ; +2,4 % sur courbe non bruitee avec
              L_e = 1,2 mH. Suffisant pour demarrer, pas pour conclure ;
      L_e   : partie imaginaire a la frequence la plus HAUTE de la grille, CORRIGEE de
              la queue de la branche motionnelle (qui y est capacitive et compense
              jusqu'a 54 % de jw L_e -- § 03.6), divisee par w.

    GARDE-FOU SUR LA BANDE. La recherche de f_1 et f_2 suppose que les DEUX flancs du
    pic redescendent sous racine(R_e Z_max) a l'interieur de la bande mesuree. Sinon on
    avertit explicitement et on se replie sur Q_ms = 3 (les moindres carres corrigent),
    au lieu de planter sur un IndexError nu. Consigne de phase 1 qui en decoule
    (§ 03.4, test F) : BALAYER AU MOINS UNE OCTAVE SOUS LE PIC ATTENDU.

    modele : 'clos' (5), 'semi' (6), 'bassreflex'/'bassreflex8' (7/8), 'deux_pics' (8),
    'RL'/'RC' (etalonnage). Les modeles a deux pics lisent leurs deux resonances sur la
    courbe (pics et creux), ce qui est la meme idee poussee d'un cran.

    Retourne theta0 (ndarray). La signature (f, mod, phi=None, Re0=None) est GELEE
    (§ 09.4) ; les arguments suivants sont nommes et facultatifs.
    """
    f = np.asarray(f, float)
    mod = np.asarray(mod, float)
    if f.size < 4:
        raise ValueError('init_depuis_courbe : au moins 4 points sont necessaires')
    ordre = np.argsort(f)
    f, mod = f[ordre], mod[ordre]
    phi = None if phi is None else np.asarray(phi, float)[ordre]
    _verifier_unite_phase(phi, bavard=bavard)
    nom, _, _ = _resoudre_modele(modele)

    # --- dipoles d'etalonnage : deux lignes, pas de pic a lire ----------------------
    if nom == 'RL':
        R0 = float(np.min(mod))
        im = _imaginaire(mod, phi)[-1]
        return np.array([R0, max(im / (2 * np.pi * f[-1]), 1e-9)])
    if nom == 'RC':
        Rs0 = max(float(np.min(mod)) * 0.1, 1e-3)
        im = _imaginaire(mod, phi)[0]
        C0 = 1.0 / (2 * np.pi * f[0] * max(-im, 1e-9)) if im < 0 else 1e-4
        return np.array([Rs0, C0])

    k = int(np.argmax(mod))
    Zmax = float(mod[k])
    Re_lu = float(Re0) if Re0 is not None else float(np.min(mod))
    Re_lu = max(Re_lu, 1e-3)

    # --- f_s : zero de phase autour du pic, repli sur le pic raffine -----------------
    fs0 = None
    if phi is not None:
        vois = np.where((f > f[k] / 2) & (f < 2 * f[k]))[0]
        vois = vois[vois < f.size - 1]
        chg = [i for i in vois if phi[i] > 0 >= phi[i + 1]]
        if chg:
            i = chg[0]
            fs0 = float(np.interp(0.0, [phi[i + 1], phi[i]], [f[i + 1], f[i]]))
    if fs0 is None or not np.isfinite(fs0) or fs0 <= 0:
        fs0, _ = MH.pic_principal(f, mod, affiner=True)
    Res0 = max(Zmax - Re_lu, 0.1 * Re_lu)

    # --- Q_ms : largeur de Small, avec le garde-fou de bande -------------------------
    Qms0, replie = _q_de_small(f, mod, k, Re_lu, Zmax, fs0)
    if replie and bavard:
        print("  AVERTISSEMENT : un flanc du pic sort de la bande mesuree "
              "(balayer au moins une octave sous f_s) ; Q_ms initialise a %.1f."
              % QMS0_REPLI)

    # --- L_e : partie imaginaire en haut de bande, corrigee de la queue motionnelle --
    f_haut = float(f[-1])
    im_mes = _imaginaire(mod, phi)[-1]
    im_mot = float(np.imag(MH.Z_ts(f_haut, Re_lu, 0.0, Res0, fs0, Qms0)))
    Le0 = max((im_mes - im_mot) / (2 * np.pi * f_haut), 1e-5)

    if nom == 'clos':
        return np.array([Re_lu, Le0, Res0, fs0, Qms0])
    if nom == 'semi':
        n0 = 0.7                                     # Leach (2002) sur moteurs reels
        K0 = MH.K_semi_depuis_Le(Le0, n0, f_ref=f_haut)
        return np.array([Re_lu, K0, n0, Res0, fs0, Qms0])

    # --- modeles a deux pics : on lit les deux resonances et le creux ----------------
    ext = MH.extrema_locaux(f, mod, lissage=3, bande=BANDE_AIGUILLAGE)
    f_pics, mod_pics = ext['f_pics'], ext['mod_pics']
    if f_pics.size >= 2:
        j = np.argsort(mod_pics)[-2:]                # les deux plus HAUTS maxima
        fL, fH = np.sort(f_pics[j])
        zL = float(mod_pics[j][np.argmin(np.abs(f_pics[j] - fL))])
        zH = float(mod_pics[j][np.argmin(np.abs(f_pics[j] - fH))])
    else:                                            # une seule bosse : on la dedouble
        fL, fH = fs0 / 1.2, fs0 * 1.2
        zL = zH = Zmax
    creux = ext['f_creux']
    entre = creux[(creux > fL) & (creux < fH)]
    fb0 = float(entre[0]) if entre.size else float(np.sqrt(fL * fH))

    if nom == 'deux_pics':
        return np.array([Re_lu, Le0,
                         max(zL - Re_lu, 0.1 * Re_lu), fL, 8.0,
                         max(zH - Re_lu, 0.1 * Re_lu), fH, 8.0])

    # Bass-reflex physique : les relations racines-coefficients du § 01.10
    #   f_L f_H = f_s f_b  et  f_L^2 + f_H^2 = f_s^2 (1 + alpha) + f_b^2
    # donnent f_s et alpha SANS ajustement -- l'initialisation est une lecture.
    fs_br = fL * fH / fb0
    alpha0 = max((fL**2 + fH**2 - fb0**2) / fs_br**2 - 1.0, 0.05)
    Res_br = max(max(zL, zH) - Re_lu, 0.1 * Re_lu)
    Qms_br = max(Qms0, 1.0)
    Ql0 = 7.0                                        # pertes de caisse realistes
    if nom == 'bassreflex':
        return np.array([Re_lu, Le0, Res_br, fs_br, Qms_br, fb0, Ql0])
    if nom == 'bassreflex8':
        return np.array([Re_lu, Le0, Res_br, fs_br, Qms_br, alpha0, fb0, Ql0])
    if nom == 'bassreflex_semi':
        n0 = 0.7
        K0 = MH.K_semi_depuis_Le(Le0, n0, f_ref=f_haut)
        return np.array([Re_lu, K0, n0, Res_br, fs_br, Qms_br, fb0, Ql0])
    raise ValueError("pas d'initialisation ecrite pour le modele '%s'" % nom)


def _imaginaire(mod, phi):
    """Partie imaginaire de Z a partir du module et de la phase EN DEGRES.

    Si la phase manque (export module seul), on la reconstruit en supposant la partie
    reelle egale au minimum de |Z| -- approximation grossiere qui ne sert QU'A
    INITIALISER L_e, jamais a ajuster.
    """
    mod = np.asarray(mod, float)
    if phi is not None:
        return mod * np.sin(np.radians(np.asarray(phi, float)))
    reel = float(np.min(mod))
    return np.sqrt(np.maximum(mod**2 - reel**2, 0.0))


def _q_de_small(f, mod, k, Re_lu, Zmax, fs0):
    """Q_ms par la largeur de Small : retourne (Q_ms0, repli_declenche).

    Seuil |Z| = racine(R_e Z_max) : c'est la definition de Small (1972), dont decoule
    la formule Q_ms = f_s racine(r_0)/(f_2 - f_1). Elle demande que les DEUX flancs
    redescendent sous le seuil DANS la bande mesuree.
    """
    seuil = np.sqrt(Re_lu * Zmax)
    g = np.where(mod[:k] < seuil)[0]
    d = np.where(mod[k:] < seuil)[0]
    if g.size and d.size:
        i1, i2 = int(g[-1]), int(k + d[0])
        f1 = np.interp(seuil, [mod[i1], mod[i1 + 1]], [f[i1], f[i1 + 1]])
        f2 = np.interp(seuil, [mod[i2], mod[i2 - 1]], [f[i2], f[i2 - 1]])
        if f2 > f1:
            return float(fs0 * np.sqrt(Zmax / Re_lu) / (f2 - f1)), False
    return QMS0_REPLI, True


def largeur_de_small(fs, Qms, Re, Res):
    """Largeur f_2 - f_1 = f_s racine(r_0)/Q_ms du pic, avec r_0 = 1 + R_es/R_e.

    Sert a DIMENSIONNER LA GRILLE DE MESURE (§ 03.4, test E) : a Q_ms = 8, valeur
    plausible pour un 18 pouces, la largeur tombe a une quinzaine de hertz, soit six
    points au 1/12 d'octave -- d'ou le resserrement au 1/24 autour du pic, qui fait
    passer l'erreur d'identification de 2,6 % a 0,9 % pour dix minutes de banc.
    """
    r0 = 1.0 + float(Res) / float(Re)
    return float(fs) * np.sqrt(r0) / float(Qms)


# =====================================================================
# 3. RESIDUS PONDERES (§ 03.2)
# =====================================================================

def residus_ts(theta, f, mod, phi, u_mod, u_phi, modele=None):
    """Vecteur des residus NORMALISES, module puis phase (signature gelee § 09.4).

    Convention de signe : r = (modele - mesure)/u. Le signe est sans effet sur S ni sur
    Cov, mais il fixe celui de la jacobienne, donc celui de la formule de covariance du
    § 03.5 -- il faut donc l'ecrire une fois pour toutes.

        r_k       = [ln|Z(f_k ; theta)| - ln|Z_k|] / (u(|Z_k|)/|Z_k|)     k <= N
        r_{N+k}   = [arg Z(f_k ; theta) - phi_k] / u(phi_k)     (degres/degres)

    POURQUOI PONDERER. Avec un bruit RELATIF de 2 %, un point du pic (ecart typique
    50 x 0,02 = 1 ohm) contribuerait a S environ (50/7)^2 = 50 fois plus qu'un point du
    plancher (7 x 0,02 = 0,14 ohm) : le pic ecraserait tout, alors que les deux points
    sont mesures avec la MEME precision relative. Normalises, chaque point compte selon
    sa precision reelle, un point bien ajuste contribue r^2 = 1, et si les u sont
    realistes S_min = 2N - p : c'est le test du chi2 reduit.

    POURQUOI LE LOG DU MODULE. ln|Z| rend le residu de module homogene a un ECART
    RELATIF, ce qui est exactement ce que la chaine de mesure produit (u(|Z|) est
    proportionnelle a |Z|, § 02.7) ; la division par u/|Z| est alors une division
    par une incertitude relative, sans unite.

    HYPOTHESE D'INDEPENDANCE, a enoncer : la matrice de poids est DIAGONALE. Module et
    phase sortent pourtant des MEMES deux tensions ; on garde la diagonale, et si
    l'etalonnage de la phase 1 revele une correlation module/phase, on passera a une
    matrice de poids pleine. Les erreurs SYSTEMATIQUES, elles, ne relevent pas du tout
    de cette matrice : voir budget_systematique().

    phi=None est accepte : les residus se reduisent alors au module (cas d'un export
    sans phase). u_mod est en ohm, u_phi en DEGRES.
    """
    _, fonc, _ = _resoudre_modele(modele)
    f = np.asarray(f, float)
    mod = np.asarray(mod, float)
    u_mod = np.asarray(u_mod, float)
    Z = fonc(f, *np.asarray(theta, float))
    r_mod = np.log(np.abs(Z) / mod) * (mod / u_mod)
    if phi is None:
        return r_mod
    r_phi = (np.degrees(np.angle(Z)) - np.asarray(phi, float)) / np.asarray(u_phi, float)
    return np.concatenate([r_mod, r_phi])


def ecarts_relatifs(theta, f, mod, phi, modele=None, bande=None):
    """Ecarts BRUTS modele-mesure : (RMS relatif sur |Z| en %, RMS sur la phase en deg).

    C'est le critere 2 du § 03.7, et il se lit sans dictionnaire : "le modele passe
    a 2 % du module et a 1 degre de la phase". A calculer sur la bande de la PORTE DE
    VALIDATION (20-300 Hz), a ne pas confondre avec la bande d'ajustement (10-500 Hz).
    """
    f = np.asarray(f, float)
    m = _bande(f, bande)
    Z = evaluer(modele, f[m], theta)
    rms_mod = 100.0 * float(np.sqrt(np.mean((np.abs(Z) / np.asarray(mod, float)[m] - 1.0)**2)))
    if phi is None:
        return rms_mod, float('nan')
    d = np.degrees(np.angle(Z)) - np.asarray(phi, float)[m]
    return rms_mod, float(np.sqrt(np.mean(d**2)))


# =====================================================================
# 4. GARDE-FOU CAISSE : le coeur du module (§ 03.4, test D)
# =====================================================================

def garde_fou_caisse(f, mod, modele='clos', bande=BANDE_AIGUILLAGE,
                     proeminence_min=0.05, bavard=True, strict=False):
    """Compte les pics de |Z| AVANT d'ajuster, et crie si le modele est inadapte.

    POURQUOI CETTE FONCTION EXISTE. Applique a une courbe a deux pics (bass-reflex), le
    modele a 5 parametres CONVERGE sans lever la moindre erreur et rend des nombres
    d'allure parfaitement plausible -- sur le jeu synthetique du § 03.4 :
    R_e = 6,17 +- 0,20 ohm, f_s = 39,0 +- 0,7 Hz, Q_ms = 2,11 +- 0,22 -- qui ne veulent
    rien dire. Seuls le chi2 reduit (s^2 = 93) et la structure des residus le
    trahissent, APRES COUP. Un modele inadapte ne se signale donc pas par une exception :
    il faut le detecter AVANT, en comptant les pics. C'est le critere 0 du § 03.7.

    DEUX AVIS INDEPENDANTS, et c'est voulu :
      * io_mesures.diagnostiquer_caisse : maxima locaux filtres par PROEMINENCE
        relative (>= 5 %), ce qui distingue un vrai second pic d'une dentelure de bruit ;
      * modele_hp.compter_pics : maxima locaux sur la courbe LISSEE par moyenne
        glissante sur 3 points (la formulation litterale du § 03.7).
    Le critere d'alerte est le MAXIMUM des deux comptages : en cas de doute, on avertit.
    Sur le jeu synthetique bass-reflex, le comptage lisse rend 3 (dont un parasite) --
    d'ou un critere ">= 2" et non "exactement 2".

    Retour : dict(n_pics, n_pics_lisses, f_pics, z_pics, f_creux, modele_conseille,
                  n_parametres_conseilles, compatible, message, avertissements).
    strict=True leve CaisseIncompatible au lieu de se contenter d'avertir.
    """
    f = np.asarray(f, float)
    mod = np.asarray(mod, float)
    m = _bande(f, bande)
    if m.sum() < 5:
        m = np.ones(f.size, bool)                    # bande trop etroite : tout garder
    diag = IO.diagnostiquer_caisse(f[m], mod[m], proeminence_min=proeminence_min)
    n_lisse = MH.compter_pics(f, mod, lissage=3, bande=bande)
    n = max(int(diag['n_pics']), int(n_lisse))

    if n >= 2:
        conseille, p_conseille = 'bassreflex8', 8
    elif n == 1:
        conseille, p_conseille = 'clos', 5
    else:
        conseille, p_conseille = 'indetermine', 0

    nom = _resoudre_modele(modele)[0] if modele is not None else None
    compatible = True
    message = ''
    if nom is not None and nom in MODELES_UN_PIC and n >= 2:
        compatible = False
        message = (
            "GARDE-FOU CAISSE -- %d maxima de |Z| entre %g et %g Hz (proeminence : %d ; "
            "lissage 3 points : %d), pics a %s Hz, creux a %s Hz. La caisse se comporte "
            "en BASS-REFLEX : le modele '%s' a %d parametres est INADAPTE. Il "
            "CONVERGERA quand meme, en silence, sur des valeurs fausses (§ 03.4, "
            "test D : s^2 = 93, residus structures, z = -5,4). Utiliser '%s' "
            "(%d parametres) -- ou passer forcer=True en connaissance de cause."
            % (n, bande[0], bande[1], diag['n_pics'], n_lisse,
               ', '.join('%.1f' % x for x in diag['f_pics']) or '?',
               ', '.join('%.1f' % x for x in diag['f_creux']) or '?',
               nom, N_PARAMETRES.get(nom, 0), conseille, p_conseille))
    elif nom is not None and nom not in MODELES_UN_PIC and n <= 1:
        compatible = False
        message = (
            "GARDE-FOU CAISSE -- un seul maximum de |Z| entre %g et %g Hz : la caisse "
            "se comporte en CLOS. Ajuster '%s' y ajouterait des parametres NON "
            "IDENTIFIABLES (f_b et Q_l n'ont aucun pic pour les contraindre) : "
            "covariance explosive, minima parasites. Utiliser 'clos' (5 parametres)."
            % (bande[0], bande[1], nom))
    elif n == 0:
        message = ("aucun pic detecte entre %g et %g Hz : bande trop etroite, grille "
                   "trop lache, ou dipole non resonant -- verifier la mesure "
                   "(§ 02.6) avant d'ajuster quoi que ce soit."
                   % (bande[0], bande[1]))

    resultat = dict(n_pics=n, n_pics_proeminence=int(diag['n_pics']),
                    n_pics_lisses=int(n_lisse),
                    f_pics=[float(x) for x in diag['f_pics']],
                    z_pics=[float(x) for x in diag['z_pics']],
                    f_creux=[float(x) for x in diag['f_creux']],
                    type_caisse='bass-reflex' if n >= 2 else ('clos' if n == 1 else 'indetermine'),
                    modele_conseille=conseille, n_parametres_conseilles=p_conseille,
                    compatible=bool(compatible), message=message,
                    avertissements=list(diag['avertissements']))
    if message:
        warnings.warn(message, UserWarning, stacklevel=2)
        if bavard:
            print('  ' + '!' * 78)
            for ligne in _replier(message, 76):
                print('  ! ' + ligne)
            print('  ' + '!' * 78)
        if strict and not compatible:
            raise CaisseIncompatible(message)
    elif bavard:
        print("  diagnostic caisse : %d pic(s) entre %g et %g Hz -> caisse %s, modele "
              "conseille '%s' (%d parametres)."
              % (n, bande[0], bande[1], resultat['type_caisse'], conseille, p_conseille))
    return resultat


def _replier(texte, largeur):
    """Repli d'un message long en lignes de <= largeur caracteres (sans dependance)."""
    mots, lignes, courante = texte.split(), [], ''
    for mot in mots:
        if courante and len(courante) + 1 + len(mot) > largeur:
            lignes.append(courante)
            courante = mot
        else:
            courante = (courante + ' ' + mot).strip()
    if courante:
        lignes.append(courante)
    return lignes


# =====================================================================
# 5. MOTEURS D'AJUSTEMENT : scipy, et le repli numpy pur
# =====================================================================

class Moteur(str):
    """Nom du moteur d'ajustement ('scipy' ou 'repli'), enrichi de ses sous-produits.

    C'est une chaine de caracteres -- donc `moteur == 'scipy'` fonctionne -- qui porte
    en plus les attributs dont on a besoin apres coup : .jac (la jacobienne au point
    final, necessaire a la covariance), .residus, .cout, .s2, .n_residus, .p, .cond,
    .alerte, .messages, .statut, .loss, .modele, .theta0, .n_eval.
    """

    def __new__(cls, nom, **attributs):
        obj = str.__new__(cls, nom)
        for cle, valeur in attributs.items():
            setattr(obj, cle, valeur)
        return obj


def moindres_carres_lm(residus, theta0, args=(), n_iter=80, lam=1e-3):
    """Levenberg-Marquardt maison (REPLI sans SciPy) -- signature gelee § 09.5.

    C'est EXACTEMENT l'algorithme du § 03.2, ecrit a la main : on linearise le
    modele autour de l'estimation courante, r(theta + d) = r(theta) + J d, on resout le
    systeme normal AMORTI (J^T J + lam diag(J^T J)) d = -J^T r, on avance si le cout
    baisse (et on divise lam par 10), sinon on augmente lam et on reessaie. Gauss-Newton
    est la methode de Newton appliquee a grad S = 0, avec la hessienne approchee par
    2 J^T J ; l'amortissement de Levenberg-Marquardt la rend robuste LOIN de la solution.

    Retourne (theta, J). La jacobienne est rendue parce que ajuster_ts() doit livrer une
    covariance DANS LES DEUX BRANCHES : sans cela la signature gelee promettrait une
    covariance que le repli ne rendrait pas, et le critere "< 3 sigma" des tests serait
    intestable sur un poste sans SciPy -- pour une raison d'interface, pas de physique.

    Les parametres sont contraints positifs (tous le sont dans nos modeles).
    """
    th = np.asarray(theta0, float).copy()
    J = None
    def S(t):
        return float(np.sum(residus(t, *args)**2))
    s = S(th)
    for _ in range(n_iter):
        r = residus(th, *args)
        J = np.empty((r.size, th.size))
        for j in range(th.size):                     # jacobienne numerique, pas relatif
            d = 1e-6 * max(abs(th[j]), 1e-12)
            tp = th.copy()
            tp[j] += d
            J[:, j] = (residus(tp, *args) - r) / d
        A, g = J.T @ J, J.T @ r
        for _ in range(40):                          # recherche du pas amorti
            try:
                pas = np.linalg.solve(A + lam * np.diag(np.diag(A)), -g)
            except np.linalg.LinAlgError:
                lam *= 10.0
                continue
            if np.all(th + pas > 0) and S(th + pas) < s:
                th, s, lam = th + pas, S(th + pas), max(lam / 10.0, 1e-12)
                break
            lam *= 10.0
        else:
            break
    return th, J


def ajuster_ts(f, mod, phi, u_mod, u_phi, theta0, forcer_repli=False, modele='clos',
               loss='linear', avec_s2=False, verifier_caisse=True, bavard=True,
               bornes=None, n_iter=80, tol=TOLERANCE):
    """Ajustement par moindres carres non lineaires ponderes -> (theta, cov, s2, moteur).

    Signature GELEE (§ 09.4) sur les sept premiers arguments ; les suivants sont
    nommes et facultatifs. forcer_repli=True impose le Levenberg-Marquardt maison meme
    si SciPy est present -- c'est ce que fait le test G, qui compare les deux.

    Retour :
      theta  : vecteur ajuste (ndarray, SI) ;
      cov    : matrice de covariance (p, p). CONVENTION GELEE (§ 03.5) : (J^T J)^-1
               SANS le facteur s^2, parce qu'apres l'etalonnage de la phase 1 les u sont
               CONNUS. Multiplier par s^2 blanchirait un defaut de modele en incertitude
               (s^2 = 5 multiplierait toutes les barres par 2,2 et ferait disparaitre le
               symptome). avec_s2=True rend l'autre convention, pour comparaison ;
      s2     : chi2 reduit S_min/(2N - p) -- un DIAGNOSTIC (critere 1), pas un correctif ;
      moteur : Moteur('scipy'|'repli') portant .jac, .residus, .cond, .alerte...

    ALERTES EMISES (elles sont le service rendu, pas du bruit) :
      * garde-fou caisse (voir garde_fou_caisse) si le modele est a un pic et la courbe
        a deux ;
      * parametre en butee (active_mask) ou jacobienne mal conditionnee (cond > 1e6) :
        la covariance n'est alors PAS exploitable. Cas concret du test a blanc : sur une
        resistance etalon de 100 ohm, l'inductance des cordons (1 uH = 0,0018 degre a
        500 Hz) n'est pas identifiable -- on lit R, on IGNORE u(L) ;
      * loss != 'linear' : le cout est transforme, s^2 n'est plus un chi2 et ne sert
        que de comparaison relative (§ 03.2, regle des points aberrants).
    """
    nom, fonc, _ = _resoudre_modele(modele)
    f = np.asarray(f, float)
    mod = np.asarray(mod, float)
    u_mod = np.asarray(u_mod, float)
    theta0 = np.asarray(theta0, float).copy()
    if phi is not None:
        phi = np.asarray(phi, float)
        u_phi = np.asarray(u_phi, float) * np.ones_like(phi)
    if np.any(mod <= 0) or np.any(u_mod <= 0):
        raise ValueError('ajuster_ts : |Z| et u(|Z|) doivent etre strictement positifs')

    messages = []
    alerte_caisse = None
    if verifier_caisse and nom in ('clos', 'semi', 'bassreflex', 'bassreflex8',
                                  'bassreflex_semi', 'deux_pics'):
        alerte_caisse = garde_fou_caisse(f, mod, modele=nom, bavard=bavard)
        if not alerte_caisse['compatible']:
            messages.append(alerte_caisse['message'])
    _verifier_unite_phase(phi, bavard=bavard)

    args = (f, mod, phi, u_mod, u_phi, nom)
    p = theta0.size
    n_res = f.size * (1 if phi is None else 2)
    if n_res <= p:
        raise ErreurAjustement('%d residus pour %d parametres : sous-determine'
                               % (n_res, p))
    bas, haut = bornes_modele(nom, p) if bornes is None else bornes
    theta0 = np.clip(theta0, bas * 1.000001, np.where(np.isfinite(haut), haut * 0.999999, np.inf))

    if SCIPY and not forcer_repli:
        echelle = np.where(np.abs(theta0) > 0, np.abs(theta0), 1.0)
        sol = least_squares(residus_ts, theta0, args=args, bounds=(bas, haut),
                            x_scale=echelle, method='trf', loss=loss,
                            ftol=tol, xtol=tol, gtol=tol)
        theta, J, r = sol.x, sol.jac, sol.fun
        cout = float(np.sum(r**2))
        statut, message_moteur = int(sol.status), str(sol.message)
        n_eval = int(sol.nfev)
        en_butee = bool(np.any(sol.active_mask != 0))
        moteur_nom = 'scipy'
    else:
        theta, J = moindres_carres_lm(residus_ts, theta0, args=args, n_iter=n_iter)
        r = residus_ts(theta, *args)
        cout = float(np.sum(r**2))
        statut, message_moteur, n_eval = 0, 'Levenberg-Marquardt maison (repli)', n_iter
        en_butee = bool(np.any(theta <= bas * 1.0001))
        moteur_nom = 'repli'

    s2 = cout / (n_res - p)
    cond = float(np.linalg.cond(J * theta))          # colonnes mises a l'echelle de theta
    alerte = en_butee or cond > 1e6
    if alerte:
        msg = ("parametre en butee ou jacobienne mal conditionnee (cond = %.1e) "
               "-> covariance NON exploitable." % cond)
        messages.append(msg)
        if bavard:
            print('  ALERTE : ' + msg)
    if loss != 'linear':
        messages.append("loss = '%s' : le cout est transforme, s^2 n'est plus un chi2 "
                        "et ne vaut que comme comparaison relative." % loss)

    try:
        cov = np.linalg.inv(J.T @ J)
    except np.linalg.LinAlgError:
        cov = np.linalg.pinv(J.T @ J)
        messages.append('J^T J singuliere : covariance par pseudo-inverse (a ne pas publier)')
    if avec_s2:
        cov = s2 * cov

    moteur = Moteur(moteur_nom, jac=J, residus=r, cout=cout, s2=s2, n_residus=n_res,
                    p=p, cond=cond, alerte=bool(alerte), messages=messages,
                    statut=statut, message=message_moteur, loss=loss, modele=nom,
                    theta0=theta0, n_eval=n_eval, caisse=alerte_caisse,
                    avec_s2=bool(avec_s2))
    return theta, cov, s2, moteur


def ajuster(modele, theta0, f, mod, phi, u_mod, u_phi, **kw):
    """Meme ajustement, MODELE EN PREMIER : ajuster(MH.Z_ts, theta0, f, ...).

    C'est l'ordre d'appel du § 03.4 ("le modele est passe en argument aux fonctions
    d'ajustement") : changer de modele ne demande que d'ecrire Z(f, *theta) et de fournir
    une initialisation. Les deux ordres existent parce que ajuster_ts a une signature
    GELEE dont le premier argument est la frequence.
    """
    return ajuster_ts(f, mod, phi, u_mod, u_phi, theta0, modele=modele, **kw)


def multi_depart(f, mod, phi, u_mod, u_phi, theta0, n=N_MULTI_DEFAUT,
                 facteur=FACTEUR_MULTI, graine=0, modele='clos', bavard=False, **kw):
    """Multi-depart : n ajustements depuis des points de depart tires au hasard.

    POURQUOI (§ 03.3). L'initialisation lue sur la courbe est bonne, mais ce n'est
    pas une PREUVE d'unicite du minimum. Le test honnete consiste a repartir de points
    volontairement mauvais sur LES MEMES donnees. Des minima parasites existent bel et
    bien (L_e -> 0, Q_ms tres grand) ; la parade est double : initialiser sur la courbe,
    et garder le cout le plus bas sur une cinquantaine de tirages. Le minimum parasite
    se reconnait instantanement a son cout : chi2 reduit de l'ordre de 1e3 contre 1,1.

    Retourne dict(theta, cov, s2, moteur, fraction, couts, n_reussis) ou 'fraction' est
    la part des departs qui retrouvent le meilleur cout a 0,1 % pres.
    """
    rng = np.random.default_rng(graine)
    theta0 = np.asarray(theta0, float)
    meilleur, couts = None, []
    for i in range(int(n)):
        if i == 0:
            depart = theta0
        else:
            depart = theta0 * np.exp(rng.uniform(-np.log(facteur), np.log(facteur),
                                                 theta0.size))
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                sol = ajuster_ts(f, mod, phi, u_mod, u_phi, depart, modele=modele,
                                 verifier_caisse=False, bavard=False, **kw)
        except Exception:
            continue
        couts.append(sol[3].cout)
        if meilleur is None or sol[3].cout < meilleur[3].cout:
            meilleur = sol
    if meilleur is None:
        raise ErreurAjustement('multi_depart : aucun ajustement n a converge')
    couts = np.array(couts, float)
    fraction = float(np.mean(couts < meilleur[3].cout * 1.001))
    if bavard:
        print('  multi-depart : %d/%d departs convergent, %.0f %% retrouvent le minimum '
              'global ; cout median des parasites %.3g'
              % (couts.size, n, 100 * fraction,
                 float(np.median(couts[couts >= meilleur[3].cout * 1.001]))
                 if np.any(couts >= meilleur[3].cout * 1.001) else float('nan')))
    return dict(theta=meilleur[0], cov=meilleur[1], s2=meilleur[2], moteur=meilleur[3],
                fraction=fraction, couts=couts, n_reussis=int(couts.size))


# =====================================================================
# 6. INCERTITUDES : covariance, Monte-Carlo, jackknife, retrait, type B
# =====================================================================

def u_covariance(cov):
    """u(theta_j) = racine(Cov_jj). La covariance COMPLETE, elle, doit etre propagee
    telle quelle a l'acte 3 : cinq u independants perdraient rho(R_es, Q_ms) = 0,83."""
    return np.sqrt(np.abs(np.diag(np.asarray(cov, float))))


def correlation(cov):
    """Matrice de correlation rho_ij = Cov_ij/(u_i u_j).

    A AFFICHER SYSTEMATIQUEMENT a cote des u (§ 03.5). La correlation dominante
    attendue est rho(R_es, Q_ms) = 0,83 : les points des FLANCS du pic verifient
    |Z_mot| = R_es/racine(1 + Q^2 x^2), donc un pic un peu plus haut ET un peu plus
    etroit passe par les memes points de flanc ; seul le sommet, plat, les departage.
    Consequence : une incertitude sur Q_ms seul sous-estime ce que l'on sait du COUPLE.
    """
    cov = np.asarray(cov, float)
    u = u_covariance(cov)
    denom = np.outer(u, u)
    with np.errstate(divide='ignore', invalid='ignore'):
        rho = np.where(denom > 0, cov / denom, 0.0)
    return rho


def monte_carlo(theta, f, u_mod, u_phi, n=N_MC_DEFAUT, graine=0, modele='clos',
                reinitialiser=True, bavard=False):
    """Bootstrap parametrique : on rejoue n fois le bruit de la chaine et on reajuste.

    On part du modele AJUSTE, on lui ajoute le bruit postule (u_mod en ohm sur le module,
    u_phi en degres sur la phase), on RE-INITIALISE depuis la courbe bruitee (ce qui
    teste au passage la robustesse de init_depuis_courbe) et on reajuste. L'ecart-type
    des n solutions est u_MC.

    CE QUE CELA PROUVE, ET CE QUE CELA NE PROUVE PAS (§ 03.5) : le Monte-Carlo
    REJOUE le bruit avec les u postules, il ne peut donc rien dire de leur realisme. Il
    reproduit (J^T J)^-1 a quelques pour-cent pres : son accord avec la covariance valide
    LA LINEARISATION, rien d'autre. Le realisme des u se juge par s^2, par le jackknife
    (seul a n'utiliser que la dispersion reellement observee) et par la couverture.

    Retourne dict(u, tirages, moyenne, biais, n_reussis).
    """
    rng = np.random.default_rng(graine)
    theta = np.asarray(theta, float)
    f = np.asarray(f, float)
    u_mod = np.asarray(u_mod, float) * np.ones_like(f)
    avec_phase = u_phi is not None
    if avec_phase:
        u_phi = np.asarray(u_phi, float) * np.ones_like(f)
    Z = evaluer(modele, f, theta)
    mod0, phi0 = np.abs(Z), np.degrees(np.angle(Z))
    tirages = []
    for _ in range(int(n)):
        mod = mod0 + u_mod * rng.standard_normal(f.size)
        phi = (phi0 + u_phi * rng.standard_normal(f.size)) if avec_phase else None
        if np.any(mod <= 0):
            continue
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                depart = (init_depuis_courbe(f, mod, phi, modele=modele, bavard=False)
                          if reinitialiser else theta)
                sol = ajuster_ts(f, mod, phi, u_mod, u_phi, depart, modele=modele,
                                 verifier_caisse=False, bavard=False)
        except Exception:
            continue
        tirages.append(sol[0])
    if len(tirages) < 3:
        raise ErreurAjustement('monte_carlo : moins de 3 tirages exploitables')
    T = np.array(tirages)
    if bavard:
        print('  Monte-Carlo : %d/%d tirages exploitables' % (T.shape[0], n))
    return dict(u=T.std(axis=0, ddof=1), tirages=T, moyenne=T.mean(axis=0),
                biais=T.mean(axis=0) - theta, n_reussis=int(T.shape[0]))


def jackknife(theta, f, mod, phi, u_mod, u_phi, modele='clos', n_max=None):
    """Jackknife : N ajustements, en retirant a chaque fois UNE FREQUENCE.

    Retirer une frequence, c'est retirer SES DEUX residus (module et phase) -- pas un
    residu sur deux. u_jack^2 = (N-1)/N somme_i (theta_(i) - theta_moyen)^2.

    Il est le seul des trois estimateurs a ne rien supposer sur le bruit : il mesure ce
    que CES donnees, avec LEUR dispersion reelle, laissent comme liberte aux parametres.
    C'est donc lui qui juge le realisme des u postules (avec s^2), pas le Monte-Carlo.
    """
    f = np.asarray(f, float)
    mod = np.asarray(mod, float)
    u_mod = np.asarray(u_mod, float) * np.ones_like(f)
    if phi is not None:
        phi = np.asarray(phi, float)
        u_phi = np.asarray(u_phi, float) * np.ones_like(f)
    N = f.size
    indices = range(N) if n_max is None or n_max >= N else np.linspace(0, N - 1, int(n_max)).astype(int)
    ths = []
    for i in indices:
        m = np.ones(N, bool)
        m[i] = False
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                sol = ajuster_ts(f[m], mod[m], None if phi is None else phi[m],
                                 u_mod[m], None if phi is None else u_phi[m],
                                 theta, modele=modele, verifier_caisse=False, bavard=False)
        except Exception:
            continue
        ths.append(sol[0])
    if len(ths) < 3:
        raise ErreurAjustement('jackknife : moins de 3 ajustements exploitables')
    T = np.array(ths)
    n = T.shape[0]
    u = np.sqrt((n - 1) / n * np.sum((T - T.mean(axis=0))**2, axis=0))
    return dict(u=u, tirages=T, n_reussis=int(n))


def stabilite_retrait(theta, f, mod, phi, u_mod, u_phi, modele='clos',
                      n=N_RETRAIT_DEFAUT, fraction=FRACTION_RETRAIT, graine=0):
    """Critere 4 : n tirages retirant au hasard une fraction des frequences.

    CE TEST NE MESURE PAS CE QU'ON CROIT, et il faut l'ecrire noir sur blanc. Pour un
    sous-echantillonnage sans remise de fraction d/n, l'ecart-type des estimations vaut
    asymptotiquement u racine(d/(n-d)) = 0,50 u pour d/n = 0,20. Un critere
    "ecart-type < u_cov" est donc satisfait PAR CONSTRUCTION -- et il l'est meme sur des
    donnees ou le modele est demontrablement faux (test C, semi-inductance, s^2 = 5,4).
    Ce test mesure le CONDITIONNEMENT, pas l'adequation ; il n'est informatif que
    NORMALISE par 0,50 u_cov (on attend 1). L'adequation, c'est s^2 et la structure des
    residus.

    DEUX PRECISIONS AJOUTEES APRES VERIFICATION NUMERIQUE, et elles comptent :
    (i) le facteur 0,50 est bien le bon pour CE plan d'experience, malgre des leviers
    tres inegaux (0,036 en moyenne, 0,134 au maximum) : la formule exacte du modele
    lineaire, moyennee sur les sous-ensembles, donne 1,00 a 1,07 fois 0,50 u_cov ;
    (ii) l'ecart-type observe se compare a 0,50 u_cov racine(s^2) et non a 0,50 u_cov,
    parce qu'il mesure la dispersion REELLEMENT observee -- c'est la convention avec
    laquelle la fourchette [0,7 ; 1,4] du § 03.7 a ete etablie (son u_cov portait
    encore le facteur s^2, gele plus tard). Le rapport brut est rapporte aussi.
    ENFIN, ce rapport est une VARIABLE ALEATOIRE : sur cinq realisations de bruit du jeu
    synthetique il va de 0,6 a 1,6 selon le parametre. Un seul depassement sur une seule
    realisation ne condamne rien -- il designe le parametre a surveiller.

    Retourne dict(ecart_type, moyenne, decalage, tirages, n_reussis, attendu_relatif).
    """
    rng = np.random.default_rng(graine)
    f = np.asarray(f, float)
    mod = np.asarray(mod, float)
    u_mod = np.asarray(u_mod, float) * np.ones_like(f)
    if phi is not None:
        phi = np.asarray(phi, float)
        u_phi = np.asarray(u_phi, float) * np.ones_like(f)
    N = f.size
    d = max(1, int(round(fraction * N)))
    ths = []
    for _ in range(int(n)):
        m = np.ones(N, bool)
        m[rng.choice(N, size=d, replace=False)] = False
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                sol = ajuster_ts(f[m], mod[m], None if phi is None else phi[m],
                                 u_mod[m], None if phi is None else u_phi[m],
                                 theta, modele=modele, verifier_caisse=False, bavard=False)
        except Exception:
            continue
        ths.append(sol[0])
    if len(ths) < 3:
        raise ErreurAjustement('stabilite_retrait : moins de 3 tirages exploitables')
    T = np.array(ths)
    return dict(ecart_type=T.std(axis=0, ddof=1), moyenne=T.mean(axis=0),
                decalage=T.mean(axis=0) - np.asarray(theta, float),
                tirages=T, n_reussis=int(T.shape[0]),
                attendu_relatif=RAPPORT_RETRAIT_ATTENDU)


def budget_systematique(theta, u_A, modele='clos', u_rel_R_ref=0.01,
                        u_B_relatives_sup=None):
    """Type A + type B sur les parametres T-S, via incertitudes.budget_parametres_ts.

    LA COMPOSANTE QUE LES TROIS ESTIMATEURS NE VOIENT PAS (§ 03.5). Covariance,
    Monte-Carlo et jackknife mesurent tous les trois la meme chose : l'ALEATOIRE. Or
    Z = R_ref V_HP/V_Rref : une erreur de +1 % sur R_ref multiplie TOUTES les |Z| par
    1,01, de facon parfaitement correlee d'un point a l'autre. Verifie numeriquement
    (voir biais_Rref) : R_e, R_es et L_e se decalent du MEME pourcentage, f_s et Q_ms ne
    bougent pas -- ce sont une POSITION et une FORME, pas un niveau -- et le chi2 ne
    bronche pas. Avec une resistance ordinaire a 3 %, le biais sur R_e vaut pres de
    7 u_cov : l'incertitude dominante ne serait pas celle qu'on affiche.

    u_B_relatives_sup : autres systematiques par parametre, par exemple la derive
    thermique de la bobine sur R_e (le cuivre gagne 0,393 %/K, soit 2 % pour 5 K),
    obtenue en relevant R_e au multimetre AVANT et APRES le balayage.

    Ne s'applique qu'au modele a 5 parametres ('clos'), seul contrat de
    incertitudes.NOMS_TS. Retourne (budget, texte) ; (None, message) sinon.
    """
    nom, _, noms = _resoudre_modele(modele)
    if nom != 'clos':
        return None, ("budget systematique non ecrit pour le modele '%s' : la table de "
                      "sensibilite a R_ref de incertitudes.py porte sur les cinq "
                      "parametres T-S. Les parametres de NIVEAU (ohms) heritent de "
                      "u(R_ref), les POSITIONS et les FORMES en sont immunisees." % nom)
    budget = INC.budget_parametres_ts(dict(zip(noms, np.asarray(theta, float))),
                                      dict(zip(noms, np.asarray(u_A, float))),
                                      u_rel_R_ref=u_rel_R_ref,
                                      u_B_relatives_sup=u_B_relatives_sup)
    return budget, INC.tableau_budget_ts(budget)


def grandeurs_derivees(tirages, modele='clos'):
    """Q_es et Q_ts avec leur incertitude, calcules SUR CHAQUE TIRAGE Monte-Carlo.

    Pourquoi pas une propagation a la main : les parametres sont CORRELES
    (rho(R_es, Q_ms) = 0,83), donc additionner des incertitudes relatives serait faux.
    On calcule la grandeur derivee sur chaque tirage et on prend l'ecart-type des
    resultats -- c'est la seule facon simple de respecter la covariance complete.
    """
    nom, _, noms = _resoudre_modele(modele)
    T = np.atleast_2d(np.asarray(tirages, float))
    if nom not in ('clos', 'semi'):
        return {}
    iRe, iRes, iQms = noms.index('Re'), noms.index('Res'), noms.index('Qms')
    Qes, Qts = MH.facteurs_qualite(T[:, iRe], T[:, iRes], T[:, iQms])
    return dict(Qes=float(np.mean(Qes)), u_Qes=float(np.std(Qes, ddof=1)),
                Qts=float(np.mean(Qts)), u_Qts=float(np.std(Qts, ddof=1)))


def bande_incertitude_Z(theta, cov, f, modele='clos', h=1e-6):
    """Incertitude sur |Z(f)| par propagation de la COVARIANCE COMPLETE.

        u(|Z|)^2 = G Cov G^T,    G_j = d|Z|/dtheta_j  (differences finies relatives)

    C'EST L'OBJET REELLEMENT LIVRE A L'ACTE 3 (§ 03.5) : pas theta, mais la courbe
    Z(f ; theta) AVEC son incertitude. Et c'est la figure la plus utile de l'acte 2 :
    elle dit A LA FREQUENCE DU RACCORD combien on connait reellement la charge. Sur le
    jeu synthetique : 0,35 % a 100 Hz en aleatoire -- a comparer au 1 % de type B apporte
    par R_ref, qui domine donc largement.

    Retourne (|Z|, u(|Z|)).
    """
    f = np.atleast_1d(np.asarray(f, float))
    theta = np.asarray(theta, float)
    base = np.abs(evaluer(modele, f, theta))
    G = np.empty((f.size, theta.size))
    for j in range(theta.size):
        t = theta.copy()
        pas = h * max(abs(theta[j]), 1e-12)
        t[j] += pas
        G[:, j] = (np.abs(evaluer(modele, f, t)) - base) / pas
    var = np.einsum('ij,jk,ik->i', G, np.asarray(cov, float), G)
    return base, np.sqrt(np.maximum(var, 0.0))


# =====================================================================
# 7. DIAGNOSTICS DE RESIDUS (§ 03.7, criteres 1 a 3)
# =====================================================================

def test_sequences(r):
    """Test des sequences de Wald-Wolfowitz sur les SIGNES des residus.

    Retourne (R, E, sd, z) : nombre de suites observees, esperance sous l'hypothese
    "signes tires au hasard", ecart-type, ecart normalise.

        E[R] = 1 + 2 n+ n-/N ,  Var(R) = 2 n+ n- (2 n+ n- - N)/(N^2 (N-1))

    C'EST LE CRITERE LE PLUS DISCRIMINANT DE TOUS (§ 03.7). Sur le bon modele,
    z = +0,4 ; sur des donnees semi-inductives ajustees avec L_e constante, z = -5,6 ;
    sur un bass-reflex ajuste par le modele clos, z = -5,4. Un modele faux produit des
    residus qui gardent le meme signe par plages : peu de suites, donc z tres negatif.
    A appliquer SEPAREMENT au module et a la phase.

    (Le critere qualitatif "pas de suite de signes identiques sur plusieurs points"
    serait piegeux : la plus longue suite vaut 6 sur le jeu synthetique, pour
    log2(69) = 6 attendus par pur hasard.)
    """
    s = np.sign(np.asarray(r, float))
    s = s[s != 0]
    a, b = int((s > 0).sum()), int((s < 0).sum())
    N = a + b
    if N < 2 or a == 0 or b == 0:                     # tous de meme signe : 1 seule suite
        return (1 if N else 0), float('nan'), float('nan'), float('nan')
    R = 1 + int(np.sum(s[1:] != s[:-1]))
    E = 1.0 + 2.0 * a * b / N
    var = 2.0 * a * b * (2.0 * a * b - N) / (N**2 * (N - 1.0))
    sd = np.sqrt(max(var, 0.0))
    return R, float(E), float(sd), float((R - E) / sd) if sd > 0 else float('nan')


def leviers(J):
    """Diagonale de la matrice chapeau H = J (J^T J)^-1 J^T : influence de chaque residu.

    Sa trace vaut p, donc la moyenne des leviers vaut p/(2N) (0,036 pour 5 parametres et
    138 residus). La dispersion globale ne dit pas QUEL point porte l'ajustement ; le
    levier, si. Sur le jeu synthetique le levier maximal est celui de la PHASE A 500 Hz
    -- le point qui, a lui seul, fixe L_e. Consequence pratique pour la phase 2 : si un
    parametre bouge trop sous retrait, on regarde les leviers pour savoir quel point
    re-mesurer, au lieu de re-mesurer les 69.
    """
    Q, _ = np.linalg.qr(np.asarray(J, float))
    return np.sum(Q**2, axis=1)


def analyser_residus(r, n_points, bande_noms=('module', 'phase')):
    """Resume statistique des residus normalises : sequences, maximum, depassements.

    LECTURE, AVEC LE BON SEUIL (§ 03.8) : les r doivent rester dans +-3 A UN OU
    DEUX POINTS PRES. Pour 138 residus on attend 138 x 0,0027 = 0,4 depassement en
    moyenne, et un ajustement PARFAIT sort de +-3 dans 31 % des cas. Alerte a partir de
    |r| > 4, ou de plusieurs depassements groupes dans la meme zone de frequence.
    """
    r = np.asarray(r, float)
    out = OrderedDict()
    blocs = [r[:n_points]] if r.size == n_points else [r[:n_points], r[n_points:]]
    for nom, bloc in zip(bande_noms, blocs):
        R, E, sd, z = test_sequences(bloc)
        out[nom] = dict(runs=R, esperance=E, ecart_type=sd, z=z,
                        rms=float(np.sqrt(np.mean(bloc**2))),
                        moyenne=float(np.mean(bloc)))
    out['max_abs'] = float(np.max(np.abs(r)))
    out['n_au_dela_3'] = int(np.sum(np.abs(r) > 3.0))
    out['n_au_dela_seuil'] = int(np.sum(np.abs(r) > SEUIL_RESIDU))
    out['seuil_alerte'] = SEUIL_RESIDU
    return out


def point_aberrant(r, s2, seuil_r=SEUIL_ABERRANT, seuil_s2=SEUIL_S2[1]):
    """Regle GELEE des points aberrants (§ 03.2), appliquee telle quelle.

    Sur une mesure au lycee, un point franchement faux est quasi certain (ronflement
    50 Hz, decrochage du GBF). Ecarter un point APRES COUP serait indefendable. Regle :
    on ajuste d'abord avec la perte quadratique ; si s^2 > 2 ET qu'UN SEUL residu depasse
    |r| = 5, on relance avec une perte robuste (soft_l1) et on RAPPORTE LES DEUX
    resultats, le point suspect restant dans les donnees et sur la figure.

    Retourne (declenche, indice_du_point, message).
    """
    r = np.asarray(r, float)
    gros = np.where(np.abs(r) > seuil_r)[0]
    if s2 > seuil_s2 and gros.size == 1:
        return True, int(gros[0]), (
            "s^2 = %.2f > %.1f ET un seul residu au-dela de |r| = %.0f (indice %d, "
            "r = %+.1f) : relancer en loss='soft_l1' et RAPPORTER LES DEUX ajustements. "
            "Le point reste dans les donnees et sur la figure."
            % (s2, seuil_s2, seuil_r, gros[0], r[gros[0]]))
    return False, -1, ''


def diagnostic_bande(theta_vrai, f_complet, u_rel=0.02, u_deg=1.0, graine=1,
                     bornes_hautes=(200.0, 300.0, 500.0, 1000.0), modele_vrai='semi',
                     bavard=True):
    """Test C : quel biais un modele a L_e CONSTANTE subit-il sur une bobine A PERTES ?

    On simule des donnees semi-inductives Z = R_e + K(jw)^n + Z_mot (n = 0,7), puis on
    les ajuste avec le modele a 5 parametres sur des bandes de plus en plus larges.

    CE QUE LE TEST ETABLIT (§ 03.6) : le modele a L_e constante n'a pas de partie
    reelle croissante, alors que la bobine reelle en a une (courants de Foucault).
    L'ajustement, force de rendre compte d'un Re(Z) qui monte, ABSORBE la croissance EN
    GONFLANT R_e -- le parametre en apparence le mieux determine, et en realite le plus
    faux. Trois conclusions : (i) restreindre la bande ne guerit PAS (le biais vaut deja
    +7 % a 10-200 Hz) ; (ii) le biais est invisible dans u_cov mais parfaitement visible
    dans s^2 et dans le test des sequences ; (iii) le remede qui marche est le modele a
    6 parametres, qui rend n a 1 % pres et fait disparaitre le biais.

    Retourne la liste des lignes du tableau (une par borne haute) + la ligne du remede.
    """
    lignes = []
    for f_max in bornes_hautes:
        m = f_complet <= f_max
        f = f_complet[m]
        mod, phi, u_mod, u_phi = simuler(theta_vrai, f, modele=modele_vrai,
                                         u_rel=u_rel, u_deg=u_deg, graine=graine)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            t0 = init_depuis_courbe(f, mod, phi, modele='clos', bavard=False)
            th, cov, s2, mot = ajuster_ts(f, mod, phi, u_mod, u_phi, t0, modele='clos',
                                          verifier_caisse=False, bavard=False)
        u = u_covariance(cov)
        _, _, _, z = test_sequences(mot.residus[:f.size])
        biais = th[0] - theta_vrai[0]
        lignes.append(dict(f_max=f_max, Re=th[0], u_Re=u[0],
                           biais_pct=100 * biais / theta_vrai[0],
                           biais_en_u=biais / u[0], s2=s2, z=z, n_points=int(f.size)))
        if bavard:
            print('  ajuste 5 param sur %5.0f-%6.0f Hz : R_e = %.3f +- %.3f (%+.1f %%, '
                  '%+.1f u) ; s2 = %.2f ; z = %+.1f'
                  % (f_complet[0], f_max, th[0], u[0], lignes[-1]['biais_pct'],
                     lignes[-1]['biais_en_u'], s2, z))
    return lignes


def biais_Rref(theta, f, mod, phi, u_mod, u_phi, erreurs=(0.01, 0.03), modele='clos',
               bavard=True):
    """Effet d'une erreur d'ECHELLE sur R_ref : le systematique que le chi2 ne voit pas.

    On multiplie toutes les |Z| par (1 + e) -- exactement ce que fait une R_ref fausse de
    e -- et on reajuste. Resultat attendu (§ 03.5) : R_e, R_es et L_e se decalent de
    +e, f_s et Q_ms ne bougent pas, s^2 reste INCHANGE. C'est la demonstration que
    l'erreur est invisible pour les trois estimateurs aleatoires, et qu'elle doit etre
    comptabilisee a part (budget_systematique).
    """
    lignes = []
    for e in erreurs:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            th, _, s2, _ = ajuster_ts(f, mod * (1 + e), phi, u_mod * (1 + e), u_phi,
                                      theta, modele=modele, verifier_caisse=False,
                                      bavard=False)
        ecart = 100.0 * (th / np.asarray(theta, float) - 1.0)
        lignes.append(dict(erreur=e, theta=th, ecart_pct=ecart, s2=s2))
        if bavard:
            print('  R_ref %+.0f %% : ecart relatif %s %% ; s2 = %.2f'
                  % (100 * e, np.array2string(ecart, precision=2, suppress_small=True), s2))
    return lignes


# =====================================================================
# 8. CRITERES DE VALIDATION (§ 03.7, les huit criteres)
# =====================================================================

def _verdict(nom, ok, valeur, seuil, message):
    return dict(critere=nom, ok=bool(ok), valeur=valeur, seuil=seuil, message=message)


def valider_identification(resultat, Re_dmm=None, Qms_datasheet=None, bavard=True):
    """Applique les criteres 1 a 6 et 8 du § 03.7 a un resultat de identifier().

    Les criteres sont GELES AVANT l'ajustement sur les vraies mesures : c'est tout
    l'interet de les ecrire dans le code plutot que de les juger a l'oeil.

      1. chi2 reduit dans [0,5 ; 2]. Signal d'alerte non bloquant si
         |s^2 - 1| > 3 racine(2/(2N - p)) : pour 133 degres de liberte la dispersion
         statistique n'est que de 0,12, donc sortir de la fourchette ne peut PAS venir du
         hasard -- c'est un defaut de modele ou une erreur de facteur sur les u.
         Diagnostiquer, ne pas "ajuster les u pour que ca passe".
      2. residus relatifs RMS du meme ordre que l'incertitude de chaine, sur 20-300 Hz.
      3. absence de structure : |z| < 3 au test des sequences, SEPAREMENT module et phase.
      4. stabilite sous retrait de 20 %, NORMALISEE (rapport a 0,50 u_cov dans
         [0,7 ; 1,4]) et decalage moyen < 0,2 u. Ne teste PAS l'adequation.
      5. concordance u_cov / u_MC / u_jack a un facteur 1,5 pres. Valide la
         linearisation, pas le realisme des u.
      6. plausibilite physique : R_e compatible avec le multimetre a 2 u composee (apres
         retrait de la resistance des cordons), Q_ms dans les ordres de grandeur.
      8. unicite du minimum : une nette majorite des departs retrouve le meilleur cout.

    (Le critere 0 est l'aiguillage de caisse, deja applique par garde_fou_caisse ; le
    critere 7 est le test a blanc du code, execute par test_a_blanc().)

    Retourne un OrderedDict de verdicts + la cle 'tout_passe'.
    """
    v = OrderedDict()
    noms = resultat['noms']
    s2 = resultat['chi2_reduit']
    ddl = resultat['n_residus'] - resultat['p']
    marge = 3.0 * np.sqrt(2.0 / ddl)
    v['0_aiguillage'] = _verdict(
        'aiguillage clos / bass-reflex', resultat['diagnostic_caisse']['compatible'],
        resultat['diagnostic_caisse']['n_pics'], '1 pic -> 5 param., >= 2 -> 8 param.',
        resultat['diagnostic_caisse']['message'] or 'modele coherent avec le nombre de pics')
    v['1_chi2'] = _verdict(
        'chi2 reduit', SEUIL_S2[0] <= s2 <= SEUIL_S2[1], s2, SEUIL_S2,
        's2 = %.3f pour %d degres de liberte (dispersion statistique attendue %.3f ; '
        'alerte non bloquante si |s2 - 1| > %.2f : %s)'
        % (s2, ddl, np.sqrt(2.0 / ddl), marge,
           'depassee' if abs(s2 - 1) > marge else 'non depassee'))
    rms_mod = resultat['residus']['rms_module_pct_validation']
    rms_phi = resultat['residus']['rms_phase_deg_validation']
    u_rel_moy = 100.0 * resultat['u_relative_moyenne_module']
    v['2_residus_relatifs'] = _verdict(
        'residus relatifs sur 20-300 Hz', rms_mod <= 3.0 * max(u_rel_moy, 1e-9),
        (rms_mod, rms_phi), '<= 3 x incertitude de chaine (%.2f %%)' % u_rel_moy,
        'RMS %.2f %% sur |Z| et %.2f deg sur la phase, pour une incertitude de chaine de '
        '%.2f %%' % (rms_mod, rms_phi, u_rel_moy))
    zs = [resultat['residus']['module']['z']]
    if 'phase' in resultat['residus']:
        zs.append(resultat['residus']['phase']['z'])
    zmax = float(np.nanmax(np.abs(zs)))
    v['3_sequences'] = _verdict(
        'structure des residus (Wald-Wolfowitz)', zmax < SEUIL_Z_SEQUENCES, zs,
        '|z| < %.0f' % SEUIL_Z_SEQUENCES,
        'z = %s (le critere le plus discriminant : -5,6 sur une bobine a pertes ajustee '
        'a L_e constante)' % ', '.join('%+.2f' % x for x in zs))
    if resultat.get('stabilite') is not None:
        rapports = np.asarray(resultat['stabilite']['rapport'], float)
        bruts = np.asarray(resultat['stabilite']['rapport_brut'], float)
        decal = np.asarray(resultat['stabilite']['decalage_en_u'], float)
        ok4 = bool(np.all((rapports > 0.7) & (rapports < 1.4)) and np.all(np.abs(decal) < 0.2))
        i_pire = int(np.argmax(np.abs(np.log(rapports))))
        v['4_stabilite'] = _verdict(
            'stabilite sous retrait de 20 % (conditionnement)', ok4,
            rapports.tolist(), '[0,7 ; 1,4] et decalage < 0,2 u',
            'rapports a 0,50 u_cov racine(s2) : %s (bruts, sans le facteur racine(s2) : '
            '%s) ; decalages %s u. Le parametre le plus ecarte est %s (%.2f) -- un '
            'rapport nettement > 1 signale un ou deux points a FORT LEVIER qui portent '
            'seuls l ajustement (voir le levier maximal). ATTENTION : ce critere mesure '
            'le CONDITIONNEMENT, pas l adequation, et sa valeur fluctue d une '
            'realisation de bruit a l autre.'
            % (np.array2string(rapports, precision=2),
               np.array2string(bruts, precision=2),
               np.array2string(decal, precision=2), noms[i_pire], rapports[i_pire]))
    if resultat.get('u_MC') is not None and resultat.get('u_jack') is not None:
        u_cov = np.asarray(resultat['u_cov'], float)
        rac = np.sqrt(resultat['chi2_reduit'])
        # Deux comparaisons mises sur le MEME pied (§ 03.5) : le Monte-Carlo
        # reproduit (J^T J)^-1 SANS s^2 (il rejoue les u postules), le jackknife mesure
        # la dispersion REELLEMENT observee, donc l'equivalent de u_cov racine(s2).
        rap_mc = np.asarray(resultat['u_MC'], float) / np.maximum(u_cov, 1e-300)
        rap_jk = np.asarray(resultat['u_jack'], float) / np.maximum(u_cov * rac, 1e-300)
        brut = np.vstack([u_cov, resultat['u_MC'], resultat['u_jack']])
        rap = brut.max(axis=0) / np.maximum(brut.min(axis=0), 1e-300)
        ok5 = bool(np.all(np.maximum(rap_mc, 1 / rap_mc) < 1.5)
                   and np.all(np.maximum(rap_jk, 1 / rap_jk) < 1.5))
        v['5_concordance'] = _verdict(
            'concordance u_cov / u_MC / u_jack', ok5,
            dict(mc=rap_mc.tolist(), jack=rap_jk.tolist(), brut=rap.tolist()),
            'facteur < 1,5', 'u_MC/u_cov = %s (teste la LINEARISATION) ; '
            'u_jack/(u_cov racine(s2)) = %s (teste la dispersion reellement observee, '
            'racine(s2) = %.3f) ; rapport max/min brut des trois : %s. Leur accord ne '
            'dit rien du realisme des u : cela, c est s2, le jackknife et la couverture.'
            % (np.array2string(rap_mc, precision=2), np.array2string(rap_jk, precision=2),
               rac, np.array2string(rap, precision=2)))
    ok6, msg6 = True, []
    if Re_dmm is not None and 'Re' in noms:
        i = noms.index('Re')
        u_c = resultat['u_composee'][i] if resultat.get('u_composee') is not None else resultat['u_cov'][i]
        ecart = abs(resultat['theta'][i] - Re_dmm) / max(u_c, 1e-12)
        ok6 = ok6 and ecart < 2.0
        msg6.append('R_e ajuste %.3f ohm vs multimetre %.3f ohm : %.1f u composee '
                    '(apres retrait des cordons)' % (resultat['theta'][i], Re_dmm, ecart))
    if 'Qms' in noms:
        q = resultat['theta'][noms.index('Qms')]
        dans = 0.5 <= q <= 20.0
        ok6 = ok6 and dans
        msg6.append('Q_ms = %.2f (%s la fourchette usuelle 2-10 des 18 pouces)'
                    % (q, 'dans' if 2.0 <= q <= 10.0 else 'HORS'))
    if Qms_datasheet is not None and 'Qms' in noms:
        msg6.append('datasheet : Q_ms = %.2f' % Qms_datasheet)
    v['6_plausibilite'] = _verdict('plausibilite physique', ok6, None,
                                   'R_e a 2 u du multimetre ; Q_ms plausible',
                                   ' ; '.join(msg6) or 'aucun controle externe fourni')
    if resultat.get('multi_depart') is not None:
        fr = resultat['multi_depart']['fraction']
        v['8_unicite'] = _verdict(
            'unicite du minimum (multi-depart)', fr >= 0.5, fr, '>= 0,5',
            '%.0f %% des departs retrouvent le meilleur cout ; les minima parasites se '
            'reconnaissent a leur cout (chi2 reduit de l ordre de 1e3), pas a une '
            'preference' % (100 * fr))
    v['tout_passe'] = bool(all(x['ok'] for k, x in v.items() if k != 'tout_passe'))
    if bavard:
        print(texte_validation(v))
    return v


def texte_validation(verdicts):
    """Met en forme les verdicts en tableau ASCII, pour le journal et l'annexe."""
    lignes = ['Criteres de validation de l identification (§ 03.7)',
              '-' * 72]
    for cle, x in verdicts.items():
        if cle == 'tout_passe':
            continue
        lignes.append('  [%s] %-38s %s' % ('OK' if x['ok'] else '!!', x['critere'],
                                           ''))
        for ligne in _replier(x['message'], 66):
            lignes.append('         ' + ligne)
    lignes.append('  => %s' % ('tous les criteres passent'
                               if verdicts.get('tout_passe') else
                               'AU MOINS UN CRITERE ECHOUE -- ne rien conclure'))
    return '\n'.join(lignes)


# =====================================================================
# 9. DONNEES SYNTHETIQUES (tests de methode UNIQUEMENT)
# =====================================================================

def simuler(theta, f, modele='clos', u_rel=0.02, u_deg=1.0, graine=0, rng=None):
    """Fabrique une courbe SYNTHETIQUE bruitee -> (mod, phi_deg, u_mod, u_phi_deg).

    AUCUNE MESURE : cette fonction sert a prouver que le code retrouve ce qu'on y a mis,
    et surtout COMMENT il echoue quand le modele est faux. En phase 2 elle est remplacee
    par la lecture du CSV (io_mesures.lire_mesure) ; rien d'autre ne change.

    Bruit : relatif u_rel sur le module (hypothese a remplacer par les incertitudes
    reellement etalonnees en phase 1), absolu u_deg sur la phase.
    """
    rng = np.random.default_rng(graine) if rng is None else rng
    f = np.asarray(f, float)
    Z = evaluer(modele, f, theta)
    mod = np.abs(Z) * (1 + u_rel * rng.standard_normal(f.size))
    phi = np.degrees(np.angle(Z)) + u_deg * rng.standard_normal(f.size)
    return mod, phi, u_rel * mod, np.full(f.size, float(u_deg))


# =====================================================================
# 10. PIPELINE COMPLET : identifier()
# =====================================================================

def identifier(f, mod, phi, u_mod, u_phi, modele='auto', Re_dmm=None,
               bande=BANDE_AJUSTEMENT, bande_validation=BANDE_VALIDATION,
               n_mc=N_MC_DEFAUT, n_retrait=N_RETRAIT_DEFAUT, n_multi=N_MULTI_DEFAUT,
               graine=0, u_rel_R_ref=0.01, u_B_relatives_sup=None, jack=True,
               forcer=False, bavard=True, source='donnees fournies en memoire',
               statut_donnees=None, reperes=(40.0, 100.0, 200.0), rapide=False):
    """Chaine complete de l'acte 2 : aiguillage -> initialisation -> ajustement ->
    incertitudes (A et B) -> diagnostics -> criteres -> dictionnaire serialisable.

    modele='auto' choisit le modele D'APRES LA COURBE (critere 0 du § 03.7) : un
    seul pic -> 'clos' (5 parametres) ; deux pics ou plus -> chaine bass-reflex
    ('bassreflex8', puis 'bassreflex', puis le repli phenomenologique 'deux_pics'), le
    premier qui converge etant retenu. Donner un nom explicite impose le modele -- et
    leve CaisseIncompatible s'il contredit le comptage des pics, sauf forcer=True.

    rapide=True reduit les tirages (developpement) ; les chiffres de l'oral se
    produisent SANS rapide.

    Retourne un OrderedDict entierement serialisable (voir resultat_serialisable) :
    theta, u_A, u_B, u_composee, covariance, correlation, chi2 reduit, residus et leurs
    diagnostics, Monte-Carlo, jackknife, stabilite, grandeurs derivees, |Z| et son
    incertitude aux frequences reperes, verdicts des criteres, provenance.
    """
    if rapide:
        n_mc, n_retrait, n_multi = max(30, n_mc // 10), max(20, n_retrait // 5), min(n_multi, 12)
    f = np.asarray(f, float)
    mod = np.asarray(mod, float)
    u_mod = np.asarray(u_mod, float) * np.ones_like(f)
    avec_phase = phi is not None
    if avec_phase:
        phi = np.asarray(phi, float)
        u_phi = np.asarray(u_phi, float) * np.ones_like(f)
    ordre = np.argsort(f)
    f, mod, u_mod = f[ordre], mod[ordre], u_mod[ordre]
    if avec_phase:
        phi, u_phi = phi[ordre], u_phi[ordre]

    m = _bande(f, bande)
    if m.sum() < 8:
        raise ValueError('identifier : seulement %d points dans la bande %s'
                         % (m.sum(), bande))
    fa, moda, u_moda = f[m], mod[m], u_mod[m]
    phia = phi[m] if avec_phase else None
    u_phia = u_phi[m] if avec_phase else None

    if bavard:
        print('grille : %d frequences de %.1f a %.1f Hz (%d residus)'
              % (fa.size, fa[0], fa[-1], fa.size * (2 if avec_phase else 1)))

    # --- critere 0 : aiguillage AVANT tout ajustement -------------------------------
    diag = garde_fou_caisse(fa, moda, modele=None, bavard=bavard)
    if modele == 'auto':
        candidats = ('clos',) if diag['n_pics'] <= 1 else CHAINE_BASSREFLEX
    else:
        nom_demande = _resoudre_modele(modele)[0]
        verif = garde_fou_caisse(fa, moda, modele=nom_demande, bavard=False,
                                 strict=not forcer)
        if not verif['compatible'] and bavard:
            print('  (modele impose malgre le garde-fou : forcer=True)')
        candidats = (nom_demande,)

    # --- initialisation lue sur la courbe, puis ajustement --------------------------
    derniere_erreur, retenu = None, None
    for nom in candidats:
        try:
            theta0 = init_depuis_courbe(fa, moda, phia, Re0=Re_dmm, modele=nom,
                                        bavard=bavard)
            theta, cov, s2, moteur = ajuster_ts(fa, moda, phia, u_moda, u_phia, theta0,
                                                modele=nom, verifier_caisse=False,
                                                bavard=bavard)
            if not np.all(np.isfinite(theta)) or not np.all(np.isfinite(cov)):
                raise ErreurAjustement('parametres ou covariance non finis')
            retenu = nom
            break
        except Exception as exc:                  # on passe au modele suivant de la chaine
            derniere_erreur = exc
            if bavard:
                print("  modele '%s' ecarte : %s" % (nom, exc))
    if retenu is None:
        raise ErreurAjustement('aucun modele de la chaine %s n a converge (%s)'
                               % (candidats, derniere_erreur))
    nom = retenu
    noms = list(_noms(nom, theta.size))
    u_cov = u_covariance(cov)
    # Le critere 0 juge le modele RETENU, pas la courbe seule : sans cette relecture, un
    # ajustement obtenu avec forcer=True serait rapporte comme "aiguillage correct".
    with warnings.catch_warnings(record=True):        # deja averti plus haut
        warnings.simplefilter('always')
        diag = garde_fou_caisse(fa, moda, modele=nom, bavard=False)

    # --- regle gelee des points aberrants -------------------------------------------
    aberrant, i_aberrant, msg_aberrant = point_aberrant(moteur.residus, s2)
    robuste = None
    if aberrant:
        if bavard:
            print('  ' + msg_aberrant)
        th_r, cov_r, s2_r, mot_r = ajuster_ts(fa, moda, phia, u_moda, u_phia, theta0,
                                              modele=nom, loss='soft_l1',
                                              verifier_caisse=False, bavard=False)
        robuste = dict(theta=th_r, u=u_covariance(cov_r), s2=s2_r,
                       indice=i_aberrant,
                       f_Hz=float(fa[i_aberrant % fa.size]), message=msg_aberrant)

    # --- incertitudes : les trois estimateurs aleatoires + le type B ----------------
    mc = monte_carlo(theta, fa, u_moda, u_phia, n=n_mc, graine=graine + 1, modele=nom)
    jk = jackknife(theta, fa, moda, phia, u_moda, u_phia, modele=nom) if jack else None
    stab = None
    if n_retrait:
        st = stabilite_retrait(theta, fa, moda, phia, u_moda, u_phia, modele=nom,
                               n=n_retrait, graine=graine + 2)
        attendu = RAPPORT_RETRAIT_ATTENDU * u_cov
        stab = dict(ecart_type=st['ecart_type'],
                    rapport=st['ecart_type'] / np.maximum(attendu * np.sqrt(s2), 1e-300),
                    rapport_brut=st['ecart_type'] / np.maximum(attendu, 1e-300),
                    decalage_en_u=st['decalage'] / np.maximum(u_cov, 1e-300),
                    n_reussis=st['n_reussis'])
    multi = multi_depart(fa, moda, phia, u_moda, u_phia, theta0, n=n_multi,
                         graine=graine + 3, modele=nom) if n_multi else None
    budget, texte_budget = budget_systematique(theta, u_cov, modele=nom,
                                               u_rel_R_ref=u_rel_R_ref,
                                               u_B_relatives_sup=u_B_relatives_sup)
    if budget is not None:
        u_B = np.array([budget[c]['u_B'] for c in noms])
        u_composee = np.array([budget[c]['u_composee'] for c in noms])
    else:
        u_B = u_composee = None

    # --- diagnostics de residus ------------------------------------------------------
    res = analyser_residus(moteur.residus, fa.size)
    rms_mod_v, rms_phi_v = ecarts_relatifs(theta, fa, moda, phia, modele=nom,
                                           bande=bande_validation)
    rms_mod_a, rms_phi_a = ecarts_relatifs(theta, fa, moda, phia, modele=nom)
    h = leviers(moteur.jac)
    i_h = int(np.argmax(h))
    levier = dict(max=float(h[i_h]), moyenne=float(np.mean(h)), indice=i_h,
                  grandeur='module' if i_h < fa.size else 'phase',
                  f_Hz=float(fa[i_h % fa.size]))

    # --- ce que recoit vraiment l'acte 3 : |Z| et son incertitude -------------------
    f_rep = np.array([x for x in reperes if fa[0] <= x <= fa[-1]], float)
    z_rep, u_rep = bande_incertitude_Z(theta, cov, f_rep, modele=nom)

    resultat = OrderedDict()
    resultat['statut_donnees'] = statut_donnees or (
        'NON RENSEIGNE -- rappel : aucune mesure de l enceinte de Thomas n existe a ce jour')
    resultat['source'] = source
    resultat['modele'] = nom
    resultat['modeles_essayes'] = list(candidats)
    resultat['noms'] = noms
    resultat['unites'] = [UNITES.get(c, '?') for c in noms]
    resultat['theta'] = theta
    resultat['theta0'] = theta0
    resultat['u_cov'] = u_cov
    resultat['u_MC'] = mc['u']
    resultat['u_jack'] = jk['u'] if jk else None
    resultat['u_A'] = u_cov
    resultat['u_B'] = u_B
    resultat['u_composee'] = u_composee
    resultat['covariance'] = cov
    resultat['correlation'] = correlation(cov)
    resultat['convention_covariance'] = ('(J^T J)^-1 SANS facteur s^2 (§ 03.5) : '
                                         's^2 est un diagnostic, pas un correctif')
    resultat['chi2_reduit'] = s2
    resultat['n_points'] = int(fa.size)
    resultat['n_residus'] = int(moteur.n_residus)
    resultat['p'] = int(theta.size)
    resultat['moteur'] = str(moteur)
    resultat['conditionnement'] = moteur.cond
    resultat['alerte_moteur'] = moteur.alerte
    resultat['messages_moteur'] = list(moteur.messages)
    resultat['bande_ajustement'] = [float(fa[0]), float(fa[-1])]
    resultat['bande_validation'] = list(bande_validation)
    resultat['diagnostic_caisse'] = diag
    resultat['u_relative_moyenne_module'] = float(np.mean(u_moda / moda))
    res_mod = res.pop('module')
    res_phi = res.pop('phase', None)
    resultat['residus'] = dict(
        r=moteur.residus, module=res_mod,
        rms_module_pct_ajustement=rms_mod_a, rms_phase_deg_ajustement=rms_phi_a,
        rms_module_pct_validation=rms_mod_v, rms_phase_deg_validation=rms_phi_v,
        levier=levier, **res)
    if res_phi is not None:
        resultat['residus']['phase'] = res_phi
    resultat['point_aberrant'] = robuste
    resultat['monte_carlo'] = dict(n=mc['n_reussis'], biais_en_u=mc['biais'] /
                                   np.maximum(u_cov, 1e-300))
    resultat['stabilite'] = stab
    resultat['multi_depart'] = (dict(fraction=multi['fraction'], n=multi['n_reussis'],
                                     cout_min=float(np.min(multi['couts'])),
                                     cout_median=float(np.median(multi['couts'])))
                                if multi else None)
    resultat['derivees'] = grandeurs_derivees(mc['tirages'], modele=nom)
    resultat['budget_systematique'] = (
        {c: dict(budget[c]) for c in noms} if budget is not None else None)
    resultat['texte_budget'] = texte_budget
    resultat['Z_reperes'] = [dict(f_Hz=float(x), module_ohm=float(z), u_ohm=float(u),
                                  u_relative_pct=100.0 * float(u / z))
                             for x, z, u in zip(f_rep, z_rep, u_rep)]
    resultat['tirages_mc'] = mc['tirages']
    resultat['provenance'] = provenance(graine=graine)
    resultat['validation'] = valider_identification(resultat, Re_dmm=Re_dmm, bavard=False)
    if bavard:
        print(texte_resultat(resultat))
    return resultat


def identifier_fichier(chemin, modele='auto', bavard=True, **kw):
    """Meme chose, en partant d'un CSV de mesure (io_mesures.lire_mesure).

    Les metadonnees FONT PARTIE de la mesure : u(R_ref) alimente le type B, R_e lu au
    multimetre avant le balayage sert au controle de plausibilite (critere 6), et le
    statut des donnees est recopie tel quel dans le resultat -- c'est ainsi qu'un
    fichier SYNTHETIQUE reste etiquete SYNTHETIQUE jusque dans le JSON livre a l'acte 3.
    """
    d, meta = IO.lire_mesure(chemin)
    u_rel_R_ref = IO.meta_flottant(meta, 'u_R_ref_relative_pct', 1.0) / 100.0
    try:
        Re_dmm = IO.meta_flottant(meta, 'Re_DC_avant_ohm')
    except Exception:
        Re_dmm = None
    kw.setdefault('Re_dmm', Re_dmm)
    kw.setdefault('u_rel_R_ref', u_rel_R_ref)
    kw.setdefault('statut_donnees', meta.get('statut_donnees'))
    res = identifier(d['f_Hz'], d['module_Z_ohm'], d['phase_deg'],
                     d['u_module_alea_ohm'], d['u_phase_deg'], modele=modele,
                     bavard=bavard, source=os.path.basename(chemin), **kw)
    res['provenance']['fichier'] = os.path.abspath(chemin)
    res['provenance']['sha256_entree'] = empreinte(chemin)
    res['metadonnees_mesure'] = dict(meta)
    return res


def texte_resultat(resultat):
    """Tableau de sortie lisible : parametres, u_A, u_B, correlations, diagnostics."""
    noms = resultat['noms']
    th, u_a = resultat['theta'], resultat['u_A']
    u_b, u_c = resultat['u_B'], resultat['u_composee']
    lignes = []
    lignes.append("modele retenu : '%s' (%d parametres), moteur %s"
                  % (resultat['modele'], resultat['p'], resultat['moteur']))
    entete = '%-6s %12s %10s %10s %10s' % ('param', 'ajuste', 'u_A', 'u_B', 'u_comp')
    lignes.append(entete)
    for i, c in enumerate(noms):
        fac, unite = AFFICHAGE.get(c, (1.0, UNITES.get(c, '-')))
        lignes.append('%-6s %12.5g %10.4g %10s %10s   [%s]'
                      % (c, th[i] * fac, u_a[i] * fac,
                         '%.4g' % (u_b[i] * fac) if u_b is not None else '-',
                         '%.4g' % (u_c[i] * fac) if u_c is not None else '-', unite))
    lignes.append('chi2 reduit s2 = %.3f (%d residus, %d parametres) ; cond(J theta) = %.2g'
                  % (resultat['chi2_reduit'], resultat['n_residus'], resultat['p'],
                     resultat['conditionnement']))
    r = resultat['residus']
    lignes.append('residu relatif RMS : %.2f %% sur |Z|, %.2f deg sur phi (bande '
                  "d'ajustement) ; %.2f %% et %.2f deg sur %g-%g Hz (porte de validation)"
                  % (r['rms_module_pct_ajustement'], r['rms_phase_deg_ajustement'],
                     r['rms_module_pct_validation'], r['rms_phase_deg_validation'],
                     resultat['bande_validation'][0], resultat['bande_validation'][1]))
    lignes.append('sequences : module z = %+.2f ; phase z = %+.2f ; max|r| = %.2f ; '
                  '%d residu(s) au-dela de 3'
                  % (r['module']['z'], r.get('phase', {}).get('z', float('nan')),
                     r['max_abs'], r['n_au_dela_3']))
    lignes.append('levier max %.3f (moyenne %.3f) -> %s a %.1f Hz'
                  % (r['levier']['max'], r['levier']['moyenne'], r['levier']['grandeur'],
                     r['levier']['f_Hz']))
    rho = np.asarray(resultat['correlation'], float)
    lignes.append('matrice de correlation (%s) :' % ', '.join(noms))
    for ligne in np.array2string(rho, precision=2, suppress_small=True).splitlines():
        lignes.append('  ' + ligne)
    d = resultat['derivees']
    if d:
        lignes.append('Q_es = %.3f +- %.3f ; Q_ts = %.3f +- %.3f (sur les tirages MC, '
                      'covariance respectee)' % (d['Qes'], d['u_Qes'], d['Qts'], d['u_Qts']))
    for z in resultat['Z_reperes']:
        lignes.append('|Z(%6.1f Hz)| = %7.2f ohm  u = %.3f ohm (%.2f %%)  '
                      '[covariance complete]'
                      % (z['f_Hz'], z['module_ohm'], z['u_ohm'], z['u_relative_pct']))
    if resultat['texte_budget'] and resultat['budget_systematique']:
        lignes.append('')
        lignes.append(resultat['texte_budget'])
    return '\n'.join(lignes)


# =====================================================================
# 11. SERIALISATION : le livrable formel de l'acte 3
# =====================================================================

def empreinte(chemin):
    """SHA-256 d'un fichier : sans elle, un JSON perime dans le depot est
    indiscernable d'un JSON a jour -- et ce sont les chiffres cites a l'oral."""
    h = hashlib.sha256()
    with open(chemin, 'rb') as fh:
        for bloc in iter(lambda: fh.read(65536), b''):
            h.update(bloc)
    return h.hexdigest()


def _commit_git():
    """Hash du commit courant, lu directement dans .git (aucun sous-processus)."""
    try:
        git = os.path.join(os.path.dirname(_ICI), '.git')
        with open(os.path.join(git, 'HEAD'), encoding='utf-8') as fh:
            tete = fh.read().strip()
        if not tete.startswith('ref:'):
            return tete
        ref = tete.split(':', 1)[1].strip()
        direct = os.path.join(git, *ref.split('/'))
        if os.path.isfile(direct):
            with open(direct, encoding='utf-8') as fh:
                return fh.read().strip()
        with open(os.path.join(git, 'packed-refs'), encoding='utf-8') as fh:
            for ligne in fh:
                if ligne.strip().endswith(' ' + ref):
                    return ligne.split()[0]
    except Exception:
        return None
    return None


def provenance(graine=None):
    """Date, versions, graine, commit : la carte d'identite d'un resultat (§ 09.8)."""
    return OrderedDict([
        ('date', datetime.now().strftime('%Y-%m-%dT%H:%M:%S')),
        ('python', sys.version.split()[0]),
        ('numpy', np.__version__),
        ('scipy', __import__('scipy').__version__ if SCIPY else 'absent (repli LM maison)'),
        ('moteur_disponible', 'scipy' if SCIPY else 'repli'),
        ('graine', graine),
        ('commit_git', _commit_git()),
        ('module', 'analyse/ts_fit.py'),
    ])


def _jsonable(objet):
    """Rend un objet serialisable : ndarray -> liste, numpy scalaire -> python."""
    if isinstance(objet, np.ndarray):
        return [_jsonable(x) for x in objet.tolist()]
    if isinstance(objet, (np.floating, np.integer)):
        return objet.item()
    if isinstance(objet, (np.bool_,)):
        return bool(objet)
    if isinstance(objet, float) and not np.isfinite(objet):
        return None                                  # JSON n'a ni NaN ni inf
    if isinstance(objet, dict):
        return {str(k): _jsonable(v) for k, v in objet.items()}
    if isinstance(objet, (list, tuple)):
        return [_jsonable(x) for x in objet]
    return objet


def resultat_serialisable(resultat, tirages=False):
    """Dictionnaire JSON-compatible. tirages=False allege le fichier (les 300 tirages
    Monte-Carlo peuvent etre ecrits a part, en CSV, pour l'acte 3)."""
    sortie = OrderedDict()
    for cle, valeur in resultat.items():
        if cle in ('tirages_mc',) and not tirages:
            continue
        if cle == 'residus':
            valeur = dict(valeur)
            valeur['r'] = _jsonable(np.asarray(valeur['r'], float))
        sortie[cle] = _jsonable(valeur)
    return sortie


def ecrire_parametres_ts(resultat, chemin=None, tirages=False):
    """Ecrit resultats/parametres_ts.json -- le LIVRABLE FORMEL pour l'acte 3.

    Sans cet artefact, la phase 3 repartirait de cinq u independants : exactement
    l'erreur que le § 03.5 denonce (rho(R_es, Q_ms) = 0,83). Le fichier porte donc
    la COVARIANCE COMPLETE, et sa PROVENANCE (SHA-256 de l'entree, commit, graine, date).

    Le fichier est l'un des deux JSON versionnes malgre la regle .gitignore
    `analyse/resultats/*` : c'est un chiffre cite a l'oral.
    """
    chemin = chemin or os.path.join(IO.DOSSIER_RESULTATS, 'parametres_ts.json')
    dossier = os.path.dirname(os.path.abspath(chemin))
    if dossier and not os.path.isdir(dossier):
        os.makedirs(dossier)
    with open(chemin, 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(resultat_serialisable(resultat, tirages=tirages), fh,
                  ensure_ascii=False, indent=2)
        fh.write('\n')
    return chemin


def ecrire_tirages_mc(resultat, chemin):
    """Ecrit les tirages Monte-Carlo en CSV (ts_mc.csv du § 03.8) : l'acte 3 les
    repasse dans l'optimiseur pour voir de combien la reponse du filtre bouge quand
    theta bouge de u. C'est le chainon qui ferme la boucle entre les actes 2 et 3."""
    T = np.asarray(resultat['tirages_mc'], float)
    with open(chemin, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('# tirages Monte-Carlo des parametres T-S -- %s\n'
                 % resultat['statut_donnees'])
        fh.write(','.join(resultat['noms']) + '\n')
        for ligne in T:
            fh.write(','.join('%.9g' % x for x in ligne) + '\n')
    return chemin


# =====================================================================
# 12. TEST A BLANC (critere 7) ET LES HUIT TESTS DE DIAGNOSTIC
# =====================================================================

def test_a_blanc(bavard=True, graine=11):
    """Critere 7 : le code retrouve-t-il des DIPOLES CONNUS ? (§ 03.4, test A)

    "Si le code ne retrouve pas une resistance, il ne retrouvera pas un haut-parleur."
    Deux dipoles, on ne change QUE le modele : une resistance etalon de 100 ohm (avec
    l'inductance de cordon, 1 uH, qui n'y est PAS identifiable -- 0,0018 degre a 500 Hz),
    et un condensateur de 150 uF d'ESR 0,30 ohm, sur deux decades.

    Sur la resistance, l'inductance sort avec une incertitude PLUS GRANDE QUE SA VALEUR
    (u(L) > L) : elle n'est pas identifiable, et c'est un exemple concret de covariance a
    ne pas publier. On lit R, on IGNORE u(L). Selon le niveau de bruit de phase simule,
    le garde-fou de conditionnement de ajuster_ts se declenche en plus -- il est signale
    quand c'est le cas.
    """
    f = MH.grille_log(10.0, 500.0, 12)
    sorties = []
    for nom, theta, u_rel, u_deg, etiquette in [
            ('RL', np.array([100.0, 1e-6]), 0.01, 0.5, 'resistance etalon 100 ohm'),
            ('RC', np.array([0.30, 150e-6]), 0.01, 0.5, 'condensateur 150 uF (ESR 0,30)')]:
        mod, phi, u_mod, u_phi = simuler(theta, f, modele=nom, u_rel=u_rel,
                                         u_deg=u_deg, graine=graine)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            t0 = init_depuis_courbe(f, mod, phi, modele=nom, bavard=False)
            th, cov, s2, mot = ajuster_ts(f, mod, phi, u_mod, u_phi, t0, modele=nom,
                                          verifier_caisse=False, bavard=False)
        u = u_covariance(cov)
        ecart = (th - theta) / np.maximum(u, 1e-300)
        sorties.append(dict(dipole=etiquette, modele=nom, theta=th, u=u, s2=s2,
                            ecart_en_u=ecart, alerte=mot.alerte, cond=mot.cond))
        if bavard:
            noms = NOMS_THETA[nom]
            if mot.alerte:
                print('  ALERTE (attendue sur la resistance) : cond = %.1e -> covariance '
                      'NON exploitable pour L' % mot.cond)
            print('  %-34s : %s ; s2 = %.2f'
                  % (etiquette,
                     ' ; '.join('%s = %.4g +- %.2g (%+.1f u)' % (c, v, uu, e)
                                for c, v, uu, e in zip(noms, th, u, ecart)), s2))
            for c, v, uu in zip(noms, th, u):
                if uu > abs(v):
                    print('     -> %s : u(%s) > |%s| -- parametre NON identifiable sur ce '
                          'dipole (une inductance de cordon de 1 uH vaut 0,0018 deg a '
                          '500 Hz). On lit la valeur utile, on ignore celle-ci.'
                          % (c, c, c))
    return sorties


def _couverture(theta_vrai, f, n=300, u_rel=0.02, u_deg=1.0, graine=5, bavard=True):
    """Test B : n realisations de bruit INDEPENDANTES -> les u annoncees sont-elles
    calibrees ? C'est L'ARGUMENT FORT du module, et celui a montrer au jury -- pas le
    tirage favorable d'un ajustement unique. On attend 68 % des ecarts sous u et 95 %
    sous 2u, et s^2 qui ne sort jamais de [0,5 ; 2]."""
    rng = np.random.default_rng(graine)
    dedans1 = np.zeros(len(theta_vrai))
    dedans2 = np.zeros(len(theta_vrai))
    tous, s2s, cinq = 0, [], 0
    for _ in range(int(n)):
        mod, phi, u_mod, u_phi = simuler(theta_vrai, f, u_rel=u_rel, u_deg=u_deg, rng=rng)
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                t0 = init_depuis_courbe(f, mod, phi, bavard=False)
                th, cov, s2, _ = ajuster_ts(f, mod, phi, u_mod, u_phi, t0,
                                            verifier_caisse=False, bavard=False)
        except Exception:
            continue
        u = u_covariance(cov)
        e = np.abs(th - theta_vrai) / u
        dedans1 += (e < 1)
        dedans2 += (e < 2)
        cinq += int(np.all(e < 1))
        s2s.append(s2)
        tous += 1
    s2s = np.array(s2s)
    out = dict(n=tous, sous_1u=100 * dedans1 / tous, sous_2u=100 * dedans2 / tous,
               tous_sous_1u=100.0 * cinq / tous, s2_moyen=float(s2s.mean()),
               s2_min=float(s2s.min()), s2_max=float(s2s.max()))
    if bavard:
        print('  |ecart| < u  : %s %% (68 attendus)'
              % np.array2string(out['sous_1u'], precision=0))
        print('  |ecart| < 2u : %s %% (95 attendus)'
              % np.array2string(out['sous_2u'], precision=0))
        print('  les %d simultanement sous 1u : %.0f %% (0,68^%d = %.0f %% attendus)'
              % (len(theta_vrai), out['tous_sous_1u'], len(theta_vrai),
                 100 * 0.68**len(theta_vrai)))
        print('  s2 : moyenne %.3f, min %.2f, max %.2f sur %d realisations'
              % (out['s2_moyen'], out['s2_min'], out['s2_max'], tous))
    return out


def dispersion_criteres(theta_vrai, f, graines=(1, 2, 3, 7, 20260913), n_retrait=200,
                        n_mc=300, u_rel=0.02, u_deg=1.0, bavard=True):
    """Criteres 4 et 5 sur PLUSIEURS realisations de bruit : ils fluctuent, et beaucoup.

    POURQUOI CE TEST EXISTE. Les criteres 4 (stabilite sous retrait) et 5 (concordance
    des trois estimateurs) ne sont pas des proprietes du code : ce sont des statistiques
    calculees sur UNE realisation de bruit, et elles ont leur propre dispersion. Juger le
    module sur une seule realisation reviendrait a confondre "le code est faux" et "ce
    tirage-la est un peu serre". Verification faite ici : le jackknife et le retrait de
    20 % mesurent tous deux la dispersion REELLEMENT observee, donc ils passent ou
    echouent ENSEMBLE -- ce qui est une coherence interne, pas un hasard -- et leur
    rapport a la valeur attendue va de 0,6 a 1,6 selon le parametre et la realisation.

    Le chiffre a citer est donc la MEDIANE sur les realisations, pas le tirage du jour.
    """
    ra, rj, rm = [], [], []
    for g in graines:
        mod, phi, u_mod, u_phi = simuler(theta_vrai, f, u_rel=u_rel, u_deg=u_deg, graine=g)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            t0 = init_depuis_courbe(f, mod, phi, bavard=False)
            th, cov, s2, _ = ajuster_ts(f, mod, phi, u_mod, u_phi, t0,
                                        verifier_caisse=False, bavard=False)
            u = u_covariance(cov)
            st = stabilite_retrait(th, f, mod, phi, u_mod, u_phi, n=n_retrait, graine=2)
            jk = jackknife(th, f, mod, phi, u_mod, u_phi)
            mc = monte_carlo(th, f, u_mod, u_phi, n=n_mc, graine=g + 100)
        rac = np.sqrt(s2)
        ra.append(st['ecart_type'] / (RAPPORT_RETRAIT_ATTENDU * u * rac))
        rj.append(jk['u'] / (u * rac))
        rm.append(mc['u'] / u)
        if bavard:
            print('  graine %8d : s2 = %.3f ; critere 4 %s ; u_jack/(u_cov rac(s2)) %s ; '
                  'u_MC/u_cov %s'
                  % (g, s2, np.array2string(ra[-1], precision=2),
                     np.array2string(rj[-1], precision=2),
                     np.array2string(rm[-1], precision=2)))
    ra, rj, rm = np.array(ra), np.array(rj), np.array(rm)
    med = dict(retrait=np.median(ra, axis=0), jack=np.median(rj, axis=0),
               mc=np.median(rm, axis=0))
    if bavard:
        print('  MEDIANE sur %d realisations : critere 4 %s ; jackknife %s ; MC %s'
              % (len(graines), np.array2string(med['retrait'], precision=2),
                 np.array2string(med['jack'], precision=2),
                 np.array2string(med['mc'], precision=2)))
        print('  -> c est la mediane qui se cite, pas le tirage du jour ; le Monte-Carlo, '
              'lui, reproduit (J^T J)^-1 a quelques pour-cent (il valide la linearisation).')
    return dict(retrait=ra, jack=rj, mc=rm, medianes=med, graines=list(graines))


def diagnostics(rapide=False):
    """Les HUIT tests de diagnostic du § 03.4, dans l'ordre, sur donnees
    SYNTHETIQUES. Retourne la liste des verdicts (nom, ok, commentaire)."""
    verdicts = []

    def verdict(nom, ok, commentaire=''):
        verdicts.append(dict(nom=nom, ok=bool(ok), commentaire=commentaire))
        print('   -> %-4s %s%s' % ('OK' if ok else 'ECHEC', nom,
                                   (' : ' + commentaire) if commentaire else ''))
        return ok

    theta_v = theta_depuis_jeu(MH.JEU_SYNTHETIQUE_V1, 'clos')
    f = MH.grille_log(10.0, 500.0, 12)
    n_b = 60 if rapide else 300

    print('\n=== A. TEST A BLANC (critere 7) : dipoles connus, on ne change que le modele ===')
    a = test_a_blanc()
    ok_a = (abs(a[0]['ecart_en_u'][0]) < 3 and abs(a[1]['ecart_en_u'][1]) < 3
            and 0.3 < a[1]['s2'] < 3)
    verdict('A. test a blanc', ok_a, 'R et C retrouves a moins de 3 u')

    print('\n=== B. COUVERTURE : %d realisations de bruit independantes ===' % n_b)
    b = _couverture(theta_v, f, n=n_b)
    ok_b = (np.all(b['sous_1u'] > 50) and np.all(b['sous_1u'] < 85)
            and np.all(b['sous_2u'] > 88) and 0.5 < b['s2_moyen'] < 2.0)
    verdict('B. couverture des incertitudes', ok_b,
            'les barres annoncees sont calibrees (68 % / 95 % attendus)')

    print('\n=== C. SEMI-INDUCTANCE : donnees K(jw)^0,7 ajustees a L_e constante ===')
    Le_ref, n_semi = 1.2e-3, 0.7
    K = MH.K_semi_depuis_Le(Le_ref, n_semi, f_ref=1000.0)
    theta_semi = np.array([6.5, K, n_semi, 44.0, 40.0, 4.0])
    f_large = MH.grille_log(10.0, 2000.0, 12)
    lignes_c = diagnostic_bande(theta_semi, f_large, modele_vrai='semi')
    mod, phi, u_mod, u_phi = simuler(theta_semi, f_large, modele='semi', graine=1)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        t0 = init_depuis_courbe(f_large, mod, phi, modele='semi', bavard=False)
        th6, cov6, s2_6, _ = ajuster_ts(f_large, mod, phi, u_mod, u_phi, t0,
                                        modele='semi', verifier_caisse=False, bavard=False)
    u6 = u_covariance(cov6)
    print('  REMEDE, modele 6 param sur 10-2000 Hz : R_e = %.3f +- %.3f ; n = %.3f +- '
          '%.3f (vrai %.3f) ; s2 = %.2f' % (th6[0], u6[0], th6[2], u6[2], n_semi, s2_6))
    biais_croissant = lignes_c[-1]['biais_pct'] > lignes_c[0]['biais_pct'] > 1.0
    ok_c = biais_croissant and abs(th6[2] - n_semi) < 0.05 and abs(th6[0] - 6.5) < 0.15
    print('  ATTENTION : sur ce modele FAUX, le critere de STABILITE (critere 4) passe '
          'quand meme -- il mesure le conditionnement, pas l adequation.')
    verdict('C. biais de R_e par semi-inductance', ok_c,
            'biais croissant avec la bande, corrige par le modele a 6 parametres')

    print('\n=== D. BASS-REFLEX (deux pics) ajuste par le modele 5 parametres ===')
    jeu_br = dict(MH.SUB_TYP_BR)
    theta_br = theta_depuis_jeu(jeu_br, 'bassreflex8')
    f_br = MH.grille_log(10.0, 500.0, 12, densifier=(20.0, 80.0, 24))
    mod_br, phi_br, u_mod_br, u_phi_br = simuler(theta_br, f_br, modele='bassreflex8',
                                                 graine=2)
    ext = MH.extrema_locaux(f_br, mod_br, lissage=3, bande=BANDE_AIGUILLAGE)
    print('  courbe vraie : pics a %s Hz, creux a %s Hz'
          % (np.array2string(ext['f_pics'], precision=1),
             np.array2string(ext['f_creux'], precision=1)))
    with warnings.catch_warnings(record=True) as attrapes:
        warnings.simplefilter('always')
        diag = garde_fou_caisse(f_br, mod_br, modele='clos', bavard=True)
        t0 = init_depuis_courbe(f_br, mod_br, phi_br, bavard=False)
        th5, cov5, s2_5, mot5 = ajuster_ts(f_br, mod_br, phi_br, u_mod_br, u_phi_br, t0,
                                           modele='clos', verifier_caisse=False,
                                           bavard=False)
    u5 = u_covariance(cov5)
    _, _, _, z5 = test_sequences(mot5.residus[:f_br.size])
    rms5, _ = ecarts_relatifs(th5, f_br, mod_br, phi_br)
    print('  ajustement 5 param : R_e = %.3f +- %.3f ; f_s = %.2f +- %.2f ; '
          'Q_ms = %.3f +- %.3f' % (th5[0], u5[0], th5[3], u5[3], th5[4], u5[4]))
    print('  -> il CONVERGE sans erreur, mais s2 = %.3g, RMS = %.1f %%, z = %+.1f'
          % (s2_5, rms5, z5))
    leve = any(issubclass(w.category, UserWarning) and 'GARDE-FOU' in str(w.message)
               for w in attrapes)
    ok_d = (leve and not diag['compatible'] and diag['n_pics'] >= 2
            and (s2_5 > SEUIL_S2[1] or abs(z5) > SEUIL_Z_SEQUENCES))
    try:
        garde_fou_caisse(f_br, mod_br, modele='clos', bavard=False, strict=True)
        ok_d = False                                  # strict=True DOIT lever
    except CaisseIncompatible:
        pass
    print("  et avec LE BON MODELE, sur les memes donnees (modele='auto' -> chaine "
          'bass-reflex) :')
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        res_br = identifier(f_br, mod_br, phi_br, u_mod_br, u_phi_br, modele='auto',
                            n_mc=40, n_retrait=0, n_multi=0, jack=False, bavard=False,
                            statut_donnees='SYNTHETIQUES (bass-reflex illustratif)')
    u_br = res_br['u_cov']
    ecart_br = np.abs(res_br['theta'] - theta_br) / np.maximum(u_br, 1e-300)
    print('    modele retenu : %s ; s2 = %.2f ; %s'
          % (res_br['modele'], res_br['chi2_reduit'],
             ' ; '.join('%s = %.4g +- %.2g (vrai %.4g)' % (c, v, uu, w)
                        for c, v, uu, w in zip(res_br['noms'], res_br['theta'], u_br,
                                               theta_br))))
    ok_br = (res_br['modele'] in CHAINE_BASSREFLEX and res_br['chi2_reduit'] < 3.0
             and abs(res_br['theta'][res_br['noms'].index('fb')] / theta_br[
                 list(NOMS_THETA['bassreflex8']).index('fb')] - 1) < 0.05)
    print('    -> ecart max aux valeurs vraies : %.1f u ; f_b retrouve a %.2f %%'
          % (float(np.max(ecart_br)),
             100 * abs(res_br['theta'][res_br['noms'].index('fb')]
                       / theta_br[list(NOMS_THETA['bassreflex8']).index('fb')] - 1)))
    verdict('D. garde-fou bass-reflex', ok_d and ok_br,
            'le garde-fou se declenche AVANT, le chi2 et les sequences confirment APRES, '
            'et le modele a deux pics retrouve la caisse')

    print('\n=== E. Q_ms ELEVE : largeur du pic et pas de grille ===')
    for q in (1.75, 4.0, 8.0, 12.0):
        larg = largeur_de_small(40.0, q, 6.5, 44.0)
        n_pts = int(np.floor(np.log2((40 + larg / 2) / (40 - larg / 2)) * 12)) + 1
        print('  Q_ms = %5.2f : f2 - f1 = %5.1f Hz -> %2d point(s) au 1/12 d octave '
              'dans la largeur' % (q, larg, n_pts))
    theta_q8 = np.array([6.5, 1.2e-3, 44.0, 40.0, 8.0])
    res_e = []
    for etiquette, grille in [('1/12 oct, 10-500 Hz      ', MH.grille_log(10, 500, 12)),
                              ('+ 1/48 oct sur 20-80 Hz  ',
                               MH.grille_log(10, 500, 12, densifier=(20, 80, 48)))]:
        mod_q, phi_q, um, up = simuler(theta_q8, grille, graine=4)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            t0 = init_depuis_courbe(grille, mod_q, phi_q, bavard=False)
            thq, covq, _, _ = ajuster_ts(grille, mod_q, phi_q, um, up, t0,
                                         verifier_caisse=False, bavard=False)
        uq = u_covariance(covq)
        res_e.append((thq, uq))
        print('  %s %3d points : Q_ms = %.3f +- %.3f (vrai 8,0) ; f_s = %.3f +- %.3f Hz'
              % (etiquette, grille.size, thq[4], uq[4], thq[3], uq[3]))
    ok_e = res_e[1][1][4] < res_e[0][1][4]
    verdict('E. densification autour du pic', ok_e,
            'u(Q_ms) diminue quand on resserre la grille la ou elle informe')

    print('\n=== F. INITIALISATION : jusqu ou faut-il descendre en frequence ? ===')
    ok_f = True
    for q in (1.75, 4.0, 8.0):
        theta_q = np.array([6.5, 1.2e-3, 44.0, 40.0, q])
        etats = []
        for fmin in (10.0, 15.0, 20.0, 25.0, 30.0):
            g = MH.grille_log(fmin, 500.0, 12)
            mod_q, phi_q, _, _ = simuler(theta_q, g, graine=6)
            k = int(np.argmax(mod_q))
            _, replie = _q_de_small(g, mod_q, k, 6.5, float(mod_q[k]), 40.0)
            etats.append('%g Hz:%s' % (fmin, 'repli' if replie else 'OK'))
        print('  Q_ms = %4.2f : %s' % (q, '  '.join(etats)))
        ok_f = ok_f and etats[0].endswith('OK')
    verdict('F. garde-fou d initialisation', ok_f,
            'balayer au moins une octave sous le pic ; sinon repli explicite, pas de plantage')

    print('\n=== G. REPLI SANS SCIPY : Levenberg-Marquardt en numpy pur ===')
    mod_g, phi_g, u_mod_g, u_phi_g = simuler(theta_v, f, graine=3)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        t0 = init_depuis_courbe(f, mod_g, phi_g, bavard=False)
        th_s, cov_s, s2_s, _ = ajuster_ts(f, mod_g, phi_g, u_mod_g, u_phi_g, t0,
                                          verifier_caisse=False, bavard=False)
        th_r, cov_r, s2_r, mot_r = ajuster_ts(f, mod_g, phi_g, u_mod_g, u_phi_g, t0,
                                              forcer_repli=True, verifier_caisse=False,
                                              bavard=False)
    ecart_th = float(np.max(np.abs(th_r / th_s - 1)))
    rapport_u = u_covariance(cov_r) / u_covariance(cov_s)
    print('  ecart relatif max sur les cinq parametres = %.1e ; s2 : %.4f (LM) vs %.4f '
          '(scipy) ; rapport des u = %s'
          % (ecart_th, s2_r, s2_s, np.array2string(rapport_u, precision=4)))
    ok_g = ecart_th < 5e-3 and np.all(np.abs(rapport_u - 1) < 5e-3)
    verdict('G. repli sans scipy', ok_g, 'meme theta et memes sigma que scipy')

    print('\n=== H. POINT ABERRANT (ronflement 50 Hz sur un point : |Z| x 1,5) ===')
    mod_h, phi_h, u_mod_h, u_phi_h = simuler(theta_v, f, graine=3)
    i50 = int(np.argmin(np.abs(f - 50.0)))
    mod_h = mod_h.copy()
    mod_h[i50] *= 1.5
    res_h = {}
    for perte in ('linear', 'soft_l1'):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            t0 = init_depuis_courbe(f, mod_h, phi_h, bavard=False)
            th_h, _, s2_h, mot_h = ajuster_ts(f, mod_h, phi_h, u_mod_h, u_phi_h, t0,
                                              loss=perte, verifier_caisse=False,
                                              bavard=False)
        res_h[perte] = (th_h, s2_h, mot_h)
        print('  loss = %-8s : f_s = %.3f Hz (vrai 40,000) ; Q_ms = %.3f (vrai 1,750) ; '
              's2 = %.2f' % (perte, th_h[3], th_h[4], s2_h))
    decl, idx, msg = point_aberrant(res_h['linear'][2].residus, res_h['linear'][1])
    print('  regle gelee des points aberrants : %s'
          % (msg if decl else 'non declenchee (s2 ou nombre de gros residus insuffisant)'))
    ok_h = (abs(res_h['soft_l1'][0][3] - 40.0) < abs(res_h['linear'][0][3] - 40.0)
            and abs(res_h['soft_l1'][0][4] - 1.75) <= abs(res_h['linear'][0][4] - 1.75))
    verdict('H. perte robuste sur point aberrant', ok_h,
            'soft_l1 ramene f_s et Q_ms vers les valeurs vraies')
    return verdicts


# =====================================================================
# 13. AUTO-TEST (python analyse/ts_fit.py)
# =====================================================================

def _autotest(rapide=False):
    """Chaine complete sur donnees SYNTHETIQUES, puis les huit tests de diagnostic."""
    print('=' * 92)
    print('ts_fit.py : identification des parametres de Thiele-Small (acte 2, § 03)')
    print('DONNEES SYNTHETIQUES -- aucune mesure de l enceinte de Thomas n existe a ce jour.')
    print('=' * 92)
    print('scipy : %s ; numpy %s' % ('present (%s)' % __import__('scipy').__version__
                                     if SCIPY else 'ABSENT -> repli LM maison',
                                     np.__version__))

    theta_v = theta_depuis_jeu(MH.JEU_SYNTHETIQUE_V1, 'clos')
    f = MH.grille_log(10.0, 500.0, 12)
    mod, phi, u_mod, u_phi = simuler(theta_v, f, u_rel=0.02, u_deg=1.0, graine=20260913)

    print('\n--- 1. Chaine complete identifier() sur le jeu synthetique v1 -------------')
    res = identifier(f, mod, phi, u_mod, u_phi, modele='auto', Re_dmm=theta_v[0],
                     graine=0, rapide=rapide, bavard=True,
                     statut_donnees='SYNTHETIQUES (jeu de test de methode v1) -- '
                                    'ne decrit AUCUN haut-parleur reel',
                     source='ts_fit._autotest (simulation)')
    ecart_u = (res['theta'] - theta_v) / res['u_cov']
    print('\nparametre        vrai      init    ajuste     u_cov  ecart/u')
    for i, c in enumerate(res['noms']):
        fac, unite = AFFICHAGE.get(c, (1.0, UNITES.get(c, '-')))
        print('%-6s %10.4g %9.4g %9.4g %9.4g %8.2f   [%s]'
              % (c, theta_v[i] * fac, res['theta0'][i] * fac, res['theta'][i] * fac,
                 res['u_cov'][i] * fac, ecart_u[i], unite))
    print('\n' + texte_validation(res['validation']))

    print('\n--- 2. Les trois estimateurs d incertitude, cote a cote -------------------')
    print('%-6s %10s %10s %10s   %s' % ('param', 'u_cov', 'u_MC', 'u_jack', 'rapport max/min'))
    U = np.vstack([res['u_cov'], res['u_MC'], res['u_jack']])
    for i, c in enumerate(res['noms']):
        fac = AFFICHAGE.get(c, (1.0, ''))[0]
        print('%-6s %10.4g %10.4g %10.4g   %.2f'
              % (c, U[0, i] * fac, U[1, i] * fac, U[2, i] * fac,
                 U[:, i].max() / U[:, i].min()))
    print('  (leur accord valide la LINEARISATION ; le realisme des u se juge par s2, '
          'par le jackknife et par la couverture du test B)')

    print('\n--- 2 bis. Criteres 4 et 5 sur plusieurs realisations de bruit ------------')
    disp = dispersion_criteres(theta_v, f, n_retrait=40 if rapide else 200,
                               n_mc=60 if rapide else 300)
    med4 = disp['medianes']['retrait']
    ok_disp = bool(np.all((med4 > 0.7) & (med4 < 1.4))
                   and np.all(np.abs(disp['medianes']['mc'] - 1) < 0.15))

    print('\n--- 3. Systematique : ce que les trois estimateurs ne voient pas -----------')
    biais_Rref(res['theta'], f, mod, phi, u_mod, u_phi)
    print('  -> f_s et Q_ms sont IMMUNISES (une position et une forme) ; R_e, R_es et '
          'L_e heritent, et s2 ne bronche pas.')

    print('\n--- 4. Livrable pour l acte 3 ---------------------------------------------')
    import tempfile
    dossier = tempfile.mkdtemp(prefix='ts_fit_')
    chemin = ecrire_parametres_ts(res, os.path.join(dossier, 'parametres_ts.json'))
    chemin_mc = ecrire_tirages_mc(res, os.path.join(dossier, 'ts_mc.csv'))
    taille = os.path.getsize(chemin)
    with open(chemin, encoding='utf-8') as fh:
        relu = json.load(fh)
    print('  %s (%d octets, %d cles de premier niveau)'
          % (chemin, taille, len(relu)))
    print('  %s (%d tirages x %d parametres)'
          % (chemin_mc, len(res['tirages_mc']), res['p']))
    print('  NOTE : ecrit dans un dossier temporaire par l auto-test ; en phase 2 la '
          'destination est analyse/resultats/parametres_ts.json (versionne).')
    ok_json = (relu['modele'] == res['modele']
               and len(relu['covariance']) == res['p']
               and relu['statut_donnees'].startswith('SYNTHETIQUES'))

    print('\n--- 5. Lecture d un CSV de mesure (io_mesures) ------------------------------')
    ok_csv = True
    try:
        chemin_csv = IO.CHEMIN_EXEMPLE
        if not os.path.isfile(chemin_csv):
            chemin_csv = IO.generer_exemple_synthetique()
        res_csv = identifier_fichier(chemin_csv, bavard=False, rapide=True, n_retrait=0)
        vrai_csv = IO.SUB_TYPIQUE
        print('  %s : modele %s, s2 = %.2f, R_e = %.3f ohm (fichier : %.3f), '
              'f_s = %.2f Hz (fichier : %.2f), Q_ms = %.2f (fichier : %.2f)'
              % (os.path.basename(chemin_csv), res_csv['modele'], res_csv['chi2_reduit'],
                 res_csv['theta'][0], vrai_csv['Re'], res_csv['theta'][3], vrai_csv['fs'],
                 res_csv['theta'][4], vrai_csv['Qms']))
        print('  statut : %s' % res_csv['statut_donnees'])
        print('  sha256 de l entree : %s...' % res_csv['provenance']['sha256_entree'][:16])
        ecarts = [abs(res_csv['theta'][0] / vrai_csv['Re'] - 1),
                  abs(res_csv['theta'][3] / vrai_csv['fs'] - 1),
                  abs(res_csv['theta'][4] / vrai_csv['Qms'] - 1)]
        ok_csv = max(ecarts) < 0.05
        print('  ecart relatif max sur (R_e, f_s, Q_ms) : %.2f %%' % (100 * max(ecarts)))
    except Exception as exc:
        ok_csv = False
        print('  ECHEC de la lecture du CSV : %s' % exc)

    print('\n' + '=' * 92)
    print('HUIT TESTS DE DIAGNOSTIC (§ 03.4)')
    print('=' * 92)
    verdicts = diagnostics(rapide=rapide)

    ok_fit = (np.all(np.abs(ecart_u) < 3.0)
              and np.all(np.abs(res['theta'] / theta_v - 1) < 0.05)
              and SEUIL_S2[0] <= res['chi2_reduit'] <= SEUIL_S2[1])
    verdicts.insert(0, dict(nom='0. chaine complete (theta a < 5 % et < 3 u, s2 dans '
                                '[0,5 ; 2])', ok=bool(ok_fit), commentaire=''))
    verdicts.append(dict(nom='I. livrable JSON relisible', ok=bool(ok_json), commentaire=''))
    verdicts.append(dict(nom='I bis. criteres 4 et 5 : medianes sur 5 realisations dans '
                             'les fourchettes', ok=ok_disp, commentaire=''))
    verdicts.append(dict(nom='J. identification depuis le CSV de mesure', ok=bool(ok_csv),
                         commentaire=''))

    print('\n' + '=' * 92)
    for v in verdicts:
        print('  [%s] %s' % ('OK' if v['ok'] else '!!', v['nom']))
    tout = all(v['ok'] for v in verdicts)
    print('AUTO-TEST : ' + ('TOUT PASSE' if tout else
                            'AU MOINS UN ECHEC -- ne conclure sur aucun chiffre'))
    print('=' * 92)
    return 0 if tout else 1


if __name__ == '__main__':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    raise SystemExit(_autotest(rapide='--rapide' in sys.argv))
