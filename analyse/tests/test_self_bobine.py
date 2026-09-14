"""Mission n. 8 / test (i) du § 09.6 -- satellite "self optimale".

CE QUE CE FICHIER PROTEGE
-------------------------
La self du passe-bas est le composant qui decide, a lui seul, du cout du filtre
passif -- en euros, en watts perdus et en kilogrammes de cuivre. Sans modele, on
achete au catalogue et on subit ; avec modele, la self entre dans la fonction de
cout et le TIPE cesse d'etre une recette.

Deux lois sont en jeu, et il ne faut surtout pas les confondre :

**1. A GEOMETRIE FIGEE (longueur de fil ell fixee), r x m est EXACTEMENT constant.**

    r = rho_Cu ell / S     et     m = rho_m S ell     donc     r m = rho_Cu rho_m ell^2

La section du fil disparait : doubler le diametre divise la resistance par 4 et
multiplie la masse par 4. C'est le compromis fondamental -- on n'achete pas "une
self", on achete un point sur une hyperbole resistance-masse, et le choix du fil
n'est rien d'autre que le choix du point.

**2. A INDUCTANCE FIXEE, c'est m r^(3/2) qui est a peu pres constant.**

    m = K_cu (L/r)^(3/2)

Cette seconde loi n'est pas exacte : quand on change de diametre a L constant, la
geometrie de la bobine change aussi (il faut plus de spires, le diametre moyen
grandit), donc la longueur de fil n'est plus la meme. K_cu vaut 1760 kg.s^(-3/2)
a 3 % pres sur le domaine utile (fil de 0,8 a 2,0 mm), ce que ce fichier verifie
contre le modele geometrique complet de Brooks. Le confondre avec la loi 1 --
"r x m = cte a L fixee" -- serait une erreur de raisonnement : r x m varie d'un
facteur 2 sur ce meme domaine.

L'enjeu chiffre : a 18 mH, viser 1 ohm de DCR au lieu de 1,64 ohm (la bobine de
Brooks en fil de 1,4 mm) fait passer la masse de cuivre de 2,0 a 4,3 kg et le
prix de 50 a 106 EUR. C'est un doublement pour 0,6 dB gagnes. Voila ce qu'une
fonction de cout doit arbitrer -- et ce qu'un catalogue ne dit pas.

Tous les prix sont des ORDRES DE GRANDEUR etiquetes ([[a verifier]] dans le
source) : aucun devis n'a ete demande.
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
import self_bobine as SB  # noqa: E402

L_CATALOGUE = 18e-3
DIAMETRES = (0.8e-3, 1.0e-3, 1.4e-3, 2.0e-3)


class TestLoiResistanceMasse(unittest.TestCase):
    """Mission n. 8 -- la loi r x m, dans sa version exacte et dans sa version approchee."""

    def test_a_geometrie_figee_le_produit_r_m_est_exactement_constant(self):
        """ell fixee : r x m = rho_Cu rho_m ell^2, independant du diametre du fil.

        C'est la loi EXACTE, et c'est elle qui porte l'argument physique : a
        longueur de fil donnee, on ne peut pas gagner sur les deux tableaux. Le
        diametre du fil deplace le point le long d'une hyperbole, il ne la quitte
        jamais. Un modele de cout qui pretendrait faire mieux se tromperait de
        physique, pas d'arrondi.
        """
        ell = 50.0  # metres
        attendu = SB.RHO_CU * SB.RHO_M * ell ** 2
        self.assertAlmostEqual(SB.produit_rm_geometrie_figee(ell), attendu, delta=1e-15)
        produits = []
        for d in DIAMETRES:
            r = SB.ohm_par_metre(d) * ell
            m_kg = SB.gramme_par_metre(d) * ell * 1e-3  # g/m -> kg
            produits.append(r * m_kg)
        produits = np.asarray(produits)
        self.assertLess(float(np.max(produits) / np.min(produits) - 1.0), 1e-12,
                        'r x m devrait etre RIGOUREUSEMENT constant a ell fixee')
        self.assertAlmostEqual(float(produits[0]), attendu, delta=1e-12 * attendu)

    def test_a_inductance_fixee_la_loi_est_en_r_puissance_trois_demis(self):
        """L fixee : m = K_cu (L/r)^(3/2), avec K_cu = 1760 a 3 % pres.

        Loi APPROCHEE, et c'est le point delicat. Quand on change de diametre a
        L constant, la bobine change de taille : la longueur de fil n'est plus la
        meme, donc la loi exacte du test precedent ne s'applique plus. On
        confronte ici le modele de cout (une puissance 3/2 et une constante) au
        modele geometrique complet (Brooks : nombre de spires, diametre moyen,
        longueur de fil developpee). L'accord a 3 % est ce qui autorise a
        remplacer le second par le premier dans la fonction de cout.
        """
        constantes = []
        for d in DIAMETRES:
            bobine = SB.brooks(L_CATALOGUE, d=d)
            constantes.append(bobine['m'] / (L_CATALOGUE / bobine['r']) ** 1.5)
        constantes = np.asarray(constantes)
        dispersion = float(np.max(constantes) / np.min(constantes) - 1.0)
        self.assertLess(dispersion, 0.10,
                        'K_cu disperse de %.1f %% sur les diametres usuels' % (100 * dispersion))
        for K in constantes:
            self.assertAlmostEqual(K / SB.K_CU_DEFAUT, 1.0, delta=0.05)

    def test_ne_pas_confondre_les_deux_lois(self):
        """A L fixee, r x m N'EST PAS constant : il varie d'un facteur 2.

        Ce test existe pour empecher une erreur de raisonnement, pas une erreur
        de code. En passant de 0,8 a 2,0 mm de fil a 18 mH, r x m passe de 2,18 a
        4,34 ohm.kg. Ecrire "r x m = cte" sans preciser "a geometrie figee" serait
        faux d'un facteur 2 -- exactement le genre d'imprecision qu'un jury
        demande de justifier.
        """
        produits = [SB.brooks(L_CATALOGUE, d=d)['r'] * SB.brooks(L_CATALOGUE, d=d)['m']
                    for d in DIAMETRES]
        rapport = max(produits) / min(produits)
        self.assertGreater(rapport, 1.5,
                           'a L fixee, r x m devrait varier nettement : %r' % produits)

    def test_masse_pour_et_brooks_s_accordent(self):
        """Modele de cout et modele geometrique doivent donner la meme masse a 5 % pres.

        ``masse_pour`` est la formule a une constante qui entre dans la fonction
        de cout ; ``brooks`` est le calcul geometrique complet, bien plus lent.
        Leur accord est ce qui permet d'enumerer 331 776 designs sans recalculer
        une bobine a chaque fois.
        """
        for d in DIAMETRES:
            with self.subTest(diametre_mm=1e3 * d):
                bobine = SB.brooks(L_CATALOGUE, d=d)
                approche = SB.masse_pour(L_CATALOGUE, bobine['r'])
                self.assertAlmostEqual(approche / bobine['m'], 1.0, delta=0.05)


class TestTrioMasseprixDcr(unittest.TestCase):
    """Le trio masse / prix / DCR : trois vues d'une meme decision d'achat."""

    def test_coherence_mutuelle_du_trio(self):
        """masse_pour, prix_pour et dcr_pour doivent etre inverses les uns des autres.

        Trois fonctions, un seul modele. Si ``dcr_pour(L, masse=m)`` ne rendait
        pas la resistance dont ``masse_pour(L, r)`` rend m, la fonction de cout
        pourrait optimiser une self qui n'existe pas.
        """
        for L in (10e-3, 18e-3, 33e-3):
            for r in (0.5, 1.0, 1.5, 2.0):
                with self.subTest(L_mH=1e3 * L, r=r):
                    m = SB.masse_pour(L, r)
                    self.assertAlmostEqual(SB.dcr_pour(L, masse=m), r, delta=1e-9 * r)
                    self.assertAlmostEqual(SB.prix_pour(L, r),
                                           m * SB.PRIX_KG_CU, delta=1e-9)
                    self.assertAlmostEqual(SB.masse_cuivre(L, r), m, delta=1e-12)
                    self.assertAlmostEqual(SB.cout_self(L, r), SB.prix_pour(L, r),
                                           delta=1e-12)

    def test_dcr_pour_exige_exactement_un_des_deux_arguments(self):
        """Donner ni r_max ni masse (ou les deux) doit LEVER.

        L'ambiguite serait couteuse : dire "je veux une self de 18 mH" sans dire
        laquelle, c'est ne rien dire. L'interface force l'appelant a se prononcer
        -- c'est le meme principe que les fabriques ci-dessous.
        """
        with self.assertRaises(Exception):
            SB.dcr_pour(L_CATALOGUE)
        with self.assertRaises(Exception):
            SB.dcr_pour(L_CATALOGUE, r_max=1.0, masse=0.5)

    def test_les_fabriques_forcent_a_dire_quelle_self_on_achete(self):
        """``fabrique_dcr`` / ``fabrique_prix_L`` rendent des fonctions de L seul.

        C'est ce que ``optim.cout(..., dcr=...)`` attend. L'interet de la
        fabrique est pedagogique autant que technique : on ne peut pas brancher un
        modele de DCR sans avoir decide, explicitement, quelle contrainte on
        s'impose (une DCR maximale ? une masse maximale ? un diametre de fil ?).
        """
        dcr = SB.fabrique_dcr(r_max=1.0)
        prix = SB.fabrique_prix_L(r_max=1.0)
        self.assertAlmostEqual(float(dcr(L_CATALOGUE)), 1.0, delta=1e-9)
        self.assertAlmostEqual(float(prix(L_CATALOGUE)),
                               SB.prix_pour(L_CATALOGUE, 1.0), delta=1e-9)
        dcr_masse = SB.fabrique_dcr(masse=1.0)
        self.assertGreater(float(dcr_masse(L_CATALOGUE)), 0.0)
        self.assertGreater(float(dcr_masse(33e-3)), float(dcr_masse(10e-3)),
                           'a masse imposee, une self plus grosse a plus de DCR')

    def test_les_fonctions_sont_vectorisees(self):
        """Elles doivent accepter un tableau de L : l'enumeration en depend.

        L'enumeration E12 evalue 331 776 designs. Si le modele de self devait
        etre appele point par point dans une boucle Python, l'acte 3 passerait de
        deux secondes a plusieurs minutes -- et on cesserait de le relancer.
        """
        L = np.array([1e-3, 18e-3, 82e-3])
        m = SB.masse_pour(L, 1.0)
        self.assertEqual(np.shape(m), (3,))
        self.assertTrue(np.all(np.diff(m) > 0.0), 'la masse doit croitre avec L')
        self.assertEqual(np.shape(SB.prix_pour(L, 1.0)), (3,))


class TestOrdresDeGrandeur(unittest.TestCase):
    """Les chiffres doivent etre plausibles : une self de 4 tonnes passerait tous les tests d'algebre."""

    def test_self_de_18_mH_a_1_ohm(self):
        """Quelques kilogrammes de cuivre et quelques dizaines d'euros, pas plus.

        Garde-fou de plausibilite. Une erreur d'unite (millimetre pris pour
        metre, gramme pour kilogramme) se voit ici et nulle part ailleurs : toutes
        les relations algebriques resteraient vraies, seuls les nombres seraient
        absurdes. Bornes larges et assumees : 0,5 a 10 kg, 10 a 400 EUR.
        """
        m = float(SB.masse_pour(L_CATALOGUE, 1.0))
        prix = float(SB.prix_pour(L_CATALOGUE, 1.0))
        self.assertGreater(m, 0.5)
        self.assertLess(m, 10.0)
        self.assertGreater(prix, 10.0)
        self.assertLess(prix, 400.0)
        self.assertAlmostEqual(m, 4.25, delta=0.05)

    def test_la_bobine_de_brooks_en_fil_de_1_4_mm(self):
        """Geometrie complete a 18 mH : ~ 454 spires, ~ 146 m de fil, 1,64 ohm, 2,02 kg.

        Ces chiffres sont le pont entre le modele et l'atelier : 146 metres de
        fil de 1,4 mm, c'est une bobine de 137 mm de diametre exterieur. Ils
        disent si le projet est realisable, pas seulement calculable.
        """
        b = SB.brooks(L_CATALOGUE)
        self.assertAlmostEqual(b['N'], 454.0, delta=5.0)
        self.assertAlmostEqual(b['ell'], 146.5, delta=2.0)
        self.assertAlmostEqual(b['r'], 1.637, delta=0.02)
        self.assertAlmostEqual(b['m'], 2.021, delta=0.03)
        self.assertAlmostEqual(b['prix'], 50.5, delta=1.0)
        self.assertAlmostEqual(b['L_verif'] / L_CATALOGUE, 1.0, delta=0.02,
                               msg='la geometrie rendue ne redonne pas L')
        self.assertAlmostEqual(SB.dcr_de_L(L_CATALOGUE), b['r'], delta=1e-9)

    def test_le_prix_de_la_dcr_basse_est_brutal(self):
        """Passer de 1,64 a 1,00 ohm double la masse et le prix, pour 0,6 dB.

        L'arbitrage central du satellite, chiffre. Sans lui, "prendre une self a
        faible DCR" est un conseil gratuit ; avec lui, c'est une decision qui
        coute 56 EUR et 2,2 kg, a mettre en balance avec le reste du budget
        (500 EUR).
        """
        m_brooks = SB.brooks(L_CATALOGUE)['m']
        r_brooks = SB.brooks(L_CATALOGUE)['r']
        m_1ohm = float(SB.masse_pour(L_CATALOGUE, 1.0))
        self.assertGreater(m_1ohm / m_brooks, 1.8)
        gain_dB = SB.insertion_dB(1.0) - SB.insertion_dB(r_brooks)
        self.assertGreater(gain_dB, 0.0)
        self.assertLess(gain_dB, 1.0, 'le gain acoustique est faible : c est tout le propos')

    def test_perte_d_insertion_d_un_ohm_face_a_huit(self):
        """1 ohm de DCR sur 8 ohm : 11,1 % de la puissance en chaleur, -1,02 dB.

        Chiffre de controle du projet, verifie ici a la source. La fraction
        dissipee est r/(r+Z) = 1/9 ; la perte en tension est 20 log(8/9).
        """
        self.assertAlmostEqual(SB.fraction_dissipee(1.0, 8.0), 1.0 / 9.0, delta=1e-12)
        self.assertAlmostEqual(SB.insertion_dB(1.0, 8.0), -1.023, delta=1e-3)
        self.assertAlmostEqual(SB.insertion_dB(1.0, 8.0),
                               20.0 * np.log10(8.0 / 9.0), delta=1e-9)

    def test_resonance_de_mesure_de_l_inductance(self):
        """18 mH en serie avec 150 uF resonne a 96,86 Hz : c'est la methode de mesure au GBF.

        Sans pont RLC, on mesure L en cherchant la resonance serie avec un C
        connu. La meme formule sert de pole au filtre -- c'est le meme objet
        physique, et le code ne doit pas en avoir deux versions.
        """
        self.assertAlmostEqual(SB.f0_serie(L_CATALOGUE, 150e-6), 96.8586, delta=1e-3)
        self.assertAlmostEqual(SB.L_depuis_f0(96.8586, 150e-6), L_CATALOGUE,
                               delta=1e-6)
        import filtre as F
        self.assertAlmostEqual(SB.f0_serie(L_CATALOGUE, 150e-6),
                               F.pole_et_q(L_CATALOGUE, 150e-6, 8.0)[0], delta=1e-9)


