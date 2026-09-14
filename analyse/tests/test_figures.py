"""(h) FIGURES -- huitieme et derniere famille de tests du § 09.6.

CE QUE CETTE FAMILLE PROTEGE, ET POURQUOI ELLE N'EST PAS DECORATIVE
-------------------------------------------------------------------
Le livrable SCEI est un PDF 4/3 de 1024 x 768 px, exporte depuis les diapositives
avec la variante CLAIRE de l'identite Blueprint (css/blueprint-light.css). Cette
recoloration ne fonctionne que si les couleurs des SVG sont des VARIABLES CSS. Une
seule couleur figee dans un fichier -- un `#0e2230` oublie par la substitution -- et
la courbe concernee reste peinte en bleu nuit sur fond blanc le jour du depot, donc
illisible, et personne ne s'en apercoit avant d'ouvrir le PDF final.

Deux pieges, tous deux verifies ici :

1. LES VARIABLES CSS SONT PROPRES A UN DOCUMENT. Un SVG appele par `<img src=...>`
   est un document independant ou `--accent` n'est defini nulle part : la
   declaration devient invalide *at computed-value time* et la courbe DISPARAIT
   (fill noir, stroke none). D'ou le repli obligatoire `var(--accent, #5fd0e0)`, qui
   rend le fichier autonome ET recolorable une fois inline. Le test verifie donc
   deux choses opposees : zero hexadecimal HORS repli, et des replis PRESENTS.

2. L'INJECTION DOIT ECHOUER BRUYAMMENT. C'est le defaut precis de `_gen.py` a la
   racine du depot : il cherchait ses figures par une expression reguliere sur un
   `aria-label`, n'en trouvait aucune, reecrivait le fichier a l'identique et
   affichait quand meme "OK injecte". Un faux positif silencieux est pire qu'une
   panne. Le test verifie donc aussi le cas d'ECHEC, pas seulement le cas nominal.

POURQUOI CE FICHIER N'EXISTAIT PAS, ET CE QUE CELA CHANGE
---------------------------------------------------------
Jusqu'a la relecture du 2026-09-14, le controle (h) n'etait execute qu'a l'etape 8
de `tout_refaire.py`. Il etait donc SAUTE par `--sans-figures` et n'etait JAMAIS joue
par la commande gelee `python -m unittest discover -s analyse/tests`. Ce n'etait pas
un test de non-regression : c'etait un controle d'execution. Il l'est maintenant.

Les seuils chiffres sont LUS dans `criteres_geles.json`, section
`tests_non_regression.h_figures` -- comme pour les sept autres familles.

Lancement (§ 09.6), depuis la racine du depot :
    python -m unittest discover -s analyse/tests -v
    python analyse/tests/test_figures.py
"""

import contextlib
import io as _io
import os
import sys
import unittest

# --- amorce de chemin (voir contexte.py) ------------------------------------
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import contexte  # noqa: E402

import matplotlib  # noqa: E402
matplotlib.use('Agg')                      # aucune fenetre : on ne trace que sur disque

import blueprint_mpl as BP  # noqa: E402
import figures as FIG  # noqa: E402


def _sans_accents(texte):
    """Retire les accents, pour comparer un titre affiche a un mot ecrit en ASCII.

    Les titres de figures portent leurs accents (ils sont rendus par matplotlib, pas
    imprimes dans une console), tandis que ce fichier de test reste sans lettres
    accentuees : il faut donc les rapprocher pour pouvoir les comparer.
    """
    import unicodedata
    decompose = unicodedata.normalize('NFD', texte)
    return ''.join(c for c in decompose if unicodedata.category(c) != 'Mn')


def _figure_minimale():
    """Une figure temoin, la plus petite qui exerce tous les rcParams a risque.

    Il faut du TEXTE (axes, etiquettes, graduations, legende, cartouche) autant que
    des COURBES : par defaut matplotlib ecrit `#000000` pour le texte, les bords
    d'axes et les graduations, et cette couleur-la echappe a la substitution si
    `style_blueprint()` ne la fixe pas. Une figure qui ne contiendrait que des
    courbes passerait le test sans rien prouver.
    """
    import numpy as np
    f = np.logspace(1, 3, 60)
    fig, ax = BP.figure(1, 1, taille=(3.2, 2.0))
    ax.plot(f, 8 + 30 / (1 + (6 * (f / 50 - 50 / f)) ** 2) ** 0.5,
            label='temoin |Z|')
    BP.axe_frequence(ax, 10.0, 1000.0)
    BP.axe_impedance(ax)
    BP.legende(ax, loc='upper right')
    BP.cartouche(ax, 'cartouche temoin', 'bas gauche')
    BP.kicker(fig, 'test (h) — figure temoin')
    BP.marque_synthetique(fig)
    return fig


