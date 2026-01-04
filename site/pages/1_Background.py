import streamlit as st
from utils import inject_css
import os

inject_css()

st.write(os.listdir(".."))

with open("../mkdwn/background.md", "r") as f:
    markd = f.read()

st.write(markd)
