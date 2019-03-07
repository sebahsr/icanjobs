# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from jobs import models 

# Register your models here.

class CategoryModelAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ('name',)

class JobModelAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ('title', 'region', 'company')

class CompanyModelAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ('name', 'country')
class RegionModelAdmin(admin.ModelAdmin):
    list_display = ('name', )
class EmployementTypeModelAdmin(admin.ModelAdmin):
    list_display = ('name', )

class JobLevelModelAdmin(admin.ModelAdmin):
    list_display = ('description', )

admin.site.register(models.Category, CategoryModelAdmin)
admin.site.register(models.Job, JobModelAdmin)
admin.site.register(models.Company, CompanyModelAdmin)
admin.site.register(models.Region, RegionModelAdmin)
admin.site.register(models.EmployementType, EmployementTypeModelAdmin)
admin.site.register(models.JobLevel, JobLevelModelAdmin)