class TestSubstitutionDesCouleurs(unittest.TestCase):
    """(h1) Aucune couleur #rrggbb residuelle hors repli var(--x, #hex)."""

    def test_h1_svg_sans_couleur_figee_dans_les_deux_variantes(self):
        """Zero hexadecimal non substitue, en variante sombre ET en variante claire.

        Les deux variantes doivent etre testees separement : ce sont deux palettes
        differentes, donc deux listes de sentinelles a substituer, et une couleur
        peut tres bien etre couverte dans l'une et oubliee dans l'autre.
        """
        maximum = contexte.critere('h_figures', 'hexadecimaux_residuels_max')
        with contexte.dossier_jetable() as dossier:
            for variante in ('sombre', 'clair'):
                with self.subTest(variante=variante):
                    with BP.style(variante):
                        fig = _figure_minimale()
                        chemin = os.path.join(dossier, 'temoin-%s.svg' % variante)
                        compte, figes = BP.enregistrer_svg(fig, chemin,
                                                           variante=variante)
                    self.assertLessEqual(
                        len(figes), maximum,
                        'couleur(s) FIGEE(S) dans %s : %s -- elles resteront fausses '
                        'dans la variante claire a l export PDF'
                        % (os.path.basename(chemin), ', '.join(figes)))
                    self.assertGreater(
                        sum(compte.values()), 0,
                        'aucune substitution : la palette ne correspond plus au SVG')

    def test_h2_les_replis_sont_presents_et_le_fichier_reste_autonome(self):
        """Chaque var() doit porter son repli : var(--accent, #5fd0e0), jamais var(--accent).

        Sans repli, un SVG ouvert hors du document HTML (en `<img>`, dans un lecteur
        SVG, dans une previsualisation) perd toutes ses couleurs : la propriete
        personnalisee n'est definie nulle part, la declaration devient invalide et la
        courbe disparait. Le repli est donc ce qui rend le fichier AUTONOME ; le test
        verifie qu'il n'a pas ete perdu en route.
        """
        import re
        with contexte.dossier_jetable() as dossier:
            with BP.style('sombre'):
                fig = _figure_minimale()
                chemin = os.path.join(dossier, 'temoin-replis.svg')
                BP.enregistrer_svg(fig, chemin, variante='sombre')
            with open(chemin, encoding='utf-8') as fh:
                svg = fh.read()
        avec_repli = re.findall(r'var\(--[a-z0-9-]+,\s*#[0-9a-fA-F]{6}\)', svg)
        sans_repli = re.findall(r'var\(--[a-z0-9-]+\s*\)', svg)
        self.assertGreater(len(avec_repli), 0, 'aucun var(--x, #hex) : le SVG ne serait '
                                               'plus recolorable par blueprint-light.css')
        self.assertEqual(sans_repli, [], 'var() SANS repli : le fichier devient noir '
                                         'des qu il sort du document HTML')

    def test_h3_verifier_svg_relit_un_fichier_sans_la_figure(self):
        """`verifier_svg` doit rendre le meme verdict que `enregistrer_svg`.

        C'est ce qui permet de controler une figure deja sur disque -- par exemple
        celles de resultats/figures/ -- sans avoir l'objet matplotlib qui l'a
        produite. Si les deux divergeaient, le controle de tout_refaire.py ne
        prouverait rien.
        """
        with contexte.dossier_jetable() as dossier:
            with BP.style('sombre'):
                fig = _figure_minimale()
                chemin = os.path.join(dossier, 'temoin-relecture.svg')
                _compte, figes = BP.enregistrer_svg(fig, chemin, variante='sombre')
            self.assertEqual(BP.verifier_svg(chemin), figes)

    def test_h4_le_test_attrape_vraiment_une_couleur_figee(self):
        """GARDE-FOU DU GARDE-FOU : une couleur volontairement figee DOIT etre vue.

        Sans ce test, rien ne prouve que (h1) puisse echouer un jour : un detecteur
        qui ne detecte rien passe tous les controles. On injecte donc a la main une
        couleur qui n'appartient a aucune palette et on exige qu'elle ressorte.
        """
        with contexte.dossier_jetable() as dossier:
            with BP.style('sombre'):
                fig = _figure_minimale()
                fig.axes[0].plot([10, 1000], [10, 10], color='#ff00ff')  # jamais palette
                chemin = os.path.join(dossier, 'temoin-fige.svg')
                _compte, figes = BP.enregistrer_svg(fig, chemin, variante='sombre')
        self.assertIn('#ff00ff', [c.lower() for c in figes],
                      'une couleur hors palette n a PAS ete detectee : le critere (h) '
                      'ne protege rien')


