"""GATE CS Ace — a free study companion for the GATE Computer Science & IT exam."""
from datetime import datetime

import streamlit as st

from gate import state, ui

st.set_page_config(page_title="GATE CS Ace", page_icon="🎯", layout="wide")
state.init()
ui.style()

pages = {
    "Prepare": [
        st.Page("views/home.py", title="Dashboard", icon="🏠", default=True),
        st.Page("views/practice.py", title="Practice", icon="✍️"),
        st.Page("views/mock.py", title="Mock Test", icon="⏱️"),
        st.Page("views/tutor.py", title="AI Tutor", icon="🤖"),
    ],
    "Plan & revise": [
        st.Page("views/planner.py", title="Study Planner", icon="🗓️"),
        st.Page("views/tracker.py", title="Syllabus Tracker", icon="✅"),
        st.Page("views/notes.py", title="Revision Notes", icon="📒"),
        st.Page("views/analytics.py", title="Analytics", icon="📈"),
    ],
}
nav = st.navigation(pages)

with st.sidebar:
    st.markdown("### 🎯 GATE CS Ace")
    d = state.days_left()
    st.markdown(f"**{max(d, 0)} days** to GATE · 🔥 {state.streak()}-day streak")
    st.divider()
    st.markdown("**Your progress file**")
    st.caption("Progress is kept in this browser session. Download it to keep it, upload it next time.")
    st.download_button("⬇️ Download progress", state.export_json(),
                       file_name=f"gate-ace-progress-{datetime.now():%Y%m%d}.json",
                       mime="application/json", width="stretch")
    up = st.file_uploader("Upload progress", type="json", label_visibility="collapsed")
    if up is not None and st.session_state.get("_last_upload") != up.file_id:
        try:
            state.import_json(up.getvalue().decode("utf-8"))
            st.session_state._last_upload = up.file_id
            st.success("Progress restored.")
            st.rerun()
        except (ValueError, UnicodeDecodeError):
            st.error("That file isn't a valid progress file.")

nav.run()
