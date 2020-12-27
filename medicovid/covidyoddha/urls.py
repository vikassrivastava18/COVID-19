from . import views
from django.urls import path, include
from django.contrib.auth.views import LoginView
from .views import StaffView, CreatePatientView, CreateReportView, AppointmentSlot, PickTime, TakeAppointment
from .views import StaffView, CreatePatientView, CreateReportView, LogoutView, login_admin, PatientDelete, PatientUpdate, AppointmentView, AppointmentUpdate
from .forms import UserLoginForm
from .views import *

urlpatterns = [
    path('', views.home, name = 'covidyoddha-home'),
    path('about/', views.about, name = 'covidyoddha-about'),
    path('report/', views.report, name = 'covidyoddha-report'),
    path('print_report/', views.GeneratePdf,name = 'print-report'),
    path('patient_register/', patient_register, name='patient_register'),
    path('verify_patient_mobile/', verify_patient_mobile, name='verify_patient_mobile'),
    path('patientDelete/<pid>', PatientDelete, name = 'patientDelete'),
    path('patientUpdate/<pid>', PatientUpdate, name = 'patientUpdate'),
    path('appointmentDelete/<aid>', AppointmentDelete, name = 'appointmentDelete'),
    path('appointmentUpdate/<aid>', AppointmentUpdate, name = 'appointmentUpdate'),
# ]
#
# urlpatterns += [
    #path('login/', LoginView.as_view(template_name="login.html",authentication_form=UserLoginForm), name='login'),
    path('account/', login_admin, name="login"),
    path('logout/', views.Logout, name='logout'),
    path('staff/', StaffView.as_view(), name='staff'),
    path('create_patient/', CreatePatientView.as_view(), name='createPatient'),
    path('create_report/', CreateReportView.as_view(), name='createReport'),
    path('appointment/', AppointmentSlot.as_view(), name='appointment'),
    path('pick_time/', PickTime.as_view(), name='pick_time'),
    path('take_appointment/', TakeAppointment.as_view(), name='take_appointment'),
    path('appointmentList/', AppointmentView.as_view(), name='appointmentList'),

]
