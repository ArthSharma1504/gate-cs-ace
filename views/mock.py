import random
import time
from datetime import datetime

import pandas as pd
import streamlit as st

from gate import scoring, state, ui
from gate.data.syllabus import SUBJECTS, SYLLABUS

prog = state.P()
st.title("⏱️ Mock Test")


# ------------------------------------------------------------------ building a test
def pick(pool, n, marks):
    cand = [q for q in pool if q["marks"] == marks]
    random.shuffle(cand)
    return cand[:n]


def weighted_core(pool, n1, n2):
    """Pick core questions roughly in proportion to subject weightage."""
    core = [q for q in pool if q["subject"] != "General Aptitude"]
    weights = {s: SYLLABUS[s]["weight"] for s in SUBJECTS if s != "General Aptitude"}
    chosen = []
    for marks, n in ((1, n1), (2, n2)):
        cand = [q for q in core if q["marks"] == marks]
        random.shuffle(cand)
        cand.sort(key=lambda q: -weights[q["subject"]] * random.random())
        chosen += cand[:n]
    return chosen


def start_mock(name, qs, minutes):
    st.session_state.mock = {
        "name": name, "qids": [q["id"] for q in qs], "minutes": minutes,
        "start": time.time(), "i": 0, "responses": {}, "status": {},  # status: visited/answered/review
        "submitted": False, "round": random.randint(0, 10**9),
    }
    st.rerun()


mock = st.session_state.get("mock")

if not mock:
    st.markdown("Exam-like tests with the real GATE marking scheme: **−1/3** for a wrong 1-mark MCQ, "
                "**−2/3** for a wrong 2-mark MCQ, no negative marking for MSQ and NAT.")
    bank = state.all_questions()
    ga = [q for q in bank if q["subject"] == "General Aptitude"]
    t1, t2, t3 = st.tabs(["Full-length (100 marks)", "Quick mock", "Subject test"])
    with t1:
        st.markdown("**65 questions · 100 marks · 180 minutes** — 10 General Aptitude + 55 Engineering "
                    "Mathematics & CS, exactly like GATE.")
        st.caption("Tip: do this on a laptop, in one sitting, with a pen, paper and the on-screen "
                   "calculator only.")
        if st.button("Start full-length mock", type="primary"):
            qs = pick(ga, 5, 1) + pick(ga, 5, 2) + weighted_core(bank, 25, 30)
            start_mock("Full-length mock", qs, 180)
    with t2:
        st.markdown("**20 questions · ~30 marks · 45 minutes** — a mixed set for a weekday evening.")
        if st.button("Start quick mock", type="primary"):
            qs = pick(ga, 2, 1) + pick(ga, 1, 2) + weighted_core(bank, 7, 10)
            start_mock("Quick mock", qs, 45)
    with t3:
        subj = st.selectbox("Subject", SUBJECTS)
        sp = [q for q in bank if q["subject"] == subj]
        n = st.slider("Number of questions", 5, max(5, len(sp)), min(10, len(sp)))
        st.caption(f"{len(sp)} questions available · {round(n * 2.8)} minutes")
        if st.button("Start subject test", type="primary"):
            random.shuffle(sp)
            start_mock(f"{SYLLABUS[subj]['short']} subject test", sp[:n], round(n * 2.8))

    if prog["mocks"]:
        st.subheader("Past tests")
        df = pd.DataFrame([{
            "When": m["ts"][:16].replace("T", " "), "Test": m["name"],
            "Score": f"{m['score']:.2f} / {m['max']}", "Percent": round(100 * m["score"] / m["max"], 1),
            "Correct": m["correct"], "Wrong": m["wrong"], "Skipped": m["skipped"], "Minutes": m["minutes"],
        } for m in reversed(prog["mocks"])])
        st.dataframe(df, hide_index=True, width="stretch")
    st.stop()

qs = [state.question_by_id(qid) for qid in mock["qids"]]
qs = [q for q in qs if q]
R = mock["round"]


def wkey(q):
    return f"mk_{R}_{q['id']}"


def save_current():
    q = qs[mock["i"]]
    resp = ui.read_input(q, wkey(q))
    mock["responses"][q["id"]] = resp
    if scoring.is_answered(q, resp):
        if mock["status"].get(q["id"]) not in ("review_answered",):
            mock["status"][q["id"]] = "answered"
    elif mock["status"].get(q["id"]) not in ("review",):
        mock["status"][q["id"]] = "visited"


def submit():
    if not mock["submitted"]:
        save_current()
        mock["submitted"] = True
        mock["end"] = time.time()
        res = {"correct": 0, "wrong": 0, "skipped": 0, "score": 0.0, "by_subject": {}}
        for q in qs:
            r = mock["responses"].get(q["id"])
            m = scoring.marks_for(q, r)
            bs = res["by_subject"].setdefault(q["subject"], [0.0, 0])
            bs[0] += m
            bs[1] += q["marks"]
            res["score"] += m
            if not scoring.is_answered(q, r):
                res["skipped"] += 1
            else:
                ok = scoring.is_correct(q, r)
                res["correct" if ok else "wrong"] += 1
                state.record_attempt(q, ok, m, "mock")
        prog["mocks"].append({
            "ts": datetime.now().isoformat(timespec="seconds"), "name": mock["name"],
            "score": round(res["score"], 2), "max": sum(q["marks"] for q in qs),
            "correct": res["correct"], "wrong": res["wrong"], "skipped": res["skipped"],
            "minutes": round((mock["end"] - mock["start"]) / 60, 1),
            "by_subject": {k: [round(v[0], 2), v[1]] for k, v in res["by_subject"].items()},
        })
        state.save()