class TestInjectionHTML(unittest.TestCase):
    """(h5-h7) Injection des SVG aux marqueurs <!--FIG:nom--> (§ 09.7)."""

    NOM = 'fig-temoin-injection'

    def _preparer(self, dossier):
        """Ecrit un SVG temoin et rend son nom."""
        with BP.style('sombre'):
            fig = _figure_minimale()
            BP.enregistrer_svg(fig, os.path.join(dossier, self.NOM + '.svg'),
                               variante='sombre')
        return self.NOM

    def test_h5_injection_nominale_marqueur_conserve(self):
        """Apres injection : le SVG est en place ET le marqueur est CONSERVE.

        CE QUE CE TEST PROTEGE. L'injection doit pouvoir etre rejouee : le protocole
        prevoit de remesurer (deux niveaux d ecoute geles, bobine chaude, reprise
        apres correction du montage), donc de regenerer les figures et de les
        reinjecter. Une injection qui consomme son marqueur ne marche qu une fois
        et condamne a rouvrir le HTML a la main. On verifie donc que le couple
        <!--FIG:nom--> ... <!--/FIG:nom--> encadre bien la figure apres coup.
        """
        with contexte.dossier_jetable() as dossier:
            nom = self._preparer(dossier)
            chemin_html = os.path.join(dossier, 'page.html')
            with open(chemin_html, 'w', encoding='utf-8', newline='\n') as fh:
                fh.write('<html><body>\n<figure><!--FIG:%s--></figure>\n'
                         '</body></html>\n' % nom)
            # injecter_figures ecrit son compte rendu sur stdout (c'est voulu : le
            # message de succes ne s'imprime qu'apres un remplacement EFFECTIF). On
            # l'etouffe ici pour que la suite de tests reste lisible.
            with contextlib.redirect_stdout(_io.StringIO()):
                n = FIG.injecter_figures(chemin_html, dossier, [nom])
            with open(chemin_html, encoding='utf-8') as fh:
                html = fh.read()
        self.assertEqual(n, 1)
        self.assertEqual(html.count('<svg'), 1)
        self.assertEqual(html.count('<!--FIG:%s-->' % nom), 1,
                         "le marqueur ouvrant doit survivre a l injection")
        self.assertEqual(html.count('<!--/FIG:%s-->' % nom), 1,
                         'la figure doit etre refermee par son marqueur')
        self.assertLess(html.index('<svg'), html.index('<!--/FIG:'),
                        'le SVG doit se trouver ENTRE les deux marqueurs')

    def test_h5bis_injection_idempotente(self):
        """Injecter deux fois de suite ne duplique rien : c est le cas d usage reel.

        CE QUE CE TEST PROTEGE. Apres chaque campagne de mesures, on relance
        figures.py puis l injection. Si la seconde passe ajoutait un SVG au lieu de
        remplacer le premier, la diapositive porterait deux courbes -- l ancienne et
        la nouvelle -- et c est l ancienne, fausse, qui serait projetee en premier.
        """
        with contexte.dossier_jetable() as dossier:
            nom = self._preparer(dossier)
            chemin_html = os.path.join(dossier, 'page.html')
            with open(chemin_html, 'w', encoding='utf-8', newline='\n') as fh:
                fh.write('<html><body>\n<figure><!--FIG:%s-->'
                         '<p class="placeholder">a mesurer</p>'
                         '<!--/FIG:%s--></figure>\n'
                         '</body></html>\n' % (nom, nom))
            with contextlib.redirect_stdout(_io.StringIO()):
                FIG.injecter_figures(chemin_html, dossier, [nom])
                FIG.injecter_figures(chemin_html, dossier, [nom])
                FIG.injecter_figures(chemin_html, dossier, [nom])
            with open(chemin_html, encoding='utf-8') as fh:
                html = fh.read()
        self.assertEqual(html.count('<svg'), 1, 'trois injections, un seul SVG')
        self.assertEqual(html.count('<!--FIG:%s-->' % nom), 1)
        self.assertEqual(html.count('<!--/FIG:%s-->' % nom), 1)
        self.assertNotIn('placeholder', html,
                         "le bloc d attente doit avoir ete remplace")

    def test_h5ter_premiere_injection_marqueur_seul(self):
        """Marqueur seul : le SVG est insere derriere lui et le fermant est ajoute.

        CE QUE CE TEST PROTEGE. C est la forme employee par les diapositives, ou le
        bloc d attente est un element VOISIN de la figure et non un bloc encadre.
        Apres cette premiere passe, le fichier est dans la forme encadree, donc
        reinjectable -- ce que verifie test_h5bis.
        """
        with contexte.dossier_jetable() as dossier:
            nom = self._preparer(dossier)
            chemin_html = os.path.join(dossier, 'nu.html')
            with open(chemin_html, 'w', encoding='utf-8', newline='\n') as fh:
                fh.write('<html><body><figure><!--FIG:%s--></figure>'
                         '</body></html>\n' % nom)
            with contextlib.redirect_stdout(_io.StringIO()):
                FIG.injecter_figures(chemin_html, dossier, [nom])
            with open(chemin_html, encoding='utf-8') as fh:
                html = fh.read()
        self.assertEqual(html.count('<svg'), 1)
        self.assertEqual(html.count('<!--FIG:%s-->' % nom), 1)
        self.assertEqual(html.count('<!--/FIG:%s-->' % nom), 1,
                         'le marqueur fermant doit avoir ete ajoute')

    def test_h6_marqueur_absent_echec_bruyant(self):
        """Marqueur absent -> SystemExit. JAMAIS un "OK injecte" sans rien injecter.

        C'est le defaut diagnostique de _gen.py, transforme en test : le faux positif
        silencieux est la panne la plus couteuse, parce qu'elle ne se voit qu'a
        l'ouverture du PDF final.
        """
        with contexte.dossier_jetable() as dossier:
            nom = self._preparer(dossier)
            chemin_html = os.path.join(dossier, 'sans_marqueur.html')
            with open(chemin_html, 'w', encoding='utf-8', newline='\n') as fh:
                fh.write('<html><body><p>aucun marqueur ici</p></body></html>\n')
            with self.assertRaises(SystemExit):
                FIG.injecter_figures(chemin_html, dossier, [nom])
            with open(chemin_html, encoding='utf-8') as fh:
                self.assertNotIn('<svg', fh.read())   # le fichier n'a pas ete touche

    def test_h7_svg_absent_echec_bruyant(self):
        """Figure demandee mais SVG introuvable -> SystemExit, pas un HTML tronque."""
        with contexte.dossier_jetable() as dossier:
            chemin_html = os.path.join(dossier, 'page.html')
            with open(chemin_html, 'w', encoding='utf-8', newline='\n') as fh:
                fh.write('<html><body><!--FIG:fig-inexistante--></body></html>\n')
            with self.assertRaises(SystemExit):
                FIG.injecter_figures(chemin_html, dossier, ['fig-inexistante'])


