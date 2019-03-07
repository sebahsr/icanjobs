"""ican URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import views as job_views

urlpatterns = [
    url(r'^jobs/(?:job-(?P<jobID>\d+)/)?$', job_views.jobView),
    url(r'^jobs/(?:category-(?P<categoryID>\d+)/)$', job_views.jobView),
    url(r'^jobs/(?:region-(?P<regionID>\d+)/)$', job_views.jobView),
    url(r'^jobs/(?:(?P<search>search)/)$', job_views.jobView),

    url(r'^companies/(?:company-(?P<companyID>\d+)/)?$', job_views.companyView),
    url(r'^companies/(?:company-(?P<companyID>\d+)/jobstatus-(?P<jobStatus>\d+)/)?$', job_views.companyView),
    url(r'^companies/(?:company-(?P<companyID>\d+)/jobemptype-(?P<jobEmpType>\d+)/)?$', job_views.companyView),
    url(r'^companies/(?:company-(?P<companyID>\d+)/category-(?P<categoryID>\d+)/)?$', job_views.companyView),

    url(r'^test/$', job_views.testView),
]
