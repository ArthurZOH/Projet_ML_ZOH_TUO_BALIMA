"""Calculs du tableau de bord (éco-points, niveaux, répartition par poubelle).

Module sans dépendance Streamlit pour rester testable par pytest.
"""

from collections import Counter

POINTS_PAR_TRI = 10

# Seuils (nombre de produits triés) -> niveau atteint
SEUILS_NIVEAUX = [
    (0, "🌱 Débutant"),
    (3, "🍃 Apprenti trieur"),
    (6, "🌿 Éco-citoyen"),
    (10, "🌳 Éco-héros"),
]


def compter_par_poubelle(history: list[dict]) -> Counter:
    """Nombre de produits triés par clé de poubelle."""
    return Counter(entree["bin_key"] for entree in history)


def calculer_niveau(nb_tris: int) -> dict:
    """Niveau de l'utilisateur et progression vers le niveau suivant.

    Renvoie : label du niveau, éco-points, seuil suivant (None au niveau
    max) et progression 0..1 entre le seuil courant et le suivant.
    """
    seuil_courant, label = SEUILS_NIVEAUX[0]
    seuil_suivant = None
    for i, (seuil, nom) in enumerate(SEUILS_NIVEAUX):
        if nb_tris >= seuil:
            seuil_courant, label = seuil, nom
            seuil_suivant = (
                SEUILS_NIVEAUX[i + 1][0] if i + 1 < len(SEUILS_NIVEAUX) else None
            )

    if seuil_suivant is None:
        progression = 1.0
    else:
        progression = (nb_tris - seuil_courant) / (seuil_suivant - seuil_courant)

    return {
        "label": label,
        "points": nb_tris * POINTS_PAR_TRI,
        "seuil_suivant": seuil_suivant,
        "progression": min(max(progression, 0.0), 1.0),
    }
