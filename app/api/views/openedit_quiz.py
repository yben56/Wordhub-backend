from django.utils.translation import gettext as _
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import os, json

from ..models import Quiz
from api.serializers.quiz_serializers import QuizSerializer

@api_view(['GET', 'POST', 'PUT'])
def openedit_quiz(request, word=None, wordid=None):
    #1. method
    method_name = f"openedit_{request.method}"
    method = globals().get(method_name, openedit_GET)

    #2. user_id
    user_id = request.user_id
    
    #3. POST (add new word)
    if word is None and wordid is None:
        output = method(user_id, request)
    
    #4. GET, PUT
    output = method(user_id, request, word, wordid)

    return Response(output['body'], status=output['status'])

def openedit_GET(user_id, request, word, wordid):

    try:
        #1. fetch
        fetchword = Quiz.objects.get(word=word, dictionary_id=wordid)
        serializer = QuizSerializer(fetchword)
        data = serializer.data

    except Quiz.DoesNotExist:
        #2. if no match
        return {
            'status' : status.HTTP_404_NOT_FOUND,
            'body' : {
                'error': True,
                'message': _('Page not found.')
            }
        }
    
    #3. output quiz
    return {
        'status' : status.HTTP_200_OK,
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
    #1. validation body
    data = opedit_validation(request.body)

    if data['error']:
        return {
            'status' : status.HTTP_400_BAD_REQUEST,
            'body' : { 'error' : True, 'message' : data['message'] }
        }
    else:
        data = json.dumps(data['body'], ensure_ascii=False)

    #2. update
    try:
        Quiz.objects.filter(word=word, dictionary_id=wordid).update(quiz=data)
    except Quiz.DoesNotExist:
        return {
            'status' : status.HTTP_404_NOT_FOUND,
            'body' : { 'error' : True, 'message' : _('Page not found.') }
        }
    
    #3. output
    return {
        'status' : status.HTTP_200_OK,
        'body' : {
            'error' : False,
            'message' : ''
        }
    }

def opedit_validation(body):
    #1. check request body
    try:
        body = json.loads(body)
    except json.JSONDecodeError as e:
        return { 'error' : True, 'message' : 'Invalid JSON format' }
    except Exception as e:
        return { 'error' : True, 'message' : str(e) }
    
    #2. check elements
    if len(body) != 4:
        return { 'error' : True, 'message' : 'Array required 4 elements' }

    #3. out only fields we want
    return {
        'error' : False,
        'body' : body
    }