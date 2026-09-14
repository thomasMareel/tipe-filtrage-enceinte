"""Mission n. 6 / test (d) du § 09.6 -- exhaustivite de l'enumeration E12.

CE QUE CE FICHIER PROTEGE
-------------------------
L'argument central de l'acte 3 est : "la recherche est EXHAUSTIVE sur la grille,
donc le minimum trouve est le minimum GLOBAL sur cette grille -- sans hypothese de
regularite de J, et sans sensibilite a l'initialisation, contrairement a un
optimiseur continu qui peut converger vers un minimum local."

Cet argument ne vaut que si trois choses sont vraies, et aucune ne se voit a
l'oeil sur une sortie de programme :

1. **Le compte y est.** 24 selfs x 24 condensateurs = 576 couples par voie, donc
   576^2 = 331 776 = 24^4 combinaisons. Un decalage d'indice quelque part et
   l'exploration saute des valeurs -- en silence, puisque le programme rend
   quand meme un gagnant.
2. **La version vectorisee calcule bien ce que calculerait une boucle.** Le code
   evalue J par produit exterieur en blocs (pour tenir en 28 Mo au lieu de
   340 Mo) ; c'est du remodelage de tableaux, l'endroit exact ou une erreur de
   transposition passe inapercue. On compare donc, sur un sous-espace reduit, la
   sortie vectorisee a une boucle explicite ecrite naivement.
3. **L'optimum n'est pas au bord.** Deux decades suffisent PARCE QUE les valeurs
   catalogue (18 mH, 141 uF) sont au centre de la grille. C'est une hypothese,
   pas un theoreme : si l'optimum se collait a 1 mH ou a 820 uF, il faudrait
   elargir la grille, et le "minimum global" annonce serait un artefact de borne.

Un quatrieme point, mineur mais souvent mal dit : la serie E12 n'est PAS
exactement geometrique. Le pas va de 1,182 a 1,250 pour un ideal 10^(1/12) =
1,2115. C'est une propriete de la norme IEC 60063, pas un bug -- le test la borne
pour qu'on puisse l'affirmer sans se tromper devant le jury.
"""

import os
import sys
import time
import unittest

_ICI = os.path.dirname(os.path.abspath(__file__))
for _d in (_ICI, os.path.dirname(_ICI)):
    if _d not in sys.path:
        sys.path.insert(0, _d)

import numpy as np  # noqa: E402
import contexte  # noqa: E402
import filtre as F  # noqa: E402
import modele_hp as MH  # noqa: E402
import optim as O  # noqa: E402


class TestGrilleE12(unittest.TestCase):
    """(d) La grille elle-meme : valeurs, pas, bornes, absence de doublon."""

    def test_la_serie_e12_a_bien_douze_valeurs_par_decade(self):
        """E12 = 1,0 1,2 1,5 1,8 2,2 2,7 3,3 3,9 4,7 5,6 6,8 8,2 -- douze, pas onze.

        Le nom de la serie dit son cardinal. Une valeur oubliee decalerait tout
        le compte de combinaisons et invaliderait l'argument d'exhaustivite.
        """
        self.assertEqual(len(O.E12), 12)
        np.testing.assert_allclose(
            O.E12, [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2])
        self.assertEqual(len(O.E6), 6)
        self.assertEqual(len(O.E24), 24)

    def test_les_deux_decades_de_selfs_et_de_condensateurs(self):
        """L_VALS : 1,0 a 82 mH (24 valeurs). C_VALS : 10 a 820 uF (24 valeurs).

        Ces bornes sont un choix documente au § 04.5 : les valeurs catalogue
        (18 mH, 141 uF) sont au CENTRE, a plus d'une decade de chaque borne. Le
        test fige le choix ; le test d'optimum interieur, plus bas, verifie qu'il
        reste justifie.
        """
        self.assertEqual(len(O.L_VALS), 24)
        self.assertEqual(len(O.C_VALS), 24)
        self.assertAlmostEqual(O.L_VALS[0], 1e-3, delta=1e-12)
        self.assertAlmostEqual(O.L_VALS[-1],
                               contexte.critere('d_series_e12', 'L_max_H'), delta=1e-12)
        self.assertAlmostEqual(O.C_VALS[0], 10e-6, delta=1e-15)
        self.assertAlmostEqual(O.C_VALS[-1],
                               contexte.critere('d_series_e12', 'C_max_F'), delta=1e-15)

    def test_grille_strictement_croissante_et_sans_doublon(self):
        """Aucune valeur repetee, ordre strict : sinon l'enumeration compte deux fois.

        Un doublon ne ferait pas planter le programme : il ferait juste que le
        nombre de combinaisons annonce (331 776) ne correspond plus au nombre de
        designs REELLEMENT distincts explores. L'argument d'exhaustivite devient
        alors une approximation non chiffree.
        """
        for nom, valeurs in (('L_VALS', O.L_VALS), ('C_VALS', O.C_VALS)):
            with self.subTest(grille=nom):
                self.assertTrue(np.all(np.diff(valeurs) > 0.0), 'non strictement croissante')
                self.assertEqual(len(set(np.round(valeurs, 15))), len(valeurs))

    def test_le_pas_de_la_serie_n_est_pas_exactement_geometrique(self):
        """Pas entre 1,182 et 1,250 pour un ideal 10^(1/12) = 1,2115.

        Propriete de la norme IEC 60063, pas un defaut de la grille. La dire
        exactement evite la phrase fausse "la serie E12 est geometrique de raison
        10^(1/12)", qu'un correcteur releverait.
        """
        espace = O.espace_de_recherche()
        self.assertAlmostEqual(espace['pas_ideal'], 10.0 ** (1.0 / 12.0), delta=1e-9)
        self.assertAlmostEqual(espace['pas_min'], 1.1818, delta=1e-3)
        self.assertAlmostEqual(espace['pas_max'], 1.2500, delta=1e-3)
        self.assertLess(espace['pas_min'], espace['pas_ideal'])
        self.assertGreater(espace['pas_max'], espace['pas_ideal'])


