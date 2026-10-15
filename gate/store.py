"""Progress storage for the signed-in users, plus a cache of AI deep-dive lessons.

Progress backend (first one configured in Streamlit secrets wins):
1. SQL database   — [connections.progress_db] url = "postgresql+psycopg2://…"
2. Private GitHub Gist — GITHUB_TOKEN = "ghp_…" (classic token with only the "gist" scope).
   The app creates one private gist in your account and keeps one JSON file per user in it.
3. Local SQLite file — fine on your own computer, but wiped whenever Streamlit Cloud restarts the app.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone

import requests
import streamlit as st
from sqlalchemy import text

LOCAL_URL = "sqlite:///gate_ace_progress.db"
GIST_DESC = "GATE CS Ace — saved progress (private, managed by the app)"
GH_API = "https://api.github.com"

DDL = """
CREATE TABLE IF NOT EXISTS gate_progress (
    user_id    VARCHAR(255) PRIMARY KEY,
    email      VARCHAR(255),
    data       TEXT NOT NULL,
    updated_at VARCHAR(40) NOT NULL
)
"""

UPSERT = """
INSERT INTO gate_progress (user_id, email, data, updated_at)
VALUES (:uid, :email, :data, :ts)
ON CONFLICT (user_id) DO UPDATE
SET email = excluded.email, data = excluded.data, updated_at = excluded.updated_at
"""


def _secret(name: str):
    try:
        return st.secrets.get(name)
    except Exception:  # no secrets file at all
        return None


def _secrets_has_db() -> bool:
    try:
        return "progress_db" in st.secrets.get("connections", {})
    except Exception:
        return False


def backend() -> str:
    if _secrets_has_db():
        return "sql"
    if _secret("GITHUB_TOKEN"):
        return "gist"
    return "local"


def is_persistent() -> bool:
    """True when progress survives Streamlit Cloud restarts."""
    return backend() in ("sql", "gist")


# ------------------------------------------------------------------ SQL (database or local file)
@st.cache_resource(show_spinner=False)
def _ready(url_hint: str) -> bool:
    with _conn().session as s:
        s.execute(text(DDL))
        s.commit()
    return True


def _conn():
    if _secrets_has_db():
        return st.connection("progress_db", type="sql")
    return st.connection("progress_db_local", type="sql", url=LOCAL_URL)


def _session():
    _ready("db" if _secrets_has_db() else LOCAL_URL)
    return _conn().session


def _sql_load(user_id: str) -> dict | None:
    with _session() as s:
        row = s.execute(text("SELECT data FROM gate_progress WHERE user_id = :uid"), {"uid": user_id}).first()
    return json.loads(row[0]) if row else None


def _sql_save(user_id: str, email: str | None, data: dict) -> None:
    with _session() as s:
        s.execute(text(UPSERT), {"uid": user_id, "email": email, "data": json.dumps(data),
                                 "ts": datetime.now(timezone.utc).isoformat(timespec="seconds")})
        s.commit()


# ------------------------------------------------------------------ private GitHub Gist
def _gh_headers() -> dict:
    return {"Authorization": f"Bearer {_secret('GITHUB_TOKEN')}", "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"}


def _gh(method: str, path: str, **kw) -> dict:
    r = requests.request(method, GH_API + path, headers=_gh_headers(), timeout=20, **kw)
    if r.status_code >= 300:
        raise RuntimeError(f"GitHub API {r.status_code}: {r.text[:200]}")
    return r.json()


@st.cache_resource(show_spinner=False)
def _gist_id(token_fingerprint: str) -> str:
    """Find (or create once) the app's private gist in the token owner's account."""
    if _secret("GIST_ID"):
        return _secret("GIST_ID")
    page = 1
    while True:
        gists = _gh("GET", f"/gists?per_page=100&page={page}")
        for g in gists:
            if g.get("description") == GIST_DESC:
                return g["id"]
        if len(gists) < 100:
            break
        page += 1
    g = _gh("POST", "/gists", json={
        "description": GIST_DESC, "public": False,
        "files": {"README.md": {"content": "Saved progress for the GATE CS Ace app. Don't rename this gist."}}})
    return g["id"]


def _gist() -> str:
    tok = _secret("GITHUB_TOKEN") or ""
    return _gist_id(hashlib.sha256(tok.encode()).hexdigest()[:16])


def _fname(user_id: str) -> str:
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in user_id)
    return f"progress-{safe}.json"


def _gist_load(user_id: str) -> dict | None:
    g = _gh("GET", f"/gists/{_gist()}")
    f = g.get("files", {}).get(_fname(user_id))
    if not f:
        return None
    content = f.get("content")
    if f.get("truncated") or content is None:
        r = requests.get(f["raw_url"], headers=_gh_headers(), timeout=20)
        r.raise_for_status()
        content = r.text
    return json.loads(content)


def _gist_save(user_id: str, data: dict) -> None:
    _gh("PATCH", f"/gists/{_gist()}", json={"files": {_fname(user_id): {"content": json.dumps(data)}}})


# ------------------------------------------------------------------ public API
def load(user_id: str) -> dict | None:
    if backend() == "gist":
        return _gist_load(user_id)
    return _sql_load(user_id)


def save(user_id: str, email: str | None, data: dict) -> None:
    if backend() == "gist":
        _gist_save(user_id, data)
    else:
        _sql_save(user_id, email, data)


# ------------------------------------------------------------------ AI lesson cache (SQL / local file)
LESSON_DDL = """
CREATE TABLE IF NOT EXISTS gate_lessons (
    lesson_key VARCHAR(400) PRIMARY KEY,
    content    TEXT NOT NULL,
    created_at VARCHAR(40) NOT NULL
)
"""


def lesson_get(key: str) -> str | None:
    """Shared cache of AI deep-dive lessons, so each topic is generated once for everyone."""
    with _session() as s:
        s.execute(text(LESSON_DDL))
        row = s.execute(text("SELECT content FROM gate_lessons WHERE lesson_key = :k"), {"k": key}).first()
        s.commit()
    return row[0] if row else None


def lesson_put(key: str, content: str) -> None:
    with _session() as s:
        s.execute(text(LESSON_DDL))
        s.execute(text(
            "INSERT INTO gate_lessons (lesson_key, content, created_at) VALUES (:k, :c, :t) "
            "ON CONFLICT (lesson_key) DO UPDATE SET content = excluded.content, created_at = excluded.created_at"),
            {"k": key, "c": content, "t": datetime.now(timezone.utc).isoformat(timespec="seconds")})
        s.commit()
