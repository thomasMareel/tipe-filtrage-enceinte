"""Mission n. 3 / tests (b1)-(b3) du § 09.6 -- porte de validation de l'optimiseur.

CE QUE CE FICHIER PROTEGE
-------------------------
C'est LA porte de validation du projet : "si ca echoue, c'est un bug, et on
n'achete rien". Elle est en deux etages, et confondre les deux serait une faute
de raisonnement, pas seulement de code.

**(b1) Le continu est un THEOREME.** Sur une charge 8 ohm resistive pure, sans
DCR ni penalite, le probleme d'optimisation continu EST celui du catalogue. Un
optimiseur qui ne redonne pas le Butterworth analytique est en panne :

    cible='butterworth' -> L = 18,006326 mH   C = 140,674424 uF   (Q = 1/racine 2)
    cible='lr2'         -> L = 25,464791 mH   C =  99,471839 uF   (Q = 1/2)

Ecart exige : moins de 1e-6 en relatif. (Mesure : 1e-15, soit la precision
machine.) La decision D2 impose que les DEUX cibles passent : la cible de
sommation est volontairement reportee apres la phase 1, donc le code ne doit
jamais la traiter comme une constante.

**(b2) Le discret N'EST PAS un theoreme.** Le passage a E12 est une PROJECTION
sur une grille, et la grille n'est pas stable par les symetries du probleme. Le
gagnant discret depend donc legitimement de J et de la bande. C'est un test de
NON-REGRESSION : il protege contre une modification involontaire de la fonction
de cout, il ne demontre rien.

    cible='butterworth' -> 18,0 mH / 150 uF | 150 uF / 18,0 mH, J = 0,9471
    cible='lr2'         -> 27,0 mH / 100 uF | 100 uF / 27,0 mH, Q = 0,4869

**(b3) L'enumeration JOINTE n'est pas une inflation.** Objection de jury
legitime : si J se separait en J1(voie 1) + J2(voie 2), 1152 evaluations
suffiraient au lieu de 331 776. Verifie ici : les termes de somme et de phase
COUPLENT les deux voies, et le couplage change la reponse -- avec le seul terme
"forme de chaque voie", le passe-haut choisit 15,0 mH ; avec le J gele, il
choisit 18,0 mH. Il faut savoir dire quels termes couplent (somme, phase, budget
total) et lesquels ne couplent pas (forme par voie, prix par voie, pertes par voie).

Les charges utilisees ici sont RESISTIVES : c'est un banc d'essai du code, pas un
modele du haut-parleur. Aucune mesure de l'enceinte n'existe a ce jour.
"""

import os
import sys
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


