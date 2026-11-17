# Rapport de rythme : vidéo d'entraînement de l'oral du 18/11/2026

**Vidéo (non répertoriée)** : https://youtu.be/boE136EmLqw
Durée : **7 min 12 s** (431,6 s). Voix « Camille » de Mistral, sous-titres français
intégrés à YouTube. Fabriquée le 17/11/2026 d'après `oral/CONSIGNES_VIDEO.md`, sans
toucher au texte ni aux diapositives.

## 1. Rythme vue par vue

« Durée mesurée » : temps d'affichage de la vue dans la vidéo, soit sa phrase lue
plus une seconde de respiration (trois secondes sur la dernière vue). « Durée visée »
et « début visé » viennent de `script_oral.json`, calculés pour un débit de 150 mots/min.

| Vue | Titre | Début | Début visé | Durée mesurée | Durée visée | Écart |
|---:|---|---:|---:|---:|---:|---:|
| 1 | Optimiser le filtre de mon enceinte sur son impédance réelle | 00:00 | 0:00 | 18,0 s | 20 s | −2,0 s (−10 %) |
| 2 | Le haut-parleur n'est pas une résistance de 8 Ω | 00:18 | 0:20 | 40,0 s | 50 s | **−10,0 s (−20 %)** |
| 3 | Ma problématique, et la démarche en quatre étapes | 00:58 | 1:10 | 36,0 s | 39 s | −3,0 s (−8 %) |
| 4 | Quatre expériences, une règle | 01:34 | 1:49 | 28,5 s | 31 s | −2,5 s (−8 %) |
| 5 | Mesurer l'impédance Z(f) du haut-parleur | 02:02 | 2:20 | 56,4 s | 65 s | −8,6 s (−13 %) |
| 6 | Étalonner : la chaîne doit retrouver des valeurs connues | 02:58 | 3:25 | 41,7 s | 47 s | −5,3 s (−11 %) |
| 7 | De la courbe mesurée au meilleur filtre | 03:40 | 4:12 | 37,6 s | 43 s | −5,4 s (−12 %) |
| 8 | Bobiner les selfs, et mesurer ce qu'elles coûtent | 04:18 | 4:55 | 42,8 s | 47 s | −4,2 s (−9 %) |
| 9 | Les filtres branchés sur les vrais haut-parleurs | 05:01 | 5:42 | 40,5 s | 44 s | −3,5 s (−8 %) |
| 10 | Le micro en champ proche, et le wattmètre | 05:41 | 6:26 | 46,2 s | 55 s | **−8,8 s (−16 %)** |
| 11 | Garde-fous et calendrier | 06:27 | 7:21 | 36,1 s | 41 s | −4,9 s (−12 %) |
| 12 | Questions ? | 07:03 | 8:02 | 7,7 s | 7 s | +0,7 s (+10 %) |
| | **Total** | | | **431,6 s = 7 min 12 s** | **489 s = 8 min 09 s** | **−57 s (−12 %)** |

Les débuts sont en partie entière de seconde, comme le chrono incrusté.

## 2. Durée totale : hors fourchette, même au ralentissement maximal

- **Au débit naturel, Camille lit à 191 mots/min**, contre 150 prévus : 6 min 16 s de
  parole, soit **6 min 28 s** avec une respiration d'une seconde par vue.
- Comme le prévoient les consignes, la voix a été **ralentie globalement de 10 %**, le
  maximum permis (facteur 0,90, hauteur de voix conservée, même réglage pour toutes les
  vues). Débit obtenu : **172 mots/min**.
- Total selon la règle des consignes (parole + 1 s par vue) : **7 min 09 s** ; vidéo
  complète, avec trois secondes sur la dernière vue : **7 min 12 s**.
