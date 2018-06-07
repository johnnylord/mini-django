import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

URL_ROOT = "project.urls"

MIDDLEWARE = [
    'middleware.TestModule.TestModule',
    'middleware.security.SecurityMiddleware',
]

INSTALLED_APPS = [
    'home',
]

ALLOWED_HOSTS = [
]

TEMPLATES = [
    {
        'DIRS' : [os.path.join('template')],
    },
]

SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = False
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
SECURE_CONTENT_TYPE_NOSNIFF = False


STATIC_URL = '/static/'