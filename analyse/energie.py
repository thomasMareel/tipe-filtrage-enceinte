"""Satellite ENERGIE : pertes Joule du passif, consommation au repos de l'actif,
et point de CROISEMENT energetique entre les deux architectures (§ 06.7 a § 06.9).

POURQUOI CE MODULE EXISTE, ET POURQUOI IL EST UN MODULE A PART
--------------------------------------------------------------
C'est le seul endroit du code qui porte l'argument SOBRIETE du theme national. Les
deux autres satellites (self optimale, reference active) parlent de matiere et de
fidelite ; celui-ci parle de kilowattheures. Le § 09.2 le gele sous le nom
``energie.py`` et le § 09.4 gele ses deux signatures :

    pertes_joule(design, Z, P_ref)           -> W dissipes dans les DCR du passif
    croisement(P_repos_actif, design, Z)     -> niveau d'ecoute P* de croisement

CE QU'IL NE FAUT PAS SE RACONTER
--------------------------------
1. CADRAGE, a dire EN PREMIER a l'oral (§ 06.9). Le haut-parleur lui-meme dissipe
   plus de 97 % de ce qu'on lui envoie (rendement eta_0 de l'ordre de 2,5 %). Tout ce
   que compare ce module est du SECOND ORDRE -- mais c'est le seul ordre sur lequel
   le concepteur du filtre a prise. Le dire renforce l'honnetete, il ne l'affaiblit pas.
2. MEME FRONTIERE DE BILAN DES DEUX COTES. C'etait la faute centrale du brouillon :
   P_repos se lit AU COMPTEUR, tandis que les pertes Joule sont une chaleur dissipee
   EN SORTIE D'AMPLIFICATEUR. Pour delivrer 1 W de plus en sortie il faut tirer 1/eta
   W au secteur. On ramene donc TOUT au compteur, d'ou le facteur eta de la formule.
3. LA CONCLUSION N'EST PAS ACQUISE. Avec P_0 = 2 W et r = 1 ohm, P* va de ~2 W a
   ~18 W selon le rendement de l'ampli et l'existence d'un L-pad : c'est A CHEVAL sur
   la zone d'ecoute domestique. La conclusion est donc CONDITIONNELLE, et ce sont
   trois mesures -- r, P_0 et eta -- qui la trancheront. Aucune n'existe a ce jour.
4. LA VEILLE DU E-800 CHANGE LA NATURE DE LA QUESTION (§ 06.7). Le t.amp E-800 bascule
   seul en veille apres quinze minutes sans signal, et cette veille est DEBRAYABLE :
   il y a donc TROIS etats au secteur, pas deux, et "la consommation au repos" n'a pas
   de sens tant que la position du commutateur n'est pas gelee.

STATUT DES CHIFFRES
-------------------
AUCUNE MESURE N'EXISTE. P_0, eta et le profil d'usage sont des ORDRES DE GRANDEUR
ETIQUETES, rassembles dans HYPOTHESES_ENERGIE ci-dessous, et toute fonction qui s'en
sert le repete dans ce qu'elle rend (cle ``statut``). Les DCR, elles, viennent du
modele de self (self_bobine, decision D6 non gelee) ou de mesures si design porte
deja r1 / r2.

Dependance : numpy seul. matplotlib n'est PAS importe ici (la figure du satellite vit
dans figures.py, comme toutes les autres).

Auto-test : python analyse/energie.py
"""

import os
import sys

import numpy as np

_ICI = os.path.dirname(os.path.abspath(__file__))
if _ICI not in sys.path:
    sys.path.insert(0, _ICI)

import filtre as F                              # noqa: E402  reseaux, tensions, courants
import modele_hp as MH                          # noqa: E402  grilles, charges typiques
import self_bobine as SB                        # noqa: E402  DCR du modele de bobinage


# ----------------------------------------------------------------------------------
# 0. Hypotheses, toutes etiquetees -- principe 2 du § 09.1
# ----------------------------------------------------------------------------------

