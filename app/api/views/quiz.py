from django.utils.translation import gettext as _
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from ..models import Dictionary, Quiz
from api.serializers.dictionary_serializers import DictionarySerializer
from api.serializers.quiz_serializers import QuizSerializer

import json, os, random

@api_view(['GET'])
def quiz(request):
    #1
    #if not request.user_id:

    #select random 10 quiz
    word = Quiz.objects.order_by('?')[:10]
    serializer = QuizSerializer(word, many=True)
    data = serializer.data

    #data = data['quiz'].apply(shuffle)
    

    return Response({
        'error' : False,
        'message' : '',
        'data' : data
    }, status=200)
        
    #select random 10 quiz according to search & query
    

    #2. resposne
    return Response({
        'error' : False,
        'message' : '',
        'data' : response
    }, status=200)

def shuffle(row):
    return json.loads(row)
