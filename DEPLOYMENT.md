# 🚀 DataFixer Deployment Guide

This guide will help you deploy your DataFixer application to various platforms for 24/7 availability.

## 📋 Prerequisites

- GitHub account
- Your code pushed to a GitHub repository
- Basic understanding of environment variables

## 🌟 Deployment Options

### Option 1: Railway (Recommended - Easiest)

**Why Railway?** Free tier, automatic deployments, simple setup.

1. **Setup:**
   ```bash
   # No CLI needed - use web interface
   ```

2. **Deploy Steps:**
   - Visit [Railway.app](https://railway.app)
   - Sign in with GitHub
   - Click "Deploy from GitHub repo"
   - Select your DataFixer repository
   - Railway auto-detects it's a Python app

3. **Environment Variables:**
   Add these in Railway dashboard:
   ```
   ENV=production
   HOST=0.0.0.0
   PORT=8000
   ```

4. **Custom Domain:**
   - Railway provides a free subdomain: `your-app.railway.app`
   - Can add custom domain in settings

---

### Option 2: Heroku (Popular)

**Why Heroku?** Well-established, good documentation, free tier.

1. **Install Heroku CLI:**
   ```bash
   # Windows
   winget install Heroku.CLI
   
   # macOS
   brew tap heroku/brew && brew install heroku
   ```

2. **Deploy:**
   ```bash
   cd "c:\SDC gemni\DataFixer"
   heroku login
   heroku create your-app-name
   git init
   git add .
   git commit -m "Deploy DataFixer"
   git push heroku main
   ```

3. **Set Environment Variables:**
   ```bash
   heroku config:set ENV=production
   heroku config:set HOST=0.0.0.0
   ```

---

### Option 3: Render (Free & Simple)

**Why Render?** Free tier, automatic HTTPS, easy setup.

1. **Setup:**
   - Visit [Render.com](https://render.com)
   - Connect GitHub account
   - Create "New Web Service"
   - Select your DataFixer repo

2. **Configuration:**
   - **Build Command:** `cd backend && pip install -r requirements.txt`
   - **Start Command:** `cd backend && python -m uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Environment Variables:**
   ```
   ENV=production
   PYTHONPATH=backend
   ```

---

### Option 4: Docker Deployment (VPS/Cloud)

**Why Docker?** Consistent across platforms, scalable.

1. **Build & Run Locally:**
   ```bash
   cd "c:\SDC gemni\DataFixer"
   docker build -t datafixer-api .
   docker run -p 8000:8000 datafixer-api
   ```

2. **Deploy to DigitalOcean/AWS/Azure:**
   ```bash
   # Push to container registry
   docker tag datafixer-api your-registry/datafixer-api
   docker push your-registry/datafixer-api
   
   # Deploy on cloud platform
   ```

---

## 🔧 Frontend Deployment

### Deploy Frontend to Vercel (Recommended)

1. **Prepare Frontend:**
   ```bash
   cd "c:\SDC gemni\DataFixer\data-cleaner-ui"
   ```

2. **Update API URL:**
   Create `.env.production`:
   ```
   VITE_API_URL=https://your-backend-url.railway.app
   ```

3. **Deploy:**
   - Install Vercel CLI: `npm i -g vercel`
   - Run: `vercel --prod`
   - Follow prompts

### Alternative: Netlify

1. **Build:**
   ```bash
   npm run build
   ```

2. **Deploy:**
   - Visit [Netlify.com](https://netlify.com)
   - Drag & drop `dist` folder
   - Or connect GitHub repo

---

## ⚙️ Environment Configuration

### Backend Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `ENV` | Environment mode | `production` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `CORS_ORIGINS` | Allowed origins | `https://your-frontend.vercel.app` |

### Frontend Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `https://your-api.railway.app` |

---

## 🔒 Production Security Checklist

- [ ] Set `ENV=production` to hide API docs
- [ ] Configure proper CORS origins (no wildcards)
- [ ] Use HTTPS for both frontend and backend
- [ ] Keep dependencies updated
- [ ] Monitor logs and errors

---

## 🚦 Quick Start Commands

### Test Locally
```bash
# Backend
cd backend
python main.py

# Frontend
cd data-cleaner-ui
npm run dev
```

### Deploy Everything
```bash
# 1. Deploy backend to Railway (via web interface)
# 2. Deploy frontend to Vercel
cd data-cleaner-ui
vercel --prod
```

---

## 🆘 Troubleshooting

### Common Issues:

1. **Import Errors:** 
   - Check `requirements.txt` has all dependencies
   - Verify Python version compatibility

2. **CORS Errors:**
   - Update `CORS_ORIGINS` with your frontend URL
   - Ensure no trailing slashes

3. **Port Issues:**
   - Railway/Heroku auto-assign ports
   - Use `PORT` environment variable

4. **Build Failures:**
   - Check Python version (3.12 recommended)
   - Verify all files are committed to git

### Getting Help:
- Railway: Check deployment logs in dashboard
- Heroku: `heroku logs --tail`
- Render: View logs in service dashboard

---

## 🎉 Success!

Once deployed:
- ✅ Your API runs 24/7
- ✅ Accessible worldwide
- ✅ Professional domain
- ✅ Automatic scaling
- ✅ Works when your laptop is off

Your users can access the app anytime at your deployed URLs!