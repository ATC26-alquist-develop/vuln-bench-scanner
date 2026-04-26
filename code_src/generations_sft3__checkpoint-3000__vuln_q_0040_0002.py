from django.conf import settings
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

class CORSMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Only allow requests from whitelisted domains
        allowed_origins = settings.ALLOWED_CORS_ORIGINS
        
        # Check if the request origin is in the whitelist
        if not request.headers.get('Origin') in allowed_origins:
            return HttpResponseForbidden("CORS not allowed")
        
        # Set CORS headers
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = request.headers.get('Origin', '')
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response