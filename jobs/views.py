# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from jobs import models, forms
from django.db.models import Q,Count, Sum, F
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from jobs import constants, functions
from jobs.decorators import *
from event import models as eventModels
from event import forms as eventForms
from django.contrib.auth.decorators import login_required,user_passes_test
from django.db.models import Sum,F



import datetime
# Create your views here.

build_resume_redirects = {
    'general' : '/employee/build-resume/summary/',
    'cv' : '/employee/',

    'summary' : '/employee/build-resume/experience/',
    'experience' : '/employee/build-resume/education/',
    'education' : '/employee/build-resume/skill/',
    'skill' : '/employee/build-resume/worksample/',
    'worksample' : '/employee/build-resume/worklink/',
    'worklink' : '/employee/build-resume/volunteer/',
    'volunteer' : '/employee/build-resume/reference/',
    'reference' : '/employee/',
    
}
def aboutUs(request):
    return render(request, 'about.tmp', locals())

def privacy(request):
    return render(request, 'privacy.policy.tmp', locals())
    
def branding(request):
    return render(request, 'employer.branding.tmp', locals())

def aboutFounder(request):
    return render(request, 'about.founder.tmp', locals())

def services(request):
    return render(request, 'services.page.tmp', locals())

def contact(request):
    contactForm = forms.ContactForm()
    if request.method == "POST":
        contactForm = forms.ContactForm(request.POST)
        if contactForm.is_valid():
            succ = "Your message succesfully sent to ican."
            contactForm.save()
        else:
            err = "Unable to send your message. Please make sure you provided value to all fields."
        
    return render(request, 'contact.tmp' ,locals())
    
def jobAlerts(request):
    jobAlertForm = forms.JobAlertForm()
    if request.method == "POST":
        jobAlertForm = forms.JobAlertForm(request.POST)
        if jobAlertForm.is_valid():
            jobAlertForm.save()
            suc = "You have subscribed succesfully."
        else:
            err = "Failed to save your subscription."

    return render(request, 'jobalert.tmp', locals())

def homeView(request, **kwargs):

    template_name = "home.tmp"
    

    categories = models.Category.objects.filter(jobs__status = constants.JOB_STATUS_OPEN).annotate(job_count=Count('jobs')).order_by('-job_count')
    featured_categories = categories[:6]
    from datetime import date
    recent_jobs = models.Job.objects.filter(is_draft=False)[:constants.RECENT_JOBS_NUMBER]
    
    for recent_job in recent_jobs:
        recent_job.expired = recent_job.deadline and recent_job.deadline < date.today()
        if not recent_job.expired and recent_job.deadline:
            delta_days = recent_job.deadline - date.today()             
            recent_job.is_soon = delta_days.days < 7
            recent_job.remaining = delta_days.days

    employement_types = models.EmployementType.objects.all()
    recent_blogs = eventModels.Blog.objects.all().order_by('-created_at')[:constants.RECENT_BLOG_NUMBER]
    regions = models.Region.objects.all()
    return render(request, template_name, locals())


@login_required
@user_passes_test(functions.is_company)
def applicationPrint(request, applicationID, dont_print=False, accesstoken=None):
    job_application = get_object_or_404(models.JobApplication, pk=applicationID)
    employee = job_application.applicant
    job = job_application.job
    return render(request, 'application.print.tmp', locals())

@can_view_employee
def employeeViewOnly(request, applicationID, accesstoken, dont_print=False):
    job_application =  get_object_or_404(models.JobApplication, pk=applicationID)
    job = job_application.job
    employee = job_application.applicant
    
    return render(request, 'application.print.tmp', locals())

@login_required
@user_passes_test(functions.is_company)
def createAccesToken(request, filter=None):
    if not filter:
        filter= ''
    
    paramQuery = request.GET.get('query')
    if not paramQuery:
        paramQuery = ''
    try:
        accesstoken = models.AccessToken.objects.get(company=request.user.company, paramFilter=filter, paramQuery=paramQuery)
    except:
        accesstoken = models.AccessToken.objects.create(company=request.user.company, paramFilter=filter, paramQuery=paramQuery,value=models.AccessToken.generateValue())
    print accesstoken
    return render(request, 'redirect.email.tmp', locals())

@user_can_acces
def applicationsViewOnly(request, accesstoken, dont_print=False):
    application_filter, applications, unread_applications_count = getJobApplications(request.user.company, accesstoken.paramFilter, accesstoken.paramQuery)
    return render(request, 'applications.view.only.tmp', locals())


@login_required
@user_passes_test(functions.is_company)
def applicationDelete(request, applicationID):
    job_application = get_object_or_404(models.JobApplication, pk=applicationID)
    job_application.delete()

    return redirect('/company/admin/applications/')

def jobView(request, **kwargs):
    jobs = None 
    template_name = "jobs.tmp"
    if kwargs.get('regionID', False):
        jobs, region = jobRegionListHelper(kwargs['regionID'])

    elif kwargs.get('categoryID', False):
        jobs, category = jobCategoryListHelper(kwargs['categoryID'])

    elif kwargs.get('jobID', False):
        try:
            jobID = kwargs.get('jobID').split('-')[-1]
            jobID = int(jobID)
        except:
            return HttpResponse('Job Not Found', status=404)
        
        job = jobDetailHelper(jobID, request)
        from datetime import date
        expired = job.deadline and job.deadline < date.today()
        job_side_ads = eventModels.Advertisement.objects.filter(placement=constants.AD_PLACE_JOBDETAIL_SIDE)
        template_name = "job_detail.tmp"


    elif kwargs.get('search', False):

        search_query = request.GET.get('q', '')
        cat = request.GET.get('cat', 'all') 
        location = request.GET.get('location', '') 
        employement_type = request.GET.get('employement_type', 'all')
        jobs, category, employement_type, region, search_query = jobSearchHelper(search_query, location, cat, employement_type)
        search_result_count = jobs.count()

    else:
        jobs, category = jobCategoryListHelper()
    
    #check for response message 
    
    # do pagination 
    if jobs: 
        jobs = jobs.filter(is_draft=False)
        page_number = request.GET.get('page', 1)
        paginator = Paginator(jobs, constants.PAG_JOB_NUMBER)
        current_page = paginator.page(page_number)
        jobs = current_page.object_list

    employement_types = models.EmployementType.objects.all()

    regions = models.Region.objects.all()
    categories = models.Category.objects.filter(jobs__status = constants.JOB_STATUS_OPEN).annotate(job_count=Count('jobs')).order_by('-job_count')

    recent_jobs = models.Job.objects.filter(is_draft=False)[:constants.RECENT_JOBS_SIDEBAR]
    return render(request, template_name, locals())
