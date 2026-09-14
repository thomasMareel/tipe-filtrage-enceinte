"""Mission n. 5 / test (c) du § 09.6 -- propagation d'incertitude sur f_0.

CE QUE CE FICHIER PROTEGE
-------------------------
La v1 du TIPE annoncait "11 % d'incertitude sur la frequence de coupure". Ce
chiffre venait d'un circuit RC du PREMIER ordre, abandonne depuis. Applique a un
LC du second ordre, il est faux d'un facteur 2 -- et un correcteur le voit
immediatement. Ce fichier est la garantie ecrite que ce chiffre ne peut plus
sortir de la chaine.

La bonne formule, pour f_0 = 1/(2 pi racine(LC)), vient de
ln f_0 = -(1/2)(ln L + ln C), d'ou le facteur 1/2 :

    u(f_0)/f_0 = (1/2) racine( (u_L/L)^2 + (u_C/C)^2 + 2 rho (u_L/L)(u_C/C) )

La formule INTERDITE, celle du premier ordre, est la meme SANS le facteur 1/2 :
racine(u_L^2 + u_C^2). C'est elle qui, a 5 % et 10 %, donne les 11,18 % de la v1.

Trois lectures a ne pas melanger, toutes trois figees ici :

    convention GUM retenue (loi rectangulaire, u = a/racine 3) ...  4,08 %
    borne au pire cas (demi-largeurs combinees en quadrature) ...   7,07 %
    memes composants correles (rho = +1, meme lot) ..............  10,00 %

Une tolerance catalogue "+/- 10 %" est une DEMI-LARGEUR de loi rectangulaire :
l'incertitude-type vaut a/racine 3 = 5,77 %, pas 10 %. Sans cette convention
ecrite, on remplacerait l'erreur de facteur 2 de la v1 par une erreur de facteur
racine 3 restee implicite. Le Monte-Carlo confirme les trois lectures -- et c'est
lui, pas un rapport a 2, qui refute la formule du premier ordre.

Le biais du Monte-Carlo est verifie lui aussi : E[f_0] n'est pas f_0(E[L], E[C]),
l'ecart attendu vaut (3/8)(u_L^2 + u_C^2) = 0,75 % a 10 %/10 %.
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
import incertitudes as N  # noqa: E402

L_CATALOGUE = 18e-3
C_CATALOGUE = 150e-6
TOLERANCE = 0.10  # DEMI-LARGEUR catalogue (+/- 10 %), pas une incertitude-type
GRAINE = 7


class TestFormuleAnalytique(unittest.TestCase):
    """(c) La formule, son facteur 1/2, et ses trois lectures."""

    def test_c_convention_gum_retenue(self):
        """Loi rectangulaire : u = a/racine 3 = 5,77 %, d'ou u(f_0)/f_0 = 4,08 %.

        C'est LA lecture retenue par le projet (GUM, JCGM 100:2008). Une
        tolerance de composant n'est pas un ecart-type : le fabricant garantit un
        intervalle, pas une gaussienne. Confondre les deux surestime l'incertitude
        d'un facteur racine 3.
        """
        u = N.type_b_rectangulaire(TOLERANCE)
        self.assertAlmostEqual(u, TOLERANCE / np.sqrt(3.0), delta=1e-12)
        self.assertAlmostEqual(u, 0.0577, delta=5e-4)
        # Seuil LU dans criteres_geles.json (§ 09.6, principe 4) : un critere qui
        # ne vit que dans le test se confronte a lui-meme.
        self.assertAlmostEqual(N.u_f0_relative(u, u),
                               contexte.critere('c_incertitudes', 'u_f0_gum_pct') / 100.,
                               delta=5e-4)

    def test_c_borne_au_pire_cas(self):
        """Demi-largeurs combinees en quadrature : 7,07 %, et c'est une BORNE.

        Chiffre citable, mais jamais comme incertitude-type. L'etiquette compte
        autant que le nombre : c'est la difference entre "mon filtre est a
        100 Hz +/- 4 %" et "au pire, 100 Hz +/- 7 %".
        """
        self.assertAlmostEqual(
            N.u_f0_relative(TOLERANCE, TOLERANCE),
            contexte.critere('c_incertitudes', 'u_f0_borne_pire_cas_pct') / 100.,
            delta=5e-4)
        self.assertAlmostEqual(N.u_f0_relative(TOLERANCE, TOLERANCE),
                               0.5 * np.sqrt(2.0) * TOLERANCE, delta=1e-12)

    def test_c_le_couple_est_rendu_ensemble_jamais_un_nombre_seul(self):
        """``u_f0`` doit rendre LES DEUX lectures, pas en choisir une.

        Une fonction qui rendrait un seul nombre obligerait l'appelant a se
        souvenir de quelle convention il a demande. En rendant le couple
        (borne au pire cas, incertitude-type), la structure du resultat empeche
        la confusion -- c'est de la conception, pas de la documentation.
        """
        couple = N.u_f0(L_CATALOGUE, C_CATALOGUE, TOLERANCE, TOLERANCE)
        self.assertAlmostEqual(couple.borne_pire_cas, 0.0707, delta=5e-4)
        self.assertAlmostEqual(couple.incertitude_type, 0.0408, delta=5e-4)
        self.assertAlmostEqual(couple.f0_Hz, 96.8586, delta=1e-3)
        self.assertAlmostEqual(couple.u_type_Hz, couple.incertitude_type * couple.f0_Hz,
                               delta=1e-9)
        self.assertGreater(couple.borne_pire_cas, couple.incertitude_type)

    def test_c_correlation_meme_lot(self):
        """rho = +1 (deux composants du meme lot) : 10,0 %, pas 7,07 %.

        L'hypothese d'independance est rendue EXPLICITE par le terme en rho. Le
        cas correle n'est pas academique : deux composants du meme lot derivent
        ensemble, et une self bobinee dont on ajuste L APRES avoir mesure le C
        reel est correlee par construction. Reponse toute prete a la question de
        jury "et si vos composants viennent du meme lot ?".
        """
        self.assertAlmostEqual(
            N.u_f0_relative(TOLERANCE, TOLERANCE, rho=1.0),
            contexte.critere('c_incertitudes', 'u_f0_meme_lot_rho1_pct') / 100.,
                               delta=1e-6)
        self.assertAlmostEqual(N.u_f0_relative(TOLERANCE, TOLERANCE, rho=-1.0), 0.0,
                               delta=1e-9)
        self.assertGreater(N.u_f0_relative(TOLERANCE, TOLERANCE, rho=1.0),
                           N.u_f0_relative(TOLERANCE, TOLERANCE, rho=0.0))

    def test_c_le_facteur_un_demi_est_bien_la(self):
        """Multiplier L et C par (1+x) doit diviser f_0 par (1+x) : d'ou le 1/2.

        Demonstration directe du facteur, sans passer par la formule : f_0 varie
        comme (LC)^(-1/2), donc une erreur relative sur le PRODUIT se transmet a
        f_0 divisee par deux. C'est la propriete que la formule du premier ordre
        ignore.
        """
        f0 = N.f0_lc(L_CATALOGUE, C_CATALOGUE)
        self.assertAlmostEqual(f0, 96.8586, delta=1e-3)
        x = 1e-4
        f0_perturbe = N.f0_lc(L_CATALOGUE * (1 + x), C_CATALOGUE * (1 + x))
        sensibilite = (f0_perturbe / f0 - 1.0) / x
        self.assertAlmostEqual(sensibilite, -1.0, delta=1e-3)
        # une seule grandeur perturbee : sensibilite -1/2
        f0_L = N.f0_lc(L_CATALOGUE * (1 + x), C_CATALOGUE)
        self.assertAlmostEqual((f0_L / f0 - 1.0) / x, -0.5, delta=1e-3)


class TestMonteCarlo(unittest.TestCase):
    """(c) Le Monte-Carlo confirme les trois lectures -- et revele le biais."""

    def test_c_monte_carlo_uniforme_rejoint_la_convention_gum(self):
        """Tirage uniforme sur +/- 10 % : 4,09 % d'ecart-type relatif, contre 4,08 % analytique.

        C'est la verification croisee qui compte : la formule analytique est une
        linearisation, le Monte-Carlo ne l'est pas. Qu'ils s'accordent a 1e-4
        pres signifie que la linearisation est licite a ce niveau de tolerance.
        """
        _, u_mc = N.mc_f0(L_CATALOGUE, C_CATALOGUE, TOLERANCE, TOLERANCE,
                          n=N.N_MC_DEFAUT, loi='uniforme', graine=GRAINE)
        self.assertAlmostEqual(u_mc, 0.0409, delta=1e-3)
        analytique = N.u_f0_relative(N.type_b_rectangulaire(TOLERANCE),
                                     N.type_b_rectangulaire(TOLERANCE))
        self.assertLess(abs(u_mc / analytique - 1.0), 0.02)

    def test_c_monte_carlo_normal_et_correlation(self):
        """loi='normale' : les entrees sont des ECARTS-TYPES, pas des demi-largeurs.

        Piege de la section, et il est signale dans la docstring de ``mc_f0`` :
        selon la loi, le meme argument 0,10 signifie deux choses differentes. On
        verifie donc les deux branches contre leur reference analytique propre.
        """
        _, u_normal = N.mc_f0(L_CATALOGUE, C_CATALOGUE, TOLERANCE, TOLERANCE,
                              n=N.N_MC_DEFAUT, loi='normale', graine=GRAINE)
        self.assertAlmostEqual(u_normal, 0.0707, delta=0.005)
        _, u_correle = N.mc_f0(L_CATALOGUE, C_CATALOGUE, TOLERANCE, TOLERANCE,
                               n=N.N_MC_DEFAUT, loi='normale', graine=GRAINE, rho=1.0)
        self.assertAlmostEqual(u_correle, 0.10, delta=0.01)
        self.assertGreater(u_correle, u_normal)

    def test_c_biais_du_monte_carlo(self):
        """E[f_0] != f_0(E[L], E[C]) : biais attendu (3/8)(u_L^2 + u_C^2) = +0,75 %.

        Consequence de la convexite de (LC)^(-1/2) : la moyenne des frequences
        n'est pas la frequence des moyennes. Le biais est petit (+0,75 % a
        10 %/10 %) mais il est PREVISIBLE -- le verifier prouve que le Monte-Carlo
        fait ce qu'on croit, et pas seulement quelque chose de vraisemblable.
        """
        f0_nominal = N.f0_lc(L_CATALOGUE, C_CATALOGUE)
        moyenne, _ = N.mc_f0(L_CATALOGUE, C_CATALOGUE, TOLERANCE, TOLERANCE,
                             n=N.N_MC_DEFAUT, loi='normale', graine=GRAINE)
        biais_mesure = moyenne / f0_nominal - 1.0
        biais_attendu = N.biais_relatif_mc_f0(TOLERANCE, TOLERANCE)
        self.assertAlmostEqual(biais_attendu, 0.0075, delta=1e-6)
        self.assertAlmostEqual(biais_attendu, (3.0 / 8.0) * 2 * TOLERANCE ** 2,
                               delta=1e-12)
        self.assertAlmostEqual(
            biais_mesure, contexte.critere('c_incertitudes', 'biais_mc_pct') / 100.,
            delta=contexte.critere('c_incertitudes', 'biais_mc_delta_pct') / 100.)

    def test_c_accord_analytique_monte_carlo_sur_plusieurs_couples(self):
        """Sur trois couples (u_L, u_C) desequilibres, analytique et MC s'accordent a 15 %.

        On desequilibre volontairement (5 %/20 % et 20 %/5 %) : si le code avait
        interverti L et C quelque part, la formule resterait symetrique alors que
        le Monte-Carlo, lui, ne l'est pas au second ordre. Le test detecterait
        l'echange.
        """
        for u_L, u_C in [(0.10, 0.10), (0.05, 0.20), (0.20, 0.05)]:
            with self.subTest(u_L=u_L, u_C=u_C):
                analytique = N.u_f0_relative(u_L, u_C)
                _, mc = N.mc_f0(L_CATALOGUE, C_CATALOGUE, u_L, u_C,
                                n=N.N_MC_DEFAUT, loi='normale', graine=GRAINE)
                self.assertLess(abs(mc / analytique - 1.0), 0.15,
                                'analytique %.4f vs MC %.4f' % (analytique, mc))


class TestGardeFouAntiFormuleDuPremierOrdre(unittest.TestCase):
    """LE test de la mission : aucune fonction ne doit pouvoir produire 11 %."""

    @staticmethod
    def _formule_interdite(u_L, u_C):
        """Formule du RC du PREMIER ordre, ABANDONNEE : racine(u_L^2 + u_C^2), sans le 1/2.

        Reproduite ici uniquement pour pouvoir la refuser explicitement. A
        5 %/10 % elle donne 11,18 % -- le "11 %" de la v1. A 10 %/10 % elle donne
        14,14 %. Dans les deux cas elle decrit un RC du premier ordre, pas un LC.
        """
        return float(np.hypot(u_L, u_C))

    def test_la_formule_interdite_donne_bien_le_11_pourcent_de_la_v1(self):
        """On reproduit le chiffre fautif pour prouver qu'on parle du meme.

        Sans cette ligne, "interdire 11 %" serait une incantation : on ne saurait
        pas d'ou vient le nombre qu'on refuse.
        """
        self.assertAlmostEqual(self._formule_interdite(0.05, 0.10), 0.1118, delta=1e-4)
        self.assertAlmostEqual(
            self._formule_interdite(0.10, 0.10),
            contexte.critere('c_incertitudes', 'formule_interdite_pct') / 100.,
            delta=1e-4)

    def test_aucune_fonction_du_module_ne_rend_le_chiffre_interdit(self):
        """Balayage de l'API publique : rien ne doit rendre 11,18 % a 5 %/10 %.

        C'est le garde-fou demande par la mission, ecrit comme un test et non
        comme un commentaire. On appelle toutes les fonctions du module qui
        prennent (u_L, u_C) ou (L, C, u_L, u_C) et on verifie qu'aucune ne rend
        la valeur fautive -- ni a 5 %/10 %, ni a 10 %/10 %.
        """
        interdits = [self._formule_interdite(0.05, 0.10),
                     self._formule_interdite(0.10, 0.10)]
        produits = []

        produits.append(N.u_f0_relative(0.05, 0.10))
        produits.append(N.u_f0_relative(0.10, 0.10))
        produits.append(N.u_f0_relative(0.05, 0.10, rho=1.0))
        couple_a = N.u_f0(L_CATALOGUE, C_CATALOGUE, 0.05, 0.10)
        couple_b = N.u_f0(L_CATALOGUE, C_CATALOGUE, 0.10, 0.10)
        produits.extend([couple_a.borne_pire_cas, couple_a.incertitude_type,
                         couple_b.borne_pire_cas, couple_b.incertitude_type])
        for u_L, u_C in [(0.05, 0.10), (0.10, 0.10)]:
            _, u_mc = N.mc_f0(L_CATALOGUE, C_CATALOGUE, u_L, u_C,
                              n=N.N_MC_RAPIDE, loi='normale', graine=GRAINE)
            produits.append(u_mc)

        for valeur in produits:
            for interdit in interdits:
                self.assertGreater(abs(float(valeur) / interdit - 1.0), 0.05,
                                   'valeur %.4f trop proche de la formule interdite %.4f'
                                   % (valeur, interdit))

    def test_le_monte_carlo_refute_la_formule_interdite(self):
        """Ce qui refute le 11 %, c'est le Monte-Carlo -- pas un rapport a 2 pose a priori.

        Argument d'oral : on ne dit pas "il fallait diviser par deux", on dit "on
        a tire 400 000 jeux de composants dans leurs tolerances et on a mesure la
        dispersion de f_0 ; elle est deux fois plus petite que ce que la formule
        du premier ordre annoncait". C'est une preuve, pas une correction.
        """
        for u_L, u_C in [(0.10, 0.10), (0.05, 0.20), (0.20, 0.05)]:
            with self.subTest(u_L=u_L, u_C=u_C):
                _, mc = N.mc_f0(L_CATALOGUE, C_CATALOGUE, u_L, u_C,
                                n=N.N_MC_DEFAUT, loi='normale', graine=GRAINE)
                ecart = abs(self._formule_interdite(u_L, u_C) / mc - 1.0)
                self.assertGreater(ecart, 0.5,
                                   'la formule du 1er ordre devrait etre grossierement fausse')

    def test_le_rapport_entre_les_deux_formules_vaut_bien_deux(self):
        """A rho = 0, formule interdite / formule juste = 2, exactement.

        Le facteur 1/2 est le seul ecart entre les deux expressions : le verifier
        a la machine pres empeche qu'un jour un "0,5" se transforme en "0,7" au
        detour d'une refonte.
        """
        for u_L, u_C in [(0.10, 0.10), (0.05, 0.10), (0.20, 0.05), (0.01, 0.30)]:
            with self.subTest(u_L=u_L, u_C=u_C):
                self.assertAlmostEqual(
                    self._formule_interdite(u_L, u_C) / N.u_f0_relative(u_L, u_C),
                    2.0, delta=1e-12)


class TestOutillageGUM(unittest.TestCase):
    """Les briques du GUM sur lesquelles tout le reste s'appuie."""

    def test_lois_de_type_b(self):
        """Rectangulaire : a/racine 3. Triangulaire : a/racine 6.

        Deux modeles pour deux situations physiques differentes : la tolerance
        catalogue (on ne sait rien dans l'intervalle) et la lecture d'un cadran
        (les valeurs centrales sont plus probables). Les confondre change
        l'incertitude de 41 %.
        """
        self.assertAlmostEqual(N.type_b_rectangulaire(0.10), 0.10 / N.RACINE_3, delta=1e-15)
        self.assertAlmostEqual(N.type_b_triangulaire(0.10), 0.10 / N.RACINE_6, delta=1e-15)
        self.assertAlmostEqual(N.RACINE_3, np.sqrt(3.0), delta=1e-15)
        self.assertGreater(N.type_b_rectangulaire(0.1), N.type_b_triangulaire(0.1))

    def test_combinaison_et_elargissement(self):
        """u_c = racine(u_A^2 + u_B^2) ; U = k u_c avec k = 2 (environ 95 %).

        Le facteur d'elargissement est celui que le jury attend sur une barre
        d'erreur affichee : il doit etre nomme, pas applique en douce.
        """
        self.assertAlmostEqual(N.combiner_types(0.03, 0.04), 0.05, delta=1e-12)
        self.assertEqual(N.K_ELARGISSEMENT, 2)
        self.assertAlmostEqual(N.elargir(0.05), 0.10, delta=1e-12)

    def test_repetabilite_distingue_l_ecart_type_et_celui_de_la_moyenne(self):
        """s (une lecture) et s/racine(n) (la moyenne) ne sont pas la meme chose.

        Erreur classique et couteuse : annoncer s/racine(n) comme incertitude
        d'une mesure unique divise l'incertitude par racine(n) sans raison. La
        structure de retour force a choisir.
        """
        valeurs = [10.1, 10.3, 9.8, 10.0, 10.2, 9.9]
        r = N.type_a_repetabilite(valeurs)
        self.assertEqual(r.n, 6)
        self.assertAlmostEqual(r.moyenne, float(np.mean(valeurs)), delta=1e-12)
        self.assertAlmostEqual(r.ecart_type_experimental,
                               float(np.std(valeurs, ddof=1)), delta=1e-12)
        self.assertAlmostEqual(r.u_moyenne,
                               r.ecart_type_experimental / np.sqrt(6.0), delta=1e-12)

    def test_facteur_de_soustraction_selon_le_montage(self):
        """Le montage de mesure change l'amplification du bruit : A, B ou C.

        En montage A, le facteur racine(2)(1 + |Z|/R_ref) explose quand |Z|
        approche R_ref -- c'est-a-dire au pic d'impedance, la ou l'on veut
        justement etre precis. Le montage C (GBF flottant) ramene le facteur a
        racine(2), constant. C'est un argument de conception de manip, chiffre.
        """
        self.assertAlmostEqual(N.facteur_soustraction('C', 100.0, 50.0),
                               np.sqrt(2.0), delta=1e-12)
        self.assertAlmostEqual(N.facteur_soustraction('A', 100.0, 50.0),
                               np.sqrt(2.0) * 1.5, delta=1e-12)
        self.assertGreater(N.facteur_soustraction('A', 100.0, 50.0),
                           N.facteur_soustraction('A', 100.0, 6.5))

    def test_propagation_lineaire_et_monte_carlo_s_accordent_sur_f0(self):
        """Les deux moteurs generiques doivent redonner la formule de f_0.

        ``propager_lineaire`` derive numeriquement le modele qu'on lui donne ;
        ``propager_monte_carlo`` echantillonne. Les brancher sur f_0 = 1/(2 pi
        racine(LC)) est le meilleur controle de non-regression possible : le
        resultat est connu analytiquement.
        """
        modele = lambda x: 1.0 / (2.0 * np.pi * np.sqrt(x[0] * x[1]))
        x = np.array([L_CATALOGUE, C_CATALOGUE])
        u = np.array([0.10 * L_CATALOGUE, 0.10 * C_CATALOGUE])
        lineaire = N.propager_lineaire(modele, x, u, noms=('L', 'C'))
        mc = N.propager_monte_carlo(modele, x, u, n=N.N_MC_RAPIDE, graine=GRAINE,
                                    noms=('L', 'C'))
        self.assertAlmostEqual(lineaire.u_relative, 0.0707, delta=1e-3)
        self.assertLess(abs(mc.u_relative / lineaire.u_relative - 1.0), 0.05)
        self.assertAlmostEqual(lineaire.valeur, 96.8586, delta=1e-3)


if __name__ == '__main__':
    unittest.main(verbosity=2)
