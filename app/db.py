import os
from dotenv import load_dotenv
from flask_mongoengine import MongoEngine
db = MongoEngine()

load_dotenv()

def initialize_db(app):
    app.config['MONGODB_SETTINGS'] = {
        'host': os.environ.get('MONGODB_URI')
    }
    db.init_app(app)
