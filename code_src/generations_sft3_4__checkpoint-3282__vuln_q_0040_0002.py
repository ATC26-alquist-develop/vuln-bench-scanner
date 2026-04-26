from django.conf import settings
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import MiddlewareNotUsed
from django.utils.translation import gettext as _
from django.utils.html import escape
from django.core.cache import cache
import time

class CORSMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Only enable if CORS is explicitly configured
        if not getattr(settings, 'CORS_REPLACE_HTTPS_REFERER', False):
            raise MiddlewareNotUsed(_("CORS middleware must be explicitly enabled"))

    def __call__(self, request):
        # Check if the request should be allowed based on cache
        if not self._should_allow(request):
            return HttpResponseForbidden(_("CORS not allowed"))

        response = self.get_response(request)
        return response

    def _should_allow(self, request):
        # Check if the request is in the cache
        cache_key = f"cors:{request.get_host()}"
        cached_result = cache.get(cache_key)
        
        if cached_result is not None:
            return cached_result

        # Check if the request should be allowed
        origin = request.headers.get('Origin', '')
        if not origin:
            return False

        # Whitelist of allowed origins
        allowed_origins = getattr(settings, 'CORS_ALLOWED_ORIGINS', [])
        
        # Check if the origin is in the whitelist
        if allowed_origins:
            return origin in allowed_origins
            
        # Check if the request is from the same site
        is_same_site = request.headers.get('X-Forwarded-Scheme') == 'https' and \
                       request.get_host().startswith('localhost') and \
                       request.get_host().replace('localhost', '127.0.0.1') in allowed_origins

        # Cache the result for 5 minutes
        cache.set(cache_key, is_same_site, 300)
        return is_same_site

    def process_response(self, request, response):
        # Add CORS headers
        response['Access-Control-Allow-Origin'] = self._get_cors_origin(request)
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = self._get_cors_headers(request)
        return response

    def _get_cors_origin(self, request):
        origin = request.headers.get('Origin', '')
        return escape(origin) if origin else ''

    def _get_cors_headers(self, request):
        headers = request.headers.get('Access-Control-Request-Headers', '')
        return escape(headers) if headers else ''