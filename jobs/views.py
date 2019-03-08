# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from jobs import models, forms
from django.db.models import Q,Count, Sum
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from jobs import constants
from django.contrib.auth.decorators import login_required

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
        status = request.GET.get('status', 'all')
        jobs = jobSearchHelper(search_query, cat, reg, status)
        search_result_count = jobs.count()

    else:
        jobs = jobCategoryListHelper()
    
    #check for response message 
    
    # do pagination 
    if jobs:
        page_number = request.GET.get('page', 1)
        paginator = Paginator(jobs, 3)
        current_page = paginator.page(page_number)
        jobs = current_page.object_list

    regions = models.Region.objects.all()
    categories = models.Category.objects.filter(jobs__status = constants.JOB_STATUS_OPEN).annotate(job_count=Count('jobs')).order_by('-job_count')
    featured_categories = categories[:6]
    recent_jobs = models.Job.objects.order_by('created_at')[:5]
    job_statuses = constants.JOB_STATUS
    recent_blogs = models.Blog.objects.all().order_by('-created_at')[:3]

    return render(request, template_name, locals())

#view helper functions for job 
def jobDetailHelper(jobID, request):
    job = get_object_or_404(models.Job, pk=jobID)

    if request.user.is_authenticated and hasattr(request.user, 'employee'):
        job.applied_already = job.applicants.filter(pk = request.user.employee.pk)

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

def jobSearchHelper(search_query, cat='all', reg='all', status='all'):
    query = Q(title__icontains=search_query)
    query &= Q(region__id = reg) if reg and reg != 'all' else Q()
    print ("status", status)
    query &= Q(status = status) if status and status != 'all' else Q()
    query &= Q(categories__id__contains=cat) if cat and cat != 'all' else Q()

    jobs = models.Job.objects.filter( query )
    return jobs 

def companyView(request, companyID, **kwargs):
    company = get_object_or_404(models.Company, pk=companyID)
    jobs = company.jobs.all()
    fact_open_jobs = jobs.filter(status=constants.JOB_STATUS_OPEN).count()
    fact_total_jobs = jobs.count()
    #fact_total_applicants = models.Employee.objects.filter(applications__in = jobs)# jobs.annotate(number_applicants = Count('applicants', distinct=True)).aggregate(company_total_applicants = Sum('number_applicants'))
    fact_total_applications = jobs.annotate(application_numbers = Count('applications')).aggregate(company_total_applications = Sum('application_numbers'))
    
    recent_jobs = jobs.order_by('created_at')[:3]

    if kwargs.get('jobStatus'):
        jobs = companyJobStatusHelper(jobs, kwargs.get('jobStatus')) 
    elif kwargs.get('jobEmpType'):
        jobs = companyJobEmpTypeHelper(jobs, kwargs.get('jobEmpType')) 
    elif kwargs.get('categoryID'):
        jobs = companyJobCategoryHelper(jobs, kwargs.get('categoryID'))
    
    page_number = request.GET.get('page', 1)
    paginator = Paginator(jobs, 3)
    current_page = paginator.page(page_number)
    jobs = current_page.object_list
    categories = models.Category.objects.all()
    employement_types = models.EmployementType.objects.all()
    job_statuses = constants.JOB_STATUS
    print(job_statuses)
    return render(request, 'company_detail.tmp', locals())

def companyJobStatusHelper(company_jobs, status):
    return company_jobs.filter(status=status)

def companyJobEmpTypeHelper(company_jobs, employement_type):
    return company_jobs.filter(employement_type__pk = employement_type)

def companyJobCategoryHelper(company_jobs, categoryID):
    return company_jobs.filter(categories__id__contains = categoryID)

def companyListView(request):
    companies =  models.Company.objects.all()
    featured_companies = companies.filter(jobs__status = constants.JOB_STATUS_OPEN).annotate(job_count=Count('jobs')).order_by('-job_count')[:4]
    regions = models.Region.objects.all()
    recent_jobs = models.Job.objects.filter(status=constants.JOB_STATUS_OPEN).order_by('created_at')[:5]
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
            employee = employee_form.save(commit=False)
            employee.user = user
            employee.save()
            suc = "Your account is created succesfully"
    
    return render(request, 'signup.tmp', locals())
    
def companySignupView(request):
    user_form = forms.UserForm()
    company_form = forms.CompanyForm()

    if request.method == "POST":
        import datetime
        userData = request.POST.copy()
        userData['date_joined'] = datetime.date.today()
        userData['last_login'] = datetime.datetime.now()
        userData['first_name'] = "company"
        userData['last_name'] = "company"

        user_form = forms.UserForm(userData)
        company_form = forms.CompanyForm(request.POST, request.FILES)
        if company_form.is_valid() and user_form.is_valid():
            user = user_form.save()
            company = company_form.save(commit=False)
            company.user = user
            company.save()
            suc = "Your account is created succesfully"
        else:
            error = str(user_form.errors.as_data())
    return render(request, 'companySignup.tmp', locals())

def employeeLoginView(request):
    if request.user.is_authenticated:
        return redirect('/employee/')

    if request.method == "POST":
        user = authenticate(username='john', password='secret')
        if not user:
            login(request, user)
            return redirect('/employee/')

    return render(request, "employeeLogin.tmp", locals())

@login_required
def employeeView(request, employeeID=None):

    if employeeID:
        employee = get_object_or_404(models.Employee, pk=employeeID)
    else:
        employee = request.user.employee
        level_jobs = models.Job.objects.filter(level__in = request.user.employeejobinterest.job_level.all())
        type_jobs = models.Job.objects.filter(employement_type__in = request.user.employeejobinterest.employement_type.all())
        region_jobs = models.Job.objects.filter(region__in = request.user.employeejobinterest.job_region.all())
        matching_jobs_ = level_jobs.union(type_jobs).union(region_jobs).filter(status=constants.JOB_STATUS_OPEN)[:4]
        employee_applications = employee.applications.all()
        matching_jobs = []
        for matching_job in matching_jobs_:
            if matching_job not in employee_applications:
                matching_jobs.append(matching_job)

    categories = models.Category.objects.all()
    employement_types = models.EmployementType.objects.all()
    job_statuses = constants.JOB_STATUS
    recent_jobs = models.Job.objects.order_by('created_at')[:5]
    open_applied_jobs = employee.applications.filter(status=constants.JOB_STATUS_OPEN)
    return render(request, "employee_profile.tmp", locals())


@login_required
def employeeJobApply(request, jobID):
    job = get_object_or_404(models.Job, pk=jobID)
    if request.user.employee.apply(job):
        return redirect('/jobs/job-%s/' % (str(jobID)))
    return redirect('/jobs/job-%s/' %(str(jobID)) )

def blogListView(request, categoryID=None):
    
    if categoryID:
        blogs = models.Blog.objects.filter(categories__id__contains = categoryID)
    else:
        blogs = models.Blog.objects.all() 

    paginator = Paginator(blogs, 4)

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



def testView(request):
    return HttpResponse('test')

    
