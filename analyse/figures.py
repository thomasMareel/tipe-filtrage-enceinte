# -*- coding: utf-8 -*-
"""figures.py -- les figures du recit, en identite Blueprint.

Voir REFERENCE-TECHNIQUE.md § 09.7 (figures, nommage, injection) et 09.4
(signatures gelees). Le style, les couleurs et la geometrie vivent dans
blueprint_mpl.py ; ce module-ci ne contient QUE la physique a montrer.

AUCUNE DE CES FIGURES N'EST UNE MESURE, ET CHACUNE LE DIT. Au 2026-09-13 rien
n'a encore ete mesure sur l'enceinte de Thomas : la premiere seance de banc est
l'objet de la phase 1. Les courbes tracees ici viennent donc
  - soit du fichier SYNTHETIQUE analyse/mesures/exemple_synthetique_sub.csv,
    engendre par io_mesures.generer_exemple_synthetique a partir d'un modele de
    Thiele-Small et bruite volontairement ;
  - soit directement d'un modele (modele_hp.SUB_TYP_CLOS, MED_TYP), dont les
    parametres sont des ORDRES DE GRANDEUR tires de datasheets publiques.
Chaque figure porte la mention "DONNEES SYNTHETIQUES" dessinee DANS l'image
(blueprint_mpl.marque_synthetique) : une figure se retrouve toujours un jour sur
une diapositive sans sa legende. Le jour ou les vraies mesures existeront, il n'y
aura qu'a changer le fichier d'entree et retirer la mention -- pas a refaire les
figures.

CONVENTION DE NOMMAGE, GELEE ICI (elle etait deja a moitie fixee au tableau du
§ 09.7, on la complete) :

    analyse/figures/<nom>.svg          figure de reference, vectorielle,
                                       couleurs en variables CSS, destinee a
                                       etre INLINEE dans les diapositives ;
    analyse/figures/<nom>.png          meme figure en bitmap : previsualisation,
                                       repli de l'export PDF (EXPORT-PDF.md),
                                       relecture rapide. Couleurs FIGEES.
    analyse/figures/<nom>-clair.svg    variante claire, pour un support imprime
    analyse/figures/<nom>-clair.png    qui ne peut pas charger blueprint-light.css.

    <nom> = fig-<sujet>[-<precision>], en minuscules, sans accent, mots separes
    par des tirets. Le nom est STABLE : c'est lui qu'appelle le marqueur
    <!--FIG:<nom>--> place dans le HTML des presentations. On ne renomme pas une
    figure, on en cree une autre.

Les six noms produits par ce module sont ceux du tableau du § 09.7 :
fig-z-sub-mesure, fig-fit-ts-sub, fig-catalogue-8ohm-vs-z,
fig-somme-catalogue-vs-optimise, fig-self-cout-dcr, fig-plateau-optimum. Les
autres lignes de ce tableau (etalonnage de chaine, acoustique en champ proche,
Monte-Carlo de f0, croisement energetique) attendent des donnees qui n'existent
pas encore : les inventer serait exactement ce que le projet s'interdit.

OU SONT ECRITES LES FIGURES. Par defaut dans analyse/figures/, dossier de
travail ; tout_refaire.py (§ 09.8) peut demander analyse/resultats/figures/,
qui est le dossier ignore par git de l'arborescence du § 09.2. Les deux
chemins sont des constantes, DOSSIER_FIGURES et DOSSIER_RESULTATS, et
tout_generer() accepte n'importe quel dossier : aucune figure n'est jamais
ecrite ailleurs que la ou l'appelant le demande.

A FAIRE DANS .gitignore, ET C'EST UNE DECISION A PRENDRE, PAS UN OUBLI. Une
figure est une SORTIE regenerable en une seconde (principe 3 du § 09.1) :
elle n'a pas a etre versionnee, sauf si l'on veut pouvoir ouvrir le depot sans
Python. Les regles du § 09.8 couvrent deja resultats/ ; pour le dossier
de travail il faut ajouter, en respectant le meme piege (une negation est
inoperante si le DOSSIER entier est exclu) :

    analyse/figures/*
    !analyse/figures/.gitkeep

Tant que rien n'est ecrit, les 12 fichiers produits ici seront proposes au
prochain commit. Lancer avec --resultats pour ecrire dans le dossier deja couvert.

EXCEPTION DE CONVENTION, LOCALISEE ET ASSUMEE. Le projet impose du francais SANS
ACCENTS dans le code (console cp1252, § 09.4) : docstrings, commentaires et
messages imprimes de ce module la respectent. Les CHAINES DESSINEES DANS LES
FIGURES portent en revanche leurs accents -- elles ne transitent jamais par la
console, elles sont rendues par matplotlib puis par le navigateur, et
"Frequence" sans accent sur une diapositive de concours est une faute. Les
chaines recurrentes sont regroupees dans TEXTES ; les annotations ponctuelles
sont ecrites sur place.

Dependances : numpy, matplotlib, et les modules voisins blueprint_mpl, modele_hp,
filtre, optim, self_bobine, ts_fit, io_mesures. scipy n'est pas requis ici.
Fichier en UTF-8, fins de ligne LF.

Utilisation :
    python analyse/figures.py                 toutes les figures, variante sombre
    python analyse/figures.py --clair         ajoute la variante claire
    python analyse/figures.py --liste         liste les figures et sort
    python analyse/figures.py fig-z-sub-mesure fig-fit-ts-sub      (au choix)
    python analyse/figures.py --dossier chemin/vers/dossier
"""

import os
import sys
import textwrap
import time
from collections import OrderedDict

import numpy as np

_ICI = os.path.dirname(os.path.abspath(__file__))
if _ICI not in sys.path:                      # rend le module importable de n'importe ou
    sys.path.insert(0, _ICI)

import matplotlib.pyplot as plt               # noqa: E402

import blueprint_mpl as BP                    # noqa: E402  style, palette, enregistrement
import filtre as F                            # noqa: E402  H_pb, H_ph, cibles, sommation
import io_mesures as IO                       # noqa: E402  lecture du CSV, criteres geles
import modele_hp as MH                        # noqa: E402  Z_ts, diagnostics de courbe
import optim as O                             # noqa: E402  enumeration E12, fonction de cout
import energie as EN                          # noqa: E402  satellite sobriete (§ 06)
import self_bobine as SB                      # noqa: E402  masse, DCR, prix de la self
import ts_fit as TS                           # noqa: E402  probleme inverse (acte 2)

# Re-export des noms geles au tableau du § 09.4 : la specification les
# attend dans le module `figures`, l'implementation vit dans blueprint_mpl.
style_blueprint = BP.style_blueprint
enregistrer_svg = BP.enregistrer_svg


# UN SEUL dossier de sortie, et c'est resultats/figures (correction de relecture du
# 2026-09-14). Il y en avait deux : analyse/figures/ pour les lancements directs de ce
# module et analyse/resultats/figures/ pour tout_refaire.py. Seul le second est couvert
# par la regle .gitignore du § 09.8, donc un `git add analyse` aurait versionne des SVG
# PERIMES -- indiscernables, une fois dans le depot, des figures a jour, et citables a
# l'oral par megarde. Le principe du § 09.2 est net : "ce qui est dans resultats/ coute
# dix secondes", donc rien de regenerable ne vit ailleurs.
DOSSIER_RESULTATS = os.path.join(_ICI, 'resultats', 'figures')
DOSSIER_FIGURES = DOSSIER_RESULTATS

# Bande et densite de TRACE (pas celles du critere : le critere, c'est
# filtre.grille_critere(), 40-250 Hz a 24 points/octave). On trace plus large
# pour montrer ce qui se passe hors de la bande de jugement -- c'est souvent la
# que le catalogue se trahit.
BANDE_TRACE = (20.0, 500.0)
N_PAR_OCTAVE_TRACE = 48

# Design "catalogue" : Butterworth 2e ordre 100 Hz calcule sur 8 ohm RESISTIFS,
# valeurs normalisees (C theorique 140,7 uF -> 150 uF). C'est le point de depart
# a battre, lexique du projet (CLAUDE.md, "ce que la v1 legue a la v2").
DESIGN_CATALOGUE = dict(L1=18e-3, C1=150e-6, C2=150e-6, L2=18e-3)

# D2 (cible de sommation) est VOLONTAIREMENT reportee apres la phase 1 : la cible
# est donc un PARAMETRE partout, jamais une constante. Cette valeur n'est qu'un
# defaut de trace, et les figures concernees l'ecrivent en toutes lettres.
CIBLE_DEFAUT = 'butterworth'

# Chaines recurrentes dessinees dans les figures (les seules a porter des
# accents dans ce fichier ; cf. docstring de module).
TEXTES = {
    'frequence': 'Fréquence (Hz)',
    'module': '|Z| (Ω)',
    'phase': 'Phase φ (°)',
    'gain': 'Gain (dB)',
    'ecart': 'Écart à la cible (dB)',
    'residus': 'Résidus (σ)',
    'grave': 'voie grave (sub 18″)',
    'medium': 'voie médium',
    'somme': 'somme des deux voies',
    'cible': 'cible',
    'mesure': 'points « mesurés » (synthétiques)',
    'modele': 'modèle ajusté',
    'catalogue': 'filtre catalogue (8 Ω)',
    'optimise': 'filtre optimisé sur Z(f)',
    'dcr': 'DCR de la self r (Ω)',
    'masse': 'Masse de cuivre (kg)',
    'prix': 'Prix du cuivre (€, ordre de grandeur)',
    'insertion': "Perte d'insertion sur 8 Ω (dB)",
    'niveau': 'Niveau d’écoute P_voie (W moyens dans la voie grave)',
    'energie': 'Énergie au compteur (W)',
}


