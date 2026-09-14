"""Amorce de chemin et fixtures partagees par la suite de tests (voir § 09.6).

CE FICHIER N'EST PAS UN TEST. Le motif de decouverte d'unittest est ``test*.py`` :
``contexte`` n'est donc jamais collecte, il est seulement importe par les modules de
test. Il n'y a volontairement AUCUN ``__init__.py`` dans ``analyse/tests/`` -- la
specification § 09.6 impose le lancement :

    python -m unittest discover -s analyse/tests -v

depuis la racine du depot, SANS ``-t .``. Dans ce mode unittest place le dossier de
depart (``analyse/tests``) en tete de ``sys.path`` ; il faut y ajouter ``analyse/``
pour que ``import optim`` fonctionne. Chaque fichier de test refait lui-meme cette
amorce en deux lignes, de sorte qu'il reste executable seul :

    python analyse/tests/test_filtre.py

Ce que ce module apporte en plus du chemin : les jeux de donnees SYNTHETIQUES
partages, un dossier jetable (les tests n'ecrivent JAMAIS dans ``analyse/mesures/``
ni dans le depot) et deux ou trois aides de comparaison.

AUCUNE MESURE DE L'ENCEINTE DU PROJET N'EXISTE a ce jour : tout chiffre manipule
ici est soit calcule, soit un ordre de grandeur etiquete.
"""

import os
import shutil
import sys
import tempfile
import warnings
from contextlib import contextmanager

# --- amorce de chemin ------------------------------------------------------
DOSSIER_TESTS = os.path.dirname(os.path.abspath(__file__))
DOSSIER_ANALYSE = os.path.dirname(DOSSIER_TESTS)
RACINE_DEPOT = os.path.dirname(DOSSIER_ANALYSE)
for _d in (DOSSIER_TESTS, DOSSIER_ANALYSE):
    if _d not in sys.path:
        sys.path.insert(0, _d)

import numpy as np  # noqa: E402  (apres l'amorce de chemin, volontairement)


# --- criteres chiffres GELES, lus dans criteres_geles.json ------------------
# Principe 4 du § 09.1 : "les decisions gelees sont un fichier, pas une intention".
# Le § 09.6 impose que les huit criteres chiffres soient RECOPIES dans
# criteres_geles.json. Avant la relecture du 2026-09-14 ils ne vivaient que dans les
# docstrings des tests : rien n'empechait de les retoucher apres avoir vu un resultat,
# et une relecture ne pouvait confronter un test qu'a LUI-MEME -- critere circulaire.
# Les assertions tirent desormais leurs seuils d'ICI.

_CRITERES = {}


def criteres_tests():
    """Section `tests_non_regression` de criteres_geles.json -> dict (mise en cache).

    Leve explicitement si la section manque : un test qui se rabattrait en silence
    sur une valeur par defaut ne prouverait plus rien.
    """
    if not _CRITERES:
        import io_mesures as IO
        c = IO.lire_criteres_geles(exiger_geles=False)
        if 'tests_non_regression' not in c:
            raise AssertionError(
                'criteres_geles.json ne porte pas la section tests_non_regression : '
                'les criteres chiffres du § 09.6 ne sont plus geles nulle part.')
        _CRITERES.update(c['tests_non_regression'])
    return _CRITERES


def critere(famille, cle):
    """Un seuil gele, par famille ('c_incertitudes') et par cle ('u_f0_gum_pct').

    Toute cle absente leve : on ne devine pas un critere, on le lit ou on echoue.
    """
    c = criteres_tests()
    if famille not in c:
        raise AssertionError("criteres_geles.json : famille de tests '%s' absente"
                             % famille)
    if cle not in c[famille]:
        raise AssertionError("criteres_geles.json : %s.%s absent" % (famille, cle))
    return c[famille][cle]


# --- jeux de parametres SYNTHETIQUES ---------------------------------------
# Etiquetage obligatoire (principe 2 du § 09.1) : ce ne sont pas des mesures.
THETA_SYNTHETIQUE = (6.5, 1.2e-3, 44.0, 40.0, 1.75)
"""theta = (Re, Le, Res, fs, Qms) du sub SYNTHETIQUE du § 04.6 -- pic large
(Qms = 1,75). ORDRE DE GRANDEUR ILLUSTRATIF, PAS UNE MESURE."""

THETA_PIC_ETROIT = (6.5, 1.2e-3, 44.0, 40.0, 8.0)
"""Meme jeu avec Qms = 8 : c'est le VRAI cas d'un 18 pouces de sono (Qms de 3 a 10),
donc un pic etroit, donc peu de points dans la largeur du pic. La § 09.6 insiste :
c'est ce cas-la qui met la grille de frequences en difficulte, pas Qms = 1,75."""

THETA_BASSREFLEX = (5.0, 1.9e-3, 105.17241379310346, 39.0, 6.1, 35.0, 7.0)
"""theta = (Re, Le, Res, fs, Qms, fb, Ql) d'une caisse BASS-REFLEX illustrative
(§ 01.10), alpha de structure laisse a sa valeur par defaut. Sert uniquement a
fabriquer des donnees a DEUX pics pour eprouver le garde-fou."""

