import os
import ast
DEBUG = ast.literal_eval(os.getenv('DEBUG', 'False'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'veereraorg' if DEBUG else 'veerera_main',
        'USER': 'root' if DEBUG else 'veerera_haradha',
        'PASSWORD': '' if DEBUG else 'Y3aZPODkHrvJ',
        'HOST':'localhost',
        'PORT': '3306',
        'OPTIONS': {
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

    
    


