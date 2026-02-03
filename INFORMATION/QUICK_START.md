# 🚀 QUICK START GUIDE - AI CHATBOT

## ⚡ 5-Minute Setup

### Step 1: Start Backend (1 minute)
```bash
# Open Terminal/PowerShell
cd c:\Products\AI_CHATBOT
cd backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000

# Wait for: "Uvicorn running on http://127.0.0.1:8000"
```

### Step 2: Open Frontend (30 seconds)
```
Open Browser: http://127.0.0.1:8000/frontend/index.html
OR
Open File: c:\Products\AI_CHATBOT\frontend\index.html
```

### Step 3: Test Registration (2 minutes)
```
1. Click "Register"
2. Fill in:
   - Name: John Doe
   - Email: your.email@gmail.com
   - Password: password123
3. Click "Send OTP"
4. Check your email for OTP code
5. Paste OTP on verify page
6. Click "Complete Registration"
7. You'll be sent back to login
```

### Step 4: Test Login (1.5 minutes)
```
1. On index.html, enter:
   - Email: your.email@gmail.com
   - Password: password123
2. Click "Send OTP"
3. Check email for OTP
4. Paste OTP on verify page
5. Click "Verify & Login"
6. You're now in the chat! 🎉
```

---

## 🎮 Try Each Feature

### 💬 Chat with AI
```
1. You're now on chat.html
2. Type: "Hello, how are you?"
3. Press Enter or click Send
4. Watch AI respond
5. Keep chatting!
```

### 📜 View Chat History
```
1. Click "History" link
2. See all your previous messages
3. Messages show timestamps
4. Blue = Your message
5. Green = AI response
```

### 📄 Upload Document
```
1. Click "Documents" link
2. Click "Upload New"
3. Select a PDF or text file
4. Click "Upload Document"
5. Success message appears
```

### ❓ Ask About Document
```
1. Go to Documents
2. Click on a document name
3. Type your question
4. Press Enter
5. AI answers based on document content
```

### 🚪 Logout
```
1. Click "Logout" button
2. You're back at login page
3. Token is cleared
4. Login again to continue
```

---

## 🔐 Test Features Checklist

After completing setup, verify these work:

- [ ] Registration page works
- [ ] OTP email received
- [ ] Registration verification works
- [ ] Login page works
- [ ] Login OTP works
- [ ] Chat page loads
- [ ] Can send messages
- [ ] AI responds
- [ ] History loads previous messages
- [ ] Can upload document
- [ ] Document appears in list
- [ ] Can ask about document
- [ ] Logout redirects to login

---

## 🐛 Quick Troubleshooting

### "Cannot connect to backend"
```
❌ Backend not running
✅ Solution: Run step 1 again, check terminal for errors
```

### "OTP not received"
```
❌ Email configuration issue
✅ Solution: Check .env file has SMTP settings, check spam folder
```

### "Login loops back to login"
```
❌ Token issue
✅ Solution: 
   1. Open DevTools (F12)
   2. Run: localStorage.clear()
   3. Refresh page
   4. Login again
```

### "Chat not working"
```
❌ Authentication failed
✅ Solution:
   1. Check console (F12 → Console tab)
   2. Look for error message
   3. Verify token exists: localStorage.getItem('token')
   4. Login again if needed
```

### "Styling looks wrong"
```
❌ CSS not loading
✅ Solution:
   1. Hard refresh: Ctrl+Shift+R
   2. Clear cache: Ctrl+Shift+Delete
   3. Restart browser
```

---

## 📱 Test on Mobile

1. Backend running on localhost
2. Find your computer's IP: `ipconfig`
3. On mobile browser: `http://YOUR_IP:8000/frontend/index.html`
4. Should see responsive design

---

## 🎯 What to Test

### User Registration Flow ✅
- Can I register?
- Do I receive OTP email?
- Can I verify with OTP?
- Does it redirect to login?

### User Login Flow ✅
- Can I login with credentials?
- Do I receive OTP?
- Can I verify with OTP?
- Am I redirected to chat?

### Chat Features ✅
- Can I send messages?
- Does AI respond?
- Are messages saved?
- Can I see history?

