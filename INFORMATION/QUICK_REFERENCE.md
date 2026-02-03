# AI Chatbot - Quick Reference Card

## 📋 File Sizes
```
app.js             10.6 KB  (395 lines - All JavaScript)
style.css           6.6 KB  (520 lines - All Styling)
index.html          1.0 KB  (Login)
register.html       1.1 KB  (Registration)
chat.html           0.9 KB  (Chat Interface)
documents.html      1.0 KB  (Document List)
upload.html         1.3 KB  (Document Upload)
history.html        0.9 KB  (Chat History)
forgot.html         0.8 KB  (Forgot Password)
reset.html          1.0 KB  (Reset Password)
login-verify.html   0.8 KB  (OTP Verification)
register-verify.html 0.8 KB (OTP Verification)
document-chat.html  1.3 KB  (Document Q&A)

TOTAL: ~32 KB (Production Ready)
```

## 🎯 User Journey Map

```
┌─────────────────────────────────────┐
│      New User? → register.html      │
│      Existing? → index.html         │
└──────────────┬──────────────────────┘
               │
       ┌───────┴────────┐
       ▼                ▼
  register.html    index.html
   (Name, Email)   (Email, Password)
   Password
   "Send OTP"      "Send OTP"
       │                │
       ▼                ▼
register-verify   login-verify
 (Enter OTP)       (Enter OTP)
 "Complete"        "Login"
   │                │
   └────────┬───────┘
            ▼
    ✅ TOKEN STORED
            │
        ┌───┴────┐
        ▼        ▼
    Chat Page  Documents
    History    Upload
    Logout     Q&A
```

## 🔑 Key Endpoints

### Auth
```
registerStep1() → POST /auth/register
registerStep2() → POST /auth/register/verify-otp
loginStep1() → POST /auth/login
loginStep2() → POST /auth/login/verify
forgotPasswordStep1() → POST /auth/forgot-password
resetPassword() → POST /auth/reset-password
```

### Features
```
sendMessage() → POST /chat (+ Bearer token)
loadChatHistory() → GET /chat/history (+ Bearer token)
uploadDocument() → POST /upload (+ Bearer token, FormData)
loadDocuments() → GET /documents (+ Bearer token)
chatWithDocument() → POST /document/chat (+ Bearer token)
```

## 🎨 Color Scheme

```css
Primary:     #6c7cff   (Purple buttons)
Background:  #0b0e1a   (Very dark blue)
Card:        #12162a   (Dark blue)
Input:       #1c2140   (Darker blue)
Border:      #3a3f5a   (Medium blue)
Text:        #e0e0e0   (Light gray)
AI Message:  #9cff6c   (Green)
Success:     #4ade80   (Green)
Error:       #ff6b6b   (Red)
```

## 🔧 Configuration

### API Base URL (app.js, Line 1)
```javascript
const API_BASE = "http://127.0.0.1:8000";
```
Change this if backend is on different server!

### LocalStorage Keys
```javascript
localStorage.getItem('token')          // JWT token
localStorage.getItem('login_email')    // Temp login email
localStorage.getItem('reg_email')      // Temp register email
localStorage.getItem('reset_email')    // Temp reset email
```

## 🚀 Quick Start

1. **Backend Running?**
   ```bash
   python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

2. **Open Frontend**
   ```
   http://localhost:8000/frontend/index.html
   OR
   c:\Products\AI_CHATBOT\frontend\index.html
   ```

3. **Test Registration**
   - Register with email & password
   - Check email for OTP
   - Complete registration

4. **Test Login**
   - Login with credentials
   - Enter OTP from email
   - Access chat

## ⚡ Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Send Message | Enter |
| Submit Form | Tab then Enter |
| Navigate Back | Browser back button |
| Logout | Click logout link |

## 🐛 Debug Commands

```javascript
// In browser console (F12):

// Check if logged in
localStorage.getItem('token')

// Clear all data
localStorage.clear()

// Check API base
console.log(API_BASE)

// Test API
fetch(API_BASE + '/chat/history', {
  headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
}).then(r => r.json()).then(console.log)
```

## 📱 Responsive Breakpoints

```css
Mobile:   < 600px   (Stacked layout)
Tablet:   600-1024px (Adapted layout)
Desktop:  > 1024px   (Full layout)
```

## ✨ Features Checklist

- [x] User Registration
- [x] Email Verification (OTP)
- [x] User Login
- [x] Password Recovery
- [x] Chat with AI
- [x] Chat History
- [x] Document Upload
- [x] Document Management
- [x] Document Q&A
- [x] Session Management
- [x] Responsive Design
- [x] Error Handling
- [x] Professional UI

## 📊 Performance

- **Total Size**: ~32 KB
- **Load Time**: < 1 second
- **API Response**: Depends on backend
- **Database Queries**: Minimal (indexed)
- **Mobile Friendly**: Yes
- **Accessibility**: Good

## 🔐 Security Notes

1. **Token Storage**: localStorage (consider moving to httpOnly cookie)
2. **OTP Validation**: 6-digit numeric code
3. **Password**: Min 6 chars, hashed by backend
4. **API Calls**: All include proper headers
5. **CORS**: Backend configured
6. **Input Sanitization**: Frontend validation present

## 🎓 Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **API**: Fetch API (async/await)
- **Auth**: JWT tokens
- **Styling**: CSS Grid, Flexbox, Gradients
- **Storage**: LocalStorage, Backend Database

## 🔗 Important Links

- Frontend: `/Products/AI_CHATBOT/frontend/`
- Backend: `/Products/AI_CHATBOT/backend/`
- Guides: See FRONTEND_GUIDE.md, TESTING_GUIDE.md
- API: http://127.0.0.1:8000/docs (FastAPI Swagger)

## 💡 Tips

1. Use browser DevTools (F12) to debug
2. Check Network tab for API calls
3. Verify token in localStorage
4. Check browser console for JS errors
5. Ensure backend server is running
6. Check .env file has all secrets
7. Review backend logs for server errors

## 🎬 Test Scenarios

```
Scenario 1: Fresh User
→ Open index.html
→ Click Register
→ Fill details
→ Enter OTP
→ Verify success

Scenario 2: Existing User
→ Open index.html
→ Enter credentials
→ Enter OTP
→ Chat with AI
→ Upload document
→ Ask about document

Scenario 3: Forgot Password
→ Click "Forgot Password?"
→ Enter email
→ Enter OTP
→ Set new password
→ Login with new password
```

---

**Everything is ready! Happy chatting! 🚀**
