from django.utils.translation import gettext as _
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

import json

@api_view(['POST'])
def answer(request):
    
    user_id = request.user_id
    wordid = request.data['wordid']
    correct = request.data['correct']

    print(request.data)

    return Response({
        'error' : False,
        'message' : '',
        'data' : correct
    }, status=200)