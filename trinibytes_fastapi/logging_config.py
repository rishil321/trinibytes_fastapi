from pathlib import Path
import sys


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default_formatter': {
            'format': '%(asctime)s-%(module)s-%(funcName)s-%(levelname)s:%(message)s'
        },
    },
    'handlers': {
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
            'level': 'DEBUG',
            'stream': 'ext://sys.stdout',
        },
        'info_rotating_file_handler': {
            'level': 'INFO',
            'formatter': 'default_formatter',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'trinibytes_fastapi.log',
            'mode': 'a',
            'maxBytes': 1048576,
            'backupCount': 10
        },
    },
    'loggers': {
        '': {
            'handlers': ['stream_handler', 'info_rotating_file_handler'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}
