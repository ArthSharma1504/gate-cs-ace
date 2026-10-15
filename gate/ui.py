"""Shared UI pieces: question rendering, answer inputs, feedback, styling."""
from __future__ import annotations

import streamlit as st

from gate import scoring

LETTERS = "ABCD"
TYPE_HELP = {
    "MCQ": "Multiple choice · one correct · negative marking",
    "MSQ": "Multiple select · one or more correct · no negative marking",
    "NAT": "Numerical answer · type a number · no negative marking",
}

CSS = """<style>
.block-container {padding-top: 2.2rem; max-width: 1100px;}
.q-meta {font-size: 0.82rem; opacity: 0.75; margin-bottom: 0.35rem;}
.tag {display:inline-block; padding:1px 8px; border-radius:999px; margin-right:6px; border:1px solid rgba(128,128,128,.35); font-size:0.75rem;}
.st-key-palette [data-testid="stHorizontalBlock"] {gap: 0.3rem;}
.st-key-palette button {padding: 0 !important; min-height: 2.1rem; min-width: 0 !important;}
.st-key-palette button p {font-size: 0.85rem; font-weight: 600; white-space: nowrap; letter-spacing: -0.02em;}
div[class*="st-key-pal-visited"] button {background: #e5484d !important; color: #fff !important; border-color: #e5484d !important;}
div[class*="st-key-pal-answered"] button {background: #2f9e44 !important; color: #fff !important; border-color: #2f9e44 !important;}
div[class*="st-key-pal-review-"] button {background: #7950f2 !important; color: #fff !important; border-color: #7950f2 !important;}
div[class*="st-key-pal-reviewanswered"] button {background: #1c7ed6 !important; color: #fff !important; border-color: #1c7ed6 !important;}
div[class*="-current-"] button {outline: 3px solid #f59f00 !important; outline-offset: 1px;}
</style>"""


def style() -> None:
    st.html(CSS)


def meta(q: dict, number: int | None = None) -> None:
    src = " · AI-generated" if q.get("source") == "ai" else ""
    head = f"Q{number} · " if number else ""
    st.markdown(
        f"<div class='q-meta'>{head}<span class='tag'>{q['subject']}</span>"
        f"<span class='tag'>{q['type']}</span><span class='tag'>{q['marks']} mark"
        f"{'s' if q['marks'] > 1 else ''}</span><span class='tag'>{q.get('difficulty', 'medium')}</span>"
        f"{src}</div>",
        unsafe_allow_html=True,
    )


def answer_input(q: dict, key: str, disabled: bool = False):
    """Render the input for q and return the current response.

    MCQ -> int | None, MSQ -> list[int], NAT -> str
    """
    st.caption(TYPE_HELP[q["type"]])
    if q["type"] == "MCQ":
        return st.radio("Your answer", list(range(len(q["options"]))), index=None, key=key,
                        format_func=lambda i: f"({LETTERS[i]})  {q['options'][i]}", disabled=disabled,
                        label_visibility="collapsed")
    if q["type"] == "MSQ":
        chosen = []
        for i, opt in enumerate(q["options"]):
            if st.checkbox(f"({LETTERS[i]})  {opt}", key=f"{key}_{i}", disabled=disabled):
                chosen.append(i)
        return chosen
    return st.text_input("Your numerical answer", key=key, disabled=disabled, placeholder="e.g. 12.5")


def seed_input(q: dict, key: str, resp) -> None:
    """Pre-fill widget state from a stored response (before the widget is drawn)."""
    if q["type"] == "MSQ":
        for i in range(len(q["options"])):
            k = f"{key}_{i}"
            if k not in st.session_state:
                st.session_state[k] = bool(resp) and i in resp
    elif key not in st.session_state:
        st.session_state[key] = resp if q["type"] == "MCQ" else (resp or "")


def read_input(q: dict, key: str):
    if q["type"] == "MSQ":
        return [i for i in range(len(q["options"])) if st.session_state.get(f"{key}_{i}")]
    return st.session_state.get(key)


def clear_input(q: dict, key: str) -> None:
    if q["type"] == "MSQ":
        for i in range(len(q["options"])):
            st.session_state.pop(f"{key}_{i}", None)
    else:
        st.session_state.pop(key, None)


def feedback(q: dict, resp) -> None:
    if scoring.is_correct(q, resp):
        st.success(f"Correct! +{q['marks']} mark{'s' if q['marks'] > 1 else ''}")
    elif not scoring.is_answered(q, resp):
        st.info(f"Answer: **{scoring.answer_text(q)}**")
    else:
        m = scoring.marks_for(q, resp)
        pen = f" ({m:+.2f} in the real exam)" if m < 0 else ""
        st.error(f"Not quite{pen}. Correct answer: **{scoring.answer_text(q)}**")
    with st.container(border=True):
        st.markdown("**Solution**")
        st.markdown(q["explanation"])
