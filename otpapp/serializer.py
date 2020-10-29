
from rest_framework import serializers
from .models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'contact']
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'firstname','lastname','address',"contact",'created','email']
        