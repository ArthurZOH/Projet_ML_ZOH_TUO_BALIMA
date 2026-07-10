"""Mocks temporaires en attendant les modules réels.

- mock_predict remplace l'inférence du modèle (Étudiant B) : renvoie une
  classe du dataset Kaggle choisie de façon déterministe.
- mock_search (scraper) a été retiré : le vrai scraper est intégré.

À supprimer lors de l'intégration du modèle réel.
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


def mock_predict(product: dict) -> str:
    """Simule l'inférence du modèle : renvoie une classe Kaggle."""
    try:
        index = MOCK_PRODUCTS.index(product)
    except ValueError:
        index = 0
    return _MOCK_CLASSES[index % len(_MOCK_CLASSES)]
