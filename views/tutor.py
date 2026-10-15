import uuid

import streamlit as st

from gate import ai, state
from gate.scoring import answer_text
from gate.data.syllabus import SUBJECTS, SYLLABUS

prog = state.P()
st.title("🤖 AI Tutor")

provider, model = ai.current()
cfg = ai.PROVIDERS[provider]
socratic = st.toggle("Socratic mode — give me hints first, not the full answer", value=False)

has_key = bool(ai.get_key(provider))
if not has_key:
    st.info(f"The tutor runs on a **free** API key. Create one at [{cfg['key_url']}]({cfg['key_url']}) "
            "(no payment needed), paste it under **AI tutor settings** in the sidebar, and you're set. "
            "Everything else in the app works without a key.")

tab_chat, tab_gen = st.tabs(["💬 Doubt solver", "🧪 Generate practice questions"])

# ------------------------------------------------------------------ chat
with tab_chat:
    st.session_state.setdefault("chat", [])
    top = st.columns([4, 1])
    top[0].caption("Ask anything: a concept, a past-paper question, a shortcut, or paste your attempt and ask "
                   "where you went wrong.")
    if top[1].button("New chat", width="stretch"):
        st.session_state.chat = []
        st.rerun()

    if not st.session_state.chat:
        st.markdown("**Try:**")
        ex = st.columns(3)
        samples = ["Explain how to find the number of tag bits in a set-associative cache, with an example",
                   "What's the fastest way to check if a language is regular in GATE questions?",
                   "Give me a 2-mark GATE-style question on deadlock and wait for my answer"]
        for c, s in zip(ex, samples):
            if c.button(s, width="stretch"):
                st.session_state.tutor_prefill = s
                st.rerun()

    for m in st.session_state.chat:
        with st.chat_message(m["role"], avatar="🎓" if m["role"] == "assistant" else None):
            st.markdown(m["content"])

    prompt = st.chat_input("Ask your GATE doubt…", disabled=not has_key)
    prefill = st.session_state.pop("tutor_prefill", None)
    if prefill and has_key:
        prompt = prefill
    elif prefill:
        st.warning("Add an API key in the sidebar, then ask again. Your question:")
        st.code(prefill, language=None)

    if prompt:
        st.session_state.chat.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant", avatar="🎓"):
            with st.spinner("Thinking…"):
                try:
                    system = ai.TUTOR_SYSTEM + (ai.SOCRATIC_ADDON if socratic else "")
                    reply = ai.chat(provider, model, st.session_state.chat[-20:], system)
                except ai.AIError as e:
                    reply = None
                    st.error(str(e))
            if reply:
                st.markdown(reply)
                st.session_state.chat.append({"role": "assistant", "content": reply})
            else:
                st.session_state.chat.pop()

# ------------------------------------------------------------------ question generator
with tab_gen:
    st.caption("Generate fresh questions on any topic, then add them to your Practice and Mock Test pool.")
    c1, c2 = st.columns(2)
    subj = c1.selectbox("Subject", SUBJECTS, key="gen_subj")
    topic = c2.selectbox("Topic", SYLLABUS[subj]["topics"], key="gen_topic")
    c3, c4, c5 = st.columns(3)
    qtype = c3.selectbox("Type", ["Mixed (MCQ, MSQ, NAT)", "MCQ", "MSQ", "NAT"])
    diff = c4.selectbox("Difficulty", ["GATE level (medium)", "easy", "hard"])
    n = c5.number_input("How many", 1, 10, 5)

    if st.button("Generate", type="primary", disabled=not has_key):
        with st.spinner("Writing questions…"):
            try:
                text = ai.chat(provider, model, [{"role": "user", "content": ai.GEN_PROMPT.format(
                    n=n, subject=subj, topic=topic, qtype=qtype, difficulty=diff)}], ai.TUTOR_SYSTEM,
                    temperature=0.7)
                st.session_state.generated = [
                    dict(q, id=f"AI-{uuid.uuid4().hex[:8]}", subject=subj, topic=topic,
                         difficulty="hard" if diff == "hard" else ("easy" if diff == "easy" else "medium"),
                         source="ai")
                    for q in ai.parse_generated(text)
                ]
            except ai.AIError as e:
                st.error(str(e))

    gen = st.session_state.get("generated", [])
    if gen:
        st.warning("AI-written questions can occasionally have wrong answers. Check the solution before "
                   "trusting it, and use the bank questions for scoring yourself.")
        for k, q in enumerate(gen, 1):
            with st.expander(f"{k}. {q['type']} · {q['marks']} mark{'s' if q['marks'] > 1 else ''}"):
                st.markdown(q["question"])
                for j, o in enumerate(q["options"]):
                    st.markdown(f"({'ABCD'[j]}) {o}")
                st.markdown(f"**Answer:** {answer_text(q)}")
                st.markdown(q["explanation"])
        a, b = st.columns(2)
        if a.button(f"➕ Add all {len(gen)} to my practice pool", type="primary"):
            prog["custom_questions"].extend(gen)
            state.save()
            st.session_state.generated = []
            st.success("Added. Find them in Practice (they're tagged AI-generated).")
        if b.button("Discard"):
            st.session_state.generated = []
            st.rerun()

    if prog["custom_questions"]:
        st.caption(f"You have {len(prog['custom_questions'])} AI-generated questions saved.")
        if st.button("Remove all AI-generated questions"):
            prog["custom_questions"] = []
            state.save()
            st.rerun()
