from django.http import JsonResponse
from rest_framework import status
from rest_framework.authentication import get_authorization_header
from .authentication import decode_access_token

class AuthenticationMiddleware:
    def __init__(self, get_response, optional=False):
        self.get_response = get_response
        self.optional = optional

    def __call__(self, request):
        #1. get header
        auth = get_authorization_header(request).split()

        #2. optional authentication (access_token optional)
        if self.optional and not auth:
            request.user_id = False

            response = self.get_response(request)
            return response

        #3. Authentication
        if not auth or len(auth) != 2:
            return self.unauthenticated_response()
        
        #4. decode
        token = auth[1].decode('utf-8')
        decode = decode_access_token(token)

        #5. error
        if decode['error']:
            return self.unauthenticated_response(message=decode['message'])

        #6. user_id
        request.user_id = decode['data']['user_id']

        #7.
        response = self.get_response(request)
        return response

    def unauthenticated_response(self, message='unauthenticated'):
        return JsonResponse({
            'error': True,
            'message': message
        }, status=status.HTTP_401_UNAUTHORIZED)