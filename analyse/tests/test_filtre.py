"""Mission n. 4 -- reperes frequentiels du filtre LC (module ``filtre``).

CE QUE CE FICHIER PROTEGE
-------------------------
Le TIPE repose sur une DEFINITION UNIQUE de f_c : la frequence de CROISEMENT des
deux voies, celle ou |H_PB| = |H_PH| (§ 04.1). Tout le reste -- le pole, les deux
reperes a -3 dB -- ce sont des REPERES nommes, pas la frequence de coupure. Le
danger est de les confondre, parce qu'ils different de 6 % sur le filtre catalogue,
c'est-a-dire de l'ordre de grandeur de l'incertitude elle-meme : une confusion de
vocabulaire devient alors indiscernable d'un resultat.

Chiffres de controle, sur le filtre catalogue 18 mH / 150 uF charge par 8 ohm
resistifs (valeurs E12 leguees par la v1) :

    pole f0 = 1/(2 pi racine(LC))       = 96,86 Hz
    Q = R racine(C/L)                   = 0,7303
    repere -3 dB mi-puissance (-3,0103 dB, convention REW, DEFAUT du projet) :
        f3_PB = 99,93 Hz   f3_PH = 93,88 Hz
    repere -3 dB seuil litteral (-3,000 dB) :
        f3_PB = 99,82 Hz   f3_PH = 93,99 Hz

L'ecart entre les deux conventions vaut 0,11 % : negligeable pour les criteres,
mais il doit etre un PARAMETRE NOMME et jamais une constante cachee, sinon deux
modules du projet rapportent des chiffres differents sans qu'on sache pourquoi.

Le controle f3_PB x f3_PH = f0^2 est la signature algebrique du couple
passe-bas / passe-haut du meme reseau : il tient EXACTEMENT, pour les deux
conventions, et il attrape toute erreur de signe ou d'inversion dans la forme
fermee.

Enfin, decision D2 (13/09/2026) : la cible de sommation est VOLONTAIREMENT
reportee apres la phase 1. Elle doit donc etre un parametre partout, jamais une
constante -- ce fichier verifie que les trois cibles sont evaluables.
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

L_CATALOGUE = 18e-3
C_CATALOGUE = 150e-6
R = contexte.R_NOM


class TestPoleEtFacteurDeQualite(unittest.TestCase):
    """Le pole et Q sont les deux grandeurs directement fonctions de L et C."""

    def test_pole_du_filtre_catalogue(self):
        """f0 = 1/(2 pi racine(LC)) = 96,8586 Hz pour 18 mH / 150 uF.

        Ce n'est PAS 100 Hz : la normalisation E12 du condensateur (141 uF
        theoriques arrondis a 150 uF) deplace le pole de 3,1 %. C'est le cout de
        la contrainte de catalogue, et il doit rester visible -- pas arrondi a
        "environ 100 Hz" dans un coin de rapport.
        """
        f0, Q, K = F.pole_et_q(L_CATALOGUE, C_CATALOGUE, R)
        self.assertAlmostEqual(f0, 96.8586, delta=0.001)
        attendu = 1.0 / (2.0 * np.pi * np.sqrt(L_CATALOGUE * C_CATALOGUE))
        self.assertAlmostEqual(f0, attendu, delta=1e-9 * attendu)

    def test_facteur_de_qualite_du_filtre_catalogue(self):
        """Q = R racine(C/L) = 0,7303, tout proche du Butterworth 1/racine(2) = 0,7071.

        Le Butterworth impose Q = 0,707 ; le couple E12 retenu donne 0,730, soit
        3,3 % de trop. Consequence physique : une legere bosse a la sommation au
        lieu d'une somme plate. C'est chiffre, pas subi.
        """
        f0, Q, K = F.pole_et_q(L_CATALOGUE, C_CATALOGUE, R)
        self.assertAlmostEqual(Q, 0.7303, delta=1e-4)
        self.assertAlmostEqual(Q, R * np.sqrt(C_CATALOGUE / L_CATALOGUE), delta=1e-12)
        self.assertAlmostEqual(K, 1.0, delta=1e-12)

    def test_le_dcr_degrade_le_facteur_de_qualite_et_le_gain(self):
        """Une DCR de 1 ohm face a 8 ohm : ~11 % de la puissance en chaleur, ~ -1 dB.

        La resistance serie de la self n'est pas un detail de second ordre : elle
        dissipe, et elle modifie l'amortissement du grave. En v2 c'est un element
        CENTRAL de la fonction de cout, donc le code doit en tenir compte dans le
        pole et le gain -- pas seulement dans un bilan energetique a part.
        """
        f0_ideal, Q_ideal, K_ideal = F.pole_et_q(L_CATALOGUE, C_CATALOGUE, R, r=0.0)
        f0_reel, Q_reel, K_reel = F.pole_et_q(L_CATALOGUE, C_CATALOGUE, R, r=1.0)
        self.assertLess(K_reel, K_ideal, 'la DCR doit faire perdre du gain')
        self.assertAlmostEqual(20.0 * np.log10(K_reel), -1.02, delta=0.05)
        self.assertNotAlmostEqual(Q_reel, Q_ideal, places=3)


class TestReperes3dB(unittest.TestCase):
    """Les reperes a -3 dB : deux conventions, un parametre nomme, jamais une constante."""

    def test_convention_mi_puissance_par_defaut(self):
        """Par defaut, le seuil est -3,0103 dB (mi-puissance, convention de REW).

        Le projet compare ses calculs a des mesures faites sous REW. Si le code
        utilisait le seuil litteral -3,000 dB par defaut, chaque comparaison
        porterait un ecart systematique de 0,11 % qu'il faudrait expliquer a
        chaque figure.
        """
        self.assertAlmostEqual(F.SEUIL_MI_PUISSANCE, 3.0103, delta=1e-6)
        self.assertAlmostEqual(F.SEUIL_MI_PUISSANCE,
                               10.0 * np.log10(2.0), delta=2e-5)
        import inspect
        defaut = inspect.signature(F.reperes_3db_ideaux).parameters['seuil'].default
        self.assertAlmostEqual(defaut, F.SEUIL_MI_PUISSANCE, delta=1e-9)
        defaut_mesure = inspect.signature(F.repere_3db).parameters['seuil'].default
        self.assertAlmostEqual(defaut_mesure, F.SEUIL_MI_PUISSANCE, delta=1e-9)

    def test_reperes_mi_puissance_du_filtre_catalogue(self):
        """Mi-puissance : f3_PB = 99,93 Hz et f3_PH = 93,88 Hz.

        Trois frequences differentes pour un seul filtre (93,88 / 96,86 / 99,93),
        soit 6 % entre extremes. Nommer chacune est la seule facon de ne pas se
        contredire d'une diapositive a l'autre.
        """
        reperes = F.reperes_3db_ideaux(L_CATALOGUE, C_CATALOGUE, R)
        self.assertAlmostEqual(reperes['f3_pb'], 99.93, delta=0.01)
        self.assertAlmostEqual(reperes['f3_ph'], 93.88, delta=0.01)

    def test_reperes_seuil_litteral_du_filtre_catalogue(self):
        """Seuil litteral -3,000 dB : f3_PB = 99,82 Hz et f3_PH = 93,99 Hz.

        Meme filtre, autre convention, 0,11 % d'ecart. Ce test fige les DEUX
        jeux de chiffres pour que personne n'ait a deviner, en relisant une note,
        laquelle des deux conventions a produit un nombre.
        """
        reperes = F.reperes_3db_ideaux(L_CATALOGUE, C_CATALOGUE, R,
                                       seuil=F.SEUIL_LITTERAL)
        self.assertAlmostEqual(reperes['f3_pb'], 99.82, delta=0.01)
        self.assertAlmostEqual(reperes['f3_ph'], 93.99, delta=0.01)
        mi_puissance = F.reperes_3db_ideaux(L_CATALOGUE, C_CATALOGUE, R)
        ecart = abs(reperes['f3_pb'] / mi_puissance['f3_pb'] - 1.0)
        self.assertAlmostEqual(100 * ecart, 0.11, delta=0.02)

    def test_produit_des_reperes_egale_le_carre_du_pole(self):
        """Controle algebrique : f3_PB x f3_PH = f0^2, EXACTEMENT, pour les deux seuils.

        Le passe-bas et le passe-haut du meme reseau LC sont images l'un de
        l'autre par f -> f0^2/f. Leurs reperes a -3 dB sont donc symetriques en
        echelle logarithmique autour du pole. Cette identite ne depend ni de Q ni
        du seuil choisi : c'est le controle le plus severe qu'on puisse faire sur
        une forme fermee, et il attrape toute inversion de signe.
        """
        f0 = F.pole_et_q(L_CATALOGUE, C_CATALOGUE, R)[0]
        for seuil in (F.SEUIL_MI_PUISSANCE, F.SEUIL_LITTERAL, 6.0):
            with self.subTest(seuil=seuil):
                reperes = F.reperes_3db_ideaux(L_CATALOGUE, C_CATALOGUE, R, seuil=seuil)
                produit = reperes['f3_pb'] * reperes['f3_ph']
                self.assertAlmostEqual(produit / f0 ** 2, 1.0, delta=1e-9)

    def test_repere_mesure_sur_courbe_egale_la_forme_fermee(self):
        """``repere_3db`` (sur tableau) doit retrouver la forme fermee a 0,1 % pres.

        Deux chemins independants vers le meme nombre : l'un analytique, l'autre
        par recherche sur la reponse effectivement calculee. S'ils divergent,
        c'est que H_pb / H_ph ne sont pas le reseau dont la forme fermee parle.
        """
        f0 = F.pole_et_q(L_CATALOGUE, C_CATALOGUE, R)[0]
        f = np.geomspace(0.2 * f0, 5.0 * f0, 20001)
        Z = contexte.charge_resistive(f)
        H_pb = F.H_pb(f, L_CATALOGUE, C_CATALOGUE, Z)
        H_ph = F.H_ph(f, C_CATALOGUE, L_CATALOGUE, Z)
        reperes = F.reperes_3db_ideaux(L_CATALOGUE, C_CATALOGUE, R)
        mesure_pb = F.repere_3db(f, H_pb)
        mesure_ph = F.repere_3db(f, H_ph)
        self.assertAlmostEqual(mesure_pb / reperes['f3_pb'], 1.0, delta=1e-3)
        self.assertAlmostEqual(mesure_ph / reperes['f3_ph'], 1.0, delta=1e-3)


class TestFrequenceDeCroisement(unittest.TestCase):
    """f_c = |H_PB| = |H_PH| : LA definition du TIPE (§ 04.1), et rien d'autre."""

    def test_croisement_du_filtre_catalogue_tombe_sur_le_pole(self):
        """Les deux voies ayant les MEMES L et C, elles se croisent exactement au pole.

        Cas particulier instructif : ici f_c et f0 coincident, ce qui pourrait
        faire croire qu'ils sont synonymes. Ils ne le sont pas -- le test suivant
        le montre en desappariant les voies.
        """
        f = np.geomspace(20.0, 500.0, 20001)
        Z = contexte.charge_resistive(f)
        H_pb = F.H_pb(f, L_CATALOGUE, C_CATALOGUE, Z)
        H_ph = F.H_ph(f, C_CATALOGUE, L_CATALOGUE, Z)
        f0 = F.pole_et_q(L_CATALOGUE, C_CATALOGUE, R)[0]
        f_x = F.frequence_croisement(f, H_pb, H_ph)
        self.assertAlmostEqual(f_x / f0, 1.0, delta=1e-4)

    def test_croisement_et_pole_sont_deux_grandeurs_distinctes(self):
        """Voies desappariees : f_c n'est NI le pole du passe-bas NI celui du passe-haut.

        C'est le coeur de la convention de vocabulaire. Avec un passe-haut a
        100 uF / 18 mH devant le passe-bas catalogue, le croisement tombe a
        116,5 Hz : 20 % au-dessus du pole passe-bas (96,86 Hz) et encore 1,8 %
        sous le pole passe-haut (118,6 Hz). Aucun des deux poles n'est f_c. Or
        c'est exactement ce que l'optimiseur E12 a le droit de produire -- choisir
        un voisin different d'une voie a l'autre. Si le code confondait les deux
        notions, ce cas parfaitement legitime rendrait un chiffre faux sans aucun
        signal.
        """
        f = np.geomspace(20.0, 500.0, 20001)
        Z = contexte.charge_resistive(f)
        H_pb = F.H_pb(f, L_CATALOGUE, C_CATALOGUE, Z)
        H_ph = F.H_ph(f, 100e-6, 18e-3, Z)  # voie haute desappariee
        f_x = F.frequence_croisement(f, H_pb, H_ph)
        f0_pb = F.pole_et_q(L_CATALOGUE, C_CATALOGUE, R)[0]
        f0_ph = F.pole_et_q(18e-3, 100e-6, R)[0]
        self.assertAlmostEqual(f_x, 116.55, delta=0.1)
        self.assertGreater(abs(f_x / f0_pb - 1.0), 0.05, 'f_c confondu avec le pole PB')
        self.assertGreater(abs(f_x / f0_ph - 1.0), 0.01, 'f_c confondu avec le pole PH')

    def test_le_croisement_bouge_peu_sous_un_ecart_e12_d_une_seule_voie(self):
        """Passer la self du passe-haut de 18 a 15 mH ne deplace f_c que de 0,47 %.

        Fait a connaitre avant de lire un classement d'optimisation : le
        croisement est PEU sensible a la self de shunt du passe-haut. C'est
        pourquoi le deuxieme meilleur design E12 differe souvent du premier par
        cette seule valeur, et pourquoi l'optimum est plat. Ce test fige le
        chiffre pour que l'argument soit defendable a l'oral plutot qu'affirme.
        """
        f = np.geomspace(20.0, 500.0, 20001)
        Z = contexte.charge_resistive(f)
        H_pb = F.H_pb(f, L_CATALOGUE, C_CATALOGUE, Z)
        f_x = F.frequence_croisement(f, H_pb, F.H_ph(f, 150e-6, 15e-3, Z))
        f0_pb = F.pole_et_q(L_CATALOGUE, C_CATALOGUE, R)[0]
        self.assertAlmostEqual(100 * (f_x / f0_pb - 1.0), 0.47, delta=0.05)

    def test_le_croisement_du_butterworth_canonique_vaut_bien_100_Hz(self):
        """Composants analytiques : le croisement doit tomber a 100,000 Hz.

        C'est la cible du projet. Sur charge resistive pure et sans contrainte de
        catalogue, le filtre canonique croise exactement a f_cible -- toute
        derive signale une erreur de definition, pas une tolerance de composant.
        """
        f = np.geomspace(20.0, 500.0, 40001)
        Z = contexte.charge_resistive(f)
        for nom in ('butterworth', 'lr2'):
            with self.subTest(cible=nom):
                L, C = F.composants_canoniques(nom, f0_cible=100.0, R=R)
                f_x = F.frequence_croisement(f, F.H_pb(f, L, C, Z), F.H_ph(f, C, L, Z))
                self.assertAlmostEqual(f_x, 100.0, delta=0.02)


