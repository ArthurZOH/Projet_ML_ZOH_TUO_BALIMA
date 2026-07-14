"""Page Recherche & tri : le cœur de l'application.

Flux : mot-clé -> résultats Jumia (ou mode démo) -> sélection ->
prédiction de la matière -> écran coloré selon la poubelle.
"""

import streamlit as st

from scraping.scraper import (
    JumiaScraper,
    NoResultsError,
    PageUnavailableError,
    ScraperError,
    ScraperTimeoutError,
)
from utils.categories import BINS, CLASS_TO_BIN
from utils.electronique import detect_electronique
from webapp import ui
from webapp.inference import SEUIL_CONFIANCE, predire_matiere

IMAGE_PLACEHOLDER = "https://placehold.co/200x200?text=Image"

SUGGESTIONS = [
    "bouteille d'eau", "écouteurs bluetooth", "cahier", "bocal de confiture",
    "canette", "chargeur usb",
]

MAX_RECHERCHES_RECENTES = 6


@st.cache_data(ttl=600, show_spinner=False)
def search_jumia(keyword: str, max_results: int) -> list[dict]:
    """Recherche sur Jumia via le scraper (Étudiant A) et adapte les
    champs (nom/prix/image/lien) au format attendu par l'interface.

    Le cache (10 min) évite de re-scraper Jumia à chaque interaction
    Streamlit (chaque clic relance le script en entier).
    """
    produits = JumiaScraper().search(keyword, max_results=max_results)
    return [
        {
            "name": p.nom,
            "price": p.prix or "Prix non disponible",
            "image_url": p.image or IMAGE_PLACEHOLDER,
            "url": p.lien,
        }
        for p in produits
    ]


def _lancer_recherche(keyword: str) -> None:
    """Enregistre la recherche et met à jour la liste des recherches récentes."""
    keyword = keyword.strip()
    if not keyword:
        return
    st.session_state["last_search"] = keyword
    recentes = st.session_state.setdefault("recent_searches", [])
    if keyword in recentes:
        recentes.remove(keyword)
    recentes.append(keyword)
    del recentes[:-MAX_RECHERCHES_RECENTES]


def _sur_pill(cle: str) -> None:
    """Callback des pills (suggestions / recherches récentes) : lance la
    recherche puis désélectionne la pill pour permettre un nouveau clic."""
    valeur = st.session_state.get(cle)
    if valeur:
        _lancer_recherche(valeur)
        st.session_state[cle] = None


