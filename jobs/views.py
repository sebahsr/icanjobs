# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from jobs import models, forms
from django.db.models import Q,Count, Sum
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from jobs import constants, functions
from django.contrib.auth.decorators import login_required,user_passes_test

# Create your views here.
def jobView(request, **kwargs):

    template_name = "jobs.tmp"
    jobs = None 

    if kwargs.get('regionID', False):
        jobs = jobRegionListHelper(kwargs['regionID'])

    elif kwargs.get('categoryID', False):
        jobs = jobCategoryListHelper(kwargs['categoryID'])

    elif kwargs.get('jobID', False):
        job = jobDetailHelper(kwargs['jobID'], request)
        template_name = "job_detail.tmp"


    elif kwargs.get('search', False):
        search_query = request.GET.get('q', '')
        cat = request.GET.get('cat', 'all') 
        reg = request.GET.get('reg', 'all') 
        employement_type = request.GET.get('employement_type', 'all')
        jobs = jobSearchHelper(search_query, cat, reg, employement_type)
        search_result_count = jobs.count()

    else:
        jobs = jobCategoryListHelper()
    
    #check for response message 
    
    # do pagination 
    if jobs: 
        page_number = request.GET.get('page', 1)
        paginator = Paginator(jobs, constants.PAG_JOB_NUMBER)
        current_page = paginator.page(page_number)
        jobs = current_page.object_list

    regions = models.Region.objects.all()
    categories = models.Category.objects.filter(jobs__status = constants.JOB_STATUS_OPEN).annotate(job_count=Count('jobs')).order_by('-job_count')
    featured_categories = categories[:6]
    recent_jobs = models.Job.objects.all()[:5]
    employement_types = models.EmployementType.objects.all()
    recent_blogs = models.Blog.objects.all().order_by('-created_at')[:3]

    return render(request, template_name, locals())

#view helper functions for job 
def jobDetailHelper(jobID, request):
    job = get_object_or_404(models.Job, pk=jobID)
    job.eligible_to_apply = request.user.is_authenticated and hasattr(request.user, 'employee') and job.apply_through_portal
    if job.eligible_to_apply:
        job.applied_already = job.applicants.filter(pk = request.user.employee.pk)
        job.eligible_to_apply = True

    return job
    

def jobCategoryListHelper(categoryID=None):
    if not categoryID:
        jobs = models.Job.objects.all()
    else:
        category = get_object_or_404(models.Category, pk=categoryID)
        jobs = category.jobs.all()

    return jobs

def jobRegionListHelper(regionID=None):
    region = get_object_or_404(models.Region, pk=regionID)
    jobs = region.jobs.all()
    return jobs

def jobSearchHelper(search_query, cat='all', reg='all', employement_type='all'):
    query = Q(title__icontains=search_query)
    query &= Q(region__id = reg) if reg and reg != 'all' else Q()

    query &= Q(employement_type__id = employement_type) if employement_type and employement_type != 'all' else Q()
    query &= Q(categories__id__contains=cat) if cat and cat != 'all' else Q()

    jobs = models.Job.objects.filter( query )
    return jobs 

def companyView(request, companyID, **kwargs):
    is_logged_in = request.user.is_authenticated and hasattr(request.user, 'company')

    if not companyID and is_logged_in:
        company = request.user.company
        jobForm = forms.JobForm()
    else:
        company = get_object_or_404(models.Company, pk=companyID)
    
    
    jobs = company.jobs.all()
    fact_open_jobs = jobs.filter(status=constants.JOB_STATUS_OPEN).count()
    fact_total_jobs = jobs.count()
    #fact_total_applicants = models.Employee.objects.filter(applications__in = jobs)# jobs.annotate(number_applicants = Count('applicants', distinct=True)).aggregate(company_total_applicants = Sum('number_applicants'))
    fact_total_applications = jobs.annotate(application_numbers = Count('applications')).aggregate(company_total_applications = Sum('application_numbers'))
    
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

