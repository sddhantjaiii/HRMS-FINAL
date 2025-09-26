#!/usr/bin/env python3
"""
Test the complete WSGI application that will be deployed to Vercel
"""
import os
import sys

# Add backend to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

def test_wsgi_app():
    """Test the WSGI application"""
    try:
        print("Testing WSGI application import...")
        from vercel_wsgi import app
        print(f"✓ WSGI app imported: {type(app)}")
        
        # Create a simple test environment
        import io
        environ = {
            'REQUEST_METHOD': 'GET',
            'PATH_INFO': '/health/',
            'QUERY_STRING': '',
            'CONTENT_TYPE': '',
            'CONTENT_LENGTH': '0',
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': '8000',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'http',
            'wsgi.input': io.BytesIO(b''),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': True,
            'wsgi.run_once': False,
        }
        
        # Test response capture
        response_data = []
        status_data = []
        headers_data = []
        
        def start_response(status, headers, exc_info=None):
            status_data.append(status)
            headers_data.append(headers)
        
        print("\nTesting WSGI application call...")
        response = app(environ, start_response)
        
        if hasattr(response, '__iter__'):
            response_body = b''.join(response).decode('utf-8')
            print(f"✓ Response status: {status_data[0] if status_data else 'No status'}")
            print(f"✓ Response headers: {len(headers_data[0]) if headers_data else 0} headers")
            print(f"✓ Response body length: {len(response_body)} characters")
            
            if len(response_body) > 200:
                print(f"Response preview: {response_body[:200]}...")
            else:
                print(f"Response body: {response_body}")
                
            return True
        else:
            print(f"❌ Invalid response type: {type(response)}")
            return False
            
    except Exception as e:
        print(f"❌ WSGI test failed: {e}")
        import traceback
        print(f"Traceback:\n{traceback.format_exc()}")
        return False

if __name__ == "__main__":
    print("=== WSGI Application Test ===")
    success = test_wsgi_app()
    print(f"\n{'✅ Test PASSED' if success else '❌ Test FAILED'}")