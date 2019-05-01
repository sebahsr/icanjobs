from django import forms
from event import models 
from django.contrib.auth.models import User 
from ckeditor_uploader.widgets import  CKEditorUploadingWidget

class EventForm(forms.ModelForm):
    description = forms.CharField(
        widget=CKEditorUploadingWidget()
    )

    class Meta:
        model = models.Event
        fields='__all__'
        widgets = {
            'title' : forms.TextInput(attrs={
                "placeholder" : "Event Title", "class" : "form-control"}),
                        
            'event_start_date' : forms.TextInput(attrs={
                "placeholder" : "Event Start Date",
                "class" : "form-control",
                "data-plugin-datepicker" : True}),
            
            'start_time' : forms.TextInput(attrs={
                "placeholder" : "Event Start Time",
                "class" : "form-control",
                "data-plugin-timepicker" : True}),
            
            'end_time' : forms.TextInput(attrs={
                "placeholder" : "Event End Time",
                "class" : "form-control",
                "data-plugin-timepicker" : True
            }),

            'event_end_date' : forms.TextInput(attrs={
                "placeholder" : "Event Start Date",
                "class" : "form-control",
                "data-plugin-datepicker" : True}),

           
            'region' : forms.Select(attrs={
                "placeholder" : "Region",
                "class" : "form-control", 
                "data-plugin-multiselect" : True}),
            
            'address' : forms.TextInput(attrs={
                "placeholder" : "Address line",
                "class" : "form-control"}),
            
            'city' : forms.TextInput(attrs={
                "placeholder" : "City",
                "class" : "form-control"}),
            

            'latitude' : forms.TextInput(attrs={
                "placeholder" : "Latitude","class" : "form-control"}),
            
            'longitude' : forms.TextInput(attrs={
                "placeholder" : "Longitude","class" : "form-control"}),
            
            'tags' : forms.SelectMultiple(attrs={
                "class" : "form-control", 
                "data-plugin-multiselect" : True}),

        }

class BlogForm(forms.ModelForm):
    content = forms.CharField(
        widget=CKEditorUploadingWidget()
    )
    class Meta:
        model = models.Blog
        fields = '__all__'
        widgets = {
            'title' : forms.TextInput(attrs={
                "placeholder" : "Blog Title", "class" : "form-control"}),


            'categories' : forms.SelectMultiple(attrs={
                "class" : "form-control", 
                "data-plugin-multiselect" : True}),
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = models.Appointment
        exclude = ('user','status')
        widgets = {
               'slot' : forms.Select(attrs={
                "placeholder" : "Region",
                "class" : "form-control"}),

                'date' : forms.DateInput(attrs={
                    "placeholder" : "Appointment Date",
                    "class" : "appointment-date single-input"
                }),

               'need' : forms.Select(attrs={
                "placeholder" : "Region",
                "class" : "form-control"}),
        }


class AppointmentFilterForm(forms.Form):
    start = forms.DateTimeField()
    end = forms.DateTimeField()
