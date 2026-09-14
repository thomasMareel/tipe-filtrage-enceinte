# -*- coding: utf-8 -*-
"""optim.py -- Acte 3 : optimisation du filtre de raccord SOUS CONTRAINTES.

Voir REFERENCE-TECHNIQUE.md § 04.5 (formulation), 04.7 (porte de validation),
04.8 (illustration), 04.9 (incertitudes) et 09.4 (signatures gelees).

CE QUE CE MODULE RESOUT, EN UNE PHRASE. Une fois Z(f) mesuree (acte 1) et les
parametres de Thiele-Small identifies (acte 2), on cherche les quatre composants
(L1, C1) de la cellule passe-bas et (C2, L2) de la cellule passe-haut qui minimisent
une fonction de cout J melangeant fidelite acoustique, euros et watts, sous des
contraintes dures (impedance vue par l'ampli, tenue en tension des condensateurs,
budget, DCR maximale de la self). Le probleme est DISCRET (series normalisees E12),
donc on l'enumere exhaustivement -- 331 776 combinaisons en deux secondes avec numpy
seul -- et on recoupe avec un optimiseur CONTINU, qui n'a pas les memes faiblesses.

POURQUOI LE PROBLEME EST INTERESSANT. Sur charge resistive R, le facteur de qualite
d'une cellule LC vaut Q = R.racine(C/L) : il appartient a la CHARGE. Le catalogue
(18 mH / 141 uF pour du Butterworth a 100 Hz sur 8 ohm) suppose R constante. Or un
haut-parleur a une impedance qui varie du simple au sextuple dans la bande du raccord :
le filtre catalogue y surtend d'environ +8 a +11 dB vers 75 Hz et deplace le raccord de
6,5 %. Optimiser, ici, ce n'est pas "faire mieux que le catalogue avec le meme modele" :
c'est resoudre le probleme que le catalogue ne pose pas.

DECISION D2 (13/09/2026), IMPERATIVE. La cible de sommation (butterworth / lr2 / plate)
est VOLONTAIREMENT reportee apres la phase 1. Elle est donc partout un PARAMETRE
(`cible_nom`), jamais une constante, et le sanity check tourne pour LES DEUX cibles.

TROIS MISES EN GARDE, a lire avant d'utiliser un chiffre sorti d'ici.

  1. J N'EST PAS LE CRITERE GELE. Le critere de la phase 4 (ecart RMS en dB de la somme
     mesuree au micro, bande 40-250 Hz, 24 points/octave, plancher 20 dB) vit dans
     filtre.ecart_rms_db(). J est un OUTIL DE CLASSEMENT qui contient ce terme parmi
     cinq, avec des euros et des watts dedans : un J de 11,04 ne se compare a aucune
     mesure. Les deux objets ne doivent jamais etre confondus a l'oral.
  2. AUCUNE MESURE N'EXISTE. Les charges utilisees dans l'auto-test sont SYNTHETIQUES
     (parametres typiques herites de archive-v1/_gen.py). Les modeles de prix sont des
     ordres de grandeur etiquetes. Rien de ce que ce module imprime n'autorise un achat.
  3. L'OPTIMUM EST PLAT, ET LE CODE LE DIT. Plusieurs designs se tiennent a 1 % de J, et
     la derniere marche E12 pese MOINS que les tolerances des composants. La fonction
     analyser_plateau() et le Monte-Carlo de comparer_marche_e12_et_tolerances() le
     mesurent et rendent un verdict explicite : "l'optimum n'est pas distinguable de ses
     voisins" est un resultat, pas un echec, et il doit etre annonce comme tel.

Dependances : numpy (obligatoire), filtre.py (obligatoire, meme dossier). scipy sert au
recoupement continu ; un Nelder-Mead maison prend le relais s'il manque (§ 09.5 :
exercice de robustesse, pas contrainte subie). self_bobine.py fournit le modele de cout
par la masse de cuivre ; io_mesures.py fournit la lecture des criteres geles. Ces deux
derniers sont optionnels et leur absence est dite, jamais contournee en silence.

Conventions (§ 09.4) : tout en SI (H, F, Hz, ohm, V, A, W), conversion en mH/uF a
l'affichage seulement ; docstrings, commentaires et messages en francais SANS ACCENTS
pour rester lisibles dans une console cp1252 ; fichier en UTF-8, fins de ligne LF.

PRET POUR LES TESTS DE NON-REGRESSION. Les portes de validation (b1), (b2) et (d) de la
§ 09.6 sont exposees comme des fonctions rendant un dict avec une cle 'ok', donc
consommables telles quelles par un futur analyse/tests/test_optimiseur.py en unittest :
  sanity_check_continu(cible)   (b1) theoreme : le continu redonne le Butterworth exact
  sanity_check_e12(cible)       (b2) non-regression : le gagnant E12 du J gele
  sanity_check_contraintes()    la contrainte d'impedance est active et calibree
  verifier_optimum_interieur()  (d) l'optimum n'est pas sur un bord de la grille
  verifier_vectorisation()      le produit externe == une double boucle explicite
  sanity_check_complet()        les quatre premieres, pour LES DEUX cibles (decision D2)

Auto-test : python analyse/optim.py          (ajouter --complet pour differential_evolution)
"""

import os
import sys
import warnings

import numpy as np

_ICI = os.path.dirname(os.path.abspath(__file__))
if _ICI not in sys.path:                      # rend le module importable de n'importe ou
    sys.path.insert(0, _ICI)

import filtre as F                             # obligatoire : H_pb, H_ph, cibles, contraintes

try:                                           # modele de cout par la masse de cuivre
    import self_bobine as SB
    AVEC_SELF_BOBINE = True
except Exception:                              # pragma: no cover
    SB = None
    AVEC_SELF_BOBINE = False

try:                                           # lecture des decisions gelees
    import io_mesures as IO
    AVEC_IO = True
except Exception:                              # pragma: no cover
    IO = None
    AVEC_IO = False

try:
    from scipy.optimize import minimize, differential_evolution
    AVEC_SCIPY = True
except ImportError:                            # pragma: no cover
    AVEC_SCIPY = False


# ==================================================================================
# 0. Constantes : series normalisees, grilles, poids, penalites
# ==================================================================================

# --- IEC 60063:2015, series de valeurs preferentielles (mantisses, une decade) ------
E6 = np.array([1.0, 1.5, 2.2, 3.3, 4.7, 6.8])
E12 = np.array([1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2])
E24 = np.array([1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
                3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1])
SERIES = {'E6': E6, 'E12': E12, 'E24': E24}

# La serie E12 n'est PAS exactement geometrique : le pas va de 1,182 (1,1 -> 1,3 ... ici
# 8,2 -> 10) a 1,250 (1,2 -> 1,5) pour un ideal 10^(1/12) = 1,2115. C'est une propriete
# de la norme, pas un bug -- le test (d) du § 09.6 borne ces deux nombres.
PAS_E12_IDEAL = 10.0 ** (1.0 / 12.0)

# --- Espace de recherche gele (§ 04.5, contrainte 1) -------------------------
DECADES_L = (-3, -2)             # E12 x {1 mH, 10 mH} -> 1,0 mH a 82 mH   (24 valeurs)
DECADES_C = (-5, -4)             # E12 x {10 uF, 100 uF} -> 10 uF a 820 uF (24 valeurs)


def serie(base, decades):
    """Concatene une serie de mantisses sur plusieurs decades -> tableau trie.

    serie(E12, (-3, -2)) rend les 24 valeurs de 1,0 mH a 82 mH. Deux decades
    suffisent parce qu'a 8 ohm et 100 Hz les valeurs catalogue (18 mH, 141 uF) sont
    AU CENTRE de la grille, a plus d'une decade de chaque borne -- mais c'est une
    hypothese, pas un theoreme, d'ou l'assertion anti-optimum-de-bord de
    verifier_optimum_interieur().
    """
    base = np.asarray(base, dtype=float)
    return np.concatenate([base * 10.0 ** d for d in decades])


def serie_normalisee(nom, decades):
    """serie_normalisee('E12', (-3, -2)) -> les 24 valeurs de 1,0 mH a 82 mH.

    nom parmi 'E6', 'E12', 'E24' (IEC 60063:2015). E6 = un terme sur deux de E12.
    """
    if nom not in SERIES:
        raise ValueError("serie_normalisee : serie inconnue '%s' ; attendu parmi %s"
                         % (nom, ', '.join(sorted(SERIES))))
    return serie(SERIES[nom], decades)


L_VALS = serie(E12, DECADES_L)   # 1,0 mH ... 82 mH   (24 valeurs)
C_VALS = serie(E12, DECADES_C)   # 10 uF ... 820 uF   (24 valeurs)
L_VALS_E6 = serie(E6, DECADES_L)
C_VALS_E6 = serie(E6, DECADES_C)

# --- Poids PROPOSES de la fonction de cout (§ 04.5, decision D5 ouverte) -----
# CE NE SONT PAS DES POIDS GELES. Tant que criteres_geles.json porte des marques
# [[a geler]], poids_geles() les rend en le DISANT. Unites et equivalences lisibles :
#   w['s']   1 dB par dB d'ecart RMS de la somme a sa cible          (critere n. 1)
#   w['v']   1 dB par dB d'ecart RMS de forme, cumule sur les 2 voies
#   w['phi'] 0,05 dB par degre d'ecart de phase entre voies  (20 deg = 1 dB)
#            RESERVE : sur-penalisant d'un facteur ~8 vis-a-vis de la somme DANS
#            L'AXE, ou 20 deg ne coutent que 0,13 dB. Defendable seulement comme
#            robustesse HORS AXE. A recalibrer sur le tau mesure : 0,50 m entre
#            centres -> 52 deg a 100 Hz -> 0,93 dB -> w_phi = 0,018 dB/deg.
#   w['eur'] 0,04 dB par euro                                (25 EUR = 1 dB)
#   w['W']   1 dB par watt Joule a P_ref = 10 W dans 8 ohm   (10 % de P_ref = 1 dB)
W_PROPOSE = dict(s=1.0, v=1.0, phi=0.05, eur=0.04, W=1.0)

# Poids du SANITY CHECK (§ 04.7) : fidelite pure, ni euros ni watts. Le terme de
# phase EST dedans -- c'est le "J gele" des §§ 04.7 / 04.8 / 09.6, celui qui rend
# J = 0,9471 en butterworth et J = 0,8264 en lr2 sur 8 ohm resistif.
#
# ATTENTION AU MOT "GELE", ET C'EST UNE CORRECTION DE RELECTURE (2026-09-14). Ce jeu
# s'appelait W_GELE, ce qui faisait cohabiter DEUX sens du mot "gele" dans un dossier
# dont l'argument d'honnetete est justement "les criteres ont ete geles avant les
# mesures" :
#   * "J gele" du § 04.7 = la REFERENCE FIXE du sanity check, celle qui rend 0,9471.
#     Elle est figee parce qu'un test de non-regression doit comparer a une constante ;
#   * decision D5 du projet = les ponderations que Thomas devra geler dans
#     criteres_geles.json. Elle est ENCORE OUVERTE ([[a geler]]).
# Le nom W_SANITY ne designe plus que le premier. L'alias W_GELE reste defini pour ne
# casser aucun appel deja ecrit, mais AUCUN message, journal ou figure ne doit plus
# employer le mot "gele" pour ces poids-la.
W_SANITY = dict(s=1.0, v=1.0, phi=0.05, eur=0.0, W=0.0)
W_GELE = W_SANITY                # alias de compatibilite -- voir le commentaire ci-dessus

# Le meme SANS le terme de phase. A conserver, parce qu'il produit un contre-exemple
# instructif : en cible 'lr2' sur 8 ohm, le gagnant E12 passe alors de 27 mH / 100 uF a
# 27 mH / 82 uF (J = 0,8073 au lieu de 0,8264). Ce n'est pas un bug, c'est la signature
# du Linkwitz-Riley 2 : sa propriete definitoire est un ecart de phase NUL entre les deux
# voies a TOUTE frequence, donc c'est le terme de phase -- et lui seul -- qui distingue un
# vrai LR2 d'un couple de cellules qui somme a peu pres plat. En cible 'butterworth', ou
# la phase du gagnant colle deja a sa cible, les deux jeux donnent le meme J = 0,9471.
W_FIDELITE = dict(s=1.0, v=1.0, phi=0.0, eur=0.0, W=0.0)

P_REF_DEFAUT = 10.0              # W, puissance de REFERENCE conventionnelle sur 8 ohm
BANDE_PHASE = (70.0, 140.0)      # Hz, sous-bande du terme de phase (§ 04.5)
PENALITE = 1e3                   # dB ajoutes par contrainte dure violee
BLOC_DEFAUT = 48                 # lignes de p1 traitees d'un coup (memoire, § 09.4)

# Valeurs de controle, toutes CALCULEES (§ 04.7) -- aucune n'est une mesure.
CONTROLE_CONTINU = {'butterworth': (18.006326e-3, 140.674424e-6),
                    'lr2': (25.464791e-3, 99.471839e-6),
                    'plate': (25.464791e-3, 99.471839e-6)}
CONTROLE_E12 = {'butterworth': (18e-3, 150e-6),
                'lr2': (27e-3, 100e-6),
                'plate': (27e-3, 100e-6)}


# ==================================================================================
# 1. Espace de recherche : couples, comptage, arrondi
# ==================================================================================

def couples(a, b):
    """Produit cartesien de deux series -> tableau (len(a)*len(b), 2).

    L'ordre est celui de [(x, y) for x in a for y in b] : la premiere colonne varie
    le plus lentement. C'est l'ordre attendu par cout() -- p1 = couples(L_vals, C_vals)
    pour la voie grave, p2 = couples(C_vals, L_vals) pour la voie medium (dans les deux
    cas le composant SERIE vient en premier, comme dans H_pb et H_ph).
    """
    A, B = np.meshgrid(np.asarray(a, float), np.asarray(b, float), indexing='ij')
    return np.column_stack([A.ravel(), B.ravel()])


