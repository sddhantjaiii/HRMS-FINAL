"""
WSGI config for Vercel deployment.
Optimized for serverless function execution.
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

# Create the WSGI application
application = get_wsgi_application()

# Export for Vercel - this is the main handler
app = application