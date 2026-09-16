# -*- coding: utf-8 -*-
"""filtre.py -- Le filtre de raccord 100 Hz sur une charge QUELCONQUE Z(f).

Acte 3 du recit (voir REFERENCE-TECHNIQUE.md § 04) : une fois Z(f) mesuree (acte 1)
et les parametres de Thiele-Small identifies (acte 2), ce module fournit les
fonctions de transfert EXACTES des deux cellules du second ordre chargees par une
impedance complexe arbitraire -- aucune approximation "8 ohm resistif" n'est faite
nulle part. C'est la brique sur laquelle optim.py (§ 04.5) construit la fonction de
cout, et c'est elle qui porte les definitions gelees du projet.

PHYSIQUE EN UNE PHRASE. Sur charge resistive R, le facteur de qualite d'une cellule
LC vaut Q = R*racine(C/L) : il appartient a la CHARGE, pas au filtre. Remplacer R par
Z(f) -- qui varie du simple au sextuple autour de la resonance du haut-parleur -- fait
donc varier Q avec la frequence, et c'est toute la difficulte du sujet v2.

DEFINITIONS GELEES REPRISES ICI (ne pas en inventer d'autres) :
  * f_c = f_x = frequence de CROISEMENT des deux voies, seule definition du TIPE
    (§ 04.1) : l'unique f de [40 ; 250] Hz telle que |H_pb.G_sub| = |H_ph.G_med|.
    Fonction : frequence_croisement().
  * f_0 = 1/(2.pi.racine(L.C)) est un REPERE nomme "le pole", jamais "f_c" (§ 09.4).
    Fonction : pole_et_q().
  * les "-3 dB" sont des REPERES nommes f3_pb et f3_ph ; la CONVENTION de seuil est un
    parametre nomme `seuil`, valeur par defaut mi-puissance 3,0103 dB = 10.log10(2)
    (convention de REW), l'autre option etant le seuil litteral 3,000 dB (§ 04.1).
    Fonction : repere_3db().
  * ecart RMS a la cible : moyenne quadratique a poids egal par octave, grille log a
    24 points/octave sur 40-250 Hz, plancher a 20 dB sous le maximum de bande
    (§ 07.9). Fonction : ecart_rms_db().

DECISION D2 (13/09/2026) : la cible de sommation est VOLONTAIREMENT reportee apres la
phase 1. La cible est donc partout un PARAMETRE ('butterworth', 'lr2', 'plate'),
jamais une constante -- voir cible() et cible_somme().

AUCUN RESULTAT MESURE ICI. Les seuls nombres presents dans ce fichier sont soit des
constantes de materiel lues sur une fiche technique (E-800), soit les valeurs de
controle CALCULEES du § 04, soit -- dans l'auto-test seulement -- des parametres de
haut-parleur SYNTHETIQUES explicitement etiquetes. Rien n'a encore ete mesure sur
l'enceinte de Thomas.

Conventions de code (§ 09.4) : tout en SI (H, F, Hz, ohm, V, A, W), conversion en
mH/uF a l'affichage seulement ; docstrings, commentaires et messages en francais SANS
ACCENTS pour rester lisibles dans une console cp1252 ; fichier en UTF-8, fins de
ligne LF. Les jeux de composants sont des tableaux (n, 2) pour que tout vectorise.

Dependance : numpy seul. scipy n'est PAS necessaire ici (les racines sont trouvees
par dichotomie maison, ce qui rend le module utilisable sur une machine du lycee).

Auto-test : python analyse/filtre.py
"""

import warnings

import numpy as np

# ----------------------------------------------------------------------------------
# 0. Constantes gelees
# ----------------------------------------------------------------------------------

SEUIL_MI_PUISSANCE = 3.0103   # dB : 10.log10(2), |H|^2 = 1/2 -- CONVENTION RETENUE
SEUIL_LITTERAL = 3.0          # dB : |H|^2 = 10^-0,3 = 0,50119 -- l'autre convention

BANDE_CRITERE = (40.0, 250.0)  # Hz, bande du critere gele (§ 07.9)
N_PAR_OCTAVE = 24              # points par octave de la grille du critere (§ 07.9)
PLANCHER_DB = 20.0             # dB sous le maximum de bande (§ 07.9)

R_NOM = 8.0                    # ohm, impedance nominale de reference
P_NOM_E800 = 350.0             # W sur 8 ohm, t.amp E-800 (fiche technique)
ZIN_MIN_E800 = 4.0             # ohm, minimum admis par l'ampli (contrainte 4, § 04.5)
C_SON = 343.0                  # m/s a 20 degres C

# Facteurs de qualite des cibles du second ordre (§ 04.3).
# 'plat' est le nom historique du § 04.6 ; 'lr2' est le nom gele par la decision D2.
CIBLES_Q = {'butterworth': 1.0 / np.sqrt(2.0),
            'lr2': 0.5,
            'plat': 0.5,
            'plate': 0.5}
CIBLES = ('butterworth', 'lr2', 'plate')   # les trois noms exposes par la decision D2

# Alias historiques acceptes en ENTREE et normalises aussitot. Correction de relecture
# (2026-09-14) : CIBLES_Q contenait un quatrieme nom, 'plat', que la validation acceptait
# silencieusement alors que le message d'erreur n'annoncait que les trois noms de D2.
# Sur une decision dont l'enonce impose exactement trois noms, laisser vivre un alias non
# annonce est la maniere dont une cible se fige par inadvertance : on le normalise donc,
# et on le DIT.
ALIAS_CIBLES = {'plat': 'lr2'}


def normaliser_cible(nom, avertir=True):
    """Ramene un nom de cible aux TROIS noms de la decision D2 -> 'butterworth' | 'lr2'
    | 'plate'.

    'plat' est l'alias historique du § 04.6 : il est accepte, traduit en 'lr2' et
    signale par un UserWarning, pour qu'un appel ecrit avant le gel de D2 ne passe plus
    en silence. Tout autre nom leve ValueError, en listant les noms admis -- alias
    compris, pour que le message dise la meme chose que le controle.
    """
    nom = str(nom)
    if nom in ALIAS_CIBLES:
        if avertir:
            warnings.warn("filtre : cible '%s' est l'alias historique de '%s' (§ 04.6) ; "
                          "la decision D2 n'expose que %s."
                          % (nom, ALIAS_CIBLES[nom], ', '.join(CIBLES)), UserWarning,
                          stacklevel=3)
        return ALIAS_CIBLES[nom]
    if nom not in CIBLES:
        raise ValueError("cible inconnue '%s' ; attendu parmi %s (decision D2) -- "
                         "alias accepte : %s"
                         % (nom, ', '.join(CIBLES),
                            ', '.join('%s = %s' % kv for kv in sorted(ALIAS_CIBLES.items()))))
    return nom


# ----------------------------------------------------------------------------------
# 1. Cellules du second ordre chargees par une impedance quelconque (§ 04.1)
# ----------------------------------------------------------------------------------

def H_pb(f, L, C, Z, r=0.0):
    """Passe-bas : L (avec sa DCR r) en SERIE, puis C en PARALLELE sur la charge Z.

    Transfert EXACT tension_HP / tension_entree, obtenu par un diviseur de tension
    sur l'impedance Z_para = Z // (1/jwC) :

        H_pb = Z_para / (jwL + r + Z_para),   Z_para = Z / (1 + jwCZ)

    Aucune hypothese sur Z : elle peut etre le 8 ohm resistif du sanity check, le
    modele de Thiele-Small identifie en phase 2, ou la mesure interpolee point a point.
    Sur charge resistive et r = 0 on retombe sur 1/(1 + jx/Q + (jx)^2) a la precision
    machine -- c'est le premier test de l'auto-test (§ 04.1).

    f : tableau (Nf,) de frequences en Hz ; L en H, C en F, r en ohm ; Z scalaire ou
    tableau (Nf,). Avec L et C de forme (n, 1) le retour est de forme (n, Nf) : c'est
    ainsi que optim.py evalue 576 couples d'un coup (§ 04.5).

    Voir § 04.1 et § 04.2.
    """
    w = 2.0 * np.pi * np.asarray(f, dtype=float)
    Z_para = Z / (1.0 + 1j * w * C * Z)          # Z // (1/jwC)
    return Z_para / (1j * w * L + r + Z_para)


def H_ph(f, C, L, Z, r=0.0):
    """Passe-haut : C en SERIE, puis L (avec sa DCR r) en PARALLELE sur la charge Z.

    Transfert EXACT tension_HP / tension_entree :

        H_ph = Z_para / (1/jwC + Z_para),   Z_para = (jwL + r) // Z

    Attention a l'ordre des arguments, gele au § 09.4 : (f, C, L, Z, r) pour le
    passe-haut, (f, L, C, Z, r) pour le passe-bas -- dans les deux cas le composant
    SERIE vient en premier. Meme regle de diffusion (n, 1) x (Nf,) -> (n, Nf).

    Voir § 04.1.
    """
    w = 2.0 * np.pi * np.asarray(f, dtype=float)
    Z_L = 1j * w * L + r
    Z_para = Z_L * Z / (Z_L + Z)                 # (jwL + r) // Z
    return Z_para / (1.0 / (1j * w * C) + Z_para)


def impedance_entree_pb(f, L, C, Z, r=0.0):
    """Impedance vue par l'amplificateur a l'entree de la cellule passe-bas.

    Z_in = jwL + r + (Z // 1/jwC). Grandeur absente de la v1 et pourtant
    dimensionnante : le filtre ne deforme pas seulement la reponse, il deforme la
    CHARGE. Sur le modele typique, le filtre catalogue fait tomber min|Z_in| de 6,7 a
    3,51 ohm, donc SOUS les 4 ohm admis par le E-800 (§ 04.2, contrainte 4 du § 04.5).

    Cout de calcul nul : c'est deja le denominateur de H_pb.
    """
    w = 2.0 * np.pi * np.asarray(f, dtype=float)
    return 1j * w * L + r + Z / (1.0 + 1j * w * C * Z)


def impedance_entree_ph(f, C, L, Z, r=0.0):
    """Impedance vue par l'amplificateur a l'entree de la cellule passe-haut :
    Z_in = 1/jwC + ((jwL + r) // Z). Voir impedance_entree_pb()."""
    w = 2.0 * np.pi * np.asarray(f, dtype=float)
    Z_L = 1j * w * L + r
    return 1.0 / (1j * w * C) + Z_L * Z / (Z_L + Z)


