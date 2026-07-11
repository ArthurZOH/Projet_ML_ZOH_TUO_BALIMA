"""
train.py — Entraînement du modèle de classification EcoSort
Étudiant B — Deep Learning

Stratégie : Transfer Learning avec MobileNetV2 (pré-entraîné sur ImageNet).
On gèle les couches de base et on entraîne uniquement une petite tête de
classification adaptée à nos 6 classes (cardboard, glass, metal, paper,
plastic, trash).

Lancer avec (environnement virtuel .venv activé) :
    python training/train.py
"""

from pathlib import Path

import numpy as np
import tensorflow as tf
from sklearn.utils.class_weight import compute_class_weight

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------
DATASET_DIR = Path("data/processed")
MODELS_DIR = Path("models")
IMG_SIZE = (224, 224)          # taille attendue par MobileNetV2
BATCH_SIZE = 32
EPOCHS = 15


def charger_datasets():
    """Charge les images depuis les dossiers déjà découpés par
    prepare_data.py (data/processed/train et data/processed/val)."""
    train_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR / "train",
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR / "val",
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        shuffle=False,
    )
    return train_ds, val_ds


def calculer_class_weight(train_ds, class_names):
    """Calcule un poids par classe pour compenser le déséquilibre
    (rappel : trash n'a que 137 images contre 594 pour paper)."""
    labels = np.concatenate([y.numpy() for _, y in train_ds])
    poids = compute_class_weight(
        class_weight="balanced",
        classes=np.arange(len(class_names)),
        y=labels,
    )
    return dict(enumerate(poids))


def construire_modele(nb_classes: int) -> tf.keras.Model:
    """Construit le modèle : MobileNetV2 gelé + petite tête de classification."""

    # Couches de data augmentation : appliquées uniquement à l'entraînement,
    # elles "inventent" des variantes des images existantes pour aider le
    # modèle à mieux généraliser avec peu de données.
    augmentation = tf.keras.Sequential([
        tf.keras.layers.RandomFlip("horizontal"),
        tf.keras.layers.RandomRotation(0.15),
        tf.keras.layers.RandomZoom(0.15),
    ])

    base_model = tf.keras.applications.MobileNetV2(
        input_shape=IMG_SIZE + (3,),
        include_top=False,       # on retire la dernière couche (1000 classes ImageNet)
        weights="imagenet",
    )
    base_model.trainable = False  # on gèle : on ne réentraîne pas ImageNet

    inputs = tf.keras.Input(shape=IMG_SIZE + (3,))
    x = augmentation(inputs)
    # Équivalent à mobilenet_v2.preprocess_input (ramène les pixels de [0,255]
    # à [-1,1]), mais via une vraie couche Keras : se sauvegarde correctement
    # en .h5, contrairement à un appel de fonction brut.
    x = tf.keras.layers.Rescaling(scale=1.0 / 127.5, offset=-1.0)(x)
    x = base_model(x, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dropout(0.2)(x)
    outputs = tf.keras.layers.Dense(nb_classes, activation="softmax")(x)

    model = tf.keras.Model(inputs, outputs)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def main():
    MODELS_DIR.mkdir(exist_ok=True)

    print("Chargement des données...")
    train_ds, val_ds = charger_datasets()
    class_names = train_ds.class_names
    print(f"Classes détectées : {class_names}")

    class_weight = calculer_class_weight(train_ds, class_names)
    print(f"Poids par classe (compense le déséquilibre) : {class_weight}")

    # Optimisation du chargement (évite que le GPU/CPU attende le disque)
    autotune = tf.data.AUTOTUNE
    train_ds = train_ds.cache().prefetch(buffer_size=autotune)
    val_ds = val_ds.cache().prefetch(buffer_size=autotune)

    print("Construction du modèle (MobileNetV2 gelé + tête de classification)...")
    model = construire_modele(nb_classes=len(class_names))
    model.summary()

    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_accuracy", patience=3, restore_best_weights=True
        ),
        tf.keras.callbacks.ModelCheckpoint(
            filepath=str(MODELS_DIR / "modele_eco_sort.h5"),
            monitor="val_accuracy",
            save_best_only=True,
        ),
    ]

    print("Entraînement en cours...")
    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS,
        class_weight=class_weight,
        callbacks=callbacks,
    )

    print(f"\n✅ Modèle sauvegardé dans {MODELS_DIR / 'modele_eco_sort.h5'}")
    print(f"Classes (ordre important pour l'inférence) : {class_names}")


if __name__ == "__main__":
    main()
