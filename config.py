import os

class Config(object):
    DEBUG = False
    BROKER_URL = REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = BROKER_URL