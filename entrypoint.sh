python manage.py migrate
daphne -b 0.0.0.0 -p 8001 django_opentelemetry_example.asgi:application
