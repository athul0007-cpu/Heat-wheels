import os
from .base import *
import os
print('🛠️ DEBUG: DATABASE_URL =', os.getenv('DATABASE_URL'))

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
DATABASES['default'] = env.db('DATABASE_URL', default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'))

# Static files configuration for production
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
WHITENOISE_USE_FINDERS = True

# Django 5 uses STORAGES; keep static/media backends explicit for Render.
# Configure storage backends. Use Cloudinary for media if CLOUDINARY_URL is set;
# otherwise fall back to the local file system storage.
import os
if os.getenv('CLOUDINARY_URL'):
    STORAGES = {
        'default': {
            'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage',
        },
        'staticfiles': {
            'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
        },
    }
else:
    # Fallback to local filesystem storage (good for testing/development)
    STORAGES = {
        'default': {
            'BACKEND': 'django.core.files.storage.FileSystemStorage',
        },
        'staticfiles': {
            'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
        },
    }

# Allow all origins by default for simplicity; you can restrict later using env var.
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=['*'])
