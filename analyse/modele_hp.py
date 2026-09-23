"""Modele direct de l'impedance electrique d'un haut-parleur : Z(jw ; theta).

C'est la PREMIERE brique du code d'analyse (voir REFERENCE-TECHNIQUE.md, § 09.2) :
elle ne lit aucun fichier, ne trace aucune figure et ne depend que de numpy. Tout le
reste s'appuie dessus :

    mesure Z(f)  ->  ts_fit.py (probleme inverse)  ->  optim.py (filtre sur charge)
                          |                                  |
                          +--------- modele_hp.py -----------+
                              (le meme Z(jw ; theta) partout)

Physique (§ 01.2 a 01.4). Un haut-parleur electrodynamique couple trois domaines. Vu
de ses bornes il se resume a la bobine (R_e en serie avec L_e) PLUS l'image electrique
de la mecanique, dite branche "motionnelle" : la f.e.m. induite Bl*v renvoie cote
electrique l'impedance Z_mot = (Bl)^2 / Z_meca. Comme Z_meca est un RLC SERIE
(R_ms, M_ms, C_ms), son inverse est un RLC PARALLELE : le couplage Bl est un
gyrateur (une masse devient une capacite, un ressort une inductance), et c'est pour
cela que la resonance mecanique se voit comme un MAXIMUM d'impedance.

    Z(jw) = R_e + jw L_e + [ 1/R_es + 1/(jw L_ces) + jw C_mes ]^-1
          = R_e + jw L_e + R_es / (1 + j Q_ms (f/f_s - f_s/f))

Consequence utile au banc : la branche motionnelle est un dipole PASSIF, donc
|Z| >= R_e a toute frequence. Une mesure qui donne |Z| < R_e denonce la chaine de
mesure, pas le haut-parleur (§ 01.3).

Ce que ce modele identifie, et ce qu'il n'identifie pas (§ 01.6). Z(f) ne determine
que CINQ nombres en caisse close : R_e, L_e, R_es, f_s, Q_ms. Les quatre grandeurs
mecaniques (Bl, M_ms, C_ms, R_ms) ne sont PAS identifiables a partir de Z(f) seule :
la famille Bl -> Bl*racine(k), M_ms -> k M_ms, C_ms -> C_ms/k, R_ms -> k R_ms donne
exactement la meme courbe. D'ou le sens unique des conversions offertes ici :
meca_vers_elec existe, l'inverse n'existe pas.

AVERTISSEMENT, a lire avant d'utiliser le moindre nombre de ce fichier : AUCUNE
MESURE N'A ENCORE ETE FAITE SUR L'ENCEINTE DE THOMAS. Les jeux de parametres
SUB_TYP, MED_TYP et JEU_SYNTHETIQUE_V1 sont des ORDRES DE GRANDEUR tires de
datasheets publiques (§ 01.13) ou des jeux de test de methode ; ils servent a
verifier le code, jamais a annoncer un resultat.

Conventions du fichier : tout en SI (henry, farad, hertz, ohm) ; conversion en
mH / uF / deg a l'affichage seulement ; francais sans accents dans le code et les
messages (console cp1252, § 09.4), fichier en UTF-8.

Verification : `python analyse/modele_hp.py` rejoue les nombres de controle des
§ 01.5, 01.8, 01.10, 01.12, 01.13 et 04.4.
"""

import warnings

import numpy as np

# Air a 20 C, 1013 hPa -- ne sert qu'aux conversions de caisse (V_as), jamais a Z(f).
RHO0 = 1.204     # masse volumique de l'air [kg/m3]
C_SON = 343.0    # celerite du son [m/s] -- SEULE definition de c du module.
# Correction de bout d'un event (REFERENCE-TECHNIQUE.md § 01.10 bis fait foi) :
# L_eff = L + k a avec a = d/2. Bout LIBRE 0,6133 a (Levine & Schwinger 1948),
# bout BRIDE 0,8216 a (Rayleigh) a 0,8488 a = 8/(3 pi) (piston bafle).
K_BOUT_DEFAUT = 1.463   # une extremite bridee (dehors) + une libre (dedans)
K_BOUT_MIN = 1.227      # deux extremites libres   (2 x 0,6133)
K_BOUT_MAX = 1.698      # deux extremites bridees  (2 x 0,8488)

# Rapport de compliances V_as/V_b utilise par defaut par Z_bassreflex quand on
# n'ajuste que 7 parametres. Voir la docstring de Z_bassreflex : ce n'est PAS un
# resultat, c'est une hypothese de structure (V_b = V_as) rendue explicite.
ALPHA_STRUCTURE_DEFAUT = 1.0

# Noms des parametres, dans l'ordre du vecteur theta de chaque modele. ts_fit.py et
# les figures s'en servent pour etiqueter les sorties sans les recopier.
NOMS_PARAMETRES = {
    'Z_ts': ('Re', 'Le', 'Res', 'fs', 'Qms'),
    'Z_semi': ('Re', 'K', 'n', 'Res', 'fs', 'Qms'),
    'Z_bassreflex': ('Re', 'Le', 'Res', 'fs', 'Qms', 'fb', 'Ql'),
    'Z_bassreflex8': ('Re', 'Le', 'Res', 'fs', 'Qms', 'alpha', 'fb', 'Ql'),
    'Z_bassreflex_semi': ('Re', 'K', 'n', 'Res', 'fs', 'Qms', 'fb', 'Ql'),
    'Z_deux_pics': ('Re', 'Le', 'R1', 'f1', 'Q1', 'R2', 'f2', 'Q2'),
}


# =====================================================================
# 1. FORMULES DE PASSAGE (mecanique <-> electrique <-> Thiele-Small)
# =====================================================================

def meca_vers_elec(Bl, Mms, Cms, Rms):
    """Parametres mecaniques -> elements de la branche motionnelle (§ 01.3).

    Le gyrateur Bl transforme la serie mecanique en parallele electrique :

        R_es  = (Bl)^2 / R_ms     pertes mecaniques   -> resistance
        L_ces = (Bl)^2 * C_ms     ressort (souplesse) -> inductance
        C_mes = M_ms / (Bl)^2     masse mobile        -> capacite

    Controle dimensionnel (§ 01.3) : (N/A)^2 / (N.s/m) = W/A^2 = ohm ;
    (N/A)^2 * (m/N) = J/A^2 = H ; kg.A^2/N^2 = F. Les trois sont homogenes.

    L'application reciproque N'EXISTE PAS : trois nombres electriques pour quatre
    inconnues mecaniques (§ 01.6). Il faut une seconde manip (masse ajoutee ou
    volume clos connu) pour lever la degenerescence.

    Retourne (Res [ohm], Lces [H], Cmes [F]).
    """
    return Bl**2 / Rms, Bl**2 * Cms, Mms / Bl**2


def rlc_vers_ts(Res, Lces, Cmes):
    """(R_es, L_ces, C_mes) -> (f_s, Q_ms), § 01.4.

        f_s  = 1/(2 pi racine(L_ces C_mes))
        Q_ms = R_es racine(C_mes / L_ces)

    C'est la parametrisation retenue pour l'ajustement : chaque parametre se LIT
    sur la courbe (f_s = position du pic, Q_ms = finesse du pic) et les ordres de
    grandeur restent comparables, ce qui conditionne bien la jacobienne (§ 03.1).
    """
    fs = 1.0 / (2 * np.pi * np.sqrt(Lces * Cmes))
    Qms = Res * np.sqrt(Cmes / Lces)
    return fs, Qms


def ts_vers_rlc(Res, fs, Qms):
    """(R_es, f_s, Q_ms) -> (L_ces, C_mes) : la reciproque exacte de rlc_vers_ts.

        L_ces = R_es / (w_s Q_ms)        C_mes = Q_ms / (w_s R_es)

    Utile des qu'on doit brancher quelque chose EN PARALLELE de la branche
    motionnelle (caisse, event : voir Z_bassreflex), parce que la forme compacte
    R_es/(1 + j Q_ms x) ne montre plus ou est le ressort et ou est la masse.
    """
    ws = 2 * np.pi * fs
    return Res / (ws * Qms), Qms / (ws * Res)


def facteurs_qualite(Re, Res, Qms):
    """(Q_es, Q_ts) a partir de R_e, R_es et Q_ms (§ 01.4).

        Q_es = Q_ms R_e / R_es        1/Q_ts = 1/Q_ms + 1/Q_es

    Q_ms ne contient que les pertes mecaniques ; Q_es decrit l'amortissement
    ELECTRIQUE, celui qu'apporte la f.e.m. induite en debitant dans R_e -- et dans
    tout ce qui est en serie avec elle : DCR de la self du filtre, cable, impedance
    de sortie de l'ampli. C'est la raison physique du terme "DCR" de la fonction de
    cout de l'acte 3 : 1 ohm de DCR relache l'amortissement du grave de ~20 %
    (§ 01.4), en plus de dissiper 11 % de la puissance.
    """
    Qes = Qms * Re / Res
    return Qes, Qms * Qes / (Qms + Qes)


def module_max_theorique(Re, Qms, Qes):
    """|Z|max = R_e (1 + Q_ms/Q_es) = R_e + R_es, hauteur du pic a f_s (§ 01.4).

    Valable si w_s L_e << R_e + R_es -- la condition porte bien sur R_e + R_es et
    non sur R_e seul, puisque a la resonance la branche motionnelle vaut R_es
    (reelle) : |Z(f_s)| = racine((R_e+R_es)^2 + (w_s L_e)^2). Sur le jeu du § 01.5,
    w_s L_e = 0,37 ohm contre 101 ohm : erreur relative 7e-6.

    Piege signale au § 01.13 : l'egalite n'est vraie QUE si l'on injecte le meme
    Q_es des deux cotes. Une datasheet dont le Q_es n'est pas coherent avec
    (Bl, R_e, M_ms, f_s) donne deux valeurs differentes -- ecart constate jusqu'a
    5 a 12 % sur une fiche du commerce.
    """
    return Re * (1.0 + Qms / Qes)


def caisse_close(fs, Qms, Qes, alpha):
    """Effet d'une caisse close : ressort d'air en serie avec la suspension (§ 01.9).

    Avec alpha = V_as/V_b, la compliance totale devient C_ms/(1+alpha), donc sur le
    modele electrique L_ces est DIVISEE par (1+alpha) :

        f_c = f_s racine(1+alpha)      Q_mc = Q_ms racine(1+alpha)
                                       Q_ec = Q_es racine(1+alpha)

    Le pic MONTE en frequence mais garde sa hauteur R_e + R_es (les deux Q sont
    multiplies par le meme facteur, leur rapport ne bouge pas). En pratique
    l'absorbant et les fuites ajoutent des pertes : le pic mesure est plus bas et
    plus large que la formule. Corollaire pour la phase 1 : mesurer un pic PLUS
    HAUT que le f_s de la datasheet n'est pas une erreur de manip, c'est
    racine(1+alpha).

    Retourne (fc, Qmc, Qec, Qtc).
    """
    k = np.sqrt(1.0 + alpha)
    fc, Qmc, Qec = fs * k, Qms * k, Qes * k
    return fc, Qmc, Qec, Qmc * Qec / (Qmc + Qec)