# ----------------------------------------------------------------------------------
# 2. Reseau de Zobel : la charge que l'on peut choisir de modifier (§ 04.4)
# ----------------------------------------------------------------------------------

def valeurs_zobel(Re, Le):
    """Valeurs qui ANNULENT exactement la partie inductive de la bobine mobile :

        R_z = Re,   C_z = Le / Re^2

    car alors (Re + jwLe) // (R_z + 1/jwC_z) = Re a TOUTE frequence.

    A dire au jury : ces valeurs sont optimales pour annuler l'inductance, rien ne
    prouve qu'elles minimisent la fonction de cout J -- d'ou le statut de simple
    BOOLEEN donne au Zobel dans l'optimisation (§ 04.5, statut du Zobel). Et surtout :
    le Zobel ne corrige PAS le pic motionnel, qui est le vrai probleme au raccord
    (sur le modele typique, a 100 Hz il fait passer |Z| de 14,1 a 11,6 ohm seulement).

    Retourne (R_z en ohm, C_z en F). Voir § 04.4.
    """
    return float(Re), float(Le) / float(Re) ** 2


def zobel(Z, f, Rz, Cz):
    """Impedance vue par le filtre quand un Zobel (Rz + Cz en serie) est monte en
    parallele sur le haut-parleur : Z // (Rz + 1/jwCz).

    Signature identique a celle gelee au § 09.4 pour modele_hp.zobel. Elle est
    redefinie ici pour que filtre.py reste utilisable seul (les modules sont ecrits en
    parallele) ; les deux implementations sont la meme formule d'une ligne, et en cas
    de divergence c'est modele_hp qui fait foi.
    """
    Z_z = Rz + 1.0 / (2j * np.pi * np.asarray(f, dtype=float) * Cz)
    return Z * Z_z / (Z + Z_z)


# ----------------------------------------------------------------------------------
# 3. Cibles de sommation -- PARAMETRE, jamais constante (decision D2, § 04.3)
# ----------------------------------------------------------------------------------

def cible(f, nom, f0_cible=100.0):
    """Formes cibles des DEUX VOIES, normalisees (charge ideale, gain de bande 1).

        s = j.f/f0_cible  (variable de Laplace normalisee),  D = 1 + s/Q + s^2
        H_pb_cible = 1/D,   H_ph_cible = s^2/D

    nom :
      'butterworth' -> Q = 1/racine(2) : chaque voie a -3,01 dB a f0_cible ; la somme
                       AVEC inversion de polarite vaut +3,01 dB a f0_cible.
      'lr2'         -> Q = 1/2 (Linkwitz-Riley 2) : chaque voie a -6,02 dB a f0_cible ;
                       la somme AVEC inversion est exactement plate (0,000 dB partout),
                       et les deux voies sont en phase a TOUTE frequence.
      'plate'       -> memes formes par voie que 'lr2' (c'est le seul couple du second
                       ordre dont la somme inversee soit plate), mais la cible de la
                       SOMME est 0 dB absolu : voir cible_somme().
      'plat'        -> alias historique de 'lr2' (nom utilise par le code du § 04.6).

    Au 2e ordre, l'inversion de polarite d'une voie est OBLIGATOIRE (Butterworth comme
    LR2) : sans elle, les deux voies sont a 180 degres a f_c et la somme s'annule.
    Elle se realise en permutant les deux fils d'un des haut-parleurs, et se verifie au
    micro en trente secondes (bosse = bon sens, trou profond = mauvais sens) -- § 04.3.

    Retourne (H_pb_cible, H_ph_cible), tableaux complexes de la forme de f.
    """
    nom = normaliser_cible(nom, avertir=False)   # 'plat' -> 'lr2', tout le reste leve
    s = 1j * np.asarray(f, dtype=float) / float(f0_cible)
    Q = CIBLES_Q[nom]
    D = 1.0 + s / Q + s ** 2
    return 1.0 / D, s ** 2 / D


def cible_somme(f, nom, f0_cible=100.0, pol=-1, G_sub=1.0, G_med=1.0, tau=0.0):
    """Cible de la SOMME des deux voies -- la grandeur que le critere gele juge.

    'butterworth' et 'lr2' : la cible est la somme des formes cibles, ponderee par les
    reponses des haut-parleurs G_sub, G_med et par le retard tau, EXACTEMENT comme la
    solution evaluee (meme polarite pol, meme tau). C'est le "critere juge le filtre et
    non les haut-parleurs" du § 07.9 : la non-planeite des HP se retrouve des deux
    cotes et se simplifie.

    'plate' : la cible est 0 dB absolu (module 1), quelles que soient G_sub et G_med.
    Le critere juge alors AUSSI la planeite des haut-parleurs -- c'est plus severe, et
    ce n'est pas la meme question. A ne choisir qu'en connaissance de cause.

    Remarque verifiee dans l'auto-test : en MODULE, 'lr2' et 'plate' donnent la meme
    cible (la somme LR2 inversee vaut exactement 1 en module) ; elles ne different que
    par la phase, dont le critere gele ne tient pas compte. Le choix entre les deux
    n'a donc d'effet que si G_sub ou G_med n'est pas plat.

    Voir § 04.3, § 04.5 (la cible suit la meme polarite que la solution) et § 07.9.
    """
    f = np.asarray(f, dtype=float)
    if nom == 'plate':
        return np.ones_like(f, dtype=complex)
    Hc_pb, Hc_ph = cible(f, nom, f0_cible)
    return sommer(f, Hc_pb, Hc_ph, pol=pol, G_sub=G_sub, G_med=G_med, tau=tau)


def composants_canoniques(nom, f0_cible=100.0, R=R_NOM):
    """Valeurs THEORIQUES (continues) de L et C d'une cellule du second ordre sur
    charge RESISTIVE R, pour la cible demandee :

        L = R / (Q.w0)      C = Q / (w0.R)      avec w0 = 2.pi.f0_cible

    C'est la porte de validation (b1) du § 09.6 : sur 8 ohm resistif, sans DCR ni
    penalite, l'optimiseur continu DOIT retomber sur ces valeurs -- c'est un theoreme,
    et rien ne s'achete tant qu'il echoue.

      butterworth, 100 Hz, 8 ohm : L = 18,0063 mH, C = 140,674 uF
      lr2 / plate, 100 Hz, 8 ohm : L = 25,4648 mH, C =  99,472 uF

    Retourne (L en H, C en F). Voir § 04.1, § 04.3 et § 09.6.
    """
    nom = normaliser_cible(nom, avertir=False)
    Q = CIBLES_Q[nom]
    w0 = 2.0 * np.pi * float(f0_cible)
    return R / (Q * w0), Q / (w0 * R)


def pole_et_q(L, C, R=R_NOM, r=0.0):
    """Reperes analytiques d'une cellule chargee par une RESISTANCE R, DCR r comprise.

    Derivation exacte (§ 04.1) :
        K  = R/(R + r)                     perte d'insertion (gain de bande passante)
        w0 = racine((R + r)/(L.C.R))       le POLE (jamais appele f_c)
        Q  = (R + r)/(w0.(L + r.R.C))

    Pour r = 0 on retrouve f0 = 1/(2.pi.racine(LC)) et Q = R.racine(C/L).
    Controle : 18 mH / 150 uF sur 8 ohm -> f0 = 96,859 Hz, Q = 0,7303, K = 1.

    La DCR agit TROIS fois : perte d'insertion K, deplacement du pole, et (sur charge
    reelle) amortissement du pic. Mais elle ne deplace presque pas le croisement
    (0,8 % pour r = 2 ohm) : c'est tout l'interet de la definition gelee de f_c.

    Retourne (f0 en Hz, Q, K).
    """
    L = float(L); C = float(C); R = float(R); r = float(r)
    w0 = np.sqrt((R + r) / (L * C * R))
    Q = (R + r) / (w0 * (L + r * R * C))
    return w0 / (2.0 * np.pi), Q, R / (R + r)


def reperes_3db_ideaux(L, C, R=R_NOM, seuil=SEUIL_MI_PUISSANCE):
    """Reperes a -3 dB, forme ANALYTIQUE, charge resistive R et DCR nulle.

    Avec t = 10^(-seuil/10) et u = (f/f0)^2, |H_pb|^2 = t s'ecrit
        u^2 + u.(1/Q^2 - 2) + 1 - 1/t = 0
    dont la racine positive donne f3_pb ; et comme |H_ph(x)| = |H_pb(1/x)| exactement,
        f3_ph = f0^2 / f3_pb
    -- c'est le controle croise f_pb x f_ph = f0^2 du § 04.1, exact dans les DEUX
    conventions de seuil (il ne prouve donc pas qu'on a choisi la bonne).

    Controle, 18 mH / 150 uF sur 8 ohm (f0 = 96,859 Hz, Q = 0,7303) :
        seuil = 3,0103 dB (mi-puissance, RETENU) -> 99,93 Hz et 93,88 Hz
        seuil = 3,000 dB  (litteral)             -> 99,82 Hz et 93,99 Hz
    L'ecart de 0,11 % est un ecart de CONVENTION, pas un arrondi fautif (§ 04.1).

    Des que la DCR n'est plus nulle ou que la charge n'est plus resistive, cette forme
    fermee ne vaut plus : utiliser repere_3db(), qui travaille sur la courbe reelle.

    Retourne un dict : f0, Q, f3_pb, f3_ph (Hz).
    """
    f0, Q, _ = pole_et_q(L, C, R, 0.0)
    t = 10.0 ** (-float(seuil) / 10.0)
    b = 1.0 / Q ** 2 - 2.0
    c = 1.0 - 1.0 / t
    u = (-b + np.sqrt(b * b - 4.0 * c)) / 2.0
    f3_pb = f0 * np.sqrt(u)
    return dict(f0=f0, Q=Q, f3_pb=f3_pb, f3_ph=f0 ** 2 / f3_pb)


# ----------------------------------------------------------------------------------
# 4. Sommation des deux voies (§ 04.2)
# ----------------------------------------------------------------------------------

