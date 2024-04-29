from django.core.mail import send_mail
from datetime import datetime, timedelta
import jwt, os

def sendmail(options):
    try:
        subject = options['subject']
        message = options['message']
        from_email = options['from_email']
        recipient_list = options['recipient_list']

        send_mail(subject, message, from_email, recipient_list)

        return False
    except Exception as e:
        return str(e)