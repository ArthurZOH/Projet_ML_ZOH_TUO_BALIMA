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
/* NB : dans Streamlit 1.46, le segmented control est rendu comme un
   stButtonGroup (comme les pills) ; on le cible via :has() sur le kind
   de ses boutons pour ne pas toucher aux pills de suggestions. */
div[data-testid="stButtonGroup"]:has(button[data-testid^="stBaseButton-segmented_control"]) {
    background: var(--navbar-bg) !important;
    backdrop-filter: blur(20px);
    border: none !important;
    border-radius: 60px;
    box-shadow: 0 2px 20px var(--navbar-shadow);
    padding: 6px 8px;
    gap: 4px;
    justify-content: center;
    animation: slideDown 0.5s ease-out;
}
button[data-testid="stBaseButton-segmented_control"],
button[data-testid="stBaseButton-segmented_controlActive"] {
    border-radius: 40px !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    background: transparent !important;
    color: var(--text-secondary) !important;
    font-weight: 500;
    padding: 0.5rem 1.1rem;
    transition: all 0.25s;
}
/* Les libellés héritent toujours de la couleur du bouton (lisibles en clair) */
button[data-testid^="stBaseButton-segmented_control"] * { color: inherit !important; }
button[data-testid="stBaseButton-segmented_control"]:hover {
    background: var(--accent-bg) !important;
    color: var(--accent) !important;
    transform: translateY(-1px);
}
/* Onglet actif : simple teinte accentuée, sans bordure ni soulignement */
button[data-testid="stBaseButton-segmented_controlActive"] {
    background: var(--accent-bg) !important;
    color: var(--accent) !important;
    font-weight: 600;
}

/* --- Boutons (secondaires, submit, download) : suivent le thème actif.
   Nécessaire car le thème Streamlit du config.toml est figé en sombre,
   alors que le mode clair est appliqué par variables CSS. --- */
button[data-testid="stBaseButton-secondary"],
button[data-testid="stBaseButton-secondaryFormSubmit"] {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-light) !important;
}
button[data-testid="stBaseButton-secondary"]:hover,
button[data-testid="stBaseButton-secondaryFormSubmit"]:hover {
    background: var(--accent-bg) !important;
    color: var(--accent) !important;
    border-color: var(--accent) !important;
}
button[data-testid="stBaseButton-secondary"] *,
button[data-testid="stBaseButton-secondaryFormSubmit"] * { color: inherit !important; }

/* --- Sliders : bornes et valeur lisibles dans les deux thèmes --- */
div[data-testid="stSliderTickBarMin"],
div[data-testid="stSliderTickBarMax"] { color: var(--text-muted) !important; }
div[data-testid="stSliderThumbValue"] { color: var(--accent) !important; }

/* --- Sidebar : textes courants et captions suivent le thème actif --- */
[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] span {
    color: var(--text-primary) !important;
}
[data-testid="stSidebar"] div[data-testid="stCaptionContainer"],
[data-testid="stSidebar"] div[data-testid="stCaptionContainer"] p,
[data-testid="stSidebar"] div[data-testid="stCaptionContainer"] span {
    color: var(--text-muted) !important;
}

/* --- Bouton de bascule de thème (rond, rotation au survol) --- */
.st-key-theme_btn button {
    width: 40px; height: 40px;
    border-radius: 50% !important;
    border: none !important;
    background: var(--accent-bg) !important;
    color: var(--text-primary) !important;
    transition: all 0.25s;
}
.st-key-theme_btn button:hover {
    background: var(--accent-hover) !important;
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

/* --- Illustrations SVG : flottement doux + animations internes --- */
@keyframes floatBob {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-8px); }
}
.eco-illustration {
    display: block;
    margin: 0 auto 0.6rem auto;
    animation: floatBob 4.5s ease-in-out infinite;
}
@keyframes spinSlow { to { transform: rotate(360deg); } }
.eco-illustration .spin {
    transform-box: fill-box;
    transform-origin: center;
    animation: spinSlow 18s linear infinite;
}
@keyframes growBar { from { transform: scaleY(0); } }
.eco-illustration .bar {
    transform-box: fill-box;
    transform-origin: bottom;
    animation: growBar 0.9s cubic-bezier(0.2, 0.8, 0.3, 1) backwards;
}
.eco-illustration rect.bar:nth-of-type(2) { animation-delay: 0.15s; }
.eco-illustration rect.bar:nth-of-type(3) { animation-delay: 0.30s; }

