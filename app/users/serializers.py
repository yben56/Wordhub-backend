from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    birthday = serializers.DateField(required=True)
    gender = serializers.BooleanField(required=True)

    def __init__(self, *args, **kwargs):
        remove_password = kwargs.pop('remove_password', False)
        super().__init__(*args, **kwargs)
        
        if remove_password:
            self.fields.pop('password')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'birthday', 'gender']