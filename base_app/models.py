from django.db import models
from django.contrib.auth.models import User


class Rehabilitator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(blank='', default='')

    def __str__(self):
        return 'Rehabilitant: %s' % self.user.username


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(blank='', default='')


class Visit(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)
    accepted = models.BooleanField(default=False)
    rehabilitator = models.ForeignKey(Rehabilitator, on_delete=models.CASCADE)
    patient_feedback = models.TextField(blank=True, default='')
