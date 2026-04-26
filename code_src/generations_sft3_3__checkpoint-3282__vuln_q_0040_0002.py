from django.conf import settings
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied

@method_decorator(ensure_csrf_cookie, name='get')
@require_http_methods(["OPTIONS", "GET", "POST", "PUT", "DELETE", "PATCH"])
def my_view(request):
    # Check if CSRF token is valid
    if not request.COOKIES.get(settings.CSRF_COOKIE_NAME):
        raise PermissionDenied("CSRF token is missing")
    
    # Check if request has valid CSRF token
    if not request.csrf_valid:
        raise PermissionDenied("CSRF token is invalid")
    
    # Your view logic here
    return HttpResponseForbidden("CORS is properly configured")