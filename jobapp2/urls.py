from django.urls import path
from jobapp2 import views

urlpatterns = [
    path('jobs/',views.all_jobs, name='jobs'),
    path('apply/<int:job_id>', views.apply_job, name="apply_job"),
    path('apply/success/', views.apply_success, name='apply_success'),
    path('dashboard/', views.dashboard_redirect, name="dashboard_redirect"),
    path('dashboard/<int:user_id>/', views.dashboard, name='dashboard'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('profile/<int:user_id>/', views.profile_view, name='profile_view'),
    path('candidate/<int:user_id>/', views.candidate_detail, name='candidate_detail'),
    path('job_detail/<int:job_id>', views.job_details_only, name='job_details_only'),
]





# path("dashboard/<str:username>/", views.user_dashboard, name='user_dashboard'),





