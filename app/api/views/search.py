from django.utils.translation import gettext as _
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from ..models import Dictionary
from api.serializers.search_serializers import SearchSerializer
import json, os

@api_view(['GET'])
def search(request, word):
    #1. search
    dictionaries = Dictionary.objects.filter(word=word)
    serializer = SearchSerializer(dictionaries, many=True)
    search = serializer.data

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