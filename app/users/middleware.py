from django.http import JsonResponse
from rest_framework import status
import jwt, os

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