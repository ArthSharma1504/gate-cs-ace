import hashlib
from datetime import date

import streamlit as st

from gate import scoring, state, ui
from gate.data.questions import QUESTIONS
from gate.data.syllabus import OFFICIAL_SITE, SUBJECTS, SYLLABUS

prog = state.P()

st.title("🎯 GATE CS Ace")
st.markdown("Your free, all-in-one prep companion for **GATE 2027 Computer Science & IT** — "
            "practise, take timed mocks, plan your days and get unstuck with an AI tutor.")

attempts = prog["attempts"]
acc = (sum(a["correct"] for a in attempts) / len(attempts)) if attempts else None
best_mock = max((m["score"] / m["max"] * 100 for m in prog["mocks"] if m["max"] == 100), default=None)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Days to GATE", max(state.days_left(), 0), help=f"Exam date: {prog['exam_date']}")
c2.metric("Questions solved", len(attempts), help="Across practice and mock tests")
c3.metric("Accuracy", f"{acc:.0%}" if acc is not None else "—")
c4.metric("Syllabus done", f"{state.syllabus_completion():.0%}",
          help="Weighted by marks; counts topics marked Practised or Confident")

left, right = st.columns([3, 2], gap="large")

with right:
    st.subheader("Today's focus")
    core = [s for s in SUBJECTS]
    ranked = sorted(core, key=lambda s: SYLLABUS[s]["weight"] * (1.15 - state.subject_mastery(s)), reverse=True)
    for s in ranked[:3]:
        m = state.subject_mastery(s)
        st.markdown(f"**{s}** · {SYLLABUS[s]['weight']} marks")
        st.progress(m, text=f"mastery {m:.0%}")
    st.caption("Ranked by marks at stake × how much room you have to improve.")
    st.page_link("views/practice.py", label="Start practising", icon="✍️")
    st.page_link("views/planner.py", label="Build my study plan", icon="🗓️")

with left:
    st.subheader("⚡ Daily challenge")
    seed = int(hashlib.sha256(date.today().isoformat().encode()).hexdigest(), 16)
    q = QUESTIONS[seed % len(QUESTIONS)]
    key = f"daily_{date.today().isoformat()}"
    with st.container(border=True):
        ui.meta(q)
        st.markdown(q["question"])
        resp = ui.answer_input(q, key, disabled=st.session_state.get(key + "_done", False))
        if not st.session_state.get(key + "_done"):
            if st.button("Check answer", type="primary"):
                if not scoring.is_answered(q, resp):
                    st.toast("Enter an answer first.")
                    st.stop()
                st.session_state[key + "_done"] = True
                state.record_attempt(q, scoring.is_correct(q, resp), scoring.marks_for(q, resp), "daily")
                st.rerun()
        else:
            ui.feedback(q, resp)

st.divider()
st.subheader("How to use this app to ace GATE")
a, b, c = st.columns(3)
a.markdown("**1 · Plan**\n\nSet your exam date and daily hours in the Study Planner. "
           "Mark what you already know in the Syllabus Tracker so the plan targets your gaps.")
b.markdown("**2 · Practise daily**\n\nSolve questions topic by topic. Every wrong answer goes to your "
           "mistake notebook — redo it until it sticks. Ask the AI tutor when stuck.")
c.markdown("**3 · Test & review**\n\nTake a timed mock every week (daily in the final weeks) with real "
           "GATE marking, then study the analytics to find weak topics.")

st.caption(f"Exam pattern and syllabus follow the official GATE 2027 information from IIT Madras "
           f"([{OFFICIAL_SITE}]({OFFICIAL_SITE})). Always confirm dates on the official site.")
