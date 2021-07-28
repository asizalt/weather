from flask import Flask
from datetime import datetime
from influxdb import InfluxDBClient


client = InfluxDBClient('influxdb', 8086, 'admin', 'admin', 'metrics')
app = Flask(__name__)


if __name__ == "__main__":
    app.run (host="0.0.0.0")
