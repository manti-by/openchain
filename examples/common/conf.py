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
                'level': 'DEBUG',
                'propagate': True
            },
        }
    },
    'pool_server': {
        'ip': '10.5.0.2',
        'port': 8000
    },
    'log_server': {
        'ip': '10.5.0.3',
        'port': 8000
    },
    'miner_server': {
        'ip': '10.5.0.4',
        'port': 8000
    }
}
