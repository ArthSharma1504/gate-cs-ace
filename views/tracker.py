import streamlit as st

from gate import state
from gate.data.syllabus import SUBJECTS, SYLLABUS, SYLLABUS_PDF
from gate.state import LEVELS

prog = state.P()
st.title("✅ Syllabus Tracker")
st.markdown(f"Rate yourself on every topic of the [official GATE 2027 CS syllabus]({SYLLABUS_PDF}). "
            "Your ratings drive the study plan and the dashboard's focus list.")

st.progress(state.syllabus_completion(),
            text=f"Weighted completion: {state.syllabus_completion():.0%} (topics at Practised or Confident)")

for s in SUBJECTS:
    ts = prog["topic_status"][s]
    done = sum(1 for v in ts.values() if v >= 2)
    with st.expander(f"**{s}** · {SYLLABUS[s]['weight']} marks · {done}/{len(ts)} topics ready"):
        for t in SYLLABUS[s]["topics"]:
            c1, c2 = st.columns([3, 2])
            c1.markdown(t)
            new = c2.segmented_control(t, LEVELS, default=LEVELS[ts[t]], key=f"tr_{s}_{t}",
                                       label_visibility="collapsed")
            if new is not None and LEVELS.index(new) != ts[t]:
                ts[t] = LEVELS.index(new)
                state.save()
                st.rerun()
