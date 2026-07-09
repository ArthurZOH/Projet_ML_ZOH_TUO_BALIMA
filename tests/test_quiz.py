"""Tests d'intégrité des questions du quiz (webapp/quiz_data.py)."""

from utils.categories import BINS
from webapp.quiz_data import QUESTIONS


def test_au_moins_six_questions():
    assert len(QUESTIONS) >= 6


def test_structure_des_questions():
    for q in QUESTIONS:
        assert q["question"].strip()
        assert q["explication"].strip()
        assert len(q["options"]) >= 2
        # Pas de doublon dans les options
        assert len(set(q["options"])) == len(q["options"])


def test_reponses_et_options_sont_des_poubelles_valides():
    for q in QUESTIONS:
        assert q["reponse"] in BINS
        for option in q["options"]:
            assert option in BINS
        # La bonne réponse doit figurer parmi les options proposées
        assert q["reponse"] in q["options"]
