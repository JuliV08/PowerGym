"""
WSGI config for powergym_project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'powergym_project.settings.production')

application = get_wsgi_application()
app = application
