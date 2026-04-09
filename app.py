#!/usr/bin/env python3
"""
Main entry point for Vercel deployment
"""
import sys
import os

# Add backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import and run the Flask app
from app import app

# For Vercel serverless functions
def handler(event, context):
    return app(event, context)

if __name__ == '__main__':
    app.run()