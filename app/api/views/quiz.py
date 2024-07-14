from django.utils.translation import gettext as _
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from ..models import Quiz
from api.serializers.quiz_serializers import QuizSerializer
from ..utils import calculate_accuracy

import pandas as pd
import json, ast

@api_view(['GET'])
def quiz(request):
    #1. items
    try:
        items = int(request.GET.get('items', 3))
    except ValueError:
        return Response({'error': True, 'message' : 'items be an integer'}, status=400)
    
    if request.user_id:
        #3. get recommand list
        recommand = request.GET.get('recommand', [])

        if len(recommand) != 0:
            try:
                recommand = ast.literal_eval(recommand)
            except (SyntaxError, ValueError) as e:
                return Response({'error': True, 'message' : 'recommand must be a list'}, status=400)
        
        #4. prevent recommand redundant
        if len(recommand) > items:
            return Response({'error': True, 'message' : 'items mus >= recommand length'}, status=400)

        #5. select recommand words
        if len(recommand) > 0:
            recommandquiz = Quiz.objects.filter(word__in=list(recommand), deleted=False).order_by('?')
            serializer = QuizSerializer(recommandquiz, rand=True, many=True)
            recommandquiz = serializer.data

            #transform to df & select unique rand
            recommandquiz = pd.DataFrame(recommandquiz)

            if len(recommandquiz):
                recommandquiz = recommandquiz.groupby("word").sample(n=1, random_state=1).reset_index(drop=True)
        else:
            recommandquiz = pd.DataFrame()

        #6. rand num (total - len(recommandquiz))
        randnum = items - len(recommandquiz)

        #7. select rand words
        if randnum > 0:
            randquiz = Quiz.objects.filter(deleted=False).order_by('?')[:randnum]

            serializer = QuizSerializer(randquiz, many=True)
            randquiz = serializer.data

            #transform to df
            randquiz = pd.DataFrame(randquiz)
        else:
            randquiz = pd.DataFrame()

        #8. merge recommandwords & randwords & transform to json
        data = pd.concat([recommandquiz, randquiz], ignore_index=True)
        data = data.to_json(orient='records', force_ascii=False)
        data = json.loads(data)

        #9. user mode (evaluation)
        for index in range(len(data)):
            data[index]['evaluation'] = calculate_accuracy(request.user_id, data[index]['word'])
    else:
        #10. guess mode
        quiz = Quiz.objects.filter(deleted=False).order_by('?')[:items]
        serializer = QuizSerializer(quiz, rand=True, many=True)
        data = serializer.data

    return Response({
        'error' : False,
        'message' : '',
        'data' : data
    }, status.HTTP_200_OK)