# ---------------------------------------------------------------------------
# 1. Sources de donnees -- toutes synthetiques, toutes etiquetees
# ---------------------------------------------------------------------------

_CACHE = {}          # les etapes couteuses (ajustement, enumeration) une seule fois


def geometrie_deliverable(bavard=False):
    """Taille de figure a utiliser, et D'OU elle vient.

    La decision D7 de criteres_geles.json ("gabarit 4/3 impose par le livrable
    SCEI, PDF 1024x768") n'est pas encore gelee au 2026-09-13. Le code lit le
    fichier quand meme : le jour du gel, la valeur ecrite la prend effet sans
    qu'on touche a figures.py -- c'est le principe 4 du § 09.1
    ("les decisions gelees sont un fichier, pas une intention").

    Rend (taille_pouces, source_lisible).
    """
    defaut = (BP.TAILLE_DIAPO, 'defaut blueprint_mpl (D7 non gelee) : %.2f x %.2f po'
              % BP.TAILLE_DIAPO)
    try:
        criteres = IO.lire_criteres_geles(exiger_geles=False)
    except Exception:                          # fichier absent : on ne bloque pas une figure
        return defaut
    d7 = criteres.get('D7_figures', {}) or {}
    l, h = d7.get('largeur_px'), d7.get('hauteur_px')
    try:
        l, h = float(l), float(h)
    except (TypeError, ValueError):             # encore '[[a geler]]'
        if bavard:
            print('D7 non gelee : taille de figure par defaut')
        return defaut
    taille = (l / BP.DPI, h / BP.DPI)
    return taille, 'D7 gelee dans criteres_geles.json : %g x %g px' % (l, h)


MOTS_DE_MESURE_ABSENTE = ('SYNTH', 'SIMUL', 'MODEL', 'AUCUNE MESURE', 'PAS UNE MESURE')


def _statut_est_une_mesure(statut):
    """Vrai seulement si le statut lu dans l'en-tete du CSV designe une VRAIE mesure.

    Le defaut est PRUDENT : en cas de doute, on repond False, donc la figure se
    declare synthetique. Se tromper dans ce sens fait perdre un peu de force a une
    vraie mesure ; se tromper dans l'autre sens fait passer un calcul pour un releve
    de banc, ce que le § 08 interdit formellement.
    """
    if not statut:
        return False
    majuscules = str(statut).upper()
    return not any(mot in majuscules for mot in MOTS_DE_MESURE_ABSENTE)


def donnees_z(chemin=None, bavard=False):
    """Rend la courbe Z(f) SYNTHETIQUE qui sert de "mesure" a tout le recit.

    Priorite au fichier analyse/mesures/exemple_synthetique_sub.csv, qui a
    l'enorme avantage de passer par le VRAI format de mesure (en-tete de 14+
    cles, colonnes brutes et derivees) : les figures s'exercent donc sur le
    chemin de code qui servira le jour du banc. S'il est absent, on simule en
    memoire avec ts_fit.simuler -- sans jamais ecrire dans mesures/, dossier de
    donnees brutes qui ne doit rien devoir a un script de figures.

    Rend un dict : f, module, phase, u_module, u_phase, meta, source, statut.
    """
    if 'z' in _CACHE:
        return _CACHE['z']
    chemin = chemin or IO.CHEMIN_EXEMPLE
    if os.path.exists(chemin):
        d, meta = IO.lire_mesure(chemin)
        donnees = dict(f=np.asarray(d['f_Hz'], float),
                       module=np.asarray(d['module_Z_ohm'], float),
                       phase=np.asarray(d['phase_deg'], float),
                       u_module=np.asarray(d['u_module_alea_ohm'], float),
                       u_phase=np.asarray(d['u_phase_deg'], float),
                       meta=meta, source=os.path.basename(chemin),
                       statut=meta.get('statut_donnees', 'SYNTHETIQUES'))
    else:
        theta = TS.theta_depuis_jeu(MH.SUB_TYP_CLOS, 'clos')
        f = MH.grille_log(10.0, 500.0, 12, densifier=(theta[3] / 2, 2 * theta[3], 24))
        mod, phi, u_mod, u_phi = TS.simuler(theta, f, u_rel=0.02, u_deg=1.0, graine=20260913)
        donnees = dict(f=f, module=mod, phase=phi, u_module=u_mod, u_phase=u_phi,
                       meta={'u_systematique_relative_pct': '1.2'},
                       source='ts_fit.simuler (aucun fichier)',
                       statut='SYNTHETIQUES -- simulation en memoire')
    if bavard:
        print('donnees Z : %d points, %s, source %s'
              % (len(donnees['f']), donnees['statut'], donnees['source']))
    _CACHE['z'] = donnees
    return donnees


def identification(bavard=False):
    """Ajustement de Thiele-Small sur la courbe synthetique (acte 2), mis en cache.

    On passe par ts_fit.identifier, c'est-a-dire par le pipeline complet
    (aiguillage clos / bass-reflex, multi-depart, Monte-Carlo, verdicts), et non
    par un ajustement au rabais ecrit pour la figure : une figure qui montre
    autre chose que ce que la chaine calcule ne prouve rien.
    """
    if 'fit' in _CACHE:
        return _CACHE['fit']
    z = donnees_z()
    t0 = time.time()
    resultat = TS.identifier(z['f'], z['module'], z['phase'], z['u_module'], z['u_phase'],
                             modele='auto', bavard=False, rapide=True,
                             source=z['source'], statut_donnees=z['statut'])
    resultat['duree_s'] = time.time() - t0
    if bavard:
        print('identification : modele %s, chi2 reduit %.3f, %.2f s'
              % (resultat['modele'], resultat['chi2_reduit'], resultat['duree_s']))
    _CACHE['fit'] = resultat
    return resultat


def charges(f, utiliser_fit=True):
    """Impedances des deux voies sur la grille f : (Z_sub, Z_medium, etiquette).

    Le sub utilise les parametres IDENTIFIES a l'acte 2 -- c'est la continuite du
    recit : on optimise sur la charge qu'on vient de mesurer, pas sur une
    datasheet. Le bloc medium, lui, n'a pas encore de courbe (une seule serie
    synthetique existe) : on prend l'ordre de grandeur etiquete MED_TYP, et la
    figure le dit.
    """
    if utiliser_fit:
        res = identification()
        Zs = TS.evaluer(res['modele'], f, res['theta'])
        etiquette = 'sub : paramètres identifiés (acte 2, données synthétiques)'
    else:
        Zs = MH.Z_depuis_jeu(f, MH.SUB_TYP_CLOS)
        etiquette = 'sub : modèle typique de datasheet'
    Zm = MH.Z_depuis_jeu(f, MH.MED_TYP)
    return Zs, Zm, etiquette


def _dcr_figures():
    """Le modele de DCR utilise par TOUTES les figures : bobine de Brooks, fil 1,4 mm.

    Un seul endroit, pour qu'une figure et le journal de la chaine ne puissent pas
    afficher deux J differents pour le meme design. D6 n'est PAS gelee : c'est un
    ordre de grandeur etiquete, et les figures concernees le disent.
    """
    if '_dcr' not in _CACHE:
        _CACHE['_dcr'] = O.fabriques_self(d_fil=1.4e-3)[0]
    return _CACHE['_dcr']


def optimisation(cible_nom=CIBLE_DEFAUT, bavard=False):
    """Enumeration exhaustive E12 sur la charge reelle (acte 3), mise en cache.

    Poids W_SANITY de optim (w_euro = w_W = 0 tant que D5 n'est pas gelee) : la
    figure qui en sort montre donc un classement sans euros ni watts, et c'est
    ecrit dans son cartouche.

    LES SELFS, ELLES, NE SONT PAS PARFAITES (correction de relecture du
    2026-09-14). Cette fonction enumerait avec dcr=None, comme tout_refaire.py.
    Le commentaire qui tenait ici affirmait que cela "FAVORISE le catalogue" :
    c'est faux, et c'est verifie -- omettre la DCR le PENALISE de plusieurs dB,
    parce que la DCR n'agit pas que par le terme de pertes (nul ici) mais par
    H_pb et H_ph, ou elle amortit la resonance de la cellule grave et abaisse le
    niveau de la voie. La figure doit montrer ce que la chaine calcule : elle
    utilise donc le MEME modele de self que tout_refaire.py (bobine de Brooks,
    fil 1,4 mm, D6 non gelee -- ordre de grandeur etiquete).

    Quand la figure est produite PAR tout_refaire.py, le cache est de toute
    facon amorce avec l'enumeration de la chaine : cette fonction ne sert alors
    qu'aux lancements directs de figures.py, et il faut qu'ils concordent.
    """
    cle = 'optim:' + cible_nom
    if cle in _CACHE:
        return _CACHE[cle]
    fg = F.grille_critere()
    Zs, Zm, _ = charges(fg)
    dcr = _dcr_figures()
    t0 = time.time()
    resultat = O.enumere_e12(fg, Zs, Zm, cible_nom=cible_nom, w=O.W_SANITY,
                             dcr=dcr, bavard=False)
    resultat['dcr'] = dcr
    resultat['duree_s'] = time.time() - t0
    resultat['cible_nom'] = cible_nom
    resultat['f_critere'] = fg
    resultat['bord'] = O.verifier_optimum_interieur(resultat)
    resultat['plateau'] = O.analyser_plateau(resultat)
    if bavard:
        print('enumeration E12 : %d combinaisons en %.2f s, J = %.3f'
              % (resultat['n_combinaisons'], resultat['duree_s'], resultat['J']))
    _CACHE[cle] = resultat
    return resultat


