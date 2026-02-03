import random
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta

# 🔥 FORCE LOAD .env FROM PROJECT ROOT
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

from passlib.context import CryptContext
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from backend.models import User
from backend.database import SessionLocal
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.models import User

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"

if not SECRET_KEY:
    print("WARNING: JWT_SECRET_KEY not found in environment variables")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str):
    return pwd_context.hash(password[:72])


def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)

def generate_otp():
    return str(random.randint(100000, 999999))

def create_token(user_id: int):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def register_user(db: Session, name, email, password):
    otp = generate_otp()
    user = User(
        name=name,
        email=email,
        password=hash_password(password),
        otp=otp
    )
    db.add(user)
    db.commit()
    return otp


def verify_otp(db, email, otp):
    user = db.query(User).filter(User.email == email).first()

    if not user or not user.otp:
        return False

    # FORCE string comparison + trim
    if str(user.otp).strip() == str(otp).strip():
        user.is_verified = True
        user.otp = None
        db.commit()
        return True

    return False


def reset_password(db: Session, email: str, new_password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False

    user.password = hash_password(new_password)
    user.otp = None
    db.commit()
    return True

##  AUTHENTICATION DEPENDENCY  ##

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
