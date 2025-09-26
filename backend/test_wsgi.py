"""
Minimal WSGI test for debugging Vercel deployment issues
"""

import os
import sys
import json
from datetime import datetime

def simple_app(environ, start_response):
    """Simple WSGI app for testing"""
    try:
        # Basic response
        status = '200 OK'
        headers = [('Content-Type', 'application/json')]
        start_response(status, headers)
        
        response_data = {
            "status": "ok",
            "message": "Simple WSGI app is working",
            "timestamp": datetime.now().isoformat(),
            "python_version": sys.version,
            "environment_vars": {
                "DJANGO_SETTINGS_MODULE": os.environ.get('DJANGO_SETTINGS_MODULE'),
                "DJANGO_USE_LIGHTWEIGHT": os.environ.get('DJANGO_USE_LIGHTWEIGHT'),
                "DATABASE_URL": "SET" if os.environ.get('DATABASE_URL') else "NOT_SET",
                "SECRET_KEY": "SET" if os.environ.get('SECRET_KEY') else "NOT_SET"
            },
            "python_path": sys.path[:5]  # First 5 paths
        }
        
        return [json.dumps(response_data, indent=2).encode('utf-8')]
        
    except Exception as e:
        # Error response
        status = '500 Internal Server Error'
        headers = [('Content-Type', 'application/json')]
        start_response(status, headers)
        
        error_data = {
            "status": "error",
            "message": str(e),
            "error_type": type(e).__name__,
            "python_path": sys.path[:3]
        }
        
        return [json.dumps(error_data, indent=2).encode('utf-8')]

# Export the simple app
app = simple_app