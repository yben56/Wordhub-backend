from rest_framework import serializers
from api.models import Dictionary, DictionaryVersion
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
    
class DictionaryUpdateSerializer(serializers.ModelSerializer):
    classification = serializers.JSONField()
    sentences = serializers.JSONField()
    
    class Meta:
        model = Dictionary
        fields = ['translation', 'phonetic', 'pos', 'classification', 'sentences', 'auther']
    
    def update(self, instance, validated_data):

        if 'classification' in validated_data:
            instance.classification = json.dumps(validated_data.pop('classification'))
        
        if 'sentences' in validated_data:
            instance.sentences = json.dumps(validated_data.pop('sentences'), ensure_ascii=False)
                
        return super().update(instance, validated_data)
    
class DictionaryPostSerializer(serializers.ModelSerializer):
    classification = serializers.JSONField()
    sentences = serializers.JSONField()

    class Meta:
        model = Dictionary
        fields = '__all__'

    def create(self, validated_data):

        classification_data = json.dumps(validated_data.pop('classification', []))
        
        sentences_data = json.dumps(validated_data.pop('sentences', []))

        dictionary_instance = Dictionary.objects.create(**validated_data)
        dictionary_instance.classification = classification_data
        dictionary_instance.sentences = sentences_data
        dictionary_instance.save()

        return dictionary_instance
    
class DictionaryVersionSerializer(serializers.ModelSerializer):
    associate = serializers.JSONField()
    classification = serializers.JSONField()
    sentences = serializers.JSONField()

    class Meta:
        model = DictionaryVersion
        fields = '__all__'