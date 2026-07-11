"""Page Mes statistiques : éco-points, niveau, répartition par poubelle."""

import altair as alt
import pandas as pd
import streamlit as st

from utils.categories import BINS
from webapp import ui
from webapp.stats import calculer_niveau, compter_par_poubelle


def render() -> None:
    ui.hero(
        "Mes <span class='eco-highlight'>statistiques</span>",
        "Votre activité de tri sur cette session.",
        svg=ui.SVG_STATS,
    )

    history = st.session_state.get("history", [])
    if not history:
        st.info(
            "Vous n'avez encore rien trié. Rendez-vous sur la page "
            "**🔍 Recherche & tri** pour gagner vos premiers éco-points !"
        )
        return

    niveau = calculer_niveau(len(history))

    col1, col2, col3 = st.columns(3)
    col1.metric("Produits triés", len(history))
    col2.metric("Éco-points", niveau["points"])
    col3.metric("Niveau", niveau["label"])

    if niveau["seuil_suivant"] is not None:
        restants = niveau["seuil_suivant"] - len(history)
        st.progress(
            niveau["progression"],
            text=f"Encore {restants} tri(s) avant le niveau suivant",
        )
    else:
        st.progress(1.0, text="Niveau maximum atteint — bravo ! 🌳")

    # --- Répartition par poubelle ---
    ui.section("Répartition par poubelle", "Vos tris de la session, poubelle par poubelle.")
    compteur = compter_par_poubelle(history)
    df = pd.DataFrame(
        {
            "Poubelle": [
                f"{BINS[cle]['emoji']} {BINS[cle]['label']}" for cle in compteur
            ],
            "Produits": list(compteur.values()),
            # Chaque barre prend la couleur officielle de sa poubelle
            "Couleur": [BINS[cle]["color"] for cle in compteur],
        }
    )
    graphe = (
        alt.Chart(df)
        # Largeur de barre fixe : reste fine même avec une seule poubelle
        .mark_bar(size=56, cornerRadiusTopLeft=8, cornerRadiusTopRight=8)
        .encode(
            x=alt.X("Poubelle:N", sort=None,
                    axis=alt.Axis(title=None, labelAngle=0, labelLimit=160)),
            y=alt.Y("Produits:Q",
                    # Graduations explicites en entiers (sinon Altair
                    # intercale des demi-valeurs arrondies : 0 1 1 2 2)
                    axis=alt.Axis(title="Produits triés", format="d",
                                  values=list(range(0, int(df["Produits"].max()) + 1))),
            ),
            color=alt.Color("Couleur:N", scale=None, legend=None),
            tooltip=["Poubelle", "Produits"],
        )
        .properties(height=320)
    )
    st.altair_chart(graphe, use_container_width=True)

    # --- Détail ---
    with st.expander("Détail des produits triés"):
        df_detail = pd.DataFrame(
            {
                "Produit": [e["name"] for e in reversed(history)],
                "Poubelle": [
                    f"{BINS[e['bin_key']]['emoji']} {BINS[e['bin_key']]['label']}"
                    for e in reversed(history)
                ],
            }
        )
        st.dataframe(df_detail, use_container_width=True, hide_index=True)
