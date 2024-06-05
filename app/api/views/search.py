from django.utils.translation import gettext as _
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from ..models import Dictionary
from api.serializers.search_serializers import SearchSerializer

from deep_translator import GoogleTranslator

@api_view(['GET'])
def search(request, word):
    #1. to lowercase
    word = word.lower()
    
    #2. translate to en
    word = GoogleTranslator(source='auto', target='en').translate(word) 

    #3. search
    dictionaries = Dictionary.objects.filter(word=word)
    serializer = SearchSerializer(dictionaries, many=True)
    search = serializer.data

    #4.
    if len(search):
        save_word_into_db = 1

    result = []

    if len(search):
        result = [{
            'word' : search[0]['word'],
            'word_prounce' : '/sounds/ding.mp3',
            'result' : search
        }]

    #4. output
    return Response({
        'error' : False,
        'message' : '',
        'data' : result
    }, status=200)