class TestExhaustivite(unittest.TestCase):
    """(d) Le compte des combinaisons, et ce qu'il autorise a dire."""

    def test_576_couples_par_voie_et_331776_combinaisons(self):
        """24 x 24 = 576 couples par voie ; 576^2 = 331 776 = 24^4 combinaisons.

        Ce nombre est cite a l'oral. S'il n'est pas exact, la phrase "recherche
        exhaustive" devient invendable.
        """
        espace = O.espace_de_recherche()
        # Seuils LUS dans criteres_geles.json (§ 09.6, principe 4) : un critere
        # chiffre qui ne vit que dans le test se confronte a lui-meme.
        n_couples = contexte.critere('d_series_e12', 'n_couples_par_voie')
        n_comb = contexte.critere('d_series_e12', 'n_combinaisons')
        n_valeurs = contexte.critere('d_series_e12', 'n_valeurs_par_serie')
        self.assertEqual(espace['n_couples_grave'], n_couples)
        self.assertEqual(espace['n_couples_medium'], n_couples)
        self.assertEqual(espace['n_combinaisons'], n_comb)
        self.assertEqual(espace['n_combinaisons'], n_valeurs ** 4)
        self.assertEqual(espace['n_combinaisons'],
                         espace['n_couples_grave'] * espace['n_couples_medium'])

    def test_couples_engendre_bien_le_produit_cartesien_sans_repetition(self):
        """``couples(a, b)`` doit rendre (len(a)*len(b), 2) paires toutes distinctes.

        C'est la brique de base de l'enumeration : une erreur ici (zip au lieu de
        produit cartesien, par exemple) reduirait silencieusement l'exploration
        de 576 a 24 couples, et le programme rendrait quand meme un gagnant.
        """
        a = np.array([1.0, 2.0, 3.0])
        b = np.array([10.0, 20.0])
        p = O.couples(a, b)
        self.assertEqual(p.shape, (6, 2))
        distincts = set(map(tuple, p.tolist()))
        self.assertEqual(len(distincts), 6)
        for x in a:
            for y in b:
                self.assertIn((float(x), float(y)), distincts)

    def test_l_enumeration_complete_annonce_le_bon_compte(self):
        """``enumere_e12`` doit rendre n_combinaisons = 331 776, effectivement evaluees.

        Le champ n'est pas declaratif : il vaut la taille du tableau J calcule.
        Si la fonction explorait moins, le compte tomberait avec.
        """
        f = F.grille_critere()
        Z = contexte.charge_resistive(f)
        debut = time.time()
        resultat = O.enumere_e12(f, Z, Z, cible_nom='butterworth', w=O.W_SANITY)
        duree = time.time() - debut
        n_comb = contexte.critere('d_series_e12', 'n_combinaisons')
        self.assertEqual(resultat['n_combinaisons'], n_comb)
        self.assertEqual(np.asarray(resultat['J_matrice']).size, n_comb)
        self.assertTrue(np.isfinite(resultat['J']))
        self.assertLess(duree, 60.0, 'enumeration anormalement lente : %.1f s' % duree)

    def test_l_optimum_n_est_pas_au_bord_de_la_grille(self):
        """Assertion anti-optimum-de-bord : 1,0 < L < 82 mH et 10 < C < 820 uF.

        Si le gagnant se collait a une borne, le "minimum global sur la grille"
        serait un artefact du domaine choisi et non une solution : il faudrait
        elargir la grille avant d'annoncer quoi que ce soit. Deux decades
        suffisent PARCE QUE les valeurs catalogue sont au centre -- c'est une
        hypothese, et ce test la controle a chaque execution.
        """
        f = F.grille_critere()
        Z = contexte.charge_resistive(f)
        resultat = O.enumere_e12(f, Z, Z, cible_nom='butterworth', w=O.W_SANITY)
        ok, avertissements = O.verifier_optimum_interieur(resultat)
        self.assertTrue(ok, 'optimum au bord : %r' % avertissements)
        for cle, grille in (('L1', O.L_VALS), ('C1', O.C_VALS),
                            ('C2', O.C_VALS), ('L2', O.L_VALS)):
            with self.subTest(composant=cle):
                self.assertGreater(resultat[cle], grille[0])
                self.assertLess(resultat[cle], grille[-1])

    def test_le_detecteur_de_bord_voit_le_cas_qui_se_produit_vraiment(self):
        """GARDE-FOU DU GARDE-FOU : sur la charge REELLE, l'optimum tombe en butee.

        Le test precedent ne s'exerce que sur 8 ohm resistif, ou l'optimum est
        interieur : il passe donc legitimement, mais il ne couvre PAS le cas qui se
        produit reellement. Sur la charge Z(f), l'optimum de la voie grave tombe sur
        la borne basse de la grille des condensateurs -- non parce que la grille est
        trop etroite, mais parce qu'une contrainte MANQUE : sans plancher sur C1, la
        cellule grave degenere en premier ordre et le 18 pouces rayonne encore a
        -23 dB a 1 kHz, defaut invisible pour une bande de cout arretee a 250 Hz
        (§ 04.5, contrainte 6).

        Un detecteur qui ne detecte jamais rien passe tous les controles. Ce test
        verifie donc que verifier_optimum_interieur repond bien FAUX quand c'est le
        cas, et nomme le composant fautif -- c'est cet avertissement-la que
        tout_refaire.py fait remonter jusqu'au recapitulatif et jusqu'a stderr.
        """
        f = F.grille_critere()
        Zs = MH.Z_depuis_jeu(f, MH.SUB_TYP_CLOS)
        Zm = MH.Z_depuis_jeu(f, MH.MED_TYP)
        dcr, _prix = O.fabriques_self(d_fil=1.4e-3)
        resultat = O.enumere_e12(f, Zs, Zm, cible_nom='butterworth', w=O.W_SANITY,
                                 dcr=dcr)
        ok, avertissements = O.verifier_optimum_interieur(resultat)
        self.assertFalse(ok, 'sur la charge reelle l optimum est cense tomber en '
                             'butee sur C1 : si ce n est plus le cas, c est un '
                             'RESULTAT, pas un detail -- verifier avant de changer '
                             'le test')
        self.assertTrue(avertissements, 'bord detecte mais aucun avertissement emis')
        self.assertTrue(any('C1' in a for a in avertissements),
                        'l avertissement ne nomme pas le composant fautif : %r'
                        % avertissements)


