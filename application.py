from flask import Flask
from flask_redis import FlaskRedis
from flask_rebar import Rebar

rebar = Rebar()
redis_store = FlaskRedis()

import deependeliminator.api_routes  # noqa


def create_app(name):
    app = Flask(name)
    app.config.from_object('config.Config')
    rebar.init_app(app=app)
    redis_store.init_app(app)

    return app

app = create_app(__name__)

import deependeliminator.routes  # noqa

if __name__ == '__main__':
    app.run()