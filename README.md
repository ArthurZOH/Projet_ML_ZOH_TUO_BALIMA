# ♻️ EcoSort-Search

Application web qui aide au tri sélectif : l'utilisateur saisit le nom d'un produit,
l'application recherche ce produit sur Jumia, puis un modèle de Deep Learning
détermine la matière de l'emballage et affiche la bonne consigne de tri
(jaune, verte, bleue, électronique, marron/noire).

## Équipe

| Étudiant | Responsabilité principale |
|---|---|
| Étudiant A | Scraping & données Jumia |
| Étudiant B | Deep Learning (classification) |
| Étudiant C | Interface & Docker |

## Architecture du dépôt

```
ecosort-search/
├── data/          # dataset Kaggle (non versionné, voir .gitignore)
├── models/        # modèle entraîné .h5 (non versionné)
├── scraper/       # module de scraping Jumia (Étudiant A)
├── training/      # entraînement / évaluation du modèle (Étudiant B)
├── webapp/        # interface utilisateur (Étudiant C)
├── utils/         # code partagé (constantes, mapping des catégories)
├── tests/         # tests unitaires
└── .github/       # template de Pull Request
```

## Statut du projet

🚧 En cours — Étape 1 : mise en place du dépôt et de l'architecture.

## Installation (à compléter à l'étape "choix techniques")

```bash
python -m venv .venv
source .venv/bin/activate      # Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

## Licence

Projet académique — usage pédagogique uniquement.
