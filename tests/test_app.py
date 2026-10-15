"""Smoke tests: every page renders and the core flows work. Run: python -m pytest -q"""
import sys
from pathlib import Path

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

PAGES = ["views/home.py", "views/practice.py", "views/mock.py", "views/tutor.py", "views/planner.py",
         "views/tracker.py", "views/notes.py", "views/analytics.py"]


def fresh():
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30)
    at.run()
    assert not at.exception, at.exception
    return at


def test_every_page_renders():
    at = fresh()
    for p in PAGES:
        at.switch_page(p).run()
        assert not at.exception, (p, at.exception)


def test_practice_flow_records_attempt():
    at = fresh()
    at.switch_page("views/practice.py").run()
    # answer whatever the first question is
    if at.radio:
        at.radio[0].set_value(0).run()
    elif at.text_input:
        at.text_input[0].input("1").run()
    else:
        at.checkbox[0].check().run()
    btn = next(b for b in at.button if b.label == "Check answer")
    btn.click().run()
    assert not at.exception, at.exception
    assert len(at.session_state.progress["attempts"]) == 1
    nxt = next(b for b in at.button if b.label == "Next question →")
    nxt.click().run()
    assert not at.exception


def test_mock_start_answer_submit():
    at = fresh()
    at.switch_page("views/mock.py").run()
    next(b for b in at.button if b.label == "Start quick mock").click().run()
    assert not at.exception, at.exception
    mock = at.session_state.mock
    assert len(mock["qids"]) == 20
    for _ in range(3):
        if at.radio:
            at.radio[0].set_value(1).run()
        elif at.text_input:
            at.text_input[0].input("7").run()
        next(b for b in at.button if b.label == "Save & Next").click().run()
        assert not at.exception, at.exception
    next(b for b in at.button if b.label == "Yes, submit").click().run()
    assert not at.exception, at.exception
    m = at.session_state.progress["mocks"][-1]
    assert m["correct"] + m["wrong"] + m["skipped"] == 20
    assert m["skipped"] >= 17 - 0
    assert any("results" in s.value for s in at.subheader)


def test_full_mock_shape():
    at = fresh()
    at.switch_page("views/mock.py").run()
    next(b for b in at.button if b.label == "Start full-length mock").click().run()
    assert not at.exception, at.exception
    from gate.data.questions import QUESTIONS
    by = {q["id"]: q for q in QUESTIONS}
    qs = [by[i] for i in at.session_state.mock["qids"]]
    assert len(qs) == 65 and len(set(q["id"] for q in qs)) == 65
    assert sum(q["marks"] for q in qs) == 100
    assert sum(q["marks"] for q in qs if q["subject"] == "General Aptitude") == 15


def test_tracker_updates_progress():
    at = fresh()
    at.switch_page("views/tracker.py").run()
    seg = at.get("button_group")[0]
    seg.set_value("Confident").run()
    assert not at.exception, at.exception
    ts = at.session_state.progress["topic_status"]["General Aptitude"]
    assert list(ts.values())[0] == 3


def test_planner_builds():
    from datetime import date
    from gate.planner import build_plan
    from gate.state import default_progress
    from gate.data.syllabus import SUBJECTS
    p = default_progress()
    df = build_plan(date(2026, 10, 15), date(2027, 2, 6), 6, {s: 0.2 for s in SUBJECTS}, p["topic_status"], 6)
    assert len(df) == (date(2027, 2, 6) - date(2026, 10, 15)).days
    assert (df["Phase"] == "Final revision").sum() >= 3
    learn = df[df["Phase"] == "Learn & practise"]["Main focus"].value_counts()
    assert learn.index[0] in ("Programming & Data Structures", "Engineering Mathematics")


def test_ai_parser():
    from gate.ai import parse_generated
    txt = 'Here: [{"type":"MCQ","marks":1,"question":"q","options":["a","b","c","d"],"answer":2,' \
          '"explanation":"e"},{"type":"NAT","marks":2,"question":"q2","options":[],"answer":5,' \
          '"explanation":"e"},{"type":"MCQ","question":"bad","options":["a"],"answer":0}]'
    out = parse_generated(txt)
    assert len(out) == 2 and out[1]["answer"] == [5.0, 5.0]
