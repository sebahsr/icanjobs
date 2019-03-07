# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from jobs import models, forms
from django.db.models import Q,Count, Sum
from django.core.paginator import Paginator

from jobs import constants

# Create your views here.
def jobView(request, **kwargs):

    template_name = "jobs.tmp"
    jobs = None 

    if kwargs.get('regionID', False):
        jobs = jobRegionListHelper(kwargs['regionID'])

    elif kwargs.get('categoryID', False):
        jobs = jobCategoryListHelper(kwargs['categoryID'])

    elif kwargs.get('jobID', False):
        job = jobDetailHelper(kwargs['jobID'])
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
    return render(request, template_name, locals())

#view helper functions for job 
def jobDetailHelper(jobID):
    return get_object_or_404(models.Job, pk=jobID)
    

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
    fact_total_applicants = jobs.annotate(number_applicants = Count('applicants')).aggregate(company_total_applicants = Sum('number_applicants'))
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

def testView(request):
    return HttpResponse('test')
    
