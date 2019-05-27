"""ican URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import views as event_views

urlpatterns = [
    
    url(r'^ican/admin/$', event_views.dashboard),
    url(r'^ican/event/(?:event-(?P<eventID>\d+)/)?$', event_views.createEvent),
    url(r'^ican/events/$', event_views.events),

    url(r'^ican/blog/(?:blog-(?P<blogID>\d+)/)?$', event_views.createBlog),
    url(r'^ican/blogs/$', event_views.blogs),
    url(r'^ican/appointmnets/$', event_views.appointments),
    url(r'^ican/appointmnets/(?P<filter>(read|unread|today|yesterday|last7))/$', event_views.appointments),
    url(r'^ican/appointmnets/json/$', event_views.appointmentsjson),
    
    url(r'^appointments/appointmentID-(?P<appointmentID>\d+)/$', event_views.appointmentRead, name='appointment-detail'),
    url(r'^settings/jobs/$', event_views.settingJob),
    url(r'^settings/events/$', event_views.settingEvent),
    url(r'^settings/employers/$', event_views.settingEmployer),


]