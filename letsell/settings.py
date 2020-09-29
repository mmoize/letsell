"""
Django settings for letsell project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from decouple import config
from dj_database_url import parse as dburl
import dj_database_url
import psycopg2
import django_heroku




# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)


ALLOWED_HOSTS = [
    'sellet.herokuapp.com',
    '127.0.0.1'
    
]

DJANGO_REST_PASSWORDRESET_TOKEN_CONFIG = {
    "CLASS": "django_rest_passwordreset.tokens.RandomStringTokenGenerator",
    "OPTIONS": {
        "min_length": 4,
        "max_length": 6
    }
}



AUTH_USER_MODEL = 'authentication.User'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.gis',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',
    'authentication.apps.AuthenticationConfig',
    'rest_framework',
    'accounts.apps.AccountsConfig',
    'corsheaders',
    'django_login_history',
    'storages',
    'discover.apps.DiscoverConfig',
    'django_extensions',
    'djgeojson',
    'taggit_serializer',
    'taggit',
    'chat.apps.ChatConfig',
    'push_notifications',
    'fcm_django',
    'rest_framework_filters',
    'django_rest_passwordreset',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'letsell.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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


WSGI_APPLICATION = 'letsell.wsgi.application'



# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
#default_dburl = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')

# default_dburl = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')

# DATABASES = {'default': config('DATABASE_URL', default=default_dburl, cast=dburl), }

import os



if os.name == 'nt':
    GDAL_DATA =' C:\OSGeo4W64\share\gdal'
    OSGEO4W_ROOT = 'C:\OSGeo4W64'
    PROJ_LIB = 'C:\OSGeo4W64\share\proj'
    GDAL_LIBRARY_PATH = r'C:\OSGeo4W64\bin\gdal300.dll'

if 'DYNO' in os.environ:
    GDAL_LIBRARY_PATH = os.environ.get('GDAL_LIBRARY_PATH')
    GEOS_LIBRARY_PATH = os.environ.get('GEOS_LIBRARY_PATH')
    
    


DATABASE_URL = os.environ['DATABASE_URL']


conn = psycopg2.connect(DATABASE_URL, sslmode='require')
#DATABASES['default']= dj_database_url.config(conn_max_age=600, ssl_require=True)
#DATABASES = { 'default': dj_database_url.config(conn_max_age=500, ssl_require=True) }
#DATABASES = { 'default': dj_database_url.config() }

db_from_env = dj_database_url.config(conn_max_age=500)



DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'dbl0883bjcaf70',
        'USER': 'qwtqyrfuqzljtd',
        'PASSWORD': 'cc2979db2f9a56e099a71022c5c8dfb21b65da99283faf73cfb79824b8e638ea',
        'HOST': 'ec2-52-86-116-94.compute-1.amazonaws.com',
        'PORT': '5432'
    }
}

DATABASES['default'].update(db_from_env)
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'



AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID') 
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_LOCATION = 'static'


AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'core.exceptions.core_exception_handler',
    'NON_FIELD_ERRORS_KEY': 'error',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'authentication.backends.JWTAuthentication',
        
    ),
    'DEFAULT_PERMISSION_CLASSES': (
      'authentication.backends.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_filters.backends.RestFrameworkFilterBackend',
    ),
    
}


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_ROOT =  os.path.join(BASE_DIR, 'static/staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')
MEDIA_URL = '/media/'


CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_WHITELIST = [
    'http://localhost:8100',
    'https://localhost:8100',
    'https://101.114.183.81',
    'https://101.114.183.81:8100',
    'https://101.114.183.81',
    'http://101.114.183.81',
    'http://localhost',
    'https://localhost',
    'https://fleek-market.web.app'

]

PUSH_NOTIFICATIONS_SETTINGS = {
        "FCM_API_KEY": "AAAAGPLtpSQ:APA91bFEKAmoNBK7KYE-gbJmxJsDl259v7sOIbe-rAbTf_1J38BAwaxQaU1-RUx26bloQeOMZ8KFBszST-kVypY5fhFTH3s6F8zv8nptORNmMBv0Qa9SM5e7n3RMakeUcPAaWkNKJkct",
        

        # "GCM_API_KEY": "[your api key]",
        # "APNS_CERTIFICATE": "/path/to/your/certificate.pem",
        # "APNS_TOPIC": "com.example.push_test",
        # "WNS_PACKAGE_SECURITY_ID": "[your package security id, e.g: 'ms-app://e-3-4-6234...']",
        # "WNS_SECRET_KEY": "[your app secret key, e.g.: 'KDiejnLKDUWodsjmewuSZkk']",
        # "WP_PRIVATE_KEY": "/path/to/your/private.pem",
        # "WP_CLAIMS": {'sub': "mailto: development@example.com"}
}


FCM_DJANGO_SETTINGS = {
        # "APP_VERBOSE_NAME": "[string for AppConfig's verbose_name]",
         # default: _('FCM Django')
        "FCM_SERVER_KEY": "AAAAGPLtpSQ:APA91bFEKAmoNBK7KYE-gbJmxJsDl259v7sOIbe-rAbTf_1J38BAwaxQaU1-RUx26bloQeOMZ8KFBszST-kVypY5fhFTH3s6F8zv8nptORNmMBv0Qa9SM5e7n3RMakeUcPAaWkNKJkct",
         # true if you want to have only one active device per registered user at a time
         # default: False
        "ONE_DEVICE_PER_USER": False,
         # devices to which notifications cannot be sent,
         # are deleted upon receiving error response from FCM
         # default: False
        "DELETE_INACTIVE_DEVICES": False,
}

DJANGORESIZED_DEFAULT_SIZE = [500, 500]
DJANGORESIZED_DEFAULT_QUALITY = 100
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'JPEG'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'JPEG': ".jpg"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True

#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'



EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'mosesmvp@gmail.com'
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD') 


STREAM_API_KEY = 'uyctzvydndw6'
STREAM_API_SECRET = '83b3uxn35w4s8cwr3e3zgucwv6jh5qzrkv4zk8t49yh4wxzvf9jzmkaqvgh646ke'


