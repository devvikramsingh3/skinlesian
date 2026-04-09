#!/usr/bin/env python3
"""
Basic Python function for Vercel (no Flask)
"""

def handler(event, context):
    """Vercel serverless function handler"""
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html"
        },
        "body": """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Skin Lesion Classifier - Python Test</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
                .container { max-width: 800px; margin: 0 auto; background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; backdrop-filter: blur(10px); }
                .success { color: #4CAF50; font-size: 28px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
                .status { background: rgba(76, 175, 80, 0.2); padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 4px solid #4CAF50; }
                .features { background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 20px 0; }
                .feature { margin: 10px 0; padding: 8px; background: rgba(255,255,255,0.1); border-radius: 5px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1 class="success">🎉 SUCCESS: Vercel Python Function Working!</h1>
                <div class="status">
                    <p><strong>✅ Status:</strong> Python serverless function executing successfully</p>
                    <p><strong>✅ Runtime:</strong> Python 3.11 on Vercel</p>
                    <p><strong>✅ Response:</strong> HTML generated dynamically</p>
                    <p><strong>📅 Date:</strong> April 10, 2026</p>
                </div>

                <h2>🚀 Next Steps for Full Application:</h2>
                <div class="features">
                    <div class="feature">🔐 <strong>User Authentication:</strong> Login/Register system with Flask-Login</div>
                    <div class="feature">📊 <strong>AI Analysis:</strong> Skin lesion classification with TensorFlow</div>
                    <div class="feature">📋 <strong>Patient History:</strong> Database tracking with SQLAlchemy</div>
                    <div class="feature">🎨 <strong>Modern UI:</strong> Responsive design with CSS</div>
                    <div class="feature">📱 <strong>Mobile Ready:</strong> Cross-device compatibility</div>
                    <div class="feature">☁️ <strong>Cloud Database:</strong> PostgreSQL for persistent storage</div>
                </div>

                <hr style="border: none; height: 1px; background: rgba(255,255,255,0.3);">
                <p style="text-align: center; font-style: italic;">
                    Skin Lesion Classifier - Full application integration in progress...
                </p>
            </div>
        </body>
        </html>
        """
    }

# Expose both handler and application names for Vercel compatibility
application = handler

# For local testing
if __name__ == '__main__':
    # Simulate Vercel event
    result = handler({}, {})
    print("Status Code:", result["statusCode"])
    print("Response length:", len(result["body"]))
    print("First 200 chars:", result["body"][:200])