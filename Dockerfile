# Utiliser une image Python officielle comme image de base
FROM python:3.9

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installer les dépendances
RUN pip install -r requirements.txt

# Copier le reste du code source dans le conteneur
COPY . .

# Exposer le port sur lequel l'application Flask s'exécutera
EXPOSE 5000

# Définir la commande pour démarrer l'application
CMD ["python", "app.py", "--host=0.0.0.0"]

