"""Tests de l'authentification de la page de garde (webapp/auth.py)."""

from webapp.auth import UTILISATEURS, verifier


def test_identifiants_valides():
    for identifiant, mot_de_passe in UTILISATEURS.items():
        assert verifier(identifiant, mot_de_passe) is True


def test_identifiant_insensible_casse_et_espaces():
    assert verifier("  Yannel ", "ecosort2026") is True


def test_mauvais_mot_de_passe_refuse():
    assert verifier("yannel", "mauvais") is False


def test_utilisateur_inconnu_refuse():
    assert verifier("intrus", "ecosort2026") is False


def test_champs_vides_refuses():
    assert verifier("", "") is False
    assert verifier("yannel", "") is False