class TestRegistreDesFigures(unittest.TestCase):
    """(h8) Le registre des figures doit couvrir la liste gelee du § 09.7."""

    def test_h8_les_figures_annoncees_existent_toutes(self):
        """Chaque nom du registre doit pointer une fonction appelable.

        Un nom de figure est aussi un marqueur HTML : `<!--FIG:fig-z-sub-mesure-->`.
        Une entree morte dans le registre se traduirait, le jour de l'injection, par
        un SystemExit sur une diapositive -- au plus mauvais moment.
        """
        self.assertGreater(len(FIG.FIGURES), 0)
        for nom, (fonction, description) in FIG.FIGURES.items():
            with self.subTest(figure=nom):
                self.assertTrue(nom.startswith('fig-'), 'nom hors convention : %s' % nom)
                self.assertTrue(callable(fonction))
                self.assertTrue(description.strip())

    def test_h8_le_satellite_energie_est_au_registre(self):
        """`fig-croisement-energie` est gelee au tableau du § 09.7 : elle doit exister.

        Elle a manque longtemps, en meme temps que le module `energie.py` : le
        satellite "croisement energetique" est pourtant le seul des trois qui porte
        l'argument SOBRIETE du theme national.
        """
        self.assertIn('fig-croisement-energie', FIG.FIGURES)

    def test_h8_un_seul_dossier_de_sortie(self):
        """DOSSIER_FIGURES et DOSSIER_RESULTATS doivent designer le MEME dossier.

        Deux dossiers de sortie pour les memes figures, dont un seul couvert par la
        regle .gitignore du § 09.8, c'est la garantie qu'une figure PERIMEE finira
        versionnee et indiscernable d'une figure a jour -- puis citee a l'oral.
        """
        self.assertEqual(os.path.normcase(os.path.abspath(FIG.DOSSIER_FIGURES)),
                         os.path.normcase(os.path.abspath(FIG.DOSSIER_RESULTATS)))


