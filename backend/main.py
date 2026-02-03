from dotenv import load_dotenv
load_dotenv()  # Load environment variables FIRST

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, APIRouter, Request
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from backend.database import engine
from backend import models
from backend.auth import (
    get_db, register_user, verify_otp,
    verify_password, create_token, generate_otp,
    reset_password, get_current_user
)
from backend.email_utils import send_otp_email
from backend.ai_utils import get_ai_response, get_document_response
from backend.chat_utils import save_message, get_chat_history
from backend.documents_utils import extract_text_from_pdf
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from time import time
from collections import defaultdict
from pathlib import Path




# ----------------- RATE LIMITING -----------------
request_history = defaultdict(list)
MAX_REQUESTS_PER_MINUTE = 60

def rate_limit_check(request: Request):
    client_ip = request.client.host
    current_time = time()
    
    # Clean old requests (older than 1 minute)
    request_history[client_ip] = [
        req_time for req_time in request_history[client_ip]
        if current_time - req_time < 60
    ]
    
    if len(request_history[client_ip]) >= MAX_REQUESTS_PER_MINUTE:
        raise HTTPException(status_code=429, detail="Too many requests. Please try again later.")
    
    request_history[client_ip].append(current_time)

# ----------------- APP SETUP -----------------

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Chatbot Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount frontend static files
frontend_path = Path(__file__).parent.parent / "frontend"
app.mount("/frontend", StaticFiles(directory=str(frontend_path), html=True), name="frontend")

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

# ----------------- AUTH ROUTES -----------------

@auth_router.post("/register")
def register(name: str, email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    otp = register_user(db, name, email, password)
    send_otp_email(email, otp)

    return {"message": "OTP sent to your email"}


@auth_router.post("/register/verify-otp")
def verify_register_otp(email: str, otp: str, db: Session = Depends(get_db)):
    if verify_otp(db, email, otp):
        return {"message": "Registration successful"}
    raise HTTPException(status_code=400, detail="Invalid OTP")


@auth_router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    otp = generate_otp()
    user.otp = otp
    db.commit()

    send_otp_email(user.email, otp)
    return {"message": "Login OTP sent to your email"}


@auth_router.post("/login/verify")
def verify_login_otp(email: str, otp: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user or not user.otp:
        raise HTTPException(status_code=400, detail="OTP expired")

    if str(user.otp).strip() == str(otp).strip():
        token = create_token(user.id)
        user.otp = None
        db.commit()
        return {"token": token}

    raise HTTPException(status_code=400, detail="Invalid OTP")


@auth_router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp = generate_otp()
    user.otp = otp
    db.commit()

    send_otp_email(user.email, otp)
    return {"message": "Password reset OTP sent"}


@auth_router.post("/reset-password")
def reset_password_api(
    email: str,
    otp: str,
    new_password: str,
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user or not user.otp:
        raise HTTPException(status_code=400, detail="OTP expired")

    if str(user.otp).strip() != str(otp).strip():
        raise HTTPException(status_code=400, detail="Invalid OTP")

    reset_password(db, email, new_password)
    return {"message": "Password reset successful"}


app.include_router(auth_router)

# ----------------- CHAT -----------------

@app.post("/chat")
def chat(
    message: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = current_user.id

    save_message(db, user_id, "user", message)
    messages = get_chat_history(db, user_id)

    ai_reply = get_ai_response(messages)

    save_message(db, user_id, "assistant", ai_reply)
    return {"reply": ai_reply}


@app.get("/chat/history")
def chat_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    messages = get_chat_history(db, current_user.id)
    return [
        {
            "role": m.role,
            "content": m.content,
            "timestamp": m.created_at
        }
        for m in messages
    ]


@app.delete("/chat/history")
def delete_chat_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db.query(models.Message).filter(
        models.Message.user_id == current_user.id
    ).delete()
    db.commit()
    return {"message": "Chat history deleted successfully"}


@app.delete("/message/{message_id}")
def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    msg = db.query(models.Message).filter(
        models.Message.id == message_id,
        models.Message.user_id == current_user.id
    ).first()

    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")

    msg.is_deleted = True
    db.commit()
    return {"message": "Message deleted successfully"}


@app.get("/user/profile")
def get_user_profile(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None
    }


@app.get("/user/stats")
def get_user_stats(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    message_count = db.query(models.Message).filter(
        models.Message.user_id == current_user.id,
        models.Message.is_deleted == False
    ).count()
    
    document_count = db.query(models.Document).filter(
        models.Document.user_id == current_user.id
    ).count()

    return {
        "messages": message_count,
        "documents": document_count,
        "user_email": current_user.email
    }

# ----------------- DOCUMENTS -----------------

UPLOAD_DIR = "uploads/documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    file_path = f"{UPLOAD_DIR}/{current_user.id}_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text_content = ""
    if file.content_type == "application/pdf":
        text_content = extract_text_from_pdf(file_path)

    doc = models.Document(
        user_id=current_user.id,
        filename=file.filename,
        filepath=file_path,
        content=text_content
    )

    db.add(doc)
    db.commit()

    return {"message": "File uploaded successfully"}


@app.get("/documents")
def list_documents(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    docs = db.query(models.Document).filter(
        models.Document.user_id == current_user.id
    ).all()

    return [
        {
            "id": d.id,
            "filename": d.filename,
            "uploaded_at": d.uploaded_at
        }
        for d in docs
    ]


@app.post("/document/chat")
def ask_document(
    document_id: int,
    question: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    doc = db.query(models.Document).filter(
        models.Document.id == document_id,
        models.Document.user_id == current_user.id
    ).first()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    answer = get_document_response(
        document_text=doc.content,
        question=question
    )

    return {"answer": answer}