class TestPorteContinue(unittest.TestCase):
    """(b1) Sur 8 ohm resistifs, l'optimiseur continu DOIT redonner l'analytique."""

    def test_b1_butterworth(self):
        """cible='butterworth' : 18,006326 mH / 140,674424 uF a 1e-6 pres.

        C'est le theoreme. Sur charge resistive pure, minimiser l'ecart a la
        cible Butterworth, c'est resoudre l'equation du catalogue -- il n'y a pas
        d'autre minimum. Un echec ici ne se negocie pas : il interdit d'acheter
        le moindre composant, parce que plus aucun chiffre produit par la chaine
        n'est garanti.
        """
        resultat = O.sanity_check_continu(cible_nom='butterworth', R=contexte.R_NOM,
                                          f0_cible=100.0, lever=False)
        self.assertTrue(resultat['ok'], 'porte continue Butterworth : %r' % resultat)
        self.assertLess(resultat['ecart_max'],
                        contexte.critere('b1_optimiseur_continu', 'ecart_relatif_max'))
        self.assertAlmostEqual(resultat['L1'], 0.018006326, delta=1e-8)
        self.assertAlmostEqual(
            resultat['C1'],
            contexte.critere('b1_optimiseur_continu', 'butterworth_C_F'), delta=1e-11)

    def test_b1_linkwitz_riley_2(self):
        """cible='lr2' : 25,464791 mH / 99,471839 uF a 1e-6 pres (decision D2).

        La cible de sommation n'est pas gelee : le code doit etre aussi juste sur
        le Linkwitz-Riley que sur le Butterworth. Si un seul des deux passait,
        cela voudrait dire qu'une cible est cablee en dur quelque part -- et le
        gel de D2 se ferait par omission, ce que la decision interdit
        explicitement.
        """
        resultat = O.sanity_check_continu(cible_nom='lr2', R=contexte.R_NOM,
                                          f0_cible=100.0, lever=False)
        self.assertTrue(resultat['ok'], 'porte continue LR2 : %r' % resultat)
        self.assertLess(resultat['ecart_max'], 1e-6)
        self.assertAlmostEqual(resultat['L1'], 0.025464791, delta=1e-8)
        self.assertAlmostEqual(resultat['C1'], 99.471839e-6, delta=1e-11)

    def test_b1_l_echec_doit_lever(self):
        """``lever=True`` doit transformer un echec en exception, pas en ligne de journal.

        ``tout_refaire.py`` s'arrete au premier echec et rend le code 1. Une porte
        de validation qui se contente d'ecrire "ok: False" quelque part n'arrete
        rien : la chaine continuerait et produirait des figures.
        """
        self.assertTrue(issubclass(O.EchecSanityCheck, AssertionError))
        with self.assertRaises(O.EchecSanityCheck):
            O.sanity_check_continu(cible_nom='butterworth', tolerance=1e-18, lever=True)

    def test_b1_les_deux_cibles_en_une_commande(self):
        """``sanity_check_complet`` doit couvrir les DEUX cibles (decision D2).

        Une seule commande qui verifie les deux : c'est ce que ``tout_refaire.py``
        appelle. Si elle n'en testait qu'une, l'autre deriverait sans que
        personne ne s'en apercoive jusqu'a la phase 3.
        """
        verdicts = O.sanity_check_complet(bavard=False)
        cibles = {v.get('cible_nom', v.get('cible')) for v in verdicts}
        self.assertIn('butterworth', cibles)
        self.assertIn('lr2', cibles)
        for verdict in verdicts:
            with self.subTest(verdict=verdict.get('cible_nom', verdict.get('cible'))):
                self.assertTrue(verdict.get('ok'), 'verdict en echec : %r' % verdict)


