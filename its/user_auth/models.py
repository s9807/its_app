"""
Models related to User and User permissions.
"""

from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractUser


class UserManager(BaseUserManager):

    def _create_user(self, email,password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if "first_name" not in extra_fields:
            raise ValueError("User must have a first_name")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_user(self, email,password=None,**extra_fields):
        """
        Method for creating a new normal user with role=ROLE_USER
        """
        extra_fields['is_staff'] = False
        extra_fields['is_superuser'] = False
        return self._create_user(email, password, **extra_fields)
        

    def create_superuser(self, email,password=None, **extra_fields):
        """
        Method for creating a Administrator with role=ROLE_ADMIN
        """
        extra_fields['role'] = "ROLE_ADMIN"
        extra_fields['is_superuser'] = True
        return self._create_user(email,password, **extra_fields)

class User(AbstractUser):

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name"]

    id = models.AutoField(primary_key=True,unique=True)
    username = models.CharField(max_length=200,null=True,blank=True)
    email = models.EmailField(('email address'), unique=True ,error_messages={
            'unique': ("A user with that username already exists."),
        }) # changes email to unique and blank to false
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    mobile = models.CharField(max_length=10)
    phone = models.CharField(max_length=10)
    role = models.CharField(max_length=20,null=True,blank=True)
    uu_id = models.UUIDField(db_index = True,default = None,editable = False,unique=True,null=True,blank=True)    

    objects = UserManager()
    def __str__(self):                                                       
        return self.email
