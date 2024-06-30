from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from ..models import Dictionary, SearchGuest, SearchWords
from api.serializers.search_serializers import SearchSerializer

from deep_translator import GoogleTranslator
from elasticsearch_dsl.query import MultiMatch
from ..documents import WordDocument

@api_view(['GET'])
def search(request, text):

    #1. to lowercase
    text = text.lower()

    #2. translate to en
    word = GoogleTranslator(source='auto', target='en').translate(text) 

    #3. search
    dictionaries = Dictionary.objects.filter(word=word, deleted=False)
    serializer = SearchSerializer(dictionaries, many=True)
    search = serializer.data

    #4. if word exist in db
    if len(search):
        exist = True
    else:
        exist = False

    #5. search record
    if request.user_id:
        #user mode
        save_search = SearchWords(user_id=request.user_id, search=text, word=word, exist=exist)
        save_search.save()
    else:
        #guest mode
        save_search = SearchGuest(search=text, word=word, exist=exist)
        save_search.save()

    #6.
    result = []
    es = False

    if len(search):
        #normal query
        result = [{
            'word' : search[0]['word'],
            'heteronyms' : 0,
            'result' : search
        }]
    else:
        #elasticsearch
        es = True

        query = MultiMatch(query=text, fields=['word', 'translation'], fuzziness='1', minimum_should_match='80%')
        search = WordDocument.search().query(query)[0:3]
        data = search.execute()
        data = [hit.to_dict() for hit in data]

        for item in data:
            result.append({
                'word' : item['word'],
                'heteronyms' : item['heteronyms'],
                'result' : [{
                    'id' : item['id'],
                    'word' : item['word'],
                    'pos' : item['pos'],
                    'translation' : item['translation']
                }]
            })

    #7. output
    return Response({
        'error' : False,
        'message' : '',
        'elasticsearch' : es,
        'data' : result
    }, status=status.HTTP_200_OK)