class TestPorteDiscrete(unittest.TestCase):
    """(b2) Non-regression du gagnant E12 sous le J gele -- pas une verite mathematique."""

    @classmethod
    def setUpClass(cls):
        """Les enumerations coutent ~3 s chacune : on les fait une fois pour la classe."""
        cls.bw = O.sanity_check_e12(cible_nom='butterworth', R=contexte.R_NOM,
                                    f0_cible=100.0, lever=False)
        cls.lr2 = O.sanity_check_e12(cible_nom='lr2', R=contexte.R_NOM,
                                     f0_cible=100.0, lever=False)

    def test_b2_gagnant_butterworth(self):
        """J gele, 8 ohm : 18,0 mH / 150 uF sur les deux voies, J = 0,9471, f0 = 96,86 Hz.

        Formulation a tenir devant le jury : "sur 8 ohm le probleme continu est
        celui du catalogue ; le passage a E12 peut legitimement choisir un voisin
        different d'une voie a l'autre, ce n'est pas un bug mais une propriete de
        la grille." Ici les deux voies tombent sur le meme couple -- mais c'est
        un resultat, pas une obligation.
        """
        design = self.bw['design']
        self.assertTrue(self.bw['ok'], 'gagnant E12 Butterworth : %r' % design)
        self.assertAlmostEqual(design['L1'], 18e-3, delta=1e-9)
        self.assertAlmostEqual(design['C1'], 150e-6, delta=1e-12)
        self.assertAlmostEqual(design['C2'], 150e-6, delta=1e-12)
        self.assertAlmostEqual(design['L2'], 18e-3, delta=1e-9)
        self.assertAlmostEqual(
            self.bw['J'], contexte.critere('b2_optimiseur_e12', 'butterworth_J'),
            delta=contexte.critere('b2_optimiseur_e12', 'butterworth_J_delta'))
        self.assertAlmostEqual(
            self.bw['f0'], contexte.critere('b2_optimiseur_e12', 'butterworth_f0_Hz'),
            delta=contexte.critere('b2_optimiseur_e12', 'butterworth_f0_delta_Hz'))
        self.assertAlmostEqual(self.bw['Q'], 0.7303, delta=1e-3)

    def test_b2_gagnant_linkwitz_riley_2(self):
        """J gele, cible LR2 : 27,0 mH / 100 uF, Q = 0,4869 (analytique 25,465 / 99,472).

        La projection E12 du LR2 analytique donne 27 mH et non 25 : l'ecart au
        Q ideal de 0,5 est de 2,6 %. C'est le cout de la contrainte de catalogue
        sur cette cible-la, et il differe de celui du Butterworth -- raison de
        plus pour que la cible reste un parametre.
        """
        design = self.lr2['design']
        self.assertTrue(self.lr2['ok'], 'gagnant E12 LR2 : %r' % design)
        self.assertAlmostEqual(design['L1'], 27e-3, delta=1e-9)
        self.assertAlmostEqual(design['C1'], 100e-6, delta=1e-12)
        self.assertAlmostEqual(self.lr2['Q'], 0.4869, delta=1e-3)
        self.assertLess(self.lr2['Q'], 0.7303,
                        'le LR2 doit etre plus amorti que le Butterworth')

    def test_b2_le_gagnant_e12_n_est_pas_l_analytique(self):
        """Le discret differe du continu : c'est le COUT de la contrainte E12.

        Ce test dit ce que (b1) et (b2) ont de different. 150 uF au lieu de
        140,67 uF, c'est 6,6 % d'ecart sur C et 3,1 % sur le pole. Si le gagnant
        E12 coincidait avec l'analytique, ce serait le signe que la grille n'est
        pas appliquee.
        """
        L_analytique, C_analytique = F.composants_canoniques('butterworth', 100.0,
                                                             contexte.R_NOM)
        design = self.bw['design']
        self.assertGreater(abs(design['C1'] / C_analytique - 1.0), 0.05)
        self.assertLess(abs(design['L1'] / L_analytique - 1.0), 0.01)

    def test_b2_le_plateau_de_l_optimum_est_plat(self):
        """Le deuxieme meilleur design doit etre proche : l'optimum est un plateau.

        Fait central pour l'honnetete de la conclusion (§ 04.8) : l'optimum
        n'est pas un pic aigu. Annoncer "le design optimal est celui-ci" sans
        dire que plusieurs voisins font aussi bien serait une fausse precision.

LE PLATEAU EST UNE PROPRIETE DE LA CHARGE REELLE, PAS DE 8 OHM (correction
        de relecture du 2026-09-14). Ce test appelait analyser_plateau(seuil_pct=50.0)
        sur la charge 8 ohm puis n'exigeait que n_dans_plateau >= 2 : a 50 % de
        tolerance des centaines de designs entrent dans le "plateau", l'assertion est
        quasi inconditionnelle, et elle ne protegeait rien tout en donnant
        l'apparence d'un controle. Le journal de tout_refaire.py, lui, utilise 1 % :
        c'est ce chiffre-la qui est cite a l'oral.

        Et surtout, teste au bon endroit le seuil de 1 % REFUTE la these : sur 8 ohm
        resistif l'optimum n'est PAS plat -- le deuxieme meilleur est a +42,6 %, un
        seul design dans le plateau a 1 %. C'est normal, et c'est meme rassurant : sur
        8 ohm le probleme continu est celui du catalogue, un theoreme, donc son
        optimum est net. Le plateau du § 04.8 est un phenomene de la CHARGE REELLE,
        ou plusieurs voisins E12 se valent parce que Z(f) aplatit les differences.
        Le test verifie donc les DEUX faits, chacun sur sa charge -- c'est ce que
        Thomas doit pouvoir dire au tableau.
        """
        classement = O.classement(self.bw['enumeration'], n=5)
        self.assertEqual(len(classement), 5)
        self.assertLessEqual(classement[0]['J'], classement[1]['J'])

        # (1) Sur 8 ohm : l'optimum est NET. Si cela changeait, ce serait un
        #     resultat, pas un detail -- la porte de validation en depend.
        plat_8ohm = O.analyser_plateau(self.bw['enumeration'], seuil_pct=1.0)
        self.assertEqual(plat_8ohm['n_dans_plateau'], 1,
                         'sur 8 ohm resistif l optimum est cense etre net')
        self.assertGreater(plat_8ohm['ecart_2e_pct'], 10.0,
                           'le 2e meilleur sur 8 ohm est cense etre loin (+42,6 %)')

        # (2) Sur la charge REELLE : c'est un plateau, et la conclusion doit parler
        #     d'une FAMILLE de designs. La marche E12 vaut environ 21 % ; ici le 2e
        #     meilleur est a moins de 1 %, soit vingt fois moins que la marche.
        f = F.grille_critere()
        Zs = MH.Z_depuis_jeu(f, MH.SUB_TYP_CLOS)
        Zm = MH.Z_depuis_jeu(f, MH.MED_TYP)
        dcr, _prix = O.fabriques_self(d_fil=1.4e-3)
        reelle = O.enumere_e12(f, Zs, Zm, cible_nom='butterworth', w=O.W_SANITY,
                               dcr=dcr)
        plat_reel = O.analyser_plateau(reelle, seuil_pct=1.0)
        self.assertGreaterEqual(
            plat_reel['n_dans_plateau'], 2,
            'sur la charge reelle, le plateau a 1 %% ne contient qu un design : '
            'annoncer un optimum unique serait alors legitime, ce qui contredit le '
            'discours du § 04.8 -- a verifier avant de changer le test')
        pas_e12 = 100.0 * (contexte.critere('d_series_e12', 'pas_grille_max') - 1.0)
        self.assertLess(
            plat_reel['ecart_2e_pct'], pas_e12,
            'sur la charge reelle le 2e meilleur est plus loin que la marche E12 '
            'elle-meme (%.1f %%) : ce ne serait plus un plateau' % pas_e12)


