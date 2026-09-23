"""Allège un PDF exporté par decktape, SANS PERTE, pour tenir le plafond SCEI de 5 Mo.

LE PROBLÈME. Chrome convertit les polices web du thème (Inter, JetBrains Mono,
Space Grotesk, servies en woff2) en polices « Type 3 » : chaque lettre devient un
petit dessin vectoriel. Et decktape imprime chaque vue SÉPARÉMENT avant de
fusionner : chaque page embarque donc ses propres copies de ces dessins. Mesure du
23/09/2026 sur la présentation finale (50 vues) : 9 643 dessins de glyphes, dont
506 seulement sont distincts ; ils pesaient 2,81 Mo sur 5,20 Mo, soit 54 % du
fichier — le plafond était dépassé à cause d'eux, pas à cause du contenu.

LA CORRECTION. Pour chaque dessin de glyphe, on calcule l'empreinte de son contenu
décompressé ; toutes les copies identiques sont remplacées par une référence à un
seul exemplaire. Le rendu est rigoureusement identique : ce sont les mêmes octets
de dessin, simplement stockés une fois. Les polices qui dépendent de ressources
propres (images, motifs) sont laissées intactes, par prudence : deux dessins
identiques pourraient alors désigner des ressources différentes.

CE QUE LE SCRIPT VÉRIFIE avant d'écrire : même nombre de pages, même texte
extrait page par page, et un fichier structurellement valide (contrôle de qpdf).
S'il échoue, le fichier d'origine n'est pas touché.

Usage :  python _alleger_pdf.py fichier.pdf [autre.pdf ...]
"""
import hashlib
import os
import sys

import pikepdf

sys.stdout.reconfigure(encoding='utf-8')

RESSOURCES_A_RISQUE = ('/XObject', '/Pattern', '/Shading', '/Font', '/ExtGState')


def texte_par_page(chemin):
    from pypdf import PdfReader
    return [(p.extract_text() or '') for p in PdfReader(chemin).pages]


def alleger(chemin):
    avant = os.path.getsize(chemin)
    textes_avant = texte_par_page(chemin)
    pdf = pikepdf.open(chemin, allow_overwriting_input=True)
    canon = {}          # empreinte -> flux canonique
    remplaces = 0
    polices_ignorees = 0
    for obj in pdf.objects:
        if not (isinstance(obj, pikepdf.Dictionary) and obj.get('/Type') == '/Font'
                and str(obj.get('/Subtype')) == '/Type3' and '/CharProcs' in obj):
            continue
        res = obj.get('/Resources')
        if res is not None and any(k in res for k in RESSOURCES_A_RISQUE):
            polices_ignorees += 1
            continue
        procs = obj['/CharProcs']
        for nom in list(procs.keys()):
            flux = procs[nom]
            empreinte = hashlib.sha256(flux.read_bytes()).hexdigest()
            if empreinte in canon:
                if canon[empreinte].objgen != flux.objgen:
                    procs[nom] = canon[empreinte]
                    remplaces += 1
            else:
                canon[empreinte] = flux
    temporaire = chemin + '.allege'
    # qpdf n'écrit que les objets encore atteignables : les copies orphelines disparaissent.
    pdf.save(temporaire, object_stream_mode=pikepdf.ObjectStreamMode.generate,
             compress_streams=True)
    pdf.close()

    try:
        verif = pikepdf.open(temporaire)
        # le nom de la methode a change selon les versions de pikepdf
        controle = getattr(verif, 'check_pdf_syntax', None) or getattr(verif, 'check')
        problemes = controle()
        n_pages = len(verif.pages)
        verif.close()
        textes_apres = texte_par_page(temporaire)
    except Exception:
        os.remove(temporaire)
        raise
    if problemes or n_pages != len(textes_avant) or textes_apres != textes_avant:
        os.remove(temporaire)
        raise SystemExit('%s : ECHEC de la verification (%s) — fichier d\'origine intact'
                         % (chemin, problemes or 'pages ou texte differents'))
    os.replace(temporaire, chemin)
    apres = os.path.getsize(chemin)
    print('%-38s %5.2f Mo -> %5.2f Mo  (%d glyphes dedupliques, %d distincts, '
          '%d polices laissees intactes ; %d pages, texte identique)'
          % (os.path.basename(chemin), avant / 1e6, apres / 1e6, remplaces,
             len(canon), polices_ignorees, n_pages))
    return apres


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        raise SystemExit(1)
    for f in sys.argv[1:]:
        alleger(f)