def espace_de_recherche(L_vals=L_VALS, C_vals=C_VALS, L_vals_2=None, C_vals_2=None):
    """Decrit et COMPTE l'espace discret, sans rien calculer d'autre.

    Retourne un dict : n_L, n_C, n_couples_grave, n_couples_medium, n_combinaisons,
    bornes, pas_min / pas_max de la grille L (controle IEC 60063).

    Comptes de reference (§ 04.5) : 24^4 = 331 776 combinaisons en E12 ;
    24^2 x 12^2 = 82 944 si les condensateurs passent en E6 ; x (12 x 24) = 96 millions
    si l'on enumerait aussi le couple Zobel (Rz, Cz) -- d'ou le choix de traiter le
    Zobel comme un BOOLEEN et non comme deux variables (restriction assumee du domaine).
    """
    L2v = L_vals if L_vals_2 is None else L_vals_2
    C2v = C_vals if C_vals_2 is None else C_vals_2
    n1 = len(L_vals) * len(C_vals)
    n2 = len(C2v) * len(L2v)
    Ls = np.sort(np.asarray(L_vals, float))
    pas = Ls[1:] / Ls[:-1]
    return dict(n_L=len(L_vals), n_C=len(C_vals),
                n_couples_grave=n1, n_couples_medium=n2, n_combinaisons=n1 * n2,
                L_min=float(Ls[0]), L_max=float(Ls[-1]),
                C_min=float(np.min(C_vals)), C_max=float(np.max(C_vals)),
                pas_min=float(pas.min()), pas_max=float(pas.max()),
                pas_ideal=PAS_E12_IDEAL)


def decrire_espace(L_vals=L_VALS, C_vals=C_VALS, prefixe='  '):
    """Chaine multi-lignes decrivant l'espace de recherche (pour le journal et l'oral)."""
    e = espace_de_recherche(L_vals, C_vals)
    return (
        "%sgrille L : %d valeurs de %.1f mH a %.1f mH   (pas reel %.3f a %.3f ; "
        "E12 ideal %.4f)\n"
        "%sgrille C : %d valeurs de %.0f uF a %.0f uF\n"
        "%s%d couples (L1, C1) x %d couples (C2, L2) = %s combinaisons"
        % (prefixe, e['n_L'], e['L_min'] * 1e3, e['L_max'] * 1e3,
           e['pas_min'], e['pas_max'], e['pas_ideal'],
           prefixe, e['n_C'], e['C_min'] * 1e6, e['C_max'] * 1e6,
           prefixe, e['n_couples_grave'], e['n_couples_medium'],
           format(e['n_combinaisons'], ',d').replace(',', ' ')))


def arrondir_serie(valeur, valeurs):
    """Arrondit a la valeur normalisee la plus proche EN ECHELLE LOG.

    L'arrondi log est le bon : une serie preferentielle est geometrique, donc c'est
    l'ecart RELATIF qui doit etre minimise. Sur 140,674 uF, l'arrondi log donne 150 uF
    (ecart 6,6 %) et non 120 uF (ecart 14,7 %) -- l'arrondi lineaire, lui, hesite.
    """
    v = np.asarray(valeurs, float)
    return float(v[int(np.argmin(np.abs(np.log(np.asarray(valeur, float) / v))))])


def arrondir_design(design, L_vals=L_VALS, C_vals=C_VALS):
    """Arrondit un design continu sur la grille normalisee (arrondi log composant par
    composant). ATTENTION (§ 04.8) : cet arrondi N'EST PAS toujours l'optimum
    discret -- c'est precisement pourquoi l'enumeration exhaustive reste la methode de
    reference et l'arrondi un simple recoupement.
    """
    return dict(L1=arrondir_serie(design['L1'], L_vals),
                C1=arrondir_serie(design['C1'], C_vals),
                C2=arrondir_serie(design['C2'], C_vals),
                L2=arrondir_serie(design['L2'], L_vals))


# ==================================================================================
# 2. Modeles economiques et modele de self (§ 04.5, contrainte 5)
# ==================================================================================

def prix_C_placeholder(C):
    """Prix d'un condensateur bipolaire de crossover : 1,00 + 0,05 EUR par uF.

    PLACEHOLDER explicite [[a remplacer par un devis reel]]. Ordre de grandeur seul :
    un 150 uF sort a 8,50 EUR, ce qui est le bon ordre pour un chimique bipolaire, et
    completement faux pour un film polypropylene (qui couterait dix fois plus).
    """
    return 1.0 + 0.05 * np.asarray(C, float) / 1e-6


def prix_L_brouillon(L):
    """Prix de self du brouillon du § 04.6 : 4,00 + 1,20 EUR par mH.

    CONSERVE UNIQUEMENT POUR REPRODUIRE LES CHIFFRES PUBLIES du § 04.8, et
    a ne pas utiliser autrement : associe a dcr(L) proportionnelle a L, il penalise
    DEUX FOIS le cuivre (un prix proportionnel a L suppose une masse proportionnelle a
    L, donc une DCR quasi constante -- l'inverse de ce que dcr() suppose). Les deux
    fonctions etant monotones de la seule variable L, elles sont de plus parfaitement
    correlees : le front de Pareto degenere en une droite et le satellite "self
    optimale" n'alimente plus aucun arbitrage.

    Le remplacant coherent est self_bobine : m = K_cu.(L/r)^1,5, d'ou prix ET DCR
    tires du MEME modele physique. Voir fabriques_self() ci-dessous.
    """
    return 4.0 + 1.2 * np.asarray(L, float) / 1e-3


def dcr_brouillon(L):
    """DCR du brouillon : 1 ohm a 18 mH, proportionnelle a L. Meme reserve que
    prix_L_brouillon(). C'est le jeu (A) "masse de cuivre fixee" du § 05.9 :
    self_bobine.dcr_pour(L, masse=4.25) rend exactement la meme chose (verifie a
    5.10^-5 pres), ce qui identifie la constante cachee du placeholder -- 4,25 kg de
    cuivre par self, soit 106 EUR au prix du cuivre, la ou le placeholder de prix n'en
    facturait que 25,60. L'incoherence est donc chiffree, pas seulement affirmee.
    """
    return 1.0 * np.asarray(L, float) / 18e-3


def fabriques_self(r_max=None, masse=None, d_fil=None, prix_kg=None):
    """Rend le couple COHERENT (dcr, prix_L) issu du meme modele de bobinage.

    Un seul des trois arguments, ce qui force l'appelant a dire quelle self il achete
    (§ 05.9) :
      r_max=1.5    self dimensionnee sur commande, DCR plafonnee -- la DCR ne depend
                   alors PAS de L (l'optimum de matiere sature la contrainte) et le
                   prix vaut prix_kg.K_cu.(L/r_max)^1,5 ;
      masse=4.25   budget de cuivre impose par self -> r proportionnelle a L ;
      d_fil=1.4e-3 fil deja achete -> r et masse en L^(3/5).

    Retourne (dcr, prix_L), deux callables L -> valeur, a passer tels quels a cout().
    Leve RuntimeError si self_bobine.py est absent : on ne fabrique pas un modele de
    cout en silence.
    """
    if not AVEC_SELF_BOBINE:
        raise RuntimeError(
            'fabriques_self : self_bobine.py est introuvable. Sans lui, le seul modele '
            'disponible est le couple INCOHERENT du brouillon (dcr_brouillon / '
            'prix_L_brouillon), qui penalise deux fois le cuivre -- a n utiliser que '
            'pour reproduire les chiffres publies du § 04.8.')
    kw = dict(r_max=r_max, masse=masse, d_fil=d_fil)
    prix_kw = dict(kw)
    if prix_kg is not None:
        prix_kw['prix_kg'] = prix_kg
    return SB.fabrique_dcr(**kw), SB.fabrique_prix_L(**prix_kw)


# ==================================================================================
# 3. Poids : lecture des decisions gelees (principe 4 du § 09.1)
# ==================================================================================

def poids_geles(chemin=None, exiger_geles=True, bavard=False):
    """Lit les cinq ponderations dans criteres_geles.json -> (w, source).

    "Les decisions gelees sont un fichier, pas une intention" (§ 09.1) : les
    poids de J ne doivent pas pouvoir etre retouches apres coup sans laisser de trace.
    Cette fonction est le seul chemin par lequel optim.py accepte des poids venus
    d'ailleurs que de son propre W_PROPOSE.

    exiger_geles=True (defaut) : toute marque [[a geler]] restante fait remonter
    l'exception CriteresNonGeles de io_mesures -- le code REFUSE de calculer.
    exiger_geles=False : replie sur W_PROPOSE en le DISANT (source l'indique et un
    avertissement est emis). Aucun chiffre destine a l'oral ne doit en sortir.

    Retourne (w, source) ou w a les cles 's', 'v', 'phi', 'eur', 'W' et source est une
    chaine tracant l'origine -- a recopier dans le journal de tout_refaire.py.
    """
    defaut = (dict(W_PROPOSE), 'optim.W_PROPOSE (PROPOSITION, decision D5 ouverte)')
    if not AVEC_IO:
        if exiger_geles:
            raise RuntimeError('poids_geles : io_mesures.py est introuvable, les '
                               'criteres geles ne peuvent pas etre lus.')
        if bavard:
            warnings.warn('poids_geles : io_mesures.py absent -> poids PROPOSES.')
        return defaut
    try:
        criteres = IO.lire_criteres_geles(chemin, exiger_geles=exiger_geles)
    except Exception:
        if exiger_geles:
            raise
        if bavard:
            warnings.warn('poids_geles : criteres non lisibles ou non geles -> '
                          'poids PROPOSES (aucun chiffre pour l oral).')
        return defaut

    brut = criteres.get('D5_fonction_cout', {}).get('poids', {})
    corresp = {'s': 'w_s', 'v': 'w_v', 'phi': 'w_phi', 'eur': 'w_euro', 'W': 'w_W'}
    w = {}
    for cle, cle_json in corresp.items():
        valeur = brut.get(cle_json)
        try:
            w[cle] = float(valeur)
        except (TypeError, ValueError):
            if exiger_geles:
                raise ValueError("poids_geles : D5_fonction_cout.poids.%s vaut %r, "
                                 "ce n'est pas un nombre gele." % (cle_json, valeur))
            if bavard:
                warnings.warn('poids_geles : %s non gele -> poids PROPOSES.' % cle_json)
            return defaut
    meta = criteres.get('meta', {})
    return w, ('criteres_geles.json, gele le %s, commit %s'
               % (meta.get('date_gel', '?'), meta.get('commit_gel', '?')))


# ==================================================================================
# 4. Fonction de cout (§ 04.5)
# ==================================================================================

def _db(x):
    """Module en dB, protege contre le zero exact (annulation de la somme)."""
    return 20.0 * np.log10(np.abs(x) + 1e-300)


def _masque(f, bande, nom):
    """Masque booleen d'une sous-bande ; None = toute la grille. Erreur si vide."""
    if bande is None:
        return np.ones(f.shape, dtype=bool)
    m = (f >= float(bande[0])) & (f <= float(bande[1]))
    if not m.any():
        raise ValueError('cout : la bande %s (%g-%g Hz) ne contient aucun point de la '
                         'grille f (%.1f-%.1f Hz)' % (nom, bande[0], bande[1],
                                                      f.min(), f.max()))
    return m


def _rms(e, m):
    """Ecart quadratique moyen sur le masque m, dernier axe."""
    return np.sqrt(np.mean(e[..., m] ** 2, axis=-1))


def _colonne(x, n):
    """Force un scalaire ou un tableau (n,) / (n,1) a la forme colonne (n, 1)."""
    a = np.asarray(x, dtype=float)
    if a.ndim == 0:
        return np.full((n, 1), float(a))
    return a.reshape(n, 1)


def _prep_voie_grave(p1, f, Zs, dcr, r1, Gs, Hc_pb, w, m_forme, m_phi,
                     P_ref, R_nom, prix_L, prix_C, V_crete, plancher_C1,
                     V_C1_nom, I_C1_max, zin_min, r_max):
    """Toutes les grandeurs de la voie GRAVE, de forme (n1, ...). Usage interne.

    Separer les deux voies est ce qui rend l'enumeration jointe abordable : H_pb ne
    depend que de (L1, C1) et H_ph que de (C2, L2), donc on calcule deux tableaux
    576 x Nf au lieu d'un tableau 331 776 x Nf (§ 04.5, astuce de vectorisation).
    Ne restent couples que la somme, la phase, le budget total et, en montage
    'parallele', l'impedance d'entree -- c'est exactement ce qu'il faut savoir dire au
    jury quand il demande si l'enumeration jointe n'est pas une inflation.
    """
    n1 = len(p1)
    L1 = p1[:, :1]
    C1 = p1[:, 1:]
    if r1 is not None:
        rr = _colonne(r1, n1)
    elif dcr is not None:
        rr = np.asarray(dcr(L1), dtype=float) * np.ones_like(L1)
    else:
        rr = np.zeros_like(L1)

    w_rad = 2.0 * np.pi * f
    H = F.H_pb(f, L1, C1, Zs, rr)                     # (n1, Nf), transfert ELECTRIQUE
    Zin = F.impedance_entree_pb(f, L1, C1, Zs, rr)    # (n1, Nf)

    # Forme de la voie : le gain acoustique Gs se simplifie exactement (il est present
    # des deux cotes du dB), on le laisse pour que la formule reste celle du texte.
    ecart = _db(H * Gs) - _db(Hc_pb * Gs)
    V = _rms(ecart, m_forme)

    # Pertes Joule dans la DCR, moyenne de bande sous V_ref (a ne pas confondre avec la
    # perte de POINTE, qui est ce qui dimensionne le fil de la self).
    V_ref = np.sqrt(float(R_nom) * float(P_ref))
    P = np.mean(np.abs(V_ref / Zin) ** 2 * rr, axis=1) if w['W'] else np.zeros(n1)

    EUR = np.zeros(n1)
    if prix_L is not None:
        EUR = EUR + np.asarray(prix_L(L1[:, 0]), dtype=float)
    if prix_C is not None:
        EUR = EUR + np.asarray(prix_C(C1[:, 0]), dtype=float)

    V_C = np.abs(H).max(axis=1) * V_crete                  # crete aux bornes de C1
    I_C = np.abs(1j * w_rad * C1 * H).max(axis=1) * V_crete
    zin_mini = np.abs(Zin).min(axis=1)

    pen = np.zeros(n1)
    if zin_min is not None:
        pen += np.where(zin_mini < float(zin_min), PENALITE, 0.0)
    if plancher_C1 is not None:
        pen += np.where(C1[:, 0] < float(plancher_C1), PENALITE, 0.0)
    if V_C1_nom is not None:
        pen += np.where(V_C > float(V_C1_nom), PENALITE, 0.0)
    if I_C1_max is not None:
        pen += np.where(I_C / np.sqrt(2.0) > float(I_C1_max), PENALITE, 0.0)
    if r_max is not None:
        pen += np.where(rr[:, 0] > float(r_max) * (1.0 + 1e-9), PENALITE, 0.0)

    return dict(H=H, Zin=Zin, r=rr[:, 0], V=V, P=P, EUR=EUR,
                V_C=V_C, I_C=I_C, zin_min=zin_mini, pen=pen)


