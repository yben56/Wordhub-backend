from validator import Validator
from django.utils import timezone

class SignupValidator(Validator):
    first_name = 'required'
    last_name = 'required'
    email = 'required|email'
    password = 'required|min_length:8'
    birthday = f'required|date:%Y-%m-%d|date_before:{(timezone.now() + timezone.timedelta(days=1)).date()}'
    gender = 'required|boolean'

    message = {
        'email' : {
            'email': 'Invalid email address'
        },
        'password' : {
            'min_length' : 'password is shotter than 8'
        } 
    }

class EmailValidator(Validator):
    email = 'required|email'

class PasswordValidator(Validator):
    password = 'required|min_length:8'

    message = {
        'password' : {
            'min_length' : 'password is shotter than 8'
        } 
    }

class TransformError:
    def __new__(cls, data):
        error_list = []
        for key, value in data.items():
            for error in value.values():
                error_list.append(error)
        return error_list[0]