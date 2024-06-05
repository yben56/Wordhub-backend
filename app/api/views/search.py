from django.utils.translation import gettext as _
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from ..models import Dictionary,  Search
from api.serializers.search_serializers import SearchSerializer

from deep_translator import GoogleTranslator

@api_view(['GET'])
def search(request, word):
    #1. translate to en
    word = GoogleTranslator(source='auto', target='en').translate(word) 

    #2. to lowercase
    word = word.lower()

    #3. search
    dictionaries = Dictionary.objects.filter(word=word)
    serializer = SearchSerializer(dictionaries, many=True)
    search = serializer.data

    #4. search record
    if len(search) and request.user_id:
        save_search = Search(user_id=request.user_id, search=word)
        save_search.save()

    #5.
    result = []

    if len(search):
        result = [{
            'word' : search[0]['word'],
            'word_prounce' : '/sounds/ding.mp3',
            'result' : search
        }]

    #6. output
    return Response({
        'error' : False,
        'message' : '',
        'data' : result
    }, status=200)