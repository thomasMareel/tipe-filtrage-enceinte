# -*- coding: utf-8 -*-
"""blueprint_mpl.py -- identite visuelle Blueprint pour matplotlib.

Voir REFERENCE-TECHNIQUE.md § 09.7 (figures : identite Blueprint) et 09.4
(signatures gelees : style_blueprint, enregistrer_svg).

CE QUE CE MODULE FAIT, EN UNE PHRASE. Il donne aux figures matplotlib exactement
les couleurs, les polices et la geometrie des diapositives du TIPE, puis il
enregistre les SVG de telle sorte que chaque couleur y soit une VARIABLE CSS
avec repli -- var(--accent, #5fd0e0) -- pour que la variante claire
(css/blueprint-light.css, utilisee a l'export PDF) recolore les courbes sans
regenerer quoi que ce soit.

LE PIEGE CENTRAL, ET IL EST FATAL SI ON LE RATE (§ 09.7). Les proprietes
personnalisees CSS sont propres a un DOCUMENT. Un SVG appele par <img src="...">
est un document independant ou --accent n'est defini nulle part : la declaration
devient invalide "at computed-value time" et la courbe disparait (trait none).
D'ou les deux precautions cumulees :
  1. chaque var() porte un REPLI : var(--accent, #5fd0e0). Le fichier est alors
     autonome hors du HTML ET recolorable une fois inline ;
  2. l'inlining se fait sur un marqueur unique <!--FIG:nom--> (voir
     figures.injecter_figures), jamais par une regex sur un aria-label -- c'est
     exactement la panne diagnostiquee sur _gen.py a la racine du depot.

"AUCUNE COULEUR FIGEE" N'EST VRAI QUE SI LE STYLE COUVRE TOUS LES rcParams. Par
defaut matplotlib ecrit #000000 pour le texte, les bords d'axes et les
graduations, et cette couleur-la echappe a la substitution : elle resterait
noire sur fond blanc dans la variante claire, illisible sur fond bleu nuit dans
la variante sombre. La liste exhaustive est fixee dans rcparams() et
enregistrer_svg() rend la liste des hexadecimaux NON substitues : c'est le
garde-fou, pas une politesse.

POLICES : CE QUI EST VENDORE N'EST PAS LISIBLE PAR MATPLOTLIB. libs/fonts/ ne
contient que des .woff2 (Inter, Space Grotesk, JetBrains Mono), format que
matplotlib ne sait pas ouvrir : il ne lit que TTF/OTF/AFM. Consequence assumee
et verifiee sur la machine du 2026-09-13 :
  - la MISE EN PAGE du texte (largeur des etiquettes, centrage) est calculee
    avec les metriques de DejaVu Sans, qui est livree avec matplotlib et donc
    presente partout : le rendu est REPRODUCTIBLE d'une machine a l'autre ;
  - le FICHIER SVG, lui, porte toute la pile demandee, parce que
    svg.fonttype='none' laisse le texte en texte et ecrit la font-family
    complete : font-family: 'Inter', 'Space Grotesk', 'DejaVu Sans', sans-serif.
    Le navigateur qui affiche la diapositive a Inter (vendoree dans
    libs/fonts/fonts.css) et l'utilise ;
  - le seul defaut residuel est un leger decalage de metrique entre le calcul
    (DejaVu) et le rendu (Inter) : a verifier a l'oeil sur les etiquettes
    longues, sans consequence sur les courbes. Aucun avertissement findfont
    n'est emis (verifie : 0 avertissement, matplotlib 3.11.0).

EXCEPTION DE CONVENTION, ASSUMEE ET LOCALISEE. Le projet impose du francais SANS
ACCENTS dans le code (console cp1252, § 09.4) : docstrings, commentaires et
messages de ce module la respectent. Les CHAINES DESSINEES DANS LES FIGURES
(titres d'axes, legendes) font exception et portent leurs accents : elles ne
transitent jamais par la console, elles sont rendues par matplotlib puis par le
navigateur, et "Frequence" sans accent sur une diapositive de concours est une
faute. Elles sont regroupees dans figures.TEXTES.

Dependances : matplotlib et numpy. Aucun acces reseau, aucune police a installer.
Fichier en UTF-8, fins de ligne LF.
"""

import logging
import os
import re
import sys

import matplotlib

# Backend non interactif : le module doit tourner dans un script, un test
# unittest ou une session sans affichage sans jamais ouvrir de fenetre.
if matplotlib.get_backend().lower() not in ('agg', 'pdf', 'svg', 'ps'):
    matplotlib.use('Agg')

import matplotlib.pyplot as plt                                  # noqa: E402
from matplotlib import font_manager                              # noqa: E402


def silence_findfont(actif=True):
    """Coupe l'avertissement findfont de matplotlib, et SEULEMENT lui.

    Le message "Failed to find font weight semibold, now using 700" est emis a
    chaque titre : DejaVu Sans, qui sert de police de METRIQUE, n'a pas de
    graisse 600. Il est sans portee, et on peut le verifier plutot que le croire
    -- le SVG produit porte bien "font-weight: 600", donc le navigateur utilise
    Inter 600, vendoree dans libs/fonts/. Le taire evite de noyer les vrais
    messages du journal de tout_refaire.py sous des centaines de lignes.
    """
    logging.getLogger('matplotlib.font_manager').setLevel(
        logging.ERROR if actif else logging.WARNING)


silence_findfont()

_ICI = os.path.dirname(os.path.abspath(__file__))
if _ICI not in sys.path:                      # rend le module importable de n'importe ou
    sys.path.insert(0, _ICI)

_RACINE = os.path.dirname(_ICI)               # racine du depot (contient css/)


# ---------------------------------------------------------------------------
# 1. Palettes -- recopiees A L'IDENTIQUE de css/blueprint.css et blueprint-light.css
# ---------------------------------------------------------------------------
#
# Toute divergence d'un seul chiffre hexadecimal casse la substitution de
# enregistrer_svg() (la couleur reste figee dans le SVG) : verifier_palettes()
# relit les deux CSS et compare, c'est un test, pas un commentaire.
#
# --grid est volontairement EXCLU : css/blueprint.css le definit en rgba(), que
# matplotlib n'emet jamais sous cette forme. La grille des figures utilise
# --trait avec une transparence (cf. rcparams : grid.alpha).

