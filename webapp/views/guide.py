"""Page Guide du tri : les 5 poubelles en cartes colorées + pièges classiques."""

import streamlit as st

from utils.categories import BINS
from webapp import ui

PIEGES = [
    ("Un verre à boire cassé", "Poubelle marron — la vaisselle n'est pas du verre d'emballage."),
    ("Un film plastique souple", "Poubelle marron — seuls les emballages rigides vont dans la jaune."),
    ("Un carton de pizza gras", "Poubelle marron — le carton souillé ne se recycle plus."),
    ("Une pile ou une batterie", "Jamais à la poubelle : point de collecte D3E obligatoire."),
    ("Un pot de yaourt", "Poubelle jaune — c'est un emballage ménager léger."),
]


def _carte_poubelle(bin_info: dict) -> None:
    chips = "".join(
        f"<span class='eco-chip'>{matiere}</span>" for matiere in bin_info["matieres"]
    ) or "<span class='eco-chip'>détection par mots-clés</span>"
    st.markdown(
        f"""
        <div class="eco-bin-card"
             style="background: {bin_info['color']}; color: {bin_info['text_color']};">
            <div class="eco-emoji">{bin_info['emoji']}</div>
            <h3>{bin_info['label']}</h3>
            <p>{bin_info['consigne']}</p>
            {chips}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render() -> None:
    ui.hero(
        "🗑️ Guide du tri",
        "Les 5 destinations possibles de vos déchets, et les pièges à éviter.",
    )

    cles = list(BINS)
    for ligne in range(0, len(cles), 2):
        colonnes = st.columns(2)
        for col, cle in zip(colonnes, cles[ligne:ligne + 2]):
            with col:
                _carte_poubelle(BINS[cle])

    ui.section("⚠️ Les pièges classiques", "Les erreurs les plus fréquentes — le quiz vous les fera réviser !")
    for titre, reponse in PIEGES:
        with st.expander(titre):
            st.write(reponse)
