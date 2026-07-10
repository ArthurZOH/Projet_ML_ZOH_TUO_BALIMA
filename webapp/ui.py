"""Composants visuels partagés de l'interface (CSS global, hero, cartes, navbar).

Design system repris du projet « suivi-ventes » (Flask), recoloré façon
« Velocity » : noir chaud + orange incandescent (le clair est sa déclinaison
crème/ambre), deux thèmes via variables CSS, navbar flottante en pilule avec
lien actif souligné, hero à horizon lumineux, fond en dégradés radiaux,
formes flottantes animées, cartes 18px qui s'embrasent au survol, DM Sans.
Tout le CSS custom du projet vit ici pour garder les vues lisibles.
"""

import streamlit as st

# Variables CSS par thème — structure suivi-ventes, couleurs « Velocity »
# (noir chaud + orange incandescent ; le clair est sa déclinaison crème/ambre)
PALETTES = {
    "dark": {
        "bg-main": "#140D08",
        "bg-card": "#1F1610",
        "bg-elevated": "#0F0A06",
        "input-bg": "#241710",
        "border": "rgba(255,140,66,0.28)",
        "border-light": "rgba(255,140,66,0.18)",
        "text-primary": "#F5EDE6",
        "text-secondary": "#E0BFA3",
        "text-muted": "#A87F5E",
        "accent": "#FF8C42",
        "accent-light": "#FFA45C",
        "accent-bg": "rgba(255,140,66,0.12)",
        "accent-hover": "rgba(255,140,66,0.22)",
        "navbar-bg": "rgba(31,22,16,0.92)",
        "navbar-shadow": "rgba(0,0,0,0.35)",
        "card-shadow": "rgba(0,0,0,0.35)",
        "card-glow": "rgba(255,140,66,0.30)",
        "hero-glow": "rgba(255,140,66,0.45)",
        "gradient-start": "rgba(232,114,44,0.14)",
        "gradient-end": "rgba(255,140,66,0.05)",
        "float-color": "rgba(255,140,66,0.04)",
    },
    "light": {
        "bg-main": "#FAF3EC",
        "bg-card": "#F4E8DC",
        "bg-elevated": "#FFFFFF",
        "input-bg": "#FFFFFF",
        "border": "rgba(120,70,30,0.25)",
        "border-light": "rgba(120,70,30,0.15)",
        "text-primary": "#2E2018",
        "text-secondary": "#6B5340",
        "text-muted": "#9A8471",
        "accent": "#E8722C",
        "accent-light": "#FF8C42",
        "accent-bg": "rgba(232,114,44,0.10)",
        "accent-hover": "rgba(232,114,44,0.18)",
        "navbar-bg": "rgba(255,255,255,0.95)",
        "navbar-shadow": "rgba(46,32,24,0.08)",
        "card-shadow": "rgba(46,32,24,0.10)",
        "card-glow": "rgba(232,114,44,0.28)",
        "hero-glow": "rgba(232,114,44,0.30)",
        "gradient-start": "rgba(232,114,44,0.10)",
        "gradient-end": "rgba(255,140,66,0.05)",
        "float-color": "rgba(232,114,44,0.05)",
    },
}

# CSS statique : ne référence que les variables --xxx injectées par thème
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700;9..40,800&display=swap');

html, body, .stApp, [data-testid="stSidebar"] {
    font-family: 'DM Sans', 'Segoe UI', sans-serif;
    letter-spacing: -0.02em;
}

/* --- Fond : couleur du thème + double dégradé radial violet --- */
.stApp {
    background-color: var(--bg-main);
    background-image:
        radial-gradient(ellipse 80% 60% at 10% 10%, var(--gradient-start) 0%, transparent 50%),
        radial-gradient(ellipse 60% 70% at 90% 90%, var(--gradient-end) 0%, transparent 50%);
    background-attachment: fixed;
    transition: background-color 0.3s;
}

/* Largeur de lecture confortable malgré le layout wide */
div[data-testid="stMainBlockContainer"] { max-width: 1100px; }

