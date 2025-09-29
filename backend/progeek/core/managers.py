from django.contrib.auth.models import BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email=None, password=None, registration_code=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        # Accept registration_code from extra_fields if not passed directly
        if not extra_fields.get('is_superuser', False):
            if not registration_code:
                registration_code = extra_fields.get('registration_code')
            if not registration_code:
                raise ValueError('Registration code is required for normal users.')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, registration_code=registration_code, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
