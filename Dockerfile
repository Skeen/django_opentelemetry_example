FROM python:3
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code/

COPY requirements.txt /code/
RUN pip install -r requirements.txt

RUN git clone https://github.com/Skeen/opentelemetry-python.git
RUN pip install -e opentelemetry-python/opentelemetry-api
RUN pip install -e opentelemetry-python/opentelemetry-sdk
RUN pip install -e opentelemetry-python/ext/opentelemetry-ext-jaeger
RUN pip install -e opentelemetry-python/ext/opentelemetry-ext-psycopg2
RUN pip install -e opentelemetry-python/ext/opentelemetry-ext-dbapi
RUN pip install -e opentelemetry-python/ext/opentelemetry-ext-wsgi
RUN pip install -e opentelemetry-python/ext/opentelemetry-ext-asgi
RUN pip install requests
RUN pip install -e opentelemetry-python/ext/opentelemetry-ext-http-requests
RUN pip install daphne
RUN pip install gunicorn

COPY . /code/

CMD ["sh", "/code/entrypoint.sh"]
