"""Tests de l'authentification de la page de garde (webapp/auth.py)."""

import json

import pytest

from webapp import auth
from webapp.auth import UTILISATEURS, creer_jeton, inscrire, verifier, verifier_jeton


@pytest.fixture(autouse=True)
def fichiers_temporaires(tmp_path, monkeypatch):
    """Chaque test travaille sur ses propres fichiers (inscrits + clé)."""
    monkeypatch.setattr(auth, "FICHIER_UTILISATEURS", tmp_path / "utilisateurs.json")
    monkeypatch.setattr(auth, "FICHIER_CLE_SESSION", tmp_path / ".cle_session")


class TestConnexion:
    def test_identifiants_demo_valides(self):
        for identifiant, mot_de_passe in UTILISATEURS.items():
            assert verifier(identifiant, mot_de_passe) is True

    def test_identifiant_insensible_casse_et_espaces(self):
        assert verifier("  Yannel ", "ecosort2026") is True

    def test_mauvais_mot_de_passe_refuse(self):
        assert verifier("yannel", "mauvais") is False

    def test_utilisateur_inconnu_refuse(self):
        assert verifier("intrus", "ecosort2026") is False

    def test_champs_vides_refuses(self):
        assert verifier("", "") is False
        assert verifier("yannel", "") is False


class TestInscription:
    def test_inscription_puis_connexion(self):
        succes, _ = inscrire("nina", "motdepasse")
        assert succes is True
        assert verifier("nina", "motdepasse") is True
        assert verifier("NINA ", "motdepasse") is True  # normalisation
        assert verifier("nina", "autre") is False

    def test_identifiant_demo_deja_pris(self):
        succes, message = inscrire("yannel", "motdepasse")
        assert succes is False
        assert "pris" in message

    def test_double_inscription_refusee(self):
        assert inscrire("nina", "motdepasse")[0] is True
        assert inscrire("nina", "autremotdepasse")[0] is False

    def test_identifiant_invalide_refuse(self):
        assert inscrire("ab", "motdepasse")[0] is False       # trop court
        assert inscrire("nina !", "motdepasse")[0] is False   # caractères interdits

    def test_mot_de_passe_trop_court_refuse(self):
        assert inscrire("nina", "abc")[0] is False

    def test_mot_de_passe_jamais_stocke_en_clair(self):
        inscrire("nina", "supersecret")
        contenu = auth.FICHIER_UTILISATEURS.read_text(encoding="utf-8")
        assert "supersecret" not in contenu
        donnees = json.loads(contenu)
        assert set(donnees["nina"]) == {"sel", "hash"}


class TestJetonsSession:
    def test_jeton_valide_restaure_l_identifiant(self):
        assert verifier_jeton(creer_jeton("Yannel ")) == "yannel"

    def test_jeton_falsifie_refuse(self):
        jeton = creer_jeton("yannel")
        assert verifier_jeton(jeton.replace("yannel", "arthur")) is None
        assert verifier_jeton(jeton[:-4] + "0000") is None

    def test_jeton_malforme_refuse(self):
        assert verifier_jeton("") is None
        assert verifier_jeton("pasdedeuxpoints") is None
        assert verifier_jeton("yannel:") is None
