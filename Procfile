web: gunicorn wsgi:app
workers: celery worker --beat -A application.celery