class TestCouplageDesDeuxVoies(unittest.TestCase):
    """(b3) L'enumeration jointe change la reponse : elle n'est pas decorative."""

    @classmethod
    def setUpClass(cls):
        f = F.grille_critere()
        Z = contexte.charge_resistive(f)
        cls.f, cls.Z = f, Z
        cls.voies_seules = O.enumere_e12(f, Z, Z, cible_nom='butterworth',
                                         w=dict(s=0.0, v=1.0, phi=0.0, eur=0.0, W=0.0))
        cls.somme_seule = O.enumere_e12(f, Z, Z, cible_nom='butterworth',
                                        w=dict(s=1.0, v=0.0, phi=0.0, eur=0.0, W=0.0))
        cls.j_gele = O.enumere_e12(f, Z, Z, cible_nom='butterworth', w=O.W_SANITY)

    def test_b3_le_terme_par_voie_seul_choisit_une_autre_self(self):
        """Critere separable : le passe-haut choisit 15,0 mH, pas 18,0 mH.

        Avec le seul terme "forme de chaque voie", J = J1 + J2 : les deux voies
        s'optimisent independamment et il suffirait de 2 x 576 evaluations. Le
        resultat differe de celui du J gele -- c'est la preuve chiffree que le
        couplage existe.
        """
        self.assertAlmostEqual(self.voies_seules['L1'], 18e-3, delta=1e-9)
        self.assertAlmostEqual(self.voies_seules['C1'], 150e-6, delta=1e-12)
        self.assertAlmostEqual(self.voies_seules['L2'], 15e-3, delta=1e-9)
        self.assertNotAlmostEqual(self.voies_seules['L2'], self.j_gele['L2'], places=6)

    def test_b3_le_terme_de_somme_seul_ne_definit_pas_un_raccord(self):
        """Somme seule : 15 mH / 120 uF | 120 uF / 22 mH -- un autre design encore.

        Degenerescence documentee au § 04.5 : la somme des deux voies peut etre
        plate sans que le raccord soit a la bonne frequence, parce qu'un
        passe-bas trop haut compense un passe-haut trop haut. Le terme "forme de
        chaque voie" est ce qui ancre la frequence de raccord ; la somme seule ne
        suffit pas.
        """
        self.assertAlmostEqual(self.somme_seule['L1'], 15e-3, delta=1e-9)
        self.assertAlmostEqual(self.somme_seule['C1'], 120e-6, delta=1e-12)
        self.assertAlmostEqual(self.somme_seule['C2'], 120e-6, delta=1e-12)
        self.assertAlmostEqual(self.somme_seule['L2'], 22e-3, delta=1e-9)

    def test_b3_le_j_gele_tranche_entre_les_deux(self):
        """Le J gele (somme + voies + phase) redonne 18 mH / 150 uF sur les deux voies.

        Les trois resultats de cette classe sont differents. C'est la reponse a
        l'objection "pourquoi 331 776 combinaisons et pas 1152 ?" : parce que les
        termes de somme et de phase couplent les voies, et que le couplage change
        le gagnant.
        """
        self.assertAlmostEqual(self.j_gele['L1'], 18e-3, delta=1e-9)
        self.assertAlmostEqual(self.j_gele['L2'], 18e-3, delta=1e-9)
        self.assertAlmostEqual(
            self.j_gele['J'], contexte.critere('b2_optimiseur_e12', 'butterworth_J'),
            delta=contexte.critere('b2_optimiseur_e12', 'butterworth_J_delta'))
        designs = {
            'voies_seules': (self.voies_seules['L1'], self.voies_seules['L2']),
            'somme_seule': (self.somme_seule['L1'], self.somme_seule['L2']),
            'j_gele': (self.j_gele['L1'], self.j_gele['L2']),
        }
        self.assertEqual(len(set(designs.values())), 3,
                         'les trois criteres devraient donner trois designs distincts')


