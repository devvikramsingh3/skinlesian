# Deployment Guide - Vercel

## Prerequisites
- GitHub account (code must be pushed to GitHub)
- Vercel account (sign up at https://vercel.com)
- (Optional) PostgreSQL database for production

## Step 1: Push Code to GitHub

```bash
git init
git add .
git commit -m "Add login and patient history features"
git remote add origin https://github.com/YOUR_USERNAME/skin-lesion-classifier.git
git branch -M main
git push -u origin main
```

## Step 2: Create Vercel Account
1. Go to https://vercel.com
2. Sign up with GitHub
3. Authorize Vercel to access your repositories

## Step 3: Deploy to Vercel

### Option A: Automatic (Recommended)
1. Go to https://vercel.com/new
2. Select "Import Git Repository"
3. Find and select `skin-lesion-classifier`
4. Click "Import"

### Option B: Using Vercel CLI
```bash
npm i -g vercel
cd skin-lesion-classifier
vercel
```

## Step 4: Configure Environment Variables

In Vercel Dashboard:
1. Go to your project settings
2. Click "Environment Variables"
3. Add these variables:

```
FLASK_ENV = production
SECRET_KEY = (use strong random key like: $(openssl rand -hex 32))
```

Optional for custom database:
```
DATABASE_URL = postgresql://user:password@host:port/database
```

## Step 5: Database Setup

### SQLite (Default - Local Only)
- Works for local development
- NOT recommended for Vercel (files not persistent)

### PostgreSQL (Recommended for Production)

1. Set up PostgreSQL on:
   - **Vercel Postgres** (integrated): https://vercel.com/docs/postgres
   - **Railway**: https://railway.app
   - **Heroku**: https://www.heroku.com
   - **AWS RDS**: https://aws.amazon.com/rds/

2. Get connection string and add to environment variables:
   ```
   DATABASE_URL = postgresql://user:password@host:5432/dbname
   ```

3. Update `requirements.txt` if using PostgreSQL:
   ```
   pip install psycopg2-binary
   ```

## Step 6: Deploy

After setting environment variables:
1. Vercel will automatically redeploy
2. Your app will be live at `https://your-project-name.vercel.app`
3. Check deployment status in Vercel Dashboard

## Monitoring & Logs

1. **View Logs**: 
   - Go to Vercel Dashboard → Project → Deployments
   - Click deployment → Details → Logs

2. **Check Status**:
   - Check health endpoint: `https://your-app.vercel.app/`

## Limitations on Vercel

### Current Setup
- Works with SQLite for testing
- Database resets on each deployment
- Mock predictions (TensorFlow not available on Vercel)

### For Production
- **Database**: Switch to PostgreSQL for persistent data
- **ML Model**: TensorFlow requires custom buildpacks; consider using:
  - Pre-computed predictions
  - Alternative ML frameworks
  - AWS Lambda with GPU support

## Troubleshooting

### "Module not found" errors
- Check `requirements.txt` has all dependencies
- Vercel logs show build errors

### Database not persisting
- SQLite files are ephemeral on Vercel
- Use PostgreSQL for production

### Deployment fails
1. Check build logs in Vercel Dashboard
2. Ensure all imports are available in `requirements.txt`
3. Verify `vercel.json` configuration

## Updating Your App

After making changes:
```bash
git add .
git commit -m "describe changes"
git push origin main
```

Vercel automatically triggers new deployment on push!

## Cost

Vercel free tier includes:
- Unlimited deployments
- 100 GB bandwidth/month
- Built-in HTTPS
- Basic analytics

Paid plans available for higher usage.
