"""Contrat inter-modules -- signatures GELEES du § 09.4 et conventions du projet.

CE QUE CE FICHIER PROTEGE
-------------------------
Les huit modules de ``analyse/`` ont ete ecrits en parallele contre un contrat
ecrit : les signatures du § 09.4. Un module qui renomme un argument ou en
change l'ordre ne casse rien chez lui -- il casse chez les autres, plus tard, et
souvent par un appel positionnel qui passe silencieusement la mauvaise valeur.
Ce fichier verifie le contrat lui-meme, pas la physique.

Trois familles de controles :

1. **Les signatures gelees**, argument par argument, dans l'ordre. ``Z_ts(f, Re,
   Le, Res, fs, Qms)`` : interchanger Res et fs ne leverait aucune exception et
   rendrait une impedance d'allure plausible.
2. **Les valeurs par defaut qui portent une decision.** Le seuil a -3 dB vaut
   3,0103 par defaut (convention REW) ; la cible de sommation est un parametre
   et non une constante (decision D2) ; ``rho=0`` rend explicite l'hypothese
   d'independance.
3. **Les conventions du projet** : fichiers UTF-8 en fins de ligne LF, sources
   sans accents (pour rester lisibles dans une console cp1252), jeux de valeurs
   typiques ETIQUETES comme n'etant pas des mesures.

Ce dernier point n'est pas cosmetique : le dossier ne contient AUCUNE mesure de
l'enceinte. Le seul rempart contre un ordre de grandeur cite un jour comme un
resultat, c'est que le source le dise a chaque occurrence.
"""

import inspect
import os
import re
import sys
import unittest

_ICI = os.path.dirname(os.path.abspath(__file__))
for _d in (_ICI, os.path.dirname(_ICI)):
    if _d not in sys.path:
        sys.path.insert(0, _d)

import numpy as np  # noqa: E402
import contexte  # noqa: E402
import filtre as F  # noqa: E402
import incertitudes as N  # noqa: E402
import energie as EN  # noqa: E402
import io_mesures as IO  # noqa: E402
import modele_hp as MH  # noqa: E402
import optim as O  # noqa: E402
import self_bobine as SB  # noqa: E402
import ts_fit as T  # noqa: E402

MODULES = {'modele_hp': MH, 'io_mesures': IO, 'ts_fit': T, 'filtre': F,
           'optim': O, 'self_bobine': SB, 'incertitudes': N, 'energie': EN}


# Bloc U+00C0..U+00FF : les lettres latines accentuees du Latin-1, moins les deux
# operateurs qui s'y sont glisses (multiplication U+00D7 et division U+00F7).
# Construit par code de caractere pour que CE fichier reste lui-meme en ASCII.
LETTRES_ACCENTUEES = ({chr(c) for c in range(0xC0, 0x100)}
                      - {chr(0xD7), chr(0xF7)})


def _encodable_cp1252(caractere):
    """Vrai si le caractere peut etre imprime dans une console Windows cp1252.

    C'est le critere qui a des consequences : un caractere hors cp1252 passe a
    ``print()`` leve UnicodeEncodeError et interrompt le script.
    """
    try:
        caractere.encode('cp1252')
    except UnicodeEncodeError:
        return False
    return True

