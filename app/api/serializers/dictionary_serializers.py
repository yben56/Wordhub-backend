from rest_framework import serializers
from api.models import Dictionary
import json

class DictionarySerializer(serializers.ModelSerializer):
    sentences = serializers.SerializerMethodField()
    associate = serializers.SerializerMethodField()

    class Meta:
        model = Dictionary
        fields = '__all__'

    def get_sentences(self, obj):
        return json.loads(obj.sentences)
    
    def get_associate(self, obj):
        return json.loads(obj.associate)
    