PALETTE_SOMBRE = {
    '--bg':       '#0e2230',   # bleu nuit : fond de figure
    '--bg-card':  '#0c1e2b',   # panneau plus sombre : fond des axes, des cartouches
    '--ink':      '#e6f1f4',   # texte principal
    '--ink-soft': '#8fb2bf',   # texte secondaire, courbes de reference
    '--accent':   '#5fd0e0',   # cyan  : voie 1 (grave), courbe principale
    '--accent2':  '#9ad6a0',   # vert  : voie 2 (medium)
    '--warn':     '#e0a84e',   # ambre : somme, alerte, point cle
    '--wire':     '#b8d4dc',   # fils de schema, points de mesure
    '--trait':    '#28485a',   # filets, bordures, grille
}

PALETTE_CLAIRE = {
    '--bg':       '#ffffff',
    '--bg-card':  '#f2f6f8',
    '--ink':      '#15242e',
    '--ink-soft': '#50626d',
    '--accent':   '#0e6f88',   # cyan fonce : contraste sur blanc
    '--accent2':  '#3a8a52',   # vert fonce
    '--warn':     '#b06a14',
    '--wire':     '#38505c',
    '--trait':    '#c7d2d8',
}

PALETTES = {'sombre': PALETTE_SOMBRE, 'clair': PALETTE_CLAIRE}

# Alias du prototype du § 09.7, garde pour que le code publie dans
# REFERENCE-TECHNIQUE.md reste executable tel quel.
BLUEPRINT = PALETTE_SOMBRE

# Roles semantiques : une figure ne nomme JAMAIS une couleur, elle nomme un role.
# Changer la charte revient alors a changer ce dictionnaire, pas douze figures.
SEMANTIQUE = {
    'fond':       '--bg',
    'panneau':    '--bg-card',
    'texte':      '--ink',
    'texte_doux': '--ink-soft',
    'grave':      '--accent',     # voie 1 : sub 18 pouces
    'medium':     '--accent2',    # voie 2 : bloc medium-aigu
    'somme':      '--warn',       # somme des deux voies, et alertes
    'alerte':     '--warn',
    'mesure':     '--wire',       # points "mesures" (ici : SYNTHETIQUES)
    'modele':     '--accent',     # courbe de modele ajuste
    'cible':      '--ink-soft',   # cible de sommation
    'reference':  '--ink-soft',   # courbe temoin (catalogue, 8 ohm)
    'filet':      '--trait',      # reperes verticaux, cadres, grille
}


def palette(variante='sombre'):
    """Rend la palette demandee ('sombre' ou 'clair') sous forme de dict copie."""
    if variante not in PALETTES:
        raise ValueError("variante inconnue : %r (attendu 'sombre' ou 'clair')" % (variante,))
    return dict(PALETTES[variante])


def couleur(role, variante=None):
    """Couleur hexadecimale associee a un ROLE semantique (cf. SEMANTIQUE).

    Exemple : couleur('grave') -> '#5fd0e0' en sombre, '#0e6f88' en clair.
    Sans argument 'variante', la variante active (celle du dernier appel a
    style_blueprint) est utilisee : une figure ecrite une fois sort donc juste
    dans les deux themes.
    """
    variante = variante or variante_active()
    if role in SEMANTIQUE:
        return PALETTES[variante][SEMANTIQUE[role]]
    if role in PALETTES[variante]:                      # on accepte aussi '--accent'
        return PALETTES[variante][role]
    if '--' + role in PALETTES[variante]:               # ... et 'accent'
        return PALETTES[variante]['--' + role]
    raise KeyError("role de couleur inconnu : %r" % (role,))


def verifier_palettes(dossier_css=None, bavard=True):
    """Relit css/blueprint.css et css/blueprint-light.css et compare aux palettes.

    C'est le seul garde-fou contre la derive silencieuse : si Thomas retouche une
    couleur dans le CSS, les figures deja produites gardent l'ancienne et plus
    personne ne le voit. Rend la liste des ecarts (vide = tout concorde) ; si un
    CSS est absent, le dit et rend une ligne d'avertissement plutot que de lever.
    """
    dossier_css = dossier_css or os.path.join(_RACINE, 'css')
    fichiers = [('sombre', os.path.join(dossier_css, 'blueprint.css')),
                ('clair', os.path.join(dossier_css, 'blueprint-light.css'))]
    motif = re.compile(r'(--[a-z0-9-]+)\s*:\s*(#[0-9a-fA-F]{6})')
    ecarts = []
    for variante, chemin in fichiers:
        if not os.path.exists(chemin):
            ecarts.append('%s : fichier absent (%s)' % (variante, chemin))
            continue
        with open(chemin, encoding='utf-8') as fh:
            lues = {}
            for ligne in fh:
                m = motif.search(ligne)
                if m and m.group(1) not in lues:        # premiere definition = celle de :root
                    lues[m.group(1)] = m.group(2).lower()
        for var, hexa in PALETTES[variante].items():
            if var not in lues:
                ecarts.append('%s : %s absent du CSS' % (variante, var))
            elif lues[var] != hexa.lower():
                ecarts.append('%s : %s = %s dans le CSS, %s dans blueprint_mpl'
                              % (variante, var, lues[var], hexa))
    if bavard:
        print('verifier_palettes :', 'OK, les deux CSS concordent' if not ecarts
              else '%d ecart(s)' % len(ecarts))
        for e in ecarts:
            print('   ', e)
    return ecarts