def _grille_trace(bande=BANDE_TRACE, n_par_octave=N_PAR_OCTAVE_TRACE):
    """Grille logarithmique dense, pour des courbes lisses (pas pour un critere)."""
    return MH.grille_log(bande[0], bande[1], n_par_octave)


def _interp_log(f, y, f0):
    """Interpolation log-log d'une grandeur positive en une frequence isolee."""
    return float(np.exp(np.interp(np.log(f0), np.log(f), np.log(y))))


def _texte_design(design, prefixe=''):
    """Ligne compacte 'L1 / C1 | C2 / L2' en mH et uF, pour un cartouche."""
    return ('%s%.3g mH / %.3g µF | %.3g µF / %.3g mH'
            % (prefixe, design['L1'] * 1e3, design['C1'] * 1e6,
               design['C2'] * 1e6, design['L2'] * 1e3))


# ---------------------------------------------------------------------------
# 2. Acte 1 -- la mesure d'impedance
# ---------------------------------------------------------------------------

def fig_z_sub_mesure(taille=None):
    """|Z(f)| et phase du sub, avec barres d'erreur : la figure de l'acte 1.

    CE QU'ELLE DOIT FAIRE COMPRENDRE EN DIX SECONDES : la charge n'est pas
    8 ohm. Le module varie du simple au sextuple dans la bande du raccord, et
    c'est exactement l'hypothese que le filtre catalogue suppose fausse.

    Deux incertitudes cohabitent et la figure les distingue, parce que les
    confondre fausse le chi2 et biaise Re (§ 09.3) :
      - barres verticales = incertitude ALEATOIRE point par point (colonne
        u_module_alea_ohm), celle qui pondere l'ajustement ;
      - bande continue = incertitude SYSTEMATIQUE de chaine (en-tete
        u_systematique_relative_pct), qui multiplie tous les points ensemble et
        ne s'applique qu'APRES l'ajustement, en propagation sur theta.
    """
    z = donnees_z()
    f, mod, phi = z['f'], z['module'], z['phase']
    u_syst = IO.meta_flottant(z['meta'], 'u_systematique_relative_pct', 0.0) / 100.0
    f2 = min(BANDE_TRACE[1], float(f.max()))

    fig, (haut, milieu, bas) = BP.figure(3, 1, taille=taille or BP.TAILLE_HAUTE,
                                         hauteurs=(2.1, 1.15, 0.85), sharex=True)

    if u_syst > 0:
        haut.fill_between(f, mod * (1 - u_syst), mod * (1 + u_syst),
                          color=BP.couleur('filet'), alpha=0.9, linewidth=0,
                          label='systématique de chaîne ±%s %%' % BP.fr(100 * u_syst, '%.1f'))
    haut.errorbar(f, mod, yerr=z['u_module'], fmt='o', markersize=2.2,
                  color=BP.couleur('mesure'), ecolor=BP.couleur('mesure'),
                  elinewidth=0.8, capsize=1.5, linestyle='none',
                  label='|Z| ± u aléatoire (k = 1)')
    haut.set_ylabel(TEXTES['module'])
    haut.set_ylim(0.8 * float(mod.min()), 1.6 * float(mod.max()))
    BP.axe_impedance(haut)

    f_pic, mod_pic = MH.pic_principal(f, mod)
    rapport = MH.rapport_max_min(f, mod, bande=BANDE_TRACE)
    z100 = _interp_log(f, mod, 100.0)
    haut.plot([f_pic], [mod_pic], marker='v', markersize=5,
              color=BP.couleur('somme'), linestyle='none', zorder=5)
    # Les chiffres du pic vont dans le cartouche, pas en annotation flottante :
    # aux abords du sommet la courbe occupe les deux cotes, et une etiquette qui
    # deborde de la figure l'ELARGIT (meme piege que blueprint_mpl.kicker).
    BP.repere_vertical(haut, 100.0, '100 Hz', haut=0.62)
    haut.plot([100.0], [z100], marker='o', markersize=4.5, markerfacecolor='none',
              markeredgecolor=BP.couleur('grave'), markeredgewidth=1.2, zorder=5)
    BP.cartouche(haut,
                 '▼ pic : %s Ω à %s Hz\n|Z|(100 Hz) = %s Ω\nmax/min = %s  (%g–%g Hz)\n'
                 '%d points'
                 % (BP.fr(mod_pic, '%.0f'), BP.fr(f_pic, '%.1f'), BP.fr(z100, '%.1f'),
                    BP.fr(rapport, '%.1f'), BANDE_TRACE[0], BANDE_TRACE[1], len(f)),
                 'bas gauche')
    BP.legende(haut, loc='upper right')

    milieu.axhline(0.0, color=BP.couleur('filet'), linewidth=0.8)
    milieu.errorbar(f, phi, yerr=z['u_phase'], fmt='o', markersize=2.0,
                    color=BP.couleur('mesure'), ecolor=BP.couleur('mesure'),
                    elinewidth=0.8, capsize=1.5, linestyle='none')
    milieu.set_ylabel(TEXTES['phase'])
    BP.repere_vertical(milieu, 100.0)

    # Troisieme panneau : LE BUDGET D'INCERTITUDE, sans lequel les barres du
    # panneau du haut sont invisibles -- 2 % sur une echelle qui couvre une
    # decade et demie, cela fait deux pixels. Or c'est precisement le partage
    # aleatoire / systematique qui decide de la pondera+tion de l'ajustement
    # (§ 09.3) : il merite son propre panneau plutot qu'une phrase en legende.
    bas.plot(f, 100 * z['u_module'] / mod, 'o', markersize=2.0,
             color=BP.couleur('mesure'), label='aléatoire, point par point')
    if u_syst > 0:
        bas.axhline(100 * u_syst, color=BP.couleur('alerte'), linewidth=1.2,
                    linestyle='--', label='systématique (en-tête, commun à tous)')
    bas.set_ylabel('u / |Z| (%)')
    haut_panneau = max(3.2, 1.45 * float(np.max(100 * z['u_module'] / mod)))
    bas.set_ylim(0, haut_panneau)
    bas.set_yticks([y for y in (0, 1, 2, 3, 4, 5) if y <= haut_panneau])
    BP.legende(bas, loc='lower left', ncols=2)
    BP.repere_vertical(bas, 100.0)
    BP.axe_frequence(bas, BANDE_TRACE[0], f2, textes=TEXTES)

    # LE TITRE DIT LE STATUT, comme l'estampille (correction de relecture du
    # 2026-09-14). Il ecrivait "IMPEDANCE MESUREE DU HAUT-PARLEUR" alors que les points
    # sortent de modele_hp.Z_ts : c'est exactement la phrase qu'un TIPE ne doit jamais
    # produire. L'estampille existait bien, mais en pied de page et en petit, et une
    # figure sortie du depot se retrouve un jour sur une diapositive sans sa legende --
    # c'est le risque que documente blueprint_mpl.marque_synthetique, et le titre le
    # recreait A L'INTERIEUR de l'image. Le jour ou mesures/ portera un CSV de statut
    # reel, le kicker redeviendra "mesurée" tout seul : le statut est deja lu par
    # io_mesures et recopie partout ailleurs.
    BP.kicker(fig, 'acte 1 — %s'
              % ('impédance mesurée du haut-parleur'
                 if _statut_est_une_mesure(z['statut'])
                 else 'impédance du haut-parleur : données SYNTHÉTIQUES, '
                      'pas une mesure'))
    BP.marque_synthetique(fig)
    return fig


# ---------------------------------------------------------------------------
# 3. Acte 2 -- le probleme inverse
# ---------------------------------------------------------------------------

