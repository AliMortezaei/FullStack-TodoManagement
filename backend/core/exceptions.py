from http import HTTPStatus

class CustomExeption(Exception):
    code = HTTPStatus.BAD_GATEWAY
    error_code = HTTPStatus.BAD_GATEWAY
    message = HTTPStatus.BAD_GATEWAY.description

    def __init__(self, message: str | None = None):
        if message:
            self.message = message

class BadRequestException(CustomExeption):
    code = HTTPStatus.BAD_REQUEST
    error_code = HTTPStatus.BAD_REQUEST
    message = HTTPStatus.BAD_REQUEST.description


class NotFoundException(CustomExeption):
    code = HTTPStatus.NOT_FOUND
    error_code = HTTPStatus.NOT_FOUND
    message = HTTPStatus.NOT_FOUND.description


class ForbiddenException(CustomExeption):
    code = HTTPStatus.FORBIDDEN
    error_code = HTTPStatus.FORBIDDEN
    message = HTTPStatus.FORBIDDEN.description

class ConflictException(CustomExeption):
    code = HTTPStatus.CONFLICT
    error_code = HTTPStatus.CONFLICT
    massage = HTTPStatus.CONFLICT.description