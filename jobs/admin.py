# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from jobs import models 

# Register your models here.

class CategoryModelAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ('name',)

class BlogModelAdmin(admin.ModelAdmin):
    list_display = ('title', )
class JobModelAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ('title', 'region', 'company')
    exclude = ('views',)
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'company':
            kwargs['queryset'] = models.Company.objects.filter(pk = request.user.company.pk)
        
        return super(JobModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

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

admin.site.register(models.Category, CategoryModelAdmin)
admin.site.register(models.Job, JobModelAdmin)
admin.site.register(models.Company, CompanyModelAdmin)
admin.site.register(models.Region, RegionModelAdmin)
admin.site.register(models.EmployementType, EmployementTypeModelAdmin)
admin.site.register(models.JobLevel, JobLevelModelAdmin)
admin.site.register(models.SchoolLevel, SchoolLevelModelAdmin)
admin.site.register(models.Employee, EmployeeModelAdmin)
admin.site.register(models.Blog, BlogModelAdmin)
admin.site.register(models.PostCategories)

