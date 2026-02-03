# AI Chatbot - Complete Setup & Testing Guide

## 🚀 Backend Setup

### 1. Install Dependencies
```bash
cd c:\Products\AI_CHATBOT
pip install -r requirements.txt
```

### 2. Environment Variables (.env file)
Create a `.env` file in the project root with:
```
JWT_SECRET_KEY=your_secret_key_here
GEMINI_API_KEY=your_gemini_api_key
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

### 3. Start Backend Server
```bash
cd backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

## 🌐 Frontend Setup

### 1. Open Frontend in Browser
- Open `c:\Products\AI_CHATBOT\frontend\index.html` in your browser
- Or use a local server:
```bash
# Using Python
python -m http.server 8001 -d c:\Products\AI_CHATBOT\frontend

# Then open: http://localhost:8001/index.html
```

## ✅ Testing Checklist

### Registration Flow
- [ ] Navigate to Register page
- [ ] Fill in Name, Email, Password (min 6 chars)
- [ ] Click "Send OTP"
- [ ] Check email for OTP code
- [ ] Enter OTP on verify page
- [ ] Should show "Registration successful!" and redirect to login

### Login Flow
- [ ] Go to Login page
- [ ] Enter email and password
- [ ] Click "Send OTP"
- [ ] Check email for OTP
- [ ] Enter OTP on verify page
- [ ] Should redirect to chat page with token in localStorage

### Chat Page
- [ ] Type a message in the input box
- [ ] Click Send or press Enter
- [ ] Message should appear in blue on the right
- [ ] AI response should appear in green on the left
- [ ] Test multiple messages

### Chat History
- [ ] Click "History" link from chat page
- [ ] Should display all previous messages
- [ ] Verify timestamps are correct

### Document Upload
- [ ] Click "Documents" → "Upload New"
- [ ] Select a PDF or text file
- [ ] Click "Upload Document"
- [ ] Should show success message

### View Documents
- [ ] Go to Documents page
- [ ] Should list all uploaded files
- [ ] Click on a document name
- [ ] Should open document chat

### Ask About Document
- [ ] Type a question about the document
- [ ] Click Send
- [ ] AI should answer based on document content

### Logout
- [ ] Click "Logout" button
- [ ] Should redirect to login page
- [ ] Token should be cleared from localStorage

### Forgot Password
- [ ] Click "Forgot Password?" on login
- [ ] Enter email address
- [ ] Check email for OTP
- [ ] Enter OTP and new password on reset page
- [ ] Should redirect to login

## 🐛 Debugging Tips

### Check Browser Console
```javascript
// Open DevTools (F12) and check Console tab for errors
// View stored token:
localStorage.getItem('token')

// Clear all localStorage:
localStorage.clear()
```

### Check Network Requests
- Open DevTools → Network tab
- Perform an action
- See all API calls and responses

### Backend Logs
- Check terminal where backend is running
- Look for error messages and status codes

## 📊 API Endpoints Reference

### Authentication
```
POST   /auth/register
POST   /auth/register/verify-otp
POST   /auth/login
POST   /auth/login/verify
POST   /auth/forgot-password
POST   /auth/reset-password
```

### Chat
```
POST   /chat
GET    /chat/history
```

### Documents
```
POST   /upload
GET    /documents
POST   /document/chat
```

## 🔧 Common Backend Issues

### "Module not found" errors
- Ensure all packages are installed: `pip install -r requirements.txt`
- Check you're using the correct Python interpreter

### "JWT_SECRET_KEY is missing"
- Create/update .env file with JWT_SECRET_KEY
- Restart backend server

### CORS errors
- Backend already configured with CORS middleware
- If still occurring, check main.py CORS setup

### Database errors
- Delete any existing database files
- Backend will create new tables on first run

## 🎯 Expected Results

### Successful Registration
```json
{
  "message": "OTP sent to your email"
}
```

### Successful Login
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Chat Response
```json
{
  "reply": "AI generated response here"
}
```

## 📱 Testing Different Scenarios

### Test with Invalid OTP
- Enter wrong OTP → Should show "Invalid OTP" error
- Try again with correct OTP

### Test with Existing Email
- Try registering with same email twice
- Should show "Email already registered"

### Test with Weak Password
- Try password less than 6 characters
- Frontend should show validation error

### Test Chat Without Authentication
- Clear localStorage token
- Try accessing chat.html
- Should redirect to login

## 🎬 Quick Start Script

Create `test_chatbot.bat` in project root:
```batch
@echo off
echo Starting AI Chatbot...
start http://127.0.0.1:8000
cd backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Then double-click the batch file to start everything!

## ✨ Features Verification

After successful login, verify:
- ✅ Chat works (API call succeeds)
- ✅ History loads (shows previous messages)
- ✅ Upload works (files accepted)
- ✅ Documents display (list populated)
- ✅ Document chat works (Q&A functions)
- ✅ Logout works (redirects + clears token)
- ✅ Navigation works (all links functional)
- ✅ Responsive design (try mobile view)

## 🆘 Need Help?

1. Check the FRONTEND_GUIDE.md for function documentation
2. Review backend code in `/backend` directory
3. Check browser console for JavaScript errors
4. Check backend terminal for server errors
5. Verify API URLs match in app.js config
6. Ensure .env file has all required variables