# ---------------------------------------------------------------------------
# 2. Geometrie : le livrable SCEI est un PDF 4/3 de 1024 x 768 points
# ---------------------------------------------------------------------------
#
# CALCUL, ECRIT ICI UNE FOIS POUR TOUTES.
# La diapositive reveal.js mesure 1024 x 768 px CSS (4/3), et c'est aussi la
# taille du PDF depose sur SCEI (§ 08). matplotlib raisonne en POUCES : il
# faut donc fixer une correspondance px <-> pouce, et c'est le seul role de DPI.
#
#   DPI = 160  =>  1 pouce = 160 px de diapositive
#                  diapositive entiere = 1024/160 x 768/160 = 6,40 x 4,80 po
#
# On en tire trois tailles, et pas une de plus (une charte a trois formats se
# tient ; a huit, elle ne se tient plus) :
#
#   TAILLE_DIAPO  = 5,60 x 3,30 po = 896 x 528 px
#       figure posee sous un titre h2 (1,3 em de 30 px + marges ~ 90 px) et
#       au-dessus d'une legende figcaption (~ 40 px), avec 64 px de marge
#       laterale de chaque cote : 768 - 90 - 40 - 2*55 = 528 px de haut utiles.
#       C'est le format par defaut.
#   TAILLE_HAUTE  = 5,60 x 4,10 po = 896 x 656 px
#       figure a trois panneaux (module / phase / residus) sur une diapositive
#       sans texte : on recupere la place de la legende et des marges.
#   TAILLE_PLEINE = 6,40 x 4,80 po = 1024 x 768 px
#       figure plein cadre, exactement la diapositive (usage exceptionnel).
#
# TAILLE DES CARACTERES. A DPI = 160, une police de 9 pt occupe
# 9/72 x 160 = 20 px sur la diapositive, soit 0,67 em du corps reveal.js
# (30 px) : exactement l'echelle des legendes du theme (.legende = 0,62 em).
# C'est pourquoi la base est a 9 pt et non a 10, valeur par defaut de matplotlib,
# qui donnerait un texte plus gros que la legende de la diapositive.
#
# bbox_inches='tight' recadre au contenu : la taille finale du SVG est donc
# legerement plus petite que les valeurs ci-dessus, ce qui est le comportement
# voulu (pas de marge morte qui mangerait la diapositive).

DPI = 160                       # px de diapositive par pouce matplotlib
DPI_PNG = 200                   # PNG de secours / previsualisation (1,25 x DPI)

TAILLE_DIAPO = (5.60, 3.30)     # 896 x 528 px  -- format par defaut
TAILLE_HAUTE = (5.60, 4.10)     # 896 x 656 px  -- trois panneaux
TAILLE_PLEINE = (6.40, 4.80)    # 1024 x 768 px -- diapositive entiere

# Pile de polices : voir la mise en garde du docstring de module.
#   - 'Inter' et 'Space Grotesk' ne sont PAS lisibles par matplotlib (woff2),
#     mais sont ecrites dans le SVG et utilisees par le navigateur ;
#   - 'DejaVu Sans' est livree avec matplotlib : c'est elle qui fixe les
#     metriques, donc le rendu est identique sur toute machine.
PILE_SANS = ['Inter', 'Space Grotesk', 'DejaVu Sans', 'sans-serif']
PILE_MONO = ['JetBrains Mono', 'DejaVu Sans Mono', 'monospace']

# Sel de hachage des identifiants SVG : fixe => deux executions successives
# produisent le MEME fichier octet pour octet (principe 3 du § 09.1,
# "tout chiffre montre au jury est regenerable"). Sans lui, chaque regeneration
# produirait un diff git integral.
SEL_SVG = 'tipe-filtrage-enceinte'

_VARIANTE_ACTIVE = 'sombre'
_STYLE_APPLIQUE = False        # voir figure() : filet pour un appel hors tout_generer


def variante_active():
    """Nom de la variante appliquee par le dernier style_blueprint() ('sombre')."""
    return _VARIANTE_ACTIVE


# ---------------------------------------------------------------------------
# 3. rcParams
# ---------------------------------------------------------------------------

