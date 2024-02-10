import mongoengine
from datetime import datetime
from flask_mongoengine import Document
from mongoengine.fields import (
    FloatField, ReferenceField, DateTimeField, StringField)

from app.models.students import Student
from app.models.subjects import Subject



class EnrolledSubject(Document):
    SUBJECT_CHOICES = (
        ('MAT1', 'Matemáticas 1'),
        ('MAT2', 'Matemáticas 2'),
        ('FIS1', 'Física 1'),
        ('FIS2', 'Física 2'),
    )

    STATUS_CHOICES = (
        ('started', 'En curso'),
        ('finished', 'Aprobada'),
        ('failed', 'Reprobada')
    )

    subject = ReferenceField(Subject, required=True, reverse_delete_rule=mongoengine.CASCADE)
    student = ReferenceField(Student, required=True)
    score = FloatField(min_value=0, max_value=5, default=0)
    status = StringField(choices=STATUS_CHOICES, default='started')
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    @staticmethod
    def get_passed_subjects(student):
        return EnrolledSubject.objects(student=student, status='finished')

    @staticmethod
    def get_failed_subjects(student):
        return EnrolledSubject.objects(student=student, status='failed')

    @staticmethod
    def get_all_subjects(student):
        return EnrolledSubject.objects(student=student)

    @staticmethod
    def determine_status(score: float) -> str:
        if score >= 3.0:
            return 'finished'
        else:
            return 'failed'

    def to_dict(self):
        return {
            'code': self.subject.code,
            'name': self.subject.name,
            'score': self.score,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

