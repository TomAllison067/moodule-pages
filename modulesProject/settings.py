import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType

"""
Django settings for modulesProject project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/

# Before deployment:
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/
"""

import os
from pathlib import Path

import environ  # Let's use django-environ to handle our environment variables
# Build paths inside the project like this: BASE_DIR / 'subdir'.
from django.urls import reverse

BASE_DIR = Path(__file__).resolve().parent.parent

"""Importing environment variables with django-environ
    https://django-environ.readthedocs.io/en/latest/#"""
env = environ.Env(
    # Debug false by default (unless specified in .env)
    DEBUG=(bool, False)
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': env.db(),
    'example': env.db('EXAMPLE_DB_URL', default="sqlite:////tmp/my-tmp-sqlite.db")
}

"""django-environ finished"""
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.8000',
    '127.0.0.1',
]

# Application definition

INSTALLED_APPS = [
    'modulesApplication.apps.ModulesApplicationConfig',  # install our app so it runs in django!
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
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

ROOT_URLCONF = 'modulesProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'modulesProject.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# https://docs.djangoproject.com/en/3.1/ref/contrib/sites/#enabling-the-sites-framework
# Use the sites framework for Django authentication. Need to look at this later.
SITE_ID = 1

SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

# MEDIA_ROOT = os.path.join(BASE_DIR, 'resources')
# MEDIA_URL = '/resources/'

"""DJANGO AUTHENTICATION SETTINGS"""
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # Django's default auth backend
    # 'django_auth_ldap.backend.LDAPBackend',  # LDAP Backend
    'modulesApplication.auth.custom_ldap_backend.CustomLDAPBackend'
)

LOGIN_REDIRECT_URL = '/'  # Upon login, redirect to index
LOGOUT_REDIRECT_URL = '/'  # Upon signout, redirect to index

AUTH_LDAP_SERVER_URI = "ldaps://directory.rhul.ac.uk:636"

AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail"
}

AUTH_LDAP_BASE_DN = "OU=MIIS Managed,DC=cc,DC=rhul,DC=local"
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    AUTH_LDAP_BASE_DN, ldap.SCOPE_SUBTREE, '(sAMAccountName=%(user)s)'
)

AUTH_LDAP_GLOBAL_OPTIONS = {
    ldap.OPT_X_TLS_REQUIRE_CERT: ldap.OPT_X_TLS_NEVER
}

AUTH_LDAP_CACHE_TIMEOUT = 3600

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {"django_auth_ldap": {"level": "DEBUG", "handlers": ["console"]}},
}
