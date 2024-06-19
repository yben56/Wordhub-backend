from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.conf import settings
import os, json

@api_view(['GET'])
def dictionarylist(request, type):
    #1. headers accept-language
    headers = request.headers
    if 'Accept-Language' in headers:
        locale = headers['Accept-Language']
    else:
        locale = 'zh-tw'

    #2. file
    if ( type == 'pos'):
        file = os.path.join(settings.BASE_DIR, 'api/dictionarylist/', 'pos.json')
    else:
        file = os.path.join(settings.BASE_DIR, f'api/dictionarylist/{locale}/', 'classification.json')
    
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return Response(data, status.HTTP_200_OK)

    except FileNotFoundError:
        raise Exception("File not found")
    except json.JSONDecodeError:
        raise Exception("Error decoding JSON")