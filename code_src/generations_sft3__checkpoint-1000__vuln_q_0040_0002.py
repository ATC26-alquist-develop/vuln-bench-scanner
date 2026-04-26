from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class CORSMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Only allow requests from whitelisted domains
        allowed_origins = settings.ALLOWED_CORS_ORIGINS
        
        if not allowed_origins:
            return None
            
        origin = request.headers.get('Origin')
        
        if not origin:
            return None
            
        if origin not in allowed_origins:
            return HttpResponse('Access Denied', status=403)
            
        return None