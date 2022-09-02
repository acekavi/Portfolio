from pathlib import Path
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG')

ALLOWED_HOSTS = list(config('ALLOWED_HOSTS'))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'blog',
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

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': '5432',
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

#AWS Settings
AWS_ACCESS_KEY_ID           = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY       = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME     = config('AWS_STORAGE_BUCKET_NAME')
CLOUDFRONT_DOMAIN           = config('CLOUDFRONT_DOMAIN')

AWS_S3_CUSTOM_DOMAIN        = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_DEFAULT_ACL             = 'public-read'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl' : 'max-age=86400'
}

AWS_LOCATION = 'static'

STATICFILES_DIRS = [
    os.path.join( BASE_DIR, 'static'),
]
MEDIA_ROOT = os.path.join( BASE_DIR, 'media')

STATICFILES_STORAGE         = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL                  = f"https://{CLOUDFRONT_DOMAIN}/{AWS_LOCATION}/"

DEFAULT_FILE_STORAGE        = 'core.storages.MediaStore'
MEDIA_URL                   = f"https://{CLOUDFRONT_DOMAIN}/media/"


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
