from django.core.files import File
from django.shortcuts import render, redirect
from .models import Patient
from .otp import send_otp , otp
from django.contrib import messages
from django.contrib.auth import settings
from django.http import HttpResponse
from .utils import render_to_pdf
from datetime import datetime
from io import BytesIO
# from .forms import mobileOTPForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import PatientCreationForm, ReportCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy


# yoddha = [
#
#     {
#         'name': 'Vikas',
#         'title': 'Covid Yoddha 1',
#         'content': 'Some little help from our side to Medical team',
#         'date':'Octobar 23, 2020'
#     },
#     {
#         'name': 'Datta',
#         'title': 'Covid Yoddha 2',
#         'content': 'My little contribute to Medical team',
#         'date':'Octobar 24, 2020'
#     }
# ]



def home(request):
    #patient = Patient.objects.all()
    if request.method == 'POST':
        request_mobile = request.POST['inputMobile']
        patient = Patient.objects.filter(patient_mobile=str(request_mobile)).first()

        if patient == None:
            messages.error(request, f'OPPS!, That mobile number is not registered.')
            return render(request, 'covidyoddha/home.html')

        else:
            request.session["patient_name"] = patient.patient_name
            patient_name = patient.patient_name
            request.session["patient_email"] = patient.patient_email
            patient_email = patient.patient_email
            request.session["patient_mobile"] = patient.patient_mobile
            patient_mobile = patient.patient_mobile
            request.session["patient_age"] = patient.patient_age
            patient_age = patient.patient_age
            request.session["patient_gender"] = patient.patient_gender
            patient_gender = patient.patient_gender

            msg_body = f'''
            Thank you For Using Covid-Yoddha Website !
            Hello Mr. { patient_name } Your Secure Device OTP is - {otp}
            '''
            sent_otp = send_otp('#', '#', msg_body,'+#','+91'+request_mobile)
            request.session["sent_otp"] = str(sent_otp)

            messages.success(request, f'Your OTP Send Successfully !!!')
            print(sent_otp)

    return render(request, 'covidyoddha/home.html')


def report(request):

    patient_name = request.session['patient_name']
    patient_email = request.session['patient_email']
    patient_mobile = request.session['patient_mobile']
    patient_age = request.session['patient_age']
    patient_gender = request.session['patient_gender']

    context = {
        'patient_name':patient_name,
        'patient_email':patient_email,
        'patient_mobile':patient_mobile,
        'patient_age':patient_age,
        'patient_gender':patient_gender,
    }
    if request.method == 'POST':
        patient_otp = request.POST['inputOTP']
        print(patient_otp , request.session['sent_otp'])

        if patient_otp == request.session['sent_otp']:
            request.session['otp_check'] = True
            messages.success(request, f'OTP Verified Successfully. Thank you !!!')
            return render(request, 'covidyoddha/report.html', context)
        else:
            messages.error(request, f'OPPS!, OTP Not Matched. Please Check OTP Again.')
            return render(request, 'covidyoddha/home.html')
    if request.session['otp_check']:
        return render(request, 'covidyoddha/report.html',context)
    else:
        return render(request, 'covidyoddha/home.html')

def GeneratePdf(request):

    patient_name = request.session['patient_name']
    patient_email = request.session['patient_email']
    patient_mobile = request.session['patient_mobile']
    patient_age = request.session['patient_age']
    patient_gender = request.session['patient_gender']

    context = {
        'patient_name': patient_name,
        'patient_email': patient_email,
        'patient_mobile': patient_mobile,
        'patient_age': patient_age,
        'patient_gender': patient_gender,
        'today':datetime.now()
    }
    pdf = render_to_pdf('covidyoddha/print_report.html', context)

    return HttpResponse(pdf, content_type='application/pdf')


def about(request):
    return render(request, 'covidyoddha/about.html', { 'title' : 'About'})


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


