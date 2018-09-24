import os

class Config(object):
    DEBUG = False
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')