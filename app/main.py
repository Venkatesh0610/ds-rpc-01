from fastapi import FastAPI, HTTPException, Depends, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Dict, Optional
from uuid import uuid4
import os
import json
import shutil
import warnings
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from langchain_community.document_loaders import DirectoryLoader, TextLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Initialize
load_dotenv()
warnings.filterwarnings("ignore")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "resources", "data")

HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

app = FastAPI(title="RAG Chatbot Auth API")

DB_FILE = "users.json"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Streamlit origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users():
    with open(DB_FILE, "w") as f:
        json.dump(users_db, f, indent=4)

users_db: Dict[str, Dict] = load_users()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user(username: str, password: str):
    for user_id, user_data in users_db.items():
        if user_data["username"] == username and user_data["password"] == password:
            return {"id": user_id, "username": username, "role": user_data["role"]}
    return None

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")
        user_id = payload.get("uid")
        if not username or not role or not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload.")
        return {"id": user_id, "username": username, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")

@app.post("/register")
def register(username: str = Form(...), password: str = Form(...), role: str = Form(...)):
    if any(u["username"] == username for u in users_db.values()):
        raise HTTPException(status_code=400, detail="Username already exists.")
    user_id = str(uuid4())
    users_db[user_id] = {"username": username, "password": password, "role": role}
    save_users()
    return {"message": f"User '{username}' registered successfully as '{role}'."}


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password.")

    # Mark user as logged in
    users_db[user["id"]]["logged_in"] = True
    save_users()

    token = create_access_token({
        "sub": user["username"],
        "uid": user["id"],
        "role": user["role"]
    })
    return {"access_token": token, "token_type": "bearer", "username": user["username"], "role": user["role"]}

@app.post("/logout")
def logout(username: str = Form(...)):
    for user_id, user_data in users_db.items():
        if user_data["username"] == username:
            user_data["logged_in"] = False
            save_users()
            return {"message": "Logged out successfully"}
    raise HTTPException(status_code=404, detail="User not found.")
@app.get("/get_user_status")
def get_user_status(username: str):
    for user_data in users_db.values():
        if user_data["username"] == username:
            return {
                "logged_in": user_data.get("logged_in", False),
                "role": user_data["role"]
            }
    raise HTTPException(status_code=404, detail="User not found.")


@app.get("/protected")
def protected(user=Depends(get_current_user)):
    return {"message": f"Hello {user['username']}! You are logged in as {user['role']}.", "user": user}

ATA_DIR = "./resources/data"
VECTOR_DIR = "./faiss_vectors"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

@app.post("/build_vectors")
def build_vectors():
    print("\n🚀 Starting vector building process...")
    logs = {}

    # 1. Reset vector storage
    if os.path.exists(VECTOR_DIR):
        print("🧹 Cleaning old vector directory...")
        shutil.rmtree(VECTOR_DIR)
    os.makedirs(VECTOR_DIR, exist_ok=True)
    print(f"📁 Vector directory ready: {VECTOR_DIR}")

    # 2. Iterate through each role
    for role in os.listdir(DATA_DIR):
        role_path = os.path.join(DATA_DIR, role)
        print(f"<UNK> Role {role} ready: {role_path}")
        if not os.path.isdir(role_path):
            continue

        print(f"\n🔍 Processing role: {role} {role_path}")
        all_docs = []

        # --- Load .md Files ---
        for fname in os.listdir(role_path):
            if fname.endswith(".md"):
                fpath = os.path.join(role_path, fname)
                try:
                    loader = TextLoader(fpath, encoding="utf-8")  # Specify encoding
                    docs = loader.load()
                    all_docs.extend(docs)
                    print(f"📄 Loaded .md file: {fname} ({len(docs)} docs)")
                except Exception as e:
                    print(f"❌ Skipping {fname}: {e}")

        # --- Load .csv Files ---
        for fname in os.listdir(role_path):
            print(fname.endswith)
            if fname.endswith(".csv"):
                fpath = os.path.join(role_path, fname)
                try:
                    loader = CSVLoader(file_path=fpath)
                    docs = loader.load()
                    all_docs.extend(docs)
                    print(f"🧾 Loaded .csv file: {fname} ({len(docs)} rows)")
                except Exception as e:
                    print(f"❌ Skipping CSV {fname}: {e}")

        if not all_docs:
            logs[role] = "⚠️ No valid documents found"
            print(logs[role])
            continue

        # 3. Chunk and store
        chunks = splitter.split_documents(all_docs)
        print(f"✂️ Created {len(chunks)} chunks for role: {role}")

        if not chunks:
            logs[role] = "⚠️ No chunks created"
            continue

        try:
            vectordb = FAISS.from_documents(chunks, embedding_model)
            role_vec_path = os.path.join(VECTOR_DIR, role)
            vectordb.save_local(role_vec_path)
            logs[role] = f"✅ {len(chunks)} chunks stored at {role_vec_path}"
            print(logs[role])
        except Exception as e:
            logs[role] = f"❌ Vector store creation failed: {e}"
            print(logs[role])

    print("\n✅ Vector building complete.\n")
    return {"status": "completed", "details": logs}

@app.post("/rag_chat")
def rag_chat(query: str = Form(...), role: str = Form(...)):
    print(f"\n🟦 Received RAG Chat Request")
    print(f"📝 Query: {query}")
    print(f"👤 Role: {role}")

    role = role.lower().strip()
    role_vector_path = os.path.join(VECTOR_DIR, role)

    if not os.path.exists(role_vector_path):
        msg = f"❌ No vector store found for role '{role}'"
        print(msg)
        raise HTTPException(status_code=404, detail=msg)

    try:
        print(f"📥 Loading vector store from: {role_vector_path}")
        vectordb = FAISS.load_local(
            folder_path=role_vector_path,
            embeddings=embedding_model,
            allow_dangerous_deserialization=True
        )
        retriever = vectordb.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 6,
                "lambda_mult": 0.6
            }
        )
        print("🔍 Querying vector store...")
        docs = retriever.invoke(query)
        print(docs)
        print(f"📄 Retrieved {len(docs)} relevant documents.")
    except Exception as e:
        msg = f"❌ Error retrieving documents: {e}"
        print(msg)
        raise HTTPException(status_code=500, detail=msg)

    if not docs:
        print("🚫 No relevant documents found.")
        return {"response": "No relevant information found."}

    context = "\n\n".join(doc.page_content for doc in docs)
    print(f"\n📚 Context for LLM:\n---\n{context[:500]}...\n---")

    prompt = PromptTemplate.from_template("""
    You are a secure, intelligent assistant named FinBot. Respond to user queries strictly based on their role and the given context.

    User Role: {role}  
    User Question: {query}

    Rules:
    - Only answer questions using the <context> provided.
    - Do **not** access or infer data for other roles.
    - If the query is outside the user's role or context, reply with:  
      "Access Denied: You are not authorized to view this information. Please ask something related to your role."
    - Do not mention “based on the context” or other filler. Just give the clean answer.
    - Use bullet points for clarity if listing items.
    - If applicable, include source document names only where mentioned.

    <context>
    {context}
    </context>
    """)

    llm = ChatGroq(model_name="llama3-8b-8192", api_key=GROQ_API_KEY)
    chain = LLMChain(llm=llm, prompt=prompt)

    try:
        print("🧠 Calling LLM to generate answer...")
        answer = chain.run({
            "context": context,
            "query": query,
            "role": role
        })
        print(f"✅ LLM Response: {answer[:300]}...\n")
    except Exception as e:
        msg = f"❌ LLM error: {e}"
        print(msg)
        raise HTTPException(status_code=500, detail=msg)

    return {"response": answer}

