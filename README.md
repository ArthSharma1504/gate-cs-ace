# 🎯 GATE CS Ace

A free, open-source study companion for **GATE 2027 Computer Science & Information Technology (CS)**, built with Streamlit.

Practice, mock tests, planning and revision all work with no API key. It also adds an optional **AI tutor** that runs on free-tier Google Gemini or Groq keys.

## Features

| | |
|---|---|
| 📚 **Learn** | A built-in lesson for **all 80 topics** of the GATE 2027 CS syllabus: the core idea, a worked GATE-style example and exam traps. Plus check-yourself questions, lecture links, a self-rating that updates the tracker, and an optional AI deep-dive lesson (generated once, then saved for every student). |
| ✍️ **Practice** | 133 original GATE-style MCQ / MSQ / NAT questions across all 11 sections, with step-by-step solutions. Filter by subject, topic, type and difficulty. Bookmarks and an automatic **mistake notebook**. |
| ⏱️ **Mock tests** | Full-length mock (65 Q · 100 marks · 180 min, exact GATE split), quick mocks and subject tests. Live timer, GATE-style colour-coded question palette, mark-for-review, and the **real marking scheme** (−1/3, −2/3 for wrong MCQs; no negative for MSQ/NAT). Detailed review after submission. |
| 🤖 **AI tutor** | Doubt-solver chat that knows the GATE pattern, a Socratic "hints first" mode, one-click "explain my mistake" from any question, and an **AI question generator** that adds fresh questions to your practice pool. |
| 🗓️ **Study planner** | Day-by-day plan up to your exam date that spends more time on high-weight subjects you're weaker in, then switches to mocks + revision in the final weeks. Downloadable as CSV. |
| ✅ **Syllabus tracker** | Every topic of the revised GATE 2027 CS syllabus, rated Not started → Confident. Drives the planner and dashboard. |
| 📒 **Revision notes** | High-yield formula and fact sheets for every subject. |
| 📈 **Analytics** | Accuracy by subject, weakest topics, daily activity, mock score trend and a rough score indicator. |
| 🏠 **Dashboard** | Countdown, streak, "today's focus" and a daily challenge question. |

## Run it locally

```bash
git clone https://github.com/ArthSharma1504/gate-cs-ace.git
cd gate-cs-ace
pip install -r requirements.txt
streamlit run app.py
```

Without sign-in configured, the app runs in guest mode: progress lives in the browser session, and students use
**Download progress** / **Upload** in the sidebar to keep it. When running on your own machine you can auto-save instead:

```bash
GATE_ACE_AUTOSAVE=~/gate-progress.json streamlit run app.py
```

## Deploy free on Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
2. **Create app** → pick this repo, branch `main`, main file `app.py` → **Deploy**.
3. *(Optional)* In **App settings → Secrets**, add `GEMINI_API_KEY = "..."` so every visitor gets a working AI tutor without their own key. See `.streamlit/secrets.toml.example`.

## Turn on Google sign-in (progress saved per student)

Students click **Sign in with Google**; after that every answer, mock score, plan setting and tracker rating is saved
automatically and follows them to any device. Guests can still use everything, and a guest's downloaded progress file
can be uploaded after signing in to merge it into their account.

**1 · Free database (Supabase, ~3 min)** — Community Cloud doesn't keep files between restarts, so progress lives here.
1. Create a free project at [supabase.com](https://supabase.com) (choose the Mumbai / `ap-south-1` region for India).
2. Click **Connect** → copy the **Transaction pooler** connection string and put your database password in it.
3. Change the start from `postgresql://` to `postgresql+psycopg2://`. The app creates its table itself.

Free tier: 500 MB (plenty for tens of thousands of students). A free project pauses after a week with no activity;
restore it from the Supabase dashboard.

**2 · Google login client (~5 min)**
1. In [Google Cloud Console](https://console.cloud.google.com/) create a project → **APIs & Services → OAuth consent
   screen** → External, add the app name and your email → publish it.
2. **Credentials → Create credentials → OAuth client ID → Web application.**
3. Under **Authorized redirect URIs** add `https://YOUR-APP.streamlit.app/oauth2callback`
   (and `http://localhost:8501/oauth2callback` for local testing).
4. Copy the client ID and client secret.

**3 · Paste the secrets** into Streamlit Cloud → your app → **Settings → Secrets**, following
[`.streamlit/secrets.toml.example`](.streamlit/secrets.toml.example): the `[auth]` block, the
`[connections.progress_db]` block, and optionally `GEMINI_API_KEY`. Save — the app restarts with sign-in enabled.

If `[auth]` is set but no database is, progress is stored in a local SQLite file: fine on your own computer, but
it is wiped whenever Community Cloud restarts the app.

## Free AI keys

- **Google Gemini**: [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
- **Groq**: [console.groq.com/keys](https://console.groq.com/keys)

Keys pasted in the app stay in the user's session only and are never stored.

## Exam facts used

From the official GATE 2027 site ([gate2027.iitm.ac.in](https://gate2027.iitm.ac.in), organised by IIT Madras):
exam on 6, 7, 13, 14, 20 and 21 February 2027; 65 questions, 100 marks, 3 hours; GA 15 marks, Engineering Mathematics 13 marks, core 72 marks; negative marking only for MCQs. Per-subject core weights in the app are approximations from recent papers, used only for prioritising. Always check the official site for the latest notices.

## Project layout

```
app.py                  navigation + sidebar
views/                  one file per page
gate/data/questions.py  question bank (add your own here)
gate/data/syllabus.py   GATE 2027 CS syllabus + weights
gate/data/notes.py      revision sheets
gate/scoring.py         GATE marking scheme
gate/planner.py         study-plan generator
gate/ai.py              Gemini / Groq tutor client
tests/                  answer verification + app smoke tests
```

## Contributing questions

Add entries to `gate/data/questions.py` using the `Q(...)` helper. For numerical questions, add an independent check in `tests/test_bank.py`. Run `python -m pytest -q` before opening a pull request — every computed answer in the bank is verified by code.

## License

MIT. Questions are original and written for this project; they are not copied from past GATE papers.
