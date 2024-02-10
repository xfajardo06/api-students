import mongoengine

from datetime import datetime
from flask_mongoengine import Document
from mongoengine.fields import (
    StringField, ReferenceField,
    BooleanField, DateTimeField, IntField)

# Models
from app.models.users import User

class Student(Document):
    # Opciones, pueden ser otra colección en la DB
    SEMESTER_CHOICES = (
        ('1', 'Semestre 1'),
        ('2', 'Semestre 2'),
        ('3', 'Semestre 3'),
        ('4', 'Semestre 4'),
    )
    user = ReferenceField(User, required=True, unique=True, reverse_delete_rule=mongoengine.CASCADE)
    name = StringField(required=True)
    credits = IntField(required=True)
    semester = StringField(choices=SEMESTER_CHOICES, required=True)
    active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)

