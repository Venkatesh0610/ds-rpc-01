from fastapi import FastAPI, HTTPException, Depends, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Dict, Optional
from uuid import uuid4
import json
import os

app = FastAPI(title="RAG Chatbot Auth API", description="Handles user registration and JWT-based login")

# File path for user data
DB_FILE = "users.json"


# Load users from file
def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}


# Save users to file
def save_users():
    with open(DB_FILE, "w") as f:
        json.dump(users_db, f, indent=4)


# In-memory DB
users_db: Dict[str, Dict] = load_users()

# JWT config
SECRET_KEY = "supersecretkey"  # Change this in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# JWT token generator
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# User authenticator
def authenticate_user(username: str, password: str):
    for user_id, user_data in users_db.items():
        if user_data["username"] == username and user_data["password"] == password:
            return {"id": user_id, "username": username, "role": user_data["role"]}
    return None


# Decode and return current user from token
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


# ✅ Register endpoint
@app.post("/register")
def register(username: str = Form(...), password: str = Form(...), role: str = Form(...)):
    if any(u["username"] == username for u in users_db.values()):
        raise HTTPException(status_code=400, detail="Username already exists.")

    user_id = str(uuid4())
    users_db[user_id] = {
        "username": username,
        "password": password,
        "role": role
    }
    save_users()
    return {"message": f"User '{username}' registered successfully as '{role}'."}


# ✅ Login endpoint — returns JWT
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password.")

    token = create_access_token({
        "sub": user["username"],
        "uid": user["id"],
        "role": user["role"]
    })
    return {"access_token": token, "token_type": "bearer"}


# ✅ Protected route
@app.get("/protected")
def protected(user=Depends(get_current_user)):
    return {
        "message": f"Hello {user['username']}! You are logged in as {user['role']}.",
        "user": user
    }
