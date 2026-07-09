"""Questions du quiz du tri (page Quiz).

Module sans dépendance Streamlit pour rester testable par pytest.
Chaque question référence des clés de poubelles de utils/categories.py.
"""

QUESTIONS = [
    {
        "question": "Où jeter une bouteille d'eau en plastique vide ?",
        "options": ["jaune", "verte", "bleue", "marron"],
        "reponse": "jaune",
        "explication": "Les bouteilles en plastique sont des emballages légers : direction la poubelle jaune.",
    },
    {
        "question": "Un bocal de confiture en verre, une fois rincé ?",
        "options": ["jaune", "verte", "bleue", "marron"],
        "reponse": "verte",
        "explication": "Le verre d'emballage (bouteilles, pots, bocaux) va dans la poubelle verte.",
    },
    {
        "question": "Des écouteurs Bluetooth qui ne fonctionnent plus ?",
        "options": ["jaune", "electronique", "bleue", "marron"],
        "reponse": "electronique",
        "explication": "Tout appareil à pile, batterie ou prise est un D3E : bac électronique dédié.",
    },
    {
        "question": "Les restes de votre déjeuner ?",
        "options": ["jaune", "verte", "bleue", "marron"],
        "reponse": "marron",
        "explication": "Les restes alimentaires sont des déchets résiduels : poubelle marron/noire.",
    },
    {
        "question": "Le journal d'hier ?",
        "options": ["jaune", "verte", "bleue", "marron"],
        "reponse": "bleue",
        "explication": "Journaux, magazines et papiers graphiques propres vont dans la poubelle bleue.",
    },
    {
        "question": "Un verre à boire cassé ?",
        "options": ["verte", "jaune", "bleue", "marron"],
        "reponse": "marron",
        "explication": "Piège ! La vaisselle n'a pas la composition du verre d'emballage : "
                       "elle va avec les résiduels, jamais dans la poubelle verte.",
    },
    {
        "question": "Une canette de soda vide ?",
        "options": ["jaune", "verte", "electronique", "marron"],
        "reponse": "jaune",
        "explication": "Les canettes sont des emballages métalliques légers : poubelle jaune.",
    },
    {
        "question": "Une pile bouton usée ?",
        "options": ["marron", "jaune", "electronique", "verte"],
        "reponse": "electronique",
        "explication": "Les piles sont très polluantes : toujours en point de collecte D3E.",
    },
    {
        "question": "Le carton de votre colis Jumia ?",
        "options": ["bleue", "jaune", "verte", "marron"],
        "reponse": "jaune",
        "explication": "Les cartons de colis sont des emballages : poubelle jaune "
                       "(la bleue est réservée aux papiers graphiques).",
    },
    {
        "question": "Un film plastique d'emballage alimentaire ?",
        "options": ["jaune", "verte", "bleue", "marron"],
        "reponse": "marron",
        "explication": "Piège ! Les films plastiques souples ne se recyclent pas comme les "
                       "bouteilles : ils partent avec les résiduels.",
    },
]