### Document Features ✅
- Can I upload files?
- Do documents appear in list?
- Can I ask questions about them?
- Does AI answer based on content?

### Navigation ✅
- Can I navigate between pages?
- Do all links work?
- Can I logout?
- Is token cleared on logout?

### Design ✅
- Does it look good on desktop?
- Does it look good on mobile?
- Are animations smooth?
- Are all colors correct?

---

## 💡 Pro Tips

### Debug in Browser Console (F12)
```javascript
// Check token
localStorage.getItem('token')

// Clear all data
localStorage.clear()

// Check API base
console.log(API_BASE)

// Test API call
fetch('http://127.0.0.1:8000/chat/history', {
  headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }
}).then(r => r.json()).then(console.log)
```

### Files to Review
- `app.js` - All functions (395 lines)
- `style.css` - All styles (520 lines)
- `index.html` - Login page
- `chat.html` - Chat interface

### Common Test Credentials
```
Email: test@example.com
Password: Password123
```

---

## ✨ Expected Behavior

### Registration Success
```
✓ Email verified
✓ OTP email sent
✓ OTP validated
✓ Redirects to login
✓ Can login with new credentials
```

### Login Success
```
✓ Email & password verified
✓ OTP email sent
✓ OTP validated
✓ Token saved to localStorage
✓ Redirects to chat
✓ Chat loads successfully
```

### Chat Success
```
✓ Message sends
✓ AI responds
✓ Message appears immediately
✓ Conversation flows naturally
✓ History is saved
```

---

## 📊 Performance Check

- **Page load**: Should be instant (< 1 sec)
- **Message send**: Should be quick (< 2 sec)
- **AI response**: Depends on Gemini API (typically 5-15 sec)
- **Document upload**: Depends on file size
- **Document Q&A**: Similar to chat (5-15 sec)

---

## 🎓 Learning Path

### Beginner
1. Use the app like a user
2. Try all features
3. Enjoy chatting!

### Intermediate
1. Check browser console (F12)
2. Review app.js functions
3. Read FRONTEND_GUIDE.md

### Advanced
1. Modify app.js
2. Add new features
3. Customize styling
4. Deploy to production

---

## 🚀 Next Steps After Testing

### If Everything Works ✅
1. Read PROJECT_SUMMARY.md for overview
2. Review IMPLEMENTATION_SUMMARY.md for details
3. Check ARCHITECTURE_DIAGRAM.md for design
4. Deploy if needed

### If You Find Issues ❌
1. Check TESTING_GUIDE.md troubleshooting
2. Review QUICK_REFERENCE.md for debug tips
3. Check browser console for errors
4. Review backend logs

### If You Want to Extend
1. Read IMPLEMENTATION_SUMMARY.md
2. Understand function structure in app.js
3. Review API endpoints in backend
4. Add new functions to app.js
5. Add new pages as needed

---

## 📞 Support Resources

| Issue | See This File |
|-------|---------------|
| How to test? | TESTING_GUIDE.md |
| How do I use it? | FRONTEND_GUIDE.md |
| What was built? | IMPLEMENTATION_SUMMARY.md |
| Need debug tips? | QUICK_REFERENCE.md |
| How's it designed? | ARCHITECTURE_DIAGRAM.md |
| Quick lookup? | QUICK_REFERENCE.md |
| Overview? | PROJECT_SUMMARY.md |

---

## ✅ Success Criteria

You'll know everything is working when:

✅ You can register with email
✅ You receive OTP via email
✅ You can verify OTP
✅ You can login
✅ You can chat with AI
✅ You can see chat history
✅ You can upload documents
✅ You can ask about documents
✅ You can logout
✅ Mobile view is responsive
✅ No console errors
✅ No API errors

---

## 🎉 You're Ready!

Everything is set up and working. Start with the steps above and enjoy your AI Chatbot!

**Questions?** → Read the relevant documentation file
**Issues?** → Check TROUBLESHOOTING section
**Features?** → Try them all!

---

**Happy Chatting! 🚀**

Last updated: January 19, 2026
Status: ✅ Production Ready
