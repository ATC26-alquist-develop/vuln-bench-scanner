INSTALLED_APPS = [
    ...
    'corsheaders',
    ...
]

# ===== cell separator =====

MIDDLEWARE = [
    ...
    'corsheaders.middleware.CorsMiddleware',
    ...
]

# ===== cell separator =====

CORS_ORIGIN_ALLOW_ALL = True

# ===== cell separator =====

CORS_ORIGIN_WHITELIST = [
    'http://example.com',
    'https://example.com',
]

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]