from django.utils.translation import gettext as _
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import api_view

from ..models import AccessWord
from api.serializers.history_serializers import HistorySerializer

from django.db.models import Max, Min, OuterRef, Subquery
import json

@api_view(['GET', 'DELETE'])
def history(request):
    if request.method == 'GET':
        #1.
        data = history_get(request.user_id, request.query_params.get('word'), request.query_params.get('page', 1))
        
        #2.
        return Response({
            'error' : False,
            'message' : '',
            'data' : data
        }, status=200)
    
    if request.method == 'DELETE':
        deleted_count = history_delete(request.user_id, request.query_params.get('wordid'))

        if deleted_count == 0:
            return Response({
                'error' : True,
                'message' : f"wordid: '{request.query_params.get('wordid')}'' no records found."
            }, status=200)

        #4.
        return Response({
            'error' : False,
            'message' : ''
    }, status=200)

def history_get(user_id, word, page):
    #1. page
    try:
        page = int(page)
    except ValueError:
        page = 1

    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page

    #2. select newest row and group by dictionary_id
    query = AccessWord.objects.filter(user_id=user_id).values('dictionary_id').annotate(latest_date=Max('date'))

    if word:
        #3. user search specific word
        history = AccessWord.objects.filter(
            Q(user_id=user_id) & 
            Q(dictionary_id__in=query.values('dictionary_id')) & 
            Q(date__in=query.values('latest_date')) &
            Q(dictionary__word=word) | Q(dictionary__translation=word)
        ).order_by('-date')[start:end]
    else:
        #4. user search all words
        history = AccessWord.objects.filter(
            Q(user_id=user_id) &
            Q(dictionary_id__in=query.values('dictionary_id')) & 
            Q(date__in=query.values('latest_date'))
        ).order_by('-date')[start:end]

    serializer = HistorySerializer(history, many=True)
    data = serializer.data

    #5.
    return data

def history_delete(user_id, wordid):
    #1. wordid
    if wordid is None:
        return Response({
            'error' : True,
            'message' : 'wordid must required.'
        }, status=200)
    
    #2. wordid must int
    if not wordid.isdigit():
        return Response({
            'error' : True,
            'message' : 'wordid must be an integer.'
        }, status=200)

    #3. DELETE
    deleted_count, _ = AccessWord.objects.filter(user_id=user_id, dictionary_id=wordid).delete()

    return deleted_count