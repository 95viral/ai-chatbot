# AI Chatbot - Complete Architecture & Feature Map

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      USER BROWSER                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │             FRONTEND (HTML + CSS + JS)                 │   │
│  │  ┌─────────────────────────────────────────────────┐   │   │
│  │  │        11 HTML Pages                           │   │   │
│  │  ├─────────────────────────────────────────────────┤   │   │
│  │  │ • index.html (Login)                           │   │   │
│  │  │ • register.html (Registration)                 │   │   │
│  │  │ • login-verify.html (OTP)                      │   │   │
│  │  │ • register-verify.html (OTP)                   │   │   │
│  │  │ • forgot.html (Password Recovery)              │   │   │
│  │  │ • reset.html (Password Reset)                  │   │   │
│  │  │ • chat.html (Chat Interface)                   │   │   │
│  │  │ • history.html (Message History)               │   │   │
│  │  │ • upload.html (Document Upload)                │   │   │
│  │  │ • documents.html (Document List)               │   │   │
│  │  │ • document-chat.html (Document Q&A)            │   │   │
│  │  └─────────────────────────────────────────────────┘   │   │
│  │                                                         │   │
│  │  ┌─────────────────────────────────────────────────┐   │   │
│  │  │    app.js (395 lines - All Functions)          │   │   │
│  │  ├─────────────────────────────────────────────────┤   │   │
│  │  │ Functions: 12 main + utilities                 │   │   │
│  │  │ • Authentication (6 functions)                 │   │   │
│  │  │ • Chat (2 functions)                           │   │   │
│  │  │ • Documents (3 functions)                      │   │   │
│  │  │ • Utilities (1 function)                       │   │   │
│  │  └─────────────────────────────────────────────────┘   │   │
│  │                                                         │   │
│  │  ┌─────────────────────────────────────────────────┐   │   │
│  │  │    style.css (520 lines - All Styling)         │   │   │
│  │  ├─────────────────────────────────────────────────┤   │   │
│  │  │ • Global Styles                                │   │   │
│  │  │ • Component Styles                             │   │   │
│  │  │ • Layout & Responsiveness                      │   │   │
│  │  │ • Animations & Effects                         │   │   │
│  │  └─────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                         │ HTTP/REST                            │
│                         │ JSON + Bearer Token                  │
│                         ▼                                       │
└─────────────────────────────────────────────────────────────────┘
                          │
                          │
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND API (FastAPI)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │         Authentication Endpoints                       │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │ POST /auth/register                                   │   │
│  │ POST /auth/register/verify-otp                        │   │
│  │ POST /auth/login                                      │   │
│  │ POST /auth/login/verify                               │   │
│  │ POST /auth/forgot-password                            │   │
│  │ POST /auth/reset-password                             │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │           Chat Endpoints                              │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │ POST /chat (Send message)                             │   │
│  │ GET /chat/history (Get messages)                      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │         Document Endpoints                            │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │ POST /upload (Upload file)                            │   │
│  │ GET /documents (List documents)                       │   │
│  │ POST /document/chat (Ask about document)              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                         │                                       │
│                         │ Database & AI                         │
│                         ▼                                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         Services & Utilities                           │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ • auth.py (Authentication logic)                       │  │
│  │ • ai_utils.py (Gemini AI integration)                  │  │
│  │ • chat_utils.py (Chat history)                         │  │
│  │ • documents_utils.py (PDF processing)                  │  │
│  │ • email_utils.py (OTP emails)                          │  │
│  │ • database.py (SQLAlchemy ORM)                         │  │
│  │ • models.py (User, Message, Document)                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                         │                                       │
│                         ▼                                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              External Services                         │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ • Gemini API (AI Responses)                            │  │
│  │ • Email Service (OTP Delivery)                         │  │
│  │ • SQLite Database (Persistence)                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow Diagrams

