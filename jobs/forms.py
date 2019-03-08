from django import forms
from jobs import models 
from django.contrib.auth.models import User 

class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        exclude=('id',)
class JobForm(forms.ModelForm):
    class Meta:
        model = models.Job
        exclude = ('id', )

class UserForm(forms.ModelForm):
    first_name = forms.CharField(widget = forms.TextInput(attrs={
                "placeholder" : "First Name","onfocus" : "this.placeholder = ''",  "onblur" : "this.placeholder = 'First Name'" ,"class" : "single-input"}))
    
    last_name = forms.CharField(widget = forms.TextInput(attrs={
                "placeholder" : "Last Name","onfocus" : "this.placeholder = ''",  "onblur" : "this.placeholder = 'Last Name'" ,"class" : "single-input"}))
    
    username = forms.CharField(widget = forms.TextInput(attrs={
                "placeholder" : "username","autocomplete" : "off", "onfocus" : "this.placeholder = ''",  "onblur" : "this.placeholder = 'username'" ,"class" : "single-input"}))
    
    password = forms.CharField(widget = forms.PasswordInput(attrs={
                "placeholder" : "password", "autocomplete" : "off","onfocus" : "this.placeholder = ''",  "onblur" : "this.placeholder = 'password'" ,"class" : "single-input"}))
    

    email = forms.CharField(widget = forms.TextInput(attrs={
                "placeholder" : "Email address","onfocus" : "this.placeholder = ''",  "onblur" : "this.placeholder = 'Email address'" ,"class" : "single-input"}))
    
    class Meta:
        model = User
        exclude = ('id', )

class CompanyForm(forms.ModelForm):
    name = forms.CharField(widget = forms.TextInput(attrs={
                "placeholder" : "Company Name","onfocus" : "this.placeholder = ''",  "onblur" : "this.placeholder = 'Company Name'" ,"class" : "single-input"}))
    
    brief_description = forms.CharField(
        widget = forms.Textarea(attrs={
             "placeholder" : "Brief Description","onfocus" : "this.placeholder = ''",  "onblur" : "this.placeholder = 'Brief Description'" ,"class" : "single-textarea"}))
    city = forms.CharField(widget = forms.TextInput(attrs={
                "placeholder" : "City","onfocus" : "this.placeholder = ''",  "onblur" : "this.placeholder = 'City'" ,"class" : "single-input"}))
    
    region = forms.ModelChoiceField(queryset=models.Region.objects.all(), empty_label=None)
    
    website = forms.CharField(widget = forms.TextInput(attrs={
                "placeholder" : "Website","onfocus" : "this.placeholder = ''",  "onblur" : "this.placeholder = 'Website'" ,"class" : "single-input"}))
    
    phone = forms.CharField(widget = forms.TextInput(attrs={
                "placeholder" : "Phone","onfocus" : "this.placeholder = ''",  "onblur" : "this.placeholder = 'Phone'" ,"class" : "single-input"}))
    

    class Meta:
        model = models.Company
        exclude = ('id', 'user')
class EmployeeForm(forms.ModelForm):
    
    phone = forms.CharField(widget = forms.TextInput(attrs={
                "placeholder" : "Phone Number","onfocus" : "this.placeholder = ''",  "onblur" : "this.placeholder = 'Phone Number'" ,"class" : "single-input"}))
    

    city = forms.CharField(widget = forms.TextInput(attrs={
                "placeholder" : "City","onfocus" : "this.placeholder = ''",  "onblur" : "this.placeholder = 'City'" ,"class" : "single-input"}))
    
    age = forms.CharField(widget = forms.TextInput(attrs={
                "placeholder" : "Age","onfocus" : "this.placeholder = ''",  "onblur" : "this.placeholder = 'Age'" ,"class" : "single-input"}))
    
    region = forms.ModelChoiceField(queryset=models.Region.objects.all(), empty_label=None)
    
    school_level = forms.ModelChoiceField(queryset=models.SchoolLevel.objects.all(), empty_label=None)

    
    class Meta:
        model = models.Employee
        exclude = ('id','applications', 'joined_at', 'user') 
    

