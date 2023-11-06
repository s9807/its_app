"""
Django settings for its project.
"""

import os
from datetime import timedelta

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR,'templates/')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.db.backends.mysql',
    "drf_standardized_errors",
    'user_auth',
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt' ,
    'rest_framework_simplejwt.token_blacklist',

]


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=72),
    'REFRESH_TOKEN_LIFETIME': timedelta(hours=96),
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,             
    'ROTATE_REFRESH_TOKENS': True,
    'USER_ID_FIELD': 'uu_id',
    'BLACKLIST_AFTER_ROTATION': True,
    'ISSUER':'RAPIFuzz',
    'USER_ID_CLAIM':'id',
}

PASSWORD_HASHERS = ['user_auth.components.authbackend.CustomPasswordHasher',]

SWAGGER_SETTINGS = {
   'USE_SESSION_AUTH': False,
   'SECURITY_DEFINITIONS': {
      'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
      }
   }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'its.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
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


WSGI_APPLICATION = 'its.wsgi.application'

# Database
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_PORT = os.environ.get('DB_PORT')
LICENSE_KEY = os.environ.get('LICENSE_KEY')
RSA_KEY = os.environ.get('RSA_KEY', "<RSAKeyValue><Modulus>yJdndsoHiNEmQ+PUprbipZrOIHlHK1OVe3xCqgDYm744q4JKZ3S4Z3iauoyWDKjIAtpuwLyDSoxRoMTF6SFVf7byr4MIK2TiyEwKL1qSbFklCC0/y9IyUcushh3GKc2vgoZuh2Iw3OvqQP6x16ZuIM+nl/vet7B242HQ6BAQerGOab+03lVBIqgEADfGS2/uH/H6iBZ3E+plF5Oy2X+aC/MMIzXVIj80ZYnnNIJXWmPkoDoYbI0xTQ4gje2+bQ/6CNb9PthPJiyI7EKT99ubmW+1T3OyRH3yik6stnGDJTwDngVPgmEymBPAoQsCiusGWO6KA5y2hvX8qNkmmuPFCw==</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>")
PRODUCT_KEY = os.environ.get('PRODUCT_KEY',"13969")
AUTH = os.environ.get("AUTH","WyIxMTQ1ODgzIiwiRjhaT3M2bUJyeUVIV1Zsa2F6STVucFppQTg5L0pCZFM5SW5NTmtlaCJd")

DATABASES = {
   'default': {
      'ENGINE': 'dj_db_conn_pool.backends.mysql',
      'HOST': DB_HOST,
      'NAME': DB_NAME,
      'USER': DB_USER,
      'PASSWORD': DB_PASSWORD,
      'PORT': DB_PORT,
      'CONN_MAX_AGE': 1800,
      'POOL_OPTIONS' : {
            'POOL_SIZE': 20,
            'MAX_OVERFLOW': -1,
            'RECYCLE': 24 * 60 * 60,
        },
      'OPTIONS': {
            'charset': 'utf8mb4',  # This is the important line
            "init_command": "SET GLOBAL max_allowed_packet = 64*1024*1024",
        },
  }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

SWAGGER_SETTINGS = {
'JSON_EDITOR': True,
}

DRF_STANDARDIZED_ERRORS = {
                            "ENABLE_IN_DEBUG_FOR_UNHANDLED_EXCEPTIONS": True,
                            "EXCEPTION_HANDLER_CLASS": "exception_handling.exception_formatter.CustomExceptionHandler",
                            "EXCEPTION_FORMATTER_CLASS": "exception_handling.exception_formatter.CustomExceptionFormatter",
                            }


REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework_simplejwt.authentication.JWTAuthentication',],
    'DATETIME_FORMAT': "%d-%b-%Y %H:%M:%S",
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'USER_AUTHENTICATION_RULE': 'fuzzer.components.authbakend.custom_user_authentication_rule',
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler"
}


CORS_ALLOW_ALL_ORIGINS  = True
REQ_TIMEOUT = 300

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

#SMTP settings
EMAIL_BACKEND  = 'django.core.mail.backends.smtp.EmailBackend'

#Custom User Backend
AUTH_USER_MODEL = "user_auth.User"
AUTHENTICATION_BACKENDS = [
                            "user_auth.components.authbackend.CustomUserModelBackend",
                            "django.contrib.auth.backends.ModelBackend",
                           ]

# Creating a superuser  
DJANGO_SUPERUSER_USERNAME = os.environ.get('DJANGO_SUPERUSER_USERNAME')
DJANGO_SUPERUSER_EMAIL = os.environ.get('DJANGO_SUPERUSER_EMAIL')
DJANGO_SUPERUSER_PASSWORD = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
DJANGO_SUPERUSER_IS_ACTIVE = os.environ.get('DJANGO_SUPERUSER_IS_ACTIVE')
DJANGO_SUPERUSER_EMAIL_VERIFIED = os.environ.get('DJANGO_SUPERUSER_EMAIL_VERIFIED')
DJANGO_SUPERUSER_NAME = "admin"
DJANGO_SUPERUSER_ROLE = "ROLE_ADMIN"


DATA_UPLOAD_MAX_MEMORY_SIZE = 1024*1024*1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 200*1024*1024*1024