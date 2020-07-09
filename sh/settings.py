"""
Django settings for sh project.

Generated by 'django-admin startproject' using Django 2.2.0

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import json
from django.core.exceptions import ImproperlyConfigured

with open("secrets.json") as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


SECRET_KEY = get_secret("SECRET_KEY")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',  # mincludes default permissions
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.postgres',  # added for search
    'django.contrib.staticfiles',
    # django.contrib.sites is required by allauth; may be disabled to get rid of SITES category in admin
    'django.contrib.sites',
    'django.contrib.gis',  # required for geo model
    'corsheaders',

    # Third-party
    'rest_framework',
    'rest_framework_gis',
    # 'rest_framework.authtoken', # is this needed for JWT?
    # 'rest_auth',
    # 'rest_auth.registration',
    'allauth',  # this is used in my session auth
    'allauth.account',
    'crispy_forms',
    'debug_toolbar',
    # 'django_url_filter',
    'django_filters',
    # 'rest_framework_filters',  # enables filtering across relationships
    'django_extensions',  # enables shell_plus jupyter notebook
    # 'djgeojson',  # may not be required for views
    # 'bootstrapform',
    # 'leaflet',  # django-leaflet

    # Local apps
    'api',
    'frontend',  # for testing session authentication with javascript fetch
    'maps',
    'obs',
    'resources',
    'search',
    'upload',
    'users',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # not needed in production
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',  # prob unneeded
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # prob unneeded
]

# CORS_ORIGIN_ALLOW_ALL = False
# CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = [
    'http://localhost:8080',
    'http://127.0.0.1:8080'
]
# CORS_ORIGIN_REGEX_WHITELIST = [
# 'http://localhost:8080',
# ]

ROOT_URLCONF = 'sh.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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


WSGI_APPLICATION = 'sh.wsgi.application'


DATABASES = get_secret("DATABASES")
# {
#     'default': {
#         'ENGINE': 'django.contrib.gis.db.backends.postgis',
#         'NAME': 'sh',
#         'USER': 'postgres',
#         'PASSWORD': '',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Pacific'

USE_I18N = False

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

# STATICFILES_DIRS = (
#     ("js", os.path.join(STATIC_ROOT, 'js')),
#     ("css", os.path.join(STATIC_ROOT, 'css')),
#     ("images", os.path.join(STATIC_ROOT, 'images')),
#  )

# STATIC_ROOT = '/static/'
# STATIC_URL = '/static/'
# STATICFILES_DIRS = os.path.join(BASE_DIR, "static")

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Enabled for django-debug-toolbar to work
# https://docs.djangoproject.com/en/2.2/ref/settings/#internal-ips
INTERNAL_IPS = ['127.0.0.1']

AUTH_USER_MODEL = 'users.CustomUser'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Django-Allauth Config see https://django-allauth.readthedocs.io/en/latest/overview.html
# note that url for allauth is /accounts but templates are in templates/account

# ACCOUNT_DEFAULT_HTTP_PROTOCOL =
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # or 'optional' or 'none'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_FORM_CLASS = 'users.forms.SignupForm'
# ACCOUNT_FORMS = {'signup': 'users.forms.SHSignupForm'}
# ACCOUNT_USER_DISPLAY = 'full_name'

LOGIN_REDIRECT_URL = '/api/projects/'
ACCOUNT_LOGIN_URL = '/accounts/login'
ACCOUNT_LOGIN_REDIRECT_URL = '/api/projects'
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login'
ACCOUNT_ADAPTER = 'users.adapter.SHAccountAdapter'


# this might be useful in production
# SESSION_COOKIE_DOMAIN=".soilhealth.app"

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

REST_FRAMEWORK = {
    # the default renderer is with HTML wrapper. Use this one to deliver JSON only.
    # 'DEFAULT_RENDERER_CLASSES': [
    #     'rest_framework.renderers.JSONRenderer'
    # ],
    # these require and enable login for API
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAuthenticated',
    # ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    # 'DEFAULT_FILTER_BACKENDS': ['rest_framework_filters.backends.RestFrameworkFilterBackend'],
    # 'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication', ),
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework.authentication.SessionAuthentication', ),
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # 'PAGE_SIZE': 100,
}

SITE_ID = 1
