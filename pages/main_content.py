import streamlit as st
import streamlit.components.v1 as components
import os
import json


def restore_session_state():
    # Get username from query params (shared in link)
    query_params = st.session_state
    username = query_params.get("username")
    print("user name ---",username)
    base_dir = os.path.dirname(os.path.abspath(__file__))  # pages/
    users_file_path = os.path.abspath(os.path.join(base_dir, "..",'app', "users.json"))
    print(users_file_path)

    if username:
        try:
            with open(users_file_path, "r") as f:
                users = json.load(f)

            # ✅ Search through values (user objects)
            user = next((u for u in users.values() if u["username"] == username), None)

            if user and user.get("logged_in"):
                st.session_state["username"] = user["username"]
                st.session_state["logged_in"] = True
                st.session_state["role"] = user.get("role")
                print(f"✅ Session restored for {username}")
            else:
                print(f"❌ Not logged in or user not found: {username}")
                st.session_state["logged_in"] = False
                st.session_state["role"] = None

        except Exception as e:
            print(f"❌ Error loading users.json: {e}")
            st.session_state["logged_in"] = False
            st.session_state["role"] = None
    else:
        print("ℹ️ No username found in query params.")
        st.session_state["logged_in"] = False
        st.session_state["role"] = None
restore_session_state()

# --- Page Redirection Based on Query Params ---
query_params = st.query_params
page = query_params.get("page", [None])
if page == "features":
    print("setting the values",query_params,query_params.get("username"))
    st.query_params.update({
        "page": "features",
        "username": query_params.get("username")
    })
    st.session_state.username = query_params.get("username")
    st.session_state.page = "features"
    st.switch_page("pages/feature.py")
elif page == "about":
    st.query_params.update({
        "page": "about",
        "username": query_params.get("username")
    })
    st.session_state.username = query_params.get("username")
    st.session_state.page = "about"
    st.switch_page("pages/about.py")
elif page == "auth_page":
    st.query_params.update({
        "page": "auth_page",
        "username": query_params.get("username")
    })
    st.session_state.username = query_params.get("username")
    st.session_state.page = "auth_page"
    st.switch_page("pages/_auth_page.py")
elif page == "home":
    st.query_params.update({
        "page": "main_content",
        "username": query_params.get("username")
    })
    st.session_state.username = query_params.get("username")
    st.session_state.page = "main_content"
    st.switch_page("pages/main_content.py")

# --- Page Configuration ---
st.set_page_config(page_title="Fintech Portal", layout="wide")

print("===========",st.session_state)
# --- Auth Check FIRST ---
logged_in = st.session_state.get("logged_in", False)
username = st.session_state.get("username", "Guest")
role = st.session_state.get("role", None)

# --- THEN Handle Query Params ---
query_params = st.query_params
page = query_params.get("page", [None])[0]

# 👇 Determine login state
logged_in = st.session_state.get("logged_in", False)
username = st.session_state.get("username", "Guest")

# 👇 Conditionally render login/logout buttons
if logged_in:
    username = st.session_state.get("username", "User")
    header_buttons = f'''<div class="user-greeting"><b>Hi, {username}</b></div>
        <form action="?page=logout" method="get">
            <button class="logout-button" type="submit">Logout</button>
        </form>'''
else:
    header_buttons = f'''<div class="auth-buttons">
        <a href="?page=auth_page&mode=login&username={username}" target="_self" class="auth-button login-btn">Login</a>
        <a href="?page=auth_page&mode=register&username={username}" target="_self" class="auth-button register-btn">Register</a>
    </div>'''

msg = "test"
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
.user-greeting {{
    font-weight: 600;
    color: #FFC107;
    margin-right: 15px;
}}
.auth-button {{
    display: inline-block;
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    text-decoration: none;  /* 🔥 Removes underline */
    cursor: pointer;
    color: white;
    transition: background-color 0.3s ease;
}}

.login-btn {{
    background-color: #1E88E9; /* Blue */
}}

.login-btn:hover {{
    background-color: #6A5ACD;
}}

.register-btn {{
    background-color: #43A047; /* Green */
}}

.register-btn:hover {{
    background-color: #2E7D32;
}}

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

<div class="header-container">
    <div class="header-logo">FinEdge.</div>
    <div class="header-nav">
        <a href="?page=home&username={username}" target="_self">Home</a>
        <a href="?page=features&username={username}" target="_self">Features</a>
        <a href="?page=about&username={username}" target="_self">About</a>
    </div>
    <div style="display: flex; align-items: center; gap: 15px;">
        {header_buttons}
    </div>