def alpha_depuis_pics(fs, fc):
    """alpha = (f_c/f_s)^2 - 1 : lecture du rapport de compliances sur deux mesures.

    C'est l'une des deux voies pour lever la degenerescence du § 01.6 : si V_b est
    connu (mesure au metre), alpha donne V_as = alpha V_b, donc C_ms, donc Bl et
    M_ms. L'autre voie est la masse ajoutee.
    """
    return (fc / fs) ** 2 - 1.0


def Vas(Sd, Cms):
    """V_as = rho0 c^2 S_d^2 C_ms : volume d'air de meme compliance que la suspension.

    N'intervient pas dans Z(f) en champ libre ; gouverne l'effet de la caisse.
    """
    return RHO0 * C_SON**2 * Sd**2 * Cms


def Res_depuis_Qes(Re, Qms, Qes):
    """R_es = R_e Q_ms / Q_es : sert a reconstruire une datasheet (§ 01.13)."""
    return Re * Qms / Qes


def K_semi_depuis_Le(Le, n, f_ref=1000.0):
    """Calibre K du modele semi-inductif sur le L_e d'une datasheet (§ 01.12).

    Les constructeurs donnent L_e "a 1 kHz" : on impose donc que K(jw)^n ait le
    MEME module que jw L_e a f_ref, soit K = w_ref L_e / w_ref^n. Sans cette
    calibration, comparer les deux modeles n'a aucun sens quantitatif -- ils ne
    decrivent plus le meme haut-parleur.
    """
    w = 2 * np.pi * f_ref
    return w * Le / w**n


# =====================================================================
# 2. MODELES DIRECTS Z(jw ; theta)
# =====================================================================

def Z_ts(f, Re, Le, Res, fs, Qms):
    """Impedance electrique du HP (modele de Thiele-Small a 5 parametres, SI).

    theta = (Re [ohm], Le [H], Res [ohm], fs [Hz], Qms [-]) ; retourne Z complexe.

        Z = R_e + jw L_e + R_es / (1 + j Q_ms (f/f_s - f_s/f))

    La quantite x = f/f_s - f_s/f est le DESACCORD REDUIT : nul a la resonance,
    negatif en dessous (le ressort domine, Z inductive), positif au-dessus (la
    masse domine, Z capacitive). C'est la forme compacte du RLC parallele
    R_es // L_ces // C_mes (identite verifiee a 3e-14 ohm, § 03.1).

    Domaine : f > 0 strictement (le modele est en f/fs - fs/f) et validite
    10-500 Hz ; au-dela, la semi-inductance (courants de Foucault) fait devier Le
    -- utiliser Z_semi (§ 01.12, § 03.6). En caisse close, on identifie (f_c, Q_mc)
    et non (f_s, Q_ms) : c'est la meme fonction, ce sont les parametres qui
    changent de nom (§ 01.9).
    """
    f = np.asarray(f, float)
    if np.any(f <= 0):
        raise ValueError('Z_ts : f doit etre > 0 (modele en f/fs - fs/f)')
    x = f / fs - fs / f                                # desaccord reduit
    return Re + 2j * np.pi * f * Le + Res / (1 + 1j * Qms * x)


def Z_semi(f, Re, K, n, Res, fs, Qms):
    """Variante SEMI-INDUCTIVE a 6 parametres : jw L_e remplace par K (jw)^n.

    Pourquoi. La bobine est bobinee sur une piece polaire ferromagnetique
    CONDUCTRICE : les courants de Foucault induits dissipent de l'energie, donc
    l'impedance de bobine a une PARTIE REELLE croissante que jw L_e n'a pas.
    Vanderkooy (1989) derive physiquement n = 1/2 ; Leach (2002) identifie
    n = 0,6 a 0,7 sur des moteurs reels. Module en w^n, phase constante n*90 deg.

    Ce que cela coute de l'ignorer, et c'est le vrai risque de l'acte 2 : force de
    rendre compte d'un Re(Z) qui monte, un ajustement a L_e constant ABSORBE la
    croissance en gonflant R_e -- le parametre en apparence le mieux determine.
    Biais mesure sur donnees synthetiques K(jw)^0,7 (§ 03.6) : +6,8 % si l'on
    ajuste sur 10-200 Hz, +11,8 % sur 10-500 Hz, +16,3 % sur 10-1000 Hz, soit
    plus de dix ecarts-types. Restreindre la bande ne guerit donc PAS ; le remede
    est ce modele-ci, qui rend n = 0,696 +- 0,005 pour n vrai = 0,700.

    theta = (Re, K [ohm.s^n], n [-], Res, fs, Qms). Calibrer K avec
    K_semi_depuis_Le() pour comparer a un L_e de datasheet.
    """
    f = np.asarray(f, float)
    if np.any(f <= 0):
        raise ValueError('Z_semi : f doit etre > 0')
    x = f / fs - fs / f
    return Re + K * (2j * np.pi * f)**n + Res / (1 + 1j * Qms * x)


def _admittance_event(f, Lces, alpha, fb, Ql):
    """Admittance de la branche caisse + event, vue cote electrique (§ 01.10).

    Cote acoustique, le haut-parleur voit la compliance de caisse C_ab EN
    PARALLELE de la masse d'air de l'event M_ap : le debit de la membrane se
    partage entre comprimer l'air de la caisse et sortir par l'event. Ramenee
    cote electrique par le gyrateur (Y_caisse = S_d^2 Z_ac / (Bl)^2), cette
    impedance acoustique devient une ADMITTANCE, et le parallele acoustique
    devient une branche SERIE electrique qui SHUNTE la branche motionnelle :

        Z_event = R_p + jw L_ceb + 1/(jw C_peb)

        L_ceb = L_ces / alpha          (compliance de caisse, alpha = V_as/V_b)
        C_peb = 1/(w_b^2 L_ceb)        (masse d'air de l'event, accord f_b)
        R_p   = w_b L_ceb / Q_l        (pertes : fuites, absorbant, event)

    Les deux limites se verifient et servent de tests : f_b -> 0 (event inerte,
    masse d'air infinie) redonne EXACTEMENT la caisse close de meme volume
    (L_ces // L_ceb = L_ces/(1+alpha), donc f_c = f_s racine(1+alpha)) ;
    Q_l -> +infini donne les deux pics sans pertes.
    """
    w = 2 * np.pi * np.asarray(f, float)
    wb = 2 * np.pi * fb
    Lceb = Lces / alpha
    Cpeb = 1.0 / (wb**2 * Lceb)
    Rp = wb * Lceb / Ql
    return 1.0 / (Rp + 1j * w * Lceb + 1.0 / (1j * w * Cpeb))


def Z_bassreflex(f, Re, Le, Res, fs, Qms, fb, Ql, alpha=ALPHA_STRUCTURE_DEFAUT):
    """Modele BASS-REFLEX : caisse accordee, DEUX pics et un creux (§ 01.10).

    theta = (Re, Le, Res, fs, Qms, fb, Ql) -- 7 parametres ajustes ; f_s est ici la
    resonance du haut-parleur EN CHAMP LIBRE (la caisse est deja dans le modele,
    via alpha), f_b l'accord de l'event, Q_l le facteur de pertes de la caisse
    (grand Q_l = caisse etanche, pic haut et creux profond ; Q_l ~ 7 a 15 = fuites
    realistes, qui abaissent nettement les deux pics, § 01.10).

    Structure : la branche event (voir _admittance_event) shunte la branche
    motionnelle. A l'accord, la membrane bouge peu -- c'est l'event qui rayonne --
    donc la f.e.m. induite s'effondre et |Z| retombe pres de R_e : c'est le CREUX,
    situe a f_b. Les deux pics l'encadrent, et ce n'est pas une constatation mais
    un resultat : en posant x = (w/w_s)^2 et beta = (f_b/f_s)^2, l'annulation de
    l'impedance mecanique donne x^2 - (1 + alpha + beta) x + beta = 0, d'ou par
    les relations racines-coefficients

        f_L f_H = f_s f_b        f_L^2 + f_H^2 = f_s^2 (1+alpha) + f_b^2

    et p(beta) = -alpha beta < 0, donc f_L < f_b < f_H toujours.

    ATTENTION -- alpha n'est PAS un parametre libre ici, et c'est une decision de
    modelisation a assumer devant le jury. Z(f) d'un bass-reflex depend de TROIS
    nombres de caisse (alpha, f_b, Q_l) et non de deux : le compte honnete est
    8 parametres (§ 01.6). Le contrat du code fixe le vecteur ajuste a 7, donc
    alpha est ici une HYPOTHESE DE STRUCTURE explicite (defaut 1,0, c.-a-d.
    V_b = V_as). Pour l'ajuster vraiment, utiliser Z_bassreflex8, dont le vecteur
    est (Re, Le, Res, fs, Qms, alpha, fb, Ql) -- c'est la meme fonction.
    """
    f = np.asarray(f, float)
    if np.any(f <= 0):
        raise ValueError('Z_bassreflex : f doit etre > 0')
    Lces, _ = ts_vers_rlc(Res, fs, Qms)
    x = f / fs - fs / f
    Y = (1 + 1j * Qms * x) / Res + _admittance_event(f, Lces, alpha, fb, Ql)
    return Re + 2j * np.pi * f * Le + 1.0 / Y


def Z_bassreflex8(f, Re, Le, Res, fs, Qms, alpha, fb, Ql):
    """Meme modele, alpha LIBRE : les 8 parametres du § 01.6, dans l'ordre du nom.

    A preferer des que la mesure montre deux pics : c'est leur ECARTEMENT qui
    porte alpha (f_L^2 + f_H^2 = f_s^2 (1+alpha) + f_b^2), donc alpha y est
    identifiable -- le figer serait s'interdire de lire ce que la courbe dit.
    """
    return Z_bassreflex(f, Re, Le, Res, fs, Qms, fb, Ql, alpha=alpha)


def Z_bassreflex_semi(f, Re, K, n, Res, fs, Qms, fb, Ql,
                      alpha=ALPHA_STRUCTURE_DEFAUT):
    """Bass-reflex + bobine a pertes : 8 parametres (les 7 du BR, L_e -> K, n).

    C'est le cumul des deux replis : deux pics EN BAS de bande, semi-inductance EN
    HAUT. A n'utiliser que si les residus des deux modeles simples le reclament
    (s^2 > 2 et residus structures) -- huit parametres sur une courbe bruitee,
    cela se justifie, cela ne se suppose pas.
    """
    f = np.asarray(f, float)
    if np.any(f <= 0):
        raise ValueError('Z_bassreflex_semi : f doit etre > 0')
    Lces, _ = ts_vers_rlc(Res, fs, Qms)
    x = f / fs - fs / f
    Y = (1 + 1j * Qms * x) / Res + _admittance_event(f, Lces, alpha, fb, Ql)
    return Re + K * (2j * np.pi * f)**n + 1.0 / Y