def fig_fit_ts_sub(taille=None):
    """Trois panneaux : module, phase, residus normalises (§ 09.7).

    LE PANNEAU DU BAS EST LE PLUS IMPORTANT, et c'est le seul que personne ne
    regarde spontanement. Un modele qui passe "a l'oeil" au milieu des points
    peut avoir des residus organises en arche : cela signifie que l'ecart n'est
    plus du bruit mais un defaut de modele (semi-inductance, deuxieme pic...).
    Des residus repartis au hasard entre -2 et +2 sigma, eux, valident a la fois
    le modele ET les incertitudes injectees -- c'est la lecture du chi2 reduit.
    """
    z = donnees_z()
    res = identification()
    f, mod, phi = z['f'], z['module'], z['phase']
    modele = res['modele']
    theta = np.asarray(res['theta'], float)
    u = np.asarray(res['u_composee'], float)

    fd = _grille_trace((max(BANDE_TRACE[0], float(f.min())),
                        min(BANDE_TRACE[1], float(f.max()))))
    Z = TS.evaluer(modele, fd, theta)

    fig, (a, b, c) = BP.figure(3, 1, taille=taille or BP.TAILLE_HAUTE,
                               hauteurs=(2.1, 1.25, 1.05), sharex=True)

    a.errorbar(f, mod, yerr=z['u_module'], fmt='o', markersize=2.2,
               color=BP.couleur('mesure'), ecolor=BP.couleur('mesure'),
               elinewidth=0.7, capsize=1.2, linestyle='none', label=TEXTES['mesure'])
    a.plot(fd, np.abs(Z), color=BP.couleur('modele'), linewidth=1.7,
           label='%s (%s, %d paramètres)' % (TEXTES['modele'], modele, len(theta)))
    a.set_ylabel(TEXTES['module'])
    a.set_ylim(0.8 * float(mod.min()), 1.7 * float(mod.max()))
    BP.axe_impedance(a)
    BP.legende(a, loc='upper right')

    noms, unites = res['noms'], res['unites']
    echelles = {'H': (1e3, 'mH'), 'ohm': (1.0, 'Ω'), 'Hz': (1.0, 'Hz'), '-': (1.0, '')}
    lignes = []
    for nom, val, inc, unite in zip(noms, theta, u, unites):
        k, symbole = echelles.get(unite, (1.0, unite))
        lignes.append('%-4s %8s ± %-6s %s' % (nom, BP.fr(val * k, '%.4g'),
                                              BP.fr(inc * k, '%.2g'), symbole))
    lignes.append('χ² réduit %s' % BP.fr(res['chi2_reduit'], '%.2f'))
    BP.cartouche(a, '\n'.join(lignes), 'bas gauche')

    b.errorbar(f, phi, yerr=z['u_phase'], fmt='o', markersize=2.0,
               color=BP.couleur('mesure'), ecolor=BP.couleur('mesure'),
               elinewidth=0.7, capsize=1.2, linestyle='none')
    b.plot(fd, np.degrees(np.angle(Z)), color=BP.couleur('modele'), linewidth=1.5)
    b.axhline(0.0, color=BP.couleur('filet'), linewidth=0.8)
    b.set_ylabel(TEXTES['phase'])

    # Residus : le vecteur rendu par ts_fit empile [log-module ; phase] sur la
    # bande d'ajustement. On le recoupe en deux pour rendre chaque moitie a sa
    # frequence -- un residu sans son abscisse ne se diagnostique pas.
    r = np.asarray(res['residus']['r'], float)
    bande = res['bande_ajustement']
    masque = (f >= bande[0]) & (f <= bande[1])
    n = int(masque.sum())
    if r.size == 2 * n:
        r_mod, r_phi = r[:n], r[n:]
    else:                                       # forme inattendue : on ne devine pas
        r_mod, r_phi = r[:n], None
    fr = f[masque]
    for y in (-3, 3):
        c.axhline(y, color=BP.couleur('alerte'), linewidth=0.7, linestyle=':')
    c.axhspan(-1, 1, color=BP.couleur('filet'), alpha=0.8, linewidth=0)
    c.axhline(0.0, color=BP.couleur('filet'), linewidth=0.8)
    c.plot(fr, r_mod, 'o', markersize=2.4, color=BP.couleur('grave'), label='module')
    if r_phi is not None:
        c.plot(fr, r_phi, 's', markersize=2.4, color=BP.couleur('medium'), label='phase')
    c.set_ylabel(TEXTES['residus'])
    c.set_ylim(-4.0, 4.0)
    BP.legende(c, loc='upper right', ncols=2)
    BP.cartouche(c, 'RMS %s %% (module)  %s° (phase)  |r|max = %s σ'
                 % (BP.fr(res['residus']['rms_module_pct_ajustement'], '%.2f'),
                    BP.fr(res['residus']['rms_phase_deg_ajustement'], '%.2f'),
                    BP.fr(res['residus']['max_abs'], '%.1f')), 'haut gauche')
    BP.axe_frequence(c, float(fd.min()), float(fd.max()), textes=TEXTES)

    BP.kicker(fig, 'acte 2 — problème inverse : identification de Thiele-Small')
    BP.marque_synthetique(fig)
    return fig


# ---------------------------------------------------------------------------
# 4. Acte 3 -- le filtre catalogue face a la charge reelle
# ---------------------------------------------------------------------------

def _tracer_voies(ax, f, design, Zs, Zm, cible_nom, pol=-1, avec_cible=True,
                  avec_legende=True):
    """Trace |H_PB|, |H_PH| et la somme en dB sur un axe. Rend (S, f_x)."""
    H1 = F.H_pb(f, design['L1'], design['C1'], Zs)
    H2 = F.H_ph(f, design['C2'], design['L2'], Zm)
    S = F.sommer(f, H1, H2, pol=pol)
    ax.plot(f, BP.db(H1), color=BP.couleur('grave'), linewidth=1.4,
            label=TEXTES['grave'])
    ax.plot(f, BP.db(H2), color=BP.couleur('medium'), linewidth=1.4,
            label=TEXTES['medium'])
    ax.plot(f, BP.db(S), color=BP.couleur('somme'), linewidth=1.9,
            label=TEXTES['somme'])
    if avec_cible:
        Sc = F.cible_somme(f, cible_nom, f0_cible=100.0, pol=pol)
        ax.plot(f, BP.db(Sc), color=BP.couleur('cible'), linewidth=1.1,
                linestyle='--', label='cible %s' % cible_nom)
    try:
        f_x = F.frequence_croisement(f, H1, H2, bande=(40.0, 250.0), strict=False)
    except Exception:
        f_x = None
    if avec_legende:
        BP.legende(ax, loc='lower center', ncols=2)
    return S, f_x


def fig_catalogue_8ohm_vs_z(taille=None, cible_nom=CIBLE_DEFAUT):
    """Le meme filtre, sur 8 ohm resistifs puis sur la charge reelle.

    C'EST LA FIGURE QUI POSE LE PROBLEME DU TIPE. A gauche, sur une resistance
    de 8 ohm, le filtre catalogue fait exactement ce que la formule promet : deux
    pentes propres, un croisement a 100 Hz, une somme plate a 3 dB pres. A
    droite, la seule chose qui a change est la charge -- le meme L et le meme C,
    branches sur un vrai haut-parleur -- et la courbe part ailleurs. Le facteur
    de qualite d'une cellule LC vaut Q = R.racine(C/L) : il appartient a la
    CHARGE, et la charge n'est pas une resistance.
    """
    f = _grille_trace()
    Zs, Zm, _etiquette = charges(f)
    R = 8.0 + 0j * f
    taille = taille or (BP.TAILLE_DIAPO[0], BP.TAILLE_DIAPO[1] * 1.10)
    fig, (g, d) = BP.figure(1, 2, taille=taille, sharey=True)

    _S8, fx8 = _tracer_voies(g, f, DESIGN_CATALOGUE, R, R, cible_nom,
                             avec_legende=False)
    _Sz, fxz = _tracer_voies(d, f, DESIGN_CATALOGUE, Zs, Zm, cible_nom,
                             avec_legende=False)

    # Titres COURTS : axes.titlelocation vaut 'left' et bbox_inches='tight'
    # elargit le fichier de tout ce qui deborde a droite (cf. blueprint_mpl.kicker).
    for ax, titre, fx in ((g, 'sur 8 Ω résistifs', fx8),
                          (d, 'sur Z(f) réelle (acte 2)', fxz)):
        ax.set_title(titre)
        ax.set_ylim(-28, 18)
        BP.axe_frequence(ax, BANDE_TRACE[0], BANDE_TRACE[1], textes=TEXTES,
                         reperes=BP.REPERES_FREQUENCE_LARGE)
        BP.repere_vertical(ax, 100.0, '100 Hz', haut=0.30)
        if fx is not None:                       # f_c REEL, celui du croisement
            BP.repere_vertical(ax, fx, 'f_c = %s Hz' % BP.fr(fx, '%.0f'),
                               role='somme', haut=0.17, style_trait=':')
    g.set_ylabel(TEXTES['gain'])
    # Legende commune SOUS la figure : deux panneaux etroits ne peuvent pas
    # heberger quatre entrees sans que les axes s'ecrasent (constrained_layout
    # le signale alors par un avertissement, et la figure sort illisible).
    poignees, etiquettes = g.get_legend_handles_labels()
    fig.legend(poignees, etiquettes, loc='outside lower center', ncols=4,
               frameon=False, fontsize=plt.rcParams['font.size'] * 0.88)

    fg = F.grille_critere()
    Zs_c, Zm_c, _ = charges(fg)
    R_c = 8.0 + 0j * fg
    resume = []
    for nom, Za, Zb in (('8 Ω', R_c, R_c), ('Z(f)', Zs_c, Zm_c)):
        H1 = F.H_pb(fg, DESIGN_CATALOGUE['L1'], DESIGN_CATALOGUE['C1'], Za)
        H2 = F.H_ph(fg, DESIGN_CATALOGUE['C2'], DESIGN_CATALOGUE['L2'], Zb)
        S = F.sommer(fg, H1, H2)
        rms, emax = F.ecart_rms_db(fg, S, cible=None)[:2]
        fx = F.frequence_croisement(fg, H1, H2, strict=False)
        zin = F.verifier_contraintes(DESIGN_CATALOGUE, Z=Za, f=fg, Z_med=Zb)[2]
        resume.append((nom, rms, emax, fx, zin))

    for ax, (nom, rms, emax, fx, zin) in zip((g, d), resume):
        BP.cartouche(ax,
                     'écart RMS %6s dB\nécart max %6s dB\nf_c       %6s Hz\n'
                     'min|Zin|  %6s Ω'
                     % (BP.fr(rms, '%.2f'), BP.fr(emax, '%.2f'),
                        BP.fr(fx, '%.1f'), BP.fr(zin, '%.2f')), 'haut droite')

    BP.kicker(fig, 'acte 3 — le même filtre, deux charges (cible %s)' % cible_nom)
    BP.marque_synthetique(fig, 'SYNTHÉTIQUE — pas une mesure', position='haut')
    # mention raccourcie et remontee : le pied de cette figure porte deja la
    # legende commune, et la ligne du haut doit tenir avec le kicker.
    return fig


