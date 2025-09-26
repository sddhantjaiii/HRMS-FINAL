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
        
    except Exception as error:
        # Return error handler if Django fails
        import json
        import traceback
        
        # Capture the error details immediately
        error_message = str(error)
        error_traceback = traceback.format_exc()
        
        def error_handler(environ, start_response):
            status = '500 Internal Server Error'
            headers = [('Content-Type', 'application/json')]
            start_response(status, headers)
            
            error_data = {
                "error": "Django initialization failed",
                "message": error_message,
                "traceback": error_traceback,
                "python_path": sys.path[:3],
                "environment": {k: v for k, v in os.environ.items() if not k.startswith('AWS')}
            }
            
            return [json.dumps(error_data, indent=2).encode('utf-8')]
        
        return error_handler

# Create the application with fallback
try:
    app = create_django_app()
except Exception as e:
    # Fallback WSGI app if Django creation fails
    import json
    
    def fallback_app(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-Type', 'application/json')]
        start_response(status, headers)
        
        error_data = {
            "error": "Complete application failure",
            "message": str(e),
            "path_info": environ.get('PATH_INFO', 'unknown'),
            "request_method": environ.get('REQUEST_METHOD', 'unknown')
        }
        
        return [json.dumps(error_data, indent=2).encode('utf-8')]
    
    app = fallback_app