def _prep_voie_medium(p2, f, Zm, dcr, r2, Gm, Hc_ph, w, m_forme, P_ref, R_nom,
                      prix_L, prix_C, V_crete, V_C2_nom, I_C2_max, zin_min, r_max,
                      protection_unilaterale, fs_med):
    """Toutes les grandeurs de la voie MEDIUM, de forme (n2, ...). Usage interne."""
    n2 = len(p2)
    C2 = p2[:, :1]
    L2 = p2[:, 1:]
    if r2 is not None:
        rr = _colonne(r2, n2)
    elif dcr is not None:
        rr = np.asarray(dcr(L2), dtype=float) * np.ones_like(L2)
    else:
        rr = np.zeros_like(L2)

    w_rad = 2.0 * np.pi * f
    H = F.H_ph(f, C2, L2, Zm, rr)                      # (n2, Nf), transfert ELECTRIQUE
    Zin = F.impedance_entree_ph(f, C2, L2, Zm, rr)

    ecart = _db(H * Gm) - _db(Hc_ph * Gm)
    if protection_unilaterale:
        # Sous fs des mediums, seul l'EXCES est penalise : proteger MIEUX que la cible
        # ne doit pas couter. Le RMS a deux cotes met "protege trop" et "protege pas
        # assez" sur le meme plan, ce qui ne peut pas porter la raison d'etre du
        # raccord (§ 04.5) -- l'optimum change de trois lignes de code.
        if fs_med is None:
            raise ValueError('cout : protection_unilaterale=True exige fs_med (Hz).')
        sous = f < float(fs_med)
        ecart = np.where(sous, np.maximum(ecart, 0.0), ecart)
    V = _rms(ecart, m_forme)

    V_ref = np.sqrt(float(R_nom) * float(P_ref))
    if w['W']:
        I_L2 = V_ref * H / (1j * w_rad * L2 + rr)
        P = np.mean(np.abs(I_L2) ** 2 * rr, axis=1)
    else:
        P = np.zeros(n2)

    EUR = np.zeros(n2)
    if prix_C is not None:
        EUR = EUR + np.asarray(prix_C(C2[:, 0]), dtype=float)
    if prix_L is not None:
        EUR = EUR + np.asarray(prix_L(L2[:, 0]), dtype=float)

    V_C = np.abs(1.0 - H).max(axis=1) * V_crete            # C2 est en SERIE
    I_C = np.abs(1j * w_rad * C2 * (1.0 - H)).max(axis=1) * V_crete
    zin_mini = np.abs(Zin).min(axis=1)

    pen = np.zeros(n2)
    if zin_min is not None:
        pen += np.where(zin_mini < float(zin_min), PENALITE, 0.0)
    if V_C2_nom is not None:
        pen += np.where(V_C > float(V_C2_nom), PENALITE, 0.0)
    if I_C2_max is not None:
        pen += np.where(I_C / np.sqrt(2.0) > float(I_C2_max), PENALITE, 0.0)
    if r_max is not None:
        pen += np.where(rr[:, 0] > float(r_max) * (1.0 + 1e-9), PENALITE, 0.0)

    return dict(H=H, Zin=Zin, r=rr[:, 0], V=V, P=P, EUR=EUR,
                V_C=V_C, I_C=I_C, zin_min=zin_mini, pen=pen)


def cout(p1, p2, f, Zs, Zm=None,
         H_ac_sub=1.0, H_ac_med=1.0, g_med=1.0,
         cible_nom='butterworth', w=None, pol=-1, dcr=None,
         P_ref=P_REF_DEFAUT, f0_cible=100.0, tau=0.0,
         bande_somme=None, bande_forme_sub=None, bande_forme_med=None,
         bande_phase=BANDE_PHASE, plancher_somme=None,
         prix_L=None, prix_C=None, budget_max=None,
         zin_min=None, montage='grave', plancher_C1=None,
         V_C_nom=None, I_C_max=None, r_max=None, r1=None, r2=None,
         P_max=F.P_NOM_E800, R_nom=F.R_NOM,
         protection_unilaterale=False, fs_med=None,
         apparie=False, detail=False, bloc=BLOC_DEFAUT):
    """Fonction de cout J du filtre -- LE coeur de l'acte 3 (§ 04.5).

        J = w_s . RMS_dB(S, S_cible)                              somme des deux voies
          + w_v . [RMS_dB(H_pb, H_pb_cible) + RMS_dB(H_ph, H_ph_cible)]  forme par voie
          + w_phi . RMS_deg(dphi, dphi_cible)                 phase entre voies, 70-140
          + w_eur . Prix                                                         euros
          + w_W . P_Joule                                     watts dans les DCR, P_ref
          + penalites dures (impedance, tension, courant, budget, ordre 2, r_max)

    ARGUMENTS GELES (§ 09.4), dans cet ordre :
      p1  tableau (n1, 2) des couples (L1, C1) de la voie GRAVE  [H, F]
      p2  tableau (n2, 2) des couples (C2, L2) de la voie MEDIUM [F, H]
      f   grille de frequences (Hz). Par defaut on prend filtre.grille_critere() :
          64 points log sur 40-250 Hz. Le pas LOG signifie qu'on pondere a energie
          constante par fraction d'octave (bruit rose) et non par hertz (bruit blanc) :
          c'est une HYPOTHESE, elle pondere lourdement le grave, elle change le
          classement des designs, et elle doit etre enoncee a l'oral.
      Zs, Zm   charges des deux voies : scalaire complexe, tableau (Nf,) ou fonction
          f -> Z. Zm=None signifie Zm = Zs (hypothese de travail a corriger des que
          l'impedance du bloc medium est mesuree).
      H_ac_sub, H_ac_med  reponses ACOUSTIQUES des haut-parleurs attaques en tension,
          mesurees en champ proche. Les laisser a 1 revient a optimiser la somme
          ELECTRIQUE alors que le critere gele est ACOUSTIQUE : c'est l'hypothese
          "HP plats et colocalises" du § 04.6, assumee tant que la phase 1
          n'a pas fourni les balayages champ proche.
      g_med   gain d'egalisation de niveau de la voie medium (L-pad ou gain d'ampli).
          Un 18" et un bloc medium n'ont aucune raison d'avoir la meme sensibilite ;
          si l'ecart n'est pas modelise, l'optimiseur le compense SILENCIEUSEMENT par
          une deformation de filtre. g_med figure des DEUX cotes (solution et cible) :
          c'est une donnee du probleme, pas une variable d'optimisation.
      cible_nom  'butterworth' | 'lr2' | 'plate' -- DECISION D2, reportee apres la
          phase 1 : jamais de constante en dur ici.
      w   dict des cinq poids ('s', 'v', 'phi', 'eur', 'W'). None -> W_PROPOSE, qui
          n'est PAS gele (voir poids_geles()).
      pol +1 (meme polarite) ou -1 (une voie inversee). Au 2e ordre l'inversion est
          OBLIGATOIRE ; la CIBLE suit la meme polarite que la solution evaluee, sans
          quoi on comparerait une somme non inversee a une cible inversee et le cout
          serait faux SANS LEVER D'ERREUR.
      dcr callable L -> r (ohm), typiquement self_bobine.fabrique_dcr(r_max=1.5).
          None -> DCR nulle (selfs parfaites). r1 / r2 permettent de fournir a la place
          des DCR MESUREES, une par ligne de p1 / p2 (mode "stock").

    ARGUMENTS DE CADRAGE (tous optionnels, tous documentes) :
      bande_somme / bande_forme_sub / bande_forme_med  sous-bandes (Hz) des trois
          termes de fidelite ; None = toute la grille f. La recommandation A3 de la
          decision D5 est 40-250 Hz pour la somme et 40-1600 Hz pour la FORME DE LA
          VOIE SUB seulement : sans cela l'optimum trouve sur 40-250 Hz fait tomber C1
          sur la borne basse (cellule du 1er ordre deguisee) et laisse le 18" rayonner
          a -23 dB a 1 kHz, defaut invisible pour une bande arretee a 250 Hz.
      plancher_somme  dB : plafonne par le bas le niveau de la somme (comme le critere
          gele du § 07.9). None par defaut, car J N'EST PAS le critere : le
          mettre a 20.0 rapproche les deux objets sans les confondre.
      budget_max  EUR : penalite dure sur le prix total des quatre composants.
      zin_min  ohm : penalite dure sur min|Z_in| (4 ohm pour le E-800). None = pas de
          contrainte. montage dit QUI voit quoi -- 'grave' (ce que regarde le J gele de
          le § 04.6), 'voie' (le plus petit des deux minimums de voie) ou
          'parallele' (les deux cellules sur un seul ampli : le cas physique reel, et
          toujours le plus bas ; il couple les deux voies, donc il coute un calcul par
          bloc). [[a trancher en phase 3 : quelle lecture entre dans la penalite dure]]
          ATTENTION AU MAILLAGE : min|Z_in| est ici cherche sur la grille de COUT (64
          points sur 40-250 Hz), qui est grossiere. Le catalogue sur la charge
          synthetique y donne 3,52 ohm, contre 3,507 ohm sur la grille fine 20-500 Hz
          en 512 points de filtre.verifier_contraintes() -- le vrai minimum tombe a
          77 Hz, entre deux points de la grille de cout. L'ecart est de 0,4 %, sans
          portee ici (on est a 12 % sous le seuil), mais un design JUSTE a la limite
          pourrait etre declare admissible a tort. La verification qui fait foi avant
          achat est filtre.verifier_contraintes(), sur sa grille fine.
      plancher_C1  F : contrainte DURE d'ordre 2 sur la cellule grave.
      V_C_nom, I_C_max  scalaire ou dict {'C1','C2'} : tenue en tension de CRETE (V) et
          courant d'ondulation admissible (A efficaces) des condensateurs achetes.
      r_max  ohm : garde-fou redondant avec le modele de self (une DCR au-dessus est
          penalisee meme si le modele l'a produite).
      protection_unilaterale, fs_med : voir _prep_voie_medium().
      apparie  False (defaut) -> J de forme (n1, n2), produit externe, par blocs.
               True  -> J de forme (n,) en APPARIANT p1[i] avec p2[i] : c'est le mode
               du Monte-Carlo, ou l'on tire n designs complets et non n^2.

    RETOUR
      J de forme (n1, n2) -- ou (n,) si apparie -- en "dB equivalents".
      detail=True : (J, termes) ou termes est un dict des cinq termes separes plus les
      diagnostics (zin_min, V_C, I_C, r, EUR, penalites). C'est ce dict qui produit la
      ligne "somme 4,26 dB, voies 8,35 dB, phase 1,9 deg, 68 EUR, pertes 2,20 W".

    VALEURS DE CONTROLE (calculees, § 04.7) : sur 8 ohm resistif, DCR nulle,
    w = W_FIDELITE, cible 'butterworth', l'enumeration E12 rend 18 mH / 150 uF sur les
    deux voies. Avec le J de reference (phase comprise) J = 0,947.

    POURQUOI CETTE SIGNATURE EST SI LONGUE, ET POURQUOI ELLE N'A PAS ETE REGROUPEE
    (note de relecture du 2026-09-14). Les 12 premiers arguments sont ceux GELES au
    § 09.4, dans l'ordre : le contrat est tenu. Les 26 suivants sont du cadrage, tous
    optionnels, tous a valeur par defaut -- un appel typique s'ecrit
    cout(p1, p2, f, Zs, Zm) et rien d'autre. Une relecture a propose, a juste titre,
    de les regrouper dans un objet de reglages pour que la fonction se lise d'un
    trait : "montrez-moi votre fonction de cout" est une question de jury certaine, la
    reponse tient sur une diapositive (six termes) et la fonction sur cinq pages.

    Ce n'est pas fait ici, et c'est un choix assume : c'est une modification
    d'INTERFACE, elle touche tous les appelants -- y compris des modules ecrits en
    parallele contre le meme contrat gele -- et elle ne corrige aucune erreur. La
    faire au milieu d'un lot de corrections de fond, c'est prendre le risque d'une
    faute que les tests ne verraient pas, pour un gain de lisibilite. Elle est
    inscrite dans LISEZMOI.md § 9 comme un geste a faire d'un seul coup, avec les
    tests, avant la phase 3.

    CE QUI EST FAIT EN ATTENDANT, et qui coute le plus a la lecture : les six termes
    de J sont assembles a la fin de la fonction sous des noms qui les designent
    (ecart_somme_dB, ecart_voies_dB, PHI, EUR, PW, PEN). Le lecteur presse peut sauter
    directement a la ligne "J = w['s'] * ... " : elle EST la formule de l'encadre
    ci-dessus, terme pour terme.
    """
    w = dict(W_PROPOSE) if w is None else dict(w)
    for cle in ('s', 'v', 'phi', 'eur', 'W'):
        w.setdefault(cle, 0.0)
    p1 = np.atleast_2d(np.asarray(p1, dtype=float))
    p2 = np.atleast_2d(np.asarray(p2, dtype=float))
    if p1.shape[1] != 2 or p2.shape[1] != 2:
        raise ValueError('cout : p1 et p2 doivent etre de forme (n, 2)')
    if apparie and len(p1) != len(p2):
        raise ValueError('cout : mode apparie -> p1 et p2 doivent avoir le meme nombre '
                         'de lignes (recu %d et %d)' % (len(p1), len(p2)))
    # Validation ET message disent desormais la meme chose : F.normaliser_cible n'admet
    # que les trois noms de D2, traduit l'alias historique 'plat' en 'lr2' avec un
    # avertissement, et leve pour tout le reste en listant les noms admis.
    cible_nom = F.normaliser_cible(cible_nom)
    if pol not in (1, -1):
        raise ValueError('cout : pol doit valoir +1 ou -1 (recu %r)' % (pol,))

    f = F.grille_critere() if f is None else np.asarray(f, dtype=float)
    Zs = np.asarray(Zs(f) if callable(Zs) else Zs)
    Zm = Zs if Zm is None else np.asarray(Zm(f) if callable(Zm) else Zm)

    # Reponses acoustiques, gain d'egalisation et retard : tout dans DEUX facteurs.
    Gs = np.asarray(H_ac_sub(f) if callable(H_ac_sub) else H_ac_sub)
    Gm = np.asarray(H_ac_med(f) if callable(H_ac_med) else H_ac_med)
    Gm = Gm * float(g_med) * np.exp(-1j * 2.0 * np.pi * f * float(tau))

    m_somme = _masque(f, bande_somme, 'somme')
    m_fs = _masque(f, bande_forme_sub, 'forme sub')
    m_fm = _masque(f, bande_forme_med, 'forme medium')
    m_phi = _masque(f, bande_phase, 'phase')

    Hc_pb, Hc_ph = F.cible(f, cible_nom, f0_cible)
    S_c = F.cible_somme(f, cible_nom, f0_cible, pol=pol, G_sub=Gs, G_med=Gm)
    dphi_c = np.angle(Hc_pb * Gs * np.conj(pol * Hc_ph * Gm))

    V_crete = F.tension_crete_amplificateur(P_max, R_nom)
    dico = lambda x, cle: (x.get(cle) if isinstance(x, dict) else x)

    a = _prep_voie_grave(p1, f, Zs, dcr, r1, Gs, Hc_pb, w, m_fs, m_phi, P_ref, R_nom,
                         prix_L, prix_C, V_crete, plancher_C1,
                         dico(V_C_nom, 'C1'), dico(I_C_max, 'C1'),
                         zin_min if montage in ('grave', 'voie') else None, r_max)
    b = _prep_voie_medium(p2, f, Zm, dcr, r2, Gm, Hc_ph, w, m_fm, P_ref, R_nom,
                          prix_L, prix_C, V_crete,
                          dico(V_C_nom, 'C2'), dico(I_C_max, 'C2'),
                          zin_min if montage == 'voie' else None, r_max,
                          protection_unilaterale, fs_med)

    n1, n2 = len(p1), len(p2)
    L_S_c = _db(S_c)
    if plancher_somme is not None:
        L_S_c = np.maximum(L_S_c, L_S_c[m_somme].max() - float(plancher_somme))

    def _somme_et_phase(Hpb, Hph):
        """Termes COUPLES (somme, phase) pour deux blocs deja diffuses."""
        S = Hpb * Gs + pol * Hph * Gm
        L_S = _db(S)
        if plancher_somme is not None:
            L_S = np.maximum(L_S, np.max(L_S[..., m_somme], axis=-1, keepdims=True)
                             - float(plancher_somme))
        ecart_somme = _rms(L_S - L_S_c, m_somme)
        d = np.angle(Hpb * Gs * np.conj(pol * Hph * Gm)) - dphi_c
        d = np.degrees((d + np.pi) % (2.0 * np.pi) - np.pi)
        return ecart_somme, _rms(d, m_phi)

    if apparie:
        ecart_somme_dB, PHI = _somme_et_phase(a['H'], b['H'])
        EUR = a['EUR'] + b['EUR']
        ecart_voies_dB = a['V'] + b['V']
        PW = a['P'] + b['P']
        PEN = a['pen'] + b['pen']
        if montage == 'parallele' and zin_min is not None:
            Zpar = a['Zin'] * b['Zin'] / (a['Zin'] + b['Zin'])
            zmin = np.abs(Zpar).min(axis=1)
            PEN = PEN + np.where(zmin < float(zin_min), PENALITE, 0.0)
        else:
            zmin = np.minimum(a['zin_min'], b['zin_min'])
    else:
        ecart_somme_dB = np.empty((n1, n2))
        PHI = np.empty((n1, n2))
        zmin = np.empty((n1, n2)) if montage == 'parallele' else None
        bloc = max(1, int(bloc))
        for i0 in range(0, n1, bloc):
            i1 = min(i0 + bloc, n1)
            Hpb = a['H'][i0:i1, None, :]
            Hph = b['H'][None, :, :]
            ecart_somme_dB[i0:i1], PHI[i0:i1] = _somme_et_phase(Hpb, Hph)
            if zmin is not None:
                Z1 = a['Zin'][i0:i1, None, :]
                Z2 = b['Zin'][None, :, :]
                zmin[i0:i1] = np.abs(Z1 * Z2 / (Z1 + Z2)).min(axis=-1)
        EUR = a['EUR'][:, None] + b['EUR'][None, :]
        ecart_voies_dB = a['V'][:, None] + b['V'][None, :]
        PW = a['P'][:, None] + b['P'][None, :]
        PEN = a['pen'][:, None] + b['pen'][None, :]
        if montage == 'parallele' and zin_min is not None:
            PEN = PEN + np.where(zmin < float(zin_min), PENALITE, 0.0)
        if zmin is None:
            zmin = np.minimum(a['zin_min'][:, None], b['zin_min'][None, :])

    if budget_max is not None:
        PEN = PEN + np.where(EUR > float(budget_max), PENALITE, 0.0)

    J = (w['s'] * ecart_somme_dB + w['v'] * ecart_voies_dB + w['phi'] * PHI
         + w['eur'] * EUR + w['W'] * PW + PEN)

    if not detail:
        return J
    # Cles du detail : les grandeurs en dB portent le suffixe _dB, les tensions et les
    # courants gardent leur nom electrique. Correction de relecture (2026-09-14) :
    # 'V_grave' valait des DECIBELS a cote de 'V_C1_crete' qui vaut des VOLTS -- un
    # lecteur de l'annexe (et Thomas dans six mois) lisait la premiere comme une tension.
    termes = dict(J=J, somme_dB=ecart_somme_dB, voies_dB=ecart_voies_dB, phase_deg=PHI,
                  prix_EUR=EUR, pertes_W=PW, penalite=PEN, zin_min=zmin,
                  voie_grave_dB=a['V'], voie_medium_dB=b['V'],
                  P_grave=a['P'], P_medium=b['P'],
                  zin_min_grave=a['zin_min'], zin_min_medium=b['zin_min'],
                  V_C1_crete=a['V_C'], V_C2_crete=b['V_C'],
                  I_C1_crete=a['I_C'], I_C2_crete=b['I_C'],
                  r1=a['r'], r2=b['r'], f=f, cible_nom=cible_nom, w=w, pol=pol)
    return J, termes


