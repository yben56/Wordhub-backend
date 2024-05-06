from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..authentication import create_token, decode_token
import os

@api_view(['POST'])    
def refresh_token(request):

    #1.
    if request.COOKIES.get('refresh_token'):
        refresh_token = request.COOKIES.get('refresh_token')
    elif 'Authorization' in request.headers and request.headers['Authorization'].startswith('Bearer '):
        refresh_token = request.headers['Authorization'].split(' ')[1]
    else:
        return Response({
            'error' : True,
            'message' : 'Invalid token'
        }, status=status.HTTP_401_UNAUTHORIZED)

    #2.
    decode = decode_token(refresh_token, os.environ.get('JWT_REFRESH_SECRET', 'JWT_REFRESHS_SECRET not found'))

    if decode['error']:
        return Response({
            'error': True,
            'message': decode['message']
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    #3.
    access_token = create_token(decode['data']['user_id'], os.environ.get('JWT_ACCESS_SECRET', 'JWT_ACCESS_SECRET not found'))

    return Response({
        'error': False,
        'message': '',
        'data': {
            'access_token' : access_token['token'],
            'access_token_exp' : access_token['exp']
        }
    }, status=status.HTTP_401_UNAUTHORIZED)