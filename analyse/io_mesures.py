# -*- coding: utf-8 -*-
"""TIPE filtrage enceinte -- entrees / sorties des mesures d'impedance.

Acte 1 du recit : MESURER Z(f). Ce module ne calcule aucune physique de
haut-parleur (c'est modele_hp) et n'ajuste rien (c'est ts_fit) : il transporte
les donnees sans les abimer, et il refuse de laisser passer un fichier douteux.

Ce qu'il fait
  * lit et ecrit le CSV de mesure "maison" (format gele au § 09.3 de
    REFERENCE-TECHNIQUE.md) : lectures BRUTES (V_d, V_R, dt) ET grandeurs
    derivees (|Z|, phi), plus l'en-tete de conditions ;
  * depouille une acquisition deux voies : |Z| = R_ref |V_d| / |V_R| ,
    phi = 360 f dt  (voie principale de la phase 1, § 02.1) ;
  * importe un export texte REW (§ 02.9) et un CSV d'oscilloscope
    deux voies (§ 09.3), avec detection synchrone non biaisee ;
  * valide un fichier : colonnes presentes, frequences strictement croissantes,
    pas de NaN, incertitudes strictement positives, grille assez serree autour
    du pic, et NOMBRE DE PICS -> type de caisse (clos = 5 parametres,
    bass-reflex = deux pics, modele a 5 parametres inadapte) ;
  * lit analyse/criteres_geles.json et REFUSE de travailler s'il est absent ou
    encore rempli de marques [[a geler]] : le code n'invente pas de criteres.

Pourquoi le fichier porte les lectures brutes (principe 1 du § 09.1)
  Si l'on decouvre apres coup que R_ref valait 99,2 ohm et non 99,7, ou qu'une
  sonde etait en x10, la serie entiere reste exploitable : on rejoue
  depouiller(). Un fichier qui ne porterait que |Z| est un dessin, pas une
  mesure.

Conventions (§ 09.4)
  * tout en SI (ohm, henry, farad, hertz, seconde, volt) ; les mH / uF ne
    servent qu'a l'affichage ;
  * phase POSITIVE pour une charge inductive (§ 02.1), avec
    dt = t(V_Rref) - t(V_dipole) sur deux passages par zero montants ;
  * docstrings et messages en francais SANS ACCENTS, pour rester lisibles dans
    une console Windows cp1252 ; les FICHIERS, eux, sont lus et ecrits en
    UTF-8 explicite ;
  * 9 chiffres significatifs a l'ecriture (aller-retour exact a 4e-9 relatif) ;
  * aucune donnee inventee : le seul fichier de mesure livre dans le depot est
    SYNTHETIQUE et le dit en toutes lettres dans son en-tete.

Signatures gelees (§ 09.4, ligne "entrees")
    lire_mesure(chemin)                              -> (d, meta)
    ecrire_mesure(chemin, d, meta)                   -> chemin
    lire_rew(chemin)                                 -> (f, mod, phi, meta)
    lire_scope(chemin)                               -> (t, v1, v2, meta)
    depouiller_scope(t, v1, v2, f0, R_ref, methode)  -> (mod, phi, A1, A2)

ECART ASSUME AVEC LE PARAGRAPHE 09.2. L'arborescence de reference nomme ce
module 'entrees.py'. Le present fichier porte le nom 'io_mesures.py' impose par
la commande de travail ; les NOMS DE FONCTIONS et les FORMATS, eux, sont ceux
de la specification, a la lettre. Si un autre module attend 'entrees', un
fichier de compatibilite d'une ligne suffit :  from io_mesures import *

Lancement direct
    python analyse/io_mesures.py              -> auto-test (ecriture/relecture,
                                                 fichier casse, signes, criteres)
    python analyse/io_mesures.py --exemple    -> regenere le CSV SYNTHETIQUE
                                                 mesures/exemple_synthetique_sub.csv
"""

import io
import json
import os
import re

import numpy as np

# ---------------------------------------------------------------------------
# Constantes de format (§ 09.3)
# ---------------------------------------------------------------------------

VERSION_FORMAT = 1

#: colonnes de LECTURE (ce que la manip produit reellement)
COLONNES_BRUTES = ('f_Hz', 'V_dipole_V', 'V_Rref_V', 'dt_s')
#: colonnes RECALCULEES a partir des precedentes par depouiller()
COLONNES_DERIVEES = ('module_Z_ohm', 'phase_deg')
#: incertitudes-types ALEATOIRES (k = 1), point par point -> poids du fit
COLONNES_INCERTITUDES = ('u_module_alea_ohm', 'u_phase_deg')
#: les huit colonnes obligatoires, dans l'ordre d'ecriture
COLONNES = COLONNES_BRUTES + COLONNES_DERIVEES + COLONNES_INCERTITUDES

#: en-tete : 14 cles obligatoires (§ 02.12, "en-tete de serie")
META_ORDRE = (
    'version_format',               # entier, pour changer d'avis sans casser
    'date',                         # ISO 8601, ex. 2026-10-05T14:32
    'dipole',                       # sub en caisse / bloc mediums / R / L / C
    'montage',                      # A, B ou C (§ 02.2)
    'R_ref_nominale_ohm',
    'R_ref_mesuree_ohm',            # celle qui entre dans le calcul de |Z|
    'u_R_ref_relative_pct',
    'u_systematique_relative_pct',  # systematique COMMUN a toute la serie
    'niveau_Vd_RMS_V',              # petits signaux (§ 02.5)
    'temperature_C',
    'operateur',
    'appareil',                     # oscilloscope + GBF, ou carte son + REW
    'Re_DC_avant_ohm',
    'Re_DC_apres_ohm',              # ecart avant/apres = echauffement
)
META_OBLIGATOIRES = META_ORDRE

#: cles numeriques : converties en flottant par meta_flottant()
META_NUMERIQUES = (
    'version_format', 'R_ref_nominale_ohm', 'R_ref_mesuree_ohm',
    'u_R_ref_relative_pct', 'u_systematique_relative_pct', 'niveau_Vd_RMS_V',
    'temperature_C', 'Re_DC_avant_ohm', 'Re_DC_apres_ohm',
)

#: une cle = un identifiant, point. Le fullmatch neutralise la ligne de titre
#: et les commentaires libres : aucune cle fantaisiste n'entre dans meta.
CLE = re.compile(r'#\s*([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)')

#: 9 chiffres significatifs : aller-retour exact a 4e-9 EN RELATIF
FORMAT_NOMBRE = '%.9g'

TITRE_DEFAUT = 'TIPE filtrage enceinte -- mesure d impedance'

#: marque d'une decision NON prise, dans criteres_geles.json
MARQUE_NON_GELE = '[['

_ICI = os.path.dirname(os.path.abspath(__file__))
DOSSIER_MESURES = os.path.join(_ICI, 'mesures')
DOSSIER_RESULTATS = os.path.join(_ICI, 'resultats')
CHEMIN_CRITERES = os.path.join(_ICI, 'criteres_geles.json')
CHEMIN_EXEMPLE = os.path.join(DOSSIER_MESURES, 'exemple_synthetique_sub.csv')


# ---------------------------------------------------------------------------
# Exceptions : un message qui dit QUOI faire, pas seulement ce qui a rate
# ---------------------------------------------------------------------------

class ErreurFormatMesure(ValueError):
    """Fichier de mesure hors format (colonne ou metadonnee manquante, NaN...)."""


class CriteresAbsents(FileNotFoundError):
    """criteres_geles.json introuvable : le code n'a pas le droit d'en inventer."""


class CriteresIncomplets(ValueError):
    """criteres_geles.json present mais il y manque des rubriques du schema."""


class CriteresNonGeles(ValueError):
    """criteres_geles.json encore rempli de marques [[a geler]] : rien n'est decide."""


# ---------------------------------------------------------------------------
# Construction et acces aux tableaux de mesure
# ---------------------------------------------------------------------------

def tableau_mesure(**colonnes):
    """Construit le tableau structure numpy d'une serie de mesure.

    Appel typique :
        d = tableau_mesure(f_Hz=f, V_dipole_V=vd, V_Rref_V=vr, dt_s=dt,
                           module_Z_ohm=mod, phase_deg=phi,
                           u_module_alea_ohm=umod, u_phase_deg=uphi)

    Les huit colonnes obligatoires (COLONNES) doivent etre fournies ; toute
    colonne supplementaire est acceptee et sera ecrite telle quelle (par
    exemple V_tot_V, divisions_CH1, calibre_CH1_V_div en montage A -- voir le
    tableau de releve du § 02.12).
    """
    absentes = [c for c in COLONNES if c not in colonnes]
    if absentes:
        raise ErreurFormatMesure('colonnes absentes : ' + ', '.join(absentes))
    noms = list(COLONNES) + [c for c in colonnes if c not in COLONNES]
    valeurs = [np.atleast_1d(np.asarray(colonnes[c], dtype=float)) for c in noms]
    n = len(valeurs[0])
    for nom, v in zip(noms, valeurs):
        if len(v) != n:
            raise ErreurFormatMesure(
                'colonne %s : %d valeurs au lieu de %d' % (nom, len(v), n))
    d = np.zeros(n, dtype=[(nom, float) for nom in noms])
    for nom, v in zip(noms, valeurs):
        d[nom] = v
    return d


