import bugsnag
from celery import Celery
from bugsnag.celery import connect_failure_handler
from bugsnag.flask import handle_exceptions
from flask import Flask
from flask_redis import FlaskRedis
from flask_rebar import Rebar
import os

import celeryconfig

rebar = Rebar()
redis_store = FlaskRedis()

import deependeliminator.api_routes  # noqa

def create_app(name):
    app = Flask(name, static_url_path='')
    app.config.from_object('config.Config')
    rebar.init_app(app=app)
    redis_store.init_app(app)
    bugsnag.configure(
        api_key=os.environ.get('BUGSNAG_API_KEY'),
    )
    handle_exceptions(app)

    return app

def make_celery(app):
    # create context tasks in celery
    celery = Celery(
        app.import_name,
        broker=os.environ.get('REDIS_URL')
    )
    celery.conf.update(app.config)
    celery.config_from_object(celeryconfig)
    connect_failure_handler()
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery


app = create_app(__name__)
celery = make_celery(app)

import deependeliminator.routes  # noqa

if __name__ == '__main__':
    app.run()