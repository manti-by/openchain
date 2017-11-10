settings = {
    'logging': {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(message)s',
                'datefmt': '%H:%M:%S'
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': True
            },
        }
    },
    'pool_server': {
        'ip': '192.168.99.100',
        'port': 8000
    },
    'logger_server': {
        'ip': '192.168.99.101',
        'port': 8000
    }
}
