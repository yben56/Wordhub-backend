from django.utils.translation import gettext as _
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from ..models import Dictionary, SearchWord
from api.serializers.dictionary_serializers import DictionarySerializer

import json, os

@api_view(['GET'])
def word(request, word, wordid):
    try:
        #1. fetch
        word = Dictionary.objects.get(word=word, id=wordid)
        serializer = DictionarySerializer(word)
        data = serializer.data

        #2. if no match
        if not len(data):
            return Response({
                'error': True,
                'message': _('Page not found.'),
                'data': None
            }, status=404)

        #3. user mode only
        if request.user_id:
            #4. create
            obj, created = SearchWord.objects.update_or_create(
                user_id=request.user_id, word_id=wordid,
                defaults={'date': timezone.now()},
            )

            #5. update
            if not created:
                obj.count += 1
                obj.date = timezone.now()
                obj.save()

        #6.
        data['probability'] = 6

        #7. evaluation (id, wordid, word, trials, correctness)
        if request.user_id:
            data['evaluation'] = {}
            data['evaluation']['trials'] = 6
            data['evaluation']['correctness'] = 2
            data['evaluation']['accuracy'] = '{}%'.format(round((data['evaluation']['correctness'] / data['evaluation']['trials']) * 100))
        
        #8. output
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