def tau_de_ecart(d, c=C_SON):
    """Retard acoustique (s) correspondant a un ecart de trajet d (m) : tau = d/c.

    A 100 Hz la longueur d'onde vaut 3,43 m : 0,50 m d'ecart entre centres acoustiques
    valent 52 degres de dephasage, soit 0,93 dB de perte sur la somme dans l'axe (20
    degres coutent 0,13 dB, 45 degres 0,69 dB, 90 degres annulent). C'est largement de
    quoi transformer la bosse Butterworth de +3 dB en creux partiel.

    ATTENTION (§ 04.2) : une mesure en CHAMP PROCHE, protocole impose a 100 Hz, mesure
    chaque haut-parleur separement et ne capte donc PAS cette difference de trajet --
    il faut l'ajouter a la main. Ecart entre le centre du 18" et celui du bloc medium :
    [[a mesurer au metre ruban]].
    """
    return float(d) / float(c)


def sommer(f, H_1, H_2, pol=-1, G_sub=1.0, G_med=1.0, tau=0.0):
    """Somme acoustique des deux voies au point d'ecoute (§ 04.2) :

        S(f) = H_pb.G_sub + pol.H_ph.G_med.exp(-j.w.tau)

    pol   : +1 (meme polarite) ou -1 (une voie inversee). Au 2e ordre l'inversion est
            OBLIGATOIRE : sans elle la somme s'annule a f_c.
    G_sub,
    G_med : reponses en pression des haut-parleurs attaques en TENSION, mesurees en
            champ proche. Les laisser a 1 revient a optimiser la somme ELECTRIQUE
            alors que le critere gele est ACOUSTIQUE, et suppose de plus les deux
            voies de meme sensibilite -- hypothese fausse entre un 18" et un bloc
            medium, que l'optimiseur compenserait silencieusement par une deformation
            de filtre (§ 04.2, trois pieges a ne pas laisser a 1).
    tau   : retard de la voie medium (s), cf. tau_de_ecart(). Convention C2 du § 07.9 :
            p(t) = Re{p.exp(+jwt)}, donc un retard multiplie par exp(-jw.tau).

    Retourne S, tableau complexe diffuse sur la forme de H_1 et H_2.
    """
    w = 2.0 * np.pi * np.asarray(f, dtype=float)
    return H_1 * G_sub + pol * H_2 * G_med * np.exp(-1j * w * float(tau))


def ecart_de_phase(f, H_1, H_2, pol=-1, G_sub=1.0, G_med=1.0, tau=0.0):
    """Ecart de phase ENTRE LES DEUX VOIES, en degres, replie dans ]-180 ; 180].

        dphi = arg(H_pb.G_sub . conj(pol.H_ph.G_med.exp(-jw.tau)))

    C'est le terme w_phi de la fonction de cout (§ 04.5), evalue sur la sous-bande
    70-140 Hz. Rappel de calibrage : 20 degres d'ecart entre deux voies d'amplitude
    egale ne coutent que 0,13 dB sur la somme DANS L'AXE -- la ponderation proposee
    (0,05 dB/degre) n'est defendable que comme robustesse HORS AXE, et reste a
    recalibrer sur le tau mesure.
    """
    w = 2.0 * np.pi * np.asarray(f, dtype=float)
    v1 = H_1 * G_sub
    v2 = pol * H_2 * G_med * np.exp(-1j * w * float(tau))
    return np.degrees(np.angle(v1 * np.conj(v2)))


# ----------------------------------------------------------------------------------
# 5. Reperes de frequence : croisement (LA definition) et -3 dB (des reperes)
# ----------------------------------------------------------------------------------

def _valeurs(H, f):
    """Evalue H sur f : H est soit un tableau deja echantillonne sur f, soit une
    fonction f -> H (appelee telle quelle). Usage interne."""
    if callable(H):
        return np.asarray(H(f), dtype=complex)
    return np.asarray(H, dtype=complex)


def _db(x):
    """Module en dB, protege contre le zero exact (annulation de la somme)."""
    return 20.0 * np.log10(np.abs(x) + 1e-300)


def _dichotomie(g, a, b, n_iter=80):
    """Racine de g sur [a, b] par dichotomie, g(a) et g(b) de signes opposes.

    Dichotomie plutot que scipy.optimize.brentq : 80 iterations donnent la precision
    machine sur un intervalle de quelques hertz, et le module reste utilisable sur une
    machine ou scipy n'est pas installe (§ 09.5). Aucune derivee n'est demandee.
    """
    ga = g(a)
    for _ in range(n_iter):
        m = 0.5 * (a + b)
        gm = g(m)
        if gm == 0.0:
            return m
        if (ga < 0.0) != (gm < 0.0):
            b = m
        else:
            a, ga = m, gm
    return 0.5 * (a + b)


def _croisements(f, g, H=None, fonction_g=None, sens='tous'):
    """Frequences ou g change de signe, affinees.

    f : grille (Nf,) ; g : tableau (Nf,) des valeurs. Si fonction_g est fournie (cas
    d'un H callable), la racine est affinee par dichotomie ; sinon elle est interpolee
    lineairement en (ln f, g), ce qui suffit sur une grille fine.
    sens : 'descendant' (g passe de + a -), 'montant', ou 'tous'. Usage interne.
    """
    f = np.asarray(f, dtype=float)
    g = np.asarray(g, dtype=float)
    i = np.nonzero(np.diff(np.signbit(g)))[0]
    racines = []
    for k in i:
        descend = g[k] > g[k + 1]
        if sens == 'descendant' and not descend:
            continue
        if sens == 'montant' and descend:
            continue
        if fonction_g is not None:
            racines.append(_dichotomie(fonction_g, f[k], f[k + 1]))
        else:
            t = g[k] / (g[k] - g[k + 1])
            racines.append(float(np.exp(np.log(f[k]) + t * (np.log(f[k + 1]) - np.log(f[k])))))
    return np.array(racines, dtype=float)


def _grille(bande, n=4001):
    """Grille log fine pour l'encadrement des racines. Usage interne."""
    return np.geomspace(float(bande[0]), float(bande[1]), int(n))


def repere_3db(f, H, seuil=SEUIL_MI_PUISSANCE, gain_ref=None, sens='auto',
               choix='auto', bande=None, toutes=False):
    """REPERE a -3 dB d'une voie -- ce n'est PAS la definition de f_c (§ 04.1).

    La CONVENTION de seuil est le parametre nomme `seuil`, comme l'impose le § 09.4 :
      seuil = 3.0103 (defaut) : mi-puissance, |H|^2 = 1/2, convention de REW et des
                                logiciels de mesure -- c'est celle du TIPE ;
      seuil = 3.0             : seuil litteral, |H|^2 = 10^-0,3 = 0,50119.
    Les deux sont exactes, chacune dans sa convention ; l'ecart vaut 0,11 % sur le
    filtre catalogue, sans portee devant la porte de validation a +/- 5 %. Mais il faut
    CHOISIR, sans quoi deux releves du meme filtre semblent se contredire.

    gain_ref : reference a laquelle les -3 dB sont comptes.
      None (defaut) -> 0 dB absolu (gain 1). C'est la lecture "-3 dB / 0 dB".
      'bande'       -> gain de bande passante K estime au bord de la grille (cote
                       basses frequences pour un passe-bas, hautes pour un passe-haut).
                       C'est la lecture "-3 dB / K", insensible a la perte d'insertion.
      un reel       -> reference imposee (par exemple le K analytique de pole_et_q()).
    Le tableau du § 04.1 montre pourquoi le parametre existe : quand la DCR passe de 0
    a 2 ohm, le repere "-3 dB / 0 dB" DESCEND de 18 % et le repere "-3 dB / K" MONTE de
    10 %, pour la meme realite physique -- pendant que le croisement, lui, ne bouge que
    de 0,8 %.

    f : grille de frequences (ou None si H est une fonction et bande est donnee).
    H : tableau (Nf,) OU fonction f -> H (alors la racine est affinee par dichotomie).
    sens/choix : 'auto' deduit le type de cellule des deux bords de la grille
    (passe-bas -> dernier croisement descendant ; passe-haut -> premier montant).
    toutes=True : retourne toutes les frequences de croisement au lieu d'une seule.

    Retourne un flottant (nan si aucun croisement), ou un tableau si toutes=True.
    """
    if f is None:
        if bande is None:
            raise ValueError("repere_3db : fournir f, ou bien bande si H est une fonction")
        f = _grille(bande)
    f = np.asarray(f, dtype=float)
    if bande is not None:
        m = (f >= bande[0]) & (f <= bande[1])
        f = f[m]
        if not callable(H):
            H = np.asarray(H)[m]
    val = _valeurs(H, f)
    if val.ndim != 1:
        raise ValueError("repere_3db : H doit etre unidimensionnel (un seul design)")

    if gain_ref is None:
        ref_db = 0.0
    elif isinstance(gain_ref, str):
        if gain_ref != 'bande':
            raise ValueError("repere_3db : gain_ref doit etre None, 'bande' ou un reel")
        passe_bas = np.abs(val[0]) > np.abs(val[-1])
        ref_db = _db(val[0] if passe_bas else val[-1])
    else:
        ref_db = 20.0 * np.log10(float(gain_ref))

    if sens == 'auto' or choix == 'auto':
        passe_bas = np.abs(val[0]) > np.abs(val[-1])
        if sens == 'auto':
            sens = 'descendant' if passe_bas else 'montant'
        if choix == 'auto':
            choix = 'dernier' if passe_bas else 'premier'

    cible_db = ref_db - float(seuil)
    g = _db(val) - cible_db
    fct = (lambda x: float(_db(_valeurs(H, np.array([x]))[0]) - cible_db)) if callable(H) else None
    racines = _croisements(f, g, fonction_g=fct, sens=sens)
    if toutes:
        return racines
    if racines.size == 0:
        return float('nan')
    return float(racines[0] if choix == 'premier' else racines[-1])


