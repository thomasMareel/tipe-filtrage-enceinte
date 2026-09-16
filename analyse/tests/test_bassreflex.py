"""Test (i) du § 09.6 -- LA VOIE BASS-REFLEX, de bout en bout.

CE QUE CE FICHIER PROTEGE
-------------------------
Le 2026-09-16, l'etudiant a constate que le sub est en caisse BASS-REFLEX AVEC
DEUX EVENTS. Ce n'etait pas su : tous les documents disaient "type de caisse a
documenter", et la chaine s'exercait sur un exemple en caisse CLOSE. Le code,
lui, portait deja le modele a 7-8 parametres et le garde-fou -- ils avaient ete
ecrits PRECISEMENT parce que le type de caisse n'etait pas connu. Ce n'est donc
pas une reprise, c'est une hypothese qui se leve.

Mais "le code porte le modele" et "la voie est eprouvee" sont deux choses
differentes, et c'est ce fichier qui fait la seconde. Ce qui manquait dans
test_ajustement.py : l'ajustement bass-reflex y partait des valeurs VRAIES
(``theta0 = theta_vrai``), ce qui ne prouve rien du chemin reel -- au banc on
n'a pas les valeurs vraies, on a une courbe. Les tests ci-dessous partent donc
de la COURBE, par ``init_depuis_courbe`` puis par le pipeline complet
``identifier(modele='auto')``, exactement comme la phase 1.

QUATRE CHOSES SONT TENUES ICI
  1. le modele a 8 parametres retrouve une Z(f) bass-reflex synthetique bruitee,
     depuis une initialisation LUE SUR LA COURBE, et l'aiguillage automatique le
     choisit tout seul ;
  2. sur la MEME courbe, le modele a 5 parametres est refuse : avertissement en
     mode normal, exception en mode strict. Sans ce refus, il convergerait en
     silence sur des valeurs fausses -- c'est le piege central du projet ;
  3. f_b se predit par la GEOMETRIE (resonateur de Helmholtz, deux events) autant
     qu'il s'ajuste sur Z(f). Deux chemins independants vers le meme nombre : la
     prediction est FALSIFIABLE, ce qui est tout l'interet ;
  4. la sommation en champ proche d'un bass-reflex (Keele) est ponderee par la
     RACINE des aires -- c'est-a-dire par les rayons -- et la charge du
     passe-haut comprend les pavillons d'ultra-aigu, hors bande acoustique mais
     bel et bien en parallele du bloc medium.

Toutes les donnees sont SYNTHETIQUES. Aucune mesure de l'enceinte n'existe a ce
jour : le TYPE de caisse est un fait, les VALEURS (alpha, f_b, Q_l, volume,
cotes des events) sont des ordres de grandeur etiquetes.
"""

import os
import sys
import unittest
import warnings

_ICI = os.path.dirname(os.path.abspath(__file__))
for _d in (_ICI, os.path.dirname(_ICI)):
    if _d not in sys.path:
        sys.path.insert(0, _d)

import numpy as np  # noqa: E402
import contexte  # noqa: E402
import io_mesures as IO  # noqa: E402
import modele_hp as MH  # noqa: E402
import ts_fit as T  # noqa: E402

GRAINE_BASSREFLEX = 20260916
"""Graine GELEE de la courbe bass-reflex synthetique. Un tirage non reproductible
n'est pas un resultat (§ 09.8)."""

THETA_BR8 = (5.4, 1.9e-3, 100.0, 40.0, 6.1, 3.0, 35.0, 7.0)
"""theta = (Re, Le, Res, fs, Qms, alpha, fb, Ql) du sub SYNTHETIQUE en
bass-reflex -- le jeu qui engendre aussi mesures/exemple_synthetique_sub.csv
(io_mesures.SUB_TYPIQUE_BR). Il produit deux pics (16,3 et 85,9 Hz) encadrant un
creux a 34,2 Hz, et |Z|(100 Hz) = 22,4 ohm. LE SECOND PIC TOMBE DANS LA ZONE DE
RACCORD : c'est ce qui rend l'hypothese "8 ohm resistifs" encore plus fausse
qu'en caisse close. ORDRES DE GRANDEUR, PAS UNE MESURE."""


