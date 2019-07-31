# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from jobs import constants, functions
from django.contrib.auth.models import User
import datetime
from ckeditor.fields import RichTextField

# Create your models here.

#supporting models 
class Region(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering='name',

class JobLevel(models.Model):
    description = models.CharField(max_length=100)

    def __unicode__(self):
        return self.description

class EmployementType(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20, default='#55a747')

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
    profile_pic = models.FileField(upload_to=functions.getFileName, null=True, blank=True)
    brief_description = models.TextField(null=True, blank=True)
    region = models.ForeignKey('Region', null=True, blank=True, related_name='companies')
    city = models.CharField(max_length=100, null=True, blank=True, default="Addis Ababa")
    website = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=25, blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Employers'

    def __unicode__(self):
        return self.name 

class AccessToken(models.Model):
    value = models.CharField(max_length=200, primary_key=True)
    paramFilter = models.CharField(max_length=100)
    paramQuery = models.CharField(max_length=300)
    company = models.ForeignKey('company', related_name='accestokens')

    @staticmethod
    def generateValue():
        import hashlib
        import random
        m = hashlib.md5()
        random_data = []
        for i in range(15):
            random_data.append( str(random.randint(1,1000)) )
        
        random_data = ''.join(random_data)
        m.update(random_data)
        return m.hexdigest()

class Contact(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length = 10, default='unread', choices=(constants.SEEN_UNSEEN_STATUS))
    messaged_on = models.DateTimeField(auto_now_add=True)
    
    @classmethod
    def todays(cls):
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        return cls.objects.filter(messaged_on__range=(today_min, today_max))
    
    @classmethod
    def yesterdays(cls):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        yesterday_min = datetime.datetime.combine(yesterday, datetime.time.min)
        yesterday_max = datetime.datetime.combine(yesterday, datetime.time.max)
        return cls.objects.filter(messaged_on__range=(yesterday_min, yesterday_max))
    
    @classmethod
    def last7days(cls):
        last7day = datetime.date.today() - datetime.timedelta(days=7)
        last7day_min = datetime.datetime.combine(last7day, datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        return cls.objects.filter(messaged_on__range=(last7day_min, today_max))

    class Meta:
        ordering = ('-status', '-messaged_on' )

    def __unicode__(self):
        return self.subject

class Message(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    company = models.ForeignKey('Company', related_name='messages')
    sender = models.ForeignKey(User, related_name='messages')
    status = models.CharField(max_length = 10, default='unread', choices=(constants.SEEN_UNSEEN_STATUS))
    messaged_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-status', '-messaged_on' )
    @classmethod
    def todays(cls):
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        return cls.objects.filter(messaged_on__range=(today_min, today_max))
    
    @classmethod
    def yesterdays(cls):
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        yesterday_min = datetime.datetime.combine(yesterday, datetime.time.min)
        yesterday_max = datetime.datetime.combine(yesterday, datetime.time.max)
        return cls.objects.filter(messaged_on__range=(yesterday_min, yesterday_max))
    
    @classmethod
    def last7days(cls):
        last7day = datetime.date.today() - datetime.timedelta(days=7)
        last7day_min = datetime.datetime.combine(last7day, datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        return cls.objects.filter(messaged_on__range=(last7day_min, today_max))


class UserBackGround(models.Model):
    city = models.CharField(max_length=100)
    start_month = models.CharField( max_length=10, choices=constants.MONTHS)
    start_year = models.IntegerField()
    end_month = models.CharField(max_length=10, choices=constants.MONTHS)
    end_year = models.IntegerField()
    description = models.TextField()

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

class JobAlert(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __unicode__(self):
        return self.full_name


class AgeRange(models.Model):
    startAge = models.IntegerField(verbose_name='Start Age')
    endAge = models.CharField(max_length=5, verbose_name='Enda Age')

    def __unicode__(self):
        if self.endAge.isnumeric():
            return "%d - %s" %(self.startAge, self.endAge)
        return "%d%s" %(self.startAge, self.endAge)
    
    class Meta:
        ordering = ('startAge',)

class JobSeekerService(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class EmployerService(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class JobType(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Employee(Entity):
    profile_pic = models.FileField(upload_to=functions.getFileName,  blank=True)
    gender = models.CharField(blank=True, max_length=8, null=True, choices=constants.GENDER_CHOICES)
    age = models.ForeignKey('AgeRange', blank=True, null=True, related_name='employees')
    highest_education_level = models.IntegerField( choices=constants.EDUCATION_LEVELS, null=True, blank=True)
    employement_status = models.IntegerField(choices=constants.EMPLOYEMENT_STATUS, null=True, blank=True)
    job_types = models.ManyToManyField('JobType', related_name='jobseekers', blank=True)
    services_intersted_in = models.ManyToManyField('JobSeekerService', related_name='jobseekers', blank=True)

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
    
    class Meta:
        verbose_name_plural = 'Job Seekers'

    def __unicode__(self):
        return self.user.first_name

    def apply(self, job):
        #check for necessary informatino before applying 
        
        if self.cvs.count() > 0:
            pass
        elif not self.experiences.count() > 0 or not self.educations.count() > 0 or not self.skills.count() > 0: 
            return False

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

class PublishedJobs(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_draft=False)

class Job(models.Model):
    title = models.CharField(max_length=100)
    summary = RichTextField(blank=True)
    requirements =RichTextField(blank=True)
    knowledge_skills =RichTextField(blank=True)
    education_experience =RichTextField(blank=True)
    how_to_apply =RichTextField(blank=True)
    responsibilities =RichTextField(blank=True)
    department = models.CharField(blank=True, max_length=100)
    level = models.ForeignKey('JobLevel', null=True, blank=True)
    company = models.ForeignKey('Company', related_name='jobs')
    salary = models.CharField(max_length=200, blank=True, null=True) #0 means not determined 
    number_of_candidates = models.IntegerField(blank=True, null=True) #0 means not determined 
    deadline = models.DateField(blank=True, null=True)
    status = models.IntegerField(choices=constants.JOB_STATUS, default=constants.JOB_STATUS_OPEN)
    employement_type = models.ForeignKey('EmployementType', blank=True, null=True)
    report_to = models.CharField(blank=True, max_length=100)
    region = models.ForeignKey('Region', null=True, blank=True, related_name='jobs')
    city = models.CharField(max_length=100, default="Addis Ababa")
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Category', blank=True, related_name='jobs')
    views = models.IntegerField(default=0, blank=True)
    apply_through_portal = models.BooleanField(default=True)
    application_link = models.URLField(blank=True, null=True)
    is_draft = models.BooleanField(default=False)


    class Meta:
        ordering = ('-created_at', )
   
    def getuniquelink(self):
        return '-'.join(self.title.replace('/', '').replace('.', '').replace('(', '').replace(')', '').replace('!', '').replace('>', '').replace('<', '').replace('?', '').replace(':', '').replace('$', '').replace('+', '').replace('-', '').replace('\\','').replace('=','').replace('*','').lower().split(" ")) + '-' + str(self.pk)
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


class CV(models.Model):
    name = models.CharField(max_length=200)
    document = models.FileField(upload_to=functions.getFileName)
    employee = models.ForeignKey('Employee', related_name='cvs')

class References(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.EmailField()
    employee = models.ForeignKey('Employee', related_name='references')



class Association(models.Model):
    name = models.CharField(max_length=200)
    employee = models.ForeignKey('Employee', related_name='associations')

class WorkSample(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    document = models.FileField(upload_to=functions.getFileName)
    employee = models.ForeignKey('Employee', related_name='worksamples')

class WorkLink(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField()
    employee = models.ForeignKey('Employee', related_name='worklinks')



class VisitCount(models.Model):

    uniqueHitCount = models.IntegerField()
    totalHitCount = models.IntegerField()
    visitDate = models.DateField(auto_now_add=True)