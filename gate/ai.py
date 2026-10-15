"""Optional AI tutor backed by free-tier LLM APIs (Google Gemini or Groq).

Keys come from the student (pasted in the app, kept only in their session) or from
Streamlit secrets (GEMINI_API_KEY / GROQ_API_KEY) if the person deploying the app wants
to provide one. Nothing is stored server-side.
"""
from __future__ import annotations

import json
import re

import requests
import streamlit as st

PROVIDERS = {
    "Google Gemini (free tier)": {
        "secret": "GEMINI_API_KEY",
        "models": ["gemini-3.6-flash", "gemini-3.8-flash", "gemini-3.5-flash-lite", "gemini-2.5-flash"],
        "key_url": "https://aistudio.google.com/apikey",
    },
    "Groq (free tier)": {
        "secret": "GROQ_API_KEY",
        "models": ["openai/gpt-oss-120b", "llama-3.3-70b-versatile", "openai/gpt-oss-20b", "llama-3.1-8b-instant"],
        "key_url": "https://console.groq.com/keys",
    },
}

TUTOR_SYSTEM = """You are GATE Ace, an expert tutor for the GATE Computer Science & IT (CS) exam in India,
organised for 2027 by IIT Madras. The paper has 65 questions for 100 marks in 3 hours: General Aptitude (15),
Engineering Mathematics (13) and core CS (72). Question types are MCQ (negative marking 1/3 or 2/3),
MSQ (no negative, no partial credit) and NAT (numerical, no negative).

How to teach:
- Solve step by step, show the key formula, then the final answer clearly.
- Point out the common trap or shortcut GATE toppers use.
- Keep answers focused; use short code blocks for C or pseudo-code and plain-text math.
- If the student seems to be guessing, check their understanding with one quick follow-up question.
- If you are unsure of a fact, say so instead of inventing it.
- Only help with exam preparation and learning, never with cheating during a live exam."""

SOCRATIC_ADDON = """
Socratic mode is ON: do not give the full solution straight away. Give a hint or ask a guiding question first,
and reveal the full solution only when the student asks for it or has tried twice."""


def settings_sidebar() -> None:
    """AI provider/model/key inputs, rendered in the sidebar on every page so the key is never dropped."""
    with st.sidebar.expander("🤖 AI tutor settings", expanded=not current_key()):
        provider = st.selectbox("Provider", list(PROVIDERS), key="ai_provider")
        cfg = PROVIDERS[provider]
        st.selectbox("Model", cfg["models"], key=f"ai_model_{provider}")
        st.text_input("API key", type="password", key=f"api_key_{provider}",
                      help="Kept only in your browser session; never saved or shared.",
                      placeholder="Using the app's shared key" if _secret_key(provider) else "Paste your free key")
        st.caption(f"Free key in a minute: [{cfg['key_url']}]({cfg['key_url']})")


def current() -> tuple[str, str]:
    provider = st.session_state.get("ai_provider") or next(iter(PROVIDERS))
    model = st.session_state.get(f"ai_model_{provider}") or PROVIDERS[provider]["models"][0]
    return provider, model


def current_key() -> str | None:
    return get_key(current()[0])


def _secret_key(provider: str) -> str | None:
    try:
        return st.secrets.get(PROVIDERS[provider]["secret"]) or None
    except Exception:
        return None


def get_key(provider: str) -> str | None:
    user_key = st.session_state.get(f"api_key_{provider}")
    if user_key:
        return user_key.strip()
    return _secret_key(provider)


class AIError(RuntimeError):
    pass


def chat(provider: str, model: str, messages: list[dict], system: str, temperature: float = 0.4,
         timeout: int = 90) -> str:
    """messages: [{"role": "user"|"assistant", "content": str}]"""
    key = get_key(provider)
    if not key:
        raise AIError("No API key set. Add one in the sidebar.")
    try:
        if provider.startswith("Google"):
            return _gemini(key, model, messages, system, temperature, timeout)
        return _groq(key, model, messages, system, temperature, timeout)
    except requests.RequestException as e:
        raise AIError(f"Network error: {e}") from e


