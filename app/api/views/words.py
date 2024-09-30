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
import ast, json, random

@api_view(['GET'])
def words(request):
    #1. items
    try:
        items = int(request.GET.get('items', 9))
    except ValueError:
        return Response({'error': True, 'message' : 'items be an integer'}, status=400)

    #2. classification
    classification = request.GET.get('classification', '').lower() if request.GET.get('classification') else None

    #3. get recommand list
    recommand = request.GET.get('recommand', [])

    #4. user mode
    if request.user_id:
        #4-1. recommand words
        recommandwords = recommandword(recommand, classification, items)

        if recommandwords['error']:
            return Response({'error': True, 'message' : recommandwords['message']}, status=400)
        else:
            recommandwords = recommandwords['data']

        #4-2.remain num (total - len(recommandwords))
        remainnum = items - len(recommandwords)

        #4-3.associate words (required remainnum > 0 & have recommand word)
        associatewords = associateword(recommandwords, classification, remainnum)

        if associatewords['error']:
            return Response({'error': True, 'message' : associatewords['message']}, status=400)
        else:
            associatewords = associatewords['data']

        #4-4. remain num (remainnum - len(associatewords))
        remainnum = remainnum - len(associatewords)

        #4-5. randwords
        randwords = randword(classification, remainnum)

        if randwords['error']:
            return Response({'error': True, 'message' : randwords['message']}, status=400)
        else:
            randwords = randwords['data']

        #4-6. merge recommandwords & associatewords & randwords & transform to json
        data = pd.concat([recommandwords, associatewords, randwords], ignore_index=True)

        data = data.to_json(orient='records', force_ascii=False)
        data = json.loads(data)

        #4-7. evaluation
        for index in range(len(data)):
            data[index]['evaluation'] = calculate_accuracy(request.user_id, data[index]['word'])
        
    #5. guess mode
    else:
        if classification is not None:
            words = Dictionary.objects.exclude(pos__in=['abbreviation', 'interrogative'])
            words = words.filter(classification__contains=classification.lower(), deleted=False).order_by('?')[:items]
        else:
            words = Dictionary.objects.exclude(pos__in=['abbreviation', 'interrogative']).order_by('?')[:items]

        serializer = DictionarySerializer(words, many=True)
        data = serializer.data

    #6. probability
    for index in range(len(data)):
        data[index]['probability'] = ''

    #7. resposne
    return Response({
        'error' : False,
        'message' : '',
        'data' : data
    }, status=200)

def recommandword(recommand, classification, items):
    try:
        if len(recommand) > 0:
            #1. recommand must be list
            try:
                recommand = ast.literal_eval(recommand)
            except (SyntaxError, ValueError) as e:
                return {'error': True, 'message' : 'recommand must be a list'}

            #2. prevent recommand redundant
            if len(recommand) > items:
                return {'error': True, 'message' : 'items mus >= recommand length'}
            
            #3. select recommand words
            if classification:
                recommandwords = Dictionary.objects.filter(word__in=list(recommand), classification__contains=classification, deleted=False).order_by('?')
            else:
                recommandwords = Dictionary.objects.filter(word__in=list(recommand), deleted=False).order_by('?')

            serializer = DictionarySerializer(recommandwords, many=True)
            recommandwords = serializer.data

            #4. transform to df & select unique rand
            recommandwords = pd.DataFrame(recommandwords)

            #5. remove multiple words (some words have multiple row, ex: bat:蝙蝠, bat:球棒)
            recommandwords = recommandwords.groupby("word").sample(n=1, random_state=1).reset_index(drop=True)
        else:
            recommandwords = pd.DataFrame()

        return {'error': False, 'message': '', 'data': recommandwords}
    except Exception as e:
        return {'error': True, 'message' : str(e)}

def associateword(recommandwords, classification, remainnum):
    try:
        if remainnum > 0 and len(recommandwords) > 0:
            #1. get associate
            randassociateword = recommandwords['associate'].apply(lambda x: list(x.keys()))
            randassociateword = pd.Series(sum(randassociateword, []))

            #2. convert json to list (associateword may less than remain)
            if len(randassociateword) >= remainnum:
                randassociateword = random.sample(randassociateword.tolist(), remainnum)
            else:
                randassociateword = random.sample(randassociateword.tolist(), len(randassociateword))

            #3. fetch associateword
            if classification:
                associateword = Dictionary.objects.filter(word__in=list(randassociateword), classification__contains=classification, deleted=False).distinct()
            else:
                associateword = Dictionary.objects.filter(word__in=list(randassociateword), deleted=False).distinct()

            serializer = DictionarySerializer(associateword, many=True)
            associateword = serializer.data

            #4. transform to df
            associateword = pd.DataFrame(associateword)

            #5. remove multiple words (some words have multiple row, ex: bat:蝙蝠, bat:球棒)
            if len(associateword):
                associateword = associateword.groupby("word").sample(n=1, random_state=1).reset_index(drop=True)
        else:
            associateword = pd.DataFrame()
        
        return {'error': False, 'message': '', 'data': associateword}
    except Exception as e:
        return {'error': True, 'message' : str(e)}

def randword(classification, remainnum):
    try:
        if remainnum > 0:
            #1. don't select abbreviation & interrogative
            randwords = Dictionary.objects.exclude(pos__in=['abbreviation', 'interrogative'])

            #2. classification
            if classification:
                randwords = randwords.filter(classification__contains=classification, deleted=False).order_by('?')[:remainnum]
            else:
                randwords = randwords.filter(deleted=False).order_by('?')[:remainnum]

            serializer = DictionarySerializer(randwords, many=True)
            randwords = serializer.data

            #3. transform to df
            randwords = pd.DataFrame(randwords)
        else:
            randwords = pd.DataFrame()

        return {'error': False, 'message': '', 'data': randwords}
    except Exception as e:
        return {'error': True, 'message' : str(e)}