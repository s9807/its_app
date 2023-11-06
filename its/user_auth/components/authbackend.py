"""
This is just to add email field as
authentication source.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import BCryptSHA256PasswordHasher
import bcrypt
from django.utils.crypto import constant_time_compare

UserModel = get_user_model()


class CustomUserModelBackend(ModelBackend):
    """
    Custom User Model backend for authenticating users.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD, kwargs.get(UserModel.EMAIL_FIELD))
        if username is None or password is None:
            return
        try:
            user = UserModel._default_manager.get(
                Q(username__exact=username) | (Q(email__iexact=username))
            )
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if 'bcrypt_sha256' not in user.password:
                user.password = "%s$%s" % ('bcrypt_sha256', user.password)# Adding algorithm name as prefix in the password in order to avoid the algoritm checks.
            if user.check_password(password) and self.user_can_authenticate(user):
                return user



class CustomPasswordHasher(BCryptSHA256PasswordHasher):
    """
    Custom password hashing ................
    This is implemented in order to remove algoritm name 
    as prefix in the password .
    
    """

    rounds = 10
    algorithm = "bcrypt_sha256"


    def salt(self):
        """
        Method for generating salt for password hashing algorithm.
        """
        return bcrypt.gensalt(self.rounds,b"2a")

    def encode(self, password, salt):
        """
        Method for hashing the password

        .. code::python

            password = password.encode()
            data = bcrypt.hashpw(password, salt)

        """
        password = password.encode()
        data = bcrypt.hashpw(password, salt)
        return  data.decode("ascii")

    # def must_update(self, encoded):
    #     """
    #     Method for updating the passwords
    #     """
    #     return True

    def verify(self, password, encoded):
        """
        Method for verifying the password stored in the database 
        and the password recieved in the input

        .. code::python 

            algorithm, data = encoded.split("$", 1)
            assert algorithm == self.algorithm
            encoded_2 = self.encode(password, data.encode("ascii"))
            encoded_2 = "%s$%s" % ('abcd', encoded_2)  
            return constant_time_compare(encoded, encoded_2)
        """
        algorithm, data = encoded.split("$", 1)
        assert algorithm == self.algorithm
        encoded_2 = self.encode(password, data.encode("ascii"))
        encoded_2 = "%s$%s" % (algorithm, encoded_2)  
        return constant_time_compare(encoded, encoded_2)