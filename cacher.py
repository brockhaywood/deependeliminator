import json
import os
from application import create_app
from application import redis_store
from apscheduler.schedulers.blocking import BlockingScheduler

from deependeliminator.standings import build_standings_list

sched = BlockingScheduler()


def do_cache():
    oauth = redis_store.get('oauth')
    if not oauth:
        raise Exception('No OAuth creds')

    with open('oauth.json', 'w+') as fd:
        fd.write(oauth.decode('utf-8'))

    redis_store.setex('standings', 7200, json.dumps(build_standings_list(os.environ.get('WEEK', 1))))

    with open('oauth.json', 'r') as fd:
        s = fd.read()
        if s:
            redis_store.set('oauth', s)

@sched.scheduled_job(
    'cron',
    day_of_week=os.environ.get('CACHER_GAME_TIME_DAY', 'sun'),
    hour=os.environ.get('CACHER_GAME_TIME_HOUR', None),
    minute=os.environ.get('CACHER_GAME_TIME_MINUTE', None)
)
def cache_standings_list_game_time():
    do_cache()


@sched.scheduled_job(
    'cron',
    day_of_week=os.environ.get('CACHER_OFF_TIME_DAY', 'mon-sat'),
    hour=os.environ.get('CACHER_OFF_TIME_HOUR', None),
    minute=os.environ.get('CACHER_OFF_TIME_MINUTE', None)
)
def cache_standings_list_off_time():
    do_cache()

if __name__ == '__main__':
    create_app(__name__)
    sched.start()
