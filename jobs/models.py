# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import constants

# Create your models here.

#supporting models 
class Region(models.Model):
    name = models.CharField(max_length=100)

class JobLevel(models.Model):
    description = models.CharField(max_length=100)

class EmployementType(models.Model):
    name = models.CharField(max_length=50)

class SchoolLevel(models.Model):
    name = models.CharField(max_length=50)

#Main models 
class Category(models.Model):
    name = models.CharField(max_length=100)

class Company(models.Model):
    name = models.CharField(max_length=100)
    brief_description = models.TextField()
    country = models.CharField(choices=constants.COUNTRIES)
    website = models.URLField()
    phone = models.CharField(max_length=25)
    email = models.EmailField()
    joined_at = models.DateTimeField(auto_now_add=True)

class Employee(models.Model):

    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    regiion = models.ForeignKey('Region')
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    intersted_in = models.ManyToManyField('Category')
    school_level = models.ForeignKey('SchoolLevel')
    joined_at = models.DateTimeField(auto_now_add=True)
    applications = models.ManyToManyField('Job', 
                                        related_name='applicants',
                                        through='JobApplication',
                                        through_fields=('applicant', 'job'))

    def jobMatches(self):
        pass

class Job(models.Model):
    title = models.CharField(max_length=100)
    summary = models.TextField()
    requirements = models.TextField()
    level = models.ForeignKey('JobLevel')
    company = models.ForeignKey('Company')
    salary = models.DecimalField(default=0) #0 means not determined 
    position = models.CharField(max_length=100)
    number_of_candidates = models.IntegerField(default=0) #0 means not determined 
    deadline = models.DateTimeField()
    status = models.IntegerField(choices=constants.JOB_STATUS)
    employement_type = models.ForeignKey('EmployementType')
    region = models.ForeignKey('Region')
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Category')

class JobApplication(models.Model):
    applicant = models.ForeignKey('Employee')
    job = models.ForeignKey('Job')
    status = models.CharField(
                                ('Pe', 'Pending'),
                                ('Ac', "Accepted"),
                                ('Re', "Rejected"),
                            )
    applied_on = models.DateTimeField(auto_now_add=True)