def meta_flottant(meta, cle, defaut=None):
    """Lit une metadonnee numerique. Erreur EXPLICITE si elle manque ou n'est
    pas un nombre : une valeur de R_ref lue de travers detruit toute la serie."""
    if cle not in meta:
        if defaut is not None:
            return float(defaut)
        raise ErreurFormatMesure("metadonnee '%s' absente de l en-tete" % cle)
    texte = str(meta[cle]).strip().replace(',', '.')
    try:
        return float(texte)
    except ValueError:
        raise ErreurFormatMesure(
            "metadonnee '%s' : '%s' n est pas un nombre" % (cle, meta[cle]))


def verifier_metadonnees(meta, obligatoires=META_OBLIGATOIRES):
    """Retourne la liste des metadonnees obligatoires manquantes (vide si tout
    est la). Garde-fou du § 09.3 : "metadonnees obligatoires refusees
    si absentes"."""
    return [c for c in obligatoires
            if c not in meta or str(meta[c]).strip() == '']


# ---------------------------------------------------------------------------
# Lecture / ecriture du CSV de mesure "maison"
# ---------------------------------------------------------------------------

def lire_mesure(chemin, valider=False):
    """Lit un CSV de mesure -> (d, meta).

    d    : tableau structure numpy, TOUJOURS 1-D (np.atleast_1d : un fichier
           d'etalonnage a une seule ligne de donnees reste indexable par
           len()) ;
    meta : dict des lignes '# cle: valeur'. Les lignes '#' qui ne sont pas de
           cette forme (titre, commentaire libre, avertissement SYNTHETIQUE)
           sont IGNOREES.

    Erreur explicite si une colonne obligatoire manque ou si version_format est
    absent (fichier hors format). valider=True lance en plus valider_mesure()
    et leve a la premiere erreur.

    Piege numpy documente au § 09.3 : genfromtxt(names=True) prend
    comme ligne de noms la PREMIERE ligne du fichier, commentee ou non -- d'ou
    le decoupage manuel en-tete / corps, qui a de toute facon l'avantage de
    rendre les metadonnees.
    """
    meta, corps = {}, []
    with open(chemin, encoding='utf-8') as fh:
        for ligne in fh:
            if ligne.startswith('#'):
                m = CLE.fullmatch(ligne.strip())
                if m:
                    meta[m.group(1)] = m.group(2).strip()
            elif ligne.strip():
                corps.append(ligne)
    if not corps:
        raise ErreurFormatMesure('%s : aucune ligne de donnees (en-tete seule ?)'
                                 % os.path.basename(chemin))
    d = np.atleast_1d(np.genfromtxt(io.StringIO(''.join(corps)),
                                    delimiter=',', names=True, dtype=float))
    absentes = [c for c in COLONNES if c not in (d.dtype.names or ())]
    if absentes:
        raise ErreurFormatMesure(
            '%s : colonnes absentes : %s (colonnes lues : %s)'
            % (os.path.basename(chemin), ', '.join(absentes),
               ', '.join(d.dtype.names or ())))
    if 'version_format' not in meta:
        raise ErreurFormatMesure('%s : version_format absent -> fichier hors format'
                                 % os.path.basename(chemin))
    if valider:
        erreurs, _ = valider_mesure(d, meta)
        if erreurs:
            raise ErreurFormatMesure('%s :\n  - %s' % (os.path.basename(chemin),
                                                       '\n  - '.join(erreurs)))
    return d, meta


def ecrire_mesure(chemin, d, meta, titre=TITRE_DEFAUT, commentaires=()):
    """Ecrit un CSV de mesure au format du § 09.3 -> chemin ecrit.

    d     : tableau structure (tableau_mesure) ou dict de colonnes ;
    meta  : dict des conditions de manip ; version_format est ajoute d'office ;
    titre : premiere ligne commentee ;
    commentaires : lignes '#' libres supplementaires -- c'est la que va
            l'avertissement "DONNEES SYNTHETIQUES" du fichier d'exemple.

    Les cles connues (META_ORDRE) sont ecrites dans l'ordre canonique, les
    autres ensuite par ordre alphabetique : un diff git reste lisible.
    %.9g partout : l'aller-retour ecriture/lecture est exact a 4e-9 en relatif,
    le fichier grossit de 15 %, et il n'y a plus rien a justifier.
    """
    if isinstance(d, dict):
        d = tableau_mesure(**d)
    noms = list(d.dtype.names)
    absentes = [c for c in COLONNES if c not in noms]
    if absentes:
        raise ErreurFormatMesure('colonnes absentes : ' + ', '.join(absentes))
    ordonnees = list(COLONNES) + [c for c in noms if c not in COLONNES]

    meta = dict(meta)
    meta.setdefault('version_format', VERSION_FORMAT)
    connues = [c for c in META_ORDRE if c in meta]
    autres = sorted(c for c in meta if c not in META_ORDRE)

    dossier = os.path.dirname(os.path.abspath(chemin))
    if dossier and not os.path.isdir(dossier):
        os.makedirs(dossier)
    with open(chemin, 'w', encoding='utf-8', newline='\n') as fh:
        if titre:
            fh.write('# %s\n' % titre)
        for c in commentaires:
            fh.write('# %s\n' % c)
        for cle in connues + autres:
            fh.write('# %s: %s\n' % (cle, meta[cle]))
        fh.write(','.join(ordonnees) + '\n')
        for i in range(len(d)):
            fh.write(','.join(FORMAT_NOMBRE % d[nom][i] for nom in ordonnees) + '\n')
    return chemin


def colonnes_depouillees(d, meta):
    """Vue "CSV depouille" du contrat d'interface avec l'acte 2 (paragraphe
    02.12) : f_Hz, Z_mod_ohm, u_Z_mod_ohm, phi_deg, u_phi_deg, Rref_ohm,
    config, methode, date. Retourne un dict -- c'est une VUE, jamais un
    remplacement du fichier maison, qui porte en plus les lectures brutes."""
    return {
        'f_Hz': d['f_Hz'].copy(),
        'Z_mod_ohm': d['module_Z_ohm'].copy(),
        'u_Z_mod_ohm': d['u_module_alea_ohm'].copy(),
        'phi_deg': d['phase_deg'].copy(),
        'u_phi_deg': d['u_phase_deg'].copy(),
        'Rref_ohm': meta.get('R_ref_mesuree_ohm', meta.get('R_ref_nominale_ohm', '')),
        'config': meta.get('montage', ''),
        'methode': meta.get('appareil', ''),
        'date': meta.get('date', ''),
    }


# ---------------------------------------------------------------------------
# Depouillement : des lectures brutes aux grandeurs derivees
# ---------------------------------------------------------------------------

def u_module_aleatoire(module, R_ref, eps, montage='C'):
    """Incertitude-type ALEATOIRE sur |Z|, en ohm (§ 02.7).

    eps = erreur relative de lecture par voie (desappariement + quantification
    + repetabilite ; objectif 1,4 %, valeur definitive a etablir par un
    type A mesure, pas par un tableau).

    Le prix de la soustraction de phaseurs est un facteur, et c'est LUI qui
    commande le choix de R_ref et du montage :
      montage A (dipole a la masse, V_R deduit)     : sqrt(2)(1 + |Z|/R_ref) eps
      montage B (R_ref a la masse, V_d deduit)      : sqrt(2)(1 + R_ref/|Z|) eps
      montage C (GBF flottant, 2 lectures directes) : sqrt(2) eps, a tout |Z|

    u(R_ref) n'est PAS ici : c'est un SYSTEMATIQUE qui multiplie tous les |Z|
    de la serie. Il vit dans l'en-tete (u_systematique_relative_pct) et
    s'applique apres l'ajustement, en propagation sur theta (§ 03.5).
    Les melanger fausse le chi2, biaise Re et sous-estime les barres d'erreur
    des parametres de Thiele-Small.
    """
    module = np.asarray(module, float)
    lettre = str(montage).strip().upper()[:1]
    if lettre == 'A':
        facteur = 1.0 + module/float(R_ref)
    elif lettre == 'B':
        facteur = 1.0 + float(R_ref)/module
    elif lettre == 'C':
        facteur = np.ones_like(module)
    else:
        raise ValueError("montage inconnu : '%s' (attendu A, B ou C)" % montage)
    return np.sqrt(2.0)*facteur*float(eps)*module


