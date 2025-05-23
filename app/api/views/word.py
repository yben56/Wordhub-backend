from django.utils.translation import gettext as _
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view

from ..models import Dictionary, AccessWord
from api.serializers.dictionary_serializers import DictionarySerializer

@api_view(['GET'])
def word(request, word, wordid):
    try:
        #1. fetch
        fetchword = Dictionary.objects.get(word=word, id=wordid, deleted=False)
        serializer = DictionarySerializer(fetchword)
        data = serializer.data

        #2. if no match
        if not len(data):
            return Response({
                'error': True,
                'message': _('Page not found.'),
                'data': None
            }, status=404)

        #3. user mode only
        if request.user_id:
            #4. create
            created = AccessWord.objects.create(
                user_id=request.user_id,
                dictionary_id=wordid,
                word=word
            )

            #5. evaluation
            from ..utils import calculate_accuracy
            data['evaluation'] = calculate_accuracy(request.user_id, word)

        #6.
        data['probability'] = ''
       
        #7. output
        return Response({
            'error' : False,
            'message' : '',
            'data' : data
        }, status=200)
    
    except Dictionary.DoesNotExist:
        return Response({
            'error': True,
            'message': _('Page not found.'),
            'data': None
        }, status=404)