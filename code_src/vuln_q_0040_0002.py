from django_cors import CorsMiddleware
from django.conf import settings

class SecureCorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_origins = settings.CORS_ALLOWED_ORIGINS  # Set this in settings.py

    def __call__(self, request):
        response = self.get_response(request)
        response['Access-Control-Allow-Origin'] = self.allowed_origins
        response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

# ===== cell separator =====

CORS_ALLOWED_ORIGINS = [
    'https://trusted-origin.com',
    'https://another-trusted-origin.com',
]