# Conventions Strictes de Nommage des Fichiers et Artefacts

Ce sous-guide définit la politique de nommage obligatoire pour **tous les artefacts** générés dans le projet Cardioid.

## Règle d'or : Représentativité et Reproductibilité
Aucun fichier généré (image, vidéo, série de frames, rapport) ne doit porter un nom générique ou ambigu (ex: `test.png`, `image1.png`, `temp.svg`). Chaque nom de fichier **DOIT** inclure les paramètres clés de sa création.

---

## 1. Images Unitaires (PNG / SVG)
- **Modèle de nommage** : `output/images/image_table_<TABLE>_modulo_<MODULO>[_labelstep_<N>][_nocircle][_nopoints].<ext>`
- **Exemples autorisés** :
  - `output/images/image_table_2_modulo_100.png`
  - `output/images/image_table_3_modulo_200.svg`
  - `output/images/image_table_2_modulo_100_labelstep_5.png`
  - `output/images/image_table_110_modulo_540_nocircle.png`

---

## 2. Dossiers de Séries / Frames
- **Modèle de nommage** : `output/frames/frames_table_<START>_to_<END>_modulo_<MODULO>[_labelstep_<N>]/`
- **Exemples autorisés** :
  - `output/frames/frames_table_2_to_10_modulo_200/frame_0001.png`
  - `output/frames/frames_table_2_to_5_modulo_100_labelstep_5/frame_0001.png`

---

## 3. Vidéos MP4
- **Modèle de nommage** : `output/videos/video_table_<START>_to_<END>_modulo_<MODULO>[_labelstep_<N>].mp4`
- **Exemples autorisés** :
  - `output/videos/video_table_2_to_10_modulo_200.mp4`
  - `output/videos/video_table_2_to_5_modulo_100_labelstep_5.mp4`

---

## 4. Rapports de Tests & Artefacts Documentation
- **Modèle de nommage** : `output/reports/rapport_tests.html`
- **Exemple autorisé** :
  - `output/reports/rapport_tests.html`
