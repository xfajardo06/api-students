from flask_mongoengine import MongoEngine
db = MongoEngine()


def initialize_db(app):
    app.config['MONGODB_SETTINGS'] = {
        'host': 'mongodb+srv://xfajardoc:UshFAaDdMta85slO@cluster0.fciqppv.mongodb.net/'
    }
    db.init_app(app)
