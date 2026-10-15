import streamlit as st

from gate import ai, scoring, state, store, ui
from gate.data.lessons import LESSONS, nptel_search_url, video_search_url
from gate.data.syllabus import SUBJECTS, SYLLABUS
from gate.state import LEVELS

prog = state.P()
st.title("📚 Learn")
st.markdown("Learn any topic of the GATE CS syllabus from scratch: the idea, a worked example, the traps examiners "
            "set, then check yourself.")

STATUS_ICON = {0: "○", 1: "◐", 2: "◕", 3: "●"}

subject = st.pills("Subject", SUBJECTS, default=st.session_state.get("learn_subject_saved", SUBJECTS[0]),
                   key="learn_subject", label_visibility="collapsed") or SUBJECTS[0]
st.session_state.learn_subject_saved = subject
topics = SYLLABUS[subject]["topics"]
ts = prog["topic_status"][subject]

c1, c2 = st.columns([3, 1], vertical_alignment="bottom")
saved_topic = st.session_state.get("learn_topic_saved")
topic = c1.selectbox(
    "Topic", topics, index=topics.index(saved_topic) if saved_topic in topics else 0,
    format_func=lambda t: f"{STATUS_ICON[ts[t]]}  {t}",
    help="○ not started · ◐ learning · ◕ practised · ● confident",
)
st.session_state.learn_topic_saved = topic
done = sum(1 for t in topics if ts[t] >= 2)
c2.metric(f"{SYLLABUS[subject]['short']} topics ready", f"{done}/{len(topics)}")

# ------------------------------------------------------------------ the lesson
with st.container(border=True):
    st.subheader(topic)
    st.markdown(LESSONS[(subject, topic)])

v1, v2, _ = st.columns([1, 1, 1])
v1.link_button("▶️ Watch lectures", video_search_url(subject, topic), width="stretch")
v2.link_button("🎓 NPTEL (IIT) lectures", nptel_search_url(subject, topic), width="stretch")

# ------------------------------------------------------------------ go deeper with AI
lesson_key = f"{subject}::{topic}"
with st.expander("🤖 Go deeper with the AI tutor — intuition, method, 2 solved examples, self-test"):
    cached = st.session_state.get(f"deep_{lesson_key}")
    if cached is None:
        try:
            cached = store.lesson_get(lesson_key)
        except Exception:
            cached = None
    if cached:
        st.markdown(cached)
        st.caption("Written by AI — double-check anything that looks off.")
    else:
        provider, model = ai.current()
        if not ai.get_key(provider):
            st.caption("Add a free API key under **AI tutor settings** in the sidebar to unlock this. "
                       "Once anyone generates it, it's saved for every student.")
        if st.button("Generate deep-dive lesson", disabled=not ai.get_key(provider), type="primary"):
            with st.spinner("Writing your lesson…"):
                try:
                    text = ai.chat(provider, model, [{"role": "user", "content": ai.LESSON_PROMPT.format(
                        topic=topic, subject=subject)}], ai.TUTOR_SYSTEM, temperature=0.4)
                    st.session_state[f"deep_{lesson_key}"] = text
                    try:
                        store.lesson_put(lesson_key, text)
                    except Exception:
                        pass
                    st.rerun()
                except ai.AIError as e:
                    st.error(str(e))

# ------------------------------------------------------------------ check yourself
st.subheader("✅ Check yourself")
qs = [q for q in state.all_questions() if q["subject"] == subject and q["topic"] == topic][:3]
if not qs:
    st.caption("No bank questions on this exact topic yet. Generate some in the AI Tutor, or practise the whole "
               "subject.")
for n, q in enumerate(qs, 1):
    key = f"learn_{q['id']}"
    with st.container(border=True):
        ui.meta(q, number=n)
        st.markdown(q["question"])
        done_q = st.session_state.get(key + "_done", False)
        resp = ui.answer_input(q, key, disabled=done_q)
        if not done_q:
            if st.button("Check", key=key + "_btn"):
                if not scoring.is_answered(q, resp):
                    st.toast("Enter an answer first.")
                else:
                    st.session_state[key + "_done"] = True
                    state.record_attempt(q, scoring.is_correct(q, resp), scoring.marks_for(q, resp), "learn")
                    st.rerun()
        else:
            ui.feedback(q, resp)

# ------------------------------------------------------------------ rate & next steps
st.subheader("How well do you know this now?")
new = st.segmented_control("Your level", LEVELS, default=LEVELS[ts[topic]], key=f"learn_lvl_{subject}_{topic}",
                           label_visibility="collapsed")
if new is not None and LEVELS.index(new) != ts[topic]:
    ts[topic] = LEVELS.index(new)
    state.save()
    st.toast(f"Saved: {topic} → {new}")
    st.rerun()

a, b, c = st.columns(3)
if a.button("✍️ Practise this topic", type="primary", width="stretch"):
    st.session_state.pr_subjects = [subject]
    st.session_state.pr_topics = [topic]
    st.switch_page("views/practice.py")
if b.button("💬 Ask the tutor a doubt", width="stretch"):
    st.session_state.tutor_prefill = (f"I'm learning '{topic}' ({subject}) for GATE CS. I've read the basics. "
                                      "Explain it again in a different way with one more solved example, then "
                                      "ask me one question to check I understood.")
    st.switch_page("views/tutor.py")
i = topics.index(topic)
if c.button("Next topic →", width="stretch", disabled=i == len(topics) - 1):
    st.session_state.learn_topic_saved = topics[i + 1]
    st.rerun()
