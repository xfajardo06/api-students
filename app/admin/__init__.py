
from .views import admin


def initialize_admin(app):
    admin.init_app(app)