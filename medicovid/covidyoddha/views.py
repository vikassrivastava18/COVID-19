from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.core.files import File
from .models import Patient, test_time_in_minute, hospital_close_at, hospital_opens_at, Appointment
from django.shortcuts import render, redirect, get_object_or_404
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
from django.views.generic import DeleteView
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

                sent_otp = send_otp('#', '#', msg_body,'+#','+91'+request_mobile)
                request.session["sent_otp"] = str(sent_otp)

                messages.success(request, f'Your OTP Send Successfully !!!')
                print(sent_otp)
            except Exception as e:
                print('error :->', e)
                messages.error(request, "Please check filling information again !!!")
                return render(request, "covidyoddha/home.html")


    return render(request, 'covidyoddha/home.html')


def report(request):
    try:
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
    except Exception as e:
        try:
            if request.session['otp_check']:
                return render(request, 'covidyoddha/report.html')
        except Exception as e:
            print('Error:->', e)
            messages.error(request, f'OPPS!, Something Went Wrong. Please Generate OTP Again.')
            return render(request, 'covidyoddha/home.html')
        print('Error:->', e)
        messages.error(request, f'OPPS!, Something Went Wrong. Please Generate OTP Again.')
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

    def get(self, request, *args, **kwargs):

        patient_list = Patient.objects.all()
        #print("patient_list",patient_list)
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
            sent_otp = send_otp('#', '#', msg_body,
                                '+#', '+91' + contact)
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

# class PatientDeleteView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#
#         patient = get_object_or_404(Patient, id=kwargs["pid"])
#         print("patient:->",patient)
#         #patient.delete()
#         return redirect('staff')

@login_required
def PatientDelete(request,pid):
    # patient = Patient.objects.get(id = pid)
    # print("patient:->",patient)
    # #patient.delete()
    # return redirect('staff')

    patient = get_object_or_404(Patient, id=pid)
    if request.method == 'POST':
        patient_first_name = patient.patient_first_name
        if request.user.is_staff and request.user.is_superuser and request.user.is_active:
            patient.delete()
            messages.success(request, f'Patient { patient_first_name } deleted Successfully. Thank You!!!')
            return redirect('staff')
        else:
            messages.warning(request, f'You do not have permission to delete this patient. Thank You!!!')
            return redirect('staff')
    else:
        context = {}
        context['patient'] = patient
        return render(request, 'covidyoddha/patientDelete.html', context)

@login_required
def PatientUpdate(request,pid):
    patient = get_object_or_404(Patient, id=pid)
    if request.method == 'POST':
        patient = get_object_or_404(Patient, id=pid)
        p_form = PatientCreationForm(request.POST, instance=patient)
        patient_first_name = patient.patient_first_name
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Information updated for patient : { patient_first_name }. Thank You!!!')
            return redirect('staff')

    else:
        p_form = PatientCreationForm(instance=patient)

    context = {
        'p_form': p_form,
        'patient':patient
    }

    return render(request, 'covidyoddha/patientUpdate.html', context)

class AppointmentSlot(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'appointment.html')


class PickTime(LoginRequiredMixin, View):
    def get(self, request):
        date = request.GET['pick_date']
        mobile = request.GET['mobile']
        patient = get_object_or_404(Patient, patient_mobile=mobile)
        request.session['patient'] = patient.id
        date_dt1 = datetime.strptime(date, '%Y-%m-%d')
        print("date_dt1:->",date_dt1)
        booked_slots_query = Appointment.objects.all()
        print("booked_slots_query:->",booked_slots_query)
        booked_slots = []
        for slot in booked_slots_query:
            print(slot.time)
            hour = slot.time.hour
            min = slot.time.minute
            print("hour:->",hour,"minutes:->",min)
            booked_slots.append({'hour':hour, 'min':min})
        available_slots = []

        total_slots_count = (abs(hospital_close_at - hospital_opens_at) * (60 / test_time_in_minute))
        print('total_slots_count', total_slots_count)
        for i in range(int(total_slots_count)):
            slot_hour = hospital_opens_at + i // 4
            slot_min = 15 * (i % 4)
            slot = {'hour':slot_hour, 'min':slot_min}
            if slot not in booked_slots:
                available_slots.append(slot)
        context = {
            'available_slots': available_slots,
            'date_picked': True,
            'date': date
        }
        return render(request, 'appointment.html', context)


class TakeAppointment(LoginRequiredMixin, View):
    def post(self, request):
        date_time = request.POST['pick_time']
        datetime_list = date_time.split(' ')
        date = datetime_list[1]
        y_m_d = date.split('-')
        year = int(y_m_d[0])
        month = int(y_m_d[1])
        day = int(y_m_d[2])
        hour = int(datetime_list[0].split('-')[0])
        min = int(datetime_list[0].split('-')[1])
        datetime_appointment = datetime(year, month, day, hour, min)
        patient = Patient.objects.get(id=request.session['patient'])
        fix_appointment = Appointment.objects.create(patient=patient, time=datetime_appointment)
        return redirect('staff')