def rcparams(variante='sombre', taille=None, echelle=1.0, fond='opaque'):
    """Jeu complet de rcParams Blueprint, rendu sous forme de dict (sans l'appliquer).

    La liste des cles de COULEUR est celle du § 09.7, verifiee
    exhaustive sur une figure |Z| + phase avec barres d'erreur et axes
    logarithmiques : toute couleur omise ici sortirait en #000000 ou #ffffff dans
    le SVG, donc NON substituable en variable CSS, donc figee a l'export PDF.

    variante : 'sombre' (diapositives) ou 'clair' (variante imprimable).
    taille   : (largeur, hauteur) en pouces ; defaut TAILLE_DIAPO.
    echelle  : multiplie toutes les tailles de caracteres (1.0 = 9 pt de base).
    fond     : 'opaque'      -> figure et axes peints avec --bg / --bg-card ;
               'transparent' -> fond non peint, la grille millimetree de la
                                diapositive reste visible derriere la figure.
                                A n'utiliser que pour une figure inlinee : un
                                PNG transparent pose sur fond blanc devient
                                illisible en variante sombre.
    """
    p = palette(variante)
    bg, card = p['--bg'], p['--bg-card']
    ink, doux, trait = p['--ink'], p['--ink-soft'], p['--trait']
    if fond == 'transparent':
        bg = card = 'none'
    elif fond != 'opaque':
        raise ValueError("fond : 'opaque' ou 'transparent', pas %r" % (fond,))
    base = 9.0 * float(echelle)
    cycle = [p['--accent'], p['--accent2'], p['--warn'], p['--wire'], p['--ink-soft'],
             p['--trait']]
    return {
        # --- figure et enregistrement -------------------------------------
        'figure.figsize': list(taille or TAILLE_DIAPO),
        'figure.dpi': DPI,
        'savefig.dpi': DPI,
        'figure.facecolor': bg,
        'figure.edgecolor': bg,
        'savefig.facecolor': bg,
        'savefig.edgecolor': bg,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.04,
        'figure.constrained_layout.use': True,
        'figure.constrained_layout.h_pad': 0.02,
        'figure.constrained_layout.w_pad': 0.02,
        'figure.titlesize': base * 1.20,
        'figure.titleweight': 'semibold',
        # --- axes ----------------------------------------------------------
        'axes.facecolor': card,
        'axes.edgecolor': trait,
        'axes.labelcolor': ink,
        'axes.titlecolor': ink,
        'axes.linewidth': 0.8,
        'axes.labelsize': base,
        'axes.titlesize': base * 1.05,
        'axes.titleweight': 'semibold',
        'axes.titlelocation': 'left',
        'axes.titlepad': 5.0,
        'axes.labelpad': 3.0,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.axisbelow': True,
        'axes.prop_cycle': plt.cycler(color=cycle),
        'axes.unicode_minus': True,
        # --- grille ---------------------------------------------------------
        # --grid du CSS est en rgba() : on utilise --trait + transparence, ce que
        # matplotlib sait ecrire (fill:#28485a + opacity) donc substituable.
        'axes.grid': True,
        'axes.grid.which': 'both',
        'grid.color': trait,
        'grid.alpha': 0.55,
        'grid.linewidth': 0.5,
        'grid.linestyle': '-',
        # --- graduations -----------------------------------------------------
        'xtick.color': trait,
        'ytick.color': trait,
        'xtick.labelcolor': doux,
        'ytick.labelcolor': doux,
        'xtick.labelsize': base * 0.88,
        'ytick.labelsize': base * 0.88,
        'xtick.direction': 'out',
        'ytick.direction': 'out',
        'xtick.major.size': 3.0,
        'ytick.major.size': 3.0,
        'xtick.minor.size': 1.6,
        'ytick.minor.size': 1.6,
        'xtick.major.width': 0.7,
        'ytick.major.width': 0.7,
        'xtick.minor.width': 0.5,
        'ytick.minor.width': 0.5,
        # --- texte ------------------------------------------------------------
        'text.color': ink,
        'font.family': 'sans-serif',
        'font.sans-serif': list(PILE_SANS),
        'font.monospace': list(PILE_MONO),
        'font.size': base,
        'mathtext.fontset': 'dejavusans',
        # --- traits et marqueurs ------------------------------------------------
        'lines.color': p['--accent'],
        'lines.linewidth': 1.6,
        'lines.markersize': 3.2,
        'lines.markeredgewidth': 0.8,
        'lines.solid_capstyle': 'round',
        'patch.edgecolor': trait,
        'patch.facecolor': p['--accent'],
        'patch.linewidth': 0.8,
        'hatch.color': trait,
        'hatch.linewidth': 0.6,
        'errorbar.capsize': 1.6,
        # --- legende -------------------------------------------------------------
        'legend.facecolor': p['--bg-card'],     # jamais 'none' : la legende doit
        'legend.edgecolor': trait,              # rester lisible par-dessus une courbe
        'legend.labelcolor': ink,
        'legend.framealpha': 0.88,
        'legend.fontsize': base * 0.88,
        'legend.borderpad': 0.35,
        'legend.labelspacing': 0.3,
        'legend.handlelength': 1.6,
        'legend.handletextpad': 0.5,
        'legend.borderaxespad': 0.3,
        'legend.fancybox': False,
        # --- sortie SVG -----------------------------------------------------------
        'svg.fonttype': 'none',     # le texte reste du texte : leger, et rendu par
                                    # les polices vendorees dans libs/fonts/
        'svg.hashsalt': SEL_SVG,    # identifiants stables => fichier reproductible
        'path.simplify': True,
        'path.simplify_threshold': 0.111111,
    }


def style_blueprint(variante='sombre', appliquer=True, taille=None, echelle=1.0,
                    fond='opaque'):
    """Applique l'identite Blueprint aux rcParams matplotlib (signature § 09.4).

    Appelable sans argument : style_blueprint(). Rend le dict effectivement
    applique, pour qu'un test puisse verifier qu'aucune cle de couleur ne manque.
    Met a jour la variante active, dont dependent couleur() et enregistrer_svg().
    """
    global _VARIANTE_ACTIVE, _STYLE_APPLIQUE
    rc = rcparams(variante, taille=taille, echelle=echelle, fond=fond)
    if appliquer:
        plt.rcParams.update(rc)
        _VARIANTE_ACTIVE, _STYLE_APPLIQUE = variante, True
    return rc


class style(object):
    """Gestionnaire de contexte : applique le style, puis restaure l'etat anterieur.

    Utile pour produire la variante claire sans contaminer le reste du script :

        with style('clair'):
            fig = ma_figure()
            enregistrer(fig, 'fig-truc-clair')
    """

    def __init__(self, variante='sombre', **kw):
        self.variante, self.kw = variante, kw
        self._avant, self._variante_avant = None, None

    def __enter__(self):
        self._avant = dict(plt.rcParams)
        self._variante_avant = _VARIANTE_ACTIVE
        style_blueprint(self.variante, **self.kw)
        return self

    def __exit__(self, *args):
        global _VARIANTE_ACTIVE
        plt.rcParams.update(self._avant)
        _VARIANTE_ACTIVE = self._variante_avant
        return False


# ---------------------------------------------------------------------------
# 4. Enregistrement : substitution des couleurs en variables CSS
# ---------------------------------------------------------------------------

_MOTIF_HEXA = re.compile(r'#[0-9a-fA-F]{6}(?![0-9a-fA-F])')
_MOTIF_REPLI = re.compile(r'var\(--[a-z0-9-]+,\s*#[0-9a-fA-F]{6}\)')
_MOTIF_BALISE_SVG = re.compile(r'<svg[^>]*>')
_MOTIF_DIMENSION = re.compile(r'\s(?:width|height)="[^"]*"')
_MOTIF_VIEWBOX = re.compile(r'viewBox="([\d.eE+-]+) ([\d.eE+-]+) ([\d.eE+-]+) ([\d.eE+-]+)"')


def _sans_dimensions(svg):
    """Retire width= et height= de la balise <svg> racine, en gardant le viewBox.

    POURQUOI, ET CE N'EST PAS UN DETAIL DE MISE EN PAGE. matplotlib ecrit la
    taille en POINTS (width="406.08pt") : un navigateur rendrait alors la figure
    a 406 x 1,333 = 541 px de large, soit la moitie d'une diapositive de
    1024 px, et tout le calcul de taille de caracteres du § 2 tomberait
    a cote. Les SVG deja inlines dans presentation-finale.html n'ont, eux, qu'un
    viewBox, et css/blueprint.css les dimensionne : `.reveal .viz svg
    { width:100%; height:auto; max-height:500px; }`. On adopte la meme
    convention : sans width/height, la figure occupe la largeur de son conteneur
    (~896 px sur une diapositive), le viewBox conserve les proportions, et 9 pt
    de texte y font bien les 20 px annonces. Hors HTML, un SVG sans dimensions
    s'affiche a la taille de la fenetre : le fichier reste donc lisible seul.
    """
    balise = _MOTIF_BALISE_SVG.search(svg)
    if not balise or 'viewBox' not in balise.group(0):    # pas de viewBox : on ne
        return svg                                        # touche a rien, on casserait
    return svg.replace(balise.group(0),
                       _MOTIF_DIMENSION.sub('', balise.group(0)), 1)


