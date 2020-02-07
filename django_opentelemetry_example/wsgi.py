"""
WSGI config for django_opentelemetry_example project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
from opentelemetry.ext.wsgi import OpenTelemetryMiddleware
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_opentelemetry_example.settings')

from django_opentelemetry_example.tracer import setup_tracer
setup_tracer('django-wsgi-service')

application = get_wsgi_application()
application = OpenTelemetryMiddleware(application)
