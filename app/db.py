from flask_mongoengine import MongoEngine
db = MongoEngine()


def initialize_db(app):
    app.config['MONGODB_SETTINGS'] = {
        'db': 'calificaciones',
        'host': 'localhost',
        'port': 27017
    }
    db.init_app(app)
