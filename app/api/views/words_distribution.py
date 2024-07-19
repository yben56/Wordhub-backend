from django.utils.translation import gettext as _
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from ..models import SearchWord, AccessWord, Answer
from ..recommendation import recommend
from datetime import timedelta
import pandas as pd
import numpy as np

@api_view(['GET'])
def words_distribution(request):

    timerange = timezone.now() - timedelta(days=30)

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

    #6. if no records
    if len(df) == 0:
        return Response({
            'error' : False,
            'message' : '',
            'data' : {}
        }, status.HTTP_200_OK)

    #7. group same word and sum
    df = df.groupby('word', as_index=False).sum()

    #8. to dictionary
    df = df.set_index('word')['counts'].to_dict()

    return Response({
        'error' : False,
        'message' : '',
        'data' : df
    }, status.HTTP_200_OK)
