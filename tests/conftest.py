import os
import tempfile

import pytest
import streamlit as st


@pytest.fixture(autouse=True)
def isolated(monkeypatch):
    """Each test gets a fresh working folder (for the local SQLite file) and fresh Streamlit caches."""
    st.cache_resource.clear()
    st.cache_data.clear()
    with tempfile.TemporaryDirectory() as d:
        monkeypatch.chdir(d)
        yield
    st.cache_resource.clear()
