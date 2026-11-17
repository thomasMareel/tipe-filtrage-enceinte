# Consignes pour la session « vidéo d'entraînement »

> Ces consignes s'adressent à une session de Claude Code ouverte dans un autre
> environnement, qui a accès à **Mistral** (voix de synthèse « Camille ») et à
> **YouTube**. Cette session ne connaît que le dépôt : tout ce qu'il faut est ici et dans
> `oral/`. En cas de doute, ne pas deviner : écrire la question dans le rapport final.

## 1. Le but

Thomas présente son projet de TIPE devant ses professeurs le **mercredi 18 novembre 2026**,
pendant environ **8 minutes**. Il veut une vidéo d'entraînement : les diapositives défilent
pendant qu'une voix de synthèse dit **exactement** son texte, au rythme prévu. Il veut
voir :
- le rythme général ;
- le moment où l'on passe d'une diapositive à la suivante ;
- les passages où l'on prend le temps d'insister.

## 2. Les fichiers d'entrée (tous dans `oral/`)

| Fichier | Rôle |
|---|---|
| `presentation.pdf` | Les diapositives à filmer : **version claire**, celle qui sera projetée. 15 pages, format 4:3 (768 × 576 pt). |
| `presentation-sombre.pdf` | La même présentation en version sombre. Ne pas l'utiliser pour la vidéo. |
| `script_oral.json` | **La source du texte.** Une entrée par page. Seules les entrées `"narree": true` (pages 1 à 12) se disent. |
| `script_oral.md` | Le même texte, lisible par un humain, avec ce qu'il faut montrer sur chaque vue. |
| `CONTEXTE.md` | Le projet, les termes techniques et **leur prononciation**. |

## 3. Ce que la session ne doit pas faire

- **Ne pas modifier le texte du script.** Si une phrase pose problème (prononciation,
  durée), le signaler dans le rapport et proposer une correction ; Thomas décide.
- **Ne pas modifier les diapositives** (`presentation-projet.html`, les PDF).
- **Ne pas synthétiser** les pages 13 à 15 (annexes) : elles ne se présentent pas.
- **Ne pas synthétiser deux fois la transition** : elle est déjà la dernière phrase du
  champ `texte`. Le champ `transition_vers_suivante` est seulement informatif.
- **Ne pas publier la vidéo en public** : non répertoriée uniquement.
- **Ne pas commiter de fichiers lourds.** Les fichiers vidéo, audio et image sont exclus
  par le `.gitignore` de `oral/video/`. Le dépôt est public.

## 4. Les étapes

1. **Vérifier les entrées.**
   - Le PDF compte 15 pages et `script_oral.json` 15 entrées, dont 12 narrées.
   - Les pages sont en 4:3.
   - Si ce n'est pas le cas, s'arrêter et le signaler.
2. **Images : une par vue narrée** (aucune vue n'a d'apparitions successives).
   - Rendre les pages 1 à 12 de `presentation.pdf` en PNG de **1440 × 1080** pixels
     (4:3), par exemple avec `pdftoppm -png -scale-to-x 1440 -scale-to-y 1080`.
   - Dossier : `oral/video/images/vue-01.png` … `vue-12.png`.
3. **Audio : un fichier par vue.**
   - Voix « Camille » de Mistral, débit naturel, sans effet.
   - Texte synthétisé : le champ `texte` de la vue, après application des
     `substitutions_tts` du JSON. Ces substitutions servent **seulement à l'audio**.
   - Dossier : `oral/video/audio/vue-01.wav` … `vue-12.wav` (ou `.mp3`).
4. **Prononciation : vérifier avant de monter.**
   - Écouter, ou mieux transcrire si un outil de reconnaissance vocale est disponible,
     chaque fichier audio.
   - Le comparer au texte, en particulier pour les mots de la table de `CONTEXTE.md`,
     section 5 : TIPE, REW, GBF, IA, MCOT, bass-reflex, selfs, « L sur r », évents.
   - En cas de mauvaise prononciation, ajouter une réécriture phonétique pour l'audio
     seulement, et la noter dans le rapport.
