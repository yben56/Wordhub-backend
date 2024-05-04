from datetime import datetime, timedelta
import jwt

def create_token(id, password, t=1):
    exp = datetime.utcnow() + timedelta(hours=t)
    token = jwt.encode({
        'user_id' : id,
        'exp': exp,
        'iat': datetime.utcnow()
    }, password, algorithm='HS256')

    return {
        'token' : token,
        'exp' : exp
    }

def decode_token(token, password):
    try:
        payload = jwt.decode(token, password, algorithms='HS256')

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