def depouiller(d, meta=None, R_ref_ohm=None, eps_relatif=None,
               u_phase_deg=None, montage=None):
    """Recalcule les colonnes DERIVEES a partir des colonnes BRUTES.

        |Z| = R_ref * V_dipole / V_Rref   (§ 02.1 : un rapport de deux
              tensions sur le MEME courant, exact quel que soit R_ref, aucune
              hypothese de courant constant)
        phi = 360 * f * dt                (dt = t(V_Rref) - t(V_dipole) sur deux
              passages par zero montants -> phi > 0 si la charge est inductive)

    Si eps_relatif est donne, u_module_alea_ohm est recalculee aussi
    (u_module_aleatoire, montage lu dans meta a defaut d'argument) ; si
    u_phase_deg est donne, la colonne d'incertitude de phase est remplie avec
    cette constante. Sinon les colonnes d'incertitude sont laissees telles
    quelles : elles peuvent venir d'une etude de type A point par point.

    Retourne une COPIE : les donnees brutes ne sont jamais reecrites
    (principe 1 du § 09.1).
    """
    meta = {} if meta is None else meta
    if R_ref_ohm is None:
        R_ref_ohm = meta_flottant(meta, 'R_ref_mesuree_ohm')
    R_ref_ohm = float(R_ref_ohm)
    if montage is None:
        montage = str(meta.get('montage', 'C')).strip()[:1] or 'C'

    e = d.copy()
    if np.any(e['V_Rref_V'] == 0.0):
        raise ErreurFormatMesure('V_Rref_V nul : division par zero dans |Z|')
    e['module_Z_ohm'] = R_ref_ohm*e['V_dipole_V']/e['V_Rref_V']
    e['phase_deg'] = 360.0*e['f_Hz']*e['dt_s']
    if eps_relatif is not None:
        e['u_module_alea_ohm'] = u_module_aleatoire(
            e['module_Z_ohm'], R_ref_ohm, eps_relatif, montage)
    if u_phase_deg is not None:
        e['u_phase_deg'] = float(u_phase_deg)
    return e


def depouiller_scope(t, v1, v2, f0, R_ref, methode='lstsq'):
    """Depouillement d'une acquisition 2 voies a la frequence f0.

    Convention § 02 : CH1 = V_dipole, CH2 = V_Rref ; Z = R_ref*A1/A2,
    donc arg(Z) > 0 pour une charge inductive.
    Retourne (|Z|, phase_deg, |A1|, |A2|).

    methode='dft'   : projection sur exp(-2j.pi.f0.t) -- EXACTE seulement si la
                      fenetre contient un nombre ENTIER de periodes de f0 ; on
                      la tronque donc a N periodes.
    methode='lstsq' : moindres carres sur [cos, sin, 1] -- valable pour une
                      fenetre QUELCONQUE, la colonne constante absorbant
                      l'offset continu.

    Pourquoi ce n'est pas cosmetique (§ 09.3) : sur 103,7 ms a 100 Hz
    la dft brute se trompe de +1,9 % sur |Z|, et de -5,5 % au deuxieme point de
    la grille. Une erreur de 5 % ruine l'ajustement de l'acte 2 et depasse a
    elle seule la porte de validation a +/-3 % de la phase 1 -- et elle ne dit
    rien : un estimateur mal conditionne se trompe SANS message d'erreur.
    """
    t = np.asarray(t, float)
    v1 = np.asarray(v1, float)
    v2 = np.asarray(v2, float)
    w = 2*np.pi*float(f0)
    if methode == 'dft':
        N = int(np.floor((t[-1] - t[0])*f0))           # periodes entieres dispo
        if N < 1:
            raise ValueError('fenetre plus courte qu une periode de f0')
        m = t <= t[0] + N/f0 - 0.5*(t[1] - t[0])       # on tronque a N periodes
        e = np.exp(-1j*w*t[m])
        A1, A2 = 2*np.mean(v1[m]*e), 2*np.mean(v2[m]*e)    # phaseurs (crete)
    elif methode == 'lstsq':
        M = np.c_[np.cos(w*t), np.sin(w*t), np.ones_like(t)]
        a1 = np.linalg.lstsq(M, v1, rcond=None)[0]
        a2 = np.linalg.lstsq(M, v2, rcond=None)[0]
        A1, A2 = a1[0] - 1j*a1[1], a2[0] - 1j*a2[1]
    else:
        raise ValueError("methode inconnue : '%s' (attendu 'lstsq' ou 'dft')" % methode)
    Z = float(R_ref)*A1/A2
    return abs(Z), np.degrees(np.angle(Z)), abs(A1), abs(A2)


# ---------------------------------------------------------------------------
# Diagnostics : densite de la grille au pic, et type de caisse
# ---------------------------------------------------------------------------

def _maxima_locaux(y):
    """Indices des maxima locaux (bords exclus)."""
    return [i for i in range(1, len(y) - 1) if y[i] >= y[i-1] and y[i] > y[i+1]]


def _proeminence_relative(y, i):
    """Proeminence d'un maximum local, rapportee a sa hauteur : hauteur
    au-dessus du plus haut des deux cols qui le separent d'un maximum plus
    eleve. C'est ce qui distingue un vrai second pic de bass-reflex d'une
    dentelure de bruit."""
    g = i
    while g > 0 and y[g-1] <= y[i]:
        g -= 1
    d = i
    while d < len(y) - 1 and y[d+1] <= y[i]:
        d += 1
    col = max(y[g:i+1].min(), y[i:d+1].min())
    return (y[i] - col)/y[i]


def diagnostiquer_caisse(f, module, proeminence_min=0.05):
    """Compte les pics de |Z| et en deduit le modele a ajuster.

    Un pic   -> caisse CLOSE : modele de Thiele-Small a 5 parametres
                (Re, Le, Res, fs, Qms), § 01.6.
    Deux pics avec un creux entre eux -> BASS-REFLEX : fL < fb < fH est un
                resultat demontre (§ 01.10), et il faut trois
                parametres de plus (alpha, fb, une perte globale), soit 8 au
                total. Ajuster un modele a 5 parametres sur une courbe a deux
                pics donne un resultat qui CONVERGE et qui est FAUX, sans
                aucun message d'erreur : d'ou cet avertissement.

    Retourne un dict : n_pics, f_pics, z_pics, f_creux, modele, avertissements.

    Le type de caisse du sub est la decision D8 de DECISIONS-PHASE-0.md : un
    CONSTAT a faire en phase 1, pas un choix. Cette fonction est l'outil du
    constat, pas le constat lui-meme.
    """
    f = np.asarray(f, float)
    module = np.asarray(module, float)
    avertissements = []
    idx = [i for i in _maxima_locaux(module)
           if _proeminence_relative(module, i) >= proeminence_min]
    idx.sort(key=lambda i: f[i])

    f_creux = []
    for a, b in zip(idx[:-1], idx[1:]):
        j = a + int(np.argmin(module[a:b+1]))
        f_creux.append(float(f[j]))

    n = len(idx)
    if n == 0:
        modele = 'indetermine'
        avertissements.append(
            'aucun pic detecte : bande trop etroite, grille trop lache ou '
            'dipole non resonant -- verifier la bande de mesure (§ 02.6)')
    elif n == 1:
        modele = 'clos_5_parametres'
    else:
        modele = 'bassreflex_8_parametres'
        avertissements.append(
            '%d pics detectes (%s Hz) et un creux vers %s Hz : la caisse se '
            'comporte en BASS-REFLEX. Un modele a 5 parametres est INADAPTE '
            '(paragraphes 01.6 et 01.10) -- il convergera quand meme, sur des '
            'valeurs fausses.'
            % (n, ', '.join('%.1f' % f[i] for i in idx),
               ', '.join('%.1f' % x for x in f_creux)))
    if n > 2:
        avertissements.append(
            'plus de deux pics : bruit de mesure ou resonance parasite -- '
            'augmenter proeminence_min ou verifier le montage')
    return {
        'n_pics': n,
        'f_pics': [float(f[i]) for i in idx],
        'z_pics': [float(module[i]) for i in idx],
        'f_creux': f_creux,
        'modele': modele,
        'avertissements': avertissements,
    }


def diagnostiquer_grille(f, module, points_min_pic=5):
    """Densite de la grille de frequences dans la largeur du pic principal.

    Largeur retenue : la plage ou la partie MOTIONNELLE de |Z| depasse sa
    valeur au pic divisee par racine(2), c'est-a-dire
    |Z| >= Re + (Zpic - Re)/racine(2), avec Re estime par le minimum de |Z| de
    la serie. Cette largeur vaut environ fs/Qms -- la largeur "a -3 dB" du pic
    au sens usuel. (Le seuil sqrt(Re*Zpic) de la methode r0 de Thiele-Small
    delimite une plage nettement plus large : il sert a ESTIMER Qms, pas a
    juger la densite de la grille.)

    Pourquoi c'est le point qui decide de la qualite de l'acte 2 : la largeur
    relative du pic vaut environ 1/Qms, et un 18 pouces de sono a un Qms de 3 a
    10. Au 1/12 d'octave il ne reste alors que 2,1 points dans la largeur du
    pic (contre 9,6 pour Qms = 1,75) : le fit passe encore, mais sans marge
    (paragraphes 02.6 et 09.6). Le remede coute dix minutes de banc :
    densifier la grille entre fs/2 et 2 fs.

    Retourne un dict : f_pic, z_pic, largeur_Hz, q_estime (= f_pic/largeur, de
    l'ordre de Qms), n_points_pic, avertissements.

    q_estime est BIAISE VERS LE HAUT quand la grille est lache : la largeur est
    mesuree entre les points effectivement presents dans le pic, donc
    sous-estimee (et infinie s'il n'en reste qu'un). C'est un indicateur de
    densite de grille, pas un estimateur de Qms -- celui-la sort de
    l'ajustement de l'acte 2.
    """
    f = np.asarray(f, float)
    module = np.asarray(module, float)
    avertissements = []
    i = int(np.argmax(module))
    z_pic, f_pic = float(module[i]), float(f[i])
    re_estime = float(module.min())
    seuil = re_estime + (z_pic - re_estime)/np.sqrt(2.0)

    g = i
    while g > 0 and module[g-1] >= seuil:
        g -= 1
    d = i
    while d < len(module) - 1 and module[d+1] >= seuil:
        d += 1
    n_points = d - g + 1
    largeur = float(f[d] - f[g])
    q_estime = f_pic/largeur if largeur > 0 else float('inf')

    if i in (0, len(module) - 1):
        avertissements.append(
            'le maximum de |Z| est au BORD de la bande mesuree (%.3g Hz) : le '
            'pic est probablement hors bande, elargir la mesure' % f_pic)
    if n_points < points_min_pic:
        avertissements.append(
            'grille trop lache au pic : %d point(s) dans la largeur a -3 dB '
            'du pic (%.3g - %.3g Hz, Q estime %.1f), il en faut au moins %d -- '
            'densifier entre fs/2 et 2 fs (§ 02.6)'
            % (n_points, f[g], f[d], q_estime, points_min_pic))
    return {
        'f_pic': f_pic, 'z_pic': z_pic, 'largeur_Hz': largeur,
        'q_estime': q_estime, 'n_points_pic': n_points,
        'avertissements': avertissements,
    }


