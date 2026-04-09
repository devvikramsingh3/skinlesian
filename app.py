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
    from app import app as flask_app
    print("Flask app imported successfully")
    # Expose as 'app' for Vercel
    app = flask_app
except Exception as e:
    print(f"Error importing Flask app: {e}")
    raise

if __name__ == '__main__':
    app.run()