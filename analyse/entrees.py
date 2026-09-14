"""entrees.py -- ALIAS DE COMPATIBILITE vers io_mesures (§ 09.2 et § 09.4).

POURQUOI CE FICHIER EXISTE
--------------------------
Le § 09.2 gele l'arborescence sous le nom `entrees.py`, et le § 09.4 gele les
signatures sous l'entete de module `entrees`. L'implementation vit dans
`io_mesures.py` : le nom a ete change a l'ecriture parce qu'il dit mieux ce que le
module fait -- il LIT et il ECRIT, il n'y a pas que des entrees -- et parce que
`entrees` est un mot assez commun pour entrer en collision un jour.

Le renommage etait documente dans LISEZMOI.md, et les signatures internes sont
respectees a la lettre. Mais le NOM DE MODULE fait partie du contrat gele du § 09,
contrat contre lequel d'autres agents ecrivent en parallele : un `import entrees`
echouait. Ce fichier retablit le nom du contrat sans dupliquer une seule ligne de
code (relecture du 2026-09-14).

CE FICHIER NE CONTIENT AUCUNE LOGIQUE, ET C'EST VOULU. Deux implementations d'un
meme lecteur de CSV divergent toujours ; un alias, jamais. Tout se lit, se corrige
et se teste dans `io_mesures.py`, y compris quand on est passe par ici.

    import entrees                 # nom du contrat, § 09.2
    import io_mesures              # nom du fichier, strictement equivalent
    entrees.lire_mesure is io_mesures.lire_mesure     # True

QUEL NOM FAIT FOI ? `io_mesures`. C'est lui qu'on ouvre, qu'on lit et qu'on
modifie ; `entrees` n'est qu'une porte d'entree pour le code ecrit contre la
specification. Le jour ou REFERENCE-TECHNIQUE.md § 09.2 sera amende pour ecrire
`io_mesures.py`, ce fichier pourra disparaitre -- et ce sera une ligne a supprimer,
pas un module a reecrire.
"""

import os
import sys

_ICI = os.path.dirname(os.path.abspath(__file__))
if _ICI not in sys.path:
    sys.path.insert(0, _ICI)

import io_mesures as _io_mesures                         # noqa: E402
from io_mesures import *                                 # noqa: E402,F401,F403

# `from ... import *` ignore les noms commencant par '_' et, si __all__ existe, tout
# ce qui n'y figure pas. On recopie donc explicitement l'espace de noms public, pour
# que `entrees.CHEMIN_EXEMPLE` et `entrees.VERSION_FORMAT` existent comme dans
# io_mesures -- un alias partiel serait pire que pas d'alias du tout.
for _nom in dir(_io_mesures):
    if not _nom.startswith('_'):
        globals().setdefault(_nom, getattr(_io_mesures, _nom))
del _nom

#: Le module reellement implemente. Utile pour l'introspection et les tests.
MODULE_IMPLEMENTE = _io_mesures


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')             # console Windows en cp1252
    print(__doc__)
    print('lire_mesure        : %s' % lire_mesure)       # noqa: F405
    print('module implemente  : %s' % MODULE_IMPLEMENTE.__file__)
