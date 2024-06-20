from django.utils.translation import gettext as _
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import os, json

from ..models import Dictionary
from api.serializers.dictionary_serializers import DictionarySerializer, DictionaryUpdateSerializer

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def openedit_quiz(request, word=None, wordid=None):
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
            'status' : status.HTTP_404_NOT_FOUND,
            'body' : {
                'error': True,
                'message': _('Page not found.')
            }
        }
            
    #3. output word
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
        data = data['body']

    #2. don't change word (it pair with id!!!)
    data['word'] = word

    #3. update
    try:
        fetchword = Dictionary.objects.get(word=word, id=wordid)
    except Dictionary.DoesNotExist:
        return {
            'status' : status.HTTP_404_NOT_FOUND,
            'body' : { 'error' : True, 'message' : _('Page not found.') }
        }
    serializer = DictionaryUpdateSerializer(fetchword, data=data)
    
    if not serializer.is_valid():
        return {
            'status' : status.HTTP_400_BAD_REQUEST,
            'body' : {
                'error' : False,
                'message' : serializer.errors
            }
        }

    serializer.save()

    #4. output
    return {
        'status' : status.HTTP_200_OK,
        'body' : {
            'error' : False,
            'message' : ''
        }
    }

def openedit_DELETE(user_id, request, word, wordid):

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
    
    #2. if missing field in body:
    if not all(key in body for key in ['translation', 'phonetic', 'pos', 'translation', 'sentences']):
        return { 'error' : True, 'message' : "body required: ['translation', 'phonetic', 'pos', 'translation', 'sentences']" }
    
    #3. check list
    if not type(body['classification']) is list:
        return { 'error' : True, 'message' : 'classification must be list' }

    if  not type(body['sentences']) is list:
        return { 'error' : True, 'message' : 'sentences must be list' }

    #4. load pos & classification json
    with open(os.path.join(settings.BASE_DIR, 'api/dictionarylist/', 'pos.json'), 'r', encoding='utf-8') as f:
        pos_list = json.load(f)

    with open(os.path.join(settings.BASE_DIR, 'api/dictionarylist/zh-tw/', 'classification.json'), 'r', encoding='utf-8') as f:
        classification_list = json.load(f)

    #5. check pos
    if body['pos'] not in pos_list:
       return { 'error' : True, 'message' : 'pos must from list we provided' }
    
    #6. check classification
    for classification in body['classification']:
        if classification not in classification_list:
            return { 'error' : True, 'message' : 'classification must from dict we provided' }
    
    #7. check sentences
    for sentence in body['sentences']:
        if not isinstance(sentence, dict):
            return { 'error' : True, 'message' : 'Invalid sentences format' }
        if 'en' not in sentence or 'zh' not in sentence:
            return { 'error' : True, 'message' : 'Invalid sentences format' }

    #8. out only fields we want
    return {
        'error' : False,
        'body' : {
            'translation' : body['translation'],
            'phonetic' : body['phonetic'],
            'pos' : body['pos'],
            'classification' : body['classification'],
            'sentences' : body['sentences']
        }
    }