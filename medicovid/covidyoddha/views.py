from django.contrib.auth.views import LogoutView
from django.core.files import File
from django.shortcuts import render, redirect
from .models import Patient
from .otp import send_otp , otp
from django.contrib import messages, auth
from django.contrib.auth import settings
from django.http import HttpResponse
from .utils import render_to_pdf
from datetime import datetime
from django.db.models import Q
from io import BytesIO
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import PatientCreationForm, ReportCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout

def home(request):
    if request.method == 'POST':
        request_firstname = request.POST['firstname']
        request_lastname = request.POST['lastname']
        #request_patient_name = request_firstname + ' '+ request_lastname
        request_mobile = request.POST['inputMobile']
        patient = Patient.objects.filter(patient_mobile=str(request_mobile)) and Patient.objects.filter(Q(patient_first_name__icontains=request_firstname)) and Patient.objects.filter(Q(patient_last_name__icontains=request_lastname)).first()
        print(patient)
        if patient == None:
            messages.error(request, f'OPPS!, That mobile number is not registered.')
            return render(request, 'covidyoddha/home.html')

        else:
            try:
                request.session["patient_first_name"] = patient.patient_first_name
                patient_first_name = patient.patient_first_name
                request.session["patient_last_name"] = patient.patient_last_name
                patient_last_name = patient.patient_last_name
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
                Hello Mr. { patient_first_name } { patient_last_name } Your Secure Device OTP is - {otp}
                '''

                sent_otp = send_otp('#', '#', msg_body,'#','+91'+request_mobile)
                request.session["sent_otp"] = str(sent_otp)

                messages.success(request, f'Your OTP Send Successfully !!!')
                print(sent_otp)
            except Exception as e:
                print('error :->', e)
                messages.error(request, "Please check filling information again !!!")
                return render(request, "covidyoddha/home.html")


    return render(request, 'covidyoddha/home.html')


def report(request):

    patient_first_name = request.session['patient_first_name']
    patient_last_name = request.session['patient_last_name']
    patient_email = request.session['patient_email']
    patient_mobile = request.session['patient_mobile']
    patient_age = request.session['patient_age']
    patient_gender = request.session['patient_gender']

    context = {
        'patient_first_name':patient_first_name,
        'patient_last_name': patient_last_name,
        'patient_email':patient_email,
        'patient_mobile':patient_mobile,
        'patient_age':patient_age,
        'patient_gender':patient_gender,
    }
    if request.method == 'POST':
        patient_otp = request.POST['inputOTP']
        #print(patient_otp , request.session['sent_otp'])
        try:
            if patient_otp == request.session['sent_otp']:
                request.session['otp_check'] = True
                messages.success(request, f'OTP Verified Successfully. Thank you !!!')
                return render(request, 'covidyoddha/report.html', context)
        except Exception as e:
            print('Error:->',e)
            messages.error(request, f'OPPS!, OTP Not Matched. Please Check OTP Again.')
            return render(request, 'covidyoddha/home.html')
    if request.session['otp_check']:
        return render(request, 'covidyoddha/report.html',context)
    else:
        return render(request, 'covidyoddha/home.html')

def GeneratePdf(request):
    patient_first_name = request.session['patient_first_name']
    patient_last_name = request.session['patient_last_name']
    patient_email = request.session['patient_email']
    patient_mobile = request.session['patient_mobile']
    patient_age = request.session['patient_age']
    patient_gender = request.session['patient_gender']

    context = {
        'patient_first_name':patient_first_name,
        'patient_last_name': patient_last_name,
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
        patient_list = Patient.objects.all()
        print("patient_list",patient_list)
        form_dict = {
            'patientForm': PatientCreationForm(),
            'patient_list': patient_list,
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


def login_admin(request):
    if request.method == "POST":
        u = request.POST["username"]
        p = request.POST["password"]
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                messages.success(request,"Logged In Successfully !!!")
                return redirect('staff')
            else:
                messages.error(request, "Invalid Login Credentials, Please try Again.")
                #return render(request, 'login_admin.html')
        except:
            messages.error(request, "Something Went Wrong, Please try Again.")
            return render(request, 'covidyoddha/login.html')

    return render(request, 'covidyoddha/login.html')


def patient_register(request):

    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        emailid = request.POST['emailid']
        contact = request.POST['contact']
        age = request.POST['age']
        gender = request.POST['gender']

        request.session["patient_first_name"] = firstname
        patient_first_name = firstname
        request.session["patient_last_name"] = lastname
        patient_last_name = lastname
        request.session["patient_email"] = emailid
        patient_email = emailid
        request.session["patient_mobile"] = contact
        patient_mobile = contact
        request.session["patient_age"] = age
        patient_age = age
        request.session["patient_gender"] = gender
        patient_gender = gender

        context = {
            'patient_first_name': patient_first_name,
            'patient_last_name': patient_last_name,
            'patient_email': patient_email,
            'patient_mobile': patient_mobile,
            'patient_age': patient_age,
            'patient_gender': patient_gender,
        }
        try:
            msg_body = f'''
                        Thank you For Using Covid-Yoddha Website !
                        Hello {firstname} {lastname} Your Secure Device OTP is - {otp}
                        '''
            sent_otp = send_otp('AC2ada64bbf0631ec1ec778efcb405c1b3', '818440649467b203ce7a7115584aca89', msg_body,
                                '+14158775175', '+91' + contact)
            request.session["sent_otp"] = str(sent_otp)
            print(sent_otp)

            messages.success(request, f'Your OTP Send Successfully !!!')
            return render(request, 'covidyoddha/patient_register.html',context)

        except Exception as e:
            print('error :->', e)
            messages.error(request, "This is not a valid mobile number, Please Try Again.")
            return render(request, "covidyoddha/patient_register.html", context)

    return render(request, 'covidyoddha/patient_register.html')

def verify_patient_mobile(request):
    try:
        firstname = request.session['patient_first_name']
        lastname = request.session['patient_last_name']
        emailid = request.session['patient_email']
        contact = request.session['patient_mobile']
        age = request.session['patient_age']
        gender = request.session['patient_gender']

        context = {
            'patient_first_name': firstname,
            'patient_last_name': lastname,
            'patient_email': emailid,
            'patient_mobile': contact,
            'patient_age': age,
            'patient_gender': gender
        }

        if request.method == 'POST':
            patient_otp = request.POST.get('inputOTP')


            print(patient_otp, request.session['sent_otp'])
            if patient_otp == request.session['sent_otp']:
                patient = Patient.objects.create(patient_first_name=firstname,
                                                 patient_last_name=lastname,
                                                 patient_email=emailid,
                                                 patient_mobile=contact,
                                                 patient_age=age,
                                                 patient_gender=gender)
                patient.save()
                messages.success(request, f'Registration Successfully Done. Thank you !!!')
                return render(request, 'covidyoddha/home.html',context)
            else:
                messages.error(request, "This is not a valid mobile number, Please Try Again.")
                return render(request, 'covidyoddha/home.html',context)
    except Exception as e:
        print('error :->', e)
        messages.error(request, "OPS! OTP is not correct, Please Try Again.")
        return render(request, "covidyoddha/patient_register.html")

    return render(request, "covidyoddha/patient_register.html",context)

def Logout(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('login')



