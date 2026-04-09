#!/usr/bin/env python3
"""
Minimal Vercel Python function
"""

def handler(event, context):
    """Vercel serverless function handler"""
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/plain"},
        "body": "Hello from Vercel Python function!"
    }

# Expose both handler and application names for Vercel compatibility
handler = handler
application = handler

# For local testing
if __name__ == '__main__':
    result = handler({}, {})
    print(result)
