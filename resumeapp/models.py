from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from jobapp.models import Userregistration


mob_regex = RegexValidator(regex=r'^\d{10}$', message="Enter a Valid 10 digit Mobile Number")


# Personal Info (prefilled from Userregistration)
class PersonalInfo(models.Model):
    user = models.OneToOneField(Userregistration, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10, validators=[mob_regex])
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    objective = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.full_name
    
# Education
class Education(models.Model):
    LEVEL_CHOICES = [
        ('10th', '10th'),
        ('12th', '12th'),
        ('Diploma', 'Diploma'),
        ('Graduate', 'Graduate'),
        ('Post Graduate', 'Post Graduate'),
        ('PhD', 'PhD'),
    ]

    BOARD_CHOICES = [
        ('CBSE', 'Central Board of Secondary Education (CBSE)'),
        ('ICSE', 'Indian Certificate of Secondary Education (ICSE)'),
        ('NIOS', 'National Institute of Open Schooling (NIOS)'),

        # State Boards (Major)
        ('Maharashtra State Board', 'Maharashtra State Board of Secondary & Higher Secondary Education'),
        ('Gujarat Board', 'Gujarat Secondary and Higher Secondary Education Board'),
        ('Tamil Nadu Board', 'Tamil Nadu State Board'),
        ('Karnataka Board', 'Karnataka Secondary Education Examination Board'),
        ('Kerala Board', 'Kerala State Education Board'),
        ('Uttar Pradesh Board', 'Uttar Pradesh Madhyamik Shiksha Parishad'),
        ('Bihar Board', 'Bihar School Examination Board'),
        ('West Bengal Board', 'West Bengal Board of Secondary Education'),
        ('Rajasthan Board', 'Board of Secondary Education, Rajasthan'),
        ('Punjab Board', 'Punjab School Education Board'),
        ('Haryana Board', 'Board of School Education Haryana'),
        ('Madhya Pradesh Board', 'Madhya Pradesh Board of Secondary Education'),
        ('Telangana Board', 'Telangana State Board of Intermediate Education'),
        ('Andhra Pradesh Board', 'Board of Secondary Education, Andhra Pradesh'),
        ('Odisha Board', 'Board of Secondary Education, Odisha'),
        ('Assam Board', 'Board of Secondary Education, Assam'),
        ('Jharkhand Board', 'Jharkhand Academic Council'),
        ('Chhattisgarh Board', 'Chhattisgarh Board of Secondary Education'),
        ('Goa Board', 'Goa Board of Secondary and Higher Secondary Education'),
        ('Delhi Board', 'Delhi Board of School Education (DBSE)'),
        ('Other', 'Other'),
    ]


    user = models.ForeignKey(Userregistration, on_delete=models.CASCADE)
    level = models.CharField(max_length=100, choices=LEVEL_CHOICES)
    board_or_degree = models.CharField(max_length=200, blank=True, null=True)
    institute = models.CharField(max_length=200)
    passing_year = models.CharField(max_length=10)
    percentage = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.level} - {self.institute}"


# Skill
class Skill(models.Model):
    user = models.ForeignKey(Userregistration, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=200)



#Projects
class Project(models.Model):
    user = models.ForeignKey(Userregistration, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    tech_tools = models.CharField(max_length=200)
    description = models.TextField()


# Work Experience
class WorkExperience(models.Model):
    user = models.ForeignKey(Userregistration, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)



