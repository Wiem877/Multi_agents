# Image de base : Python 3.12 version légère
FROM python:3.12-slim

# Dossier de travail à l'intérieur du container
WORKDIR /app

# Copier requirements.txt dans le container
COPY requirements.txt .

# Installer toutes les bibliothèques
RUN pip install --no-cache-dir -r requirements.txt

# Créer un utilisateur non-root (sécurité)
RUN useradd -m sandboxuser
USER sandboxuser

# Dossier où le code généré sera exécuté
WORKDIR /app/sandbox