def Z_deux_pics(f, Re, Le, R1, f1, Q1, R2, f2, Q2):
    """Repli PHENOMENOLOGIQUE a 8 parametres : deux resonances en serie (§ 03.1).

    Il decrit deux pics sans pretendre nommer f_b, alpha ni Q_l -- suffisant pour
    l'acte 3, qui ne voit que Z(f), mais il ne dit rien de la caisse. A reserver
    au cas ou le modele physique Z_bassreflex8 ne converge pas, ou pour un BLOC de
    deux haut-parleurs mal apparies (deux f_s distincts, § 01.12) : dans ce
    dernier cas les deux resonances sont deux moteurs, pas une caisse accordee.
    """
    f = np.asarray(f, float)
    if np.any(f <= 0):
        raise ValueError('Z_deux_pics : f doit etre > 0')
    return (Re + 2j * np.pi * f * Le
            + R1 / (1 + 1j * Q1 * (f / f1 - f1 / f))
            + R2 / (1 + 1j * Q2 * (f / f2 - f2 / f)))


def Z_serie_2hp(f, theta_a, theta_b):
    """Deux haut-parleurs EN SERIE (le bloc medium : 2 x 4 ohm = 8 ohm).

    theta_a, theta_b : deux vecteurs a 5 parametres (modele Z_ts). Les impedances
    s'ajoutent. Si les deux HP sont identiques, Z double sans changer de forme ;
    s'ils ne sont pas apparies, la somme montre deux pics distincts -- ecartes de
    17 Hz pour 10 % d'ecart sur f_s, de 8 Hz pour 5 % (§ 01.12), d'ou la consigne
    de mesure au 1/24 d'octave (ou 1 Hz lineaire) sur 60-110 Hz.

    Strategie tranchee pour l'acte 2 (§ 03.1) : le bloc est d'abord identifie
    comme UN SEUL dipole a 5 parametres, parce que c'est tout ce dont le
    passe-haut a besoin. Cette fonction sert a fabriquer le cas de test et a
    verifier la coherence (R_e et L_e du bloc ~ deux fois ceux d'un medium seul).
    """
    return Z_ts(f, *theta_a) + Z_ts(f, *theta_b)


def Z_charge_passe_haut(f, theta_medium, n_medium=2, R_aigu=None, C_aigu=None,
                        n_aigu=2, C_commun=None):
    """Charge COMPOSITE reellement vue par le passe-haut (§ 01.12, constat du 2026-09-16).

    L'enceinte ne porte pas deux voies mais trois familles de transducteurs : le
    18 pouces, les DEUX mediums cables en serie, et DEUX pavillons d'ultra-aigu
    cables EN PARALLELE du bloc medium. Les pavillons sont hors perimetre
    ACOUSTIQUE -- ils ne rayonnent rien a 100 Hz -- mais ils ne sont PAS hors
    perimetre ELECTRIQUE : etant en parallele, ils font partie de la charge que
    le passe-haut doit entrainer. Confondre les deux plans, c'est optimiser un
    filtre sur une charge qui n'existe pas.

        Z = (n_medium HP en SERIE)  //  (branche aigu)

        branche aigu = [ n_aigu x (R_aigu + 1/(jw C_aigu)) en parallele ]
                       + 1/(jw C_commun)

    LES DEUX CABLAGES POSSIBLES, ET POURQUOI ON NE TRANCHE PAS ICI. La presence
    d'un condensateur de protection en serie avec les pavillons est un CONSTAT A
    FAIRE, pas une hypothese a poser : [[a verifier aupres de l'etudiant]]. Le
    verdict ne se devine pas, il se calcule -- et il depend de |Z| DU BLOC
    MEDIUM a 100 Hz, ce que l'on oublie en repetant "un condensateur, c'est un
    circuit ouvert en bas". Sur les ordres de grandeur etiquetes MED_TYP (deux
    8 pouces en serie, pic a 80 Hz), a 100 Hz, deux pavillons de 8 ohm :
      * AVEC condensateur (protection du premier ordre, 3 a 10 uF) : la branche
        vaut 4 - j117 ohm pour 6,8 uF, soit |Z| = 117 ohm -- grand, mais pas
        devant les 29 ohm du bloc medium au voisinage de SA resonance. Resultat :
        |Z| du bloc passe de 29,3 a 23,7 ohm, soit -19 %. Ce n'est PAS
        negligeable, contrairement a l'intuition courante ; ce n'est pas non plus
        redhibitoire, et cela s'ajuste comme le reste ;
      * SANS condensateur : la branche est un simple 4 ohm en parallele direct.
        |Z| du bloc tombe de 29,3 a 3,7 ohm (-87 %), c'est-a-dire SOUS le minimum
        de 4 ohm du t.amp E-800 une fois le filtre autour -- et les pavillons
        recoivent du 100 Hz a pleine puissance, ce qui est un risque MATERIEL
        pendant les balayages, pas seulement une erreur de modele.
    Passer C_aigu=None modelise le second cas ; c'est le seul reglage qui demande
    une decision, et il est explicite dans la signature. Le chiffrage complet est
    rendu par effet_branche_aigu().

    LA CONSEQUENCE PRATIQUE EST LA MEME DANS LES DEUX CAS : on mesure le bloc
    medium TEL QU'IL EST CABLE, pavillons connectes, puisque c'est cela que le
    filtre voit. Cette fonction ne sert donc pas a remplacer la mesure mais a
    CHIFFRER l'enjeu avant de la faire (voir effet_branche_aigu).

    R_aigu : un moteur a compression est modelise ici par une simple resistance.
    C'est une approximation ASSUMEE et valable dans la seule bande qui nous
    interesse : sa propre resonance vit vers 500-1500 Hz, donc a 100 Hz, deux a
    quatre octaves dessous, |Z| y est proche de R_e (l'inductance de sa bobine,
    quelques dizaines de uH, vaut moins de 0,05 ohm a 100 Hz). Hors bande de
    raccord, ce modele ne vaut rien -- et il n'a pas a valoir.

    theta_medium : vecteur a 5 parametres d'UN medium (Z_ts), ou une sequence de
    vecteurs si les HP ne sont pas apparies (ils sont alors sommes tels quels et
    n_medium est ignore). R_aigu=None retire la branche aigu : on retrouve
    exactement n_medium x Z_ts, c'est-a-dire l'ancienne modelisation.
    """
    f = np.asarray(f, float)
    if np.any(f <= 0):
        raise ValueError('Z_charge_passe_haut : f doit etre > 0')
    theta = np.asarray(theta_medium, float)
    if theta.ndim == 1:
        Z_med = int(n_medium) * Z_ts(f, *theta)          # HP identiques, en serie
    else:
        Z_med = sum(Z_ts(f, *t) for t in theta)          # HP quelconques, en serie
    if R_aigu is None:
        return Z_med

    w = 2 * np.pi * f
    Z_un = np.full(f.shape, complex(float(R_aigu)))
    if C_aigu is not None:
        Z_un = Z_un + 1.0 / (1j * w * float(C_aigu))
    n_aigu = max(int(n_aigu), 1)
    Z_aigu = Z_un / n_aigu                               # n branches identiques //
    if C_commun is not None:
        Z_aigu = Z_aigu + 1.0 / (1j * w * float(C_commun))
    return 1.0 / (1.0 / Z_med + 1.0 / Z_aigu)


def effet_branche_aigu(theta_medium, f_ref=100.0, n_medium=2, R_aigu=8.0,
                       C_aigu=6.8e-6, n_aigu=2):
    """Chiffre, a f_ref, ce que la branche aigu change a |Z| du bloc medium.

    Rend un dict : |Z| du bloc SEUL, |Z| avec les pavillons ET leur condensateur,
    |Z| avec les pavillons SANS condensateur, et les deux ecarts relatifs. C'est
    le nombre qui dit a l'etudiant si la question du condensateur est CRITIQUE ou
    SECONDAIRE -- et il vaut mieux le calculer avant la seance que le decouvrir
    dessus. Aucune mesure n'entre ici : c'est un modele sur des ordres de
    grandeur etiquetes.
    """
    f = np.array([float(f_ref)])
    z_seul = float(np.abs(Z_charge_passe_haut(f, theta_medium, n_medium,
                                              R_aigu=None))[0])
    z_avec = float(np.abs(Z_charge_passe_haut(f, theta_medium, n_medium, R_aigu,
                                              C_aigu, n_aigu))[0])
    z_sans = float(np.abs(Z_charge_passe_haut(f, theta_medium, n_medium, R_aigu,
                                              None, n_aigu))[0])
    z_branche = float(np.abs(
        float(R_aigu) + (0.0 if C_aigu is None
                         else 1.0 / (2j * np.pi * float(f_ref) * float(C_aigu)))
    )) / max(int(n_aigu), 1)
    return dict(f_Hz=float(f_ref), module_bloc_seul=z_seul,
                module_avec_condensateur=z_avec, module_sans_condensateur=z_sans,
                ecart_avec_pct=100.0 * (z_avec / z_seul - 1.0),
                ecart_sans_pct=100.0 * (z_sans / z_seul - 1.0),
                module_branche_aigu=z_branche,
                rapport_branche_sur_bloc=z_branche / z_seul,
                Z_condensateur_ohm=(None if C_aigu is None
                                    else 1.0 / (2 * np.pi * float(f_ref) * C_aigu)))


def Z_depuis_jeu(f, jeu):
    """Z(f) a partir d'un dictionnaire de parametres (SUB_TYP, MED_TYP, ...).

    Aiguillage sur la cle 'modele' : 'clos' -> Z_ts, 'semi' -> Z_semi,
    'bassreflex' -> Z_bassreflex8. Les cles descriptives ('nom', 'source',
    'avertissement', ...) sont ignorees. C'est le raccourci que filtre.py et
    optim.py utilisent pour obtenir une charge de demonstration en une ligne.
    """
    modele = jeu.get('modele', 'clos')
    if modele == 'clos':
        cles = ('Re', 'Le', 'Res', 'fs', 'Qms')
        return Z_ts(f, *[jeu[c] for c in cles])
    if modele == 'semi':
        cles = ('Re', 'K', 'n', 'Res', 'fs', 'Qms')
        return Z_semi(f, *[jeu[c] for c in cles])
    if modele == 'bassreflex':
        cles = ('Re', 'Le', 'Res', 'fs', 'Qms', 'alpha', 'fb', 'Ql')
        return Z_bassreflex8(f, *[jeu[c] for c in cles])
    raise ValueError("Z_depuis_jeu : modele inconnu '%s' "
                     "(attendu 'clos', 'semi' ou 'bassreflex')" % modele)


# =====================================================================
# 3. RESEAUX DE CORRECTION DE LA CHARGE (§ 04.4)
# =====================================================================

def zobel(Z, f, Rz, Cz):
    """Ajoute un reseau de Zobel (R_z + C_z serie) EN PARALLELE sur le dipole.

    Z est l'impedance du haut-parleur deja calculee sur la grille f (c'est la
    signature gelee du § 09.4 : on corrige une charge, on ne recalcule pas un
    modele). Retourne l'impedance vue par le filtre.

    Avec R_z = R_e et C_z = L_e/R_e^2 (voir zobel_ideal), la partie inductive est
    annulee EXACTEMENT a toute frequence : (R_e + jw L_e) // (R_z + 1/jw C_z) =
    R_e (verifie a 3e-15 ohm sur 10 Hz - 10 kHz). Mais le Zobel ne corrige PAS le
    pic motionnel, qui est le vrai probleme au raccord : sur le jeu illustratif,
    il fait passer 14,1 ohm a 11,6 ohm a 100 Hz (et degrade meme la phase,
    -47 deg -> -54 deg) alors qu'il ramene 9,2 ohm / 45 deg a 6,1 ohm / 0 deg a
    1 kHz. C'est la reponse a l'objection "pourquoi pas simplement un Zobel ?".
    """
    w = 2 * np.pi * np.asarray(f, float)
    Zz = Rz + 1.0 / (1j * w * Cz)
    return Z * Zz / (Z + Zz)


