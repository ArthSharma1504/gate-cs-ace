import random

import streamlit as st

from gate import scoring, state, ui
from gate.data.syllabus import SUBJECTS, SYLLABUS

prog = state.P()
st.title("✍️ Practice")

bank = state.all_questions()
attempted = {a["qid"] for a in prog["attempts"]}
last_result = {}
for a in prog["attempts"]:
    last_result[a["qid"]] = a["correct"]
mistakes = {qid for qid, ok in last_result.items() if not ok}

with st.container(border=True):
    c1, c2 = st.columns([2, 1])
    subjects = c1.multiselect("Subjects", SUBJECTS, placeholder="All subjects", key="pr_subjects")
    mode = c2.selectbox("Show", ["All questions", "Not attempted yet", "Mistake notebook", "Bookmarked"])
    c3, c4, c5 = st.columns(3)
    types = c3.multiselect("Type", ["MCQ", "MSQ", "NAT"], placeholder="All types")
    diffs = c4.multiselect("Difficulty", ["easy", "medium", "hard"], placeholder="Any difficulty")
    topics_all = [t for s in (subjects or SUBJECTS) for t in SYLLABUS[s]["topics"]]
    if any(t not in topics_all for t in st.session_state.get("pr_topics", [])):
        st.session_state.pr_topics = [t for t in st.session_state.pr_topics if t in topics_all]
    topics = c5.multiselect("Topics", topics_all, placeholder="All topics", key="pr_topics")

pool = [
    q for q in bank
    if (not subjects or q["subject"] in subjects)
    and (not types or q["type"] in types)
    and (not diffs or q.get("difficulty", "medium") in diffs)
    and (not topics or q["topic"] in topics)
    and (mode != "Not attempted yet" or q["id"] not in attempted)
    and (mode != "Mistake notebook" or q["id"] in mistakes)
    and (mode != "Bookmarked" or q["id"] in prog["bookmarks"])
]

sig = (tuple(subjects), mode, tuple(types), tuple(diffs), tuple(topics), len(bank))
if st.session_state.get("pr_sig") != sig:
    order = [q["id"] for q in pool]
    random.shuffle(order)
    st.session_state.pr_sig = sig
    st.session_state.pr_order = order
    st.session_state.pr_i = 0
    st.session_state.pr_checked = False
    st.session_state.pr_round = st.session_state.get("pr_round", 0) + 1

order = st.session_state.pr_order
if not order:
    msg = {
        "Mistake notebook": "No mistakes logged yet for these filters — nice. Keep practising!",
        "Bookmarked": "No bookmarked questions yet. Use ☆ on any question to save it.",
        "Not attempted yet": "You've attempted every question for these filters. Try the AI Tutor to "
                             "generate fresh ones.",
    }.get(mode, "No questions match these filters.")
    st.info(msg)
    st.stop()

i = st.session_state.pr_i % len(order)
q = state.question_by_id(order[i])
key = f"pr_{st.session_state.pr_round}_{i}_{q['id']}"

st.progress((i + 1) / len(order), text=f"Question {i + 1} of {len(order)}")
with st.container(border=True):
    top = st.columns([6, 1])
    with top[0]:
        ui.meta(q)
    with top[1]:
        marked = q["id"] in prog["bookmarks"]
        if st.button("★" if marked else "☆", key=f"bm_{key}", help="Bookmark this question"):
            state.toggle_bookmark(q["id"])
            st.rerun()
    st.markdown(q["question"])
    checked = st.session_state.pr_checked
    resp = ui.answer_input(q, key, disabled=checked)

    b1, b2, b3, _ = st.columns([1.2, 1, 1.4, 2])
    if not checked:
        if b1.button("Check answer", type="primary"):
            if not scoring.is_answered(q, resp):
                st.toast("Enter an answer first (or use Show solution).")
                st.stop()
            st.session_state.pr_checked = True
            state.record_attempt(q, scoring.is_correct(q, resp), scoring.marks_for(q, resp), "practice")
            st.rerun()
        if b2.button("Show solution"):
            st.session_state.pr_checked = True
            state.record_attempt(q, False, 0.0, "practice")
            st.rerun()
    else:
        if b1.button("Next question →", type="primary"):
            st.session_state.pr_i = i + 1
            st.session_state.pr_checked = False
            st.rerun()
        if b3.button("🤖 Explain with AI tutor"):
            st.session_state.tutor_prefill = (
                f"I'm practising this GATE question:\n\n{q['question']}\n\n"
                + (("Options:\n" + "\n".join(f"({ui.LETTERS[j]}) {o}" for j, o in enumerate(q['options'])) + "\n\n")
                   if q["options"] else "")
                + f"My answer: {scoring.response_text(q, resp)}\nCorrect answer: {scoring.answer_text(q)}\n\n"
                "Explain the concept behind it, why my answer is right or wrong, and a shortcut to solve "
                "similar questions faster."
            )
            st.switch_page("views/tutor.py")

if st.session_state.pr_checked:
    ui.feedback(q, resp)

nav = st.columns([1, 1, 4])
if nav[0].button("← Previous", disabled=i == 0):
    st.session_state.pr_i = i - 1
    st.session_state.pr_checked = False
    st.rerun()
if nav[1].button("Skip →"):
    st.session_state.pr_i = i + 1
    st.session_state.pr_checked = False
    st.rerun()
