from django.db import models
from AccountApp.models import Doctor, Patient
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.
class Appointment(models.Model):
    reason=models.TextField()
    prescription=models.FileField(
        blank=True,
        upload_to='prescriptions/'
    )


    class Status(models.TextChoices):
        PENDING = "PENDING","en attente"
        APPROVED = "CONFIRMED","confirmé"
        REJECTED = "CANCELLED","annulé"
    status=models.CharField(max_length=10,choices=Status.choices,default=Status.PENDING)
    duration_minutes=models.PositiveIntegerField(default=30)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    appointment_date=models.DateTimeField()
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name='appointments')
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE,related_name='appointments')
    
    def clean(self):
        modified_date = self._state.adding or (
            Appointment.objects.filter(
                pk=self.pk, appointment_date=self.appointment_date
            ).exists()
        )
        if modified_date and self.appointment_date <= timezone.now():
            raise ValidationError("La date du rdv doit être dupérieure a la date d'aujourdhui.")
        
    
    class Meta:
        ordering =["-appointment_date"]
        constraints=[
            models.UniqueConstraint(
                fields=["doctor","appointment_date"],
                name="unicite_patient-doctor-date",
                violation_error_message="ce docteur possede un rdv avec cette date"
            )
        ]

    def __str__(self):
        return f"le rdv est pour la raison {self.reason}"