def zobel_ideal(Re, Le):
    """Valeurs qui annulent exactement jw L_e : (R_z, C_z) = (R_e, L_e/R_e^2).

    Rappel du § 04.5 : ces valeurs sont optimales pour ANNULER l'inductance, pas
    pour minimiser la fonction de cout du filtre -- si un Zobel est retenu, ses
    deux valeurs entrent dans l'optimisation comme les autres.
    """
    return Re, Le / Re**2


def compensation_rlc(Re, Res, fs, Qms):
    """Reseau qui linearise le PIC motionnel : RLC serie accorde sur f_s (§ 04.4).

    On cherche Z_c tel que (R_e + Z_mot) // Z_c = R_e, soit
    Z_c = R_e + R_e^2 Y_mot : c'est un RLC serie de

        R_c = R_e + R_e^2/R_es      L_c = C_mes R_e^2      C_c = L_ces/R_e^2

    (homogeneite : F.ohm^2 = H et H/ohm^2 = F), accorde sur 1/(2 pi racine(L_c C_c))
    = f_s. Il linearise parfaitement (7e-15 ohm hors L_e) -- et c'est precisement
    pour cela qu'il est ecarte : a 100 Hz il demande un condensateur de 2,4 mF
    sous plus de 250 V crete, et a la resonance la resistance dissipe ~375 W quand
    le haut-parleur n'en recoit que 55. Ce n'est pas un paradoxe : le reseau
    absorbe exactement ce que le HP cesse d'absorber quand il resonne. Cout et
    matiere x2 a x3 : l'inverse du theme "sobriete", d'ou la voie v2 (laisser Z(f)
    tel quel et optimiser le filtre dessus).

    Retourne (Rc [ohm], Lc [H], Cc [F]).
    """
    Lces, Cmes = ts_vers_rlc(Res, fs, Qms)
    return Re + Re**2 / Res, Cmes * Re**2, Lces / Re**2


# =====================================================================
# 4. CAISSE BASS-REFLEX : GEOMETRIE DES EVENTS ET CHAMP PROCHE
# =====================================================================
# Cette section est la seule du module qui parle d'ACOUSTIQUE et non
# d'impedance electrique. Elle existe parce que le constat du 2026-09-16 --
# le sub est en bass-reflex, avec DEUX events -- ouvre une PREDICTION
# FALSIFIABLE : la geometrie de la caisse donne f_b par le resonateur de
# Helmholtz, l'ajustement de Z(f) donne f_b par le probleme inverse, et rien
# n'oblige les deux a tomber ensemble. Confronter deux chemins independants
# vers le meme nombre vaut mieux que mesurer deux fois par le meme chemin :
# c'est ce qui distingue une verification d'une repetition.

def frequence_accord_helmholtz(volume_caisse_L, n_events, diametre_event_mm,
                               longueur_event_mm, k_correction=K_BOUT_DEFAUT, c=C_SON,
                               detail=False):
    """f_b PREDITE par la geometrie : resonateur de Helmholtz a N events (§ 01.10).

    PHYSIQUE. La caisse close est un RESSORT d'air (raideur de compression du
    volume V) et la colonne d'air des events une MASSE (elle est poussee en bloc,
    sans etre comprimee, tant que la longueur d'onde est tres grande devant les
    dimensions). Ressort + masse = oscillateur, et sa frequence propre est

        f_b = (c / 2 pi) racine( S_tot / (V L_eff) )

    avec S_tot = N pi d^2/4 l'aire TOTALE des events et L_eff leur longueur
    EFFECTIVE. La demonstration tient en deux lignes : la masse acoustique d'un
    conduit est M_a = rho0 L_eff / S_tot, la compliance du volume est
    C_a = V/(rho0 c^2), et f_b = 1/(2 pi racine(M_a C_a)) donne l'expression
    ci-dessus -- rho0 disparait, ce qui explique qu'une caisse ne se desaccorde
    pas en changeant d'altitude autant qu'on le croit.

    N events IDENTIQUES : leurs masses acoustiques sont en PARALLELE (le meme
    ecart de pression les traverse), donc la masse totale est divisee par N.
    C'est pour cela que N entre au numerateur via S_tot et non ailleurs :
    doubler le nombre d'events monte f_b d'un facteur racine(2), pas de 2.

    CORRECTION DE BOUT, ET LA CONVENTION RETENUE. Un tube court "entraine" de
    l'air au-dela de ses deux extremites : la masse en mouvement est plus grande
    que rho0 L/S, donc L_eff > L. On ecrit

        L_eff = L + k a        avec a = d/2 le RAYON de l'event

    et le coefficient k est la SOMME des deux corrections d'extremite, chacune
    valant k_a a selon ce que cette extremite-la voit :
      * extremite LIBRE (unflanged), tube debouchant dans un volume : 0,6133 a
        (Levine & Schwinger 1948, limite basse frequence exacte) ;
      * extremite BRIDEE (flanged), affleurant un grand plan : 0,8216 a
        (Rayleigh), ou 0,8488 a = 8/(3 pi) dans l'approximation du piston bafle.
    CONVENTION PAR DEFAUT ICI, et elle fait foi dans tout le projet
    (REFERENCE-TECHNIQUE.md § 01.10 bis) : k = 1,463, c'est-a-dire une extremite
    BRIDEE dehors (l'event affleure le baffle) et une extremite LIBRE dedans (il
    debouche dans le volume). C'est la configuration ordinaire d'un event de
    caisse, et 1,463 est aussi la constante de la formule de longueur d'event de
    toute la litterature haut-parleur (Small 1973 ; Dickason), ce qui rend nos
    chiffres comparables aux siens.

    CE QUE CETTE INCERTITUDE DE CONVENTION COUTE, ET POURQUOI ON LA DIT. Les
    extremites reelles ne sont ni parfaitement bridees ni parfaitement libres :
    un event peut deboucher pres d'une paroi ou de son voisin, ce qui le bride
    en pratique. On transporte donc l'encadrement COMPLET k dans [1,227 ; 1,698]
    (deux bouts libres -> deux bouts brides), soit quelques pour cent sur f_b :
    la prediction geometrique n'est PAS a la virgule pres, et l'annoncer comme
    telle serait malhonnete. detail=True rend cet encadrement en meme temps que
    la valeur : c'est ce couple, et non un nombre seul, qui se compare au f_b
    ajuste sur Z(f).

    LIMITES A CONNAITRE AVANT DE CRIER AU DESACCORD (toutes vont dans le meme
    sens : f_b reel plus BAS que predit) : le volume occupe par le haut-parleur,
    par les events eux-memes et par l'eventuel absorbant reduit V utile ; deux
    events voisins se "voient" et leur correction de bout mutuelle augmente
    L_eff ; l'absorbant rend la compression partiellement isotherme. Un ecart de
    5 a 10 % entre geometrie et ajustement est donc ATTENDU et ne disqualifie ni
    l'un ni l'autre. Un ecart de 30 % denonce une erreur de mesure ou de saisie.

    Arguments : volume de la caisse en LITRES, nombre d'events, diametre et
    longueur d'UN event en MILLIMETRES (unites du metre-ruban, pas du SI --
    c'est la fonction qui convertit, pas l'etudiant a 23 h). Rend f_b en Hz, ou
    un dict si detail=True.
    """
    V = float(volume_caisse_L) * 1e-3                    # litres -> m3
    d = float(diametre_event_mm) * 1e-3                  # mm -> m
    L = float(longueur_event_mm) * 1e-3
    N = int(n_events)
    if V <= 0 or d <= 0 or L < 0 or N < 1:
        raise ValueError('frequence_accord_helmholtz : volume, diametre et nombre '
                         "d'events doivent etre > 0 et la longueur >= 0")
    S_un = np.pi * d**2 / 4.0
    S_tot = N * S_un
    L_eff = L + float(k_correction) * d / 2.0
    fb = float(c) / (2 * np.pi) * np.sqrt(S_tot / (V * L_eff))
    if not detail:
        return float(fb)

    def _fb(k):
        return float(c) / (2 * np.pi) * np.sqrt(S_tot / (V * (L + k * d / 2.0)))

    encadrement = sorted((_fb(K_BOUT_MIN), _fb(K_BOUT_MAX)))
    return dict(fb_Hz=float(fb), S_event_m2=float(S_un), S_totale_m2=float(S_tot),
                L_effective_m=float(L_eff), L_physique_m=float(L),
                correction_de_bout_m=float(k_correction) * d / 2.0,
                k_correction=float(k_correction), n_events=N,
                volume_m3=float(V),
                fb_encadrement_Hz=(float(encadrement[0]), float(encadrement[1])),
                convention=('L_eff = L + k a, a = d/2 ; k = 0,6133 par extremite '
                            'LIBRE, 0,8216 a 0,8488 par extremite BRIDEE ; defaut '
                            'k = 1,463 = une bridee (dehors) + une libre (dedans), '
                            'convention du projet ; encadrement transporte '
                            '[1,227 ; 1,698] = deux libres a deux bridees'),
                avertissement=('PREDICTION geometrique, pas une mesure. V utile, '
                               'interaction entre events voisins et absorbant '
                               'abaissent f_b : 5 a 10 % d ecart avec le f_b '
                               'ajuste sur Z(f) est attendu.'))