def _courbe_bassreflex(graine=GRAINE_BASSREFLEX, u_rel=0.02, u_deg=1.0):
    """Une mesure SYNTHETIQUE bass-reflex : (f, module, phase, u_mod, u_phi).

    Grille densifiee de f_b/3 a 3 f_b au 1/24 d'octave : en bass-reflex il y a
    DEUX pics et un creux a echantillonner, et ils sont ecartes. C'est la meme
    consigne qu'au § 02.6 -- resserrer la grille la ou elle informe -- appliquee
    au bon endroit ; c'est aussi exactement la grille que genere le fichier
    d'exemple, donc le test eprouve le reglage qui servira au banc.
    """
    fb = THETA_BR8[6]
    f = MH.grille_log(10.0, 500.0, 12, densifier=(fb / 3.0, 3.0 * fb, 24))
    mod, phi, u_mod, u_phi = T.simuler(np.asarray(THETA_BR8, float), f,
                                       modele='bassreflex8', u_rel=u_rel,
                                       u_deg=u_deg, graine=graine)
    return f, mod, phi, u_mod, u_phi


class TestAjustementBassReflex(unittest.TestCase):
    """(i1) Le modele a 8 parametres doit retrouver ce qu'on lui a cache."""

    def test_i1_init_lue_sur_la_courbe_puis_ajustement(self):
        """Depuis une initialisation LUE SUR LA COURBE : 8 parametres retrouves.

        L'initialisation est ici la moitie du travail, et elle n'a rien d'un
        reglage : f_L f_H = f_s f_b et f_L^2 + f_H^2 = f_s^2 (1+alpha) + f_b^2
        donnent f_s et alpha SANS ajustement, par simple lecture des deux pics et
        du creux. Si ce test tombe, c'est que la lecture des extrema s'est
        degradee -- pas les moindres carres.
        """
        f, mod, phi, u_mod, u_phi = _courbe_bassreflex()
        c = contexte.critere('i_bassreflex', 'ajustement_8_parametres')
        with contexte.sans_avertissement():
            theta0 = T.init_depuis_courbe(f, mod, phi, modele='bassreflex8',
                                          bavard=False)
            theta, cov, chi2, _ = T.ajuster_ts(f, mod, phi, u_mod, u_phi, theta0,
                                               modele='bassreflex8',
                                               verifier_caisse=False, bavard=False)
        sigma = T.u_covariance(cov)
        self.assertEqual(len(theta), 8)
        vrai = np.asarray(THETA_BR8, float)
        for i, nom in enumerate(T.NOMS_THETA['bassreflex8']):
            with self.subTest(parametre=nom):
                ecart = abs(theta[i] / vrai[i] - 1.0)
                self.assertLess(100 * ecart, c['ecart_parametre_max_pct'],
                                '%s : %.2f %%' % (nom, 100 * ecart))
                self.assertLess(abs(theta[i] - vrai[i]) / sigma[i],
                                c['ecart_sigma_max'],
                                '%s : %.1f sigma' % (nom, abs(theta[i] - vrai[i]) / sigma[i]))
        self.assertGreater(chi2, c['chi2_reduit_min'])
        self.assertLess(chi2, c['chi2_reduit_max'])

    def test_i1_le_pipeline_auto_choisit_seul_le_bon_modele(self):
        """``identifier(modele='auto')`` doit aiguiller sur la chaine bass-reflex.

        C'est le chemin que prend REELLEMENT la chaine (tout_refaire.py etape 5) :
        personne ne lui dit le type de caisse, il le lit sur la courbe. Le test
        verifie le modele retenu, le chi2, ET que f_b est rendu -- car c'est f_b,
        et lui seul, que la prediction geometrique pourra contredire.
        """
        f, mod, phi, u_mod, u_phi = _courbe_bassreflex()
        c = contexte.critere('i_bassreflex', 'ajustement_8_parametres')
        with contexte.sans_avertissement():
            res = T.identifier(f, mod, phi, u_mod, u_phi, modele='auto',
                               n_mc=40, n_retrait=0, n_multi=0, jack=False,
                               bavard=False,
                               statut_donnees='SYNTHETIQUES (bass-reflex, test i1)')
        self.assertIn(res['modele'], c['modeles_acceptes'])
        self.assertEqual(res['diagnostic_caisse']['type_caisse'], 'bass-reflex')
        self.assertLess(res['chi2_reduit'], c['chi2_reduit_max'])
        self.assertIn('fb', res['noms'])
        fb = float(res['theta'][list(res['noms']).index('fb')])
        self.assertLess(abs(fb / THETA_BR8[6] - 1.0),
                        c['ecart_parametre_max_pct'] / 100.0,
                        'f_b ajuste = %.3f Hz (vrai %.3f)' % (fb, THETA_BR8[6]))

    def test_i1_le_fichier_d_exemple_est_bien_en_bass_reflex(self):
        """Le CSV de demonstration doit decrire la caisse REELLE, pas une autre.

        Tant que l'exemple etait en caisse close, la commande gelee
        ``python analyse/tout_refaire.py`` n'exercait JAMAIS le garde-fou ni le
        modele a 8 parametres : la piece la plus utile du code n'etait eprouvee
        que par un test. Elle l'est maintenant par la chaine entiere.
        """
        d, meta = IO.lire_mesure(IO.CHEMIN_EXEMPLE)
        self.assertIn('BASS-REFLEX', meta.get('dipole', '').upper())
        self.assertIn('SYNTHETIQUE', meta.get('dipole', '').upper())
        self.assertIn('2 events', meta.get('type_caisse', ''))
        diagnostic = IO.diagnostiquer_caisse(d['f_Hz'], d['module_Z_ohm'])
        self.assertGreaterEqual(diagnostic['n_pics'],
                                contexte.critere('i_bassreflex', 'garde_fou')['n_pics_min'])


