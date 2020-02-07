#!/bin/bash

# Migrate database, and create admin user
python manage.py migrate
python manage.py shell -c "from django.contrib.auth import get_user_model; get_user_model().objects.create(username='admin')"

# Start ASGI
daphne -b 0.0.0.0 -p 8001 django_opentelemetry_example.asgi:application &
ASGI_PID=$!

# Start WSGI
gunicorn -b 0.0.0.0 -p 8000 django_opentelemetry_example.wsgi:application &
WSGI_PID=$!

# Wait for both to exit
wait ${ASGI_PID}
wait ${WSGI_PID}
