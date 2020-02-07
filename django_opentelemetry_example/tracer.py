from opentelemetry import trace
from opentelemetry.ext import jaeger
from opentelemetry.sdk.trace import TracerSource
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor

import psycopg2
from opentelemetry.ext.psycopg2 import trace_integration

def setup_tracer(service_name):
    jaeger_exporter = jaeger.JaegerSpanExporter(
        service_name=service_name,
        # configure agent
        agent_host_name='jaeger',
        agent_port=6831,
    )
    span_processor = BatchExportSpanProcessor(jaeger_exporter)

    trace.set_preferred_tracer_source_implementation(lambda T: TracerSource())
    trace.tracer_source().add_span_processor(
        span_processor
    )

    postgres_tracer = trace.tracer_source().get_tracer('postgres')
    trace_integration(postgres_tracer)
