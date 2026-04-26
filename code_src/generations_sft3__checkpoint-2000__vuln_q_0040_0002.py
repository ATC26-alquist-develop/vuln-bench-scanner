from django.conf import settings
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
@require_http_methods(["GET", "POST", "OPTIONS"])
def my_view(request):
    # Your view logic here
    return HttpResponseForbidden("CORS not allowed")