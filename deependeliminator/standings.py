import datetime
import json
import os
import xmltodict

from yahoo_oauth import OAuth2

from application import redis_store

def build_standings_list(week=1, load_oauth_from_redis=True, write_oauth_to_redis=True):

    if load_oauth_from_redis:
        oauth = redis_store.get('oauth')
        if not oauth:
            raise Exception('No OAuth creds')

        with open('oauth.json', 'w+') as fd:
            fd.write(oauth.decode('utf-8'))

    oauth = OAuth2(None, None, from_file='oauth.json')
    oauth.refresh_access_token()

    teams = []

    doc = xmltodict.parse(oauth.session.get(
        'https://fantasysports.yahooapis.com/fantasy/v2/league/380.l.298570/teams').text)

    team_keys = [team['team_key'] for team in doc['fantasy_content']['league']['teams']['team']]

    for team_key in team_keys:
        doc = xmltodict.parse(
            oauth.session.get('https://fantasysports.yahooapis.com/fantasy/v2/team/{}/roster;'.format(team_key)).text)

        players_node = doc['fantasy_content']['team']['roster']['players']

        if not players_node or (int(players_node['@count']) < int(os.environ.get('MIN_PLAYERS', 7))):
            continue

        doc = xmltodict.parse(
            oauth.session.get('https://fantasysports.yahooapis.com/fantasy/v2/team/{}/stats;type=week;week={}'.format(
                team_key, week)).text)

        teams.append({
            'name': doc['fantasy_content']['team']['name'],
            'points': float(doc['fantasy_content']['team']['team_points']['total'])
        })

    if write_oauth_to_redis:
        with open('oauth.json', 'r') as fd:
            s = fd.read()
            if s:
                redis_store.set('oauth', s)

    return sorted(teams, key=lambda x: x['points'], reverse=True)


def get_standings_list():
    standings_str = redis_store.get('standings')

    if standings_str:
        standings = json.loads(standings_str.decode('utf-8'))
    else:
        standings = build_standings_list(get_week())

    return standings


def get_week():

    opening_day = datetime.datetime.strptime(os.environ.get('OPENING_DAY', '2018-09-06'), '%Y-%m-%d')
    now = datetime.datetime.now()

    return int(((now - opening_day).days / 7) + 1)