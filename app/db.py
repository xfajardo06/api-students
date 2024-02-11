import os
from dotenv import load_dotenv
from flask_mongoengine import MongoEngine
db = MongoEngine()

load_dotenv()

def initialize_db(app):
    if os.environ.get('MONGODB_URI'):
        app.config['MONGODB_SETTINGS'] = {
            'host': os.environ.get('MONGODB_URI')
        }
    else:
        app.config['MONGODB_SETTINGS'] = {
        'db': 'calificaciones',
        'host': 'localhost',
        'port': 27017
    }
    db.init_app(app)