def termes_du_design(design, f, Zs, Zm=None, **kw):
    """Evalue UN design (dict L1, C1, C2, L2) et rend le detail de tous les termes.

    C'est la fonction a appeler pour produire la ligne de journal
    "J = 11,04 (somme 2,06 dB, voies 5,15 dB, phase 11,5 deg, 63 EUR, pertes 0,72 W)".
    Retourne un dict de SCALAIRES (et non de tableaux), plus 'design'.
    """
    p1 = np.array([[float(design['L1']), float(design['C1'])]])
    p2 = np.array([[float(design['C2']), float(design['L2'])]])
    kw.pop('apparie', None)
    _, t = cout(p1, p2, f, Zs, Zm, detail=True, **kw)
    plat = {}
    for cle, val in t.items():
        a = np.asarray(val) if not isinstance(val, (str, dict)) else val
        if isinstance(a, np.ndarray) and a.size == 1:
            plat[cle] = float(a.ravel()[0])
        else:
            plat[cle] = val
    plat['design'] = dict(design)
    return plat


def resume_design(design, f, Zs, Zm=None, **kw):
    """Ligne de journal lisible pour un design. Voir termes_du_design().

    LES TERMES A POIDS NUL SONT DITS "NON CALCULES", PAS "0,00" (correction de
    relecture du 2026-09-14). _prep_voie_* ne calcule les euros et les watts que si
    leur poids est non nul -- une economie legitime sur 331 776 combinaisons. Mais
    afficher "pertes 0,00 W" a cote d'un design dont le journal chiffre dix lignes
    plus bas "DCR 1,85 ohm" fait lire un resultat physique la ou il n'y a qu'un terme
    desactive. Un zero qui n'est pas une mesure doit dire qu'il n'en est pas une :
    c'est la meme regle que pour les donnees synthetiques.
    """
    t = termes_du_design(design, f, Zs, Zm, **kw)
    w = t['w']
    eur = ('%5.1f EUR' % t['prix_EUR']) if w.get('eur') else '  EUR non comptes'
    watts = ('pertes %5.2f W' % t['pertes_W']) if w.get('W') else 'pertes non comptees'
    return ("%5.1f mH / %5.1f uF | %5.1f uF / %5.1f mH : J = %8.3f "
            "(somme %5.2f dB, voies %5.2f dB, phase %5.1f deg, %s, "
            "%s, min|Zin| %5.2f ohm%s)"
            % (design['L1'] * 1e3, design['C1'] * 1e6,
               design['C2'] * 1e6, design['L2'] * 1e3, t['J'],
               t['somme_dB'], t['voies_dB'], t['phase_deg'], eur,
               watts, t['zin_min'],
               ', DISQUALIFIE' if t['penalite'] > 0 else ''))


# ==================================================================================
# 5. Enumeration exhaustive (methode de reference, numpy seul)
# ==================================================================================

def enumere_e12(f, Zs, Zm=None, L_vals=L_VALS, C_vals=C_VALS, bloc=BLOC_DEFAUT,
                garder_J=True, bavard=False, **kw):
    """Recherche EXHAUSTIVE sur la grille normalisee -> le meilleur design.

    Le minimum trouve est le minimum GLOBAL SUR LA GRILLE, sans hypothese sur la
    regularite de J ni sensibilite a l'initialisation -- contrairement a un optimiseur
    continu, qui peut converger vers un minimum local. Attention a la formulation :
    l'exhaustivite ne SUPPRIME pas les minima locaux, elle garantit de les traverser.

    Memoire : le tableau intermediaire des sommes pese 16.bloc.n2.Nf octets (28 Mo pour
    bloc = 48, n2 = 576, Nf = 64) ; sans decoupage il peserait 340 Mo a Nf = 64 et
    1,06 Go a Nf = 200 -- c'est le point qui fait planter un PC de lycee. J final,
    float64 (576, 576), pese 2,7 Mo.

    Retourne un dict : L1, C1, C2, L2 (SI), J, n_combinaisons, et si garder_J,
    la matrice J_matrice avec p1 et p2 (pour analyser_plateau() et classement()).
    Les cles L1/C1/C2/L2 sont directement utilisables comme `design`.
    """
    p1 = couples(L_vals, C_vals)
    p2 = couples(C_vals, L_vals)
    if bavard:
        print(decrire_espace(L_vals, C_vals))
    J = cout(p1, p2, f, Zs, Zm, bloc=bloc, **kw)
    i, j = np.unravel_index(int(np.argmin(J)), J.shape)
    res = dict(L1=float(p1[i, 0]), C1=float(p1[i, 1]),
               C2=float(p2[j, 0]), L2=float(p2[j, 1]),
               J=float(J[i, j]), n_combinaisons=int(J.size),
               indices=(int(i), int(j)))
    if garder_J:
        res.update(J_matrice=J, p1=p1, p2=p2, L_vals=np.asarray(L_vals, float),
                   C_vals=np.asarray(C_vals, float))
    return res


# Alias sous le nom court du squelette du § 04.6.
enumere = enumere_e12


def design_de(resultat):
    """Extrait le dict design (L1, C1, C2, L2) d'un resultat d'enumeration."""
    return {c: float(resultat[c]) for c in ('L1', 'C1', 'C2', 'L2')}


def classement(resultat, n=5):
    """Les n meilleurs designs d'une enumeration, du meilleur au moins bon.

    Retourne une liste de dicts (L1, C1, C2, L2, J, rang). Exige garder_J=True.
    """
    if 'J_matrice' not in resultat:
        raise ValueError('classement : relancer enumere_e12 avec garder_J=True')
    J = resultat['J_matrice']
    p1, p2 = resultat['p1'], resultat['p2']
    n = min(int(n), J.size)
    plats = np.argpartition(J.ravel(), n - 1)[:n]
    plats = plats[np.argsort(J.ravel()[plats])]
    sortie = []
    for rang, k in enumerate(plats, start=1):
        i, j = np.unravel_index(int(k), J.shape)
        sortie.append(dict(rang=rang, L1=float(p1[i, 0]), C1=float(p1[i, 1]),
                           C2=float(p2[j, 0]), L2=float(p2[j, 1]),
                           J=float(J[i, j])))
    return sortie


def verifier_optimum_interieur(resultat, marge=0):
    """Verifie que l'optimum n'est pas sur un BORD de la grille (test (d), § 09.6).

    Un optimum de bord ne dit pas "voici la meilleure valeur", il dit "la grille est
    trop etroite" : l'optimiseur pousse contre la butee et la vraie solution est
    ailleurs. Le cas est reel -- sur la charge typique et la bande 40-250 Hz, C1 tombe
    sur 10 uF, la borne basse, ce qui signifie "supprimez ce condensateur" et viole la
    contrainte d'ordre 2 (§ 04.8).

    Retourne (ok, avertissements). N'ecrit rien, ne leve rien : c'est a l'appelant de
    decider, mais le message est ecrit pour etre recopie tel quel dans le journal.
    """
    av = []
    bornes = {'L1': resultat.get('L_vals'), 'C1': resultat.get('C_vals'),
              'C2': resultat.get('C_vals'), 'L2': resultat.get('L_vals')}
    unite = {'L1': (1e3, 'mH'), 'L2': (1e3, 'mH'), 'C1': (1e6, 'uF'), 'C2': (1e6, 'uF')}
    for cle in ('L1', 'C1', 'C2', 'L2'):
        vals = bornes[cle]
        if vals is None:
            continue
        v = np.sort(np.asarray(vals, float))
        x = float(resultat[cle])
        k, u = unite[cle]
        if x <= v[marge]:
            av.append("%s est sur la BORNE BASSE de la grille (%.4g %s) : l'optimum est "
                      "contre la butee, donc hors domaine. Soit la grille est trop "
                      "etroite, soit une contrainte manque -- pour C1 c'est la "
                      "contrainte d'ORDRE 2 (10 uF, c'est l'absence de condensateur : "
                      "la cellule grave degenere en premier ordre et le 18 pouces "
                      "rayonne encore a -23 dB a 1 kHz, defaut invisible pour une bande "
                      "de cout arretee a 250 Hz)." % (cle, x * k, u))
        elif x >= v[-1 - marge]:
            av.append("%s est sur la BORNE HAUTE de la grille (%.4g %s) : l'optimum est "
                      "contre la butee, elargir la grille avant de conclure."
                      % (cle, x * k, u))
    return (len(av) == 0), av


# ==================================================================================
# 6. Recoupement continu (scipy, ou Nelder-Mead maison)
# ==================================================================================

