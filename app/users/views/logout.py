from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])    
def logout(request):
    response = Response({
        'error' : False,
        'message' : ''
    }, status=status.HTTP_200_OK)

    response.delete_cookie(key='refresh_token')
    
    return response