def geometrie_svg(chemin, dpi=DPI):
    """Rend (largeur_pt, hauteur_pt, largeur_px, hauteur_px) d'un SVG produit ici.

    Les px sont ceux de la diapositive 1024 x 768 : viewBox en points (1/72 po)
    converti a DPI px/po. Sert a verifier qu'une figure tient dans la zone utile
    (896 x 528 px pour TAILLE_DIAPO).
    """
    with open(chemin, encoding='utf-8') as fh:
        tete = fh.read(4096)
    m = _MOTIF_VIEWBOX.search(tete)
    if not m:
        raise ValueError('viewBox introuvable dans %s' % (chemin,))
    l_pt, h_pt = float(m.group(3)), float(m.group(4))
    return l_pt, h_pt, l_pt * dpi / 72.0, h_pt * dpi / 72.0


_MOTIF_STYLE = re.compile(r'\sstyle="([^"]{20,})"')


def _factoriser_styles(svg, prefixe, seuil=3):
    """Deplace les attributs style repetes dans un bloc <style>. SANS PERTE.

    matplotlib recopie l'attribut style en entier sur chaque element dessine :
    une courbe de 130 points en errorbar produit pres d'un millier de <use>
    portant tous la meme chaine d'une centaine de caracteres. La moitie du
    fichier est alors une repetition.

    On remplace chaque style vu au moins `seuil` fois par une classe, definie une
    seule fois. Aucun point de donnee n'est retire et aucune couleur n'est
    changee : c'est une reecriture a rendu identique.

    POURQUOI CA COMPTE ICI. Les SVG sont inlines dans les diapositives, et le PDF
    exporte doit tenir sous les 5 Mo imposes par le SCEI (REFERENCE-TECHNIQUE.md
    § 08.2). C'est une contrainte dure du livrable.

    Le prefixe rend les classes propres a la figure : deux SVG inlines dans la
    meme page HTML ne peuvent pas se voler leurs regles.

    Rend (svg_reecrit, nombre_de_classes_creees).
    """
    styles = {}
    for m in _MOTIF_STYLE.finditer(svg):
        styles[m.group(1)] = styles.get(m.group(1), 0) + 1
    repetes = [s for s, n in styles.items() if n >= seuil]
    if not repetes:
        return svg, 0
    # Ordre decroissant de gain : on nomme d'abord ce qui pese le plus.
    repetes.sort(key=lambda s: -len(s) * styles[s])
    regles, classes = [], {}
    for i, style in enumerate(repetes):
        nom = '%s-s%d' % (prefixe, i)
        classes[style] = nom
        regles.append('.%s{%s}' % (nom, style.replace('; ', ';')))

    def _remplacer(m):
        nom = classes.get(m.group(1))
        return ' class="%s"' % nom if nom else m.group(0)

    svg = _MOTIF_STYLE.sub(_remplacer, svg)
    bloc = '<style type="text/css">' + ''.join(regles) + '</style>'
    # On insere juste apres la balise <svg ...> ouvrante.
    fin = svg.index('>', svg.index('<svg')) + 1
    return svg[:fin] + chr(10) + bloc + svg[fin:], len(repetes)


