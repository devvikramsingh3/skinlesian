#!/usr/bin/env python3
"""
Minimal Vercel test app
"""
from flask import Flask, render_template_string

# Create a minimal Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Skin Lesion Classifier - Vercel Test</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            .success { color: green; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="success">✅ Vercel Deployment Successful!</h1>
            <p>This is a minimal test version of the Skin Lesion Classifier.</p>
            <p><strong>Status:</strong> Basic Flask app working on Vercel</p>
            <p><strong>Next steps:</strong> Full app integration pending</p>
            <hr>
            <h3>Available Features (Coming Soon):</h3>
            <ul>
                <li>🔐 User Authentication (Login/Register)</li>
                <li>📊 Skin Lesion Analysis</li>
                <li>📋 Patient History Tracking</li>
                <li>🎨 Modern UI with CSS</li>
            </ul>
        </div>
    </body>
    </html>
    """)

@app.route('/test')
def test():
    return {"message": "Vercel Python function working!", "status": "success"}

if __name__ == '__main__':
    app.run()

if __name__ == '__main__':
    app.run()