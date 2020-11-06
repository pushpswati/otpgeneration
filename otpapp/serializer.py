
from rest_framework import serializers

from . import models
from .models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'contact']
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'firstname','lastname','address',"contact",'created','email']

class Otpverify(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["contact","token"]

class UserFileViewSerializer(serializers.ModelSerializer):
    """
    CustomerSerializer class for Customer model
    """
    class Meta:
        model=models.User
        fields = ('id','file_name','file_type','created')