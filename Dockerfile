# EcoSort-Search — image de production
# Build : docker build -t ecosort .
# Run   : docker run -p 8501:8501 ecosort
FROM python:3.11-slim

WORKDIR /app

# Dépendances d'abord (cache Docker : ne se réinstalle que si requirements change)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code du projet (data/ et .venv exclus via .dockerignore)
COPY . .

EXPOSE 8501

# server.address=0.0.0.0 obligatoire pour être joignable depuis l'hôte
CMD ["streamlit", "run", "webapp/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