class TestCibleParametreEtPoidsNonGeles(unittest.TestCase):
    """Decision D2 et principe 4 : la cible et les poids ne sont pas des constantes."""

    def test_la_fonction_de_cout_s_evalue_sur_les_trois_cibles(self):
        """``cout`` doit accepter les trois noms de cible, et les DISTINGUER.

        Decision D2 : la cible est un parametre. Le discriminant le plus net est
        le J rendu sur un meme design : le Butterworth et le Linkwitz-Riley ne
        peuvent pas noter 18 mH / 150 uF de la meme facon.

        Point a ne pas confondre avec un bug : 'plate' et 'lr2' donnent
        EXACTEMENT le meme J, et c'est voulu. Deux filtres du 2e ordre en
        quadrature dont la somme est plate, c'est precisement la paire
        Linkwitz-Riley (Q = 1/2) : la somme des modules y vaut 1, soit 0 dB.
        Le Butterworth (Q = 1/racine 2), lui, somme a +3 dB au croisement. 'plate'
        est donc le nom PHYSIQUE de ce que 'lr2' nomme par sa famille de filtre ;
        les deux designent la meme cible. Le test fige cette equivalence pour
        qu'un lecteur ne la prenne pas pour un parametre ignore.
        """
        f = F.grille_critere()
        Z = contexte.charge_resistive(f)
        p1 = np.array([[18e-3, 150e-6]])
        p2 = np.array([[150e-6, 18e-3]])
        valeurs = {}
        for nom in F.CIBLES:
            J = O.cout(p1, p2, f, Z, Z, cible_nom=nom, w=O.W_SANITY)
            valeurs[nom] = float(np.asarray(J).reshape(-1)[0])
            with self.subTest(cible=nom):
                self.assertTrue(np.isfinite(valeurs[nom]))
        self.assertNotAlmostEqual(valeurs['butterworth'], valeurs['lr2'], places=3,
                                  msg='Butterworth et LR2 notent pareil : cible ignoree')
        self.assertAlmostEqual(valeurs['plate'], valeurs['lr2'], places=9,
                               msg="'plate' et 'lr2' sont la meme cible par construction")

    def test_la_cible_plate_somme_a_0_dB_et_le_butterworth_a_plus_3_dB(self):
        """Le discriminant physique des deux cibles, au croisement.

        Butterworth 2e ordre : les deux voies valent 1/racine(2) a f_c et sont en
        quadrature -- avec l'inversion de polarite obligatoire, la somme vaut
        racine(2), soit +3 dB. Linkwitz-Riley 2 : les deux voies valent 1/2, en
        phase apres inversion, la somme vaut 1, soit 0 dB. C'est exactement le
        choix que la decision D2 laisse ouvert : accepter une bosse de 3 dB au
        raccord, ou viser une somme plate. Le chiffrer ici evite de trancher par
        habitude.
        """
        f_c = np.array([100.0])
        self.assertAlmostEqual(abs(F.cible_somme(f_c, 'butterworth')[0]),
                               np.sqrt(2.0), delta=1e-6)
        self.assertAlmostEqual(abs(F.cible_somme(f_c, 'lr2')[0]), 1.0, delta=1e-6)
        self.assertAlmostEqual(abs(F.cible_somme(f_c, 'plate')[0]), 1.0, delta=1e-6)
        self.assertAlmostEqual(F.CIBLES_Q['butterworth'], 1 / np.sqrt(2.0), delta=1e-12)
        self.assertAlmostEqual(F.CIBLES_Q['lr2'], 0.5, delta=1e-12)

    def test_les_poids_restent_refuses_tant_que_d5_n_est_pas_gelee(self):
        """``poids_geles`` doit LEVER tant que la decision D5 porte [[a geler]].

        Principe 4 du § 09.1 : les decisions gelees sont un fichier, pas une
        intention. Tant que les poids de J ne sont pas signes et dates, le code ne
        doit pas s'en servir en silence -- sinon rien n'empeche de les retoucher
        apres avoir vu les resultats, et l'honnetete du sujet s'effondre.
        """
        import io_mesures as IO
        with self.assertRaises(IO.CriteresNonGeles):
            O.poids_geles(exiger_geles=True)
        w, source = O.poids_geles(exiger_geles=False)
        self.assertIn('PROPOSITION', source.upper())
        self.assertEqual(set(w), set(O.W_PROPOSE))

    def test_le_cout_accepte_un_modele_de_dcr_venu_de_self_bobine(self):
        """L'argument ``dcr`` doit brancher le satellite "self optimale" sur le cout.

        C'est ce couplage -- et lui seul -- qui fait de l'etude de la self une
        piece du recit plutot qu'une annexe decorative : la self choisie change
        les watts perdus et les euros depenses, donc le design optimal.
        """
        f = F.grille_critere()
        Z = contexte.charge_resistive(f)
        p1 = np.array([[18e-3, 150e-6]])
        p2 = np.array([[150e-6, 18e-3]])
        dcr, prix_L = O.fabriques_self(r_max=1.0)
        self.assertAlmostEqual(float(dcr(18e-3)), 1.0, delta=1e-9)
        self.assertGreater(float(prix_L(18e-3)), 0.0)
        sans = float(np.asarray(O.cout(p1, p2, f, Z, Z, w=O.W_PROPOSE)).reshape(-1)[0])
        avec = float(np.asarray(O.cout(p1, p2, f, Z, Z, w=O.W_PROPOSE, dcr=dcr,
                                       prix_L=prix_L)).reshape(-1)[0])
        self.assertGreater(avec, sans,
                           'une self reelle (DCR + prix) doit couter plus qu une self ideale')


if __name__ == '__main__':
    unittest.main(verbosity=2)
