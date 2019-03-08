# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from jobs import constants, functions
from django.contrib.auth.models import User
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
        verbose_name_plural = 'categories'

class Entity(models.Model):
    user =  models.OneToOneField(User, on_delete=models.CASCADE)
    class Meta:
        abstract = True
    
    
class Company(Entity):
    name = models.CharField(max_length=100)
    profile_pic = models.FileField(upload_to=functions.getFileName)
    brief_description = models.TextField()
    region = models.ForeignKey('Region', related_name='companies')
    city = models.CharField(max_length=100)
    website = models.URLField()
    phone = models.CharField(max_length=25)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Companies'

    def __unicode__(self):
        return self.name 

class Employee(Entity):
    profile_pic = models.FileField(upload_to=functions.getFileName)
    age = models.IntegerField()
    region = models.ForeignKey('Region')
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    intersted_in = models.ManyToManyField('Category', blank=True, null=True, related_name='interested_employees')
    school_level = models.ForeignKey('SchoolLevel')
    joined_at = models.DateTimeField(auto_now_add=True)
    applications = models.ManyToManyField('Job', 
                                        blank=True, null=True,
                                        related_name='applicants',
                                        through='JobApplication',
                                        through_fields=('applicant', 'job'))
    
    def __unicode__(self):
        return self.user.first_name

    def apply(self, job):
        if not self.applications.filter(pk = job.pk):
            application = JobApplication.objects.create(applicant=self, job=job, status='Pe')
            return application
        return False

    def jobMatches(self):
        pass

class Job(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField()
    requirements = models.TextField()
    level = models.ForeignKey('JobLevel')
    company = models.ForeignKey('Company', related_name='jobs')
    salary = models.FloatField(default=0) #0 means not determined 
    position = models.CharField(max_length=100)
    number_of_candidates = models.IntegerField(default=0) #0 means not determined 
    deadline = models.DateTimeField()
    status = models.IntegerField(choices=constants.JOB_STATUS)
    employement_type = models.ForeignKey('EmployementType')
    region = models.ForeignKey('Region', related_name='jobs')
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Category', related_name='jobs')
    views = models.IntegerField(default=0)

   

class JobApplication(models.Model):
    applicant = models.ForeignKey('Employee')
    job = models.ForeignKey('Job', related_name='applications')
    status = models.CharField(max_length = 10, choices= (
                                ('Pe', 'Pending'),
                                ('Ac', "Accepted"),
                                ('Re', "Rejected"),
                            )
    )
    applied_on = models.DateTimeField(auto_now_add=True)

class Blog(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    categories = models.ManyToManyField('PostCategories', related_name='blogs')
    image = models.FileField(upload_to=functions.getFileName)
    created_at = models.DateTimeField(auto_now_add=True)
    
class PostCategories(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name