from datetime import datetime

from rest_framework.exceptions import APIException

from Fundoonotes.Response import response_code


class MyBaseException(Exception):
    def __init__(self, msg, code):
        self.code = code
        self.msg = msg


def validate_time(time_data):
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    if time_data < current_time:
        raise PassedTimeException


class DoesNotExistException(APIException):
    status_code = 409
    default_detail = response_code[409]
    default_code = response_code[409]


class PassedTimeException(APIException):
    status_code = 415
    default_detail = response_code[415]
    default_code = response_code[415]


class DoesNotExist(MyBaseException):
    pass


class EmailAlreadyExistsError(MyBaseException):
    pass


class PasswordDidntMatched(MyBaseException):
    pass


class PasswordPatternMatchError(MyBaseException):
    pass


class UsernameDoesNotExistsError(MyBaseException):
    pass


class EmailDoesNotExistsError(MyBaseException):
    pass
