from .models import Answer
from api.serializers.answer_serializers import AnswerSerializer

def calculate_accuracy(user_id, word):
    fetchanswer = Answer.objects.filter(user_id=user_id, word=word).first()
    serializer = AnswerSerializer(fetchanswer)

    output = {}
    output = serializer.data
    output['accuracy'] = '{}%'.format(
        round((output['correct'] / output['trials']) * 100)  if output['trials'] else 0
    )

    return output