#view helper functions for job 
def jobDetailHelper(jobID, request):
    job = get_object_or_404(models.Job, pk=jobID, is_draft=False)
    job.eligible_to_apply = request.user.is_authenticated and hasattr(request.user, 'employee') and job.apply_through_portal
    if job.eligible_to_apply:
        job.applied_already = job.applicants.filter(pk = request.user.employee.pk)
        job.eligible_to_apply = True

    return job
    

def jobCategoryListHelper(categoryID=None):
    if not categoryID:
        jobs = models.Job.objects.filter(is_draft=False)
    else:
        category = get_object_or_404(models.Category, pk=categoryID)
        jobs = category.jobs.filter(is_draft=False)
        return jobs, category

    return jobs, None

def jobRegionListHelper(regionID=None):
    region = get_object_or_404(models.Region, pk=regionID)
    jobs = region.jobs.filter(is_draft=False)
    return jobs, region

def jobSearchHelper(search_query, location, cat='all', employement_type='all'):

    query = Q(title__icontains=search_query)
    regions = models.Region.objects.filter(name__icontains=location)
    query &= Q(region__in=regions) | Q(city__icontains=location)
    employement_type = get_object_or_404(models.EmployementType, pk=employement_type) if employement_type and employement_type != 'all' else None
    query &= Q(employement_type=employement_type) if employement_type else Q()
    category=get_object_or_404(models.Category, pk=cat) if cat and cat != 'all' else None
    query &= Q(categories__pk__contains=category.pk) if category else Q()


    jobs = models.Job.objects.filter( query )
    return jobs, category, employement_type, regions , search_query

def companyView(request, companyID, **kwargs):
    is_logged_in = request.user.is_authenticated and hasattr(request.user, 'company')

    if not companyID and is_logged_in:
        company = request.user.company
        jobForm = forms.JobForm()
    else:
        company = get_object_or_404(models.Company, pk=companyID)
    
    
    jobs = company.jobs.filter(is_draft=False)
    fact_open_jobs = jobs.filter(status=constants.JOB_STATUS_OPEN).count()
    fact_total_jobs = jobs.count()
    #fact_total_applicants = models.Employee.objects.filter(applications__in = jobs)# jobs.annotate(number_applicants = Count('applicants', distinct=True)).aggregate(company_total_applicants = Sum('number_applicants'))
    fact_total_applications = jobs.annotate(application_numbers = Count('applications')).aggregate(company_total_applications = Sum('application_numbers')) or 0
    
    recent_jobs = jobs[:3]

    if kwargs.get('jobStatus'):
        jobs = companyJobStatusHelper(jobs, kwargs.get('jobStatus')) 
    elif kwargs.get('jobEmpType'):
        jobs = companyJobEmpTypeHelper(jobs, kwargs.get('jobEmpType')) 
    elif kwargs.get('categoryID'):
        jobs = companyJobCategoryHelper(jobs, kwargs.get('categoryID'))
    
    page_number = request.GET.get('page', 1)
    paginator = Paginator(jobs, constants.PAG_JOB_NUMBER)
    current_page = paginator.page(page_number)
    jobs = current_page.object_list
    categories = models.Category.objects.all()
    employement_types = models.EmployementType.objects.all()
    job_statuses = constants.JOB_STATUS
    if request.GET.get('messageSent'):
        messageSent = 'Message is sucesfully sent.';

    messageForm = forms.MessageForm()
    return render(request, 'company_detail.tmp', locals())

def companyDetailView(request):
    is_logged_in = request.user.is_authenticated and hasattr(request.user, 'company')

    if not companyID and is_logged_in:
        company = request.user.company
        jobForm = forms.JobForm()
    else:
        company = get_object_or_404(models.Company, pk=companyID)
    
    
    jobs = company.jobs.filter(is_draft=False)
    fact_open_jobs = jobs.filter(status=constants.JOB_STATUS_OPEN).count()
    fact_total_jobs = jobs.count()
    #fact_total_applicants = models.Employee.objects.filter(applications__in = jobs)# jobs.annotate(number_applicants = Count('applicants', distinct=True)).aggregate(company_total_applicants = Sum('number_applicants'))
    fact_total_applications = jobs.annotate(application_numbers = Count('applications')).aggregate(company_total_applications = Sum('application_numbers')) or 0
    
    recent_jobs = jobs[:3]

    if kwargs.get('jobStatus'):
        jobs = companyJobStatusHelper(jobs, kwargs.get('jobStatus')) 
    elif kwargs.get('jobEmpType'):
        jobs = companyJobEmpTypeHelper(jobs, kwargs.get('jobEmpType')) 
    elif kwargs.get('categoryID'):
        jobs = companyJobCategoryHelper(jobs, kwargs.get('categoryID'))
    
    page_number = request.GET.get('page', 1)
    paginator = Paginator(jobs, constants.PAG_JOB_NUMBER)
    current_page = paginator.page(page_number)
    jobs = current_page.object_list
    categories = models.Category.objects.all()
    employement_types = models.EmployementType.objects.all()
    job_statuses = constants.JOB_STATUS
    
    return render(request, 'company_detail.tmp', locals())

