from django.conf import settings
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext as _
from django.utils.html import escape

class CORSMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Check if CORS is explicitly enabled in settings
        if not getattr(settings, 'CORS_REPLACE_HTTPS_REFERER', False):
            return None
            
        # Validate and sanitize the referer
        referer = request.META.get('HTTP_X_FORWARDED_FOR', 
                                  request.META.get('HTTP_CLIENT_IP', '')).strip()
        if not referer:
            return HttpResponseForbidden(_("Invalid or missing referer"))
            
        # Sanitize the referer to prevent XSS
        referer = escape(referer)
        
        # Check if the referer matches any allowed origin
        allowed_origins = settings.CORS_ALLOWED_ORIGINS
        
        if not allowed_origins:
            raise ImproperlyConfigured(_("CORS_ALLOWED_ORIGINS must be set in settings"))
            
        if not isinstance(allowed_origins, (list, tuple)):
            raise ImproperlyConfigured(_("CORS_ALLOWED_ORIGINS must be a list or tuple"))
            
        # Check if the referer matches any allowed origin
        if not any(referer.startswith(origin) for origin in allowed_origins):
            return HttpResponseForbidden(_("Access Denied"))