"""Member sign-in and saved-progress tests. GitHub Gist calls are faked, so no network is used."""
import json
import sys
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from gate import state  # noqa: E402

USERS = {"arth": {"name": "Arth", "password": "pw-arth-123"}, "riya": {"name": "Riya", "password": "pw-riya-456"}}


class FakeGist:
    """In-memory stand-in for the GitHub Gist API."""

    def __init__(self):
        self.gists = {}
        self.fail = False

    def request(self, method, url, headers=None, json=None, timeout=None):
        assert headers["Authorization"] == "Bearer tok"
        if self.fail:
            return Resp(503, {"message": "down"})
        path = url.replace("https://api.github.com", "")
        if method == "GET" and path.startswith("/gists?"):
            return Resp(200, [{"id": k, "description": v["description"]} for k, v in self.gists.items()])
        if method == "POST" and path == "/gists":
            gid = f"g{len(self.gists) + 1}"
            assert json["public"] is False
            self.gists[gid] = {"description": json["description"],
                               "files": {n: {"content": f["content"]} for n, f in json["files"].items()}}
            return Resp(201, {"id": gid})
        gid = path.split("/")[2]
        if method == "GET":
            return Resp(200, self.gists[gid])
        if method == "PATCH":
            for n, f in json["files"].items():
                self.gists[gid]["files"][n] = {"content": f["content"]}
            return Resp(200, self.gists[gid])
        raise AssertionError((method, url))


class Resp:
    def __init__(self, code, body):
        self.status_code, self._body = code, body
        self.text = str(body)

    def json(self):
        return self._body


@pytest.fixture
def gist(monkeypatch):
    fake = FakeGist()
    import gate.store as store
    monkeypatch.setattr(store.requests, "request", fake.request)
    return fake


def app(secrets):
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30)
    for k, v in secrets.items():
        at.secrets[k] = v
    at.run()
    assert not at.exception, at.exception
    return at


def sign_in(at, user, pw):
    at.text_input(key="login_user").input(user)
    at.text_input(key="login_pwd").input(pw)
    next(b for b in at.sidebar.button if b.label == "Sign in").click().run()
    assert not at.exception, at.exception


def answer_one(at):
    at.switch_page("views/practice.py").run()
    if at.radio:
        at.radio[0].set_value(0).run()
    elif at.text_input:
        at.text_input[0].input("1").run()
    else:
        at.checkbox[0].check().run()
    next(b for b in at.button if b.label == "Check answer").click().run()
    assert not at.exception, at.exception


def test_guest_has_no_way_to_save(gist):
    at = app({"users": USERS, "GITHUB_TOKEN": "tok"})
    labels = [b.label for b in at.sidebar.button]
    assert "Sign in" in labels
    assert not at.sidebar.get("download_button") and not at.sidebar.get("file_uploader")
    answer_one(at)
    assert gist.gists == {}  # nothing stored for a guest


def test_wrong_password_is_rejected(gist):
    at = app({"users": USERS, "GITHUB_TOKEN": "tok"})
    sign_in(at, "arth", "wrong")
    assert "_auth_user" not in at.session_state
    assert any("Wrong username or password" in e.value for e in at.sidebar.error)


def test_member_progress_saved_to_private_gist_and_reloaded(gist):
    at = app({"users": USERS, "GITHUB_TOKEN": "tok"})
    sign_in(at, "ARTH", "pw-arth-123")  # username is case-insensitive
    assert "Sign out" in [b.label for b in at.sidebar.button]
    answer_one(at)
    (gid, g), = gist.gists.items()
    saved = json.loads(g["files"]["progress-arth.json"]["content"])
    assert len(saved["attempts"]) == 1

    # a brand-new session (another day / device) gets it back after signing in
    at2 = app({"users": USERS, "GITHUB_TOKEN": "tok"})
    assert at2.session_state.progress["attempts"] == []
    sign_in(at2, "arth", "pw-arth-123")
    assert len(at2.session_state.progress["attempts"]) == 1

    # the other member has separate progress
    at3 = app({"users": USERS, "GITHUB_TOKEN": "tok"})
    sign_in(at3, "riya", "pw-riya-456")
    assert at3.session_state.progress["attempts"] == []


def test_guest_work_is_kept_when_member_signs_in(gist):
    at = app({"users": USERS, "GITHUB_TOKEN": "tok"})
    answer_one(at)
    sign_in(at, "arth", "pw-arth-123")
    assert len(at.session_state.progress["attempts"]) == 1
    (_, g), = gist.gists.items()
    assert len(json.loads(g["files"]["progress-arth.json"]["content"])["attempts"]) == 1


def test_failed_load_never_overwrites_saved_progress(gist):
    at = app({"users": USERS, "GITHUB_TOKEN": "tok"})
    sign_in(at, "arth", "pw-arth-123")
    answer_one(at)
    (_, g), = gist.gists.items()
    before = g["files"]["progress-arth.json"]["content"]

    gist.fail = True  # GitHub is down when the student comes back
    at2 = app({"users": USERS, "GITHUB_TOKEN": "tok"})
    sign_in(at2, "arth", "pw-arth-123")
    answer_one(at2)
    assert g["files"]["progress-arth.json"]["content"] == before
    assert any("saving is paused" in e.value for e in at2.sidebar.error)


def test_sign_out_returns_to_guest(gist):
    at = app({"users": USERS, "GITHUB_TOKEN": "tok"})
    sign_in(at, "riya", "pw-riya-456")
    next(b for b in at.sidebar.button if b.label == "Sign out").click().run()
    assert not at.exception
    assert "_auth_user" not in at.session_state
    assert at.session_state.progress["attempts"] == []


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


def test_token_found_even_when_pasted_under_a_user_section(gist):
    users = {"arth": dict(USERS["arth"]), "riya": dict(USERS["riya"], GITHUB_TOKEN="tok")}
    at = app({"users": users})
    sign_in(at, "arth", "pw-arth-123")
    assert any("saves automatically" in c.value for c in at.sidebar.caption)
    answer_one(at)
    (_, g), = gist.gists.items()
    assert "progress-arth.json" in g["files"]
