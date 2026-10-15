from datetime import date

import streamlit as st

from gate import state
from gate.data.syllabus import EXAM_DATES, SUBJECTS
from gate.planner import build_plan

prog = state.P()
st.title("🗓️ Study Planner")
st.markdown("A day-by-day plan that puts more hours on high-weight subjects you're weaker in, then switches "
            "to mocks and revision in the final weeks.")

with st.container(border=True):
    c1, c2, c3 = st.columns(3)
    options = [date.fromisoformat(d) for d in EXAM_DATES]
    current = date.fromisoformat(prog["exam_date"])
    exam = c1.selectbox("Your GATE exam date", options, index=options.index(current) if current in options else 0,
                        format_func=lambda d: d.strftime("%a, %d %b %Y"),
                        help="GATE 2027 runs on 6, 7, 13, 14, 20 and 21 February. Pick yours once your admit "
                             "card is out; until then, the earliest date is safest.")
    hours = c2.slider("Study hours per day", 1.0, 12.0, float(prog["hours_per_day"]), 0.5)
    rest = c3.selectbox("Weekly rest day", ["None", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], index=7)
    if exam.isoformat() != prog["exam_date"] or hours != prog["hours_per_day"]:
        prog["exam_date"], prog["hours_per_day"] = exam.isoformat(), hours
        state.save()

mastery = {s: state.subject_mastery(s) for s in SUBJECTS}
rest_idx = None if rest == "None" else ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].index(rest)
plan = build_plan(date.today(), exam, hours, mastery, prog["topic_status"], rest_idx)

if plan.empty:
    st.warning("The exam date has passed. Pick a future date.")
    st.stop()

days = len(plan)
study_hours = plan["Hours"].sum()
c1, c2, c3 = st.columns(3)
c1.metric("Days left", days)
c2.metric("Planned study hours", f"{study_hours:,.0f}")
c3.metric("Full mocks planned", int(plan["Main focus"].str.startswith("Full mock").sum()))

if days < 30:
    st.info("Under a month left: the plan focuses on mocks and revision. Don't start brand-new heavy topics; "
            "maximise marks from what you already know plus General Aptitude and Engineering Maths.")

st.subheader("Hours by subject (learning phase)")
learn = plan[plan["Phase"] == "Learn & practise"]
if not learn.empty:
    share = learn.groupby("Main focus")["Hours"].sum().sort_values(ascending=False) * 0.5
    st.bar_chart(share, horizontal=True, y_label="", x_label="Main-focus hours")

st.subheader("Your schedule")
view = st.radio("Show", ["Next 14 days", "Whole plan"], horizontal=True)
shown = plan.head(14) if view == "Next 14 days" else plan
out = shown.copy()
out["Date"] = out["Date"].map(lambda d: d.strftime("%d %b"))
st.dataframe(out, hide_index=True, width="stretch",
             column_config={"Plan": st.column_config.TextColumn(width="large")})

st.download_button("⬇️ Download plan (CSV, opens in Excel / Google Sheets)", plan.to_csv(index=False),
                   file_name="gate-study-plan.csv", mime="text/csv")
st.caption("The plan updates as you mark topics in the Syllabus Tracker and practise — come back weekly.")
