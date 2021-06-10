import datetime
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!g41e+44yvk!0l$em#54!euap&x5r6jl2-h0^vz8a27$-o(xwy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', ]

# Application definition
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'haystack',
    'rest_framework',
    'drf_yasg',
    'django_filters',
    'common',
    'book',
    'borrow',
    'comment',
    'search',
    'recommendation',
    'library'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'library.middleware.response.RemoveRealm',
    'library.middleware.knn_init.InitKNNModel',
    'library.middleware.exception.ExceptionBoxMiddleware',
    'library.middleware.log.RequestLogMiddleware',
]

ROOT_URLCONF = 'library.urls'
WSGI_APPLICATION = 'library.wsgi.application'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'EXCEPTION_HANDLER': 'library.exceptions.library_global_exception_handler',
    'PAGE_SIZE': 10
}

# Config Haystack's search engine backend as whoosh
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'index'),
    },
}

# Automatic update index
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
# Tell haystack to use customer highlighter
# HAYSTACK_CUSTOM_HIGHLIGHTER = 'search.utils.Highlighter'

# Mysql database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 数据库引擎
        'NAME': 'library',  # 数据库名
        'USER': 'root',  # 账号
        'PASSWORD': '123456',  # 密码
        'HOST': '127.0.0.1',  # HOST
        'POST': 3306,  # 端口
    }
}
# set upload path
MEDIA_ROOT = os.path.join(BASE_DIR, 'upload')
MEDIA_URL = "/upload/"
UPLOAD_URL = 'upload'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'upload'),
)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# User
AUTH_USER_MODEL = 'common.User'

# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Bangkok'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

LOGS_DIR = os.path.join(BASE_DIR, 'logs')

if not os.path.exists(LOGS_DIR):
    os.mkdir(LOGS_DIR)

LOGGING = {
    'version': 1,
    # whether disable default loggers
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s[%(levelname)s][%(filename)s: %(module)s: %(funcName)s: %(lineno)d]: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },

    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': sys.stdout,
        },
        # customer handlers，output to file
        'restful_api': {
            'level': 'DEBUG',
            # time slide split
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOGS_DIR, 'web-log.log'),
            'formatter': 'standard',
            # split file in midnight
            'when': 'MIDNIGHT',
            # save file for 30 days
            'backupCount': 30,
        },
    },
    'loggers': {
        'default': {
            'handlers': ['restful_api', 'default'],
            'level': 'INFO',
            'propagate': False
        },
        'web.log': {
            'handlers': ['restful_api', 'default'],
            'level': 'INFO',
            # tell django need not log this information again
            'propagate': False
        },
    }
}
