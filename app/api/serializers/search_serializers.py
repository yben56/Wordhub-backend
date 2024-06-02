from rest_framework import serializers
from api.models import Dictionary

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dictionary
        fields = ['id', 'word', 'phonetic', 'pos', 'translation', 'associate']