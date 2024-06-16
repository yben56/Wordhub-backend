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
    #1. pages
    pages = request.GET.get('pages')

    if pages is not None:
        try:
            pages = int(pages)
        except ValueError:
            return Response({
                'error' : True,
                'message' : 'Invalid Pages'
            }, status=status.HTTP_400_BAD_REQUEST)
    else:
        pages = 1 
    
    #2. select quiz
    word = Quiz.objects.order_by('?')[:pages]
    serializer = QuizSerializer(word, many=True)
    data = serializer.data

    #3. user mode (evaluation)
    if request.user_id:
        from ..utils import calculate_accuracy

        for index in range(len(data)):
            data[index]['evaluation'] = calculate_accuracy(request.user_id, data[index]['word'])
    

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
