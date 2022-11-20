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
        user = self.model(email=email, name=name)

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
    name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    contact_nr = models.CharField(null=True, max_length=20)
    email = models.EmailField(max_length=30, unique=True)
    position = models.ForeignKey('clinic_api.Position', null=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name for user"""
        return f"{self.name, self.last_name}"

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of user"""
        return self.email


class Clinic(models.Model):
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    contact_nr = models.CharField(max_length=20)
    email = models.EmailField(max_length=20)
    website = models.CharField(max_length=20)

    def __str__(self):
        """Return string representation of user"""
        return self.name


class Patient(models.Model):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('X', "Don't say")
    ]

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(max_length=20)
    gender = models.CharField( max_length=6, choices=GENDER_CHOICES , default='X')
    height = models.FloatField(default=0)
    weight = models.FloatField(default=0)
    contact_nr = models.CharField(max_length=20)
    email = models.EmailField(max_length=20)
    problem = models.CharField(max_length=100)

    @property
    def BMI(self):
        return self.weight / ((self.height / 100) ** 2)

    def __str__(self):
        """Return string representation of user"""
        return f"{self.first_name, self.last_name}"


class Appointment(models.Model):
    user = models.ForeignKey('clinic_api.UserProfile', on_delete=models.CASCADE)
    patient = models.ForeignKey('clinic_api.Patient', on_delete=models.CASCADE)
    service = models.ForeignKey('clinic_api.Service', on_delete=models.CASCADE)
    invoice = models.ForeignKey('clinic_api.Invoice', on_delete=models.CASCADE)
    date = models.DateField(max_length=20)
    time = models.TimeField(max_length=20)
    price = models.FloatField(default=0)
    quantity = models.FloatField(default=0)

    @property
    def total(self):
        return self.price * self.quantity

    def __str__(self):
        return f'{self.service} - {self.invoice}'


class Service(models.Model):
    name = models.CharField(max_length=20)
    price = models.FloatField(default=0)
    quantity = models.FloatField(default=0)

    def __str__(self):
        """Return string representation of user"""
        return self.name


class Report(models.Model):
    appointment = models.ForeignKey('clinic_api.Appointment', on_delete=models.CASCADE)
    medication = models.CharField(max_length=50)
    comments = models.CharField(max_length=50)

    def __str__(self):
        """Return string representation of user"""
        return str(self.appointment)


class Position(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        """Return string representation of user"""
        return self.name


class Invoice(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    patient = models.ForeignKey('clinic_api.Patient', on_delete=models.CASCADE)
    clinic = models.ForeignKey('clinic_api.Clinic', on_delete=models.CASCADE)

    @property
    def total(self):

        return {self.appointment_set.all().aggregate(total=Sum(F('quantity') * F('price')))}

    def __str__(self):
        return f'{self.patient} / {self.date}'
