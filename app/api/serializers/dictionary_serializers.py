from rest_framework import serializers
from api.models import Dictionary
import json

class DictionarySerializer(serializers.ModelSerializer):
    sentences = serializers.SerializerMethodField()
    associate = serializers.SerializerMethodField()
    classification = serializers.SerializerMethodField()

    class Meta:
        model = Dictionary
        fields = '__all__'

    def get_sentences(self, obj):
        if obj.sentences:
            try:
                return json.loads(obj.sentences)
            except json.JSONDecodeError:
                return []
        return []
    
    def get_associate(self, obj):
        if obj.associate:
            try:
                return json.loads(obj.associate)
            except json.JSONDecodeError:
                return {}
        return {}
    
    def get_classification(self, obj):
        if obj.classification:
            try:
                return json.loads(obj.classification)
            except json.JSONDecodeError:
                return []
        return []