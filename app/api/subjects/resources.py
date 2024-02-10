from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required
from pydantic import ValidationError
from app.api.subjects.schemas import SchemaFinishSubject

# Models
from app.models.enrollments import EnrolledSubject

# Utils
from app.utils.responses import response_with
import app.utils.responses as resp
api = Namespace('subjects', 'API para registrar nota de estudiantes')

@api.route("/finish/<string:enrolled_subject_id>")
@api.doc(params={'enrolled_subject_id': 'ID of the enrolled subject'})
class FinishSubject(Resource):
    @jwt_required()
    def post(self, enrolled_subject_id):
        """
        Endpoint para finalizar una materia inscrita por un estudiante.
        """
        data = request.json
        try:
            create_request = SchemaFinishSubject(**data)
        except ValidationError as e:
                return response_with(
                    response=resp.BAD_REQUEST_SCHEMA,
                    error = e.errors()
                )

        enrolled_subject = EnrolledSubject.objects(id=enrolled_subject_id).first()

        if not enrolled_subject:
            return response_with(response=resp.NOT_FOUND_404, error="Materia inscrita no encontrada")

        # Verificar si la materia ya está finalizada
        if enrolled_subject.status == 'finished' or enrolled_subject.status == 'failed':
            return response_with(response=resp.BAD_REQUEST_400, error="La materia ya está finalizada")

        # Actualizar el estado de la materia a finalizada
        enrolled_subject.status = EnrolledSubject.determine_status(create_request.score)
        enrolled_subject.score = create_request.score
        enrolled_subject.save()

        return response_with(response=resp.SUCCESS_200, message='Materia finalizada exitosamente')
