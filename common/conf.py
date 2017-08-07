settings = {
    'logging': {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'simple': {
                'format': '%(asctime)s %(message)s',
                'datefmt': '%H:%M:%S'
            },
            'standard': {
                'format': '%(asctime)s [%(levelname)-8s] %(name)-15s %(lineno)4d - %(message)s',
                'datefmt': '%H:%M:%S'
            }
        },
        'handlers': {
            'print': {
                'level':'INFO',
                'class':'logging.StreamHandler',
                'formatter': 'simple',
            },
            'console': {
                'level':'WARNING',
                'class':'logging.StreamHandler',
                'formatter': 'standard',
            },
        },
        'loggers': {
            '': {
                'handlers': ['print', 'console'],
                'level': 'INFO',
                'propagate': True
            },
        }
    }
}