def fig_somme_catalogue_vs_optimise(taille=None, cible_nom=CIBLE_DEFAUT):
    """Catalogue contre optimise E12, sur la MEME charge reelle.

    HONNETETE DE LA COMPARAISON, POINT PAR POINT. Les deux designs sont evalues
    sur la meme charge, la meme cible, la meme bande, les memes poids, et avec
    des selfs IDEALES (aucune DCR injectee, D6 non gelee) -- hypothese qui
    favorise le catalogue, puisque ses selfs sont les plus grosses. Le seul
    ecart entre les deux colonnes est le choix des quatre composants.
    L'optimise est contraint a la grille E12 : ce n'est pas "le meilleur filtre
    possible", c'est "le meilleur filtre achetable".
    """
    f = _grille_trace()
    Zs, Zm, etiquette = charges(f)
    opt = optimisation(cible_nom)
    design_opt = O.design_de(opt)

    fig, (haut, bas) = BP.figure(2, 1, taille=taille or BP.TAILLE_HAUTE,
                                 hauteurs=(2.0, 1.15), sharex=True)

    Sc_cible = F.cible_somme(f, cible_nom, f0_cible=100.0)
    haut.plot(f, BP.db(Sc_cible), color=BP.couleur('cible'), linewidth=1.1,
              linestyle='--', label='cible %s' % cible_nom)
    courbes = []
    for design, nom, couleur, epaisseur in (
            (DESIGN_CATALOGUE, TEXTES['catalogue'], BP.couleur('somme'), 1.5),
            (design_opt, TEXTES['optimise'], BP.couleur('grave'), 1.9)):
        H1 = F.H_pb(f, design['L1'], design['C1'], Zs)
        H2 = F.H_ph(f, design['C2'], design['L2'], Zm)
        S = F.sommer(f, H1, H2)
        haut.plot(f, BP.db(S), color=couleur, linewidth=epaisseur, label=nom)
        courbes.append((design, nom, couleur, S))
    haut.set_ylabel('Somme (dB)')
    # Plafond CALCULE, pas devine : la surtension du catalogue sur charge reelle
    # depasse +15 dB, et une courbe coupee par le cadre donne l'impression d'un
    # bug alors que c'est le resultat.
    plafond = max(float(np.max(BP.db(S))) for _d, _n, _c, S in courbes)
    haut.set_ylim(-20, float(np.ceil(plafond)) + 3)
    BP.legende(haut, loc='lower left', ncols=1)

    fg = F.grille_critere()
    Zs_c, Zm_c, _ = charges(fg)
    lignes = []
    for design, nom, couleur, _S in courbes:
        H1 = F.H_pb(fg, design['L1'], design['C1'], Zs_c)
        H2 = F.H_ph(fg, design['C2'], design['L2'], Zm_c)
        S = F.sommer(fg, H1, H2)
        # ek est DEJA l'ecart point par point au niveau libre optimal (le
        # "niveau libre" du critere gele retire la constante) : on ne recentre
        # pas une deuxieme fois, ce serait compter deux fois la meme operation.
        rms, emax, fk, ek = F.ecart_rms_db(fg, S, cible=None)
        bas.plot(fk, ek, color=couleur, linewidth=1.5, label=nom)
        fx = F.frequence_croisement(fg, H1, H2, strict=False)
        zin = F.verifier_contraintes(design, Z=Zs_c, f=fg, Z_med=Zm_c)[2]
        # Meme modele de self que l'enumeration : un J affiche sur la figure et un J
        # calcule par la chaine doivent etre le MEME nombre.
        J = O.termes_du_design(design, fg, Zs_c, Zm_c, cible_nom=cible_nom,
                               w=O.W_SANITY, dcr=_dcr_figures())['J']
        lignes.append('%-26s  RMS %5s dB   max %5s dB   f_c %5s Hz   '
                      'min|Zin| %4s Ω   J %6s'
                      % (nom, BP.fr(rms, '%.2f'), BP.fr(emax, '%.2f'),
                         BP.fr(fx, '%.1f'), BP.fr(zin, '%.2f'), BP.fr(J, '%.2f')))
    bas.axhline(0.0, color=BP.couleur('filet'), linewidth=0.8)
    bas.set_ylabel('Écart (dB)')
    bas.set_ylim(-13, 17)
    BP.axe_frequence(bas, BANDE_TRACE[0], BANDE_TRACE[1], textes=TEXTES)
    for ax in (haut, bas):
        BP.repere_vertical(ax, 100.0, '100 Hz', haut=0.33)
    for x in (40.0, 250.0):
        bas.axvline(x, color=BP.couleur('cible'), linewidth=0.8, linestyle=':')
    bas.annotate('bande du critère 40–250 Hz', xy=(np.sqrt(40 * 250), 0.06),
                 xycoords=('data', 'axes fraction'), ha='center', va='bottom',
                 fontsize=plt.rcParams['font.size'] * 0.78,
                 color=BP.couleur('texte_doux'))

    BP.cartouche(haut, _texte_design(DESIGN_CATALOGUE, 'catalogue  ') + '\n'
                 + _texte_design(design_opt, 'optimisé   '), 'bas droite')
    lignes.append('charge : %s' % etiquette)
    fig.text(0.002, 0.052, '\n'.join(lignes), ha='left', va='bottom',
             fontsize=plt.rcParams['font.size'] * 0.74, family='monospace',
             color=BP.couleur('texte_doux'), linespacing=1.4)
    BP.reserver_bande(fig, bas=0.10)

    # "POIDS GELES" ETAIT UNE COLLISION DE VOCABULAIRE (correction de relecture du
    # 2026-09-14) : optim.W_SANITY (ex-W_GELE) designe les poids FIXES du sanity check
    # du § 04.7, pas la decision D5 du projet -- laquelle est encore ouverte, comme le
    # journal de la meme execution l'ecrit noir sur blanc. Deux sens du mot "gele" dans
    # un dossier dont l'argument d'honnetete est "les criteres ont ete geles avant les
    # mesures", c'est la contradiction la plus facile a exploiter par un jury, et elle
    # survivait hors de son contexte puisqu'elle etait DANS l'image.
    BP.kicker(fig, 'acte 3 — %d combinaisons E12, poids W_SANITY du § 04.7 '
                   '(D5 ouverte), selfs de Brooks (cible %s)'
              % (opt['n_combinaisons'], cible_nom))
    BP.marque_synthetique(fig)
    return fig


# ---------------------------------------------------------------------------
# 5. Satellite -- la self : masse, DCR, euros
# ---------------------------------------------------------------------------

