python manage.py migrate
python manage.py shell -c "from django.contrib.auth import get_user_model; get_user_model().objects.create(username='admin')"
daphne -b 0.0.0.0 -p 8001 django_opentelemetry_example.asgi:application
