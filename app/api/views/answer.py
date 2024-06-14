from django.utils.translation import gettext as _
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view

from ..models import Answer

@api_view(['POST'])
def answer(request):
    #1.
    wordid = request.data['wordid']
    word = request.data['word']
    correct = request.data['correct']
    if correct:
        correct = 1
    else:
        correct = 0

    #2.
    obj, created = Answer.objects.update_or_create(
        user_id=request.user_id, 
        dictionary_id=wordid,
        defaults={'word': word},
    )

    obj.correct += correct 
    obj.trials += 1
    obj.date = timezone.now()   
    obj.save()

    #4.
    return Response({
        'error' : False,
        'message' : '',
        'data' : ''
    }, status=200)