# (module, fonction, arguments positionnels dans l'ORDRE gele)
SIGNATURES_GELEES = [
    (MH, 'Z_ts', ['f', 'Re', 'Le', 'Res', 'fs', 'Qms']),
    (MH, 'grille_log', ['f1', 'f2', 'n_par_octave', 'densifier']),
    (MH, 'zobel', ['Z', 'f', 'Rz', 'Cz']),
    (IO, 'lire_mesure', ['chemin']),
    (IO, 'ecrire_mesure', ['chemin', 'd', 'meta']),
    (IO, 'lire_rew', ['chemin']),
    (IO, 'lire_scope', ['chemin']),
    (IO, 'depouiller_scope', ['t', 'v1', 'v2', 'f0', 'R_ref', 'methode']),
    (T, 'init_depuis_courbe', ['f', 'mod', 'phi', 'Re0']),
    (T, 'residus_ts', ['theta', 'f', 'mod', 'phi', 'u_mod', 'u_phi']),
    (T, 'ajuster_ts', ['f', 'mod', 'phi', 'u_mod', 'u_phi', 'theta0', 'forcer_repli']),
    (F, 'H_pb', ['f', 'L', 'C', 'Z', 'r']),
    (F, 'H_ph', ['f', 'C', 'L', 'Z', 'r']),
    (F, 'cible', ['f', 'nom', 'f0_cible']),
    (F, 'verifier_contraintes', ['design', 'P_max', 'Z']),
    (F, 'exporter_netlist', ['design', 'Z_rlc', 'chemin']),
    (O, 'cout', ['p1', 'p2', 'f', 'Zs', 'Zm', 'H_ac_sub', 'H_ac_med', 'g_med',
                 'cible_nom', 'w', 'pol', 'dcr']),
    (O, 'enumere_e12', ['f', 'Zs', 'Zm', 'L_vals', 'C_vals']),
    (SB, 'L_wheeler', ['N', 'a', 'b', 'c']),
    (SB, 'dcr_de_L', ['L', 'd_fil', 'geometrie']),
    (SB, 'masse_cuivre', ['L', 'DCR']),
    (SB, 'brooks', ['L']),
    (SB, 'cout_self', ['L']),
    (N, 'u_f0_relative', ['uL_rel', 'uC_rel', 'rho']),
    (N, 'mc_f0', ['L', 'C', 'uL_rel', 'uC_rel', 'n', 'loi', 'graine', 'rho']),
    # Satellite ENERGIE (§ 06). Ces deux signatures sont gelees au tableau du
    # § 09.4 au meme titre que les autres ; le module manquait purement et
    # simplement jusqu'a la relecture du 2026-09-14, alors qu'un autre agent
    # ecrivant contre le contrat et faisant `import energie` aurait echoue.
    (EN, 'pertes_joule', ['design', 'Z', 'P_ref']),
    (EN, 'croisement', ['P_repos_actif', 'design', 'Z']),
]


class TestSignaturesGelees(unittest.TestCase):
    """§ 09.4 : ces signatures sont un contrat entre modules ecrits en parallele."""

    def test_les_signatures_gelees_sont_respectees_a_la_lettre(self):
        """Nom ET ordre des arguments positionnels, pour chaque signature gelee.

        L'ordre compte autant que le nom : ``Z_ts(f, Re, Le, Res, fs, Qms)``
        appelee avec Res et fs intervertis ne leve rien et rend une courbe
        d'allure vraisemblable. C'est le type d'erreur que seule une verification
        mecanique attrape.
        """
        for module, nom, attendus in SIGNATURES_GELEES:
            with self.subTest(fonction='%s.%s' % (module.__name__, nom)):
                self.assertTrue(hasattr(module, nom),
                                '%s.%s absente' % (module.__name__, nom))
                parametres = list(inspect.signature(getattr(module, nom)).parameters)
                self.assertEqual(parametres[:len(attendus)], attendus,
                                 'signature derivee : %r' % parametres)

    def test_les_retours_ont_la_forme_promise(self):
        """Chaque signature gelee promet une forme de retour : on la verifie.

        Une fonction qui rendrait un scalaire la ou le contrat promet un couple
        casserait ses appelants a la ligne suivante, loin de la cause.
        """
        f = MH.grille_log(20.0, 200.0, 12)
        Z = MH.Z_ts(f, *contexte.THETA_SYNTHETIQUE)
        self.assertEqual(np.shape(Z), f.shape)
        self.assertTrue(np.iscomplexobj(Z))

        Hc = F.cible(f, 'butterworth', 100.0)
        self.assertEqual(len(Hc), 2)

        contraintes = F.verifier_contraintes(contexte.DESIGN_CATALOGUE, 350.0,
                                             contexte.charge_resistive(f), f=f)
        self.assertEqual(len(contraintes), 4)
        self.assertIsInstance(contraintes[3], (bool, np.bool_))

        self.assertEqual(len(MH.zobel(Z, f, 8.0, 1e-5)), f.size)
        self.assertEqual(len(F.valeurs_zobel(6.5, 1.2e-3)), 2)
        self.assertEqual(len(SB.brooks(18e-3)['N'].shape), 0)

    def test_diffusion_des_fonctions_de_transfert(self):
        """H_pb / H_ph doivent diffuser (n,1) x (Nf,) -> (n,Nf).

        C'est ce qui permet a la fonction de cout d'evaluer 576 couples d'un seul
        coup au lieu de boucler. Sans cette propriete, l'enumeration des 331 776
        combinaisons passerait de deux secondes a plusieurs minutes.
        """
        f = F.grille_critere()
        Z = contexte.charge_resistive(f)
        L = np.array([[10e-3], [18e-3], [27e-3]])
        C = np.array([[100e-6], [150e-6], [220e-6]])
        H = F.H_pb(f, L, C, Z)
        self.assertEqual(np.shape(H), (3, f.size))
        ligne = F.H_pb(f, 18e-3, 150e-6, Z)
        np.testing.assert_allclose(H[1], ligne, rtol=1e-12)


