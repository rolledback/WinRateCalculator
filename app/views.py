import requests
from flask import Flask
from flask import render_template
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
    user = {'nickname': 'Matthew'}
    return render_template('index.html', title = 'Home', user = user)

# view current vehicle IDs
@app.route('/vehicles', methods = ['GET'])
def get_veh_ids():
    return str(vehicle_ids)

# view player ID cache
@app.route('/cache', methods = ['GET'])
def get_id_cache():
    return str(id_cache)

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

    return str(player_tanks)

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