def fig_self_cout_dcr(taille=None, inductances=(5.6e-3, 10e-3, 18e-3, 33e-3, 47e-3),
                      budget_eur=500.0):
    """Le compromis de la self : moins de pertes se paie en cuivre, vite.

    LE MODELE, ET SA LIMITE. A geometrie semblable, la masse de cuivre suit
    m = K_cu (L/r)^{3/2} (§ 05) : diviser la DCR par deux multiplie le cuivre
    par 2^{3/2} = 2,83. C'est cette loi, et non un catalogue, qui est tracee --
    K_cu = %s kg.s^{-3/2} et le prix du cuivre sont des ordres de grandeur
    ETIQUETES (D6 non gelee), d'ou l'axe des euros annote comme tel. Ce qui est
    robuste dans cette figure, c'est l'EXPOSANT 3/2, pas la position verticale
    des courbes.

    Le point marque est la bobine de Brooks calculee par self_bobine.brooks()
    pour un fil de 1,4 mm : ce n'est pas un ajustement, c'est la geometrie qui
    maximise L a longueur de fil donnee.
    """
    fig, (g, d) = BP.figure(1, 2, taille=taille or (BP.TAILLE_DIAPO[0],
                                                    BP.TAILLE_DIAPO[1] * 1.05))
    r = np.logspace(np.log10(0.12), np.log10(3.0), 200)

    for L in inductances:
        g.plot(r, SB.masse_pour(L, r), linewidth=1.5, label='%s mH' % BP.fr(L * 1e3, '%.3g'))
    BP.axe_log(g, 'x', [0.2, 0.3, 0.5, 0.7, 1, 1.5, 2, 3],
               bornes=(r[0], r[-1]), etiquette=TEXTES['dcr'])
    BP.axe_log(g, 'y', [0.1, 0.3, 1, 3, 10, 30, 100, 300], etiquette=TEXTES['masse'])
    BP.legende(g, loc='upper right', ncols=2, title='inductance')

    b = SB.brooks(18e-3)
    g.plot([b['r']], [b['m']], marker='o', markersize=5,
           markerfacecolor=BP.couleur('panneau'), markeredgecolor=BP.couleur('somme'),
           markeredgewidth=1.4, zorder=6)
    g.annotate('Brooks 18 mH', xy=(b['r'], b['m']), xytext=(7, 7),
               textcoords='offset points', ha='left', va='bottom',
               fontsize=plt.rcParams['font.size'] * 0.78, color=BP.couleur('somme'))
    BP.cartouche(g, 'm = K_cu (L/r)^3/2\nr ÷ 2  ⇒  m × 2,83\nK_cu = %s kg·s^-3/2\n'
                 'Brooks 18 mH, fil 1,4 mm :\n  %s Ω — %s kg — %s €'
                 % (BP.fr(SB.K_CU_DEFAUT, '%g'), BP.fr(b['r'], '%.2f'),
                    BP.fr(b['m'], '%.2f'), BP.fr(b['prix'], '%.0f')), 'bas gauche')

    perte = -SB.insertion_dB(r)                      # perte positive = ce qu'on perd
    for L in inductances:
        d.plot(perte, SB.prix_pour(L, r), linewidth=1.5,
               label='%s mH' % BP.fr(L * 1e3, '%.3g'))
    BP.axe_log(d, 'x', [0.05, 0.1, 0.2, 0.3, 0.5, 1, 2],
               bornes=(float(perte.min()), float(perte.max())),
               etiquette=TEXTES['insertion'])
    BP.axe_log(d, 'y', [10, 30, 100, 300, 1000, 3000], bornes=(5, 5e3),
               etiquette=TEXTES['prix'])
    d.axhline(budget_eur, color=BP.couleur('alerte'), linewidth=1.0, linestyle='--')
    d.annotate('budget du projet : %g € (toutes pièces)' % budget_eur,
               xy=(float(perte.min()), budget_eur), xytext=(4, 4),
               textcoords='offset points', ha='left', va='bottom',
               fontsize=plt.rcParams['font.size'] * 0.78, color=BP.couleur('alerte'))
    BP.cartouche(d, 'une self de 18 mH :\n  %s Ω → %s kg, %s €\n  %s Ω → %s kg, %s €\n'
                 '  %s Ω → %s kg, %s €'
                 % (BP.fr(0.5), BP.fr(SB.masse_pour(18e-3, 0.5), '%.1f'),
                    BP.fr(SB.prix_pour(18e-3, 0.5), '%.0f'),
                    BP.fr(1.0, '%.1f'), BP.fr(SB.masse_pour(18e-3, 1.0), '%.1f'),
                    BP.fr(SB.prix_pour(18e-3, 1.0), '%.0f'),
                    BP.fr(2.0, '%.1f'), BP.fr(SB.masse_pour(18e-3, 2.0), '%.1f'),
                    BP.fr(SB.prix_pour(18e-3, 2.0), '%.0f')), 'bas gauche')

    BP.kicker(fig, 'satellite — self : la sobriété se paie en cuivre '
                   '(K_cu et prix : ordres de grandeur)')
    BP.marque_synthetique(fig, 'MODÈLE — prix et K_cu à vérifier avant tout achat')
    return fig


# ---------------------------------------------------------------------------
# 6. Acte 3 (suite) -- la carte du cout
# ---------------------------------------------------------------------------

def _bords_log(valeurs):
    """Bords de cellules d'une grille logarithmique (moyennes geometriques).

    pcolormesh veut N+1 bords pour N valeurs. Sur une serie E12, les bords
    naturels sont les moyennes GEOMETRIQUES des valeurs voisines : la grille est
    geometrique (pas de 1,212 en ideal), pas arithmetique.
    """
    v = np.asarray(valeurs, float)
    interieurs = np.sqrt(v[:-1] * v[1:])
    return np.concatenate(([v[0] ** 2 / interieurs[0]], interieurs,
                           [v[-1] ** 2 / interieurs[-1]]))


def fig_plateau_optimum(taille=None, cible_nom=CIBLE_DEFAUT):
    """Carte de J dans le plan (L1, C1) : l'optimum est PLAT, et il faut le dire.

    CE QUE CETTE FIGURE PROUVE, ET QUI EST UN RESULTAT EN SOI. L'enumeration
    rend un vainqueur unique, ce qui donne l'illusion d'une precision qu'aucune
    mesure ne justifie. La carte montre la verite : plusieurs designs voisins se
    tiennent a quelques pourcents de J, et la derniere marche E12 pese souvent
    MOINS que la tolerance des composants (±10 % sur L, ±20 % sur C). Annoncer
    "l'optimum n'est pas distinguable de ses voisins" est honnete ; annoncer
    18,0 mH quand 15 mH fait pareil ne l'est pas.

    La carte est une COUPE : la voie medium est figee a son optimum, et seuls
    (L1, C1) varient. J n'est pas separable (les termes de somme et de phase
    couplent les deux voies, § 09.4), donc une coupe n'est pas la fonction
    entiere -- c'est ecrit sur la figure.
    """
    opt = optimisation(cible_nom)
    L_vals, C_vals = opt['L_vals'], opt['C_vals']
    n1, n2 = len(L_vals), len(C_vals)
    J = np.asarray(opt['J_matrice'], float)
    _i_opt, j_opt = opt['indices']
    # p1 = couples(L_vals, C_vals) : la premiere colonne (L1) varie le plus
    # lentement, donc l'indice i de p1 se relit en (i_L, i_C) par un reshape.
    carte = J[:, j_opt].reshape(n1, n2)                 # (indice L1, indice C1)
    J_min = float(np.nanmin(carte))

    # Niveaux DISCRETS et couleurs toutes tirees de --accent : le SVG ne contient
    # alors qu'un seul hexadecimal pour toute la carte, donc il reste recolorable
    # par blueprint-light.css (une palette continue figerait 200 couleurs).
    from matplotlib.colors import BoundaryNorm, ListedColormap, to_rgba
    ratios = [1.0, 1.02, 1.05, 1.15, 1.4, 2.0, 3.0, 1e9]
    alphas = [0.95, 0.78, 0.60, 0.44, 0.30, 0.18, 0.07]
    cmap = ListedColormap([to_rgba(BP.couleur('grave'), a) for a in alphas])
    norme = BoundaryNorm([J_min * x for x in ratios], cmap.N)

    fig, ax = BP.figure(1, 1, taille=taille or BP.TAILLE_DIAPO)
    maille = ax.pcolormesh(_bords_log(L_vals) * 1e3, _bords_log(C_vals) * 1e6,
                           carte.T, cmap=cmap, norm=norme, shading='flat',
                           edgecolors='none')
    BP.axe_log(ax, 'x', [1, 1.5, 2, 3, 4.7, 6.8, 10, 15, 22, 33, 47, 68],
               etiquette='Self série de la voie grave L₁ (mH)')
    BP.axe_log(ax, 'y', [10, 15, 22, 33, 47, 68, 100, 150, 220, 330, 470, 680],
               etiquette='Condensateur parallèle C₁ (µF)')
    ax.grid(False)

    barre = fig.colorbar(maille, ax=ax, pad=0.015, fraction=0.05,
                         ticks=[J_min * x for x in ratios[:-1]])
    barre.ax.set_yticklabels([BP.fr(x, '%.3g') for x in ratios[:-1]])
    barre.set_label('J / J_min')
    barre.outline.set_edgecolor(BP.couleur('filet'))
    barre.outline.set_linewidth(0.6)

    ax.plot([opt['L1'] * 1e3], [opt['C1'] * 1e6], marker='o', markersize=7,
            markerfacecolor='none', markeredgecolor=BP.couleur('somme'),
            markeredgewidth=1.6, zorder=6, label='optimum E12')
    ax.plot([DESIGN_CATALOGUE['L1'] * 1e3], [DESIGN_CATALOGUE['C1'] * 1e6],
            marker='s', markersize=6, markerfacecolor='none',
            markeredgecolor=BP.couleur('medium'), markeredgewidth=1.6, zorder=6,
            label='catalogue 8 Ω')
    BP.legende(ax, loc='upper left')

    plateau = opt['plateau']
    bord_ok, avertissements = opt['bord']
    texte = ('J minimal = %s\n%s\nplateau à 1 %% : %d design(s)\n'
             '2ᵉ meilleur : +%s %%\ncoupe à voie médium figée\n(%s µF / %s mH)'
             % (BP.fr(J_min, '%.3g'), _texte_design(O.design_de(opt)),
                plateau['n_dans_plateau'], BP.fr(plateau['ecart_2e_pct'], '%.1f'),
                BP.fr(opt['C2'] * 1e6, '%.3g'), BP.fr(opt['L2'] * 1e3, '%.3g')))
    BP.cartouche(ax, texte, 'haut droite')
    if not bord_ok:
        # Un optimum colle a une butee de la grille : ce n'est pas un optimum,
        # c'est une contrainte. Le dire sur la figure vaut mieux que de laisser
        # un lecteur croire que 10 uF est un choix (test (d) du § 09.6).
        # Premiere phrase seulement, repliee : le message complet de optim
        # explique aussi POURQUOI (ici, la contrainte d'ordre 2 qui manque) --
        # cela appartient au journal, pas a une diapositive.
        premiere = avertissements[0].split('. ')[0] + '.'
        ax.text(0.02, 0.02, '⚠ optimum sur un bord de la grille E12 :\n'
                + textwrap.fill(premiere, 52),
                transform=ax.transAxes, ha='left', va='bottom',
                fontsize=plt.rcParams['font.size'] * 0.76,
                color=BP.couleur('alerte'), zorder=7,
                bbox=dict(boxstyle='round,pad=0.25', facecolor=BP.couleur('panneau'),
                          edgecolor=BP.couleur('alerte'), linewidth=0.8))

    BP.kicker(fig, 'acte 3 — carte du coût J, cible %s : l’optimum est un plateau'
              % cible_nom)
    BP.marque_synthetique(fig)
    return fig


