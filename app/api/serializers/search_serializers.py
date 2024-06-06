from rest_framework import serializers
from api.models import Dictionary

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dictionary
        fields = ['id', 'word', 'heteronyms', 'pos', 'translation']

class AssociateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dictionary
        fields = ['word', 'associate']