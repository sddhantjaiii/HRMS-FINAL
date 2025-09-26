"""
Simple health check views for debugging Vercel deployment
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os

@csrf_exempt
def health_check(request):
    """Basic health check endpoint"""
    try:
        return JsonResponse({
            'status': 'ok',
            'message': 'Django is running',
            'debug': settings.DEBUG,
            'django_use_lightweight': os.environ.get('DJANGO_USE_LIGHTWEIGHT', 'false'),
            'python_path': os.sys.path[:3],  # First 3 paths
            'environment': {
                'DATABASE_URL': 'SET' if os.environ.get('DATABASE_URL') else 'NOT_SET',
                'SECRET_KEY': 'SET' if os.environ.get('SECRET_KEY') else 'NOT_SET',
                'FRONTEND_URL': os.environ.get('FRONTEND_URL', 'NOT_SET'),
                'BACKEND_URL': os.environ.get('BACKEND_URL', 'NOT_SET'),
            }
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e),
            'error_type': type(e).__name__
        }, status=500)

@csrf_exempt
def database_check(request):
    """Database connection check"""
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
        
        return JsonResponse({
            'status': 'ok',
            'message': 'Database connection successful',
            'result': result[0] if result else None
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Database connection failed: {str(e)}',
            'error_type': type(e).__name__
        }, status=500)