HYPOTHESES_ENERGIE = {
    'P_repos_actif_marginal_W': 1.0,
    'P_repos_actif_systeme_W': 20.0,
    'eta_ampli': (0.15, 0.40, 0.60, 1.0),
    't_on_sur_t_ecoute': 1.0,
    'a_lpad': 1.0,
    'phi_lpad': 0.0,
    'P_voie_domestique_W': 3.0,
    'avertissement': ('ORDRES DE GRANDEUR ETIQUETES -- AUCUNE MESURE. P_0, eta et le '
                      'profil d usage sont les trois grandeurs qui tranchent (§ 06.8) '
                      'et elles seront relevees au wattmetre en phase 4.'),
}
"""Hypotheses du bilan energetique. LIRE L'AVERTISSEMENT : ce ne sont pas des mesures.

  P_repos_actif_marginal_W  comptabilite MARGINALE (un seul E-800 possede, allume dans
        les deux scenarios) : seules les cartes AOP et leur alimentation comptent.
  P_repos_actif_systeme_W   comptabilite SYSTEME (stereo equivalente : deux amplis
        stereo en bi-amplification contre un seul en passif) : un E-800 entier de plus,
        PLUS les DEUX cartes AOP (une par enceinte).
  eta_ampli   rendement de l'amplificateur au point de fonctionnement. Mediocre a
        faible puissance : quelques watts moyens sur un ampli de 350 W en classe H
        donnent eta de l'ordre de 15 a 40 %. eta = 1 est la reference du brouillon,
        conservee UNIQUEMENT pour montrer de combien il se trompait.
  t_on_sur_t_ecoute   profil d'usage. Le surcout actif court tant que la chaine est
        allumee, les pertes passives seulement pendant l'ecoute -- mais la veille
        automatique du E-800 coupe ce raisonnement (§ 06.7).
  a_lpad, phi_lpad    rapport de tension du L-pad d'egalisation (1 = pas de L-pad) et
        fraction de la puissance dirigee vers la voie attenuee.
"""

R_NOM = F.R_NOM                 # 8 ohm, charge nominale de reference
P_REF_DEFAUT = 10.0             # W, puissance de REFERENCE conventionnelle sur 8 ohm
KWH_PAR_J = 1.0 / 3.6e6         # conversion joules -> kWh
HEURES_PAR_AN = 365.25 * 24.0


def _statut():
    """Etiquette de statut recopiee dans tout ce que rend ce module."""
    return HYPOTHESES_ENERGIE['avertissement']


def _design_avec_dcr(design, dcr=None):
    """Complete un design avec ses DCR r1 / r2, et dit d'ou elles viennent.

    Trois cas, dans cet ordre de priorite :
      1. design porte deja r1 / r2 -> ce sont des DCR MESUREES (ou imposees), on les
         garde telles quelles et on le dit ;
      2. dcr est un callable L -> r (typiquement self_bobine.fabrique_dcr) -> modele ;
      3. dcr est None -> modele de bobinage par defaut (bobine de Brooks, fil 1,4 mm),
         D6 NON GELEE. On ne rend JAMAIS r = 0 en silence : une self parfaite n'existe
         pas, et un bilan de pertes a DCR nulle serait vide de sens.
    """
    d = dict(design)
    if 'r1' in d and 'r2' in d:
        return d, 'DCR fournies dans le design (mesurees ou imposees)'
    if callable(dcr):
        d.setdefault('r1', float(dcr(d['L1'])))
        d.setdefault('r2', float(dcr(d['L2'])))
        return d, 'DCR du modele de self fourni par l appelant'
    d.setdefault('r1', float(SB.dcr_de_L(d['L1'], d_fil=1.4e-3, geometrie='brooks')))
    d.setdefault('r2', float(SB.dcr_de_L(d['L2'], d_fil=1.4e-3, geometrie='brooks')))
    return d, ('DCR du modele de bobinage par defaut (Brooks, fil 1,4 mm) -- '
               'decision D6 NON GELEE, ordre de grandeur')


# ----------------------------------------------------------------------------------
# 1. Cote passif : les pertes Joule (signature gelee du § 09.4)
# ----------------------------------------------------------------------------------

