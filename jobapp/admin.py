from django.contrib import admin
from django import forms
from jobapp.models import ItJobs
from jobapp.models import Userregistration

class ItJobsForm(forms.ModelForm):
    class Meta:
        model = ItJobs
        fields = '__all__'
        widgets = {
            'app_deadline': forms.DateInput(attrs={'type': 'date'})
        }

class ItJobsAdmin(admin.ModelAdmin):
    form = ItJobsForm
    

admin.site.register(ItJobs)
admin.site.register(Userregistration)