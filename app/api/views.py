from django.utils.translation import gettext as _
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from app.helpers import postman
import json, os

@api_view(['GET'])
def words(request):
    #1. api
    #response = postman('GET', 'http://localhost:3000/database/Words.json')

    data = open(os.getcwd() + '/api/database/Words.json', encoding='utf-8')
    response = json.load(data)

    #2. resposne
    return Response({
        'error' : False,
        'message' : '',
        'data' : response
    }, status=200)

@api_view(['GET'])
def search(request):
    #1. api
    #response = postman('GET', 'http://localhost:3000/database/Search.json')

    data = open(os.getcwd() + '/api/database/Search.json', encoding='utf-8')
    response = json.load(data)

    #2. resposne
    return Response({
        'error' : False,
        'message' : '',
        'data' : response
    }, status=200)

@api_view(['GET'])
def word(request):
    #1. api
    #response = postman('GET', 'http://localhost:3000/database/Word.json')

    data = open(os.getcwd() + '/api/database/Word.json', encoding='utf-8')
    response = json.load(data)

    #2. resposne
    return Response({
        'error' : False,
        'message' : '',
        'data' : response
    }, status=200)


@api_view(['GET'])
def quizs(request):
    #1. api
    #response = postman('GET', 'http://localhost:3000/database/Quizs.json')

    data = open(os.getcwd() + '/api/database/Quizs.json', encoding='utf-8')
    response = json.load(data)

    #2. resposne
    return Response({
        'error' : False,
        'message' : '',
        'data' : response
    }, status=200)