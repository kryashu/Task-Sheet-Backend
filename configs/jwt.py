import os


class JWTConfig:
    USER_WEB_AUTH_API_SECRET = os.environ.get("USER_WEB_AUTH_API_SECRET", "USER_WEB_AUTH_API_SECRET")
    iv=os.environ.get("iv",b'0123456789abcdef')
