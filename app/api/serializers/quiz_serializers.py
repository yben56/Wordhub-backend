from rest_framework import serializers
from api.models import Quiz
import json, random

class QuizSerializer(serializers.ModelSerializer):
    quiz = serializers.SerializerMethodField()
    
    class Meta:
        model = Quiz
        fields = '__all__'

    def get_quiz(self, obj):
        quiz_list = json.loads(obj.quiz)
        random.shuffle(quiz_list)
        return quiz_list