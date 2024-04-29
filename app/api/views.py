from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from app.helpers import postman
from django.utils.translation import gettext as _

@api_view(['GET'])
def words(request):
    #1. api
    response = postman('GET', 'http://localhost:3000/database/Words.json')

    #2. resposne
    return Response({
        'error' : False,
        'message' : '',
        'data' : response['body']
    }, status=response['status'])

@api_view(['GET'])
def search(request):
    #1. api
    response = postman('GET', 'http://localhost:3000/database/Search.json')

    #2. resposne
    return Response({
        'error' : False,
        'message' : '',
        'data' : response['body']
    }, status=response['status'])

@api_view(['GET'])
def word(request):
    #1. api
    response = postman('GET', 'http://localhost:3000/database/Word.json')

    #2. resposne
    return Response({
        'error' : False,
        'message' : '',
        'data' : response['body']
    }, status=response['status'])

@api_view(['GET'])
def quizs(request):
    #1. api
    response = postman('GET', 'http://localhost:3000/database/Quizs.json')

    #2. resposne
    return Response({
        'error' : False,
        'message' : '',
        'data' : response['body']
    }, status=response['status'])

@api_view(['GET'])
def homonyms(request):
    #1. api
    response = postman('GET', 'http://localhost:3000/database/Homonyms.json')

    #2. resposne
    return Response({
        'error' : False,
        'message' : '',
        'data' : response['body']
    }, status=response['status'])

@api_view(['GET'])
def homophones(request):
    #1. api
    response = postman('GET', 'http://localhost:3000/database/Homophones.json')

    #2. resposne
    return Response({
        'error' : False,
        'message' : '',
        'data' : response['body']
    }, status=response['status'])

@api_view(['GET'])
def connectapi_lock(request):
    return Response({
        'error' : False,
        'message' : '',
        'data' : {
            'user_id' : request.userinfo['id']
        }
    }, status=status.HTTP_200_OK)