#!/usr/bin/env python3
"""
Main entry point for Vercel deployment
"""
import sys
import os

# Add backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Import the Flask app directly
try:
    from backend.app import app
    print("Flask app imported successfully from backend.app")
except Exception as e:
    print(f"Error importing Flask app: {e}")
    import traceback
    traceback.print_exc()
    raise

# For Vercel serverless functions
if __name__ == '__main__':
    app.run()

if __name__ == '__main__':
    app.run()