def frequence_croisement(f, H_1, H_2, G_sub=1.0, G_med=1.0, bande=BANDE_CRITERE,
                         toutes=False, strict=True):
    """f_c -- LA definition gelee du TIPE (§ 04.1), notee aussi f_x.

        f_c = l'unique f de [40 ; 250] Hz telle que |H_pb.G_sub| = |H_ph.G_med|

    Pourquoi celle-la, et pas le pole ni un -3 dB (les quatre candidates ne coincident
    plus des que la self a une DCR ou que la charge n'est pas resistive) :
      (i)   seule insensible a la perte d'insertion, qui deplace les deux "-3 dB
            absolus" sans rien changer au raccord ;
      (ii)  seule interpretable sur la charge reelle, ou |H| culmine a +10,8 dB et ou
            un "-3 dB" tombe 14 dB sous le pic sans plus rien designer de physique ;
      (iii) c'est la grandeur qui gouverne la somme acoustique, donc le critere ;
      (iv)  elle se mesure directement : deux balayages de Bode, on lit l'intersection.

    Valeurs de controle (§ 04.1 et § 04.2), catalogue 18 mH / 150 uF :
        8 ohm, r = 0     -> 96,86 Hz     8 ohm, r = 1 ohm -> 96,66 Hz
        8 ohm, r = 2 ohm -> 96,05 Hz
        charges typiques DIFFERENTES PAR VOIE, jeux illustratifs du § 04.6 --
        Z_sub = Z_ts(f, 6,5 ohm, 1,2 mH, 44 ohm, 40 Hz, 1,75) sur le PASSE-BAS et
        Z_med = Z_ts(f, 6,4 ohm, 0,5 mH, 30 ohm, 60 Hz, 3,0) sur le PASSE-HAUT --
        avec r = 1 ohm -> 102,95 Hz (+6,5 % par rapport aux 96,66 Hz sur 8 ohm).
        (Avec les jeux modele_hp.SUB_TYP / MED_TYP, qui sont d'autres ordres de
        grandeur, le meme calcul rend 78,83 Hz : le chiffre depend de la charge,
        c'est tout le sujet du TIPE.)

    CETTE DERNIERE LIGNE EST PRECISE PARCE QU'ELLE DOIT L'ETRE (correction de relecture
    du 2026-09-14 : elle disait "charge typique" sans dire laquelle, et un lecteur qui
    la reproduisait avec UNE SEULE charge trouvait 96,66 Hz et concluait a un bug).
    Fait exact, et bon point d'oral : pour un design SYMETRIQUE (L1 = L2, C1 = C2)
    charge par la MEME Z sur les deux voies, les deux cellules partagent le meme
    denominateur, le rapport se simplifie en

        |H_PB / H_PH| = |1/(jwC)| / |jwL + r|

    et f_c est alors RIGOUREUSEMENT independante de Z (verifie a 1,4e-14 pres). Le
    croisement ne bouge donc, sur un design symetrique, que si les deux voies voient
    des charges differentes -- ce qui est le cas reel (18 pouces contre bloc medium).
    C'est un argument de plus pour les points (i) et (ii) ci-dessus : de toutes les
    definitions candidates, f_c est la plus stable vis-a-vis de la charge.

    H_1, H_2 : tableaux sur f, ou fonctions f -> H (racine affinee par dichotomie).
    strict=True : leve une erreur si le nombre de croisements n'est pas 1, ce qui est
    le cas ou la notion de "raccord" perd son sens (deux voies qui se croisent trois
    fois ne se raccordent pas). strict=False : avertit et rend le premier.
    toutes=True : rend toutes les solutions.
    """
    if f is None:
        f = _grille(bande)
    f = np.asarray(f, dtype=float)
    m = (f >= bande[0]) & (f <= bande[1])
    fb = f[m]
    v1 = _valeurs(H_1, fb) if callable(H_1) else np.asarray(H_1)[m]
    v2 = _valeurs(H_2, fb) if callable(H_2) else np.asarray(H_2)[m]
    if np.ndim(v1) != 1 or np.ndim(v2) != 1:
        raise ValueError("frequence_croisement : un seul design a la fois")
    g = _db(v1 * G_sub) - _db(v2 * G_med)

    fct = None
    if callable(H_1) and callable(H_2):
        def fct(x):
            xa = np.array([x], dtype=float)
            return float(_db(_valeurs(H_1, xa)[0] * G_sub) - _db(_valeurs(H_2, xa)[0] * G_med))

    racines = _croisements(fb, g, fonction_g=fct, sens='tous')
    if toutes:
        return racines
    if racines.size != 1:
        message = ("frequence_croisement : %d croisement(s) dans %g-%g Hz (attendu 1) ; "
                   "la definition gelee suppose l'unicite" % (racines.size, bande[0], bande[1]))
        if strict:
            raise ValueError(message)
        print("AVERTISSEMENT -- " + message)
        if racines.size == 0:
            return float('nan')
    return float(racines[0])


# ----------------------------------------------------------------------------------
# 6. Critere : ecart RMS en dB a une cible (definition gelee du § 07.9)
# ----------------------------------------------------------------------------------

def grille_critere(f1=BANDE_CRITERE[0], f2=BANDE_CRITERE[1], n_par_octave=N_PAR_OCTAVE):
    """Grille du critere gele : N = round(n_par_octave.log2(f2/f1)) + 1 points
    geometriquement espaces. Pour 40-250 Hz a 24 points/octave : N = 64 (§ 07.9).

    Le pas log signifie que l'on pondere a energie constante PAR FRACTION D'OCTAVE
    (bruit rose) et non par hertz (bruit blanc) : c'est une hypothese, elle pondere
    lourdement le grave et elle change le classement des designs (§ 04.5).
    """
    N = int(round(np.log2(float(f2) / float(f1)) * n_par_octave)) + 1
    return np.geomspace(float(f1), float(f2), N)


def ecart_rms_db(f, S, cible=None, f1=BANDE_CRITERE[0], f2=BANDE_CRITERE[1],
                 n_par_octave=N_PAR_OCTAVE, plancher=PLANCHER_DB, niveau_libre=None,
                 en_db=None):
    """Ecart RMS (dB) d'une courbe a une cible sur [f1, f2] -- CRITERE GELE (§ 07.9).

    Definition, litteralement celle du § 07.9 :
      1. on echantillonne le niveau L(f) sur la grille log a n_par_octave points par
         octave (interpolation lineaire en ln f) ;
      2. on PLAFONNE PAR LE BAS : L~ = max(L, max(L) - plancher), plancher = 20 dB ;
      3. ecart quadratique moyen a la reference :
             eps = racine( moyenne( (L~ - ref)^2 ) )
         avec ref = moyenne(L~) si cible vaut None (cible plate de NIVEAU LIBRE : la
         forme seule est jugee, la constante qui minimise l'ecart est retiree), sinon
         ref = la cible fournie.

    Pourquoi le plancher fait partie du critere et n'est pas un bricolage : quand la
    somme presente un ZERO de transmission dans la bande (Butterworth non inverse,
    exactement), L tend vers moins l'infini et l'ESTIMATEUR DISCRET devient erratique
    -- 1027 dB a 12 points/octave, 7,3 dB a 24, 375 dB a 96, alors que l'integrale
    continue vaut 7,77 dB. Avec le plancher : 5,9 dB a toutes les resolutions. Le
    plancher est aussi physiquement fonde (aucune annulation reelle n'est infinie) et
    sa valeur, 20 dB, est GELEE : 15 dB donnerait 5,0 dB et 30 dB donnerait 7,0 dB.

    f  : frequences de la courbe (quelconques, au moins deux points).
    S  : amplitude COMPLEXE (tableau complexe) ou niveau en dB (tableau reel) ;
         en_db force l'interpretation si besoin.
    cible : None (plate, niveau libre) ; une fonction fk -> dB ; ou un tableau sur f
         (complexe -> converti en dB, reel -> deja en dB), interpole comme la courbe.
    niveau_libre : None (defaut) = True si cible est None, False sinon -- c'est la
         convention gelee. Le forcer a True avec une cible revient a ne juger que la
         forme relative : hors definition gelee, a dire si on l'utilise.

    Retourne (rms, ecart_max_absolu, fk, ek) : les deux premiers en dB, fk la grille,
    ek les ecarts point par point (utiles pour tracer la figure du critere).

    Note d'interface : la fonction ecart_rms() du § 07.9, qui lit une courbe MESUREE
    (export REW) et applique la meme formule, appartient au module d'acoustique. Ici
    on travaille sur des fonctions de transfert calculees ; les deux doivent donner le
    meme nombre sur la meme courbe -- c'est un test croise a ecrire en phase 4.
    """
    f = np.asarray(f, dtype=float)
    S = np.asarray(S)
    if en_db is None:
        en_db = not np.iscomplexobj(S)
    L = np.asarray(S, dtype=float) if en_db else _db(S)
    if L.ndim != 1:
        raise ValueError("ecart_rms_db : une seule courbe a la fois (tableau 1-D)")

    fk = grille_critere(f1, f2, n_par_octave)
    Lk = np.interp(np.log(fk), np.log(f), L)
    if plancher is not None:
        Lk = np.maximum(Lk, Lk.max() - float(plancher))

    if niveau_libre is None:
        niveau_libre = cible is None

    if cible is None:
        ref = np.zeros_like(fk)
    elif callable(cible):
        ref = np.asarray(cible(fk), dtype=float)
    else:
        c = np.asarray(cible)
        c_db = np.asarray(c, dtype=float) if not np.iscomplexobj(c) else _db(c)
        ref = np.interp(np.log(fk), np.log(f), c_db)

    ek = Lk - ref
    if niveau_libre:
        ek = ek - np.mean(ek)
    return float(np.sqrt(np.mean(ek ** 2))), float(np.max(np.abs(ek))), fk, ek


# ----------------------------------------------------------------------------------
# 7. Contraintes physiques : impedance vue par l'ampli, tensions, courants (§ 04.5)
# ----------------------------------------------------------------------------------

def tension_crete_amplificateur(P_max=P_NOM_E800, R_nom=R_NOM):
    """Tension de CRETE a l'entree du filtre, ampli assimile a une source de tension
    limitee par ses rails : V_crete = racine(2).racine(P_max.R_nom).

    350 W sur 8 ohm -> 52,9 V efficaces -> 74,8 V crete (§ 04.2).

    Reserve d'honnetete a garder avec le chiffre : c'est un MAJORANT. A 75 Hz
    l'impedance d'entree du filtre catalogue tombe a 3,5 ohm et le montage tirerait
    15 A ; un E-800 (500 W/4 ohm, soit environ 11 A) ecrete bien avant. La limite
    reelle est fixee par l'enveloppe tension/courant de l'ampli.
    """
    return np.sqrt(2.0) * np.sqrt(float(P_max) * float(R_nom))


