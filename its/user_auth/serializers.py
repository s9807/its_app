from .models import *
from rest_framework import serializers
from uuid import uuid4
from rest_framework import status
from django.db import transaction
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password
import re

def check_valid_password(password):
    """
    This function is for password restrictions.
    """
    if (len(password)<1 or len(password)>50):
        return False
    elif not re.search("[a-z]",password):
        return False
    elif not re.search("[0-9]",password):
        return False
    elif not re.search("[A-Z]",password):
        return False
    elif not re.search("[!@#$%^&*())_+$#@]",password):
        return False
    elif re.search("\s",password):
        return False
    else:
        return True

class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer
    """
    name_regex = "^[a-zA-Z]([\\s](?![\\s])|[a-zA-Z]){1,30}[a-zA-Z]$"
    name_validator = RegexValidator(regex = name_regex, message = "Enter a valid username")
    # permissions = PermissionSerializer() # Nested use of serializers...
    password = serializers.JSONField(required=True)
    email = serializers.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['first_name',"last_name","password",'last_login', 'email','id','is_active','mobile','phone','role']

    def validate_email(self,email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")
        return email
    
    def validate(self, data):

        data["uu_id"] = str(uuid4()).replace('-','') # add uuid to the new user 
        # data['name'] = data['name'].lower() # user name is always in lowercase
        data['is_staff'] = True
        if not check_valid_password(data['password']): # For password validation
            raise serializers.ValidationError("The password must contain a minimum of 8 characters, a minimum of 1 uppercase, a minimum of 1 lowercase, a minimum of 1 special character, and 1 number" , code = "abcd")
        return data
    
    
    def to_representation(self, instance):
        """
        In built serializer method which creates the representation of
        the queryset object.
        """
        representation = super().to_representation(instance)
        representation.pop('password', None)# Exclude the 'password' field from the serialized data
        return representation
    
    
    def create(self, validated_data):
        """
        Create or update the user details in the database.
        """  
    
        with transaction.atomic():    
            if validated_data['role'] == "ROLE_ADMIN": # Condition for creating admin role
                user = User.objects.create_superuser(**validated_data)

        with transaction.atomic():   
            user = User.objects.create_user(**validated_data)
            return user       


class EditUserSerializer(serializers.ModelSerializer):
    # permissions = PermissionSerializer() # Nested use of serializers...
    password = serializers.JSONField(required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ['first_name','last_name', 'last_login', 'email','id','is_active','password','mobile','phone','role']


    def check_required_fields(self,data):
        """
        This method can initially get the data from frontend &
        we add a key into permission_data as name 'operation_'
        if during updation of data we can restrict email updation & 
        rest of details will be uudated except email .

        .. code-block:: python

            if 'permissions' not in data:
                return {"msg": "persmissions keyword is missing"}
            if 'password' not in data:
                return {"msg": "password keyword is missing"}
            if 'is_active' not in data:
                return {"msg": "is_active keyword is missing"}
            if 'name' not in data:
                return {"msg": "name keyword is missing"}
            return None

        .. note::This method is deprecated.    
        """
        if 'permissions' not in data:
            return {"msg": "persmissions keyword is missing"}
        if 'password' not in data:
            return {"msg": "password keyword is missing"}
        if 'is_active' not in data:
            return {"msg": "is_active keyword is missing"}
        if 'first_name' not in data:
            return {"msg": "first_name keyword is missing"}
        return None    
    
    def validate_email(self,email):
        pk = self.context.get('request').parser_context.get('kwargs').get('pk')
        if email.lower() != User.objects.filter(id=pk).values()[0]['email']:
            raise serializers.ValidationError("Email can not be updated")
        return email
    
    def validate_password(self, password):
        if check_valid_password(password): # For password validation
            password = make_password(password)
        else:
            raise serializers.ValidationError("Please enter valid password/Password must be a combination of uppercase, lowercase, special character and a digit")
        return password
    

    def validate(self, data):
        pk = self.context.get('request').parser_context.get('kwargs').get('pk')
        # data['name'] = data['name'].lower() # user name is always in lowercase
        data['is_staff'] = True
        data['email_verified'] = True
        return data

    
    def to_representation(self, instance):
        """
        In built serializer method which creates the representation of
        the queryset object.
        """
        representation = super().to_representation(instance)
        representation.pop('password', None)# Exclude the 'password' field from the serialized data
        return representation
     
        
    def update(self,instance,validated_data):
        """
        This method is to update the resource details in the database
        """      
        return super().update(instance,validated_data)
