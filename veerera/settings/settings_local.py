
import os
import dotenv
dotenv.load_dotenv()
LANGUAGE_CODE = 'en'
TIME_ZONE = 'Asia/Dhaka'
USE_I18N = True
USE_L10N = True
USE_TZ = True

IP_LOCATION_API = os.getenv('IP_LOCATION_API')

