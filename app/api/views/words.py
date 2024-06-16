from django.utils.translation import gettext as _
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from ..models import Dictionary
from api.serializers.dictionary_serializers import DictionarySerializer
from ..utils import calculate_accuracy

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
        ###REPLACE THIS PART WITH ALGORITHM###
        words = Dictionary.objects.exclude(pos__in=['abbreviation', 'interrogative'])

        if classification is not None:
            words = words.filter(classification__contains=classification.lower()).order_by('?')[:pages]

        serializer = DictionarySerializer(words, many=True)
        data = serializer.data

        for index in range(len(data)):
            data[index]['probability'] = 6

            #4. evaluation
            data[index]['evaluation'] = calculate_accuracy(request.user_id, data[index]['word'])

    #5. guess mode
    else:
        words = Dictionary.objects.exclude(pos__in=['abbreviation', 'interrogative'])

        if classification is not None:
            words = words.filter(classification__contains=classification.lower()).order_by('?')[:pages]

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