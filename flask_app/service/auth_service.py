import jwt
import datetime
from service.user_service import UserService


class AuthenticationService:
    def __init__(self, secret_key='tomas_o_trem', algorithm='HS256'):
        self.user_service = UserService()
        self.secret_key = secret_key
        self.algorithm = algorithm

    def authenticate_user(self, username, password):
        user = self.user_service.check_user_credentials(username, password)
        if user:
            token = self.generate_token(user)
            return token
        else:
            return None

    def generate_token(self, username):
        payload = {
            'user_name': username,
            'exp': datetime.datetime.now() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token

    def verify_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=self.algorithm)
            return payload
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False