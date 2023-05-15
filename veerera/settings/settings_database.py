import os, dotenv

if os.getenv('ENVIRONMENT') == 'production':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASS'),
            'HOST':'localhost',
            'PORT': '3306',
            'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            }
        }
    }
else:   
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'veereraorg',
            'USER': 'root',
            'PASSWORD': '',
            'HOST':'localhost',
            'PORT': '3306',
            'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            }
        }
    }
        



