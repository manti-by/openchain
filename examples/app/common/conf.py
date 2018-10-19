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
            }
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True
            }
        }
    },
    'pool_server': {
        'ip': 'openchain-pool',
        'port': 8000
    },
    'generator_server': {
        'ip': 'openchain-generator',
        'port': 8000
    },
    'generator_last_hash': '/var/lib/openchain/generator.hash',
    'builder_server': {
        'ip': 'openchain-builder',
        'port': 8000
    },
    'builder_tree_path': '/var/lib/openchain/tree.json'
}
