---
name: modular-art
description: Skill d'assistance pour la génération, la vérification et le test d'œuvres géométriques modulaires basées sur les tables de multiplication (Cardioid). À activer lorsque l'utilisateur demande de générer une table de multiplication géométrique, de modifier ses paramètres (table, modulo, résolution, masquage d'éléments), d'exporter en PNG/SVG, de générer une série d'images ou une vidéo MP4 (FFmpeg), de générer le rapport de test HTML, le manuel d'utilisation interactif ou de lancer les tests unitaires du projet Cardioid.
---

# Modular Art - Visualisation des Tables de Multiplication Modulaires

Ce skill définit la procédure standard pour manipuler, tester et vérifier la génération d'images géométriques, d'animations vidéo, du manuel CLI et de l'application Web interactive dans le projet Cardioid.

> **Sous-référence obligatoire** : [Conventions de nommage des artefacts](references/naming_conventions.md)  
> **Application Web Temps Réel** : [web/index.html](file:///Volumes/my_Data/CodeProgramming/Cardioid/web/index.html)  
> **Manuel interactif CLI HTML** : [docs/manual.html](file:///Volumes/my_Data/CodeProgramming/Cardioid/docs/manual.html)

---

## 1. Règle Qualité Absolue : Nommage Représentatif des Artefacts

Tout artefact créé (image, vidéo, série de frames, rapport, manuel) **DOIT** obligatoirement respecter la convention de nommage explicite des paramètres :
- **Images** : `output/images/image_table_<TABLE>_modulo_<MODULO>[_labelstep_<N>].<png|svg>`
- **Séries de frames** : `output/frames/frames_table_<START>_to_<END>_modulo_<MODULO>[_labelstep_<N>]/`
- **Vidéos** : `output/videos/video_table_<START>_to_<END>_modulo_<MODULO>[_labelstep_<N>].mp4`
- **Rapports & Applications** : `output/reports/rapport_tests.html`, `docs/manual.html` et `web/index.html`

Il est **strictement interdit** de générer un fichier nommé `test.png`, `temp.png` ou tout nom générique non représentatif.

---

## 2. Application Web Temps Réel 60 FPS (Canvas 2D)

Le projet embarque une application Web complète hébergée localement sous [web/index.html](file:///Volumes/my_Data/CodeProgramming/Cardioid/web/index.html) :
- **Animation 60 FPS** : Rendu dynamique en temps réel de la métamorphose des tables avec contrôle Play/Pause et Vitesse.
- **Contrôles interactifs** : Curseurs et sélecteurs pour table $n$, modulo $m$, couleurs (fond, cordes, points, texte), transparence, épaisseur, affichage cercle, points, numéros et titre (bas droite/gauche).
- **Exports direct en 1 clic** : Téléchargement instantané d'images **PNG (HD)** et **SVG (Vectoriel)** générées par le navigateur selon les conventions de nommage représentatives.

---

## 3. Manuel CLI & Générateur de Commandes

Un générateur graphique de commandes CLI est disponible sous [docs/manual.html](file:///Volumes/my_Data/CodeProgramming/Cardioid/docs/manual.html) avec boutons de copie en 1 clic.

---

## 4. Procédure étape par étape

### Étape 1 : Exécution préalable des tests unitaires et rapport HTML
```bash
pytest tests/
```

### Étape 2 : Modes de génération CLI

#### A. Image unique (PNG / SVG)
```bash
python3 main.py --table 2 --modulo 100 --show-labels --label-step 5
```

#### B. Série de frames PNG
```bash
python3 main.py --series --start-table 2.0 --end-table 5.0 --step 0.05 --modulo 100 --show-labels --label-step 5
```

#### C. Animation vidéo MP4 (FFmpeg)
```bash
python3 main.py --video --start-table 2.0 --end-table 5.0 --step 0.05 --modulo 100 --show-labels --label-step 5
```

---

## 5. Critères de Validation

L'opération est considérée comme réussie uniquement si :
1. La commande `pytest tests/` retourne `0` (11/11 PASSED).
2. Le fichier PNG, SVG ou MP4 est présent dans `output/` et respecte la convention de nommage représentative.
3. L'application Web `web/index.html` fonctionne de manière fluide à 60 FPS.