def companyDetailView(request):
    is_logged_in = request.user.is_authenticated and hasattr(request.user, 'company')

    if not companyID and is_logged_in:
        company = request.user.company
        jobForm = forms.JobForm()
    else:
        company = get_object_or_404(models.Company, pk=companyID)
    
    
    jobs = company.jobs.all()
    fact_open_jobs = jobs.filter(status=constants.JOB_STATUS_OPEN).count()
    fact_total_jobs = jobs.count()
    #fact_total_applicants = models.Employee.objects.filter(applications__in = jobs)# jobs.annotate(number_applicants = Count('applicants', distinct=True)).aggregate(company_total_applicants = Sum('number_applicants'))
    fact_total_applications = jobs.annotate(application_numbers = Count('applications')).aggregate(company_total_applications = Sum('application_numbers'))
    
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

    if request.method == "POST":
        import datetime
        userData = request.POST.copy()
        userData['date_joined'] = datetime.date.today()
        userData['last_login'] = datetime.datetime.now()

        user_form = forms.UserForm(userData)
        employee_form = forms.EmployeeForm(request.POST, request.FILES)
        if employee_form.is_valid() and user_form.is_valid():
            user = user_form.save()
            user.is_active = True
            user.save()
            employee = employee_form.save(commit=False)
            employee.user = user
            employee.save()
            return redirect('/login/')
        else:
            err = "Failed to register. Please try again."
            print employee_form.errors, user_form.errors
    
    return render(request, 'signup.tmp', locals())
    


@login_required
def companyCreateJobView(request):
    jobForm = forms.JobForm()
    if request.method == "POST":
        jobForm = forms.JobForm(request.POST)
        if jobForm.is_valid():
            job = jobForm.save(commit=False);
            job.company = request.user.company
            job.save()
            return redirect('/company/')
        print jobForm.errors
    
    return render(request, 'create_job.tmp', locals())
        
def employeeLoginView(request):
    if request.user.is_authenticated:
        return redirect('/employee/')

    if request.method == "POST":
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        print("User",user, request.POST.get('username'), request.POST.get('password'))

        if user and hasattr(user, 'employee'):
            login(request, user)
            return redirect('/employee/')
        
        err = "Login Failed. Try again"

    return render(request, "employeeLogin.tmp", locals())




@login_required
@user_passes_test(functions.is_employee)
def employeeView(request):
    is_logged_in_as_emp = True
    
    employee = request.user.employee
    pro_active_tab = 'profile-tab-active'
    return render(request, "employee_profile.tmp", locals())

@login_required
def employeeOtherView(request, employeeID):
    employee = get_object_or_404(models.Employee, pk=employeeID)    
    pro_active_tab = 'profile-tab-active'
    return render(request, "employee_profile.tmp", locals())



@login_required
@user_passes_test(functions.is_employee)
def employeeProfileEditView(request, section):
    employee = request.user.employee
    if section == constants.EDIT_SEC_EXPR:
        experienceForm = forms.ExperienceForm()
        if request.method == "POST":
            return employeExperienceView(request)

    elif section == constants.EDIT_SEC_EDUC:
        educationForm = forms.EducationForm()
        if request.method=="POST":
            return employeeEducationView(request)

    elif section == constants.EDIT_SEC_WEBS:
        websiteForm = forms.WebisteInfoForm()
        if request.method == "POST":
            return employeWebsiteInfoView(request)

    elif section == constants.EDIT_SEC_GENR:
        
        if request.method == "POST":
            employeeForm = forms.EmployeeForm(request.POST, request.FILES, instance=request.user.employee)
            userForm = forms.UserForm(request.POST, instance=request.user)
            
            if employeeForm.is_valid() and userForm.is_valid():
                userForm.save()
                employeeForm.save()
                return redirect('/employee/')
            print userForm.errors
        else:
            employeeForm = forms.EmployeeForm(instance = request.user.employee)
            userForm = forms.UserForm(instance=request.user)

    elif section == constants.EDIT_SEC_SKILL:
        skillForm = forms.SkillForm()
        if request.method == 'POST':
            return employeSkillView(request)

    pro_active_tab = 'profile-tab-active'
    return render(request, "employee_profile.tmp", locals())

@login_required
@user_passes_test(functions.is_employee)
def employeExperienceView(request):
    if request.method == 'POST':
        experienceForm = forms.ExperienceForm(request.POST)
        if experienceForm.is_valid():
            experience = experienceForm.save(commit=False)
            experience.employee = request.user.employee
            experience.save()
            return redirect('/employee/')
        else:
            print(experienceForm.errors)
    
    pro_active_tab = 'profile-tab-active'
    return render(request, "employee_profile.tmp", locals())

