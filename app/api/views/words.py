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
        #recommand###########################################################################################
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
            if classification:
                recommandwords = Dictionary.objects.filter(word__in=list(recommand), classification__contains=classification, deleted=False).order_by('?')
            else:
                recommandwords = Dictionary.objects.filter(word__in=list(recommand), deleted=False).order_by('?')

            serializer = DictionarySerializer(recommandwords, many=True)
            recommandwords = serializer.data

            #transform to df & select unique rand
            recommandwords = pd.DataFrame(recommandwords)

            #remove multiple words (some words have multiple row, ex: bat:蝙蝠, bat:球棒)
            if len(recommandwords):
                recommandwords = recommandwords.groupby("word").sample(n=1, random_state=1).reset_index(drop=True)
        else:
            recommandwords = pd.DataFrame()

        #6.remain num (total - len(recommandwords))
        remainnum = items - len(recommandwords)
        
        #associate word (required have recommand)###################################################################################
        #7. select random associate words
        if len(recommandwords) > 0:
            randassociateword = recommandwords['associate'].apply(lambda x: list(x.keys()))
            randassociateword = pd.Series(sum(randassociateword, []))

            #convert to list (associateword may less than remain)
            if len(randassociateword) >= remainnum:
                randassociateword = random.sample(randassociateword.tolist(), remainnum)
            else:
                randassociateword = random.sample(randassociateword.tolist(), len(randassociateword))

            #fetch associateword
            associateword = Dictionary.objects.filter(word__in=randassociateword, deleted=False).distinct()
            serializer = DictionarySerializer(associateword, many=True)
            associateword = serializer.data

            #transform to df
            associateword = pd.DataFrame(associateword)

            #remove multiple words (some words have multiple row, ex: bat:蝙蝠, bat:球棒)
            if len(associateword):
                associateword = associateword.groupby("word").sample(n=1, random_state=1).reset_index(drop=True)
            
            #remain num (total - len(recommandwords))
            remainnum = remainnum - len(associateword)
        else:
            associateword = pd.DataFrame()

        #rand words###########################################################################################
        #8. select rand words
        if remainnum > 0:
            randwords = Dictionary.objects.exclude(pos__in=['abbreviation', 'interrogative'])

            if classification:
                randwords = randwords.filter(classification__contains=classification, deleted=False).order_by('?')[:remainnum]
            else:
                randwords = randwords.filter(deleted=False).order_by('?')[:remainnum]

            serializer = DictionarySerializer(randwords, many=True)
            randwords = serializer.data

            #transform to df
            randwords = pd.DataFrame(randwords)
        else:
            randwords = pd.DataFrame()

        #merge recommand, associate, randwords ####################################################################  
        #8. merge recommandwords & randwords & transform to json
        data = pd.concat([recommandwords, associateword, randwords], ignore_index=True)

        data = data.to_json(orient='records', force_ascii=False)
        data = json.loads(data)

        #9. evaluation
        for index in range(len(data)):
            data[index]['evaluation'] = calculate_accuracy(request.user_id, data[index]['word'])
        
    #10. guess mode
    else:
        if classification is not None:
            words = Dictionary.objects.exclude(pos__in=['abbreviation', 'interrogative'])
            words = words.filter(classification__contains=classification.lower(), deleted=False).order_by('?')[:items]
        else:
            words = Dictionary.objects.exclude(pos__in=['abbreviation', 'interrogative']).order_by('?')[:items]

        serializer = DictionarySerializer(words, many=True)
        data = serializer.data

    #11. probability
    for index in range(len(data)):
        data[index]['probability'] = ''

    #12. resposne
    return Response({
        'error' : False,
        'message' : '',
        'data' : data
    }, status=200)