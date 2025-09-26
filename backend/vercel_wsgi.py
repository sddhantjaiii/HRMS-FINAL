"""
WSGI config for Vercel deployment.
Optimized for serverless function execution.
"""

import os
from django.core.wsgi import get_wsgi_application

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

# Create the WSGI application
application = get_wsgi_application()

# Vercel serverless function handler
def handler(request, context):
    """
    Vercel serverless function handler
    """
    return application(request.environ, context)

# Export for Vercel
app = application