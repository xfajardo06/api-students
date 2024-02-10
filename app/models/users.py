from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mongoengine import Document
from mongoengine.fields import (
    StringField, EmailField, ListField,
    BooleanField, DateTimeField)


class User(Document):
    name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    roles = ListField(StringField(), default=["student"])  # Por defecto, un usuario es un estudiante
    active = BooleanField(default=True)
    phone = StringField(max_length=15)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)