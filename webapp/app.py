"""EcoSort-Search — interface Streamlit (squelette).

Flux : saisie d'un produit -> résultats Jumia (mock pour l'instant)
-> sélection -> prédiction de la matière (mock) -> écran coloré
selon la poubelle correspondante.

Lancement local :  streamlit run webapp/app.py
"""

import sys
from pathlib import Path

import streamlit as st

# Permet d'importer utils/ quand on lance `streamlit run webapp/app.py`
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.categories import BINS, CLASS_TO_BIN  # noqa: E402
from webapp.mocks import mock_predict, mock_search  # noqa: E402

st.set_page_config(page_title="EcoSort-Search", page_icon="♻️", layout="centered")


def detect_electronique(product_name: str) -> bool:
    """Détection D3E par mots-clés sur le titre produit (v0 simple).

    La version affinée (liste complète, accents, pluriels) est prévue
    avec l'Étudiant B lors du mapping des catégories.
    """
    keywords = [
        "bluetooth", "écouteur", "ecouteur", "casque", "chargeur", "câble",
        "cable", "usb", "smartphone", "téléphone", "telephone", "tablette",
        "batterie", "pile", "montre", "mixeur", "blender", "télécommande",
        "telecommande", "lampe", "led", "électrique", "electrique", "electronique",
    ]
    name = product_name.lower()
    return any(kw in name for kw in keywords)


def show_bin(bin_key: str) -> None:
    """Colore l'écran aux couleurs de la poubelle et affiche la consigne."""
    bin_info = BINS[bin_key]
    st.markdown(
        f"""
        <style>
        .stApp {{ background-color: {bin_info["color"]}; }}
        .ecosort-result {{
            color: {bin_info["text_color"]};
            text-align: center;
            padding: 2rem 1rem;
        }}
        </style>
        <div class="ecosort-result">
            <h1>{bin_info["emoji"]} {bin_info["label"]}</h1>
            <p style="font-size: 1.2rem;">{bin_info["consigne"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("🔄 Nouvelle recherche"):
        st.session_state.clear()
        st.rerun()


def main() -> None:
    st.title("♻️ EcoSort-Search")
    st.caption("Trouvez la bonne poubelle pour n'importe quel produit.")

    selected = st.session_state.get("selected_product")

    # --- Écran résultat : produit choisi -> poubelle colorée ---
    if selected is not None:
        if detect_electronique(selected["name"]):
            bin_key = "electronique"
        else:
            predicted_class = mock_predict(selected)  # TODO: modèle réel (Étudiant B)
            bin_key = CLASS_TO_BIN.get(predicted_class, "marron")
        st.subheader(selected["name"])
        show_bin(bin_key)
        return

    # --- Écran recherche : mot-clé -> résultats Jumia ---
    keyword = st.text_input("Quel produit voulez-vous jeter ?", placeholder="Ex. : bouteille d'eau")
    if not keyword:
        st.info("Saisissez un nom de produit pour lancer la recherche sur Jumia.")
        return

    results = mock_search(keyword)  # TODO: scraper réel (Étudiant A)
    if not results:
        st.warning("Aucun résultat trouvé. Essayez un autre mot-clé.")
        return

    st.subheader(f"Résultats pour « {keyword} »")
    for i, product in enumerate(results):
        col_img, col_info, col_btn = st.columns([1, 3, 1])
        with col_img:
            st.image(product["image_url"], width=80)
        with col_info:
            st.markdown(f"**{product['name']}**")
            st.caption(product["price"])
        with col_btn:
            if st.button("Choisir", key=f"choose_{i}"):
                st.session_state["selected_product"] = product
                st.rerun()


main()
