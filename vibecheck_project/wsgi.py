"""
WSGI config for vibecheck_project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vibecheck_project.settings')

application = get_wsgi_application()
