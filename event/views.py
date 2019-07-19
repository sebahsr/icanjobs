# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required,user_passes_test

from django.shortcuts import render, get_object_or_404, redirect
from event import forms, models
from jobs import models as jobModels
from jobs import constants
from django.core.paginator import Paginator
from event import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request

from django.http import HttpResponse,JsonResponse

# Create your views here.

@login_required(login_url='/admin/login/')
@user_passes_test(lambda u: u.is_staff)
def dashboard(request):
    total_employees = jobModels.Employee.objects.count()
    total_employers = jobModels.Company.objects.count()
    total_jobs = jobModels.Job.objects.count()
    total_events = models.Event.objects.count()
    recent_jobs = jobModels.Job.objects.all()[:5]
    recent_companies = jobModels.Company.objects.all()[:5]
    sidebar_dashboard_active = 'profile-tab-active'
    return render(request, 'admin/dashboard.tmp', locals())


@login_required(login_url='/admin/login/')
@user_passes_test(lambda u: u.is_staff)
def createEvent(request, eventID=None):
    createEventForm = forms.EventForm()
    event = None
    if eventID:
        event = get_object_or_404(models.Event, pk=eventID)
        createEventForm = forms.EventForm(instance=event)

    if request.method == 'POST':
        createEventForm = forms.EventForm(request.POST, request.FILES, instance=event)

        if createEventForm.is_valid():
            createEventForm.save()
            return redirect('/ican/events/')

    return render(request, 'admin/create-event.tmp', locals())

@login_required(login_url='/admin/login/')
@user_passes_test(lambda u: u.is_staff)
def events(request):
    events = models.Event.objects.all()
    paginator = Paginator(events, constants.PAG_BLOG_NUMBER)

    page_number = request.GET.get('page', 1)
    current_page = paginator.page(page_number)
    events = current_page.object_list

    return render(request, 'admin/admin.eventlist.tmp', locals())


@login_required(login_url='/admin/login/')
@user_passes_test(lambda u: u.is_staff)
def createBlog(request, blogID=None):
    blogForm = forms.BlogForm()
    blog = None
    if blogID:
        blog = get_object_or_404(models.Blog, pk=blogID)
        blogForm = forms.BlogForm(instance=blog)

    if request.method == 'POST':
        blogForm = forms.BlogForm(request.POST, request.FILES, instance=blog)

        if blogForm.is_valid():
            article = blogForm.save()
            article.save()
                
            return redirect('/ican/blogs/')
        print blogForm.errors
    return render(request, 'admin/create-blog.tmp', locals())



@login_required(login_url='/admin/login/')
@user_passes_test(lambda u: u.is_staff)
def blogs(request, articleType='blogs'):
    articleType = {
        'news' : constants.ARTICLE_NEWS,
        'blogs' : constants.ARTICLE_BLOG
    }[articleType]

    is_news_article = True if articleType == constants.ARTICLE_NEWS else False
    blogs = models.Blog.objects.filter(article_type=articleType)
    paginator = Paginator(blogs, constants.PAG_BLOG_NUMBER)

    page_number = request.GET.get('page', 1)
    current_page = paginator.page(page_number)
    blogs = current_page.object_list

    return render(request, 'admin/admin.bloglist.tmp', locals())

@login_required(login_url='/admin/login/')
@user_passes_test(lambda u : u.is_staff)
def appointments(request, filter=None):
    return render(request, 'event/admin.appointment.list.tmp', locals())

@login_required(login_url='/admin/login/')
@user_passes_test(lambda u : u.is_staff)
def appointmentsjson(request):
    appointments = models.Appointment.objects.all()
    from django.utils import dateparse
    start = dateparse.parse_datetime(request.GET.get('start')).date()
    end = dateparse.parse_datetime(request.GET.get('end')).date()
    
    appointments = appointments.filter(date__range=[start, end])
    import json
    appointments = json.dumps([ {'url' : '/appointments/appointmentID-%d/' %(appointment.pk), 'slot' : appointment.slot.slot, 'user' : "%s %s" %(appointment.user.first_name, appointment.user.last_name), 'userid' : '%d' %(appointment.user.pk), 'backgroundColor' :'#0088cc' if appointment.status=='read' else '#b92222', 'title' : appointment.need.name , 'start' : str(appointment.date), 'end' : str(appointment.date)} for appointment in appointments])
    return HttpResponse(appointments)
    print appointmentFilterForm.errors
    print request.GET
    return HttpResponse("DOne")

@login_required(login_url='/admin/login/')
@user_passes_test(lambda u : u.is_staff)
def appointmentRead(request, appointmentID):
    appointment = get_object_or_404(models.Appointment, pk=appointmentID)
    appointment.status = 'read'
    appointment.save()
    serializer_context = {
        'request': Request(request),
    }
    serializer = serializers.AppointmentSerializer(appointment, context=serializer_context)
    serializer.userID = 12
    data  = JSONRenderer().render(serializer.data)

    return HttpResponse(data)

def settingJob(request):
    return render(request, 'event/jobsettings.tmp') 
def settingEvent(request):
    return render(request, 'event/eventsettings.tmp') 

def settingEmployer(request):
    return render(request, 'event/employersetting.tmp') 