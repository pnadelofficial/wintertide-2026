import streamlit as st
from utils import inject_css 

inject_css()

st.title("Wintertide Feast")
st.write("January 18th, 2026")

st.write("""
This site contains all of the information that you need to participate in the Wintertide Feast. Let me know if you have any questions. 

-- Peter

""".strip())

