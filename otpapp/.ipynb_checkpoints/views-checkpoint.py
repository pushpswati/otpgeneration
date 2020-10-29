from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserSerializer,UserProfileSerializer
import random
import json
import jwt

# Create your views here.
class Userview(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        request.META["token"]="asnfjksdbfhjzdbfhjzfjsbfhjsbfhjsfhjsdfvshjf"
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
        data=request.data
        if "+" in str(data['contact']):
            data['contact']=str(data["contact"])[3:].replace(' ',"").replace("-","")
            
        serializer = UserSerializer(data=data)
        
        contact = int(data["contact"])
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
#             response=json.dumps(response)
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Otpverify(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def post(self, request, format=None):
        data=request.data
        print(data)
        if "+" in str(data['contact']):
            data['contact']=str(data["contact"])[3:].replace(' ',"").replace("-","")
        contact = int(data["contact"])
        otp = int(data["otp"])
        print("OTP: ",otp)
        userdbobj=User.objects.get(contact=contact)
        availotp=userdbobj.otp
        if otp==availotp:
            response={"success":True}
            return Response(response,status.HTTP_200_OK)
        else:
            response={"success":False}
            return Response(response,status=status.HTTP_401_UNAUTHORIZED)


    
class UserProfileView(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except UserProfileSerializer.DoesNotExist:
            raise Http404

    
    def get(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = UserProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        profile = self.get_object(pk)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
