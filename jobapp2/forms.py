from django import forms
from jobapp2.models import JobApplication, Profile

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        exclude = ["job", "applied_on"]  # job will be linked in view, not manually filled
        widgets = {
            "dob": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-control"}),
            "highest_qualification": forms.TextInput(attrs={"class": "form-control"}),
            "specialization": forms.TextInput(attrs={"class": "form-control"}),
            "passout_year": forms.TextInput(attrs={"class": "form-control"}),
            "university": forms.TextInput(attrs={"class": "form-control"}),
            "experience": forms.TextInput(attrs={"class": "form-control"}),
            "skills": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "resume": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address', 'profile_pic', 'skills', 'experience', 'resume', 'github']




        