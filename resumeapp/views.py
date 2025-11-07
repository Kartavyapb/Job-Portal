# resumeapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse
from django.forms import modelformset_factory
from .models import PersonalInfo, Education, Skill, Project, WorkExperience
from .forms import (PersonalInfoForm, EducationFormSet, SkillFormSet,
                    ProjectFormSet, ExperienceFormSet)
from django.template.loader import render_to_string

# For PDF generation
from xhtml2pdf import pisa
from io import BytesIO


# @login_required
# def resume_builder(request, personal_id=None):
#     user = request.user

#     # Try to load existing PersonalInfo; else create None (forms will be empty)
#     personal = PersonalInfo.objects.filter(user=user).first()


#     if request.method == 'POST':
#         per_form = PersonalInfoForm(request.POST, instance=personal)
#         edu_qs = Education.objects.filter(user=user)
#         skill_qs = Skill.objects.filter(user=user)
#         proj_qs = Project.objects.filter(user=user)
#         exp_qs = WorkExperience.objects.filter(user=user)

#         edu_formset = EducationFormSet(request.POST, queryset=edu_qs, prefix='edu')
#         skill_formset = SkillFormSet(request.POST, queryset=skill_qs, prefix='skill')
#         proj_formset = ProjectFormSet(request.POST, queryset=proj_qs, prefix='proj')
#         exp_formset = ExperienceFormSet(request.POST, queryset=exp_qs, prefix='exp')

#         # Validate required things:
#         per_valid = per_form.is_valid()
#         edu_valid = edu_formset.is_valid()
#         skill_valid = skill_formset.is_valid()
#         proj_valid = proj_formset.is_valid()
#         exp_valid = exp_formset.is_valid()

#         # At least one education and at least one skill required:
#         educations_present = any([f.cleaned_data and not f.cleaned_data.get('DELETE', False) for f in edu_formset.forms if f.is_valid()])
#         skills_present = any([f.cleaned_data and not f.cleaned_data.get('DELETE', False) for f in skill_formset.forms if f.is_valid()])

#         if not educations_present:
#             edu_valid = False
#             # add non-field error by manipulating formset
#             edu_formset.non_form_errors = ["Please add at least one Education entry."]

#         if not skills_present:
#             skill_valid = False
#             skill_formset.non_form_errors = ["Please add at least one Skill entry."]

#         if per_valid and edu_valid and skill_valid and proj_valid and exp_valid:
#             # Save personal
#             personal_info = per_form.save(commit=False)
#             personal_info.user = user
#             personal_info.save()

#             # Replace all Education/Skill/Project/Exp for this user:
#             Education.objects.filter(user=user).delete()
#             Skill.objects.filter(user=user).delete()
#             Project.objects.filter(user=user).delete()
#             WorkExperience.objects.filter(user=user).delete()

#             for f in edu_formset:
#                 if f.cleaned_data and not f.cleaned_data.get('DELETE', False):
#                     ed = Education(
#                         user=user,
#                         level=f.cleaned_data['level'],
#                         board_or_degree=f.cleaned_data['board_or_degree'],
#                         institute=f.cleaned_data['institute'],
#                         passing_year=f.cleaned_data['passing_year'],
#                         percentage=f.cleaned_data['percentage']
#                     )
#                     ed.save()

#             for f in skill_formset:
#                 if f.cleaned_data and not f.cleaned_data.get('DELETE', False):
#                     sk = Skill(user=user, category=f.cleaned_data['category'], name=f.cleaned_data['name'])
#                     sk.save()

#             for f in proj_formset:
#                 if f.cleaned_data and not f.cleaned_data.get('DELETE', False):
#                     pj = Project(user=user, title=f.cleaned_data['title'], tech_tools=f.cleaned_data['tech_tools'], description=f.cleaned_data['description'])
#                     pj.save()

#             for f in exp_formset:
#                 if f.cleaned_data and not f.cleaned_data.get('DELETE', False):
#                     we = WorkExperience(user=user, job_title=f.cleaned_data['job_title'], company=f.cleaned_data['company'], description=f.cleaned_data['description'])
#                     we.save()

#             # redirect to review page
#             return redirect('resume_review', personal_id=personal_info.id)

#     else:
#         # GET: show forms with existing data if any
#         per_form = PersonalInfoForm(instance=personal)
#         edu_formset = EducationFormSet(queryset=Education.objects.filter(user=user), prefix='edu')
#         skill_formset = SkillFormSet(queryset=Skill.objects.filter(user=user), prefix='skill')
#         proj_formset = ProjectFormSet(queryset=Project.objects.filter(user=user), prefix='proj')
#         exp_formset = ExperienceFormSet(queryset=WorkExperience.objects.filter(user=user), prefix='exp')


