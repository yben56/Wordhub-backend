from datetime import datetime, timedelta
import jwt

def jwtoken(id, secret):
    payload = {
        'id' : id,
        'exp': datetime.utcnow() + timedelta(minutes=60),
        'iat': datetime.utcnow()
    }

    token = jwt.encode(payload, secret, algorithm='HS256')

    return token