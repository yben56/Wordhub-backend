from rest_framework import exceptions
from datetime import datetime, timedelta
import jwt, os

def create_access_token(id):
    return jwt.encode({
        'user_id' : id,
        'exp': datetime.utcnow() + timedelta(minutes=60),
        'iat': datetime.utcnow()
    }, os.environ.get('JWT_ACCESS_SECRET', 'JWT_ACCESS_SECRET not found'), algorithm='HS256')

def decode_access_token(token):
    try:
        payload = jwt.decode(token, os.environ.get('JWT_ACCESS_SECRET', 'JWT_ACCESS_SECRET not found'), algorithms='HS256')

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
    
def create_refresh_token(id):
    return jwt.encode({
        'user_id' : id,
        'exp': datetime.utcnow() + timedelta(days=30),
        'iat': datetime.utcnow()
    }, os.environ.get('JWT_REFRESH_SECRET', 'JWT_REFRESH_SECRET not found'), algorithm='HS256') 

def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, os.environ.get('JWT_REFRESH_SECRET', 'JWT_REFRESH_SECRET not found'), algorithms='HS256')

        return {
            'error' : False,
            'message' : '',
            'data' : payload['user_id']
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