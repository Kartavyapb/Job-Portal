from django import forms
from django.forms import ModelForm
from jobapp.models import ItJobs
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from jobapp.models import Userregistration
from jobapp.models import *
from django.contrib.auth.models import User

class CreateItJobsForm(ModelForm):
    class Meta:
        model = ItJobs
        fields = '__all__'
        exclude = ['posted_by']
        widgets = {
            'app_deadline': forms.DateInput(attrs={'type': 'date'})
        }

        
class UpdateItJobsForm(ModelForm):
    class Meta:
        model = ItJobs
        fields = '__all__'
        widgets = {
            'app_deadline': forms.DateInput(attrs={'type': 'date'})
        }




class UserregistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = Userregistration
        fields = ["full_name", "username", "phone", "email", "role", "password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
      