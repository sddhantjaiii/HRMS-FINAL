#!/usr/bin/env python3
"""
Test Django setup in lightweight mode
"""
import os
import sys

# Add backend to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Set environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
os.environ.setdefault('DJANGO_USE_LIGHTWEIGHT', 'true')

print(f"Python path: {sys.path[:3]}")
print(f"Django settings module: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
print(f"Lightweight mode: {os.environ.get('DJANGO_USE_LIGHTWEIGHT')}")

try:
    print("\n1. Testing Django core imports...")
    import django
    print(f"✓ Django version: {django.get_version()}")
    
    print("\n2. Testing settings import...")
    from django.conf import settings
    print(f"✓ Settings imported")
    
    print("\n3. Testing Django setup...")
    django.setup()
    print(f"✓ Django setup complete")
    
    print("\n4. Testing WSGI application...")
    from django.core.wsgi import get_wsgi_application
    wsgi_app = get_wsgi_application()
    print(f"✓ WSGI application created: {type(wsgi_app)}")
    
    print("\n5. Testing basic settings...")
    print(f"DEBUG: {settings.DEBUG}")
    print(f"SECRET_KEY set: {'SECRET_KEY' in dir(settings) and bool(settings.SECRET_KEY)}")
    print(f"DATABASES configured: {bool(settings.DATABASES)}")
    
    print("\n✅ All Django tests passed!")
    
except Exception as e:
    print(f"\n❌ Django test failed: {e}")
    import traceback
    print(f"Traceback:\n{traceback.format_exc()}")