

from . import BASE_DIR
import os
import dotenv
dotenv.load_dotenv()

FORMATTERS = (
    {
        "verbose": {
            "format": "{levelname} {asctime} {name} {threadName} {thread} {pathname} {lineno} {funcName} {process} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {asctime} {pathname} {lineno} {message}",
            "style": "{",
        },
    },
)

HANDLERS = {
    "console_handler": {
        "class": "logging.StreamHandler",
        "formatter": "simple",
        "level": "DEBUG"
    },
    "info_handler": {
        "class": "logging.handlers.RotatingFileHandler",
        "filename": os.path.join(BASE_DIR, 'logs/veerera_debug.log' ),
        "mode": "a",
        "encoding": "utf-8",
        "formatter": "verbose",
        "level": "INFO",
        "backupCount": 5,
        "maxBytes": 1024 * 1024 * 5,  # 5 MB
    },
    "error_handler": {
        "class": "logging.handlers.RotatingFileHandler",
        "filename": os.path.join(BASE_DIR, 'logs/veerera_debug.log' ),
        "mode": "a",
        "formatter": "verbose",
        "level": "WARNING",
        "backupCount": 5,
        "maxBytes": 1024 * 1024 * 5,  # 5 MB
    },
    'veereralog_handler': {
        "filename": os.path.join(BASE_DIR, 'logs/veerera_debug.log' ),
        "mode": "a",
        "maxBytes": 1024 * 1024 * 5,  # 5 MB            
        'class': 'logging.handlers.RotatingFileHandler',
        "formatter": "simple",
        "encoding": "utf-8",
        "level": "DEBUG",
        "backupCount": 5,
        
    }
}

LOGGERS = (
    {
        "django": {
            "handlers": ["console_handler", "info_handler"],
            "level": "INFO",
           
        },
        "django.request": {
            "handlers": ["error_handler"],
            'level': 'INFO',             
            "propagate": True,
        },
        "django.template": {
            "handlers": ["error_handler"],
            'level': 'INFO',             
            "propagate": False,
        },
        "django.server": {
            "handlers": ["error_handler"],
            'level': 'INFO',             
            "propagate": True,
        },
        'log': {
            'handlers': ['console_handler', 'veereralog_handler'],
            'level': 'INFO', 
            'level': 'DEBUG',   
            "propagate": True,    
            
        },
    },
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": FORMATTERS[0],
    "handlers": HANDLERS,
    "loggers": LOGGERS[0],
}