import pandas as pd
import streamlit as st

from gate import state
from gate.data.syllabus import SUBJECTS, SYLLABUS

prog = state.P()
st.title("📈 Analytics")

att = pd.DataFrame(prog["attempts"])
if att.empty:
    st.info("No attempts yet. Solve a few questions in Practice or take a Mock Test and your analysis "
            "will appear here.")
    st.page_link("views/practice.py", label="Go to Practice", icon="✍️")
    st.stop()

att["day"] = pd.to_datetime(att["ts"]).dt.date

c1, c2, c3, c4 = st.columns(4)
c1.metric("Attempts", len(att))
c2.metric("Accuracy", f"{att['correct'].mean():.0%}")
c3.metric("Active days", len(prog["active_days"]))
c4.metric("Current streak", f"{state.streak()} days")

st.subheader("Accuracy by subject")
by = att.groupby("subject").agg(attempts=("correct", "size"), accuracy=("correct", "mean"))
by = by.reindex([s for s in SUBJECTS if s in by.index])
st.bar_chart((by["accuracy"] * 100).rename("Accuracy %"), horizontal=True, y_label="")

proj = sum(SYLLABUS[s]["weight"] * (by.loc[s, "accuracy"] if s in by.index else 0) for s in SUBJECTS)
covered = sum(SYLLABUS[s]["weight"] for s in SUBJECTS if s in by.index)
st.markdown(f"**Rough score indicator:** about **{proj:.0f} / 100** if your current accuracy held across the "
            f"paper (based on subjects worth {covered} marks that you've practised; ignores negative marking).")
st.caption("This is a motivation gauge, not a prediction of your GATE score or rank.")

st.subheader("Weakest topics")
tp = att.groupby(["subject", "topic"]).agg(attempts=("correct", "size"), accuracy=("correct", "mean"))
tp = tp[tp["attempts"] >= 2].sort_values(["accuracy", "attempts"], ascending=[True, False]).head(8)
if tp.empty:
    st.caption("Attempt at least two questions per topic to see this.")
else:
    tp = tp.reset_index()
    tp["accuracy"] = (tp["accuracy"] * 100).round().astype(int).astype(str) + "%"
    st.dataframe(tp, hide_index=True, width="stretch")

st.subheader("Daily activity")
daily = att.groupby("day").agg(solved=("correct", "size"), correct=("correct", "sum"))
st.bar_chart(daily, stack=False)

if prog["mocks"]:
    st.subheader("Mock test trend")
    mk = pd.DataFrame(prog["mocks"])
    mk["percent"] = (mk["score"] / mk["max"] * 100).round(1)
    mk["test"] = [f"{i + 1}. {n}" for i, n in enumerate(mk["name"])]
    st.line_chart(mk.set_index("test")["percent"], y_label="Score %")