def _nelder_mead_maison(fonction, x0, bornes=None, n_iter=6000, tol=1e-14):
    """Nelder-Mead ecrit a la main (REPLI sans SciPy, § 09.5).

    Simplexe de n+1 points, reflexion / expansion / contraction / retrecissement, avec
    projection sur les bornes a chaque evaluation. Ce n'est pas un pis-aller : c'est
    la meme methode que scipy, ecrite, et l'avoir ecrite est un bon argument d'oral.
    Retourne (x, valeur, n_evaluations).
    """
    x0 = np.asarray(x0, dtype=float)
    n = x0.size
    if bornes is not None:
        lo = np.array([b[0] for b in bornes], dtype=float)
        hi = np.array([b[1] for b in bornes], dtype=float)
        projeter = lambda x: np.clip(x, lo, hi)
    else:
        projeter = lambda x: x
    compteur = [0]

    def g(x):
        compteur[0] += 1
        return float(fonction(projeter(x)))

    simplexe = [projeter(x0)]
    for k in range(n):
        pas = 0.05 * max(abs(x0[k]), 1.0)
        y = x0.copy()
        y[k] += pas
        simplexe.append(projeter(y))
    simplexe = np.array(simplexe)
    valeurs = np.array([g(x) for x in simplexe])

    alpha, gamma, rho, sigma = 1.0, 2.0, 0.5, 0.5
    for _ in range(n_iter):
        ordre = np.argsort(valeurs)
        simplexe, valeurs = simplexe[ordre], valeurs[ordre]
        if np.max(np.abs(simplexe[1:] - simplexe[0])) < tol:
            break
        centre = simplexe[:-1].mean(axis=0)
        xr = projeter(centre + alpha * (centre - simplexe[-1]))
        fr = g(xr)
        if fr < valeurs[0]:
            xe = projeter(centre + gamma * (xr - centre))
            fe = g(xe)
            simplexe[-1], valeurs[-1] = (xe, fe) if fe < fr else (xr, fr)
        elif fr < valeurs[-2]:
            simplexe[-1], valeurs[-1] = xr, fr
        else:
            xc = projeter(centre + rho * (simplexe[-1] - centre))
            fc = g(xc)
            if fc < valeurs[-1]:
                simplexe[-1], valeurs[-1] = xc, fc
            else:
                simplexe[1:] = projeter(simplexe[0] + sigma * (simplexe[1:] - simplexe[0]))
                valeurs[1:] = [g(x) for x in simplexe[1:]]
    k = int(np.argmin(valeurs))
    return projeter(simplexe[k]), float(valeurs[k]), compteur[0]


def _bornes_log10(L_vals=L_VALS, C_vals=C_VALS):
    """Bornes du domaine continu, en log10 et dans l'ordre (L1, C1, C2, L2).

    BORNER N'EST PAS COSMETIQUE (§ 04.8) : non borne, l'optimiseur continu
    minimise sur log10(C1) sans plancher, donc C1 tend vers zero, l'affichage imprime
    "0 uF" et le J correspondant n'appartient PAS au domaine admissible. Ce n'est pas
    un optimum, c'est une BORNE INFERIEURE -- et c'est exactement le piege numerique a
    savoir raconter au jury.
    """
    lL = (np.log10(np.min(L_vals)), np.log10(np.max(L_vals)))
    lC = (np.log10(np.min(C_vals)), np.log10(np.max(C_vals)))
    return [lL, lC, lC, lL]


def cout_continu(x_log10, f, Zs, Zm=None, **kw):
    """J d'un design decrit par x = (log10 L1, log10 C1, log10 C2, log10 L2) -> scalaire.

    Les variables sont prises en LOG parce que le probleme est multiplicatif : les
    valeurs s'etalent sur deux decades et la grille normalisee est geometrique. En
    lineaire, un pas d'optimiseur adapte a 82 mH est aveugle a 1 mH.
    """
    x = np.asarray(x_log10, dtype=float)
    L1, C1, C2, L2 = 10.0 ** x
    kw.pop('apparie', None)
    kw.pop('detail', None)
    J = cout(np.array([[L1, C1]]), np.array([[C2, L2]]), f, Zs, Zm, **kw)
    return float(J[0, 0])


def optimiser_continu(f, Zs, Zm=None, x0=None, L_vals=L_VALS, C_vals=C_VALS,
                      methode='nelder-mead', bornes=None, graine=20260913,
                      forcer_repli=False, maxiter=None, n_redemarrages=3, **kw):
    """Recoupement CONTINU du probleme discret (§ 04.7).

    Le passage a E12 n'est pas un theoreme : c'est une PROJECTION sur une grille, et
    la grille n'est pas stable par les symetries du probleme. L'optimiseur continu dit
    donc deux choses que l'enumeration ne dit pas : (i) ou est l'optimum si l'on pouvait
    acheter n'importe quelle valeur -- ce qui est presque le cas des selfs BOBINEES
    MAISON, quasi continues puisque quantifiees par le nombre de spires ; (ii) de combien
    la contrainte E12 coute reellement.

    methode : 'nelder-mead' (rapide, local, borne) ou 'differential_evolution' (global,
    lent, graine fixee). Sans scipy, le Nelder-Mead maison prend le relais.
    x0 : depart en SI (dict design) ; None -> centre geometrique du domaine, ce qui
    evite de partir de la reponse attendue -- un sanity check qui part de la solution
    ne teste rien.

    n_redemarrages : Nelder-Mead RETRECIT son simplexe a mesure qu'il converge, et
    finit par s'arreter sur un simplexe trop plat pour explorer -- pas parce qu'il est
    au minimum, mais parce qu'il ne voit plus rien. Le remede standard est de relancer
    depuis le point trouve, ce qui re-gonfle le simplexe. Mesure sur ce probleme : en
    cible 'lr2', un seul passage s'arrete a J = 4,7.10^-2 (ecart de 1,6 % sur L2) ;
    apres UN redemarrage, J = 1,3.10^-14 et l'ecart tombe a 10^-15. La cible LR2 est
    plus difficile que la Butterworth parce que sa somme est plate pour un LR2 a
    N'IMPORTE QUELLE frequence (degenerescence du § 04.5) : la vallee est
    longue et seul le terme par voie la referme.

    Retourne un dict : L1, C1, C2, L2, J, methode, n_evaluations, n_passes, borne.
    """
    bornes = _bornes_log10(L_vals, C_vals) if bornes is None else bornes
    if x0 is None:
        x0 = np.array([0.5 * (b[0] + b[1]) for b in bornes])
    elif isinstance(x0, dict):
        x0 = np.log10([x0['L1'], x0['C1'], x0['C2'], x0['L2']])
    else:
        x0 = np.asarray(x0, dtype=float)

    fn = lambda x: cout_continu(x, f, Zs, Zm, **kw)

    if methode == 'differential_evolution':
        if not AVEC_SCIPY or forcer_repli:
            raise RuntimeError("optimiser_continu : differential_evolution exige scipy "
                               "(le repli maison n'implemente que Nelder-Mead).")
        essais = [dict(rng=graine), dict(seed=graine)]   # scipy >= 1.15 renomme seed -> rng
        derniere = None
        for extra in essais:
            try:
                sol = differential_evolution(fn, bornes, tol=1e-12, polish=True,
                                             maxiter=maxiter or 400, **extra)
                break
            except TypeError as exc:                      # pragma: no cover
                derniere = exc
        else:                                             # pragma: no cover
            raise derniere
        x, val, nev, passes = sol.x, float(sol.fun), int(sol.nfev), 1
        nom = 'scipy.differential_evolution'
    elif AVEC_SCIPY and not forcer_repli:
        x, val, nev, passes = x0, np.inf, 0, 0
        for _ in range(max(1, int(n_redemarrages) + 1)):
            sol = minimize(fn, x, method='Nelder-Mead', bounds=bornes,
                           options=dict(xatol=1e-12, fatol=1e-14,
                                        maxiter=maxiter or 3000, maxfev=maxiter or 3000))
            x, nev, passes = sol.x, nev + int(sol.nfev), passes + 1
            if np.isfinite(val) and val - float(sol.fun) <= 1e-15 * max(1.0, abs(val)):
                val = float(sol.fun)
                break                       # plus rien a gagner : on arrete de relancer
            val = float(sol.fun)
        nom = 'scipy.minimize Nelder-Mead (borne, %d passe(s))' % passes
    else:
        x, val, nev, passes = x0, np.inf, 0, 0
        for _ in range(max(1, int(n_redemarrages) + 1)):
            x, v, n = _nelder_mead_maison(fn, x, bornes, n_iter=maxiter or 3000)
            nev, passes = nev + n, passes + 1
            if np.isfinite(val) and val - v <= 1e-15 * max(1.0, abs(val)):
                val = v
                break
            val = v
        nom = 'Nelder-Mead maison, repli sans scipy (%d passe(s))' % passes

    L1, C1, C2, L2 = 10.0 ** np.asarray(x, dtype=float)
    return dict(L1=float(L1), C1=float(C1), C2=float(C2), L2=float(L2),
                J=val, methode=nom, n_evaluations=nev, n_passes=passes, borne=True)


def recouper(f, Zs, Zm=None, L_vals=L_VALS, C_vals=C_VALS, bavard=False, **kw):
    """Confronte enumeration E12 et optimiseur continu, puis ARRONDIT le continu.

    Trois chiffres sortent d'ici et il faut les distinguer :
      * discret   : le meilleur point de la grille, minimum GLOBAL sur la grille ;
      * continu   : le minimum sur le domaine borne -- toujours <= discret, c'est une
                    BORNE INFERIEURE de ce que la contrainte E12 permet d'atteindre ;
      * arrondi   : le continu projete sur la grille. Il n'est PAS toujours egal au
                    discret (§ 04.8) : l'arrondi se fait composant par composant,
                    or J n'est pas separable. Quand ils different, c'est le discret qui
                    fait foi, et le dire est plus honnete que de choisir le plus flatteur.

    Retourne un dict : discret, continu, arrondi, J_arrondi, accord (bool),
    cout_de_la_contrainte_E12 (J_discret - J_continu, en dB equivalents).
    """
    # Les deux moteurs n'acceptent pas les memes options de pilotage : on les aiguille
    # plutot que de laisser un TypeError obscur remonter depuis cout().
    cles_continu = ('x0', 'methode', 'bornes', 'graine', 'forcer_repli', 'maxiter',
                    'n_redemarrages')
    cles_enum = ('bloc', 'garder_J')
    kw_commun = {k: v for k, v in kw.items() if k not in cles_continu + cles_enum}
    kw_e = dict(kw_commun, **{k: v for k, v in kw.items() if k in cles_enum})
    kw_c = dict(kw_commun, **{k: v for k, v in kw.items() if k in cles_continu})

    d = enumere_e12(f, Zs, Zm, L_vals, C_vals, **kw_e)
    c = optimiser_continu(f, Zs, Zm, L_vals=L_vals, C_vals=C_vals, **kw_c)
    a = arrondir_design(c, L_vals, C_vals)
    J_a = termes_du_design(a, f, Zs, Zm, **kw_commun)['J']
    accord = all(abs(a[k] / d[k] - 1.0) < 1e-9 for k in ('L1', 'C1', 'C2', 'L2'))
    res = dict(discret=design_de(d), J_discret=d['J'], enumeration=d,
               continu={k: c[k] for k in ('L1', 'C1', 'C2', 'L2')}, J_continu=c['J'],
               methode_continue=c['methode'],
               arrondi=a, J_arrondi=float(J_a), accord=bool(accord),
               cout_de_la_contrainte_E12=float(d['J'] - c['J']))
    if bavard:
        print('  discret (E12)          : ' + _mm(res['discret']) + '  J = %.4f' % d['J'])
        print('  continu (%-22s): %s  J = %.4g'
              % (c['methode'][:22], _mm(res['continu']), c['J']))
        print('  arrondi du continu     : ' + _mm(a) + '  J = %.4f' % J_a)
        print('  accord arrondi/discret : %s ; cout de la contrainte E12 = %.4f dB eq.'
              % ('OUI' if accord else 'NON (le discret fait foi)',
                 res['cout_de_la_contrainte_E12']))
    return res


def _mm(d):
    """Formatage court d'un design : '18.0 mH/150 uF | 150 uF/18.0 mH'."""
    return ('%6.3g mH/%6.4g uF | %6.4g uF/%6.3g mH'
            % (d['L1'] * 1e3, d['C1'] * 1e6, d['C2'] * 1e6, d['L2'] * 1e3))


# ==================================================================================
# 7. SANITY CHECK -- porte de validation de la phase 3 (§§ 04.7 et 09.6)
# ==================================================================================

class EchecSanityCheck(AssertionError):
    """L'optimiseur ne retrouve pas la solution analytique sur charge 8 ohm.

    Ce n'est pas un avertissement : c'est un BUG dans la fonction de cout ou dans les
    cellules, et rien ne s'achete tant qu'il n'est pas corrige (§ 09.6, test b1).
    """


def sanity_check_continu(cible_nom='butterworth', R=F.R_NOM, f0_cible=100.0,
                         f=None, tolerance=1e-4, lever=True, methode='nelder-mead',
                         bavard=False, **kw):
    """PORTE DE VALIDATION, version theoreme (test b1 du § 09.6).

    Sur charge R RESISTIVE PURE, sans DCR ni penalite, le probleme continu EST celui du
    catalogue : les valeurs analytiques L = R/(Q.w0) et C = Q/(w0.R) annulent
    exactement les trois termes de fidelite (chaque voie egale sa cible, donc leur
    somme egale la somme cible), donc J = 0, donc c'est le minimum global. Un
    Nelder-Mead sur (log L, log C) doit y retomber.

    Attendu (calcule, § 04.7) :
        cible 'butterworth' -> L = 18,0063 mH, C = 140,674 uF
        cible 'lr2'/'plate' -> L = 25,4648 mH, C =  99,472 uF
    Les deux voies doivent trouver les MEMES valeurs (le probleme est symetrique).

    Les penalites dures sont DESACTIVEES ici, et c'est volontaire : ce test verifie un
    theoreme d'analyse, pas l'admissibilite d'un objet. La contrainte d'impedance est
    controlee separement par sanity_check_contraintes().

    tolerance : ecart RELATIF admis sur chaque composant. 1e-4 par defaut ; la section
    09.6 annonce 1e-6 pour l'optimiseur bien converge -- le defaut est plus lache pour
    rester passant sur une machine lente, et la valeur obtenue est toujours rendue.
    lever=True (defaut) : leve EchecSanityCheck en cas d'echec. lever=False rend le
    dict avec ok=False (pour un test unittest qui prefere assertTrue).

    Retourne un dict : cible, L_attendu, C_attendu, L, C, ecarts relatifs, J, ok.
    """
    f = F.grille_critere() if f is None else f
    Z = complex(R)
    L_th, C_th = F.composants_canoniques(cible_nom, f0_cible, R)
    opts = dict(cible_nom=cible_nom, w=W_SANITY, f0_cible=f0_cible,
                dcr=None, prix_L=None, prix_C=None,
                zin_min=None, plancher_C1=None, budget_max=None,
                V_C_nom=None, I_C_max=None, r_max=None)
    opts.update(kw)
    sol = optimiser_continu(f, Z, Z, methode=methode, **opts)

    ecarts = {'L1': sol['L1'] / L_th - 1.0, 'C1': sol['C1'] / C_th - 1.0,
              'C2': sol['C2'] / C_th - 1.0, 'L2': sol['L2'] / L_th - 1.0}
    pire = max(abs(v) for v in ecarts.values())
    ok = pire <= float(tolerance)
    res = dict(cible=cible_nom, R=float(R), f0_cible=float(f0_cible),
               L_attendu=L_th, C_attendu=C_th,
               L1=sol['L1'], C1=sol['C1'], C2=sol['C2'], L2=sol['L2'],
               ecarts=ecarts, ecart_max=float(pire), J=sol['J'],
               methode=sol['methode'], tolerance=float(tolerance), ok=bool(ok))
    if bavard:
        print('  [%s] continu %s : L = %.5f mH (attendu %.5f), C = %.4f uF '
              '(attendu %.4f) ; ecart max %.2e ; J = %.3g'
              % ('OK  ' if ok else 'ECHEC', cible_nom, sol['L1'] * 1e3, L_th * 1e3,
                 sol['C1'] * 1e6, C_th * 1e6, pire, sol['J']))
    if not ok and lever:
        raise EchecSanityCheck(
            "sanity check CONTINU en echec pour la cible '%s' sur %.3g ohm resistif :\n"
            "  attendu L = %.6f mH et C = %.6f uF (formules analytiques du catalogue)\n"
            "  obtenu  L1 = %.6f mH, C1 = %.6f uF, C2 = %.6f uF, L2 = %.6f mH\n"
            "  ecart relatif maximal %.3e > tolerance %.3e, J = %.6g\n"
            "  C'EST UN BUG : sur 8 ohm resistif le probleme continu EST celui du\n"
            "  catalogue. Corriger la fonction de cout ou les cellules AVANT tout achat."
            % (cible_nom, R, L_th * 1e3, C_th * 1e6,
               sol['L1'] * 1e3, sol['C1'] * 1e6, sol['C2'] * 1e6, sol['L2'] * 1e3,
               pire, tolerance, sol['J']))
    return res


