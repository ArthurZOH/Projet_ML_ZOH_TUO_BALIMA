"""Tests du pont interface <-> modèle (webapp/inference.py)."""

import sys
import types

from webapp.inference import predire_matiere

PRODUIT = {
    "name": "Bouteille d'eau minérale Awa 1,5 L (pack de 6)",
    "price": "1 200 FCFA",
    "image_url": "https://exemple.test/image.jpg",
    "url": "https://www.jumia.ci/exemple",
}


def _faux_module_predict(fonction):
    """Installe un faux training.predict dans sys.modules."""
    module = types.ModuleType("training.predict")
    module.predict_produit = fonction
    return module


def test_utilise_le_modele_quand_disponible(monkeypatch):
    monkeypatch.setitem(
        sys.modules, "training.predict",
        _faux_module_predict(lambda url: {"matiere": "glass", "confiance": 0.91}),
    )
    resultat = predire_matiere(PRODUIT)
    assert resultat == {"matiere": "glass", "confiance": 0.91, "reel": True}


def test_fallback_si_prediction_echoue(monkeypatch):
    def predict_qui_plante(url):
        raise RuntimeError("URL d'image cassée")

    monkeypatch.setitem(
        sys.modules, "training.predict", _faux_module_predict(predict_qui_plante)
    )
    resultat = predire_matiere(PRODUIT)
    assert resultat["reel"] is False
    assert resultat["confiance"] is None
    assert resultat["matiere"] == "plastic"  # mock déterministe pour ce produit


def test_fallback_sans_tensorflow():
    # Sur ce poste, TensorFlow n'est pas installé : l'import réel de
    # training.predict échoue et le mock doit prendre le relais.
    assert "tensorflow" not in sys.modules
    resultat = predire_matiere(PRODUIT)
    assert resultat["reel"] is False
    assert resultat["matiere"] == "plastic"
