
"""EcoSort-Search — point d'entrée Streamlit.

Page de garde (connexion requise), puis navigation horizontale : une barre
de boutons coulissants en haut de page (st.segmented_control) route
directement vers les 3 vues :
  - Recherche & tri : mot-clé -> Jumia -> matière -> poubelle colorée
  - Mes statistiques : éco-points, niveau, répartition par poubelle
  - Guide du tri
La sidebar garde les réglages (nb résultats, historique, déconnexion).

Lancement local :  streamlit run webapp/app.py
"""

import sys
from pathlib import Path

import streamlit as st

# Permet d'importer utils/ et scraping/ quand on lance `streamlit run webapp/app.py`
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from webapp import ui  # noqa: E402
from webapp.views import dashboard, guide, login, recherche  # noqa: E402

st.set_page_config(
    page_title="EcoSort-Search",
    page_icon="♻️",
    layout="wide",
    menu_items={"about": "EcoSort-Search )"},
)

# Thème clair/sombre : persiste en session, basculé par le bouton de la navbar
theme = st.session_state.setdefault("theme", "dark")
ui.inject_css(theme)

# --- Page de garde : rien n'est accessible sans connexion ---
if not st.session_state.get("utilisateur"):
    login.render()
    st.stop()

# Libellé de la navbar -> vue (l'ordre définit l'ordre des boutons)
VUES = {
    "🛒 Recherche": recherche.render,
    "🏆 Statistiques": dashboard.render,
    "♻️ Guide": guide.render,
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

# --- Sidebar : marque + session + réglages + mini-historique ---
with st.sidebar:
    st.markdown("## ♻️ EcoSort-Search")
    st.caption(f"Connecté : **{st.session_state['utilisateur'].capitalize()}**")
    if st.button("Se déconnecter", use_container_width=True):
        st.session_state.pop("utilisateur", None)
        st.rerun()

    st.divider()
    st.slider("Nombre de résultats Jumia", 3, 10, 5, key="max_results")

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