def _gemini(key, model, messages, system, temperature, timeout):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    body = {
        "systemInstruction": {"parts": [{"text": system}]},
        "contents": [
            {"role": "model" if m["role"] == "assistant" else "user", "parts": [{"text": m["content"]}]}
            for m in messages
        ],
        "generationConfig": {"temperature": temperature},
    }
    r = requests.post(url, json=body, headers={"x-goog-api-key": key}, timeout=timeout)
    if r.status_code != 200:
        raise AIError(_err(r))
    data = r.json()
    try:
        parts = data["candidates"][0]["content"]["parts"]
        return "".join(p.get("text", "") for p in parts if not p.get("thought"))
    except (KeyError, IndexError):
        raise AIError(f"Unexpected response: {json.dumps(data)[:300]}")


def _groq(key, model, messages, system, temperature, timeout):
    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {key}"},
        json={"model": model, "temperature": temperature,
              "messages": [{"role": "system", "content": system}] + messages},
        timeout=timeout,
    )
    if r.status_code != 200:
        raise AIError(_err(r))
    return r.json()["choices"][0]["message"]["content"]


def _err(r) -> str:
    try:
        msg = r.json().get("error", {})
        msg = msg.get("message", msg) if isinstance(msg, dict) else msg
    except ValueError:
        msg = r.text[:300]
    hint = ""
    if r.status_code in (401, 403):
        hint = " Check that the API key is correct."
    elif r.status_code == 429:
        hint = " Free-tier rate limit reached; wait a minute or switch model."
    elif r.status_code == 404:
        hint = " This model may be unavailable for your key; pick another in the sidebar."
    return f"API error {r.status_code}: {msg}.{hint}"


LESSON_PROMPT = """Teach the GATE CS topic "{topic}" (subject: {subject}) to a student who has read a one-page summary
and wants to go deeper. Write in clear, simple English with markdown headings:
### Build the intuition  (explain the core idea with an everyday analogy)
### Step-by-step method  (how to solve GATE questions on this topic)
### Two solved GATE-level examples  (one 1-mark, one 2-mark, full working)
### Common mistakes
### Quick self-test  (3 short questions; put the answers at the very end under "Answers")
Keep it under 900 words. Be accurate; if a fact is uncertain, leave it out."""

GEN_PROMPT = """Write {n} new, original GATE CS-style questions.
Subject: {subject}. Topic: {topic}. Question type: {qtype}. Difficulty: {difficulty}.
Return ONLY a JSON array, no prose, where each item has:
  "type": "MCQ" | "MSQ" | "NAT",
  "marks": 1 or 2,
  "question": string (markdown allowed; use ``` for code),
  "options": array of exactly 4 strings for MCQ/MSQ, [] for NAT,
  "answer": integer index 0-3 for MCQ, array of indices for MSQ, [low, high] numbers for NAT,
  "explanation": step-by-step solution string.
Double-check every answer by solving the question yourself before writing it."""


def parse_generated(text: str) -> list[dict]:
    m = re.search(r"\[.*\]", text, re.S)
    if not m:
        raise AIError("The model did not return a JSON list. Try again.")
    try:
        items = json.loads(m.group(0))
    except ValueError as e:
        raise AIError(f"Could not parse the questions: {e}") from e
    out = []
    for it in items:
        try:
            t = it["type"].upper()
            q = {"type": t, "marks": 2 if int(it.get("marks", 1)) == 2 else 1,
                 "question": str(it["question"]), "explanation": str(it.get("explanation", "")),
                 "options": [str(o) for o in it.get("options", [])]}
            if t == "MCQ":
                q["answer"] = int(it["answer"])
                assert len(q["options"]) == 4 and 0 <= q["answer"] < 4
            elif t == "MSQ":
                q["answer"] = sorted({int(i) for i in it["answer"]})
                assert len(q["options"]) == 4 and q["answer"] and all(0 <= i < 4 for i in q["answer"])
            elif t == "NAT":
                a = it["answer"]
                lo, hi = (float(a[0]), float(a[-1])) if isinstance(a, list) else (float(a), float(a))
                q["answer"], q["options"] = [min(lo, hi), max(lo, hi)], []
            else:
                continue
            out.append(q)
        except (KeyError, ValueError, TypeError, AssertionError):
            continue
    if not out:
        raise AIError("None of the generated questions were in a valid format. Try again.")
    return out
