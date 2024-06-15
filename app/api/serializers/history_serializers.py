from rest_framework import serializers
from api.models import Dictionary, SearchWord

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
        model = SearchWord
        fields = ['id', 'word', 'pos', 'translation', 'count', 'date']