def tensions_et_courants(f, design, Z_sub, Z_med=None, V_in=1.0):
    """Toutes les tensions et tous les courants du filtre, pour V_in donnee.

    design : dict avec L1, C1 (voie grave), C2, L2 (voie medium), et en option r1, r2
    (DCR des selfs, 0 par defaut). Z_sub, Z_med : charges des deux voies (Z_med = Z_sub
    si non fournie -- hypothese de travail a corriger des que Z des mediums est
    mesuree). V_in : tension d'entree (efficace ou crete : tout est proportionnel, le
    resultat est dans la meme unite).

    Topologie et relations exactes :
        voie grave  : V_C1 = H_pb.V_in           (C1 est aux bornes du HP)
                      V_L1 = (1 - H_pb).V_in     (le reste de la maille)
                      I_L1 = V_in / Z_in_pb      (courant de la self serie)
                      I_C1 = jwC1.V_C1
        voie medium : V_C2 = (1 - H_ph).V_in     (C2 est en serie)
                      V_L2 = H_ph.V_in           (L2 est aux bornes du HP)
                      I_C2 = jwC2.V_C2 = courant de la voie
                      I_L2 = V_L2 / (jwL2 + r2)

    SECURITE -- c'est la raison d'etre de cette fonction : a la resonance du LC sur la
    charge reelle, |V_C1/V_in| monte a 2,92 et |V_C2/V_in| a 2,16 (modele typique,
    r = 0,5 ohm), soit 154 V et 114 V EFFICACES sous 52,9 V d'entree, donc 218 V et
    162 V CRETE. Un condensateur se specifie en tension continue ou de crete, jamais
    en efficace : il faut du 250 V DC au catalogue. Les "100 V" de la v1 seraient
    detruits, et un 160 V achete sur la foi du "154 V" aussi (§ 04.2).

    Retourne un dict de tableaux complexes (plus Z_in_pb, Z_in_ph, Z_in_parallele).
    """
    f = np.asarray(f, dtype=float)
    w = 2.0 * np.pi * f
    L1 = float(design['L1']); C1 = float(design['C1'])
    C2 = float(design['C2']); L2 = float(design['L2'])
    r1 = float(design.get('r1', 0.0)); r2 = float(design.get('r2', 0.0))
    if Z_med is None:
        Z_med = Z_sub

    h_pb = H_pb(f, L1, C1, Z_sub, r1)
    h_ph = H_ph(f, C2, L2, Z_med, r2)
    Zin_pb = impedance_entree_pb(f, L1, C1, Z_sub, r1)
    Zin_ph = impedance_entree_ph(f, C2, L2, Z_med, r2)

    V_C1 = h_pb * V_in
    V_L1 = (1.0 - h_pb) * V_in
    V_C2 = (1.0 - h_ph) * V_in
    V_L2 = h_ph * V_in
    return dict(f=f, H_pb=h_pb, H_ph=h_ph,
                Z_in_pb=Zin_pb, Z_in_ph=Zin_ph,
                Z_in_parallele=Zin_pb * Zin_ph / (Zin_pb + Zin_ph),
                V_C1=V_C1, V_L1=V_L1, V_C2=V_C2, V_L2=V_L2,
                I_L1=V_in / Zin_pb, I_C1=1j * w * C1 * V_C1,
                I_C2=1j * w * C2 * V_C2, I_L2=V_L2 / (1j * w * L2 + r2),
                I_hp_sub=V_C1 / Z_sub, I_hp_med=V_L2 / Z_med)


def verifier_contraintes(design, P_max=P_NOM_E800, Z=None, f=None, Z_med=None,
                         montage='voie', zin_min=ZIN_MIN_E800, R_nom=R_NOM,
                         detail=False):
    """Controle des contraintes physiques d'un design (§ 04.5, contraintes 2 a 4).

    Signature gelee au § 09.4 : verifier_contraintes(design, P_max, Z) -> les trois
    premiers arguments sont positionnels et dans cet ordre ; les autres sont optionnels.

    design : dict L1, C1, C2, L2 (+ r1, r2 en option). En option aussi V_C1_nom,
             V_C2_nom (tenue en tension CRETE achetee, V) et I_C1_max, I_C2_max
             (courant d'ondulation admissible, A efficaces) : si elles sont fournies,
             elles entrent dans le verdict.
    P_max  : puissance nominale de l'ampli sur R_nom -> tension de crete (majorant).
    Z      : charge. Tableau sur f, fonction f -> Z, ou couple (f, Z).
    f      : grille de frequences si Z est un tableau seul. Par defaut 20-500 Hz, 512
             points log -- la bande sur laquelle le § 04.2 rapporte min|Z_in|.
    montage: qui voit quoi. Trois lectures, toutes les trois dans le dict detaille --
             les comparer est un bon reflexe, car elles ne donnent pas le meme verdict.
             'grave'     -> voie grave seule : c'est EXACTEMENT ce que verifie la
                            fonction de cout gelee du § 04.6, et c'est ce qui donne les
                            3,51 ohm du catalogue.
             'voie'      -> (defaut) le plus petit des deux minimums de voie. Plus
                            severe que le precedent : sur le design optimise du § 04.8
                            (27 mH/10 uF | 120 uF/12 mH) la voie grave remonte bien a
                            11,3 ohm, mais la voie MEDIUM descend a 6,3 ohm -- que la
                            fonction de cout gelee ne regarde pas.
             'parallele' -> les deux cellules en parallele sur UN ampli : c'est le cas
                            physique du filtre passif reel, et il est toujours PLUS
                            BAS. Pour le catalogue sur la charge synthetique il donne
                            2,57 ohm, la ou la voie grave seule en donne 3,51 : la
                            disqualification du catalogue est donc encore plus nette
                            que ne le dit le § 04.8. [[a trancher en phase 3 : quelle
                            lecture entre dans la penalite dure de J]]
    Attention a la bande : le minimum de la voie MEDIUM tombe souvent sur la borne
    HAUTE de la grille (le condensateur serie devient un court-circuit et l'ampli voit
    le haut-parleur presque nu), donc ce chiffre depend de f. Celui de la voie grave,
    lui, est un vrai minimum interieur (77 Hz pour le catalogue).

    Retourne (V_C_crete, I_L_crete, Zin_min, ok) :
      V_C_crete : dict {'C1', 'C2'} des tensions de CRETE aux bornes des condensateurs
                  sous V_in de crete (les valeurs efficaces, divisees par racine(2),
                  sont dans le dict detaille) ;
      I_L_crete : dict {'L1', 'L2'} des courants de CRETE dans les selfs ;
      Zin_min   : minimum de |Z_in| sur la bande (ohm) ;
      ok        : booleen, contrainte 4 (Zin_min >= zin_min) et, si les specifications
                  des composants sont fournies, contraintes 2 et 3.
    detail=True : retourne en plus un dict complet (valeurs efficaces, frequences des
    maxima, marges, verdicts par contrainte).

    Rappel du resultat qui n'etait pas prevu (§ 04.8) : cette contrainte DISQUALIFIE le
    filtre catalogue sur la charge typique (3,51 ohm < 4 ohm) AVANT toute comparaison
    de fidelite -- et 162 des 576 couples (L1, C1) de la grille E12 la violent deja sur
    8 ohm resistif. Ce n'est pas un cas pathologique isole.
    """
    if isinstance(Z, tuple) and len(Z) == 2 and not np.isscalar(Z[0]):
        f, Z = Z
    if f is None:
        f = np.geomspace(20.0, 500.0, 512)
    f = np.asarray(f, dtype=float)
    Z_sub = _valeurs(Z, f) if callable(Z) else np.asarray(Z)
    Z_m = None if Z_med is None else (_valeurs(Z_med, f) if callable(Z_med) else np.asarray(Z_med))

    V_crete = tension_crete_amplificateur(P_max, R_nom)
    g = tensions_et_courants(f, design, Z_sub, Z_m, V_in=V_crete)

    mod = lambda x: np.abs(np.asarray(x))
    V_C = {'C1': float(mod(g['V_C1']).max()), 'C2': float(mod(g['V_C2']).max())}
    I_L = {'L1': float(mod(g['I_L1']).max()), 'L2': float(mod(g['I_L2']).max())}
    I_C = {'C1': float(mod(g['I_C1']).max()), 'C2': float(mod(g['I_C2']).max())}

    zin_grave = float(mod(g['Z_in_pb']).min())
    zin_medium = float(mod(g['Z_in_ph']).min())
    zin_voie = min(zin_grave, zin_medium)
    zin_par = float(mod(g['Z_in_parallele']).min())
    try:
        Zin_min = {'grave': zin_grave, 'voie': zin_voie, 'parallele': zin_par}[montage]
    except KeyError:
        raise ValueError("verifier_contraintes : montage doit valoir "
                         "'grave', 'voie' ou 'parallele' (recu '%s')" % montage) from None

    verdicts = {'impedance': bool(Zin_min >= zin_min)}
    for c in ('C1', 'C2'):
        v_nom = design.get('V_%s_nom' % c)
        if v_nom is not None:
            verdicts['tension_%s' % c] = bool(V_C[c] <= float(v_nom))
        i_max = design.get('I_%s_max' % c)
        if i_max is not None:
            verdicts['courant_%s' % c] = bool(I_C[c] / np.sqrt(2.0) <= float(i_max))
    ok = all(verdicts.values())

    if not detail:
        return V_C, I_L, Zin_min, ok

    arg = lambda x: float(f[int(np.argmax(mod(x)))])
    d = dict(V_C_crete=V_C, I_L_crete=I_L, I_C_crete=I_C,
             V_C_efficace={k: v / np.sqrt(2.0) for k, v in V_C.items()},
             I_L_efficace={k: v / np.sqrt(2.0) for k, v in I_L.items()},
             I_C_efficace={k: v / np.sqrt(2.0) for k, v in I_C.items()},
             f_max_V_C1=arg(g['V_C1']), f_max_I_L1=arg(g['I_L1']),
             Zin_min=Zin_min, Zin_min_voie=zin_voie, Zin_min_parallele=zin_par,
             Zin_min_grave=zin_grave, Zin_min_medium=zin_medium,
             f_Zin_min=float(f[int(np.argmin(mod(g['Z_in_pb'])))]),
             f_Zin_min_medium=float(f[int(np.argmin(mod(g['Z_in_ph'])))]),
             V_in_crete=V_crete, V_in_efficace=V_crete / np.sqrt(2.0),
             verdicts=verdicts, ok=ok, montage=montage)
    return V_C, I_L, Zin_min, ok, d


