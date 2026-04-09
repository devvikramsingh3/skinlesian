#!/usr/bin/env python3
"""
Main entry point for Vercel deployment
"""
import sys
import os

# Add backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import the Flask app
try:
    from app import app
    print("Flask app imported successfully")
except Exception as e:
    print(f"Error importing Flask app: {e}")
    raise

# For Vercel serverless functions - expose the Flask app as WSGI application
application = app

if __name__ == '__main__':
    app.run()