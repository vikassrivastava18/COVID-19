from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import PatientCreationForm, ReportCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

# Create your views here.


class StaffView(LoginRequiredMixin, View):

    def get(self, request):
        form_dict = {
            'patientForm': PatientCreationForm()
        }
        return render(request, 'staff.html', form_dict)


class CreatePatientView(LoginRequiredMixin, CreateView):
    form_class = PatientCreationForm
    template_name = "addPatient.html"
    success_url = reverse_lazy('staff')


class CreateReportView(LoginRequiredMixin, CreateView):
    form_class = ReportCreationForm
    template_name = "addReport.html"
    success_url = reverse_lazy('staff')
    # def valid