@login_required
@user_passes_test(functions.is_employee)
def employeeEducationView(request):
    if request.method == 'POST':
        educationForm = forms.EducationForm(request.POST)
        if educationForm.is_valid():
            experience = educationForm.save(commit=False)
            experience.employee = request.user.employee
            experience.save()
            return redirect('/employee/')
        else:
            print("EDUCATION FORM ERROS", educationForm.errors)
    
    pro_active_tab = 'profile-tab-active'
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
            return redirect('/employee/')
    
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
    return redirect('/jobs/job-%s/' %(str(jobID)) )

def applicationRead(request, applicationID):
    application = get_object_or_404(models.JobApplication, pk=applicationID)
    application.status = 'read'
    application.save()

    return redirect(request.GET.get('redirect_to', '/jobs/'))

@login_required
def employeePreferenceView(request, employeeID=None):

    is_logged_in_as_emp = not employeeID and request.user.is_authenticated and hasattr(request.user, 'employee')
    if is_logged_in_as_emp:
        employee = request.user.employee
    else:
        employee = get_object_or_404(models.Employee, pk=employeeID)

    pre_active_tab = 'profile-tab-active'
    instance_object =  employee.preference if hasattr(employee, 'preference') else None
    preferenceForm = forms.EmployeeJobInterestForm(instance= instance_object)
    if request.method == "POST":
        preferenceForm = forms.EmployeeJobInterestForm(request.POST, instance=instance_object)
        if preferenceForm.is_valid():
            preference = preferenceForm.save(commit=False)
            preference.employee = employee
            preference.save()
        else:
            print("PREF ERRORS", preferenceForm.errors)
    return render(request, 'employee_preference.tmp', locals())

@login_required
@user_passes_test(functions.is_employee)
def employeeMatchedJobView(request):
    is_logged_in_as_emp =request.user.is_authenticated and hasattr(request.user, 'employee')
    mat_active_tab = 'profile-tab-active'
    emp_pref = request.user.employee.preference
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
    recent_jobs = models.Job.objects.all()[:5]
    job_statuses = constants.JOB_STATUS
    regions = models.Region.objects.all()

    return render(request, 'employee_matched_jobs.tmp', locals())



@login_required
@user_passes_test(functions.is_employee)
def employeeAppliedJobs(request):
    is_logged_in_as_emp =request.user.is_authenticated and hasattr(request.user, 'employee')
    app_active_tab = 'profile-tab-active'
    emp_pref = request.user.employee.preference
    query_condition = Q(region = emp_pref.job_region) |  Q(employement_type = emp_pref.employement_type) | (Q(salary__gte = emp_pref.salary_start) & Q(salary__lte = emp_pref.salary_end))
    #query_condition |= Q(categories__contains = emp_pref.job_category)
    print("user applY", request.user.employee.applications.all())
    applied_jobs = request.user.employee.applications.all()
    employee = request.user.employee
    categories = models.Category.objects.filter(jobs__status = constants.JOB_STATUS_OPEN).annotate(job_count=Count('jobs')).order_by('-job_count')
    featured_categories = categories[:6]
    recent_jobs = models.Job.objects.all()[:5]
    job_statuses = constants.JOB_STATUS
    regions = models.Region.objects.all()

    recent_blogs = models.Blog.objects.all().order_by('-created_at')[:3]


    return render(request, 'emplooyee_applied_jobs.tmp', locals())


def blogListView(request, categoryID=None):
    
    if categoryID:
        blogs = models.Blog.objects.filter(categories__id__contains = categoryID)
    else:
        blogs = models.Blog.objects.all() 

    paginator = Paginator(blogs, constants.PAG_BLOG_NUMBER)

    page_number = request.GET.get('page', 1)
    current_page = paginator.page(page_number)
    blogs = current_page.object_list

    postcategories = models.PostCategories.objects.all()
    recent_blogs = models.Blog.objects.all().order_by('-created_at')[:5]

    return render(request, 'blogs.tmp', locals())
