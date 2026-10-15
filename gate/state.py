"""Session state and progress persistence.

Progress lives in st.session_state["progress"]. Students can download it as JSON and
upload it later (works on Streamlit Community Cloud, where server disk is shared and
temporary). When running locally, set GATE_ACE_AUTOSAVE=/path/progress.json to save
automatically after every change.
"""
from __future__ import annotations

import json
import os
from datetime import date, datetime
from pathlib import Path

import streamlit as st

from gate.data.questions import QUESTIONS
from gate.data.syllabus import EXAM_DATES, SUBJECTS, SYLLABUS

LEVELS = ["Not started", "Learning", "Practised", "Confident"]
AUTOSAVE = os.environ.get("GATE_ACE_AUTOSAVE")


def default_progress() -> dict:
    return {
        "version": 1,
        "exam_date": EXAM_DATES[0],
        "hours_per_day": 6,
        "attempts": [],          # {qid, subject, topic, correct, marks, ts, mode}
        "bookmarks": [],
        "topic_status": {s: {t: 0 for t in SYLLABUS[s]["topics"]} for s in SUBJECTS},
        "mocks": [],             # {ts, name, score, max, correct, wrong, skipped, minutes, by_subject}
        "custom_questions": [],  # AI-generated questions the student kept
        "active_days": [],
    }


def _merge(loaded: dict) -> dict:
    """Fill in keys missing from older or hand-edited progress files."""
    base = default_progress()
    for k, v in loaded.items():
        if k == "topic_status":
            for s, topics in v.items():
                if s in base["topic_status"]:
                    for t, lvl in topics.items():
                        if t in base["topic_status"][s]:
                            base["topic_status"][s][t] = int(lvl)
        elif k in base:
            base[k] = v
    return base


def init() -> None:
    if "progress" in st.session_state:
        return
    prog = default_progress()
    if AUTOSAVE and Path(AUTOSAVE).exists():
        try:
            prog = _merge(json.loads(Path(AUTOSAVE).read_text()))
        except (OSError, ValueError):
            pass
    st.session_state.progress = prog


def P() -> dict:
    init()
    return st.session_state.progress


def save() -> None:
    if AUTOSAVE:
        try:
            Path(AUTOSAVE).write_text(json.dumps(P(), indent=1))
        except OSError:
            pass


def export_json() -> str:
    return json.dumps(P(), indent=1)


def import_json(text: str) -> None:
    st.session_state.progress = _merge(json.loads(text))
    save()


def all_questions() -> list[dict]:
    return QUESTIONS + P()["custom_questions"]


def question_by_id(qid: str) -> dict | None:
    return next((q for q in all_questions() if q["id"] == qid), None)


def record_attempt(q: dict, correct: bool, marks: float, mode: str) -> None:
    prog = P()
    today = date.today().isoformat()
    prog["attempts"].append({
        "qid": q["id"], "subject": q["subject"], "topic": q["topic"],
        "correct": bool(correct), "marks": marks, "ts": datetime.now().isoformat(timespec="seconds"),
        "mode": mode,
    })
    if today not in prog["active_days"]:
        prog["active_days"].append(today)
    save()


def toggle_bookmark(qid: str) -> None:
    b = P()["bookmarks"]
    if qid in b:
        b.remove(qid)
    else:
        b.append(qid)
    save()


def days_left() -> int:
    try:
        return (date.fromisoformat(P()["exam_date"]) - date.today()).days
    except ValueError:
        return 0


def streak() -> int:
    days = {date.fromisoformat(d) for d in P()["active_days"]}
    n, d = 0, date.today()
    if d not in days:
        d = date.fromordinal(d.toordinal() - 1)
    while d in days:
        n += 1
        d = date.fromordinal(d.toordinal() - 1)
    return n


def subject_mastery(subject: str) -> float:
    """0..1 blend of self-rated syllabus coverage and practice accuracy."""
    ts = P()["topic_status"][subject]
    coverage = sum(ts.values()) / (3 * len(ts)) if ts else 0
    att = [a for a in P()["attempts"] if a["subject"] == subject]
    if len(att) < 3:
        return coverage
    acc = sum(a["correct"] for a in att[-30:]) / len(att[-30:])
    return 0.5 * coverage + 0.5 * acc


def syllabus_completion() -> float:
    """Weight-adjusted share of topics marked Practised or Confident."""
    total = done = 0.0
    for s in SUBJECTS:
        ts = P()["topic_status"][s]
        w = SYLLABUS[s]["weight"]
        total += w
        done += w * sum(1 for v in ts.values() if v >= 2) / len(ts)
    return done / total if total else 0.0
