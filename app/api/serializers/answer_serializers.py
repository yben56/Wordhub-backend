from rest_framework import serializers
from api.models import Answer

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['correct', 'trials']

    def get_initial(self):
        if self.instance is None:
            return {'correct': 0, 'trials': 0}
        
        return super().get_initial()