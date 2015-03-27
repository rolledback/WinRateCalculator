import requests
import os

from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import json

app = Flask(__name__)
app_id = ''
base_url = 'https://api.worldoftanks.com/wot/'
id_cache = {}
vehicle_ids = {}

@app.route('/')
@app.route('/index')
def index():
    return render_template('app.html')

# view current vehicle IDs
@app.route('/api/vehicles', methods = ['GET'])
def get_veh_ids():
    return json.jsonify(vehicle_ids)

# get player ID cache
@app.route('/api/cache', methods = ['GET'])
def get_id_cache():
    return json.jsonify(id_cache)

@app.route('/api/player/<name>', methods = ['GET'])
def get_player(name):
    result = {'name': '', 'tanks': []}

    # see if player id is in cache, if not then request via Wargaming API
    if(name not in id_cache):
        request = requests.get(base_url + 'account/list/?application_id=' + app_id + '&search=' + name)
        if(len(request.json()['data']) < 1):
            return json.jsonify(result)
        id_data = request.json()['data']
        id_cache[name] = str(id_data[0]['account_id'])
    user_id = id_cache[name]

    # create JSON object with battle/win rate stats for the player's tanks
    player_tanks = []
    request = requests.get(base_url + 'account/tanks/?application_id=' + app_id + '&account_id=' + user_id)
    tank_data = request.json()['data'][user_id]

    win_total = 0.0
    battle_total = 0.0

    for tank in tank_data:
        tank_win_rate = (tank['statistics']['wins'] * 1.0 / tank['statistics']['battles']) * 100
        tank_wins = tank['statistics']['wins']
        tank_battles = tank['statistics']['battles']
        stats_record = {'name': vehicle_ids[str(tank['tank_id'])]['short_name'],
                        'win_rate': str(round(tank_win_rate, 2)),
                        'wins': str(tank_wins),
                        'battles': str(tank_battles),
                        'image': vehicle_ids[str(tank['tank_id'])]['image'],
                        'sort_value': 0}
        player_tanks.append(stats_record)

        win_total = win_total + tank_wins
        battle_total = battle_total + tank_battles

    player_tanks.append({'name': 'Overall',
                         'win_rate': '0' if battle_total == 0 else str(round(win_total / battle_total * 100, 2)),
                         'wins': str(win_total),
                         'battles': str(battle_total),
                         'image': "",
                         'sort_value': 1})
    player_tanks = sorted(player_tanks, key = lambda k: (k['sort_value'], float(k['battles'])), reverse = True)

    result['tanks'] = player_tanks
    result['name'] = name
    return json.jsonify(result)

# http://mrayermann.com:5000/calc?battles=1000&wins=527&curr=52.7&new=60.0&goal=55.0
@app.route('/api/calc', methods = ['GET'])
def calc_battles():
    data_points = []

    battles = float(request.args['battles'])
    wins = float(request.args['wins'])
    losses = float(battles - wins)
    curr_rate = float(request.args['curr'])
    new_rate = float(request.args['new'])
    goal_rate = float(request.args['goal'])

    if('nick' in request.args):
        nick =  request.args['nick']
    else:
        nick =''

    new_wins = 0.0
    new_battles = 0.0

    increasing = goal_rate > curr_rate
    orig_rate = curr_rate
    while((increasing and curr_rate < goal_rate) or (not increasing and curr_rate > goal_rate)):
        data_points.append({'x' : int(new_battles), 'y' : curr_rate})
        new_battles = new_battles + 1
        new_wins = float((new_battles * (new_rate / 100.0)))
        curr_rate = (new_wins + wins) / (new_battles + battles) * 100.0
   
    result = {'new_rate': new_rate,
              'orig_rate': orig_rate,
              'new_wins': new_wins,
              'new_losses': new_battles - new_wins,
              'new_battles': new_battles,
              'new_rate': new_wins / new_battles * 100.0,
              'goal_rate': goal_rate,
              'data_points': data_points,
              'nick': nick}

    return json.jsonify(result)

# load vehicle ID information from Wargaming API
def load_vehicles():
    request = requests.get(base_url + 'encyclopedia/tanks/?application_id=' + app_id + '&fields=tank_id,short_name_i18n,image_small')
    data = request.json()['data']
    for tank_id in data:
        vehicle_ids[tank_id] = {'short_name': data[tank_id]['short_name_i18n'], 'image': data[tank_id]['image_small']}

if __name__ == '__main__':
    with open('config.ini', 'r') as in_file:
        app_id = eval(in_file.read())['app_id']
    load_vehicles()
    app.run(debug = False, host = '0.0.0.0')