R_NOM = 8.0
"""Charge resistive pure de reference. Sur 8 ohm le probleme continu EST celui du
catalogue : c'est la porte de validation (b1) du § 09.6."""

DESIGN_CATALOGUE = dict(L1=18e-3, C1=150e-6, C2=150e-6, L2=18e-3)
"""Filtre Butterworth 2e ordre 100 Hz / 8 ohm normalise E12, legue par la v1.
C'est le point de depart a battre, pas un resultat."""


# --- aides ------------------------------------------------------------------
def charge_resistive(f, R=R_NOM):
    """Charge 8 ohm resistive pure, en tableau complexe de la meme taille que f.

    Physiquement c'est le haut-parleur IDEAL que le catalogue suppose ; tout
    l'interet du TIPE est justement que le vrai HP n'est pas cela (Z varie du
    simple au sextuple). Cette charge sert donc de banc d'essai du CODE, pas de
    modele du HP.
    """
    f = np.asarray(f, float)
    return np.full(f.shape, complex(R, 0.0))


def ecart_relatif_max(a, b):
    """Plus grand ecart RELATIF entre deux tableaux, terme a terme.

    On compare en relatif parce que les grandeurs du projet s'etalent sur des
    decades (1e-5 F et 1e-2 H dans le meme design) : un ecart absolu n'y veut
    rien dire.
    """
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    return float(np.max(np.abs(a / b - 1.0)))


def metadonnees_completes(**remplacements):
    """Jeu des 14 metadonnees obligatoires (§ 09.3), rempli de valeurs plausibles.

    Le fichier de mesure ne se reduit pas a deux colonnes : sans la date, le
    montage, la R_ref MESUREE et le niveau, une courbe d'impedance n'est pas une
    mesure, c'est un dessin. Le format les exige, ce jeu les fournit pour les tests.
    """
    import io_mesures as IO

    meta = {
        'version_format': str(IO.VERSION_FORMAT),
        'date': '2026-09-13T14:32',
        'dipole': 'SYNTHETIQUE (test de non-regression, PAS une mesure)',
        'montage': 'A (dipole a la masse) -- GBF + oscilloscope 2 voies',
        'R_ref_nominale_ohm': '100',
        'R_ref_mesuree_ohm': '99.7',
        'u_R_ref_relative_pct': '0.5',
        'u_systematique_relative_pct': '1.2',
        'niveau_Vd_RMS_V': '0.150',
        'temperature_C': '20.0',
        'operateur': 'suite de tests',
        'appareil': 'AUCUN -- donnees engendrees numeriquement',
        'Re_DC_avant_ohm': '6.50',
        'Re_DC_apres_ohm': '6.50',
    }
    meta.update({k: str(v) for k, v in remplacements.items()})
    return meta


def mesure_synthetique(theta=THETA_SYNTHETIQUE, R_ref=99.7, bruit_relatif=1e-3,
                       graine=1, n_par_octave=12):
    """Fabrique un couple (tableau structure, metadonnees) de mesure SYNTHETIQUE.

    On simule le montage du § 02 : le dipole et R_ref en serie sous le GBF, on
    releve les deux amplitudes et le decalage temporel, puis |Z| = R_ref*Vd/Vr et
    phi = 360*f*dt. Les colonnes brutes sont donc les LECTURES et les colonnes
    derivees s'en deduisent -- c'est tout l'interet du format (principe 1).
    """
    import io_mesures as IO
    import modele_hp as MH

    rng = np.random.default_rng(graine)
    f = MH.grille_log(10.0, 500.0, n_par_octave)
    Z = MH.Z_ts(f, *theta)
    module = np.abs(Z)
    bruit = 1.0 + bruit_relatif * rng.standard_normal(f.size)
    V_r = R_ref / np.abs(Z + R_ref)
    V_d = module / np.abs(Z + R_ref) * bruit
    dt = np.angle(Z) / (2.0 * np.pi * f)
    d = IO.tableau_mesure(
        f_Hz=f, V_dipole_V=V_d, V_Rref_V=V_r, dt_s=dt,
        module_Z_ohm=R_ref * V_d / V_r,
        phase_deg=360.0 * f * dt,
        u_module_alea_ohm=0.02 * module,
        u_phase_deg=np.full(f.size, 1.0),
    )
    return d, metadonnees_completes(R_ref_mesuree_ohm=R_ref, montage='C')


@contextmanager
def dossier_jetable():
    """Dossier temporaire supprime a la sortie.

    Regle du projet : ce qui est dans ``analyse/mesures/`` a coute une seance de
    banc. Un test n'y ecrit jamais -- il ne doit meme pas pouvoir y ecrire par
    accident.
    """
    chemin = tempfile.mkdtemp(prefix='tipe_tests_')
    try:
        yield chemin
    finally:
        shutil.rmtree(chemin, ignore_errors=True)


@contextmanager
def sans_avertissement():
    """Etouffe les UserWarning pendant un bloc.

    A n'utiliser que lorsque l'avertissement est ATTENDU et deja teste ailleurs
    (typiquement le garde-fou de caisse). Ne jamais s'en servir pour faire taire
    un avertissement qu'on n'a pas compris.
    """
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', UserWarning)
        yield
