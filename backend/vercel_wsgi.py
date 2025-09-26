"""
WSGI config for Vercel deployment.
Optimized for serverless function execution.
"""

import os
import sys

def create_django_app():
    """Create Django WSGI application with proper error handling"""
    try:
        # Add the current directory to Python path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # Set Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
        os.environ.setdefault('DJANGO_USE_LIGHTWEIGHT', 'true')
        
        # Import and create Django WSGI application
        from django.core.wsgi import get_wsgi_application
        return get_wsgi_application()
        
    except Exception as e:
        # Return error handler if Django fails
        import json
        import traceback
        
        def error_handler(environ, start_response):
            status = '500 Internal Server Error'
            headers = [('Content-Type', 'application/json')]
            start_response(status, headers)
            
            error_data = {
                "error": "Django initialization failed",
                "message": str(e),
                "traceback": traceback.format_exc(),
                "python_path": sys.path[:3],
                "environment": dict(os.environ)
            }
            
            return [json.dumps(error_data, indent=2).encode('utf-8')]
        
        return error_handler

# Create the application
app = create_django_app()