class TestCiblesParametrables(unittest.TestCase):
    """Decision D2 : la cible de sommation est un PARAMETRE, jamais une constante."""

    def test_les_trois_cibles_sont_evaluables(self):
        """'butterworth', 'lr2' et 'plate' doivent toutes trois repondre.

        La cible est volontairement reportee apres la phase 1 (decision D2 du
        13/09/2026). Tant qu'elle n'est pas gelee, le code doit pouvoir l'evaluer
        sur les trois options -- sinon le gel se fera par defaut, c'est-a-dire
        par omission.
        """
        f = F.grille_critere()
        self.assertEqual(tuple(F.CIBLES), ('butterworth', 'lr2', 'plate'))
        for nom in F.CIBLES:
            with self.subTest(cible=nom):
                Hc_pb, Hc_ph = F.cible(f, nom, f0_cible=100.0)
                self.assertEqual(np.shape(Hc_pb), f.shape)
                self.assertEqual(np.shape(Hc_ph), f.shape)
                self.assertTrue(np.all(np.isfinite(Hc_pb)))

    def test_composants_canoniques_butterworth_et_lr2(self):
        """Butterworth : 18,0063 mH / 140,674 uF. Linkwitz-Riley 2 : 25,4648 mH / 99,472 uF.

        Ces deux couples sont les REFERENCES ANALYTIQUES de la porte de
        validation : sur 8 ohm resistifs, l'optimiseur continu doit y retomber.
        Les figer ici evite de dependre de l'optimiseur pour savoir ce qu'on
        attend de lui.
        """
        L_bw, C_bw = F.composants_canoniques('butterworth', 100.0, R)
        self.assertAlmostEqual(L_bw, 0.018006326, delta=1e-9)
        self.assertAlmostEqual(C_bw, 140.674424e-6, delta=1e-12)
        self.assertAlmostEqual(L_bw, np.sqrt(2.0) * R / (2 * np.pi * 100.0), delta=1e-12)

        L_lr, C_lr = F.composants_canoniques('lr2', 100.0, R)
        self.assertAlmostEqual(L_lr, 0.025464791, delta=1e-9)
        self.assertAlmostEqual(C_lr, 99.471839e-6, delta=1e-12)
        self.assertAlmostEqual(R * np.sqrt(C_lr / L_lr), 0.5, delta=1e-6,
                               msg='Linkwitz-Riley 2 impose Q = 1/2')
        self.assertAlmostEqual(R * np.sqrt(C_bw / L_bw), 1 / np.sqrt(2.0), delta=1e-6,
                               msg='Butterworth 2 impose Q = 1/racine(2)')

    def test_inversion_de_polarite_obligatoire_au_second_ordre(self):
        """2e ordre : sans inversion d'une voie, la somme fait un TROU profond a f_c.

        Point scientifique releve par le professeur et jamais perime : au second
        ordre les deux voies sont en opposition de phase au croisement. En
        polarite normale la somme s'effondre ; en polarite inversee elle passe a
        une bosse de +3 dB. Ce n'est pas un detail de cablage, c'est la difference
        entre une enceinte qui fonctionne et une enceinte qui n'a plus de grave
        au raccord.
        """
        f = np.geomspace(40.0, 250.0, 2001)
        Z = contexte.charge_resistive(f)
        L, C = F.composants_canoniques('butterworth', 100.0, R)
        H_pb, H_ph = F.H_pb(f, L, C, Z), F.H_ph(f, C, L, Z)
        somme_normale = np.abs(F.sommer(f, H_pb, H_ph, pol=+1))
        somme_inversee = np.abs(F.sommer(f, H_pb, H_ph, pol=-1))
        i = int(np.argmin(np.abs(f - 100.0)))
        creux_db = 20.0 * np.log10(somme_normale[i])
        bosse_db = 20.0 * np.log10(somme_inversee[i])
        self.assertLess(creux_db, -20.0,
                        'sans inversion la somme devrait s effondrer a f_c')
        self.assertAlmostEqual(bosse_db, 3.0, delta=0.3)