class TestDefautsQuiPortentUneDecision(unittest.TestCase):
    """Certaines valeurs par defaut sont des decisions de projet, pas des commodites."""

    def test_le_seuil_3dB_par_defaut_est_la_convention_de_rew(self):
        """seuil=3.0103 (mi-puissance) partout ou un repere a -3 dB est calcule.

        Le projet compare ses calculs a des mesures REW. Un defaut a -3,000 dB
        introduirait un ecart systematique de 0,11 % dans chaque comparaison.
        """
        for fonction in (F.reperes_3db_ideaux, F.repere_3db):
            with self.subTest(fonction=fonction.__name__):
                defaut = inspect.signature(fonction).parameters['seuil'].default
                self.assertAlmostEqual(defaut, 3.0103, delta=1e-9)
        self.assertAlmostEqual(F.SEUIL_MI_PUISSANCE, 3.0103, delta=1e-9)
        self.assertAlmostEqual(F.SEUIL_LITTERAL, 3.0, delta=1e-12)

    def test_la_cible_de_sommation_est_un_parametre_partout(self):
        """Decision D2 : jamais de cible cablee en dur, ni dans filtre ni dans optim.

        La cible (Butterworth / LR2 / plate) est volontairement reportee apres la
        phase 1. Si une fonction la figeait, le gel se ferait par omission -- ce
        que la decision interdit explicitement.
        """
        self.assertIn('nom', inspect.signature(F.cible).parameters)
        self.assertIn('cible_nom', inspect.signature(O.cout).parameters)
        self.assertEqual(inspect.signature(O.sanity_check_continu)
                         .parameters['cible_nom'].default, 'butterworth')
        self.assertEqual(tuple(F.CIBLES), ('butterworth', 'lr2', 'plate'))

    def test_l_hypothese_d_independance_est_explicite(self):
        """rho=0 par defaut : l'independance de L et C est une HYPOTHESE, pas un fait.

        Deux composants du meme lot sont correles. Que le parametre existe et
        vaille zero par defaut rend l'hypothese visible dans la signature -- et
        donc discutable a l'oral.
        """
        self.assertEqual(inspect.signature(N.u_f0_relative).parameters['rho'].default, 0.0)
        self.assertEqual(inspect.signature(N.mc_f0).parameters['rho'].default, 0.0)

    def test_le_montage_de_mesure_est_un_parametre(self):
        """L'incertitude de module depend du montage : A, B ou C doivent exister.

        Une incertitude calculee sans savoir comment la mesure a ete faite est
        un nombre, pas une incertitude.
        """
        parametres = inspect.signature(IO.u_module_aleatoire).parameters
        self.assertIn('montage', parametres)
        for montage in ('A', 'B', 'C'):
            with self.subTest(montage=montage):
                u = IO.u_module_aleatoire(14.0, 100.0, 0.014, montage=montage)
                self.assertGreater(u, 0.0)


