import constants

import json

import requests

def get_leaderboard_data():
    session = requests.Session()
    session.post('https://duelingnexus.com/api/login.php', data = {'email' : constants.EMAIL, 'password' : constants.PASSWORD, 'remember' : 'true'})

    return json.loads(session.get('https://duelingnexus.com/api/leaderboard.php').text).get('players')

def format_leaderboard(leaderboard):
    leaderboard_str = '**#** **Player** **Rating**\n'

    for player in leaderboard:
        rank = player.get('rank')
        username = player.get('username')
        rating = player.get('rating')

        leaderboard_str += '**{}** {} ({})\n'.format(rank, username, rating)

    return leaderboard_str

def get_leaderboard(page):
    return format_leaderboard(get_leaderboard_data()[page * 10 - 10 : page * 10])
