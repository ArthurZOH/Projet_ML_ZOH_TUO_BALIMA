"""Détection de poubelle par mots-clés sur le titre du produit.

Décision de la réunion d'équipe du 13/07, complétée le 14/07 : quand le
modèle d'image doute (confiance < seuil), les mots-clés du titre guident
le choix de la poubelle ; sans aucun indice, direction les résiduels
(marron) par précaution — la règle d'or du tri réel.

L'électronique est testée en premier (matière absente du dataset Kaggle),
puis les matières recyclables ; le marron sert de filet de sécurité.
Normalisation : insensible aux accents, mots entiers uniquement.
"""

import re
import unicodedata

# Mots simples (comparés aux mots entiers du titre normalisé) et
# expressions (cherchées telles quelles), par poubelle.
MOTS_CLES_POUBELLES = {
    "electronique": {
        "mots": {
            "bluetooth", "ecouteur", "ecouteurs", "casque", "chargeur", "cable",
            "usb", "smartphone", "telephone", "tablette", "batterie", "batteries",
            "pile", "piles", "montre", "mixeur", "blender", "telecommande",
            "lampe", "led", "electrique", "electronique", "ventilateur",
            "console", "ordinateur", "clavier", "souris", "enceinte", "radio",
            "televiseur", "tv", "camera", "drone", "rasoir", "ampoule",
            "imprimante", "scanner", "ecran", "moniteur", "modem", "routeur",
            "manette", "projecteur", "videoprojecteur", "webcam", "climatiseur",
            "refrigerateur", "frigo", "congelateur", "aspirateur", "bouilloire",
        },
        "phrases": (
            "seche cheveux", "fer a repasser", "machine a coudre",
            "micro ondes", "machine a laver", "grille pain", "fer a lisser",
        ),
    },
    "jaune": {
        "mots": {
            "plastique", "bouteille", "bouteilles", "canette", "canettes",
            "conserve", "conserves", "aluminium", "alu", "carton", "cartons",
            "brique", "flacon", "bidon", "gobelet", "gobelets",
        },
        "phrases": (),
    },
    "verte": {
        "mots": {"verre", "bocal", "bocaux", "carafe"},
        "phrases": (),
    },
    "bleue": {
        "mots": {
            "papier", "papiers", "cahier", "cahiers", "journal", "livre",
            "livres", "magazine", "enveloppe", "enveloppes", "carnet", "agenda",
        },
        "phrases": (),
    },
    "marron": {
        "mots": {
            "ceramique", "porcelaine", "assiette", "assiettes", "bol", "bols",
            "tasse", "tasses", "mug", "vaisselle", "eponge", "eponges",
            "couche", "couches", "serviette", "serviettes", "coton",
        },
        "phrases": (),
    },
}

# Ordre de test : l'électronique d'abord (hors modèle), puis les matières
# recyclables (un mot de matière prime sur un mot d'objet : « bol en
# plastique » -> jaune), le marron en dernier.
PRIORITE = ("electronique", "jaune", "verte", "bleue", "marron")


def _normaliser(texte: str) -> str:
    """Minuscules, accents supprimés, tirets/apostrophes ramenés à l'espace."""
    texte = unicodedata.normalize("NFKD", texte.lower())
    texte = "".join(c for c in texte if not unicodedata.combining(c))
    return re.sub(r"[-'’/]", " ", texte)


def detecter_poubelle(product_name: str) -> str | None:
    """Renvoie la clé de poubelle suggérée par le titre, ou None si le
    titre ne contient aucun mot-clé connu."""
    texte = _normaliser(product_name)
    mots = set(re.findall(r"[a-z0-9]+", texte))
    for cle in PRIORITE:
        regles = MOTS_CLES_POUBELLES[cle]
        if mots & regles["mots"]:
            return cle
        if any(phrase in texte for phrase in regles["phrases"]):
            return cle
    return None
