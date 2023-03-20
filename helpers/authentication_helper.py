from datetime import datetime, timedelta
from backend.settings import JwtConstants
import jwt
from hashlib import sha1
class AuthenticationHelper:
    def __init__(self, id):
        self.id = id
        self.token_secret = JwtConstants.SECRET_KEY
        self.algorithm = JwtConstants.JWT_ALGORITHM
        self.seconds = int(JwtConstants.JWT_EXPIRY_IN_SEC)

    def authentication(self,user,password):
        return user.password==sha1(password.encode()).hexdigest()

    def generate_access_token(self):
        try:
            payload = {
                'id': self.id.hex,
                'exp': datetime.utcnow() + timedelta(seconds=self.seconds)
            }

            return jwt.encode(payload, self.token_secret, algorithm=self.algorithm)
        except Exception as message:
            raise message