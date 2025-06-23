import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="Features - FinEdge", layout="wide")

username = st.session_state.get("username", "Guest")


# --- Hide Sidebar ---
st.markdown("""
<style>
[data-testid="stSidebar"], [data-testid="collapsedControl"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown(f"""
<style>
.header-container {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 40px;
    background: linear-gradient(90deg, #6C5CE7, #8A2BE2);
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 1000;
}}
.header-logo {{
    font-size: 24px;
    font-weight: 700;
    color: white;
}}
.header-nav {{
    display: flex;
    gap: 30px;
}}
.header-nav a {{
    color: white;
    text-decoration: none;
    font-weight: 500;
    transition: color 0.3s ease;
}}
.header-nav a:hover {{
    color: #FFC107;
}}
.user-greeting {{
    font-weight: 600;
    color: #FFC107;
}}
.logout-button {{
    background-color: #f44336;
    color: white;
    padding: 10px 20px;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    border: none;
}}
.logout-button:hover {{
    background-color: #d32f2f;
}}
</style>

<script>
function handleLogout() {{
    window.parent.postMessage({{ type: 'streamlit:setSessionState', data: {{ logged_in: false }} }}, '*');
}}
</script>

<div class="header-container">
    <div class="header-logo">FinEdge.</div>
    <div class="header-nav">
        <a href="main_content">Home</a>
        <a href="?page=about">About</a>
        <a href="?page=feature">Features</a>
        <a href="?page=contact">Contact</a>
    </div>
    <div style="display: flex; align-items: center; gap: 15px;">
        <span class="user-greeting">Hello, {username}!</span>
        <button class="logout-button" onclick="handleLogout()">Logout</button>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Feature Cards ---
st.markdown("""
<style>
.feature-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 25px;
    margin-top: 40px;
    justify-content: center;
}
.feature-card {
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    padding: 30px;
    max-width: 300px;
    min-width: 280px;
    text-align: center;
    transition: transform 0.2s ease-in-out;
}
.feature-card:hover {
    transform: translateY(-8px);
}
.feature-icon {
    width: 60px;
    margin-bottom: 20px;
}
.feature-title {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 10px;
}
.feature-desc {
    font-size: 14px;
    color: #555;
}
</style>

<h2 style="text-align: center; margin-top: 30px;">Explore Our Core Features</h2>

<div class="feature-grid">
    <div class="feature-card">
        <img class="feature-icon" src="https://img.icons8.com/ios-filled/100/6C5CE7/lock--v1.png"/>
        <div class="feature-title">Role-Based Access</div>
        <div class="feature-desc">Secure and granular access based on roles and permissions.</div>
    </div>
    <div class="feature-card">
        <img class="feature-icon" src="https://img.icons8.com/ios-filled/100/6C5CE7/speech-bubble.png"/>
        <div class="feature-title">Natural Language Queries</div>
        <div class="feature-desc">Interact with the system using human-like language.</div>
    </div>
    <div class="feature-card">
        <img class="feature-icon" src="https://img.icons8.com/ios-filled/100/6C5CE7/data-configuration.png"/>
        <div class="feature-title">RAG-Powered Responses</div>
        <div class="feature-desc">Combines retrieval and generation for accurate answers.</div>
    </div>
    <div class="feature-card">
        <img class="feature-icon" src="https://img.icons8.com/ios-filled/100/6C5CE7/identification-documents.png"/>
        <div class="feature-title">Authentication</div>
        <div class="feature-desc">Smart login with role recognition for personalized access.</div>
    </div>
    <div class="feature-card">
        <img class="feature-icon" src="https://img.icons8.com/ios-filled/100/6C5CE7/server.png"/>
        <div class="feature-title">Data Reference</div>
        <div class="feature-desc">Bot replies are linked to the actual source documents.</div>
    </div>
</div>
""", unsafe_allow_html=True)
