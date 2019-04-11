# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required,user_passes_test

from django.shortcuts import render, get_object_or_404, redirect
from event import forms, models
from jobs import models as jobModels
from jobs import constants
from django.core.paginator import Paginator


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
            blogForm.save()
            return redirect('/ican/blogs/')
        print blogForm.errors
    return render(request, 'admin/create-blog.tmp', locals())

@login_required(login_url='/admin/login/')
@user_passes_test(lambda u: u.is_staff)
def blogs(request):
    blogs = models.Blog.objects.all()
    paginator = Paginator(blogs, constants.PAG_BLOG_NUMBER)

    page_number = request.GET.get('page', 1)
    current_page = paginator.page(page_number)
    blogs = current_page.object_list

    return render(request, 'admin/admin.bloglist.tmp', locals())

@login_required(login_url='/admin/login/')
@user_passes_test(lambda u : u.is_staff)
def appointments(request, filter=None):
    appointments = models.Appointment.objects.all()
    
    appointment_filter = 'All'
    if filter=='read' or filter=='unread':
        appointments = appointments.filter(status=filter)
        appointment_filter = filter.capitalize()
    elif filter=='today':
        appointments = models.Appointment.todays()
        appointment_filter = 'Today\'s'
    elif filter=='yesterday':
        appointments = models.Appointment.yesterdays()
        appointment_filter = "Yesterday's"
    elif filter=='last7':
        appointments = models.Appointment.last7days()
        appointment_filter = "Last Seven days"
    

    return render(request, 'event/admin.appointment.list.tmp', locals())

@login_required(login_url='/admin/login/')
@user_passes_test(lambda u : u.is_staff)
def appointmentRead(request, appointmentID):
    application = get_object_or_404(models.Appointment, pk=appointmentID)
    application.status = 'read'
    application.save()

    return redirect(request.GET.get('redirect_to', '/ican/admin/'))