</div>
""", unsafe_allow_html=True)



# --- Main Layout ---
col1, col2 = st.columns([3, 1])

# Left column for homepage content
with col1:
    st.markdown("""
    <style>
    .hero-min {
        background: linear-gradient(135deg, #6C5CE7, #9B59B6); /* Purple to Lighter Purple gradient */
        color: white;
        border-radius: 12px;
        padding: 40px;
        margin: 20px 0 30px 0;
        
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        text-align: center;
    }
    .hero-min h1 {
        font-size: 36px;
        margin-bottom: 10px;
        font-weight: 700;
    }
    .hero-min p {
        font-size: 16px;
        opacity: 0.9;
        margin-bottom: 25px;
    }
    .hero-min button {
        padding: 10px 24px;
        background-color: #4CAF50; /* Green button */
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        cursor: pointer;
        transition: background 0.3s ease;
    }
    .hero-min button:hover {
        background-color: #388e3c;
    }

    /* New Card Styles with Gradients and Images */
    .card-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        margin-top: 20px;
        justify-content: center; /* Center cards if they don't fill a row */
    }
    .colored-card {
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        padding: 20px;
        flex: 1;
        min-width: 280px;
        max-width: calc(50% - 20px);
        text-align: center; /* Center content for consistent look */
        transition: transform 0.2s ease-in-out;
        color: white; /* Default text color for colored cards */
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .colored-card:hover {
        transform: translateY(-5px);
    }
    .colored-card h4 {
        margin-top: 10px; /* Space for icon */
        font-size: 20px; /* Slightly larger for impact */
        color: inherit; /* Inherit color from parent card */
        margin-bottom: 8px;
    }
    .colored-card p {
        font-size: 14px;
        line-height: 1.5;
        margin-bottom: 0;
        color: inherit; /* Inherit color from parent card */
        opacity: 0.9;
    }
    .card-icon-img {
        width: 60px; /* Size of the image */
        height: 60px;
        margin-bottom: 10px;
        border-radius: 50%; /* Make images circular if desired */
        object-fit: cover; /* Ensures image covers area */
        background-color: rgba(255,255,255,0.2); /* Light background for icons */
        padding: 5px;
    }

    /* Specific gradient colors for Feature Cards */
    .feature-card-1 { background: linear-gradient(135deg, #FF6F61, #E53935); } /* Coral to Red */
    .feature-card-2 { background: linear-gradient(135deg, #4CAF50, #66BB6A); } /* Green to Light Green */
    .feature-card-3 { background: linear-gradient(135deg, #2196F3, #42A5F5); } /* Blue to Light Blue */
    .feature-card-4 { background: linear-gradient(135deg, #FFC107, #FFD54F); } /* Amber to Light Amber */
    .feature-card-5 { background: linear-gradient(135deg, #9C27B0, #BA68C8); } /* Deep Purple to Light Purple */

    /* Specific gradient colors for Roles Cards */
    .role-card-1 { background: linear-gradient(135deg, #FF5722, #F4511E); } /* Deep Orange */
    .role-card-2 { background: linear-gradient(135deg, #E91E63, #EC407A); } /* Pink */
    .role-card-3 { background: linear-gradient(135deg, #607D8B, #78909C); } /* Blue Grey */
    .role-card-4 { background: linear-gradient(135deg, #009688, #26A69A); } /* Teal */
    .role-card-5 { background: linear-gradient(135deg, #673AB7, #7E57C2); } /* Darker Purple */
    .role-card-6 { background: linear-gradient(135deg, #795548, #8D6E63); } /* Brown */

    /* Specific colors for Tech Stack Cards (white with subtle hover gradient) */
    .tech-stack-card {
        background-color: white; /* Keep tech stack cards white for contrast */
        border: 1px solid #ddd; /* Light border */
        color: #333; /* Dark text for white cards */
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        padding: 15px 20px;
        flex: 1;
        min-width: 150px;
        max-width: calc(33.333% - 20px);
        text-align: center;
        transition: all 0.2s ease-in-out;
    }
    .tech-stack-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
        background: linear-gradient(45deg, #e0f7fa, #e8f5e9); /* Subtle light gradient on hover */
    }
    .tech-stack-card h5 {
        margin: 0;
        font-size: 16px;
        color: #333;
        font-weight: 600;
        margin-bottom: 5px;
    }
    .tech-stack-card .tech-icon-img {
        width: 40px; /* Smaller icons for tech stack */
        height: 40px;
        margin-bottom: 5px;
        object-fit: contain; /* Contain to show full logo */
    }

    </style>

    <div class="hero-min">
        <h1>Welcome to FinEdge Portal</h1>
        <p>Access powerful tools & insights with FinBot, your smart AI assistant designed to simplify work across departments.</p>
        </div>

    <h2 style="text-align: center; color: #333; margin-top: 40px; margin-bottom: 20px;">Our Key Capabilities</h2>
    <div class="card-grid">
        <div class="colored-card feature-card-1">
            <img src="https://img.icons8.com/ios-filled/100/FFFFFF/lock--v1.png" alt="Security Icon" class="card-icon-img">
            <h4>Role-Based Access Control</h4>
            <p>Ensures secure and granular access to data based on user roles and permissions.</p>
        </div>
        <div class="colored-card feature-card-2">
            <img src="https://img.icons8.com/ios-filled/100/FFFFFF/speech-bubble.png" alt="Chat Icon" class="card-icon-img">
            <h4>Natural Language Processing</h4>
            <p>Understands and processes complex queries in natural language for intuitive interactions.</p>
        </div>
        <div class="colored-card feature-card-3">
            <img src="https://img.icons8.com/ios-filled/100/FFFFFF/data-configuration.png" alt="RAG Icon" class="card-icon-img">
            <h4>Retrieval-Augmented Generation (RAG)</h4>
            <p>Combines information retrieval with powerful language generation for insightful responses.</p>
        </div>
        <div class="colored-card feature-card-4">
            <img src="https://img.icons8.com/ios-filled/100/FFFFFF/identification-documents.png" alt="Auth Icon" class="card-icon-img">
            <h4>Authentication & Role Assignment</h4>
            <p>The chatbot authenticates users and assigns roles to personalize data access.</p>
        </div>
        <div class="colored-card feature-card-5">
            <img src="https://img.icons8.com/ios-filled/100/FFFFFF/server.png" alt="Data Icon" class="card-icon-img">
            <h4>Intelligent Data Handling</h4>
            <p>Responds with relevant departmental data, referencing original source documents.</p>
        </div>
    </div>

    <h2 style="text-align: center; color: #333; margin-top: 60px; margin-bottom: 20px;">Roles and Permissions</h2>
    <div class="card-grid">
        <div class="colored-card role-card-1">
            <img src="https://png.pngtree.com/png-vector/20190301/ourmid/pngtree-vector-stock-market-icon-png-image_747147.jpg" alt="Finance Icon" class="card-icon-img">
            <h4>Finance Team</h4>
            <p>Access to financial reports, marketing expenses, equipment costs, reimbursements.</p>
        </div>
        <div class="colored-card role-card-2">
            <img src="https://cdn-icons-png.flaticon.com/512/4547/4547422.png" alt="Marketing Icon" class="card-icon-img">
            <h4>Marketing Team</h4>
            <p>Access to campaign performance data, customer feedback, and sales metrics.</p>
        </div>
        <div class="colored-card role-card-3">
            <img src="https://img.icons8.com/ios-filled/100/FFFFFF/management.png" alt="HR Icon" class="card-icon-img">
            <h4>HR Team</h4>
            <p>Access to employee data, attendance records, payroll, and performance reviews.</p>
        </div>
        <div class="colored-card role-card-4">
            <img src="https://img.icons8.com/ios-filled/100/FFFFFF/services.png" alt="Engineering Icon" class="card-icon-img">
            <h4>Engineering Department</h4>
            <p>Access to technical architecture, development processes, and operational guidelines.</p>
        </div>
        <div class="colored-card role-card-5">
            <img src="https://cdn-icons-png.flaticon.com/512/71/71028.png" alt="C-Level Icon" class="card-icon-img">
            <h4>C-Level Executives</h4>
            <p>Full access to all company data.</p>
        </div>
        <div class="colored-card role-card-6">
            <img src="https://img.icons8.com/ios-filled/100/FFFFFF/user--v1.png" alt="Employee Icon" class="card-icon-img">
            <h4>Employee Level</h4>
            <p>Access only to general company information such as policies, events, and FAQs.</p>
        </div>
    </div>

    <h2 style="text-align: center; color: #333; margin-top: 60px; margin-bottom: 20px;">Our Tech Stack</h2>
    <div class="card-grid">
        <div class="tech-stack-card">
            <img src="https://img.icons8.com/color/96/python.png" alt="Python Icon" class="tech-icon-img">
            <h5>Python</h5>
        </div>
            <div class="tech-stack-card">
                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQgqHmPo-63nxV3scHcaP7x3QPw7RzjagCoig&s" alt="FastAPI Icon" class="tech-icon-img">
                <h5>FastAPI</h5>
            </div>
        <div class="tech-stack-card">
            <img src="https://img.icons8.com/color/96/streamlit.png" alt="Streamlit Icon" class="tech-icon-img">
            <h5>Streamlit</h5>
        </div>
        <div class="tech-stack-card">
            <img src="https://img.icons8.com/color/96/artificial-intelligence.png" alt="LLM Icon" class="tech-icon-img">
            <h5>LLMs (GPT-3/4, Llama)</h5>
        </div>
        <div class="tech-stack-card">
            <img src="https://img.icons8.com/color/96/database.png" alt="Vector Store Icon" class="tech-icon-img">
            <h5>Vector Store</h5>
        </div>
    </div>
    """, unsafe_allow_html=True)


# Right column for chatbot (bottom-right aligned inside column)
with col2:
    if logged_in:
        components.html(f"""
            <style>
            .chat-container {{
                position: relative;
                width: 100%;
                height: 500px;
            }}
    
            .chat-toggle {{
                position: absolute;
                bottom: 0;
                right: 0;
                background-color: #4CAF50;
                color: white;
                border-radius: 50%;
                width: 60px;
                height: 60px;
                font-size: 28px;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                transition: background 0.3s ease;
            }}
    
            .chat-toggle:hover {{
                background-color: #388e3c;
            }}
    
            .chat-window {{
                display: none;
                position: absolute;
                bottom: 80px;
                right: 0;
                width: 100%;
                height: 420px;
                background-color: white;
                border-radius: 15px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.25);
                overflow: hidden;
                flex-direction: column;
            }}
    
            .chat-window.open {{
                display: flex;
                flex-direction: column;
            }}
    
            .chat-header {{
                background: linear-gradient(135deg, #4158d0, #c850c0);
                color: white;
                padding: 12px;
                text-align: center;
                font-weight: bold;
                font-size: 16px;
            }}
    
            #chatMessages {{
                flex: 1;
                padding: 10px;
                overflow-y: auto;
                background-color: #f7f7f7;
                display: flex;
                flex-direction: column;
                scroll-behavior: smooth;
            }}
    
            .message {{
                padding: 10px 14px;
                border-radius: 12px;
                font-size: 14px;
                max-width: 85%;
                margin: 5px 0;
            }}
    
            .message.user {{
                background-color: #e0f7fa;
                align-self: flex-end;
            }}
    
            .message.bot {{
                background-color: #eeeeee;
                align-self: flex-start;
            }}
    
            .chat-input {{
                padding: 10px;
                border-top: 1px solid #ccc;
            }}
    
            .chat-input input {{
                width: 100%;
                padding: 10px;
                font-size: 14px;
                border-radius: 8px;
                border: 1px solid #ccc;
                outline: none;
            }}
            </style>
    
            <div class="chat-container">
                <div class="chat-toggle" onclick="toggleChat()">💬</div>
                <div class="chat-window" id="chatWindow">
                    <div class="chat-header">FinBot</div>
                    <div id="chatMessages">
                        <div class="message bot">Hello,{username}, how can I assist you today?</div>
                    </div>
                    <div class="chat-input">
                        <input type="text" id="chatInput" placeholder="Type your message..." onkeydown="handleEnter(event)">
                    </div>
                </div>
            </div>
    
            <script>
            function toggleChat() {{
                const chatWindow = document.getElementById("chatWindow");
                chatWindow.classList.toggle("open");
            }}
    
            function formatBotReply(text) {{
                return text
                    .replace(/\\n/g, "<br>")
                    .replace(/\\*\\*(.*?)\\*\\*/g, "<strong>$1</strong>")
                    .replace(/\\* (.*?)<br>/g, "• $1<br>");
            }}
    
            async function handleEnter(event) {{
                if (event.key === "Enter") {{
                    const input = document.getElementById("chatInput");
                    const msg = input.value.trim();
                    if (msg !== "") {{
                        const chat = document.getElementById("chatMessages");
                        chat.innerHTML += `<div class='message user'>${{msg}}</div>`;
                        input.value = "";
    
                        const formData = new FormData();
                        formData.append("query", msg);
                        formData.append("role", "{role}");
    
                        try {{
                            console.log("📤 Sending to /rag_chat");
                            const response = await fetch("http://localhost:8000/rag_chat", {{
                                method: "POST",
                                body: formData
                            }});
                            console.log("📥 Raw response:", response);
    
                            if (!response.ok) {{
                                throw new Error("Server returned error: " + response.status);
                            }}
    
                            const data = await response.json();
                            console.log("✅ Parsed response:", data);
    
                            const botReply = data.response || "Sorry, I couldn't find anything relevant.";
                            chat.innerHTML += `<div class='message bot'><br>${{formatBotReply(botReply)}}</div>`;
                        }} catch (error) {{
                            console.error("❌ Error during fetch or parse:", error);
                            chat.innerHTML += `<div class='message bot'>Sorry, something went wrong 😢</div>`;
                        }}
    
                        setTimeout(() => {{
                            chat.scrollTop = chat.scrollHeight;
                        }}, 100);
                    }}
                }}
            }}
            </script>
        """, height=600)
    else:
        st.warning("🔒 Please login to access FinBot (the chatbot assistant).")
