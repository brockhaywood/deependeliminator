import os

from flask import render_template

from application import app
from deependeliminator.standings import get_standings_list


@app.route('/')
@app.route('/index')
def index():
    week = os.environ.get('WEEK', 1)
    return render_template('index.html', week=week, standings=get_standings_list())
