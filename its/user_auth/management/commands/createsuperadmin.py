from django.core.management.base import BaseCommand as CreatesuperuserCommand
from uuid import uuid4
from django.core.exceptions import ValidationError
from django.conf import settings
from user_auth.models import User
from django.db import transaction


class Command(CreatesuperuserCommand):
    def handle(self, *args, **options):
        super_user = {}
        super_user['username'] = settings.DJANGO_SUPERUSER_USERNAME
        super_user['first_name'] = settings.DJANGO_SUPERUSER_NAME
        super_user['last_name'] = settings.DJANGO_SUPERUSER_NAME
        super_user['password'] = settings.DJANGO_SUPERUSER_PASSWORD
        super_user['email'] = settings.DJANGO_SUPERUSER_EMAIL
        super_user['is_active'] = settings.DJANGO_SUPERUSER_IS_ACTIVE
        super_user['role'] = settings.DJANGO_SUPERUSER_ROLE
        super_user['uu_id'] = str(uuid4()).replace('-','') # add uuid to the new user 

        # Custom email validation
        if "email" not in super_user:
            raise ValidationError('Email must be provided')
        if "password" not in super_user:
            raise ValidationError('Password must be provided')
        with transaction.atomic():
            User.objects.create_superuser(**super_user)
        return "SuperAdmin created successfully"