class TestVectorisation(unittest.TestCase):
    """(d) Le calcul par blocs doit rendre exactement ce qu'une boucle rendrait."""

    def test_la_version_vectorisee_egale_la_boucle_explicite(self):
        """Sur un sous-espace reduit, vectorise et boucle doivent coincider.

        Le produit exterieur par blocs existe pour une raison prosaique : sans
        decoupage, le tableau intermediaire des sommes pese 340 Mo a Nf = 64 et
        1,06 Go a Nf = 200 -- de quoi faire tomber un PC de lycee. Avec bloc = 48
        la crete retombe a 28 Mo. Mais du remodelage de tableaux est exactement
        l'endroit ou une transposition inversee produit un resultat plausible et
        faux. D'ou la comparaison a une boucle ecrite naivement.
        """
        verdict = O.verifier_vectorisation(bavard=False)
        self.assertTrue(verdict['ok'], 'vectorisation divergente : %r' % verdict)
        self.assertLess(verdict['ecart_max'], 1e-9)
        self.assertEqual(verdict['argmin_vect'], verdict['argmin_boucle'])
        self.assertGreater(verdict['n_combinaisons'], 100)

    def test_le_decoupage_en_blocs_ne_change_pas_le_resultat(self):
        """Changer la taille de bloc ne doit RIEN changer au J calcule.

        La taille de bloc est un reglage de memoire, pas un parametre physique.
        Si J en dependait, ce serait la preuve d'un effet de bord dans
        l'accumulation -- et les chiffres publies dependraient de la machine.
        """
        f = F.grille_critere()
        Z = contexte.charge_resistive(f)
        L_reduit = O.L_VALS[8:14]
        C_reduit = O.C_VALS[10:16]
        reference = None
        for bloc in (4, 17, 512):
            resultat = O.enumere_e12(f, Z, Z, L_vals=L_reduit, C_vals=C_reduit,
                                     bloc=bloc, cible_nom='butterworth', w=O.W_SANITY)
            J = np.asarray(resultat['J_matrice'], float)
            if reference is None:
                reference = J
            else:
                with self.subTest(bloc=bloc):
                    self.assertEqual(J.shape, reference.shape)
                    np.testing.assert_allclose(J, reference, rtol=1e-12, atol=1e-12)

    def test_le_minimum_annonce_est_bien_le_minimum_du_tableau(self):
        """Le design rendu doit correspondre a l'argmin du tableau J, pas a autre chose.

        Controle d'interface elementaire, et pourtant le seul qui garantisse que
        l'indice desapplati (``unravel_index``) pointe la bonne case. Une erreur
        de forme ici rendrait un design pris au hasard avec un J juste.
        """
        f = F.grille_critere()
        Z = contexte.charge_resistive(f)
        L_reduit = O.L_VALS[8:14]
        C_reduit = O.C_VALS[10:16]
        resultat = O.enumere_e12(f, Z, Z, L_vals=L_reduit, C_vals=C_reduit,
                                 cible_nom='butterworth', w=O.W_SANITY)
        J = np.asarray(resultat['J_matrice'], float)
        self.assertAlmostEqual(resultat['J'], float(J.min()), delta=1e-12)

        p1 = np.asarray(resultat['p1'], float)
        p2 = np.asarray(resultat['p2'], float)
        i, j = np.unravel_index(int(np.argmin(J)), J.shape)
        self.assertAlmostEqual(resultat['L1'], p1[i, 0], delta=1e-15)
        self.assertAlmostEqual(resultat['C1'], p1[i, 1], delta=1e-18)
        self.assertAlmostEqual(resultat['C2'], p2[j, 0], delta=1e-18)
        self.assertAlmostEqual(resultat['L2'], p2[j, 1], delta=1e-15)


