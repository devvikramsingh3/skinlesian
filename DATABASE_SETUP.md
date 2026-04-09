# PostgreSQL Setup Guide for Production

## Why PostgreSQL?
- SQLite is for local development only
- Vercel's filesystem is ephemeral (resets on each deployment)
- PostgreSQL persists data across deployments
- Free options available

## Option 1: Vercel Postgres (Recommended - Easiest)

### Setup:
1. Vercel Dashboard → Select your project
2. Go to **Storage** tab
3. Click **Create** → **Postgres**
4. Click **Create** (uses 5GB free tier)
5. Copy the connection string

### Add to Vercel:
1. Go to **Settings** → **Environment Variables**
2. Add: `DATABASE_URL` = (paste the connection string)
3. Redeploy

### Update requirements.txt:
```bash
pip install psycopg2-binary
```

---

## Option 2: Railway.app (Good Alternative)

### Setup:
1. Go to https://railway.app
2. Click **New Project** → **Create**
3. Add **PostgreSQL** plugin
4. Copy connection URL from PostgreSQL service

### Add to Vercel:
1. Settings → Environment Variables
2. Add: `DATABASE_URL` = `postgresql://user:pass@host:port/dbname`
3. Rebuild

---

## Option 3: Other Providers

### Heroku Postgres
- Sign up at heroku.com
- `heroku addons:create heroku-postgresql:mini`
- Copy DATABASE_URL

### AWS RDS
- RDS → Databases → Create
- PostgreSQL database
- Get connection endpoint

### Neon (Fast Growing)
- https://neon.tech
- Serverless Postgres
- Copy connection string

---

## Testing Connection

After setting DATABASE_URL:

```python
# Add this to app.py temporarily
@app.route("/db-test")
def db_test():
    try:
        db.session.execute(db.select(User).limit(1))
        return jsonify({"status": "Database connected successfully!"})
    except Exception as e:
        return jsonify({"status": f"Database error: {str(e)}"})
```

Then visit: `https://your-app.vercel.app/db-test`

---

## Initialize Database Schema

After first deployment with DATABASE_URL:

```bash
# Locally (won't work on Vercel)
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database initialized')"
```

Or tables auto-create on first request via:
```python
with app.app_context():
    db.create_all()
```

---

## Troubleshooting

### "psycopg2 not found"
- Add to requirements.txt: `psycopg2-binary>=2.9.0`
- Redeploy

### Connection timeout
- Check DATABASE_URL format
- Verify database is running
- Check firewall rules

### Still using SQLite?
- Vercel might not recognize DATABASE_URL
- Check environment variables are lowercase
- Use `SQLALCHEMY_DATABASE_URI` instead

### Reset database
- Delete all tables (careful!)
- Vercel → Deployments → Redeploy
- Tables auto-create from models.py
