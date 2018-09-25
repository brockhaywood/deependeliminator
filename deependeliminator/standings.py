import json
import os
import xmltodict

from yahoo_oauth import OAuth2

from application import redis_store


def build_standings_list(week=1):

    oauth = OAuth2(None, None, from_file='oauth.json')
    oauth.refresh_access_token()

    teams = []

    doc = xmltodict.parse(oauth.session.get('https://fantasysports.yahooapis.com/fantasy/v2/league/380.l.1020481/teams').text)

    team_keys = [team['team_key'] for team in doc['fantasy_content']['league']['teams']['team']]

    for team_key in team_keys:
        doc = xmltodict.parse(
            oauth.session.get('https://fantasysports.yahooapis.com/fantasy/v2/team/{}/stats;type=week;week={}'.format(team_key, week)).text)

        teams.append({
            'name': doc['fantasy_content']['team']['name'],
            'points': float(doc['fantasy_content']['team']['team_points']['total'])
        })

    teams = sorted(teams, key=lambda x: x['points'], reverse=True)

    week = int(week)
    if week > 1:
        teams = teams[:-(week-1)]

    return teams


def get_standings_list():
    standings_str = redis_store.get('standings')

    if standings_str:
        standings = json.loads(standings_str.decode('utf-8'))
    else:
        standings = build_standings_list(os.environ.get('WEEK', 1))

    return standings
