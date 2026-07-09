"""Tests de la détection D3E (utils/electronique.py)."""

import pytest

from utils.electronique import detect_electronique


class TestDetectionPositive:
    @pytest.mark.parametrize("titre", [
        "Écouteurs Bluetooth sans fil TWS",
        "Chargeur USB-C rapide 25W",
        "TÉLÉPHONE Android 128 Go",          # accents + majuscules
        "Montre connectée étanche",
        "Lampe LED rechargeable",
        "Sèche-cheveux professionnel 2000W",  # expression multi-mots avec tiret
        "Fer à repasser vapeur",
    ])
    def test_produits_electroniques_detectes(self, titre):
        assert detect_electronique(titre) is True


class TestDetectionNegative:
    @pytest.mark.parametrize("titre", [
        "Bouteille d'eau minérale Awa 1,5 L",
        "Cahier 200 pages grands carreaux",
        "Bocal de confiture de fraises 370 g",
        "Pileuse à riz traditionnelle",   # « pile » ne doit pas matcher en sous-chaîne
        "Sac à main en cuir camel",       # « came » != « camera »
    ])
    def test_produits_non_electroniques_ignores(self, titre):
        assert detect_electronique(titre) is False


def test_titre_vide():
    assert detect_electronique("") is False