def pertes_joule_dcr(f, design, Z_sub, Z_med=None, P_ref=10.0, R_nom=R_NOM,
                     bande=BANDE_CRITERE):
    """Puissance Joule moyenne de bande dissipee dans les DCR des deux selfs (W),
    sous la tension de reference V_ref = racine(R_nom.P_ref) (§ 04.5, terme w_W).

    P_ref = 10 W est une puissance de REFERENCE CONVENTIONNELLE sur 8 ohm
    (V_ref = 8,94 V), pas la puissance reellement delivree a la charge : sur la charge
    reelle le filtre catalogue dissipe 2,20 W pour ce P_ref, soit 22 % -- et la part de
    r1 dans la puissance ACTIVE de la voie grave atteint 33 % a 100 Hz (§ 04.2). La
    charge reelle aggrave donc aussi la facture energetique de la DCR.

    La moyenne est prise sur la grille fournie (log par defaut) : moyenne de BANDE, a
    ne pas confondre avec la perte de POINTE, qui est ce qui dimensionne le fil de la
    self (6,5 W de pointe contre 2,20 W de moyenne au niveau d'ecoute gele).

    Retourne (P_totale, P_r1, P_r2) en W.
    """
    f = np.asarray(f, dtype=float)
    m = (f >= bande[0]) & (f <= bande[1])
    V_ref = np.sqrt(float(R_nom) * float(P_ref))
    g = tensions_et_courants(f, design, Z_sub, Z_med, V_in=V_ref)
    r1 = float(design.get('r1', 0.0)); r2 = float(design.get('r2', 0.0))
    P1 = float(np.mean(np.abs(g['I_L1'][m]) ** 2 * r1))
    P2 = float(np.mean(np.abs(g['I_L2'][m]) ** 2 * r2))
    return P1 + P2, P1, P2


# ----------------------------------------------------------------------------------
# 8. Export LTspice : "comment savez-vous que votre code est juste ?" (§ 04.10)
# ----------------------------------------------------------------------------------

def _spice(x):
    """Formate un nombre en notation SPICE (18,0063 mH -> '18.0063m').

    On evite volontairement le suffixe 'F' (femto en SPICE, pas farad) et 'M'
    (milli, PAS mega : mega s'ecrit 'MEG') -- ce sont les deux pieges classiques.
    """
    x = float(x)
    if x == 0.0:
        return '0'
    for seuil, suffixe in ((1e3, 'k'), (1.0, ''), (1e-3, 'm'), (1e-6, 'u'),
                           (1e-9, 'n'), (1e-12, 'p')):
        if abs(x) >= seuil:
            return ('%.6g' % (x / seuil)) + suffixe
    return '%.6g' % x


def _rlc_motionnel(p):
    """(Re, Le, Res, Les, Ces) a partir d'un dict T-S (Re, Le, Res, fs, Qms) ou
    (Re, Le, Res, Les, Ces). Les = Res/(ws.Qms) et Ces = Qms/(ws.Res) -- voir § 04.2.
    """
    Re, Le, Res = float(p['Re']), float(p['Le']), float(p['Res'])
    if 'Les' in p and 'Ces' in p:
        return Re, Le, Res, float(p['Les']), float(p['Ces'])
    ws = 2.0 * np.pi * float(p['fs'])
    Qms = float(p['Qms'])
    return Re, Le, Res, Res / (ws * Qms), Qms / (ws * Res)


def _rlc_event(p, Les):
    """(Rp, Lceb, Cpeb) de la branche EVENT d'un bass-reflex, ou None (§ 01.10).

    Le dict du sub porte f_b, Q_l et alpha des que l'acte 2 a retenu un modele a
    deux pics. Sans cette branche, la netlist LTspice decrirait une caisse CLOSE
    en pretendant decrire la charge identifiee : la contre-verification
    comparerait alors deux circuits differents et "prouverait" un desaccord qui
    n'existe pas -- ou pire, masquerait un vrai.

    Cote electrique, la compliance de caisse et la masse d'air de l'event forment
    une branche SERIE R_p + L_ceb + C_peb qui SHUNTE la branche motionnelle :
    L_ceb = L_ces/alpha, C_peb = 1/(w_b^2 L_ceb), R_p = w_b L_ceb / Q_l.
    """
    if 'fb' not in p or 'Ql' not in p:
        return None
    alpha = float(p.get('alpha', 1.0))
    wb = 2.0 * np.pi * float(p['fb'])
    Lceb = float(Les) / alpha
    return wb * Lceb / float(p['Ql']), Lceb, 1.0 / (wb ** 2 * Lceb)


