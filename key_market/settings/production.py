from key_market.settings.common import *  # NOQA

DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',
)

MIDDLEWARE_CLASSES += (
    'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
)

RAVEN_CONFIG = {
    'dsn': '',  # NOQA
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': ('raven.contrib.django.raven_compat.handlers.'
                      'SentryHandler'),
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['sentry'],
            'propagate': False,
        },
        'raven': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'key_market': {
            'level': 'ERROR',
            'handlers': ['sentry'],
            'propagate': False,
        },
    },
}