5. **Durée : 7 min 30 à 8 min 30 au total.**
   - Total = somme des audios + une respiration d'**une seconde** après chaque vue.
   - Comparer chaque vue à `duree_visee_s` ; le total visé est 8 min 15.
   - Hors fourchette : ajuster la vitesse de la voix **globalement**, dans la limite de
     ±10 %. Ne jamais changer le texte, ni la vitesse d'une seule vue.
   - Si l'écart persiste, le dire dans le rapport.
6. **Montage.**
   - Chaque image reste affichée pendant son audio, plus une seconde de silence ; trois
     secondes sur la dernière vue.
   - Format : vidéo 1440 × 1080, 25 ou 30 images/s, H.264 et audio AAC 48 kHz.
   - Fichier : `oral/video/presentation_oral.mp4`.
7. **Incrustations discrètes**, dans les **coins du haut** : le bas des diapositives porte
   déjà un numéro de page du PDF.
   - En haut à gauche : le numéro de la vue, sous la forme « vue 5 / 12 ».
   - En haut à droite : un **chrono qui défile depuis le début**, « mm:ss » (00:00 au
     début, sans retour à zéro entre les vues).
   - Petite police (environ 2,5 % de la hauteur), sur un fond sombre semi-transparent.
   - Ne rien masquer du contenu.
8. **Sous-titres** : `oral/video/presentation_oral.srt`, en français.
   - Fabriqués à partir du `texte` **original**, sans les substitutions phonétiques.
   - Un sous-titre par phrase ou par membre de phrase : au plus 2 lignes de 42 caractères.
   - Calage : sur les horodatages de la synthèse vocale s'ils existent ; sinon, durée de
     chaque vue répartie entre ses sous-titres au prorata du nombre de caractères.
   - Vérifier que les sous-titres d'une vue ne débordent pas sur la suivante.
9. **Rapport de rythme** : `oral/video/RAPPORT.md`. C'est ce que Thomas regardera en
   premier.
   - Un tableau avec, pour chaque vue : son titre, son début dans la vidéo (mm:ss), sa
     durée mesurée, sa durée visée et l'écart.
   - La durée totale.
   - Les vues nettement plus longues ou plus courtes que prévu (écart de plus de 15 %).
   - Les corrections de prononciation appliquées.
   - Le lien YouTube.
10. **Mise en ligne sur YouTube.**
    - Visibilité : **non répertoriée** (`unlisted`). Contenu non destiné aux enfants.
    - Titre : « TIPE — répétition de la présentation du projet (18/11/2026), voix de
      synthèse ».
    - Description :
      - une phrase qui dit que la voix est une synthèse vocale et que rien n'est encore
        mesuré ;
      - puis les **chapitres** : une ligne par vue, « mm:ss Titre de la vue », la première
        à 00:00. YouTube exige au moins 10 s par chapitre : fusionner la vue 12
        (« Questions ? ») avec la vue 11.
    - Ajouter le fichier `.srt` comme sous-titres en français.
11. **Commiter et pousser sur `main`** seulement `oral/video/RAPPORT.md` et
    `oral/video/presentation_oral.srt`, avec un message en français. Donner ensuite à
    Thomas le lien YouTube et le tableau du rapport.

## 5. Contrôles avant de dire « c'est fini »

- [ ] 12 vues dans l'ordre, chacune avec son audio, et aucune annexe dans la vidéo.
- [ ] Durée totale entre 7 min 30 et 8 min 30.
- [ ] Chrono : départ à 00:00, croissant, et égal au temps réel de la vidéo à la fin.
- [ ] Numéro de vue juste à chaque changement de diapositive.
- [ ] Sous-titres calés, sans fautes, sans les réécritures phonétiques.
- [ ] Prononciation vérifiée sur les termes de `CONTEXTE.md`, section 5.
- [ ] Vidéo **non répertoriée**, lien testé dans une fenêtre de navigation privée.
- [ ] Aucun fichier `.mp4`, `.wav`, `.mp3` ou `.png` commité.
