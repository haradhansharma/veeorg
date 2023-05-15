
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30
X_FRAME_OPTIONS = 'SAMEORIGIN'
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# FILE_UPLOAD_DIRECTORY_PERMISSIONS =0o777
# FILE_UPLOAD_PERMISSIONS = 0o644

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True
SECURE_SSL_HOST = True

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SAMESITE = 'None'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