class TestStatutDesDonneesSurLaFigure(unittest.TestCase):
    """(h9) Le TITRE d'une figure ne doit jamais dire "mesuree" sur du calcul."""

    def test_h9_un_statut_synthetique_n_est_jamais_une_mesure(self):
        """`_statut_est_une_mesure` doit repondre False sur tout statut synthetique.

        Le defaut est PRUDENT par construction : en cas de doute on repond False,
        donc la figure se declare synthetique. Se tromper dans ce sens fait perdre un
        peu de force a une vraie mesure ; se tromper dans l'autre fait passer un
        calcul pour un releve de banc, ce que le § 08 interdit.
        """
        for statut in ('SYNTHETIQUES', 'SYNTHETIQUE (demo, pas une mesure)',
                       'SYNTHETIQUES -- simulation en memoire',
                       'modele numerique, AUCUNE MESURE', '', None):
            with self.subTest(statut=statut):
                self.assertFalse(FIG._statut_est_une_mesure(statut))

    def test_h9_le_kicker_de_la_figure_1_suit_le_statut(self):
        """Tant que mesures/ est synthetique, le titre ne doit pas dire "mesurée".

        Le titre est ce qu'on lit en premier, et une figure sortie du depot se
        retrouve un jour sur une diapositive sans sa legende : l'estampille de pied de
        page ne suffit pas si le titre dit le contraire.
        """
        z = FIG.donnees_z()
        self.assertFalse(FIG._statut_est_une_mesure(z['statut']),
                         'les donnees de demonstration ne sont plus etiquetees '
                         'synthetiques : verifier mesures/')
        with BP.style('sombre'):
            fig = FIG.fig_z_sub_mesure(taille=(3.2, 2.4))
        try:
            textes = [t.get_text() for t in fig.texts]
        finally:
            import matplotlib.pyplot as plt
            plt.close(fig)
        titres = [t for t in textes if 'ACTE 1' in t.upper()]
        self.assertTrue(titres, 'kicker introuvable sur la figure de l acte 1')
        titre = titres[0].upper()
        # Deux exigences opposees, et il faut les DEUX. Ne pas se contenter de
        # chercher le mot "MESURE" : "PAS UNE MESURE" le contient aussi, et un test
        # qui echouerait sur la bonne formulation serait pire que pas de test.
        self.assertNotIn('MESUREE', _sans_accents(titre),
                         'le titre qualifie les donnees de MESUREES alors qu elles '
                         'sont calculees : c est exactement la phrase qu un TIPE ne '
                         'doit pas produire')
        self.assertIn('SYNTH', titre,
                      'le titre ne dit pas que les donnees sont synthetiques ; '
                      'l estampille de pied de page ne suffit pas, une figure se '
                      'retrouve un jour sur une diapositive sans sa legende')


if __name__ == '__main__':
    unittest.main(verbosity=2)
