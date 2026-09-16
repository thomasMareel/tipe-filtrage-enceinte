"""Rejoue TOUTE la chaine d'analyse dans l'ordre du recit -- § 09.8.

    python analyse/tout_refaire.py [--rapide] [--sans-figures]

Interface GELEE (§ 09.8) : code de retour 0 si tout passe, 1 au premier
echec, avec le nom de l'etape sur stderr. `--rapide` reduit le Monte-Carlo de
400 000 a 20 000 tirages (et le dit au journal) pour la boucle de developpement ;
LES CHIFFRES DE L'ORAL SE PRODUISENT SANS --rapide. `--sans-figures` saute la
generation des SVG/PNG, qui est la seule etape qui demande matplotlib.

POURQUOI CE FICHIER EXISTE
--------------------------
Principe 3 du § 09.1 : "tout chiffre montre au jury est regenerable par
une commande". Sans lui, un chiffre de diapositive est inverifiable -- on ne sait
plus quelle version du code, quelles donnees ni quelle graine l'ont produit. Avec
lui, la reponse a "d'ou sort ce 96,86 Hz ?" est une ligne de commande, et le
journal (resultats/journal.txt) porte la date, les versions, les graines et les
empreintes SHA-256 des entrees.

L'ORDRE N'EST PAS DECORATIF
---------------------------
1. Les TESTS d'abord. Si un test tombe, aucun chiffre n'est plus garanti : on
   s'arrete avant d'avoir produit un seul JSON. C'est la difference entre "la
   chaine a tourne" et "la chaine a tourne juste".
2. Les DECISIONS GELEES (criteres_geles.json), recopiees integralement au
   journal : c'est ce qui rend VERIFIABLE l'affirmation "criteres geles avant les
   mesures", socle d'honnetete du sujet (§ 08).
3. Les MESURES, avec leur empreinte SHA-256. Un JSON perime dans le depot est
   sinon indiscernable d'un JSON a jour.
4. La PORTE DE VALIDATION sur 8 ohm resistif, POUR LES DEUX CIBLES (decision D2) :
   sans contrainte E12, l'optimiseur continu DOIT rendre le Butterworth (ou le
   Linkwitz-Riley) analytique. C'est un theoreme ; tant qu'il echoue, on n'achete
   rien et le reste de la chaine ne veut rien dire.
5. L'ACTE 2 (probleme inverse) puis l'ACTE 3 (optimisation), chacun verifiant
   l'existence de sa sortie amont plutot que de recalculer en silence.
6. Les INCERTITUDES, les FIGURES, et le JOURNAL.

STATUT DES DONNEES AU 2026-09-14
--------------------------------
AUCUNE MESURE DE L'ENCEINTE N'EXISTE. La chaine tourne sur le fichier
`mesures/exemple_synthetique_sub.csv`, engendre par un modele de Thiele-Small et
etiquete SYNTHETIQUE dans son en-tete ; tout nombre qui en sort herite de cette
etiquette jusque dans les JSON produits. Le jour de la phase 1, il suffit de
deposer les vrais CSV dans `mesures/` : rien d'autre ne change.

Ce module n'a pas de fonction publique destinee a etre importee ailleurs : il
orchestre, il ne calcule pas. Toute la physique vit dans les huit modules du
contrat (§ 09.4).
"""

import io
import json
import os
import subprocess
import sys
import time
import traceback
import warnings
from collections import OrderedDict

_ICI = os.path.dirname(os.path.abspath(__file__))
_RACINE = os.path.dirname(_ICI)                 # racine du depot (contient .git, css/)
if _ICI not in sys.path:                        # importable depuis n'importe ou
    sys.path.insert(0, _ICI)

import numpy as np                              # noqa: E402

import filtre as F                              # noqa: E402  acte 3 : reseaux, cibles
import incertitudes as N                        # noqa: E402  GUM et Monte-Carlo
import io_mesures as IO                         # noqa: E402  CSV, criteres geles
import modele_hp as MH                          # noqa: E402  Z_ts, grilles, MED_TYP
import energie as EN                            # noqa: E402  satellite sobriete (§ 06)
import optim as O                               # noqa: E402  E12, cout, portes 8 ohm
import self_bobine as SB                        # noqa: E402  DCR, masse, prix (satellite)
import ts_fit as TS                             # noqa: E402  acte 2 : probleme inverse


DOSSIER_RESULTATS = os.path.join(_ICI, 'resultats')
DOSSIER_FIGURES = os.path.join(DOSSIER_RESULTATS, 'figures')
DOSSIER_MESURES = IO.DOSSIER_MESURES

# Les deux SEULS fichiers de resultats/ qui sont versionnes (regle .gitignore de
# le § 09.8) : ce sont les chiffres cites a l'oral, ils portent donc leur
# provenance (SHA-256 des entrees, commit git, graine, date).
JSON_TS = os.path.join(DOSSIER_RESULTATS, 'parametres_ts.json')
JSON_DESIGN = os.path.join(DOSSIER_RESULTATS, 'design_optimise.json')
JOURNAL = os.path.join(DOSSIER_RESULTATS, 'journal.txt')

# Graine unique de toute la chaine. Un Monte-Carlo non reproductible n'est pas un
# resultat (§ 09.8) : elle est ecrite au journal et dans les deux JSON.
GRAINE = 20260914

# Cible de sommation : D2 est VOLONTAIREMENT reportee apres la phase 1, donc la
# cible est un PARAMETRE, jamais une constante. Tant qu'elle n'est pas gelee, la
# chaine produit le recit sur 'butterworth' ET rejoue la porte de validation sur
# les deux cibles ('butterworth' et 'lr2').
CIBLE_DEFAUT = 'butterworth'
CIBLES_PORTE = ('butterworth', 'lr2')

# Design "catalogue" : Butterworth 2e ordre 100 Hz calcule sur 8 ohm RESISTIFS.
# C'est le point de depart a battre, pas un resultat.
DESIGN_CATALOGUE = dict(L1=18e-3, C1=150e-6, C2=150e-6, L2=18e-3)

# Tolerances catalogue, DEMI-LARGEURS de loi rectangulaire (convention GUM gelee
# § 09.6 : u = a/racine(3)).
TOL_L = 0.10
TOL_C = 0.20


class EchecEtape(RuntimeError):
    """Une etape a echoue : la chaine s'arrete la, code de retour 1."""


# ==================================================================================
# 1. Journal
# ==================================================================================

