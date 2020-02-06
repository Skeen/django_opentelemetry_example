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

from pprint import pformat


class App:
    def __init__(self, scope):
        self.scope = scope

    async def __call__(self, receive, send):
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                [b'content-type', b'text/plain'],
            ],
        })
        await send({
            'type': 'http.response.body',
            'body': pformat(self.scope).encode('utf8'),
        })

from opentelemetry import trace
from opentelemetry.ext import jaeger
from opentelemetry.sdk.trace import TracerSource
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor

jaeger_exporter = jaeger.JaegerSpanExporter(
    service_name='django-asgi-service',
    # configure agent
    agent_host_name='jaeger',
    agent_port=6831,
)
span_processor = BatchExportSpanProcessor(jaeger_exporter)

trace.set_preferred_tracer_source_implementation(lambda T: TracerSource())
trace.tracer_source().add_span_processor(
    span_processor
)

import psycopg2
from opentelemetry.ext.psycopg2 import trace_integration

postgres_tracer = trace.tracer_source().get_tracer('postgres')
trace_integration(postgres_tracer)

class DebugMiddleware:
    def __init__(self, asgi):
        self.asgi = asgi

    async def __call__(self, scope, receive, send):
        async def wrapped_send(payload):
            print(payload)
            return await send(payload)
        await self.asgi(scope, receive, wrapped_send)

application = App
# application = get_default_application()
application = OpenTelemetryMiddleware(application)
application = DebugMiddleware(application)
