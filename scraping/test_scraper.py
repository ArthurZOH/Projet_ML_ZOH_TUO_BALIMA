"""
test_scraper.py — Tests unitaires du module de scraping Jumia
Étudiant A

On ne fait AUCUN vrai appel réseau : requests.get est simulé (mock) pour que
les tests soient rapides, reproductibles, et ne dépendent pas de l'état
actuel du site Jumia.

Lancer avec :  pytest test_scraper.py -v
"""

import requests
import pytest
from unittest.mock import patch, Mock

from scraper import (
    JumiaScraper,
    NoResultsError,
    PageUnavailableError,
    ScraperTimeoutError,
)


# --------------------------------------------------------------------------
# HTML factices imitant la structure attendue d'une page de résultats Jumia
# --------------------------------------------------------------------------
HTML_AVEC_RESULTATS = """
<html><body>
<article class="prd">
  <a class="core" href="/produit-1.html">
    <img class="img" data-src="https://img.jumia.ci/produit1.jpg" />
    <div class="info">
      <h3 class="name">Smartphone Samsung Galaxy A15</h3>
      <div class="prc">99 900 FCFA</div>
    </div>
  </a>
</article>
<article class="prd">
  <a class="core" href="/produit-2.html">
    <img class="img" src="https://img.jumia.ci/produit2.jpg" />
    <div class="info">
      <h3 class="name">Smartphone Samsung Galaxy A05</h3>
      <div class="prc">69 900 FCFA</div>
    </div>
  </a>
</article>
</body></html>
"""

HTML_SANS_RESULTATS = "<html><body><div class='no-results'>Aucun produit</div></body></html>"

HTML_CARTE_MALFORMEE = """
<html><body>
<article class="prd">
  <a class="core" href="/produit-1.html">
    <h3 class="name">Produit valide</h3>
    <div class="prc">1000 FCFA</div>
  </a>
</article>
<article class="prd">
  <!-- carte cassée : pas de lien ni de nom -->
  <div class="info">Rien d'exploitable ici</div>
</article>
</body></html>
"""


def _mock_response(status_code=200, text=""):
    mock_resp = Mock()
    mock_resp.status_code = status_code
    mock_resp.text = text
    return mock_resp


class TestSearchSuccess:
    @patch("scraper.requests.get")
    def test_renvoie_produits_bien_structures(self, mock_get):
        mock_get.return_value = _mock_response(200, HTML_AVEC_RESULTATS)
        scraper = JumiaScraper()

        resultats = scraper.search("samsung", max_results=5)

        assert len(resultats) == 2
        premier = resultats[0]
        assert premier.nom == "Smartphone Samsung Galaxy A15"
        assert premier.prix == "99 900 FCFA"
        assert premier.lien == "https://www.jumia.ci/produit-1.html"
        assert premier.image == "https://img.jumia.ci/produit1.jpg"

    @patch("scraper.requests.get")
    def test_respecte_max_results(self, mock_get):
        mock_get.return_value = _mock_response(200, HTML_AVEC_RESULTATS)
        scraper = JumiaScraper()

        resultats = scraper.search("samsung", max_results=1)

        assert len(resultats) == 1

    @patch("scraper.requests.get")
    def test_ignore_cartes_malformees_sans_planter(self, mock_get):
        mock_get.return_value = _mock_response(200, HTML_CARTE_MALFORMEE)
        scraper = JumiaScraper()

        resultats = scraper.search("test")

        # Une seule carte exploitable sur les deux
        assert len(resultats) == 1
        assert resultats[0].nom == "Produit valide"


class TestGestionErreurs:
    @patch("scraper.requests.get")
    def test_aucun_resultat_leve_no_results_error(self, mock_get):
        mock_get.return_value = _mock_response(200, HTML_SANS_RESULTATS)
        scraper = JumiaScraper()

        with pytest.raises(NoResultsError):
            scraper.search("produitquinexistepas12345")

    @patch("scraper.requests.get")
    def test_statut_http_erreur_leve_page_unavailable(self, mock_get):
        mock_get.return_value = _mock_response(503, "")
        scraper = JumiaScraper()

        with pytest.raises(PageUnavailableError):
            scraper.search("samsung")

    @patch("scraper.requests.get")
    def test_timeout_leve_scraper_timeout_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout()
        scraper = JumiaScraper()

        with pytest.raises(ScraperTimeoutError):
            scraper.search("samsung")

    @patch("scraper.requests.get")
    def test_erreur_connexion_leve_page_unavailable(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError()
        scraper = JumiaScraper()

        with pytest.raises(PageUnavailableError):
            scraper.search("samsung")

    def test_mot_cle_vide_leve_value_error(self):
        scraper = JumiaScraper()
        with pytest.raises(ValueError):
            scraper.search("   ")


class TestNettoyageTexte:
    def test_clean_text_supprime_espaces_multiples(self):
        assert JumiaScraper._clean_text("  Samsung   Galaxy \n A15 ") == "Samsung Galaxy A15"