@login_required
def companyMessage(request, companyID):
    company = get_object_or_404(models.Company, pk=companyID)
    if request.method == "POST":
        messageForm = forms.MessageForm(request.POST)
        if messageForm.is_valid():
            message = messageForm.save(commit=False)
            message.company = company
            message.sender = request.user
            message.save()

    return redirect('/companies/company-' + str(companyID) + '/?messageSent=true')

def companyJobStatusHelper(company_jobs, status):
    return company_jobs.filter(status=status)

def companyJobEmpTypeHelper(company_jobs, employement_type):
    return company_jobs.filter(employement_type__pk = employement_type)

def companyJobCategoryHelper(company_jobs, categoryID):
    return company_jobs.filter(categories__id__contains = categoryID)

def companyListView(request, regionID=None):
    companies =  models.Company.objects.all()
    if regionID:
        region = get_object_or_404(models.Region, pk=regionID)
        companies = companies.filter(region = region)

    featured_companies = companies.filter(jobs__status = constants.JOB_STATUS_OPEN).annotate(job_count=Count('jobs')).order_by('-job_count')[:4]
    regions = models.Region.objects.all()
    recent_jobs = models.Job.objects.filter(status=constants.JOB_STATUS_OPEN)[:5]
    return render(request, 'companies.tmp', locals())

def employeeSignupView(request):
    user_form = forms.UserForm()
    employee_form = forms.EmployeeForm()
    userNameForm = forms.UserNameForm()
    if request.method == "POST":
        import datetime
        userData = request.POST.copy()
        user_form = forms.UserForm(userData)
        userNameForm = forms.UserNameForm(userData)
        employee_form = forms.EmployeeForm(request.POST, request.FILES)

        newPassword = request.POST.get('pwd')
        newPasswordRepeat = request.POST.get('pwd_confirm')
        print request.POST, newPassword, newPasswordRepeat
        if newPassword != newPasswordRepeat:

            passerr = "The new password doesnt match. Please provide matching password"
        
        elif userNameForm.is_valid() and employee_form.is_valid() and user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(newPassword)
            user.username = userNameForm.cleaned_data.get('username')
            user.save()
            employee = employee_form.save(commit=False)
            employee.user = user
            employee.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return redirect('/employee/build-resume/')
        else:
            err = "Failed to register. Please try again."
            print employee_form.errors, user_form.errors
    
    return render(request, 'signuptmp.tmp', locals())
    
 

@login_required(login_url='/company/admin/login/')
def companyCreateJobView(request, jobID=None):
    jobForm = forms.JobForm()
    job = None
    if jobID:
        job = get_object_or_404(models.Job, pk=jobID)
        jobForm = forms.JobForm(instance=job)


    if request.method == "POST":
        jobForm = forms.JobForm(request.POST, instance=job)
        if jobForm.is_valid():
            job = jobForm.save(commit=False);
            job.company = request.user.company
            job.save()
            return redirect('/company/')
        print jobForm.errors
    
    return render(request, 'create_job.tmp', locals())
        