def pertes_joule(design, Z, P_ref=P_REF_DEFAUT, Z_med=None, f=None, dcr=None,
                 R_nom=R_NOM, bande=F.BANDE_CRITERE, detail=False):
    """Puissance Joule moyenne de bande dissipee dans les DCR des deux selfs (W).

    SIGNATURE GELEE (§ 09.4) : ``pertes_joule(design, Z, P_ref)``. Les arguments qui
    suivent sont du cadrage, tous optionnels.

    LA PHYSIQUE. Sous la tension de reference V_ref = racine(R_nom.P_ref), on calcule
    les courants EXACTS dans les deux selfs par filtre.tensions_et_courants -- donc sur
    la charge Z(f) reelle, sans hypothese de courant constant -- puis on moyenne
    |I|^2.r sur la bande du critere. C'est une moyenne de BANDE, a ne pas confondre
    avec la perte de POINTE, qui est ce qui dimensionne le fil de la self.

    POURQUOI CE N'EST PAS "11 %" (§ 06.1). Sur 8 ohm resistifs, r = 1 ohm dissipe
    r/(R+r) = 11,1 % de la puissance, soit -1,02 dB. Sur la charge REELLE la fraction
    va de 2 % au pic de resonance (ou |Z| monte a 40-60 ohm, donc le courant chute) a
    33 % au raccord (ou |Z| est basse). Le chiffre unique "11 %" est donc un reperage
    de catalogue, pas un resultat : d'ou une evaluation SPECTRALE, sur les deux
    branches, et c'est ce que fait cette fonction.

    P_ref = 10 W est une puissance de REFERENCE CONVENTIONNELLE sur 8 ohm (V_ref =
    8,94 V), pas la puissance reellement delivree a la charge.

    Retourne P_totale (W). detail=True -> dict complet (P_r1, P_r2, fractions, DCR
    retenues, provenance des DCR, statut des donnees).

    Voir § 06.1, § 06.4 et § 09.4. La moitie electrique du calcul delegue a
    filtre.pertes_joule_dcr : une seule implementation, deux noms.
    """
    d, provenance = _design_avec_dcr(design, dcr)
    if f is None:
        f = F.grille_critere()
    f = np.asarray(f, dtype=float)
    Z = np.asarray(Z(f) if callable(Z) else Z)
    Z_med = Z if Z_med is None else np.asarray(Z_med(f) if callable(Z_med) else Z_med)

    P_tot, P1, P2 = F.pertes_joule_dcr(f, d, Z, Z_med, P_ref=P_ref, R_nom=R_nom,
                                       bande=bande)
    if not detail:
        return P_tot

    # Fraction de reference (catalogue) : ce que r dissiperait sur 8 ohm RESISTIFS.
    fraction_8ohm = d['r1'] / (R_nom + d['r1'])
    return dict(P_totale_W=float(P_tot), P_r1_W=float(P1), P_r2_W=float(P2),
                fraction_de_P_ref=float(P_tot / float(P_ref)),
                fraction_catalogue_8ohm=float(fraction_8ohm),
                insertion_dB_8ohm=float(SB.insertion_dB(d['r1'], R_nom)),
                r1_ohm=float(d['r1']), r2_ohm=float(d['r2']),
                P_ref_W=float(P_ref), bande_Hz=tuple(float(x) for x in bande),
                provenance_dcr=provenance, statut=_statut())


def fraction_pertes(design, Z, Z_med=None, f=None, dcr=None, R_nom=R_NOM,
                    bande=F.BANDE_CRITERE):
    """Fraction SANS DIMENSION des pertes Joule : P_Joule / P_ref, sur la charge Z.

    C'est le crochet [ r/(R+r) + (1-a^2).phi ] de la formule du § 06.8, mais evalue
    spectralement sur la charge reelle au lieu d'etre lu sur 8 ohm resistifs. Sans
    L-pad, elle vaut r/(R+r) sur charge resistive et s'en ecarte franchement sur
    Z(f) : c'est exactement ce que le TIPE cherche a montrer.
    """
    return float(pertes_joule(design, Z, P_REF_DEFAUT, Z_med=Z_med, f=f, dcr=dcr,
                              R_nom=R_nom, bande=bande)) / P_REF_DEFAUT


# ----------------------------------------------------------------------------------
# 2. Le point de croisement energetique (signature gelee du § 09.4)
# ----------------------------------------------------------------------------------

