from django.utils.translation import gettext as _
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from ..models import Dictionary, SearchWord, AccessWord, Answer
from api.serializers.dictionary_serializers import DictionarySerializer
from ..utils import calculate_accuracy

from ..recommendation import recommend
from datetime import timedelta
import pandas as pd
import numpy as np

@api_view(['GET'])
def words(request):
    #1. pages
    pages = request.GET.get('pages')

    if pages is not None:
        try:
            pages = int(pages)
        except ValueError:
            return Response({
                'error' : True,
                'message' : 'Invalid Pages'
            }
            , status=status.HTTP_400_BAD_REQUEST)
    else:
        pages = 9 

    #2. classification
    classification = request.GET.get('classification')

    #3. user mode
    if request.user_id:

        timerange = timezone.now() - timedelta(days=2)

        #1. fetch search
        search_words = SearchWord.objects.filter(user_id=request.user_id, exist=True, date__gte=timerange).values()

        #2. fetch access
        access_words = AccessWord.objects.filter(user_id=request.user_id, date__gte=timerange).values()

        #3. fetch quiz answer
        answer_words = Answer.objects.filter(user_id=request.user_id, date__gte=timerange).values('word', 'correct', 'trials', 'date')

        #4. caculate counts
        search_words = recommend(search_words, 1)
        access_words = recommend(access_words, 1.5)
        answer_words = recommend(answer_words, 2, True)

        #5. merge 3 df
        df = pd.concat([search_words, access_words, answer_words])

        df = df.groupby('word', as_index=False).sum()

        #6. probability for each words
        total_counts = df['counts'].sum()
        df['probability'] = round(df['counts'] / total_counts, 2)
        df['probability'] = df['probability'] / df['probability'].sum()

        #7. select words from distribution
        selected_words = np.random.choice(df['word'], size=3, p=df['probability'], replace=False)

        words = Dictionary.objects.filter(word__in=list(selected_words)).order_by('?')
        serializer = DictionarySerializer(words, many=True)
        data = serializer.data

        '''
        if classification is not None:
            words = Dictionary.objects.exclude(pos__in=['abbreviation', 'interrogative'])
            words = words.filter(classification__contains=classification.lower(), deleted=False).order_by('?')[:pages]
        else:
            words = Dictionary.objects.exclude(pos__in=['abbreviation', 'interrogative']).order_by('?')[:pages]

        serializer = DictionarySerializer(words, many=True)
        data = serializer.data
        '''

        for index in range(len(data)):
            data[index]['probability'] = 6

            #4. evaluation
            data[index]['evaluation'] = calculate_accuracy(request.user_id, data[index]['word'])
        

    #5. guess mode
    else:
        if classification is not None:
            words = Dictionary.objects.exclude(pos__in=['abbreviation', 'interrogative'])
            words = words.filter(classification__contains=classification.lower(), deleted=False).order_by('?')[:pages]
        else:
            words = Dictionary.objects.exclude(pos__in=['abbreviation', 'interrogative']).order_by('?')[:pages]

        serializer = DictionarySerializer(words, many=True)
        data = serializer.data

        for index in range(len(data)):
            data[index]['probability'] = 6

    #6. resposne
    return Response({
        'error' : False,
        'message' : '',
        'data' : data
    }, status=200)