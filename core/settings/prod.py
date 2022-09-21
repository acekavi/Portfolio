from decouple import config
from .base import *

SECRET_KEY = config('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['.acekavi.me']

### AWS Settings
AWS_ACCESS_KEY_ID           = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY       = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME     = config('AWS_STORAGE_BUCKET_NAME')
CLOUDFRONT_DOMAIN           = config('CLOUDFRONT_DOMAIN')

AWS_S3_CUSTOM_DOMAIN        = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_DEFAULT_ACL             = 'public-read'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl' : 'max-age=86400'
}
AWS_QUERYSTRING_AUTH = False
AWS_LOCATION = 'static'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
MEDIA_ROOT = [
    BASE_DIR / 'media',
]

STATICFILES_STORAGE         = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL                  = f"https://{CLOUDFRONT_DOMAIN}/{AWS_LOCATION}/"

DEFAULT_FILE_STORAGE        = 'core.utils.MediaStore'
MEDIA_URL                   = f"https://{CLOUDFRONT_DOMAIN}/media/"

CKEDITOR_UPLOAD_PATH = 'uploads/'

SECURE_HSTS_SECONDS = 2592000  # Unit is seconds; *USE A SMALL VALUE FOR TESTING!*
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
