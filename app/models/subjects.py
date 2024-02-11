import mongoengine
from flask_mongoengine import Document
from datetime import datetime
from mongoengine.fields import (
    StringField, DateTimeField, ListField,
    IntField, ReferenceField)

# Modelos

class Subject(Document):
    SEMESTER_CHOICES = (
        ('1', 'Semestre 1'),
        ('2', 'Semestre 2'),
        ('3', 'Semestre 3'),
        ('4', 'Semestre 4'),
    )
    code = StringField(required=True, unique=True)
    name = StringField(required=True)
    semester = StringField(choices=SEMESTER_CHOICES, required=True)
    credits = IntField(required=True)
    prerequisites = ListField(ReferenceField('self', reverse_delete_rule=mongoengine.CASCADE))

    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    def get_prerequisites_dict(self):
        prerequisites_dict = {}
        for prerequisite in self.prerequisites:
            prerequisites_dict[prerequisite.code] = prerequisite.name
        return prerequisites_dict

    meta = {
        'indexes': ['code']
    }
