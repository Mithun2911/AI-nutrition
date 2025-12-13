# 🚀 Free Deployment Guide - NutriVision AI

This guide will help you deploy your NutriVision AI app to free hosting platforms so you can share it with your friends!

## 📋 Prerequisites

1. A GitHub account (free) - [Sign up here](https://github.com)
2. Your code ready to deploy

---

## 🌐 Option 1: Render (Recommended - Easiest)

**Free Tier:** 750 hours/month (enough for 24/7 operation)

### Steps:

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/nutrivision-ai.git
   git push -u origin main
   ```

2. **Deploy on Render:**
   - Go to [render.com](https://render.com) and sign up (free)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name:** nutrivision-ai (or any name)
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements_deploy.txt`
     - **Start Command:** `gunicorn app:app`
     - **Plan:** Free
   - Click "Create Web Service"
   - Wait 5-10 minutes for deployment
   - Your app will be live at: `https://nutrivision-ai.onrender.com`

3. **Important Settings:**
   - Under "Environment" tab, add:
     - `FLASK_ENV=production`
     - `PYTHON_VERSION=3.11.9`

---

## 🚂 Option 2: Railway (Great Free Tier)

**Free Tier:** $5 credit/month (plenty for a small app)

### Steps:

1. **Push to GitHub** (same as Option 1)

2. **Deploy on Railway:**
   - Go to [railway.app](https://railway.app) and sign up
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Python apps
   - It will automatically:
     - Detect `requirements_deploy.txt`
     - Use `Procfile` for start command
     - Deploy your app
   - Your app will be live at: `https://your-app-name.up.railway.app`

3. **Configure:**
   - Add environment variable: `FLASK_ENV=production`
   - Railway automatically sets `PORT` environment variable

---

## 🐍 Option 3: PythonAnywhere (Simple & Reliable)

**Free Tier:** Limited but good for testing

### Steps:

1. **Sign up:** Go to [pythonanywhere.com](https://www.pythonanywhere.com) (free account)

2. **Upload your code:**
   - Go to "Files" tab
   - Upload all your files (or use Git)
   - Or use "Bash" console and clone from GitHub:
     ```bash
     git clone https://github.com/YOUR_USERNAME/nutrivision-ai.git
     ```

3. **Install dependencies:**
   - Open "Bash" console
   ```bash
   cd nutrivision-ai
   pip3.10 install --user -r requirements_deploy.txt
   ```

4. **Create Web App:**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration" → Python 3.10
   - In "WSGI configuration file", edit and add:
     ```python
     import sys
     path = '/home/YOUR_USERNAME/nutrivision-ai'
     if path not in sys.path:
         sys.path.append(path)
     
     from app import app as application
     ```

5. **Configure:**
   - Set "Source code" to your project folder
   - Click "Reload" button
   - Your app will be at: `https://YOUR_USERNAME.pythonanywhere.com`

---

## 🎨 Option 4: Replit (Easiest for Beginners)

**Free Tier:** Always-on option available

### Steps:

1. **Go to Replit:**
   - Visit [replit.com](https://replit.com) and sign up

2. **Create New Repl:**
   - Click "Create Repl"
   - Choose "Flask" template
   - Name it "nutrivision-ai"

3. **Upload Files:**
   - Drag and drop all your project files
   - Or use "Upload folder" option

4. **Install Dependencies:**
   - Replit auto-installs from `requirements_deploy.txt`
   - Or run in Shell: `pip install -r requirements_deploy.txt`

5. **Run:**
   - Click "Run" button
   - Your app will be live immediately
   - Share the URL with friends!

---

## 📝 Quick Setup Checklist

Before deploying, make sure:

- [ ] All files are committed to Git
- [ ] `requirements_deploy.txt` exists (lightweight version)
- [ ] `Procfile` exists (for Render/Railway)
- [ ] `runtime.txt` exists (for Python version)
- [ ] No hardcoded localhost URLs in code
- [ ] Environment variables are set (if needed)

---

## 🔧 Troubleshooting

### App won't start:
- Check build logs for errors
- Ensure `gunicorn` is in `requirements_deploy.txt`
- Verify `Procfile` has correct command: `web: gunicorn app:app`

### Static files not loading:
- Make sure `static/` folder is in repository
- Check file paths use `/static/` not absolute paths

### Upload folder issues:
- Some platforms have read-only filesystems
- Consider using cloud storage (AWS S3, Cloudinary) for uploads
- Or use temporary storage for demo

### Port errors:
- The app automatically uses `PORT` environment variable
- Don't hardcode port numbers

---

## 🌍 Recommended: Render or Railway

**For beginners:** Use **Render** - it's the easiest
**For more control:** Use **Railway** - better free tier

Both are excellent choices and will keep your app running 24/7 for free!

---

## 📞 Need Help?

If you encounter issues:
1. Check the deployment platform's logs
2. Verify all files are uploaded correctly
3. Make sure Python version matches (3.11.9)
4. Check that `gunicorn` is installed

---

## 🎉 After Deployment

Once deployed, you'll get a URL like:
- `https://nutrivision-ai.onrender.com` (Render)
- `https://your-app.up.railway.app` (Railway)

Share this URL with your friends and they can use your app from anywhere!

---

**Good luck with your deployment! 🚀**

