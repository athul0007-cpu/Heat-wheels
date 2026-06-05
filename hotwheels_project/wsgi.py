import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotwheels_project.settings.production')

application = get_wsgi_application()

# Auto-run migrations on serverless cold start (Vercel)
try:
    from django.core.management import call_command
    call_command('migrate', '--run-syncdb', verbosity=0)
except Exception:
    pass

app = application