# ---------------------------------------------------------------------------
# Validation d'un fichier de mesure
# ---------------------------------------------------------------------------

def valider_mesure(d, meta, points_min_pic=5, tolerance_derivees=1e-6,
                   strict=False):
    """Controle complet d'une serie -> (erreurs, avertissements).

    ERREURS -- le fichier ne doit pas servir tel quel :
      * colonne obligatoire absente ;
      * valeur non finie (NaN, inf) dans une colonne ;
      * frequences non strictement croissantes, nulles ou negatives (le modele
        de Thiele-Small est en f/fs - fs/f : f > 0 strictement) ;
      * incertitude nulle ou negative (elle sert de poids 1/u^2 au fit de
        l'acte 2 : une incertitude nulle donne un poids infini) ;
      * tension nulle ou negative dans une colonne de lecture (ce sont des
        amplitudes, pas des grandeurs signees) ;
      * metadonnee obligatoire manquante.

    AVERTISSEMENTS -- le fichier est lisible, mais quelque chose cloche :
      * colonnes derivees incoherentes avec les lectures brutes et R_ref ;
      * grille trop lache autour du pic ;
      * deux pics -> modele a 5 parametres inadapte ;
      * fichier declare SYNTHETIQUE.

    strict=True leve ErreurFormatMesure s'il y a au moins une erreur.
    """
    erreurs, avertissements = [], []
    noms = d.dtype.names or ()

    absentes = [c for c in COLONNES if c not in noms]
    if absentes:
        erreurs.append('colonnes absentes : ' + ', '.join(absentes))
        if strict:
            raise ErreurFormatMesure(erreurs[0])
        return erreurs, avertissements

    for c in noms:
        if not np.all(np.isfinite(d[c])):
            k = int(np.argmin(np.isfinite(d[c])))
            erreurs.append('colonne %s : valeur non finie (NaN ou inf) ligne %d'
                           % (c, k + 1))

    f = d['f_Hz']
    if np.any(f <= 0):
        erreurs.append('f_Hz : frequence nulle ou negative (le modele est en '
                       'f/fs - fs/f, f > 0 strictement)')
    if len(f) > 1 and np.any(np.diff(f) <= 0):
        k = int(np.argmin(np.diff(f) > 0))
        erreurs.append('f_Hz : frequences non strictement croissantes '
                       '(ligne %d : %.6g puis %.6g)' % (k + 2, f[k], f[k+1]))

    for c in COLONNES_INCERTITUDES:
        if np.any(d[c] <= 0):
            erreurs.append('colonne %s : incertitude nulle ou negative -- elle '
                           'sert de poids 1/u^2 au fit de l acte 2' % c)
    for c in ('V_dipole_V', 'V_Rref_V'):
        if np.any(d[c] <= 0):
            erreurs.append('colonne %s : tension nulle ou negative (amplitude '
                           'attendue, pas une grandeur signee)' % c)
    if np.any(d['module_Z_ohm'] <= 0):
        erreurs.append('module_Z_ohm : module nul ou negatif')

    manquantes = verifier_metadonnees(meta)
    if manquantes:
        erreurs.append('metadonnees manquantes : ' + ', '.join(manquantes))

    if strict and erreurs:
        raise ErreurFormatMesure('\n  - '.join([''] + erreurs))
    if erreurs:
        return erreurs, avertissements

    # --- avertissements (seulement si les donnees sont exploitables)
    if 'R_ref_mesuree_ohm' in meta:
        R_ref = meta_flottant(meta, 'R_ref_mesuree_ohm')
        mod = R_ref*d['V_dipole_V']/d['V_Rref_V']
        phi = 360.0*d['f_Hz']*d['dt_s']
        e_mod = float(np.max(np.abs(mod - d['module_Z_ohm'])/np.abs(mod)))
        e_phi = float(np.max(np.abs(phi - d['phase_deg'])))
        if e_mod > tolerance_derivees:
            avertissements.append(
                'module_Z_ohm ne se recalcule pas depuis les lectures brutes '
                '(ecart relatif max %.2g) : R_ref ou les colonnes brutes ont '
                'change -- rejouer depouiller()' % e_mod)
        if e_phi > 1e-6:
            avertissements.append(
                'phase_deg ne se recalcule pas depuis f et dt (ecart max '
                '%.2g deg) -- rejouer depouiller()' % e_phi)

    if 'SYNTHET' in ' '.join(str(v) for v in meta.values()).upper():
        avertissements.append(
            'fichier declare SYNTHETIQUE : utilisable pour tester la chaine, '
            'jamais citable comme resultat de mesure')

    g = diagnostiquer_grille(d['f_Hz'], d['module_Z_ohm'], points_min_pic)
    avertissements.extend(g['avertissements'])
    c = diagnostiquer_caisse(d['f_Hz'], d['module_Z_ohm'])
    avertissements.extend(c['avertissements'])
    return erreurs, avertissements


# ---------------------------------------------------------------------------
# Imports exterieurs : REW et oscilloscope
# ---------------------------------------------------------------------------

def _separateur(lignes):
    """Detecte le separateur de colonnes parmi ';', tabulation, ',' (dans cet
    ordre) et, a defaut, les espaces.

    Retourne (separateur, lignes_corrigees). Le separateur decimal virgule
    n'est converti en point QUE si le separateur de colonnes n'est pas la
    virgule : un fichier a separateur virgule n'est donc pas corrompu
    silencieusement.
    """
    echantillon = lignes[:20]
    for sep in (';', '\t', ','):
        n = [ligne.count(sep) for ligne in echantillon]
        if min(n) >= 1 and len(set(n)) == 1:
            if sep != ',':
                lignes = [re.sub(r'(?<=\d),(?=\d)', '.', l) for l in lignes]
            return sep, lignes
    return None, [re.sub(r'(?<=\d),(?=\d)', '.', l) for l in lignes]


def lire_rew(chemin, u_module_relative=None, u_phase_deg=None):
    """Lit un export texte REW -> (f, mod, phi, meta).

    Format suppose (aide en ligne REW, File > Export > Export measurement as
    text) : en-tete prefixee par '*', puis trois colonnes
    Freq (Hz) / Z (ohm) / Phase (deg).

    [[A VERIFIER SUR UN EXPORT REEL]] -- hypotheses faites ici, et comment
    chacune se leve en une minute le jour du premier export :
      1. separateur de colonnes : auto-detecte parmi ',', ';', tabulation,
         espaces (il depend de la version et des reglages regionaux) ;
      2. separateur decimal : la virgule entre deux chiffres n'est convertie en
         point que si le separateur de colonnes n'est pas la virgule ;
      3. colonne 2 = MODULE en ohm. Si l'export est une reponse en frequence
         (.frd), la colonne 2 est un niveau en dB SPL et le "module" lu serait
         absurde (des "ohms" entre 20 et 140) : un controle le signale dans
         meta['alerte'] ;
      4. convention de phase : REW est suppose compter la phase POSITIVE pour
         une charge inductive, comme le § 02.1 [[a verifier]].

    REW donne des centaines de points SANS incertitude. u_module_relative
    (ex. 0.03 pour 3 %) et u_phase_deg permettent de leur AFFECTER
    l'incertitude de chaine issue des calibrations (§ 02.9) ; elles
    sont rangees dans meta, jamais fabriquees d'office.

    Note : un import REW n'est PAS convertible en fichier maison, faute de
    lectures brutes (V_d, V_R, dt). Il se consomme tel quel et sert de
    VERIFICATION INDEPENDANTE de la serie a l'oscilloscope (test h).
    """
    entete, lignes = [], []
    with open(chemin, encoding='utf-8', errors='replace') as fh:
        for ligne in fh:
            if re.match(r'\s*[-+.0-9]', ligne):
                lignes.append(ligne)
            elif ligne.strip():
                entete.append(ligne.strip().lstrip('*').strip())
    if not lignes:
        raise ErreurFormatMesure(
            '%s : aucune ligne de donnees reconnue (en-tete seule ? separateur '
            'decimal ?)' % os.path.basename(chemin))
    sep, lignes = _separateur(lignes)
    data = np.loadtxt(io.StringIO(''.join(lignes)), delimiter=sep, ndmin=2)
    if data.shape[1] < 2:
        raise ErreurFormatMesure(
            '%s : %d colonne(s), 2 au minimum attendues (separateur de colonnes ? '
            'separateur decimal ?)' % (os.path.basename(chemin), data.shape[1]))

    f, mod = data[:, 0], data[:, 1]
    phi = data[:, 2] if data.shape[1] > 2 else np.zeros_like(f)
    meta = {
        'source': 'REW (export texte)',
        'fichier': os.path.basename(chemin),
        'separateur': repr(sep),
        'entete_brute': entete,
        'n_points': int(len(f)),
        'hypothese': 'colonnes Freq/Z/Phase, phase positive = inductif '
                     '[[a verifier sur un export reel]]',
    }
    for ligne in entete:
        m = re.fullmatch(r'([A-Za-z][A-Za-z0-9 _()-]*?)\s*[:=]\s*(.+)', ligne)
        if m:
            meta['rew_' + m.group(1).strip().replace(' ', '_').lower()] = m.group(2).strip()
    if u_module_relative is not None:
        meta['u_module_relative'] = float(u_module_relative)
    if u_phase_deg is not None:
        meta['u_phase_deg'] = float(u_phase_deg)
    if np.all(mod > 20.0) and np.all(mod < 140.0):
        meta['alerte'] = ('colonne 2 entierement comprise entre 20 et 140 : '
                          'est-ce un niveau en dB SPL plutot qu un module en ohm ?')
    return f, mod, phi, meta


