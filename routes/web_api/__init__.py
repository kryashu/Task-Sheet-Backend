from functools import wraps
from http import HTTPStatus

import jwt
from flask import request

from application.configs.jwt import JWTConfig
from application.models.users import User
from application.utilities.flask import APIError


def consumer_web_api_check(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        authorization = request.headers.get("Authorization")
        if not authorization:
            return APIError(message="Un-Authorized", status=HTTPStatus.UNAUTHORIZED)

        try:
            bearer, auth_token = authorization.split()
            if not auth_token:
                return APIError(message="Un-Authorized", status=HTTPStatus.UNAUTHORIZED)
            payload = jwt.decode(auth_token, JWTConfig.USER_WEB_AUTH_API_SECRET)
        except Exception as e:
            return APIError(message="Un-Authorized", status=HTTPStatus.UNAUTHORIZED)
        user = User.get(id=payload["user_id"])
        if not user:
            return APIError(message="Un-Authorized", status=HTTPStatus.UNAUTHORIZED)
        request.data = {"auth_user": user}
        return f(*args, **kwargs)
    return decorated_function
