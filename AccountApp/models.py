from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
# Create your models here.


class Specialty(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    doctors = models.ManyToManyField(
        "AccountApp.Doctor",
    )

class User(AbstractUser):
    pass

class Doctor(User):
    license_number = models.CharField(max_length=6, unique=True,validators=[MinLengthValidator(6), MaxLengthValidator(6)])
    phone = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    specialities=models.ManyToManyField(
        Specialty,
        related_name='doctors',
    )

number_validator = RegexValidator(r'^\d{8}$', message='le numero de telephone doit contenir exactement 8 chiffres.')
def validate_date_of_birth(v):
    if v > timezone.now().date():
        raise ValidationError("La date de naissance ne peut pas être dans le futur.")

class Patient(User):
    national_id = models.CharField(max_length=8, unique=True,validators=[number_validator])
    phone = models.CharField(max_length=8,validators=[number_validator])
    birth_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    