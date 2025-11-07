from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from jobapp.forms import CreateItJobsForm , UpdateItJobsForm
from jobapp.models import ItJobs
from django.core.mail import send_mail
from django.conf import settings
from jobapp.forms import UserregistrationForm
from jobapp.models import *
from jobapp.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from jobapp2.models import JobApplication, Profile



def home(request):
    query = request.GET.get('q')

    if query:
        # Redirect to list of jobs page with the search query
        return redirect(f'/jobs/?q={query}')
    else:
        jobs = ItJobs.objects.all()

    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()

    return render(request, 'jobapp/home.html', {'jobs': jobs, 'profile': profile})


def welcome(request):
    return render(request , 'jobapp/welcome.html')


def user_registration(request):
    # form = UserCreationForm()
    if request.method == 'POST':
        form = UserregistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')

            messages.success(request, f"Account Created Successfully for {username}. You can now Login In.")

            subject = "Registration Successful"

            message = f'''
                        Hello {username},
                        
                        Your Account has been Successfully Created !
                        
                        Here are your Login Details:
                        Username: {username}
                        Password: {password}

                        You Can Now Log In to Your Account.
                        
                        Thank You,
                        Job Portal Team
                        '''
            
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,   # Sender
                [email],                   # Receiver
                fail_silently=False,
            )

            return redirect('/login/')
        
    else:
        form = UserregistrationForm()

    return render(request, 'jobapp/register.html',{'form': form})

            
    
@login_required
def create_it_jobs(request):
    #form = CreateItJobsForm()

    if request.method == 'POST':
        form = CreateItJobsForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            return redirect('/dashboard/')
        else:
            print(form.errors)
    else:
        form = CreateItJobsForm()

    context = {
        'form' : form
    }
    return render(request , 'jobapp/create-it-jobs.html', context)


def list_of_it_jobs(request):
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

    context={
        'jobs' : jobs,
        'query' : query
    }
    return render(request, 'jobapp/list_of_it_jobs.html', context)

def update_it_jobs(request, id):

    obj = ItJobs.objects.get(pk = id)

    if request.method == 'POST':
        form = UpdateItJobsForm(request.POST , instance=obj)
        if form.is_valid():
            form.save()
            return redirect('/list_of_it_jobs/')
        
    context = {
        'form' : UpdateItJobsForm(instance=obj)
        
    }
    return render(request, 'jobapp/update_it.html', context)


def itdelete(request,id):
    job = get_object_or_404(ItJobs, id=id)
    return render(request, 'jobapp/itdelete.html', {'job': job})



def delete_it_jobs(request, id):

    obj = ItJobs.objects.get(pk = id)

    obj.delete()

    messages.success(request, "✅ Job Deleted Successfully")

    return redirect('/list_of_it_jobs/', id=id)


def help(request):
    return render(request, 'jobapp/help.html')

def about(request):
    return render(request, ('jobapp/about.html'))


def contact(request):
    success_message = None

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        subject = f"New Contact Message from {name}"
        full_message = f"Sender Name: {name}\nSender Email: {email}\n\nMessage:\n{message}"

        send_mail(
            subject,
            full_message,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            fail_silently = False,
        )

        subject_user = "Thank you for contacting Job Portal"
        confirmation_message = (
            f"Hello {name},\n\n"
            f"Thank you for reaching out to us. We have received your message:\n\n"
            f"\"{message}\"\n\n"
            f"Our support team will get back to you shortly.\n\n"
            f"Best Regards,\nJob Portal Team"
        )

        send_mail(
            subject_user,
            confirmation_message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently = False,
        )

        success_message = "✅ Your message has been sent successfully! A confirmation email has been sent to your inbox."

    return render(request, "jobapp/contact.html",{"success_message": success_message})


