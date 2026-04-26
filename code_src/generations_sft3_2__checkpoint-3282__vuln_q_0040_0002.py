from django.conf import settings
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext as _

@require_http_methods(["GET", "POST", "OPTIONS"])
def cors_allowed(request):
    if not settings.DEBUG and not request.headers.get('Origin') in settings.ALLOWED_CORS_ORIGINS:
        return HttpResponseForbidden(_("CORS not allowed"))
    return None