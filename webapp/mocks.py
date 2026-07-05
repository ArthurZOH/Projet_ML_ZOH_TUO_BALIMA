"""Mocks temporaires en attendant les modules réels.

- mock_search remplace scraper.search (Étudiant A) : renvoie des produits
  factices au format convenu (nom, prix, image, lien).
- mock_predict remplace l'inférence du modèle (Étudiant B) : renvoie une
  classe du dataset Kaggle choisie de façon déterministe.

À supprimer lors de l'intégration (J7 du plan de travail).
"""

# Format de résultat convenu avec l'Étudiant A (scraper Jumia)
MOCK_PRODUCTS = [
    {
        "name": "Bouteille d'eau minérale Awa 1,5 L (pack de 6)",
        "price": "1 200 FCFA",
        "image_url": "https://placehold.co/200x200?text=Bouteille",
        "url": "https://www.jumia.ci/exemple-bouteille",
    },
    {
        "name": "Bocal de confiture de fraises 370 g",
        "price": "2 500 FCFA",
        "image_url": "https://placehold.co/200x200?text=Bocal",
        "url": "https://www.jumia.ci/exemple-bocal",
    },
    {
        "name": "Cahier 200 pages grands carreaux",
        "price": "800 FCFA",
        "image_url": "https://placehold.co/200x200?text=Cahier",
        "url": "https://www.jumia.ci/exemple-cahier",
    },
    {
        "name": "Écouteurs Bluetooth sans fil TWS",
        "price": "5 900 FCFA",
        "image_url": "https://placehold.co/200x200?text=Ecouteurs",
        "url": "https://www.jumia.ci/exemple-ecouteurs",
    },
]

# Classes du dataset Kaggle, dans l'ordre des produits mock ci-dessus
_MOCK_CLASSES = ["plastic", "glass", "paper", "trash"]


def mock_search(keyword: str) -> list[dict]:
    """Simule scraper.search(keyword) : 3 à 5 produits Jumia."""
    if not keyword.strip():
        return []
    return MOCK_PRODUCTS


def mock_predict(product: dict) -> str:
    """Simule l'inférence du modèle : renvoie une classe Kaggle."""
    try:
        index = MOCK_PRODUCTS.index(product)
    except ValueError:
        index = 0
    return _MOCK_CLASSES[index % len(_MOCK_CLASSES)]
