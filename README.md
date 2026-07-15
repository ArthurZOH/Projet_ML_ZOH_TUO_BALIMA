# EcoSort-Search

Application web qui aide au tri sélectif. L'utilisateur saisit le nom d'un produit,
l'application recherche ce produit sur Jumia, puis un modèle de Deep Learning détermine
la matière de l'emballage et affiche la bonne consigne de tri (jaune, verte, bleue,
électronique, marron/noire).

## Fonctionnement

Le parcours est le suivant : mot clé saisi par l'utilisateur, recherche des produits
correspondants sur Jumia, sélection d'un produit, prédiction de la matière par le modèle,
puis affichage de la poubelle adaptée. Une cascade de décision combine l'image du produit,
des mots clés par poubelle et un dernier recours vers la poubelle marron.

## Équipe et contributions

Le projet est réparti en trois piliers, un par membre. Chacun est responsable d'un
sous-système complet du dépôt.

### TUO Nompan Fatima Alice, scraping et données Jumia

Conception du module de recherche Jumia (`scraping/scraper.py`) : envoi des requêtes,
extraction du nom, du prix, de l'image et du lien, et gestion des cas d'erreur (absence de
résultat, page indisponible, délai dépassé). Écriture des tests unitaires du scraper
(`scraping/test_scraper.py`) et gestion des dépendances associées.

### Arthur ZOH, Deep Learning

Préparation et exploration du jeu de données (`training/prepare_data.py`,
`training/explore_dataset.py`), entraînement du modèle de classification d'images
MobileNetV2 (`training/train.py`) atteignant 86 pour cent d'exactitude, évaluation avec
matrice de confusion (`training/evaluate.py`), module d'inférence (`training/predict.py`)
et correspondance des classes du modèle vers les catégories de tri
(`utils/tri_categories.py`). Mise en place initiale de l'architecture du dépôt et
versionnement du modèle entraîné.

### Yannel BALIMA, interface, intégration et Docker

Application web Streamlit (`webapp/`) : page de garde avec connexion et inscription,
authentification par jeton signé, vues Recherche, Statistiques et Guide du tri. Intégration
du modèle dans l'interface (`webapp/inference.py`) reliant le scraping, la prédiction et la
consigne de tri, avec repli sur des données simulées si le modèle est absent.
Conteneurisation Docker et pipeline d'intégration continue (tests et build validés sur
GitHub Actions).

## Architecture du dépôt

```
ecosort-search/
  data/          jeu de données (non versionné, voir .gitignore)
  models/        modèle entraîné .h5
  scraping/      module de scraping Jumia
  training/      entraînement, évaluation et inférence du modèle
  webapp/        interface utilisateur Streamlit
  utils/         code partagé (constantes, mapping des catégories)
  tests/         tests unitaires
  .github/       workflow d'intégration continue et template de Pull Request
```

## Installation

```
python -m venv .venv
source .venv/bin/activate      # Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

## Lancement en local

```
streamlit run webapp/app.py
```

L'application est alors accessible sur http://localhost:8501.

## Lancement avec Docker

```
docker build -t ecosort .
docker run -p 8501:8501 ecosort
```

## Tests et intégration continue

```
pytest -v
```

À chaque push et pull request, GitHub Actions exécute deux vérifications : les tests
unitaires et le build de l'image Docker suivi d'un test de démarrage de l'application. Le
build Docker est validé sur les serveurs GitHub, sans nécessiter Docker sur les machines des
membres.

## Comptes de démonstration

Identifiants : alice, arthur ou yannel. Mot de passe : ecosort2026.

## Licence

Projet académique, usage pédagogique uniquement.
