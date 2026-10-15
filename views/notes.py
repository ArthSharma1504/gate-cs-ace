import streamlit as st

from gate.data.notes import NOTES
from gate.data.syllabus import SUBJECTS, SYLLABUS

st.title("📒 Revision Notes")
st.markdown("High-yield formulas, facts and traps for each subject. Read one sheet a day in the final weeks.")

subject = st.pills("Subject", SUBJECTS, default=SUBJECTS[0], label_visibility="collapsed")
subject = subject or SUBJECTS[0]
st.subheader(f"{subject} · {SYLLABUS[subject]['weight']} marks")
with st.container(border=True):
    st.markdown(NOTES[subject])

c1, c2 = st.columns(2)
if c1.button(f"Practise {SYLLABUS[subject]['short']} questions →", type="primary"):
    st.session_state.pr_subjects = [subject]
    st.switch_page("views/practice.py")
c2.download_button("⬇️ Download all notes (Markdown)",
                   "\n\n".join(f"# {s}\n{NOTES[s]}" for s in SUBJECTS),
                   file_name="gate-cs-revision-notes.md")
