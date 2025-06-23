import streamlit as st
import streamlit.components.v1 as components

# --- Page Configuration ---
st.set_page_config(page_title="Finbot Chat", layout="wide")

# --- Auth Check (important for all pages) ---
logged_in = st.session_state.get("logged_in", False)
username = st.session_state.get("username", "Guest")

if not logged_in:
    st.switch_page("pages/_auth_page.py") # Redirect to auth if not logged in
    st.stop()

# --- Custom CSS for the chatbot page ---
st.markdown("""
<style>
/* General body background for this page */
body {
    background-color: #f0f2f6; /* Light greyish-blue background */
    margin: 0;
    padding: 0;
}

/* Streamlit specific hides/adjustments */
[data-testid="stSidebar"], [data-testid="collapsedControl"] {
    display: none !important;
}
.stApp {
    background-color: #f0f2f6; /* Apply background to the entire Streamlit app container */
}

/* Header Styling (can be re-used or simplified for this page) */
.header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 40px;
    background: linear-gradient(90deg, #6C5CE7, #8A2BE2); /* Purple to Violet gradient */
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    position: sticky; /* Make header stick */
    top: 0; /* Stick to the top */
    z-index: 1000; /* Ensure it's above other content */
    width: 100%; /* Ensure it spans full width */
    box-sizing: border-box; /* Include padding in width */
}
.header-logo {
    font-size: 24px;
    font-weight: 700;
    color: white; /* White color for logo on gradient background */
}
.header-nav {
    display: flex;
    gap: 30px;
}
.header-nav a {
    color: white; /* White color for navigation links */
    text-decoration: none;
    font-weight: 500;
    transition: color 0.3s ease;
}
.header-nav a:hover {
    color: #FFC107; /* Amber on hover */
}
.user-greeting {
    font-weight: 600;
    color: #FFC107; /* Amber for greeting */
}
.logout-button {
    background-color: #f44336;
    color: white;
    padding: 10px 20px;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    border: none;
}
.logout-button:hover {
    background-color: #d32f2f;
}

/* Chatbot container for the dedicated page */
.chatbot-page-container {
    display: flex;
    justify-content: center; /* Center the chatbot horizontally */
    align-items: center; /* Center the chatbot vertically */
    min-height: calc(100vh - 70px); /* Adjust height for header, 70px approx header height */
    padding: 20px;
    box-sizing: border-box;
}

.chat-window {
    width: 100%; /* Take full width of its container (which is centered) */
    max-width: 600px; /* Max width for readability */
    height: 70vh; /* Make it tall on the page */
    background-color: white;
    border-radius: 15px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.25);
    overflow: hidden;
    display: flex;
    flex-direction: column;
}

.chat-header {
    background: linear-gradient(135deg, #4158d0, #c850c0);
    color: white;
    padding: 15px;
    text-align: center;
    font-weight: bold;
    font-size: 18px;
}

#chatMessages {
    flex: 1;
    padding: 15px;
    overflow-y: auto;
    background-color: #f7f7f7;
    display: flex;
    flex-direction: column;
    scroll-behavior: smooth;
}

.message {
    padding: 10px 14px;
    border-radius: 12px;
    font-size: 15px;
    max-width: 80%;
    margin: 8px 0;
}

.message.user {
    background-color: #e0f7fa; /* Light blue */
    align-self: flex-end;
}

.message.bot {
    background-color: #eeeeee; /* Light grey */
    align-self: flex-start;
}

.chat-input {
    padding: 15px;
    border-top: 1px solid #ccc;
    background-color: #fff;
}

.chat-input input {
    width: 100%;
    padding: 12px;
    font-size: 16px;
    border-radius: 8px;
    border: 1px solid #ddd;
    outline: none;
}
</style>
""", unsafe_allow_html=True)

# --- Header (re-use the same header structure for consistency) ---
st.markdown(f"""
<div class="header-container">
    <div class="header-logo">FinEdge.</div>
    <div class="header-nav">
        <a href="/">Home</a> <a href="#about">About</a>
        <a href="#features">Features</a>
        <a href="#contact">Contact</a>
    </div>
    <div style="display: flex; align-items: center; gap: 15px;">
        <span class="user-greeting">Hello, {username}!</span>
        <button class="logout-button" onclick="handleLogout()">Logout</button>
    </div>
</div>
<script>
function handleLogout() {{
    window.parent.postMessage({{ type: 'streamlit:setSessionState', data: {{ logged_in: false }} }}, '*');
}}
</script>
""", unsafe_allow_html=True)

# --- Chatbot content for the dedicated page ---
st.markdown("""
<div class="chatbot-page-container">
    <div class="chat-window" id="chatWindow">
        <div class="chat-header">FinBot</div>
        <div id="chatMessages">
            <div class="message bot"><strong>FinBot:</strong> Hello 👋 I'm your AI assistant. How can I help you today?</div>
        </div>
        <div class="chat-input">
            <input type="text" id="chatInput" placeholder="Type your message..." onkeydown="handleEnter(event)">
        </div>
    </div>
</div>

<script>
function handleEnter(event) {
    if (event.key === "Enter") {
        const input = document.getElementById("chatInput");
        const msg = input.value.trim();
        if (msg !== "") {
            const chat = document.getElementById("chatMessages");
            chat.innerHTML += `<div class='message user'><strong>You:</strong> ${msg}</div>`;
            // Simulate bot response - In a real app, this would be an API call
            chat.innerHTML += `<div class='message bot'><strong>FinBot:</strong> I received your message: "${msg}". This is a demo response.</div>`;
            input.value = "";
            setTimeout(() => {
                chat.scrollTop = chat.scrollHeight;
            }, 100);
        }
    }
}
</script>
""", unsafe_allow_html=True)