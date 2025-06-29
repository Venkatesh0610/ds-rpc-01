import streamlit as st

st.set_page_config(page_title="About - FinEdge", layout="wide")
query_params = st.query_params
username = (
    query_params.get("username", ["Guest"])
    if query_params.get("username")
    else st.session_state.get("username", "Guest")
)
page = query_params.get("page", [None]) if query_params.get("page") else None
print("Page details================",username,page)
if page == "features":
    st.session_state.page = "features"
    st.session_state["logged_in"] = True
    st.switch_page("pages/feature.py")
elif page == "about":
    st.session_state.page = "about"
    st.session_state["logged_in"] = True
    st.switch_page("pages/about.py")
elif page == "auth_page":
    st.session_state.page = "auth_page"
    st.session_state["logged_in"] = True
    st.switch_page("pages/_auth_page.py")
elif page == "home":
    st.query_params["page"] = "main_content"
    st.query_params["username"] = query_params.get("username")
    st.session_state["username"] = query_params.get("username")
    st.session_state["logged_in"] = True
    st.switch_page("pages/main_content.py")

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
.profile-container {{
    margin-top: 60px;
    text-align: center;
}}
.profile-pic {{
    width: 140px;
    height: 140px;
    border-radius: 50%;
    object-fit: cover;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}}
.profile-name {{
    font-size: 28px;
    font-weight: 700;
    margin-top: 15px;
    color: #333;
}}
.profile-desc {{
    font-size: 16px;
    color: #666;
    max-width: 600px;
    margin: 15px auto;
}}
.social-icons {{
    margin-top: 20px;
}}
.social-icons a {{
    margin: 0 10px;
    text-decoration: none;
}}
.social-icons img {{
    width: 32px;
    height: 32px;
    transition: transform 0.2s ease-in-out;
}}
.social-icons img:hover {{
    transform: scale(1.1);
}}
</style>

<div class="header-container">
    <div class="header-logo">FinEdge.</div>
    <div class="header-nav">
        <a href="?page=home&username={username}" target="_self">Home</a>
        <a href="?page=features&username={username}" target="_self">Features</a>
        <a href="?page=about&username={username}" target="_self">About</a>
    </div>
    <div style="display: flex; align-items: center; gap: 15px;">
    </div>
</div>

<div class="profile-container">
    <img class="profile-pic" src="https://avatars.githubusercontent.com/u/62538952?s=400&u=85437376424597075f61b8ef9a90f0aa0a3565bb&v=4" alt="Profile Picture"/>
    <div class="profile-name">A Venkatesh</div>
    <div class="profile-desc">
        Hi, I'm a Senior AI/ML Analyst
with 4+ years of experience in computer vision, ML, deep learning, and LLMs, I build smart solutions and love sharing AI insights through my content on YouTube, Medium, and more.
    </div>
    <div class="social-icons">
        <a href="http://www.youtube.com/@avenkatesh0610" target="_blank"><img src="https://img.icons8.com/ios-filled/50/FF0000/youtube-play.png" alt="YouTube"/></a>
        <a href="http://linkedin.com/in/venkatesh-a-400459191" target="_blank"><img src="https://img.icons8.com/ios-filled/50/0077B5/linkedin.png" alt="LinkedIn"/></a>
        <a href="http://medium.com/@avenkatesh0610" target="_blank"><img src="https://img.icons8.com/ios-filled/50/000000/medium-logo.png" alt="Medium"/></a>
        <a href="https://github.com/Venkatesh0610" target="_blank"><img src="https://img.icons8.com/ios-filled/50/000000/github.png" alt="GitHub"/></a>
    </div>
</div>
""", unsafe_allow_html=True)
