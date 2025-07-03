import os
import requests
from datetime import datetime
from app import db
from app.models import TemperatureReading

class NestClient:
    def __init__(self):
        self.client_id = os.getenv('NEST_CLIENT_ID')
        self.client_secret = os.getenv('NEST_CLIENT_SECRET')
        self.project_id = os.getenv('NEST_PROJECT_ID')
        self.refresh_token = os.getenv('NEST_REFRESH_TOKEN')
        self.access_token = None
        
    def get_access_token(self):
        if not self.refresh_token:
            print("No refresh token available")
            return None
            
        url = "https://www.googleapis.com/oauth2/v4/token"
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token,
            'grant_type': 'refresh_token'
        }
        
        response = requests.post(url, data=data)
        if response.status_code == 200:
            self.access_token = response.json()['access_token']
            return self.access_token
        else:
            print(f"Failed to get access token: {response.status_code}")
            print(f"Error response: {response.text}")
            return None
    
    def get_devices(self):
        if not self.access_token:
            self.get_access_token()
            
        if not self.access_token:
            return None
            
        url = f"https://smartdevicemanagement.googleapis.com/v1/enterprises/{self.project_id}/devices"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('devices', [])
        else:
            print(f"Failed to get devices: {response.status_code}")
            return None
    
    def get_thermostat_data(self, device_id):
        if not self.access_token:
            self.get_access_token()
            
        if not self.access_token:
            return None
            
        url = f"https://smartdevicemanagement.googleapis.com/v1/{device_id}"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"Raw API response: {data}")
            return data
        else:
            print(f"Failed to get thermostat data: {response.status_code}")
            print(f"Error response: {response.text}")
            return None

def collect_temperature_data():
    from app import create_app
    app = create_app()
    
    with app.app_context():
        client = NestClient()
        devices = client.get_devices()
        
        if not devices:
            print("No devices found or authentication failed")
            return
        
        for device in devices:
            device_id = device.get('name')
            device_data = client.get_thermostat_data(device_id)
            
            if device_data:
                traits = device_data.get('traits', {})
                
                temp_data = traits.get('sdm.devices.traits.Temperature', {})
                humidity_data = traits.get('sdm.devices.traits.Humidity', {})
                thermostat_data = traits.get('sdm.devices.traits.ThermostatTemperatureSetpoint', {})
                hvac_data = traits.get('sdm.devices.traits.ThermostatHvac', {})
                
                if temp_data:
                    temp_c = temp_data.get('ambientTemperatureCelsius')
                    print(f"Temperature data extracted: {temp_c}°C")
                    print(f"Full temperature traits: {temp_data}")
                    
                    reading = TemperatureReading(
                        device_name=device_data.get('displayName', 'Unknown'),
                        temperature_c=temp_c,
                        temperature_f=temp_c * 9/5 + 32 if temp_c else None,
                        humidity=humidity_data.get('ambientHumidityPercent'),
                        target_temperature_c=thermostat_data.get('heatCelsius') or thermostat_data.get('coolCelsius'),
                        target_temperature_f=(thermostat_data.get('heatCelsius') or thermostat_data.get('coolCelsius', 0)) * 9/5 + 32 if thermostat_data else None,
                        hvac_mode=hvac_data.get('mode'),
                        hvac_state=hvac_data.get('status')
                    )
                    
                    db.session.add(reading)
        
        db.session.commit()
        print(f"Temperature data collected at {datetime.now()}")