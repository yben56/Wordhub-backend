from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..authentication import create_token, decode_token
import os

@api_view(['POST'])    
def refresh_token(request):

    #1.
    refresh_token = request.COOKIES.get('refresh_token')

    if not refresh_token:
        return Response({
            'error': True,
            'message': 'No refresh token'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    #2.
    decode = decode_token(refresh_token, os.environ.get('JWT_REFRESH_SECRET', 'JWT_REFRESHS_SECRET not found'))

    if decode['error']:
        response = Response({
            'error': True,
            'message': decode['message']
        }, status=status.HTTP_401_UNAUTHORIZED)
    
        response.delete_cookie(key='refresh_token', path='/')

        return response
      
    #3.
    access_token = create_token(decode['data']['user_id'], os.environ.get('JWT_ACCESS_SECRET', 'JWT_ACCESS_SECRET not found'))

    return Response({
        'error': False,
        'message': '',
        'data': {
            'access_token' : access_token['token'],
            'access_token_exp' : access_token['exp']
        }
    }, status=status.HTTP_200_OK)