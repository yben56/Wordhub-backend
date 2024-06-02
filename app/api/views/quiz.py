from django.utils.translation import gettext as _
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from ..models import Quiz
from api.serializers.quiz_serializers import QuizSerializer

import json, os, random

@api_view(['GET'])
def quiz(request):
    
    '''
    wordid = random.randint(1, 42189)
   
    word = Quiz.objects.get(wordid=wordid)
    serializer = QuizSerializer(word)

    data = serializer.data

    return Response({
        'error' : False,
        'message' : '',
        'data' : data
    }, status=200)
    '''

    data = open(os.getcwd() + '/api/database/Quizs.json', encoding='utf-8')
    response = json.load(data)

    #2. resposne
    return Response({
        'error' : False,
        'message' : '',
        'data' : response
    }, status=200)