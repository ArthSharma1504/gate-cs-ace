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

def progress_file_tools(expanded_label: str | None = None) -> None:
    box = st.expander(expanded_label) if expanded_label else st.container()
    with box:
        st.download_button("⬇️ Download progress", state.export_json(),
                           file_name=f"gate-ace-progress-{datetime.now():%Y%m%d}.json",
                           mime="application/json", width="stretch")
        up = st.file_uploader("Upload progress", type="json", label_visibility="collapsed")
        if up is not None and st.session_state.get("_last_upload") != up.file_id:
            try:
                state.import_json(up.getvalue().decode("utf-8"))
                st.session_state._last_upload = up.file_id
                st.toast("Progress file added to your progress.", icon="✅")
                st.rerun()
            except (ValueError, UnicodeDecodeError, KeyError, TypeError):
                st.error("That file isn't a valid progress file.")


with st.sidebar:
    st.markdown("### 🎯 GATE CS Ace")
    d = state.days_left()
    st.markdown(f"**{max(d, 0)} days** to GATE · 🔥 {state.streak()}-day streak")
    st.divider()
    user = state.current_user()
    if user:
        st.markdown(f"👤 **{user['name']}**")
        if st.session_state.get("_store_error"):
            st.error("Couldn't reach the progress database, so recent work may not be saved. "
                     "Download a backup below.")
        else:
            st.caption("✅ Your progress saves automatically.")
        if st.button("Sign out", width="stretch"):
            st.logout()
        progress_file_tools("Backup or import a progress file")
    elif state.auth_enabled():
        st.markdown("**Save your progress**")
        st.caption("Sign in so your practice, mocks and plan are saved and follow you to any device.")
        if st.button("Sign in with Google", type="primary", width="stretch", icon=":material/login:"):
            st.login()
        if state.P()["attempts"]:
            st.caption("Already practised as a guest? Download your progress first, then upload it after "
                       "signing in and it will be added to your account.")
        progress_file_tools("Guest progress file")
    else:
        st.markdown("**Your progress file**")
        st.caption("Progress is kept in this browser session. Download it to keep it, upload it next time.")
        progress_file_tools()

nav.run()
