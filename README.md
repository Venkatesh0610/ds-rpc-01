# 🤖 FinBot – Role-Based Internal AI Assistant

A secure, intelligent AI chatbot for internal use, built with **Streamlit**, **FastAPI**, **JWT Auth**, and **RAG using FAISS**. Powered by **Groq's `llama3-8b-8192` model**, FinBot delivers **role-specific insights** in real time with blazing speed.

https://youtu.be/0Bfxs5S0HyM

---

## ⚡ Tech Stack

- 🎨 **Streamlit** – Interactive UI with login, chatbot, and static pages  
- 🚀 **FastAPI** – API backend for authentication and RAG-based chat  
- 🔐 **JWT Authentication** – Manages secure logins and session state  
- 📁 **FAISS** – Fast vector retrieval for contextual responses  
- 🧠 **Groq + LLaMA 3** – Ultra-fast LLM responses via `llama3-8b-8192`  
- 🔎 **RAG (Retrieval-Augmented Generation)** – Factual, role-specific answers

---

## 📌 Features

- 🔐 **Role-Based Access Control (RBAC)**  
  Chatbot access is restricted by department role after login (e.g., HR, Finance, etc.).

- 💬 **Groq-Powered Chatbot (RAG + LLaMA 3)**  
  Leverages FAISS vector store and `llama3-8b-8192` via Groq API to provide smart, fast answers.

- 🖼️ **Streamlit Frontend**  
  Includes homepage with chatbot (for logged-in users), feature highlights, about, and contact.

- 🧠 **Conversation Memory**  
  Maintains context for more natural and informative interactions.

- 🛡️ **JWT Authentication**  
  Secure login/logout system stored in `users.json`.

- 📄 **Dynamic Vector Store**  
  Vectors generated from role-specific documents using FastAPI endpoint.

---

## 🗂️ Project Structure

```
.
├── app/                       # Backend FastAPI code and vector logic
│   ├── faiss_vectors/         # Stored vector DBs per role
│   ├── main.py                # FastAPI backend with all APIs
│   ├── users.json             # JSON database for registered users
│   ├── pages/                 # Streamlit frontend pages
│   │   ├── _auth_page.py      # Login/Register UI
│   │   ├── about.py           # About me page
│   │   ├── features.py        # Feature showcase
│   │   └── main_content.py    # Homepage with chatbot (role-gated)
│   └── resources/             # Role-specific document sources
│
├── app.py                     # Main Streamlit application entry point (outside app/)
```

---

## ⚙️ Setup Instructions

### 🔧 Backend (FastAPI)

```bash
cd app
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate (Windows)
pip install -r requirements.txt
```

Create your `.env` file in the `app/` directory:

```env
GROQ_API_KEY=your_groq_api_key
```

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

---

### 🖼️ Frontend (Streamlit)

```bash
streamlit run app.py
```

If using a deployed backend, update your Streamlit `secrets.toml`:

```toml
[api]
base_url = "https://your-fastapi-url.com"
```

---

## 🔐 Roles & Access

| Role         | Access Scope                                       |
|--------------|----------------------------------------------------|
| HR           | Employee data, attendance, payroll, policies       |
| Finance      | Expenses, budgets, and revenue                     |
| Marketing    | Campaigns, leads, customer engagement              |
| Engineering  | DevOps docs, architecture, release notes           |
| C-Level Exec | Full access to all departmental data               |
| Employee     | General HR policies and FAQs                       |

---

## 💬 Sample User Queries

* **HR**: *"Who has the most leave balance left this year?"*  
* **Finance**: *"List all Q2 reimbursements over ₹10,000."*  
* **Engineering**: *"Explain the current CI/CD pipeline."*  
* **Employee**: *"Where do I check leave application status?"*

---

## 🚀 Deployment

| Component | Status        |
|----------|----------------|
| Backend  | FastAPI (local or hosted) |
| Frontend | Streamlit Cloud / Local   |

---

## 👤 About the Developer

Built by **A Venkatesh** as part of an advanced internal chatbot system for secure and role-aware information access, powered by **Groq’s blazing-fast LLMs** and **modern AI tooling**.

---

## 🪪 License

This project is for educational and demo purposes. Please credit if reused or extended.
