import os

# Default setting module for developer convenience.
# For production, set DJANGO_SETTINGS_MODULE=hotwheels_project.settings.production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotwheels_project.settings.local')

from .local import *
