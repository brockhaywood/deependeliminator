import os

from flask import render_template

from application import app


@app.route('/')
@app.route('/index')
def index():
    from deependeliminator.standings import get_standings_list
    from deependeliminator.standings import get_week
    return render_template('index.html', week=get_week(), standings=get_standings_list())