def somme_champ_proche_bassreflex(p_membrane, p_events, Sd_m2, S_event_m2,
                                  n_events=1):
    """Pression totale d'un bass-reflex reconstituee en CHAMP PROCHE (Keele, 1974).

    POURQUOI ON NE PEUT PAS MESURER AUTREMENT A 100 Hz (§ 02.10). A 100 Hz la
    longueur d'onde vaut 3,4 m : dans une piece ordinaire les modes propres
    imposent des ecarts de plus de 10 dB selon l'endroit du micro, et le
    fenetrage temporel -- le remede habituel -- est inoperant, puisqu'isoler le
    direct demanderait une fenetre plus courte qu'une periode. Le champ proche
    contourne l'obstacle : a quelques millimetres de la membrane, le direct
    ecrase le reverbere de 30 a 40 dB, et la mesure redevient celle du
    haut-parleur et non celle de la piece.

    MAIS un bass-reflex a DEUX sources : la membrane et le(s) event(s). En
    dessous de f_b elles sont en OPPOSITION de phase (c'est meme la definition de
    l'accord : l'event prend le relais et la membrane se bloque), donc mesurer la
    seule membrane rend une courbe qui n'existe nulle part. Il faut sommer -- et
    surtout, sommer avec la BONNE ponderation.

    LA PONDERATION, ET SA DEMONSTRATION (c'est le coeur de la methode). En champ
    proche, sur l'axe d'un piston de rayon a, la pression vaut
    p_pp = 2 rho0 c u sin(k a / 2) ~ rho0 omega u a a basse frequence, alors que
    le champ lointain ne depend que du DEBIT U = S u :
    p_loin = rho0 omega U / (2 pi r). En eliminant u entre les deux :

        U  proportionnel a  p_pp x a          (a = rayon de la source)

    donc le debit total est proportionnel a (p_D a_D + somme_i p_i a_i) et la
    reponse du systeme se reconstruit, ramenee a l'echelle de la membrane, par

        p_total = p_membrane + somme_i racine(S_i / S_d) x p_i

    puisque a_i/a_D = racine(S_i/S_d). LA PONDERATION EST DONC EN RACINE DES
    AIRES, c'est-a-dire en RAYONS -- pas en aires. C'est l'erreur classique : un
    event de 100 mm devant une membrane de S_d = 0,1190 m2 (diametre equivalent
    389 mm -- le S_d employe par l'auto-test) pese 0,2569 et non 0,0660, soit
    11,8 dB d'ecart sur sa contribution. Le calcul ci-dessus, fait une fois, evite
    de la commettre a 23 h la veille du depot.

    DEUX POINTS DE MANIP QUI RENDENT LA SOMME FAUSSE S'ILS SONT RATES :
      * il faut sommer des COMPLEXES (module ET phase), avec la MEME reference de
        temps pour toutes les acquisitions -- typiquement la meme boucle de
        mesure sans toucher au routage. Sommer des modules donne une courbe
        toujours trop haute autour de f_b, precisement la ou tout se joue ;
      * meme micro, meme gain, meme distance a la source, et le micro au CENTRE
        de la membrane / dans le plan de la bouche de l'event.

    ARGUMENTS. p_membrane : pression complexe relevee au centre de la membrane
    (tableau, une valeur par frequence). p_events : soit UN tableau (un seul
    event releve ; on suppose alors les N events identiques et en phase, d'ou le
    facteur n_events), soit une sequence de N tableaux (chaque event releve, ce
    qui est preferable -- deux events ne debitent pas forcement pareil). Sd_m2 :
    aire EFFECTIVE de la membrane (celle de la datasheet, S_d ; pas pi d^2/4 sur
    le diametre exterieur du saladier). S_event_m2 : aire geometrique d'un event,
    ou une sequence si les events different.

    Rend la pression complexe totale, a l'echelle du champ proche de la membrane.
    Ce n'est PAS un niveau absolu : c'est une reponse en frequence relative, la
    seule chose dont l'acte 4 ait besoin pour juger une somme a +-1 dB.
    """
    p_D = np.asarray(p_membrane, dtype=complex)
    Sd = float(Sd_m2)
    if Sd <= 0:
        raise ValueError('somme_champ_proche_bassreflex : S_d doit etre > 0')

    liste_p = ([np.asarray(p, dtype=complex) for p in p_events]
               if isinstance(p_events, (list, tuple))
               else [np.asarray(p_events, dtype=complex)] * max(int(n_events), 1))
    aires = (list(S_event_m2) if isinstance(S_event_m2, (list, tuple, np.ndarray))
             else [float(S_event_m2)] * len(liste_p))
    if len(aires) != len(liste_p):
        raise ValueError('somme_champ_proche_bassreflex : %d event(s) mais %d aire(s)'
                         % (len(liste_p), len(aires)))

    total = p_D.astype(complex).copy()
    for p_i, S_i in zip(liste_p, aires):
        if float(S_i) <= 0:
            raise ValueError('somme_champ_proche_bassreflex : aire d event <= 0')
        if p_i.shape != p_D.shape:
            raise ValueError('somme_champ_proche_bassreflex : les tableaux de '
                             'pression doivent avoir la meme taille que la membrane')
        total = total + np.sqrt(float(S_i) / Sd) * p_i
    return total


# =====================================================================
# 5. GRILLES DE FREQUENCES (§ 02.6)
# =====================================================================

def _grille_geometrique(f1, f2, n_par_octave):
    """Grille geometrique dont les DEUX bornes sont exactement f1 et f2.

    On arrondit le nombre d'intervalles, le pas vaut donc environ
    1/n_par_octave d'octave. Borner exactement est ce qui permet d'annoncer
    "10 Hz - 1 kHz, exactement deux decades" (porte de validation du § 02.8).
    """
    if not (f1 > 0 and f2 > f1):
        raise ValueError('grille : il faut 0 < f1 < f2')
    n = max(1, int(round(np.log2(f2 / f1) * n_par_octave)))
    return f1 * (f2 / f1) ** (np.arange(n + 1) / n)


def grille_log(f1, f2, n_par_octave=12, densifier=None):
    """Grille logarithmique, avec resserrement optionnel autour du pic.

    densifier = (f_bas, f_haut, n_par_octave_local) ajoute une grille plus fine sur
    la sous-bande [f_bas, f_haut] (bornee a [f1, f2]) et fusionne sans doublon.
    Valeur RECOMMANDEE : (fs/2, 2*fs, 24) -- elle ne peut pas etre une valeur par
    defaut puisqu'elle depend de f_s, qu'on ne connait qu'apres la passe 1.

    Pourquoi resserrer, chiffre (§ 02.6, § 01.9, § 03.4 test E). La largeur du pic
    vaut f_2 - f_1 = f_s racine(r_0)/Q_ms : 64 Hz pour Q_ms = 1,75, mais 14 Hz
    seulement pour Q_ms = 8 -- valeur plausible d'un 18 pouces de sono -- soit
    6 points au 1/12 d'octave. Or c'est le pic qui porte TOUTE l'information sur
    f_s, Q_ms et Q_es. Densifier au 1/24 fait passer l'erreur d'identification de
    2,6 % a 0,9 % pour une vingtaine de points de plus, soit dix minutes de banc :
    c'est l'argument "efficacite" du TIPE applique au protocole lui-meme.

    Divers : eviter 50 et 100 Hz exacts (residu secteur) ; la grille 1/12 issue de
    10 Hz tombe a 50,4 et 100,8 Hz, ce qui convient.
    """
    f = _grille_geometrique(f1, f2, n_par_octave)
    if densifier is not None:
        fa, fb, npo = densifier
        fa, fb = max(float(fa), f1), min(float(fb), f2)
        if fb > fa:
            f = np.concatenate([f, _grille_geometrique(fa, fb, npo)])
    return _unifier(f)


def _unifier(f, tol_relative=1e-9):
    """Trie et supprime les doublons a tol_relative pres (fusion de deux grilles)."""
    f = np.sort(np.asarray(f, float))
    garder = np.ones(f.size, bool)
    garder[1:] = np.diff(f) > tol_relative * f[:-1]
    return f[garder]


# =====================================================================
# 6. LECTURE D'UNE COURBE |Z| : pic, creux, diagnostic de caisse
# =====================================================================

def _module(Z):
    """Accepte indifferemment une impedance complexe ou un module deja calcule."""
    Z = np.asarray(Z)
    return np.abs(Z) if np.iscomplexobj(Z) else Z.astype(float)


def _moyenne_glissante(y, n):
    """Moyenne glissante sur n points, bords conserves (lissage du § 03.7).

    Le lissage est INDISPENSABLE avant de compter les maxima : sur une courbe
    brute bruitee a 2 %, le bruit cree des maxima parasites et le diagnostic
    clos/bass-reflex se trompe.
    """
    y = np.asarray(y, float)
    if n <= 1 or y.size < n:
        return y.copy()
    noyau = np.ones(n) / n
    lisse = np.convolve(y, noyau, mode='same')
    demi = n // 2                                  # bords : on garde le brut
    lisse[:demi], lisse[-demi:] = y[:demi], y[-demi:]
    return lisse


def rapport_max_min(f, Z, bande=None):
    """max|Z| / min|Z| sur une bande -- le "du simple au sextuple" de la problematique.

    bande = (f_bas, f_haut) en Hz ; None = toute la grille fournie.

    Deux lectures honnetes du rapport, a ne pas confondre (§ 01.8) : rapporte a
    l'impedance NOMINALE, un pic de 40 a 60 ohms fait x5 a x7,5 par rapport a
    8 ohms ; rapporte a R_e, les datasheets donnent plutot x20 en champ libre
    (|Z|max/R_e = 1 + Q_ms/Q_es). Sur la charge du passe-bas, dans sa propre bande
    40-250 Hz, le modele typique en caisse close donne 19,9. Le "sextuple" est
    donc une BORNE BASSE plausible, a remplacer par le rapport mesure en caisse.
    """
    f = np.asarray(f, float)
    mod = _module(Z)
    if bande is not None:
        m = (f >= bande[0]) & (f <= bande[1])
        if not np.any(m):
            raise ValueError('rapport_max_min : aucun point dans la bande')
        mod = mod[m]
    return float(mod.max() / mod.min())


def pic_principal(f, Z, affiner=True):
    """Position et hauteur du maximum de |Z| : retourne (f_pic [Hz], |Z|_pic [ohm]).

    affiner=True raffine par une parabole sur les trois points voisins, en
    log(f) : le sommet de |Z| est PLAT, donc sur une grille au 1/12 d'octave
    bruitee a 2 % l'argmax brut tombe couramment a un pas de grille de la verite
    (42,4 Hz pour 40 Hz vrais, § 03.3).

    Trois avertissements d'usage, tous verifies numeriquement (§ 01.4, § 03.3) :
    (1) f_pic n'est PAS f_s -- L_e decale le maximum de |Z| et le zero de phase en
    sens OPPOSES (39,940 Hz et 40,079 Hz pour f_s = 40,000) ; seul l'ajustement
    rend f_s ; (2) |Z|_pic n'est pas exactement R_e + R_es pour la meme raison ;
    (3) sur une courbe bruitee, initialiser f_s par le PASSAGE PAR ZERO DE LA
    PHASE est plus net que par cet argmax (c'est ce que fait ts_fit).
    """
    f = np.asarray(f, float)
    mod = _module(Z)
    k = int(np.argmax(mod))
    if not affiner or k == 0 or k == f.size - 1:
        return float(f[k]), float(mod[k])
    lx = np.log(f[k - 1:k + 2])
    a, b, c = np.polyfit(lx, mod[k - 1:k + 2], 2)
    if a >= 0:                                     # pas de sommet : on garde le point
        return float(f[k]), float(mod[k])
    sommet = -b / (2 * a)
    if not (lx[0] <= sommet <= lx[2]):             # extrapolation : on refuse
        return float(f[k]), float(mod[k])
    return float(np.exp(sommet)), float(a * sommet**2 + b * sommet + c)


def extrema_locaux(f, Z, lissage=3, bande=None):
    """Maxima et minima locaux de |Z| apres lissage (base du diagnostic de caisse).

    Retourne un dict : 'f_pics', 'mod_pics', 'f_creux', 'mod_creux' (tableaux
    numpy, tries en frequence). Les extrema sont cherches au sens strict sur la
    courbe LISSEE (§ 03.7) ; les bornes de la bande ne comptent jamais comme
    extremum, ce qui evite de compter la remontee inductive de haut de bande.
    """
    f = np.asarray(f, float)
    mod = _module(Z)
    if bande is not None:
        m = (f >= bande[0]) & (f <= bande[1])
        f, mod = f[m], mod[m]
    y = _moyenne_glissante(mod, lissage)
    if y.size < 3:
        vide = np.array([])
        return dict(f_pics=vide, mod_pics=vide, f_creux=vide, mod_creux=vide)
    haut = (y[1:-1] > y[:-2]) & (y[1:-1] >= y[2:])
    bas = (y[1:-1] < y[:-2]) & (y[1:-1] <= y[2:])
    i_h, i_b = np.where(haut)[0] + 1, np.where(bas)[0] + 1
    return dict(f_pics=f[i_h], mod_pics=mod[i_h],
                f_creux=f[i_b], mod_creux=mod[i_b])


