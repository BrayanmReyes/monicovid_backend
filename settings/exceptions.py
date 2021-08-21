from werkzeug.exceptions import HTTPException


class BadRequestException(HTTPException):
    code = 400

    def __init__(self, data):
        super().__init__(data)


class NotFoundException(HTTPException):
    code = 404

    def __init__(self, data, attribute, value):
        message = f'The {data} was not found with the given {attribute}: {value}'
        super().__init__(message)


class InvalidInputException(HTTPException):
    code = 422

    def __init__(self):
        message = f'You have send invalid inputs'
        super().__init__(message)


class InternalServerException(HTTPException):
    code = 500

    def __init__(self):
        message = 'Internal server error has occurred'
        super().__init__(message)


def handle_exception(error):
    return error


def handle_no_token(error):
    print(error)
    return {'message': 'No token found'}, 401


def handle_invalid_header(error):
    print(error)
    return {'message': 'Token is invalid'}, 401


def handle_expires_token(error):
    print(error)
    return {'message': 'The token has expired'}, 401
