# resumeapp/urls.py
from django.urls import path
from resumeapp import views

#app_name = 'resumeapp'

urlpatterns = [
    path('resume-builder/', views.resume_builder, name='resume_builder'),
    path('review/', views.review_resume, name='review_resume'),
    path('templates/', views.template_selection, name='template_selection'),
    path('generate/<int:template_id>/', views.generate_resume, name='generate_resume'),
    
]
