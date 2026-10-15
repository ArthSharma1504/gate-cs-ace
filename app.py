"""GATE CS Ace — a free study companion for the GATE Computer Science & IT exam."""
from datetime import datetime

import streamlit as st

from gate import ai, state, store, ui

st.set_page_config(page_title="GATE CS Ace", page_icon="🎯", layout="wide")
state.init()
ui.style()

pages = {
    "Prepare": [
        st.Page("views/home.py", title="Dashboard", icon="🏠", default=True),
        st.Page("views/learn.py", title="Learn", icon="📚"),
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
    user = state.current_user()
    if user:
        st.markdown(f"👤 **{user['name']}**")
        if st.session_state.get("_load_failed"):
            st.error("Couldn't load your saved progress, so saving is paused to protect it. "
                     "Refresh the page in a minute.")
        elif st.session_state.get("_store_error"):
            st.warning("Couldn't save your latest progress. It will retry with your next answer.")
        elif store.is_persistent():
            st.caption("✅ Your progress saves automatically.")
        else:
            st.caption("⚠️ Saving to this server only. Ask the app owner to add GITHUB_TOKEN so progress "
                       "survives restarts.")
        st.download_button("⬇️ Download a backup", state.export_json(),
                           file_name=f"gate-ace-{user['id']}-{datetime.now():%Y%m%d}.json",
                           mime="application/json", width="stretch")
        if st.button("Sign out", width="stretch"):
            state.logout()
            st.rerun()
    else:
        if state.auth_enabled():
            with st.expander("🔑 Member sign-in"):
                with st.form("login", clear_on_submit=False, border=False):
                    uname = st.text_input("Username", key="login_user")
                    pwd = st.text_input("Password", type="password", key="login_pwd")
                    if st.form_submit_button("Sign in", type="primary", width="stretch"):
                        if state.login(uname, pwd):
                            st.rerun()
                        else:
                            st.error("Wrong username or password.")
        st.caption("👋 You're using guest mode — every feature works, but progress isn't saved and is "
                   "lost when you close the tab.")

ai.settings_sidebar()
nav.run()
