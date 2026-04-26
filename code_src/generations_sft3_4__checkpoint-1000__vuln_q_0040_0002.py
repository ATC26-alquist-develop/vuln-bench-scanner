from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

class CORSMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Validate CORS settings
        if not hasattr(settings, 'CORS_ORIGIN_WHITELIST'):
            raise ImproperlyConfigured("CORS_ORIGIN_WHITELIST must be defined in settings.py")
        
        # Check if the request origin is in the whitelist
        origin = request.headers.get('Origin')
        if not origin:
            return HttpResponse('No Origin header', status=400)
        
        if origin not in settings.CORS_ORIGIN_WHITELIST:
            return HttpResponse('Access Denied', status=403)
        
        # Set CORS headers
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = origin
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        
        return response