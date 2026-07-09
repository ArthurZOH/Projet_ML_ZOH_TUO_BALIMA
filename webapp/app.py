"""EcoSort-Search — interface Streamlit.

Flux : saisie d'un produit -> résultats Jumia (scraper Étudiant A)
-> sélection -> prédiction de la matière (mock) -> écran coloré
selon la poubelle correspondante.

Lancement local :  streamlit run webapp/app.py
"""

import sys
from pathlib import Path

import streamlit as st

# Permet d'importer utils/ et scraping/ quand on lance `streamlit run webapp/app.py`
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scraping.scraper import (  # noqa: E402
    JumiaScraper,
    NoResultsError,
    PageUnavailableError,
    ScraperError,
    ScraperTimeoutError,
)
from utils.categories import BINS, CLASS_TO_BIN  # noqa: E402
from utils.electronique import detect_electronique  # noqa: E402
from webapp.mocks import mock_predict  # noqa: E402

IMAGE_PLACEHOLDER = "https://placehold.co/200x200?text=Image"

st.set_page_config(
    page_title="EcoSort-Search",
    page_icon="♻️",
    layout="centered",
    menu_items={"about": "EcoSort-Search — projet ISE2 (Alice, Arthur, Yannel)"},
)

# CSS global : cartes produits, prix, en-tête. Le fond coloré de l'écran
# résultat est injecté séparément par show_bin().
GLOBAL_CSS = """
<style>
.ecosort-hero h1 { margin-bottom: 0; }
.ecosort-hero p  { color: #558B2F; font-size: 1.05rem; margin-top: 0.2rem; }
.ecosort-prix    { color: #2E7D32; font-weight: 700; }
.ecosort-result  { text-align: center; padding: 2rem 1rem; }
div[data-testid="stVerticalBlockBorderWrapper"] { background-color: #FFFFFF; }
</style>
"""


def show_sidebar() -> int:
    """Barre latérale : réglages, guide du tri, historique de la session.
    Renvoie le nombre de résultats souhaité pour la recherche."""
    with st.sidebar:
        st.markdown("## ♻️ EcoSort-Search")
        st.caption("Le bon geste de tri, produit par produit.")

        max_results = st.slider("Nombre de résultats Jumia", 3, 10, 5)

        st.divider()
        st.markdown("### 🗑️ Guide du tri")
        for bin_info in BINS.values():
            with st.expander(f"{bin_info['emoji']} {bin_info['label']}"):
                st.write(bin_info["consigne"])

        historique = st.session_state.get("history", [])
        if historique:
            st.divider()
            st.markdown("### 🕘 Déjà triés")
            for entree in reversed(historique[-8:]):
                emoji = BINS[entree["bin_key"]]["emoji"]
                st.caption(f"{emoji} {entree['name']}")

    return max_results


