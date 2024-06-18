from django.utils.translation import gettext as _
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from ..models import Dictionary, SearchWord
from api.serializers.dictionary_serializers import DictionarySerializer

import json

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def openedit(request, word=None, wordid=None):
    #1. method
    method_name = f"openedit_{request.method}"
    method = globals().get(method_name, openedit_GET)

    #2. user_id
    user_id = request.user_id
    
    #3. POST (add new word)
    if word is None and wordid is None:
        output = method(user_id, request)
    
    #4. GET, PUT, DELETE
    output = method(user_id, request, word, wordid)

    return Response(output['body'], status=output['status'])

def openedit_GET(user_id, request, word, wordid):
    try:
        #1. fetch
        fetchword = Dictionary.objects.get(word=word, id=wordid)
        serializer = DictionarySerializer(fetchword)
        data = serializer.data

    except Dictionary.DoesNotExist:
        #2. if no match
        return {
            'status' : 404,
            'body' : {
                'error': True,
                'message': _('Page not found.')
            }
        }
            
    #3. output word
    return {
        'status' : 200,
        'body' : {
            'error' : False,
            'message' : '',
            'data' : data
        }
    }

def openedit_POST(user_id, request):

    return {
        'error' : False,
        'message' : '',
        'data' : user_id
    }

def openedit_PUT(user_id, request, word, wordid):

    return {
        'status' : 200,
        'body' : {
            'error' : False,
            'message' : '',
            'data' : json.loads(request.body)
        }
    }

def openedit_DELETE(user_id, request, word, wordid):

    return {
        'status' : 200,
        'body' : {
            'error' : False,
            'message' : ''
        }
    }