def lire_scope(chemin, colonnes=(0, 1, 2), increment_s=None, t0_s=0.0):
    """Lit un CSV d'oscilloscope deux voies -> (t, v1, v2, meta).

    Convention imposee (§ 09.3) : CH1 = V_dipole, CH2 = V_Rref.

    [[FORMAT DU MODELE DU LYCEE A RELEVER]] -- ce lecteur est volontairement
    tolerant, et il dit ce qu'il a suppose :
      * l'en-tete (tout ce qui n'est pas une ligne de nombres) est conservee
        dans meta['entete_brute'] ; les couples 'cle,valeur' ou 'cle:valeur' y
        sont extraits (les Rigol ecrivent par exemple 'Increment,1e-06') ;
      * separateur auto-detecte, virgule decimale geree comme pour REW ;
      * colonnes = (indice_temps, indice_CH1, indice_CH2). Si l'appareil
        n'exporte PAS de colonne de temps (certains n'exportent que les
        echantillons et un pas en en-tete), passer colonnes=(None, 0, 1) et
        increment_s : le temps est alors reconstruit, t = t0 + k*increment.

    Le temps sert ensuite a depouiller_scope() : c'est lui qui porte la phase.
    Une base de temps fausse de 1 % donne une phase fausse de 1 % -- petit a
    100 Hz, mais SYSTEMATIQUE.
    """
    entete, lignes = [], []
    with open(chemin, encoding='utf-8', errors='replace') as fh:
        for ligne in fh:
            if re.match(r'\s*[-+.0-9]', ligne) and re.search(r'\d', ligne):
                lignes.append(ligne)
            elif ligne.strip():
                entete.append(ligne.strip())
    if not lignes:
        raise ErreurFormatMesure('%s : aucune ligne de donnees reconnue'
                                 % os.path.basename(chemin))
    sep, lignes = _separateur(lignes)
    data = np.loadtxt(io.StringIO(''.join(lignes)), delimiter=sep, ndmin=2)

    meta = {'source': 'oscilloscope (export CSV)',
            'fichier': os.path.basename(chemin),
            'separateur': repr(sep),
            'entete_brute': entete,
            'n_echantillons': int(data.shape[0]),
            'hypothese': 'CH1 = V_dipole, CH2 = V_Rref '
                         '[[format du modele du lycee a relever]]'}
    for ligne in entete:
        m = re.fullmatch(r'([A-Za-z][A-Za-z0-9 _()-]*?)\s*[,;:=]\s*(.+)', ligne)
        if m:
            meta['scope_' + m.group(1).strip().replace(' ', '_').lower()] = m.group(2).strip()

    i_t, i_1, i_2 = colonnes
    besoin = max(x for x in (i_t, i_1, i_2) if x is not None) + 1
    if data.shape[1] < besoin:
        raise ErreurFormatMesure(
            '%s : %d colonne(s) lue(s), %d attendue(s) (argument colonnes=%s)'
            % (os.path.basename(chemin), data.shape[1], besoin, (i_t, i_1, i_2)))
    v1, v2 = data[:, i_1], data[:, i_2]
    if i_t is None:
        if increment_s is None:
            increment_s = meta.get('scope_increment')
        if increment_s is None:
            raise ErreurFormatMesure(
                'pas de colonne de temps et pas d increment : passer '
                'increment_s (pas d echantillonnage, en secondes)')
        t = float(t0_s) + np.arange(len(v1))*float(increment_s)
        meta['temps'] = 'reconstruit : t0 + k*increment'
    else:
        t = data[:, i_t]
        meta['temps'] = 'colonne %d du fichier' % i_t
    if len(t) > 1:
        meta['f_echantillonnage_Hz'] = float(1.0/np.median(np.diff(t)))
    return t, v1, v2, meta


# ---------------------------------------------------------------------------
# Criteres geles (principe 4 du § 09.1)
# ---------------------------------------------------------------------------

#: rubrique -> cles obligatoires. Le schema suit DECISIONS-PHASE-0.md : une
#: rubrique par decision D1..D8, plus un bloc 'meta' de tracabilite.
SCHEMA_CRITERES = {
    'meta': ('version_schema', 'date_gel', 'commit_gel', 'signe_par', 'source'),
    'D1_definition_fc': ('definition', 'convention_3dB_dB', 'porte_phase_4_pct'),
    'D2_cible_sommation': ('cible', 'f_cible_Hz', 'polarite_voie_medium'),
    'D3_niveaux_ecoute': ('grandeur_de_reference', 'niveau_faible',
                          'niveau_fort', 'repetitions'),
    'D4_criteres_comparaison': ('liste', 'critere_principal', 'bande_Hz',
                                'points_par_octave', 'plancher_dB', 'arrondi_dB',
                                'seuil_de_departage'),
    'D5_fonction_cout': ('bande_somme_Hz', 'bande_forme_voie_Hz',
                         'points_par_octave', 'sous_bande_phase_Hz', 'poids',
                         'P_ref_W', 'hypothese_bruit_rose',
                         'protection_medium_unilaterale', 'plancher_C1_F'),
    'D6_self': ('r_max_ohm', 'modele_dcr_prix'),
    'D7_figures': ('format', 'largeur_px', 'hauteur_px'),
    'D8_type_caisse': ('type', 'date_du_constat', 'n_parametres_fit'),
    # Les huit familles de tests du § 09.6. Le § 09.6 impose qu'elles soient
    # RECOPIEES ici : sans cela les criteres chiffres ne vivent que dans les
    # docstrings des tests, et une relecture ne peut confronter un test qu'a
    # lui-meme (correction de relecture du 2026-09-14). Elles ne portent PAS de
    # marque [[a geler]] : ce sont des criteres de code, pas des choix de Thomas.
    'tests_non_regression': ('a_ajustement', 'b1_optimiseur_continu',
                             'b2_optimiseur_e12', 'b3_degenerescence',
                             'c_incertitudes', 'd_series_e12', 'g_entrees',
                             'h_figures'),
}


