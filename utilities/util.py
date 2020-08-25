from flask import request
from application.utilities.flask import APIError
from http import HTTPStatus

def required_params(params):
    def wrapper(func):
        def inner(*args, **kwargs):
            parsed_json = request.get_json()
            for param in params:
                if param not in parsed_json:
                    return APIError(
                        message=f"{param} is required", status=HTTPStatus.BAD_REQUEST
                    )
                kwargs.update({param: parsed_json[param]})
            return func(*args, **kwargs)

        inner.__name__ = func.__name__
        return inner

    return wrapper
