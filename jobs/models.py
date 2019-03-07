# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from jobs import constants, functions

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
    class Meta:
        abstract = True
    
    
class Company(Entity):
    name = models.CharField(max_length=100)
    profile_pic = models.FileField(upload_to=functions.getFileName)
    brief_description = models.TextField()
    country = models.CharField(max_length=10, choices=constants.COUNTRIES)
    website = models.URLField()
    phone = models.CharField(max_length=25)
    email = models.EmailField()
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Companies'

    def __unicode__(self):
        return self.name 

class Employee(Entity):

    full_name = models.CharField(max_length=100)
    profile_pic = models.FileField(upload_to=functions.getFileName)
    age = models.IntegerField()
    regiion = models.ForeignKey('Region')
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    intersted_in = models.ManyToManyField('Category', related_name='interested_employees')
    school_level = models.ForeignKey('SchoolLevel')
    joined_at = models.DateTimeField(auto_now_add=True)
    applications = models.ManyToManyField('Job', 
                                        related_name='applicants',
                                        through='JobApplication',
                                        through_fields=('applicant', 'job'))
    
    def __unicode__(self):
        return self.full_name

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