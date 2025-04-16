from django.utils.translation import gettext as _
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..authentication import create_token
from ..models import User
from ..validator import EmailValidator, PasswordValidator, TransformError
import os

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
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    #6. ban
    if user.ban:
        return Response({
            'error': True,
            'message' : _('This account has been banned. If you have any questions, please contact the administrator')
        }, status=status.HTTP_403_FORBIDDEN)
    
    #7. token
    access_token = create_token(user.id, os.environ.get('JWT_ACCESS_SECRET', 'JWT_ACCESS_SECRET not found'), 720)
    refresh_token = create_token(user.id, os.environ.get('JWT_REFRESH_SECRET', 'JWT_REFRESH_SECRET not found'), 720)

    response = Response({
        'error' : False,
        'message' : '',
        'data' : {
            'access_token' : access_token['token'],
            'access_token_exp' : access_token['exp'],
            'first_name' : user.first_name,
            'profile_picture' : user.profile_picture
        }
    }, status=status.HTTP_200_OK)
    
    response.set_cookie(
        key='refresh_token', 
        value=refresh_token, 
        httponly=True,
        secure=os.environ.get('SET_COOKIE_SECURE', 'SET_COOKIE_SECURE not found'), # allow only https（dev enviroment can set False）
        samesite='Strict', #prevent CSRF attack
        max_age=30 * 24 * 60 * 60    
    )

    return response