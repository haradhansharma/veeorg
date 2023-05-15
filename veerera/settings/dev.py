
# import os
from . import BASE_DIR, os


DEBUG = os.getenv("DEBUG", "True")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", ["*"])


CSRF_TRUSTED_ORIGINS = os.getenv(
    "CSRF_TRUSTED_ORIGINS", "https://127.0.0.1 https://localhost"
).split(" ")

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',  #new    
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware', #new    
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]

STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]



EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

from .settings_email import *
from .settings_local import *
from .settings_logs import *
# from .settings_security import *
from .settings_database import *
from .settings_summernote import *


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': 'F:/django/veereraorg/cache/',
        'TIMEOUT': 3600,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}
USER_AGENTS_CACHE = None


RECAPTCHA_PUBLIC_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'#this is develoment key to test
RECAPTCHA_PRIVATE_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'#this is develoment key to test
RECAPTCHA_DOMAIN = 'www.recaptcha.net'
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']







