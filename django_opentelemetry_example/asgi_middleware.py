import functools
import typing

from opentelemetry import propagators, trace
# from opentelemetry.ext.wsgi.version import __version__  # noqa
from opentelemetry.trace.status import Status, StatusCanonicalCode

__version__ = '0.0.0'

_HTTP_VERSION_PREFIX = "HTTP/"


def get_header_from_scope(
    scope: dict, header_name: str
) -> typing.List[str]:
    headers = scope.get('headers')
    for key, value in headers:
        if key == header_name:
            return [value]
    return []


def get_default_span_name(scope):
    return scope.get("path", "/")


class OpenTelemetryMiddleware:
    """The ASGI application middleware.

    Args:
        asgi: The ASGI application callable to forward requests to.
    """
    def __init__(self, asgi):
        self.asgi = asgi
        self.tracer = trace.tracer_source().get_tracer(__name__, __version__)

    async def __call__(self, scope, receive, send):
        parent_span = propagators.extract(get_header_from_scope, scope)
        span_name = get_default_span_name(scope)

        span = self.tracer.start_span(
            span_name,
            parent_span,
            kind=trace.SpanKind.SERVER,
            attributes={}#collect_request_attributes(scope),
        )

        try:
            with self.tracer.use_span(span):
                await self.asgi(scope)(receive, send)
                span.end()
        except:  # noqa
            # TODO Set span status (cf. https://github.com/open-telemetry/opentelemetry-python/issues/292)
            span.end()
            raise
