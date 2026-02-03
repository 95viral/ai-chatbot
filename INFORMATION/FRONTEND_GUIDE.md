# AI Chatbot Frontend Guide

## 📋 Project Structure

```
frontend/
├── index.html                 (Login)
├── login-verify.html          (Login OTP Verification)
├── register.html              (Registration)
├── register-verify.html       (Registration OTP Verification)
├── forgot.html                (Forgot Password)
├── reset.html                 (Password Reset)
├── chat.html                  (Main Chat Interface)
├── history.html               (Chat History)
├── upload.html                (Document Upload)
├── documents.html             (View Uploaded Documents)
├── document-chat.html         (Ask Questions About Documents)
├── app.js                     (All JavaScript Functions)
└── style.css                  (All Styling)
```

## 🔐 Authentication Flow

### Registration Flow
1. **register.html** - User fills in: Name, Email, Password
2. **registerStep1()** - Sends data to `/auth/register`
3. **register-verify.html** - User enters OTP received via email
4. **registerStep2()** - Verifies OTP with `/auth/register/verify-otp`
5. Redirects to login page

### Login Flow
1. **index.html** - User enters Email and Password
2. **loginStep1()** - Sends credentials to `/auth/login`
3. **login-verify.html** - User enters OTP sent to email
4. **loginStep2()** - Verifies OTP with `/auth/login/verify`
5. Token is stored in localStorage
6. Redirects to chat page

### Forgot Password Flow
1. **forgot.html** - User enters email address
2. **forgotPasswordStep1()** - Sends email to `/auth/forgot-password`
3. **reset.html** - User enters OTP and new password
4. **resetPassword()** - Sends to `/auth/reset-password`
5. Redirects to login page

## 💬 Chat Features

### Main Chat (chat.html)
- Real-time messaging with AI assistant
- **sendMessage()** - Sends message to `/chat` endpoint
- Press Enter or click Send button
- Message history displayed in chat box
- Navigation bar with quick links to History and Documents

### Chat History (history.html)
- **loadChatHistory()** - Fetches from `/chat/history` endpoint
- Displays all previous messages with timestamps
- Shows user messages in blue, AI responses in green

## 📄 Document Management

### Upload Documents (upload.html)
- **uploadDocument()** - Uploads files to `/upload` endpoint
- Supports PDF and text files
- Files stored per user (user_id)

### View Documents (documents.html)
- **loadDocuments()** - Fetches from `/documents` endpoint
- Lists all user's uploaded documents
- Click on document to chat with it

### Document Chat (document-chat.html)
- **chatWithDocument()** - Sends question to `/document/chat` endpoint
- Ask questions about specific documents
- AI answers based on document content only

## 🎨 UI/UX Features

### Navigation Bar
- Appears on all authenticated pages
- Quick access to Chat, History, Documents
- Logout button

### Responsive Design
- Mobile-friendly layout
- Adapts to different screen sizes
- Touch-friendly buttons

### Error Handling
- All functions include try-catch blocks
- Error messages displayed via alerts
- API validation checks

### Success Notifications
- Shows success messages on important actions
- Auto-redirects after 1.5 seconds

## 🔧 JavaScript Functions Reference

### Authentication Functions
```javascript
loginStep1()          // Send login OTP
loginStep2()          // Verify login OTP
registerStep1()       // Send registration OTP
registerStep2()       // Verify registration OTP
forgotPasswordStep1() // Send password reset OTP
resetPassword()       // Complete password reset
```

### Chat Functions
```javascript
sendMessage()         // Send chat message
loadChatHistory()     // Load previous messages
```

### Document Functions
```javascript
uploadDocument()      // Upload new file
loadDocuments()       // List user's documents
chatWithDocument()    // Ask question about document
```

### Utility Functions
```javascript
checkAuth()          // Verify user is logged in
logout()             // Clear token and redirect
showError()          // Display error message
showSuccess()        // Display success message
```

## 🔑 LocalStorage Keys

```javascript
token              // JWT authentication token
login_email        // Temporary: current login email
reg_email          // Temporary: current registration email
reg_password       // Temporary: current registration password
reset_email        // Temporary: email for password reset
```

## 📝 Important Notes

1. **OTP Validation**: OTP is a 6-digit code sent via email
2. **Token Storage**: JWT token stored in localStorage for API authentication
3. **API Base URL**: `http://127.0.0.1:8000` (change in app.js if needed)
4. **Authentication Header**: All protected endpoints require: `Authorization: Bearer {token}`
5. **Data Validation**: Frontend validates before sending to backend

## 🚀 How to Run

1. Ensure backend is running on `http://127.0.0.1:8000`
2. Open any HTML file in a browser (e.g., `index.html`)
3. Start with registration or login
4. Navigate using the interface

## ⚠️ Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "Error: Failed to load" | Ensure backend server is running |
| "Invalid OTP" | Check email for correct OTP, verify spelling |
| "Token expired" | Login again to get a new token |
| CORS errors | Backend should have CORS enabled (check main.py) |
| No documents showing | Upload a file first at `/upload.html` |

## 🎯 Features Implemented

✅ User Registration with OTP
✅ User Login with OTP
✅ Password Reset with OTP
✅ Real-time Chat with AI
✅ Chat History Management
✅ Document Upload (PDF/TXT)
✅ Document Management
✅ Ask Questions About Documents
✅ Responsive Design
✅ Error Handling & Validation
✅ Session Management (localStorage tokens)
✅ Navigation & Page Routing
