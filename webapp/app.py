"""EcoSort-Search — point d'entrée Streamlit.

Navigation latérale multi-pages (st.navigation) :
  - Recherche & tri : mot-clé -> Jumia -> matière -> poubelle colorée
  - Mes statistiques : éco-points, niveau, répartition par poubelle
  - Guide du tri / Quiz / À propos

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

ui.inject_css()

pages = st.navigation(
    {
        "Application": [
            st.Page(recherche.render, title="Recherche & tri", icon="🔍", default=True),
            st.Page(dashboard.render, title="Mes statistiques", icon="📊", url_path="stats"),
        ],
        "Découvrir": [
            st.Page(guide.render, title="Guide du tri", icon="🗑️", url_path="guide"),
            st.Page(quiz.render, title="Quiz du tri", icon="🧠", url_path="quiz"),
            st.Page(apropos.render, title="À propos", icon="ℹ️", url_path="a-propos"),
        ],
    }
)

# Réglages et mini-historique, sous le menu de navigation
with st.sidebar:
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

pages.run()
