"""Authentification simple de la page de garde.

Comptes de démonstration en dur : suffisant pour le cadre du projet
(pas de données sensibles), et sans dépendance à une base de données.
Module sans dépendance Streamlit pour rester testable par pytest.
"""

UTILISATEURS = {
    "alice": "ecosort2026",
    "arthur": "ecosort2026",
    "yannel": "ecosort2026",
}


def verifier(identifiant: str, mot_de_passe: str) -> bool:
    """Renvoie True si le couple identifiant/mot de passe est valide."""
    if not identifiant or not mot_de_passe:
        return False
    return UTILISATEURS.get(identifiant.strip().lower()) == mot_de_passe