class Journal(object):
    """Ecrit a l'ecran ET en memoire, pour finir dans resultats/journal.txt.

    Un journal qui n'existe qu'a l'ecran disparait avec la fenetre : ce qu'on
    veut pouvoir relire six mois plus tard, c'est la date, les versions, les
    graines et les empreintes des entrees qui ont produit un chiffre de
    diapositive.
    """

    def __init__(self, bavard=True):
        self.lignes = []
        self.bavard = bavard
        self.t0 = time.time()

    def __call__(self, texte=''):
        for ligne in str(texte).splitlines() or ['']:
            self.lignes.append(ligne)
            if self.bavard:
                print(ligne)
        if self.bavard:
            sys.stdout.flush()

    def titre(self, numero, texte):
        """Un cartouche d'etape, avec le temps ecoule depuis le debut."""
        self('')
        self('=' * 78)
        self('[%s] %-58s t+%6.1f s' % (numero, texte, time.time() - self.t0))
        self('=' * 78)

    def bloc(self, texte, prefixe='  '):
        """Recopie un texte multiligne en le decalant (JSON, tableaux)."""
        for ligne in str(texte).splitlines():
            self(prefixe + ligne)

    def ecrire(self, chemin):
        """Fichier UTF-8, fins de ligne LF (convention du depot)."""
        _assurer_dossier(os.path.dirname(chemin))
        with open(chemin, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\n'.join(self.lignes) + '\n')
        return chemin


def _assurer_dossier(chemin):
    if chemin and not os.path.isdir(chemin):
        os.makedirs(chemin)
    return chemin


def _ecrire_json(chemin, contenu):
    """JSON UTF-8, LF, indente : il est relu par un humain autant que par un script."""
    _assurer_dossier(os.path.dirname(chemin))
    with open(chemin, 'w', encoding='utf-8', newline='\n') as fh:
        json.dump(TS._jsonable(contenu), fh, ensure_ascii=False, indent=2)
        fh.write('\n')
    return chemin


def _exiger(chemin, etape_amont):
    """Chaque etape verifie l'existence de sa sortie AMONT (§ 09.8).

    Plutot que de recalculer en silence ce qui manque -- et de masquer ainsi une
    etape qui n'a pas tourne -- on echoue explicitement en nommant l'etape qui
    aurait du produire le fichier.
    """
    if not os.path.isfile(chemin):
        raise EchecEtape('%s est introuvable : l etape "%s" n a pas produit sa sortie.'
                         % (chemin, etape_amont))
    return chemin


def _mm(x):
    return x * 1e3


def _uf(x):
    return x * 1e6


def _design_lisible(design):
    return ('%.4g mH / %.4g uF | %.4g uF / %.4g mH'
            % (_mm(design['L1']), _uf(design['C1']),
               _uf(design['C2']), _mm(design['L2'])))


# ==================================================================================
# 2. Etapes
# ==================================================================================

def etape_1_tests(jrn, rapide):
    """Les tests de non-regression AVANT tout calcul (§ 09.6).

    On relance la commande gelee, telle qu'elle est documentee, dans un
    sous-processus : c'est la meme que celle que Thomas tape a la main, et elle
    part d'un interpreteur propre -- un module deja importe par la chaine ne peut
    donc pas masquer une erreur d'import. Si un test tombe, ON NE VA PAS PLUS
    LOIN : aucun chiffre n'est plus garanti.
    """
    jrn.titre('1/8', 'Tests de non-regression (unittest)')
    commande = [sys.executable, '-m', 'unittest', 'discover', '-s', 'analyse/tests']
    jrn('commande : %s' % ' '.join(commande))
    jrn('dossier   : %s' % _RACINE)
    t0 = time.time()
    proc = subprocess.run(commande, cwd=_RACINE, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT)
    sortie = proc.stdout.decode('utf-8', 'replace')
    duree = time.time() - t0
    # unittest ecrit son compte rendu sur stderr : on ne garde que la fin, le
    # detail vit dans la sortie de la commande lancee a la main.
    queue = [l for l in sortie.splitlines() if l.strip()][-6:]
    jrn.bloc('\n'.join(queue))
    jrn('duree : %.1f s ; code de retour %d' % (duree, proc.returncode))
    if proc.returncode != 0:
        jrn.bloc(sortie)
        raise EchecEtape('la suite unittest a echoue (code %d) : aucun chiffre '
                         'de la chaine n est garanti.' % proc.returncode)
    n_tests = 0
    for ligne in sortie.splitlines():
        if ligne.startswith('Ran ') and ' test' in ligne:
            n_tests = int(ligne.split()[1])
    jrn('%d tests au vert.' % n_tests)
    return dict(n_tests=n_tests, duree_s=duree, commande=' '.join(commande))


def etape_2_criteres(jrn):
    """Lit criteres_geles.json et le RECOPIE INTEGRALEMENT au journal.

    Principe 4 du § 09.1 : "les decisions gelees sont un fichier, pas une
    intention". Recopier le fichier au journal, c'est ce qui permet, plus tard, de
    prouver que les poids de J n'ont pas ete retouches apres les mesures.

    Au 2026-09-14 AUCUNE decision n'est gelee : la chaine continue, mais elle
    l'ecrit noir sur blanc et aucun chiffre produit ce jour-la n'est un chiffre
    d'oral.
    """
    jrn.titre('2/8', 'Decisions gelees (criteres_geles.json)')
    chemin = IO.CHEMIN_CRITERES
    _exiger(chemin, 'phase 0 : gel des criteres')
    sha = TS.empreinte(chemin)
    jrn('fichier   : %s' % chemin)
    jrn('SHA-256   : %s' % sha)
    criteres = IO.lire_criteres_geles(chemin, exiger_geles=False)
    non_geles = criteres.get('_non_geles', [])
    meta = criteres.get('meta', {})
    jrn('date_gel  : %s ; commit_gel : %s'
        % (meta.get('date_gel', '?'), meta.get('commit_gel', '?')))
    if non_geles:
        jrn('')
        jrn('AVERTISSEMENT : %d decision(s) NON GELEE(S). La chaine tourne pour'
            % len(non_geles))
        jrn('eprouver le code, mais AUCUN chiffre produit aujourd hui n est un')
        jrn('chiffre d oral. Voir DECISIONS-PHASE-0.md.')
        for cle in non_geles:
            jrn('  - %s' % cle)
    else:
        jrn('toutes les decisions sont gelees.')
    jrn('')
    jrn('--- recopie integrale de criteres_geles.json -------------------------------')
    with open(chemin, encoding='utf-8') as fh:
        jrn.bloc(fh.read().rstrip('\n'), prefixe='| ')
    jrn('--- fin de la recopie ------------------------------------------------------')

    # Les poids de J : seul chemin autorise pour des poids venus d'ailleurs que de
    # optim.W_PROPOSE. D5 n'etant pas gelee, on prend W_SANITY (w_euro = w_W = 0),
    # c'est-a-dire un classement PUREMENT acoustique.
    #
    # CORRECTION DE RELECTURE (2026-09-14). Le commentaire qui tenait ici affirmait
    # que "aucun modele de prix ni de DCR n'est injecte" et que ce reglage etait "le
    # plus defavorable au design optimise". Les deux etaient FAUX, et ils melangeaient
    # deux choses independantes :
    #   * w_euro = w_W = 0 retire les euros et les watts de J. Cela favorise bien le
    #     catalogue, qui est la self la moins chere ;
    #   * mais la DCR n'est pas seulement un terme de cout. Elle entre dans H_pb et
    #     H_ph -- elle amortit la resonance de la cellule grave et abaisse le niveau
    #     de la voie -- donc elle change les termes SOMME et VOIES, ceux qui pesent 1.
    #     Les ignorer PENALISE le catalogue. C'est pourquoi l'etape 6 enumere
    #     desormais AVEC et SANS DCR, et journalise l'ecart.
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        _w_fichier, source_poids = O.poids_geles(exiger_geles=False, bavard=False)
    w = dict(O.W_SANITY)
    jrn('')
    jrn('poids de J lus par optim.poids_geles : %s' % source_poids)
    jrn('poids EFFECTIVEMENT utilises (D5 non gelee) : W_SANITY = %s' % w)
    jrn('  -> w_euro = w_W = 0 : ni euros ni watts dans J. CE reglage-la favorise le')
    jrn('     catalogue, qui est la self la moins chere.')
    jrn('  -> le modele de DCR, lui, est une question SEPAREE : la DCR entre dans')
    jrn('     H_pb et H_ph, donc dans les termes somme et voies, qui pesent 1. La')
    jrn('     supposer nulle ne "neutralise" rien, cela change le classement. L etape')
    jrn('     6 enumere donc les deux variantes (selfs ideales / selfs de Brooks) et')
    jrn('     ecrit l ecart : c est lui, le resultat.')
    jrn('  -> le nom W_SANITY designe les poids FIXES du sanity check du § 04.7, PAS')
    jrn('     la decision D5 du projet, qui est encore ouverte. Deux sens du mot')
    jrn('     "gele" dans le meme dossier seraient une contradiction d oral.')
    return dict(chemin=chemin, sha256=sha, criteres=criteres, non_geles=non_geles,
                w=w, source_poids=source_poids)


def etape_3_mesures(jrn):
    """Inventaire de mesures/, empreinte SHA-256 de chaque fichier, et validation.

    "Ce qui est dans mesures/ a coute une seance de banc, ce qui est dans
    resultats/ coute dix secondes" (§ 09.2) : ce dossier est en LECTURE
    SEULE pour toute la chaine, et rien ici ne le reecrit.
    """
    jrn.titre('3/8', 'Donnees brutes (mesures/)')
    _assurer_dossier(DOSSIER_MESURES)
    fichiers = sorted(n for n in os.listdir(DOSSIER_MESURES) if n.endswith('.csv'))
    if not fichiers:
        raise EchecEtape('aucun CSV dans %s : la chaine n a rien a depouiller.'
                         % DOSSIER_MESURES)
    inventaire = []
    for nom in fichiers:
        chemin = os.path.join(DOSSIER_MESURES, nom)
        sha = TS.empreinte(chemin)
        d, meta = IO.lire_mesure(chemin)
        erreurs, avertissements = IO.valider_mesure(d, meta)
        statut = meta.get('statut_donnees') or meta.get('dipole', '?')
        jrn('%s' % nom)
        jrn('  SHA-256 : %s' % sha)
        jrn('  %d points de %.4g a %.4g Hz ; format v%s'
            % (len(d), d['f_Hz'].min(), d['f_Hz'].max(), meta.get('version_format', '?')))
        jrn('  statut  : %s' % statut)
        for e in erreurs:
            jrn('  ERREUR  : %s' % e)
        for a in avertissements:
            jrn('  note    : %s' % a)
        if erreurs:
            raise EchecEtape('%s : %d erreur(s) de format, le fichier ne doit pas '
                             'servir tel quel.' % (nom, len(erreurs)))
        inventaire.append(dict(fichier=nom, sha256=sha, n_points=len(d),
                               f_min=float(d['f_Hz'].min()), f_max=float(d['f_Hz'].max()),
                               statut=statut, avertissements=avertissements))

    # Le fichier du sub est celui sur lequel tourne le recit. Tant qu'il n'y a
    # qu'une serie, c'est l'exemple synthetique ; le jour de la phase 1, c'est le
    # CSV du 18 pouces en caisse qui prendra sa place (meme nom de variable).
    principal = IO.CHEMIN_EXEMPLE if os.path.isfile(IO.CHEMIN_EXEMPLE) else \
        os.path.join(DOSSIER_MESURES, fichiers[0])
    jrn('')
    jrn('serie retenue pour le recit : %s' % os.path.basename(principal))
    return dict(inventaire=inventaire, principal=principal,
                sha256_principal=TS.empreinte(principal))


def etape_4_porte_8ohm(jrn):
    """PORTE DE VALIDATION sur 8 ohm resistif pur, POUR LES DEUX CIBLES (D2).

    Sur une charge resistive pure, sans DCR ni penalite, le probleme
    d'optimisation CONTINU est exactement celui du catalogue : c'est un theoreme
    (§ 09.6, test b1). Si l'optimiseur ne retrouve pas le Butterworth
    analytique a 1e-6 pres, c'est un bug -- et on n'achete rien.

    Le passage a E12 (test b2), lui, n'est PAS un theoreme : c'est une projection
    sur une grille, et la grille n'est pas stable par les symetries du probleme.
    Il est verifie ici comme test de NON-REGRESSION de la fonction de cout.

    Formulation a tenir devant le jury : "sur 8 ohm le probleme continu est celui
    du catalogue ; le passage a E12 peut legitimement choisir un voisin different
    d'une voie a l'autre, ce n'est pas un bug mais une propriete de la grille."
    """
    jrn.titre('4/8', 'Porte de validation 8 ohm resistif -- les DEUX cibles (D2)')
    jrn('D2 (cible de sommation) est VOLONTAIREMENT reportee : la cible est un')
    jrn('parametre du code. La porte est donc jouee sur butterworth ET sur lr2.')
    jrn('')
    tampon = io.StringIO()
    sortie_reelle, sys.stdout = sys.stdout, tampon
    try:
        resultats = O.sanity_check_complet(bavard=True)
    except O.EchecSanityCheck as exc:
        sys.stdout = sortie_reelle
        jrn.bloc(tampon.getvalue().rstrip('\n'))
        raise EchecEtape('porte de validation 8 ohm en echec : %s' % exc)
    finally:
        sys.stdout = sortie_reelle
    jrn.bloc(tampon.getvalue().rstrip('\n'))
    for r in resultats:
        if not r.get('ok', True):
            raise EchecEtape('porte de validation 8 ohm : %s' % r)
    jrn('')
    jrn('les %d portes sont franchies : le code retrouve les formules analytiques'
        % len(resultats))
    jrn('sur charge resistive, pour les deux cibles. On peut continuer.')
    return dict(portes=[{k: v for k, v in r.items() if not isinstance(v, np.ndarray)}
                        for r in resultats])


def etape_5_ajustement(jrn, mesures, rapide):
    """ACTE 2 -- probleme inverse : Z(f) mesuree -> parametres de Thiele-Small.

    Passe par le pipeline complet ts_fit.identifier_fichier : aiguillage
    clos/bass-reflex D'APRES LA COURBE (le type de caisse n'est pas su, section
    09), multi-depart, incertitudes de type A et de type B, diagnostics de
    residus, verdicts. Produit resultats/parametres_ts.json, qui porte la
    COVARIANCE COMPLETE -- sans elle, l'acte 3 repartirait de cinq incertitudes
    independantes, exactement l'erreur que denonce le § 03.5.
    """
    jrn.titre('5/8', 'Acte 2 : identification de Thiele-Small (probleme inverse)')
    chemin = mesures['principal']
    jrn('entree : %s' % os.path.basename(chemin))
    jrn('SHA-256 de l entree : %s' % mesures['sha256_principal'])
    t0 = time.time()
    resultat = TS.identifier_fichier(chemin, modele='auto', bavard=False,
                                     graine=GRAINE, rapide=rapide)
    duree = time.time() - t0
    jrn('')
    jrn.bloc(TS.texte_resultat(resultat))
    jrn('')
    jrn('duree : %.1f s%s' % (duree, ' (--rapide : tirages reduits)' if rapide else ''))
    verdicts = resultat.get('validation', {})
    echecs = [nom for nom, v in verdicts.items()
              if isinstance(v, dict) and v.get('ok') is False]
    if echecs:
        jrn('criteres de validation en echec : %s' % ', '.join(echecs))
    resultat['provenance']['graine'] = GRAINE
    TS.ecrire_parametres_ts(resultat, JSON_TS)
    jrn('ecrit : %s' % JSON_TS)
    jrn('statut des donnees : %s' % resultat.get('statut_donnees'))
    return dict(resultat=resultat, chemin_json=JSON_TS, duree_s=duree, echecs=echecs)


def etape_6_optimisation(jrn, criteres, fit, rapide):
    """ACTE 3 -- enumeration exhaustive E12 sur la charge IDENTIFIEE.

    C'est la continuite du recit : on optimise sur la charge qu'on vient de
    mesurer, pas sur une datasheet. 331 776 combinaisons (24^4) sont evaluees par
    blocs -- le minimum trouve est le minimum GLOBAL SUR LA GRILLE.

    Trois controles accompagnent le gagnant, et aucun n'est decoratif :
      * l'optimum n'est pas sur un BORD de la grille (sinon la grille est trop
        etroite et le chiffre ne veut rien dire) ;
      * le PLATEAU : combien de designs sont a 1 % de J. La derniere marche E12 ne
        separe souvent rien -- il faut parler d'une FAMILLE de designs ;
      * les CONTRAINTES physiques (tenue en tension, courant, min|Z_in| vu par
        l'ampli), qui peuvent disqualifier un design AVANT toute comparaison de
        fidelite.
    """
    jrn.titre('6/8', 'Acte 3 : optimisation E12 sur la charge identifiee')
    _exiger(fit['chemin_json'], 'etape 5 : ajustement')
    res_fit = fit['resultat']
    w = criteres['w']
    cible_nom = CIBLE_DEFAUT

    f = F.grille_critere()                         # 40-250 Hz, 24 points/octave
    Zs = TS.evaluer(res_fit['modele'], f, res_fit['theta'])
    Zm = MH.Z_depuis_jeu(f, MH.MED_TYP)
    jrn('charge grave  : parametres IDENTIFIES a l acte 2 (modele %s)'
        % res_fit['modele'])
    jrn('charge medium : %s' % MH.MED_TYP['nom'])
    jrn('                %s' % MH.MED_TYP['avertissement'])
    # LES PAVILLONS SONT DANS LA CHARGE, MEME S'ILS NE RAYONNENT PAS A 100 Hz.
    # Constat du 2026-09-16 : deux pavillons d'ultra-aigu sont cables EN PARALLELE
    # du bloc medium. Hors perimetre ACOUSTIQUE (rien a 100 Hz), DANS le perimetre
    # ELECTRIQUE (c'est ce que le passe-haut entraine). Le Zm ci-dessus les ignore
    # encore -- il le faut bien, on ne sait pas s'il y a un condensateur en serie
    # avec eux -- mais taire l'enjeu serait pire que le chiffrer : on le chiffre.
    th_med = [MH.MED_UNITAIRE_TYP[c] for c in ('Re', 'Le', 'Res', 'fs', 'Qms')]
    ea = MH.effet_branche_aigu(th_med, f_ref=100.0, R_aigu=8.0, C_aigu=6.8e-6,
                               n_aigu=2)
    jrn('                pavillons d ultra-aigu EN PARALLELE : hors bande acoustique,')
    jrn('                mais DANS la charge electrique. Effet sur |Z| a 100 Hz')
    jrn('                (modele, 2 pavillons de 8 ohm) : bloc seul %.2f ohm ;'
        % ea['module_bloc_seul'])
    jrn('                avec condensateur 6,8 uF %.2f ohm (%+.0f %%) ; SANS '
        'condensateur' % (ea['module_avec_condensateur'], ea['ecart_avec_pct']))
    jrn('                %.2f ohm (%+.0f %%), sous le minimum de 4 ohm du E-800.'
        % (ea['module_sans_condensateur'], ea['ecart_sans_pct']))
    jrn('                [[a verifier]] : y a-t-il ce condensateur ? La mesure de')
    jrn('                phase 1 se fait pavillons CONNECTES dans les deux cas.')
    jrn('bande du critere : %.4g-%.4g Hz, %d points ; cible = %s (D2 non gelee)'
        % (f[0], f[-1], f.size, cible_nom))
    jrn('rapport max/min de |Z| du grave sur la bande : %.2f'
        % (np.abs(Zs).max() / np.abs(Zs).min()))
    jrn('')
    jrn(O.decrire_espace())

    # --- LES SELFS NE SONT PAS PARFAITES, ET C'EST LE CŒUR DU SUJET ---------------
    # CORRECTION DE RELECTURE (2026-09-14). L'enumeration tournait ici sans argument
    # dcr=, donc cout() prenait son defaut dcr=None et evaluait les 331 776
    # combinaisons avec r1 = r2 = 0 : le design annonce etait l'optimum d'un probleme
    # ou les selfs sont PARFAITES, alors que dix lignes plus bas le meme journal
    # chiffrait "self L1 : DCR 1,85 ohm". Or la DCR n'agit pas que par le terme de
    # pertes w_W (qui vaut 0 ici) : elle entre dans H_pb et H_ph, donc dans les
    # termes somme et voies, qui pesent 1. Le § 09.4 est explicite : "l'argument dcr
    # vient de self_bobine.dcr_de_L : c'est ce couplage -- et lui seul -- qui fait du
    # satellite self optimale une piece du recit plutot qu'une annexe decorative".
    #
    # D6 (le modele de DCR/prix) n'etant PAS gelee, on ne choisit pas a la place de
    # Thomas : on produit les DEUX enumerations et on ecrit l'ecart. C'est un
    # resultat, pas une complication -- et c'est la reponse a la question de jury la
    # plus previsible sur ce sujet.
    dcr_brooks, _prix_L_brooks = O.fabriques_self(d_fil=1.4e-3)
    variantes_dcr = OrderedDict([
        ('selfs ideales (r = 0)', None),
        ('selfs de Brooks, fil 1,4 mm (D6 non gelee)', dcr_brooks),
    ])

    resultats_dcr = OrderedDict()
    for nom_v, modele_dcr in variantes_dcr.items():
        t0 = time.time()
        r_v = O.enumere_e12(f, Zs, Zm, cible_nom=cible_nom, w=w, dcr=modele_dcr,
                            bavard=False)
        r_v['duree_s'] = time.time() - t0
        r_v['dcr'] = modele_dcr
        resultats_dcr[nom_v] = r_v
        jrn('%-44s -> %s (J = %.4f, %d comb. en %.2f s)'
            % (nom_v, _design_lisible(O.design_de(r_v)), r_v['J'],
               r_v['n_combinaisons'], r_v['duree_s']))

    # Le RECIT s'appuie sur le modele physique complet : selfs reelles. Le cas
    # "selfs ideales" reste calcule et journalise, comme temoin.
    nom_retenu = 'selfs de Brooks, fil 1,4 mm (D6 non gelee)'
    resultat = resultats_dcr[nom_retenu]
    dcr = resultat['dcr']
    duree = resultat['duree_s']
    design = O.design_de(resultat)
    kw_cout = dict(cible_nom=cible_nom, w=w, dcr=dcr)

    # L'ecart entre les deux variantes EST le resultat du couplage : on le chiffre.
    ideal = resultats_dcr['selfs ideales (r = 0)']
    design_ideal = O.design_de(ideal)
    J_ideal_reevalue = O.termes_du_design(design_ideal, f, Zs, Zm, **kw_cout)['J']
    jrn('')
    jrn('ECART ENTRE LES DEUX MODELES DE SELF (ce n est pas un detail) :')
    jrn('  le gagnant a selfs IDEALES, reevalue avec sa VRAIE DCR, vaut J = %.4f'
        % J_ideal_reevalue)
    jrn('  le gagnant a selfs REELLES vaut J = %.4f' % resultat['J'])
    if _design_lisible(design_ideal) != _design_lisible(design):
        jrn('  -> les deux designs DIFFERENT : supposer les selfs parfaites change')
        jrn('     les composants achetes, pas seulement le chiffre de J.')
    else:
        jrn('  -> les deux designs coincident ici ; l ecart ne porte que sur J.')
    jrn('  raison physique : la DCR amortit la resonance de la cellule grave (§ 04.2)')
    jrn('  et abaisse le niveau de la voie -- deux effets qui vivent dans les termes')
    jrn('  somme et voies, PAS dans le terme de pertes (w_W = 0 ici).')
    jrn('')
    jrn('design retenu pour la suite du recit : %s' % nom_retenu)
    jrn('  DCR : r1 = %.2f ohm, r2 = %.2f ohm' % (dcr(design['L1']), dcr(design['L2'])))
    jrn('')
    jrn('OPTIMISE  : ' + O.resume_design(design, f, Zs, Zm, **kw_cout))
    jrn('CATALOGUE : ' + O.resume_design(DESIGN_CATALOGUE, f, Zs, Zm, **kw_cout))
    termes_opt = O.termes_du_design(design, f, Zs, Zm, **kw_cout)
    termes_cat = O.termes_du_design(DESIGN_CATALOGUE, f, Zs, Zm, **kw_cout)

    ok_bord, avertissements = O.verifier_optimum_interieur(resultat)
    jrn('')
    if ok_bord:
        jrn('optimum interieur a la grille (test (d)) : OK')
    else:
        for a in avertissements:
            jrn('BORD DE GRILLE : %s' % a)

    plateau = O.analyser_plateau(resultat)
    jrn('')
    jrn('plateau : ' + plateau['verdict'])
    jrn('classement (les 5 meilleurs) :')
    for d in plateau['classement'][:5]:
        jrn('  %d. %s   J = %.4f' % (d['rang'], _design_lisible(d), d['J']))

    # --- contraintes physiques ----------------------------------------------------
    jrn('')
    f_large = MH.grille_log(20.0, 500.0, 24)
    Zs_large = TS.evaluer(res_fit['modele'], f_large, res_fit['theta'])
    Zm_large = MH.Z_depuis_jeu(f_large, MH.MED_TYP)
    # Les DCR font partie du CIRCUIT, pas d'un reglage : elles entrent dans les
    # contraintes (elles limitent le courant) comme dans la netlist LTspice.
    design_r = dict(design, r1=float(dcr(design['L1'])), r2=float(dcr(design['L2'])))
    catalogue_r = dict(DESIGN_CATALOGUE,
                       r1=float(dcr(DESIGN_CATALOGUE['L1'])),
                       r2=float(dcr(DESIGN_CATALOGUE['L2'])))
    contraintes = {}
    for nom, d in (('optimise', design_r), ('catalogue', catalogue_r)):
        V_C, I_L, Zin, ok, detail = F.verifier_contraintes(
            d, F.P_NOM_E800, Zs_large, f=f_large, Z_med=Zm_large,
            montage='voie', detail=True)
        contraintes[nom] = dict(V_C_crete=V_C, I_L_crete=I_L, Zin_min=Zin, ok=bool(ok),
                                Zin_min_grave=detail['Zin_min_grave'],
                                Zin_min_medium=detail['Zin_min_medium'],
                                Zin_min_parallele=detail['Zin_min_parallele'])
        jrn('contraintes %-9s : V(C1) %.0f V, V(C2) %.0f V, I(L1) %.1f A, '
            'min|Zin| %.2f ohm (grave %.2f / medium %.2f / parallele %.2f) -> %s'
            % (nom, V_C['C1'], V_C['C2'], I_L['L1'], Zin,
               detail['Zin_min_grave'], detail['Zin_min_medium'],
               detail['Zin_min_parallele'], 'OK' if ok else 'DISQUALIFIE'))

    # --- netlists LTspice ---------------------------------------------------------
    jrn('')
    noms_theta = TS.NOMS_THETA[res_fit['modele']]
    p_sub = {nom: float(v) for nom, v in zip(noms_theta, res_fit['theta'])}
    p_med = {c: float(MH.MED_TYP[c]) for c in ('Re', 'Le', 'Res', 'fs', 'Qms')}
    netlists = {}
    for nom, d in (('optimise', design_r), ('catalogue', catalogue_r)):
        chemin = os.path.join(DOSSIER_RESULTATS, 'filtre_%s.cir' % nom)
        _assurer_dossier(DOSSIER_RESULTATS)
        F.exporter_netlist(d, (p_sub, p_med), chemin,
                           titre='Filtre %s -- %s' % (nom, _design_lisible(d)),
                           commentaire=('Charge grave : parametres IDENTIFIES sur '
                                        '%s (statut : %s).\n'
                                        'Charge medium : %s'
                                        % (os.path.basename(fit['resultat']['source']),
                                           fit['resultat'].get('statut_donnees'),
                                           MH.MED_TYP['avertissement'])))
        netlists[nom] = chemin
        jrn('netlist LTspice : %s' % chemin)

    # --- satellite : ce que couterait la self du design ---------------------------
    jrn('')
    for cle in ('L1', 'L2'):
        L = design[cle]
        r = SB.dcr_de_L(L, d_fil=1.4e-3, geometrie='brooks')
        jrn('self %s = %.4g mH (bobine de Brooks, fil 1,4 mm) : DCR %.2f ohm, '
            '%.2f kg de cuivre, %.0f EUR, insertion %.2f dB sur 8 ohm'
            % (cle, _mm(L), r, SB.masse_cuivre(L, r), SB.cout_self(L, r),
               SB.insertion_dB(r)))
    jrn('  (modele de DCR/prix : D6 NON GELEE -- ordres de grandeur, pas un devis.')
    jrn('   Les EUROS n entrent pas dans J tant que w_euro = 0 ; les DCR, SI : elles')
    jrn('   sont dans H_pb et H_ph, donc dans les termes somme et voies. C est ce')
    jrn('   couplage qui fait du satellite self une piece du recit, § 09.4.)')

    # --- satellite ENERGIE : ce que ces DCR coutent en watts (§ 06) ---------------
    # w_W = 0, donc les pertes n'entrent PAS dans J. Elles existent physiquement
    # quand meme : les chiffrer ici, c'est la difference entre "le terme est
    # desactive" et "il n'y a pas de pertes".
    jrn('')
    energie = {}
    for nom, d in (('optimise', design_r), ('catalogue', catalogue_r)):
        p = EN.pertes_joule(d, Zs, EN.P_REF_DEFAUT, Z_med=Zm, f=f, detail=True)
        energie[nom] = p
        jrn('pertes Joule %-9s : %.2f W pour %.0f W de reference, soit %.1f %% -- '
            'a comparer aux %.1f %% que donnerait le calcul de catalogue sur 8 ohm '
            'RESISTIFS'
            % (nom, p['P_totale_W'], p['P_ref_W'], 100 * p['fraction_de_P_ref'],
               100 * p['fraction_catalogue_8ohm']))
    p_etoile = EN.croisement(EN.HYPOTHESES_ENERGIE['P_repos_actif_marginal_W'],
                             design_r, Zs, eta=0.40, Z_med=Zm, f=f)
    jrn('croisement energetique passif / actif : P* = %.1f W (P_0 = %.3g W, eta = 0,40)'
        % (p_etoile, EN.HYPOTHESES_ENERGIE['P_repos_actif_marginal_W']))
    jrn('  CONCLUSION CONDITIONNELLE : P* est a cheval sur l ecoute domestique, et')
    jrn('  il depend de TROIS grandeurs non mesurees -- r, P_0 et le rendement de')
    jrn('  l ampli. Donner un intervalle, jamais "le passif gagne" (§ 06.9). Et le')
    jrn('  cadrage d abord : le haut-parleur dissipe lui-meme plus de 97 % de ce')
    jrn('  qu on lui envoie ; tout ceci est du second ordre -- mais c est le seul')
    jrn('  ordre sur lequel le concepteur du filtre a prise.')

    # --- D2 n'est PAS gelee : on chiffre les TROIS cibles -------------------------
    # CORRECTION DE RELECTURE (2026-09-14). L'acte 3 ne tournait que sur 'butterworth',
    # une cible que le journal lui-meme etiquette "(D2 non gelee)". Le jour ou D2 sera
    # gelee sur 'lr2', personne n'aurait vu le design correspondant ni son ecart au
    # precedent -- alors que c'est precisement l'information qui rend le report de D2
    # defendable ("on ne fige pas un cahier des charges sur une charge supposee").
    # L'interface gelee [--rapide] [--sans-figures] n'a pas a changer : la cible du
    # recit reste CIBLE_DEFAUT, seul le tableau comparatif s'ajoute. Cout : deux
    # enumerations de quelques secondes.
    jrn('')
    jrn('COMPARAISON DES TROIS CIBLES (D2 NON GELEE -- aucune n est choisie)')
    comparaison_cibles = OrderedDict()
    for nom_cible in F.CIBLES:
        if nom_cible == cible_nom:
            r_c = resultat
        else:
            r_c = O.enumere_e12(f, Zs, Zm, cible_nom=nom_cible, w=w, dcr=dcr,
                                bavard=False)
        d_c = O.design_de(r_c)
        pole = F.pole_et_q(d_c['L1'], d_c['C1'], R=F.R_NOM,
                           r=float(dcr(d_c['L1'])))[0]
        comparaison_cibles[nom_cible] = OrderedDict([
            ('design', _design_lisible(d_c)),
            ('L1_H', d_c['L1']), ('C1_F', d_c['C1']),
            ('C2_F', d_c['C2']), ('L2_H', d_c['L2']),
            ('J', float(r_c['J'])),
            ('pole_Hz', float(pole)),
            ('retenue_pour_le_recit', nom_cible == cible_nom),
        ])
        jrn('  %-12s %s  J = %8.4f  pole %7.2f Hz%s'
            % (nom_cible, _design_lisible(d_c), r_c['J'], pole,
               '   <- cible du recit' if nom_cible == cible_nom else ''))
    jrn('  (lr2 et plate partagent Q = 0,5 : leurs lignes DOIVENT coincider -- c est')
    jrn('   un controle, pas une redondance. Aucune de ces trois cibles n est')
    jrn('   choisie : D2 est volontairement reportee apres la phase 1.)')

    contenu = OrderedDict([
        ('_lisez_moi',
         'Design optimise par enumeration exhaustive E12 sur la charge IDENTIFIEE. '
         'Regenerable par : python analyse/tout_refaire.py'),
        ('statut_donnees', fit['resultat'].get('statut_donnees')),
        ('provenance', TS.provenance(GRAINE)),
        ('entrees', OrderedDict([
            ('parametres_ts_json', os.path.basename(JSON_TS)),
            ('sha256_parametres_ts', TS.empreinte(JSON_TS)),
            ('criteres_geles_json', os.path.basename(criteres['chemin'])),
            ('sha256_criteres', criteres['sha256']),
            ('decisions_non_gelees', criteres['non_geles']),
        ])),
        ('reglages', OrderedDict([
            ('cible', cible_nom),
            ('cible_gelee', False),
            ('poids', w),
            ('source_poids', criteres['source_poids']),
            ('bande_critere_Hz', [float(f[0]), float(f[-1])]),
            ('n_points_critere', int(f.size)),
            ('serie', 'E12'),
            ('L_vals_mH', [float(_mm(v)) for v in O.L_VALS]),
            ('C_vals_uF', [float(_uf(v)) for v in O.C_VALS]),
        ])),
        # La cle s'appelait 'design_optimise' et ne portait pas le drapeau : un
        # chiffre recopie depuis ce fichier perdait son avertissement en chemin
        # (correction de relecture du 2026-09-14). 'hors_domaine' est desormais au
        # MEME niveau que les valeurs, donc impossible a ne pas lire.
        ('design_optimise', OrderedDict([
            ('hors_domaine', not bool(ok_bord)),
            ('_statut', 'DESIGN CANDIDAT -- '
                        + ('HORS DOMAINE : ' + '; '.join(avertissements)
                           if not ok_bord else 'optimum interieur a la grille')),
            ('L1_H', design['L1']), ('C1_F', design['C1']),
            ('C2_F', design['C2']), ('L2_H', design['L2']),
            ('lisible', _design_lisible(design)),
            ('J', float(resultat['J'])),
            ('modele_de_self', nom_retenu),
            ('r1_ohm', float(dcr(design['L1']))), ('r2_ohm', float(dcr(design['L2']))),
            ('n_combinaisons', int(resultat['n_combinaisons'])),
            ('duree_s', duree),
            ('termes', {k: v for k, v in termes_opt.items() if k != 'design'}),
        ])),
        ('variantes_de_self', OrderedDict([
            ('_lisez_moi',
             'D6 (modele de DCR/prix) n est PAS gelee : les deux enumerations sont '
             'donnees, et l ecart entre elles EST le resultat. La DCR entre dans '
             'H_pb et H_ph, donc dans les termes somme et voies -- voir § 09.4.'),
            ('retenue', nom_retenu),
            ('selfs_ideales', OrderedDict([
                ('design', _design_lisible(design_ideal)),
                ('J_avec_selfs_ideales', float(ideal['J'])),
                ('J_reevalue_avec_sa_vraie_dcr', float(J_ideal_reevalue)),
            ])),
            ('selfs_brooks', OrderedDict([
                ('design', _design_lisible(design)),
                ('J', float(resultat['J'])),
            ])),
        ])),
        ('comparaison_cibles', comparaison_cibles),
        ('design_catalogue', OrderedDict([
            ('_lisez_moi', 'Butterworth 2e ordre 100 Hz calcule sur 8 ohm RESISTIFS : '
                           'le point de depart a battre, pas un resultat.'),
            ('L1_H', DESIGN_CATALOGUE['L1']), ('C1_F', DESIGN_CATALOGUE['C1']),
            ('C2_F', DESIGN_CATALOGUE['C2']), ('L2_H', DESIGN_CATALOGUE['L2']),
            ('J', float(termes_cat['J'])),
            ('termes', {k: v for k, v in termes_cat.items() if k != 'design'}),
        ])),
        ('optimum_interieur', OrderedDict([
            ('ok', bool(ok_bord)), ('avertissements', avertissements)])),
        ('plateau', OrderedDict([
            ('n_dans_plateau', plateau['n_dans_plateau']),
            ('seuil_pct', plateau['seuil_pct']),
            ('ecart_2e_pct', plateau['ecart_2e_pct']),
            ('verdict', plateau['verdict']),
            ('classement', plateau['classement'][:5]),
        ])),
        ('contraintes', contraintes),
        ('energie', OrderedDict([
            ('_lisez_moi',
             'Satellite SOBRIETE (§ 06). w_W = 0 : ces watts n entrent PAS dans J, '
             'mais ils existent physiquement. La fraction est evaluee '
             'SPECTRALEMENT sur Z(f), pas lue sur 8 ohm resistifs.'),
            ('pertes_joule_W', {k: v['P_totale_W'] for k, v in energie.items()}),
            ('fraction_de_P_ref', {k: v['fraction_de_P_ref']
                                   for k, v in energie.items()}),
            ('fraction_catalogue_8ohm',
             energie['optimise']['fraction_catalogue_8ohm']),
            ('P_etoile_croisement_W', float(p_etoile)),
            ('hypotheses', EN.HYPOTHESES_ENERGIE['avertissement']),
        ])),
        ('netlists', {k: os.path.basename(v) for k, v in netlists.items()}),
    ])
    _ecrire_json(JSON_DESIGN, contenu)
    jrn('')
    jrn('ecrit : %s' % JSON_DESIGN)
    return dict(design=design, resultat=resultat, f=f, Zs=Zs, Zm=Zm, w=w,
                cible_nom=cible_nom, plateau=plateau, termes=termes_opt,
                termes_catalogue=termes_cat, chemin_json=JSON_DESIGN,
                dcr=dcr, modele_self=nom_retenu,
                optimum_interieur=bool(ok_bord),
                motif_hors_domaine=('; '.join(avertissements) if avertissements else ''),
                contraintes=contraintes, comparaison_cibles=comparaison_cibles,
                design_selfs_ideales=design_ideal,
                J_selfs_ideales_reevalue=float(J_ideal_reevalue))


def _mention_domaine(optimum):
    """Mention a accoler au design partout ou il est nomme : '' ou l'avertissement.

    Le diagnostic de bord de grille existait et etait excellent, mais il restait
    ENTERRE dans le journal, trente lignes plus haut que le recapitulatif. Or le seul
    chiffre affiche au terminal est celui qui sera recopie, cite et retenu -- par un
    jury notamment. Cette fonction fait remonter le drapeau jusqu'au titre de l'etape
    7 et jusqu'au recapitulatif final (correction de relecture du 2026-09-14).
    """
    if optimum.get('optimum_interieur', True):
        return ''
    motif = optimum.get('motif_hors_domaine') or 'optimum sur un bord de grille'
    # PREMIERE PHRASE SEULEMENT. Le motif complet explique aussi POURQUOI (ici, la
    # contrainte d'ordre 2 qui manque) : cela appartient au journal de l'etape 6 et au
    # JSON, pas a une ligne de recapitulatif qu'on doit pouvoir lire d'un trait.
    return ' -- CANDIDAT HORS DOMAINE : %s.' % motif.split('. ')[0].rstrip('.')


def etape_7_incertitudes(jrn, optimum, fit, rapide):
    """Incertitudes : tolerances des composants ET covariance des parametres T-S.

    Deux tirages DISTINCTS, et les confondre serait une faute :
      * les TOLERANCES d'achat (self +/-10 %, condensateur +/-20 %) repondent a
        "l'objet fabrique realisera-t-il le design calcule ?" -- c'est une
        DISPERSION ;
      * la covariance du fit repond a "la charge est-elle bien celle qu'on croit ?"
        -- et le § 04.9 conclut que Z(f) est un BIAIS, pas une dispersion.
        Un biais ne se reduit pas en resserrant les tolerances.

    La convention GUM est gelee (§ 09.6) : une tolerance "+/-10 %" est une
    DEMI-LARGEUR de loi rectangulaire, donc u = a/racine(3) = 5,77 %, donc
    u(f_0)/f_0 = 4,08 %. Le 7,07 % est la BORNE AU PIRE CAS. Le 11 % de la v1
    venait d'un RC du premier ordre, hors sujet ici.
    """
    jrn.titre('7/8', 'Incertitudes : tolerances et propagation')
    n_mc = N.N_MC_RAPIDE if rapide else N.N_MC_DEFAUT
    jrn('tirages Monte-Carlo : %d%s' % (n_mc, ' (--rapide)' if rapide else ''))
    jrn('graine : %d' % GRAINE)
    jrn('')

    # --- les chiffres de CONTROLE, sur le couple catalogue 18 mH / 150 uF ---------
    # Ce sont eux que le § 09.6 gele et que l'oral cite : ils ne dependent
    # pas du design retenu, seulement des tolerances. On les recalcule a chaque
    # execution plutot que de les recopier -- un chiffre recopie ne se verifie pas.
    L_c, C_c = DESIGN_CATALOGUE['L1'], DESIGN_CATALOGUE['C1']
    f0_c = N.f0_lc(L_c, C_c)
    a = 0.10                                       # DEMI-largeur, L et C a +/-10 %
    u = a / np.sqrt(3.0)                           # incertitude-type GUM
    gum = N.u_f0_relative(u, u)
    pire = N.u_f0_relative(a, a)
    meme_lot = N.u_f0_relative(a, a, rho=1.0)
    _moy, mc_unif = N.mc_f0(L_c, C_c, a, a, n=n_mc, loi='uniforme', graine=GRAINE)
    jrn('CHIFFRES DE CONTROLE (couple catalogue %.4g mH / %.4g uF, L et C a +/-10 %%)'
        % (_mm(L_c), _uf(C_c)))
    jrn('  pole f_0 = 1/(2 pi racine(L C))                      : %.2f Hz' % f0_c)
    jrn('    (le POLE, un repere nomme -- f_c reste la frequence de CROISEMENT)')
    jrn('  u(f_0)/f_0, convention GUM retenue (u = a/racine 3)  : %.2f %%'
        % (100 * gum))
    jrn('  Monte-Carlo uniforme, memes tolerances               : %.2f %%'
        % (100 * mc_unif))
    jrn('  borne au pire cas (demi-largeurs en quadrature)      : %.2f %%'
        % (100 * pire))
    jrn('  meme lot (rho = +1), reponse toute prete au jury     : %.2f %%'
        % (100 * meme_lot))
    jrn('  formule du RC 1er ordre (INTERDITE, v1)              : %.2f %% -- elle'
        % (100 * np.hypot(a, a)))
    jrn('    decrit un RC du premier ordre, pas un LC : ne jamais la produire.')

    # --- le design effectivement retenu, avec SES tolerances d'achat -------------
    design = optimum['design']
    L, C = design['L1'], design['C1']
    a_L, a_C = TOL_L, TOL_C
    u_L, u_C = a_L / np.sqrt(3.0), a_C / np.sqrt(3.0)
    f0_nom = N.f0_lc(L, C)
    gum_design = N.u_f0_relative(u_L, u_C)
    jrn('')
    jrn('DESIGN CANDIDAT (%.4g mH / %.4g uF, self +/-%.0f %% et condensateur '
        '+/-%.0f %%)%s'
        % (_mm(L), _uf(C), 100 * TOL_L, 100 * TOL_C, _mention_domaine(optimum)))
    if not optimum.get('optimum_interieur', True):
        jrn('  (le mot CANDIDAT n est pas un ornement : ce design est declare HORS')
        jrn('   DOMAINE a l etape 6, et rien ne doit etre achete sur sa foi.)')
    jrn('  pole f_0 = %.2f Hz ; u(f_0)/f_0 = %.2f %% (GUM)'
        % (f0_nom, 100 * gum_design))

    # Tolerances -> critere et frequence de CROISEMENT (la seule definition de f_c).
    jrn('')
    n_tol = 500 if rapide else 4000
    mc = O.monte_carlo_tolerances(design, optimum['f'], optimum['Zs'], optimum['Zm'],
                                  n=n_tol, tol_L=TOL_L, tol_C=TOL_C, loi='uniforme',
                                  graine=GRAINE, cible_nom=optimum['cible_nom'],
                                  w=optimum['w'])
    jrn('tolerances -> criteres (%d tirages, loi rectangulaire +/-%.0f %% / +/-%.0f %%) :'
        % (n_tol, 100 * TOL_L, 100 * TOL_C))
    jrn('  J nominal %.4f ; J moyen %.4f +/- %.4f (5 %% / 50 %% / 95 %% : %s)'
        % (mc['J_nominal'], mc['J_moyen'], mc['J_ecart_type'],
           ' / '.join('%.3f' % q for q in np.atleast_1d(mc['J_quantiles']))))
    if np.isfinite(mc.get('fc_moyen', np.nan)):
        jrn('  f_c (CROISEMENT des deux voies, %d tirages valides) : '
            '%.2f Hz +/- %.2f Hz (%.2f %%)'
            % (mc['fc_n_valides'], mc['fc_moyen'], mc['fc_ecart_type'],
               mc['fc_relatif_pct']))
    else:
        jrn('  f_c : aucun croisement trouve dans la bande sur les tirages -- le')
        jrn('        design retenu ne realise pas un raccord dans 40-250 Hz.')

    # Ce que vaut l'incertitude sur la CHARGE, via la covariance du fit.
    jrn('')
    res_fit = fit['resultat']
    u_c = np.asarray(res_fit['u_composee'], float)
    theta = np.asarray(res_fit['theta'], float)
    jrn('incertitude de la CHARGE (covariance complete du fit, acte 2) :')
    for nom, t, u in zip(res_fit['noms'], theta, u_c):
        jrn('  %-4s %12.5g  +/- %-10.4g  (%.2f %%)' % (nom, t, u, 100 * u / abs(t)))
    jrn('  rappel § 04.9 : Z(f) est un BIAIS (quelques dB systematiques sur')
    jrn('  l ecart RMS), les tolerances sont une DISPERSION (quelques dixiemes de')
    jrn('  dB). Un biais ne se corrige pas en resserrant les tolerances.')

    contenu = OrderedDict([
        ('controle_couple_catalogue', OrderedDict([
            ('L_H', L_c), ('C_F', C_c),
            ('f0_pole_Hz', float(f0_c)),
            ('tolerances_demi_largeur', a),
            ('u_f0_relative_GUM', float(gum)),
            ('u_f0_relative_mc_uniforme', float(mc_unif)),
            ('u_f0_relative_borne_pire_cas', float(pire)),
            ('u_f0_relative_meme_lot_rho1', float(meme_lot)),
        ])),
        ('f0_nominal_Hz', float(f0_nom)),
        ('u_f0_relative_GUM_design', float(gum_design)),
        ('n_tirages', int(n_mc)),
        ('graine', GRAINE),
        ('tolerances', dict(tol_L=TOL_L, tol_C=TOL_C, loi='uniforme (rectangulaire)')),
        ('monte_carlo_tolerances', {k: v for k, v in mc.items()
                                    if not isinstance(v, np.ndarray) or v.size < 20}),
    ])
    chemin = os.path.join(DOSSIER_RESULTATS, 'incertitudes.json')
    _ecrire_json(chemin, contenu)
    jrn('')
    jrn('ecrit : %s' % chemin)
    return dict(gum=gum, mc=mc, chemin_json=chemin)


def etape_8_figures(jrn, fit, optimum, sans_figures):
    """Figures Blueprint + controle du test (h), puis essai d'injection HTML.

    Le cache de figures.py est AMORCE avec les resultats calcules ci-dessus : une
    figure qui montrerait autre chose que ce que la chaine vient de calculer ne
    prouverait rien.

    L'injection dans les presentations du depot n'est PAS faite ici : aucune ne
    porte encore de marqueur <!--FIG:nom--> (la refonte v2 des diapositives est
    prevue en phase 5). Le mecanisme est neanmoins EPROUVE sur un HTML temporaire
    -- c'est exactement le defaut de _gen.py (annoncer "OK injecte" sans rien
    injecter) que ce controle interdit.
    """
    jrn.titre('8/8', 'Figures (identite Blueprint) et injection')
    if sans_figures:
        jrn('--sans-figures : etape sautee (matplotlib n est pas sollicite).')
        return dict(saute=True)
    import figures as FIG                         # importe ici : seul consommateur de mpl

    FIG._CACHE['fit'] = fit['resultat']
    cle_optim = 'optim:' + optimum['cible_nom']
    r = dict(optimum['resultat'])
    r.update(cible_nom=optimum['cible_nom'], f_critere=optimum['f'],
             duree_s=0.0, bord=O.verifier_optimum_interieur(optimum['resultat']),
             plateau=optimum['plateau'])
    FIG._CACHE[cle_optim] = r
    jrn('cache de figures.py amorce avec le fit et l enumeration de cette execution.')
    jrn('')

    _assurer_dossier(DOSSIER_FIGURES)
    tampon = io.StringIO()
    sortie_reelle, sys.stdout = sys.stdout, tampon
    try:
        comptes = FIG.tout_generer(dossier=DOSSIER_FIGURES, variantes=('sombre', 'clair'),
                                   formats=('svg', 'png'), bavard=True)
    finally:
        sys.stdout = sortie_reelle
    jrn.bloc(tampon.getvalue().rstrip('\n'))
    echecs = [c['figure'] for c in comptes if not c['ok']]
    if echecs:
        raise EchecEtape('figure(s) en echec (couleur figee ou fichier vide) : %s'
                         % ', '.join(sorted(set(echecs))))
    jrn('')
    jrn('%d fichier(s) de figure produits, 0 couleur hexadecimale figee (test (h)).'
        % sum(len(c['chemins']) for c in comptes))

    # Essai d'injection sur un HTML temporaire : le mecanisme est prouve, aucune
    # diapositive du depot n'est touchee.
    import tempfile
    noms = [c['figure'] for c in comptes if c['variante'] == 'sombre']
    temporaire = os.path.join(tempfile.gettempdir(), 'tipe_injection_tout_refaire.html')
    with open(temporaire, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('<html><body>\n'
                 + '\n'.join('<figure><!--FIG:%s--></figure>' % n for n in noms)
                 + '\n</body></html>\n')
    tampon = io.StringIO()
    sortie_reelle, sys.stdout = sys.stdout, tampon
    try:
        n = FIG.injecter_figures(temporaire, DOSSIER_FIGURES, noms)
    finally:
        sys.stdout = sortie_reelle
        os.remove(temporaire)
    jrn('essai d injection : %s' % tampon.getvalue().strip())
    if n != len(noms):
        raise EchecEtape('injection : %d figure(s) injectee(s) sur %d' % (n, len(noms)))

    presentations = [n for n in sorted(os.listdir(_RACINE)) if n.endswith('.html')]
    porteuses = []
    for nom in presentations:
        with open(os.path.join(_RACINE, nom), encoding='utf-8') as fh:
            if '<!--FIG:' in fh.read():
                porteuses.append(nom)
    jrn('')
    if porteuses:
        jrn('HTML porteurs de marqueurs <!--FIG:...--> : %s' % ', '.join(porteuses))
        jrn('  -> refonte v2 FAITE (gabarit 4/3) et figures deja injectees dans ces')
        jrn('     decks. On ne reinjecte PAS ici : l injection reecrit le HTML en place,')
        jrn('     donc elle se lance a la main, sur un depot propre ou sur une copie.')
    else:
        jrn('aucun HTML du depot ne porte de marqueur <!--FIG:nom--> : injection dans')
        jrn('les presentations REPORTEE en phase 5 (refonte v2 des diapositives).')
        jrn('Les %d HTML presents (%s) sont encore ceux de la v1.'
            % (len(presentations), ', '.join(presentations)))
    return dict(saute=False, n_fichiers=sum(len(c['chemins']) for c in comptes),
                dossier=DOSSIER_FIGURES, n_injectees=n)


# ==================================================================================
# 3. Orchestration
# ==================================================================================

AIDE = """tout_refaire.py -- rejoue toute la chaine d'analyse (§ 09.8)

Usage :
  python analyse/tout_refaire.py [--rapide] [--sans-figures]

  --rapide         Monte-Carlo a %d tirages au lieu de %d, ajustement allege.
                   Pour la boucle de developpement UNIQUEMENT : les chiffres de
                   l'oral se produisent SANS cette option.
  --sans-figures   saute la generation des SVG/PNG (seule etape qui demande
                   matplotlib).
  -h, --aide       affiche ce message.

Code de retour : 0 si tout passe, 1 au premier echec (nom de l'etape sur stderr).
""" % (N.N_MC_RAPIDE, N.N_MC_DEFAUT)


def principal(arguments=None):
    """Enchaine les huit etapes et rend le code de retour (0 ou 1)."""
    arguments = list(sys.argv[1:] if arguments is None else arguments)
    if '-h' in arguments or '--aide' in arguments or '--help' in arguments:
        print(AIDE)
        return 0
    rapide = '--rapide' in arguments
    sans_figures = '--sans-figures' in arguments
    inconnus = [a for a in arguments if a not in ('--rapide', '--sans-figures')]
    if inconnus:
        sys.stderr.write('tout_refaire : option inconnue : %s\n' % ' '.join(inconnus))
        sys.stderr.write(AIDE)
        return 1

    _assurer_dossier(DOSSIER_RESULTATS)
    jrn = Journal()
    jrn('TIPE filtrage enceinte -- chaine d analyse complete (§ 09.8)')
    jrn('=' * 78)
    entete = TS.provenance(GRAINE)
    entete['module'] = 'analyse/tout_refaire.py'   # la provenance est celle de CETTE chaine
    for cle, valeur in entete.items():
        jrn('%-18s %s' % (cle + ' :', valeur))
    jrn('%-18s %s' % ('matplotlib :', 'non sollicite (--sans-figures)' if sans_figures
                      else __import__('matplotlib').__version__))
    jrn('%-18s %s' % ('options :', ' '.join(arguments) or '(aucune)'))
    jrn('%-18s %s' % ('depot :', _RACINE))
    jrn('')
    jrn('AUCUNE MESURE DE L ENCEINTE N EXISTE a ce jour. La chaine tourne sur des')
    jrn('donnees SYNTHETIQUES etiquetees comme telles dans leur en-tete : elle')
    jrn('prouve que le code est juste, elle ne dit RIEN du haut-parleur reel.')
    if rapide:
        jrn('')
        jrn('*** --rapide : tirages reduits. AUCUN chiffre de cette execution ne doit')
        jrn('*** etre cite a l oral. Relancer sans --rapide pour les chiffres finaux.')

    etat = {}
    etapes = [
        ('tests', lambda: etape_1_tests(jrn, rapide)),
        ('criteres', lambda: etape_2_criteres(jrn)),
        ('mesures', lambda: etape_3_mesures(jrn)),
        ('porte_8ohm', lambda: etape_4_porte_8ohm(jrn)),
        ('ajustement', lambda: etape_5_ajustement(jrn, etat['mesures'], rapide)),
        ('optimisation', lambda: etape_6_optimisation(jrn, etat['criteres'],
                                                      etat['ajustement'], rapide)),
        ('incertitudes', lambda: etape_7_incertitudes(jrn, etat['optimisation'],
                                                      etat['ajustement'], rapide)),
        ('figures', lambda: etape_8_figures(jrn, etat['ajustement'],
                                            etat['optimisation'], sans_figures)),
    ]
    for nom, fonction in etapes:
        try:
            etat[nom] = fonction()
        except Exception as exc:                  # noqa: BLE001 -- on veut TOUT attraper
            jrn('')
            jrn('!!! ECHEC DE L ETAPE "%s" : %s' % (nom, exc))
            if not isinstance(exc, EchecEtape):
                jrn.bloc(traceback.format_exc())
            jrn.ecrire(JOURNAL)
            sys.stderr.write('tout_refaire : ECHEC de l etape "%s" : %s\n' % (nom, exc))
            sys.stderr.write('tout_refaire : journal partiel dans %s\n' % JOURNAL)
            return 1

    jrn.titre('fin', 'Recapitulatif')
    jrn('tests            : %d au vert en %.1f s'
        % (etat['tests']['n_tests'], etat['tests']['duree_s']))
    jrn('decisions gelees : %d encore ouvertes' % len(etat['criteres']['non_geles']))
    jrn('mesures          : %d fichier(s), toutes SYNTHETIQUES'
        % len(etat['mesures']['inventaire']))
    jrn('portes 8 ohm     : %d franchies (butterworth et lr2)'
        % len(etat['porte_8ohm']['portes']))
    jrn('ajustement       : modele %s, chi2 reduit %.3f'
        % (etat['ajustement']['resultat']['modele'],
           etat['ajustement']['resultat']['chi2_reduit']))
    # LE RECAPITULATIF PORTE LES DRAPEAUX, et ce n'est pas cosmetique : c'est la
    # SEULE partie du journal qu'un lecteur presse lira, donc le seul chiffre qui
    # sera recopie et cite. Un design declare hors domaine trente lignes plus haut,
    # ou un catalogue disqualifie par min|Zin|, doivent le redire ici (correction de
    # relecture du 2026-09-14).
    opt = etat['optimisation']
    jrn('optimisation     : %s (J = %.4f)%s'
        % (_design_lisible(opt['design']), opt['termes']['J'],
           _mention_domaine(opt)))
    jrn('                   modele de self : %s' % opt['modele_self'])
    c_cat = opt.get('contraintes', {}).get('catalogue', {})
    jrn('                   catalogue : %s (J = %.4f)%s'
        % (_design_lisible(DESIGN_CATALOGUE),
           opt['termes_catalogue']['J'],
           ('' if c_cat.get('ok', True)
            else ' -- DISQUALIFIE (min|Zin| %.2f ohm < %.0f)'
                 % (c_cat.get('Zin_min', float('nan')), F.ZIN_MIN_E800))))
    jrn('                   cibles (D2 ouverte) : %s'
        % ' | '.join('%s J = %.3f' % (k, v['J'])
                     for k, v in opt['comparaison_cibles'].items()))
    if not opt.get('optimum_interieur', True):
        sys.stderr.write('tout_refaire : AVERTISSEMENT -- l optimum retenu est sur un '
                         'bord de la grille E12, donc hors domaine ; il n est pas '
                         'exploitable tel quel. Motif complet : etape 6 du journal '
                         '(%s).\n' % JOURNAL)
    jrn('incertitudes     : u(f_0)/f_0 = %.2f %% (GUM)'
        % (100 * etat['incertitudes']['gum']))
    if etat['figures'].get('saute'):
        jrn('figures          : sautees (--sans-figures)')
    else:
        jrn('figures          : %d fichier(s) dans %s'
            % (etat['figures']['n_fichiers'], etat['figures']['dossier']))
    jrn('')
    jrn('livrables versionnes :')
    for chemin in (JSON_TS, JSON_DESIGN):
        jrn('  %s (%d octets)' % (chemin, os.path.getsize(chemin)))
    jrn('')
    jrn('duree totale : %.1f s' % (time.time() - jrn.t0))
    jrn.ecrire(JOURNAL)
    jrn('journal : %s' % JOURNAL)
    # La ligne ci-dessus est ecrite APRES la sauvegarde : elle n'a de sens qu'a
    # l'ecran, et le journal n'a pas a contenir son propre chemin deux fois.
    return 0


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')      # console Windows en cp1252
    raise SystemExit(principal())
