"""
scraper.py — Module de scraping Jumia (EcoSort-Search)
Étudiant A — Scraping & données Jumia

Responsabilités couvertes :
  - Conception du module de scraping (Requests/BeautifulSoup)
  - Recherche dynamique (mot-clé fourni par l'utilisateur)
  - Nettoyage et structuration des résultats (nom, image, prix, lien)
  - Gestion des erreurs (aucun résultat, page indisponible, timeout)

NOTE IMPORTANTE :
  Les sélecteurs CSS ci-dessous (`article.prd`, `div.info`, etc.) correspondent
  à la structure HTML observée sur jumia.ci au moment de l'écriture. Jumia
  modifie régulièrement son balisage : si le scraper renvoie une liste vide
  alors que la recherche existe bien sur le site, ouvre la page dans un
  navigateur, fais clic droit > Inspecter sur un produit, et ajuste les
  sélecteurs dans `_parse_product()`.
"""

from dataclasses import dataclass, asdict
from typing import List, Optional
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup


# --------------------------------------------------------------------------
# Exceptions personnalisées : permettent au code appelant (interface,
# tests, autre membre de l'équipe) de distinguer précisément le type d'échec.
# --------------------------------------------------------------------------
class ScraperError(Exception):
    """Erreur générique du scraper."""


class NoResultsError(ScraperError):
    """Levée quand la recherche ne retourne aucun produit sur Jumia."""


class PageUnavailableError(ScraperError):
    """Levée quand Jumia répond avec un statut HTTP d'erreur (403, 404, 500...)."""


class ScraperTimeoutError(ScraperError):
    """Levée quand la requête dépasse le délai imparti."""


# --------------------------------------------------------------------------
# Structure de données pour un résultat propre et typé
# --------------------------------------------------------------------------
@dataclass
class Produit:
    nom: str
    image: Optional[str]
    prix: Optional[str]
    lien: str

    def to_dict(self) -> dict:
        return asdict(self)


class JumiaScraper:
    BASE_URL = "https://www.jumia.ci/catalog/?q={query}"
    HEADERS = {
        # Un User-Agent réaliste réduit le risque d'être bloqué (403)
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }

    def __init__(self, timeout: int = 8):
        self.timeout = timeout

    def search(self, keyword: str, max_results: int = 5) -> List[Produit]:
        """
        Recherche `keyword` sur Jumia et renvoie une liste de Produit
        (3 à 5 résultats par défaut, bornée par max_results).

        Lève :
          - PageUnavailableError si la page ne répond pas correctement
          - ScraperTimeoutError si la requête expire
          - NoResultsError si aucun produit n'est trouvé
        """
        if not keyword or not keyword.strip():
            raise ValueError("Le mot-clé de recherche ne peut pas être vide.")

        url = self.BASE_URL.format(query=quote_plus(keyword.strip()))

        try:
            response = requests.get(url, headers=self.HEADERS, timeout=self.timeout)
        except requests.exceptions.Timeout as exc:
            raise ScraperTimeoutError(
                f"La requête vers Jumia a expiré après {self.timeout}s."
            ) from exc
        except requests.exceptions.RequestException as exc:
            raise PageUnavailableError(
                f"Impossible de joindre Jumia : {exc}"
            ) from exc

        if response.status_code != 200:
            raise PageUnavailableError(
                f"Jumia a répondu avec le statut {response.status_code}."
            )

        produits = self._parse_results(response.text)

        if not produits:
            raise NoResultsError(f"Aucun résultat trouvé pour « {keyword} ».")

        return produits[:max_results]

    # ----------------------------------------------------------------
    # Parsing
    # ----------------------------------------------------------------
    def _parse_results(self, html: str) -> List[Produit]:
        soup = BeautifulSoup(html, "html.parser")
        cards = soup.select("article.prd")  # carte produit Jumia
        produits = []
        for card in cards:
            produit = self._parse_product(card)
            if produit is not None:
                produits.append(produit)
        return produits

    def _parse_product(self, card) -> Optional[Produit]:
        """Extrait nom, image, prix, lien d'une carte produit.
        Renvoie None si les champs essentiels (nom + lien) sont introuvables,
        plutôt que de planter tout le scraping pour une seule carte malformée.
        """
        try:
            lien_tag = card.select_one("a.core")
            if lien_tag is None or not lien_tag.get("href"):
                return None
            lien = lien_tag["href"]
            if lien.startswith("/"):
                lien = "https://www.jumia.ci" + lien

            nom_tag = card.select_one("h3.name")
            nom = self._clean_text(nom_tag.get_text()) if nom_tag else None
            if not nom:
                return None

            prix_tag = card.select_one("div.prc")
            prix = self._clean_text(prix_tag.get_text()) if prix_tag else None

            img_tag = card.select_one("img.img")
            image = None
            if img_tag is not None:
                # Jumia charge parfois l'image en lazy-load : la vraie URL
                # peut être dans data-src plutôt que src
                image = img_tag.get("data-src") or img_tag.get("src")

            return Produit(nom=nom, image=image, prix=prix, lien=lien)

        except Exception:
            # Une carte imprévue ne doit pas interrompre tout le scraping
            return None

    @staticmethod
    def _clean_text(text: str) -> str:
        return " ".join(text.split()).strip()


if __name__ == "__main__":
    scraper = JumiaScraper()
    try:
        resultats = scraper.search("smartphone samsung", max_results=5)
        for p in resultats:
            print(p.to_dict())
    except ScraperError as e:
        print(f"Erreur : {e}")
