from django.utils.translation import gettext as _
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..authentication import create_token, decode_token
from ..mail import sendmail
from ..models import User
from ..validator import EmailValidator, TransformError
import os



@api_view(['GET', 'POST'])
def email_confirmation(request):
    ##user click links from his/her email & confirm his/her account
    if request.method == 'GET':
        #1. token
        token = request.GET.get('token')

        if not token:
            return Response({
                'error' : True,
                'message' : 'Unauthenticated'
            }, status=status.HTTP_403_FORBIDDEN) 

        #2. decode
        decode = decode_token(token, os.environ.get('JWT_EMAIL_CONFIRMATION_SECRET', 'JWT_EMAIL_CONFIRMATION_SECRET not found'))

        if decode['error']:
            return Response({
                'error' : True,
                'message' : decode['message']
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        user_id = decode['data']['user_id']

        #3. check active
        user = User.objects.filter(id=user_id).first()
        
        if not user:
            return Response({
                'error' : True,
                'message' : _('We could not find this email address.')
            }, status=status.HTTP_403_FORBIDDEN)

        if user.is_active:
            return Response({
                'error' : True,
                'message' : _('This email address has already confirmed.')
            }, status=status.HTTP_403_FORBIDDEN)
        
        #4. update db
        User.objects.filter(id=user_id).update(is_active=1)

        #5. response
        return Response({
            'error' : False,
            'message' : _('Email confirm successfully. Please login again.')
        },status=status.HTTP_200_OK)
    
    ##use for resend Email Confirmation
    if request.method == 'POST':

        #1. validation
        validator = EmailValidator(request.data)

        if validator.validate() == False:
            return Response({
                'error' : True,
                'message' : TransformError(validator.get_message())
            }, status=status.HTTP_400_BAD_REQUEST)
        
        #2. get user
        user = User.objects.filter(email=request.data.get('email'), is_active=0).first()
        if not user:
            return Response({
                'error' : True,
                'message' : _('We could not find this email address')
            }, status=status.HTTP_400_BAD_REQUEST)

        #3. token
        token = create_token(user.id, os.environ.get('JWT_EMAIL_CONFIRMATION_SECRET', 'JWT_EMAIL_CONFIRMATION_SECRET not found'))
        token = token['token']

        #4. send confirmation email
        site_url = os.environ.get('SITE_URL', 'SITE_URL not found')
        site_url = f'{site_url}/EmailConfirmation?token={token}'

        #5. send confirmation email
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

        #6. respose
        return Response({
            'error' : False,
            'message' : _('Email confirmation has send')
        }, status=status.HTTP_200_OK)