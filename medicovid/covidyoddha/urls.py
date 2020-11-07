from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name = 'covidyoddha-home'),
    path('about/', views.about, name = 'covidyoddha-about'),
    path('report/', views.report, name = 'covidyoddha-report'),
    path('print_report/', views.GeneratePdf,name = 'print-report'),
]