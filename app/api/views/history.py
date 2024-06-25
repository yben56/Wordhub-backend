from django.utils.translation import gettext as _
from rest_framework.response import Response
from rest_framework.decorators import api_view

from ..models import SearchWord
from api.serializers.history_serializers import HistorySerializer

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

    #2.
    if word:
        history = SearchWord.objects.filter(user_id=user_id, dictionary__word=word).order_by('-date')[start:end]
    else:
        history = SearchWord.objects.filter(user_id=user_id).order_by('-date')[start:end]

    serializer = HistorySerializer(history, many=True)
    data = serializer.data

    #3.
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
    deleted_count, _ = SearchWord.objects.filter(user_id=user_id, dictionary_id=wordid).delete()

    return deleted_count