def show_bin(bin_key: str, product: dict, predicted_class: str | None) -> None:
    """Colore l'écran aux couleurs de la poubelle et affiche la consigne."""
    bin_info = BINS[bin_key]
    st.markdown(
        f"""
        <style>
        .stApp {{ background-color: {bin_info["color"]}; }}
        .ecosort-result {{ color: {bin_info["text_color"]}; }}
        </style>
        <div class="ecosort-result">
            <h1>{bin_info["emoji"]} {bin_info["label"]}</h1>
            <p style="font-size: 1.2rem;">{bin_info["consigne"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Récapitulatif du produit analysé, sur fond blanc pour rester lisible
    with st.container(border=True):
        col_img, col_info = st.columns([1, 3])
        with col_img:
            st.image(product["image_url"], width=90)
        with col_info:
            st.markdown(f"**{product['name']}**")
            st.markdown(
                f"<span class='ecosort-prix'>{product['price']}</span>",
                unsafe_allow_html=True,
            )
            if predicted_class is not None:
                st.caption(f"Matière détectée : {predicted_class} (modèle de démonstration)")
            else:
                st.caption("Détecté comme appareil électronique (D3E)")
            st.markdown(f"[Voir le produit sur Jumia ↗]({product['url']})")

    if st.button("🔄 Nouvelle recherche", use_container_width=True):
        # On ne vide pas toute la session : l'historique et les derniers
        # résultats de recherche doivent survivre au retour en arrière.
        st.session_state.pop("selected_product", None)
        st.session_state.pop("history_recorded", None)
        st.rerun()


@st.cache_data(ttl=600, show_spinner=False)
def search_jumia(keyword: str, max_results: int) -> list[dict]:
    """Recherche sur Jumia via le scraper (Étudiant A) et adapte les
    champs (nom/prix/image/lien) au format attendu par l'interface.

    Le cache (10 min) évite de re-scraper Jumia à chaque interaction
    Streamlit (chaque clic relance le script en entier).
    """
    produits = JumiaScraper().search(keyword, max_results=max_results)
    return [
        {
            "name": p.nom,
            "price": p.prix or "Prix non disponible",
            "image_url": p.image or IMAGE_PLACEHOLDER,
            "url": p.lien,
        }
        for p in produits
    ]


def show_results(results: list[dict]) -> None:
    """Grille de cartes produits (2 colonnes)."""
    for ligne in range(0, len(results), 2):
        colonnes = st.columns(2)
        for col, (i, product) in zip(
            colonnes, enumerate(results[ligne:ligne + 2], start=ligne)
        ):
            with col, st.container(border=True):
                st.image(product["image_url"], use_container_width=True)
                st.markdown(f"**{product['name']}**")
                st.markdown(
                    f"<span class='ecosort-prix'>{product['price']}</span>",
                    unsafe_allow_html=True,
                )
                if st.button("♻️ Trier ce produit", key=f"choose_{i}",
                             use_container_width=True):
                    st.session_state["selected_product"] = product
                    st.rerun()


def main() -> None:
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    max_results = show_sidebar()

    selected = st.session_state.get("selected_product")

    # --- Écran résultat : produit choisi -> poubelle colorée ---
    if selected is not None:
        if detect_electronique(selected["name"]):
            bin_key, predicted_class = "electronique", None
        else:
            predicted_class = mock_predict(selected)  # TODO: modèle réel (Étudiant B)
            bin_key = CLASS_TO_BIN.get(predicted_class, "marron")

        # Enregistre le tri une seule fois (pas à chaque rerun de l'écran)
        if not st.session_state.get("history_recorded"):
            st.session_state.setdefault("history", []).append(
                {"name": selected["name"], "bin_key": bin_key}
            )
            st.session_state["history_recorded"] = True

        show_bin(bin_key, selected, predicted_class)
        return

    # --- Écran recherche : mot-clé -> résultats Jumia ---
    st.markdown(
        """
        <div class="ecosort-hero">
            <h1>♻️ EcoSort-Search</h1>
            <p>Cherchez un produit, on vous dit dans quelle poubelle le jeter.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("recherche", border=False):
        col_champ, col_bouton = st.columns([4, 1], vertical_alignment="bottom")
        with col_champ:
            keyword = st.text_input(
                "Quel produit voulez-vous jeter ?",
                placeholder="Ex. : bouteille d'eau",
            )
        with col_bouton:
            submitted = st.form_submit_button("🔍", use_container_width=True)

    if submitted and keyword.strip():
        st.session_state["last_search"] = keyword.strip()

    last_search = st.session_state.get("last_search")
    if not last_search:
        st.info("Saisissez un nom de produit pour lancer la recherche sur Jumia.")
        return

    with st.spinner(f"Recherche de « {last_search} » sur Jumia…"):
        try:
            results = search_jumia(last_search, max_results)
        except NoResultsError:
            st.warning(f"Aucun résultat trouvé pour « {last_search} ». Essayez un autre mot-clé.")
            return
        except ScraperTimeoutError:
            st.error("Jumia met trop de temps à répondre. Réessayez dans un instant.")
            return
        except (PageUnavailableError, ScraperError):
            st.error("Jumia est indisponible pour le moment. Réessayez plus tard.")
            return

    st.subheader(f"Résultats pour « {last_search} »")
    show_results(results)


main()
