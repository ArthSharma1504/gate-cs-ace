"""Builds a day-by-day study plan from the exam date, daily hours and current mastery."""
from __future__ import annotations

from datetime import date, timedelta

import pandas as pd

from gate.data.syllabus import SUBJECTS, SYLLABUS


def build_plan(start: date, exam: date, hours: float, mastery: dict[str, float], topic_status: dict,
               rest_weekday: int | None = None, revision_days: int | None = None) -> pd.DataFrame:
    """Return a DataFrame with one row per study day.

    Phase 1 (learn + practise): subjects scheduled by priority = weight × (1.15 − mastery),
    weaker topics first. Phase 2 (final weeks): alternating full mocks, analysis and revision.
    """
    total_days = (exam - start).days
    if total_days <= 0:
        return pd.DataFrame()
    if revision_days is None:
        revision_days = max(3, min(21, round(total_days * 0.18)))
    revision_days = min(revision_days, total_days)
    learn_days = total_days - revision_days

    core = [s for s in SUBJECTS if s != "General Aptitude"]
    priority = {s: SYLLABUS[s]["weight"] * (1.15 - mastery.get(s, 0)) for s in core}
    credit = {s: 0.0 for s in core}
    queue = {
        s: sorted(SYLLABUS[s]["topics"], key=lambda t: topic_status[s].get(t, 0))
        for s in core
    }
    pos = {s: 0 for s in core}

    def next_topics(s, k=2):
        tops = queue[s]
        picked = [tops[(pos[s] + i) % len(tops)] for i in range(k)]
        pos[s] = (pos[s] + k) % len(tops)
        return picked

    def pick_subject(exclude=None):
        tot = sum(priority.values())
        for s in core:
            credit[s] += priority[s] / tot
        best = max((s for s in core if s != exclude), key=lambda s: credit[s])
        credit[best] -= 1
        return best

    rows = []
    day = start
    mock_no = 0
    for i in range(total_days):
        day = start + timedelta(days=i)
        if rest_weekday is not None and day.weekday() == rest_weekday:
            rows.append({"Date": day, "Day": day.strftime("%a"), "Phase": "Rest",
                         "Main focus": "Rest & light revision", "Topics": "Skim your formula notes",
                         "Plan": "Take a break. 30 min skim of notes is enough.", "Hours": 0.5})
            continue
        if i < learn_days:
            main = pick_subject()
            second = pick_subject(exclude=main)
            h_main, h_second, h_ga = round(hours * 0.5, 1), round(hours * 0.3, 1), round(hours * 0.2, 1)
            weekly_test = (i + 1) % 7 == 0
            plan = (f"{h_main}h learn + solve on {main}; {h_second}h practice questions on {second}; "
                    f"{h_ga}h General Aptitude / Engineering Maths drill.")
            if weekly_test:
                plan += " End the day with a Quick Mock and log mistakes."
            rows.append({"Date": day, "Day": day.strftime("%a"), "Phase": "Learn & practise",
                         "Main focus": main, "Topics": " · ".join(next_topics(main)),
                         "Plan": plan, "Hours": hours})
        else:
            j = i - learn_days
            if j % 2 == 0:
                mock_no += 1
                rows.append({"Date": day, "Day": day.strftime("%a"), "Phase": "Final revision",
                             "Main focus": f"Full mock #{mock_no}",
                             "Topics": "All subjects",
                             "Plan": "3h full-length mock in exam conditions, then review every wrong and "
                                     "skipped question.",
                             "Hours": hours})
            else:
                weak = sorted(core, key=lambda s: mastery.get(s, 0))[:2]
                rows.append({"Date": day, "Day": day.strftime("%a"), "Phase": "Final revision",
                             "Main focus": "Revise weak areas", "Topics": " · ".join(weak),
                             "Plan": "Revise formula sheets, redo your mistake notebook, then a subject test on "
                                     f"{weak[0]}.",
                             "Hours": hours})
    df = pd.DataFrame(rows)
    return df
