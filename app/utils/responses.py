from http import HTTPStatus
from flask import make_response, jsonify


SUCCESS_200 = {
    'http_code': HTTPStatus.OK,
    'code': 'success',
    "message": "OK"
}

BAD_REQUEST_400 = {
    "http_code": HTTPStatus.BAD_REQUEST,
    "code": "badRequest",
    "message": "Petición errada."
}

BAD_REQUEST_SCHEMA = {
    "http_code": HTTPStatus.BAD_REQUEST,
    "code": "batchSchemaError",
    "message": "Hay un error en la estructura del json."
}

NOT_FOUND_404 = {
    "http_code": HTTPStatus.NOT_FOUND,
    "code": "notFound",
    "message": "Recurso no encontrado."
}

UNAUTHORIZED_401 = {
    "http_code": HTTPStatus.UNAUTHORIZED,
    "code": "Unauthorized",
    "message": "Recurso no encontrado."
}


SERVER_ERROR_500 = {
    "http_code": HTTPStatus.INTERNAL_SERVER_ERROR,
    "code": "serverError",
    "message": "Error de servidor."
}


def response_with(response, data=None, message=None, error=None, pagination=None):
    result = {
        'code': response.get('code', 200),
        'status': response.get('http_code', 200),
    }

    if 'message' in response:
        result['message'] = response['message']
    if data is not None:
        result['data'] = data
    if message is not None:
        result['message'] = message
    if error is not None:
        result['errors'] = error
    if pagination is not None:
        result['pagination'] = pagination

    return make_response(jsonify(result), result['status'])