def compter_pics(f, Z, lissage=3, bande=(10.0, 100.0)):
    """Nombre de maxima locaux de |Z| dans la bande (critere d'aiguillage § 03.7).

    Un seul maximum -> caisse close (modele a 5 parametres). Deux ou plus ->
    bass-reflex. Le critere est bien ">= 2" et non "exactement 2" : sur le jeu
    synthetique a deux pics, le comptage rend 3 (dont un parasite) et cela ne doit
    pas faire echouer le diagnostic.
    """
    return int(extrema_locaux(f, Z, lissage=lissage, bande=bande)['f_pics'].size)


def diagnostic_caisse(f, Z, lissage=3, bande=(10.0, 100.0), bavard=True):
    """Aiguillage clos / bass-reflex AVANT tout ajustement, et son avertissement.

    Pourquoi cette fonction existe, et pourquoi elle crie (§ 03.4, test D) :
    applique a une courbe a DEUX pics, le modele a 5 parametres CONVERGE sans
    lever la moindre erreur et rend des nombres d'allure parfaitement plausible
    (R_e = 6,17 +- 0,20 ohm, f_s = 39,0 +- 0,7 Hz, Q_ms = 2,11 +- 0,22) qui ne
    veulent rien dire. Seuls le chi2 reduit (s^2 = 93) et la structure des residus
    le trahissent. Un modele inadapte ne se signale donc pas par une exception :
    il faut le detecter AVANT, en comptant les pics.

    Retourne un dict : 'type_caisse' ('clos' ou 'bass-reflex'), 'n_pics',
    'f_pics', 'f_creux', 'modele_conseille', 'n_parametres', 'message'.
    Emet un UserWarning (donc capturable par les tests) si la courbe montre deux
    pics ou plus.
    """
    ext = extrema_locaux(f, Z, lissage=lissage, bande=bande)
    n = int(ext['f_pics'].size)
    if n >= 2:
        diag = dict(type_caisse='bass-reflex', modele_conseille='Z_bassreflex8',
                    n_parametres=8)
        diag['message'] = (
            "%d maxima de |Z| entre %g et %g Hz : la caisse est un BASS-REFLEX. "
            "NE PAS ajuster le modele a 5 parametres -- il convergerait en silence "
            "sur des valeurs fausses (voir § 03.4 test D)." % (n, bande[0], bande[1]))
        warnings.warn(diag['message'], UserWarning, stacklevel=2)
    else:
        diag = dict(type_caisse='clos', modele_conseille='Z_ts', n_parametres=5)
        diag['message'] = ("1 maximum de |Z| entre %g et %g Hz : caisse close, "
                           "modele a 5 parametres." % (bande[0], bande[1]))
    diag.update(n_pics=n, f_pics=ext['f_pics'], f_creux=ext['f_creux'])
    if bavard:
        print('  diagnostic caisse : ' + diag['message'])
    return diag


# =====================================================================
# 7. JEUX DE PARAMETRES TYPIQUES -- ORDRES DE GRANDEUR, PAS DES MESURES
# =====================================================================

_AVERT = ("ORDRE DE GRANDEUR TYPIQUE -- AUCUNE MESURE DE L'ENCEINTE DE THOMAS. "
          "A remplacer par les parametres identifies en phase 2.")

# 18 pouces de sono, 8 ohm nominal. Datasheet publique B&C Speakers 18PS76
# (bcspeakers.com, consultee le 2026-09-02, § 01.13) : Re = 5,0 ohm ;
# Le = 1,9 mH a 1 kHz ; fs = 39 Hz (CHAMP LIBRE) ; Qms = 6,1 ; Qes = 0,29.
# R_es est reconstruit par R_e Q_ms / Q_es -- il n'est jamais dans une fiche.
# Avertissement honnete (§ 01.13) : CETTE fiche n'est pas auto-coherente. Avec le
# Q_es publie on obtient Res = 105 ohm et |Z|max = 110 ohm ; en RECALCULANT Q_es
# depuis (Bl, Re, Mms, fs) on trouve 0,274, donc Res = 111 ohm et |Z|max = 116 ohm.
# Trois tests concordants (Q_es, V_as, |Z|max) donnent 5 a 12 % d'ecart sur cette
# fiche : c'est l'ordre de grandeur de la confiance a accorder a une datasheet, et
# le meilleur argument du projet pour aller mesurer. On retient ici le Q_es publie.
SUB_TYP = {
    'modele': 'clos',
    'nom': '18 pouces sono 8 ohm (ordre de grandeur)',
    'source': 'datasheet publique B&C Speakers 18PS76, consultee le 2026-09-02 (§ 01.13)',
    'avertissement': _AVERT,
    'Re': 5.0, 'Le': 1.9e-3, 'fs': 39.0, 'Qms': 6.1,
    'Qes_datasheet': 0.29,
}
SUB_TYP['Res'] = Res_depuis_Qes(SUB_TYP['Re'], SUB_TYP['Qms'], SUB_TYP['Qes_datasheet'])

# Le meme 18 pouces mis en caisse CLOSE de volume V_b = V_as (alpha = 1) : f_s et
# Q_ms sont multiplies par racine(2). C'est cette charge-la que verrait le filtre,
# et son pic tombe alors DANS la bande de raccord.
_fc, _Qmc, _Qec, _ = caisse_close(SUB_TYP['fs'], SUB_TYP['Qms'],
                                  SUB_TYP['Qes_datasheet'], alpha=1.0)
SUB_TYP_CLOS = dict(SUB_TYP, nom='18 pouces en caisse close alpha = 1 (V_b = V_as)',
                    fs=_fc, Qms=_Qmc, Qes_datasheet=_Qec)

# Le meme 18 pouces en BASS-REFLEX, variante ACCORD BAS / GROSSE CAISSE : alpha,
# f_b et Q_l sont ici de PURES illustrations (§ 01.10). alpha = V_as/V_b, et on
# ecrit les DEUX volumes pour que l'incoherence ne puisse pas se reformer :
# V_as = 207 L (datasheet B&C 18PS76, § 01.13) et V_b = 230 L -> alpha = 0,9 ;
# accord f_b = 35 Hz ; pertes de caisse Q_l = 7, valeur realiste qui abaisse
# nettement les deux pics. C'est le cas de COMPARAISON (le pic haut reste a
# 60 Hz, loin du raccord) ; le cas du projet est io_mesures.SUB_TYPIQUE_BR,
# caisse PETITE devant V_as (alpha = 3), ou le pic haut remonte vers 86 Hz.
SUB_TYP_BR = dict(SUB_TYP, modele='bassreflex',
                  nom='18 pouces en bass-reflex (illustration, § 01.10)',
                  alpha=0.9, fb=35.0, Ql=7.0)

# Bloc medium = DEUX 4 ohm cables en serie (= 8 ohm). Datasheet publique
# FaitalPRO 8FE200-4 (faitalpro.com, consultee le 2026-09-02, § 01.13) :
# Re = 3,0 ohm ; Le = 0,25 mH ; fs = 80 Hz ; Qms = 8,7 ; Qes = 0,47. En serie,
# R_e, L_e et R_es doublent, f_s et Q_ms ne bougent pas.
MED_UNITAIRE_TYP = {
    'modele': 'clos',
    'nom': 'medium 8 pouces 4 ohm, un seul (ordre de grandeur)',
    'source': 'datasheet publique FaitalPRO 8FE200-4, consultee le 2026-09-02 (§ 01.13)',
    'avertissement': _AVERT,
    'Re': 3.0, 'Le': 0.25e-3, 'fs': 80.0, 'Qms': 8.7,
    'Qes_datasheet': 0.47,
}
MED_UNITAIRE_TYP['Res'] = Res_depuis_Qes(3.0, 8.7, 0.47)

MED_TYP = dict(MED_UNITAIRE_TYP,
               nom='bloc medium : 2 x 4 ohm en serie (= 8 ohm)',
               Re=2 * MED_UNITAIRE_TYP['Re'], Le=2 * MED_UNITAIRE_TYP['Le'],
               Res=2 * MED_UNITAIRE_TYP['Res'])

# Jeu de test de METHODE herite de la v1 (archive-v1/_gen.py). Il sert aux donnees
# synthetiques de ts_fit : il est plausible en FORME, pas en valeurs (Q_ms = 1,75,
# soit trois a six fois moins que les fiches ci-dessus, donc un pic bien plus large
# et bien mieux echantillonne que le vrai). NE JAMAIS le citer comme representatif
# du sub (§ 01.13).
JEU_SYNTHETIQUE_V1 = {
    'modele': 'clos',
    'nom': 'jeu SYNTHETIQUE de test de methode (v1)',
    'source': 'archive-v1/_gen.py -- test de methode, § 03.4',
    'avertissement': "SYNTHETIQUE : ne decrit AUCUN haut-parleur reel.",
    'Re': 6.5, 'Le': 1.2e-3, 'Res': 44.0, 'fs': 40.0, 'Qms': 1.75,
}

# Jeu MECANIQUE du § 01.5, recale sur les fourchettes du § 01.13. Il sert a
# verifier les formules de passage (c'est le seul endroit du projet ou l'on part
# de Bl, M_ms, C_ms, R_ms -- grandeurs que Z(f) ne rend PAS, § 01.6).
JEU_MECANIQUE_01_5 = {
    'nom': 'jeu mecanique illustratif du § 01.5 (18 pouces)',
    'avertissement': _AVERT,
    'Re': 5.0, 'Le': 1.5e-3,
    'Bl': 24.0, 'Mms': 0.150, 'Cms': 1.1e-4, 'Rms': 6.0, 'Sd': 0.1190,
}


# =====================================================================
# 8. AUTO-VERIFICATION (python analyse/modele_hp.py)
# =====================================================================

def _titre(t):
    print('\n' + t + '\n' + '-' * len(t))


