from flask import Flask, jsonify, request, make_response, abort
from influxdb import InfluxDBClient
import requests
import os
from datetime import datetime
from service import find_by_city, parse_city_response

INFLUXDB_USER = os.environ.get('INFLUXDB_USER')
INFLUXDB_PASSWORD = os.environ.get('INFLUXDB_PASSWORD')
INFLUX_DB = os.environ.get('INFLUX_DB')
client = InfluxDBClient('influxdb', 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, INFLUX_DB)

app = Flask(__name__)


@app.route("/checkCurrentWeather", methods=['GET'])
def current_weather():
    city = requests.get('http://ipinfo.io/json').json()['city']
    return city_weather(city)


@app.route("/checkCityWeather", methods=['GET'])
def city_weather(city = None):
    if city == None:
        city = request.args.get('city')
    if city is None:
        abort(404)
    weather = find_by_city(city)
    if weather['cod'] != 200:
        abort(404)
    response = parse_city_response(weather)

    client.write_points([{
        "measurement": "endpoint_request",
        "tags": {
            "endpoint": "/checkCityWeather",
            "city": response['city']
        },
        "time": datetime.now(),
        "fields": {
            "value": response['degrees']
        }
    }])
    return response



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__":
    app.run (host="0.0.0.0",debug=True)
