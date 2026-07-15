"""Constantes partagées : les 5 catégories de tri officielles du projet.

Référence UI pour l'habillage visuel (Étudiant C) et cible du mapping
classes du modèle -> poubelles (Étudiant B).
"""

BINS = {
    "jaune": {
        "label": "Poubelle JAUNE",
        "color": "#F5C518",
        "text_color": "#000000",
        "emoji": "🟡",
        "consigne": "Emballages ménagers légers : bouteilles plastique, canettes, "
                    "conserves, briques, flacons, cartons de colis.",
        "matieres": ["plastic", "metal", "cardboard"],
    },
    "verte": {
        "label": "Poubelle VERTE",
        "color": "#2E7D32",
        "text_color": "#FFFFFF",
        "emoji": "🟢",
        "consigne": "Verre d'emballage uniquement : bouteilles, pots, bocaux. "
                    "Vaisselle cassée interdite.",
        "matieres": ["glass"],
    },
    "bleue": {
        "label": "Poubelle BLEUE",
        "color": "#1565C0",
        "text_color": "#FFFFFF",
        "emoji": "🔵",
        "consigne": "Papiers graphiques propres : journaux, magazines, cahiers, "
                    "livres, enveloppes, prospectus.",
        "matieres": ["paper"],
    },
    "electronique": {
        "label": "Bac ÉLECTRONIQUE (D3E)",
        "color": "#616161",
        "text_color": "#FFFFFF",
        "emoji": "🎛️",
        "consigne": "Tout produit à pile, batterie ou prise : smartphones, "
                    "écouteurs, chargeurs, mixeurs, montres.",
        "matieres": [],
    },
    "marron": {
        "label": "Poubelle MARRON / NOIRE",
        "color": "#4E342E",
        "text_color": "#FFFFFF",
        "emoji": "⚫",
        "consigne": "Déchets résiduels non recyclables : restes alimentaires, "
                    "films plastiques, produits d'hygiène, multicouches.",
        "matieres": ["trash"],
    },
}

# Mapping classe du modèle -> clé de poubelle. Les classes proviennent du
# dataset Kaggle Garbage Classification ; "electronique" sera traité à part
# (mots-clés sur le titre produit, voir Étudiant B).
CLASS_TO_BIN = {
    "plastic": "jaune",
    "metal": "jaune",
    "cardboard": "jaune",
    "glass": "verte",
    "paper": "bleue",
    "trash": "marron",
}
