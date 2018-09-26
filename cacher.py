import json
import os
from application import create_app
from application import redis_store
from apscheduler.schedulers.blocking import BlockingScheduler

from deependeliminator.standings import build_standings_list

sched = BlockingScheduler()


def do_cache(load_oauth_from_redis=True, write_oauth_to_redis=True):

    redis_store.setex(
        'standings',
        7200,
        json.dumps(build_standings_list(
            week=os.environ.get('WEEK', 1),
            load_oauth_from_redis=load_oauth_from_redis,
            write_oauth_to_redis=write_oauth_to_redis
        ))
    )

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