- **L'écart persiste : il manque environ 20 s pour atteindre 7 min 30** (18 s sur la
  vidéo complète). Rien d'autre n'a été
  changé (ni le texte, ni la vitesse d'une seule vue).
- **Lecture pratique.** Les proportions entre vues restent bonnes, mais la vidéo est
  environ 12 % plus rapide que le débit de référence. À 150 mots/min, Thomas fera
  environ 8 min 09 : multiplier les temps de la vidéo par 1,13, ou lire la colonne
  « début visé ».
- **Si Thomas veut une vidéo dans la fourchette** (sa décision) : facteur 0,85 →
  7 min 36 ; facteur 0,80 → 8 min 04, au prix d'une voix nettement plus lente que
  naturelle.

## 3. Vues à plus de 15 % d'écart

- **Vue 2 (−20 %)** et **vue 10 (−16 %)**. Leur durée visée correspond pourtant au même
  débit de 150 mots/min que les autres vues. L'écart vient de la voix, qui accélère sur
  ces deux vues (188 et 180 mots/min contre 163 à 174 ailleurs). **Ce n'est pas un
  déséquilibre du texte** : rien à corriger dans le script pour cette raison.
- Aucune vue n'est nettement plus longue que prévu. La vue 12 (+0,7 s) ne dépasse que
  par ses trois secondes finales de silence.

## 4. Prononciation

Chaque audio a été **transcrit automatiquement** (reconnaissance vocale Mistral) puis
comparé au texte, en particulier sur les termes de `CONTEXTE.md`, section 5.

**Corrections appliquées (audio seulement ; sous-titres et JSON inchangés) :**

| Vue | Mot | Ce que donnait la substitution du JSON | Réécriture pour l'audio | Résultat |
|---:|---|---|---|---|
| 7 | IA | « I. A. » : la voix dit « d'une I… » puis, après une pause, « A » (transcrit « du NII. Ah ») ; défaut reproduit sur une phrase isolée | « I.A. » (sans espaces) | transcrit « d'une IA » |
| 5 | REW | « R. E. W. » : transcrit « R. Et W » par trois modèles ; le E est probablement dit « é » au lieu de « eu » | « èr-eu-double-vé » | transcrit « REW » |

**Proposition pour Thomas** (il décide ; le JSON n'a pas été modifié) : dans
`substitutions_tts` de `script_oral.json`, remplacer « I. A. » par « I.A. » et
« R. E. W. » par « èr-eu-double-vé ».

**Vérifiés, sans correction :**
- TIPE (dit « tipe », transcrit « type », homophone attendu) ;
- GBF, MCOT (transcrit « M-Cote ») ;
- bass-reflex (transcrit « bas réflexe ») ;
- selfs, « L sur r », évents.
- Les liaisons « huit‿ohms » et « cent‿ohms » sont normales.

**À écouter une fois — vue 8, vers 04:39 :** « à la puissance trois demis ».
- La transcription écrit « 3,5 » ; cela ne prouve rien, car elle écrit aussi « 3,5 »
  quand on synthétise exprès « trois demis ».
- Un modèle audio interrogé a donné des réponses contradictoires, y compris sur des
  échantillons de référence : il n'est pas fiable ici.
- Les spectrogrammes de la vue 8 ont la même signature que des références
  « trois demis » : une explosion de [d] juste après « trois », sans la liaison [z] de
  « trois et demi ».
- La prise retenue dit donc très probablement « trois demis ». Un « trois et demi »
  serait une erreur de physique (exposant 3,5 au lieu de 3/2) : une écoute suffit à
  trancher.

## 5. Fabrication

- **Images** : pages 1 à 12 de `presentation.pdf` en PNG 1440 × 1080 (`pdftoppm`) ;
  aucune annexe dans la vidéo.
- **Voix** : modèle `voxtral-mini-tts-3`, voix « Camille » (préréglage français).
  `voxtral-mini-tts-latest` refuse cette voix.
  - Texte = champ `texte` de chaque vue après `substitutions_tts`, plus les deux
    réécritures ci-dessus.
  - La transition n'est dite qu'une fois.
- **Montage** :
  - ralentissement de 0,90 (rubberband) pour toutes les vues ;
  - H.264 1440 × 1080 à 25 images/s, AAC 48 kHz stéréo ;
  - changements de vue calés à l'image près sur la fin de la respiration.
  - Contrôles faits : 24 images aux changements de vue (diapositive, numéro et chrono
    justes), début et fin de parole intacts après ralentissement, chrono de 00:00 à
    07:11 pour 431,6 s.
- **Incrustations** : « vue n / 12 » en haut à gauche et chrono mm:ss en haut à droite.
  Police de 27 px (2,5 % de la hauteur) sur fond sombre semi-transparent, dans la marge
  haute, vide sur les 12 vues.
- **Sous-titres** (`presentation_oral.srt`, 140 sous-titres) :
  - tirés du texte **original**, au plus 2 lignes de 42 caractères ;
  - aucun chevauchement, aucun débordement sur la vue suivante.
  - Calage : la synthèse ne fournit pas d'horodatages. Plutôt que le prorata des
    caractères prévu en repli, chaque sous-titre est calé sur les horodatages mot à
    mot de la transcription de l'audio ; 91 à 100 % des mots sont ancrés selon les
    vues, les autres sont interpolés au prorata des caractères.
- **YouTube** :
  - visibilité non répertoriée, « pas conçue pour les enfants », catégorie Éducation ;
  - 11 chapitres dans la description (vue 12 fusionnée avec la vue 11) ;
  - sous-titres français actifs ; traitement terminé en HD.
- **Test du lien sans connexion** :
  - l'oEmbed de YouTube, interrogé sans aucun compte, répond (titre et chaîne) ; une
    vidéo privée y serait refusée ;
  - l'ouverture de la page complète en navigation privée n'a pas pu être faite depuis
    l'environnement de fabrication : **à faire par Thomas** (une minute, sur
    téléphone).
- Rien de lourd n'est versionné : seuls ce rapport et le `.srt` sont commités.
