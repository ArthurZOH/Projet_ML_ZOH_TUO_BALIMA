# webapp/

**Responsable : Étudiant C**

Interface utilisateur multi-pages (navigation latérale via `st.navigation`) :

| Fichier | Rôle |
|---|---|
| `app.py` | Point d'entrée : navigation, réglages sidebar (mode démo, nb résultats) |
| `ui.py` | CSS global et composants partagés (hero, cartes produits) |
| `views/recherche.py` | Recherche Jumia → sélection → poubelle colorée |
| `views/dashboard.py` | Statistiques de session : éco-points, niveaux, export CSV |
| `views/guide.py` | Guide visuel des 5 poubelles + pièges classiques |
| `views/quiz.py` | Quiz du tri (10 questions, données dans `quiz_data.py`) |
| `views/apropos.py` | Présentation du projet et de l'équipe |
| `stats.py`, `quiz_data.py` | Logique pure, testée par pytest (`tests/`) |
| `mocks.py` | Produits factices (mode démo) + prédiction factice |

Framework retenu : **Streamlit** (port 8501, aligné sur la commande
`docker run -p 8501:8501` de l'énoncé). Thème : `.streamlit/config.toml`.

À faire (étapes suivantes) :
- [x] Choisir le framework (Streamlit vs Flask/FastAPI)
- [x] Squelette de l'app (recherche -> sélection -> écran coloré, avec mocks)
- [x] Habillage visuel des 5 catégories de tri (`utils/categories.py`)
- [x] Dockerfile / docker-compose (squelette)
- [x] Intégration scraper réel (Étudiant A) -> choix utilisateur
- [x] Refonte pro : navigation latérale, dashboard, quiz, guide, mode démo
- [ ] Chargement du modèle `.h5` dans l'application (Étudiant B, PR #3)

Lancement local :

```bash
streamlit run webapp/app.py
```

Lancement Docker :

```bash
docker build -t ecosort .
docker run -p 8501:8501 ecosort
```
