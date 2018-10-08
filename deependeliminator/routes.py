import os

from flask import render_template

from application import app
from deependeliminator.standings import get_standings_list
from standings import get_week


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', week=get_week(), standings=get_standings_list())
