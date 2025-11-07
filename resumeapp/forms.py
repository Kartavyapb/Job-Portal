# resumeapp/forms.py
from django import forms
from django.forms import modelformset_factory
from .models import PersonalInfo, Education, Skill, Project, WorkExperience

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = ['full_name', 'email', 'phone', 'address', 'objective', 'linkedin', 'github']
        widgets = {
            'full_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Full name' , 'required':'required'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email', 'required':'required'}),
            'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone', 'required':'required'}),
            'address': forms.Textarea(attrs={'class':'form-control', 'rows':2, 'placeholder':'Address', 'required':'required'}),
            'objective': forms.Textarea(attrs={'class':'form-control', 'rows':3, 'placeholder':'Career objective', 'required':'required'}),
            'linkedin': forms.URLInput(attrs={'class':'form-control', 'placeholder':'LinkedIn (optional)'}),
            'github': forms.URLInput(attrs={'class':'form-control', 'placeholder':'GitHub (optional)'}),
        }

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['level', 'board_or_degree', 'institute', 'passing_year', 'percentage']
        widgets = {
            'level': forms.Select(attrs={'class': 'form-select level-select', 'required': 'required'}),
            'board': forms.Select(attrs={'class': 'form-select board-select d-none'}),
            'board_or_degree': forms.TextInput(attrs={'class': 'form-control degree-input d-none', 'placeholder': 'Enter Degree/Diploma Name'}),
            'institute': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter institute name', 'required': 'required'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Passing Year', 'required': 'required'}),
            'percentage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Percentage/CGPA', 'required': 'required'}),
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['category', 'name']
        widgets = {
            'category': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Category (e.g., IT, Civil, Mechanical)'}),
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Skill name'}),
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'tech_tools', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'tech_tools': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'rows':3}),
        }

class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['job_title', 'company', 'description']
        widgets = {
            'job_title': forms.TextInput(attrs={'class':'form-control'}),
            'company': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'rows':3}),
        }

# formset factories (we'll use these in view)
EducationFormSet = modelformset_factory(Education, form=EducationForm, extra=1, can_delete=True)
SkillFormSet     = modelformset_factory(Skill, form=SkillForm, extra=1, can_delete=True)
ProjectFormSet   = modelformset_factory(Project, form=ProjectForm, extra=1, can_delete=True)
ExperienceFormSet= modelformset_factory(WorkExperience, form=WorkExperienceForm, extra=1, can_delete=True)
