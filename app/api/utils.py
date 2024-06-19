from .models import Answer
from api.serializers.answer_serializers import AnswerSerializer
from openai import OpenAI
import os

def calculate_accuracy(user_id, word):
    fetchanswer = Answer.objects.filter(user_id=user_id, word=word).first()
    serializer = AnswerSerializer(fetchanswer)

    output = {}
    output = serializer.data
    output['accuracy'] = '{}%'.format(
        round((output['correct'] / output['trials']) * 100)  if output['trials'] else 0
    )

    return output

def chat_gpt(command):
    model = os.environ.get('CHAT_GPT_MODEL', 'CHAT_GPT_MODEL not found')
    client = OpenAI(api_key=os.environ.get('CHAT_GPT_API_KEY', 'CHAT_GPT_API_KEY not found'))

    return command

    '''
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": command},
        ]
    )
    
    return response.choices[0].message.content
    '''