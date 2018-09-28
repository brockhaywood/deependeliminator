web: newrelic-admin run-program  gunicorn wsgi:app
workers: newrelic-admin run-program  celery worker --beat -A application.celery