def sanity_check_e12(cible_nom='butterworth', R=F.R_NOM, f0_cible=100.0, f=None,
                     attendu=None, lever=True, bavard=False, **kw):
    """PORTE DE VALIDATION, version discrete (test b2 du § 09.6).

    C'est un test de NON-REGRESSION, pas une verite mathematique : le passage a E12 est
    une projection sur une grille, et le gagnant discret depend legitimement de J et de
    la bande. Avec le J GELE (W_SANITY : somme + voies + phase, ni euros ni watts), sur
    8 ohm resistif, on attend :
        cible 'butterworth' -> 18,0 mH / 150 uF sur les deux voies, J = 0,9471
        cible 'lr2'/'plate' -> 27,0 mH / 100 uF sur les deux voies, J = 0,8264
    Formulation a tenir devant le jury : "sur 8 ohm le probleme continu est celui du
    catalogue ; le passage a E12 peut legitimement choisir un voisin different d'une
    voie a l'autre, ce n'est pas un bug mais une propriete de la grille."

    Le terme de phase n'est PAS decoratif ici : retire (w=W_FIDELITE), le gagnant en
    cible 'lr2' devient 27 mH / 82 uF -- voir le commentaire de W_FIDELITE. C'est un
    bon exemple de ce que "le gagnant E12 depend de J" veut dire concretement.

    Retourne un dict (design trouve, attendu, J, ok) ; leve EchecSanityCheck si lever.
    """
    f = F.grille_critere() if f is None else f
    Z = complex(R)
    attendu = CONTROLE_E12[cible_nom] if attendu is None else attendu
    opts = dict(cible_nom=cible_nom, w=W_SANITY, f0_cible=f0_cible,
                dcr=None, prix_L=None, prix_C=None,
                zin_min=None, plancher_C1=None, budget_max=None)
    opts.update(kw)
    d = enumere_e12(f, Z, Z, garder_J=True, **opts)
    L_att, C_att = attendu
    ok = (abs(d['L1'] / L_att - 1) < 1e-9 and abs(d['C1'] / C_att - 1) < 1e-9
          and abs(d['C2'] / C_att - 1) < 1e-9 and abs(d['L2'] / L_att - 1) < 1e-9)
    f0, Q, K = F.pole_et_q(d['L1'], d['C1'], R, 0.0)
    res = dict(cible=cible_nom, design=design_de(d), attendu=dict(L=L_att, C=C_att),
               J=d['J'], f0=f0, Q=Q, n_combinaisons=d['n_combinaisons'],
               ok=bool(ok), enumeration=d)
    if bavard:
        print('  [%s] E12 %-11s : %s ; J = %.4f ; f0 = %.3f Hz, Q = %.4f  '
              '[attendu %.3g mH / %.3g uF]'
              % ('OK  ' if ok else 'ECHEC', cible_nom, _mm(design_de(d)), d['J'],
                 f0, Q, L_att * 1e3, C_att * 1e6))
    if not ok and lever:
        raise EchecSanityCheck(
            "sanity check E12 en echec pour la cible '%s' sur %.3g ohm :\n"
            "  attendu %.4g mH / %.4g uF sur les deux voies\n"
            "  obtenu  %s (J = %.6f)\n"
            "  C'est un test de NON-REGRESSION : la fonction de cout a change. Soit le\n"
            "  changement est voulu et il faut mettre a jour la valeur attendue en le\n"
            "  datant, soit c'est une regression."
            % (cible_nom, R, L_att * 1e3, C_att * 1e6, _mm(design_de(d)), d['J']))
    return res


def sanity_check_contraintes(R=F.R_NOM, f=None, zin_min=F.ZIN_MIN_E800):
    """Controle que la contrainte d'impedance est bien ACTIVE et bien calibree.

    Deux faits verifies (§ 04.5, contrainte 4 ; § 04.8) :
      * le Butterworth analytique sur 8 ohm la respecte (sinon le sanity check continu
        serait fausse par une penalite) ;
      * elle disqualifie une part non negligeable de la grille meme sur 8 ohm resistif
        -- l'ordre de grandeur annonce est 162 couples (L1, C1) sur 576. Le nombre
        exact depend de la bande de frequences balayee, donc il est RENDU, pas asserte.

    Retourne un dict : zin_catalogue, zin_analytique, n_couples_violant, n_couples.
    """
    f = F.grille_critere() if f is None else np.asarray(f, float)
    Z = complex(R)
    L_th, C_th = F.composants_canoniques('butterworth', 100.0, R)
    p1 = couples(L_VALS, C_VALS)
    Zin = F.impedance_entree_pb(f, p1[:, :1], p1[:, 1:], Z, 0.0)
    zmin = np.abs(Zin).min(axis=1)
    cat = dict(L1=18e-3, C1=150e-6, C2=150e-6, L2=18e-3)
    return dict(
        zin_analytique=float(np.abs(F.impedance_entree_pb(f, L_th, C_th, Z, 0.0)).min()),
        zin_catalogue=float(np.abs(F.impedance_entree_pb(f, cat['L1'], cat['C1'],
                                                         Z, 0.0)).min()),
        n_couples=int(len(p1)), n_couples_violant=int(np.sum(zmin < float(zin_min))),
        zin_min=float(zin_min), bande=(float(f.min()), float(f.max())))


# Cles acceptees par cout() : sert au garde-fou de sanity_check_complet, qui sinon
# laisserait une faute de frappe remonter en TypeError au fond de scipy.
_CLES_COUT = frozenset(('H_ac_med', 'H_ac_sub', 'I_C_max', 'P_max', 'P_ref', 'R_nom', 'V_C_nom', 'apparie', 'bande_forme_med', 'bande_forme_sub', 'bande_phase', 'bande_somme', 'bloc', 'budget_max', 'cible_nom', 'dcr', 'detail', 'f0_cible', 'fs_med', 'g_med', 'montage', 'plancher_C1', 'plancher_somme', 'pol', 'prix_C', 'prix_L', 'protection_unilaterale', 'r1', 'r2', 'r_max', 'tau', 'w', 'zin_min'))


def sanity_check_complet(f=None, tolerance=1e-4, bavard=True, **kw):
    """Rejoue TOUTES les portes de validation, pour LES DEUX cibles (decision D2).

    A rejouer a chaque modification de la fonction de cout, AVANT tout achat
    (FEUILLE-DE-ROUTE, phase 3). Leve EchecSanityCheck au premier echec.
    Retourne la liste des dicts de resultats.
    """
    if 'cible' in kw:
        raise TypeError(
            "parametre inconnu 'cible' : la cible de sommation se nomme 'cible_nom' "
            "(valeurs : 'butterworth', 'lr2', 'plate'). Voir DECISIONS-PHASE-0.md, D2.")
    inconnus = [k for k in kw if k not in _CLES_COUT]
    if inconnus:
        raise TypeError(
            "parametre(s) inconnu(s) transmis a la fonction de cout : %s. "
            "Sans ce garde-fou, l'erreur ne remonterait qu'au fond de scipy."
            % ', '.join(sorted(inconnus)))
    sortie = []
    for cible_nom in ('butterworth', 'lr2'):
        sortie.append(sanity_check_continu(cible_nom, f=f, tolerance=tolerance,
                                           bavard=bavard, **kw))
        sortie.append(sanity_check_e12(cible_nom, f=f, bavard=bavard, **kw))
    return sortie


def verifier_vectorisation(f=None, Zs=None, Zm=None, L_vals=None, C_vals=None,
                           bavard=False, **kw):
    """Compare l'enumeration VECTORISEE a une double boucle explicite (§ 04.7).

    La version vectorisee calcule deux tableaux (576, Nf) puis un produit externe par
    blocs ; la version naive fait deux boucles Python imbriquees. Elles doivent donner
    le MEME J pour chaque combinaison, a la precision machine. C'est le seul controle
    qui attrape une erreur d'indice ou d'axe -- un bug qui, sans cela, ne se manifeste
    que par un optimum silencieusement faux.

    Sous-espace reduit par defaut (5 x 5 valeurs par voie = 625 combinaisons) pour que
    la boucle explicite reste rapide. Retourne un dict : ecart_max, ok, n_combinaisons.
    """
    f = F.grille_critere() if f is None else f
    if Zs is None:
        Zs = 8.0 + 0j
    L_vals = L_VALS[::5] if L_vals is None else np.asarray(L_vals, float)
    C_vals = C_VALS[::5] if C_vals is None else np.asarray(C_vals, float)
    p1 = couples(L_vals, C_vals)
    p2 = couples(C_vals, L_vals)

    J_vect = cout(p1, p2, f, Zs, Zm, **kw)
    J_boucle = np.empty_like(J_vect)
    for i in range(len(p1)):
        for j in range(len(p2)):
            J_boucle[i, j] = cout(p1[i:i + 1], p2[j:j + 1], f, Zs, Zm, **kw)[0, 0]

    ecart = float(np.max(np.abs(J_vect - J_boucle)))
    ok = ecart < 1e-9
    if bavard:
        print('  [%s] vectorisation vs boucle explicite : %d combinaisons, '
              'ecart max %.2e' % ('OK  ' if ok else 'ECHEC', J_vect.size, ecart))
    return dict(ecart_max=ecart, ok=bool(ok), n_combinaisons=int(J_vect.size),
                argmin_vect=int(np.argmin(J_vect)), argmin_boucle=int(np.argmin(J_boucle)))


# ==================================================================================
# 8. Le plateau : l'optimum est-il distinguable de ses voisins ? (§§ 04.8, 04.9)
# ==================================================================================

def analyser_plateau(resultat, seuil_pct=1.0, n_max=20):
    """Compte les designs dont le J est a moins de seuil_pct % de l'optimum.

    RESULTAT A ANNONCER, PAS A CACHER (§ 04.8). Sur la charge typique, quatre
    designs se tiennent a 1 % de J : la derniere marche E12 ne separe rien. Presenter
    "l'optimum" comme un point unique serait une sur-interpretation du bruit de
    modele ; la bonne formulation est "une FAMILLE de designs equivalents, dont on
    choisit le moins cher ou le plus disponible".

    Retourne un dict : n_dans_plateau, designs (liste), ecart_2e_pct, verdict (phrase).
    """
    if 'J_matrice' not in resultat:
        raise ValueError('analyser_plateau : relancer enumere_e12 avec garder_J=True')
    J = resultat['J_matrice']
    J_min = float(J.min())
    seuil = J_min * (1.0 + float(seuil_pct) / 100.0) if J_min > 0 else \
        J_min + abs(J_min) * float(seuil_pct) / 100.0 + 1e-12
    n = int(np.sum(J <= seuil))
    meilleurs = classement(resultat, min(int(n_max), max(5, n)))
    ecart_2e = (meilleurs[1]['J'] / J_min - 1.0) * 100.0 if len(meilleurs) > 1 else np.inf
    if n > 1:
        verdict = ("l'optimum est PLAT : %d designs de la grille sont a moins de %.1f %% "
                   "de J (le 2e meilleur n'est qu'a %.2f %%). Il faut donc parler d'une "
                   "FAMILLE de designs equivalents et choisir dans cette famille sur la "
                   "disponibilite, le prix ou la DCR mesuree -- pas sur la troisieme "
                   "decimale de J." % (n, seuil_pct, ecart_2e))
    else:
        verdict = ("l'optimum est ISOLE : aucun autre design de la grille n'est a moins "
                   "de %.1f %% de J (le 2e meilleur est a %.2f %%)."
                   % (seuil_pct, ecart_2e))
    return dict(J_min=J_min, seuil=float(seuil), seuil_pct=float(seuil_pct),
                n_dans_plateau=n, designs=[d for d in meilleurs if d['J'] <= seuil],
                classement=meilleurs, ecart_2e_pct=float(ecart_2e), verdict=verdict)


