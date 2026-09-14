"""Test (g) du § 09.6 -- entrees/sorties de mesure (module ``io_mesures``).

CE QUE CE FICHIER PROTEGE
-------------------------
Le fichier de mesure est le SEUL objet du TIPE qui coute une seance de banc. Tout
le reste se recalcule en dix secondes. Trois facons de le perdre, toutes silencieuses :

1. **L'aller-retour n'est pas exact.** On ecrit en texte, on relit, et les
   ``%.9g`` ont mange des chiffres. Une serie relue a 1e-3 pres n'est plus la serie
   mesuree, et personne ne le voit -- la courbe reste jolie. Critere : 1e-8 en
   RELATIF (mesure : 4,8e-9).
2. **Les colonnes derivees ne sont plus recalculables.** Le principe 1 de la
   § 09.1 dit : le fichier porte les LECTURES (V_d, V_R, dt) *et* les grandeurs
   derivees (|Z|, phi). Si l'on decouvre apres coup que R_ref valait 99,2 et non
   99,7, on rejoue ``depouiller()`` et la serie entiere reste exploitable. Cela
   n'est vrai que si le recalcul redonne bien les colonnes ecrites.
3. **Un fichier hors format est accepte.** Sans ``version_format``, sans les 14
   metadonnees obligatoires, sans une colonne, la lecture doit ECHOUER
   bruyamment. Un fichier a moitie lu qui rend quand meme un tableau est le pire
   des cas : il produit des chiffres.

S'y ajoute le piege d'estimation du § 09.3 : la detection synchrone sur une
fenetre qui ne contient pas un nombre ENTIER de periodes se trompe de 5 % sur |Z|
SANS RIEN DIRE. Trois lignes de moindres carres l'en empechent -- et le controle
de signe (self pure -> +90 deg, condensateur pur -> -90 deg) attrape une fois pour
toutes l'erreur de convention qui, sinon, rend un Qms negatif a l'acte 2.
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
import io_mesures as IO  # noqa: E402
import modele_hp as MH  # noqa: E402


class TestAllerRetourCSV(unittest.TestCase):
    """(g1) Ecrire puis relire un CSV de mesure ne doit rien perdre."""

    def setUp(self):
        self.d, self.meta = contexte.mesure_synthetique()

    def test_g1_aller_retour_exact_en_relatif(self):
        """Le CSV est ecrit en %.9g : l'aller-retour doit etre exact a 1e-8 RELATIF.

        Neuf chiffres significatifs coutent 15 % de taille de fichier et
        suppriment toute discussion : la valeur relue EST la valeur mesuree. Avec
        le %.6g par defaut on perdrait 1e-6 en relatif, ce qui est deja du meme
        ordre que la resolution de lecture de l'oscilloscope -- donc indiscernable
        d'une vraie fluctuation, donc indebogable.
        """
        with contexte.dossier_jetable() as dossier:
            chemin = os.path.join(dossier, 'aller_retour.csv')
            IO.ecrire_mesure(chemin, self.d, self.meta)
            relu, meta_relue = IO.lire_mesure(chemin)

        self.assertEqual(relu.shape, self.d.shape)
        pires = {}
        for colonne in IO.COLONNES:
            avant, apres = self.d[colonne], relu[colonne]
            if np.all(avant != 0.0):
                pires[colonne] = contexte.ecart_relatif_max(apres, avant)
            else:
                pires[colonne] = float(np.max(np.abs(apres - avant)))
        pire = max(pires.values())
        self.assertLess(pire, 1e-8, 'aller-retour degrade : %r' % pires)

    def test_g2_metadonnees_conservees(self):
        """Les 14 metadonnees obligatoires doivent survivre a l'aller-retour.

        Ce sont les CONDITIONS de la mesure (date, montage, R_ref mesuree, niveau,
        temperature, Re en continu avant et apres). Sans elles la courbe n'est pas
        une mesure : on ne peut ni la rejouer, ni la recouper, ni la defendre.
        """
        with contexte.dossier_jetable() as dossier:
            chemin = os.path.join(dossier, 'meta.csv')
            IO.ecrire_mesure(chemin, self.d, self.meta)
            _, meta_relue = IO.lire_mesure(chemin)

        manquantes = IO.verifier_metadonnees(meta_relue)
        self.assertEqual(manquantes, [], 'metadonnees perdues : %r' % manquantes)
        for cle, valeur in self.meta.items():
            self.assertEqual(meta_relue.get(cle), valeur, 'cle alteree : %s' % cle)

    def test_g3_fichier_utf8_et_fins_de_ligne_lf(self):
        """Convention du projet : fichiers en UTF-8, fins de ligne LF, meme sous Windows.

        Un CSV ecrit en CRLF sur le poste personnel et relu sur une machine du
        lycee produit des lignes avec un retour chariot colle au dernier nombre.
        La regle est donc ecrite, et testee.
        """
        with contexte.dossier_jetable() as dossier:
            chemin = os.path.join(dossier, 'fins_de_ligne.csv')
            IO.ecrire_mesure(chemin, self.d, self.meta)
            with open(chemin, 'rb') as fh:
                octets = fh.read()

        self.assertNotIn(b'\r\n', octets, 'fins de ligne CRLF : convention LF violee')
        octets.decode('utf-8')  # leve UnicodeDecodeError si le fichier n'est pas UTF-8

    def test_g4_colonnes_derivees_recalculables(self):
        """|Z| et phi doivent se recalculer depuis les LECTURES brutes.

        C'est le principe 1 du § 09.1 rendu verifiable : si R_ref se revele
        fausse apres coup, on rejoue ``depouiller()`` au lieu de refaire la seance.
        Le critere est RELATIF (1e-8) parce que |Z| monte a plusieurs dizaines
        d'ohms au pic : 1e-7 ohm en absolu serait plus severe en haut de pic qu'en
        bas, sans raison physique.
        """
        depouille = IO.depouiller(self.d, self.meta)
        for colonne in IO.COLONNES_DERIVEES:
            ecart_rel = contexte.ecart_relatif_max(depouille[colonne], self.d[colonne]) \
                if np.all(self.d[colonne] != 0.0) else 0.0
            ecart_abs = float(np.max(np.abs(depouille[colonne] - self.d[colonne])))
            self.assertLess(ecart_rel, 1e-8,
                            '%s : recalcul a %.2e en relatif' % (colonne, ecart_rel))
            self.assertLess(ecart_abs, 1e-6,
                            '%s : recalcul a %.2e en absolu' % (colonne, ecart_abs))

    def test_g5_depouillement_rejoue_avec_une_autre_Rref(self):
        """Changer R_ref APRES la seance doit changer |Z| proportionnellement.

        Preuve que la serie brute est bien ce qui est conserve : |Z| = R_ref*Vd/Vr
        est strictement proportionnelle a R_ref. Si ce test tombe, c'est que
        ``depouiller`` recopie les colonnes derivees au lieu de les refaire.
        """
        corrige = IO.depouiller(self.d, self.meta, R_ref_ohm=99.2)
        rapport = corrige['module_Z_ohm'] / self.d['module_Z_ohm']
        attendu = 99.2 / 99.7
        self.assertLess(float(np.max(np.abs(rapport / attendu - 1.0))), 1e-9)


class TestRefusFichierInvalide(unittest.TestCase):
    """(g6) Un fichier hors format doit echouer bruyamment, jamais en silence."""

    def _ecrire(self, dossier, nom, texte):
        chemin = os.path.join(dossier, nom)
        with open(chemin, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(texte)
        return chemin

    def test_g6_version_format_absente(self):
        """Sans ``version_format``, le fichier est hors format : refus.

        C'est la cle qui permettra de changer d'avis sur le format sans casser les
        anciens fichiers. Un fichier qui ne la porte pas n'a pas ete ecrit par la
        chaine : on ne sait pas ce qu'on lit.
        """
        entete = '# titre libre\n# date: 2026-09-13\n'
        colonnes = ','.join(IO.COLONNES) + '\n'
        with contexte.dossier_jetable() as dossier:
            chemin = self._ecrire(dossier, 'sans_version.csv',
                                  entete + colonnes + '10,1,1,0,1,0,0,0\n')
            with self.assertRaises(IO.ErreurFormatMesure):
                IO.lire_mesure(chemin)

    def test_g6_colonne_manquante(self):
        """Une colonne absente doit etre NOMMEE dans le message d'erreur.

        Un message du type 'IndexError' ne dit pas quoi corriger ; un message qui
        cite la colonne se corrige en dix secondes le soir de la manip.
        """
        with contexte.dossier_jetable() as dossier:
            chemin = self._ecrire(dossier, 'colonne_absente.csv',
                                  '# version_format: 1\nf_Hz,V_dipole_V\n10,1\n')
            with self.assertRaises(IO.ErreurFormatMesure) as capture:
                IO.lire_mesure(chemin)
        message = str(capture.exception)
        self.assertIn('V_Rref_V', message)
        self.assertIn('module_Z_ohm', message)

    def test_g6_aucune_ligne_de_donnees(self):
        """Une en-tete seule (manip interrompue) doit etre refusee, pas rendue vide.

        Un tableau vide se propage jusqu'a l'ajustement, ou il produit un message
        illisible loin de la cause.
        """
        with contexte.dossier_jetable() as dossier:
            chemin = self._ecrire(dossier, 'vide.csv', '# version_format: 1\n')
            with self.assertRaises(IO.ErreurFormatMesure):
                IO.lire_mesure(chemin)

    def test_g6_metadonnee_obligatoire_manquante(self):
        """``verifier_metadonnees`` doit lister exactement ce qui manque.

        La liste des 14 cles est la version executable de l'etape 12 du § 02.11 :
        si elle n'est pas contrainte par le code, elle ne sera pas remplie un soir
        de manip a 18 h.
        """
        meta = contexte.metadonnees_completes()
        del meta['R_ref_mesuree_ohm']
        del meta['temperature_C']
        manquantes = IO.verifier_metadonnees(meta)
        self.assertEqual(sorted(manquantes), ['R_ref_mesuree_ohm', 'temperature_C'])
        self.assertEqual(len(IO.META_OBLIGATOIRES), 14)

    def test_g6_lignes_de_commentaire_libre_ignorees(self):
        """Une ligne '#' qui n'est pas 'cle: valeur' ne doit pas entrer dans meta.

        Sans ce filtre, la ligne de titre du fichier deviendrait une metadonnee
        fantaisiste, et ``verifier_metadonnees`` cesserait de dire la verite.
        """
        d, meta = contexte.mesure_synthetique()
        with contexte.dossier_jetable() as dossier:
            chemin = os.path.join(dossier, 'commentaires.csv')
            IO.ecrire_mesure(chemin, d, meta,
                             commentaires=('phrase libre sans deux-points',
                                           'DONNEES SYNTHETIQUES'))
            _, relue = IO.lire_mesure(chemin)
        for cle in relue:
            self.assertNotIn(' ', cle, 'cle fantaisiste entree dans meta : %r' % cle)


class TestDepouillementOscilloscope(unittest.TestCase):
    """(g7-g8) Estimation du module et de la phase depuis une acquisition 2 voies."""

    @staticmethod
    def _acquisition(Z, f0, duree, R_ref=100.0, offset=0.0, f_ech=50000.0):
        """Simule les deux voies du montage : CH1 = V_dipole, CH2 = V_Rref."""
        t = np.arange(0.0, duree, 1.0 / f_ech)
        w = 2.0 * np.pi * f0
        A1 = Z / (Z + R_ref)
        A2 = R_ref / (Z + R_ref)
        v1 = np.real(A1 * np.exp(1j * w * t)) + offset
        v2 = np.real(A2 * np.exp(1j * w * t)) + offset
        return t, v1, v2

    def test_g7_signe_de_la_phase(self):
        """Self pure -> +90,00 deg ; condensateur pur -> -90,00 deg.

        Trois lignes de test contre une erreur de convention qui, sinon, se paie
        a l'acte 2 par un Qms negatif ou une phase en miroir, SANS AUCUN MESSAGE
        D'ERREUR. La convention gelee (§ 02) est dt = t(V_Rref) - t(V_dipole) sur
        deux passages par zero montants, d'ou phi > 0 pour une charge inductive.
        """
        f0, R_ref = 100.0, 100.0
        w = 2.0 * np.pi * f0
        # Seuils LUS dans criteres_geles.json (§ 09.6, principe 4).
        phi_self = contexte.critere('g_entrees', 'phase_self_pure_deg')
        phi_condo = contexte.critere('g_entrees', 'phase_condensateur_pur_deg')
        delta = contexte.critere('g_entrees', 'phase_delta_deg')
        cas = [('self pure 10 mH', 1j * w * 10e-3, phi_self),
               ('condensateur pur 100 uF', 1.0 / (1j * w * 100e-6), phi_condo)]
        for nom, Z, phase_attendue in cas:
            with self.subTest(dipole=nom):
                t, v1, v2 = self._acquisition(Z, f0, duree=0.1)
                module, phase, _, _ = IO.depouiller_scope(t, v1, v2, f0, R_ref)
                self.assertAlmostEqual(phase, phase_attendue, delta=delta)
                self.assertAlmostEqual(module, abs(Z), delta=1e-3 * abs(Z))

    def test_g8_fenetre_non_entiere_les_moindres_carres_ne_se_trompent_pas(self):
        """Fenetre de 1,06 periode + offset continu : lstsq doit rester a +/- 0,5 %.

        Le piege documente au § 09.3 : la projection sur un seul point de DFT
        n'est exacte que si la fenetre contient un nombre ENTIER de periodes.
        Au deuxieme point de la grille (10,59 Hz sur 100 ms) la DFT brute se
        trompe de -5,5 % sur |Z| et de 2,6 deg sur la phase -- assez pour ruiner
        l'ajustement de l'acte 2 et depasser a elle seule la porte de validation
        a +/- 3 % de la phase 1. Les moindres carres sur [cos, sin, 1] sont
        valables pour une fenetre QUELCONQUE et absorbent l'offset au passage.
        """
        f0 = 10.5946  # deuxieme point de la grille log du § 02.6
        Z = complex(MH.Z_ts(np.array([f0]), *contexte.THETA_SYNTHETIQUE)[0])
        t, v1, v2 = self._acquisition(Z, f0, duree=0.1, offset=0.01)  # 1,06 periode
        module, phase, _, _ = IO.depouiller_scope(t, v1, v2, f0, 100.0, methode='lstsq')
        self.assertLess(abs(module / abs(Z) - 1.0), 5e-3,
                        'lstsq hors tolerance sur fenetre non entiere')
        self.assertLess(abs(phase - np.degrees(np.angle(Z))),
                        contexte.critere('g_entrees', 'lstsq_fenetre_quelconque_pct'))

    def test_g8_dft_tronquee_coherente_avec_lstsq(self):
        """La DFT TRONQUEE a un nombre entier de periodes doit rejoindre lstsq.

        On ne teste pas la DFT brute : la fonction du projet tronque toujours,
        precisement pour rendre le piege inatteignable. Ce test verifie que les
        deux estimateurs, pourtant tres differents, donnent la meme reponse -- ce
        qui est l'argument pour faire confiance a l'un comme a l'autre.
        """
        f0 = 10.5946
        Z = complex(MH.Z_ts(np.array([f0]), *contexte.THETA_SYNTHETIQUE)[0])
        t, v1, v2 = self._acquisition(Z, f0, duree=0.1, offset=0.01)
        m_lstsq, p_lstsq, _, _ = IO.depouiller_scope(t, v1, v2, f0, 100.0, methode='lstsq')
        m_dft, p_dft, _, _ = IO.depouiller_scope(t, v1, v2, f0, 100.0, methode='dft')
        self.assertLess(abs(m_dft / m_lstsq - 1.0), 5e-3)
        self.assertLess(abs(p_dft - p_lstsq), 0.5)

    def test_g8_fenetre_trop_courte_refusee(self):
        """Moins d'une periode de f0 : la DFT doit refuser, pas deviner.

        Avec zero periode entiere disponible il n'y a rien a projeter. Rendre un
        nombre serait rendre du bruit avec trois decimales.
        """
        f0 = 100.0
        Z = complex(8.0)
        t, v1, v2 = self._acquisition(Z, f0, duree=0.005)  # 0,5 periode
        with self.assertRaises(ValueError):
            IO.depouiller_scope(t, v1, v2, f0, 100.0, methode='dft')


class TestFormatsImportes(unittest.TestCase):
    """(g9) REW et oscilloscope : deux formats subis, deux lecteurs geles."""

    def test_g9_lecture_rew_auto_detection_du_separateur(self):
        """Le separateur d'un export REW depend des reglages regionaux : l'auto-detecter.

        Sur une machine francaise, le point-virgule et la virgule decimale sont
        courants. Un lecteur qui suppose la virgule rendrait deux fois plus de
        colonnes que prevu -- ou, pire, une colonne de NaN.
        """
        lignes_espaces = ('* Measurement data measured by REW\n'
                          '* Freq(Hz) Z(ohms) Phase(degrees)\n'
                          '10.000 10.077 41.726\n20.000 25.110 12.000\n40.000 50.000 -3.000\n')
        lignes_virgules = ('"Freq","Z","Phase"\n10,10.077,41.726\n'
                           '20,25.110,12.000\n40,50.000,-3.000\n')
        with contexte.dossier_jetable() as dossier:
            for nom, texte in (('rew_espaces.txt', lignes_espaces),
                               ('rew_virgules.csv', lignes_virgules)):
                chemin = os.path.join(dossier, nom)
                with open(chemin, 'w', encoding='utf-8', newline='\n') as fh:
                    fh.write(texte)
                f, mod, phi, meta = IO.lire_rew(chemin, u_module_relative=0.02,
                                                u_phase_deg=1.5)
                with self.subTest(fichier=nom):
                    self.assertEqual(f.size, 3)
                    np.testing.assert_allclose(f, [10.0, 20.0, 40.0])
                    np.testing.assert_allclose(mod, [10.077, 25.110, 50.0])
                    np.testing.assert_allclose(phi, [41.726, 12.0, -3.0])
                    self.assertIn('n_points', meta)

    def test_g9_lecture_scope(self):
        """L'export d'oscilloscope donne (t, CH1, CH2) et sa frequence d'echantillonnage.

        C'est la porte d'entree de ``depouiller_scope`` : si le temps est mal lu,
        toute la detection synchrone est fausse d'un facteur inconnu.
        """
        texte = 'Time,CH1,CH2\n0,0.10,0.50\n1e-5,0.11,0.51\n2e-5,0.12,0.52\n'
        with contexte.dossier_jetable() as dossier:
            chemin = os.path.join(dossier, 'scope.csv')
            with open(chemin, 'w', encoding='utf-8', newline='\n') as fh:
                fh.write(texte)
            t, v1, v2, meta = IO.lire_scope(chemin)
        np.testing.assert_allclose(t, [0.0, 1e-5, 2e-5])
        np.testing.assert_allclose(v1, [0.10, 0.11, 0.12])
        np.testing.assert_allclose(v2, [0.50, 0.51, 0.52])
        self.assertAlmostEqual(meta['f_echantillonnage_Hz'], 1e5, delta=1.0)


class TestHonneteteDesDonnees(unittest.TestCase):
    """(g10) Le dossier ne contient aucune mesure : le code doit le DIRE."""

    def test_g10_exemple_est_etiquete_synthetique(self):
        """Le CSV d'exemple livre doit se declarer SYNTHETIQUE dans son en-tete.

        C'est le socle d'honnetete du sujet (§ 08). Un fichier d'exemple non
        etiquete finit tot ou tard cite comme une mesure -- a l'oral, devant un
        jury qui demandera la date de la seance.
        """
        self.assertTrue(os.path.exists(IO.CHEMIN_EXEMPLE),
                        'exemple synthetique absent : %s' % IO.CHEMIN_EXEMPLE)
        with open(IO.CHEMIN_EXEMPLE, encoding='utf-8') as fh:
            entete = fh.read(2000).upper()
        self.assertIn('SYNTHETIQUE', entete)
        _, meta = IO.lire_mesure(IO.CHEMIN_EXEMPLE)
        self.assertIn('SYNTHETIQUE', meta.get('dipole', '').upper())

    def test_g10_criteres_non_geles_refuses(self):
        """Tant que les decisions portent [[a geler]], la lecture stricte doit LEVER.

        Principe 4 du § 09.1 : les decisions gelees sont un fichier, pas une
        intention. Si le code acceptait de tourner sur des criteres non signes,
        l'affirmation "criteres geles avant les mesures" ne serait plus verifiable
        -- et rien n'empecherait de retoucher les poids apres coup.
        """
        with self.assertRaises(IO.CriteresNonGeles):
            IO.lire_criteres_geles(exiger_geles=True)
        criteres = IO.lire_criteres_geles(exiger_geles=False)
        for rubrique in IO.SCHEMA_CRITERES:
            self.assertIn(rubrique, criteres)

    def test_g10_ecriture_des_criteres_n_ecrase_jamais(self):
        """``ecrire_criteres_geles`` ne doit jamais ecraser un fichier existant.

        Un gel qu'un script peut reecrire n'est pas un gel.
        """
        with contexte.dossier_jetable() as dossier:
            chemin = os.path.join(dossier, 'criteres.json')
            IO.ecrire_criteres_geles(chemin)
            self.assertTrue(os.path.exists(chemin))
            with self.assertRaises(Exception):
                IO.ecrire_criteres_geles(chemin)


class TestIncertitudeDeMesure(unittest.TestCase):
    """(g11) L'incertitude de module depend du MONTAGE -- pas une constante."""

    def test_g11_facteur_de_soustraction_par_montage(self):
        """Montage A : le facteur sqrt(2)(1 + |Z|/R_ref) explose quand |Z| ~ R_ref.

        C'est l'argument chiffre pour le montage C (GBF flottant) ou pour une
        R_ref de 10 ohm au voisinage du pic : en montage A avec R_ref = 100 ohm et
        |Z| = 50 ohm au pic, l'incertitude relative est multipliee par 1,5 par
        rapport a la bande ou |Z| ~ Re. Le code doit donc DEMANDER le montage.
        """
        eps, R_ref = 0.014, 100.0
        for module in (6.5, 14.0, 50.0):
            u_A = IO.u_module_aleatoire(module, R_ref, eps, montage='A')
            u_B = IO.u_module_aleatoire(module, R_ref, eps, montage='B')
            u_C = IO.u_module_aleatoire(module, R_ref, eps, montage='C')
            with self.subTest(module=module):
                attendu_A = np.sqrt(2.0) * (1.0 + module / R_ref) * eps * module
                attendu_B = np.sqrt(2.0) * (1.0 + R_ref / module) * eps * module
                attendu_C = np.sqrt(2.0) * eps * module
                self.assertAlmostEqual(u_A, attendu_A, delta=1e-9 * attendu_A)
                self.assertAlmostEqual(u_B, attendu_B, delta=1e-9 * attendu_B)
                self.assertAlmostEqual(u_C, attendu_C, delta=1e-9 * attendu_C)
                self.assertGreater(u_A, u_C)

    def test_g11_diagnostic_de_grille_sur_un_pic_sous_echantillonne(self):
        """Un pic couvert par moins de 5 points doit declencher un avertissement.

        Un 18 pouces de sono a un Qms de 3 a 10 : le pic est ETROIT
        (largeur ~ fs/Qms). Au 1/12 d'octave a 40 Hz il ne reste que deux points
        dans la largeur du pic, et l'ajustement perd 2 % sur Res et Qms. Le
        diagnostic dit d'avance qu'il faut densifier -- dix minutes de banc.
        """
        f_large = MH.grille_log(10.0, 500.0, 6)
        module = np.abs(MH.Z_ts(f_large, *contexte.THETA_PIC_ETROIT))
        diagnostic = IO.diagnostiquer_grille(f_large, module, points_min_pic=5)
        self.assertLess(diagnostic['n_points_pic'], 5)
        self.assertTrue(diagnostic['avertissements'])

        f_dense = MH.grille_log(10.0, 500.0, 12, densifier=(20.0, 80.0, 48))
        module_dense = np.abs(MH.Z_ts(f_dense, *contexte.THETA_PIC_ETROIT))
        diagnostic_dense = IO.diagnostiquer_grille(f_dense, module_dense, points_min_pic=5)
        self.assertGreaterEqual(diagnostic_dense['n_points_pic'], 5)


if __name__ == '__main__':
    unittest.main(verbosity=2)
