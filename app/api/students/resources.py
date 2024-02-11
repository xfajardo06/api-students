
from flask_restx import Namespace, Resource
from flask import make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import ValidationError
from app.api.students.schemas import SchemaStudentCreated, SchemaStudentInscription

# Models
from app.models.students import Student
from app.models.enrollments import EnrolledSubject
from app.models.subjects import Subject
from app.models.users import User

import app.utils.responses as resp
from app.utils.responses import response_with

api = Namespace(
    'students',
    description="API para obtener información de estudiantes y gestionar sus materias",
)

@api.route("/inscription")
class CreateStudent(Resource):
    @jwt_required()
    def post(self):
        """
        Endpoint para crear un nuevo estudiante.
        """
        try:
            current_user_id = get_jwt_identity()

            user = User.objects(id=current_user_id).first()
            data = request.json

            try:
                create_request = SchemaStudentCreated(**data)
            except ValidationError as e:
                return response_with(
                    response=resp.BAD_REQUEST_SCHEMA,
                    error = e.errors()
                )


            if Student.objects(user=user).first():
                return response_with(
                    response=resp.BAD_REQUEST_400,
                    error="El estudiante ya existe"
                )
            student = Student(
                user=user,
                name=create_request.name,
                semester=create_request.semester,
                credits=create_request.credits
            )
            student.save()

            return response_with(resp.SUCCESS_200, data={'student_id': str(student.id)})
        except Exception as err:
            return response_with(
                response=resp.BAD_REQUEST_400,
                error="Algo inesperado ha ocurrido"
            )


@api.route("/<string:student_id>/enrolled_subject")
class RegisterSubject(Resource):
    @jwt_required()
    def post(self, student_id):
        """
        Endpoint para inscribir a un estudiante en una materia.
        """
        student = Student.objects(id=student_id).first()

        if not student:
            return response_with(response=resp.NOT_FOUND_404, error="Estudiante no encontrado")

        data = request.json

        # Validar los datos de entrada
        try:
            create_request = SchemaStudentInscription(**data)
        except ValidationError as e:
            return response_with(response=resp.BAD_REQUEST_SCHEMA, error= e.errors())

        # Obtener los códigos de las materias de la solicitud
        subject_codes = create_request.subject_codes

        # Obtener las materias correspondientes a los códigos
        subjects = Subject.objects(code__in=subject_codes)

        if not subjects:
            return response_with(response=resp.BAD_REQUEST_400, error="Datos inválidos")

        # Verificar si las materias están relacionadas al semestre del estudiante
        if any(student.semester != subject.semester for subject in subjects):
            return response_with(
                response=resp.BAD_REQUEST_400,
                error="Las materias no están relacionadas al semestre del estudiante"
            )

        # Verificar si el estudiante ya está inscrito en alguna de las materias
        enrolled_subjects = EnrolledSubject.objects(student=student, subject__in=subjects)
        if enrolled_subjects:
            return response_with(
                response=resp.BAD_REQUEST_400,
                error="El estudiante no puede inscribirse 2 veces en la misma materia"
            )

        # Verificar si el estudiante ha aprobado los requisitos previos de las materias
        for subject in subjects:
            if subject.prerequisites:
                for prerequisite in subject.prerequisites:
                    if not EnrolledSubject.objects(student=student, subject=prerequisite, status='finished'):
                        return response_with(
                            response=resp.BAD_REQUEST_400,
                            error=f"El estudiante no ha aprobado el requisito previo {prerequisite.code}"
                        )

        # Inscribir al estudiante en las materias
        subjects_enrolled = []
        for subject in subjects:
            enrolled_subject = EnrolledSubject(
                subject=subject,
                student=student
            )
            enrolled_subject.save()
            subjects_enrolled.append(enrolled_subject.to_dict())

        return response_with(
            response=resp.SUCCESS_200,
            data={'name': student.name, 'subjects_enrolled': subjects_enrolled}
        )


@api.route("/<string:student_id>/subjects")
class Subjects(Resource):
    @jwt_required()
    def get(self, student_id):
        """
        Obtiene las materias inscritas por un estudiante.

        Returns:
            JSON: Respuesta con las materias inscritas del estudiante y código de estado HTTP.
        """
        student = Student.objects(id=student_id).first()
        if student:
            subjects_enrolled = EnrolledSubject.get_all_subjects(student)
            subjects_enrolled = [subject.to_dict() for subject in subjects_enrolled]

            # Devolver una respuesta exitosa con las materias inscritas
            return response_with(
                response=resp.SUCCESS_200,
                data={'name': student.name, 'subjects_enrolled': subjects_enrolled}
            )


@api.route('/<string:student_id>/subjects/passed')
class Approveds(Resource):
    @jwt_required()
    def get(self, student_id):
        """
        Endpoint para que un estudiante obtenga la lista de materias aprobadas.
        """
        student = Student.objects(id=student_id).first()
        if student:
            subjects_passed = EnrolledSubject.get_passed_subjects(student)
            subjects_passed = [subject.to_dict() for subject in subjects_passed]

            return response_with(
                response=resp.SUCCESS_200,
                data={'name': student.name, 'subjects_passed': subjects_passed}
            )

        else:
            return response_with(
                response=resp.NOT_FOUND_404,
                error='Estudiante no encontrado'
            )

@api.route('/<string:student_id>/subjects/average')
class Average(Resource):
    @jwt_required()
    def get(self, student_id):
        """
        Endpoint para que un estudiante obtenga el promedio de puntaje general.
        """
        student = Student.objects(id=student_id).first()
        if student:
            subjects = EnrolledSubject.objects(student=student, status__ne='started')
            if subjects:
                total_score = subjects.sum('score')
                average_score = total_score / len(subjects)

                return response_with(
                    response=resp.SUCCESS_200,
                    data={'name': student.name, 'average_score': average_score}
                )
            else:
                return response_with(
                    response=resp.BAD_REQUEST_400,
                    error="El estudiante no tiene materias con puntaje"
                )

        else:
            return response_with(
                response=resp.NOT_FOUND_404,
                error='Estudiante no encontrado'
            )


@api.route('/<string:student_id>/subjects/failed')
class Failed(Resource):
    @jwt_required()
    def get(self, student_id):
        """
        Endpoint para que un estudiante obtenga la lista de materias reprobadas.
        """
        student = Student.objects(id=student_id).first()
        if student:

            failed_subjects = EnrolledSubject.get_failed_subjects(student)
            failed_subjects = [subject.to_dict() for subject in failed_subjects]
            # Filtrar las asignaturas reprobadas
            return response_with(
                    response=resp.SUCCESS_200,
                    data={'name': student.name, 'failed_subjects': failed_subjects}
                )
        else:
            return response_with(
                response=resp.NOT_FOUND_404,
                error='Estudiante no encontrado'
            )