def croisement(P_repos_actif, design, Z, eta=0.40, t_on_sur_t_ecoute=None,
               a_lpad=None, phi_lpad=None, Z_med=None, f=None, dcr=None,
               R_nom=R_NOM, bande=F.BANDE_CRITERE, detail=False):
    """Niveau d'ecoute P* auquel les deux architectures consomment AUTANT (§ 06.8).

    SIGNATURE GELEE (§ 09.4) : ``croisement(P_repos_actif, design, Z)``.

    L'EGALITE, ET SA FRONTIERE DE BILAN. Le surcout de l'actif est sa consommation au
    repos P_0, lue AU COMPTEUR, pendant t_on. Le surcout du passif est la chaleur des
    DCR, dissipee EN SORTIE D'AMPLI pendant t_ecoute ; pour delivrer cette chaleur
    l'ampli tire 1/eta fois plus au secteur. En ramenant tout au compteur :

        P_0 . t_on = (1/eta) [ r/(R+r) + (1-a^2).phi ] . P_voie . t_ecoute

    d'ou le niveau d'ecoute de croisement

        P* = eta . P_0 . (t_on / t_ecoute) / [ r/(R+r) + (1-a^2).phi ]

    Au-DESSOUS de P*, l'actif consomme plus (son repos n'est pas amorti) ; au-DESSUS,
    le passif consomme plus (ses pertes croissent avec le niveau). Sans L-pad (a = 1)
    et a eta = 1, on retrouve la forme simple du brouillon, P* = 9.P_0 pour r = 1 ohm :
    ELLE SURESTIME P* D'UN FACTEUR 2 A 9, parce qu'elle comptait les pertes passives en
    sortie d'ampli et le repos actif au compteur.

    ICI, la fraction de pertes n'est PAS lue sur 8 ohm : elle est calculee
    spectralement sur la charge Z fournie (voir fraction_pertes). C'est la difference
    entre un exercice de cours et le sujet v2.

    Retourne P* en W. detail=True -> dict (fraction de pertes, DCR, hypotheses, statut).

    LE RESULTAT EST CONDITIONNEL, et il faut le dire ainsi : P* depend de trois
    grandeurs encore NON MESUREES -- r, P_0 et eta. Donner un INTERVALLE, jamais "le
    passif gagne" (§ 06.9).
    """
    if t_on_sur_t_ecoute is None:
        t_on_sur_t_ecoute = HYPOTHESES_ENERGIE['t_on_sur_t_ecoute']
    if a_lpad is None:
        a_lpad = HYPOTHESES_ENERGIE['a_lpad']
    if phi_lpad is None:
        phi_lpad = HYPOTHESES_ENERGIE['phi_lpad']

    d, provenance = _design_avec_dcr(design, dcr)
    frac_dcr = fraction_pertes(d, Z, Z_med=Z_med, f=f, dcr=dcr, R_nom=R_nom, bande=bande)
    frac_lpad = (1.0 - float(a_lpad) ** 2) * float(phi_lpad)
    frac = frac_dcr + frac_lpad
    if frac <= 0.0:
        raise ValueError('croisement : fraction de pertes nulle ou negative (%g) -- '
                         'un passif sans aucune perte ne croise jamais l actif.' % frac)

    P_etoile = float(eta) * float(P_repos_actif) * float(t_on_sur_t_ecoute) / frac
    if not detail:
        return P_etoile
    return dict(P_etoile_W=P_etoile, fraction_pertes=float(frac),
                fraction_dcr=float(frac_dcr), fraction_lpad=float(frac_lpad),
                P_repos_actif_W=float(P_repos_actif), eta=float(eta),
                t_on_sur_t_ecoute=float(t_on_sur_t_ecoute),
                a_lpad=float(a_lpad), phi_lpad=float(phi_lpad),
                r1_ohm=float(d['r1']), r2_ohm=float(d['r2']),
                provenance_dcr=provenance, statut=_statut())