class TestGardeFouSurLaCourbeReelleDuProjet(unittest.TestCase):
    """(i2) Sur une courbe a deux pics, 5 parametres doit etre REFUSE."""

    def test_i2_avertissement_puis_exception_en_mode_strict(self):
        """Un avertissement se perd dans un journal ; une exception arrete la chaine.

        Les deux comportements sont voulus et tous deux testes : en interactif on
        veut pouvoir passer outre en connaissance de cause (``forcer=True``), mais
        ``tout_refaire.py`` s'arrete au premier echec et ne doit pas produire de
        JSON a partir d'un modele inadapte.
        """
        f, mod, _, _, _ = _courbe_bassreflex()
        c = contexte.critere('i_bassreflex', 'garde_fou')
        with self.assertWarns(UserWarning) as capture:
            diagnostic = T.garde_fou_caisse(f, mod, modele='clos', bavard=False)
        self.assertIn('BASS-REFLEX', str(capture.warning).upper())
        self.assertFalse(diagnostic['compatible'])
        self.assertGreaterEqual(diagnostic['n_pics'], c['n_pics_min'])
        self.assertGreaterEqual(diagnostic['n_parametres_conseilles'],
                                c['n_parametres_conseilles_min'])
        with contexte.sans_avertissement():
            with self.assertRaises(T.CaisseIncompatible):
                T.garde_fou_caisse(f, mod, modele='clos', bavard=False, strict=True)

    def test_i2_identifier_refuse_un_modele_a_5_parametres_impose(self):
        """Imposer ``modele='clos'`` sur une courbe a deux pics doit LEVER.

        Le garde-fou ne sert a rien s'il ne s'arme que dans le mode automatique :
        c'est justement quand on impose un modele a la main qu'on se trompe.
        ``forcer=True`` reste la porte de sortie, explicite et tracee.
        """
        f, mod, phi, u_mod, u_phi = _courbe_bassreflex()
        with contexte.sans_avertissement():
            with self.assertRaises(T.CaisseIncompatible):
                T.identifier(f, mod, phi, u_mod, u_phi, modele='clos', n_mc=10,
                             n_retrait=0, n_multi=0, jack=False, bavard=False)

    def test_i2_le_modele_a_5_parametres_converge_quand_meme(self):
        """Justification du garde-fou : force, le fit rend un f_s qui n'existe pas.

        Si ce test tombait -- si le modele a 5 parametres divergeait franchement
        sur du bass-reflex -- le garde-fou deviendrait facultatif, puisque
        l'erreur se verrait. Tant qu'il passe, le garde-fou est indispensable.

        Ce que rend l'ajustement force sur ce jeu : f_s = 86 Hz, c'est-a-dire le
        pic HAUT de l'impedance, alors que la resonance du haut-parleur en champ
        libre vaut 40 Hz -- un facteur 2,15. Le nombre a l'air d'un f_s, il a la
        bonne unite, il tombe meme sur une vraie particularite de la courbe, et
        il ne veut rien dire. Seuls le chi2 et les residus le trahissent, APRES.
        """
        f, mod, phi, u_mod, u_phi = _courbe_bassreflex()
        with contexte.sans_avertissement():
            theta0 = T.init_depuis_courbe(f, mod, phi, modele='clos', bavard=False)
            theta, _, chi2, _ = T.ajuster_ts(f, mod, phi, u_mod, u_phi, theta0,
                                             modele='clos', verifier_caisse=False,
                                             bavard=False)
        self.assertTrue(np.all(np.isfinite(theta)),
                        'le fit a diverge : le danger serait visible, donc moindre')
        self.assertEqual(len(theta), 5)
        ecart_fs = abs(theta[3] / THETA_BR8[3] - 1.0)
        self.assertGreater(ecart_fs, 0.5,
                           'f_s ajuste = %.1f Hz contre %.1f Hz vrais : si l ecart '
                           'devenait petit, le modele a 5 parametres cesserait d etre '
                           'dangereux' % (theta[3], THETA_BR8[3]))
        self.assertGreater(chi2, contexte.critere('i_bassreflex',
                                                  'ajustement_8_parametres')['chi2_reduit_max'],
                           'un chi2 acceptable sur un modele faux : le seul garde-fou '
                           'a posteriori tomberait aussi')


