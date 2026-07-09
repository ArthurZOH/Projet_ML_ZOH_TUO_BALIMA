"""Page Mes statistiques : éco-points, niveau, répartition par poubelle."""

import pandas as pd
import streamlit as st

from utils.categories import BINS
from webapp import ui
from webapp.stats import calculer_niveau, compter_par_poubelle


def render() -> None:
    ui.hero(
        "📊 Mes statistiques",
        "Votre activité de tri sur cette session.",
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

    st.divider()

    # --- Répartition par poubelle ---
    st.subheader("Répartition par poubelle")
    compteur = compter_par_poubelle(history)
    df = pd.DataFrame(
        {
            "Poubelle": [
                f"{BINS[cle]['emoji']} {BINS[cle]['label']}" for cle in compteur
            ],
            "Produits": list(compteur.values()),
        }
    )
    st.bar_chart(df, x="Poubelle", y="Produits", color="#2E7D32", horizontal=True)

    # --- Détail + export ---
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

    st.download_button(
        "⬇️ Exporter l'historique (CSV)",
        data=pd.DataFrame(history).to_csv(index=False).encode("utf-8"),
        file_name="ecosort_historique.csv",
        mime="text/csv",
        use_container_width=True,
    )
