from nexios.auth.middleware import AuthenticationMiddleware
from nexios.auth.backends import JWTAuthBackend
from .utils import get_user_from_payload

middleware = AuthenticationMiddleware(
    backend=JWTAuthBackend(
        authenticate_func=get_user_from_payload,   
    )
)