# ---------------------------------------------------------------------------
# 6 bis. Satellite -- le croisement energetique passif / actif (§ 06.8)
# ---------------------------------------------------------------------------

def fig_croisement_energie(taille=None, etas=(0.15, 0.40, 1.0),
                           P_repos=(1.0, 20.0), design=None):
    """Ou se croisent les deux architectures : conso au repos contre pertes Joule.

    LA FIGURE DIT TROIS CHOSES, DANS CET ORDRE.
      1. L'actif paie un FORFAIT : sa consommation au repos ne depend pas du
         niveau d'ecoute -- deux droites HORIZONTALES, une par comptabilite
         (marginale : les cartes AOP seules ; systeme : un second ampli entier).
      2. Le passif paie A L'USAGE : ses pertes croissent avec le niveau -- une
         BANDE, pas une droite, parce que le rendement de l'ampli est inconnu et
         qu'il divise toute la pente (§ 06.8).
      3. Les deux se croisent, et le croisement P* tombe A CHEVAL sur la zone
         d'ecoute domestique. La conclusion "le passif est plus sobre" n'est donc
         PAS acquise : elle depend de trois grandeurs encore NON MESUREES -- la
         DCR r, la consommation au repos P_0 et le rendement eta.

    POURQUOI LES DEUX AXES SONT EN WATTS AU COMPTEUR. C'etait la faute centrale du
    brouillon : P_0 se lit a la prise, tandis que les pertes Joule sont une chaleur
    dissipee en SORTIE d'amplificateur. Pour delivrer 1 W de plus en sortie il faut
    en tirer 1/eta au secteur. Tout est donc ramene au compteur, sans quoi on
    comparerait deux grandeurs qui n'ont pas la meme frontiere de bilan.

    CADRAGE A DIRE EN PREMIER (§ 06.9) : le haut-parleur dissipe lui-meme plus de
    97 % de ce qu'on lui envoie. Tout ce que montre cette figure est du second
    ordre -- mais c'est le seul ordre sur lequel le concepteur du filtre a prise.
    """
    design = dict(DESIGN_CATALOGUE if design is None else design)
    fg = _grille_trace()
    Zs, Zm, etiquette = charges(F.grille_critere())
    frac = EN.fraction_pertes(design, Zs, Z_med=Zm)
    d_dcr, provenance = EN._design_avec_dcr(design)

    P_voie = np.logspace(np.log10(0.2), np.log10(200.0), 200)
    fig, ax = BP.figure(1, 1, taille=taille or BP.TAILLE_DIAPO)

    # Le passif : une BANDE entre le meilleur et le pire rendement d'ampli.
    e_min, e_max = min(etas), max(etas)
    ax.fill_between(P_voie, frac * P_voie / e_max, frac * P_voie / e_min,
                    color=BP.couleur('grave'), alpha=0.22, linewidth=0,
                    label='passif : pertes Joule au compteur, η de %s à %s'
                          % (BP.fr(e_min, '%.2f'), BP.fr(e_max, '%.2f')))
    for e in sorted(etas):
        ax.plot(P_voie, frac * P_voie / e, linewidth=1.3,
                color=BP.couleur('grave'), alpha=0.9 if e == min(etas) else 0.55)

    # L'actif : un forfait, donc une horizontale par comptabilite.
    styles = ('-', '--')
    noms = ('marginale : cartes AOP seules', 'système : + un second ampli')
    for p0, st, nom_c in zip(P_repos, styles, noms):
        ax.axhline(p0, color=BP.couleur('medium'), linewidth=1.4, linestyle=st,
                   label='actif, comptabilité %s : P₀ = %s W'
                         % (nom_c, BP.fr(p0, '%.3g')))

    # Les croisements, un par (P_0, eta).
    for p0 in P_repos:
        for e in sorted(etas):
            p_etoile = EN.croisement(p0, d_dcr, Zs, eta=e, Z_med=Zm)
            if P_voie[0] <= p_etoile <= P_voie[-1]:
                ax.plot([p_etoile], [p0], marker='o', markersize=5,
                        markerfacecolor='none', markeredgecolor=BP.couleur('somme'),
                        markeredgewidth=1.4, zorder=6)

    BP.axe_log(ax, 'x', [0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200],
               bornes=(P_voie[0], P_voie[-1]), etiquette=TEXTES['niveau'])
    BP.axe_log(ax, 'y', [0.05, 0.1, 0.5, 1, 5, 10, 50, 100],
               bornes=(0.03, 150.0), etiquette=TEXTES['energie'])

    # Les deux niveaux d'ecoute de reference : D3 n'est PAS gelee, donc on trace
    # une ZONE etiquetee comme telle, jamais deux traits qui feraient croire a un
    # choix arrete.
    ax.axvspan(1.0, 10.0, color=BP.couleur('filet'), alpha=0.55, linewidth=0, zorder=0)
    # L'etiquette de la zone vit dans le cartouche et non en annotation flottante : a
    # cet endroit la bande du passif et la legende occupent deja les quatre coins, et
    # une etiquette qui deborde ELARGIT le fichier produit (cf. blueprint_mpl.kicker).
    BP.legende(ax, loc='upper left')

    BP.cartouche(ax,
                 'fraction de pertes sur Z(f) : %s %%\n'
                 '(catalogue sur 8 Ω : %s %%)\n'
                 'r₁ = %s Ω, r₂ = %s Ω\n'
                 'P* = η·P₀·(t_on/t_écoute) / fraction\n'
                 'zone ombrée : écoute domestique (D3 non gelée)\n'
                 'charge : %s'
                 % (BP.fr(100 * frac, '%.1f'),
                    BP.fr(100 * d_dcr['r1'] / (8.0 + d_dcr['r1']), '%.1f'),
                    BP.fr(d_dcr['r1'], '%.2f'), BP.fr(d_dcr['r2'], '%.2f'),
                    etiquette),
                 'bas droite')

    # Le kicker passe en MAJUSCULES (blueprint_mpl.kicker) : on evite d'y mettre des
    # lettres grecques minuscules, qui s'y transforment en capitales grecques
    # illisibles (eta -> H). On les nomme donc en toutes lettres.
    BP.kicker(fig, 'satellite — croisement énergétique : ni P0, ni le rendement, '
                   'ni la DCR ne sont mesurés')
    BP.marque_synthetique(fig, 'ORDRES DE GRANDEUR — aucune mesure de P₀ ni de η')
    return fig


# ---------------------------------------------------------------------------
# 7. Registre, generation, injection
# ---------------------------------------------------------------------------

FIGURES = OrderedDict([
    ('fig-z-sub-mesure', (fig_z_sub_mesure,
     'acte 1 : |Z| et phase du sub avec barres d erreur (aleatoire vs systematique)')),
    ('fig-fit-ts-sub', (fig_fit_ts_sub,
     'acte 2 : mesure contre modele ajuste, et residus normalises')),
    ('fig-catalogue-8ohm-vs-z', (fig_catalogue_8ohm_vs_z,
     'acte 3 : le filtre catalogue sur 8 ohm puis sur la charge reelle')),
    ('fig-somme-catalogue-vs-optimise', (fig_somme_catalogue_vs_optimise,
     'acte 3 : sommes predites, catalogue contre optimise E12')),
    ('fig-self-cout-dcr', (fig_self_cout_dcr,
     'satellite : masse de cuivre, DCR et euros de la self')),
    ('fig-plateau-optimum', (fig_plateau_optimum,
     'acte 3 : carte du cout J dans le plan (L1, C1), plateau de l optimum')),
    ('fig-croisement-energie', (fig_croisement_energie,
     'satellite : conso au repos de l actif contre pertes Joule du passif (§ 06.8)')),
])


def tout_generer(dossier=None, noms=None, variantes=('sombre',),
                 formats=('svg', 'png'), bavard=True, taille=None):
    """Produit toutes les figures et CONTROLE le resultat.

    Ne se contente pas d'ecrire : verifie que chaque fichier existe, qu'il n'est
    pas vide, et que le SVG ne contient AUCUNE couleur figee (critere du test (h)
    du § 09.6). Rend la liste des comptes rendus, un par figure et par
    variante ; la cle 'ok' vaut False des qu'un controle echoue.
    """
    dossier = dossier or DOSSIER_FIGURES
    noms = list(noms) if noms else list(FIGURES)
    inconnues = [n for n in noms if n not in FIGURES]
    if inconnues:
        raise KeyError('figure(s) inconnue(s) : %s' % ', '.join(inconnues))
    # Geometrie : chaque figure choisit sa hauteur (TAILLE_DIAPO ou TAILLE_HAUTE
    # selon son nombre de panneaux) ; on n'impose une taille commune que si
    # l'appelant le demande explicitement, ou si D7 est gelee.
    if taille is None:
        _taille_d7, origine = geometrie_deliverable()
        if 'D7 gelee' in origine:
            taille = _taille_d7
    else:
        origine = 'taille imposee par l appelant : %.2f x %.2f po' % tuple(taille)
    comptes = []
    if bavard:
        print('figures -> %s' % dossier)
        print('geometrie : %s ; DPI %d ; PNG %d dpi' % (origine, BP.DPI, BP.DPI_PNG))
    for variante in variantes:
        with BP.style(variante):
            for nom in noms:
                fonction = FIGURES[nom][0]
                t0 = time.time()
                fig = fonction(taille=taille)
                nom_fichier = nom + ('-clair' if variante == 'clair' else '')
                r = BP.enregistrer(fig, nom_fichier, dossier, formats=formats,
                                   variante=variante)
                r['duree_s'] = time.time() - t0
                r['figure'] = nom
                r['ok'] = (not r['hexa_figes']
                           and all(os.path.exists(c) for c in r['chemins'].values())
                           and all(o > 1024 for o in r['octets'].values()))
                comptes.append(r)
                if bavard:
                    print('  %-34s %5.1f ko svg  %6.1f ko png  %4d x %3d px  %4.1f s  %s'
                          % (nom_fichier, r['octets'].get('svg', 0) / 1024.,
                             r['octets'].get('png', 0) / 1024.,
                             r.get('px', (0, 0))[0], r.get('px', (0, 0))[1],
                             r['duree_s'],
                             'OK' if r['ok'] else 'ECHEC : ' + ', '.join(r['hexa_figes'])))
    if bavard:
        total = sum(sum(r['octets'].values()) for r in comptes)
        print('%d figure(s), %d fichier(s), %.1f ko au total ; %d couleur(s) figee(s)'
              % (len(comptes), sum(len(r['chemins']) for r in comptes), total / 1024.,
                 sum(len(r['hexa_figes']) for r in comptes)))
    return comptes