### Registration Flow
```
User fills form
     │
     ▼
registerStep1() ─────► Validate inputs
     │
     ├─ Invalid? → Show error
     │
     └─ Valid ─────► POST /auth/register
                          │
                          ▼
                    Generate OTP
                    Send email
                          │
                          ├─ Success ─────► Store temp email
                          │                 Redirect to verify page
                          │
                          └─ Error ──────► Show error
                                          Retry
                                          
registerStep2() ◄──── User enters OTP
     │
     ▼
Validate OTP ────► POST /auth/register/verify-otp
     │
     ├─ Invalid ─────► Show error, retry
     │
     └─ Valid ──────► Mark user verified
                      Clear temp data
                      Redirect to login
```

### Login & Chat Flow
```
loginStep1() ──► POST /auth/login ──► Send OTP
                      │
                      ▼
              Store login_email
              Redirect to OTP page

loginStep2() ──► POST /auth/login/verify
                      │
                      ▼
                Get JWT token
                Save to localStorage
                Redirect to chat.html

sendMessage() ──► POST /chat (with token)
                      │
                      ▼
                Save user message
                Get AI response
                Save AI response
                Display in chat UI
```

### Document Flow
```
uploadDocument() ──► POST /upload (FormData + token)
                          │
                          ▼
                    Save file
                    Extract text
                    Save to DB
                    Redirect to documents
                    
loadDocuments() ──► GET /documents (token)
                          │
                          ▼
                    Fetch user documents
                    Display list
                    Add click handlers
                    
chatWithDocument() ──► POST /document/chat (token + question)
                          │
                          ▼
                    Get document text
                    Create prompt
                    Call Gemini AI
                    Display answer
```

## 🎯 Feature Map

```
┌─────────────────────────────────────────────────────────────┐
│                    AI CHATBOT FEATURES                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  🔐 AUTHENTICATION                                          │
│  ├─ User Registration (3-step process)                      │
│  ├─ Email verification with OTP                             │
│  ├─ User Login (3-step with 2FA)                            │
│  ├─ JWT token management                                    │
│  ├─ Password recovery flow                                  │
│  └─ Session management                                      │
│                                                              │
│  💬 MESSAGING                                               │
│  ├─ Real-time chat with AI                                  │
│  ├─ Message history persistence                             │
│  ├─ Conversation context                                    │
│  ├─ User/AI role distinction                                │
│  └─ Timestamp tracking                                      │
│                                                              │
│  📄 DOCUMENT MANAGEMENT                                    │
│  ├─ PDF upload support                                      │
│  ├─ Text file upload                                        │
│  ├─ Automatic text extraction                               │
│  ├─ Document listing                                        │
│  ├─ Document-specific Q&A                                   │
│  └─ Per-user document storage                               │
│                                                              │
│  🎨 USER INTERFACE                                         │
│  ├─ Beautiful dark theme                                    │
│  ├─ Responsive design                                       │
│  ├─ Mobile optimized                                        │
│  ├─ Smooth animations                                       │
│  ├─ Professional styling                                    │
│  └─ Intuitive navigation                                    │
│                                                              │
│  🔒 SECURITY                                               │
│  ├─ Password hashing (bcrypt)                               │
│  ├─ JWT authentication                                      │
│  ├─ Input validation                                        │
│  ├─ Error handling                                          │
│  ├─ CORS protection                                         │
│  └─ Secure token storage                                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Component Interaction Map

```
                    ┌─────────────────┐
                    │   index.html    │
                    │    (Login)      │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ loginStep1()    │
                    │ loginStep2()    │
                    └────────┬────────┘
                             │
        ┌────────────────────┼─────────────────────┐
        │                    │                     │
        ▼                    ▼                     ▼
   ┌────────────┐      ┌────────────┐      ┌──────────────┐
   │ chat.html  │      │ history    │      │ documents    │
   │(sendMsg)   │      │.html       │      │.html         │
   └────┬───────┘      └────┬───────┘      └──┬───────────┘
        │                   │                  │
        │ POST /chat        │ GET /history    │ POST /upload
        │                   │                 │
        │                   │              ┌──▼────────────┐
        │                   │              │ upload.html   │
        │                   │              │uploadDocument │
        │                   │              └──┬────────────┘
        │                   │                 │
        │                   │              POST /upload
        │                   │                 │
        │                   └─────────────────┼─────────┐
        │                                     │         │
        │                        ┌────────────▼──┐   ┌──▼────────────┐
        │                        │ database      │   │document-chat  │
        │                        │messages       │   │.html          │
        └────────────────────────┤documents      │   │chatWithDoc()  │
                         Messages │users          │   └──┬────────────┘
                                  └───────────────┘      │
                                                         │ POST /doc/chat
                                                         │
                                              ┌──────────▼──────────┐
                                              │ Gemini API Response │
                                              └─────────────────────┘
