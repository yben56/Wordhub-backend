from django.utils.translation import gettext as _
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from ..models import Dictionary
from api.serializers.dictionary_serializers import DictionarySerializer

import json, os

@api_view(['GET'])
def words(request):
    #1. pages
    pages = request.GET.get('pages')

    if pages is not None:
        try:
            pages = int(pages)
        except ValueError:
            return Response({
                'error' : True,
                'message' : 'Invalid Pages'
            }
            , status=status.HTTP_400_BAD_REQUEST)
    else:
        pages = 9 

    #2. guest mode
    if request.user_id:
        data = []
    else:
        words = Dictionary.objects.exclude(pos__in=['abbreviation', 'interrogative']).order_by('?')[:pages]
        serializer = DictionarySerializer(words, many=True)
        data = serializer.data

        for index in range(len(data)):
            data[index]['probability'] = 6

            #3. evaluation (id, wordid, word, trials, correctness)
            if request.user_id:
                data[index]['evaluation'] = {}
                data[index]['evaluation']['trials'] = 6
                data[index]['evaluation']['correctness'] = 2
                data[index]['evaluation']['accuracy'] = '{}%'.format(round((data[index]['evaluation']['correctness'] / data[index]['evaluation']['trials']) * 100))

    #2. resposne
    return Response({
        'error' : False,
        'message' : '',
        'data' : data
    }, status=200)