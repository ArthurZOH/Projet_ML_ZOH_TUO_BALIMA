# scraper/

**Responsable : Étudiant A**

Module en charge d'interroger Jumia à partir du nom de produit saisi par
l'utilisateur, et de retourner 3 à 5 résultats structurés (nom, image, prix, lien).
Conception du module de recherche Jumia (scraping/scraper.py) : envoi des requêtes, extraction du nom, du prix, de l'image et du lien, et gestion des cas d'erreur (absence de résultat, page indisponible, délai dépassé). Écriture des tests unitaires du scraper (scraping/test_scraper.py) et gestion des dépendances associées.
À faire (étapes suivantes) :
- [x] Choisir la méthode de scraping (Requests+BeautifulSoup vs Selenium)
- [x] Fonction de recherche + parsing des résultats
- [x] Gestion des erreurs (aucun résultat, page indisponible, timeout)
- [x] Tests unitaires dans `tests/`
