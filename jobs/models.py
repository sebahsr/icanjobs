# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from jobs import constants, functions
from django.contrib.auth.models import User
import datetime

# Create your models here.

#supporting models 
class Region(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class JobLevel(models.Model):
    description = models.CharField(max_length=100)

    def __unicode__(self):
        return self.description

class EmployementType(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Degree(models.Model):

    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name 
    
class SchoolLevel(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name 

#Main models 
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name 
    
    class Meta:
        verbose_name_plural = 'Sectors'
        verbose_name = 'Sector'

class Entity(models.Model):
    user =  models.OneToOneField(User, on_delete=models.CASCADE)
    class Meta:
        abstract = True
    
    
class Company(Entity):
    name = models.CharField(max_length=100)
    profile_pic = models.FileField(upload_to=functions.getFileName)
    brief_description = models.TextField(null=True, blank=True)
    region = models.ForeignKey('Region', related_name='companies')
    city = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=25)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Companies'

    def __unicode__(self):
        return self.name 

class UserBackGround(models.Model):
    city = models.CharField(max_length=100)
    start_month = models.CharField( max_length=10, choices=constants.MONTHS)
    start_year = models.IntegerField()
    end_month = models.CharField(max_length=10, choices=constants.MONTHS)
    end_year = models.IntegerField()
    description = models.TextField()
    is_currently = models.BooleanField(default=False)

    class Meta:
        abstract = True
    
class Experience(UserBackGround):
    job_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    employee = models.ForeignKey('Employee', related_name='experiences')
    region = models.ForeignKey('Region')

class Education(UserBackGround):
    school = models.CharField(max_length=100)
    degree = models.ForeignKey('Degree')
    field_of_study = models.CharField(max_length=100)
    employee = models.ForeignKey('Employee', related_name='educations')
    region = models.ForeignKey('Region')

class Skill(models.Model):
    name = models.CharField(max_length=100)
    employee = models.ForeignKey('Employee', related_name='skills') 

class WebsiteInfo(models.Model):
    adress = models.URLField()
    employee = models.ForeignKey('Employee', related_name='websites')

class Employee(Entity):
    profile_pic = models.FileField(upload_to=functions.getFileName, blank=True)

    #location information 
    city = models.CharField(max_length=100, null=True, blank=True)
    region = models.ForeignKey('Region', blank=True, null=True)
    
    about_me = models.TextField(blank=True)
    volunteer_experience = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    facebook_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)

    applications = models.ManyToManyField('Job', 
                                        blank=True,
                                        related_name='applicants',
                                        through='JobApplication',
                                        through_fields=('applicant', 'job'))
    
    def __unicode__(self):
        return self.user.first_name

    def apply(self, job):
        if not self.applications.filter(pk = job.pk):
            application = JobApplication.objects.create(applicant=self, job=job)
            return application
        return False


    @property
    def first_name(self):
        return self.user.first_name 
    
    @property
    def last_name(self):
        return self.user.last_name 

    def jobMatches(self):
        pass
class EmployeeJobInterest(models.Model):
    job_level = models.ForeignKey('JobLevel', blank=True, null=True)
    job_category = models.ForeignKey( 'Category', blank=True, null=True)
    job_region = models.ForeignKey('Region', blank=True, null=True)
    employement_type = models.ForeignKey( 'EmployementType', blank=True, null=True)
    salary_start = models.IntegerField(blank=True, null=True)
    salary_end = models.IntegerField(blank=True, null=True)
    pay_period = models.CharField(max_length = 10, blank=True, null=True, choices=constants.PAY_PERIOD)
    employee = models.OneToOneField(Employee, related_name='preference')


class Job(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    knowledge_skills = models.TextField(blank=True)
    education_experience = models.TextField(blank=True)
    how_to_apply = models.TextField(blank=True)
    responsibilities = models.TextField(blank=True)
    department = models.CharField(blank=True, max_length=100)

    level = models.ForeignKey('JobLevel')
    company = models.ForeignKey('Company', related_name='jobs')
    salary = models.FloatField(blank=True, null=True) #0 means not determined 
    position = models.CharField(max_length=100, null=True, blank=True)
    number_of_candidates = models.IntegerField(blank=True, null=True) #0 means not determined 
    deadline = models.DateField(blank=True, null=True)
    status = models.IntegerField(choices=constants.JOB_STATUS, default=constants.JOB_STATUS_OPEN)
    employement_type = models.ForeignKey('EmployementType', blank=True, null=True)
    report_to = models.CharField(blank=True, max_length=100)
    region = models.ForeignKey('Region', related_name='jobs')
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Category', blank=True, related_name='jobs')
    views = models.IntegerField(default=0, blank=True)
    apply_through_portal = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created_at', )
   

class JobApplication(models.Model):
    applicant = models.ForeignKey('Employee')
    job = models.ForeignKey('Job', related_name='applications')
    status = models.CharField(max_length = 10, default='unread', choices=(constants.SEEN_UNSEEN_STATUS))
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-status', '-applied_on')
    
    @classmethod
    def todays(cls, jobs):
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        return cls.objects.filter(applied_on__range=(today_min, today_max), job__in=jobs)
    
    @classmethod
    def yesterdays(cls, jobs):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        yesterday_min = datetime.datetime.combine(yesterday, datetime.time.min)
        yesterday_max = datetime.datetime.combine(yesterday, datetime.time.max)
        return cls.objects.filter(applied_on__range=(yesterday_min, yesterday_max), job__in=jobs)
    
    @classmethod
    def last7days(cls, jobs):
        last7day = datetime.date.today() - datetime.timedelta(days=7)
        last7day_min = datetime.datetime.combine(last7day, datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        return cls.objects.filter(applied_on__range=(last7day_min, today_max), job__in=jobs)