def monte_carlo_tolerances(design, f, Zs, Zm=None, n=2000, tol_L=0.10, tol_C=0.20,
                           loi='uniforme', graine=20260913, avec_fc=True, **kw):
    """Propagation des TOLERANCES des composants sur le critere et sur f_c (§ 04.9).

    Le composant achete n'a pas sa valeur nominale : une self de crossover est donnee a
    +/-10 % et un condensateur bipolaire a +/-20 %. Ces tolerances sont des DEMI-LARGEURS
    de loi rectangulaire ; la convention GUM retenue pour tout le TIPE est
    u = a/racine(3), et loi='uniforme' (defaut) tire exactement cela. loi='normale'
    interprete tol_L / tol_C comme des ECARTS-TYPES -- c'est le piege de la section, et
    la docstring l'ecrit.

    Ce que le tirage repond : "l'objet fabrique realisera-t-il le design calcule ?".
    Ce que le Monte-Carlo NE couvre PAS ici : l'incertitude sur Z(f) elle-meme, qui se
    propage par la covariance du fit T-S (§ 03.5) et qu'il faut tirer separement.
    Rappel de la conclusion du § 04.9 : Z(f) est un BIAIS, les tolerances sont
    une DISPERSION -- +3,8 dB systematiques sur l'ecart RMS contre +/-0,26 dB de
    dispersion toutes sources reunies. Un biais ne se reduit pas en resserrant les
    tolerances ; il ne se corrige qu'en le mesurant.

    Retourne un dict : J_nominal, J_moyen, J_ecart_type, J_quantiles (5/50/95 %),
    et si avec_fc, fc_moyen / fc_ecart_type / fc_relatif_pct (en %) -- f_c etant la
    frequence de CROISEMENT, seule definition gelee du TIPE.
    """
    rng = np.random.default_rng(graine)
    n = int(n)
    base = np.array([design['L1'], design['C1'], design['C2'], design['L2']], float)
    tol = np.array([tol_L, tol_C, tol_C, tol_L], float)
    if loi == 'uniforme':
        facteur = 1.0 + rng.uniform(-1.0, 1.0, size=(n, 4)) * tol
    elif loi == 'normale':
        facteur = 1.0 + rng.standard_normal((n, 4)) * tol
    else:
        raise ValueError("monte_carlo_tolerances : loi doit valoir 'uniforme' ou "
                         "'normale' (recu %r)" % (loi,))
    tirages = base * facteur
    p1 = tirages[:, [0, 1]]
    p2 = tirages[:, [2, 3]]

    kw_ap = dict(kw)
    kw_ap.pop('apparie', None)
    kw_ap.pop('detail', None)
    J = cout(p1, p2, f, Zs, Zm, apparie=True, **kw_ap)
    J_nom = termes_du_design(design, f, Zs, Zm, **kw_ap)['J']

    res = dict(n=n, loi=loi, graine=int(graine), tol_L=float(tol_L), tol_C=float(tol_C),
               J_nominal=float(J_nom), J_moyen=float(np.mean(J)),
               J_ecart_type=float(np.std(J, ddof=1)),
               J_quantiles=tuple(float(q) for q in np.percentile(J, [5, 50, 95])),
               J_tirages=J, tirages=tirages)

    if avec_fc:
        Zs_ev = np.asarray(Zs(f) if callable(Zs) else Zs)
        Zm_ev = Zs_ev if Zm is None else np.asarray(Zm(f) if callable(Zm) else Zm)
        dcr = kw_ap.get('dcr')
        fcs = []
        for k in range(n):
            L1, C1, C2, L2 = tirages[k]
            r1 = float(np.asarray(dcr(L1))) if dcr is not None else 0.0
            r2 = float(np.asarray(dcr(L2))) if dcr is not None else 0.0
            h1 = F.H_pb(f, L1, C1, Zs_ev, r1)
            h2 = F.H_ph(f, C2, L2, Zm_ev, r2)
            try:
                fcs.append(F.frequence_croisement(f, h1, h2, strict=False))
            except Exception:
                fcs.append(np.nan)
        fcs = np.asarray(fcs, dtype=float)
        bons = np.isfinite(fcs)
        res.update(fc_tirages=fcs, fc_n_valides=int(bons.sum()),
                   fc_moyen=float(np.mean(fcs[bons])) if bons.any() else np.nan,
                   fc_ecart_type=float(np.std(fcs[bons], ddof=1)) if bons.sum() > 1 else np.nan)
        if bons.any() and np.isfinite(res['fc_moyen']) and res['fc_moyen'] > 0:
            res['fc_relatif_pct'] = 100.0 * res['fc_ecart_type'] / res['fc_moyen']
        else:
            res['fc_relatif_pct'] = np.nan
    return res


def comparer_marche_e12_et_tolerances(resultat, f, Zs, Zm=None, n=2000,
                                      tol_L=0.10, tol_C=0.20, graine=20260913, **kw):
    """Confronte la DERNIERE MARCHE E12 a la DISPERSION due aux tolerances.

    C'est la question qui decide si "optimiser" a encore un sens a la fin : l'ecart de
    J entre le meilleur design de la grille et son voisin immediat est-il plus grand
    que l'ecart-type de J sous les tolerances des composants ? Si non -- et c'est ce
    qui est observe -- alors le classement des derniers candidats n'est pas
    significatif, et le code doit le DIRE.

    Retourne un dict : delta_J_marche_E12, sigma_J_tolerances, rapport, verdict.
    """
    cl = classement(resultat, 2)
    d1 = {c: cl[0][c] for c in ('L1', 'C1', 'C2', 'L2')}
    delta = cl[1]['J'] - cl[0]['J'] if len(cl) > 1 else np.inf
    mc = monte_carlo_tolerances(d1, f, Zs, Zm, n=n, tol_L=tol_L, tol_C=tol_C,
                                graine=graine, avec_fc=False, **kw)
    sigma = mc['J_ecart_type']
    rapport = delta / sigma if sigma > 0 else np.inf
    if rapport < 1.0:
        verdict = ("la marche E12 (%.4f dB eq.) est PLUS PETITE que la dispersion due "
                   "aux tolerances (sigma = %.4f dB eq., rapport %.2f) : le classement "
                   "des deux meilleurs designs n'est PAS significatif. Choisir sur le "
                   "prix, la disponibilite ou la DCR mesuree -- pas sur J."
                   % (delta, sigma, rapport))
    elif rapport < 3.0:
        verdict = ("la marche E12 (%.4f dB eq.) est du MEME ORDRE que la dispersion "
                   "(sigma = %.4f, rapport %.2f) : la preference pour le premier design "
                   "est faible et doit etre annoncee comme telle."
                   % (delta, sigma, rapport))
    else:
        verdict = ("la marche E12 (%.4f dB eq.) domine la dispersion (sigma = %.4f, "
                   "rapport %.2f) : le classement est significatif."
                   % (delta, sigma, rapport))
    return dict(meilleur=d1, second={c: cl[1][c] for c in ('L1', 'C1', 'C2', 'L2')}
                if len(cl) > 1 else None,
                J_meilleur=cl[0]['J'], J_second=cl[1]['J'] if len(cl) > 1 else np.inf,
                delta_J_marche_E12=float(delta), sigma_J_tolerances=float(sigma),
                rapport=float(rapport), monte_carlo=mc, verdict=verdict)


# ==================================================================================
# 9. Optimisation sur le STOCK reellement possede (§ 09.8)
# ==================================================================================

def optimiser_sur_stock(stock, f, Zs, Zm=None, reutilisation=False, bavard=False, **kw):
    """Optimise sur les composants REELLEMENT POSSEDES et MESURES (§ 09.8).

    C'est la version vraiment sobre du probleme, et elle n'est pas cosmetique : un
    condensateur +/-20 % achete a 150 uF en fait 163. Le design optimal doit etre
    recalcule sur les valeurs MESUREES, pas nominales -- et l'optimisation la plus
    econome consiste a TRIER ET APPARIER le stock plutot qu'a racheter. Benefice
    collatteral sur les incertitudes : mesures a 1 %, L et C font tomber u(f0)/f0 sous
    1 %, contre 4,1 % sur les tolerances catalogue.

    stock : dict {'L': [...], 'C': [...]} ou chaque element est
            soit un nombre (la valeur MESUREE en SI),
            soit un dict {'valeur': H ou F, 'dcr': ohm (selfs), 'ref': str,
                          'prix': EUR (0 si deja possede)}.
    reutilisation : False (defaut) = un exemplaire physique ne peut PAS servir sur les
            deux voies a la fois -- les combinaisons L1 = L2 = meme objet sont exclues.
            True = on suppose qu'on peut en racheter un identique.

    Retourne un dict comme enumere_e12, plus les references des composants choisis.
    """
    def _normaliser(liste, avec_dcr):
        vals, dcrs, prix, refs = [], [], [], []
        for k, item in enumerate(liste):
            if isinstance(item, dict):
                vals.append(float(item['valeur']))
                dcrs.append(float(item.get('dcr', 0.0)))
                prix.append(float(item.get('prix', 0.0)))
                refs.append(str(item.get('ref', '#%d' % k)))
            else:
                vals.append(float(item))
                dcrs.append(0.0)
                prix.append(0.0)
                refs.append('#%d' % k)
        return (np.array(vals), np.array(dcrs) if avec_dcr else None,
                np.array(prix), refs)

    L_val, L_dcr, L_prix, L_ref = _normaliser(stock['L'], True)
    C_val, _, C_prix, C_ref = _normaliser(stock['C'], False)
    nL, nC = len(L_val), len(C_val)
    if nL < (1 if reutilisation else 2) or nC < (1 if reutilisation else 2):
        raise ValueError('optimiser_sur_stock : il faut au moins deux selfs et deux '
                         'condensateurs distincts (ou reutilisation=True).')

    iL, iC = np.meshgrid(np.arange(nL), np.arange(nC), indexing='ij')
    iL1, iC1 = iL.ravel(), iC.ravel()
    p1 = np.column_stack([L_val[iL1], C_val[iC1]])
    r1 = L_dcr[iL1]
    jC, jL = np.meshgrid(np.arange(nC), np.arange(nL), indexing='ij')
    iC2, iL2 = jC.ravel(), jL.ravel()          # voie medium : (C2, L2), C en premier
    p2 = np.column_stack([C_val[iC2], L_val[iL2]])
    r2 = L_dcr[iL2]

    kw.pop('dcr', None)                         # les DCR viennent du stock, MESUREES
    kw.pop('prix_L', None)
    kw.pop('prix_C', None)
    J = cout(p1, p2, f, Zs, Zm, r1=r1, r2=r2, **kw)

    if not reutilisation:                       # un objet ne sert pas deux fois
        interdit = (iL1[:, None] == iL2[None, :]) | (iC1[:, None] == iC2[None, :])
        J = np.where(interdit, np.inf, J)
    i, j = np.unravel_index(int(np.argmin(J)), J.shape)
    prix_marginal = float(L_prix[iL1[i]] + C_prix[iC1[i]]
                          + C_prix[iC2[j]] + L_prix[iL2[j]])
    res = dict(L1=float(p1[i, 0]), C1=float(p1[i, 1]),
               C2=float(p2[j, 0]), L2=float(p2[j, 1]),
               r1=float(r1[i]), r2=float(r2[j]), J=float(J[i, j]),
               n_combinaisons=int(np.sum(np.isfinite(J))),
               references=dict(L1=L_ref[iL1[i]], C1=C_ref[iC1[i]],
                               C2=C_ref[iC2[j]], L2=L_ref[iL2[j]]),
               prix_marginal=prix_marginal, J_matrice=J, p1=p1, p2=p2,
               L_vals=np.sort(L_val), C_vals=np.sort(C_val))
    if bavard:
        print('  stock : %d selfs x %d condensateurs -> %s combinaisons admissibles'
              % (nL, nC, format(res['n_combinaisons'], ',d').replace(',', ' ')))
        print('  choix : L1=%s (%.4g mH, DCR %.3f ohm), C1=%s (%.4g uF) | '
              'C2=%s (%.4g uF), L2=%s (%.4g mH, DCR %.3f ohm) ; J = %.4f'
              % (res['references']['L1'], res['L1'] * 1e3, res['r1'],
                 res['references']['C1'], res['C1'] * 1e6,
                 res['references']['C2'], res['C2'] * 1e6,
                 res['references']['L2'], res['L2'] * 1e3, res['r2'], res['J']))
    return res


# ==================================================================================
# 10. Charges SYNTHETIQUES de demonstration -- AUCUNE N'EST UNE MESURE
# ==================================================================================

# Parametres TYPIQUES herites de archive-v1/_gen.py et du § 04.2. Ils servent
# uniquement a faire tourner l'auto-test : ce ne sont PAS les haut-parleurs de Thomas,
# dont Z(f) sera mesuree en phase 1. Aucun design ne doit etre achete sur leur foi.
SUB_SYNTHETIQUE = dict(Re=6.5, Le=1.2e-3, Res=44.0, fs=40.0, Qms=1.75)
MED_SYNTHETIQUE = dict(Re=6.4, Le=0.5e-3, Res=30.0, fs=60.0, Qms=3.0)


def _z_ts(f, Re, Le, Res, fs, Qms):
    """Impedance de Thiele-Small a 5 parametres (repli local, § 01).

    Utilise modele_hp.Z_ts des qu'il est importable ; sinon la meme formule, ecrite
    ici, pour que optim.py reste autonome sur une machine ou modele_hp manque.
    """
    f = np.asarray(f, dtype=float)
    w = 2.0 * np.pi * f
    ws = 2.0 * np.pi * fs
    Les = Res / (ws * Qms)
    Ces = Qms / (ws * Res)
    return Re + 1j * w * Le + 1.0 / (1.0 / Res + 1.0 / (1j * w * Les) + 1j * w * Ces)


def charge_synthetique(f, jeu=None):
    """Z(f) synthetique pour les demonstrations. ETIQUETEE, jamais presentee comme mesure."""
    p = dict(SUB_SYNTHETIQUE if jeu is None else jeu)
    try:
        from modele_hp import Z_ts
        return Z_ts(f, **p)
    except Exception:
        return _z_ts(f, **p)


# ==================================================================================
# 11. Auto-test : rejoue les valeurs de controle du § 04
# ==================================================================================

