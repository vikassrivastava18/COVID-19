from django.core.files import File
from django.shortcuts import render
from .models import Patient
from .otp import send_otp , otp
from django.contrib import messages
from django.contrib.auth import settings
from django.http import HttpResponse
from .utils import render_to_pdf
from datetime import datetime
from io import BytesIO


def home(request):
    if request.method == 'POST':
        request_mobile = request.POST['inputMobile']
        patient = Patient.objects.filter(patient_mobile=str(request_mobile)).first()
        print(patient)
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
            print(msg_body)
            sent_otp = send_otp('AC454eb3b87b77a6113b0cbe038d71f699', '2e133945b41c8443a99dcc98dcb15def', msg_body,'+13158190802','+91'+request_mobile)
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