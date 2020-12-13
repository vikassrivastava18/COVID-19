from . import views
from django.urls import path, include
from django.contrib.auth.views import LoginView
from .views import StaffView, CreatePatientView, CreateReportView, AppointmentSlot, PickTime, TakeAppointment
from .forms import UserLoginForm

urlpatterns = [
    path('', views.home, name = 'covidyoddha-home'),
    path('about/', views.about, name = 'covidyoddha-about'),
    path('report/', views.report, name = 'covidyoddha-report'),
    path('print_report/', views.GeneratePdf,name = 'print-report'),
]

urlpatterns += [
    path('login/', LoginView.as_view(template_name="login.html",
                                     authentication_form=UserLoginForm), name='login'),
    path('staff/', StaffView.as_view(), name='staff'),
    path('create_patient/', CreatePatientView.as_view(), name='createPatient'),
    path('create_report/', CreateReportView.as_view(), name='createReport'),
    path('appointment/', AppointmentSlot.as_view(), name='appointment'),
    path('pick_time/', PickTime.as_view(), name='pick_time'),
    path('take_appointment/', TakeAppointment.as_view(), name='take_appointment')
]
