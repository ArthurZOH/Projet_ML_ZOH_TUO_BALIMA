# webapp/

**Responsable : Étudiant C**

Interface utilisateur avec page de garde (connexion) puis navigation
horizontale (barre de boutons coulissants, `st.segmented_control`) :

| Fichier | Rôle |
|---|---|
| `app.py` | Point d'entrée : login obligatoire, navbar, thème clair/sombre, sidebar |
| `ui.py` | Design system (variables CSS par thème, hero, cartes, navbar) |
| `auth.py` | Vérification des identifiants (comptes de démo, testé par pytest) |
| `views/login.py` | Page de garde : formulaire de connexion |
| `views/recherche.py` | Recherche Jumia → sélection → poubelle colorée |
| `views/dashboard.py` | Statistiques de session : éco-points, niveaux, graphique par poubelle |
| `views/guide.py` | Guide visuel des 5 poubelles + pièges classiques |
| `stats.py` | Logique pure éco-points/niveaux, testée par pytest (`tests/`) |
| `inference.py` | Chargement du modèle `.h5` et prédiction de la matière (repli sur `mocks.py` si le modèle est absent) |
| `mocks.py` | Prédiction factice, utilisée en repli quand le modèle n'est pas disponible |

Framework retenu : **Streamlit** (port 8501, aligné sur la commande
`docker run -p 8501:8501` de l'énoncé). Thème : `.streamlit/config.toml`
(sombre par défaut) + bascule 🌙/☀️ dans la navbar.

Comptes de démo : `alice`, `arthur`, `yannel` — mot de passe `ecosort2026`.

À faire (étapes suivantes) :
- [x] Choisir le framework (Streamlit vs Flask/FastAPI)
- [x] Squelette de l'app (recherche -> sélection -> écran coloré, avec mocks)
- [x] Habillage visuel des 5 catégories de tri (`utils/categories.py`)
- [x] Dockerfile / docker-compose (squelette)
- [x] Intégration scraper réel (Étudiant A) -> choix utilisateur
- [x] Design system (thèmes clair/sombre), navbar horizontale, page de connexion
- [x] Chargement du modèle `.h5` dans l'application (`inference.py`, repli mocks si absent)

Lancement local :

```bash
streamlit run webapp/app.py
```

Lancement Docker :

```bash
docker build -t ecosort .
docker run -p 8501:8501 ecosort
```