def employeeLoginView(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        print("User",user, request.POST.get('username'), request.POST.get('password'))

        if user and hasattr(user, 'employee'):
            login(request, user)

            return redirect('/employee/build-resume/')
        
        err = "Login Failed. Try again"
    next_url = request.GET.get('next') if request.GET.get('next') else '/employee/'
    return render(request, "employeeLogin.tmp", locals())



@login_required
@user_passes_test(functions.is_employee)
def employeeView(request):
    is_logged_in_as_emp = True
    
    employee = request.user.employee
    pro_active_tab = 'profile-tab-active'
    empPercent = functions.calc_emp_percent(employee)
    return render(request, "employee_profile.tmp", locals())


@login_required
def employeeOtherView(request, employeeID):
    print employeeID, "EMPL ID"
    employee = get_object_or_404(models.Employee, pk=employeeID)    
    pro_active_tab = 'profile-tab-active'
    return render(request, "employee_profile.tmp", locals())

    

@login_required
@user_passes_test(functions.is_employee)
def buildResume(request, section=None, pk=None, add=None):
    global build_resume_redirects
    build_resume_redirect_s = build_resume_redirects
    is_logged_in_as_emp = True
    employee = request.user.employee
    build_active_tab = 'profile-tab-active'
    if section == constants.EDIT_SEC_EXPR:
        experienceObj = None

        if pk:
            experienceObj = get_object_or_404(models.Experience, pk=pk)

        experienceForm = forms.ExperienceForm(instance=experienceObj)
        build_active_prof = 'active'

        if request.method == "POST":
            return employeExperienceView(request, experienceObj)

    elif section == constants.EDIT_SEC_EDUC:
        build_active_edu = 'active'
        educationObject = None
        if pk:
            educationObject = get_object_or_404(models.Education, pk=pk)
        
        educationForm = forms.EducationForm(instance=educationObject)
        if request.method=="POST":
            return employeeEducationView(request, educationObject)

    elif section == constants.EDIT_SEC_WEBS:
        websiteForm = forms.WebisteInfoForm()
        build_active_edu = 'active'
        if request.method == "POST":
            return employeWebsiteInfoView(request)

    elif section == constants.EDIT_SEC_GENR:
        build_active_gen = 'active'
        if request.method == "POST":
            employeeForm = forms.EmployeeForm(request.POST, request.FILES, instance=request.user.employee)
            userForm = forms.UserForm(request.POST, instance=request.user)
            
            if employeeForm.is_valid() and userForm.is_valid():
                userForm.save()
                employeeForm.save()
                return redirect('/employee/build-resume/general/')
            print employeeForm.errors, "GENERAL ERRORS"
        else:
            employeeForm = forms.EmployeeForm(instance = request.user.employee)
            userForm = forms.UserForm(instance=request.user)

    elif section == constants.EDIT_SEC_CV:
        build_active_resume = 'active'
        cvObject = None
        if pk:
            cvObject = get_object_or_404(models.CV, pk=pk)

        if request.method == "POST":
            cvForm = forms.CVForm(request.POST, request.FILES, instance=cvObject)
            
            if cvForm.is_valid() :
                cv = cvForm.save(commit=False)
                cv.employee = request.user.employee
                cv.save()
                return redirect('/employee/build-resume/cv')
            else:
                print cvForm.errors
        else:
            cvForm = forms.CVForm(instance=cvObject)
    elif section == constants.EDIT_SEC_SUM:
        build_active_sum = 'active'
        summaryForm = forms.EmployeeAboutMeForm(instance=request.user.employee)
        if request.method == 'POST':
            summaryForm = forms.EmployeeAboutMeForm(request.POST, instance=request.user.employee)
            if summaryForm.is_valid():
                summary = summaryForm.save()
                return redirect( '/employee/build-resume/summary' )

    elif section == constants.EDIT_SEC_VOL:
        build_active_vol = 'active'
        volunteerForm = forms.EmployeeVolunteerForm(instance=request.user.employee)
        if request.method == 'POST':
            volunteerForm = forms.EmployeeVolunteerForm(request.POST, instance=request.user.employee)
            if volunteerForm.is_valid():
                summary = volunteerForm.save()
                return redirect('/employee/build-resume/volunteer')
    elif section == constants.EDIT_SEC_REFER:
        build_active_ref = 'active'
        
        referenceObject = None
        if pk:
            referenceObject = get_object_or_404(models.References, pk=pk)
        
        if request.method == "POST":
            referenceForm = forms.ReferenceForm(request.POST, instance=referenceObject)
            if referenceForm.is_valid() :
                reference = referenceForm.save(commit=False)
                reference.employee = request.user.employee
                reference.save()
                return redirect('/employee/build-resume/reference')
            else:
                print referenceForm.errors
        else:
            referenceForm = forms.ReferenceForm(instance=referenceObject)

    elif section == constants.EDIT_SEC_LINK:
        build_active_worklink = 'active'

        workLinkObj = None
        if pk:
            workLinkObj = get_object_or_404(models.WorkLink, pk=pk)

        if request.method == "POST":
            workLinkForm = forms.WorkLinkForm(request.POST, instance=workLinkObj)
            if workLinkForm.is_valid() :
                workLink = workLinkForm.save(commit=False)
                workLink.employee = request.user.employee
                workLink.save()
                return redirect('/employee/build-resume/worklink/')
            else:
                print workLinkForm.errors
        else:
            workLinkForm = forms.WorkLinkForm(instance=workLinkObj)

    elif section == constants.EDIT_SEC_SAMP:
        build_active_worksample = 'active'
        worksampleObj = None
        if pk:
            worksampleObj = get_object_or_404(models.WorkSample, pk=pk)

        if request.method == "POST":
            workSampleForm = forms.WorkSampleForm(request.POST, request.FILES, instance=worksampleObj)
            if workSampleForm.is_valid() :
                workSample = workSampleForm.save(commit=False)
                workSample.employee = request.user.employee
                workSample.save()
                return redirect('/employee/build-resume/worksample')
            else:
                print workSampleForm.errors
        else:
            workSampleForm = forms.WorkSampleForm(instance=worksampleObj)
    
    elif section == constants.EDIT_SEC_ASSOC:
        build_active_assoc = 'active'

        if request.method == "POST":
            associationForm = forms.AssociationForm(request.POST)
            if associationForm.is_valid() :
                association = associationForm.save(commit=False)
                association.employee = request.user.employee
                association.save()
                return redirect('/employee/')
            else:
                print associationForm.errors
        else:
            associationForm = forms.AssociationForm()

    elif section == constants.EDIT_SEC_SKILL:
        build_active_skill = 'active'
        skillForm = forms.SkillForm()
        if request.method == 'POST':
            return employeSkillView(request)
    
    done_sections = functions.getSavedResumeSections(employee)
    return render(request, "build.resume.tmp", locals())

@login_required
@user_passes_test(functions.is_employee)
def deleteResumeData(request, section, pk):
    if section == constants.EDIT_SEC_EXPR:
        try:
            experienceObject = request.user.employee.experiences.get(pk=pk)
            experienceObject.delete()

        except models.Experience.DoesNotExist:
            pass
            
        return redirect('/employee/build-resume/experience/')
    
    elif section == constants.EDIT_SEC_LINK:
        try:
            worklinkObject = request.user.employee.worklinks.get(pk=pk)
            worklinkObject.delete()

        except models.WorkLink.DoesNotExist:
            pass
            
        return redirect('/employee/build-resume/worklink/')
    elif section == constants.EDIT_SEC_REFER:
        try:
            referenceObject = request.user.employee.references.get(pk=pk)
            referenceObject.delete()

        except models.References.DoesNotExist:
            pass
            
        return redirect('/employee/build-resume/reference/')
    
    elif section == constants.EDIT_SEC_SKILL:
        try:
            skill = request.user.employee.skills.get(pk=pk)
            skill.delete()

        except models.Skill.DoesNotExist:
            pass
            
        return redirect('/employee/build-resume/skill/')  

    elif section == constants.EDIT_SEC_EDUC:
        try:
            education = request.user.employee.educations.get(pk=pk)
            education.delete()

        except models.Education.DoesNotExist:
            pass
            
        return redirect('/employee/build-resume/education/')  
    
    elif section == constants.EDIT_SEC_SAMP:
        try:
            worksample = request.user.employee.worksamples.get(pk=pk)
            worksample.delete()

        except models.WorkSample.DoesNotExist:
            pass
            
        return redirect('/employee/build-resume/worksample/')   
    
    elif section == constants.EDIT_SEC_CV:
        try:
            cv = request.user.employee.cvs.get(pk=pk)
            cv.delete()

        except models.CV.DoesNotExist:
            pass
            
        return redirect('/employee/build-resume/cv/') 
@login_required
@user_passes_test(functions.is_employee)
def employeExperienceView(request, experienceObj):
    global build_resume_redirects
    if request.method == 'POST':
        experienceForm = forms.ExperienceForm(request.POST, instance=experienceObj)
        if experienceForm.is_valid():
            experience = experienceForm.save(commit=False)
            experience.employee = request.user.employee
            experience.save()
            return redirect( '/employee/build-resume/experience')
        else:
            print(experienceForm.errors)
    
    pro_active_tab = 'profile-tab-active'
    build_resume_redirect_s = build_resume_redirects
    return render(request, "employee_profile.tmp", locals())

@login_required
@user_passes_test(functions.is_employee)
def employeeEducationView(request, educationObject):
    
    global build_resume_redirects
    build_resume_redirect_s = build_resume_redirects

    if request.method == 'POST':
        educationForm = forms.EducationForm(request.POST, instance=educationObject)
        if educationForm.is_valid():
            experience = educationForm.save(commit=False)
            experience.employee = request.user.employee
            experience.save()
            return redirect('/employee/build-resume/education/')
        else:
            print("EDUCATION FORM ERROS", educationForm.errors)
    
    pro_active_tab = 'profile-tab-active'
    data_me = "tabor shiferaw"
    return render(request, "employee_profile.tmp", locals())

@login_required
@user_passes_test(functions.is_employee)
def employeSkillView(request):
    if request.method == 'POST':
        skillForm = forms.SkillForm(request.POST)
        if skillForm.is_valid():
            skill = skillForm.save(commit=False)
            skill.employee = request.user.employee
            skill.save()
            return redirect('/employee/build-resume/skill')
    
    pro_active_tab = 'profile-tab-active'
    return render(request, "employee_profile.tmp", locals())

@login_required
@user_passes_test(functions.is_employee)
def employeWebsiteInfoView(request):
    if request.method == 'POST':
        websiteInfoForm = forms.WebisteInfoForm(request.POST)
        if websiteInfoForm.is_valid():
            websiteInfo = websiteInfoForm.save(commit=False)
            websiteInfo.employee = request.user.employee
            websiteInfo.save()
            return redirect('/employee/')
    
    pro_active_tab = 'profile-tab-active'
    return render(request, "employee_profile.tmp", locals())


@login_required
@user_passes_test(functions.is_employee)
def employeeJobApply(request, jobID):
    job = get_object_or_404(models.Job, pk=jobID)
    if request.user.employee.apply(job):
        return redirect('/jobs/job-%s/' % (str(jobID)))
    return redirect('/employee/build-resume/' )

@login_required
def applicationRead(request, applicationID):
    application = get_object_or_404(models.JobApplication, pk=applicationID)
    application.status = 'read'
    application.save()

    return redirect(request.GET.get('redirect_to', '/jobs/'))



@login_required
@user_passes_test(functions.is_employee)
def employeeMatchedJobView(request):
    is_logged_in_as_emp =request.user.is_authenticated and hasattr(request.user, 'employee')
    mat_active_tab = 'profile-tab-active'
    emp_pref = request.user.employee.preference if hasattr(request.user.employee, 'preference') else None
    matching_jobs = []

    instance_object =  request.user.employee.preference if hasattr(request.user.employee, 'preference') else None
    preferenceForm = forms.EmployeeJobInterestForm(instance= instance_object)
    if request.method == "POST":
        preferenceForm = forms.EmployeeJobInterestForm(request.POST, instance=instance_object)
        if preferenceForm.is_valid():
            preference = preferenceForm.save(commit=False)
            preference.employee = request.user.employee
            preference.save()

    if emp_pref:
        query_condition = Q(region = emp_pref.job_region) |  Q(employement_type = emp_pref.employement_type) | (Q(salary__gte = emp_pref.salary_start) & Q(salary__lte = emp_pref.salary_end))
    #query_condition |= Q(categories__contains = emp_pref.job_category)
        employee = request.user.employee
        matching_jobs = models.Job.objects.filter( query_condition )
        matching_jobs_percented = {}
        count_matches = 0
        comparing_factors = 5.0

    for matching_job in matching_jobs:
        if matching_job.region == emp_pref.job_region:
            count_matches += 1

        
        if emp_pref.job_category in matching_job.categories.all():
            count_matches += 1

        if matching_job.employement_type == emp_pref.employement_type:
            count_matches += 1

        if emp_pref.salary_start <= matching_job.salary <= emp_pref.salary_end:
            count_matches += 2
        elif emp_pref.salary_start <= matching_job.salary:
            count_matches += 1

        matching_job.match_percent = (count_matches/comparing_factors) * 100
        if matching_job.match_percent < 25:
            matching_job.match_color = 'color-2'
        elif matching_job.match_percent <= 50:
            matching_job.match_color = 'color-3'
        elif matching_job.match_percent <= 75:
            matching_job.match_color = 'color-1'
        elif matching_job.match_percent <= 100:
            matching_job.match_color = 'color-4'

    categories = models.Category.objects.filter(jobs__status = constants.JOB_STATUS_OPEN).annotate(job_count=Count('jobs')).order_by('-job_count')
    featured_categories = categories[:6]
    recent_jobs = models.Job.objects.filter(is_draft=False)[:5]
    job_statuses = constants.JOB_STATUS
    regions = models.Region.objects.all()

    return render(request, 'employee_matched_jobs.tmp', locals())



@login_required
@user_passes_test(functions.is_employee)
def employeeAppliedJobs(request):
    is_logged_in_as_emp =request.user.is_authenticated and hasattr(request.user, 'employee')
    app_active_tab = 'profile-tab-active'
    #emp_pref = request.user.employee.preference
    #query_condition = Q(region = emp_pref.job_region) |  Q(employement_type = emp_pref.employement_type) | (Q(salary__gte = emp_pref.salary_start) & Q(salary__lte = emp_pref.salary_end))
    #query_condition |= Q(categories__contains = emp_pref.job_category)
    print("user applY", request.user.employee.applications.all())
    applied_jobs = request.user.employee.applications.all()
    employee = request.user.employee
    categories = models.Category.objects.filter(jobs__status = constants.JOB_STATUS_OPEN).annotate(job_count=Count('jobs')).order_by('-job_count')
    featured_categories = categories[:6]
    recent_jobs = models.Job.objects.filter(is_draft=False)[:5]
    job_statuses = constants.JOB_STATUS
    regions = models.Region.objects.all()

    recent_blogs = eventModels.Blog.objects.all().order_by('-created_at')[:3]


    return render(request, 'emplooyee_applied_jobs.tmp', locals())


def blogListView(request, articleType='blogs', categoryID=None):
    articleType={
        'news' : constants.ARTICLE_NEWS,
        'blogs' : constants.ARTICLE_BLOG
    }[articleType]

    if categoryID:
        blogs = eventModels.Blog.objects.filter(categories__id__contains = categoryID)
    else:
        blogs = eventModels.Blog.objects.all() 

    blogs = blogs.filter(article_type=articleType)
    is_news_article = True if articleType == constants.ARTICLE_NEWS else False
    paginator = Paginator(blogs, constants.PAG_BLOG_NUMBER)

    page_number = request.GET.get('page', 1)
    current_page = paginator.page(page_number)
    blogs = current_page.object_list

    postcategories = eventModels.PostCategories.objects.all()
    recent_blogs = eventModels.Blog.objects.filter(article_type=articleType).order_by('-created_at')[:5]

    return render(request, 'blogs.tmp', locals())

def blogDetailView(request, blogID):
    blog = get_object_or_404(eventModels.Blog, pk=blogID)
    blog.view_count+=1
    blog.save()
    postcategories = eventModels.PostCategories.objects.all()
    recent_blogs = eventModels.Blog.objects.all().order_by('-created_at')[:5]
    commentForm = eventForms.CommentForm()
    comments = blog.comments.all()
    blog_side_ads = eventModels.Advertisement.objects.filter(placement=constants.AD_PLACE_BLOGDETAIL_SIDE)
    
    return render(request, 'blog-detail.tmp', locals())


@login_required
def commentView(request, blogID):
    blog = get_object_or_404(eventModels.Blog, pk=blogID)
    if request.method == "POST":
        commentForm = eventForms.CommentForm(request.POST)
        if commentForm.is_valid():
            print "IAM HERE",request.user
            comment = commentForm.save(commit=False) 
            comment.commented_by= request.user
            comment.blog = blog 
            comment.save()

    return redirect('/blogs/blog-%d/' % ( blog.pk))
#// Admin views 
@login_required
@user_passes_test(functions.is_company)
def adminCompanyView(request):
    company = request.user.company
    jobs = company.jobs.filter(is_draft=False)
    fact_open_jobs = jobs.filter(status=constants.JOB_STATUS_OPEN).count()
    fact_total_jobs = jobs.count()
    fact_total_applications = jobs.annotate(application_numbers = Count('applications')).aggregate(company_total_applications = Sum('application_numbers')) or 0
    
    companyForm = forms.CompanyForm(instance=company)
    userForm = forms.UserForm(instance=request.user)
    userNameForm = forms.UserNameForm(instance=request.user)
    
    profile_overview_active = 'active'

    if request.method == "POST":
        companyForm = forms.CompanyForm(request.POST, request.FILES, instance=company)
        userData = request.POST.copy()
        userData['username'] = request.user.username
        userForm = forms.UserForm(userData, instance=request.user)
        
        profile_edit_active = 'active'
        if companyForm.is_valid() and userForm.is_valid():
            company = companyForm.save(commit=False)
            user = userForm.save()
            company.user = user

            company.save()

            return redirect('/company/admin/')
    recent_jobs = jobs[:constants.RECENT_JOBS_NUMBER]
    categories = models.Category.objects.all()
    employement_types = models.EmployementType.objects.all()
    job_statuses = constants.JOB_STATUS

    applications = models.JobApplication.objects.filter(job__in = company.jobs.filter(is_draft=False))
    unread_applications_count = applications.filter(status='unread').count()
    unread_messages_count = request.user.company.messages.filter(status='unread').count()

    sidebar_profile_info_active = 'nav-active'
    return render(request, 'company/company-profile.tmp', locals())

@login_required(login_url='/company/admin/login/')
@user_passes_test(functions.is_company)
def adminCompanyEditUsernameView(request):
    profile_overview_active = True
    if request.method == 'POST':
        userNameForm = forms.UserNameForm(request.POST, instance=request.user)
        if userNameForm.is_valid():
            userNameForm.save()
            return redirect('/company/admin/')

        return redirect('/company/admin/edit/')

    profile_edit_active = True 
    return redirect('/company/admin/')

@login_required(login_url='/company/admin/login/')
@user_passes_test(functions.is_company)
def adminCompanyChangePasswordView(request):
    profile_overview_active = True
    if request.method == 'POST':
        oldPassword = request.POST.get('oldPassword')
        newPassword = request.POST.get('newPassword')
        newPasswordRepeat = request.POST.get('newPasswordRepeat')
        if newPassword != newPasswordRepeat:
            passerr = "The new password doesnt match. Please provide matching password"
        elif request.user.check_password(oldPassword):
            request.user.set_password(newPassword)
            request.user.save()
            return redirect('/company/admin/')
        else:
            passerr = "Invalid Old Password"
        
        profile_edit_active = True
        return redirect('/company/admin/edit/')

    return redirect('/company/admin/')

def loginCompanyView(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('pwd'))
        print(user, request.POST.get('username'), request.POST.get('pwd'))
        if user and functions.is_company(user):
            login(request, user)
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('/company/admin/')
        
        err = True
    next_url = request.GET.get('next') if request.GET.get('next') else '/company/admin/'
    return render(request, 'company/pages-signin.tmp', locals())

def signUpCompanyView(request):
        user_form = forms.UserForm()
        company_form = forms.CompanyForm()
        username_form = forms.UserNameForm()

        if request.method == "POST":
            user_form = forms.UserForm(request.POST)
            company_form = forms.CompanyForm(request.POST, request.FILES)
            username_form = forms.UserNameForm(request.POST, request.FILES)
            print request.POST
            newPassword = request.POST.get('pwd')
            repeatNewPassword = request.POST.get('pwd_confirm')
            print newPassword, repeatNewPassword, "Password confirmatin"
            if newPassword and newPassword == repeatNewPassword:
                if company_form.is_valid() and username_form.is_valid() and user_form.is_valid():
                    user = user_form.save(commit=False)
                    user.set_password(newPassword)
                    user.username = username_form.cleaned_data['username']
                    user.save()
                    company = company_form.save(commit=False)
                    company.user = user
                    company.save()
                    login(request, company.user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('/company/admin/')
            else:
                error = "The password doesnt match"
            
            print company_form.errors, user_form.errors
        return render(request, 'company/pages-signup.tmp', locals())


@login_required(login_url='/company/admin/login/')
@user_passes_test(functions.is_company)
def createJobView(request, jobID=None):
    jobForm = forms.JobForm()
    job = None
    if jobID:
        job = get_object_or_404(models.Job, pk=jobID)
        jobForm = forms.JobForm(instance=job)

    company = request.user.company
    if request.method == "POST":
        import datetime
        reqData = request.POST.copy()

        jobForm = forms.JobForm(reqData, instance=job)
        if jobForm.is_valid():
            job = jobForm.save(commit=False)
            job.company = company
            job.is_draft = True if reqData.get('save-job', False) else False
            job.save()
            jobForm.save_m2m()
            return redirect('/company/admin/jobs/')

    applications = models.JobApplication.objects.filter(job__in = company.jobs.filter(is_draft=False))
    unread_applications_count = applications.filter(status='unread').count()
    unread_messages_count = request.user.company.messages.filter(status='unread').count()

    sidebar_create_job_active = 'nav-active'
    
    return render(request, 'company/create-job.tmp', locals())
@login_required
def companyRecruitView(request):
    sidebar_recruite_active = True
    admin = request.user.is_staff
    recruitFilterForm = forms.RecruitFilterForm()
    if request.GET.get('query'):
        recruitFilterForm = forms.RecruitFilterForm(request.GET)
        query = Q()
        gender_query = None
        if request.GET.get('employement_status', None):
            query |= Q(employement_status = request.GET.get('employement_status', 1) )
        
        if request.GET.get('highest_education_level', None):
            query |= Q(highest_education_level=request.GET.get('highest_education_level'))

        if request.GET.get('ageRange', None):
            query |= Q(age=request.GET.get('ageRange'))
        
        if request.GET.get('educationTitle', None):
            query |= Q(educations__field_of_study__icontains=request.GET.get('educationTitle'))
        
        if request.GET.get('gender', None):
            query |= Q(gender=request.GET.get('gender', 'Male'))
        

        job_seekers = models.Employee.objects.filter(query ).distinct()
        job_seeker_experiences = models.Experience.objects.filter(employee__in=job_seekers).values('employee').annotate(exp=Sum(F('end_year')-F('start_year')))
        
        print job_seekers,job_seeker_experiences

        if request.GET.get('experience', None):
            try:
                experience = float(request.GET.get('experience'))
                job_seeker_experiences = job_seeker_experiences.filter(exp__gte=experience)
            except ValueError:
                pass
        job_seeker_experiences_dict = {}

        for job_seeker_experience in job_seeker_experiences:
            job_seeker_experiences_dict[job_seeker_experience['employee']] = job_seeker_experience['exp']

        job_seekers_arr = []
        for job_seeker in job_seekers:
            if job_seeker_experiences_dict.get(job_seeker.pk, False):
                job_seekers_arr.append( job_seeker)


        
        
    sidebar_recruit_active = 'nav-active'

    return render(request, 'company/recruit.tmp', locals())
    
@login_required
@user_passes_test(functions.is_company)
def companyJobListView(request, isDraft=None):
    company = request.user.company
    if not isDraft:
        sidebar_job_listing_active = 'nav-active'

        jobs = company.jobs.filter(is_draft=False)
    else:
        sidebar_job_saved_active = 'nav-active'
        jobs = company.jobs.filter(is_draft=True)

    page_number = request.GET.get('page', 1)
    paginator = Paginator(jobs, 10)
    current_page = paginator.page(page_number)
    jobs = current_page.object_list

    applications = models.JobApplication.objects.filter(job__in = company.jobs.filter(is_draft=False))
    unread_applications_count = applications.filter(status='unread').count()
    unread_messages_count = request.user.company.messages.filter(status='unread').count()

    return render(request, 'company/company.admin.joblist.tmp', locals())

@login_required
@user_passes_test(functions.is_company)
def jobDelete(request, jobID, confirmed=None):
    try:
        job = request.user.company.jobs.get(pk=jobID)
    except models.Job.DoesNotExist:
        return HttpResponse('Job Not Found', 404)

    if not confirmed:
        return render(request, 'company/company.admin.jobremoveconfirm.tmp', locals())
    else:
        job.delete()
        return redirect('/company/admin/jobs/')

@login_required
@user_passes_test(functions.is_staff)
def blogDelete(request, blogID, confirmed=None):
    blog = get_object_or_404(eventModels.Blog, pk=blogID)

    if not confirmed:
        return render(request, 'company/company.admin.blogremoveconfirm.tmp', locals())
    else:
        blog.delete()
        return redirect('/ican/blogs/')

def getJobApplications(company, filter, paramQuery):
    company_jobs = company.jobs.filter(is_draft=False)
    applications = models.JobApplication.objects.filter(job__in = company_jobs)
    unread_applications_count = applications.filter(status='unread').count()

    application_filter = 'All'
    if filter=='read' or filter=='unread':
        applications = applications.filter(status=filter)
        application_filter = filter.capitalize()
    elif filter=='today':
        applications = models.JobApplication.todays(company_jobs)
        application_filter = 'Today\'s'
    elif filter=='yesterday':
        applications = models.JobApplication.yesterdays(company_jobs)
        application_filter = "Yesterday's"
    elif filter=='last7':
        applications = models.JobApplication.last7days(company_jobs)
        application_filter = "Last Seven days"
    if paramQuery:
        queryData = paramQuery
        queries = queryData.split(',')
        query = Q()
        for qry in queries:
            inside_query = Q()
            
            for inside_qry in qry.split(' '):
                inside_query &= Q(job__title__icontains=inside_qry)

            query |= Q(inside_query)
        applications = applications.filter(query)

    return application_filter, applications, unread_applications_count

@login_required
@user_passes_test(functions.is_company)
def applications(request, filter=None):
    company = request.user.company
    unread_messages_count = request.user.company.messages.filter(status='unread').count()
    application_filter, applications, unread_applications_count = getJobApplications(company, filter, request.GET.get('query'))
    paramQuery = request.GET.get('query')
    sidebar_applications_active = 'nav-active'
    return render(request, 'company/applications.tmp', locals())

def saveApplications(request):
    print request.GET.getlist('applicatinID')
    applications = models.JobApplication.objects.filter(pk__in=request.GET.getlist('applicatinID'))
    
    return render(request, 'applications.save.tmp', locals())

def advertisement(request):
    advertisement = models.Advertisement.objects.filter()
@login_required
@user_passes_test(functions.is_company)
def messages(request, filter=None):
    messages = request.user.company.messages.all()
    unread_messages_count = messages.filter(status='unread').count()

    sidebar_messages_active = 'nav-active'
    
    message_filter = 'All'
    if filter=='read' or filter=='unread':
        messages = messages.filter(status=filter)
        message_filter = filter.capitalize()
    elif filter=='today':
        messages = models.Message.todays()
        message_filter = 'Today\'s'
    elif filter=='yesterday':
        messages = models.Message.yesterdays()
        message_filter = "Yesterday's"
    elif filter=='last7':
        messages = models.Message.last7days()
        message_filter = "Last Seven days"

    return render(request, 'company/messages.tmp', locals())

@login_required
def contactMessages(request, filter=None):
    messages = models.Contact.objects.all()
    unread_messages_count = messages.filter(status='unread').count()

    sidebar_messages_active = 'nav-active'
    
    message_filter = 'All'
    if filter=='read' or filter=='unread':
        messages = messages.filter(status=filter)
        message_filter = filter.capitalize()
    elif filter=='today':
        messages = models.Message.todays()
        message_filter = 'Today\'s'
    elif filter=='yesterday':
        messages = models.Message.yesterdays()
        message_filter = "Yesterday's"
    elif filter=='last7':
        messages = models.Message.last7days()
        message_filter = "Last Seven days"

    return render(request, 'admin/messages.tmp', locals())
@login_required
def contact_message_detail(request, messageID):
    message = get_object_or_404(models.Contact, pk=messageID)
    message.status = 'read'
    message.save()

    unread_messages_count = models.Contact.objects.filter(status='unread').count()

    return render(request, 'admin/contact.message.detail.tmp', locals())

@login_required
def message_detail(request, messageID):
    message = get_object_or_404(models.Message, pk=messageID)
    message.status = 'read'
    message.save()

    unread_messages_count = request.user.company.messages.filter(status='unread').count()


    return render(request, 'company/message-detail.tmp', locals())

@login_required
def message_delete(request, messageID):
    message = get_object_or_404(models.Message, pk=messageID)
    message.delete()

    return redirect('/company/admin/messages/')


def logoutView(request):
    logout(request)

    return redirect('/')

def testView(request):
    return HttpResponse('test')

def events(request, tagID=None):
    events = eventModels.Event.objects.all()
    recent_events = events[:5]
    if tagID:
        events = events.filter(tags__pk__contains = tagID)

    page_number = request.GET.get('page', 1)
    paginator = Paginator(events, constants.PAG_JOB_NUMBER)
    current_page = paginator.page(page_number)
    events = current_page.object_list
    tags = eventModels.EventTag.objects.all()
    events = events.annotate(upcoming=F('event_start_date') - datetime.date.today())
    
    return render(request, "event/events.tmp", locals())

def eventDetail(request, eventID):
    event = get_object_or_404(eventModels.Event, pk=eventID)
    tags = eventModels.EventTag.objects.all()
    recent_events = eventModels.Event.objects.all()[:5]
    return render(request, "event/event.detail.tmp", locals())

@login_required
@user_passes_test(functions.is_employee)
def makeAppointment(request):
    appointmentForm = eventForms.AppointmentForm()
    if request.method == "POST":
        appointmentForm = eventForms.AppointmentForm(request.POST)
        
        if appointmentForm.is_valid():

            appointment = appointmentForm.save(commit=False)
            if not appointment.slot.appointments.filter(date=appointment.date):
                appointment.user = request.user.employee
                appointment.save()
                suc = "Appoointment succesfully made!"
            else:
                error = "The slot you chose is occupied on the spcified date. Please try another time slot"
        

    return render(request, 'event/make-appointment.tmp', locals())

@login_required
@user_passes_test(functions.is_employee)
def appointments(request):
    appointments = request.user.employee.appointments.all()
    
    return render(request, 'appointments.tmp', locals())
