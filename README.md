# Cardioid — Visualisateur Géométrique & Arithmétique Modulaire

Une application moderne et complète pour l'exploration, le rendu et l'animation des figures géométriques générées par les tables de multiplication modulaires.

![Format d'exportation](https://img.shields.io/badge/Release-v1.2-pink.svg)
![Python](https://img.shields.io/badge/Python-3.12+-sky.svg)
![Web App](https://img.shields.io/badge/Web_Canvas-60_FPS-green.svg)

---

## 🌟 Fonctionnalités Principales

1. **Application Web Temps Réel (HTML5 Canvas 2D)** :
   - Rendu dynamique à 60 FPS avec progression fluide du multiplicateur (table $n$).
   - Animation personnalisable (lecture, pause, vitesse d'incrémentation).
   - Borne maximale dynamique ajustée au modulo.
   - Palette de couleurs complète (fond, cercle, cordes, points, texte) et transparence.
   - Export instantané d'images **PNG (HD)** et **SVG (Vectoriel W3C)**.
   - Enregistreur vidéo intégré avec choix du format **MP4 (H.264)** ou **WebM (VP9)**.

2. **Moteur Python CLI (High-Performance)** :
   - Rendu matriciel PNG (Pillow) et vectoriel SVG.
   - Incrustation du titre d'identification (`Table N | Modulo M`) avec choix de position (bas droite / bas gauche).
   - Générateur de séries de frames PNG avec nommage explicite et représentatif.
   - Compilateur vidéo MP4 (intégration FFmpeg).

3. **Manuel Interactif CLI** :
   - Générateur visuel de commandes CLI en temps réel avec boutons de copie en 1 clic (`docs/manual.html`).

---

## 🚀 Prise en Main Rapide

### 🌐 1. Application Web Interactive
Ouvrez simplement [web/index.html](web/index.html) dans n'importe quel navigateur Web moderne.

### 🐍 2. Moteur Python (CLI)

```bash
# Générer une image unitaire PNG
python3 main.py --table 2 --modulo 100

# Générer une figure SVG vectorielle avec numéros tous les 5 points
python3 main.py --table 3 --modulo 200 --format svg --show-labels --label-step 5

# Générer une animation vidéo MP4 complète (FFmpeg)
python3 main.py --video --start-table 2.0 --end-table 61.0 --step 0.5 --modulo 540
```

---

## 🧪 Tests Unitaires

La suite de 11 tests unitaires peut être exécutée via Pytest :

```bash
pytest -v tests/
```

---

## 📄 Licence
Projet open-source disponible pour étude, exploration et développement.
