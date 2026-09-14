"""injecter_figures.py -- ALIAS DE COMPATIBILITE vers figures (§ 09.2 et § 09.7).

POURQUOI CE FICHIER EXISTE
--------------------------
Le § 09.2 gele un module `injecter_figures.py` distinct de `figures.py`. Les deux ont
ete fusionnes a l'ecriture, pour une raison de fond : l'injection a besoin de la
LISTE DES FIGURES (`figures.FIGURES`), puisqu'un nom de figure est aussi le nom de
son marqueur HTML `<!--FIG:nom-->`. Deux fichiers auraient signifie deux listes, donc
un jour deux listes divergentes -- et un `SystemExit` sur une diapositive au plus
mauvais moment.

Le NOM du module fait neanmoins partie du contrat gele du § 09, contrat contre lequel
d'autres agents ecrivent en parallele : un `import injecter_figures` echouait. Ce
fichier retablit le nom sans dupliquer une ligne de code (relecture du 2026-09-14).

    import injecter_figures
    injecter_figures.injecter_figures(chemin_html, dossier, noms)

QUEL NOM FAIT FOI ? `figures`. Le jour ou REFERENCE-TECHNIQUE.md § 09.2 sera amende,
ce fichier pourra disparaitre.

UTILISABLE EN LIGNE DE COMMANDE, comme le prototype du § 09.7 :

    python analyse/injecter_figures.py <fichier.html> [nom_de_figure ...]

Sans nom de figure, toutes celles du registre sont injectees. L'INJECTION ECHOUE
BRUYAMMENT si un marqueur manque : c'est le defaut precis de `_gen.py` a la racine du
depot, qui affichait "OK injecte" sans rien injecter.
"""

import os
import sys

_ICI = os.path.dirname(os.path.abspath(__file__))
if _ICI not in sys.path:
    sys.path.insert(0, _ICI)

import figures as _figures                                # noqa: E402
from figures import (DOSSIER_FIGURES, DOSSIER_RESULTATS,  # noqa: E402,F401
                     FIGURES, injecter_figures)

#: Le module reellement implemente. Utile pour l'introspection et les tests.
MODULE_IMPLEMENTE = _figures


def principal(arguments=None):
    """Injecte des figures dans un HTML. Rend 0 si tout passe.

    Aucune valeur par defaut sur le fichier HTML : injecter dans un fichier qu'on
    n'a pas nomme serait exactement le genre de surprise que le § 09.7 proscrit.
    """
    arguments = list(sys.argv[1:] if arguments is None else arguments)
    if not arguments or arguments[0] in ('-h', '--aide', '--help'):
        print(__doc__)
        return 0 if arguments else 1
    chemin_html = arguments[0]
    noms = arguments[1:] or list(FIGURES)
    injecter_figures(chemin_html, DOSSIER_RESULTATS, noms)
    return 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')              # console Windows en cp1252
    raise SystemExit(principal())
