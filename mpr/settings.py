import os
from os import environ as env
from django.conf import global_settings
import dj_database_url

DEBUG = env.get('DJANGO_DEBUG', 'true') == 'true'
PROJECT_ROOT = os.path.dirname(os.path.realpath(__name__))

ADMINS = (
    ('Adi Eyal', 'adi@openup.org.za'),
)

MANAGERS = ADMINS

DATABASES = {
    # load from DATABASE_URL env var, or default to this
    'default': dj_database_url.config(default='sqlite:///mpr.db')
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    'code4sa-mpr.herokuapp.com',
    'mpr.code4sa.org',
    'mpr.openup.org.za',
    'localhost',
    '127.0.0.1',
    'medicineprices.org.za'
]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Africa/Johannesburg'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: '/var/www/example.com/media/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: 'http://example.com/media/', 'http://media.example.com/'
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' 'static/' subdirectories and in STATICFILES_DIRS.
# Example: '/var/www/example.com/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# URL prefix for static files.
# Example: 'http://example.com/static/', 'http://static.example.com/'
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like '/home/html/static' or 'C:/www/django/static'.
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'mpr', 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

if DEBUG:
    # Make this unique, and don't share it with anybody.
    SECRET_KEY = 'ub7dk%m=d*k=aip1rl)z&v8sj&fg2msc&=km0z3u#5ct9+_43w'
else:
    SECRET_KEY = env.get('DJANGO_SECRET_KEY')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        }
    },
]

MIDDLEWARE = (
    'mpr.middleware.CORSMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


ROOT_URLCONF = 'mpr.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'mpr.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'pipeline',
    'mpr',
#    'behave_django',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

PIPELINE = {
    'ENABLED': env.get("DJANGO_PIPELINE_ENABLED", True),
    'JAVASCRIPT': {
        'mprbase' : {
            'source_filenames': (
              'js/jquery-1.10.2.js',
              'js/bootstrap.js',
              'js/jquery.ba-hashchange.js',
              'js/knockout.js',
              'js/survey.ko.js',
              'js/medloader.js',
            ),
            'output_filename': 'js/mprbase.js',
        },
    },
    'STYLESHEETS' : {
        'mpr' : {
            'source_filenames': (
              'css/bootstrap.css',
              #'css/bootstrap-theme.css',
              'css/custom.css',
              #'css/survey.css',
            ),
            'output_filename': 'css/mpr.css',
        }
    },
    'CSS_COMPRESSOR' : 'pipeline.compressors.yuglify.YuglifyCompressor',
    'JS_COMPRESSOR' : 'pipeline.compressors.yuglify.YuglifyCompressor',
    'DISABLE_WRAPPER' : True
}

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt' : '%d/%b/%Y %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'mpr': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'ERROR',
            'propagate': True,
        },
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'TIMEOUT' : 60*60*24*7
    }
}

SEGMENT_IO_KEY = env.get('SEGMENT_IO_KEY')
SESSION = 'django.contrib.sessions.backends.signed_cookies'

PRICE_PARAMETERS = {
    "VAT" : 1.15,
    "prices" : [
        (113.72, 0.46, 15.95),
        (303.32, 0.33, 29.07),
        (1061.62, 0.15, 82.77),
        (float('inf'), 0.05, 190.68),
    ]
}

from . import loganalytics
if DEBUG:
    ANALYTICS = loganalytics.test_log_analytics
else:
    ANALYTICS = loganalytics.log_analytics
