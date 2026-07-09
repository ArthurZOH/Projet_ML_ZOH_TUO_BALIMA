"""Page Quiz du tri : QCM pour réviser les bons gestes."""

import streamlit as st

from utils.categories import BINS
from webapp import ui
from webapp.quiz_data import QUESTIONS


def _rejouer() -> None:
    for cle in ("quiz_i", "quiz_score", "quiz_choix"):
        st.session_state.pop(cle, None)


def _ecran_final(score: int) -> None:
    total = len(QUESTIONS)
    st.markdown(f"## Résultat : {score}/{total}")
    if score == total:
        st.success("Sans faute — vous êtes un pro du tri ! 🌳")
        st.balloons()
    elif score >= total * 0.7:
        st.success("Très bon score ! Encore quelques pièges à réviser. 🌿")
    else:
        st.warning("Un tour sur la page **🗑️ Guide du tri** vous fera du bien. 🌱")
    st.button("🔁 Rejouer", on_click=_rejouer, use_container_width=True)


def render() -> None:
    ui.hero(
        "🧠 Quiz du tri",
        "10 questions pour tester vos réflexes — attention aux pièges.",
    )

    i = st.session_state.get("quiz_i", 0)
    score = st.session_state.get("quiz_score", 0)

    if i >= len(QUESTIONS):
        _ecran_final(score)
        return

    st.progress(i / len(QUESTIONS), text=f"Question {i + 1}/{len(QUESTIONS)} — score : {score}")

    question = QUESTIONS[i]
    st.subheader(question["question"])

    choix_valide = st.session_state.get("quiz_choix")  # réponse déjà validée ?

    reponse = st.radio(
        "Votre réponse :",
        question["options"],
        format_func=lambda cle: f"{BINS[cle]['emoji']} {BINS[cle]['label']}",
        index=None,
        key=f"quiz_radio_{i}",
        disabled=choix_valide is not None,
    )

    if choix_valide is None:
        if st.button("✅ Valider", use_container_width=True, disabled=reponse is None):
            st.session_state["quiz_choix"] = reponse
            if reponse == question["reponse"]:
                st.session_state["quiz_score"] = score + 1
            st.rerun()
        return

    # --- Feedback après validation ---
    bonne = BINS[question["reponse"]]
    if choix_valide == question["reponse"]:
        st.success(f"Bonne réponse ! {bonne['emoji']} {question['explication']}")
    else:
        st.error(
            f"Raté — c'était {bonne['emoji']} **{bonne['label']}**. "
            f"{question['explication']}"
        )

    def _suivante() -> None:
        st.session_state["quiz_i"] = i + 1
        st.session_state.pop("quiz_choix", None)

    st.button("➡️ Question suivante", on_click=_suivante, use_container_width=True)
