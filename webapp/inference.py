"""Pont entre l'interface et le modèle de Deep Learning (Étudiant B).

`training.predict` est importé paresseusement : TensorFlow et le fichier
models/modele_eco_sort.h5 ne sont pas présents sur tous les postes (ni,
pour l'instant, dans le repo). Dans ce cas, l'interface retombe sur la
prédiction factice, en le signalant via le champ `reel`.

Conformément à la review de la PR #3, seuls `matiere` et `confiance`
sont consommés ici : le mapping matière -> poubelle reste du ressort de
l'interface (utils/categories.py).
"""

# Décision de la réunion d'équipe du 13/07 : « se baser sur les images
# d'abord, et s'il y a un doute se référer aux mots-clés ». En dessous de
# ce seuil de confiance, la prédiction du modèle est considérée douteuse.
SEUIL_CONFIANCE = 0.70


def predire_matiere(product: dict) -> dict:
    """Prédit la matière d'un produit à partir de son image.

    Renvoie {"matiere": str, "confiance": float | None, "reel": bool} —
    `reel` vaut False quand la prédiction vient du mock (TensorFlow ou
    .h5 indisponible, image illisible...).
    """
    try:
        from training.predict import predict_produit

        resultat = predict_produit(product["image_url"])
        return {
            "matiere": resultat["matiere"],
            "confiance": resultat["confiance"],
            "reel": True,
        }
    except Exception:
        # Volontairement large : quel que soit l'empêchement (TensorFlow
        # absent, modèle non entraîné, URL d'image cassée), l'application
        # doit rester utilisable pour la démo.
        from webapp.mocks import mock_predict

        return {"matiere": mock_predict(product), "confiance": None, "reel": False}