def injecter_figures(chemin_html, dossier, noms):
    """Inline chaque SVG DERRIERE son marqueur <!--FIG:nom--> (§ 09.7).

    IDEMPOTENTE, ET C'EST LE POINT IMPORTANT. Le marqueur n'est pas consomme : la
    figure est encadree par <!--FIG:nom--> ... <!--/FIG:nom-->, et une nouvelle
    injection remplace ce qui se trouve entre les deux. Sans cela on n'injecte
    qu'une fois : apres la premiere campagne de mesures le marqueur aurait disparu,
    et il faudrait rouvrir le HTML a la main pour mettre a jour la courbe -- alors
    que tout le protocole prevoit justement de REMESURER (deux niveaux d'ecoute,
    bobine chaude, apres correction du montage).

    Le bloc encadre peut donc etre n'importe quoi : le .placeholder ecrit a la main
    avant la premiere mesure, ou le SVG d'une injection precedente. Les deux sont
    remplaces de la meme facon.

    ECHEC FATAL si un marqueur est absent. C'est le defaut precis de _gen.py a la
    racine du depot : il cherchait des motifs sur un aria-label, n'en trouvait
    aucun, reecrivait le fichier a l'identique et affichait quand meme
    "OK injecte". Un faux positif silencieux est pire qu'une panne. On leve donc
    SystemExit, volontairement : un `except Exception` de confort ne peut pas
    l'avaler par megarde.

    Rend le nombre de figures injectees.
    """
    with open(chemin_html, encoding='utf-8') as fh:
        html = fh.read()
    n_avant = html.count('<svg')
    saut = chr(10)
    for nom in noms:
        ouvrant = '<!--FIG:%s-->' % nom
        fermant = '<!--/FIG:%s-->' % nom
        if ouvrant not in html:
            raise SystemExit('injecter_figures : marqueur %s absent de %s'
                             % (ouvrant, chemin_html))
        chemin_svg = os.path.join(dossier, nom + '.svg')
        if not os.path.exists(chemin_svg):
            raise SystemExit('injecter_figures : %s introuvable' % chemin_svg)
        with open(chemin_svg, encoding='utf-8') as fh:
            svg = fh.read()
        svg = svg[svg.index('<svg'):]              # on jette l en-tete XML
        bloc = ouvrant + saut + svg + saut + fermant
        if fermant in html:
            # Re-injection : on remplace tout ce qui separe les deux marqueurs.
            debut = html.index(ouvrant)
            fin = html.index(fermant, debut) + len(fermant)
            html = html[:debut] + bloc + html[fin:]
        else:
            html = html.replace(ouvrant, bloc, 1)
    with open(chemin_html, 'w', encoding='utf-8', newline=saut) as fh:
        fh.write(html)
    n_apres = html.count('<svg')
    manquants = [n for n in noms if ('<!--/FIG:%s-->' % n) not in html]
    if manquants:
        raise SystemExit('injecter_figures : controle final en echec, figures non '
                         'refermees : %s' % ', '.join(manquants))
    print('injecte %d figure(s) ; <svg> : %d -> %d' % (len(noms), n_avant, n_apres))
    return len(noms)
def demonstration(dossier=None, bavard=True, noms=None, variantes=('sombre',),
                  formats=('svg', 'png')):
    """Chaine complete : genere tout, controle les fichiers, teste l injection.

    L'injection est testee sur un HTML TEMPORAIRE, jamais sur les presentations
    du depot : une figure ne doit pas pouvoir modifier une diapositive par
    accident. Rend la liste des verdicts.
    """
    import tempfile
    dossier = dossier or DOSSIER_FIGURES
    comptes = tout_generer(dossier=dossier, bavard=bavard, noms=noms,
                           variantes=variantes, formats=formats)
    verdicts = [dict(nom=r['figure'], variante=r['variante'], ok=r['ok'],
                     octets=r['octets']) for r in comptes]
    noms = [r['figure'] for r in comptes if r['variante'] == 'sombre']
    fichier = os.path.join(tempfile.gettempdir(), 'tipe_test_injection.html')
    with open(fichier, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('<html><body>\n'
                 + '\n'.join('<figure class="viz"><!--FIG:%s--></figure>' % n for n in noms)
                 + '\n</body></html>\n')
    n = injecter_figures(fichier, dossier, noms)
    with open(fichier, encoding='utf-8') as fh:
        html = fh.read()
    ok = (n == len(noms) and '<!--FIG:' not in html and html.count('<svg') == len(noms))
    if bavard:
        print("test d'injection sur %s : %s" % (fichier, 'OK' if ok else 'ECHEC'))
    os.remove(fichier)
    verdicts.append(dict(nom='injection', variante='-', ok=ok, octets={}))
    return verdicts


def verifier(dossier=None, bavard=True):
    """Les controles du test (h) du § 09.6, sous forme consommable.

    Rend une liste de dict(nom, calc, attendu, ok), exactement la forme
    qu'attend un futur analyse/tests/test_figures.py en unittest : il lui
    suffira de boucler et d'appeler assertTrue(ligne['ok']).

    Les trois criteres chiffres du tableau du § 09.6 :
      - 0 couleur hexadecimale figee dans les SVG (hors repli var(--x, #hex)) ;
      - apres injection, 0 marqueur restant et autant de <svg> ajoutes que de
        figures demandees ;
    auxquels s'ajoute le controle elementaire "le fichier existe et n'est pas
    vide", sans lequel une figure vide passerait les deux autres.
    """
    dossier = dossier or DOSSIER_FIGURES
    verdicts = demonstration(dossier=dossier, bavard=bavard)
    lignes = []
    for v in verdicts:
        if v['nom'] == 'injection':
            lignes.append(dict(nom='injection HTML', calc='0 marqueur restant',
                               attendu='0 marqueur restant', ok=v['ok']))
            continue
        octets = v['octets']
        lignes.append(dict(nom=v['nom'], ok=v['ok'],
                           calc='svg %d o, png %d o' % (octets.get('svg', 0),
                                                        octets.get('png', 0)),
                           attendu='fichiers non vides, 0 couleur figee'))
    hexa = []
    for nom in FIGURES:
        chemin = os.path.join(dossier, nom + '.svg')
        if os.path.exists(chemin):
            hexa.extend(BP.verifier_svg(chemin))
    lignes.append(dict(nom='couleurs figees (test h)', calc='%d' % len(set(hexa)),
                       attendu='0', ok=not hexa))
    if bavard:
        print()
        for l in lignes:
            print('  %-34s %-34s %s' % (l['nom'], l['calc'], 'OK' if l['ok'] else 'ECHEC'))
    return lignes


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    arguments = sys.argv[1:]
    if '--liste' in arguments:
        print('figures disponibles (dossier par defaut : %s)' % DOSSIER_FIGURES)
        for nom, (_fonction, description) in FIGURES.items():
            print('  %-34s %s' % (nom, description))
        raise SystemExit(0)
    dossier = None
    if '--dossier' in arguments:
        i = arguments.index('--dossier')
        dossier = arguments[i + 1]
        del arguments[i:i + 2]
    if '--resultats' in arguments:
        dossier = DOSSIER_RESULTATS
        arguments.remove('--resultats')
    variantes = ('sombre', 'clair') if '--clair' in arguments else ('sombre',)
    formats = ('svg',) if '--svg-seul' in arguments else ('svg', 'png')
    noms = [a for a in arguments if not a.startswith('--')] or None

    print('figures.py -- figures du TIPE, identite Blueprint')
    donnees_z(bavard=True)
    identification(bavard=True)
    optimisation(bavard=True)
    print()
    if noms is None and variantes == ('sombre',) and formats == ('svg', 'png'):
        verdicts = verifier(dossier=dossier)          # rapport complet, criteres (h)
    else:
        verdicts = demonstration(dossier=dossier, noms=noms, variantes=variantes,
                                 formats=formats)
    echecs = [v for v in verdicts if not v['ok']]
    print()
    print('%d controle(s), %d echec(s)' % (len(verdicts), len(echecs)))
    raise SystemExit(1 if echecs else 0)
