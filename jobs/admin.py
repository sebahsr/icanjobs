# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from jobs import models 
from django.contrib.auth.models import User
# Register your models here.

class CategoryModelAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ('name',)


class JobModelAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ('title', 'region', 'company')
    exclude = ('views',)

class CompanyModelAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ('name', 'region', 'city')
class RegionModelAdmin(admin.ModelAdmin):
    list_display = ('name', )
class EmployementTypeModelAdmin(admin.ModelAdmin):
    list_display = ('name', )

class JobLevelModelAdmin(admin.ModelAdmin):
    list_display = ('description', )

class SchoolLevelModelAdmin(admin.ModelAdmin):
    list_display = ('name', )

class EmployeeModelAdmin(admin.ModelAdmin):
    list_display = ("full_name_view", "username_view")

    def full_name_view(self, employee):
        return "%s %s" %(employee.user.first_name, employee.user.last_name)
    
    def username_view(self, employee):
        return "%s" % (employee.user.username)
class EmployeeJobInterestModelAdmin(admin.ModelAdmin):
    list_display = ("employee", 'job_category', 'job_region', 'employement_type')
    
  
class DegreeModelAdmin(admin.ModelAdmin):
    list_display = ('name', )

admin.site.register(models.Category, CategoryModelAdmin)
admin.site.register(models.Job, JobModelAdmin)
admin.site.register(models.Company, CompanyModelAdmin)
admin.site.register(models.Region, RegionModelAdmin)
admin.site.register(models.EmployementType, EmployementTypeModelAdmin)
admin.site.register(models.JobLevel, JobLevelModelAdmin)
admin.site.register(models.SchoolLevel, SchoolLevelModelAdmin)
admin.site.register(models.Employee, EmployeeModelAdmin)
#admin.site.register(models.Blog, BlogModelAdmin)
admin.site.register(models.EmployeeJobInterest, EmployeeJobInterestModelAdmin)
admin.site.register(models.Degree, DegreeModelAdmin)
admin.site.register(models.AgeRange)
admin.site.register(models.JobSeekerService)
admin.site.register(models.EmployerService)
admin.site.register(models.JobType)