def gabarit_criteres_geles():
    """Gabarit de criteres_geles.json : la structure attendue, remplie de
    marques [[a geler]]. Chaque rubrique renvoie a sa decision dans
    DECISIONS-PHASE-0.md et rappelle la RECOMMANDATION du registre -- une
    recommandation n'est pas une decision : seul Thomas gele, date et signe."""
    m = '[[a geler]]'
    r = '[[a recopier du § 09.6]]'    # criteres de CODE, pas decisions de Thomas
    return {
        '_lisez_moi': (
            'Decisions GELEES du TIPE. Tant qu une valeur contient la marque '
            '[[a geler]], la decision n est pas prise et le code REFUSE de s en '
            'servir. Registre, options et consequences chiffrees : '
            'DECISIONS-PHASE-0.md. Toute modification apres gel doit etre '
            'inscrite, datee et justifiee dans le Journal des modifications de '
            'ce meme fichier -- et dite a l oral.'),
        'meta': {
            'version_schema': 1,
            'date_gel': m,
            'commit_gel': m,
            'signe_par': m,
            'source': 'DECISIONS-PHASE-0.md',
        },
        'D1_definition_fc': {
            '_aide': 'D1. Recommandation du registre : f_c = frequence de '
                     'CROISEMENT des deux voies (|H_PB| = |H_PH|) ; convention '
                     'de demi-puissance -3,0103 dB pour tous les reperes -3 dB ; '
                     'porte de la phase 4 a +/-5 % sur le croisement.',
            'definition': m,
            'convention_3dB_dB': m,
            'porte_phase_4_pct': m,
        },
        'D2_cible_sommation': {
            '_aide': 'D2. VOLONTAIREMENT REPORTEE apres la phase 1 : la cible '
                     'est un PARAMETRE du code (butterworth | lr2 | plate), '
                     'jamais une constante. Sanity check sur 8 ohm resistif : '
                     '18,0 mH / 140,7 uF en butterworth, 25,5 mH / 99,5 uF en '
                     'lr2. Butterworth 2nd ordre => inversion de polarite '
                     'd une voie OBLIGATOIRE.',
            'cible': m,
            'f_cible_Hz': m,
            'polarite_voie_medium': m,
        },
        'D3_niveaux_ecoute': {
            '_aide': 'D3. Les deux niveaux d ecoute de reference, definis par '
                     'une grandeur MESURABLE (tension aux bornes du HP, ou SPL '
                     'a 1 m), jamais par une position de bouton.',
            'grandeur_de_reference': m,
            'niveau_faible': m,
            'niveau_fort': m,
            'repetitions': m,
        },
        'D4_criteres_comparaison': {
            '_aide': 'D4. Les huit criteres de comparaison. Recommandation : '
                     'les geler avec les trois amendements (declasser le '
                     'critere 2 en indicateur, ajouter l ecart MAX au critere 1, '
                     'geler la definition complete du critere 1 : bande '
                     '40-250 Hz, 24 points/octave, plancher 20 dB, arrondi '
                     '0,1 dB, 3 repetitions).',
            'liste': m,
            'critere_principal': m,
            'bande_Hz': m,
            'points_par_octave': m,
            'plancher_dB': m,
            'arrondi_dB': m,
            'seuil_de_departage': m,
        },
        'D5_fonction_cout': {
            '_aide': 'D5. Bande et ponderations de J (§ 04.5). '
                     'Recommandation A3 : plancher dur sur C1 (contrainte '
                     'ordre 2) ET bande elargie a 40-1600 Hz pour le seul terme '
                     'de forme de la voie sub, 40-250 Hz pour le terme de somme. '
                     'Poids proposes : w_s = 1, w_v = 1, w_euro = 0,04 dB/euro, '
                     'w_W = 1 dB/W a P_ref = 10 W, w_phi a RECALIBRER sur le '
                     'decalage acoustique mesure (0,018 dB/deg pour 0,50 m).',
            'bande_somme_Hz': m,
            'bande_forme_voie_Hz': m,
            'points_par_octave': m,
            'sous_bande_phase_Hz': m,
            'poids': {'w_s': m, 'w_v': m, 'w_phi': m, 'w_euro': m, 'w_W': m},
            'P_ref_W': m,
            'hypothese_bruit_rose': m,
            'protection_medium_unilaterale': m,
            'plancher_C1_F': m,
        },
        'D6_self': {
            '_aide': 'D6. r_max de la self, et LE modele de DCR / prix retenu '
                     '(A : masse de cuivre fixee, r proportionnel a L ; '
                     'B : DCR fixee, prix proportionnel a L ; C : fil fixe, r et '
                     'prix en racine de L). Les placeholders du brouillon '
                     'penalisent DEUX FOIS le cuivre : il faut en choisir un.',
            'r_max_ohm': m,
            'modele_dcr_prix': m,
        },
        'D7_figures': {
            '_aide': 'D7. Gabarit 4/3 impose par le livrable SCEI (PDF '
                     '1024x768). A geler avant la premiere figure.',
            'format': m,
            'largeur_px': m,
            'hauteur_px': m,
        },
        'D8_type_caisse': {
            '_aide': 'D8. CONSTAT, pas un choix : clos (un pic, 5 parametres) '
                     'ou bass-reflex (deux pics, 8 parametres). A remplir apres '
                     'la premiere mesure Z(f) de la phase 1 ; '
                     'io_mesures.diagnostiquer_caisse() fournit le constat.',
            'type': m,
            'date_du_constat': m,
            'n_parametres_fit': m,
        },
        # Les huit familles de tests du § 09.6. CE NE SONT PAS DES DECISIONS DE
        # THOMAS : ce sont les criteres chiffres de la specification, a RECOPIER
        # depuis le § 09.6. Le gabarit ne peut pas les inventer -- il en pose la
        # structure et le dit. Le fichier reellement en service, lui, les porte
        # (correction de relecture du 2026-09-14).
        'tests_non_regression': {
            '_lisez_moi': (
                'Criteres chiffres des huit familles de tests (§ 09.6), RECOPIES '
                'depuis REFERENCE-TECHNIQUE.md et lus par analyse/tests/contexte.py. '
                'Un critere qui ne vit que dans le test qu il gouverne se confronte '
                'a lui-meme : rien n empeche alors de le retoucher apres avoir vu un '
                'resultat. Tout amendement va dans journal_des_modifications, date '
                'et motive.'),
            'date_gel': m,
            'commit_gel': m,
            'a_ajustement': {'_aide': '(a) ajustement T-S', 'criteres': r},
            'b1_optimiseur_continu': {'_aide': '(b1) porte 8 ohm, continu',
                                      'criteres': r},
            'b2_optimiseur_e12': {'_aide': '(b2) porte 8 ohm, E12', 'criteres': r},
            'b3_degenerescence': {'_aide': '(b3) somme seule', 'criteres': r},
            'c_incertitudes': {'_aide': '(c) propagation sur f_0', 'criteres': r},
            'd_series_e12': {'_aide': '(d) exhaustivite E12', 'criteres': r},
            'g_entrees': {'_aide': '(g) CSV et depouillement', 'criteres': r},
            'h_figures': {'_aide': '(h) SVG et injection', 'criteres': r},
        },
        'journal_des_modifications': [],
    }


def _marques_non_gelees(obj, chemin=''):
    """Liste les chemins de cles dont la valeur porte encore une marque [[...]].
    Les cles commencant par '_' (aide, lisez-moi) sont ignorees."""
    trouvees = []
    if isinstance(obj, dict):
        for cle, valeur in obj.items():
            if str(cle).startswith('_'):
                continue
            suite = '%s.%s' % (chemin, cle) if chemin else str(cle)
            trouvees.extend(_marques_non_gelees(valeur, suite))
    elif isinstance(obj, (list, tuple)):
        for i, valeur in enumerate(obj):
            trouvees.extend(_marques_non_gelees(valeur, '%s[%d]' % (chemin, i)))
    elif isinstance(obj, str) and MARQUE_NON_GELE in obj:
        trouvees.append(chemin)
    return trouvees


def lire_criteres_geles(chemin=None, exiger_geles=True):
    """Lit analyse/criteres_geles.json -> dict, ou REFUSE.

    Trois refus, tous explicites, et aucune valeur par defaut nulle part :
      * fichier absent                    -> CriteresAbsents
      * rubrique ou cle manquante         -> CriteresIncomplets (liste)
      * valeur encore marquee [[a geler]] -> CriteresNonGeles (liste)

    C'est le principe 4 du § 09.1 : "les decisions gelees sont un
    fichier, pas une intention". C'est aussi ce qui rend VERIFIABLE
    l'affirmation "criteres geles avant les mesures", socle d'honnetete du
    sujet -- sinon rien n'empeche de retoucher les poids apres coup.

    exiger_geles=False sert uniquement a inspecter le gabarit pendant le
    developpement ; aucun chiffre destine a l'oral ne doit en sortir. La liste
    des cles non gelees est renvoyee dans la cle '_non_geles'.
    """
    chemin = CHEMIN_CRITERES if chemin is None else chemin
    if not os.path.isfile(chemin):
        raise CriteresAbsents(
            '%s est introuvable.\n'
            '  Le code ne fabrique PAS de criteres : ils se gelent a la main, '
            'dates et signes, d apres DECISIONS-PHASE-0.md.\n'
            '  Pour repartir du gabarit : '
            'python analyse/io_mesures.py --gabarit-criteres' % chemin)
    with open(chemin, encoding='utf-8') as fh:
        try:
            criteres = json.load(fh)
        except json.JSONDecodeError as exc:
            raise ErreurFormatMesure('%s : JSON invalide (%s)' % (chemin, exc))

    manquantes = []
    for rubrique, cles in SCHEMA_CRITERES.items():
        if rubrique not in criteres:
            manquantes.append(rubrique)
            continue
        contenu = criteres[rubrique]
        if not isinstance(contenu, dict):
            manquantes.append('%s (doit etre un objet)' % rubrique)
            continue
        manquantes.extend('%s.%s' % (rubrique, c) for c in cles if c not in contenu)
    if manquantes:
        raise CriteresIncomplets(
            '%s : rubrique(s) ou cle(s) manquante(s) :\n  - %s'
            % (os.path.basename(chemin), '\n  - '.join(manquantes)))

    non_geles = _marques_non_gelees(criteres)
    if non_geles and exiger_geles:
        raise CriteresNonGeles(
            '%s : %d decision(s) non gelee(s) :\n  - %s\n'
            '  Tant qu une marque %s subsiste, la decision n est pas prise -- '
            'voir DECISIONS-PHASE-0.md.'
            % (os.path.basename(chemin), len(non_geles),
               '\n  - '.join(non_geles), MARQUE_NON_GELE))
    criteres['_non_geles'] = non_geles
    return criteres


