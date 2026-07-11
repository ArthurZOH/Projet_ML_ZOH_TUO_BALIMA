"""
evaluate.py — Évaluation détaillée du modèle EcoSort
Étudiant B — Deep Learning

Charge le modèle déjà entraîné et calcule, sur les données de validation :
  - une matrice de confusion (sauvegardée en image)
  - un rapport précision/rappel par classe

Lancer avec (environnement virtuel .venv activé) :
    python training/evaluate.py
"""

from pathlib import Path

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report, ConfusionMatrixDisplay

# --------------------------------------------------------------------------
# Configuration — DOIT correspondre exactement à train.py pour retomber
# sur le même découpage train/validation (même seed, même split)
# --------------------------------------------------------------------------
DATASET_DIR = Path("data/processed")
MODEL_PATH = Path("models/modele_eco_sort.h5")
OUTPUT_DIR = Path("training/outputs")
IMG_SIZE = (224, 224)
BATCH_SIZE = 32


def charger_dataset_validation():
    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR / "val",
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=False,  # important : pour aligner prédictions et vraies étiquettes
    )
    return val_ds


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Chargement du modèle depuis {MODEL_PATH}...")
    model = tf.keras.models.load_model(MODEL_PATH)

    print("Chargement des données de validation...")
    val_ds = charger_dataset_validation()
    class_names = val_ds.class_names

    print("Prédiction sur les données de validation...")
    y_true = np.concatenate([y.numpy() for _, y in val_ds])
    y_pred_probs = model.predict(val_ds)
    y_pred = np.argmax(y_pred_probs, axis=1)

    # --- Rapport texte : précision/rappel/f1 par classe ---
    print("\n" + "=" * 60)
    print("RAPPORT DE CLASSIFICATION")
    print("=" * 60)
    print(classification_report(y_true, y_pred, target_names=class_names))

    # --- Matrice de confusion : sauvegardée en image ---
    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)
    fig, ax = plt.subplots(figsize=(8, 8))
    disp.plot(ax=ax, cmap="Blues", xticks_rotation=45, colorbar=False)
    plt.title("Matrice de confusion — EcoSort-Search")
    plt.tight_layout()

    chemin_image = OUTPUT_DIR / "matrice_confusion.png"
    plt.savefig(chemin_image, dpi=150)
    print(f"\n✅ Matrice de confusion sauvegardée dans {chemin_image}")


if __name__ == "__main__":
    main()
