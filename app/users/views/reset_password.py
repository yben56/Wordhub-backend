from django.utils.translation import gettext as _
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..mail import sendmail
from django.db import transaction
from ..validator import EmailValidator, PasswordValidator, TransformError
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import datetime, timedelta
from ..jwtoken import jwtoken
import jwt, os

from ..models import User, UserResetPassword

@api_view(['GET', 'POST', 'PUT'])
def reset_password(request):
     
     secret = os.environ.get('JWT_ENCRYPT_SECRET', 'JWT_ENCRYPT_SECRET not found')

     ##user request forgot password
     if request.method == 'POST':
        #1. validation
        email_validator = EmailValidator(request.data)
        
        if email_validator.validate() == False:
            return Response({
                'error' : True,
                'message' : TransformError(email_validator.get_message())
            }, status=status.HTTP_400_BAD_REQUEST)

        #2. get user
        user = User.objects.filter(email=request.data['email'], is_active=1).first()

        #3. check email
        if user is None:
            return Response({
                'error' : True,
                'message' : _('We could not find this email address')
            }, status=status.HTTP_400_BAD_REQUEST)
        
        #4. user_reset_password
        user_reset_password = UserResetPassword.objects.filter(user_id=user.id).order_by('-date').first()

        #4. user should only request per hour!!!
        if user_reset_password and user_reset_password.date >= timezone.now() - timedelta(hours=1):
            return Response({
                'error' : True,
                'message' : _('In the past hour, a password reset request has already been submitted, and therefore cannot be submitted again temporarily.')
            }, status=status.HTTP_403_FORBIDDEN)

        #5. token
        token = jwtoken(user.id, secret)

        #6. save record to user_reset_password
        UserResetPassword.objects.create(user_id=user.id, token=token, date=timezone.now())

        #7. send mail
        site_url = os.environ.get('SITE_URL', 'SITE_URL not found')
        message = _('You are receiving this email because you requested to reset your password. If you did not make this request, you can ignore this email.\n\nTo reset your password, please click on the following link:')

        email = sendmail({
            'subject' : 'Reset Your Password',
            'message' : f'{message} {site_url}/ResetPassword?token={token}',
            'from_email' : os.environ.get('EMAIL_HOST_USER', 'EMAIL_HOST_USER not found'),
            'recipient_list' : [user.email]
        })

        if email:
            return Response({
                'error' : True,
                'message' : email
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        #6. respose
        return Response({
            'error' : False,
            'message' : _('Reset Password link has send to your email.')
        }, status=status.HTTP_200_OK)
     
     ##user click reset password links
     if request.method == 'GET':
        #1. token
        token = request.GET.get('token')

        if not token:
            return Response({
                'error' : True,
                'message' : 'Unauthenticated'
            }, status=status.HTTP_403_FORBIDDEN) 

        #2. decode
        try:
            payload = jwt.decode(token, secret, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({
                'error' : True,
                'message' : 'Token expired'
            }, status=status.HTTP_403_FORBIDDEN) 
        except jwt.DecodeError:
            return Response({
                'error' : True,
                'message' : 'Invalid Token'
            }, status=status.HTTP_403_FORBIDDEN) 

        #3. check user
        user = User.objects.filter(id=payload['id'], is_active=1).first()

        #4. response
        return Response({
            'error' : False,
            'message' : ''
        }, status=status.HTTP_200_OK)   
             
     ##user update password
     if request.method == 'PUT':
        #1. token
        token = request.data.get('token')

        if not token:
            return Response({
                'error' : True,
                'message' : 'Unauthenticated'
            }, status=status.HTTP_403_FORBIDDEN) 

        #2. decode
        try:
            payload = jwt.decode(token, secret, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({
                'error' : True,
                'message' : 'Token expired'
            }, status=status.HTTP_403_FORBIDDEN) 
        except jwt.DecodeError:
            return Response({
                'error' : True,
                'message' : 'Invalid Token'
            }, status=status.HTTP_403_FORBIDDEN) 
        
        #3. password validator
        password_validator = PasswordValidator(request.data)

        if password_validator.validate() == False:
            return Response(TransformError(password_validator.get_message()), status=status.HTTP_400_BAD_REQUEST)
        
        #4. password encrypt
        #request.data._mutable = True
        pwd = make_password(request.data.get('password'))

        #5. check record
        resetpwd = UserResetPassword.objects.filter(token=token, used=0).first()

        if not resetpwd:
            return Response({
            'error' : False,
            'message' : _('Can not find Reset Password request or this link already been used.')
        }, status=status.HTTP_403_FORBIDDEN)

        with transaction.atomic():
            #5. update password
            User.objects.filter(id=payload['id']).update(password=pwd)

            #6. mark used reset password
            UserResetPassword.objects.filter(token=token).update(used=1)

        #7.
        return Response({
            'error' : False,
            'message' : _('Password has been updated.')
        }, status=status.HTTP_200_OK)