/* --- Couleurs de texte pilotées par le thème --- */
.stApp h1, .stApp h2, .stApp h3, .stApp h4 { color: var(--text-primary); }
div[data-testid="stMarkdownContainer"], div[data-testid="stMarkdownContainer"] p,
div[data-testid="stMarkdownContainer"] li, div[data-testid="stMarkdownContainer"] span {
    color: var(--text-primary);
}
div[data-testid="stCaptionContainer"], div[data-testid="stCaptionContainer"] p {
    color: var(--text-muted) !important;
}
div[data-testid="stWidgetLabel"] p { color: var(--text-secondary) !important; }
[data-testid="stMetricValue"] { color: var(--text-primary); }
[data-testid="stMetricLabel"] p { color: var(--text-secondary) !important; }

/* --- Sidebar --- */
[data-testid="stSidebar"] {
    background: var(--bg-elevated);
    border-right: 1px solid var(--border-light);
    transition: background-color 0.3s;
}
[data-testid="stSidebar"] h2 { color: var(--text-primary); }

/* --- Alertes (info/succès/erreur) : habillage neutre du thème --- */
div[data-testid="stAlert"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
}
div[data-testid="stAlert"] * { color: var(--text-primary) !important; }

/* --- Champs de saisie --- */
div[data-baseweb="input"] {
    background: var(--input-bg);
    border-color: var(--border);
}
div[data-baseweb="input"] input { color: var(--text-primary); }

/* --- Expanders --- */
[data-testid="stExpander"] details {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: 12px;
}
[data-testid="stExpander"] summary span { color: var(--text-primary); }

/* --- Navbar flottante en pilule (segmented control) --- */
@keyframes slideDown {
    from { transform: translateY(-24px); opacity: 0; }
    to   { transform: translateY(0);     opacity: 1; }
}
div[data-testid="stSegmentedControl"] {
    display: flex;
    justify-content: center;
    animation: slideDown 0.5s ease-out;
}
div[data-testid="stSegmentedControl"] [data-testid="stButtonGroup"] {
    background: var(--navbar-bg);
    backdrop-filter: blur(20px);
    border: 1px solid var(--border-light);
    border-radius: 60px;
    box-shadow: 0 2px 20px var(--navbar-shadow);
    padding: 6px 8px;
}
div[data-testid="stSegmentedControl"] button {
    border-radius: 40px !important;
    border: none !important;
    background: transparent;
    color: var(--text-secondary);
    font-weight: 500;
    padding: 0.5rem 1.1rem;
    position: relative;
    transition: all 0.25s;
}
div[data-testid="stSegmentedControl"] button:hover {
    background: var(--accent-bg);
    color: var(--accent);
    transform: translateY(-1px);
}
/* Onglet actif : fond accent + petit soulignement, comme .nav-link.active */
div[data-testid="stSegmentedControl"] button[data-testid$="Active"],
div[data-testid="stSegmentedControl"] button[aria-checked="true"] {
    background: var(--accent-bg) !important;
    color: var(--accent) !important;
    font-weight: 600;
}
div[data-testid="stSegmentedControl"] button[data-testid$="Active"]::after,
div[data-testid="stSegmentedControl"] button[aria-checked="true"]::after {
    content: '';
    position: absolute;
    bottom: 3px; left: 50%;
    transform: translateX(-50%);
    width: 16px; height: 3px;
    border-radius: 2px;
    background: var(--accent);
}

/* --- Bouton de bascule de thème (rond, rotation au survol) --- */
.st-key-theme_btn button {
    width: 40px; height: 40px;
    border-radius: 50% !important;
    border: none !important;
    background: var(--accent-bg);
    color: var(--text-primary);
    transition: all 0.25s;
}
.st-key-theme_btn button:hover {
    background: var(--accent-hover);
    transform: scale(1.12) rotate(15deg);
}

