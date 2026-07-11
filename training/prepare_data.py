"""
prepare_data.py — Découpage physique du dataset en train/ et val/
Étudiant B — Deep Learning

Pourquoi ce script existe :
  train.py et evaluate.py recréaient chacun leur propre découpage
  train/validation "à la volée" avec le même seed, en supposant que
  l'ordre de lecture des fichiers serait identique d'une exécution à
  l'autre. Sur Windows, ce n'est pas garanti, ce qui cassait la
  correspondance entre les deux scripts.

  Ce script fait le découpage UNE SEULE FOIS, physiquement, en copiant
  les images dans data/processed/train/<classe>/ et
  data/processed/val/<classe>/. Plus aucune ambiguïté ensuite.

Lancer avec (environnement virtuel .venv activé), une seule fois :
    python training/prepare_data.py
"""

import random
import shutil
from pathlib import Path

SOURCE_DIR = Path("data/raw/Garbage classification/Garbage classification")
DEST_DIR = Path("data/processed")
VALIDATION_SPLIT = 0.2
SEED = 42
EXTENSIONS_IMAGES = {".jpg", ".jpeg", ".png"}


def main():
    random.seed(SEED)

    if not SOURCE_DIR.exists():
        raise FileNotFoundError(f"Dossier source introuvable : {SOURCE_DIR}")

    # Repart de zéro à chaque exécution pour éviter les mélanges d'anciens essais
    if DEST_DIR.exists():
        shutil.rmtree(DEST_DIR)
    (DEST_DIR / "train").mkdir(parents=True)
    (DEST_DIR / "val").mkdir(parents=True)

    resume = {}
    for classe_dir in sorted(SOURCE_DIR.iterdir()):
        if not classe_dir.is_dir():
            continue

        images = [
            f for f in classe_dir.iterdir()
            if f.suffix.lower() in EXTENSIONS_IMAGES
        ]
        random.shuffle(images)

        nb_val = int(len(images) * VALIDATION_SPLIT)
        images_val = images[:nb_val]
        images_train = images[nb_val:]

        train_classe_dir = DEST_DIR / "train" / classe_dir.name
        val_classe_dir = DEST_DIR / "val" / classe_dir.name
        train_classe_dir.mkdir(parents=True)
        val_classe_dir.mkdir(parents=True)

        for f in images_train:
            shutil.copy2(f, train_classe_dir / f.name)
        for f in images_val:
            shutil.copy2(f, val_classe_dir / f.name)

        resume[classe_dir.name] = (len(images_train), len(images_val))
        print(f"{classe_dir.name:<12} -> train: {len(images_train):<4} val: {len(images_val)}")

    total_train = sum(v[0] for v in resume.values())
    total_val = sum(v[1] for v in resume.values())
    print(f"\nTotal : {total_train} images train / {total_val} images validation")
    print(f"✅ Données préparées dans {DEST_DIR}/train et {DEST_DIR}/val")


if __name__ == "__main__":
    main()
