---
name: sw-expert
description: Skill d’expertise en génie logiciel pour l’analyse de problèmes, la détection de la cause racine (root cause), l’identification de la solution dans le code, la présentation comparative (code AVANT / code APRÈS) et l’application contrôlée des modifications. À activer pour diagnostiquer et résoudre des bugs complexes reported par l'utilisateur.
---

# SW Expert — Expertise en Diagnostic et Génie Logiciel

Ce skill définit la méthodologie rigoureuse d'analyse et de correction de bugs.

## 1. Procédure de Diagnostic & Correction

Pour tout problème technique ou bug signalé par l'utilisateur :

1. **Analyse du Problème** : Analyser les symptômes décrits et le contexte d'exécution.
2. **Détection de la Cause Racine (Root Cause)** : Inspecter le code source de manière empirique pour identifier le dysfonctionnement exact (ex: propagation d'événements DOM, effet de bord, typage, concurrence).
3. **Identification de la Solution** : Concevoir le correctif minimal et robuste sans régression.
4. **Présentation Comparative (Avant / Après)** : Présenter obligatoirement à l'utilisateur :
   - Le **Code AVANT** (avec l'endroit exact du bug)
   - Le **Code APRÈS** (avec la correction apportée)
   - L'explication technique détaillée de la cause racine et de la résolution.
5. **Application & Validation** : Appliquer les modifications et valider le comportement par les tests.