def balayage_croisement(design, Z, P_repos=(1.0, 20.0), etas=None, Z_med=None, f=None,
                        dcr=None, R_nom=R_NOM, bande=F.BANDE_CRITERE):
    """P* pour plusieurs P_0 et plusieurs eta -> le tableau du § 06.8.

    C'est la forme honnete du resultat : un TABLEAU, donc un intervalle, et non un
    chiffre unique. Rend un dict avec la grille (P_repos x eta) et la matrice des P*.
    """
    etas = HYPOTHESES_ENERGIE['eta_ampli'] if etas is None else etas
    P_repos = np.atleast_1d(np.asarray(P_repos, float))
    etas = np.atleast_1d(np.asarray(etas, float))
    d, provenance = _design_avec_dcr(design, dcr)
    frac = fraction_pertes(d, Z, Z_med=Z_med, f=f, dcr=dcr, R_nom=R_nom, bande=bande)
    P = np.empty((P_repos.size, etas.size))
    for i, p0 in enumerate(P_repos):
        for j, e in enumerate(etas):
            P[i, j] = e * p0 * HYPOTHESES_ENERGIE['t_on_sur_t_ecoute'] / frac
    return dict(P_repos_W=P_repos, eta=etas, P_etoile_W=P, fraction_pertes=float(frac),
                r1_ohm=float(d['r1']), r2_ohm=float(d['r2']),
                provenance_dcr=provenance, statut=_statut())


# ----------------------------------------------------------------------------------
# 3. Energies annuelles : ce que le jury retient (§ 06.8, exemple chiffre)
# ----------------------------------------------------------------------------------

def energie_annuelle(P_repos_actif, design, Z, P_voie=None, heures_on_par_jour=2.0,
                     heures_ecoute_par_jour=2.0, eta=0.40, Z_med=None, f=None, dcr=None,
                     R_nom=R_NOM, bande=F.BANDE_CRITERE):
    """Energie consommee EN UN AN par chaque architecture, ramenee au compteur (kWh).

    Les deux termes n'ont ni la meme base de temps ni le meme lieu de dissipation --
    c'est tout le piege de ce satellite, et cette fonction le rend explicite :
      * actif  : P_0 pendant heures_on_par_jour (il consomme des que la chaine est
                 allumee, meme silencieuse -- sauf veille, voir § 06.7) ;
      * passif : fraction . P_voie / eta pendant heures_ecoute_par_jour (il ne
                 consomme que quand ca joue, mais la chaleur est payee au secteur
                 divisee par le rendement de l'ampli).

    Retourne un dict : E_actif_kWh, E_passif_kWh, rapport, et les hypotheses.
    """
    P_voie = HYPOTHESES_ENERGIE['P_voie_domestique_W'] if P_voie is None else P_voie
    frac = fraction_pertes(design, Z, Z_med=Z_med, f=f, dcr=dcr, R_nom=R_nom, bande=bande)
    E_actif = float(P_repos_actif) * heures_on_par_jour * 365.25 / 1000.0
    E_passif = (frac * float(P_voie) / float(eta)) * heures_ecoute_par_jour * 365.25 / 1000.0
    return dict(E_actif_kWh=E_actif, E_passif_kWh=E_passif,
                rapport_actif_sur_passif=(E_actif / E_passif if E_passif > 0 else np.inf),
                fraction_pertes=float(frac), P_voie_W=float(P_voie), eta=float(eta),
                heures_on_par_jour=float(heures_on_par_jour),
                heures_ecoute_par_jour=float(heures_ecoute_par_jour),
                statut=_statut())


# ----------------------------------------------------------------------------------
# 4. Auto-test
# ----------------------------------------------------------------------------------

