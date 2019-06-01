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
    
    url(r'^$', job_views.homeView),
    url(r'^about/$', job_views.aboutUs),
    url(r'^branding/$', job_views.branding),
    url(r'^services/$', job_views.services),
    url(r'^jobalerts/$', job_views.jobAlerts),
    url(r'^contact/$', job_views.contact),
    url(r'^privacy/$', job_views.privacy),

    url(r'^jobs/(?:job-(?P<jobID>([a-zA-Z\-\d])+)/)?$', job_views.jobView),
    url(r'^jobs/(?:category-(?P<categoryID>\d+)/)$', job_views.jobView),
    url(r'^jobs/(?:region-(?P<regionID>\d+)/)$', job_views.jobView),
    url(r'^jobs/(?:(?P<search>search)/)$', job_views.jobView),

    url(r'^companies/$', job_views.companyListView),
    url(r'^companies/(?:region-(?P<regionID>\d+)/)$', job_views.companyListView),
    url(r'^company/create-job/$', job_views.companyCreateJobView),
    url(r'^(companies|company)/(?:company-(?P<companyID>\d+)/)?$', job_views.companyView),
    url(r'^company/$', job_views.companyDetailView),
    url(r'^companies/(?:company-(?P<companyID>\d+)/jobstatus-(?P<jobStatus>\d+)/)?$', job_views.companyView),
    url(r'^companies/(?:company-(?P<companyID>\d+)/jobemptype-(?P<jobEmpType>\d+)/)?$', job_views.companyView),
    url(r'^companies/(?:company-(?P<companyID>\d+)/category-(?P<categoryID>\d+)/)?$', job_views.companyView),

    url(r'^signup/$',job_views.employeeSignupView),
    url(r'^login/$', job_views.employeeLoginView),
    url(r'^logout/$', job_views.logoutView),
    url(r'^employee/$',job_views.employeeView),
    url(r'^employee/(?:employee-(?P<employeeID>\d+))/$',job_views.employeeOtherView),
    url(r'employee/matched-jobs/$', job_views.employeeMatchedJobView),
    url(r'employee/applied-jobs/$', job_views.employeeAppliedJobs),
    url(r'employee/build-resume/$', job_views.buildResume),


    url(r'employee/build-resume/(?P<section>(skill|experience|general|education|website|cv|reference|worklink|worksample|association|summary|volunteer))/$', job_views.buildResume),
    url(r'^jobs/applly/job-(?P<jobID>\d+)?/$', job_views.employeeJobApply),

    url(r'^blogs/(?:category-(?P<categoryID>\d+)/)?$', job_views.blogListView),
    url(r'^blogs/blog-(?P<blogID>\d+)/$', job_views.blogDetailView),
    url(r'^test/$', job_views.testView),

    url(r'^company/admin/$', job_views.adminCompanyView),
    url(r'^company/admin/edit/$', job_views.adminCompanyView),
    url(r'^company/edit/username/$', job_views.adminCompanyEditUsernameView),
    url(r'^company/edit/password/$', job_views.adminCompanyChangePasswordView),
    url(r'^company/admin/jobs/$', job_views.companyJobListView),
    url(r'^company/admin/applications/$', job_views.applications),
    url(r'^company/admin/applications/(?P<filter>(read|unread|today|yesterday|last7))/$', job_views.applications),

    url(r'^company/admin/login/$', job_views.loginCompanyView),
    url(r'^company/admin/signup/$', job_views.signUpCompanyView),
    url(r'^company/admin/create-job/(?:job-(?P<jobID>\d+)/)?$', job_views.createJobView),
    url(r'^company/admin/confirm-delete/job-(?P<jobID>\d+)/((?P<confirmed>confirmed)/)?$', job_views.jobDelete),
    url(r'^ican/blog/confirm-delete/blog-(?P<blogID>\d+)/((?P<confirmed>confirmed)/)?$', job_views.blogDelete),

    url(r'^applications/applicationID-(?P<applicationID>\d+)/$', job_views.applicationRead),
    
    url(r'^events/(?:tag-(?P<tagID>\d+)/)?', job_views.events),
    url(r'^event/(?:event-(?P<eventID>\d+))/$', job_views.eventDetail),
    url(r'^appointmnet/make/$', job_views.makeAppointment),
    url(r'^appointmnets/$', job_views.appointments)

]
