"""
predict.py — Inférence : prédit la catégorie de tri d'un produit à partir
d'une image (chemin local OU URL).
Étudiant B — Deep Learning

C'est ce module que l'interface (webapp/) appellera après que
l'utilisateur ait choisi un produit parmi les résultats du scraper.

Utilisation :
    from training.predict import predict_produit
    resultat = predict_produit("https://img.jumia.ci/produit1.jpg")
    # ou
    resultat = predict_produit("data/raw/.../plastic/plastic1.jpg")

    print(resultat)
    # {'matiere': 'plastic', 'confiance': 0.94,
    #  'categorie': 'Poubelle JAUNE', 'couleur_nom': 'jaune',
    #  'couleur_hex': '#FFCD00'}
"""

import sys
from io import BytesIO
from pathlib import Path

import numpy as np
import requests
import tensorflow as tf
from PIL import Image

# Permet d'importer utils/ même si ce script est lancé directement
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.tri_categories import get_categorie_tri  # noqa: E402

MODEL_PATH = Path("models/modele_eco_sort.h5")
IMG_SIZE = (224, 224)

# IMPORTANT : cet ordre doit être EXACTEMENT celui affiché par train.py
# ("Classes (ordre important pour l'inférence)"), car c'est l'ordre des
# neurones de sortie du modèle.
NOMS_CLASSES = ["cardboard", "glass", "metal", "paper", "plastic", "trash"]


class ModeleNonTrouveError(Exception):
    """Levée si modele_eco_sort.h5 n'existe pas (pas encore entraîné)."""


class ImageInvalideError(Exception):
    """Levée si l'image ne peut pas être chargée (URL cassée, fichier corrompu...)."""


_modele = None  # cache : le modèle n'est chargé qu'une seule fois par processus


def _charger_modele() -> tf.keras.Model:
    global _modele
    if _modele is None:
        if not MODEL_PATH.exists():
            raise ModeleNonTrouveError(
                f"Modèle introuvable à {MODEL_PATH}. "
                "Lance d'abord training/train.py pour l'entraîner."
            )
        _modele = tf.keras.models.load_model(MODEL_PATH)
    return _modele


def _charger_image(source: str) -> Image.Image:
    """Charge une image depuis une URL (http/https) ou un chemin local."""
    try:
        if source.startswith("http://") or source.startswith("https://"):
            reponse = requests.get(source, timeout=8)
            reponse.raise_for_status()
            image = Image.open(BytesIO(reponse.content))
        else:
            image = Image.open(source)
        return image.convert("RGB")  # évite les soucis avec les PNG en RGBA
    except Exception as exc:
        raise ImageInvalideError(f"Impossible de charger l'image « {source} » : {exc}") from exc


def predict_produit(source_image: str) -> dict:
    """
    Prédit la matière et la catégorie de tri d'un produit à partir d'une image.

    Args:
        source_image: URL (http/https) ou chemin de fichier local.

    Returns:
        dict avec : matiere, confiance, categorie, couleur_nom, couleur_hex

    Lève :
        ModeleNonTrouveError, ImageInvalideError
    """
    modele = _charger_modele()
    image = _charger_image(source_image)

    image = image.resize(IMG_SIZE)
    array = np.array(image, dtype=np.float32)
    array = np.expand_dims(array, axis=0)  # le modèle attend un batch (1, 224, 224, 3)

    # Pas de normalisation manuelle ici : la couche Rescaling est déjà
    # intégrée DANS le modèle (voir train.py), on donne donc les pixels
    # bruts [0, 255] directement.
    predictions = modele.predict(array, verbose=0)[0]

    index_predit = int(np.argmax(predictions))
    matiere = NOMS_CLASSES[index_predit]
    confiance = float(predictions[index_predit])

    info_tri = get_categorie_tri(matiere)

    return {
        "matiere": matiere,
        "confiance": round(confiance, 4),
        **info_tri,
    }


if __name__ == "__main__":
    # Petit test manuel : lance avec un chemin ou une URL en argument
    #   python training/predict.py chemin/vers/une/image.jpg
    if len(sys.argv) < 2:
        print("Usage : python training/predict.py <chemin_ou_url_image>")
        sys.exit(1)

    resultat = predict_produit(sys.argv[1])
    print(resultat)
