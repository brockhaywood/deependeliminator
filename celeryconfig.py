import os
from celery.schedules import crontab


CELERY_IMPORTS = ('deependeliminator.tasks')
CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'UTC'

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULE = {
    'update_standings_off_time': {
        'task': 'deependeliminator.tasks.cache_standings',
        'schedule': crontab(
            day_of_week=os.environ.get('CACHER_OFF_TIME_DAY', 'mon-sat'),
            hour=os.environ.get('CACHER_OFF_TIME_HOUR', '*'),
            minute=os.environ.get('CACHER_OFF_TIME_MINUTE', '*/30')
        ),
    },
    'update_standings_on_time': {
        'task': 'deependeliminator.tasks.cache_standings',
        'schedule': crontab(
            day_of_week=os.environ.get('CACHER_GAME_TIME_DAY', 'sun'),
            hour=os.environ.get('CACHER_GAME_TIME_HOUR', '*'),
            minute=os.environ.get('CACHER_GAME_TIME_MINUTE', '*/5')
        ),
    }
}