from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

GENDER = (
             ('M', 'Male'),
             ('F','Female'),
             ('O', 'Other'),
)

class Patient(models.Model):
    patient_first_name = models.CharField(max_length=100)
    patient_last_name = models.CharField(max_length=100)
    patient_mobile = models.CharField(max_length=13)
    patient_email = models.EmailField(null=True)
    patient_age = models.IntegerField()
    patient_gender = models.CharField(
        max_length=1,
        choices= GENDER,
        help_text='Please select your Gender'
    )

    def __str__(self):
        return self.patient_first_name


RESULT = (
    ('h', 'hold'),
    ('p', 'positive'),
    ('n', 'negative')
)


class Report(models.Model):
    report_id = models.UUIDField(primary_key=True, default=uuid.uuid1,
                                 help_text='Unique ID for this particular report')

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    result = models.CharField(
        max_length=1,
        default= 'h',
        help_text = 'Status of the report',
        choices= RESULT
    )
    file = models.FileField(upload_to='report/')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.result


class Staff(models.Model):
    staff = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13)

    def __str__(self):
        return self.staff.username


test_time_in_minute = 15   #15 Minutes
hospital_opens_at = 10   # 10 am
hospital_close_at = 18      # 6 pm


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete= models.SET_NULL, null=True)
    time = models.DateTimeField()

    # def __str__(self):
    #     return self.time
