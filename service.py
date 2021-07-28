import requests
import os
weather_key = os.environ.get('WEATHER_KEY')

def find_by_city(city):
    urla = "http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric".format(city=city, key=weather_key)
    weather = requests.get(urla).json()
    return weather

def parse_city_response(response):
    return {'city':response['name'], 'country':response['sys']['country'], 'degrees':response['main']['temp']}