import os


# Repository directory.
ROOT = os.path.dirname(os.path.dirname(__file__))

# path bases things off of ROOT
def path(*a):
    return os.path.abspath(os.path.join(ROOT, *a))

# DjangoUeditor setting
UEDITOR_SETTINGS = {
    "images_upload":{
        'allow_type': 'jpg, png, gif',
        'path': 'img_upload_file/',
        'max_size': '3000kb',
        },
    }


ALLOWED_HOSTS = ["*"]
TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'zh-cn'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOGIN_URL = '/account/signin'

MEDIA_ROOT = path(ROOT, 'webroot', 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = path(ROOT, 'webroot', 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    path('stucampus', 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
   # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

ROOT_URLCONF = 'stucampus.urls'

WSGI_APPLICATION = 'stucampus.wsgi.application'

TEMPLATE_DIRS = (
    path('stucampus', 'templates'),
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'stucampus.middleware.PutHTTPMethodDataMiddleware'
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'raven.contrib.django.raven_compat',
    'DjangoUeditor',
    'stucampus.master',
    'stucampus.account',
    'stucampus.infor',
    'stucampus.organization',
    'stucampus.lecture',
    'stucampus.activity',
    'stucampus.articles',
    'stucampus.magazine',
    'stucampus.spider',
    'stucampus.szuspeech',
    'stucampus.minivideo',
    # 'stucampus.dreamer',
    'stucampus.FreeTimeCount',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '''[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s]
                         %(message)s''',
            'datefmt': "%d/%b/%Y %H:%M:%S"
         }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'stucampus_error.log',
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'stucampus': {
            'handlers': ['file'],
            'level': 'ERROR',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}



try:
    from stucampus.config.production import *
except ImportError:
    from stucampus.config.development import *
