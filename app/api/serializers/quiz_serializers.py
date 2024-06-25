from rest_framework import serializers
from api.models import Quiz, QuizVersion
import json, random

class QuizSerializer(serializers.ModelSerializer):
    quiz = serializers.SerializerMethodField()
    
    def __init__(self, *args, **kwargs):
        self.rand = kwargs.pop('rand', False)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Quiz
        fields = '__all__'

    def get_quiz(self, obj):
        quiz_list = json.loads(obj.quiz)
        if self.rand:
            random.shuffle(quiz_list)
        return quiz_list
    
class QuizUpdateSerializer(serializers.ModelSerializer):
    quiz = serializers.JSONField()
    
    class Meta:
        model = Quiz
        fields = ['dictionary', 'word', 'quiz', 'auther']
    
    def create(self, validated_data):
        validated_data['quiz'] = json.dumps(validated_data['quiz'], ensure_ascii=False)
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if 'quiz' in validated_data:
            instance.quiz = json.dumps(validated_data.pop('quiz'), ensure_ascii=False)
                
        return super().update(instance, validated_data)
    
class QuizVersionSerializer(serializers.ModelSerializer):
    quiz = serializers.JSONField()

    class Meta:
        model = QuizVersion
        fields = '__all__'