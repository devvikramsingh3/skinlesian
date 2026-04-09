# Quick Start - Deploy to Vercel in 5 Minutes

## ✅ Step 1: Prepare Your Code
```bash
# Make sure everything is committed
git add .
git commit -m "Prepare for Vercel deployment"

# Push to GitHub
git push origin main
```

## ✅ Step 2: Create Vercel Account
1. Go to https://vercel.com
2. Click **"Sign Up"** → Choose **"Continue with GitHub"**
3. Authorize Vercel to access your GitHub

## ✅ Step 3: Deploy Project
1. Log in to Vercel Dashboard
2. Click **"New Project"**
3. Select your **`skin-lesion-classifier`** repository
4. Click **"Import"**

## ✅ Step 4: Configure Environment Variables
In the import dialog, scroll to **"Environment Variables"**:
1. Add: `FLASK_ENV` → `production`
2. Add: `SECRET_KEY` → Generate a random key (use online generator)
3. Click **"Deploy"**

## ✅ Step 5: Wait for Deployment
- Watch the build process in real-time
- Deployment takes 2-5 minutes
- You'll get a live URL like: `https://skin-lesion-classifier.vercel.app`

## 🎉 Done!
Your app is now live! 

### First Time Setup:
1. Visit your live URL
2. Click "Register" to create an account
3. Log in and start analyzing images

## 📊 Test the Deployment
```bash
# Check your app status
curl https://your-app.vercel.app/

# View logs
# Go to Vercel Dashboard → Project → Deployments → Click latest
```

## 🔧 Future Updates
Every time you push to GitHub, Vercel automatically deploys:
```bash
# Make changes locally
git add .
git commit -m "New feature"
git push origin main
# Vercel automatically deploys within 1-2 minutes
```

## ⚠️ Important Notes

### Database
- Currently uses SQLite (for testing only)
- **For production**: Add PostgreSQL database
  - Option 1: Use Vercel Postgres (integrated)
  - Option 2: Railway, Heroku, or AWS RDS
  - Set `DATABASE_URL` environment variable

### Machine Learning
- Currently uses **mock predictions** (TensorFlow not available)
- Real predictions require GPU support (see DEPLOYMENT.md for options)

### Security
- Change `SECRET_KEY` to a strong random value
- Don't commit `.env` files
- Use Vercel's environment variables for secrets

## 🆘 Troubleshooting

### Build fails?
- Check Vercel logs: Dashboard → Deployments → Latest → Logs
- Ensure `requirements.txt` has all dependencies
- Python 3.11 is used (optimized for Vercel)

### App crashes?
- Check Function Logs in Vercel Dashboard
- Look for import errors or missing modules
- Verify environment variables are set

### Features not working?
- Database not persisting? → Need PostgreSQL
- ML predictions wrong? → Using mock data currently

## 📚 Learn More
- Full guide: See `DEPLOYMENT.md`
- Vercel docs: https://vercel.com/docs
- Flask on Vercel: https://vercel.com/docs/frameworks/flask
