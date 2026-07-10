"""Composants visuels partagés de l'interface (CSS global, hero, cartes, navbar).

Direction artistique : sombre premium façon landing page « Velocity » —
fond noir chaud, halos orange incandescents, hero avec horizon lumineux,
sections centrées avec sous-titre, cartes arrondies, navbar horizontale
à boutons coulissants. Tout le CSS custom du projet vit ici pour garder
les vues lisibles.
"""

import streamlit as st

GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');

html, body, .stApp, [data-testid="stSidebar"] {
    font-family: 'Poppins', 'Segoe UI', sans-serif;
}

/* Fond général : halo ambré très discret en haut de page */
.stApp {
    background-image:
        radial-gradient(ellipse 80% 40% at 50% 0%, rgba(232, 114, 44, 0.14), transparent 60%);
}

/* Largeur de lecture confortable malgré le layout wide */
div[data-testid="stMainBlockContainer"] { max-width: 1100px; }

/* --- Hero : panneau noir chaud avec halo et horizon incandescent --- */
.eco-hero {
    background:
        radial-gradient(ellipse 70% 90% at 50% 115%, rgba(255, 140, 66, 0.5), transparent 60%),
        linear-gradient(160deg, #241710 0%, #140D08 70%);
    border: 1px solid rgba(255, 140, 66, 0.28);
    box-shadow: 0 30px 60px -30px rgba(255, 140, 66, 0.45);
    color: #F5EDE6;
    padding: 2.8rem 2.4rem;
    border-radius: 20px;
    margin-bottom: 1.6rem;
    text-align: center;
}
.eco-hero h1 {
    color: #F5EDE6;
    margin: 0;
    font-weight: 800;
    font-size: 2.6rem;
    line-height: 1.15;
}
.eco-hero p { margin: 0.7rem 0 0 0; font-size: 1.1rem; color: #E0BFA3; }
.eco-highlight {
    background: #E8722C;
    padding: 0 0.45rem;
    border-radius: 10px;
    box-shadow: 0 0 26px rgba(255, 140, 66, 0.65);
}
.eco-badge {
    display: inline-block;
    border: 1px solid rgba(255, 140, 66, 0.5);
    color: #F0C9A8;
    padding: 0.25rem 0.9rem;
    border-radius: 999px;
    font-size: 0.85rem;
    margin-bottom: 1rem;
}

/* --- Titres de section centrés avec sous-titre, façon landing page --- */
.eco-section { text-align: center; margin: 2.2rem 0 1.2rem 0; }
.eco-section h2 {
    color: #F5EDE6;
    font-weight: 800;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    font-size: 1.45rem;
    margin: 0;
}
.eco-section p { color: #C79A78; margin: 0.3rem 0 0 0; font-size: 0.95rem; }

/* --- Cartes (conteneurs avec bordure) : sombres, halo ambré au survol --- */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #1F1610;
    border: 1px solid rgba(255, 140, 66, 0.18);
    border-radius: 18px;
    transition: box-shadow 0.25s ease, transform 0.25s ease, border-color 0.25s ease;
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    box-shadow: 0 0 30px rgba(255, 140, 66, 0.3);
    border-color: rgba(255, 140, 66, 0.55);
    transform: translateY(-4px);
}
/* Images des cartes : hauteur homogène sans déformation, coins doux */
div[data-testid="stVerticalBlockBorderWrapper"] img {
    height: 150px;
    object-fit: contain;
    border-radius: 12px;
    background: #FFFFFF;
}

.eco-prix { color: #FFA45C; font-weight: 700; font-size: 1.05rem; }

.stButton button, .stFormSubmitButton button, .stDownloadButton button {
    border-radius: 12px;
}

/* --- Écran résultat : apparition animée --- */
@keyframes ecoPop {
    0%   { transform: scale(0.6); opacity: 0; }
    100% { transform: scale(1);   opacity: 1; }
}
.ecosort-result { text-align: center; padding: 1.6rem 1rem; animation: ecoPop 0.5s ease-out; }
.ecosort-result .eco-emoji { font-size: 4.5rem; line-height: 1; }

/* --- Cartes du guide du tri (couleurs officielles des poubelles) --- */
.eco-bin-card {
    border-radius: 18px;
    padding: 1.4rem;
    margin-bottom: 1rem;
    min-height: 210px;
    box-shadow: 0 8px 26px rgba(0, 0, 0, 0.45);
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

/* --- Navbar horizontale : boutons segmentés coulissants --- */
div[data-testid="stSegmentedControl"] {
    display: flex;
    justify-content: center;
    margin-bottom: 0.8rem;
}
div[data-testid="stSegmentedControl"] [data-testid="stButtonGroup"] {
    background: #1F1610;
    border: 1px solid rgba(255, 140, 66, 0.22);
    border-radius: 999px;
    padding: 0.25rem;
}
div[data-testid="stSegmentedControl"] button {
    border-radius: 999px !important;
    border: none !important;
    padding: 0.45rem 1.2rem;
    transition: background 0.3s ease, box-shadow 0.3s ease,
                color 0.3s ease, transform 0.3s ease;
}
div[data-testid="stSegmentedControl"] button:hover {
    transform: translateY(-1px);
    color: #FFA45C;
}
/* Bouton actif : pastille orange qui « glisse » d'un onglet à l'autre */
div[data-testid="stSegmentedControl"] button[data-testid$="Active"],
div[data-testid="stSegmentedControl"] button[aria-checked="true"] {
    background: linear-gradient(160deg, #FF8C42 0%, #E8722C 100%) !important;
    color: #1A0F08 !important;
    box-shadow: 0 0 18px rgba(255, 140, 66, 0.55);
    font-weight: 600;
}
</style>
"""


def inject_css() -> None:
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def hero(titre: str, sous_titre: str, badge: str | None = None) -> None:
    """Bandeau d'en-tête façon landing page. `titre` peut contenir un
    <span class='eco-highlight'>mot surligné</span>."""
    badge_html = f'<div><span class="eco-badge">{badge}</span></div>' if badge else ""
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


def section(titre: str, sous_titre: str = "") -> None:
    """Titre de section centré avec sous-titre, façon landing page."""
    sous_titre_html = f"<p>{sous_titre}</p>" if sous_titre else ""
    st.markdown(
        f'<div class="eco-section"><h2>{titre}</h2>{sous_titre_html}</div>',
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
