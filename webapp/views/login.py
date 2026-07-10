"""Page de garde : connexion requise avant d'accéder à l'application."""

import streamlit as st

from webapp import ui
from webapp.auth import verifier


def render() -> None:
    _, col_centre, _ = st.columns([1, 1.2, 1])
    with col_centre:
        st.markdown("<div style='height: 6vh'></div>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown(
                ui.SVG_RECYCLE
                + "<h2 style='text-align:center; margin-bottom:0;'>EcoSort-Search</h2>"
                "<p style='text-align:center;'>Connectez-vous pour accéder à l'application.</p>",
                unsafe_allow_html=True,
            )
            with st.form("login", border=False):
                identifiant = st.text_input("Identifiant", placeholder="ex. : yannel")
                mot_de_passe = st.text_input("Mot de passe", type="password")
                soumis = st.form_submit_button("Se connecter", use_container_width=True)

            if soumis:
                if verifier(identifiant, mot_de_passe):
                    st.session_state["utilisateur"] = identifiant.strip().lower()
                    st.rerun()
                else:
                    st.error("Identifiant ou mot de passe incorrect.")

            st.caption(
                "Comptes de démo : alice, arthur ou yannel — mot de passe « ecosort2026 »"
            )
