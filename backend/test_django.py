#!/usr/bin/env python
"""
Simple Django settings test
"""
import os
import sys

# Set up the environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
os.environ.setdefault('DJANGO_USE_LIGHTWEIGHT', 'true')

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    print("Testing Django settings import...")
    
    # Test basic imports
    import django
    print(f"✅ Django version: {django.get_version()}")
    
    # Test settings import
    from django.conf import settings
    print("✅ Django settings imported successfully")
    
    # Test app imports
    django.setup()
    print("✅ Django setup completed")
    
    # Test WSGI
    from django.core.wsgi import get_wsgi_application
    app = get_wsgi_application()
    print("✅ WSGI application created successfully")
    
    print("\n🎉 All tests passed! Django should work on Vercel.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    print(traceback.format_exc())
    sys.exit(1)