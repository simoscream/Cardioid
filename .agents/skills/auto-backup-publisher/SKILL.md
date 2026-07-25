---
name: auto-backup-publisher
description: Skill d'assistance pour l'exécution automatique et la vérification contrôlée des sauvegardes synchronisées (Git local + GitHub distant). À activer lorsque l'utilisateur demande "sauvegarde", "save", "sauvegarde vX.Y" ou "mets à jour la version".
---

# Auto Backup & Publisher — Skill de Sauvegarde Double & Vérification GitHub

Ce skill garantit que chaque demande de sauvegarde ("sauvegarde", "save", "publie", etc.) exécute **systématiquement et simultanément** la sauvegarde locale Git et la publication vérifiée sur GitHub.

---

## 🎯 Déclencheurs de la Compétence (Triggers)
Activer cette compétence dès que l'utilisateur prononce :
- *"fais une sauvegarde"* / *"sauvegarde vX.Y"*
- *"save"* / *"save local et github"*
- *"sauve le projet"*

---

## 📋 Procédure Automatisée en 4 Étapes

### Étape 1 : Sauvegarde Locale (Git Commit & Tag)
1. Vérifier l'état des fichiers :
   ```bash
   git status
   ```
2. Créer un commit propre avec un message explicite :
   ```bash
   git add .
   git commit -m "Cardioid vX.Y - <Description des nouveautés>"
   ```
3. Poser ou mettre à jour le tag de version correspondant :
   ```bash
   git tag -d vX.Y 2>/dev/null || true
   git tag -a vX.Y -m "Version X.Y - Release"
   ```

---

### Étape 2 : Publication Distante sur GitHub
Pousser simultanément la branche `main` et les tags vers le dépôt distant GitHub :

```bash
git push origin main --tags
```

---

### Étape 3 : Compétence de Vérification Empirique GitHub (Mandatory Verification)
**Ne jamais déclarer le succès sans avoir contrôlé que le serveur distant GitHub possède exactement la même version.**

Exécuter la vérification du hash distant :

```bash
git ls-remote --tags origin
git log origin/main -n 1 --oneline
```

**Critères d'acceptation :**
- Le commit `HEAD` local et le commit `origin/main` distant doivent partager **le même hash SHA**.
- Le tag `vX.Y` doit être présent sur le serveur distant `origin`.

---

### Étape 4 : Rapport de Confirmation Synthétique
Présenter à l'utilisateur :
- Le tag local et le tag GitHub validés (`vX.Y`).
- Le lien direct vers le commit sur GitHub (`https://github.com/simoscream/Cardioid/commits/main`).
- Le lien direct vers l'application Web déployée (`https://simoscream.github.io/Cardioid/`).
