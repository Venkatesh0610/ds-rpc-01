import streamlit as st

# ------------- SESSION CHECK ----------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.stop()

# ------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Fintech Home | RAG Chatbot", layout="wide")

# ------------- PAGE CONTENT ----------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background: #f5f7fa;
    }

    .header-title {
        font-size: 40px;
        font-weight: 700;
        color: #2b2f77;
        margin-bottom: 10px;
    }
    .sub-title {
        font-size: 20px;
        font-weight: 400;
        color: #555;
        margin-bottom: 30px;
    }
    .section {
        font-size: 18px;
        margin-top: 20px;
        color: #333;
        line-height: 1.6;
    }
    .chat-icon {
        position: fixed;
        right: 25px;
        bottom: 25px;
        background: linear-gradient(135deg, #c850c0, #4158d0);
        color: white;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        text-align: center;
        line-height: 60px;
        font-size: 30px;
        cursor: pointer;
        z-index: 999;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .feature-box {
        background: #ffffff;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="header-title">💼 Welcome to FinEdge Internal Portal</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Your smart gateway to everything fintech — secure, fast, and role-based.</div>', unsafe_allow_html=True)

# Sections
st.markdown('''
<div class="section">
    <div class="feature-box">
        <h4>📊 Financial Reports & Dashboards</h4>
        Get real-time insights into revenue streams, cost analysis, and projections. Access depends on your department role.
    </div>
    <div class="feature-box">
        <h4>📢 Company Announcements</h4>
        Stay informed with regular updates, performance milestones, and strategic initiatives.
    </div>
    <div class="feature-box">
        <h4>📁 Document Center</h4>
        Access HR policies, compliance manuals, product briefs, and onboarding kits all in one place.
    </div>
    <div class="feature-box">
        <h4>🤝 Department Tools</h4>
        Tailored views and tools for Finance, HR, Engineering, Marketing, and C-level teams.
    </div>
</div>
''', unsafe_allow_html=True)

# Chat Icon Only (chatbox and logic will be added later)
st.markdown("""
    <div class="chat-icon" onclick="alert('Chatbot will be activated soon!')">
        💬
    </div>
""", unsafe_allow_html=True)
