from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserSerializer
import random
import json

# Create your views here.
class Userview(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)
    def isuserexist(self,contact):
        try:
             userdbobj=User.objects.get(contact=contact)
             return userdbobj
        except :
            return None



    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        data=request.data
        contact = data["contact"]
        iscontact=self.isuserexist(contact)
        if serializer.is_valid():
            if iscontact is None:
               serializer.save()
            otpnum = random.randint(1111, 9999)
            userdbobj =User.objects.get(contact=contact)
            userdbobj.otp=otpnum
            userdbobj.save()

            # here should be sms code...
            response={"success":True,"otp":otpnum}
            response=json.dumps(response)
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)