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
        exclude = ('id', 'views', 'company', 'status')
        widgets = {
            'title' : forms.TextInput(attrs={
                "placeholder" : "Job Title", "class" : "form-control"}),
            
            'summary' : forms.Textarea(attrs={
                "placeholder" : "Job Overview","class" : "form-control"}),
            
            'requirements' : forms.Textarea(attrs={
                "placeholder" : "Key Requirements","class" : "form-control"}),

            'education_experience' : forms.Textarea(attrs={
                "placeholder" : "Educations and Experiences","class" : "form-control"}),

            'deadline' : forms.TextInput(attrs={
                "placeholder" : "Deadline Date",
                "class" : "form-control",
                "data-plugin-datepicker" : True}),
                
            'apply_through_portal' : forms.CheckboxInput(attrs={
                "class" : "form-control"
            }),

            'level' : forms.Select(attrs={
                "placeholder" : "Job Level",
                "class" : "form-control", 
                "data-plugin-multiselect" : True}),
            
            'department' : forms.TextInput(attrs={
                "placeholder" : "Department",
                "class" : "form-control"}),
            
            'report_to' : forms.TextInput(attrs={
                "placeholder" : "Report to",
                "class" : "form-control"}),
            

            'salary' : forms.NumberInput(attrs={
                "placeholder" : "Salary","class" : "form-control"}),

            'position' : forms.TextInput(attrs={
                "placeholder" : "Job Position","class" : "form-control"}),
            
            'number_of_candidates' : forms.TextInput(attrs={
                "placeholder" : "Number of Candidates","class" : "form-control"}),

            'employement_type' : forms.Select(attrs={
                "class" : "form-control", 
                "data-plugin-multiselect" : True}),
            'region' : forms.Select(attrs={
                "class" : "form-control", 
                "data-plugin-multiselect" : True}),

            'categories' : forms.SelectMultiple(attrs={
                "class" : "form-control", 
                "data-plugin-multiselect" : True}),

            'city' : forms.TextInput(attrs={
                "placeholder" : "City","class" : "form-control"}),

            'summary' : forms.Textarea(attrs={
                "placeholder" : "Summary" , "class" : "form-control"
            }),
            'requirements' : forms.Textarea(attrs={
                "placeholder" : "Requirements" , "class" : "form-control"
            }),
            'responsibilities' : forms.Textarea(attrs={
                "placeholder" : "Responsibilities" , "class" : "form-control"
            }),
            'how_to_apply' : forms.Textarea(attrs={
                "placeholder" : "How to Apply" , "class" : "form-control"
            }),

            'knowledge_skills' : forms.Textarea(attrs={
                "placeholder" : "Knowledge and Skills" , "class" : "form-control"
            })
            
            

        }

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields=('first_name', 'last_name', 'email')
        widgets = {
            'email' : forms.TextInput(attrs={
                "placeholder" : "Email address","class" : "form-control"}),
            
            'first_name' : forms.TextInput(attrs={
                "placeholder" : "First Name","class" : "form-control"}),
            
            'last_name' : forms.TextInput(attrs={
                "placeholder" : "Last Name","class" : "form-control"}),
            
            'username' : forms.TextInput(attrs={
                "placeholder" : "Username","class" : "form-control"}),
            

        }

class UserNameForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields=('username', )
        widgets = {
            'username' : forms.TextInput(attrs={
                "placeholder" : "Username","class" : "form-control"}),    
        }

class CompanyForm(forms.ModelForm):
    class Meta:
        model = models.Company
        exclude = ('id', 'user')
        widgets = {
            'brief_description' : forms.Textarea(attrs={
                "placeholder" : "Brief Description About the comapny",
                'class' : "form-control"}),

            'city' : forms.TextInput(attrs={
                "placeholder" : "City",
                "class" : "form-control"}),
            
            'name' : forms.TextInput(attrs={
                "placeholder" : "Company Name",
                "class" : "form-control"}),
            
            'phone' : forms.TextInput(attrs={
                'data-plugin-masked-input' : True,
                'data-input-mask':"(999) 999-9999",
                'placeholder' : "(123) 123-1234",
                "class" : "form-control"}),
            
            'facebook' : forms.TextInput(attrs={
                "placeholder" : "Facebook Address",
                "class" : "form-control"}),
            
            'twitter' : forms.TextInput(attrs={
                "placeholder" : "Twitter Address",
                "class" : "form-control"}),
            
            'linkedin' : forms.TextInput(attrs={
                "placeholder" : "Linkedin Address",
                "class" : "form-control"}),

            'region' : forms.Select(attrs={
                "placeholder" : "Job Level",
                "class" : "form-control", 
                "data-plugin-multiselect" : True}),

            'website' : forms.TextInput(attrs={
                "placeholder" : "Website",
                "class" : "form-control"})
            
        }




class EmployeeForm(forms.ModelForm):
    class Meta:
        model = models.Employee
        exclude = ('id','applications', 'joined_at', 'user') 
        widgets = {
            'about_me' : forms.Textarea(attrs={
                "placeholder" : "About Me","onfocus" : "this.placeholder = ''",  
                "onblur" : "this.placeholder = 'About Me'" ,'class' : "single-textarea"}),

            'city' : forms.TextInput(attrs={
                "placeholder" : "City","onfocus" : "this.placeholder = ''",  "onblur" : "this.placeholder = 'City'" ,
                "class" : "single-input"}),
            
            'phone' : forms.TextInput(attrs={
                "placeholder" : "Phone","onfocus" : "this.placeholder = ''",  "onblur" : "this.placeholder = 'Phone'" ,
                "class" : "single-input"}),
            'region' : forms.Select(),
            
        }