#     return render(request, 'resumeapp/resume_builder.html', {
#         'per_form': per_form,
#         'edu_formset': edu_formset,
#         'skill_formset': skill_formset,
#         'proj_formset': proj_formset,
#         'exp_formset': exp_formset,
#     })








@login_required
def resume_builder(request, personal_id=None):
    user = request.user

    personal = PersonalInfo.objects.filter(user=user).first()

    per_form = PersonalInfoForm(instance=personal)
    edu_formset = EducationFormSet(queryset=Education.objects.filter(user=user), prefix='edu')
    skill_formset = SkillFormSet(queryset=Skill.objects.filter(user=user), prefix='skill')
    proj_formset = ProjectFormSet(queryset=Project.objects.filter(user=user), prefix='proj')
    exp_formset = ExperienceFormSet(queryset=WorkExperience.objects.filter(user=user), prefix='exp')

    return render(request, 'resumeapp/resume_builder.html', {
        'per_form': per_form,
        'edu_formset': edu_formset,
        'skill_formset': skill_formset,
        'proj_formset': proj_formset,
        'exp_formset': exp_formset,
    })


@login_required
def review_resume(request):
    return render(request, 'resumeapp/review_resume.html')


@login_required
def template_selection(request):
    return render(request, 'resumeapp/template_selection.html')


@login_required
def generate_resume(request, template_id):
    template_file = f"resumeapp/templates/resumeapp/generated_resume_{template_id}.html"

    # You can dynamically select template here, for now just render one page
    context = {
        "template_id": template_id
    }
    return render(request, f"resumeapp/generated_resume_{template_id}.html", context)






























# @login_required
# def resume_review(request, personal_id):
#     personal = get_object_or_404(PersonalInfo, id=personal_id, user=request.user)
#     education = Education.objects.filter(user=request.user)
#     skills = Skill.objects.filter(user=request.user)
#     projects = Project.objects.filter(user=request.user)
#     experiences = WorkExperience.objects.filter(user=request.user)

#     return render(request, 'resumeapp/review_resume.html', {
#         'personal': personal,
#         'education': education,
#         'skills': skills,
#         'projects': projects,
#         'experiences': experiences
#     })



# @login_required
# def select_template(request):
#     """
#     Show 5 templates for selection. When selected, redirect to preview page (resume_template_preview).
#     """
#     templates = [
#         {'id': 'template1', 'title': 'Classic'},
#         {'id': 'template2', 'title': 'Modern'},
#         {'id': 'template3', 'title': 'Creative'},
#         {'id': 'template4', 'title': 'Professional'},
#         {'id': 'template5', 'title': 'Minimal'},
#     ]
#     return render(request, 'resumeapp/select_template.html', {'templates': templates})


# @login_required
# def resume_template_preview(request, template_name):
#     """
#     Render selected template with user's saved data and offer Download PDF.
#     """
#     personal = PersonalInfo.objects.filter(user=request.user).first()
#     educations = Education.objects.filter(user=request.user)
#     skills = Skill.objects.filter(user=request.user)
#     projects = Project.objects.filter(user=request.user)
#     experiences = WorkExperience.objects.filter(user=request.user)

#     return render(request, f'resumeapp/resume_templates/{template_name}.html', {
#         'personal': personal,
#         'educations': educations,
#         'skills': skills,
#         'projects': projects,
#         'experiences': experiences,
#     })



# @login_required
# def download_resume_pdf(request, template_name):
#     """
#     Generate PDF from template (xhtml2pdf).
#     """
#     personal = PersonalInfo.objects.filter(user=request.user).first()
#     educations = Education.objects.filter(user=request.user)
#     skills = Skill.objects.filter(user=request.user)
#     projects = Project.objects.filter(user=request.user)
#     experiences = WorkExperience.objects.filter(user=request.user)

#     html = render_to_string(f'resumeapp/resume_templates/{template_name}.html', {
#         'personal': personal,
#         'educations': educations,
#         'skills': skills,
#         'projects': projects,
#         'experiences': experiences,
#         'pdf': True,  # optional flag inside template to adjust styling for PDF
#     })

#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
#     if pdf.err:
#         return HttpResponse('PDF generation error', status=500, content_type='text/plain')
#     return HttpResponse(result.getvalue(), content_type='application/pdf')
