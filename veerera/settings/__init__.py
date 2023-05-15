import os
from pathlib import Path
from django.core.management.utils import get_random_secret_key
import ast
import dotenv
dotenv.load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent.parent


DEBUG = ast.literal_eval(os.getenv('DEBUG', 'False'))

SECRET_KEY = os.getenv("SECRET_KEY", get_random_secret_key())
if not SECRET_KEY:
    raise ValueError("No DJANGO_SECRET_KEY set for production!")

if DEBUG:
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", ["*"])
    CSRF_TRUSTED_ORIGINS = os.getenv(
        "CSRF_TRUSTED_ORIGINS", "https://127.0.0.1 https://localhost"
    ).split(" ")
else:
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "veerera.org www.veerera.org").split(" ")
    CSRF_TRUSTED_ORIGINS = os.getenv(
        "CSRF_TRUSTED_ORIGINS", "https://veerera.org"
    ).split(" ")


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

if DEBUG:
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
else:
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

from .settings_database import *
from .settings_local import *


STATIC_URL = '/static/'

if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



if DEBUG:
    from .dev import *
else:
    from .pro import *
    

    
    
