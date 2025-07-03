from app import db
from datetime import datetime

class TemperatureReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    device_name = db.Column(db.String(100), nullable=False)
    temperature_c = db.Column(db.Float, nullable=False)
    temperature_f = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float)
    target_temperature_c = db.Column(db.Float)
    target_temperature_f = db.Column(db.Float)
    hvac_mode = db.Column(db.String(50))
    hvac_state = db.Column(db.String(50))
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'device_name': self.device_name,
            'temperature_c': self.temperature_c,
            'temperature_f': self.temperature_f,
            'humidity': self.humidity,
            'target_temperature_c': self.target_temperature_c,
            'target_temperature_f': self.target_temperature_f,
            'hvac_mode': self.hvac_mode,
            'hvac_state': self.hvac_state
        }