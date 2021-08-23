FROM python:3.8.5

WORKDIR /code

COPY ../backend/requirements.in ../backend/Makefile ./
RUN make deps && apt-get update && apt-get install nano
COPY ../backend/ .

CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000
