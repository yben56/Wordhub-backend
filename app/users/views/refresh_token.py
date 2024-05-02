from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..authentication import create_access_token, decode_refresh_token

from ..models import User
from ..serializers import UserSerializer

from rest_framework.authentication import get_authorization_header
from ..authentication import decode_access_token, decode_refresh_token

@api_view(['POST'])    
def refresh_token(request):
    refresh_token = request.COOKIES.get('refresh_token')

    #1.
    if not refresh_token:
        return Response({
            'error' : True,
            'message' : 'Invalid token'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    #2.
    decode = decode_refresh_token(refresh_token)

    if decode['error']:
        return Response({
            'error': True,
            'message': decode['message']
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    #3.
    access_token = create_access_token(decode['data']['user_id'])

    return Response({
        'error': False,
        'message': '',
        'data': {
            'access_token' : access_token
        }
    }, status=status.HTTP_401_UNAUTHORIZED)