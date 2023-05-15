import os
from pathlib import Path
from django.core.management.utils import get_random_secret_key


BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv("SECRET_KEY", get_random_secret_key())
if not SECRET_KEY:
    raise ValueError("No DJANGO_SECRET_KEY set for production!")

SITE_ID=1

INSTALLED_APPS = [
    'django.contrib.admin',
    'django_summernote',
    'django_user_agents',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'core',
    'django.contrib.sitemaps',
    'captcha',       
    
]


ROOT_URLCONF = 'veerera.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processor.core_con'
            ],
        },
    },
]

WSGI_APPLICATION = 'veerera.wsgi.application'


STATIC_URL = '/static/'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

import dotenv
dotenv.load_dotenv()

ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')

if ENVIRONMENT == 'production':
    from .pro import *
else:
    from .dev import *
    
    
