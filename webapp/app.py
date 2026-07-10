"""EcoSort-Search — point d'entrée Streamlit.

Navigation horizontale : une barre de boutons coulissants en haut de page
(st.segmented_control) route directement vers les 5 vues :
  - Recherche & tri : mot-clé -> Jumia -> matière -> poubelle colorée
  - Mes statistiques : éco-points, niveau, répartition par poubelle
  - Guide du tri / Quiz / À propos
La sidebar ne garde que les réglages (mode démo, nb résultats, historique).

Lancement local :  streamlit run webapp/app.py
"""

import sys
from pathlib import Path

import streamlit as st

# Permet d'importer utils/ et scraping/ quand on lance `streamlit run webapp/app.py`
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from webapp import ui  # noqa: E402
from webapp.views import apropos, dashboard, guide, quiz, recherche  # noqa: E402

st.set_page_config(
    page_title="EcoSort-Search",
    page_icon="♻️",
    layout="wide",
    menu_items={"about": "EcoSort-Search — projet ISE2 (Alice, Arthur, Yannel)"},
)

# Thème clair/sombre : persiste en session, basculé par le bouton de la navbar
theme = st.session_state.setdefault("theme", "light")
ui.inject_css(theme)

# Libellé de la navbar -> vue (l'ordre définit l'ordre des boutons)
VUES = {
    "🔍 Recherche": recherche.render,
    "📊 Statistiques": dashboard.render,
    "🗑️ Guide": guide.render,
    "🧠 Quiz": quiz.render,
    "ℹ️ À propos": apropos.render,
}
LABELS = list(VUES)

# --- Navbar horizontale (pilule flottante) + bouton de thème à droite.
# La clé de session fait persister l'onglet actif entre les reruns.
col_nav, col_theme = st.columns([11, 1], vertical_alignment="center")
with col_nav:
    choix = st.segmented_control(
        "Navigation",
        LABELS,
        default=LABELS[0],
        key="navbar",
        label_visibility="collapsed",
    )
with col_theme:
    if st.button(
        "🌙" if theme == "light" else "☀️",
        key="theme_btn",
        help="Changer le thème",
    ):
        st.session_state["theme"] = "dark" if theme == "light" else "light"
        st.rerun()

# --- Sidebar : marque + réglages + mini-historique ---
with st.sidebar:
    st.markdown("## ♻️ EcoSort-Search")
    st.caption("Le bon geste de tri, produit par produit.")
    st.divider()
    st.slider("Nombre de résultats Jumia", 3, 10, 5, key="max_results")
    st.toggle(
        "🧪 Mode démo (sans Jumia)",
        key="demo_mode",
        help="Produits factices, aucune requête réseau — pratique pour la démo.",
    )

    historique = st.session_state.get("history", [])
    if historique:
        st.divider()
        st.markdown("**🕘 Déjà triés**")
        from utils.categories import BINS  # import local : après le sys.path hack

        for entree in reversed(historique[-6:]):
            st.caption(f"{BINS[entree['bin_key']]['emoji']} {entree['name']}")

# `choix` vaut None si l'utilisateur désélectionne l'onglet actif :
# on retombe alors sur la première vue (Recherche).
VUES[choix or LABELS[0]]()
