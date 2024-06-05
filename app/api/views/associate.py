from django.utils.translation import gettext as _
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from ..models import Dictionary
from api.serializers.search_serializers import SearchSerializer, AssociateSerializer
import json

from deep_translator import GoogleTranslator

@api_view(['GET'])
def associate(request, word):
    #1. translate to en
    word = GoogleTranslator(source='auto', target='en').translate(word)

    #2. to lowercase
    word = word.lower()

    #3. word
    dictionaries = Dictionary.objects.filter(word=word)
    serializer = AssociateSerializer(dictionaries, many=True)
    search = serializer.data

    #4. sort association by rating
    associate = {}
    for index in range(len(search)):
        associate.update(json.loads(search[index]['associate']))

    association = list(associate.keys())

    #5. remove associate == word
    association = [item for item in association if item != word]

    #6. page
    try:
        page = request.query_params.get('page', 1)
        page = int(page)
    except ValueError:
        page = 1

    #7. page index
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page

    #8. find words
    dictionaries = Dictionary.objects.filter(word__in=association[start:end])
    serializer = SearchSerializer(dictionaries, many=True)
    associate = serializer.data

    #9. merge associate with words in group
    output = []
    for item in association:
        output.append({
            'word': item,
            'word_prounce': '/sounds/ding.mp3',
            'result': []
        })

    for row in associate:
        for item in output:
            if row['word'] == item['word']:
                 item['result'].append(row)
    
    output = [item for item in output if item['result']]

    #10. output
    return Response({
        'error' : False,
        'message' : '',
        'data' : output
    }, status=200)