"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os
import django
from channels.routing import get_default_application
from opentelemetry.ext.asgi import OpenTelemetryMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_opentelemetry_example.settings')
django.setup()

from django_opentelemetry_example.tracer import setup_tracer
setup_tracer('django-asgi-service')

class DebugMiddleware:
    def __init__(self, asgi):
        self.asgi = asgi

    async def __call__(self, scope, receive, send):
        async def wrapped_receive():
            payload = await receive()
            print(payload)
            return payload

        async def wrapped_send(payload):
            print(payload)
            await send(payload)
        
        await self.asgi(scope, wrapped_receive, wrapped_send)

application = get_default_application()
application = OpenTelemetryMiddleware(application)
application = DebugMiddleware(application)
