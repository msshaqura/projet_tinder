# 🔥 Tinder Speed Dating Analysis

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://huggingface.co/spaces/msshaqura/tinder_projet)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## 📌 Présentation du projet

Ce projet analyse les données de **speed dating** (2002-2004) pour comprendre ce qui influence la décision d'accepter un deuxième rendez-vous.  
L'objectif est d'aider **Tinder** à identifier les facteurs clés qui maximisent les **matches**.

### 🎯 Problématique business

> **Pourquoi Tinder perd-il des matches ?**

L'application constate une baisse du nombre de matches et souhaite comprendre :
- Quels critères influencent réellement la décision ?
- Y a-t-il des différences entre les attentes déclarées et le comportement réel ?
- Comment améliorer l'expérience utilisateur ?

### 📊 Questions analysées

| # | Question | Statut |
|---|----------|--------|
| 1 | Quels sont les attributs les moins désirables selon le genre ? | ✅ |
| 2 | Les gens sous-estiment-ils l'importance de l'attractivité ? | ✅ |
| 3 | Les intérêts communs sont-ils plus importants que l'origine ethnique ? | ✅ |
| 4 | Les gens prédisent-ils correctement leur valeur perçue ? | ✅ |
| 5 | Vaut-il mieux être premier ou dernier speed date ? | ✅ |
| + | Analyses supplémentaires (confiance, domaine d'étude, sorties) | ✅ |

---

## 📊 Résultats clés

| Découverte | Impact |
|------------|--------|
| **Intérêts communs** | Attribut le moins important pour les deux genres |
| **Attractivité** | Sous-estimée de **5 points sur 10** |
| **Confiance en soi** | Facteur déterminant (+4% de matchs) |
| **Domaine d'étude** | Médecine (23%), Droit (21%), Sciences sociales (13%) |
| **Position du date** | Premier date : 23.3%, dernier : 22.2%, autres : 16.0% |

### 🎯 Recommandations pour Tinder

1. **Mettre en avant les intérêts communs** dans les profils
2. **Valoriser le domaine d'étude** (badges Médecine, Droit)
3. **Proposer des conseils** pour renforcer la confiance en soi
4. **Optimiser l'ordre de présentation** des profils
5. **Réduire l'importance des filtres ethniques**

---

## 🚀 Démo en ligne

L'application est disponible sur **Hugging Face Spaces** :

👉 [https://huggingface.co/spaces/msshaqura/tinder_projet](https://huggingface.co/spaces/msshaqura/tinder_projet)

---

## 💻 Installation locale

### Prérequis

- Python 3.9 ou supérieur
- Git

### Étapes d'installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/msshaqura/projet_tinder.git

# 2. Créer un environnement virtuel
python -m venv venv_tinder
source venv_tinder/Scripts/activate   # Sur linux : venv_tinder\bin\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer l'application
streamlit run app.py

Avec Docker

# Construire l'image
docker build -t tinder-analysis .

# Lancer le conteneur
docker run -p 8501:8501 tinder-analysis
Puis ouvrir http://localhost:8501

📁 Structure du projet
tinder-speed-dating/
├── app.py                      # Application Streamlit
├── data_processing.py          # Fonctions de traitement des données
├── requirements.txt            # Dépendances Python
├── Dockerfile                  # Configuration Docker
├── .gitignore                  # Fichiers à exclure
├── speed_dating_data.csv       # Données brutes
└── README.md                   # Documentation

🛠️ Technologies utilisées
Technologie	Utilisation
Python	Langage principal
Streamlit	Interface interactive
Pandas	Manipulation des données
Matplotlib / Seaborn	Visualisations
Scipy	Tests statistiques
Docker	Conteneurisation
Hugging Face Spaces	Déploiement

📈 Tests statistiques utilisés
Test	Utilisation
Test t de Student	Comparaison des moyennes (hommes/femmes)
Test du Chi2	Comparaison des proportions (catégories)
Seuil de significativité	p < 0.05

📝 Licence
Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.

👤 Auteur
Mohammed SHAQURA - Data Analyst

https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white
https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white

🙏 Remerciements
Données fournies par Jedha Bootcamp

Projet réalisé dans le cadre d'une analyse de données suite à une formation de DATA ANALYSIS

🔄 Mise à jour automatique
Le déploiement sur Hugging Face est automatisé via GitHub Actions.
À chaque git push, l'application est automatiquement reconstruite et redéployée.


