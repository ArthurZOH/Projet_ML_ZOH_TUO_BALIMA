"""Page À propos : le projet, le pipeline et l'équipe."""

import streamlit as st

from webapp import ui

EQUIPE = [
    ("👩🏾‍💻 Alice", "Lead Scraping", "Scraper Jumia, dataset Kaggle, page recherche"),
    ("👨🏾‍💻 Arthur", "Lead IA", "Modèle MobileNetV2, mapping classes → poubelles"),
    ("👨🏾‍💻 Yannel", "Lead App & Docker", "Interface Streamlit, Dockerfile, CI"),
]

TECHNOS = "`Python` `Streamlit` `TensorFlow / Keras` `BeautifulSoup` `Docker` `GitHub Actions`"


def render() -> None:
    ui.hero(
        "ℹ️ À propos d'EcoSort-Search",
        "Projet de groupe ISE2 — le tri sélectif assisté par le Deep Learning.",
    )

    st.markdown(
        """
        **EcoSort-Search** répond à une question du quotidien : *« dans quelle
        poubelle va ce produit ? »*. L'application cherche le produit sur
        **Jumia**, l'analyse avec un modèle de **Deep Learning** entraîné sur le
        dataset Kaggle *Garbage Classification*, puis affiche la poubelle
        correspondante parmi les 5 destinations de tri.
        """
    )

    st.subheader("⚙️ Le pipeline")
    st.markdown(
        """
        > 🔍 **Recherche** du produit &nbsp;→&nbsp; 🕷️ **Scraping Jumia**
        (nom, prix, image) &nbsp;→&nbsp; 🧠 **Classification CNN**
        (MobileNetV2, 6 matières) &nbsp;→&nbsp; ♻️ **Poubelle recommandée**
        (mapping 6 matières → 5 poubelles + détection D3E par mots-clés)
        """
    )

    st.subheader("👥 L'équipe")
    colonnes = st.columns(3)
    for col, (nom, role, taches) in zip(colonnes, EQUIPE):
        with col, st.container(border=True):
            st.markdown(f"### {nom}")
            st.markdown(f"**{role}**")
            st.caption(taches)

    st.subheader("🧰 Technologies")
    st.markdown(TECHNOS)
    st.caption(
        "Code source : github.com/ArthurZOH/Projet_ML_ZOH_TUO_BALIMA — "
        "CI : tests + build Docker à chaque push."
    )
