import bugsnag
from bugsnag.flask import handle_exceptions
from flask import Flask
from flask_redis import FlaskRedis
from flask_rebar import Rebar
import os

rebar = Rebar()
redis_store = FlaskRedis()


import deependeliminator.api_routes  # noqa


def create_app(name):
    app = Flask(name)
    app.config.from_object('config.Config')
    rebar.init_app(app=app)
    redis_store.init_app(app)
    bugsnag.configure(
        api_key=os.environ.get('BUGSNAG_API_KEY'),
    )
    handle_exceptions(app)

    return app

app = create_app(__name__)

import deependeliminator.routes  # noqa

if __name__ == '__main__':
    app.run()