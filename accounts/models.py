from phonenumber_field.modelfields import PhoneNumberField # for phone number
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager ## Two new classes are imported. ##

# https://www.fomfus.com/articles/how-to-use-email-as-username-for-django-authentication-removing-the-username
# https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#auth-custom-user
# https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#custom-users-and-proxy-models
# https://medium.com/agatha-codes/options-objects-customizing-the-django-user-model-6d42b3e971a4

class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, phone_number,dob, **extra_fields):
        """Create and save a User with the given email and password, dob, phone_number ."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.phone_number = phone_number
        user.dob = dob
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, phone_number, dob, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, dob, phone_number, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, dob = 'null', phone_number = 'null', **extra_fields)



class CustomUser(AbstractUser):

# """
# All you have to do is add AUTH_USER_MODEL to settings with path to custom user class, which extends either
# AbstractBaseUser (more customizable version) or AbstractUser (more or less old User class you can extend).
# You are:
# Extending the base class that Django has for User models.
# Removing the username field.
# Making the email field required and unique.
# Telling Django that you are going to use the email field as the USERNAME_FIELD.
# Removing the email field from the REQUIRED_FIELDS settings (it is automatically included as USERNAME_FIELD)."""
    username = None
    email = models.EmailField(verbose_name='email dob', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

# DONE
# Now, add more field
    # https://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-phone-number-in-django-models
    # https://pypi.org/project/django-phonenumber-field/
    phone_number = PhoneNumberField(null=False, blank=False)
    dob = models.DateField()

    objects = CustomUserManager() ## This is the new line in the User model. ##
