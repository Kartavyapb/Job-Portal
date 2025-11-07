from django.shortcuts import render, get_object_or_404, redirect
from jobapp.models import ItJobs
from django.http import HttpResponse
from jobapp2.models import JobApplication, Profile
from jobapp.models import Userregistration
from jobapp2.forms import JobApplicationForm, ProfileForm
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from django.contrib.auth import get_user_model

# Create your views here.
def all_jobs(request):
    query = request.GET.get('q')
    if query:
        jobs = ItJobs.objects.filter(
            company_name__icontains=query
        ) | ItJobs.objects.filter(
            industry__icontains=query
        ) | ItJobs.objects.filter(
            job_title__icontains=query
        ) | ItJobs.objects.filter(
            job_location__icontains=query
        )

    else:
        jobs = ItJobs.objects.all()

    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
    context={
        'jobs' : jobs,
        'query' : query,
        'profile' : profile
    }
    return render(request, 'jobapp2/jobs.html', context)    

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(ItJobs, id=job_id)

    if request.method == "POST":
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job   # link application with the job
            application.applicant = request.user
            application.save()
            return redirect("apply_success")  # redirect to a success page
    else:
        form = JobApplicationForm()

    return render(request, "jobapp2/apply_job.html", {"form": form, "job": job})


def apply_success(request):
    return render(request, "jobapp2/apply_success.html")

@login_required
def dashboard_redirect(request):
    return redirect("dashboard", user_id=request.user.id)


User = get_user_model()

@login_required
def dashboard(request, user_id):
    user = get_object_or_404(Userregistration, id=user_id)
    posted_jobs       = ItJobs.objects.filter(posted_by=request.user)
    applied_jobs      = JobApplication.objects.filter(applicant=request.user)
    profile, created  = Profile.objects.get_or_create(user=request.user)
    
    display_name = user.full_name if user.full_name else user.username

    return render(request, "jobapp2/dashboard.html", {
        "posted_jobs" : posted_jobs,
        "applied_jobs" : applied_jobs,
        "profile" : profile,
        "dashboard_user" : user,
        "display_name" : display_name,
    })


def job_detail(request, job_id):
    job = get_object_or_404(ItJobs, id=job_id)
    applications = JobApplication.objects.filter(job=job).select_related("applicant")

    return render(request, "jobapp2/job_detail.html", {
        "job": job,
        "applications": applications,
    })




def candidate_detail(request, user_id):
    candidate = get_object_or_404(User, id=user_id)
    return render(request, 'jobapp2/candidate_detail.html', {
        'candidate': candidate,
    })


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        # Update text fields
        profile.phone = request.POST.get("phone")
        profile.address = request.POST.get("address")
        profile.skills = request.POST.get("skills")
        profile.experience = request.POST.get("experience")
        profile.github = request.POST.get("github")
        profile.profile_pic = request.FILES.get("profile_pic")

        # ✅ delete old profile pic if new one is uploaded and it's not default
        if profile.profile_pic:
            if profile.profile_pic and profile.profile_pic.name != "profile_pics/default-avatar.png":
                old_path = os.path.join(settings.MEDIA_ROOT, str(profile.profile_pic))
                if os.path.exists(old_path):
                    os.remove(old_path)
            profile.profile_pic = profile.profile_pic

        profile.phone = profile.phone
        profile.address = profile.address
        profile.skills = profile.skills
        profile.experience = profile.experience
        profile.github = profile.github
        profile.save()

        return redirect("dashboard", user_id=request.user.id)

    return render(request, "jobapp2/edit_profile.html", {"profile": profile})



@login_required
def profile_view(request,user_id):
    candidate  = get_object_or_404(Userregistration, id=user_id)
    profile , created  = Profile.objects.get_or_create(user=candidate)

    job_id  = request.GET.get("job_id")

    application = None
    if job_id:
        application = JobApplication.objects.filter(applicant=candidate, job_id=job_id).first()

    return render(request, "jobapp2/profile_view.html", {
        'candidate' : candidate,
        'profile' : profile,
        'job_id'  : job_id,
        'application' : application,
    })


def user_dashboard(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile  # assuming you have OneToOne relation with Profile
    posted_jobs = user.job_set.all()  # jobs posted by that user
    applied_jobs = user.application_set.all()  # jobs applied by that user

    context = {
        'profile': profile,
        'posted_jobs': posted_jobs,
        'applied_jobs': applied_jobs,
    }
    return render(request, "dashboard.html", context)

def job_details_only(request, job_id):
    job = get_object_or_404(ItJobs, id=job_id)
    applications = JobApplication.objects.filter(job=job).select_related("applicant")

    return render(request, "jobapp2/job_details_only.html", {
        "job": job,
        "applications": applications,
    })