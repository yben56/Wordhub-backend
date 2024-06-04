from django.utils.translation import gettext as _
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from ..models import Dictionary
from api.serializers.search_serializers import SearchSerializer, AssociateSerializer
import json, os

@api_view(['GET'])
def associate(request, word):
    word = word.lower()
    
    #1. word
    dictionaries = Dictionary.objects.filter(word=word)
    serializer = AssociateSerializer(dictionaries, many=True)
    search = serializer.data

    #2. sort association by rating
    associate = {}
    for index in range(len(search)):
        associate.update(json.loads(search[index]['associate']))

    association = list(associate.keys())

    #3. remove associate == word
    association = [item for item in association if item != word]

    #4. page
    try:
        page = request.query_params.get('page', 1)
        page = int(page)
    except ValueError:
        page = 1

    #5. page index
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page

    #6. find words
    dictionaries = Dictionary.objects.filter(word__in=association[start:end])
    serializer = SearchSerializer(dictionaries, many=True)
    associate = serializer.data

    #7. merge associate with words in group
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

    #8. output
    return Response({
        'error' : False,
        'message' : '',
        'data' : output
    }, status=200)