# Dockerfile pour Tinder Speed Dating Analysis
# Utilisation de l'image officielle Python

FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tous les fichiers du projet
COPY . .

# Exposer le port Streamlit (par défaut 8501)
EXPOSE 8501

# Commande pour lancer l'application
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Lancer Streamlit
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]