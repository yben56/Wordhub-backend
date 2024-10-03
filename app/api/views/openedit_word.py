from django.utils.translation import gettext as _
from django.conf import settings
from django.db import transaction
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import os, json

from ..models import Dictionary
from api.serializers.dictionary_serializers import DictionarySerializer, DictionaryUpdateSerializer, DictionaryPostSerializer, DictionaryVersionSerializer

from text_to_speech import save

@api_view(['GET', 'POST', 'PUT'])
def openedit_word(request, word=None, wordid=None):
    #1. method
    method_name = f"openedit_{request.method}"
    method = globals().get(method_name, openedit_GET)

    #2. user_id
    user_id = request.user_id
    
    #3. POST (add new word)
    if request.method == 'POST':
        output = method(user_id, request)
    else:
        #4. GET, PUT
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

    #1. validation
    data = opedit_validation(request.body)

    if data['error']:
        return {
            'status' : status.HTTP_400_BAD_REQUEST,
            'body' : { 'error' : True, 'message' : data['message'] }
        }
    else:
        data = data['body']
    
    #2. check 'word & pos & translation' db exist
    exists = Dictionary.objects.filter(word=data['word'], pos=data['pos'], translation=data['translation']).exists()

    if exists:
        return {
            'status' : status.HTTP_409_CONFLICT,
            'body' : { 'error' : True, 'message' : _('Word already exist.') }
        }

    #3.
    serializer = DictionaryPostSerializer(data={
        'word' : data['word'],
        'translation' : data['translation'],
        'phonetic' : data['phonetic'],
        'pos' : data['pos'],
        'classification' : data['classification'],
        'sentences' : data['sentences'],
        'auther' : user_id
    })

    if not serializer.is_valid():
        return {
            'status' : status.HTTP_400_BAD_REQUEST,
            'body' : { 'error' : True, 'message' : serializer.errors }
        }

    instance = serializer.save()

    last_insert_id = instance.id

    #4. Pronounce
    pronounce_path = os.environ.get('PRONOUNCE_PATH', 'PRONOUNCE_PATH not found')
    filename = f"{pronounce_path}/{data['word']}.mp3"
    save(data['word'], 'en', file=filename)
    
    return {
        'status' : status.HTTP_200_OK,
        'body' : {
            'error' : False,
            'message' : '',
            'data' : {
                'wordid' : last_insert_id,
                'word' : data['word']
            }
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
    else:
        data = data['body']
    
    #2. don't change word (it pair with id!!!)
    data['word'] = word

    #3. get db data
    try:
        fetchword = Dictionary.objects.get(word=word, id=wordid, deleted=False)
    except Dictionary.DoesNotExist:
        return {
            'status' : status.HTTP_404_NOT_FOUND,
            'body' : { 'error' : True, 'message' : _('Page not found.') }
        }
    
    serializer = DictionarySerializer(fetchword)
    dbdata = serializer.data

    #4. check user update content or not
    if all(data[key] == dbdata[key] for key in ['word', 'translation', 'phonetic', 'pos', 'classification', 'sentences']):
        return {
            'status' : status.HTTP_400_BAD_REQUEST,
            'body' : {
                'error' : True,
                'message' : _('update data is the same as database')
            }
        }

    #5. dictionary version serializer
    version_serializer = DictionaryVersionSerializer(data={
        'dictionary' : dbdata['id'],
        'word' : dbdata['word'],
        'phonetic' : dbdata['phonetic'],
        'heteronyms' : dbdata['heteronyms'],
        'pos' : dbdata['pos'],
        'translation' : dbdata['translation'],
        'sentences' : dbdata['sentences'],
        'associate' : dbdata['associate'],
        'classification' : dbdata['classification'],
        'auther' : dbdata['auther'],
        'date' : dbdata['date'],
    })

    if not version_serializer.is_valid():
        return {
            'status' : status.HTTP_400_BAD_REQUEST,
            'body' : {
                'error' : True,
                'message' : version_serializer.errors
            }
        }

    #6. dictionary serializer
    serializer = DictionaryUpdateSerializer(fetchword, data={
        'translation' : data['translation'],
        'phonetic' : data['phonetic'],
        'pos' : data['pos'],
        'classification' : data['classification'],
        'sentences' : data['sentences'],
        'auther' : user_id
    })
    
    if not serializer.is_valid():
        return {
            'status' : status.HTTP_400_BAD_REQUEST,
            'body' : {
                'error' : True,
                'message' : serializer.errors
            }
        }

    with transaction.atomic():
        version_serializer.save()
        serializer.save()

    #7. output
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
    if not all(key in body for key in ['word', 'translation', 'phonetic', 'pos', 'translation', 'sentences']):
        return { 'error' : True, 'message' : "body required: ['translation', 'phonetic', 'pos', 'translation', 'sentences']" }
    
    #3. check word & translation not null
    if body['word'] == '' or body['translation'] == '':
        return { 'error' : True, 'message' : "word & translation must not null" }
    
    #4. check list
    if not type(body['classification']) is list:
        return { 'error' : True, 'message' : 'classification must be list' }

    if  not type(body['sentences']) is list:
        return { 'error' : True, 'message' : 'sentences must be list' }

    #5. load pos & classification json
    with open(os.path.join(settings.BASE_DIR, 'api/dictionarylist/', 'pos.json'), 'r', encoding='utf-8') as f:
        pos_list = json.load(f)

    with open(os.path.join(settings.BASE_DIR, 'api/dictionarylist/zh-tw/', 'classification.json'), 'r', encoding='utf-8') as f:
        classification_list = json.load(f)
    
    #6. check pos
    if body['pos'] not in pos_list:
       return { 'error' : True, 'message' : 'pos must from list we provided' }
    
    #7. check classification
    '''
    for classification in body['classification']:
        if classification not in classification_list:
            return { 'error' : True, 'message' : 'classification must from dict we provided' }
    '''
    
    #8. check sentences
    for sentence in body['sentences']:
        if not isinstance(sentence, dict):
            return { 'error' : True, 'message' : 'Invalid sentences format' }
        if 'en' not in sentence or 'zh' not in sentence:
            return { 'error' : True, 'message' : 'Invalid sentences format' }
     
    #9. out only fields we want
    return {
        'error' : False,
        'body' : {
            'word' : body['word'],
            'translation' : body['translation'],
            'phonetic' : body['phonetic'],
            'pos' : body['pos'],
            'classification' : body['classification'],
            'sentences' : body['sentences']
        }
    }