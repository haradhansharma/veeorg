
import os
import dotenv
dotenv.load_dotenv()

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
from .settings_email import *
from .settings_logs import *
from .settings_security import *
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
CACHE_MIDDLEWARE_ALIAS = 'default'
USER_AGENTS_CACHE = 'default'


RECAPTCHA_PUBLIC_KEY = str(os.getenv("RECAPTCHA_PUBLIC_KEY"))
RECAPTCHA_PRIVATE_KEY = str(os.getenv("RECAPTCHA_PRIVATE_KEY"))
# RECAPTCHA_DOMAIN = 'www.recaptcha.net'
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']