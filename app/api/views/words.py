from django.utils.translation import gettext as _
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from ..models import Dictionary, SearchWord, AccessWord, Answer
from api.serializers.dictionary_serializers import DictionarySerializer
from ..utils import calculate_accuracy

from ..recommendation import recommend
import pandas as pd
import ast, json

@api_view(['GET'])
def words(request):
    try:
        items = int(request.GET.get('items', 9))
    except ValueError:
        return Response({'error': True, 'message' : 'items be an integer'}, status=400)

    #1. classification
    classification = request.GET.get('classification', None)
    
    if classification is not None:
        classification = classification.lower()

    #2. user mode
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
            recommandwords = Dictionary.objects.filter(word__in=list(recommand)).order_by('?')
            serializer = DictionarySerializer(recommandwords, many=True)
            recommandwords = serializer.data

            #transform to df & select unique rand
            recommandwords = pd.DataFrame(recommandwords)
            recommandwords = recommandwords.groupby("word").sample(n=1, random_state=1).reset_index(drop=True)
        else:
            recommandwords = pd.DataFrame()

        #6. select rand words
        if items - len(recommand) > 0:
            randwords = Dictionary.objects.exclude(pos__in=['abbreviation', 'interrogative'])

            if classification:
                randwords = randwords.filter(classification__contains=classification, deleted=False).order_by('?')[:items - len(recommand)]
            else:
                randwords = randwords.filter(deleted=False).order_by('?')[:items - len(recommand)]

            serializer = DictionarySerializer(randwords, many=True)
            randwords = serializer.data

            #transform to df
            randwords = pd.DataFrame(randwords)
        else:
            randwords = pd.DataFrame()
        
        #7. merge recommandwords & randwords & transform to json
        data = pd.concat([recommandwords, randwords], ignore_index=True)
        data = data.to_json(orient='records', force_ascii=False)
        data = json.loads(data)

        #8. evaluation
        for index in range(len(data)):
            data[index]['evaluation'] = calculate_accuracy(request.user_id, data[index]['word'])
        
    #9. guess mode
    else:
        if classification is not None:
            words = Dictionary.objects.exclude(pos__in=['abbreviation', 'interrogative'])
            words = words.filter(classification__contains=classification.lower(), deleted=False).order_by('?')[:items]
        else:
            words = Dictionary.objects.exclude(pos__in=['abbreviation', 'interrogative']).order_by('?')[:items]

        serializer = DictionarySerializer(words, many=True)
        data = serializer.data

    #10. probability
    for index in range(len(data)):
        data[index]['probability'] = 0

    #11. resposne
    return Response({
        'error' : False,
        'message' : '',
        'data' : data
    }, status=200)