import jwt
import datetime
from config import settings
from functools import wraps
def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, settings.AUTH_SECRET, algorithms='HS256')
        return payload['sub']
    except Exception as e:
        print(e)
    except jwt.ExpiredSignatureError:
        return 'Signature Expired Please re-login'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please re-login'

def encode_auth_token(user_id):
    try:
        payload = {
            'exp':datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=0),
            'iat':datetime.datetime.utcnow(),
            'sub':user_id
        }
        return jwt.encode(
            payload,
            settings.AUTH_SECRET,
            algorithm='HS256'
        )
    except Exception as e:
        return e

def jwt_required(token):
    return False

def jwt_required_wrap(token):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            jwt_required(token)
            return fn(*args, **kwargs)
        return decorator
    return wrapper