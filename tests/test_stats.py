"""Tests des calculs du tableau de bord (webapp/stats.py)."""

from webapp.stats import POINTS_PAR_TRI, SEUILS_NIVEAUX, calculer_niveau, compter_par_poubelle


def test_compter_par_poubelle():
    history = [
        {"name": "Bouteille", "bin_key": "jaune"},
        {"name": "Canette", "bin_key": "jaune"},
        {"name": "Bocal", "bin_key": "verte"},
    ]
    compteur = compter_par_poubelle(history)
    assert compteur["jaune"] == 2
    assert compteur["verte"] == 1
    assert compteur["marron"] == 0


def test_niveau_debutant_a_zero_tri():
    niveau = calculer_niveau(0)
    assert niveau["label"] == SEUILS_NIVEAUX[0][1]
    assert niveau["points"] == 0
    assert niveau["progression"] == 0.0


def test_points_proportionnels_aux_tris():
    assert calculer_niveau(4)["points"] == 4 * POINTS_PAR_TRI


def test_changement_de_niveau_au_seuil():
    seuil, label = SEUILS_NIVEAUX[1]
    assert calculer_niveau(seuil - 1)["label"] == SEUILS_NIVEAUX[0][1]
    assert calculer_niveau(seuil)["label"] == label


def test_niveau_maximum():
    dernier_seuil, dernier_label = SEUILS_NIVEAUX[-1]
    niveau = calculer_niveau(dernier_seuil + 5)
    assert niveau["label"] == dernier_label
    assert niveau["seuil_suivant"] is None
    assert niveau["progression"] == 1.0


def test_progression_toujours_entre_0_et_1():
    for nb in range(0, 15):
        assert 0.0 <= calculer_niveau(nb)["progression"] <= 1.0
