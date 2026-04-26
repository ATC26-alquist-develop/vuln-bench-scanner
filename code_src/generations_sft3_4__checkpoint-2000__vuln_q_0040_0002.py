from django.conf import settings
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin

class CORSMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Only allow requests from whitelisted domains
        allowed_origins = settings.ALLOWED_CORS_ORIGINS
        
        if not allowed_origins:
            return HttpResponseForbidden("CORS not configured")
            
        origin = request.headers.get('Origin')
        if not origin or origin not in allowed_origins:
            return HttpResponseForbidden("Not allowed by CORS policy")