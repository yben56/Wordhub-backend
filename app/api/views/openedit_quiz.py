from django.utils.translation import gettext as _
from django.conf import settings
from django.db import IntegrityError
from django.db import transaction
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import json

from ..models import Dictionary, Quiz
from api.serializers.quiz_serializers import QuizSerializer, QuizUpdateSerializer, QuizVersionSerializer

@api_view(['GET', 'PUT'])
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

def openedit_PUT(user_id, request, word, wordid):
    #1. validation body
    data = opedit_validation(request.body)

    if data['error']:
        return {
            'status' : status.HTTP_400_BAD_REQUEST,
            'body' : { 'error' : True, 'message' : data['message'] }
        }
    
    data = data['body']

    #2. check wordid exist (Must have word for add or update quiz)
    word = Dictionary.objects.filter(id=wordid).first()

    if not word:
        return {
            'status' : status.HTTP_400_BAD_REQUEST,
            'body' : {
                'error' : True,
                'message' : 'word not found, must have word before add or update quiz'
            }
        }

    #3. get data from db
    quiz = Quiz.objects.filter(dictionary_id=wordid).first()
    quiz_serializer = QuizSerializer(quiz)

    #4.
    if quiz:
        #UPDATE

        #5. check user update content or not
        sorted_data = sorted(data, key=lambda x: (x[0], x[1], x[2]))
        sorted_quiz = sorted(quiz_serializer.data['quiz'], key=lambda x: (x[0], x[1], x[2]))
        
        if sorted_data == sorted_quiz:
            return {
                'status' : status.HTTP_400_BAD_REQUEST,
                'body' : {
                    'error' : True,
                    'message' : 'update data == db data'
                }
            }

        #6. update quiz version
        quiz_version_serializer = QuizVersionSerializer(data={
            'dictionary' : quiz_serializer.data['dictionary'],
            'word' : quiz_serializer.data['word'],
            'quiz' : quiz_serializer.data['quiz'],
            'auther' : quiz_serializer.data['auther']
        })

        if not quiz_version_serializer.is_valid():
            return {
                'status': status.HTTP_404_NOT_FOUND,
                'body': {
                    'error': True, 
                    'message': quiz_version_serializer.errors
                }
            }

        #7. update quiz
        serializer = QuizUpdateSerializer(quiz, data={
            'dictionary' : quiz_serializer.data['dictionary'],
            'word' : quiz_serializer.data['word'],
            'quiz' : data,
            'auther' : user_id
        })

        if not serializer.is_valid():
            return {
                'status': status.HTTP_404_NOT_FOUND,
                'body': {
                    'error': True, 
                    'message': serializer.errors
                }
            }

        #8. transaction
        with transaction.atomic():
            quiz_version_serializer.save()
            serializer.save()

    else:
        #INSERT
        #9. insert quiz
        serializer = QuizUpdateSerializer(data={
            'dictionary': wordid,
            'word': word,
            'quiz': data,
            'auther': user_id
        })

        if not serializer.is_valid():
             return {
                'status': status.HTTP_400_BAD_REQUEST,
                'body': {
                    'error': True, 
                    'message': serializer.errors
                }
            }
        
        serializer.save()

    #10. output
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
    
    #3. check each items contain 3 elements
    for i, item in enumerate(body):
        if len(item) != 3:
            return { 'error' : True, 'message' : 'Each items required 3 elements' }

    #4. check elements format [str, str, boolean]
    for i, item in enumerate(body):
        if not isinstance(item[0], str) or not isinstance(item[1], str) or not isinstance(item[2], bool):
            return { 'error' : True, 'message' : 'Each elements required in [str, str, boolean] format' }

    #5. check item contain 1 ture 3 false
    true_count = 0
    for i, item in enumerate(body):
        if item[2]:
            true_count += 1

    if true_count != 1:
        return { 'error' : True, 'message' : 'item required 1 ture 3 false' }

    #6. out only fields we want
    return {
        'error' : False,
        'body' : body
    }