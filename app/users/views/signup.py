from django.utils.translation import gettext as _
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..validator import SignupValidator, TransformError
from django.contrib.auth.hashers import make_password

from ..models import User
from ..serializers import UserSerializer

from ..mail import sendmail
from ..jwtoken import jwtoken
import os

@api_view(['POST'])
def signup(request):
    #1. validator
    validator = SignupValidator(request.data)
    
    if validator.validate() == False:
        return Response({
            'error' : True,
            'message' : TransformError(validator.get_message())
        }, status=status.HTTP_400_BAD_REQUEST)

    #2. user exist or not
    user = User.objects.filter(email=request.data.get('email')).first()

    if user:
        #3. user is_not_active
        if user.is_active == 0:
            return Response({
                'error': True,
                'message' : _('This email address has been registered but has not been confirmed yet. Please reconfirm your email')
            }, status=status.HTTP_403_FORBIDDEN)

        #4. email exists
        else:
            return Response({
                'error' : True,
                'message' : _('This email address is already in use')
            }, status=status.HTTP_400_BAD_REQUEST)
    
    #5. password encrypt
    #request.data._mutable = True
    request.data['password'] = make_password(request.data.get('password'))

    #6. serializer
    serializer = UserSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({
            'error' : True,
            'message' : serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    #7. insert db
    user = User.objects.create(**serializer.validated_data)
        
    #8. token
    secret = os.environ.get('JWT_ENCRYPT_SECRET', 'JWT_ENCRYPT_SECRET not found')
    token = jwtoken(user.id, secret)

    #9. confirmation email url
    site_url = os.environ.get('SITE_URL', 'SITE_URL not found')
    site_url = f'{site_url}/EmailConfirmation?token={token}'

    #10. send confirmation email
    message = _('Please confirm your email by clicking on the following link:')

    email = sendmail({
        'subject' : _('Please confirm your email'),
        'message' : message + ' ' + site_url,
        'from_email' : os.environ.get('EMAIL_HOST_USER', 'EMAIL_HOST_USER not found'),
        'recipient_list' : [user.email]
    })

    if email:
        return Response({
            'error' : True,
            'message' : email
        }, status=status.HTTP_400_BAD_REQUEST)

    #11.
    return Response({
        'error' : False,
        'message' : _('Please confirm your email')
    }, status=status.HTTP_200_OK)