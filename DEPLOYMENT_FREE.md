# 🚀 Free Deployment Guide for AI Chatbot

## Overview
Your application has two parts that need deployment:
1. **Frontend**: HTML, CSS, JavaScript (static files)
2. **Backend**: Python FastAPI server with SQLite database

---

## ✅ Option 1: RECOMMENDED - Vercel + Railway (Best for Beginners)

### Frontend Deployment on Vercel (FREE)
**Why Vercel?**
- Super easy deployment
- Free tier is generous
- Automatic HTTPS
- Fast CDN globally
- No credit card needed

**Steps:**
1. Go to https://vercel.com
2. Sign up with GitHub account
3. Create new project → Import from GitHub
4. Select your repository
5. Deploy! (Takes 2 minutes)

**Cost:** FREE

---

### Backend Deployment on Railway (FREE)
**Why Railway?**
- Easy FastAPI deployment
- Free tier: $5/month credit (more than enough)
- Automatic SSL/HTTPS
- Environment variables support
- Database-friendly

**Steps:**
1. Go to https://railway.app
2. Sign up with GitHub
3. Create new project
4. Connect your GitHub repo
5. Deploy! Railway auto-detects FastAPI

**Cost:** FREE ($5 monthly credit is enough)

---

## ✅ Option 2: Netlify + Render (Alternative)

### Frontend on Netlify
- Similar to Vercel
- Go to https://netlify.com
- Connect GitHub repo
- Automatic deployment

### Backend on Render
- Go to https://render.com
- Create Web Service
- Connect GitHub
- Deploy FastAPI app

---

## ✅ Option 3: PythonAnywhere (All-in-One)
**Good for:** Running both frontend and backend in one place

1. Go to https://pythonanywhere.com
2. Sign up (free account available)
3. Upload files
4. Configure FastAPI app
5. Point domain

**Cost:** FREE with limitations (or $5/month for more)

---

## 📋 Pre-Deployment Checklist

Before deploying, you need to:

### 1. Create `requirements.txt` ✅ (Already have it)
Your `requirements.txt` is ready!

### 2. Create `.env` file for secrets
Create file: `backend/.env`
```
OPENAI_API_KEY=your_key_here
GOOGLE_GENAI_API_KEY=your_key_here
GMAIL_EMAIL=your_email@gmail.com
GMAIL_PASSWORD=your_app_password
```

### 3. Update API_BASE in frontend
In `frontend/app.js`, change:
```javascript
const API_BASE = "http://127.0.0.1:8000";
```
to:
```javascript
const API_BASE = "https://your-backend-url.railway.app";
```

### 4. Add CORS for frontend domain
In `backend/main.py`, update CORS:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.vercel.app", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 5. Create `Procfile` for Railway ✅ (Already have it)
Verify your Procfile:
```
web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

---

## 🎯 QUICKEST PATH (Recommended)

### Step 1: Prepare Repository (5 min)
```bash
# Make sure you have git initialized
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/ai-chatbot
git push -u origin main
```

### Step 2: Deploy Backend on Railway (10 min)
1. Go to https://railway.app
2. Sign in with GitHub
3. Click "Create new project"
4. Select "Deploy from GitHub repo"
5. Choose your `ai-chatbot` repo
6. Railway auto-detects `requirements.txt`
7. Done! You get a URL: `https://ai-chatbot-prod.railway.app`

### Step 3: Deploy Frontend on Vercel (5 min)
1. Go to https://vercel.com
2. Sign in with GitHub
3. Click "Add New..." → "Project"
4. Import your GitHub repo
5. Change build settings:
   - **Framework Preset:** Other
   - **Build Command:** (leave empty)
   - **Output Directory:** `frontend`
6. Add environment variable:
   - **Name:** `REACT_APP_API_BASE`
   - **Value:** `https://ai-chatbot-prod.railway.app`
7. Deploy!

### Step 4: Update Frontend Code (2 min)
Edit `frontend/app.js`:
```javascript
const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:8000";
```

---

## 🔐 Managing Secrets

### Method 1: Railway Environment Variables
1. Go to Railway dashboard
2. Select your project
3. Go to "Variables" tab
4. Add:
   - `OPENAI_API_KEY`
   - `GOOGLE_GENAI_API_KEY`
   - `GMAIL_EMAIL`
   - `GMAIL_PASSWORD`
5. Railway automatically injects them at runtime

### Method 2: Vercel Environment Variables
For frontend (if needed):
1. Project Settings → Environment Variables
2. Add variables

---

## 📊 Cost Breakdown

| Service | Free Tier | Cost |
|---------|-----------|------|
| Vercel (Frontend) | Unlimited | $0 |
| Railway (Backend) | $5/month credit | $0 |
| Domain (optional) | N/A | $10/year (Namecheap) |
| **TOTAL** | - | **$0-10/year** |

---

## 🛠️ Troubleshooting

### CORS Errors
Update `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For testing only!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 404 errors on frontend routing
In Vercel, go to Project Settings → Functions and add rewrite rules for SPA

### Database errors
Railway provides PostgreSQL for free. Consider migrating from SQLite:
```python
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
```

---

## 🚀 Final Deployment Steps

1. **Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Deploy Backend**
   - Railway auto-redeploys on push

3. **Deploy Frontend**
   - Vercel auto-redeploys on push

4. **Update frontend API URL**
   - Change in `app.js`
   - Commit and push

5. **Test**
   - Go to your Vercel URL
   - Test login, chat, upload features

---

## 📱 Monitor Your Deployment

- **Railway**: https://railway.app/dashboard
- **Vercel**: https://vercel.com/dashboard
- Both show logs, errors, and analytics

---

## 💡 Next Steps (Optional Upgrades)

- Add custom domain ($10-15/year)
- Upgrade to paid tier for more capacity
- Add CDN for better performance
- Use PostgreSQL instead of SQLite
- Add monitoring with Sentry
- Enable analytics with Vercel Analytics

---

## ❓ Common Questions

**Q: Will my API keys be exposed?**
A: No, Railway and Vercel keep secrets safe. Never commit `.env` files!

**Q: Can I use free tier forever?**
A: Yes! Railway's $5 credit renews monthly. More than enough.

**Q: How much traffic can I handle?**
A: Vercel handles millions of requests. Railway can handle moderate traffic.

**Q: Can I add a custom domain?**
A: Yes! Both services support custom domains ($10-15/year from registrars)

---

## 📚 Resources

- [Vercel Docs](https://vercel.com/docs)
- [Railway Docs](https://docs.railway.app)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [GitHub Pages (Frontend Alternative)](https://pages.github.com/)

---

**Ready to deploy? Start with Railway + Vercel above!** 🎉
