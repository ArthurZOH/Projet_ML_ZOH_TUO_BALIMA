# training/

**Responsable : Étudiant B**
Préparation et exploration du jeu de données (`training/prepare_data.py`,
`training/explore_dataset.py`), entraînement du modèle de classification d'images
MobileNetV2 (`training/train.py`) atteignant 86 pour cent d'exactitude, évaluation avec
matrice de confusion (`training/evaluate.py`), module d'inférence (`training/predict.py`)
et correspondance des classes du modèle vers les catégories de tri
(`utils/tri_categories.py`). Mise en place initiale de l'architecture du dépôt et
versionnement du modèle entraîné.
Scripts d'entraînement et d'évaluation du modèle de classification
(matière de l'emballage : plastic, metal, cardboard, glass, paper, trash).

À faire (étapes suivantes) :
- [x] Récupération du dataset Kaggle "Garbage Classification"
- [x] Prétraitement / augmentation des images
- [x] Entraînement (CNN custom ou Transfer Learning)
- [x] Évaluation (accuracy, matrice de confusion)
- [x] Export du modèle dans `models/`
