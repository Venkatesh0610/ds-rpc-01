import streamlit as st
import requests

st.set_page_config(page_title="Auth | RAG Chatbot", layout="centered")
API_URL = "http://localhost:8000"

# Session initialization
if "mode" not in st.session_state:
    st.session_state.mode = "login"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "token" not in st.session_state:
    st.session_state.token = None

# --- If already logged in ---
if st.session_state.logged_in:
    st.success(f"✅ Welcome {st.session_state.username} ({st.session_state.role})")
    st.info("You now have access to the RAG Chatbot.")

    if st.button("🔒 Logout"):
        st.session_state.clear()
        st.rerun()
    st.stop()

# --- CSS Styling (modern web feel) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    background: #f2f2f2;
}

.wrapper {
    max-width: 400px;
    margin: 5vh auto;
    background: white;
    border-radius: 12px;
    box-shadow: 0 15px 25px rgba(0,0,0,0.1);
    overflow: hidden;
}

.title {
    padding: 30px;
    background: linear-gradient(135deg, #c850c0, #4158d0);
    color: white;
    font-size: 28px;
    text-align: center;
    font-weight: 600;
}

.form-container {
    padding: 30px;
}

input, select {
    width: 100%;
    padding: 12px;
    margin-top: 10px;
    margin-bottom: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
}

.stButton button {
    width: 100%;
    background: linear-gradient(135deg, #c850c0, #4158d0);
    color: white;
    padding: 12px;
    border: none;
    border-radius: 25px;
    font-size: 16px;
    margin-top: 10px;
}

.switch-link {
    text-align: center;
    margin-top: 15px;
    font-size: 14px;
}

.switch-link a {
    color: #4158d0;
    text-decoration: none;
    font-weight: 600;
}

.switch-link a:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

# Wrapper
st.markdown('<div class="wrapper">', unsafe_allow_html=True)

# Title
st.markdown(f'<div class="title">{"Login" if st.session_state.mode == "login" else "Register"}</div>', unsafe_allow_html=True)
st.markdown('<div class="form-container">', unsafe_allow_html=True)

# --- Login ---
if st.session_state.mode == "login":
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", placeholder="Enter your password", type="password")

    if st.button("Login"):
        res = requests.post(f"{API_URL}/login", data={
            "username": username,
            "password": password
        })

        if res.status_code == 200:
            token = res.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            protected = requests.get(f"{API_URL}/protected", headers=headers)

            if protected.ok:
                user_data = protected.json()["user"]
                st.session_state.logged_in = True
                st.session_state.token = token
                st.session_state.username = user_data["username"]
                st.session_state.role = user_data["role"]
                st.switch_page("pages/home_page.py")
            else:
                st.error("🔒 Invalid token or expired.")
        else:
            st.error("❌ Login failed. Check credentials.")

    st.markdown('<div class="switch-link">Not a member? <a href="#" onclick="window.location.reload()">Register now</a></div>', unsafe_allow_html=True)
    if st.session_state.get("switch_to_register"):
        st.session_state.mode = "register"
        st.session_state.switch_to_register = False

# --- Register ---
elif st.session_state.mode == "register":
    username = st.text_input("Username", placeholder="Choose a username")
    password = st.text_input("Password", placeholder="Create a password", type="password")

    role_labels = {
        "engineering": "⚙️ Engineering",
        "marketing": "📢 Marketing",
        "finance": "💰 Finance",
        "hr": "👥 HR",
        "employee": "🧑‍💼 Employee",
        "c-suite": "🏢 C-Level Executive"
    }

    role = st.selectbox("Role", list(role_labels.keys()), format_func=lambda x: role_labels[x])

    if st.button("Register"):
        if username and password:
            res = requests.post(f"{API_URL}/register", data={
                "username": username,
                "password": password,
                "role": role
            })
            if res.status_code == 200:
                st.success("🎉 Registration successful! Please login now.")
                st.session_state.mode = "login"
                st.rerun()
            else:
                st.error(f"❌ {res.json().get('detail', 'Registration failed.')}")
        else:
            st.warning("⚠️ Fill in all fields to register.")

    st.markdown('<div class="switch-link">Already have an account? <a href="#" onclick="window.location.reload()">Login</a></div>', unsafe_allow_html=True)

# Close wrapper
st.markdown('</div></div>', unsafe_allow_html=True)
