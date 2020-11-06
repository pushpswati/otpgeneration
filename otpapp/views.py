from django.http import Http404

from jwtotp import settings
from . import models
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserSerializer,UserProfileSerializer,UserFileViewSerializer
import random
import json
import jwt
import os
import sys
import uuid
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import FileUploadParser, MultiPartParser
from . import jwtToken

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
            jwtvar= jwtToken.Jwt.jwtsignature(contact)
            userdbobj.token=jwtvar
            userdbobj.save()
            response={"success":True,"token":jwtvar}
            return Response(response,status.HTTP_200_OK)
        else:
            response={"success":False}
            return Response(response,status=status.HTTP_401_UNAUTHORIZED)

# def jwtsignature(self,contact):
#
#    encoded_jwt = jwt.encode({'contact': contact}, 'secret', algorithm='HS256')
#       response={'token':encoded_jwt}
#       return response
    
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
    
class UserFileView(APIView):
    """
    Upload flle upload view for FileUpload model
    """
    parser_classes = (MultiPartParser,)
    def post(self, request, format=None):
        """

        :param request:
        :param format:
        :return:
        """
        #try:
        file_name = request.data["file_name"]

        # token = request.META['HTTP_X_HEADER_TOKEN']
        # payload = jwtsignature().authenticate_credentials(token)
        # print("payload", payload)
        #if payload:
        #userobj=User.objects.get(contact=contact)
        data = request.data
        print(data,"kya data")
        contact = int(data["contact"])
        print(contact,"contact")
        user = models.User.objects.get(contact=contact)
        print(user,"user...")
        doc_obj=models.Media.objects.create(user=user,
                                                   file_name=file_name)
        doc_obj.save()
        file_url=str(doc_obj.file_name)

        RESPONSE = {'success': True,
            'response': {'file_name': file_url}}
        return Response(json.dumps(RESPONSE), status=status.HTTP_200_OK)



            #return Response(BEDRESPONSE, status=status.HTTP_401_UNAUTHORIZED)

        # except Exception as e:
        #     exc_type, exc_obj, exc_tb = sys.exc_info()
        #     print(sys.exc_info())
        #     BEDRESPONS = {'success': False,
        #     'response': str(sys.exc_info())}
        #     return Response(json.dumps(BEDRESPONS), status=status.HTTP_400_BAD_REQUEST)
