# 🌸 Cardioid — Real-Time Geometric Visualizer & CLI Engine

> **A modern, dual-engine software suite for high-performance visualization, vector rendering, frame sequence generation, and video export of modular multiplication tables geometry.**

[![Python 3.12](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen.svg)](https://simoscream.github.io/Cardioid/)
[![Version](https://img.shields.io/badge/Release-v2.1-pink.svg)](https://github.com/simoscream/Cardioid/tags)

---

## 🌐 Live Web Application & Documentation

- **60 FPS Interactive Visualizer**: [https://simoscream.github.io/Cardioid/](https://simoscream.github.io/Cardioid/)
- **🎓 Educational Principles Guide**: [https://simoscream.github.io/Cardioid/docs/educational.html](https://simoscream.github.io/Cardioid/docs/educational.html)
- **🏛️ Software Architecture Specification**: [https://simoscream.github.io/Cardioid/docs/architecture.html](https://simoscream.github.io/Cardioid/docs/architecture.html)
- **📖 Interactive CLI Manual**: [https://simoscream.github.io/Cardioid/docs/manual.html](https://simoscream.github.io/Cardioid/docs/manual.html)
- **🧪 Pytest Test Suite Report**: [https://simoscream.github.io/Cardioid/output/reports/rapport_tests.html](https://simoscream.github.io/Cardioid/output/reports/rapport_tests.html)

---

## ✨ Key Features

- **Dual Rendering Engine**: Zero-dependency Browser Canvas 2D (60 FPS) + High-resolution Python Pillow/SVG CLI rendering.
- **Continuous Decimal Morphing**: Smooth sub-integer table factor progression (e.g. $n = 61.00$).
- **Multi-Format Export**: 1-click PNG image, W3C vector SVG XML, frame PNG series, and H.264 MP4 / WebM video exports.
- **Interactive Educational Calculator**: Real-time modular arithmetic breakdown $(n \times i) \bmod m$.
- **Global 7-Language i18n & `localStorage` Persistence**: Complete translation in EN (default), FR, ES, DE, AR (with RTL support), JP, and CN.

---

## 📜 Version Release History

| Version | Release Date | Key Features & Major Enhancements |
| :--- | :--- | :--- |
| **`v1.0`** | 2026-07-24 | Initial modular arithmetic rendering engine (Pillow PNG, SVG, CLI parser). |
| **`v1.1`** | 2026-07-24 | Bound multiplier max slider dynamically to modulo (`table.max = modulo`). Added Pytest suite. |
| **`v1.2`** | 2026-07-24 | Cleaned code of external references. Refactored architecture into `src/` modules. |
| **`v1.3`** | 2026-07-25 | GitHub Pages publishing, `.nojekyll` configuration, and root redirect setup. |
| **`v2.0`** | 2026-07-25 | Official Release: 7-language i18n, Educational Guide, Software Architecture Specification, and PlantUML diagrams. |
| **`v2.1`** | 2026-07-25 | Interactive Modulo Calculator, embedded figure images, `localStorage` language persistence across all pages, and repository privacy hygiene (`.gitignore`). |

---

## 💻 CLI Quickstart

```bash
# Render single PNG cardioid (Table 2, Modulo 200)
python3 main.py -t 2.0 -m 200 -o output/images/cardioid_t2.png

# Render vector SVG nephroid (Table 3, Modulo 200)
python3 main.py -t 3.0 -m 200 --format svg -o output/images/nephroid_t3.svg

# Generate frame series (Table 2 to 10)
python3 main.py --series --start-table 2.0 --end-table 10.0 --step 0.1 -m 200

# Compile H.264 MP4 video via FFmpeg
python3 main.py --video --start-table 2.0 --end-table 10.0 --step 0.1 -m 200
```

---

## 🧪 Testing

```bash
# Run unit & integration tests
pytest
```

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for details.
