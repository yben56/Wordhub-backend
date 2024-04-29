from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['DELETE'])    
def logout(request):
    response = Response({
        'error' : False,
        'message' : ''
    }, status=status.HTTP_200_OK)

    #Remove record from db

    response.delete_cookie('jwt')
    
    return response