/* --- Hero --- */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
.eco-hero {
    background:
        radial-gradient(ellipse 70% 90% at 50% 115%, var(--hero-glow) 0%, transparent 60%),
        var(--bg-card);
    border: 1px solid var(--border);
    box-shadow: 0 30px 60px -30px var(--hero-glow);
    color: var(--text-primary);
    padding: 2.6rem 2.4rem;
    border-radius: 20px;
    margin-bottom: 1.4rem;
    text-align: center;
    animation: fadeInUp 0.5s ease-out;
}
.eco-hero h1 {
    color: var(--text-primary);
    margin: 0;
    font-weight: 800;
    font-size: 2.5rem;
    line-height: 1.15;
    letter-spacing: -0.5px;
}
.eco-hero p { margin: 0.7rem 0 0 0; font-size: 1.08rem; color: var(--text-secondary); }
.eco-highlight {
    background: linear-gradient(135deg, #FF8C42, #E8722C);
    color: #1A0F08;
    padding: 0 0.45rem;
    border-radius: 10px;
    box-shadow: 0 0 26px rgba(255, 140, 66, 0.65);
}
.eco-badge {
    display: inline-block;
    background: var(--accent-bg);
    color: var(--accent);
    padding: 0.25rem 0.9rem;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 500;
    margin-bottom: 1rem;
}

/* --- Titres de section centrés avec sous-titre --- */
.eco-section { text-align: center; margin: 2.2rem 0 1.2rem 0; }
.eco-section h2 {
    color: var(--text-primary);
    font-weight: 800;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    font-size: 1.4rem;
    margin: 0;
}
.eco-section p { color: var(--text-muted); margin: 0.3rem 0 0 0; font-size: 0.95rem; }

/* --- Cartes (conteneurs avec bordure) : élévation au survol --- */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: 18px;
    box-shadow: 0 1px 4px var(--card-shadow);
    transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    box-shadow: 0 0 28px var(--card-glow);
    border-color: var(--accent);
    transform: translateY(-4px);
}
/* Images des cartes : hauteur homogène sans déformation, coins doux */
div[data-testid="stVerticalBlockBorderWrapper"] img {
    height: 150px;
    object-fit: contain;
    border-radius: 12px;
    background: #FFFFFF;
}

.eco-prix { color: var(--accent); font-weight: 700; font-size: 1.05rem; }

.stButton button, .stFormSubmitButton button, .stDownloadButton button {
    border-radius: 40px;
    transition: all 0.25s;
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
    box-shadow: 0 6px 22px var(--card-shadow);
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

/* --- Formes flottantes décoratives (très discrètes) --- */
@keyframes floatUp {
    0%   { transform: translateY(100vh) rotate(0deg);   opacity: 0; }
    10%  { opacity: 1; }
    90%  { opacity: 1; }
    100% { transform: translateY(-10vh) rotate(360deg); opacity: 0; }
}
.floating-shapes { position: fixed; inset: 0; z-index: 0; pointer-events: none; overflow: hidden; }
.floating-shapes .shape {
    position: absolute;
    border-radius: 50%;
    background: var(--float-color);
    animation: floatUp linear infinite;
}
.floating-shapes .shape:nth-child(1) { width: 60px; height: 60px; left: 10%; animation-duration: 18s; }
.floating-shapes .shape:nth-child(2) { width: 30px; height: 30px; left: 25%; animation-duration: 22s; animation-delay: 3s; }
.floating-shapes .shape:nth-child(3) { width: 80px; height: 80px; left: 45%; animation-duration: 25s; animation-delay: 6s; border-radius: 20%; }
.floating-shapes .shape:nth-child(4) { width: 40px; height: 40px; left: 65%; animation-duration: 20s; animation-delay: 2s; }
.floating-shapes .shape:nth-child(5) { width: 50px; height: 50px; left: 80%; animation-duration: 28s; animation-delay: 5s; border-radius: 30%; }
.floating-shapes .shape:nth-child(6) { width: 25px; height: 25px; left: 90%; animation-duration: 16s; animation-delay: 8s; }
</style>
"""

SHAPES_HTML = (
    '<div class="floating-shapes">'
    + '<div class="shape"></div>' * 6
    + "</div>"
)


def inject_css(theme: str = "light") -> None:
    """Injecte les variables du thème choisi puis le CSS global."""
    palette = PALETTES.get(theme, PALETTES["light"])
    variables = "".join(f"--{nom}: {valeur};" for nom, valeur in palette.items())
    st.markdown(f"<style>:root {{ {variables} }}</style>", unsafe_allow_html=True)
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    st.markdown(SHAPES_HTML, unsafe_allow_html=True)


def hero(titre: str, sous_titre: str, badge: str | None = None) -> None:
    """Bandeau d'en-tête. `titre` peut contenir un
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
    """Titre de section centré avec sous-titre."""
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
