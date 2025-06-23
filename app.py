import streamlit as st

st.set_page_config(page_title="FinEdge Portal", layout="wide")

# Initialize session state safely
st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("username", None)
st.session_state.setdefault("role", None)
st.session_state.setdefault("token", None)

# Redirect to main content page
st.switch_page("pages/main_content.py")

# This part won't be executed after switch_page