def blogDetailView(request, blogID):
    blog = get_object_or_404(models.Blog, pk=blogID)
    postcategories = models.PostCategories.objects.all()
    recent_blogs = models.Blog.objects.all().order_by('-created_at')[:5]
    return render(request, 'blog-detail.tmp', locals())

#// Admin views 
@login_required(login_url='/company/admin/login/')
@user_passes_test(functions.is_company)
def adminCompanyView(request):
    company = request.user.company
    jobs = company.jobs.all()
    fact_open_jobs = jobs.filter(status=constants.JOB_STATUS_OPEN).count()
    fact_total_jobs = jobs.count()
    fact_total_applications = jobs.annotate(application_numbers = Count('applications')).aggregate(company_total_applications = Sum('application_numbers'))
    
    companyForm = forms.CompanyForm(instance=company)
    userForm = forms.UserForm(instance=request.user)
    userNameForm = forms.UserNameForm(instance=request.user)
    
    profile_overview_active = 'active'

    if request.method == "POST":
        companyForm = forms.CompanyForm(instance=company, data=request.POST)
        userForm = forms.UserForm(instance=request.user, data=request.POST)
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

    applications = models.JobApplication.objects.filter(job__in = company.jobs.all())
    unread_applications_count = applications.filter(status='unread').count()
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
        return redirect('/company/admin/')

    if request.method == "POST":
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('pwd'))
        print(user, request.POST.get('username'), request.POST.get('pwd'))
        if user and functions.is_company(user):
            login(request, user)
            return redirect('/company/admin/')
        
        err = True

    return render(request, 'company/pages-signin.tmp', locals())

def signUpCompanyView(request):
        user_form = forms.UserForm()
        company_form = forms.CompanyForm()
        username_form = forms.UserNameForm()

        if request.method == "POST":
            user_form = forms.UserForm(request.POST)
            company_form = forms.CompanyForm(request.POST, request.FILES)
            username_form = forms.UserNameForm(request.POST, request.FILES)

            newPassword = request.POST.get('pwd')
            repeatNewPassword = request.POST.get('pwd_confirm')

            if newPassword and newPassword == repeatNewPassword:
                if company_form.is_valid() and username_form.is_valid() and user_form.is_valid():
                    user = user_form.save(commit=False)
                    user.set_password(newPassword)
                    user.username = username_form.cleaned_data['username']
                    user.save()
                    company = company_form.save(commit=False)
                    company.user = user
                    company.save()
                    return redirect('/company/admin/login/')
            else:
                error = "The password doesnt match"
            print company_form.errors, user_form.errors
        return render(request, 'company/pages-signup.tmp', locals())


@login_required
@user_passes_test(functions.is_company)
def createJobView(request):
    jobForm = forms.JobForm()
    company = request.user.company
    if request.method == "POST":
        import datetime
        reqData = request.POST.copy()

        jobForm = forms.JobForm(reqData)
        if jobForm.is_valid():
            job = jobForm.save(commit=False)
            job.company = company
            job.save()
            jobForm.save_m2m()
            return redirect('company/admin/jobs/')
    print jobForm.errors
    applications = models.JobApplication.objects.filter(job__in = company.jobs.all())
    unread_applications_count = applications.filter(status='unread').count()
    sidebar_create_job_active = 'nav-active'
    return render(request, 'company/create-job.tmp', locals())

@login_required
@user_passes_test(functions.is_company)
def companyJobListView(request):
    company = request.user.company
    jobs = company.jobs.all()
    page_number = request.GET.get('page', 1)
    paginator = Paginator(jobs, 5)
    current_page = paginator.page(page_number)
    jobs = current_page.object_list

    applications = models.JobApplication.objects.filter(job__in = company.jobs.all())
    unread_applications_count = applications.filter(status='unread').count()
    sidebar_job_listing_active = 'nav-active'
    return render(request, 'company/company.admin.joblist.tmp', locals())

@login_required
@user_passes_test(functions.is_company)
def applications(request, filter=None):
    company = request.user.company
    company_jobs = company.jobs.all()
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
    
    sidebar_applications_active = 'nav-active'
    return render(request, 'company/applications.tmp', locals())

def logoutView(request):
    logout(request)

    return redirect('/')

def testView(request):
    return HttpResponse('test')

    
