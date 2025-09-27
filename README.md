# 🌳 Dashboard Arbres Paris

Un tableau de bord interactif moderne pour visualiser et analyser les données des arbres de Paris, développé avec Python, Dash et Plotly.

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Dash](https://img.shields.io/badge/Dash-Latest-green.svg)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table des matières

- [Aperçu](#aperçu)
- [Fonctionnalités](#fonctionnalités)
- [Technologies utilisées](#technologies-utilisées)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Structure du projet](#structure-du-projet)
- [Déploiement](#déploiement)
- [Visualisations](#visualisations)
- [Contribution](#contribution)

## 🎯 Aperçu

Ce projet présente un dashboard interactif permettant d'explorer et d'analyser les données des arbres parisiens. Il offre des visualisations géospatiales, des analyses statistiques et des insights sur la biodiversité urbaine de Paris.

### Objectifs du projet
- 📊 Visualiser la distribution géographique des arbres parisiens
- 🌿 Analyser la diversité des espèces d'arbres
- 📈 Présenter des statistiques détaillées par arrondissement
- 🗺️ Offrir une interface interactive et intuitive

## ✨ Fonctionnalités

### 🗺️ Cartographie interactive
- Visualisation géospatiale des arbres sur une carte de Paris
- Filtrage par arrondissement, espèce et caractéristiques
- Clustering intelligent pour les grandes densités d'arbres

### 📊 Analyses statistiques
- Distribution des espèces d'arbres par arrondissement
- Analyse de la biodiversité urbaine
- Métriques de santé et de développement des arbres

### 🎨 Interface utilisateur
- Design moderne et responsive
- Navigation intuitive avec Bootstrap
- Graphiques interactifs avec Plotly

### 🔍 Fonctionnalités avancées
- Recherche et filtrage en temps réel
- Export des données et visualisations
- Analyses prédictives avec scikit-learn

## 🛠️ Technologies utilisées

### Backend & Data Processing
- **Python 3.11** - Langage principal
- **Pandas** - Manipulation et analyse des données
- **GeoPandas** - Traitement des données géospatiales
- **SQLAlchemy** - ORM pour la base de données
- **PostgreSQL** - Base de données principale

### Frontend & Visualisation
- **Dash** - Framework web interactif
- **Plotly** - Graphiques interactifs
- **Dash Bootstrap Components** - Interface utilisateur moderne
- **Folium** - Cartes interactives
- **Matplotlib** - Graphiques statiques

### Infrastructure & Déploiement
- **Docker** - Conteneurisation
- **Docker Compose** - Orchestration des services
- **Nginx** - Serveur web et proxy inverse
- **Gunicorn** - Serveur WSGI Python

### Outils de développement
- **Shapely** - Manipulation de géométries
- **PyProj** - Projections cartographiques
- **Scikit-learn** - Machine learning et analyses prédictives

## 🚀 Installation

### Prérequis
- Docker et Docker Compose
- Python 3.11+ (pour le développement local)
- Git

### Installation avec Docker


1. **Configurer les variables d'environnement**
\`\`\`bash
cp  .env
# Éditer le fichier .env avec vos configurations
\`\`

2. **Créer le réseau Docker**
\`\`\`bash
docker network create paris-net
\`\`\`

3. **Lancer l'application**
\`\`\`bash
docker-compose up -d
\`\`\`

4. **Accéder au dashboard**
- Application : http://localhost
- Dashboard direct : http://localhost:8050

### Installation locale

1. **Créer un environnement virtuel**
\`\`\`bash
python -m venv venv
\`\`\`
\`\`\`bash
venv\Scripts\activate 
\`\`\`

2. **Installer les dépendances**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. **Configurer les variables d'environnement**
\`\`\`bash
export DATA_FILE="data/arbres_paris.csv"
export DATABASE_URL="postgresql://user:password@localhost/paris_trees"
export DEBUG="True"
\`\`\`

4. **Lancer l'application**
\`\`\`bash
python dashboard/app.py
\`\`\`

## 📁 Structure du projet


📁dashboard-Arbres-Paris/

├── 📁 dashboard/           
│   ├── app.py                    
├── 📁 data/               
│   ├── ..         
├── 📁 scripts/            
│   ├── ..      
├── 📁 secrets/          
├── 📁 .idea/             
├── 🐳 Dockerfile       
├── 🐳 docker-compose.yml   
├── 🌐 nginx.conf       
├── 📋 requirements.txt   
└── 📝 README.md          


## 🎨 Visualisations

Le dashboard propose plusieurs types de visualisations:

### 🗺️ Cartes géospatiales
- Carte de densité des arbres par arrondissement
- Visualisation des espèces par zones géographiques
- Heatmap de la biodiversité urbaine

### 📊 Graphiques statistiques
- Histogrammes de distribution des espèces
- Graphiques en secteurs par arrondissement
- Analyses temporelles de plantation

### 📈 Tableaux de bord
- KPI de biodiversité urbaine
- Métriques de santé des arbres
- Comparaisons inter-arrondissements

## 🚀 Déploiement

### Déploiement avec Docker

Le projet est entièrement dockerisé pour un déploiement facile :

\`\`\`
docker-compose -f docker-compose.prod.yml up -d
docker-compose up -d
\`\`\`

### Déploiement avec ngrok

- Invoke-WebRequest -Uri "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip" -OutFile "ngrok_v3.zip"
- Expand-Archive .\ngrok_v3.zip -DestinationPath .\ngrok_v3
- $env:Path += ";$PWD\ngrok_v3"
- ngrok authtoken <TON_AUTHTOKEN_ICI>
- ngrok http 8050
-Forwarding  https://random-name-12345.ngrok.io -> http://localhost:8050


### Variables d'environnement

\`\`\`env\`\`\`
# Configuration de l'application
DATA_FILE=data/arbres_paris.csv
DATABASE_URL=postgresql+psycopg2://eya:eyaeya@db:5432/paris_data
DEBUG=True

# Configuration serveur
WORKERS=2
TIMEOUT=120
BIND=0.0.0.0:8050


## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment contribuer :

1. **Fork** le projet
2. **Créer** une branche pour votre fonctionnalité (`git checkout -b  `)
3. **Commit** vos changements (`git commit -m 'exemple commit'`)
4. **Push** vers la branche (`git push origin main`)
5. **Ouvrir** une Pull Request

### Standards de code
- Suivre PEP 8 pour Python
- Documenter les nouvelles fonctionnalités
- Ajouter des tests pour les nouvelles fonctionnalités
- Maintenir la compatibilité avec Python 3.11+

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👨‍💻 Auteur

**Eyamhir** - [GitHub](https://github.com/eyamhir)

