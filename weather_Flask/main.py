from flask import Flask, render_template, request
import requests
import os
from pprint import pformat

app = Flask(__name__)

# Configuration for weather providers
WEATHER_PROVIDERS = {
    'openweather': {
        'name': 'OpenWeatherMap',
        'url': lambda city, key: f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric",
        'api_key': os.getenv('OPENWEATHER_API_KEY', ''),
        'parser': lambda data: {
            'temp': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description']
        }
    },
    'weatherapi': {
        'name': 'WeatherAPI',
        'url': lambda city, key: f"http://api.weatherapi.com/v1/current.json?key={key}&q={city}&aqi=no",
        'api_key': os.getenv('WEATHERAPI_API_KEY', ''),
        'parser': lambda data: {
            'temp': data['current']['temp_c'],
            'humidity': data['current']['humidity'],
            'description': data['current']['condition']['text']
        }
    }
}

@app.route('/')
def index():
    return render_template('index.html', providers=WEATHER_PROVIDERS.keys())

@app.route('/weather', methods=['POST'])
def get_weather():
    city = request.form['city']
    selected_providers = request.form.getlist('providers')
    
    results = []
    
    for provider_id in selected_providers:
        provider = WEATHER_PROVIDERS.get(provider_id)
        if not provider or not provider['api_key']:
            continue
            
        try:
            response = requests.get(provider['url'](city, provider['api_key']))
            response.raise_for_status()
            weather_data = response.json()
            parsed_data = provider['parser'](weather_data)
            results.append({
                'provider': provider['name'],
                'data': parsed_data,
                'raw': pformat(weather_data)
            })
        except requests.exceptions.RequestException as e:
            results.append({
                'provider': provider['name'],
                'error': str(e)
            })
        except KeyError as e:
            results.append({
                'provider': provider['name'],
                'error': f'Unexpected response format: {str(e)}'
            })
    
    return render_template('weather.html', city=city, results=results)

if __name__ == '__main__':
    app.run(debug=True)