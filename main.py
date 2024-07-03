from flask import Flask, request, jsonify
import requests
from os import environ

app = Flask(__name__)


IP_INFO_SECRET_KEY = environ.get("IP_INFO_SECRET_KEY")
OPEN_WEATHER_MAP_API_KEY = environ.get("OPEN_WEATHER_MAP_API_KEY")


def get_client_ip():
    response = requests.get(f"https://ipinfo.io/json?token={IP_INFO_SECRET_KEY}").json()
    return response


def get_location(ip):
    response = requests.get(f'https://ip-api.com/json/{ip}').json()
    return response


@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name = request.args.get('visitor_name', 'Not provided')
    ip_info = get_client_ip()
    client_ip = ip_info['ip']
    
    location_data = get_location(client_ip)
    city = location_data['city']
    lon, lat = location_data['lon'], location_data['lat']

    temperature = get_temperature(lon, lat)
    temperature = int(temperature) - 273

    greeting = f"Hello, {visitor_name}! The temperature is {temperature} degrees Celsius in {city}"

    response = {
        "client_ip": client_ip,
        "location": city,
        "greeting": greeting
    }

    return jsonify(response)


def get_temperature(long, lat):
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={OPEN_WEATHER_MAP_API_KEY}").json()
    return response['main']['temp']


if __name__ == '_main_':
    app.run()
