"""Tests de la détection de poubelle par mots-clés (utils/mots_cles.py)."""

import pytest

from utils.categories import BINS
from utils.mots_cles import MOTS_CLES_POUBELLES, PRIORITE, detecter_poubelle


def test_toutes_les_poubelles_referencees_existent():
    assert set(MOTS_CLES_POUBELLES) == set(PRIORITE)
    for cle in MOTS_CLES_POUBELLES:
        assert cle in BINS


@pytest.mark.parametrize("titre, attendu", [
    ("Écouteurs Bluetooth sans fil TWS", "electronique"),
    ("Imprimante multifonction jet d'encre", "electronique"),
    ("Machine à laver 7 kg", "electronique"),
    ("Pack de 6 bouteilles d'eau minérale", "jaune"),
    ("Canette de soda 33 cl", "jaune"),
    ("Bocal de confiture de fraises", "verte"),
    ("Cahier 200 pages grands carreaux", "bleue"),
    ("Bol à soupe en céramique", "marron"),
    ("Assiette en porcelaine blanche", "marron"),
])
def test_detection_par_poubelle(titre, attendu):
    assert detecter_poubelle(titre) == attendu


def test_electronique_prioritaire_sur_le_reste():
    # « mixeur » (D3E) doit l'emporter sur « bol » (marron)
    assert detecter_poubelle("Bol mixeur électrique 2 L") == "electronique"


def test_matiere_prime_sur_objet():
    # « plastique » (jaune) doit l'emporter sur « bol » (marron)
    assert detecter_poubelle("Bol en plastique incassable") == "jaune"


def test_aucun_indice_renvoie_none():
    assert detecter_poubelle("Sac à main en cuir camel") is None
    assert detecter_poubelle("") is None
