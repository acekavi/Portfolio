from decouple import config
from .base import *

SECRET_KEY = config('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = []

STATICFILES_DIRS = [ BASE_DIR / 'static', ]

MEDIA_ROOT = BASE_DIR / 'media'

STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
STATIC_URL = 'staticfiles/'

CKEDITOR_UPLOAD_PATH = 'uploads/'