def _autotest():
    """Rejoue les nombres de controle de la reference. Aucune mesure n'est lue."""
    print('=== modele_hp.py : auto-verification ===')
    print('DONNEES SYNTHETIQUES OU DATASHEETS PUBLIQUES -- aucune mesure de '
          "l'enceinte de Thomas n'existe a ce jour.")
    ok = []

    # ---- 1. formules de passage, et aller-retour parametres -> Z -> pic --------
    _titre('1. Formules de passage (jeu mecanique du § 01.5)')
    j = JEU_MECANIQUE_01_5
    Res, Lces, Cmes = meca_vers_elec(j['Bl'], j['Mms'], j['Cms'], j['Rms'])
    fs, Qms = rlc_vers_ts(Res, Lces, Cmes)
    Qes, Qts = facteurs_qualite(j['Re'], Res, Qms)
    print('  Res = %.1f ohm   Lces = %.1f mH   Cmes = %.0f uF   (§ 01.5 : 96,0 / 63,4 / 260)'
          % (Res, 1e3 * Lces, 1e6 * Cmes))
    print('  fs = %.2f Hz   Qms = %.3f   Qes = %.4f   Qts = %.4f'
          '   (§ 01.5 : 39,2 / 6,15 / 0,321 / 0,305)' % (fs, Qms, Qes, Qts))
    print('  Vas = %.0f L (Sd = %.0f cm2)   (§ 01.9 : 220 L)'
          % (1e3 * Vas(j['Sd'], j['Cms']), 1e4 * j['Sd']))

    Lces2, Cmes2 = ts_vers_rlc(Res, fs, Qms)
    ar = max(abs(Lces2 / Lces - 1), abs(Cmes2 / Cmes - 1))
    print('  aller-retour (Res,fs,Qms) -> (Lces,Cmes) -> retour : ecart relatif %.1e' % ar)
    ok.append(('aller-retour des formules de passage', ar < 1e-12))

    f = grille_log(5.0, 2000.0, 96)
    Z = Z_ts(f, j['Re'], j['Le'], Res, fs, Qms)
    f_pic, m_pic = pic_principal(f, Z)
    m_th = module_max_theorique(j['Re'], Qms, Qes)
    print('  |Z|max theorique Re(1+Qms/Qes) = %.2f ohm ; lu sur la courbe %.2f ohm a %.2f Hz'
          % (m_th, m_pic, f_pic))
    print('    -> ecart %.3f %% sur la hauteur, %.3f %% sur la frequence (L_e decale le pic)'
          % (100 * (m_pic / m_th - 1), 100 * (f_pic / fs - 1)))
    ok.append(('relecture du pic sur la courbe', abs(m_pic / m_th - 1) < 2e-3
               and abs(f_pic / fs - 1) < 2e-3))
    print('  min|Z| sur la grille = %.4f ohm pour Re = %.2f ohm (branche motionnelle '
          'passive : |Z| >= Re partout, § 01.3)' % (np.abs(Z).min(), j['Re']))
    ok.append(('|Z| >= Re partout', np.abs(Z).min() >= j['Re'] - 1e-9))

    # ---- 2. caisse close : le pic entre dans la bande de raccord --------------
    _titre('2. Caisse close alpha = 1 : ce que le passe-bas voit vraiment (§ 01.8)')
    fc, Qmc, Qec, Qtc = caisse_close(fs, Qms, Qes, alpha=1.0)
    print('  fc = %.2f Hz (§ 01.9 : 55,4)   Qmc = %.2f   Qec = %.4f   Qtc = %.3f'
          % (fc, Qmc, Qec, Qtc))
    print('  alpha relu par (fc/fs)^2 - 1 = %.4f' % alpha_depuis_pics(fs, fc))
    fg = grille_log(20.0, 500.0, 96)
    Zc = Z_ts(fg, j['Re'], j['Le'], Res, fc, Qmc)
    for f0, att in ((60.0, 58.78), (100.0, 9.72), (150.0, 6.18)):
        z = Z_ts(f0, j['Re'], j['Le'], Res, fc, Qmc)
        print('  f = %5.0f Hz : |Z| = %7.2f ohm, phase = %+6.1f deg   (§ 01.8 : %.2f ohm)'
              % (f0, abs(z), np.degrees(np.angle(z)), att))
    z100 = Z_ts(100.0, j['Re'], j['Le'], Res, fc, Qmc)
    ok.append(('|Z|(100 Hz) en caisse close = 9,72 ohm', abs(abs(z100) - 9.72) < 0.02))
    r = rapport_max_min(fg, Zc, bande=(40.0, 250.0))
    print('  rapport max/min de |Z| sur 40-250 Hz = %.1f   (§ 01.8 : 19,9)' % r)
    ok.append(('rapport max/min = 19,9 sur 40-250 Hz', abs(r - 19.9) < 0.3))

    # ---- 3. jeux typiques : ordres de grandeur --------------------------------
    _titre('3. Jeux typiques (datasheets publiques -- AUCUNE mesure)')
    for jeu in (SUB_TYP, MED_TYP):
        fx = grille_log(10.0, 1000.0, 96)
        Zx = Z_depuis_jeu(fx, jeu)
        fp, mp = pic_principal(fx, Zx)
        z100 = Z_depuis_jeu(100.0, jeu)
        print('  %s' % jeu['nom'])
        print('    Re = %.1f ohm  Res = %.1f ohm  fs = %.0f Hz  Qms = %.2f  Qes = %.3f'
              % (jeu['Re'], jeu['Res'], jeu['fs'], jeu['Qms'], jeu['Qes_datasheet']))
        print('    |Z|max = %.1f ohm a %.1f Hz   |Z|(100 Hz) = %.1f ohm, phase %+.0f deg'
              % (mp, fp, abs(z100), np.degrees(np.angle(z100))))
    fx = grille_log(10.0, 1000.0, 96)
    _, mp_sub = pic_principal(fx, Z_depuis_jeu(fx, SUB_TYP))
    print('  controle d ordre de grandeur du 18 pouces : pic attendu entre 60 et 200 ohm')
    ok.append(('pic du 18 pouces dans [60, 200] ohm', 60.0 <= mp_sub <= 200.0))
    _, mp_med = pic_principal(fx, Z_depuis_jeu(fx, MED_TYP))
    ok.append(('pic du bloc medium ~ 117 ohm (§ 01.13)', abs(mp_med - 117.0) < 2.0))
    # deux mediums mal apparies : le bloc montre deux pics (§ 01.12)
    ta = (MED_UNITAIRE_TYP['Re'], MED_UNITAIRE_TYP['Le'], MED_UNITAIRE_TYP['Res'],
          80.0 * 0.9, MED_UNITAIRE_TYP['Qms'])
    tb = (MED_UNITAIRE_TYP['Re'], MED_UNITAIRE_TYP['Le'], MED_UNITAIRE_TYP['Res'],
          80.0 * 1.1, MED_UNITAIRE_TYP['Qms'])
    fm = grille_log(40.0, 200.0, 192)
    e = extrema_locaux(fm, Z_serie_2hp(fm, ta, tb))
    print('  bloc medium DESAPPARIE de +-10 %% sur fs : pics a %s Hz (ecart %.0f Hz)'
          % (np.round(e['f_pics'], 1), np.ptp(e['f_pics']) if e['f_pics'].size > 1 else 0))
    ok.append(('deux pics si les mediums sont desapparies', e['f_pics'].size == 2))

    # ---- 3 bis. charge COMPOSITE du passe-haut : pavillons en parallele -------
    _titre('3 bis. Les pavillons sont hors bande ACOUSTIQUE, pas hors charge ELECTRIQUE')
    th_med = [MED_UNITAIRE_TYP[c] for c in ('Re', 'Le', 'Res', 'fs', 'Qms')]
    print('  Condensateur en serie avec les pavillons : PRESENT (constat du 16/09/2026),')
    print('  valeur [[a mesurer]]. Le calcul ci-dessous encadre son effet.')
    print('  %-12s %12s %12s %12s' % ('condensateur', '|Z| branche', '|Z| bloc', 'ecart'))
    for etiquette, C in (('aucun', None), ('3,3 uF', 3.3e-6), ('6,8 uF', 6.8e-6),
                         ('10 uF', 10e-6)):
        ea = effet_branche_aigu(th_med, f_ref=100.0, R_aigu=8.0, C_aigu=C, n_aigu=2)
        z = ea['module_sans_condensateur'] if C is None else ea['module_avec_condensateur']
        ecart = ea['ecart_sans_pct'] if C is None else ea['ecart_avec_pct']
        print('  %-12s %9.1f ohm %9.2f ohm %+11.1f %%'
              % (etiquette, ea['module_branche_aigu'], z, ecart))
    ea0 = effet_branche_aigu(th_med, f_ref=100.0, R_aigu=8.0, C_aigu=6.8e-6, n_aigu=2)
    print('  bloc medium SEUL a 100 Hz : %.2f ohm' % ea0['module_bloc_seul'])
    print('  lecture : SANS condensateur la charge tombe a %.1f ohm -- sous le minimum'
          % ea0['module_sans_condensateur'])
    print('  de 4 ohm du t.amp E-800 -- et les pavillons prennent du 100 Hz a pleine')
    print('  puissance. AVEC 6,8 uF l effet reste de %+.0f %% : notable, pas anodin.'
          % ea0['ecart_avec_pct'])
    ok.append(('branche aigu SANS condensateur : chute de plus de 50 % de |Z|',
               ea0['ecart_sans_pct'] < -50.0))
    ok.append(('branche aigu AVEC condensateur : effet non nul mais modere',
               -40.0 < ea0['ecart_avec_pct'] < -1.0))
    ok.append(('R_aigu=None redonne exactement le bloc seul',
               abs(ea0['module_bloc_seul']
                   / abs(complex(Z_serie_2hp(np.array([100.0]), th_med, th_med)[0]))
                   - 1.0) < 1e-12))

    # ---- 4. bass-reflex : deux pics, un creux, et les deux identites ----------
    _titre('4. Bass-reflex : deux pics et un creux (§ 01.10)')
    b = SUB_TYP_BR
    fb_ = grille_log(10.0, 300.0, 192)
    Zb = Z_depuis_jeu(fb_, b)
    e = extrema_locaux(fb_, Zb, bande=(10.0, 150.0))
    print('  pics a %s Hz (|Z| = %s ohm)'
          % (np.round(e['f_pics'], 1), np.round(e['mod_pics'], 1)))
    print('  creux a %s Hz (|Z| = %s ohm) ; accord fb = %.1f Hz'
          % (np.round(e['f_creux'], 1), np.round(e['mod_creux'], 1), b['fb']))
    ok.append(('bass-reflex : 2 pics', e['f_pics'].size == 2))
    ok.append(('bass-reflex : 1 creux entre les deux pics', e['f_creux'].size == 1))
    if e['f_pics'].size == 2:
        fL, fH = e['f_pics']
        fbb, fss, al = b['fb'], b['fs'], b['alpha']
        print('  controle fL < fb < fH : %.1f < %.1f < %.1f' % (fL, fbb, fH))
        print('  controle fL*fH = %.0f  vs  fs*fb = %.0f   (ecart %+.2f %%)'
              % (fL * fH, fss * fbb, 100 * (fL * fH / (fss * fbb) - 1)))
        att = fss**2 * (1 + al) + fbb**2
        print('  controle fL^2+fH^2 = %.0f  vs  fs^2(1+alpha)+fb^2 = %.0f  (ecart %+.2f %%)'
              % (fL**2 + fH**2, att, 100 * ((fL**2 + fH**2) / att - 1)))
        ok.append(('identite fL*fH = fs*fb (a 2 %)',
                   abs(fL * fH / (fss * fbb) - 1) < 0.02))
        ok.append(('identite fL^2+fH^2 (a 2 %)',
                   abs((fL**2 + fH**2) / att - 1) < 0.02))
        ok.append(('fL < fb < fH', fL < fbb < fH))
    # event inerte (masse d'air infinie, fb -> 0) : on doit RETOMBER sur la close
    fz = grille_log(10.0, 500.0, 48)
    Z_inerte = Z_bassreflex(fz, b['Re'], b['Le'], b['Res'], b['fs'], b['Qms'],
                            fb=1e-4, Ql=1e9, alpha=1.0)
    fc1, Qmc1, _, _ = caisse_close(b['fs'], b['Qms'], b['Qes_datasheet'], alpha=1.0)
    Z_clos = Z_ts(fz, b['Re'], b['Le'], b['Res'], fc1, Qmc1)
    ecart = float(np.max(np.abs(Z_inerte - Z_clos)))
    print('  controle "event inerte" (fb -> 0) = caisse close de meme volume : '
          'ecart max %.1e ohm' % ecart)
    ok.append(('event inerte -> caisse close', ecart < 1e-6))

    # ---- 4 bis. geometrie des events : la prediction falsifiable de f_b -------
    _titre('4 bis. f_b predite par la geometrie (Helmholtz, 2 events) -- § 01.10')
    print('  Geometrie ILLUSTRATIVE (la vraie est [[a mesurer]]) : V = 110 L,')
    print('  2 events de 100 mm de diametre et 274 mm de long. Ces cotes ont ete')
    print('  RESOLUES A L ENVERS pour donner f_b = 35 Hz : la concordance avec')
    print('  SUB_TYPIQUE_BR ci-dessous est une verification de CODE, pas un resultat.')
    g = frequence_accord_helmholtz(110.0, 2, 100.0, 274.0, detail=True)
    print('  S_tot = %.4f m2 ; L_eff = L + k a = %.0f + %.0f = %.0f mm (k = %.2f)'
          % (g['S_totale_m2'], 1e3 * g['L_physique_m'],
             1e3 * g['correction_de_bout_m'], 1e3 * g['L_effective_m'],
             g['k_correction']))
    print('  f_b = %.2f Hz ; encadrement k = 1,227 a 1,698 : %.2f - %.2f Hz'
          % (g['fb_Hz'], g['fb_encadrement_Hz'][0], g['fb_encadrement_Hz'][1]))
    un = frequence_accord_helmholtz(110.0, 1, 100.0, 274.0)
    print('  un SEUL event de meme geometrie : %.2f Hz -- le rapport vaut racine(2) '
          '= %.4f' % (un, g['fb_Hz'] / un))
    ok.append(('doubler le nombre d events monte f_b de racine(2)',
               abs(g['fb_Hz'] / un / np.sqrt(2.0) - 1.0) < 1e-12))
    ok.append(('f_b geometrique coherent avec l accord illustratif de SUB_TYP_BR',
               abs(g['fb_Hz'] / SUB_TYP_BR['fb'] - 1.0) < 0.05))

    # ---- 4 ter. sommation en champ proche (Keele) ------------------------------
    _titre('4 ter. Champ proche : membrane + events, ponderes par les RAYONS (§ 02.10)')
    Sd, Sev = 0.1190, np.pi * 0.100**2 / 4.0
    poids = np.sqrt(Sev / Sd)
    print('  S_d = %.4f m2 (datasheet), S_event = %.5f m2 -> poids racine(S/S_d) = %.4f'
          % (Sd, Sev, poids))
    print('  l erreur classique serait de ponderer par les AIRES : %.4f, soit %.1f dB'
          ' de moins' % (Sev / Sd, 20 * np.log10(poids / (Sev / Sd))))
    # controle : deux sources en opposition exacte s'annulent au poids pres
    p_m = np.array([1.0 + 0j, 1.0 + 0j])
    p_e = np.array([-1.0 + 0j, -1.0 + 0j]) / poids / 2.0
    tot = somme_champ_proche_bassreflex(p_m, p_e, Sd, Sev, n_events=2)
    print('  controle : 2 events en opposition exacte, ponderes -> somme = %s'
          % np.round(np.abs(tot), 12))
    ok.append(('sommation de Keele : annulation exacte en opposition',
               float(np.max(np.abs(tot))) < 1e-12))
    tot1 = somme_champ_proche_bassreflex(p_m, np.zeros_like(p_m), Sd, Sev, n_events=2)
    ok.append(('events muets -> la somme redonne la membrane',
               float(np.max(np.abs(tot1 - p_m))) < 1e-15))

    # ---- 5. diagnostic clos / bass-reflex -------------------------------------
    _titre('5. Diagnostic de caisse AVANT ajustement (§ 03.7, § 03.4 test D)')
    fd = grille_log(10.0, 500.0, 24)
    with warnings.catch_warnings(record=True) as capte:
        warnings.simplefilter('always')
        d_clos = diagnostic_caisse(fd, Z_depuis_jeu(fd, SUB_TYP_CLOS))
        n_avert_clos = len(capte)
    with warnings.catch_warnings(record=True) as capte:
        warnings.simplefilter('always')
        d_br = diagnostic_caisse(fd, Z_depuis_jeu(fd, SUB_TYP_BR))
        n_avert_br = len(capte)
    print('  clos       : %d pic(s) -> %s (%d parametres), %d avertissement'
          % (d_clos['n_pics'], d_clos['modele_conseille'], d_clos['n_parametres'],
             n_avert_clos))
    print('  bass-reflex: %d pic(s) -> %s (%d parametres), %d avertissement'
          % (d_br['n_pics'], d_br['modele_conseille'], d_br['n_parametres'],
             n_avert_br))
    ok.append(('diagnostic : clos detecte, sans avertissement',
               d_clos['type_caisse'] == 'clos' and n_avert_clos == 0))
    ok.append(('diagnostic : bass-reflex detecte ET signale',
               d_br['type_caisse'] == 'bass-reflex' and n_avert_br == 1))

    # ---- 6. semi-inductance ---------------------------------------------------
    _titre('6. Semi-inductance K(jw)^n : pourquoi un L_e constant biaise R_e (§ 01.12)')
    Le, n = 1.5e-3, 0.65
    K = K_semi_depuis_Le(Le, n)
    print('  Le = %.1f mH -> K = w_ref Le / w_ref^n = %.4f ohm.s^%.2f  (§ 01.12 : 0,0320)'
          % (1e3 * Le, K, n))
    for f0 in (100.0, 1000.0, 10000.0):
        w = 2 * np.pi * f0
        zl, zk = 1j * w * Le, K * (1j * w)**n
        print('  f = %6.0f Hz : jwLe = %6.2f ohm (90 deg) ; K(jw)^n = %6.2f ohm (%.0f deg) ;'
              ' Re(K(jw)^n) = %5.2f ohm ; rapport = %.2f'
              % (f0, abs(zl), abs(zk), np.degrees(np.angle(zk)), zk.real,
                 abs(zk) / abs(zl)))
    ok.append(('calibration de K a 1 kHz', abs(K - 0.0320) < 5e-4))
    print('  -> a 100 Hz le modele a pertes a une PARTIE REELLE de 1,10 ohm que jwLe'
          " n'a pas : un ajustement a Le constant la reporte sur R_e (+11,8 % sur"
          ' 10-500 Hz, § 03.6).')

    # ---- 7. Zobel et compensation de resonance --------------------------------
    _titre('7. Zobel et compensation de resonance (§ 04.4)')
    v = JEU_SYNTHETIQUE_V1
    Rz, Cz = zobel_ideal(v['Re'], v['Le'])
    fzz = grille_log(10.0, 10000.0, 48)
    Zbob = v['Re'] + 2j * np.pi * fzz * v['Le']
    ecart = float(np.max(np.abs(zobel(Zbob, fzz, Rz, Cz) - v['Re'])))
    print('  Rz = %.1f ohm, Cz = %.1f uF : (Re + jwLe) // Zobel = Re a %.1e ohm pres'
          % (Rz, 1e6 * Cz, ecart))
    ok.append(('Zobel ideal : annulation exacte de jwLe', ecart < 1e-12))
    Zv = Z_depuis_jeu(fzz, v)
    Zz = zobel(Zv, fzz, Rz, Cz)
    for f0 in (100.0, 1000.0):
        i = int(np.argmin(np.abs(fzz - f0)))
        print('  f = %5.0f Hz : |Z| %6.2f ohm (%+.0f deg) -> avec Zobel %6.2f ohm (%+.0f deg)'
              % (fzz[i], abs(Zv[i]), np.degrees(np.angle(Zv[i])),
                 abs(Zz[i]), np.degrees(np.angle(Zz[i]))))
    print('  (§ 04.4 : 14,1 -> 11,6 ohm a 100 Hz ; 9,2 -> 6,1 ohm a 1 kHz : le Zobel ne'
          ' corrige PAS le pic motionnel, qui est le vrai probleme au raccord)')
    Rc, Lc, Cc = compensation_rlc(v['Re'], v['Res'], v['fs'], v['Qms'])
    print('  compensation RLC serie : Rc = %.2f ohm, Lc = %.2f mH, Cc = %.0f uF'
          '   (§ 04.4 : 7,46 / 6,69 / 2368)' % (Rc, 1e3 * Lc, 1e6 * Cc))
    print('  accord 1/(2 pi racine(Lc Cc)) = %.2f Hz (doit valoir fs = %.2f Hz)'
          % (1 / (2 * np.pi * np.sqrt(Lc * Cc)), v['fs']))
    ok.append(('compensation RLC accordee sur fs',
               abs(1 / (2 * np.pi * np.sqrt(Lc * Cc)) / v['fs'] - 1) < 1e-9))

    # ---- 8. grilles -----------------------------------------------------------
    _titre('8. Grilles de frequences (§ 02.6)')
    g1 = grille_log(10.0, 500.0, 12)
    g2 = grille_log(10.0, 1000.0, 12)
    g3 = grille_log(10.0, 500.0, 12, densifier=(SUB_TYP['fs'] / 2, 2 * SUB_TYP['fs'], 24))
    print('  10-500 Hz au 1/12 d octave : %d points (§ 03.4 : 69) ; bornes %.1f et %.1f Hz'
          % (g1.size, g1[0], g1[-1]))
    print('  10-1000 Hz au 1/12 d octave : %d points (§ 02.6 : 81)' % g2.size)
    print('  idem + densifier=(fs/2, 2fs, 24) autour de fs = %.0f Hz : %d points'
          % (SUB_TYP['fs'], g3.size))
    print('  points proches du secteur : %s Hz (50 et 100 Hz exacts evites)'
          % np.round(g1[(g1 > 48) & (g1 < 52) | (g1 > 98) & (g1 < 103)], 1))
    ok.append(('grille 10-500 au 1/12 = 69 points', g1.size == 69))
    ok.append(('grille 10-1000 au 1/12 = 81 points', g2.size == 81))
    ok.append(('densification sans doublon', g3.size > g1.size
               and np.all(np.diff(g3) > 0)))

    # ---- bilan ---------------------------------------------------------------
    _titre('BILAN')
    for nom, val in ok:
        print('  [%s] %s' % ('OK ' if val else 'ECHEC', nom))
    n_ko = sum(1 for _, v_ in ok if not v_)
    print('\n  %d controle(s) sur %d passent.' % (len(ok) - n_ko, len(ok)))
    return n_ko == 0


if __name__ == '__main__':
    import sys
    try:                      # console Windows en cp1252 : le signe § casse l'affichage
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, OSError):
        pass
    sys.exit(0 if _autotest() else 1)
