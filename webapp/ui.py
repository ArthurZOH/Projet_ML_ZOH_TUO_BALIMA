"""Composants visuels partagés de l'interface (CSS global, hero, cartes, footer).

Direction artistique : sombre premium façon landing page « Velocity » —
fond noir chaud, halos orange incandescents, hero avec horizon lumineux,
sections centrées avec sous-titre, cartes arrondies, footer en colonnes.
Tout le CSS custom du projet vit ici pour garder les vues lisibles.
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

/* --- Footer noir chaud en colonnes, façon landing page --- */
.eco-footer {
    background: #0F0A06;
    border: 1px solid rgba(255, 140, 66, 0.2);
    border-radius: 20px;
    padding: 2rem 2.2rem 1rem 2.2rem;
    margin-top: 3rem;
}
.eco-footer-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
    gap: 1.4rem;
}
.eco-footer h4 { color: #FF8C42; margin: 0 0 0.5rem 0; font-size: 0.95rem; }
.eco-footer p, .eco-footer a, .eco-footer li {
    color: #E8CDB8;
    font-size: 0.85rem;
    text-decoration: none;
}
.eco-footer ul { list-style: none; padding: 0; margin: 0; }
.eco-footer li { margin-bottom: 0.35rem; }
.eco-footer a:hover { color: #FFFFFF; }
.eco-footer-bottom {
    text-align: center;
    color: #A87F5E;
    font-size: 0.78rem;
    border-top: 1px solid rgba(255, 140, 66, 0.15);
    margin-top: 1.4rem;
    padding-top: 0.9rem;
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


def footer() -> None:
    """Footer commun à toutes les pages (colonnes façon landing page)."""
    st.markdown(
        """
        <div class="eco-footer">
          <div class="eco-footer-grid">
            <div>
              <h4>♻️ EcoSort-Search</h4>
              <p>Le bon geste de tri pour chaque produit, propulsé par le
              Deep Learning et les données Jumia.</p>
            </div>
            <div>
              <h4>Navigation</h4>
              <ul>
                <li><a href="/" target="_self">🔍 Recherche & tri</a></li>
                <li><a href="/stats" target="_self">📊 Mes statistiques</a></li>
                <li><a href="/guide" target="_self">🗑️ Guide du tri</a></li>
                <li><a href="/quiz" target="_self">🧠 Quiz du tri</a></li>
                <li><a href="/a-propos" target="_self">ℹ️ À propos</a></li>
              </ul>
            </div>
            <div>
              <h4>Équipe</h4>
              <ul>
                <li>Alice — Scraping</li>
                <li>Arthur — Intelligence artificielle</li>
                <li>Yannel — Application & Docker</li>
              </ul>
            </div>
            <div>
              <h4>Projet</h4>
              <ul>
                <li><a href="https://github.com/ArthurZOH/Projet_ML_ZOH_TUO_BALIMA">Code source (GitHub)</a></li>
                <li>Dataset : Kaggle Garbage Classification</li>
                <li>CI : tests + build Docker</li>
              </ul>
            </div>
          </div>
          <div class="eco-footer-bottom">
            © 2026 EcoSort-Search — Projet pédagogique ISE2
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
