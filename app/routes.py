from flask import Blueprint, render_template, jsonify, request
from app.models import TemperatureReading
from app import db
from datetime import datetime, timedelta
from sqlalchemy import func

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/api/temperatures')
def get_temperatures():
    hours = int(request.args.get('hours', 24))
    since = datetime.utcnow() - timedelta(hours=hours)
    
    readings = TemperatureReading.query.filter(
        TemperatureReading.timestamp >= since
    ).order_by(TemperatureReading.timestamp).all()
    
    return jsonify([r.to_dict() for r in readings])

@main.route('/api/current')
def get_current():
    latest = TemperatureReading.query.order_by(
        TemperatureReading.timestamp.desc()
    ).first()
    
    if latest:
        return jsonify(latest.to_dict())
    return jsonify({'error': 'No data available'}), 404

@main.route('/api/statistics')
def get_statistics():
    hours = int(request.args.get('hours', 24))
    since = datetime.utcnow() - timedelta(hours=hours)
    
    stats = db.session.query(
        func.avg(TemperatureReading.temperature_c).label('avg_temp'),
        func.min(TemperatureReading.temperature_c).label('min_temp'),
        func.max(TemperatureReading.temperature_c).label('max_temp'),
        func.avg(TemperatureReading.humidity).label('avg_humidity')
    ).filter(TemperatureReading.timestamp >= since).first()
    
    return jsonify({
        'avg_temperature': round(stats.avg_temp, 1) if stats.avg_temp else None,
        'min_temperature': round(stats.min_temp, 1) if stats.min_temp else None,
        'max_temperature': round(stats.max_temp, 1) if stats.max_temp else None,
        'avg_humidity': round(stats.avg_humidity, 1) if stats.avg_humidity else None,
        'period_hours': hours
    })

@main.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'service': 'house-temp-tracker'}), 200