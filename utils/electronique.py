"""Détection des produits électroniques (D3E) par mots-clés sur le titre.

Les D3E (déchets d'équipements électriques et électroniques) ne figurent
pas dans le dataset Kaggle : on les détecte en amont du modèle, à partir
du nom du produit. Version affinée par rapport à la v0 de webapp/app.py :
  - insensible aux accents (« Téléphone » == « telephone ») ;
  - mots entiers uniquement, pour éviter les faux positifs
    (ex. « pile » ne doit pas matcher « pileuse à riz »).
"""

import re
import unicodedata

# Mots-clés simples, comparés aux mots entiers du titre normalisé
KEYWORDS_D3E = {
    "bluetooth", "ecouteur", "ecouteurs", "casque", "chargeur", "cable",
    "usb", "smartphone", "telephone", "tablette", "batterie", "batteries",
    "pile", "piles", "montre", "mixeur", "blender", "telecommande",
    "lampe", "led", "electrique", "electronique", "ventilateur",
    "console", "ordinateur", "clavier", "souris", "enceinte", "radio",
    "televiseur", "tv", "camera", "drone", "rasoir", "ampoule",
    # Ajouts réunion d'équipe du 13/07
    "imprimante", "scanner", "ecran", "moniteur", "modem", "routeur",
    "manette", "projecteur", "videoprojecteur", "webcam", "climatiseur",
    "refrigerateur", "frigo", "congelateur", "aspirateur", "bouilloire",
}

# Expressions multi-mots, cherchées telles quelles dans le titre normalisé
PHRASES_D3E = (
    "seche cheveux",
    "fer a repasser",
    "machine a coudre",
    # Ajouts réunion d'équipe du 13/07
    "micro ondes",
    "machine a laver",
    "grille pain",
    "fer a lisser",
)


def _normaliser(texte: str) -> str:
    """Minuscules, accents supprimés, tirets/apostrophes ramenés à l'espace."""
    texte = unicodedata.normalize("NFKD", texte.lower())
    texte = "".join(c for c in texte if not unicodedata.combining(c))
    return re.sub(r"[-'’/]", " ", texte)


def detect_electronique(product_name: str) -> bool:
    """Renvoie True si le titre du produit évoque un appareil électronique."""
    texte = _normaliser(product_name)
    mots = set(re.findall(r"[a-z0-9]+", texte))
    if mots & KEYWORDS_D3E:
        return True
    return any(phrase in texte for phrase in PHRASES_D3E)
