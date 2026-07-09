"""Composants visuels partagés de l'interface (CSS global, hero, cartes, footer).

Direction artistique : thème sombre premium, halos verts lumineux,
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

/* Fond général : halo vert très discret en haut de page */
.stApp {
    background-image:
        radial-gradient(ellipse 80% 40% at 50% 0%, rgba(76, 175, 80, 0.14), transparent 60%);
}

/* Largeur de lecture confortable malgré le layout wide */
div[data-testid="stMainBlockContainer"] { max-width: 1100px; }

/* --- Hero : panneau sombre avec halo lumineux, façon landing page --- */
.eco-hero {
    background:
        radial-gradient(ellipse 60% 80% at 25% 0%, rgba(76, 175, 80, 0.35), transparent 60%),
        linear-gradient(160deg, #16261B 0%, #0F1511 75%);
    border: 1px solid rgba(139, 195, 74, 0.22);
    color: #FFFFFF;
    padding: 2.8rem 2.4rem;
    border-radius: 20px;
    margin-bottom: 1.6rem;
    text-align: center;
}
.eco-hero h1 {
    color: #FFFFFF;
    margin: 0;
    font-weight: 800;
    font-size: 2.6rem;
    line-height: 1.15;
}
.eco-hero p { margin: 0.7rem 0 0 0; font-size: 1.1rem; color: #C8E6C9; }
.eco-highlight {
    background: #2E7D32;
    padding: 0 0.45rem;
    border-radius: 10px;
    box-shadow: 0 0 24px rgba(76, 175, 80, 0.55);
}
.eco-badge {
    display: inline-block;
    border: 1px solid rgba(139, 195, 74, 0.45);
    color: #A5D6A7;
    padding: 0.25rem 0.9rem;
    border-radius: 999px;
    font-size: 0.85rem;
    margin-bottom: 1rem;
}

/* --- Titres de section centrés avec sous-titre, façon vitrine --- */
.eco-section { text-align: center; margin: 2.2rem 0 1.2rem 0; }
.eco-section h2 {
    color: #FFFFFF;
    font-weight: 800;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    font-size: 1.45rem;
    margin: 0;
}
.eco-section p { color: #A5D6A7; margin: 0.3rem 0 0 0; font-size: 0.95rem; }

/* --- Cartes (conteneurs avec bordure) : sombres, halo vert au survol --- */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #18231B;
    border: 1px solid rgba(139, 195, 74, 0.18);
    border-radius: 18px;
    transition: box-shadow 0.25s ease, transform 0.25s ease, border-color 0.25s ease;
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    box-shadow: 0 0 28px rgba(76, 175, 80, 0.28);
    border-color: rgba(139, 195, 74, 0.5);
    transform: translateY(-4px);
}
/* Images des cartes : hauteur homogène sans déformation, coins doux */
div[data-testid="stVerticalBlockBorderWrapper"] img {
    height: 150px;
    object-fit: contain;
    border-radius: 12px;
    background: #FFFFFF;
}

.eco-prix { color: #8BC34A; font-weight: 700; font-size: 1.05rem; }

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
    box-shadow: 0 6px 22px rgba(0, 0, 0, 0.35);
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

/* --- Footer sombre en colonnes, façon site vitrine --- */
.eco-footer {
    background: #0B120D;
    border: 1px solid rgba(139, 195, 74, 0.15);
    border-radius: 20px;
    padding: 2rem 2.2rem 1rem 2.2rem;
    margin-top: 3rem;
}
.eco-footer-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
    gap: 1.4rem;
}
.eco-footer h4 { color: #8BC34A; margin: 0 0 0.5rem 0; font-size: 0.95rem; }
.eco-footer p, .eco-footer a, .eco-footer li {
    color: #C8E6C9;
    font-size: 0.85rem;
    text-decoration: none;
}
.eco-footer ul { list-style: none; padding: 0; margin: 0; }
.eco-footer li { margin-bottom: 0.35rem; }
.eco-footer a:hover { color: #FFFFFF; }
.eco-footer-bottom {
    text-align: center;
    color: #7CA982;
    font-size: 0.78rem;
    border-top: 1px solid rgba(139, 195, 74, 0.12);
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
    """Titre de section centré avec sous-titre, façon vitrine."""
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
    """Footer commun à toutes les pages (colonnes façon site vitrine)."""
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
