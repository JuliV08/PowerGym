"""
Production settings for powergym_project.
"""
from .base import *
from decouple import config

# Override DEBUG
# Override DEBUG
# Override DEBUG
# Override DEBUG
DEBUG = True

# ALLOWED_HOSTS from environment
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='.vercel.app,.powergym.ar').split(',')

# CSRF Settings
CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='https://*.vercel.app,https://powergym.ar,https://www.powergym.ar'
).split(',')

# Security settings for production
SECURE_SSL_REDIRECT = False  # Nginx maneja SSL
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static files
# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles_build' / 'static'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Media Files - Supabase Storage (S3 Compatible)
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default=None)
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default=None)
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', default='Media')
AWS_S3_ENDPOINT_URL = config('AWS_S3_ENDPOINT_URL', default=None)

if AWS_ACCESS_KEY_ID:
    # S3 Settings
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_LOCATION = ''
    AWS_DEFAULT_ACL = 'public-read'
    AWS_QUERYSTRING_AUTH = False  # Important: Supabase public buckets don't use signed URLs
    
    # Use S3 for Media
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    
    # Generate public URL for Supabase: https://[project].supabase.co/storage/v1/object/public/[bucket]/
    # AWS_S3_CUSTOM_DOMAIN needs to be: [project].supabase.co/storage/v1/object/public/[bucket]
    _project_domain = AWS_S3_ENDPOINT_URL.split('//')[1].replace('/s3', '') # Remove https:// and /s3
    AWS_S3_CUSTOM_DOMAIN = f'{_project_domain}/object/public/{AWS_STORAGE_BUCKET_NAME}'
    
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
else:
    # Fallback to local (for build process or if keys missing)
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

# Database - override if using DATABASE_URL
    # Mask password for security in case of screenshot, show host/port
    # safe_url = db_url.split('@')[-1] if '@' in db_url else 'INVALID_FORMAT'
    # raise Exception(f"DIAGNOSTIC: DATABASE_URL is SET. Target: {safe_url}")

if config('DATABASE_URL', default=None):
    import dj_database_url
    DATABASES['default'] = dj_database_url.parse(config('DATABASE_URL'))

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