def ecrire_criteres_geles(chemin=None, criteres=None):
    """Ecrit le fichier des criteres (par defaut le GABARIT). N'ecrase jamais
    un fichier existant : c'est un document date et signe."""
    chemin = CHEMIN_CRITERES if chemin is None else chemin
    criteres = gabarit_criteres_geles() if criteres is None else criteres
    if os.path.isfile(chemin):
        raise FileExistsError(
            '%s existe deja : ce fichier est signe, il ne se reecrit pas tout '
            'seul (le supprimer a la main si c est voulu)' % chemin)
    with open(chemin, 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(criteres, fh, ensure_ascii=False, indent=2)
        fh.write('\n')
    return chemin


# ---------------------------------------------------------------------------
# Jeu d'exemple SYNTHETIQUE
# ---------------------------------------------------------------------------

def _z_ts_local(f, Re, Le, Res, fs, Qms):
    """Repli local de modele_hp.Z_ts (Thiele-Small a 5 parametres, SI).

    Present uniquement pour que ce module puisse engendrer son fichier
    d'exemple et s'auto-tester sans dependre de l'ordre d'ecriture des modules.
    Des que modele_hp est disponible, c'est LUI qui sert (voir
    generer_exemple_synthetique) : toute divergence entre les deux serait un
    bug, et la reference est modele_hp.
    """
    f = np.asarray(f, float)
    if np.any(f <= 0):
        raise ValueError('Z_ts : f doit etre > 0 (modele en f/fs - fs/f)')
    x = f/fs - fs/f                       # desaccord reduit
    return Re + 2j*np.pi*f*Le + Res/(1 + 1j*Qms*x)


def _grille_locale(f1, f2, n_par_octave=12, densifier=None):
    """Repli local de modele_hp.grille_log : grille geometrique, avec une zone
    densifiee optionnelle (f_a, f_b, n_par_octave)."""
    n = int(round(np.log2(f2/f1)*n_par_octave)) + 1
    f = np.geomspace(f1, f2, n)
    if densifier is not None:
        fa, fb, npo = densifier
        m = int(round(np.log2(fb/fa)*npo)) + 1
        f = np.unique(np.concatenate([f, np.geomspace(fa, fb, m)]))
    return f


#: parametres TYPIQUES d'un 18 pouces 8 ohm de sono en caisse close.
#: ATTENTION : ordres de grandeur lus sur des datasheets publiques
#: (§ 01.13), PAS une mesure du haut-parleur du projet.
SUB_TYPIQUE = dict(Re=5.4, Le=1.9e-3, Res=100.0, fs=55.0, Qms=6.1)


def generer_exemple_synthetique(chemin=None, parametres=None, R_ref=100.0,
                                eps=0.014, u_phase=1.5, niveau_Vd=0.150,
                                graine=20260913):
    """Engendre mesures/exemple_synthetique_sub.csv -> chemin ecrit.

    Fichier de DEMONSTRATION : il sert a eprouver la chaine (lecture,
    validation, ajustement, figures) avant la premiere seance de banc. Son
    en-tete dit en toutes lettres qu'il est SYNTHETIQUE.

    Simulation, deliberement simple et entierement tracable :
      * Z(f) par le modele de Thiele-Small a 5 parametres, parametres TYPIQUES
        (SUB_TYPIQUE) -- ordres de grandeur de datasheets, pas une mesure ;
      * protocole du § 02.5 : tension aux bornes du dipole maintenue a
        niveau_Vd a chaque point, d ou V_Rref = R_ref*V_dipole/|Z| ;
      * dt = phi/(360 f), donc phase positive pour une charge inductive ;
      * bruit de lecture gaussien relatif eps sur chaque voie et ABSOLU
        u_phase (en degres) sur la phase, graine FIXEE (un tirage non
        reproductible n est pas un resultat) ;
      * les colonnes derivees sont recalculees depuis les lectures BRUITEES :
        le fichier est donc coherent avec lui-meme au sens du test (g).
    """
    chemin = CHEMIN_EXEMPLE if chemin is None else chemin
    p = dict(SUB_TYPIQUE if parametres is None else parametres)
    rng = np.random.default_rng(graine)

    try:                                     # la reference, des qu elle existe
        from modele_hp import Z_ts, grille_log
        source_modele = 'modele_hp.Z_ts'
        f = grille_log(10.0, 1000.0, 12, densifier=(p['fs']/2, 2*p['fs'], 24))
    except Exception:                        # repli autonome, meme formule
        Z_ts, source_modele = _z_ts_local, 'io_mesures._z_ts_local (repli)'
        f = _grille_locale(10.0, 1000.0, 12, densifier=(p['fs']/2, 2*p['fs'], 24))

    Z = Z_ts(f, **p)
    module_vrai, phase_vraie = np.abs(Z), np.degrees(np.angle(Z))

    v_d = niveau_Vd*(1 + eps*rng.standard_normal(len(f)))
    v_r = R_ref*niveau_Vd/module_vrai*(1 + eps*rng.standard_normal(len(f)))
    # Bruit de phase ABSOLU (u_phase degres), et NON relatif a la phase. On
    # pointe un passage par zero : on se trompe d un TEMPS, pas d un pourcentage
    # de la phase lue. Un bruit relatif rendrait la phase connue a 0,1 degre pres
    # la ou l en-tete en annonce 1,5 ; le chi2 reduit de l acte 2 tomberait alors
    # a 0,42, et l ajustement "validerait" des incertitudes qui ne decrivent pas
    # les donnees -- exactement ce que le chi2 est cense detecter (§ 03.7).
    dt = (phase_vraie + u_phase*rng.standard_normal(len(f)))/(360.0*f)

    d = tableau_mesure(f_Hz=f, V_dipole_V=v_d, V_Rref_V=v_r, dt_s=dt,
                       module_Z_ohm=np.zeros_like(f), phase_deg=np.zeros_like(f),
                       u_module_alea_ohm=np.ones_like(f),
                       u_phase_deg=np.full_like(f, u_phase))
    meta = {
        'version_format': VERSION_FORMAT,
        'date': '2026-09-13T00:00',
        'dipole': 'SYNTHETIQUE -- 18 pouces 8 ohm en caisse close, parametres '
                  'TYPIQUES de datasheet (§ 01.13), PAS le HP du projet',
        'montage': 'C (GBF flottant, noeud milieu a la masse) -- simule',
        'R_ref_nominale_ohm': '%.6g' % R_ref,
        'R_ref_mesuree_ohm': '%.6g' % R_ref,
        'u_R_ref_relative_pct': '1.0',
        'u_systematique_relative_pct': '1.2',
        'niveau_Vd_RMS_V': '%.6g' % niveau_Vd,
        'temperature_C': '20',
        'operateur': 'genere par io_mesures.generer_exemple_synthetique',
        'appareil': 'AUCUN -- simulation numerique (%s)' % source_modele,
        'Re_DC_avant_ohm': '%.6g' % p['Re'],
        'Re_DC_apres_ohm': '%.6g' % p['Re'],
        'statut_donnees': 'SYNTHETIQUES -- aucune mesure de l enceinte du projet',
        'parametres_du_modele': 'Re=%.6g ohm, Le=%.6g H, Res=%.6g ohm, fs=%.6g Hz, '
                                'Qms=%.6g' % (p['Re'], p['Le'], p['Res'],
                                              p['fs'], p['Qms']),
        'bruit_simule': 'gaussien %.3g %% par voie sur les tensions, %.3g deg '
                        '(absolus) sur la phase' % (100*eps, u_phase),
        'graine': '%d' % graine,
    }
    d = depouiller(d, meta, R_ref_ohm=R_ref, eps_relatif=eps,
                   u_phase_deg=u_phase, montage='C')
    commentaires = [
        'DONNEES SYNTHETIQUES -- aucune mesure de l enceinte du projet.',
        'Engendrees par un modele de Thiele-Small a 5 parametres pour eprouver',
        'la chaine d analyse avant la premiere seance de banc. Ne jamais citer',
        'un chiffre issu de ce fichier comme un resultat de mesure.',
    ]
    return ecrire_mesure(chemin, d, meta, commentaires=commentaires)


# ---------------------------------------------------------------------------
# Auto-test (lancement direct)
# ---------------------------------------------------------------------------

def _auto_test():
    """Verifie ce que le module promet : aller-retour exact, recalcul des
    colonnes derivees, refus d'un fichier casse, signes de la phase, refus des
    criteres non geles. Les vrais tests de non-regression vivent dans
    analyse/tests/ (test g du § 09.6) ; celui-ci est la preuve
    minimale que le fichier s'execute."""
    import tempfile
    ok = True
    tmp = tempfile.mkdtemp(prefix='tipe_io_')

    # (1) aller-retour ecriture / relecture
    chemin = os.path.join(tmp, 'aller_retour.csv')
    generer_exemple_synthetique(chemin)
    d, meta = lire_mesure(chemin)
    d2, meta2 = lire_mesure(ecrire_mesure(os.path.join(tmp, 'bis.csv'), d, meta))
    ecart = max(float(np.max(np.abs(d2[c] - d[c])/np.maximum(np.abs(d[c]), 1e-300)))
                for c in COLONNES)
    print('(1) aller-retour CSV : %d points, %d cles de metadonnees ; '
          'ecart max %.1e EN RELATIF' % (len(d), len(meta), ecart))
    ok &= ecart < 4e-9

    # (2) colonnes derivees recalculables depuis le brut
    #     Le critere est RELATIF : le fichier porte 9 chiffres significatifs,
    #     donc l'ecart absolu sur |Z| croit avec |Z| (1e-7 ohm a 100 ohm, mais
    #     1e-8 ohm a 10 ohm) -- l'ecart absolu du § 09.6 vaut pour la
    #     serie qui l'a produit, pas pour toutes.
    e = depouiller(d, meta)
    rel_mod = float(np.max(np.abs(e['module_Z_ohm']/d['module_Z_ohm'] - 1)))
    abs_mod = float(np.max(np.abs(e['module_Z_ohm'] - d['module_Z_ohm'])))
    rel_phi = float(np.max(np.abs(e['phase_deg']/d['phase_deg'] - 1)))
    print('(2) colonnes derivees recalculees depuis le brut : %.1e en relatif '
          'sur |Z| (%.1e ohm au pic), %.1e sur la phase'
          % (rel_mod, abs_mod, rel_phi))
    ok &= rel_mod < 1e-8 and rel_phi < 1e-8

    # (3) validation du fichier sain
    erreurs, avertissements = valider_mesure(d, meta)
    print('(3) validation du fichier sain : %d erreur(s), %d avertissement(s)'
          % (len(erreurs), len(avertissements)))
    for a in avertissements:
        print('      avertissement : %s' % a.split(' :')[0])
    ok &= not erreurs

    # (3 bis) grille trop lache : le cas Qms = 8 du § 09.6
    for n_par_octave in (6, 12, 24):
        f_l = _grille_locale(10., 1000., n_par_octave)
        z_l = np.abs(_z_ts_local(f_l, 5.4, 1.9e-3, 100., 55., 8.))
        g = diagnostiquer_grille(f_l, z_l)
        print('(3 bis) grille 1/%-2d d octave : %d point(s) dans la largeur du '
              'pic (Q estime %.1f) -> %s'
              % (n_par_octave, g['n_points_pic'], g['q_estime'],
                 'AVERTISSEMENT' if g['avertissements'] else 'grille suffisante'))
    ok &= bool(diagnostiquer_grille(
        _grille_locale(10., 1000., 6),
        np.abs(_z_ts_local(_grille_locale(10., 1000., 6),
                           5.4, 1.9e-3, 100., 55., 8.)))['avertissements'])

    # (4) fichier volontairement casse
    casse = os.path.join(tmp, 'casse.csv')
    d3 = d.copy()
    d3['f_Hz'][5], d3['f_Hz'][6] = d3['f_Hz'][6], d3['f_Hz'][5]   # non croissantes
    d3['u_module_alea_ohm'][2] = 0.0                              # poids infini
    d3['V_Rref_V'][3] = -1.0                                      # amplitude < 0
    meta3 = {c: v for c, v in meta.items() if c != 'R_ref_mesuree_ohm'}
    ecrire_mesure(casse, d3, meta3)
    d3, meta3 = lire_mesure(casse)
    erreurs, _ = valider_mesure(d3, meta3)
    print('(4) fichier casse : %d erreurs detectees' % len(erreurs))
    for e_ in erreurs:
        print('      %s' % e_.split(' --')[0].split(' (ligne')[0])
    ok &= len(erreurs) >= 4

    # (4 bis) fichier hors format : colonnes absentes
    hors = os.path.join(tmp, 'hors_format.csv')
    with open(hors, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('# version_format: 1\nf_Hz,module_Z_ohm\n100,14.1\n')
    try:
        lire_mesure(hors)
        print('(4 bis) ECHEC : un fichier a 2 colonnes a ete accepte')
        ok = False
    except ErreurFormatMesure as exc:
        print('(4 bis) colonnes absentes -> refus : %s'
              % str(exc).splitlines()[0][:76])

    # (5) depouillement d'une acquisition simulee, fenetre NON entiere
    R_ref, f0 = 100.0, 100.0
    Z_vrai = complex(_z_ts_local(f0, **SUB_TYPIQUE))
    for duree, etiquette in ((0.100, '10 periodes'), (0.1037, '10,37 periodes')):
        t = np.arange(0, duree, 1/50000.)
        rng = np.random.default_rng(3)
        v1 = 0.15*np.sqrt(2)*np.cos(2*np.pi*f0*t + np.angle(Z_vrai))
        v2 = 0.15*np.sqrt(2)*R_ref/abs(Z_vrai)*np.cos(2*np.pi*f0*t)
        bruit = 0.002*rng.standard_normal(len(t)) + 0.01      # bruit + offset
        mod_l, phi_l, _, _ = depouiller_scope(t, v1 + bruit, v2 + bruit, f0, R_ref, 'lstsq')
        mod_d, phi_d, _, _ = depouiller_scope(t, v1 + bruit, v2 + bruit, f0, R_ref, 'dft')
        noyau = np.exp(-2j*np.pi*f0*t)                # dft BRUTE, non tronquee
        mod_b = abs(R_ref*np.mean((v1 + bruit)*noyau)/np.mean((v2 + bruit)*noyau))
        print('(5) %-16s |Z| vrai %.4f ohm -> dft brute %+.3f %% | dft tronquee '
              '%+.3f %% | lstsq %+.3f %%'
              % (etiquette, abs(Z_vrai), 100*(mod_b/abs(Z_vrai) - 1),
                 100*(mod_d/abs(Z_vrai) - 1), 100*(mod_l/abs(Z_vrai) - 1)))
        ok &= abs(mod_l/abs(Z_vrai) - 1) < 5e-3

    # (6) controle de signe : self pure -> +90 deg, condensateur pur -> -90 deg
    t = np.arange(0, 0.1037, 1/50000.)
    for nom, Z in (('self pure 10 mH', 2j*np.pi*f0*10e-3),
                   ('condo pur 100 uF', 1/(2j*np.pi*f0*100e-6))):
        v1 = np.cos(2*np.pi*f0*t + np.angle(Z))
        v2 = np.cos(2*np.pi*f0*t)/abs(Z)*R_ref
        _, phi, _, _ = depouiller_scope(t, v1, v2, f0, R_ref, 'lstsq')
        print('(6) %-17s -> phi = %+.2f deg' % (nom, phi))
        ok &= abs(phi - np.degrees(np.angle(Z))) < 0.01

    # (7) diagnostic : deux pics -> modele a 5 parametres refuse
    f = _grille_locale(10., 300., 48)
    z_br = np.abs(_z_ts_local(f, 5.4, 1.9e-3, 60., 23., 4.)
                  + _z_ts_local(f, 0.0, 0.0, 60., 60., 4.))
    diag = diagnostiquer_caisse(f, z_br)
    print('(7) diagnostic caisse : %d pic(s) a %s Hz -> %s'
          % (diag['n_pics'], ', '.join('%.1f' % x for x in diag['f_pics']),
             diag['modele']))
    ok &= diag['n_pics'] == 2 and diag['modele'] == 'bassreflex_8_parametres'
    diag_clos = diagnostiquer_caisse(d['f_Hz'], d['module_Z_ohm'])
    print('    (meme fonction sur le fichier d exemple : %d pic -> %s)'
          % (diag_clos['n_pics'], diag_clos['modele']))
    ok &= diag_clos['modele'] == 'clos_5_parametres'

    # (8) criteres geles : gabarit -> refus, fichier absent -> refus
    chemin_crit = os.path.join(tmp, 'criteres_geles.json')
    ecrire_criteres_geles(chemin_crit)
    try:
        lire_criteres_geles(chemin_crit)
        print('(8) ECHEC : le gabarit non gele a ete accepte')
        ok = False
    except CriteresNonGeles as exc:
        print('(8) gabarit -> refus : %s' % str(exc).splitlines()[0])
    try:
        lire_criteres_geles(os.path.join(tmp, 'absent.json'))
        print('(8 bis) ECHEC : un fichier absent a ete accepte')
        ok = False
    except CriteresAbsents:
        print('(8 bis) fichier absent -> refus explicite (aucun critere invente)')
    with open(chemin_crit, encoding='utf-8') as fh:
        partiel = json.load(fh)
    del partiel['D5_fonction_cout']['poids']
    del partiel['D8_type_caisse']
    partiel_chemin = os.path.join(tmp, 'partiel.json')
    with open(partiel_chemin, 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(partiel, fh, ensure_ascii=False, indent=2)
    try:
        lire_criteres_geles(partiel_chemin, exiger_geles=False)
        print('(8 ter) ECHEC : un fichier incomplet a ete accepte')
        ok = False
    except CriteresIncomplets as exc:
        print('(8 ter) fichier incomplet -> refus : %s'
              % ' / '.join(str(exc).splitlines()[1:]).replace('  - ', ''))
    criteres = lire_criteres_geles(chemin_crit, exiger_geles=False)
    print('(8 quater) schema : %d rubriques, %d cles non gelees dans le gabarit'
          % (len(SCHEMA_CRITERES), len(criteres['_non_geles'])))

    print('\nRESULTAT : %s' % ('tous les controles passent' if ok
                               else 'AU MOINS UN CONTROLE A ECHOUE'))
    return 0 if ok else 1


if __name__ == '__main__':
    import sys
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    if '--exemple' in sys.argv:
        print('CSV synthetique ecrit : %s' % generer_exemple_synthetique())
    elif '--gabarit-criteres' in sys.argv:
        print('gabarit ecrit : %s' % ecrire_criteres_geles())
    else:
        raise SystemExit(_auto_test())
