from django.contrib import admin

from .models import *
# Register your models here.

#admin.site.register(Patient)
@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id',  'patient_first_name', 'patient_last_name', 'patient_mobile','patient_email','patient_age','patient_gender')
    ordering = ['-id']

#admin.site.register(Report)
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('patient', 'result', 'file','date')

#admin.site.register(Appointment)
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'time')