# ------------------------------------------------------------------ results
if mock["submitted"]:
    last = prog["mocks"][-1]
    st.subheader(f"{mock['name']} — results")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Score", f"{last['score']:.2f} / {last['max']}")
    c2.metric("Correct", last["correct"])
    c3.metric("Wrong", last["wrong"])
    c4.metric("Skipped", last["skipped"])
    neg = sum(min(0, scoring.marks_for(q, mock["responses"].get(q["id"]))) for q in qs)
    if neg < 0:
        st.warning(f"You lost **{-neg:.2f} marks** to negative marking. On MCQs, only answer when you can "
                   "eliminate at least two options.")
    bs = pd.DataFrame([{"Subject": s, "Marks": v[0], "Out of": v[1],
                        "Percent": round(100 * max(v[0], 0) / v[1]) if v[1] else 0}
                       for s, v in last["by_subject"].items()]).sort_values("Percent")
    st.dataframe(bs, hide_index=True, width="stretch")

    st.subheader("Review every question")
    show = st.radio("Show", ["Wrong & skipped", "All"], horizontal=True)
    for n, q in enumerate(qs, 1):
        r = mock["responses"].get(q["id"])
        ok = scoring.is_correct(q, r)
        if show != "All" and ok:
            continue
        icon = "✅" if ok else ("⏭️" if not scoring.is_answered(q, r) else "❌")
        m = scoring.marks_for(q, r)
        with st.expander(f"{icon} Q{n} · {q['subject']} · {m:+.2f}"):
            ui.meta(q)
            st.markdown(q["question"])
            for j, o in enumerate(q["options"]):
                st.markdown(f"({ui.LETTERS[j]}) {o}")
            st.markdown(f"**Your answer:** {scoring.response_text(q, r)}  \n"
                        f"**Correct answer:** {scoring.answer_text(q)}")
            st.markdown(q["explanation"])
    if st.button("Take another test", type="primary"):
        del st.session_state.mock
        st.rerun()
    st.stop()


# ------------------------------------------------------------------ live test
deadline = mock["start"] + mock["minutes"] * 60


@st.fragment(run_every=1)
def timer():
    left = int(deadline - time.time())
    if left <= 0:
        st.error("Time's up — submitting your test.")
        submit()
        st.rerun(scope="app")
    h, rem = divmod(left, 3600)
    m, s = divmod(rem, 60)
    colour = "red" if left < 300 else "inherit"
    st.markdown(f"<div style='text-align:right;font-size:1.4rem;font-weight:700;color:{colour}'>"
                f"⏱ {h:d}:{m:02d}:{s:02d}</div>", unsafe_allow_html=True)


head = st.columns([3, 1])
head[0].markdown(f"**{mock['name']}** · {len(qs)} questions · {sum(q['marks'] for q in qs)} marks")
with head[1]:
    timer()

main, side = st.columns([3, 1.3], gap="medium")
i = mock["i"]
q = qs[i]
mock["status"].setdefault(q["id"], "visited")

with main:
    with st.container(border=True):
        ui.meta(q, number=i + 1)
        st.markdown(q["question"])
        ui.seed_input(q, wkey(q), mock["responses"].get(q["id"]))
        ui.answer_input(q, wkey(q))
    b = st.columns(4)
    if b[0].button("Save & Next", type="primary", width="stretch"):
        save_current()
        mock["i"] = min(i + 1, len(qs) - 1)
        st.rerun()
    if b[1].button("Review & Next", width="stretch"):
        save_current()
        ans = scoring.is_answered(q, mock["responses"].get(q["id"]))
        mock["status"][q["id"]] = "review_answered" if ans else "review"
        mock["i"] = min(i + 1, len(qs) - 1)
        st.rerun()
    if b[2].button("Clear response", width="stretch"):
        ui.clear_input(q, wkey(q))
        mock["responses"][q["id"]] = None
        mock["status"][q["id"]] = "visited"
        st.rerun()
    if b[3].button("← Previous", width="stretch", disabled=i == 0):
        save_current()
        mock["i"] = i - 1
        st.rerun()

with side:
    st.markdown("**Question palette**")
    st.caption("⬜ not visited · 🟥 not answered · 🟩 answered · 🟪 marked for review · "
               "🟦 answered & marked · outlined = current")
    pal = st.container(key="palette")
    cols = pal.columns(5, gap="small")
    for n, qq in enumerate(qs):
        status = (mock["status"].get(qq["id"]) or "none").replace("_", "")
        cur = "-current" if n == i else ""
        box = cols[n % 5].container(key=f"pal-{status}{cur}-{R}-{n}")
        if box.button(str(n + 1), key=f"pal_{R}_{n}", width="stretch"):
            save_current()
            mock["i"] = n
            st.rerun()
    answered = sum(1 for v in mock["status"].values() if v in ("answered", "review_answered"))
    st.caption(f"Answered {answered} of {len(qs)}")
    with st.popover("Submit test", width="stretch"):
        st.markdown("Submit now? You can't change answers afterwards.")
        if st.button("Yes, submit", type="primary"):
            submit()
            st.rerun()
    if st.button("Abandon test", width="stretch"):
        del st.session_state.mock
        st.rerun()