class TestFrequenceAccordHelmholtz(unittest.TestCase):
    """(i3) f_b predite par la geometrie : une prediction FALSIFIABLE."""

    def test_i3_valeur_et_convention_de_correction_de_bout(self):
        """V = 110 L, 2 events de 100 mm / 274 mm -> f_b = 35,01 Hz.

        Ce n'est pas un nombre magique : c'est c/(2 pi) racine(S_tot/(V L_eff))
        avec L_eff = L + k a et k = 1,463 (une extremite BRIDEE dehors, une LIBRE
        dedans -- la convention du projet, § 01.10 bis). Ces cotes ont ete
        resolues A L'ENVERS pour accorder a 35 Hz : le test verifie donc le CODE,
        pas la caisse. Le test fige la CONVENTION de correction de bout
        autant que la valeur -- changer k sans le dire deplacerait la prediction
        de quelques pour cent, c'est-a-dire juste assez pour "expliquer" apres
        coup un ecart avec l'ajustement.
        """
        c = contexte.critere('i_bassreflex', 'helmholtz')
        fb = MH.frequence_accord_helmholtz(c['volume_L'], c['n_events'],
                                           c['diametre_event_mm'],
                                           c['longueur_event_mm'])
        self.assertAlmostEqual(fb, c['fb_Hz'], delta=c['fb_delta_Hz'])
        detail = MH.frequence_accord_helmholtz(c['volume_L'], c['n_events'],
                                               c['diametre_event_mm'],
                                               c['longueur_event_mm'], detail=True)
        bas, haut = detail['fb_encadrement_Hz']
        self.assertLessEqual(bas, fb + 1e-9)
        self.assertGreaterEqual(haut, fb - 1e-9)
        self.assertGreater(haut / bas - 1.0, 0.01,
                           "les deux conventions de bout doivent ecarter f_b d'au "
                           'moins 1 % : sinon le choix de k ne serait pas un choix')
        # L'etiquetage n'est pas cosmetique : ce nombre est un MODELE, et il sera
        # compare a une mesure. La fonction doit le dire dans son propre resultat.
        self.assertIn('PREDICTION', detail['avertissement'].upper())
        self.assertEqual(detail['n_events'], c['n_events'])

    def test_i3_n_events_entre_en_racine_carree(self):
        """Doubler le nombre d'events monte f_b d'un facteur racine(2), pas de 2.

        Les masses acoustiques des events sont en PARALLELE : la masse totale est
        divisee par N, donc f_b est multipliee par racine(N). C'est exactement le
        genre de facteur qu'on retrouve faux dans un calcul fait de tete, et il
        vaut ici un facteur 1,41 sur la frequence d'accord -- soit, a 35 Hz, une
        erreur de 14 Hz.
        """
        c = contexte.critere('i_bassreflex', 'helmholtz')
        un = MH.frequence_accord_helmholtz(c['volume_L'], 1, c['diametre_event_mm'],
                                           c['longueur_event_mm'])
        deux = MH.frequence_accord_helmholtz(c['volume_L'], 2, c['diametre_event_mm'],
                                             c['longueur_event_mm'])
        self.assertAlmostEqual(deux / un, c['rapport_deux_events_sur_un'],
                               delta=c['rapport_delta'])

    def test_i3_monotonies_physiques(self):
        """Plus de volume, plus long, plus etroit : f_b baisse. Les trois sens.

        Un test de monotonie attrape ce qu'aucun test de valeur n'attrape : une
        inversion de facteur qui laisserait le nombre "plausible" sur le seul jeu
        verifie. Ici les trois dependances sont independantes et de sens connu.
        """
        base = dict(volume_caisse_L=110.0, n_events=2, diametre_event_mm=100.0,
                    longueur_event_mm=274.0)
        f0 = MH.frequence_accord_helmholtz(**base)
        self.assertLess(MH.frequence_accord_helmholtz(**dict(base, volume_caisse_L=200.0)), f0)
        self.assertLess(MH.frequence_accord_helmholtz(**dict(base, longueur_event_mm=400.0)), f0)
        self.assertLess(MH.frequence_accord_helmholtz(**dict(base, diametre_event_mm=70.0)), f0)

    def test_i3_geometrie_et_ajustement_se_confrontent(self):
        """LA prediction falsifiable : f_b geometrique contre f_b ajuste sur Z(f).

        Deux chemins independants vers le meme nombre -- l'un par un metre-ruban,
        l'autre par des moindres carres sur une courbe d'impedance. Sur le jeu
        synthetique ils doivent tomber a moins de 5 % l'un de l'autre (la
        geometrie d'exemple a ete choisie pour accorder a 35 Hz). Au banc, un
        ecart de 5 a 10 % restera ATTENDU -- volume utile, interaction entre
        events, absorbant ; c'est un ecart de 30 % qui denoncerait une erreur.
        """
        c = contexte.critere('i_bassreflex', 'helmholtz')
        fb_geo = MH.frequence_accord_helmholtz(c['volume_L'], c['n_events'],
                                               c['diametre_event_mm'],
                                               c['longueur_event_mm'])
        f, mod, phi, u_mod, u_phi = _courbe_bassreflex()
        with contexte.sans_avertissement():
            theta0 = T.init_depuis_courbe(f, mod, phi, modele='bassreflex8',
                                          bavard=False)
            theta, _, _, _ = T.ajuster_ts(f, mod, phi, u_mod, u_phi, theta0,
                                          modele='bassreflex8',
                                          verifier_caisse=False, bavard=False)
        fb_fit = float(theta[list(T.NOMS_THETA['bassreflex8']).index('fb')])
        ecart = 100.0 * abs(fb_geo / fb_fit - 1.0)
        self.assertLess(ecart, c['ecart_max_geometrie_vs_ajustement_pct'],
                        'f_b geometrique %.2f Hz contre f_b ajuste %.2f Hz : %.1f %%'
                        % (fb_geo, fb_fit, ecart))


