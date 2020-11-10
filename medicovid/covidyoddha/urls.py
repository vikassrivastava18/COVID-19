from django.urls import path, include
from django.contrib.auth.views import LoginView
from .views import StaffView, CreatePatientView, CreateReportView
from .forms import UserLoginForm

urlpatterns = [
    path('login/', LoginView.as_view(template_name="login.html",
                                     authentication_form=UserLoginForm), name='login'),
    path('staff/', StaffView.as_view(), name='staff'),
    path('create_patient/', CreatePatientView.as_view(), name='createPatient'),
    path('create_report/', CreateReportView.as_view(), name='createReport'),
]
