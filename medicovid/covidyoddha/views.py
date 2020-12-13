from django.core.files import File
from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient, test_time_in_minute, hospital_close_at, hospital_opens_at, Appointment
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
        booked_slots_query = Appointment.objects.filter(time__date=datetime.date(date_dt1))
        booked_slots = []
        for slot in booked_slots_query:
            print(slot.time)
            hour = slot.time.hour
            min = slot.time.minute
            booked_slots.append({'hour':hour, 'min':min})
        available_slots = []
        total_slots_count = ((hospital_close_at - hospital_opens_at) * (60 / test_time_in_minute))
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