from rest_framework import serializers
from api.models import Dictionary

class DictionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dictionary
        fields = '__all__'