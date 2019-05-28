# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from event import models
# Register your models here.

class EventTagModelAdmin(admin.ModelAdmin):
    list_filters = ('name', )

class BlogModelAdmin(admin.ModelAdmin):
    list_display = ('title', )

admin.site.register(models.EventTag, EventTagModelAdmin)
admin.site.register(models.PostCategories)
admin.site.register(models.AppointmentNeed)
admin.site.register(models.AppointmentSlot)
admin.site.register(models.MenuLinks)