```

## 🎬 Page Navigation Graph

```
START
  │
  ├─► index.html ◄─────┐
  │    (Login)         │
  │    ▼               │
  │  loginStep1() ─────┤
  │    │               │
  │    └──► login-verify.html
  │         loginStep2()
  │         ▼
  │    TOKEN STORAGE
  │    ▼
  │
  ├─► register.html ◄──┐
  │    (Register)      │
  │    ▼               │
  │  registerStep1()───┤
  │    │               │
  │    └──► register-verify.html
  │         registerStep2()
  │         ▼
  │    BACK TO LOGIN
  │
  ├─► forgot.html ◄────┐
  │    (Forgot)        │
  │    ▼               │
  │  forgotPasswordStep1()
  │    │               │
  │    └──► reset.html
  │         resetPassword()
  │         ▼
  │    BACK TO LOGIN
  │
  └─► AUTHENTICATED ───► chat.html ◄──────┐
       ▼                 ▼                │
       TOKEN             sendMessage()   │
       ▼                 │                │
       PROTECTED    ┌────┼────┐           │
       PAGES        │    │    │           │
       │       history documents upload   │
       │            │    │    │ │         │
       │            │    │    ▼ │ ────┐  │
       │            │    │   upload.html┼──┘
       │            │    │    │         │
       │            │    │    ▼         │
       │            │    └►documents.html
       │            │         │
       │            │         ▼
       │            │    document-chat.html
       │            │    chatWithDocument()
       │            │         │
       └────────────┴─────────┴──► logout() ──► index.html
```

## 💾 Data Models

```
User
├── id (PK)
├── name
├── email (UNIQUE)
├── password (hashed)
├── otp (temp, cleared after use)
└── is_verified

Message
├── id (PK)
├── user_id (FK)
├── role ("user" or "assistant")
├── content
└── created_at

Document
├── id (PK)
├── user_id (FK)
├── filename
├── filepath
├── content (extracted text)
└── uploaded_at
```

## 🔐 Security Flow

```
User Input
    │
    ▼
Frontend Validation
    │
    ├─ Invalid? → Error message
    │
    └─ Valid ────► Encode parameters
                   │
                   ▼
              POST/GET request
               (with Bearer token if needed)
                   │
                   ▼
              Backend Receives
               (CORS verified)
                   │
                   ▼
              Backend Validation
               (input check)
                   │
                   ├─ Invalid? → 400 error
                   │
                   └─ Valid ────► Auth check
                                  (verify token)
                                  │
                                  ├─ Missing? → 401 error
                                  │
                                  └─ Valid ────► Process
                                                  Execute
                                                  Response
                                                  │
                                                  ▼
                                            Frontend receives
                                            (check .ok)
                                            │
                                            ├─ Error? → Show error
                                            │
                                            └─ Success → Update UI
                                                Save data
                                                Redirect if needed
```

---

**This complete architecture ensures a robust, secure, and user-friendly AI Chatbot application!** 🚀