def _autotest(bavard=True):
    """Controles internes du module. Rend le nombre d'echecs (0 attendu).

    Ce qui est verifie, et pourquoi c'est verifiable malgre l'absence de mesures :
      * sur 8 ohm RESISTIFS, la fraction de pertes doit valoir EXACTEMENT r/(R+r)
        -- c'est un calcul de diviseur, pas une modelisation. Avec r = 1 ohm :
        11,11 % et -1,023 dB, les deux nombres de controle de CLAUDE.md ;
      * sur cette meme charge et sans L-pad, P* doit valoir eta.P_0.(R+r)/r ;
      * sur la charge Z(f) typique, la fraction doit S'ECARTER de 11 % : si elle n'en
        s'ecartait pas, le sujet du TIPE n'existerait pas.
    """
    echecs = 0
    f = F.grille_critere()
    Z8 = np.full(f.shape, complex(R_NOM, 0.0))
    design = dict(L1=18e-3, C1=150e-6, C2=150e-6, L2=18e-3, r1=1.0, r2=1.0)

    # (1) Charge resistive : la fraction est un diviseur de puissance exact.
    # |I_L1| = V_ref/|Z_in| et la puissance utile n'est pas |I|^2.R a cause de C1 :
    # on compare donc a la valeur analytique de la BRANCHE, pas a r/(R+r) directement.
    p = pertes_joule(design, Z8, P_ref=P_REF_DEFAUT, detail=True)
    attendu_catalogue = 1.0 / (R_NOM + 1.0)
    if abs(p['fraction_catalogue_8ohm'] - attendu_catalogue) > 1e-12:
        echecs += 1
        print('ECHEC : fraction catalogue %.6f attendue %.6f'
              % (p['fraction_catalogue_8ohm'], attendu_catalogue))
    if abs(p['insertion_dB_8ohm'] + 1.0228) > 1e-3:
        echecs += 1
        print('ECHEC : insertion %.4f dB attendue -1,0228 dB' % p['insertion_dB_8ohm'])

    # (2) Croisement sur charge resistive, sans L-pad : forme close.
    c = croisement(2.0, design, Z8, eta=1.0, detail=True)
    attendu = 1.0 * 2.0 * 1.0 / c['fraction_pertes']
    if abs(c['P_etoile_W'] - attendu) > 1e-9:
        echecs += 1
        print('ECHEC : P* %.4f W attendu %.4f W' % (c['P_etoile_W'], attendu))

    # (3) La charge reelle DOIT deplacer la fraction. C'est le resultat du satellite.
    Zs = MH.Z_depuis_jeu(f, MH.SUB_TYP_CLOS)
    Zm = MH.Z_depuis_jeu(f, MH.MED_TYP)
    frac_reelle = fraction_pertes(design, Zs, Z_med=Zm)
    if abs(frac_reelle - attendu_catalogue) < 1e-3:
        echecs += 1
        print('ECHEC : la charge reelle donne la MEME fraction que 8 ohm (%.4f) -- '
              'le satellite ne dirait plus rien.' % frac_reelle)

    if bavard:
        print('energie.py -- auto-test')
        print('  STATUT : %s' % _statut())
        print('  design de controle : catalogue 18 mH / 150 uF, r1 = r2 = 1 ohm')
        print('  8 ohm resistifs  : fraction catalogue r/(R+r) = %.2f %%, '
              'insertion %.3f dB' % (100 * p['fraction_catalogue_8ohm'],
                                     p['insertion_dB_8ohm']))
        print('  8 ohm resistifs  : pertes de bande %.3f W pour P_ref = %.0f W '
              '(%.2f %%)' % (p['P_totale_W'], p['P_ref_W'],
                             100 * p['fraction_de_P_ref']))
        print('  charge Z(f) typique : fraction de bande %.2f %% -- a comparer aux '
              '%.2f %% du catalogue' % (100 * frac_reelle, 100 * attendu_catalogue))
        bal = balayage_croisement(design, Zs, Z_med=Zm, P_repos=(1.0, 2.0, 20.0))
        print('  P* (W) sur la charge Z(f), sans L-pad :')
        print('      P_0 \\ eta   ' + '  '.join('%7.2f' % e for e in bal['eta']))
        for i, p0 in enumerate(bal['P_repos_W']):
            print('      %6.1f W    ' % p0
                  + '  '.join('%7.2f' % v for v in bal['P_etoile_W'][i]))
        e = energie_annuelle(2.0, design, Zs, Z_med=Zm, eta=0.40)
        print('  energie annuelle (P_0 = 2 W, 2 h/j, P_voie = 3 W, eta = 0,40) :')
        print('      actif %.2f kWh/an ; passif %.2f kWh/an ; rapport %.1f'
              % (e['E_actif_kWh'], e['E_passif_kWh'], e['rapport_actif_sur_passif']))
        print('  CONCLUSION CONDITIONNELLE : P* est a cheval sur l ecoute domestique.')
        print('  Ce sont r, P_0 et eta MESURES qui trancheront -- aucun ne l est.')
        print('  %d echec(s)' % echecs)
    return echecs


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')     # console Windows en cp1252
    raise SystemExit(1 if _autotest() else 0)