def exporter_netlist(design, Z_rlc, chemin, voies='les_deux', ac='oct 48 10 10k',
                     titre=None, commentaire=None):
    """Ecrit la netlist LTspice du filtre charge par le modele T-S (§ 04.10).

    FEUILLE-DE-ROUTE impose "LTspice en contre-verification", et le § 08 s'en prevaut
    devant le jury : le sanity check sur 8 ohm prouve que le code Python retrouve les
    formules analytiques sur charge resistive, PAS qu'il traite correctement une charge
    complexe. La superposition des deux courbes ferme la question.

    design : dict L1, C1, C2, L2 (+ r1, r2). Les DCR sont ecrites comme des resistances
             SERIE explicites -- elles font partie du circuit, pas d'un reglage.
    Z_rlc  : dict T-S du sub, ou couple (dict_sub, dict_med). Cles : Re, Le, Res et
             (fs, Qms) ou (Les, Ces). La branche motionnelle est un RLC PARALLELE
             accorde sur fs. Si le dict porte EN PLUS fb, Ql (et alpha), la charge
             est ecrite en BASS-REFLEX : la branche event R_p + L_ceb + C_peb est
             ajoutee en shunt de la branche motionnelle (§ 01.10). C'est ce qui
             permet a la netlist de decrire la charge REELLEMENT identifiee a
             l'acte 2, et non une caisse close qui lui ressemblerait.
    voies  : 'les_deux' (defaut), 'pb' ou 'ph'. Les deux voies sont ecrites comme deux
             circuits galvaniquement separes avec chacun sa source AC 1 : une seule
             simulation .ac donne V(hp_pb) et V(hp_ph).

    Valeurs a retrouver sous LTspice (calculees par ce module, charge typique
    SYNTHETIQUE, 18 mH / 150 uF, r1 = 1 ohm) : |H_pb| = +7,97 dB a 75 Hz, +0,73 dB a
    100 Hz, -17,87 dB a 250 Hz, phase -131,5 degres a 100 Hz.

    Retourne le texte ecrit (fichier en UTF-8, fins de ligne LF).
    """
    p_sub, p_med = (Z_rlc if isinstance(Z_rlc, (tuple, list)) else (Z_rlc, Z_rlc))
    L1 = float(design['L1']); C1 = float(design['C1'])
    C2 = float(design['C2']); L2 = float(design['L2'])
    r1 = float(design.get('r1', 0.0)); r2 = float(design.get('r2', 0.0))

    lignes = ['* ' + (titre or "Filtre de raccord -- netlist generee par analyse/filtre.py"),
              "* Voir REFERENCE-TECHNIQUE.md § 04.10 (contre-verification LTspice).",
              "* Charge = modele de Thiele-Small ; PARAMETRES A ETIQUETER (mesures ? typiques ?)."]
    if commentaire:
        lignes += ['* ' + l for l in str(commentaire).splitlines()]

    def bloc(prefixe, noeud_in, p, index):
        Re, Le, Res, Les, Ces = _rlc_motionnel(p)
        fs_ctrl = 1.0 / (2.0 * np.pi * np.sqrt(Les * Ces))
        Qms_ctrl = Res * np.sqrt(Ces / Les)
        lignes_bloc = [
            "Re%s %s e%s %s" % (index, noeud_in, index, _spice(Re)),
            "Le%s e%s n%s %s" % (index, index, index, _spice(Le)),
            "Res%s n%s 0 %s" % (index, index, _spice(Res)),
            "Les%s n%s 0 %s" % (index, index, _spice(Les)),
            "Ces%s n%s 0 %s   ; controle : fs = %.3f Hz, Qms = %.4f"
            % (index, index, _spice(Ces), fs_ctrl, Qms_ctrl)]
        event = _rlc_event(p, Les)
        if event is not None:
            Rp, Lceb, Cpeb = event
            lignes_bloc += [
                "* branche EVENT (bass-reflex) : shunte la branche motionnelle",
                "Rp%s n%s b%s %s" % (index, index, index, _spice(Rp)),
                "Lceb%s b%s c%s %s" % (index, index, index, _spice(Lceb)),
                "Cpeb%s c%s 0 %s   ; accord fb = %.3f Hz, Ql = %.3f, alpha = %.3f"
                % (index, index, _spice(Cpeb), float(p['fb']), float(p['Ql']),
                   float(p.get('alpha', 1.0)))]
        return lignes_bloc

    if voies in ('les_deux', 'pb'):
        lignes += ["", "* --- Voie grave : L1 (+ DCR r1) serie, C1 parallele ---",
                   "V1 in1 0 AC 1",
                   "L1 in1 m1 %s" % _spice(L1),
                   "Rd1 m1 hp1 %s   ; DCR de la self, en serie" % _spice(r1) if r1 else
                   "Rd1 m1 hp1 1e-9   ; DCR nulle (court-circuit numerique)",
                   "C1 hp1 0 %s" % _spice(C1)]
        lignes += bloc('pb', 'hp1', p_sub, '1')
    if voies in ('les_deux', 'ph'):
        lignes += ["", "* --- Voie medium : C2 serie, L2 (+ DCR r2) parallele ---",
                   "V2 in2 0 AC 1",
                   "C2 in2 hp2 %s" % _spice(C2),
                   "L2 hp2 m2 %s" % _spice(L2),
                   "Rd2 m2 0 %s   ; DCR de la self, en serie" % _spice(r2) if r2 else
                   "Rd2 m2 0 1e-9   ; DCR nulle (court-circuit numerique)"]
        lignes += bloc('ph', 'hp2', p_med, '2')
    lignes += ["", ".ac %s" % ac, ".end", ""]

    texte = '\n'.join(lignes)
    with open(chemin, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(texte)
    return texte


# ----------------------------------------------------------------------------------
# 9. Auto-test : reproduction des valeurs de controle du § 04
# ----------------------------------------------------------------------------------

def _z_ts_local(f, Re, Le, Res, fs, Qms):
    """Duplicata LOCAL de modele_hp.Z_ts, pour que l'auto-test tourne meme si
    modele_hp.py n'est pas encore ecrit. modele_hp fait foi ; l'auto-test verifie que
    les deux coincident quand le module est importable."""
    f = np.asarray(f, dtype=float)
    w = 2.0 * np.pi * f
    ws = 2.0 * np.pi * fs
    Les = Res / (ws * Qms)
    Ces = Qms / (ws * Res)
    return Re + 1j * w * Le + 1.0 / (1.0 / Res + 1.0 / (1j * w * Les) + 1j * w * Ces)


# Parametres SYNTHETIQUES, heritee de archive-v1/_gen.py : ordre de grandeur d'un
# 18" et d'un bloc de deux mediums 4 ohm en serie. CE NE SONT PAS DES MESURES.
_SUB_SYNTH = dict(Re=6.5, Le=1.2e-3, Res=44.0, fs=40.0, Qms=1.75)
_MED_SYNTH = dict(Re=6.4, Le=0.5e-3, Res=30.0, fs=60.0, Qms=3.0)


def _autotest():
    """Rejoue les valeurs de controle du § 04 et affiche l'attendu en regard."""
    import sys
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    ok_global = [True]

    def verifie(nom, obtenu, attendu, tol):
        bon = abs(obtenu - attendu) <= tol
        ok_global[0] = ok_global[0] and bon
        return "%s %-46s %12.6g  [attendu %-10.6g tol %.3g]" % (
            "OK  " if bon else "ECHEC", nom, obtenu, attendu, tol)

    print("=" * 92)
    print("filtre.py -- auto-test : valeurs de controle de REFERENCE-TECHNIQUE.md § 04")
    print("=" * 92)

    # --- 1. Sanity check 8 ohm : les formules exactes redonnent le Butterworth -------
    print("\n1. Charge 8 ohm resistive, DCR nulle : les cellules exactes = la forme normalisee")
    f = np.geomspace(20.0, 1000.0, 1201)
    L_b, C_b = composants_canoniques('butterworth', 100.0, 8.0)
    L_lr, C_lr = composants_canoniques('lr2', 100.0, 8.0)
    print(verifie("L Butterworth (H)", L_b, 18.0063e-3, 1e-7))
    print(verifie("C Butterworth (F)", C_b, 140.674e-6, 1e-9))
    print(verifie("L LR2 (H)", L_lr, 25.4648e-3, 1e-7))
    print(verifie("C LR2 (F)", C_lr, 99.472e-6, 1e-9))
    h_pb = H_pb(f, L_b, C_b, 8.0 + 0j, 0.0)
    h_ph = H_ph(f, C_b, L_b, 8.0 + 0j, 0.0)
    Hc_pb, Hc_ph = cible(f, 'butterworth', 100.0)
    print(verifie("ecart max |H_pb exact - Butterworth|",
                  float(np.max(np.abs(h_pb - Hc_pb))), 0.0, 1e-14))
    print(verifie("ecart max |H_ph exact - Butterworth|",
                  float(np.max(np.abs(h_ph - Hc_ph))), 0.0, 1e-14))
    fx = frequence_croisement(f, h_pb, h_ph)
    print(verifie("f_c croisement (Hz)", fx, 100.0, 1e-3))
    _, Q_b, _ = pole_et_q(L_b, C_b, 8.0)
    print(verifie("Q", Q_b, 1.0 / np.sqrt(2.0), 1e-9))
    for freq, att_pb, att_ph in ((50.0, -0.26, -12.30), (100.0, -3.01, -3.01),
                                 (200.0, -12.30, -0.26), (1000.0, -40.00, -0.00)):
        a = float(_db(H_pb(np.array([freq]), L_b, C_b, 8.0 + 0j)[0]))
        b = float(_db(H_ph(np.array([freq]), C_b, L_b, 8.0 + 0j)[0]))
        print("       f = %6.0f Hz : PB %7.2f dB [%6.2f]   PH %7.2f dB [%6.2f]"
              % (freq, a, att_pb, b, att_ph))

    # --- 2. Filtre catalogue 18 mH / 150 uF : pole, Q, et les DEUX conventions -------
    print("\n2. Catalogue 18 mH / 150 uF sur 8 ohm : le pole, Q, et les deux conventions de seuil")
    L0, C0 = 18e-3, 150e-6
    f0, Q0, K0 = pole_et_q(L0, C0, 8.0)
    print(verifie("pole f0 (Hz)", f0, 96.859, 1e-2))
    print(verifie("Q = R.racine(C/L)", Q0, 0.7303, 1e-3))
    fin = np.geomspace(40.0, 250.0, 20001)
    h_pb0 = H_pb(fin, L0, C0, 8.0 + 0j)
    h_ph0 = H_ph(fin, C0, L0, 8.0 + 0j)
    for seuil, att_pb, att_ph, nom in ((SEUIL_MI_PUISSANCE, 99.931, 93.881, "mi-puissance 3,0103 dB"),
                                       (SEUIL_LITTERAL, 99.820, 93.985, "litteral     3,000  dB")):
        a = repere_3db(fin, h_pb0, seuil=seuil)
        b = repere_3db(fin, h_ph0, seuil=seuil)
        print("   %s : f3_pb = %7.3f Hz [%7.3f]  f3_ph = %7.3f Hz [%7.3f]  produit/f0^2 = %.9f"
              % (nom, a, att_pb, b, att_ph, a * b / f0 ** 2))
        ok_global[0] = ok_global[0] and abs(a - att_pb) < 5e-3 and abs(b - att_ph) < 5e-3
        ok_global[0] = ok_global[0] and abs(a * b / f0 ** 2 - 1.0) < 1e-6
        ana = reperes_3db_ideaux(L0, C0, 8.0, seuil)
        print("        forme analytique : %7.3f / %7.3f Hz  (ecart numerique %.2e Hz)"
              % (ana['f3_pb'], ana['f3_ph'], max(abs(ana['f3_pb'] - a), abs(ana['f3_ph'] - b))))
        ok_global[0] = ok_global[0] and abs(ana['f3_pb'] - a) < 1e-3

    # --- 3. Effet de la DCR : le tableau du § 04.1 ------------------------------------
    print("\n3. Effet de la DCR sur charge 8 ohm (tableau § 04.1) : le croisement ne bouge pas")
    print("   r(ohm)  K(dB)[att]      f0(Hz)[att]   Q[att]     f3/0dB[att]   f3/K[att]    f_c[att]")
    table = ((0.0, 0.00, 96.9, 0.730, 99.9, 99.9, 96.86),
             (0.5, -0.53, 99.8, 0.728, 96.7, 102.8, 96.81),
             (1.0, -1.02, 102.7, 0.726, 92.8, 105.4, 96.66),
             (2.0, -1.94, 108.3, 0.720, 81.5, 110.3, 96.05))
    fl = np.geomspace(20.0, 400.0, 40001)
    for r, aK, af0, aQ, a30, a3K, afc in table:
        fr0, Qr, Kr = pole_et_q(L0, C0, 8.0, r)
        hp = H_pb(fl, L0, C0, 8.0 + 0j, r)
        hh = H_ph(fl, C0, L0, 8.0 + 0j, r)
        f30 = repere_3db(fl, hp, gain_ref=None)
        f3K = repere_3db(fl, hp, gain_ref=Kr)
        fc = frequence_croisement(fl, hp, hh)
        print("   %4.1f  %6.2f[%5.2f]  %7.2f[%5.1f]  %.4f[%.3f]  %6.1f[%5.1f]  %6.1f[%5.1f]  %6.2f[%5.2f]"
              % (r, 20 * np.log10(Kr), aK, fr0, af0, Qr, aQ, f30, a30, f3K, a3K, fc, afc))
        ok_global[0] = ok_global[0] and abs(fc - afc) < 0.02 and abs(f30 - a30) < 0.15

    # --- 4. Cibles et sommation -------------------------------------------------------
    print("\n4. Cibles de sommation (decision D2 : la cible est un parametre)")
    fc_g = grille_critere()
    print(verifie("taille de la grille du critere", float(fc_g.size), 64.0, 0.0))
    for nom in CIBLES:
        Sc = cible_somme(fc_g, nom, 100.0, pol=-1)
        Hp, Hh = cible(fc_g, nom, 100.0)
        S_pol_plus = sommer(fc_g, Hp, Hh, pol=+1)
        i100 = int(np.argmin(np.abs(fc_g - 100.0)))
        print("   %-12s : |S(f_x)| = %+6.3f dB   ecart-type de |S| sur la bande = %.3e dB"
              "   |S| sans inversion a f_x = %+8.2f dB"
              % (nom, _db(Sc[i100]), float(np.std(_db(Sc))), _db(S_pol_plus[i100])))
    S_but = cible_somme(fc_g, 'butterworth', 100.0)
    S_lr2 = cible_somme(fc_g, 'lr2', 100.0)
    S_pla = cible_somme(fc_g, 'plate', 100.0)
    print(verifie("Butterworth inverse : |S| a f_x (dB)", float(_db(S_but[32])), 3.0103, 2e-3))
    print(verifie("LR2 inverse : platitude max (dB)", float(np.max(np.abs(_db(S_lr2)))), 0.0, 1e-12))
    print(verifie("|cible lr2| - |cible plate| max (dB)",
                  float(np.max(np.abs(_db(S_lr2) - _db(S_pla)))), 0.0, 1e-12))
    rms_but_plate = ecart_rms_db(fc_g, S_but, cible=np.zeros_like(fc_g))[0]
    rms_but_libre = ecart_rms_db(fc_g, S_but, cible=None)[0]
    print(verifie("ecart RMS Butterworth vs cible 0 dB", rms_but_plate, 2.29, 5e-3))
    print(verifie("ecart RMS Butterworth, niveau libre", rms_but_libre, 0.60, 5e-3))
    Hp, Hh = cible(fc_g, 'butterworth', 100.0)
    S_meme_pol = sommer(fc_g, Hp, Hh, pol=+1)
    print(verifie("ecart RMS meme polarite (zero de transmission, plancher 20 dB)",
                  ecart_rms_db(fc_g, S_meme_pol, cible=None)[0], 5.91, 2e-2))
    sans_plancher = ecart_rms_db(fc_g, S_meme_pol, cible=None, plancher=None)[0]
    print("   sans plancher, meme courbe : %.2f dB  [7,26 attendu] -- estimateur erratique," % sans_plancher)
    print("   d'ou le plancher gele a 20 dB (a 12 pts/octave, sans plancher : 1027 dB)")

    # --- 5. Retard entre centres acoustiques ------------------------------------------
    print("\n5. Retard acoustique (§ 04.2) : 0,50 m entre centres a 100 Hz")
    tau = tau_de_ecart(0.50)
    dphi = 360.0 * 100.0 * tau
    f100 = np.array([100.0])
    perte = _db(sommer(f100, np.array([1.0 + 0j]), np.array([1.0 + 0j]), pol=+1, tau=tau)[0] / 2.0)
    print(verifie("dephasage a 100 Hz (degres)", dphi, 52.5, 0.5))
    print(verifie("perte sur la somme dans l'axe (dB)", float(perte), -0.93, 0.02))

    # --- 6. Charge SYNTHETIQUE : les valeurs du § 04.2 et § 04.10 ----------------------
    print("\n6. Charge SYNTHETIQUE (parametres typiques, PAS une mesure) : § 04.2 et § 04.10")
    try:
        from modele_hp import Z_ts as Z_ts_officiel
        ecart = float(np.max(np.abs(Z_ts_officiel(np.array([40.0, 100.0]), **_SUB_SYNTH)
                                    - _z_ts_local(np.array([40.0, 100.0]), **_SUB_SYNTH))))
        print("   modele_hp importe : ecart max avec le duplicata local = %.2e ohm" % ecart)
    except Exception as exc:
        print("   modele_hp non importable (%s) : duplicata local utilise" % type(exc).__name__)
    fg = np.geomspace(20.0, 2000.0, 40001)
    Zs = _z_ts_local(fg, **_SUB_SYNTH)
    Zm = _z_ts_local(fg, **_MED_SYNTH)
    print("   f (Hz)      40      50      70      75     100     140     200     250    1000")
    ctrl_Z = (50.50, 39.68, 22.40, 20.24, 14.10, 10.21, 8.00, 7.23, 9.23)
    ctrl_H = (1.32, 3.06, 7.68, 7.97, 0.73, -7.74, -14.37, -17.87, -39.76)
    ctrl_p = (-8.5, -14.9, -54.0, -73.1, -131.5, -145.3, -148.2, -149.2, -174.4)
    fpts = np.array([40, 50, 70, 75, 100, 140, 200, 250, 1000], dtype=float)
    Zp = _z_ts_local(fpts, **_SUB_SYNTH)
    Hp1 = H_pb(fpts, L0, C0, Zp, 1.0)
    print("   |Z| calc %s" % ''.join("%8.2f" % v for v in np.abs(Zp)))
    print("   |Z| ref  %s" % ''.join("%8.2f" % v for v in ctrl_Z))
    print("   H_pb dB  %s" % ''.join("%8.2f" % v for v in _db(Hp1)))
    print("   ref      %s" % ''.join("%8.2f" % v for v in ctrl_H))
    print("   phase    %s" % ''.join("%8.1f" % v for v in np.degrees(np.angle(Hp1))))
    print("   ref      %s" % ''.join("%8.1f" % v for v in ctrl_p))
    ok_global[0] = ok_global[0] and np.max(np.abs(np.abs(Zp) - np.array(ctrl_Z))) < 0.02
    ok_global[0] = ok_global[0] and np.max(np.abs(_db(Hp1) - np.array(ctrl_H))) < 0.02

    hpb1 = H_pb(fg, L0, C0, Zs, 1.0)
    hph1 = H_ph(fg, C0, L0, Zm, 1.0)
    print(verifie("f_c sur charge synthetique, r = 1 ohm (Hz)",
                  frequence_croisement(fg, hpb1, hph1), 102.95, 0.02))
    hpb0 = H_pb(fg, L0, C0, Zs, 0.0)
    print(verifie("max |H_pb| sans DCR (dB)", float(np.max(_db(hpb0))), 10.85, 0.02))
    print(verifie("max |H_pb| avec r = 1 ohm (dB)", float(np.max(_db(hpb1))), 7.99, 0.02))
    print(verifie("f(-3 dB / 0 dB) du PB, r = 1 ohm (Hz)",
                  repere_3db(fg, hpb1, gain_ref=None, bande=(40.0, 400.0)), 114.3, 0.1))

    # --- 7. Contraintes : le catalogue est DISQUALIFIE ---------------------------------
    print("\n7. Contraintes physiques sur la charge synthetique (§ 04.2, § 04.5)")
    design = dict(L1=L0, C1=C0, C2=C0, L2=L0, r1=1.0, r2=1.0)
    V_C, I_L, Zin, ok, d = verifier_contraintes(design, 350.0, Zs, f=fg, Z_med=Zm, detail=True)
    print("   V_in : %.1f V efficaces, %.1f V crete" % (d['V_in_efficace'], d['V_in_crete']))
    print(verifie("min |Z_in| voie grave (ohm)", d['Zin_min_grave'], 3.51, 0.02))
    print("   trois lectures : voie grave %.2f ohm a %.0f Hz [3,51 a 77 Hz] | voie medium %.2f ohm"
          " a %.0f Hz (borne de bande) | les deux en PARALLELE sur un seul ampli %.2f ohm"
          % (d['Zin_min_grave'], d['f_Zin_min'], d['Zin_min_medium'], d['f_Zin_min_medium'],
             d['Zin_min_parallele']))
    print(verifie("I_L1 efficace maximal (A)", d['I_L_efficace']['L1'], 15.1, 0.1))
    print(verifie("I_C1 efficace maximal (A)", d['I_C_efficace']['C1'], 9.4, 0.1))
    print("   verdict : ok = %s  (contrainte 4 : min|Z_in| = %.2f ohm < %.1f ohm -> le filtre"
          " CATALOGUE est disqualifie)" % (ok, Zin, ZIN_MIN_E800))
    ok_global[0] = ok_global[0] and (ok is False)
    design05 = dict(design, r1=0.5, r2=0.5)
    g05 = tensions_et_courants(fg, design05, Zs, Zm, V_in=1.0)
    print(verifie("max |V_C1/V_in| (r = 0,5 ohm)", float(np.max(np.abs(g05['V_C1']))), 2.92, 0.02))
    print(verifie("max |V_C2/V_in| (r = 0,5 ohm)", float(np.max(np.abs(g05['V_C2']))), 2.16, 0.02))
    V_eff = 52.9
    print("   -> %.0f V efficaces sur C1 et %.0f V sur C2 sous %.1f V efficaces, soit %.0f et"
          " %.0f V CRETE : 250 V DC au catalogue, pas 100 V ni 160 V."
          % (np.max(np.abs(g05['V_C1'])) * V_eff, np.max(np.abs(g05['V_C2'])) * V_eff, V_eff,
             np.max(np.abs(g05['V_C1'])) * V_eff * np.sqrt(2), np.max(np.abs(g05['V_C2'])) * V_eff * np.sqrt(2)))
    P_tot, P1, P2 = pertes_joule_dcr(fg, design, Zs, Zm, P_ref=10.0)
    print(verifie("pertes Joule DCR moyenne de bande a P_ref = 10 W (W)", P_tot, 2.20, 0.05))

    # --- 8. Zobel ---------------------------------------------------------------------
    print("\n8. Zobel (§ 04.4) : exact sur l'inductance, inoperant sur le pic motionnel")
    Rz, Cz = valeurs_zobel(_SUB_SYNTH['Re'], _SUB_SYNTH['Le'])
    print(verifie("R_z (ohm)", Rz, 6.5, 1e-9))
    print(verifie("C_z (uF)", Cz * 1e6, 28.4, 0.05))
    fz = np.geomspace(10.0, 10000.0, 2001)
    Z_bobine = _SUB_SYNTH['Re'] + 2j * np.pi * fz * _SUB_SYNTH['Le']
    print(verifie("ecart max |(Re+jwLe)//Zobel - Re| (ohm)",
                  float(np.max(np.abs(zobel(Z_bobine, fz, Rz, Cz) - _SUB_SYNTH['Re']))), 0.0, 1e-12))
    f1k = np.array([100.0, 1000.0])
    Zav = _z_ts_local(f1k, **_SUB_SYNTH)
    Zap = zobel(Zav, f1k, Rz, Cz)
    print("   sub synthetique : a 100 Hz %.1f ohm %+.0f deg -> %.1f ohm %+.0f deg [14,1 -> 11,6 ;"
          " -47 -> -54] ; a 1 kHz %.1f -> %.1f ohm"
          % (abs(Zav[0]), np.degrees(np.angle(Zav[0])), abs(Zap[0]), np.degrees(np.angle(Zap[0])),
             abs(Zav[1]), abs(Zap[1])))

    # --- 9. Netlist -------------------------------------------------------------------
    print("\n9. Export LTspice (§ 04.10)")
    import tempfile, os
    chemin = os.path.join(tempfile.gettempdir(), 'filtre_autotest.cir')
    texte = exporter_netlist(design, (_SUB_SYNTH, _MED_SYNTH), chemin,
                             commentaire="Parametres de charge SYNTHETIQUES (non mesures).")
    lignes = texte.splitlines()
    print("   %d lignes ecrites dans %s" % (len(lignes), chemin))
    for l in lignes[4:12]:
        print("     " + l)
    ok_global[0] = ok_global[0] and 'L1 in1 m1 18m' in texte and '.end' in texte

    print("\n" + "=" * 92)
    print("AUTO-TEST : " + ("TOUT PASSE" if ok_global[0] else "AU MOINS UN ECHEC -- ne rien acheter"))
    print("=" * 92)
    return 0 if ok_global[0] else 1


if __name__ == '__main__':
    raise SystemExit(_autotest())
