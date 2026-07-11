"""
tri_categories.py — Mapping matière -> catégorie de tri officielle
Code partagé (utils/) : utilisé par le module d'inférence (training/)
et par l'interface (webapp/) pour un affichage cohérent.

Référence : catégories officielles définies dans l'énoncé du projet.
"""

# Les 6 classes reconnues par le modèle de Deep Learning, mappées vers
# les 5 catégories officielles de tri.
CATEGORIES_TRI = {
    "plastic":   {"categorie": "Poubelle JAUNE", "couleur_nom": "jaune",  "couleur_hex": "#FFCD00"},
    "metal":     {"categorie": "Poubelle JAUNE", "couleur_nom": "jaune",  "couleur_hex": "#FFCD00"},
    "cardboard": {"categorie": "Poubelle JAUNE", "couleur_nom": "jaune",  "couleur_hex": "#FFCD00"},
    "glass":     {"categorie": "Poubelle VERTE",  "couleur_nom": "vert",  "couleur_hex": "#2E8B57"},
    "paper":     {"categorie": "Poubelle BLEUE",  "couleur_nom": "bleu",  "couleur_hex": "#1E64C8"},
    "trash":     {"categorie": "Poubelle MARRON/NOIRE", "couleur_nom": "marron", "couleur_hex": "#5A3C28"},
}

# Rappel : le Bac Électronique (D3E) n'est PAS géré par le modèle d'image
# (absent du dataset Kaggle) — à détecter par mots-clés sur le nom du
# produit scrapé, en amont ou en aval de l'appel au modèle. À gérer côté
# webapp lors de l'intégration finale.


def get_categorie_tri(matiere: str) -> dict:
    """Renvoie la catégorie de tri (nom + couleur) pour une matière donnée.
    Lève une KeyError explicite si la matière est inconnue, plutôt que de
    renvoyer silencieusement une valeur par défaut trompeuse.
    """
    if matiere not in CATEGORIES_TRI:
        raise KeyError(
            f"Matière inconnue : « {matiere} ». "
            f"Matières valides : {list(CATEGORIES_TRI.keys())}"
        )
    return CATEGORIES_TRI[matiere]
