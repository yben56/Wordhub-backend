from django.utils.translation import gettext as _
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from app.helpers import postman
import json, os

@api_view(['GET'])
def word(request, word, wordid):




    data = open(os.getcwd() + '/api/database/Word.json', encoding='utf-8')
    response = json.load(data)

    #2. resposne
    return Response({
        'error' : False,
        'message' : '',
        'data' : response
    }, status=200)