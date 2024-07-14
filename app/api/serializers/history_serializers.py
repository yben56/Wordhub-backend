from rest_framework import serializers
from api.models import Dictionary, AccessWord

class DictionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dictionary
        fields = ['id', 'word', 'pos', 'translation']

class HistorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='dictionary.id')
    word = serializers.CharField(source='dictionary.word')
    pos = serializers.CharField(source='dictionary.pos')
    translation = serializers.CharField(source='dictionary.translation')
    
    class Meta:
        model = AccessWord
        fields = ['id', 'word', 'pos', 'translation', 'date']