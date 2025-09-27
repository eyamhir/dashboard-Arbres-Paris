# 🌳 Dashboard Arbres Paris

Un tableau de bord interactif pour visualiser et analyser les données des arbres de Paris, développé avec Dash/Plotly et déployé avec Docker.

## 📋 Table des matières

- [Vue d'ensemble](#vue-densemble)
- [Fonctionnalités](#fonctionnalités)
- [Architecture](#architecture)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Visualisations](#visualisations)
- [Technologies utilisées](#technologies-utilisées)
- [Structure du projet](#structure-du-projet)
- [Configuration](#configuration)
- [Déploiement](#déploiement)
- [Contribution](#contribution)

## 🎯 Vue d'ensemble

Ce projet présente un dashboard interactif permettant d'explorer les données des arbres parisiens. Il offre des visualisations dynamiques, des filtres interactifs et des métriques clés pour analyser la biodiversité urbaine de Paris.

### Objectifs du projet
- **Visualisation des données** : Présenter les informations sur les arbres de manière claire et interactive
- **Analyse de la biodiversité** : Identifier les espèces, leur répartition et leur rareté
- **Interface utilisateur intuitive** : Permettre une exploration facile des données
- **Déploiement scalable** : Architecture containerisée pour un déploiement flexible

## ✨ Fonctionnalités

### 📊 Métriques principales
- **Total des arbres** : Nombre total d'arbres dans la base de données
- **Espèces uniques** : Diversité des espèces présentes
- **Taille moyenne** : Statistiques sur les dimensions des arbres
- **Espèce la plus rare** : Identification des espèces les moins communes

### 🔍 Filtres interactifs
- **Filtrage par espèce** : Sélection multiple d'espèces d'arbres
- **Filtrage par adresse** : Localisation géographique des arbres
- **Mise à jour en temps réel** : Toutes les visualisations se mettent à jour automatiquement

### 📈 Visualisations avancées
- **Graphique de dispersion** : Relation taille vs score de conservation
- **Histogramme** : Distribution des tailles d'arbres
- **Graphique circulaire** : Répartition de la rareté
- **Graphiques en barres** : Top 10 des espèces et adresses

### 💾 Fonctionnalités supplémentaires
- **Export de données** : Téléchargement des données filtrées au format CSV
- **Interface responsive** : Adaptation à tous les types d'écrans
- **Thème sombre** : Interface moderne avec Plotly Dark

## 🏗️ Architecture

### Architecture applicative
\`\`\`
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Nginx       │    │   Dashboard     │    │   Data Layer    │
│   (Reverse      │────│   (Dash/Flask)  │────│   (CSV Files)   │
│    Proxy)       │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
    Port 80                 Port 8050              File System
\`\`\`

### Composants principaux
1. **Frontend** : Interface Dash avec Bootstrap pour le styling
2. **Backend** : Serveur Flask intégré avec Gunicorn
3. **Reverse Proxy** : Nginx pour la gestion du trafic
4. **Containerisation** : Docker et Docker Compose

## 🚀 Installation

### Prérequis
- Docker et Docker Compose installés
- Git pour cloner le repository
- Au minimum 2GB de RAM disponible

### Installation rapide

1. **Cloner le repository**
\`\`\`bash
git clone https://github.com/eyamhir/dashboard-Arbres-Paris.git
cd dashboard-Arbres-Paris
\`\`\`

2. **Créer le fichier d'environnement**
\`\`\`bash
cp .env.example .env
# Éditer le fichier .env selon vos besoins
\`\`\`

3. **Créer le réseau Docker**
\`\`\`bash
docker network create paris-net
\`\`\`

4. **Lancer l'application**
\`\`\`bash
docker-compose up -d
\`\`\`

5. **Accéder au dashboard**
Ouvrir votre navigateur à l'adresse : `http://localhost`

### Installation pour le développement

1. **Créer un environnement virtuel**
\`\`\`bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
\`\`\`

2. **Installer les dépendances**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. **Lancer en mode développement**
\`\`\`bash
cd dashboard
python app.py
\`\`\`

## 🎮 Utilisation

### Interface utilisateur

1. **Page d'accueil** : Vue d'ensemble avec les métriques principales
2. **Filtres** : Panel de gauche pour sélectionner espèces et adresses
3. **Visualisations** : Graphiques interactifs mis à jour en temps réel
4. **Export** : Bouton de téléchargement pour les données filtrées

### Interactions disponibles
- **Zoom** : Clic et glisser sur les graphiques
- **Sélection** : Clic sur les légendes pour masquer/afficher des données
- **Hover** : Informations détaillées au survol
- **Filtrage** : Sélection multiple dans les dropdowns

## 📊 Visualisations

### 1. Graphique de dispersion (Taille vs Conservation)
- **Axe X** : Taille brute des arbres (`size_raw`)
- **Axe Y** : Score de conservation (`conservation_score`)
- **Couleur** : Niveau de rareté normalisé (`rarity_norm`)
- **Interaction** : Hover pour voir espèce et adresse

### 2. Histogramme des tailles
- **Distribution** : Répartition des tailles d'arbres
- **Bins** : 20 intervalles automatiques
- **Couleur** : Bleu cyan (#17BECF)

### 3. Graphique circulaire de rareté
- **Segments** : Niveaux de rareté normalisés
- **Pourcentages** : Affichage des proportions
- **Couleurs** : Palette Viridis

### 4. Top 10 des espèces
- **Données** : Espèces les plus représentées
- **Tri** : Par nombre d'occurrences décroissant
- **Format** : Graphique en barres horizontales

### 5. Top 10 des adresses
- **Données** : Adresses avec le plus d'arbres
- **Tri** : Par nombre d'arbres décroissant
- **Format** : Graphique en barres horizontales

## 🛠️ Technologies utilisées

### Backend
- **Python 3.11** : Langage principal
- **Dash** : Framework pour applications web analytiques
- **Plotly** : Bibliothèque de visualisation interactive
- **Pandas** : Manipulation et analyse de données
- **Flask** : Serveur web intégré

### Frontend
- **Dash Bootstrap Components** : Composants UI responsives
- **Plotly.js** : Graphiques interactifs côté client
- **HTML/CSS** : Structure et styling

### Infrastructure
- **Docker** : Containerisation de l'application
- **Nginx** : Reverse proxy et serveur web
- **Gunicorn** : Serveur WSGI pour Python

### Données et traitement
- **GeoPandas** : Données géospatiales
- **Scikit-learn** : Algorithmes de machine learning
- **PostgreSQL** : Base de données (optionnel)

## 📁 Structure du projet

\`\`\`
dashboard-Arbres-Paris/
├── 📁 dashboard/           # Code principal de l'application
│   ├── app.py             # Application Dash principale
│   └── ...                # Autres modules dashboard
├── 📁 data/               # Fichiers de données
│   ├── arbres_enriched.csv # Données principales des arbres
│   └── ...                # Autres fichiers de données
├── 📁 scripts/            # Scripts de traitement des données
│   ├── data_processing.py # Traitement et enrichissement
│   └── ...                # Autres scripts utilitaires
├── 📁 secrets/            # Fichiers de configuration sensibles
├── 📁 .idea/              # Configuration IDE
├── 📄 requirements.txt    # Dépendances Python
├── 📄 Dockerfile          # Configuration Docker
├── 📄 docker-compose.yml  # Orchestration des services
├── 📄 nginx.conf          # Configuration Nginx
├── 📄 .gitignore          # Fichiers ignorés par Git
└── 📄 .env.example        # Template de variables d'environnement
\`\`\`

## ⚙️ Configuration

### Variables d'environnement

Créer un fichier `.env` avec les variables suivantes :

\`\`\`env
# Fichier de données principal
DATA_FILE=/app/data/arbres_enriched.csv

# Configuration base de données (optionnel)
DATABASE_URL=postgresql://user:password@localhost:5432/paris_trees

# Mode debug
DEBUG=False

# Configuration serveur
WORKERS=2
THREADS=2
TIMEOUT=120
\`\`\`

### Configuration Nginx

Le fichier `nginx.conf` configure le reverse proxy :
- Port d'écoute : 80
- Proxy vers le dashboard : port 8050
- Gestion des fichiers statiques
- Headers de sécurité

### Configuration Docker

**Dockerfile** :
- Image de base : Python 3.11 slim
- Installation des dépendances système
- Configuration utilisateur non-root
- Exposition du port 8050

**docker-compose.yml** :
- Service dashboard avec build local
- Service nginx avec image officielle
- Réseau partagé `paris-net`
- Volumes pour les données et configuration

## 🚀 Déploiement

### Déploiement local avec Docker

\`\`\`bash
# Construction et lancement
docker-compose up --build -d

# Vérification des logs
docker-compose logs -f

# Arrêt des services
docker-compose down
\`\`\`

### Déploiement en production

1. **Serveur cloud** (AWS, GCP, Azure)
\`\`\`bash
# Sur le serveur
git clone https://github.com/eyamhir/dashboard-Arbres-Paris.git
cd dashboard-Arbres-Paris
docker network create paris-net
docker-compose up -d
\`\`\`

2. **Configuration du domaine**
- Pointer le domaine vers l'IP du serveur
- Configurer HTTPS avec Let's Encrypt
- Ajuster nginx.conf pour SSL

3. **Monitoring et logs**
\`\`\`bash
# Surveillance des conteneurs
docker stats

# Logs en temps réel
docker-compose logs -f dashboard
\`\`\`

### Déploiement avec CI/CD

Exemple de workflow GitHub Actions :

\`\`\`yaml
name: Deploy Dashboard
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to server
        run: |
          ssh user@server 'cd dashboard-Arbres-Paris && git pull && docker-compose up -d --build'
\`\`\`

## 🤝 Contribution

### Comment contribuer

1. **Fork** le repository
2. **Créer** une branche pour votre fonctionnalité
\`\`\`bash
git checkout -b feature/nouvelle-fonctionnalite
\`\`\`
3. **Commiter** vos changements
\`\`\`bash
git commit -m "Ajout de nouvelle fonctionnalité"
\`\`\`
4. **Pousser** vers la branche
\`\`\`bash
git push origin feature/nouvelle-fonctionnalite
\`\`\`
5. **Créer** une Pull Request

### Standards de code

- **PEP 8** : Respect des conventions Python
- **Docstrings** : Documentation des fonctions
- **Tests** : Ajout de tests pour les nouvelles fonctionnalités
- **Commits** : Messages clairs et descriptifs

### Roadmap

- [ ] Ajout de cartes interactives avec Folium
- [ ] API REST pour accès aux données
- [ ] Authentification utilisateur
- [ ] Tableau de bord administrateur
- [ ] Export en différents formats (PDF, Excel)
- [ ] Intégration de données météorologiques
- [ ] Prédictions avec machine learning

## 📞 Support

- **Issues** : [GitHub Issues](https://github.com/eyamhir/dashboard-Arbres-Paris/issues)
- **Discussions** : [GitHub Discussions](https://github.com/eyamhir/dashboard-Arbres-Paris/discussions)
- **Email** : eyamhir@example.com

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

**Développé avec ❤️ pour la ville de Paris et ses arbres** 🌳
