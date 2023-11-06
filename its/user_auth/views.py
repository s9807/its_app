"""
Views regarding user creation and updation.
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import logging,string,random
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,UpdateAPIView,RetrieveUpdateAPIView,ListAPIView
from django.contrib.auth.hashers import make_password
import random
from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend
from django.http import HttpResponse
from uuid import uuid4
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken



def secret_key(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class CreateUser(CreateAPIView):
    """
    This class view is for creating a new user.

    For creating a new user you need to
    send the data in the json format just like

    .. code-block:: json

        {
            "email":"sam@mail.com",
            "name":"Sammy",
            "password":"sam123"
        }


    **Parameters**

    .. code-block:: json

        {
        "in": requestbody
        "name": email
        "type": str
        "required": true
        "description": user email.

        "name": name
        "type": str
        "required": true
        "description": user name.

        "in": requestbody
        "name": password
        "type": str
        "required": true
        "description": user password.
        }


    **Returns**

        status_code : 201 CREATED
        
        .. code-block:: json

            {
            "id": 6,
            "last_login": null,
            "is_superuser": false,
            "is_staff": true,
            "is_active": true,
            "date_joined": ,
            "username": null,
            "email": "raj.sandip2962@gmail.com",
            "name": "sandeep kr2",
            "password": "Bcrypt password",
            "role": null,
            "email_verified": true,
            "groups": [],
            "user_permissions": []
            }
    """
    # permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    

class UserRetrieveUpdateView(RetrieveUpdateAPIView):
    """
    For updating the user details.

    This class view updates the User details
    in the user table.
    """
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'
    serializer_class = EditUserSerializer
    queryset = User.objects.all()
    


class ResetPassword(APIView):
    """
    This API View is reseting the user password
    in the user table.

    The password gets changed if the user wants to 
    change the old password.

    .. code-block:: python

        User.objects.filter(email=email).update(password=make_password(password))
    """

    def put(self, request):
        data = request.data
        email = data['email']
        password = data['password']
        User.objects.filter(email=email).update(password=make_password(password))
        return Response({"msg":"Password updated"},status=status.HTTP_200_OK)

class LogoutView(APIView):
    def post(self,request):
        """
        Used for blacklist the token.
        """
        refresh_token = request.data.get("refresh")
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"msg":"Successfully logged out"},status=status.HTTP_200_OK)

class UserListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.filter(role="ROLE_USER")