/* Cartes : apparition douce à l'affichage (backwards pour ne pas
   bloquer le transform du survol une fois l'animation finie) */
div[data-testid="stVerticalBlockBorderWrapper"] {
    animation: fadeInUp 0.45s ease-out backwards;
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

# --- Illustrations SVG dessinées main : elles utilisent les variables CSS
# du thème (var(--accent)...) et sont animées par les règles .eco-illustration.

# Loupe avec feuille : page Recherche
SVG_RECHERCHE = """
<svg class="eco-illustration" width="88" height="88" viewBox="0 0 100 100" aria-hidden="true">
  <circle cx="42" cy="42" r="27" fill="var(--accent-bg)" stroke="var(--accent)" stroke-width="6"/>
  <path d="M42 27 C 53 32, 55 45, 42 56 C 29 45, 31 32, 42 27 Z" fill="var(--accent)"/>
  <line x1="42" y1="36" x2="42" y2="52" stroke="var(--bg-card)" stroke-width="3" stroke-linecap="round"/>
  <line x1="63" y1="63" x2="84" y2="84" stroke="var(--accent)" stroke-width="9" stroke-linecap="round"/>
</svg>
"""

# Barres qui poussent : page Statistiques
SVG_STATS = """
<svg class="eco-illustration" width="88" height="88" viewBox="0 0 100 100" aria-hidden="true">
  <line x1="12" y1="88" x2="88" y2="88" stroke="var(--text-muted)" stroke-width="4" stroke-linecap="round"/>
  <rect class="bar" x="20" y="56" width="15" height="28" rx="4" fill="var(--accent-light)"/>
  <rect class="bar" x="43" y="40" width="15" height="44" rx="4" fill="var(--accent)"/>
  <rect class="bar" x="66" y="22" width="15" height="62" rx="4" fill="var(--accent-light)"/>
  <circle cx="73" cy="13" r="5" fill="var(--accent)"/>
</svg>
"""

# Boucle de recyclage en rotation lente : page Guide et page de connexion
SVG_RECYCLE = """
<svg class="eco-illustration" width="88" height="88" viewBox="0 0 100 100" aria-hidden="true">
  <g class="spin">
    <path d="M50 14 A 36 36 0 1 1 18 62" fill="none" stroke="var(--accent)" stroke-width="8" stroke-linecap="round"/>
    <polygon points="6,54 30,54 16,76" fill="var(--accent)"/>
  </g>
  <circle cx="50" cy="50" r="12" fill="var(--accent-bg)" stroke="var(--accent)" stroke-width="4"/>
</svg>
"""


def inject_css(theme: str = "light") -> None:
    """Injecte les variables du thème choisi puis le CSS global."""
    palette = PALETTES.get(theme, PALETTES["light"])
    variables = "".join(f"--{nom}: {valeur};" for nom, valeur in palette.items())
    st.markdown(f"<style>:root {{ {variables} }}</style>", unsafe_allow_html=True)
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    st.markdown(SHAPES_HTML, unsafe_allow_html=True)


def hero(titre: str, sous_titre: str, badge: str | None = None,
         svg: str | None = None) -> None:
    """Bandeau d'en-tête. `titre` peut contenir un
    <span class='eco-highlight'>mot surligné</span> ; `svg` une
    illustration (SVG_RECHERCHE, SVG_STATS, SVG_RECYCLE...).

    NB : le HTML est assemblé d'un seul tenant, sans ligne vide ni
    indentation — sinon Markdown ferme le bloc HTML et affiche la
    suite comme du code."""
    badge_html = f'<div><span class="eco-badge">{badge}</span></div>' if badge else ""
    st.markdown(
        '<div class="eco-hero">'
        + (svg.strip() if svg else "")
        + badge_html
        + f"<h1>{titre}</h1>"
        + f"<p>{sous_titre}</p>"
        + "</div>",
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
