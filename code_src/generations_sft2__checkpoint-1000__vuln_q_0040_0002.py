from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import secure_etag
from django.views.decorators.http import require_http_methods
import re

def cors_allow_all():
    """
    Secure CORS configuration allowing all origins with specific methods.
    """
    def decorator(view_func):
        @csrf_exempt
        @require_http_methods(["OPTIONS"])
        @secure_etag
        def _cors_view(request):
            # Only allow specific HTTP methods
            allowed_methods = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
            if request.method not in allowed_methods:
                return HttpResponse(
                    'Method Not Allowed',
                    status=405,
                    content_type='text/plain'
                )
            
            # Only allow specific headers
            allowed_headers = ['Content-Type', 'Authorization', 'X-Requested-With']
            if not all(header in request.headers for header in allowed_headers):
                return HttpResponse(
                    'Bad Request',
                    status=400,
                    content_type='text/plain'
                )
            
            # Allow all origins
            response = HttpResponse(
                'Access-Control-Allow-Origin: *',
                content_type='text/plain'
            )
            
            # Set other CORS headers
            response['Access-Control-Allow-Methods'] = ', '.join(allowed_methods)
            response['Access-Control-Allow-Headers'] = ', '.join(allowed_headers)
            
            return response
        return _cors_view
    return decorator