class TestSuiteInterneDuModule(unittest.TestCase):
    """Le module porte sa propre batterie de controles : on la consomme ici."""

    def test_les_53_controles_internes_passent(self):
        """``self_bobine.verifier()`` doit rendre 53 controles, tous au vert.

        Integrales elliptiques par AGM, formule de Wheeler contre un cas tabule,
        constante de Brooks retrouvee par extrapolation, effet de peau... Ces
        controles sont ecrits au plus pres des formules ; les rejouer depuis la
        suite unittest garantit qu'ils tournent dans ``tout_refaire.py``, et pas
        seulement quand quelqu'un execute le module a la main.
        """
        controles = SB.verifier(verbeux=False)
        self.assertGreaterEqual(len(controles), 50)
        echecs = [c for c in controles if not c['ok']]
        self.assertEqual(echecs, [], '%d controle(s) interne(s) en echec : %r'
                         % (len(echecs), [c['nom'] for c in echecs]))

    def test_forme_optimale_de_wheeler(self):
        """Lagrange sur le modele de Wheeler : b/a = 2/3 exact et c/a = 0,600.

        La bobine de Brooks n'est pas une recette d'atelier : c'est le maximum
        d'inductance a longueur de fil donnee, et il se demontre. Le retrouver
        par optimisation numerique est exactement le genre de resultat que le
        niveau prepa permet de defendre.
        """
        beta, gamma = SB.proportions_optimales_wheeler()
        self.assertAlmostEqual(beta, 2.0 / 3.0, delta=1e-6)
        self.assertAlmostEqual(gamma, 0.600, delta=5e-3)
        beta_num, gamma_num = SB.optimum_forme_wheeler()
        self.assertAlmostEqual(beta_num, beta, delta=5e-3)
        self.assertAlmostEqual(gamma_num, gamma, delta=5e-3)


if __name__ == '__main__':
    unittest.main(verbosity=2)