def _autotest(complet=False):
    """Rejoue les portes de validation et les illustrations du § 04."""
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    ok_global = [True]

    def note(bon):
        ok_global[0] = ok_global[0] and bool(bon)
        return 'OK  ' if bon else 'ECHEC'

    ligne = '=' * 92
    print(ligne)
    print("optim.py -- auto-test : valeurs de controle de REFERENCE-TECHNIQUE.md "
          "§§ 04.5 a 04.9")
    print("ATTENTION : toutes les charges utilisees ici sont SYNTHETIQUES. "
          "Aucun chiffre n'autorise un achat.")
    print(ligne)

    f = F.grille_critere()
    Z8 = 8.0 + 0j

    # --- 1. Espace de recherche ----------------------------------------------------
    print("\n1. Espace de recherche discret (§ 04.5, contrainte 1)")
    print(decrire_espace())
    e = espace_de_recherche()
    print("  %s  combinaisons = 24^4 attendu 331 776 : %s"
          % (format(e['n_combinaisons'], ',d').replace(',', ' '),
             note(e['n_combinaisons'] == 331776)))
    e6 = espace_de_recherche(L_VALS, C_VALS_E6)
    print("  condensateurs en E6 : %s combinaisons (attendu 82 944) : %s"
          % (format(e6['n_combinaisons'], ',d').replace(',', ' '),
             note(e6['n_combinaisons'] == 82944)))
    print("  pas de la grille L : min %.3f, max %.3f (E12 ideal %.4f) -- la serie "
          "n'est PAS exactement geometrique, c'est la norme IEC 60063, pas un bug"
          % (e['pas_min'], e['pas_max'], e['pas_ideal']))

    # --- 2. Sanity check continu, LES DEUX cibles (decision D2) --------------------
    print("\n2. PORTE DE VALIDATION, version theoreme : charge 8 ohm RESISTIVE PURE")
    print("   (penalites desactivees : on teste un theoreme d'analyse, pas "
          "l'admissibilite d'un objet)")
    for cible_nom in ('butterworth', 'lr2'):
        r = sanity_check_continu(cible_nom, f=f, tolerance=1e-4, lever=False)
        print("  [%s] %-11s : L = %9.5f mH (attendu %9.5f) ; C = %8.4f uF "
              "(attendu %8.4f) ; ecart max %.2e ; J = %.3g"
              % (note(r['ok']), cible_nom, r['L1'] * 1e3, r['L_attendu'] * 1e3,
                 r['C1'] * 1e6, r['C_attendu'] * 1e6, r['ecart_max'], r['J']))
        print("       %s : L2 = %9.5f mH, C2 = %8.4f uF (les deux voies doivent "
              "trouver les memes valeurs)"
              % (note(abs(r['ecarts']['L2']) < 1e-4 and abs(r['ecarts']['C2']) < 1e-4),
                 r['L2'] * 1e3, r['C2'] * 1e6))
    print("  moteur : %s" % sanity_check_continu('butterworth', f=f, lever=False)['methode'])

    if complet and AVEC_SCIPY:
        print("\n   recoupement par differential_evolution (global, graine fixee) :")
        for cible_nom in ('butterworth', 'lr2'):
            r = sanity_check_continu(cible_nom, f=f, tolerance=1e-3, lever=False,
                                     methode='differential_evolution')
            print("  [%s] %-11s : L = %9.5f mH, C = %8.4f uF ; ecart max %.2e ; J = %.3g"
                  % (note(r['ok']), cible_nom, r['L1'] * 1e3, r['C1'] * 1e6,
                     r['ecart_max'], r['J']))

    # --- 3. Sanity check E12 -------------------------------------------------------
    print("\n3. PORTE DE VALIDATION, version discrete (NON-REGRESSION, J gele = "
          "somme + voies + phase)")
    attendu_J = {'butterworth': 0.9471, 'lr2': 0.8264}
    for cible_nom in ('butterworth', 'lr2'):
        r = sanity_check_e12(cible_nom, f=f, lever=False)
        print("  [%s] %-11s : %s ; J = %.4f ; f0 = %.3f Hz, Q = %.4f  "
              "[attendu %.4g mH / %.4g uF, J = %.4f]"
              % (note(r['ok'] and abs(r['J'] - attendu_J[cible_nom]) < 0.005),
                 cible_nom, _mm(r['design']), r['J'], r['f0'], r['Q'],
                 r['attendu']['L'] * 1e3, r['attendu']['C'] * 1e6, attendu_J[cible_nom]))
        if cible_nom == 'butterworth':
            cl = classement(r['enumeration'], 2)
            print("       2e meilleur : %s (J = %.4f) [attendu 18 mH/150 uF | "
                  "150 uF/15 mH, J = 1,351] : le voisin E12 est a portee"
                  % (_mm(cl[1]), cl[1]['J']))
    # Contre-exemple : ce que le terme de PHASE tient reellement en cible LR2.
    r0 = sanity_check_e12('lr2', f=f, lever=False, w=W_FIDELITE)
    print("  [%s] meme cible lr2 SANS le terme de phase : %s ; J = %.4f -- le gagnant "
          "change de C1 (82 uF au lieu de 100). Ce n'est pas un bug : la propriete "
          "definitoire du LR2 est un ecart de phase NUL entre voies a toute frequence, "
          "donc c'est le terme de phase qui distingue un vrai LR2 d'un couple de "
          "cellules qui somme a peu pres plat."
          % (note(abs(r0['design']['C1'] - 82e-6) < 1e-9), _mm(r0['design']), r0['J']))

    # --- 4. Contraintes ------------------------------------------------------------
    print("\n4. Contrainte d'impedance : est-elle active et bien calibree ? "
          "(§ 04.5, contrainte 4)")
    c = sanity_check_contraintes(f=f)
    print("  min|Z_in| du Butterworth analytique sur 8 ohm : %.3f ohm (seuil %.1f) : %s"
          % (c['zin_analytique'], c['zin_min'], note(c['zin_analytique'] >= c['zin_min'])))
    print("  min|Z_in| du catalogue 18 mH/150 uF sur 8 ohm : %.3f ohm" % c['zin_catalogue'])
    print("  couples (L1, C1) violant la contrainte sur 8 ohm resistif : %d / %d "
          "(ordre de grandeur annonce : 162/576 ; le nombre exact depend de la bande "
          "%.0f-%.0f Hz)" % (c['n_couples_violant'], c['n_couples'],
                             c['bande'][0], c['bande'][1]))

    # --- 5. Vectorisation vs boucle explicite --------------------------------------
    print("\n5. Controle croise : enumeration VECTORISEE contre double boucle explicite")
    v = verifier_vectorisation(f=f, Zs=Z8, w=W_PROPOSE, prix_C=prix_C_placeholder,
                               prix_L=prix_L_brouillon, dcr=dcr_brouillon,
                               zin_min=F.ZIN_MIN_E800)
    print("  [%s] %d combinaisons, ecart max %.2e, meme argmin : %s"
          % (note(v['ok']), v['n_combinaisons'], v['ecart_max'],
             note(v['argmin_vect'] == v['argmin_boucle'])))

    # --- 6. Recoupement continu / discret ------------------------------------------
    print("\n6. Recoupement continu <-> discret sur 8 ohm (cible butterworth)")
    rec = recouper(f, Z8, Z8, cible_nom='butterworth', w=W_SANITY, bavard=True)
    print("  [%s] l'arrondi E12 du continu coincide avec l'optimum discret"
          % note(rec['accord']))

    # --- 7. Modeles de self : coherence -------------------------------------------
    print("\n7. Modele de self : le couple du brouillon est INCOHERENT, celui de "
          "self_bobine ne l'est pas (§ 04.5, contrainte 5)")
    if AVEC_SELF_BOBINE:
        ecart = float(abs(SB.dcr_pour(np.array([18e-3]), masse=4.25)[0] - 1.0))
        print("  [%s] dcr_brouillon(18 mH) = %.4f ohm == self_bobine.dcr_pour(18 mH, "
              "masse=4,25 kg) a %.1e pres : la constante cachee du placeholder est "
              "4,25 kg de cuivre par self, soit %.0f EUR -- la ou prix_L_brouillon "
              "n'en facture que %.1f."
              % (note(ecart < 1e-3), float(dcr_brouillon(18e-3)), ecart,
                 float(SB.prix_pour(18e-3, 1.0)), float(prix_L_brouillon(18e-3))))
        d15, p15 = fabriques_self(r_max=1.5)
        print("      modele coherent r_max = 1,5 ohm : DCR(33 mH) = %.2f ohm, "
              "prix(33 mH) = %.1f EUR (masse %.2f kg)"
              % (float(np.asarray(d15(33e-3))), float(p15(33e-3)),
                 float(SB.masse_pour(33e-3, 1.5))))
    else:
        print("  self_bobine.py absent : modele de cout par la masse indisponible.")

    # --- 8. Poids : lecture des criteres geles -------------------------------------
    print("\n8. Poids de J : lecture de criteres_geles.json (principe 4, § 09.1)")
    w_lu, source = poids_geles(exiger_geles=False)
    print("  source : %s" % source)
    print("  w = %s" % ', '.join('%s=%g' % (k, w_lu[k]) for k in ('s', 'v', 'phi',
                                                                  'eur', 'W')))
    if AVEC_IO:
        try:
            poids_geles(exiger_geles=True)
            print("  [ATTENTION] les criteres sont declares GELES : verifier la date "
                  "et le commit avant de citer un chiffre.")
        except Exception as exc:
            print("  [OK  ] avec exiger_geles=True le code REFUSE de calculer : %s"
                  % type(exc).__name__)

    # --- 9. Charge synthetique : illustration de la methode ------------------------
    print("\n9. Illustration sur une charge SYNTHETIQUE (§ 04.8)")
    print("   /!\\ demonstration de METHODE : parametres typiques, NON MESURES. "
          "Ne rien acheter sur ces valeurs.")
    Zs = charge_synthetique(f, SUB_SYNTHETIQUE)
    Zm = charge_synthetique(f, MED_SYNTHETIQUE)
    opts = dict(cible_nom='butterworth', w=W_PROPOSE, dcr=dcr_brouillon,
                prix_L=prix_L_brouillon, prix_C=prix_C_placeholder,
                zin_min=F.ZIN_MIN_E800, montage='grave')
    cat = dict(L1=18e-3, C1=150e-6, C2=150e-6, L2=18e-3)
    print("  catalogue  : " + resume_design(cat, f, Zs, Zm, **opts))
    import time
    t0 = time.perf_counter()
    d = enumere_e12(f, Zs, Zm, **opts)
    dt = time.perf_counter() - t0
    print("  optimise   : " + resume_design(design_de(d), f, Zs, Zm, **opts))
    print("  %s combinaisons en %.2f s"
          % (format(d['n_combinaisons'], ',d').replace(',', ' '), dt))
    ok_bord, av = verifier_optimum_interieur(d)
    for a in av:
        print("  [AVERTISSEMENT] " + a)

    # Recoupement des valeurs publiees du § 04 (non-regression sur la charge
    # synthetique). Tout est calcule, rien n'est mesure.
    t_cat = termes_du_design(cat, f, Zs, Zm, **opts)
    h1 = F.H_pb(f, 18e-3, 150e-6, Zs, 1.0)
    h2 = F.H_ph(f, 150e-6, 18e-3, Zm, 1.0)
    fc_cat = F.frequence_croisement(f, h1, h2)
    fl = np.geomspace(20.0, 500.0, 512)
    zin_fin = float(np.abs(F.impedance_entree_pb(
        fl, 18e-3, 150e-6, charge_synthetique(fl, SUB_SYNTHETIQUE), 1.0)).min())
    print("  recoupement des valeurs publiees (§ 04.2 / 04.8) :")
    print("   [%s] J du catalogue = %.2f [attendu 1017,63]   somme = %.2f dB "
          "[attendu 4,26]" % (note(abs(t_cat['J'] - 1017.63) < 0.5
                                   and abs(t_cat['somme_dB'] - 4.26) < 0.02),
                              t_cat['J'], t_cat['somme_dB']))
    print("   [%s] J de l'optimise = %.3f [attendu 11,04]    f_c du catalogue sur "
          "cette charge = %.2f Hz [attendu 102,95]"
          % (note(abs(d['J'] - 11.04) < 0.02 and abs(fc_cat - 102.95) < 0.05),
             d['J'], fc_cat))
    print("   [%s] min|Zin| du catalogue : %.3f ohm sur la grille fine 20-500 Hz "
          "[attendu 3,51 a 77 Hz] contre %.2f ohm sur la grille de cout 40-250 Hz -- "
          "c'est filtre.verifier_contraintes() qui fait foi avant achat"
          % (note(abs(zin_fin - 3.51) < 0.02), zin_fin, t_cat['zin_min']))

    # --- 10. Le plateau, et ce qu'il faut en dire ----------------------------------
    print("\n10. L'optimum est-il distinguable de ses voisins ? (§§ 04.8, 04.9)")
    pl = analyser_plateau(d, seuil_pct=1.0)
    for c_ in pl['classement'][:4]:
        print("   rang %d : %s  J = %.4f" % (c_['rang'], _mm(c_), c_['J']))
    print("   -> " + pl['verdict'])
    cmp_ = comparer_marche_e12_et_tolerances(d, f, Zs, Zm, n=600, **opts)
    print("   -> " + cmp_['verdict'])
    mc = monte_carlo_tolerances(design_de(d), f, Zs, Zm, n=600, **opts)
    print("   Monte-Carlo (L +/-10 %%, C +/-20 %%, loi rectangulaire, %d tirages, "
          "graine %d) :" % (mc['n'], mc['graine']))
    print("     J = %.3f nominal ; %.3f +/- %.3f (5-95 %% : %.3f a %.3f)"
          % (mc['J_nominal'], mc['J_moyen'], mc['J_ecart_type'],
             mc['J_quantiles'][0], mc['J_quantiles'][2]))
    print("     f_c (CROISEMENT, seule definition gelee) = %.2f +/- %.2f Hz (%.1f %%)"
          % (mc['fc_moyen'], mc['fc_ecart_type'], mc['fc_relatif_pct']))
    opts_sans = dict(opts, zin_min=None)
    mc_cat = monte_carlo_tolerances(cat, f, Zs, Zm, n=600, **opts_sans)
    print("   [%s] meme tirage sur le CATALOGUE : f_c = %.1f +/- %.1f Hz (%.1f %%) "
          "[attendu § 04.9 : 103,7 +/- 7,4 Hz, soit 7,1 %%]"
          % (note(abs(mc_cat['fc_relatif_pct'] - 7.1) < 1.0),
             mc_cat['fc_moyen'], mc_cat['fc_ecart_type'], mc_cat['fc_relatif_pct']))
    print("   Rappel de la conclusion du § 04.9, a ne pas inverser : Z(f) est "
          "un BIAIS (+3,8 dB systematiques sur l'ecart RMS), les tolerances sont une "
          "DISPERSION (+/-0,26 dB). Un biais ne se reduit pas en resserrant les "
          "tolerances -- il ne se corrige qu'en le MESURANT, puis en optimisant dessus.")

    # --- 11. Optimisation sur stock ------------------------------------------------
    print("\n11. Optimisation sur STOCK mesure (§ 09.8) -- valeurs d'exemple, "
          "SYNTHETIQUES")
    stock = dict(
        L=[dict(valeur=18.4e-3, dcr=0.95, ref='L-A'), dict(valeur=27.3e-3, dcr=1.42, ref='L-B'),
           dict(valeur=12.1e-3, dcr=0.71, ref='L-C'), dict(valeur=33.6e-3, dcr=1.70, ref='L-D')],
        C=[dict(valeur=163e-6, ref='C-A'), dict(valeur=118e-6, ref='C-B'),
           dict(valeur=99e-6, ref='C-C'), dict(valeur=12.4e-6, ref='C-D')])
    st = optimiser_sur_stock(stock, f, Zs, Zm, bavard=True,
                             cible_nom='butterworth', w=W_FIDELITE,
                             zin_min=F.ZIN_MIN_E800)
    print("   prix marginal du design : %.2f EUR (les composants sont deja possedes) "
          "-- c'est la comptabilite 'sobriete'." % st['prix_marginal'])

    print("\n" + ligne)
    print("VERDICT GLOBAL : %s" % ('tous les controles passent' if ok_global[0]
                                   else 'AU MOINS UN CONTROLE A ECHOUE'))
    print("Rappel : J n'est pas le critere gele ; aucune charge utilisee ici n'est une "
          "mesure ; l'optimum est plat.")
    print(ligne)
    return ok_global[0]


if __name__ == '__main__':
    sys.exit(0 if _autotest('--complet' in sys.argv) else 1)
