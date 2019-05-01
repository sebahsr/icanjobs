# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from jobs import constants
import datetime
from jobs import models as jobModels
from ckeditor_uploader.fields import  RichTextUploadingField

# Create your models here.
"""
    Event TItle { must }
    Event Description { must }
    Event tags { must }
    Date and Time { must}
    Event image optional
    Location
    Address line 1 (must)
    City (must)
    Region (must)
    Latitude (optional)
    Longitude (optional)

"""
from jobs import functions
from jobs import models as job_models

class EventTag(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        ordering = ('name', )
    
    def __unicode__(self):
        return self.name

class PostCategories(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = RichTextUploadingField()
    event_start_date = models.DateField()
    event_end_date = models.DateField()
    start_time = models.CharField(max_length=10)
    end_time = models.CharField(max_length=10)
    image = models.FileField(upload_to=functions.getFileName, null=True, blank=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    region = models.ForeignKey(job_models.Region)
    latitude = models.CharField(max_length=10, null=True, blank=True)
    longitude = models.CharField(max_length=10, null=True, blank=True)
    tags = models.ManyToManyField('EventTag', blank=True, related_name='events')

    class Meta:
        ordering = ('event_start_date', )

class Blog(models.Model):
    title = models.CharField(max_length=150)
    content = RichTextUploadingField()
    categories = models.ManyToManyField('PostCategories', related_name='blogs')
    image = models.FileField(upload_to=functions.getFileName)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('created_at',)

class AppointmentNeed(models.Model):
    name = models.CharField(max_length=150)
    def __unicode__(self):
        return self.name 
class AppointmentSlot(models.Model):
    slot = models.CharField(max_length=150)

    def __unicode__(self):
        return self.slot

class Appointment(models.Model):
    user = models.ForeignKey(jobModels.Employee, related_name="appointments")
    need = models.ForeignKey('AppointmentNeed', related_name='appointments')
    slot = models.ForeignKey("AppointmentSlot", related_name='appointments')
    date = models.DateField()
    status = models.CharField(max_length = 10, default='unread', choices=(constants.SEEN_UNSEEN_STATUS))
    created_on = models.DateTimeField(auto_now_add=True)

    @classmethod
    def todays(cls):
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        return cls.objects.filter(created_on__range=(today_min, today_max))
    
    @classmethod
    def yesterdays(cls):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        yesterday_min = datetime.datetime.combine(yesterday, datetime.time.min)
        yesterday_max = datetime.datetime.combine(yesterday, datetime.time.max)
        return cls.objects.filter(created_on__range=(yesterday_min, yesterday_max))
    
    @classmethod
    def last7days(cls):
        last7day = datetime.date.today() - datetime.timedelta(days=7)
        last7day_min = datetime.datetime.combine(last7day, datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        return cls.objects.filter(created_on__range=(last7day_min, today_max))

