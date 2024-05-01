from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..models import User
from ..serializers import UserSerializer

from rest_framework.authentication import get_authorization_header
from ..authentication import decode_access_token, decode_refresh_token

@api_view(['GET'])    
def user(request):
    user_id = request.user_id

    return Response({
        'error' : False,
        'message' : '',
        'data' : {'user_id' : user_id}
    }, status=status.HTTP_200_OK)