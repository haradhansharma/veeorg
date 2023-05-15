from . import os, dotenv
import dj_database_url



if os.getenv('ENVIRONMENT') == 'production':
    dotenv.load_dotenv('.env.production')
else:   
    dotenv.load_dotenv('.env.development')
    


DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