class EmployeeJobInterestForm(forms.ModelForm):
    class Meta:
        model = models.EmployeeJobInterest
        exclude = ('id', 'employee' )
        widgets = {
            'salary_start' : forms.TextInput(attrs={
                "placeholder" : "Salary Start","onfocus" : "this.placeholder = ''",  "onblur" : "this.placeholder = 'Salary Start'" ,"class" : "single-input"}),
            
            'salary_end' : forms.TextInput(attrs={
                "placeholder" : "Salry End","onfocus" : "this.placeholder = ''",  
                "onblur" : "this.placeholder = 'Salary End'" ,"class" : "single-input"}),
            
            'pay_period' : forms.Select(),
            'job_level' : forms.Select(),
            'job_category' : forms.Select(),
            'job_region' : forms.Select(),
            'employement_type' : forms.Select()
            
        }
class UserBackgroundForm(forms.ModelForm):
    class Meta:
        widgets = {}
    

class ExperienceForm(UserBackgroundForm):
    class Meta:
        model = models.Experience
        exclude = ('id', 'employee')
        widgets = {
            'city' : forms.TextInput(attrs={
                "placeholder" : "City","onfocus" : "this.placeholder = ''",  
                "onblur" : "this.placeholder = 'City'" ,"class" : "single-input"}),
            'region' : forms.Select(),
            'start_year' : forms.TextInput(attrs={
                "placeholder" : "Start Year","onfocus" : "this.placeholder = ''",  
                "onblur" : "this.placeholder = 'Start Year'" ,"class" : "single-input"}),

            'start_month' : forms.Select(attrs={
                "placeholder" : "Start Month","onfocus" : "this.placeholder = ''",  
                "onblur" : "this.placeholder = 'Start Month'" ,"class" : "single-input"}),

            'end_month' : forms.Select(attrs={
                "placeholder" : "End Month","onfocus" : "this.placeholder = ''",  
                "onblur" : "this.placeholder = 'End Month'" ,"class" : "single-input"}),

            'end_year' : forms.TextInput(attrs={
                "placeholder" : "End Year","onfocus" : "this.placeholder = ''",  
                "onblur" : "this.placeholder = 'End Year'" ,"class" : "single-input"}),

            'description' : forms.Textarea(attrs={
                "placeholder" : "Description","onfocus" : "this.placeholder = ''",  
                "onblur" : "this.placeholder = 'Description'" ,'class' : "single-textarea"}),

            'is_currently' : forms.CheckboxInput(attrs={}),
            'job_title' : forms.TextInput(
                attrs={
                    "placeholder" : "Job Title","onfocus" : "this.placeholder = ''",  
                    "onblur" : "this.placeholder = 'Job Title'" ,"class" : "single-input"}),

            'company_name' : forms.TextInput(
                attrs={
                    "placeholder" : "Company Name","onfocus" : "this.placeholder = ''",  
                    "onblur" : "this.placeholder = 'Company Name'" ,"class" : "single-input"})
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = models.Skill
        exclude = ('id', 'employee')
        widgets = {
            'name' : forms.TextInput(attrs={
                "placeholder" : "Area of Expertise ","onfocus" : "this.placeholder = ''",  
                "onblur" : "this.placeholder = 'Area of Expertise'" ,"class" : "single-input"}),
        }

class WebisteInfoForm(forms.ModelForm):
    class Meta:
        model = models.WebsiteInfo
        exclude = ( 'employee', )
        widgets = {
            'adress' : forms.TextInput(attrs={
                "placeholder" : "http://yourwebsite.com ","onfocus" : "this.placeholder = ''",  
                "onblur" : "this.placeholder = 'http://yourwebsite.com'" ,"class" : "single-input"}),
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = models.Education
        exclude = ('id', 'employee')
        widgets = {
            'city' : forms.TextInput(attrs={
                "placeholder" : "City","onfocus" : "this.placeholder = ''",  
                "onblur" : "this.placeholder = 'City'" ,"class" : "single-input"}),
            'region' : forms.Select(),
            'start_year' : forms.TextInput(attrs={
                "placeholder" : "Start Year","onfocus" : "this.placeholder = ''",  
                "onblur" : "this.placeholder = 'Start Year'" ,"class" : "single-input"}),

            'start_month' : forms.Select(attrs={
                "placeholder" : "Start Month","onfocus" : "this.placeholder = ''",  
                "onblur" : "this.placeholder = 'Start Month'" ,"class" : "single-input"}),

            'end_month' : forms.Select(attrs={
                "placeholder" : "End Month","onfocus" : "this.placeholder = ''",  
                "onblur" : "this.placeholder = 'End Month'" ,"class" : "single-input"}),

            'end_year' : forms.TextInput(attrs={
                "placeholder" : "End Year","onfocus" : "this.placeholder = ''",  
                "onblur" : "this.placeholder = 'End Year'" ,"class" : "single-input"}),

            'description' : forms.Textarea(attrs={
                "placeholder" : "Description","onfocus" : "this.placeholder = ''",  
                "onblur" : "this.placeholder = 'Description'" ,'class' : "single-textarea"}),

            'is_currently' : forms.CheckboxInput(attrs={}),

            'school' : forms.TextInput(
                attrs={
                    "placeholder" : "School","onfocus" : "this.placeholder = ''",  
                    "onblur" : "this.placeholder = 'Salary End'" ,"class" : "single-input"}),

            'field_of_study' : forms.TextInput(
                attrs={
                    "placeholder" : "Field Of Study","onfocus" : "this.placeholder = ''",  
                    "onblur" : "this.placeholder = 'Salary End'" ,"class" : "single-input"}),
            
            'degree' : forms.Select(attrs={}),

        }

    