class TestSommationChampProche(unittest.TestCase):
    """(i4) Champ proche d'un bass-reflex : membrane + events, methode de Keele."""

    @staticmethod
    def _aires():
        c = contexte.critere('i_bassreflex', 'champ_proche_keele')
        Sd = c['Sd_m2']
        Sev = np.pi * (c['diametre_event_mm'] * 1e-3) ** 2 / 4.0
        return c, Sd, Sev

    def test_i4_la_ponderation_est_en_racine_des_aires(self):
        """Le poids d'un event vaut racine(S/S_d), pas S/S_d : 11,8 dB d'ecart.

        C'est LA faute classique de la methode, et elle ne se voit pas sur une
        courbe -- elle donne juste un creux trop profond autour de f_b. La
        demonstration tient en deux lignes (p_champ_proche ~ rho0 omega u a et
        p_lointain ~ rho0 omega S u / 2 pi r, donc le debit est proportionnel au
        produit pression x RAYON) et elle est dans la docstring de la fonction.
        """
        c, Sd, Sev = self._aires()
        p_m = np.array([0.0 + 0j])
        p_e = np.array([1.0 + 0j])
        total = MH.somme_champ_proche_bassreflex(p_m, p_e, Sd, Sev, n_events=1)
        self.assertAlmostEqual(float(np.abs(total[0])), c['poids_attendu'],
                               delta=c['poids_delta'])
        self.assertGreater(c['poids_attendu'], Sev / Sd,
                           'ponderer par les aires sous-estimerait la contribution')

    def test_i4_deux_events_comptent_double(self):
        """N events identiques : leur contribution est multipliee par N, pas par racine(N).

        A ne pas confondre avec le racine(N) de la frequence d'accord : la, ce
        sont des masses acoustiques en parallele ; ici, ce sont des debits qui
        s'ajoutent. Deux formules voisines et deux exposants differents, c'est
        exactement ce qu'un test de non-regression doit tenir separement.
        """
        c, Sd, Sev = self._aires()
        p_m = np.zeros(3, dtype=complex)
        p_e = np.ones(3, dtype=complex)
        un = MH.somme_champ_proche_bassreflex(p_m, p_e, Sd, Sev, n_events=1)
        deux = MH.somme_champ_proche_bassreflex(p_m, p_e, Sd, Sev, n_events=2)
        self.assertTrue(np.allclose(deux, 2.0 * un, atol=1e-15))

    def test_i4_somme_complexe_et_non_somme_de_modules(self):
        """Sous f_b la membrane et l'event sont en OPPOSITION : la somme doit chuter.

        Sommer des modules donnerait ici 1 + poids au lieu de 1 - poids, soit une
        courbe toujours trop haute precisement autour de l'accord -- la zone qui
        decide de tout. Le test impose l'annulation exacte quand les deux sources
        se compensent, ce qu'une somme de modules ne peut pas produire.
        """
        c, Sd, Sev = self._aires()
        poids = np.sqrt(Sev / Sd)
        p_m = np.ones(4, dtype=complex)
        p_e = -np.ones(4, dtype=complex) / poids / 2.0     # 2 events
        total = MH.somme_champ_proche_bassreflex(p_m, p_e, Sd, Sev, n_events=2)
        self.assertLess(float(np.max(np.abs(total))), c['annulation_max'])

    def test_i4_events_mesures_separement(self):
        """Deux events releves un par un : la fonction accepte la liste.

        Deux events ne debitent pas forcement pareil (un seul peut siffler, ou
        etre a demi obstrue). Relever chacun est la bonne manip ; le code doit
        donc accepter N tableaux et N aires, et pas seulement "un event fois N".
        """
        c, Sd, Sev = self._aires()
        p_m = np.array([1.0 + 0j, 1.0 + 0j])
        p_1 = np.array([0.5 + 0j, 0.5 + 0j])
        p_2 = np.array([0.0 + 0j, 0.0 + 0j])               # event obstrue
        total = MH.somme_champ_proche_bassreflex(p_m, [p_1, p_2], Sd, Sev)
        attendu = p_m + np.sqrt(Sev / Sd) * p_1
        self.assertTrue(np.allclose(total, attendu, atol=1e-15))
        with self.assertRaises(ValueError):
            MH.somme_champ_proche_bassreflex(p_m, [p_1, p_2], Sd, [Sev])