class TestArrondiSurLaGrille(unittest.TestCase):
    """Projeter une valeur continue sur E12 : l'operation qui fait le cout de la contrainte."""

    def test_arrondir_serie_prend_le_plus_proche_en_echelle_log(self):
        """141 uF doit s'arrondir a 150 uF, pas a 120 uF.

        L'arrondi se fait en echelle LOGARITHMIQUE, parce que la grille l'est :
        en echelle lineaire, 141 est a 21 de 120 et a 9 de 150 -- meme conclusion
        ici, mais l'inverse arrive ailleurs sur la serie. Cet arrondi est
        exactement l'operation qui transforme le theoreme (b1) en non-theoreme (b2).
        """
        self.assertAlmostEqual(O.arrondir_serie(140.674e-6, O.C_VALS), 150e-6, delta=1e-12)
        self.assertAlmostEqual(O.arrondir_serie(18.006e-3, O.L_VALS), 18e-3, delta=1e-12)
        self.assertAlmostEqual(O.arrondir_serie(25.465e-3, O.L_VALS), 27e-3, delta=1e-12)
        self.assertAlmostEqual(O.arrondir_serie(99.47e-6, O.C_VALS), 100e-6, delta=1e-12)

    def test_arrondir_un_design_entier(self):
        """Le design analytique projete sur E12 doit donner le couple catalogue.

        C'est le chainon entre (b1) et (b2), ecrit noir sur blanc : le catalogue
        de la v1 n'est pas tombe du ciel, c'est le Butterworth analytique arrondi.
        """
        L, C = F.composants_canoniques('butterworth', 100.0, contexte.R_NOM)
        design = O.arrondir_design(dict(L1=L, C1=C, C2=C, L2=L), O.L_VALS, O.C_VALS)
        self.assertAlmostEqual(design['L1'], 18e-3, delta=1e-12)
        self.assertAlmostEqual(design['C1'], 150e-6, delta=1e-15)

    def test_une_valeur_hors_grille_est_ramenee_a_la_borne(self):
        """Demander 5000 uF sur une grille qui s'arrete a 820 uF doit rendre 820 uF.

        Comportement a connaitre : l'arrondi ne se plaint pas, il sature. C'est
        precisement pour cela que l'assertion anti-optimum-de-bord existe --
        elle, elle se plaint.
        """
        self.assertAlmostEqual(O.arrondir_serie(5000e-6, O.C_VALS), 820e-6, delta=1e-15)
        self.assertAlmostEqual(O.arrondir_serie(1e-9, O.C_VALS), 10e-6, delta=1e-15)


if __name__ == '__main__':
    unittest.main(verbosity=2)
