"""
Django settings for sneaky project.

Generated by 'django-admin startproject' using Django 2.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3!gvz!kq2c@-fp29n7#w%(_eb$a!k(ui2yeb&fh%jt9326lj+h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECRET_KEY = os.environ.get('SECRET_KEY', '3!gvz!kq2c@-fp29n7#w%(_eb$a!k(ui2yeb&fh%jt9326lj+h')

# DEBUG can be True/False or 1/0
# DEBUG = int(os.environ.get('DEBUG', default=1))

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'addresses',
    'billing',
    'carts',
    'compressor',
    'orders',
    'products',
    'search',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sneaky.urls'

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

WSGI_APPLICATION = 'sneaky.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# """
# Local development database settings.
# """
# DATABASES = {
#     'default': {
#         'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3'),
#         'NAME': os.environ.get('DB_DATABASE_NAME', os.path.join(BASE_DIR, 'db.sqlite3')),
#         'USER': os.environ.get('DB_USERNAME', 'user'),
#         'PASSWORD': os.environ.get('DB_PASSWORD', 'password'),
#         'HOST': os.environ.get('DB_HOST', 'localhost'),
#         'PORT': os.environ.get('DB_PORT', '5432'),
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    # 'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
PROTECTED_ROOT = os.path.join(BASE_DIR, 'protected_media')

AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = '/login/'
LOGIN_URL_REDIRECT = '/'
LOGOUT_URL = '/logout/'
LOGOUT_REDIRECT_URL = '/login/'
ROOT_URLCONF = 'sneaky.urls'

FORCE_SESSION_TO_ONE = False
FORCE_INACTIVE_USER_END_SESSION = False

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'prj.ecom.pydj@gmail.com'
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "Python337Django22")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Python eCommerce <prj.ecom.pydj@gmail.com>'
BASE_URL = '127.0.0.1:8000'

# MAILCHIMP_API_KEY = os.environ["MAILCHIMP_API_KEY"] # Use this when running server with heroku
MAILCHIMP_API_KEY = os.environ.get("MAILCHIMP_API_KEY", "DEFAULT")
MAILCHIMP_DATA_CENTER = "us3"
MAILCHIMP_EMAIL_LIST_ID = os.environ.get("MAILCHIMP_EMAIL_LIST_ID")

STRIPE_SEC_KEY = os.environ.get("STRIPE_SEC_KEY", "sk_test_L2UkxaY9kJLqL3veVS0fCuLv00uVo6w8I4")
STRIPE_PUB_KEY = os.environ.get("STRIPE_PUB_KEY", "pk_test_8hljcboVHoSIRIswWFCEwlIY00Xdsw19Ue")

MANAGERS = (
    ('Admin', 'prj.ecom.pydj@gmail.com'),
)
ADMINS = MANAGERS
