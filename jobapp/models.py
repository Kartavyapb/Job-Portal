from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.conf import settings

mob_regex = RegexValidator(regex=r'^\d{10}$', message="Enter a Valid 10 digit Mobile Number")

class ItJobs(models.Model):
    industry_choices = [
        ("it", "IT"),
        ("mechanical", "Mechanical"),
        ("civil", "Civil"),
        ("management", "Management"),
        ("electrical","Electrical"),
        ("healthcare","HealthCare"),
        ("other","Other"),
    ]

    job_type_choices = [
        ("full-time","Full-Time"),
        ("part-time", "Part-Time"),
        ("hybrid", "Hybrid"),
        ("internship", "Internship"),
        ("freelacing", "Freelancing"),
        ("other", "Other"),
    ]


    company_name                = models.CharField(max_length=100)
    industry                    = models.CharField('Industry', max_length= 30, choices=industry_choices, default='Select-Industry')
    company_email               = models.EmailField('Company Email', default="Ex. abc@gmail.com")
    contact_person_name         = models.CharField('Contact Person Name', max_length=50)
    contact_person_email        = models.EmailField('Contact Person Email', default="Ex. abc@gmail.com")
    contact_person_mobile       = models.CharField('Contact Person Mobile Number', max_length=10, validators=[mob_regex])
    company_address             = models.TextField('Company Address')
    company_description         = models.TextField('Company Description')

#-------------------------------------------------------------------------------------------------------------

    job_title                   = models.CharField('Job Title' , max_length=100)
    job_type                    = models.CharField('Job Type', max_length=20, choices=job_type_choices, default="Select-Job-Type")
    num_vacancy                 = models.IntegerField('Number of Vacancies')
    job_location                = models.CharField('Location' , max_length=100, default="Enter-City")
    job_discription             = models.TextField('Job Description' ,null=True , blank=True)
    key_skiils                  = models.TextField('Required Skills')
    experience                  = models.CharField('Experience Required', null=True, blank=True)
    Edu_qualification           = models.TextField('Education Qualification')
    pass_batch                  = models.CharField('Passout Batch', null=True, blank=True)

#--------------------------------------------------------------------------------------------------------------
    
    salary                      = models.FloatField('Salary per Month')
    app_deadline                = models.DateField('Application Deadline')
    hiring_process              = models.TextField('Hiring Process')    
    posted_on                   = models.DateTimeField(auto_now_add=True)


    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = "jobs",
        null=True,
        blank=True
    )


    def __str__(self):  
        return self.company_name
    


class Userregistration(AbstractUser):
    ROLE_CHOICES = [
        ("recruiter", "Recruiter"),
        ("jobseeker", "Jobseeker"),
    ]

    # Link with built-in User
    #user = models.OneToOneField(User, on_delete=models.CASCADE)

    email = models.EmailField('Email', unique=True)
    phone = models.CharField('Mobile number', max_length=10, unique=True, validators=[mob_regex])
    role = models.CharField('Role', max_length=20, choices=ROLE_CHOICES, default='jobseeker')

    full_name = models.CharField("Full Name", max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.username} ({self.role})'
