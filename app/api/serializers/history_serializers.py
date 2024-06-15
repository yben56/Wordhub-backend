from rest_framework import serializers
from api.models import Dictionary, SearchWord

class DictionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dictionary
        fields = ['id', 'word']

class HistorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='dictionary.id')
    word = serializers.CharField(source='dictionary.word')
    
    class Meta:
        model = SearchWord
        fields = ['id', 'word', 'count', 'date']