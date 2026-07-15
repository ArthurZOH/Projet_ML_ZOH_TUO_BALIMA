"""Détection des produits électroniques (D3E) par mots-clés sur le titre.

Depuis la généralisation des mots-clés à toutes les poubelles (réunion
du 13/07), la logique vit dans utils/mots_cles.py — ce module conserve
l'API historique `detect_electronique` utilisée par les tests et la doc.
"""

from utils.mots_cles import detecter_poubelle


def detect_electronique(product_name: str) -> bool:
    """Renvoie True si le titre du produit évoque un appareil électronique."""
    return detecter_poubelle(product_name) == "electronique"
