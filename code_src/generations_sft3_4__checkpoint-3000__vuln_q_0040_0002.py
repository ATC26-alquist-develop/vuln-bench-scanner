from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

@method_decorator(ensure_csrf_cookie, name='get')
@require_http_methods(["OPTIONS", "GET", "POST", "PUT", "DELETE", "PATCH"])
def my_view(request):
    # Validate CORS settings
    if not hasattr(settings, 'CORS_ORIGIN_WHITELIST'):
        raise ValidationError("CORS configuration is not properly set up")
    
    # Check if request origin is in whitelist
    origin = request.headers.get('Origin')
    if not origin or origin not in settings.CORS_ORIGIN_WHITELIST:
        return HttpResponse(status=403)
    
    return HttpResponse(status=200)