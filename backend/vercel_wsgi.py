"""
WSGI config for Vercel deployment.
Optimized for serverless function execution with error handling.
"""

import os
import sys
import logging

# Configure logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Add the backend directory to Python path
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)
    
    logger.info(f"Added to Python path: {backend_dir}")
    
    # Set required environment variables for Vercel
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
    os.environ.setdefault('DJANGO_USE_LIGHTWEIGHT', 'true')
    
    # Import Django WSGI
    from django.core.wsgi import get_wsgi_application
    
    # Create the WSGI application
    application = get_wsgi_application()
    logger.info("Django WSGI application created successfully")
    
    # Export for Vercel - this is the main handler
    app = application

except Exception as e:
    logger.error(f"Error initializing Django application: {str(e)}")
    import traceback
    logger.error(traceback.format_exc())
    
    # Create a simple error application
    def error_app(environ, start_response):
        status = '500 Internal Server Error'
        headers = [('Content-type', 'application/json')]
        start_response(status, headers)
        error_message = {
            "error": "Django initialization failed",
            "message": str(e),
            "path": backend_dir
        }
        import json
        return [json.dumps(error_message).encode('utf-8')]
    
    app = error_app