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

@app.route('/vehicles', methods = ['GET'])
def get_veh_ids():
    return str(vehicle_ids)

@app.route('/player/<name>', methods = ['GET'])
def get_player(name):
    if(name not in id_cache):
        request = requests.get(base_url + 'account/list/?application_id=' + app_id + '&search=' + name)
        data = request.json()['data']
        id_cache[name] = data[0]['account_id']
    user_id = id_cache[name]
    return str(id_cache)

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

