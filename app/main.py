from fastapi import FastAPI, HTTPException, Depends, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Dict, Optional

app = FastAPI(title="RAG Chatbot Auth API", description="Handles user registration and JWT-based login")

# In-memory users DB (replace with real DB in production)
users_db: Dict[str, Dict[str, str]] = {}

# JWT configuration
SECRET_KEY = "supersecretkey"  # Change this in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Create JWT token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Authenticate user from users_db
def authenticate_user(username: str, password: str):
    user = users_db.get(username)
    if not user or user["password"] != password:
        return None
    return {"username": username, "role": user["role"]}

# Decode and return current user info from token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")
        if not username or not role:
            raise HTTPException(status_code=401, detail="Invalid token payload.")
        return {"username": username, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")

# ✅ Registration endpoint
@app.post("/register")
def register(username: str = Form(...), password: str = Form(...), role: str = Form(...)):
    if username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists.")
    users_db[username] = {"password": password, "role": role}
    return {"message": f"User '{username}' registered successfully as '{role}'."}

# ✅ Login endpoint — returns JWT token
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password.")
    access_token = create_access_token(data={"sub": user["username"], "role": user["role"]})
    return {"access_token": access_token, "token_type": "bearer"}

# ✅ Protected endpoint to verify token
@app.get("/protected")
def protected_route(user=Depends(get_current_user)):
    return {
        "message": f"Hello {user['username']}, your role is '{user['role']}'.",
        "user": user
    }
