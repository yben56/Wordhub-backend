from django.http import JsonResponse
from rest_framework import status
from rest_framework.authentication import get_authorization_header
from .authentication import decode_access_token

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        #1.
        auth = get_authorization_header(request).split()

        if not auth or len(auth) != 2:
            return self.unauthenticated_response()
        
        #2. decode
        token = auth[1].decode('utf-8')
        decode = decode_access_token(token)

        #3. error
        if decode['error']:
            return self.unauthenticated_response(message=decode['message'])

        request.user_id = decode['data']['user_id']

        response = self.get_response(request)
        return response

    def unauthenticated_response(self, message='unauthenticated'):
        return JsonResponse({
            'error': True,
            'message': message
        }, status=status.HTTP_401_UNAUTHORIZED)





'''
class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            return JsonResponse({'error' : 'Unauthenticated'}, status=403)
    
        try:
            #1. decode
            secret = os.environ.get('JWT_ENCRYPT_SECRET', 'JWT_ENCRYPT_SECRET not found')
            payload = jwt.decode(token, secret, algorithms=['HS256'])

            #2. save user id after decode
            request.userinfo = payload
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error' : 'Token expired'}, status=403)
        except jwt.DecodeError:
            return JsonResponse({'error' : 'Invalid token'}, status=403)

        response = self.get_response(request)
        return response

class UserIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get('jwt')

        if token:
            try:
                #1. decode
                secret = os.environ.get('JWT_ENCRYPT_SECRET', 'JWT_ENCRYPT_SECRET not found')
                payload = jwt.decode(token, secret, algorithms=['HS256'])

                #2. save user id after decode
                request.userinfo = payload
            except jwt.ExpiredSignatureError:
                return JsonResponse({'error' : 'Token expired'}, status=403)
            except jwt.DecodeError:
                return JsonResponse({'error' : 'Invalid token'}, status=403)
        else:
            request.userinfo = {
                'id' : False,
                'exp': False,
                'iat': False
            }
        
        response = self.get_response(request)
        return response
'''