class TestConventionsDuDepot(unittest.TestCase):
    """UTF-8, fins de ligne LF, sources sans accents -- et donnees etiquetees."""

    @staticmethod
    def _sources():
        dossier = contexte.DOSSIER_ANALYSE
        chemins = [os.path.join(dossier, nom) for nom in sorted(os.listdir(dossier))
                   if nom.endswith('.py')]
        chemins += [os.path.join(contexte.DOSSIER_TESTS, nom)
                    for nom in sorted(os.listdir(contexte.DOSSIER_TESTS))
                    if nom.endswith('.py')]
        return chemins

    def test_tous_les_sources_sont_utf8_sans_crlf(self):
        """Convention gelee : UTF-8 explicite, fins de ligne LF, y compris sous Windows.

        Le depot est partage entre un poste Windows et, potentiellement, une
        machine du lycee. Des fins de ligne melangees rendent chaque diff
        illisible et masquent les vraies modifications.
        """
        for chemin in self._sources():
            with self.subTest(fichier=os.path.basename(chemin)):
                with open(chemin, 'rb') as fh:
                    octets = fh.read()
                self.assertNotIn(b'\r\n', octets, 'fins de ligne CRLF')
                octets.decode('utf-8')

    def test_les_sources_restent_imprimables_dans_une_console_cp1252(self):
        """Aucun caractere hors cp1252 dans les modules de calcul.

        Pourquoi ce critere et pas "pas d'accents". La console Windows par defaut
        est en cp1252, qui encode parfaitement les accents francais : ecrire
        "frequence" sans accent est une habitude de prudence, pas une necessite
        technique. Ce qui plante VRAIMENT un script, c'est un caractere hors de
        cp1252 -- Omega, phi, fleche, symbole d'avertissement -- passe a
        ``print()`` : UnicodeEncodeError, arret du script, et le message qu'on
        voulait afficher est perdu. Le test controle donc la propriete qui a des
        consequences, pas la coutume.

        EXEMPTION explicite et justifiee : ``figures.py`` et ``blueprint_mpl.py``
        contiennent Omega, phi, chi, fleches et exposants parce que ce sont des
        ETIQUETTES D'AXES destinees a matplotlib, qui les rend en SVG et ne les
        imprime jamais. L'exemption est nominative : si un module de calcul
        adoptait la meme pratique, ce test le signalerait. A surveiller malgre
        tout du cote figures : un de ces caracteres passe par megarde a un
        ``print()`` de diagnostic ferait tomber la chaine sur le poste de Thomas.
        """
        exemptes = {'figures.py', 'blueprint_mpl.py'}
        for chemin in self._sources():
            nom = os.path.basename(chemin)
            if nom in exemptes:
                continue
            with self.subTest(fichier=nom):
                with open(chemin, encoding='utf-8') as fh:
                    texte = fh.read()
                hors = sorted({c for c in set(texte)
                               if not c.isascii() and not _encodable_cp1252(c)})
                self.assertEqual(hors, [], 'caracteres hors cp1252 : %r' % hors)

    def test_les_modules_du_contrat_n_utilisent_pas_de_lettres_accentuees(self):
        """Les huit modules du § 09.4 : aucune LETTRE accentuee dans le source.

        Convention du projet, tenue aujourd'hui par les huit modules du contrat.
        La ponctuation typographique qu'ils emploient -- le signe de section et
        les guillemets francais -- est autorisee : elle s'encode en cp1252, donc
        elle s'imprime, et elle rend les renvois "voir § 04.5" lisibles. Ce
        qui est proscrit, ce sont les lettres accentuees, parce que le jour ou un
        fichier est relu avec le mauvais encodage, ce sont elles qui rendent le
        texte illisible en masse.
        """
        noms_contrat = {'%s.py' % nom for nom in MODULES}
        for chemin in self._sources():
            nom = os.path.basename(chemin)
            if nom not in noms_contrat:
                continue
            with self.subTest(module=nom):
                with open(chemin, encoding='utf-8') as fh:
                    texte = fh.read()
                trouvees = sorted(set(texte) & LETTRES_ACCENTUEES)
                self.assertEqual(trouvees, [], 'lettres accentuees : %r' % trouvees)

    def test_une_seule_convention_de_renvoi_le_signe_de_section(self):
        """Tous les renvois s'ecrivent « § NN », jamais « section NN ».

        Ce n'est pas une coquetterie : le dossier analyse/ sera imprime et lu d'un
        bloc, en annexe du PDF d'oral. Deux conventions de renvoi -- et un fichier
        qui melangeait les deux -- donnent l'impression de fichiers ecrits par des
        mains differentes. Le « § » a ete choisi parce qu'il est plus court, qu'il
        s'encode en cp1252 (0xA7, donc imprimable dans une console Windows) et que le
        paragraphe etant MASCULIN, tous les articles retombent juste : « du § 03.7 »,
        « au § 09.4 ». Le remplacement mecanique inverse avait laisse 27 fautes
        d'accord du type « du section 03.7 » (relecture du 2026-09-14).

        Le mot « section » reste evidemment permis dans son sens physique -- la
        section d'un fil de cuivre, dans self_bobine -- d'ou le motif qui n'attrape
        que « section » SUIVI D'UN NUMERO.
        """
        motif = re.compile(r'[Ss]ections?\s+\d')
        for chemin in self._sources():
            with self.subTest(fichier=os.path.basename(chemin)):
                with open(chemin, encoding='utf-8') as fh:
                    texte = fh.read()
                trouves = motif.findall(texte)
                self.assertEqual(
                    trouves, [],
                    'renvoi hors convention (%d) : ecrire « § NN », pas « section NN »'
                    % len(trouves))

    def test_les_noms_de_modules_du_contrat_sont_importables(self):
        """Les noms de MODULE du § 09.2 doivent tous repondre a un `import`.

        Le nom de module fait partie du contrat gele, contrat contre lequel d'autres
        agents ecrivent en parallele : un `import entrees` ou un
        `import injecter_figures` qui echoue casse leur code, meme si les signatures
        internes sont respectees a la lettre. Deux modules ont ete renommes a
        l'ecriture (entrees -> io_mesures, injecter_figures fusionne dans figures),
        pour de bonnes raisons documentees dans LISEZMOI.md ; des alias retablissent
        les noms du contrat sans dupliquer une ligne de code (relecture du
        2026-09-14).

        Le test verifie l'IDENTITE des objets, pas seulement leur existence : deux
        implementations d'un meme lecteur de CSV divergeraient tot ou tard.
        """
        import entrees
        import injecter_figures
        import figures as FIGMOD

        for nom in ('lire_mesure', 'ecrire_mesure', 'lire_rew', 'lire_scope',
                    'depouiller_scope', 'CHEMIN_EXEMPLE', 'VERSION_FORMAT'):
            with self.subTest(nom='entrees.%s' % nom):
                self.assertTrue(hasattr(entrees, nom), 'entrees.%s absent' % nom)
                self.assertIs(getattr(entrees, nom), getattr(IO, nom))

        self.assertIs(injecter_figures.injecter_figures, FIGMOD.injecter_figures)
        self.assertIs(injecter_figures.FIGURES, FIGMOD.FIGURES)

    def test_les_jeux_typiques_portent_leur_avertissement(self):
        """Aucun resultat invente : chaque jeu de valeurs typiques doit se declarer.

        Principe 2 du § 09.1. ``SUB_TYP`` vient d'une datasheet publique, pas
        du haut-parleur de Thomas ; ``SUB_SYNTHETIQUE`` vient d'un modele. Sans
        etiquette dans l'objet lui-meme, ces chiffres finiraient un jour dans une
        diapositive comme s'ils etaient mesures.
        """
        for nom in ('SUB_TYP', 'SUB_TYP_CLOS', 'SUB_TYP_BR', 'MED_TYP'):
            jeu = getattr(MH, nom, None)
            if jeu is None:
                continue
            with self.subTest(jeu=nom):
                self.assertIn('avertissement', jeu)
                self.assertIn('MESURE', jeu['avertissement'].upper())
                self.assertIn('source', jeu)

    def test_les_chemins_livres_restent_dans_le_dossier_analyse(self):
        """Les constantes de chemin ne doivent pas pointer hors du projet.

        Un chemin absolu code en dur vers le poste de Thomas rendrait la chaine
        injouable ailleurs -- notamment sur la machine du lycee.
        """
        for nom in ('CHEMIN_CRITERES', 'CHEMIN_EXEMPLE', 'DOSSIER_MESURES'):
            chemin = getattr(IO, nom, None)
            if chemin is None:
                continue
            with self.subTest(constante=nom):
                self.assertTrue(os.path.abspath(str(chemin))
                                .startswith(contexte.DOSSIER_ANALYSE),
                                '%s sort de analyse/ : %s' % (nom, chemin))

    def test_pas_de_fichier_init_dans_le_dossier_de_tests(self):
        """§ 09.6 : pas de ``__init__.py`` dans ``tests/``.

        Avec un ``__init__.py``, ``python -m unittest discover -s analyse/tests``
        echoue sur "Start directory is not importable". La commande de lancement
        est gelee ; ce test empeche qu'on la casse en croyant bien faire.
        """
        self.assertFalse(os.path.exists(os.path.join(contexte.DOSSIER_TESTS,
                                                     '__init__.py')))


