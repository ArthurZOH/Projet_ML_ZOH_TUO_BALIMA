"""Authentification de la page de garde : comptes de démo + inscriptions.

Les comptes de démonstration restent en dur (pratique pour la soutenance).
Les comptes créés via le formulaire d'inscription sont stockés dans
data/utilisateurs.json (gitignoré), mot de passe haché (sha256 + sel) —
jamais en clair.
Module sans dépendance Streamlit pour rester testable par pytest.
"""

import hashlib
import hmac
import json
import secrets
from pathlib import Path

FICHIER_UTILISATEURS = Path("data/utilisateurs.json")
FICHIER_CLE_SESSION = Path("data/.cle_session")

# Comptes de démonstration (soutenance)
UTILISATEURS = {
    "alice": "ecosort2026",
    "arthur": "ecosort2026",
    "yannel": "ecosort2026",
}

LONGUEUR_MDP_MIN = 6


def _normaliser(identifiant: str) -> str:
    return identifiant.strip().lower()


def _hacher(mot_de_passe: str, sel: str) -> str:
    return hashlib.sha256((sel + mot_de_passe).encode("utf-8")).hexdigest()


def _charger_inscrits() -> dict:
    if FICHIER_UTILISATEURS.exists():
        try:
            return json.loads(FICHIER_UTILISATEURS.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def verifier(identifiant: str, mot_de_passe: str) -> bool:
    """Renvoie True si le couple identifiant/mot de passe est valide
    (compte de démo ou compte inscrit)."""
    if not identifiant or not mot_de_passe:
        return False
    identifiant = _normaliser(identifiant)
    if UTILISATEURS.get(identifiant) == mot_de_passe:
        return True
    inscrit = _charger_inscrits().get(identifiant)
    if inscrit is None:
        return False
    return _hacher(mot_de_passe, inscrit["sel"]) == inscrit["hash"]


def inscrire(identifiant: str, mot_de_passe: str) -> tuple[bool, str]:
    """Crée un compte. Renvoie (succès, message à afficher)."""
    identifiant = _normaliser(identifiant)
    if len(identifiant) < 3 or not identifiant.isalnum():
        return False, "Identifiant : 3 caractères minimum, lettres et chiffres uniquement."
    if len(mot_de_passe) < LONGUEUR_MDP_MIN:
        return False, f"Mot de passe : {LONGUEUR_MDP_MIN} caractères minimum."

    inscrits = _charger_inscrits()
    if identifiant in UTILISATEURS or identifiant in inscrits:
        return False, "Cet identifiant est déjà pris."

    sel = secrets.token_hex(8)
    inscrits[identifiant] = {"sel": sel, "hash": _hacher(mot_de_passe, sel)}
    FICHIER_UTILISATEURS.parent.mkdir(parents=True, exist_ok=True)
    FICHIER_UTILISATEURS.write_text(
        json.dumps(inscrits, indent=2), encoding="utf-8"
    )
    return True, "Compte créé."


# --------------------------------------------------------------------------
# Jetons de session : Streamlit repart de zéro à chaque rafraîchissement du
# navigateur ; un jeton signé (HMAC) placé dans l'URL permet de restaurer la
# connexion sans pouvoir être forgé (la clé secrète reste sur le serveur).
# --------------------------------------------------------------------------

def _cle_session() -> bytes:
    if FICHIER_CLE_SESSION.exists():
        return bytes.fromhex(FICHIER_CLE_SESSION.read_text(encoding="utf-8"))
    cle = secrets.token_bytes(32)
    FICHIER_CLE_SESSION.parent.mkdir(parents=True, exist_ok=True)
    FICHIER_CLE_SESSION.write_text(cle.hex(), encoding="utf-8")
    return cle


def creer_jeton(identifiant: str) -> str:
    """Jeton « identifiant:signature » à placer dans l'URL."""
    identifiant = _normaliser(identifiant)
    signature = hmac.new(
        _cle_session(), identifiant.encode("utf-8"), hashlib.sha256
    ).hexdigest()
    return f"{identifiant}:{signature}"


def verifier_jeton(jeton: str) -> str | None:
    """Renvoie l'identifiant si le jeton est authentique, sinon None."""
    identifiant, _, signature = (jeton or "").partition(":")
    if not identifiant or not signature:
        return None
    attendu = hmac.new(
        _cle_session(), identifiant.encode("utf-8"), hashlib.sha256
    ).hexdigest()
    return identifiant if hmac.compare_digest(signature, attendu) else None
