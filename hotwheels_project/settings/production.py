import os
from .base import *

DEBUG = False

# Allowed hosts for production
ALLOWED_HOSTS = ['heatwheels.onrender.com', 'localhost', '127.0.0.1', '.vercel.app']
if 'RENDER_EXTERNAL_HOSTNAME' in os.environ:
    ALLOWED_HOSTS.append(os.environ['RENDER_EXTERNAL_HOSTNAME'])
if 'VERCEL_URL' in os.environ:
    ALLOWED_HOSTS.append(os.environ['VERCEL_URL'])

# CSRF trusted origins for production
CSRF_TRUSTED_ORIGINS = ['https://heatwheels.onrender.com', 'https://*.vercel.app']
if 'RENDER_EXTERNAL_HOSTNAME' in os.environ:
    CSRF_TRUSTED_ORIGINS.append('https://' + os.environ['RENDER_EXTERNAL_HOSTNAME'])
if 'VERCEL_URL' in os.environ:
    CSRF_TRUSTED_ORIGINS.append('https://' + os.environ['VERCEL_URL'])

# In production, set the database connection via environment variables.
# Falls back to SQLite if DATABASE_URL is not set or is the placeholder.
_db_url = os.getenv('DATABASE_URL', '')
if _db_url and not _db_url.startswith('<'):
    DATABASES['default'] = env.db('DATABASE_URL')
else:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/db.sqlite3',
    }

# Static files — WhiteNoise serves them via middleware
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True

# Django 5 uses STORAGES; keep static/media backends explicit for Render.
# Configure storage backends. Use Cloudinary for media if CLOUDINARY_URL is set;
# otherwise fall back to the local file system storage.

if os.getenv('CLOUDINARY_URL'):
    STORAGES = {
        'default': {
            'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage',
        },
        'staticfiles': {
            'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
        },
    }
else:
    # Fallback to local filesystem storage (good for testing/development)
    STORAGES = {
        'default': {
            'BACKEND': 'django.core.files.storage.FileSystemStorage',
        },
        'staticfiles': {
            'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
        },
    }

# CORS — only set if django-cors-headers is installed
try:
    import corsheaders  # noqa
    CORS_ALLOW_ALL_ORIGINS = True
except ImportError:
    pass
