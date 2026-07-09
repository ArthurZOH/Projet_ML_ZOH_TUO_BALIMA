"""Composants visuels partagés de l'interface (CSS global, hero, cartes).

Tout le CSS custom du projet vit ici pour garder les vues lisibles.
"""

import streamlit as st

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');

html, body, .stApp, [data-testid="stSidebar"] {
    font-family: 'Poppins', 'Segoe UI', sans-serif;
}

/* Largeur de lecture confortable malgré le layout wide */
div[data-testid="stMainBlockContainer"] { max-width: 1100px; }

/* --- Hero (bandeau dégradé) --- */
.eco-hero {
    background: linear-gradient(135deg, #1B5E20 0%, #43A047 55%, #9CCC65 100%);
    color: #FFFFFF;
    padding: 2.2rem 2rem;
    border-radius: 18px;
    margin-bottom: 1.2rem;
}
.eco-hero h1 { color: #FFFFFF; margin: 0; font-weight: 800; }
.eco-hero p  { margin: 0.4rem 0 0 0; font-size: 1.1rem; opacity: 0.95; }
.eco-badge {
    display: inline-block;
    background: rgba(255, 255, 255, 0.18);
    padding: 0.25rem 0.8rem;
    border-radius: 999px;
    font-size: 0.85rem;
    margin-bottom: 0.6rem;
}

/* --- Cartes (conteneurs avec bordure) : coins ronds + survol --- */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 16px;
    background-color: #FFFFFF;
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    box-shadow: 0 8px 24px rgba(46, 125, 50, 0.18);
    transform: translateY(-3px);
}
/* Images des cartes : hauteur homogène sans déformation */
div[data-testid="stVerticalBlockBorderWrapper"] img {
    height: 150px;
    object-fit: contain;
}

.eco-prix { color: #2E7D32; font-weight: 700; font-size: 1.05rem; }

.stButton button { border-radius: 12px; }

/* --- Écran résultat : apparition animée --- */
@keyframes ecoPop {
    0%   { transform: scale(0.6); opacity: 0; }
    100% { transform: scale(1);   opacity: 1; }
}
.ecosort-result { text-align: center; padding: 1.6rem 1rem; animation: ecoPop 0.5s ease-out; }
.ecosort-result .eco-emoji { font-size: 4.5rem; line-height: 1; }

/* --- Cartes du guide du tri --- */
.eco-bin-card {
    border-radius: 16px;
    padding: 1.4rem;
    margin-bottom: 1rem;
    min-height: 210px;
}
.eco-bin-card h3 { margin: 0.3rem 0; color: inherit; }
.eco-bin-card .eco-emoji { font-size: 2.2rem; }
.eco-chip {
    display: inline-block;
    background: rgba(255, 255, 255, 0.25);
    border-radius: 999px;
    padding: 0.1rem 0.65rem;
    margin: 0.15rem 0.15rem 0 0;
    font-size: 0.8rem;
}
</style>
"""


def inject_css() -> None:
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def hero(titre: str, sous_titre: str, badge: str | None = None) -> None:
    """Bandeau d'en-tête dégradé, commun aux pages."""
    badge_html = f'<span class="eco-badge">{badge}</span><br>' if badge else ""
    st.markdown(
        f"""
        <div class="eco-hero">
            {badge_html}
            <h1>{titre}</h1>
            <p>{sous_titre}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def prix(texte: str) -> None:
    st.markdown(f"<span class='eco-prix'>{texte}</span>", unsafe_allow_html=True)


def carte_produit(product: dict, key: str) -> bool:
    """Carte produit cliquable. Renvoie True si l'utilisateur la choisit."""
    with st.container(border=True):
        st.image(product["image_url"], use_container_width=True)
        st.markdown(f"**{product['name']}**")
        prix(product["price"])
        return st.button("♻️ Trier ce produit", key=key, use_container_width=True)
