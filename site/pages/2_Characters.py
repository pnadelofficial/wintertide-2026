import streamlit as st
from utils import inject_css

inject_css()
with open("../mkdwn/characters.md", "r") as f:
    markd = f.read()

st.markdown(markd)
