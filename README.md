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

Without any `[users]` in secrets, everyone uses guest mode (progress isn't saved). On your own machine you can
auto-save guest progress to a file instead:

```bash
GATE_ACE_AUTOSAVE=~/gate-progress.json streamlit run app.py
```

## Deploy free on Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
2. **Create app** → pick this repo, branch `main`, main file `app.py` → **Deploy**.
3. *(Optional)* In **App settings → Secrets**, add `GEMINI_API_KEY = "..."` so every visitor gets a working AI tutor without their own key. See `.streamlit/secrets.toml.example`.

## Member sign-in (only the people you choose can save progress)

Anyone can open the app and use every feature as a **guest**, but guests' progress is never saved and there is no
download/upload option. Only the users you list in the app's Secrets can sign in, and their progress is saved
automatically after every answer, so it's there on any device.

**Setup — about 3 minutes, all on two web pages:**

1. **Create a GitHub token** (this is where the members' progress is stored, in one *private* gist in your account):
   open [this link](https://github.com/settings/tokens/new?scopes=gist&description=GATE%20CS%20Ace), make sure
   **only "gist"** is ticked, choose an expiry (e.g. "No expiration" or 1 year), click **Generate token**, and copy it.
2. **Paste the secrets:** on [share.streamlit.io](https://share.streamlit.io) open your app → **⋮ → Settings →
   Secrets**, paste the block below with your own usernames, names and passwords, and **Save**:

```toml
[users.arth]
name = "Arth"
password = "choose-a-long-password"

[users.friend]
name = "Friend's name"
password = "another-long-password"

GITHUB_TOKEN = "ghp_paste-your-token-here"
```

The app restarts and shows **🔑 Member sign-in** in the sidebar. To add a third person later, add another
`[users.name]` block. To remove someone, delete their block.

Notes
- Usernames aren't case-sensitive. Use long passwords; anyone who knows one can sign in as that user.
- If a member practised as a guest first and then signs in, that session's work is added to their account.
- If GitHub can't be reached when a member signs in, saving pauses (so their saved progress is never overwritten)
  until the page is refreshed.
- Prefer a database? Add a `[connections.progress_db]` URL (any Postgres, e.g. free Supabase) and it's used instead.

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
