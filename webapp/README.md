# webapp/

**Responsable : Étudiant C**

Interface utilisateur : saisie du produit, affichage des résultats du scraper,
sélection d'un produit, appel du modèle, affichage de la couleur de tri.

Framework retenu : **Streamlit** (port 8501, aligné sur la commande
`docker run -p 8501:8501` de l'énoncé).

À faire (étapes suivantes) :
- [x] Choisir le framework (Streamlit vs Flask/FastAPI)
- [x] Squelette de l'app (recherche -> sélection -> écran coloré, avec mocks)
- [x] Habillage visuel des 5 catégories de tri (`utils/categories.py`)
- [x] Dockerfile / docker-compose (squelette)
- [ ] Intégration scraper réel (Étudiant A) -> choix utilisateur -> modèle réel (Étudiant B)
- [ ] Chargement du modèle `.h5` dans l'application

Lancement local :

```bash
streamlit run webapp/app.py
```

Lancement Docker :

```bash
docker build -t ecosort .
docker run -p 8501:8501 ecosort
```
