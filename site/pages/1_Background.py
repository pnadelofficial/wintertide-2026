import streamlit as st
from utils import inject_css

inject_css()
with open("/mount/src/wintertide-2026/site/mkdwn/background.md", "r") as f:
    markd = f.read()

st.write(markd)
