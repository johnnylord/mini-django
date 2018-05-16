MIDDLEWARE = [
    'middleware.TestModule.TestModule',
    'middleware.security.SecurityMiddleware',
]

ALLOWED_HOSTS = []

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = False
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
SECURE_CONTENT_TYPE_NOSNIFF = False