import json

def load_station_name(station_code=None):
    with open('station.json') as json_file:
        json_data = json.load(json_file, endcoding='utf8')
        print(json_data)

load_station_name()