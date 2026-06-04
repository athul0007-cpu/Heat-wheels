from .base import *

# Local development settings
DEBUG = True
ALLOWED_HOSTS = ['*']

# In development, use SQLite by default. PostgreSQL can be configured in production.
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
}
