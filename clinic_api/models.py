from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.db.models import Sum, F


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name for user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of user"""
        return self.email


# class ProfileFeedItem(models.Model):
#     """Profile status update"""
#     user_profile = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE
#     )
#     status_text = models.CharField(max_length=255)
#     created_on = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         """Return the model as a string"""
#         return self.status_text

class Clinic(models.Model):
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    contact_nr = models.IntegerField
    email = models.EmailField(max_length=20)
    website = models.CharField(max_length=20)

class Staff(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    position = models.CharField(max_length=20)
    contact_nr = models.IntegerField
    email = models.EmailField(max_length=20)

    def __str__(self):
        return self.first_name


class Patient(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField
    gender = models.CharField(max_length=20)
    contact_nr = models.IntegerField
    email = models.EmailField(max_length=20)
    problem = models.CharField(max_length=100)

    def __str__(self):
        return self.first_name


class Appointment(models.Model):
    staff = models.ForeignKey('clinic_api.Staff', on_delete=models.CASCADE)
    patient = models.ForeignKey('clinic_api.Patient', on_delete=models.CASCADE)
    service = models.ForeignKey('clinic_api.Service', on_delete=models.CASCADE)
    invoice = models.ForeignKey('clinic_api.Invoice', on_delete=models.CASCADE)
    date = models.DateField(max_length=20)
    time = models.TimeField(max_length=20)
    price = models.FloatField(max_length=20)

    def __str__(self):
        return self.date


class Service(models.Model):
    name = models.CharField(max_length=20)
    price = models.FloatField(max_length=20)


class Report (models.Model):
    appointment = models.ForeignKey('clinic_api.Appointment', on_delete=models.CASCADE)
    medication = models.CharField(max_length=50)
    comments = models.CharField(max_length=50)


class Invoice(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    patient = models.ForeignKey('clinic_api.Patient', on_delete=models.CASCADE)
    clinic = models.ForeignKey('clinic_api.Clinic', on_delete=models.CASCADE)
    # service = models.FloatField(default=0)
    # price = models.FloatField(default=0)
    #
    # @property
    # def total(self):
    #     return self.price * self.quantity
    #
    # def __str__(self):
    #     return f'{self.product} - {self.invoice}'
