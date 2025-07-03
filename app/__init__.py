from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-key')
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "data", "temperatures.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    from app.routes import main
    app.register_blueprint(main)
    
    from app.swagger import init_swagger
    init_swagger(app)
    
    with app.app_context():
        db.create_all()
    
    return app