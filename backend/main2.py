from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, APIRouter
from sqlalchemy.orm import Session
from backend.database import engine
from backend import models
from backend.auth import (
    get_db, register_user, verify_otp,
    verify_password, create_token, generate_otp, reset_password, get_current_user
)
from backend.email_utils import send_otp_email
from backend.models import User
from backend.ai_utils import get_ai_response, get_document_response

from backend.chat_utils import save_message, get_chat_history
import os
import shutil
from backend.documents_utils import extract_text_from_pdf
from fastapi.middleware.cors import CORSMiddleware



models.Base.metadata.create_all(bind=engine)
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])



app = FastAPI(title="Auth System with OTP & Session")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# REGISTER
@app.post("/register")
def register(name: str, email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    otp = register_user(db, name, email, password)
    send_otp_email(email, otp)
    return {"message": "OTP sent to your email"}
    # return {"message": "OTP sent", "otp": otp}  # OTP shown for demo

# VERIFY OTP (REGISTER)
@app.post("/verify-register-otp")
def verify_register_otp(email: str, otp: str, db: Session = Depends(get_db)):
    if verify_otp(db, email, otp):
        return {"message": "Registration successful"}
    raise HTTPException(status_code=400, detail="Invalid OTP")

# LOGIN
@app.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    otp = generate_otp()     # 🔥 REAL OTP
    user.otp = otp
    db.commit()              # 🔥 SAVE TO DB
    send_otp_email(user.email, otp)
    return {"message": "Login OTP sent to your email"}
    # print("LOGIN OTP:", otp) # debug only

    # return {
    #     "message": "Login OTP sent",
    #     # "otp": otp           # demo only (remove in real app)
    # }

# VERIFY LOGIN OTP + SESSION
@app.post("/verify-login-otp")
def verify_login_otp(email: str, otp: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user or not user.otp:
        raise HTTPException(status_code=400, detail="OTP expired")

    print("DB OTP:", user.otp)
    print("INPUT OTP:", otp)

    if str(user.otp).strip() == str(otp).strip():
        token = create_token(user.id)
        user.otp = None
        db.commit()
        return {
            "message": "Login successful",
            "token": token
        }

    raise HTTPException(status_code=400, detail="Invalid OTP")

# REQUEST PASSWORD RESET
@app.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp = generate_otp()
    user.otp = otp
    db.commit()

    send_otp_email(user.email, otp)

    return {"message": "Password reset OTP sent to email"}

@app.post("/reset-password")
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


@app.post("/chat")
def chat(
    message: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    user_id = current_user.id

    # Save user message
    save_message(db, user_id, "user", message)

    # Load chat history
    messages = get_chat_history(db, user_id)

    # AI response
    ai_reply = get_ai_response(messages)

    # Save AI message
    save_message(db, user_id, "assistant", ai_reply)

    return {"reply": ai_reply}

## GET CHAT HISTORY

@app.get("/chat/history")
def chat_history(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    messages = get_chat_history(db, current_user.id)

    return [
        {
            "role": msg.role,
            "content": msg.content,
            "timestamp": msg.created_at
        }
        for msg in messages
    ]

# UPLOAD DOCUMENT

from fastapi import UploadFile, File
import shutil
import os

UPLOAD_DIR = "uploads/documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    file_path = f"{UPLOAD_DIR}/{current_user.id}_{file.filename}"

    # 1️⃣ Save file to disk
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2️⃣ Extract text (ONLY for PDF)
    text_content = ""
    if file.content_type == "application/pdf":
        text_content = extract_text_from_pdf(file_path)

    # 3️⃣ Save to database
    doc = models.Document(
        user_id=current_user.id,
        filename=file.filename,
        filepath=file_path,
        content=text_content   # 👈 STEP 4 IS THIS
    )

    db.add(doc)
    db.commit()

    return {"message": "File uploaded successfully"}


@app.get("/documents")
def list_documents(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    docs = db.query(models.Document)\
             .filter(models.Document.user_id == current_user.id)\
             .all()

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
    current_user = Depends(get_current_user)
):
    doc = db.query(models.Document).filter(
        models.Document.id == document_id,
        models.Document.user_id == current_user.id
    ).first()

    if not doc:
        return {"error": "Document not found"}

    answer = get_document_response(
        document_text=doc.content,
        question=question
    )

    return {"answer": answer}
