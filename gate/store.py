"""Per-user progress storage for signed-in students.

Uses the SQL connection named "progress_db" from Streamlit secrets, e.g. a free Supabase Postgres:

    [connections.progress_db]
    url = "postgresql+psycopg2://USER:PASSWORD@HOST:6543/postgres"

Without that secret it falls back to a local SQLite file, which is fine on your own computer but is
wiped whenever Streamlit Community Cloud restarts the app.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone

import streamlit as st
from sqlalchemy import text

LOCAL_URL = "sqlite:///gate_ace_progress.db"

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


def _secrets_has_db() -> bool:
    try:
        return "progress_db" in st.secrets.get("connections", {})
    except Exception:  # no secrets file at all
        return False


def is_persistent() -> bool:
    """True when progress goes to an external database that survives app restarts."""
    return _secrets_has_db()


@st.cache_resource(show_spinner=False)
def _ready(url_hint: str) -> bool:
    """Create the table once per process."""
    conn = _conn()
    with conn.session as s:
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


def load(user_id: str) -> dict | None:
    with _session() as s:
        row = s.execute(text("SELECT data FROM gate_progress WHERE user_id = :uid"), {"uid": user_id}).first()
    return json.loads(row[0]) if row else None


def save(user_id: str, email: str | None, data: dict) -> None:
    with _session() as s:
        s.execute(text(UPSERT), {
            "uid": user_id, "email": email, "data": json.dumps(data),
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        })
        s.commit()


def delete(user_id: str) -> None:
    with _session() as s:
        s.execute(text("DELETE FROM gate_progress WHERE user_id = :uid"), {"uid": user_id})
        s.commit()
