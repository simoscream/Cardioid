---
name: github-publisher
description: Skill d'assistance pour la publication automatique, la gestion des dépôts GitHub et le déploiement sur GitHub Pages. À utiliser lorsque l'utilisateur souhaite créer un dépôt GitHub public/privé, pousser le code source propre et publier l'application Web en ligne via GitHub Pages.
---

# GitHub Publisher — Skill de Publication & Déploiement GitHub

Ce skill définit la procédure automatisée pour publier un projet local sur GitHub et déployer l'application Web sur **GitHub Pages**.

---

## 🛠️ Réponses aux questions techniques

### 1. A-t-on besoin d'un MCP (Model Context Protocol) ?
**Non, absolument pas !**  
Le Model Context Protocol (MCP) n'est pas nécessaire. L'API REST officielle de GitHub (`https://api.github.com`) combinée à `git` et `curl` permet d'exécuter l'intégralité des opérations directement depuis le terminal.

### 2. Comment fonctionne l'authentification GitHub ?
Pour que le skill puisse créer le dépôt à votre place sur GitHub, il suffit d'un **Personal Access Token (PAT)** ou d'une clé SSH GitHub.

---

## 📋 Procédure de Publication Automatisée en 4 Étapes

### Étape 1 : Vérification de la propreté du dépôt Git
S'assurer que le projet est sur une branche propre avec un commit unique (ex: `Cardioid v1.2`).

```bash
git status
git log --oneline
```

### Étape 2 : Création du dépôt distant via l'API REST GitHub
Créer le dépôt public `Cardioid` sur le compte GitHub via `curl` :

```bash
curl -H "Authorization: token $GITHUB_TOKEN" \
     -d '{"name":"Cardioid","public":true,"description":"Cardioid — Visualisateur Géométrique & Arithmétique Modulaire 60 FPS"}' \
     https://api.github.com/user/repos
```

### Étape 3 : Publication des Commits & Tags
Lier le dépôt distant et pousser le code :

```bash
git remote add origin https://github.com/<pseudo>/Cardioid.git
git push -u origin main --tags
```

### Étape 4 : Activation automatique de GitHub Pages
Activer le déploiement du site Web sur la branche `main` / dossier `root` ou `web` via l'API :

```bash
curl -H "Authorization: token $GITHUB_TOKEN" \
     -H "Accept: application/vnd.github.v3+json" \
     -d '{"source":{"branch":"main","path":"/"}}' \
     https://api.github.com/repos/<pseudo>/Cardioid/pages
```

L'application Web sera immédiatement accessible en ligne sous :  
`https://<pseudo>.github.io/Cardioid/web/index.html`
