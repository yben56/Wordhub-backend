from django.utils.translation import gettext as _
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from ..models import Dictionary,  Search
from api.serializers.search_serializers import SearchSerializer

from deep_translator import GoogleTranslator

@api_view(['GET'])
def search(request, text):
    #1. translate to en
    word = GoogleTranslator(source='auto', target='en').translate(text) 

    #2. to lowercase
    word = word.lower()

    #3. search
    dictionaries = Dictionary.objects.filter(word=word)
    serializer = SearchSerializer(dictionaries, many=True)
    search = serializer.data

    #4. if word exist in db
    if len(search):
        exist = True
    else:
        exist = False

    #5. search record
    if request.user_id:
        save_search = Search(user_id=request.user_id, search=text, word=word, exist=exist)
        save_search.save()

    #6.
    result = []

    if len(search):
        result = [{
            'word' : search[0]['word'],
            'heteronyms' : search[0]['heteronyms'],
            'result' : search
        }]

    #7. output
    return Response({
        'error' : False,
        'message' : '',
        'data' : result
    }, status=200)