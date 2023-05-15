
# from . import BASE_DIR, os


DEBUG = os.getenv("DEBUG", "False")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "veerera.org www.veerera.org").split(" ")

CSRF_TRUSTED_ORIGINS = os.getenv(
    "CSRF_TRUSTED_ORIGINS", "https://veerera.org"
).split(" ")


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',  #new    
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware', #new    
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]

CACHE_MIDDLEWARE_ALIAS = 'default'




STATIC_ROOT = os.path.join(BASE_DIR, 'static')



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

from .settings_email import *
from .settings_local import *
from .settings_logs import *
from .settings_security import *
from .settings_database import *
from .settings_summernote import *





CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.getenv('CACHE_LOCATION'),
        'TIMEOUT': 3600,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}
USER_AGENTS_CACHE = 'default'


RECAPTCHA_PUBLIC_KEY = os.getenv("RECAPTCHA_PUBLIC_KEY")
RECAPTCHA_PRIVATE_KEY = os.getenv("RECAPTCHA_PRIVATE_KEY")
# RECAPTCHA_DOMAIN = 'www.recaptcha.net'
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']