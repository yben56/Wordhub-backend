from django.utils.translation import gettext as _
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from ..models import Dictionary
from api.serializers.dictionary_serializers import DictionarySerializer

import json, os

@api_view(['GET'])
def word(request, word, wordid):
    try:
        word = Dictionary.objects.get(word=word, id=wordid)
        serializer = DictionarySerializer(word)

        data = serializer.data

        data['sentences'] = json.loads(data['sentences'])
        data['associate'] = json.loads(data['associate'])

        data['word_prounce'] = 'sounds/ding.mp3'
        data['probability'] = 6

        #evaluation (id, wordid, word, trials, correctness)
        data['evaluation'] = {}
        data['evaluation']['trials'] = 6
        data['evaluation']['correctness'] = 2
        data['evaluation']['accuracy'] = '{}%'.format(round((data['evaluation']['correctness'] / data['evaluation']['trials']) * 100))
        
        return Response({
            'error' : False,
            'message' : '',
            'data' : data
        }, status=200)
    
    except Dictionary.DoesNotExist:
        return Response({
            'error': True,
            'message': _('Page not found.'),
            'data': None
        }, status=404)