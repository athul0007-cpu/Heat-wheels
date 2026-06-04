from .base import *

DEBUG = False

# Allowed hosts for production
ALLOWED_HOSTS = ['heatwheels.onrender.com', 'localhost', '127.0.0.1']

# CSRF trusted origins for production
CSRF_TRUSTED_ORIGINS = ['https://heatwheels.onrender.com']

# In production, set the database connection via environment variables.
DATABASES['default'] = env.db('DATABASE_URL', default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'))

# Static files configuration for production
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
WHITENOISE_USE_FINDERS = True

# Django 5 uses STORAGES; keep static/media backends explicit for Render.
STORAGES = {
    'default': {
        'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage',
    },
    'staticfiles': {
        'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
    },
}

CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])
