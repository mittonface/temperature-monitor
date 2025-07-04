import os
import requests
from datetime import datetime

class WeatherClient:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.lat = os.getenv('LOCATION_LAT')
        self.lon = os.getenv('LOCATION_LON')
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    def get_current_weather(self):
        """Fetch current weather data from OpenWeatherMap API"""
        if not self.api_key or self.api_key == 'YOUR_API_KEY_HERE':
            print("OpenWeatherMap API key not configured")
            return None
        
        if not self.lat or not self.lon or self.lat == 'YOUR_LATITUDE' or self.lon == 'YOUR_LONGITUDE':
            print("Location coordinates not configured")
            return None
        
        try:
            params = {
                'lat': self.lat,
                'lon': self.lon,
                'appid': self.api_key,
                'units': 'metric'  # Get temperature in Celsius
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'temperature_c': data['main']['temp'],
                    'temperature_f': data['main']['temp'] * 9/5 + 32,
                    'description': data['weather'][0]['description'],
                    'humidity': data['main']['humidity'],
                    'wind_speed': data['wind']['speed']
                }
            else:
                print(f"Failed to get weather data: {response.status_code}")
                print(f"Error response: {response.text}")
                return None
                
        except requests.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None