import os
from dotenv import load_dotenv
from . import BASE_DIR
load_dotenv(os.path.join(BASE_DIR, '.env.veerera'))
DEFAULT_FROM_EMAIL = str(os.getenv('DEFAULT_FROM_EMAIL'))
EMAIL_HOST = str(os.getenv('EMAIL_HOST'))
EMAIL_PORT= str(os.getenv('EMAIL_PORT'))
EMAIL_HOST_USER=str(os.getenv('EMAIL_HOST_USER'))
EMAIL_HOST_PASSWORD=str(os.getenv('EMAIL_HOST_PASSWORD'))
EMAIL_USE_TLS=False
EMAIL_USE_SSL=True
# import ast
# ADMINS = ast.literal_eval(os.getenv('ADMINS'))