def _ecran_resultat(selected: dict) -> None:
    """Écran coloré aux couleurs de la poubelle + récapitulatif produit.

    Logique décidée en réunion d'équipe (13/07) : l'image d'abord — si le
    modèle est confiant (>= SEUIL_CONFIANCE), sa prédiction fait foi ;
    en cas de doute, on se réfère aux mots-clés D3E du titre.
    """
    prediction = predire_matiere(selected)
    incertain = False
    if prediction["reel"] and prediction["confiance"] >= SEUIL_CONFIANCE:
        bin_key = CLASS_TO_BIN.get(prediction["matiere"], "marron")
    elif detect_electronique(selected["name"]):
        bin_key, prediction = "electronique", None
    else:
        bin_key = CLASS_TO_BIN.get(prediction["matiere"], "marron")
        # On avertit seulement quand le vrai modèle doute (pas le mock)
        incertain = prediction["reel"]

    # Enregistre le tri une seule fois (pas à chaque rerun de l'écran)
    if not st.session_state.get("history_recorded"):
        st.session_state.setdefault("history", []).append(
            {"name": selected["name"], "bin_key": bin_key}
        )
        st.session_state["history_recorded"] = True
        st.toast("+10 éco-points ! 🌱")
        st.balloons()

    bin_info = BINS[bin_key]
    st.markdown(
        f"""
        <style>
        .stApp {{ background: {bin_info["color"]} !important; background-image: none !important; }}
        .floating-shapes {{ display: none; }}
        .ecosort-result {{ color: {bin_info["text_color"]}; }}
        </style>
        <div class="ecosort-result">
            <div class="eco-emoji">{bin_info["emoji"]}</div>
            <h1>{bin_info["label"]}</h1>
            <p style="font-size: 1.2rem;">{bin_info["consigne"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Récapitulatif du produit analysé, sur carte blanche pour rester lisible
    with st.container(border=True):
        col_img, col_info = st.columns([1, 3])
        with col_img:
            st.image(selected["image_url"], width=90)
        with col_info:
            st.markdown(f"**{selected['name']}**")
            ui.prix(selected["price"])
            if prediction is None:
                st.caption("Détecté comme appareil électronique (D3E, mots-clés)")
            elif prediction["reel"]:
                st.caption(
                    f"Matière détectée : {prediction['matiere']} "
                    f"(confiance : {prediction['confiance']:.0%})"
                )
            else:
                st.caption(
                    f"Matière détectée : {prediction['matiere']} (modèle de démonstration)"
                )
            st.markdown(f"[Voir le produit sur Jumia ↗]({selected['url']})")

    if incertain:
        st.warning(
            f"Prédiction incertaine ({prediction['confiance']:.0%}) : "
            "vérifiez la consigne — dans le doute, privilégiez la poubelle marron."
        )

    # On ne vide jamais toute la session : historique et recherches
    # récentes doivent survivre à la navigation.
    col_retour, col_nouvelle = st.columns(2)
    with col_retour:
        if st.button("← Retour aux résultats", use_container_width=True):
            st.session_state.pop("selected_product", None)
            st.session_state.pop("history_recorded", None)
            st.rerun()
    with col_nouvelle:
        if st.button("🔍 Nouvelle recherche", use_container_width=True):
            st.session_state.pop("selected_product", None)
            st.session_state.pop("history_recorded", None)
            st.session_state.pop("last_search", None)
            st.rerun()


def render() -> None:
    selected = st.session_state.get("selected_product")
    if selected is not None:
        _ecran_resultat(selected)
        return

    ui.hero(
        "Cherchez. Triez. <span class='eco-highlight'>Recyclez.</span>",
        "L'IA qui trouve la bonne poubelle pour chaque produit Jumia.",
        badge="♻️ EcoSort-Search",
        svg=ui.SVG_RECHERCHE,
    )

    with st.form("recherche", border=False):
        col_champ, col_bouton = st.columns([4, 1], vertical_alignment="bottom")
        with col_champ:
            keyword = st.text_input(
                "Quel produit voulez-vous jeter ?",
                placeholder="Ex. : bouteille d'eau",
                key="search_input",
            )
        with col_bouton:
            submitted = st.form_submit_button("🔍 Chercher", use_container_width=True)
    if submitted:
        _lancer_recherche(keyword)

    st.pills(
        "💡 Suggestions",
        SUGGESTIONS,
        key="pill_suggestions",
        on_change=_sur_pill,
        args=("pill_suggestions",),
    )
    recentes = st.session_state.get("recent_searches", [])
    if recentes:
        st.pills(
            "🕘 Recherches récentes",
            list(reversed(recentes)),
            key="pill_recentes",
            on_change=_sur_pill,
            args=("pill_recentes",),
        )

    last_search = st.session_state.get("last_search")
    if not last_search:
        st.info("Saisissez un produit, ou piochez dans les suggestions ci-dessus.")
        return

    max_results = st.session_state.get("max_results", 5)

    with st.spinner(f"Recherche de « {last_search} »…"):
        try:
            results = search_jumia(last_search, max_results)
        except NoResultsError:
            st.warning(f"Aucun résultat trouvé pour « {last_search} ». Essayez un autre mot-clé.")
            return
        except ScraperTimeoutError:
            st.error("Jumia met trop de temps à répondre. Réessayez dans un instant.")
            return
        except (PageUnavailableError, ScraperError):
            st.error("Jumia est indisponible pour le moment. Réessayez plus tard.")
            return

    ui.section(
        f"Résultats pour « {last_search} »",
        "Cliquez sur un produit pour découvrir sa poubelle.",
    )

    # Retour à l'accueil sans avoir à choisir un produit
    _, col_effacer, _ = st.columns([2, 1, 2])
    with col_effacer:
        if st.button("✖ Effacer la recherche", use_container_width=True):
            st.session_state.pop("last_search", None)
            st.rerun()

    # Grille de cartes produits (3 colonnes)
    for ligne in range(0, len(results), 3):
        colonnes = st.columns(3)
        for col, (i, product) in zip(
            colonnes, enumerate(results[ligne:ligne + 3], start=ligne)
        ):
            with col:
                if ui.carte_produit(product, key=f"choose_{i}"):
                    st.session_state["selected_product"] = product
                    st.rerun()
