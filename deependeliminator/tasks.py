import celery
import json
import os
from standings import get_week


@celery.task()
def cache_standings(load_oauth_from_redis=True, write_oauth_to_redis=True):
    from deependeliminator.standings import build_standings_list
    from application import redis_store

    redis_store.setex(
        'standings',
        7200,
        json.dumps(build_standings_list(
            week=get_week(),
            load_oauth_from_redis=load_oauth_from_redis,
            write_oauth_to_redis=write_oauth_to_redis
        ))
    )
