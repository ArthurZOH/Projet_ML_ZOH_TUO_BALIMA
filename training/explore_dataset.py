"""
explore_dataset.py — Exploration du dataset Garbage Classification
Étudiant B — Deep Learning

Objectif : compter le nombre d'images par classe pour savoir si le
dataset est équilibré, avant de choisir la stratégie d'entraînement.

Lancer avec :  python training/explore_dataset.py
"""

from pathlib import Path

# Chemin vers le dossier contenant les 6 sous-dossiers (cardboard, glass, ...)
DATASET_DIR = Path("data/raw/Garbage classification/Garbage classification")

EXTENSIONS_IMAGES = {".jpg", ".jpeg", ".png"}


def compter_images_par_classe(dataset_dir: Path) -> dict:
    if not dataset_dir.exists():
        raise FileNotFoundError(
            f"Dossier introuvable : {dataset_dir}\n"
            "Vérifie le chemin exact vers le dossier contenant "
            "cardboard/, glass/, metal/, paper/, plastic/, trash/."
        )

    resultats = {}
    for classe_dir in sorted(dataset_dir.iterdir()):
        if classe_dir.is_dir():
            nb_images = sum(
                1 for f in classe_dir.iterdir()
                if f.suffix.lower() in EXTENSIONS_IMAGES
            )
            resultats[classe_dir.name] = nb_images
    return resultats


def afficher_resultats(resultats: dict) -> None:
    if not resultats:
        print("Aucune classe trouvée. Vérifie le chemin DATASET_DIR.")
        return

    total = sum(resultats.values())
    print(f"\n{'Classe':<15}{'Nb images':<12}{'Proportion'}")
    print("-" * 40)
    for classe, nb in resultats.items():
        proportion = (nb / total * 100) if total else 0
        barre = "█" * int(proportion / 2)
        print(f"{classe:<15}{nb:<12}{proportion:5.1f}%  {barre}")
    print("-" * 40)
    print(f"{'TOTAL':<15}{total}\n")

    minimum = min(resultats.values())
    maximum = max(resultats.values())
    ratio = maximum / minimum if minimum else float("inf")
    print(f"Classe la plus petite : {minimum} images")
    print(f"Classe la plus grande : {maximum} images")
    print(f"Ratio déséquilibre max/min : {ratio:.1f}x")
    if ratio > 2:
        print("⚠️  Déséquilibre notable entre les classes — à garder en tête "
              "pour l'entraînement (data augmentation, class_weight, etc.)")
    else:
        print("✅ Dataset globalement équilibré.")


if __name__ == "__main__":
    resultats = compter_images_par_classe(DATASET_DIR)
    afficher_resultats(resultats)
