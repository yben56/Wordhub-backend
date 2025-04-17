from datetime import datetime, timedelta
from calendar import timegm
import jwt

def create_token(id, password, t=1):
    now = datetime.utcnow()
    exp = now + timedelta(minutes=int(t))

    token = jwt.encode({
        'user_id': id,
        'exp': timegm(exp.timetuple()),
        'iat': timegm(now.timetuple())
    }, password, algorithm='HS256')

    return {
        'token' : token,
        'exp' : timegm(exp.timetuple())
    }

def decode_token(token, password):
    try:
        payload = jwt.decode(token, password, algorithms=['HS256'], options={"verify_exp": False})

        if payload['exp'] < int(datetime.utcnow().timestamp()):
            raise jwt.ExpiredSignatureError()

        return {
            'error' : False,
            'message' : '',
            'data' : {'user_id' : payload['user_id']}
        }
    except jwt.ExpiredSignatureError:
        return {
            'error': True,
            'message': 'Token expired'
        }
    except jwt.InvalidTokenError:
        return {
            'error': True,
            'message': 'Invalid token'
        }
    except Exception as e:
        return {
            'error': True,
            'message': str(e)
        }