class TestChargeCompositeDuPasseHaut(unittest.TestCase):
    """(i5) Les pavillons sont hors bande ACOUSTIQUE, pas hors charge ELECTRIQUE."""

    @staticmethod
    def _theta_medium():
        return [MH.MED_UNITAIRE_TYP[c] for c in ('Re', 'Le', 'Res', 'fs', 'Qms')]

    def test_i5_sans_branche_aigu_on_retrouve_le_bloc_en_serie(self):
        """R_aigu=None doit redonner EXACTEMENT deux mediums en serie.

        Un ajout de modele qui changerait le cas de base serait une regression
        silencieuse sur tout l'acte 3, qui optimise sur cette charge-la.
        """
        f = MH.grille_log(40.0, 250.0, 24)
        th = self._theta_medium()
        Z_nouveau = MH.Z_charge_passe_haut(f, th, n_medium=2, R_aigu=None)
        Z_ancien = MH.Z_serie_2hp(f, th, th)
        self.assertLess(float(np.max(np.abs(Z_nouveau - Z_ancien))), 1e-12)

    def test_i5_le_condensateur_est_une_question_a_trancher_pas_a_supposer(self):
        """Le chiffre qui dit si [[a verifier]] est critique ou secondaire.

        SANS condensateur, la branche aigu est un simple 4 ohm en parallele : la
        charge du passe-haut s'effondre sous le minimum de 4 ohm admis par le
        t.amp E-800, et les pavillons prennent du 100 Hz a pleine puissance --
        risque MATERIEL pendant les balayages. AVEC un condensateur de 6,8 uF
        l'effet subsiste (de l'ordre de -19 %) parce que |Z| du bloc medium au
        voisinage de sa propre resonance n'est PAS petit devant les 117 ohm de la
        branche : l'intuition "un condensateur, c'est un circuit ouvert en bas"
        est donc fausse ici, et c'est ce test qui l'empeche de revenir.
        """
        c = contexte.critere('i_bassreflex', 'charge_passe_haut')
        e = MH.effet_branche_aigu(self._theta_medium(), f_ref=c['f_Hz'],
                                  R_aigu=c['R_aigu_ohm'], C_aigu=c['C_aigu_F'],
                                  n_aigu=c['n_aigu'])
        self.assertLess(e['ecart_sans_pct'], -c['chute_min_sans_condensateur_pct'],
                        'sans condensateur : %.1f %%' % e['ecart_sans_pct'])
        self.assertLess(e['module_sans_condensateur'], c['Zin_minimal_ampli_ohm'],
                        'la charge devrait tomber sous le minimum de l amplificateur')
        self.assertLess(e['ecart_avec_pct'], -c['effet_min_avec_condensateur_pct'],
                        'avec condensateur : effet annonce nul, %.1f %%' % e['ecart_avec_pct'])
        self.assertGreater(e['ecart_avec_pct'], -c['effet_max_avec_condensateur_pct'],
                           'avec condensateur : effet aberrant, %.1f %%' % e['ecart_avec_pct'])

    def test_i5_plus_le_condensateur_est_gros_plus_il_charge(self):
        """Monotonie : |Z| du bloc decroit quand C croit, et tend vers le cas sans C.

        C'est la seule facon de verifier que le condensateur est bien EN SERIE
        avec les pavillons et non en parallele -- une erreur de topologie donnerait
        la monotonie inverse, avec des nombres tout aussi plausibles.
        """
        th = self._theta_medium()
        modules = [MH.effet_branche_aigu(th, 100.0, R_aigu=8.0, C_aigu=C,
                                         n_aigu=2)['module_avec_condensateur']
                   for C in (1e-6, 3.3e-6, 6.8e-6, 10e-6, 47e-6)]
        self.assertTrue(all(b < a for a, b in zip(modules, modules[1:])),
                        'monotonie rompue : %s' % np.round(modules, 3))
        sans = MH.effet_branche_aigu(th, 100.0, R_aigu=8.0, C_aigu=None,
                                     n_aigu=2)['module_sans_condensateur']
        self.assertGreater(modules[-1], sans)

    def test_i5_condensateur_commun_aux_deux_pavillons(self):
        """Un seul condensateur pour les deux pavillons n'est pas deux condensateurs.

        Les deux cablages existent dans le commerce et ne donnent pas la meme
        charge : c'est encore un [[a verifier]], et le code doit pouvoir decrire
        les deux plutot que d'en imposer un en silence.
        """
        f = np.array([100.0])
        th = self._theta_medium()
        chacun = MH.Z_charge_passe_haut(f, th, 2, R_aigu=8.0, C_aigu=6.8e-6, n_aigu=2)
        commun = MH.Z_charge_passe_haut(f, th, 2, R_aigu=8.0, C_aigu=None, n_aigu=2,
                                        C_commun=6.8e-6)
        self.assertGreater(abs(commun[0]), abs(chacun[0]),
                           'un condensateur commun protege PLUS : sa reactance n est '
                           'pas divisee par deux')


