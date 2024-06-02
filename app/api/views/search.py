from django.utils.translation import gettext as _
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from ..models import Dictionary
from api.serializers.search_serializers import SearchSerializer
import json, os

@api_view(['GET'])
def search(request, word):
    
    #word
    dictionaries = Dictionary.objects.filter(word=word)
    serializer = SearchSerializer(dictionaries, many=True)
    search = serializer.data

    for index in range(len(search)):
        search[index]['word_prounce'] = 'sounds/ding.mp3'
        search[index]['probability'] = 6

        search[index]['evaluation'] = {}
        search[index]['evaluation']['trials'] = 6
        search[index]['evaluation']['correctness'] = 2
        search[index]['evaluation']['accuracy'] = '{}%'.format(round((search[index]['evaluation']['correctness'] / search[index]['evaluation']['trials']) * 100))
    
    #associate
    associate = {}
    for index in range(len(search)):
        associate.update(json.loads(search[index]['associate']))

    associate = sorted(associate, key=associate.get, reverse=True)

    dictionaries = Dictionary.objects.filter(word__in=associate[0:10])
    serializer = SearchSerializer(dictionaries, many=True)
    associate = serializer.data

    for index in range(len(associate)):
        associate[index]['word_prounce'] = 'sounds/ding.mp3'
        associate[index]['probability'] = 6

        associate[index]['evaluation'] = {}
        associate[index]['evaluation']['trials'] = 6
        associate[index]['evaluation']['correctness'] = 2
        associate[index]['evaluation']['accuracy'] = '{}%'.format(round((associate[index]['evaluation']['correctness'] / associate[index]['evaluation']['trials']) * 100))

    #remove associate from dict
    search = [{k: v for k, v in d.items() if k != "associate"} for d in search]
    associate = [{k: v for k, v in d.items() if k != "associate"} for d in associate]

    return Response({
        'error' : False,
        'message' : '',
        'data' : {
            'search' : search,
            'associate': associate
        }
    }, status=200)