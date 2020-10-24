from django.db import models
from django.contrib.auth.models import User
# Create your models here.

GENDER = (
             ('M', 'Male'),
             ('F','Female'),
             ('O', 'Other'),
)

class Patient(models.Model):
    patient = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    patient_name = models.CharField(max_length=200)
    patient_mobile = models.CharField(max_length=13)
    patient_email = models.EmailField()
    patient_age = models.IntegerField()
    patient_gender = models.CharField(
        max_length=1,
        choices= GENDER,
        help_text='Please select your Gender'
    )

    def __str__(self):
        return self.patient_name

RESULT = (
    ('h', 'hold'),
    ('p', 'positive'),
    ('n', 'negative')
)

class Report(models.Model):
    report_id = models.CharField(max_length=64, primary_key=True, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    result = models.CharField(
        max_length=1,
        default= 'h',
        help_text = 'Status of the report',
        choices= RESULT
    )
    file = models.FileField(upload_to='media/report')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.result

class Staff(models.Model):
    staff = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13)

    def __str__(self):
        return self.staff.username