class TestBudgetSystematiqueSurHuitParametres(unittest.TestCase):
    """(i6) L'incertitude de type B doit suivre le modele, pas rester a cinq lignes."""

    def test_i6_identite_d_echelle_du_modele_bass_reflex(self):
        """Multiplier R_e, L_e et R_es par (1+d) multiplie Z par (1+d) -- exactement.

        C'est ce theoreme, et lui seul, qui autorise a dire que f_s, f_b, Q_ms,
        Q_l et alpha sont IMMUNISES contre une erreur d'echelle sur R_ref. En
        caisse close il est evident ; en bass-reflex il ne l'est pas, puisque la
        branche event porte trois parametres de plus -- mais toute cette branche
        est proportionnelle a R_es (L_ceb = L_ces/alpha avec L_ces = R_es/(w_s
        Q_ms), C_peb = 1/(w_b^2 L_ceb), R_p = w_b L_ceb/Q_l), donc l'identite
        tient. On le VERIFIE ici au lieu de l'affirmer.
        """
        c = contexte.critere('i_bassreflex', 'budget_systematique')
        noms = list(T.NOMS_THETA['bassreflex8'])
        f = MH.grille_log(10.0, 1000.0, 24)
        theta = dict(zip(noms, THETA_BR8))
        for d in (0.01, 0.03, -0.02):
            mis_a_l_echelle = dict(theta)
            for nom in c['herites']:
                mis_a_l_echelle[nom] = theta[nom] * (1.0 + d)
            ecart = np.max(np.abs((1.0 + d) * MH.Z_bassreflex8(f, **theta)
                                  - MH.Z_bassreflex8(f, **mis_a_l_echelle)))
            with self.subTest(d=d):
                self.assertLess(float(ecart), c['identite_echelle_max_ohm'])

    def test_i6_le_budget_porte_sur_les_huit_parametres(self):
        """Huit parametres ajustes, huit lignes de budget -- et les bonnes immunites.

        Le defaut de ``incertitudes.budget_parametres_ts`` porte sur les CINQ noms
        de Thiele-Small. Laisse tel quel, il rendait un tableau a cinq lignes qu'on
        aurait cru complet -- ou, pire, attribuait a alpha, f_b et Q_l la
        sensibilite par defaut de 1,0, c'est-a-dire une incertitude inventee.
        """
        c = contexte.critere('i_bassreflex', 'budget_systematique')
        u_A = np.array(THETA_BR8, float) * 0.01
        budget, texte = T.budget_systematique(np.array(THETA_BR8, float), u_A,
                                              modele='bassreflex8', u_rel_R_ref=0.01)
        self.assertIsNotNone(budget, texte)
        self.assertEqual(len(budget), c['n_lignes_budget'])
        for nom in c['immunises']:
            with self.subTest(parametre=nom):
                self.assertTrue(budget[nom]['immunise'])
                self.assertEqual(budget[nom]['u_B'], 0.0)
        for nom in c['herites']:
            with self.subTest(parametre=nom):
                self.assertFalse(budget[nom]['immunise'])
                self.assertGreater(budget[nom]['u_B'], 0.0)
        # La ligne de synthese du tableau doit citer TOUS les immunises du budget
        # rendu, et pas la liste figee des cinq parametres de Thiele-Small.
        synthese = [l for l in texte.splitlines() if l.startswith('Immunises :')]
        self.assertEqual(len(synthese), 1, texte)
        for nom in c['immunises']:
            self.assertIn(nom, synthese[0])

    def test_i6_le_pipeline_rend_une_incertitude_composee(self):
        """``identifier`` doit rendre u_B et u_composee, pas None, sur huit parametres.

        C'est ce None qui a fait tomber l'etape 7 de ``tout_refaire.py`` le jour
        du passage en bass-reflex : la chaine s'arretait sur ``iteration over a
        0-d array``. Un test vaut mieux qu'un souvenir.
        """
        f, mod, phi, u_mod, u_phi = _courbe_bassreflex()
        with contexte.sans_avertissement():
            res = T.identifier(f, mod, phi, u_mod, u_phi, modele='auto', n_mc=20,
                               n_retrait=0, n_multi=0, jack=False, bavard=False,
                               statut_donnees='SYNTHETIQUES (bass-reflex, test i6)')
        self.assertIsNotNone(res['u_B'])
        self.assertIsNotNone(res['u_composee'])
        self.assertEqual(len(res['u_composee']), len(res['theta']))
        self.assertTrue(np.all(np.asarray(res['u_composee'], float)
                               >= np.asarray(res['u_A'], float) - 1e-15))


if __name__ == '__main__':
    unittest.main(verbosity=2)
