from base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG
PIPELINE = True

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