def enregistrer_svg(fig, chemin, variante=None):
    """Enregistre la figure en SVG, couleurs remplacees par des variables CSS.

    Signature gelee (§ 09.4) : enregistrer_svg(fig, chemin). L'argument
    'variante' est nomme et facultatif ; par defaut c'est la variante active, ce
    qui est le comportement attendu dans 100 % des appels.

    Chaque couleur de la palette devient var(--nom, #hexa) : AVEC LE REPLI, sans
    quoi le fichier serait noir hors du document HTML (cf. docstring de module).

    Rend (compte, hexadecimaux_non_substitues) :
      - compte : nombre de substitutions par variable, pour voir d'un coup d'oeil
        qu'une variable n'a pas ete oubliee ;
      - hexadecimaux_non_substitues : LISTE QUI DOIT ETRE VIDE. Tout element
        est une couleur figee, donc une couleur qui restera fausse dans la
        variante claire a l'export PDF. C'est le critere chiffre du test (h).
    """
    variante = variante or variante_active()
    dossier = os.path.dirname(os.path.abspath(chemin))
    if dossier and not os.path.isdir(dossier):
        os.makedirs(dossier)
    # metadata Date=None : sans cela matplotlib date le SVG et deux executions
    # identiques produisent deux fichiers differents (diff git a chaque relance).
    fig.savefig(chemin, format='svg', bbox_inches='tight', metadata={'Date': None})
    with open(chemin, encoding='utf-8') as fh:
        svg = fh.read()
    compte = {}
    for var, hexa in PALETTES[variante].items():
        svg, n = re.compile(re.escape(hexa), re.IGNORECASE).subn(
            'var(%s, %s)' % (var, hexa), svg)
        compte[var] = n
    svg = _sans_dimensions(svg)                # cf. docstring : points -> conteneur
    # Factorisation des styles repetes : sans perte, et indispensable pour que le
    # PDF exporte tienne sous les 5 Mo du SCEI (cf. _factoriser_styles).
    prefixe = re.sub(r'[^a-z0-9]+', '-',
                     os.path.splitext(os.path.basename(chemin))[0].lower()).strip('-')
    svg, _n_classes = _factoriser_styles(svg, prefixe or 'fig')
    with open(chemin, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(svg)
    nu = _MOTIF_REPLI.sub('', svg)                     # on retire les replis legitimes
    return compte, sorted(set(_MOTIF_HEXA.findall(nu)))


def verifier_svg(chemin):
    """Relit un SVG deja ecrit et rend la liste de ses couleurs NON substituees.

    Sert au test (h) et a l'auto-verification de figures.tout_generer : on peut
    controler un fichier sans avoir la figure matplotlib qui l'a produit.
    """
    with open(chemin, encoding='utf-8') as fh:
        svg = fh.read()
    return sorted(set(_MOTIF_HEXA.findall(_MOTIF_REPLI.sub('', svg))))


def enregistrer(fig, nom, dossier, formats=('svg', 'png'), variante=None,
                fermer=True, dpi_png=DPI_PNG):
    """Enregistre une figure sous <dossier>/<nom>.<ext> pour chaque format demande.

    SVG : format de reference, vectoriel, couleurs en variables CSS, inline dans
          les diapositives par figures.injecter_figures.
    PNG : confort (previsualisation, repli bitmap de l'export PDF decrit dans
          EXPORT-PDF.md). Les couleurs y sont FIGEES -- un PNG sombre ne se
          recolore pas -- d'ou la variante '-clair' produite separement.

    Rend un dict : chemins par format, taille en octets, compte des
    substitutions, hexadecimaux non substitues.
    """
    variante = variante or variante_active()
    if not os.path.isdir(dossier):
        os.makedirs(dossier)
    resultat = {'nom': nom, 'variante': variante, 'chemins': {}, 'octets': {},
                'substitutions': {}, 'hexa_figes': []}
    for ext in formats:
        chemin = os.path.join(dossier, nom + '.' + ext)
        if ext == 'svg':
            compte, figes = enregistrer_svg(fig, chemin, variante=variante)
            resultat['substitutions'], resultat['hexa_figes'] = compte, figes
            resultat['px'] = tuple(round(v) for v in geometrie_svg(chemin)[2:])
        elif ext == 'png':
            fig.savefig(chemin, format='png', dpi=dpi_png, bbox_inches='tight')
        elif ext == 'pdf':
            fig.savefig(chemin, format='pdf', bbox_inches='tight')
        else:
            raise ValueError('format inconnu : %r (svg, png ou pdf)' % (ext,))
        resultat['chemins'][ext] = chemin
        resultat['octets'][ext] = os.path.getsize(chemin)
    if fermer:
        plt.close(fig)
    return resultat


# ---------------------------------------------------------------------------
# 5. Briques de dessin communes a toutes les figures
# ---------------------------------------------------------------------------

def figure(nlignes=1, ncolonnes=1, taille=None, hauteurs=None, largeurs=None, **kw):
    """Cree (fig, axes) au format Blueprint. Enveloppe mince de plt.subplots.

    taille    : (largeur, hauteur) en pouces ; defaut = rcParams (TAILLE_DIAPO).
    hauteurs / largeurs : proportions des panneaux (gridspec height_ratios).

    Si le style n'a jamais ete applique dans la session, il l'est ici. Sans ce
    filet, appeler une figure directement depuis une console produirait des
    courbes aux couleurs Blueprint sur des axes matplotlib par defaut -- du
    texte noir sur fond bleu nuit, illisible, et surtout des hexadecimaux non
    substituables a l'enregistrement.
    """
    if not _STYLE_APPLIQUE:
        style_blueprint()
    gridspec = dict(kw.pop('gridspec_kw', {}) or {})
    if hauteurs is not None:
        gridspec['height_ratios'] = list(hauteurs)
    if largeurs is not None:
        gridspec['width_ratios'] = list(largeurs)
    fig, axes = plt.subplots(nlignes, ncolonnes,
                             figsize=taille or plt.rcParams['figure.figsize'],
                             gridspec_kw=gridspec or None, **kw)
    return fig, axes


def fr(valeur, format='%g'):
    """Formate un nombre a la francaise : virgule decimale.

    "18,0 mH" et non "18.0 mH". Le projet ecrit ses nombres en francais partout
    (REFERENCE-TECHNIQUE.md, les diapositives), il n'y a pas de raison que les
    figures soient les seules a parler anglais. Ne s'applique QU'AUX CHAINES
    DESSINEES : les fichiers de donnees, eux, gardent le point decimal, sans
    quoi plus rien ne se relit avec numpy (§ 09.3).
    """
    return (format % valeur).replace('.', ',')


REPERES_FREQUENCE = [10, 20, 30, 50, 70, 100, 150, 200, 300, 500, 700, 1000]
REPERES_FREQUENCE_LARGE = [10, 20, 50, 100, 200, 500, 1000]
REPERES_IMPEDANCE = [2, 3, 4, 5, 6, 8, 10, 15, 20, 30, 40, 50, 70, 100, 150, 200, 300, 500]


def axe_log(ax, axe='x', reperes=(), bornes=None, etiquette=None, format='%g'):
    """Echelle logarithmique avec des graduations LISIBLES sur une diapositive.

    Par defaut matplotlib ecrit 2 x 10^-1 et 4 x 10^-1 en echelle log, ce qui
    donne sur un panneau etroit une bouillie d'exposants qui se chevauchent.
    Personne ne lit "4 x 10 puissance -1" : tout le monde lit 0,4. On impose
    donc des valeurs rondes, et seulement celles qui tiennent dans les bornes.
    """
    from matplotlib.ticker import FixedLocator, FixedFormatter, NullFormatter
    axis = ax.xaxis if axe == 'x' else ax.yaxis
    (ax.set_xscale if axe == 'x' else ax.set_yscale)('log')
    if bornes is not None:
        (ax.set_xlim if axe == 'x' else ax.set_ylim)(*bornes)
    bas, haut = (ax.get_xlim() if axe == 'x' else ax.get_ylim())
    vals = [v for v in reperes if bas <= v <= haut]
    if len(vals) >= 2:
        axis.set_major_locator(FixedLocator(vals))
        axis.set_major_formatter(FixedFormatter([fr(v, format) for v in vals]))
        axis.set_minor_formatter(NullFormatter())
    if etiquette:
        (ax.set_xlabel if axe == 'x' else ax.set_ylabel)(etiquette)
    return ax


def axe_frequence(ax, f1=20.0, f2=500.0, etiquette=True, textes=None, reperes=None):
    """Axe des frequences : echelle log, graduations rondes, bornes imposees.

    reperes : liste de frequences a graduer ; par defaut REPERES_FREQUENCE, a
    remplacer par REPERES_FREQUENCE_LARGE sur un panneau etroit (deux figures
    cote a cote), ou les etiquettes se chevaucheraient.
    """
    axe_log(ax, 'x', reperes if reperes is not None else REPERES_FREQUENCE,
            bornes=(f1, f2))
    if etiquette:
        ax.set_xlabel((textes or {}).get('frequence', 'Fréquence (Hz)'))
    return ax


def axe_impedance(ax, zmin=None, zmax=None, reperes=None, etiquette=None):
    """Axe |Z| logarithmique gradue en ohms ronds (5, 10, 20, 50...)."""
    bornes = (zmin, zmax) if (zmin is not None and zmax is not None) else None
    return axe_log(ax, 'y', reperes or REPERES_IMPEDANCE, bornes=bornes,
                   etiquette=etiquette)


def repere_vertical(ax, f, texte=None, role='filet', haut=0.94, style_trait='--'):
    """Trace un repere vertical (100 Hz, f_s, f_c...) avec son etiquette.

    Le trait est sous les courbes (axisbelow) et l'etiquette est en petit, en
    haut : une frequence remarquable doit se voir sans masquer la mesure.
    """
    ax.axvline(f, color=couleur(role), linewidth=0.9, linestyle=style_trait, zorder=1.5)
    if texte:
        ax.annotate(texte, xy=(f, haut), xycoords=('data', 'axes fraction'),
                    ha='center', va='top', fontsize=plt.rcParams['font.size'] * 0.80,
                    color=couleur('texte_doux'),
                    bbox=dict(boxstyle='round,pad=0.18', facecolor=couleur('panneau'),
                              edgecolor=couleur('filet'), linewidth=0.5, alpha=0.9))
    return ax


def cartouche(ax, texte, position='haut gauche', role='texte_doux', mono=True,
              cadre=True):
    """Pose un petit cartouche de texte dans un coin des axes (valeurs, verdict).

    C'est l'equivalent du .chip des diapositives : on y met les chiffres qu'on
    citerait a l'oral, pour que la figure se suffise a elle-meme en annexe.

    `position` est un coin nomme, ou un quadruplet (x, y, ha, va) en fraction
    des axes quand aucun coin n'est libre -- cas de l'impedance bass-reflex, dont
    les deux pics et le creux occupent les deux coins bas et le coin haut droit.
    """
    coins = {'haut gauche': (0.02, 0.97, 'left', 'top'),
             'haut droite': (0.98, 0.97, 'right', 'top'),
             'bas gauche': (0.02, 0.03, 'left', 'bottom'),
             'bas droite': (0.98, 0.03, 'right', 'bottom')}
    if isinstance(position, tuple) and len(position) == 4:
        x, y, ha, va = position
    elif position in coins:
        x, y, ha, va = coins[position]
    else:
        raise ValueError('position inconnue : %r' % (position,))
    return ax.text(x, y, texte, transform=ax.transAxes, ha=ha, va=va,
                   fontsize=plt.rcParams['font.size'] * 0.80, color=couleur(role),
                   family='monospace' if mono else 'sans-serif', linespacing=1.35,
                   bbox=(dict(boxstyle='round,pad=0.30', facecolor=couleur('panneau'),
                              edgecolor=couleur('filet'), linewidth=0.6, alpha=0.92)
                         if cadre else None), zorder=6)


def reserver_bande(fig, haut=0.0, bas=0.0):
    """Retrecit la zone des axes pour loger une bande de texte en pied ou en tete.

    Sans cela, un fig.text() se superpose au titre ou a l'etiquette d'abscisse :
    constrained_layout ne connait que les axes, pas les textes libres de la
    figure. On lui donne donc un rectangle utile reduit, et les reservations
    successives s'additionnent (un kicker ET une mention => deux bandes).
    """
    rect = list(getattr(fig, '_bp_rect', [0.0, 0.0, 1.0, 1.0]))
    rect = [rect[0], rect[1] + bas, rect[2], rect[3] - haut - bas]
    fig._bp_rect = rect
    moteur = fig.get_layout_engine()
    if moteur is not None and hasattr(moteur, 'set'):
        try:
            moteur.set(rect=tuple(rect))
        except (TypeError, ValueError):       # moteur sans rect : on laisse tel quel
            pass
    return rect


_reserver_bande = reserver_bande          # alias interne, ancien nom


MENTION_SYNTHETIQUE = 'DONNÉES SYNTHÉTIQUES — aucune mesure de l\'enceinte'


def marque_synthetique(fig, texte=MENTION_SYNTHETIQUE, role='alerte', position='bas'):
    """Estampille la figure : ces courbes ne sont PAS des mesures.

    Principe 2 du § 09.1 et regle d'honnetete du sujet (§ 08) :
    une figure sortie du depot peut se retrouver sur une diapositive sans sa
    legende. La mention doit donc etre DANS l'image, pas a cote. A retirer
    figure par figure le jour ou les vraies mesures existent -- et ce jour-la,
    c'est une ligne a supprimer, pas une figure a refaire.

    position : 'bas' (defaut) ou 'haut', quand une legende commune occupe deja
    le pied de la figure -- la mention doit rester lisible, pas se superposer.
    """
    if position == 'haut':
        reserver_bande(fig, haut=0.052)
        return fig.text(0.998, 0.998, texte, ha='right', va='top',
                        fontsize=plt.rcParams['font.size'] * 0.72,
                        color=couleur(role), family='monospace', zorder=10)
    reserver_bande(fig, bas=0.052)
    return fig.text(0.998, 0.004, texte, ha='right', va='bottom',
                    fontsize=plt.rcParams['font.size'] * 0.72, color=couleur(role),
                    family='monospace', zorder=10)


LARGEUR_KICKER = 92        # caracteres ; au-dela, la figure s'elargit -- voir ci-dessous


def kicker(fig, texte, role='texte_doux', largeur=LARGEUR_KICKER):
    """Eyebrow en mono majuscule en haut a gauche (equivalent du .kicker CSS).

    LE TEXTE EST TRONQUE, ET CE N'EST PAS DE LA COQUETTERIE. Avec
    bbox_inches='tight', tout element qui depasse de la figure ELARGIT le
    fichier produit : un kicker de 150 caracteres a 6,5 pt sort une figure de
    1341 px de large au lieu de 905, qui ecrase les axes une fois remise a la
    largeur de la diapositive. 92 caracteres tiennent dans 5,6 pouces avec les
    metriques de DejaVu Sans Mono ; au-dela on coupe, visiblement.
    """
    texte = texte.upper()
    if len(texte) > largeur:
        texte = texte[:largeur - 1].rstrip() + '…'
    reserver_bande(fig, haut=0.058)
    return fig.text(0.002, 0.998, texte, ha='left', va='top',
                    fontsize=plt.rcParams['font.size'] * 0.72, color=couleur(role),
                    family='monospace', zorder=10)


def legende(ax, *args, **kw):
    """Legende Blueprint : cadre discret, fond de panneau, pas d'ombre."""
    kw.setdefault('frameon', True)
    kw.setdefault('fancybox', False)
    leg = ax.legend(*args, **kw)
    if leg is not None:
        leg.get_frame().set_linewidth(0.6)
    return leg


def db(x, plancher=1e-12):
    """20 log10|x|, avec plancher : evite -inf sur un zero exact de sommation."""
    import numpy as np
    return 20.0 * np.log10(np.maximum(np.abs(x), plancher))


# ---------------------------------------------------------------------------
# 6. Auto-verification
# ---------------------------------------------------------------------------

def verifier_polices(bavard=True):
    """Dit quelles polices de la pile matplotlib sait REELLEMENT ouvrir.

    Repond une fois pour toutes a "pourquoi mes figures ne sont pas en Inter ?" :
    les woff2 de libs/fonts/ ne sont pas lisibles par matplotlib ; la pile
    complete est neanmoins ecrite dans le SVG (svg.fonttype='none'), donc le
    navigateur, lui, utilise Inter.
    """
    disponibles = {f.name for f in font_manager.fontManager.ttflist}
    etat = [(nom, nom in disponibles) for nom in PILE_SANS + PILE_MONO
            if not nom.endswith('serif') and nom != 'monospace']
    dossier = os.path.join(_RACINE, 'libs', 'fonts')
    woff2 = sorted(f for f in os.listdir(dossier)) if os.path.isdir(dossier) else []
    if bavard:
        print('polices : metriques calculees avec la premiere disponible de la pile')
        for nom, ok in etat:
            print('   %-16s %s' % (nom, 'lisible par matplotlib' if ok else
                                   'ABSENTE (ecrite dans le SVG, rendue par le navigateur)'))
        print('   libs/fonts/ : %d fichier(s) woff2 vendore(s), non lisibles par matplotlib'
              % len([f for f in woff2 if f.endswith('.woff2')]))
    return dict(etat)


def demonstration(dossier=None, bavard=True):
    """Produit une figure temoin dans les deux variantes et controle le SVG.

    C'est le test (h) du § 09.6 en miniature : 0 couleur figee, et un
    fichier reproductible (deux enregistrements successifs donnent le meme
    contenu, sel de hachage fixe et date retiree).
    """
    import numpy as np
    # UN SEUL dossier de sortie dans tout le depot : analyse/resultats/figures, le seul
    # couvert par la regle .gitignore du § 09.8. Un seconde dossier analyse/figures/
    # aurait fini versionne par un `git add analyse`, avec des figures PERIMEES
    # indiscernables des figures a jour (correction de relecture du 2026-09-14).
    dossier = dossier or os.path.join(_ICI, 'resultats', 'figures')
    verdicts = []
    f = np.logspace(np.log10(20.), np.log10(500.), 200)
    for variante in ('sombre', 'clair'):
        with style(variante):
            fig, (h, b) = figure(2, 1, taille=TAILLE_DIAPO, hauteurs=(2, 1), sharex=True)
            h.plot(f, 8 + 40 / (1 + (10 * (f / 55 - 55 / f)) ** 2) ** .5,
                   color=couleur('grave'), label='voie grave')
            h.plot(f, 6 + 2e-3 * 2 * np.pi * f, color=couleur('medium'),
                   label='voie médium')
            h.set_yscale('log')
            h.set_ylabel('|Z| (Ω)')
            h.set_title('Figure témoin — style Blueprint')
            legende(h, loc='upper right')
            cartouche(h, 'témoin\nstyle %s' % variante, 'haut gauche')
            b.errorbar(f[::12], 20 * np.sin(f[::12] / 80), yerr=2.0, fmt='o',
                       color=couleur('mesure'), ecolor=couleur('filet'),
                       markersize=2.6, linewidth=0.9)
            b.set_ylabel('φ (°)')
            axe_frequence(b, 20, 500)
            repere_vertical(b, 100.0, '100 Hz')
            kicker(fig, 'blueprint_mpl — démonstration')
            marque_synthetique(fig)
            nom = 'fig-demo-blueprint' + ('-clair' if variante == 'clair' else '')
            r = enregistrer(fig, nom, dossier)
        ok = not r['hexa_figes']
        verdicts.append(dict(nom=nom, variante=variante, ok=ok,
                             octets=r['octets'], figes=r['hexa_figes'],
                             substitutions=r['substitutions']))
        if bavard:
            print('%-28s %-7s %6.1f ko svg  %6.1f ko png  %4d x %3d px  couleurs figees : %s'
                  % (nom, variante, r['octets']['svg'] / 1024.,
                     r['octets'].get('png', 0) / 1024.,
                     r['px'][0], r['px'][1],
                     'aucune' if ok else ', '.join(r['hexa_figes'])))
            print('    substitutions :', ' '.join(
                '%s=%d' % (k.lstrip('-'), v) for k, v in r['substitutions'].items() if v))
    return verdicts


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    print('blueprint_mpl -- identite visuelle Blueprint pour matplotlib')
    print('matplotlib', matplotlib.__version__, '| backend', matplotlib.get_backend())
    print()
    verifier_palettes()
    print()
    verifier_polices()
    print()
    demonstration()
