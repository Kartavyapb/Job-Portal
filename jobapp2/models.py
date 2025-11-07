from django.db import models
from jobapp.models import ItJobs
from django.core.validators import RegexValidator
from django.conf import settings

mob_regex = RegexValidator(regex=r'^\d{10}$', message="Enter a Valid 10 digit Mobile Number")


class JobApplication(models.Model):
    job        = models.ForeignKey(ItJobs, on_delete=models.CASCADE, related_name="applications")  # link with job
    applicant  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")

    full_name  = models.CharField("Full Name", max_length=100)
    email      = models.EmailField("Email")
    phone      = models.CharField("Mobile Number", max_length=10, validators=[mob_regex])
    dob        = models.DateField("Date of Birth")

    gender_choices = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]
    gender    = models.CharField("Gender", max_length=10, choices=gender_choices)

    highest_qualification  = models.CharField("Highest Qualification", max_length=100)
    specialization         = models.CharField("Specialization", max_length=100, blank=True, null=True)
    passout_year           = models.CharField("Passout Year", max_length=10)
    university             = models.CharField("University/College", max_length=150)

    experience             = models.CharField("Experience", max_length=100, help_text="Eg: 2 years, Fresher")
    skills                 = models.TextField("Skills")
    resume                 = models.FileField("Upload Resume (PDF/Doc)", upload_to="resumes/")

    applied_on             = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} → {self.job.job_title}"
    

class Profile(models.Model):
    user          = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone         = models.CharField(max_length=10, blank=True, null=True, validators=[mob_regex])
    address       = models.TextField(blank=True, null=True)
    profile_pic   = models.ImageField(upload_to="profile_pics/", default="default-avatar.png", blank=True, null=True)
    skills        = models.TextField(blank=True, null=True)
    experience    = models.TextField(blank=True, null=True)
    resume        = models.FileField(upload_to="resumes/", blank=True, null=True)
    github        = models.URLField(blank=True , null=True)

    def __str__(self):
        return self.user.username
    