class TestCoherenceEntreModules(unittest.TestCase):
    """Deux modules qui calculent la meme grandeur doivent trouver la meme chose."""

    def test_le_pole_lc_est_le_meme_dans_les_trois_modules(self):
        """f0 = 1/(2 pi racine(LC)) : filtre, self_bobine et incertitudes doivent coincider.

        Trois implementations independantes du meme objet physique. Si elles
        divergeaient, deux parties du rapport citeraient deux frequences
        differentes pour le meme filtre.
        """
        L, C = 18e-3, 150e-6
        f0_filtre = F.pole_et_q(L, C, 8.0)[0]
        f0_self = SB.f0_serie(L, C)
        f0_incertitudes = N.f0_lc(L, C)
        self.assertAlmostEqual(f0_filtre, f0_self, delta=1e-9)
        self.assertAlmostEqual(f0_filtre, f0_incertitudes, delta=1e-9)

    def test_zobel_est_la_meme_formule_dans_filtre_et_modele_hp(self):
        """``zobel`` est redefinie dans les deux modules pour l'autonomie : meme resultat exige.

        La duplication est assumee (chaque module doit rester utilisable seul),
        mais une duplication qui derive est pire qu'une dependance.
        """
        f = MH.grille_log(20.0, 500.0, 12)
        Z = MH.Z_ts(f, *contexte.THETA_SYNTHETIQUE)
        Rz, Cz = MH.zobel_ideal(6.5, 1.2e-3)
        np.testing.assert_allclose(MH.zobel(Z, f, Rz, Cz), F.zobel(Z, f, Rz, Cz),
                                   rtol=1e-12)
        self.assertEqual(F.valeurs_zobel(6.5, 1.2e-3), (Rz, Cz))

    def test_le_repli_local_de_io_mesures_egale_modele_hp(self):
        """``io_mesures`` porte un repli interne de Z_ts : il doit etre identique.

        Le repli existe pour que la lecture de mesures ne dependent pas du module
        de modele. Identique signifie ici a 0 pres, pas "du meme ordre".
        """
        f = MH.grille_log(10.0, 500.0, 12)
        theta = contexte.THETA_SYNTHETIQUE
        Z_reference = MH.Z_ts(f, *theta)
        Z_repli = IO._z_ts_local(f, *theta)
        self.assertEqual(float(np.max(np.abs(Z_repli - Z_reference))), 0.0)

    def test_les_charges_synthetiques_des_deux_modules_concordent(self):
        """``optim.charge_synthetique`` doit rendre la Z_ts du jeu qu'elle annonce.

        Sinon l'optimiseur travaillerait sur une charge differente de celle que
        les figures montrent.
        """
        f = F.grille_critere()
        Z_optim = O.charge_synthetique(f)
        Z_modele = MH.Z_ts(f, **{k: O.SUB_SYNTHETIQUE[k]
                                 for k in ('Re', 'Le', 'Res', 'fs', 'Qms')})
        np.testing.assert_allclose(Z_optim, Z_modele, rtol=1e-10)

    def test_tous_les_modules_s_importent_et_declarent_scipy(self):
        """Les huit modules doivent s'importer, et ts_fit dire si SciPy est la.

        Fait de reference du 2026-09-13 : scipy 1.18.1 EST installe. Le repli
        n'est pas une contrainte subie mais un exercice de robustesse -- encore
        faut-il que le code sache lequel des deux il utilise, et le dise.
        """
        for nom, module in MODULES.items():
            with self.subTest(module=nom):
                self.assertTrue(hasattr(module, '__doc__'))
        self.assertIsInstance(T.SCIPY, bool)
        self.assertTrue(T.SCIPY, 'scipy absent : verifier l environnement (§ 09.5)')


if __name__ == '__main__':
    unittest.main(verbosity=2)
