from . import views
from django.urls import path, include
from django.contrib.auth.views import LoginView
from .views import StaffView, CreatePatientView, CreateReportView, LogoutView, login_admin
from .forms import UserLoginForm
from .views import *

urlpatterns = [
    path('', views.home, name = 'covidyoddha-home'),
    path('about/', views.about, name = 'covidyoddha-about'),
    path('report/', views.report, name = 'covidyoddha-report'),
    path('print_report/', views.GeneratePdf,name = 'print-report'),
    path('patient_register/', patient_register, name='patient_register'),
    path('verify_patient_mobile/', verify_patient_mobile, name='verify_patient_mobile'),
]

urlpatterns += [
    #path('login/', LoginView.as_view(template_name="login.html",authentication_form=UserLoginForm), name='login'),
    path('account/', login_admin, name="login"),
    path('logout/', views.Logout, name='logout'),
    path('staff/', StaffView.as_view(), name='staff'),
    path('create_patient/', CreatePatientView.as_view(), name='createPatient'),
    path('create_report/', CreateReportView.as_view(), name='createReport'),

]
