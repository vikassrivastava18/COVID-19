from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Patient, GENDER, Report, RESULT
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
import datetime


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        }
    ))


class PatientCreationForm(ModelForm):

    class Meta:
        model = Patient
        fields = ['patient_first_name', 'patient_last_name','patient_email', 'patient_age', 'patient_mobile', 'patient_gender']

    patient_first_name = forms.CharField(
        label="Patient First Name",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        )
    )

    patient_last_name = forms.CharField(
        label="Patient Last Name",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        )
    )
    patient_email = forms.EmailField(
        label="Patient's Email",
        widget = forms.EmailInput(
            attrs={
                "class": "form-control",
            }
        )
    )
    patient_age = forms.IntegerField(
        label="Patient's Age",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
            }
        )
    )
    patient_mobile = forms.CharField(
        label="Patient's Mobile Number",
        widget = forms.TextInput(
            attrs={
                "class": "form-control",
            }
        )
    )

    def clean_patient_mobile(self):
        data = self.cleaned_data['patient_mobile']

    #     Check the length of mobile number
        if len(data) < 10 or len(data) > 10:
            raise ValidationError(_('Invalid number, please enter 10 digits'))
        return data

    patient_gender = forms.ChoiceField(
        label="Patient's Gender",
        choices=GENDER,
        widget=forms.RadioSelect(
            attrs={

            }
        )
    )


class ReportCreationForm(ModelForm):

    class Meta:
        model = Report
        fields = ['patient', 'result', 'file']

    result = forms.ChoiceField(
        label="Report's Result",
        choices=RESULT,
        widget=forms.RadioSelect(
            attrs={

            }
        )
    )
