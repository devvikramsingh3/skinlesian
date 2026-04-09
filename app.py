#!/usr/bin/env python3
"""
Ultra-minimal Vercel test app
"""
from flask import Flask

# Create a minimal Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Skin Lesion Classifier - Vercel Test</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f0f0f0; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
            .success { color: green; font-size: 24px; }
            .status { background: #e8f5e8; padding: 10px; border-radius: 5px; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="success">✅ Vercel Deployment Successful!</h1>
            <div class="status">
                <p><strong>Status:</strong> Flask app working on Vercel serverless</p>
                <p><strong>Python Version:</strong> 3.11</p>
                <p><strong>Framework:</strong> Flask</p>
            </div>
            <p>This confirms that Vercel can run Python Flask applications successfully.</p>
            <hr>
            <h3>Next Steps for Full App:</h3>
            <ul>
                <li>🔐 Add user authentication system</li>
                <li>📊 Integrate skin lesion analysis model</li>
                <li>📋 Add patient history database</li>
                <li>🎨 Implement modern UI with CSS</li>
                <li>📱 Add responsive design</li>
            </ul>
            <p><a href="/test">Test JSON API</a></p>
        </div>
    </body>
    </html>
    """

@app.route('/test')
def test():
    return {"message": "Vercel Python function working!", "status": "success", "timestamp": "2026-04-10"}

if __name__ == '__main__':
    app.run()

if __name__ == '__main__':
    app.run()