"""Page de garde : connexion ou inscription avant d'accéder à l'application.
La bascule clair/sombre est disponible dès cette page."""

import streamlit as st

from webapp import ui
from webapp.auth import creer_jeton, inscrire, verifier


def _ouvrir_session(identifiant: str) -> None:
    """Connecte l'utilisateur et pose le jeton d'URL (survit au refresh)."""
    identifiant = identifiant.strip().lower()
    st.session_state["utilisateur"] = identifiant
    st.query_params["session"] = creer_jeton(identifiant)
    st.rerun()


def _formulaire_connexion() -> None:
    with st.form("login", border=False):
        identifiant = st.text_input("Identifiant", placeholder="ex. : yannel")
        mot_de_passe = st.text_input("Mot de passe", type="password")
        soumis = st.form_submit_button("Se connecter", use_container_width=True)

    if soumis:
        if verifier(identifiant, mot_de_passe):
            _ouvrir_session(identifiant)
        else:
            st.error("Identifiant ou mot de passe incorrect.")

    st.caption(
        "Comptes de démo : alice, arthur ou yannel — mot de passe « ecosort2026 »"
    )


def _formulaire_inscription() -> None:
    with st.form("inscription", border=False):
        identifiant = st.text_input("Identifiant", placeholder="lettres et chiffres")
        mot_de_passe = st.text_input("Mot de passe", type="password")
        confirmation = st.text_input("Confirmez le mot de passe", type="password")
        soumis = st.form_submit_button("Créer mon compte", use_container_width=True)

    if not soumis:
        return
    if mot_de_passe != confirmation:
        st.error("Les deux mots de passe ne correspondent pas.")
        return
    succes, message = inscrire(identifiant, mot_de_passe)
    if succes:
        _ouvrir_session(identifiant)  # connexion automatique après l'inscription
    else:
        st.error(message)


def render() -> None:
    # Bascule de thème disponible avant même la connexion. On la place en
    # haut à droite, DANS le flux de la page (sous le header Streamlit) :
    # placée là, elle reste cliquable, contrairement à un bouton flottant
    # qui passe sous la barre d'outils du header.
    _, col_theme = st.columns([11, 1], vertical_alignment="center")
    with col_theme:
        ui.bouton_theme(key="theme_btn_login")

    _, col_centre, _ = st.columns([1, 1.2, 1])
    with col_centre:
        st.markdown("<div style='height: 6vh'></div>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(
                '<div class="eco-logo-wrap"><span class="eco-logo-emoji">♻️</span></div>'
                "<h2 style='text-align:center; margin-bottom:0;'>EcoSort-Search</h2>"
                "<p style='text-align:center;'>Connectez-vous pour accéder à l'application.</p>",
                unsafe_allow_html=True,
            )
            onglet_connexion, onglet_inscription = st.tabs(
                ["Se connecter", "Créer un compte"]
            )
            with onglet_connexion:
                _formulaire_connexion()
            with onglet_inscription:
                _formulaire_inscription()
