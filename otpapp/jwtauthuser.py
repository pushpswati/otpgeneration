import jwt,json

from django.conf import settings
from otpapp.models import User
from django.utils import timezone

from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication

class JSONWebTokenAuthentication(TokenAuthentication):
    def  __init__(self,dbobject=None):
        self.dbobject=dbobject
    def authenticate_credentials(self, key):
        try:
            payload = jwt.decode(key, settings.SECRET_KEY)
            age=payload['age']
            print("authenticate_credentials", payload)
            now = timezone.now()
            timed = 24 * 60 * 60 * now.day + now.hour * 60 * 60 + now.minute * 60 + now.second
            print("timed",timed)
            if True:#int(timed)<=int(age):
                print("authenticate_credentials",payload)
                return payload

        except (jwt.DecodeError, User.DoesNotExist):
            return {}
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired')



    def get_user_jwt(self,age):
        payload = {
            'contact': self.dbobject.contact,
            'age':age

        }
        encoded = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return encoded.decode()

    def get_wishpoint_jwt(self,age):
        payload = {
            'email': self.dbobject.email,
            'age':age

        }
        encoded = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return encoded.decode()
