import requests
import random
from flask import Flask
from flask import render_template
from flask import request
from flask import json

app = Flask(__name__)
app_id = ''
base_url = 'https://api.worldoftanks.com/wot/'
id_cache = {}
vehicle_ids = {}
random.seed(1337)

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Matthew'}
    return render_template('index.html', title = 'Home', user = user)

# view current vehicle IDs
@app.route('/vehicles', methods = ['GET'])
def get_veh_ids():
    return json.jsonify(vehicle_ids)

# view player ID cache
@app.route('/cache', methods = ['GET'])
def get_id_cache():
    return json.jsonify(id_cache)

@app.route('/player/<name>', methods = ['GET'])
def get_player(name):
    # see if player id is in cache, if not then request via Wargaming API
    if(name not in id_cache):
        request = requests.get(base_url + 'account/list/?application_id=' + app_id + '&search=' + name)
        id_data = request.json()['data']
        id_cache[name] = str(id_data[0]['account_id'])
    user_id = id_cache[name]

    # create JSON object with battle/win rate stats for the player's tanks
    player_tanks = {}
    request = requests.get(base_url + 'account/tanks/?application_id=' + app_id + '&account_id=' + user_id)
    tank_data = request.json()['data'][user_id]

    for tank in tank_data:
        tank_win_rate = (tank['statistics']['wins'] * 1.0 / tank['statistics']['battles']) * 100
        tank_battles = tank['statistics']['battles']
        stats_record = {'win_rate': str(tank_win_rate),
                        'battles': str(tank_battles)}
        player_tanks[vehicle_ids[str(tank['tank_id'])]] = stats_record

    return json.jsonify(player_tanks)

# http://mrayermann.com:5000/calc?battles=1000&wins=527&curr=52.7&new=60.0&goal=55.0
@app.route('/calc', methods = ['GET'])
def calc_battles():
    data_points = []
    
    battles = float(request.args['battles'])
    wins = float(request.args['wins'])
    losses = float(battles - wins)
    curr_rate = float(request.args['curr'])
    new_rate = float(request.args['new'])
    goal_rate = float(request.args['goal'])

    new_wins = 0.0
    new_losses = 0.0

    increasing = goal_rate > curr_rate

    while((increasing and curr_rate < goal_rate) or (not increasing and curr_rate > goal_rate)):
        data_points.append(curr_rate)
        battles = battles + 1

        if(random.random() < new_rate / 100.0):
            new_wins = new_wins + 1
            wins = wins + 1
        else:
            new_losses = new_losses + 1
            losses = losses + 1
        
        curr_rate = wins / battles * 100.0
   
    result = {'new_wins': new_wins,
              'new_losses': new_losses,
              'num_battles': new_wins + new_losses,
              'final_rate': curr_rate,
              'new_rate': new_wins / (new_wins + new_losses) * 100.0,
              'data_points': data_points}

    return json.jsonify(result)

# load vehicle ID information from Wargaming API
def load_vehicles():
    request = requests.get(base_url + 'encyclopedia/tanks/?application_id=' + app_id + '&fields=tank_id,short_name_i18n')
    data = request.json()['data']
    for tank_id in data:
        vehicle_ids[tank_id] = data[tank_id]['short_name_i18n']

if __name__ == '__main__':
    with open('config.ini', 'r') as in_file:
        app_id = eval(in_file.read())['app_id']
    load_vehicles()
    app.run(debug = True, host = '0.0.0.0')

