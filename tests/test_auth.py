"""Sign-in and per-user storage tests (simulated user; real Google login needs live credentials)."""
import sys
from pathlib import Path

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from gate import state  # noqa: E402

AUTH = {"redirect_uri": "http://localhost:8501/oauth2callback", "cookie_secret": "x" * 32,
        "client_id": "id", "client_secret": "secret",
        "server_metadata_url": "https://accounts.google.com/.well-known/openid-configuration"}


def app(monkeypatch, user, tmp_path):
    monkeypatch.chdir(tmp_path)  # local SQLite file lands in a temp folder
    monkeypatch.setattr(state, "current_user", lambda: user)
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30)
    at.secrets["auth"] = AUTH
    at.run()
    assert not at.exception, at.exception
    return at


def test_guest_sees_sign_in(monkeypatch, tmp_path):
    at = app(monkeypatch, None, tmp_path)
    labels = [b.label for b in at.sidebar.button]
    assert "Sign in with Google" in labels


def test_signed_in_progress_is_saved_and_reloaded(monkeypatch, tmp_path):
    user = {"id": "google-123", "email": "student@example.com", "name": "Asha Rao"}
    at = app(monkeypatch, user, tmp_path)
    assert "Sign out" in [b.label for b in at.sidebar.button]
    at.switch_page("views/practice.py").run()
    if at.radio:
        at.radio[0].set_value(0).run()
    elif at.text_input:
        at.text_input[0].input("1").run()
    else:
        at.checkbox[0].check().run()
    next(b for b in at.button if b.label == "Check answer").click().run()
    assert not at.exception, at.exception

    # a brand-new session for the same student (e.g. phone the next day) sees the attempt
    at2 = app(monkeypatch, user, tmp_path)
    assert len(at2.session_state.progress["attempts"]) == 1
    # a different student does not
    at3 = app(monkeypatch, {"id": "google-999", "email": "b@x.com", "name": "B"}, tmp_path)
    assert at3.session_state.progress["attempts"] == []


def test_combine_keeps_both_sides():
    a, b = state.default_progress(), state.default_progress()
    a["attempts"] = [{"qid": "GA01", "subject": "General Aptitude", "topic": "t", "correct": True, "marks": 1,
                      "ts": "2026-10-01T10:00:00", "mode": "practice"}]
    b["attempts"] = a["attempts"] + [{"qid": "GA02", "subject": "General Aptitude", "topic": "t", "correct": False,
                                      "marks": 0, "ts": "2026-10-02T10:00:00", "mode": "practice"}]
    b["bookmarks"] = ["EM01"]
    s = "Algorithms"
    t = next(iter(b["topic_status"][s]))
    b["topic_status"][s][t] = 3
    c = state.combine(a, b)
    assert [x["qid"] for x in c["attempts"]] == ["GA01", "GA02"]
    assert c["bookmarks"] == ["EM01"] and c["topic_status"][s][t] == 3
