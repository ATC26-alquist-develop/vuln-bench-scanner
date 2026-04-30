from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import secure_etag

def cors_allow_all(view_func):
    """
    Decorator to allow CORS from all origins with secure headers.
    """
    @csrf_exempt
    @secure_etag
    def _wrapped_view(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response['Access-Control-Allow-Credentials'] = 'true'
        return response
    return _wrapped_view