class TestContraintesElectriques(unittest.TestCase):
    """Ce que le filtre fait subir aux composants -- et a l'amplificateur."""

    def test_tension_crete_de_l_amplificateur(self):
        """350 W sur 8 ohm => 74,83 V crete : c'est la tension a tenir, pas 50 V.

        Un condensateur choisi sur la tension EFFICACE (52,9 V) serait sous-calibre
        de 41 %. Le calibre s'achete une fois ; se tromper coute le composant.
        """
        self.assertAlmostEqual(F.tension_crete_amplificateur(350.0, 8.0), 74.833,
                               delta=1e-3)
        self.assertAlmostEqual(F.tension_crete_amplificateur(350.0, 8.0),
                               np.sqrt(2.0 * 350.0 * 8.0), delta=1e-9)

    def test_impedance_d_entree_reste_au_dessus_du_minimum_de_l_ampli(self):
        """Le E-800 ne descend pas sous 4 ohm : le filtre catalogue doit le respecter.

        Un filtre qui optimise parfaitement la somme mais presente 2 ohm a
        l'amplificateur n'est pas une solution, c'est une panne differee. La
        contrainte appartient donc au probleme d'optimisation, pas au commentaire.
        """
        f = F.grille_critere()
        Z = contexte.charge_resistive(f)
        V_C, I_L, Zin_min, ok = F.verifier_contraintes(contexte.DESIGN_CATALOGUE,
                                                       F.P_NOM_E800, Z, f=f)
        self.assertTrue(ok)
        self.assertGreater(Zin_min, F.ZIN_MIN_E800)
        self.assertIn('C1', V_C)
        self.assertIn('L1', I_L)
        self.assertLess(V_C['C1'], 2 * F.tension_crete_amplificateur())

    def test_pertes_joule_croissent_avec_la_dcr(self):
        """Sans DCR, zero watt dissipe ; avec 1 ohm, une fraction non negligeable.

        C'est le pont entre le filtre et le satellite "self optimale" : la DCR
        entre dans la fonction de cout par les watts qu'elle brule, et ces watts
        se calculent -- ils ne s'estiment pas.
        """
        f = F.grille_critere()
        Z = contexte.charge_resistive(f)
        sans = F.pertes_joule_dcr(f, contexte.DESIGN_CATALOGUE, Z, Z, P_ref=10.0)
        avec = F.pertes_joule_dcr(f, dict(contexte.DESIGN_CATALOGUE, r1=1.0, r2=1.0),
                                  Z, Z, P_ref=10.0)
        self.assertAlmostEqual(sans[0], 0.0, delta=1e-12)
        self.assertGreater(avec[0], 0.0)
        self.assertAlmostEqual(avec[0], avec[1] + avec[2], delta=1e-9)


if __name__ == '__main__':
    unittest.main(verbosity=2)
