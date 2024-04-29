from django.utils.translation import gettext as _
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..validator import EmailValidator, PasswordValidator, TransformError
from datetime import datetime, timedelta
import jwt, os

from ..models import User
from ..serializers import UserSerializer

@api_view(['POST'])
def login(request):
    #1. validator
    email_validator = EmailValidator(request.data)
    
    if email_validator.validate() == False:
        return Response({
            'error' : True,
            'message' : TransformError(email_validator.get_message())
        }
        , status=status.HTTP_400_BAD_REQUEST)
    
    password_validator = PasswordValidator(request.data)
    
    if password_validator.validate() == False:
        return Response({
            'error' : True,
            'message' : TransformError(password_validator.get_message())
        }, status=status.HTTP_400_BAD_REQUEST)
    
    #2. get user
    user = User.objects.filter(email=request.data['email']).first()

    #3. check email
    if user is None:
        return Response({
            'error' : True,
            'message' : _('Invalid Email or Password')
        }, status=status.HTTP_400_BAD_REQUEST)

    #4. check pwd
    if not user.check_password(request.data['password']):
        return Response({
            'error' : True,
            'message' : _('Invalid Email or Password')
        }, status=status.HTTP_400_BAD_REQUEST)
    
    #5. active
    if not user.is_active:
        return Response({
            'error': True,
            'message' : _('This email address has been registered but has not been confirmed yet. Please reconfirm your email')
        }, status=status.HTTP_403_FORBIDDEN)

    #6. jwt
    payload = {
        'id' : user.id,
        'exp': datetime.utcnow() + timedelta(minutes=60),
        'iat': datetime.utcnow()
    }

    #7.
    secret = os.environ.get('JWT_ENCRYPT_SECRET', 'JWT_ENCRYPT_SECRET not found')
    access_token = jwt.encode(payload, secret, algorithm='HS256')

    token = {
        'access_token' : access_token,
        'refresh_token' : ''
    }

    response = Response({
        'error' : False,
        'message' : '',
        'data' : {
            'first_name' : user.first_name,
            'profile_picture' : user.profile_picture
        }
    }, status=status.HTTP_200_OK)
    
    response.set_cookie(key='token', value=token, httponly=True)

    return response