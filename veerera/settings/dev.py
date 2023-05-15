

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
from .settings_email import *
from .settings_logs import *
# from .settings_security import *
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







