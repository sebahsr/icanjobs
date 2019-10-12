from django import forms
from jobs import models, constants
from django.contrib.auth.models import User 
from ckeditor.widgets import CKEditorWidget

class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        exclude=('id',)

class JobSortForm(forms.Form):
    sort_type = forms.ChoiceField(choices=(
        ('posted_date_rec','Posted Date (Recent)'),
        ('posted_date_old','Posted Date (Oldest)'),
        ('deadline_asc','Deadline (Ascending)'),
        ('deadline_desc','Deadline (Descending)'),
    ))
class RecruitFilterForm(forms.Form):
    gender = forms.ChoiceField(choices=constants.GENDER_CHOICES, widget=forms.Select(attrs={ "class" : "form-control"}))
    highest_education_level = forms.ChoiceField(required=False, choices=constants.EDUCATION_LEVELS, widget=forms.Select(attrs={ "class" : "form-control"}))
    employement_status = forms.ChoiceField(required=False, choices=constants.EMPLOYEMENT_STATUS, widget=forms.Select(attrs={ "class" : "form-control"}))
    job_type = forms.ModelChoiceField(required=False, queryset=models.JobType.objects.all(), widget=forms.Select(attrs={ "class" : "form-control"}))
    ageRange = forms.ModelChoiceField(required=False, queryset=models.AgeRange.objects.all(), widget=forms.Select(attrs={ "class" : "form-control"}))
    educationTitle = forms.CharField(required=False, widget=forms.TextInput(attrs={'class' : "form-control", 'placeholder' : 'Education Title'}))
    experience = forms.CharField(required=False, widget=forms.TextInput(attrs={'class' : "form-control", 'placeholder' : 'Experience ( Greater than or equal to)'}))
    class Meta:
        fields = '__all__'
        widgets = {
                'gender' : forms.Select(attrs={ "class" : "form-control"}),
                'highest_education_level' : forms.Select(attrs={ "class" : "form-control"}),
                'employement_status' : forms.Select(attrs={ "class" : "form-control"}),
                'job_type' : forms.Select(attrs={ "class" : "form-control"}),
                'services_intersted_in' : forms.Select(attrs={ "class" : "form-control"}),
                'educationTitle' : forms.TextInput(attrs={'class' : "form-control", 'placeholder' : 'Education Title'}),
                'experience' : forms.TextInput(attrs={'class' : "form-control", 'placeholder' : 'Experience ( Greater than or equal to)'}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = models.Message
        fields = ('content', 'subject')
        widgets = {
            'content' : forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : 'Message should have more than 50 characters', 'rows' : 4, 'style' : "margin-bottom:10px;height: 125px;padding-top:5px"}),
            'subject' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'subject', 'style' : "margin-bottom:10px;padding-top:5px"}),
        }
        
class ContactForm(forms.ModelForm):
    class Meta:
        model = models.Contact
        fields = 'full_name', 'email', 'subject', 'message'
        widgets = {
            'full_name' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Full Name'}),
            'email' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Your Email'}),
            'subject' : forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Subject'}),
            'message' : forms.Textarea(attrs={'class' : 'form-control', 'placeholder' : 'Message'}),
        }
class JobAlertForm(forms.ModelForm):
    class Meta:
        model = models.JobAlert
        fields = '__all__'
        widgets = {
            'full_name' : forms.TextInput(attrs={
                'placeholder' : 'Full Name', 'class' : 'form-control'
            }),

            'email' : forms.TextInput(attrs={
                'placeholder' : 'Your Email Adress', 'class' : 'form-control'
            })
        }

class VisitForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.TextInput(attrs={
                "placeholder" : "Start Date",
                "class" : "form-control",
                'autocomplete' : False,
                "data-plugin-datepicker" : True}))
    end_date = forms.DateField(required=False, widget=forms.TextInput(attrs={
                "placeholder" : "End Date",
                "class" : "form-control",
                  'autocomplete' : False,
                "data-plugin-datepicker" : True}) )

class JobForm(forms.ModelForm):
    summary = forms.CharField(required=False, widget=CKEditorWidget(attrs={'spellcheck' : "true"},  config_name='jobpost'))
    requirements = forms.CharField(required=False, widget=CKEditorWidget(attrs={'spellcheck' : "true"},  config_name='jobpost'))
    education_experience = forms.CharField(required=False, widget=CKEditorWidget( attrs={'spellcheck' : "true"}, config_name='jobpost'))
    responsibilities = forms.CharField(required=False, widget=CKEditorWidget(attrs={'spellcheck' : "true"},  config_name='jobpost'))
    how_to_apply = forms.CharField(required=False, widget=CKEditorWidget(attrs={'spellcheck' : "true"},  config_name='jobpost'))
    knowledge_skills = forms.CharField(required=False, widget=CKEditorWidget(attrs={'spellcheck' : "true"},  config_name='jobpost'))

    class Meta:
        model = models.Job
        exclude = ('id', 'views', 'company', 'status')
        widgets = {
            'title' : forms.TextInput(attrs={
                "placeholder" : "Job Title", "class" : "form-control"}),
            
          

            'deadline' : forms.TextInput(attrs={
                "placeholder" : "Closing On",
                "class" : "form-control",
                "data-date-format" : "yyyy-mm-dd",
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
            

            'salary' : forms.TextInput(attrs={
                "placeholder" : "Salary","class" : "form-control"}),

            'position' : forms.TextInput(attrs={
                "placeholder" : "Job Position","class" : "form-control"}),
            
            'number_of_candidates' : forms.TextInput(attrs={
                "placeholder" : "Number of Positions","class" : "form-control"}),

            'employement_type' : forms.Select(attrs={
                "class" : "form-control", 
                "data-plugin-multiselect" : True}),
            'region' : forms.Select(attrs={
                "class" : "form-control chosen-select-deselect", 
                "data-plugin-multiselect" : True}),

            'categories' : forms.SelectMultiple(attrs={
                "class" : "form-control", 
                "data-plugin-multiselect" : True}),
            
            

            'city' : forms.TextInput(attrs={
                "placeholder" : "Location","class" : "form-control"}),
           
           

            'application_link' : forms.TextInput(attrs={
                "class" : "form-control",
                "placeholder" : "http://example.com"
            }),

            
        }

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields=('first_name', 'last_name', 'email', 'username')
        widgets = {
            'email' : forms.TextInput(attrs={
                "placeholder" : "Email address","class" : " form-control"}),
            
            'first_name' : forms.TextInput(attrs={
                "placeholder" : "First Name","class" : " form-control"}),
            
            'last_name' : forms.TextInput(attrs={
                "placeholder" : "Last Name","class" : " form-control"}),
            
            'username' : forms.TextInput(attrs={
                "placeholder" : "Username","class" : " form-control"}),
            

        }

class UserNameForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields=('username', )
        widgets = {
            'username' : forms.TextInput(attrs={
                "placeholder" : "Username","class" : "single-input form-control"}),    
        }

class PassWordForm(forms.Form):
    oldPassword = forms.CharField(min_length=8, required=True,
            widget = forms.TextInput(attrs={
                'placholder' : "Old Password", 
                'class' : 'form-control'}) )

    newPassword = forms.CharField(min_length=8, required=True,
            widget = forms.TextInput(attrs={
                'placholder' : "New Password", 
                'class' : 'form-control'}) )
    
    conPassword = forms.CharField(min_length=8, required=True,
            widget = forms.TextInput(attrs={
                'placholder' : "Repeat New Password", 
                'class' : 'form-control'}) )

    username = forms.CharField(required=True)
    
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
        except:
            raise forms.ValidationError('Cant find user') 

        return user 

    def clean(self):
        
        cleaned_data = super( PassWordForm, self).clean()
        oldPassword = cleaned_data.get('oldPassword')
        newPassword = cleaned_data.get('newPassword')
        conPassword = cleaned_data.get('conPassword')
        user = cleaned_data.get('username')
        
        if not user.check_password( oldPassword ):
            raise forms.ValidationError("Invalid old password.")
        if not newPassword:
            raise forms.ValidationError("Please provide new password of atleast 8 characters long.")
        if not newPassword == conPassword:
            raise forms.ValidationError("Your new password doesnt match")
        
        
        
        return cleaned_data
    
    def save(self):
        user = self.cleaned_data['username']
        user.set_password( self.cleaned_data.get('newPassword'))
        user.save()
        return user


class CompanyForm(forms.ModelForm):
    class Meta:
        model = models.Company
        exclude = ('id', 'user')
        widgets = {
            'brief_description' : forms.Textarea(attrs={
                "placeholder" : "Brief Description About the comapny",
                'class' : "form-control"}),

            'city' : forms.TextInput(attrs={
                "placeholder" : "Location",
                "class" : "form-control"}),
            
            'name' : forms.TextInput(attrs={
                "placeholder" : "Company Name",
                "class" : "form-control"}),
            
            'phone' : forms.TextInput(attrs={
                'placeholder' : "Phone Number",
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
                "class" : "form-control chosen-select-deselect", 
                "data-plugin-multiselect" : True}),

            'website' : forms.TextInput(attrs={
                "placeholder" : "Website",
                "class" : "form-control"})
            
        }



class EmployeeAboutMeForm(forms.ModelForm):
    class Meta:
        model = models.Employee
        fields = ('about_me', )
        widgets = {
            'about_me' : forms.Textarea(attrs={
                "placeholder" : "About Me" ,'class' : "form-control"}),
         }

class EmployeeVolunteerForm(forms.ModelForm):
    class Meta:
        model = models.Employee
        fields = ('volunteer_experience', )
        widgets = {
            'volunteer_experience' : forms.Textarea(attrs={
                "placeholder" : "Volunteer Experience/Memberships/Affilations" ,'class' : "form-control"}),
         }

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = models.Employee
        exclude = ('id','applications', 'joined_at', 'user', 'about_me', 'volunteer_experience') 
        widgets = {
            'about_me' : forms.Textarea(attrs={
                "placeholder" : "About Me" ,'class' : "form-control"}),
            'volunteer_experience' : forms.Textarea(attrs={
                "placeholder" : "Volunteer Experience/Memberships/Affilations" ,'class' : "form-control"}),

            'city' : forms.TextInput(attrs={
                "placeholder" : "Location" ,
                "class" : "form-control"}),
            
            'phone' : forms.TextInput(attrs={
                "placeholder" : "Phone" ,
                "class" : "form-control"}),

            'facebook_url' : forms.TextInput(attrs={
                "placeholder" : "Facebook" ,
                "class" : "form-control"}),

            'twitter_url' : forms.TextInput(attrs={
                "placeholder" : "Twitter" ,
                "class" : "form-control"}),

            'linkedin_url' : forms.TextInput(attrs={
                "placeholder" : "Linkedin" ,
                "class" : "form-control"}),


            'region' : forms.Select(attrs={
                'class' : 'chosen-select-deselect form-control'
            }),
            'gender' : forms.Select( attrs={
                'class' : 'form-control',
            }),
            'age' : forms.Select( attrs={
                'class' : 'form-control',
                
            }),

            'highest_education_level' : forms.Select( attrs={
                'class' : 'form-control chosen-select-deselect',
            }),
            'employement_status' : forms.Select( attrs={
                'class' : 'form-control chosen-select-deselect',
            }),
            'job_types' :  forms.SelectMultiple( attrs={
                'class' : 'form-control multiselect chosen-select-deselect',

            }),
            'services_intersted_in' : forms.SelectMultiple( attrs={
                'class' : 'form-control multiselect chosen-select-deselect',
            }),
            
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
                "placeholder" : "Location","class" : "form-control"}),
            'region' : forms.Select(attrs={"class" : "chosen-select-deselect  form-control"}),
            'start_year' : forms.TextInput(attrs={
                "placeholder" : "Start Year" ,"class" : "form-control"}),

            'start_month' : forms.Select(attrs={
                "placeholder" : "Start Month","class" : "chosen-select-deselect form-control"}),

            'end_month' : forms.Select(attrs={
                "placeholder" : "End Month" ,"class" : "chosen-select-deselect form-control"}),

            'end_year' : forms.TextInput(attrs={
                "placeholder" : "End Year" ,"class" : "form-control"}),

            'description' : forms.Textarea(attrs={
                "placeholder" : "Description" ,'class' : "form-control"}),

            'is_currently' : forms.CheckboxInput(attrs={}),
            'job_title' : forms.TextInput(
                attrs={
                    "placeholder" : "Job Title","class" : "form-control"}),

            'company_name' : forms.TextInput(
                attrs={
                    "placeholder" : "Employer","class" : "form-control"})
        }


class SkillForm(forms.ModelForm):
    class Meta:
        model = models.Skill
        exclude = ('id', 'employee')
        widgets = {
            'name' : forms.TextInput(attrs={
                "placeholder" : "Area of Expertise ","class" : "form-control"}),
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
                "placeholder" : "Location" ,"class" : "form-control"}),
            'region' : forms.Select(attrs={'class' : 'chosen-select-deselect form-control'}),
            'start_year' : forms.TextInput(attrs={
                "placeholder" : "Start Year" ,"class" : "form-control"}),

            'start_month' : forms.Select(attrs={
                "placeholder" : "Start Month","class" : "chosen-select-deselect form-control"}),

            'end_month' : forms.Select(attrs={
                "placeholder" : "End Month" ,"class" : "chosen-select-deselect form-control"}),

            'end_year' : forms.TextInput(attrs={
                "placeholder" : "End Year","class" : "form-control"}),

            'description' : forms.Textarea(attrs={
                "placeholder" : "Description" ,'class' : "form-control"}),

            'is_currently' : forms.CheckboxInput(attrs={}),

            'school' : forms.TextInput(
                attrs={
                    "placeholder" : "School","class" : "form-control"}),

            'field_of_study' : forms.TextInput(
                attrs={
                    "placeholder" : "Field Of Study","class" : "form-control"}),
            
            'degree' : forms.Select(attrs={"class" : 'form-control'}),

        }

class CVForm(forms.ModelForm):
    class Meta:
        model = models.CV
        exclude = ('employee', )
        widgets = {
            'name' : forms.TextInput(attrs={
                "placeholder" : "Position Title","class" : "form-control"}),
        }

class ReferenceForm(forms.ModelForm):
    class Meta:
        model = models.References
        exclude = ('employee', )
        widgets = {
            'first_name' : forms.TextInput(attrs={
                "placeholder" : "First Name","class" : "form-control"}),
            
            'last_name' : forms.TextInput(attrs={
                "placeholder" : "Last Name","class" : "form-control"}),
            
            'organization' : forms.TextInput(attrs={
                "placeholder" : "Organization","class" : "form-control"}),
            
            'title' : forms.TextInput(attrs={
                "placeholder" : "Title","class" : "form-control"}),
            'phone' : forms.TextInput(attrs={
                "placeholder" : "Phone","class" : "form-control"}),
            
            'email' : forms.TextInput(attrs={
                "placeholder" : "Email","class" : "form-control"}),
        }

class AssociationForm(forms.ModelForm):
    class Meta:
        model = models.Association
        exclude = ('employee', )
        widgets = {
            'name' : forms.TextInput(attrs={
                "placeholder" : "name","class" : "form-control"}),
        }

class WorkSampleForm(forms.ModelForm):
    class Meta:
        model = models.WorkSample
        exclude = ('employee', )
        widgets = {
            'name' : forms.TextInput(attrs={
                "placeholder" : 'name',"class" : "form-control"}),
            
            'description' : forms.TextInput(attrs={
                "placeholder" : "description","class" : "form-control"}),
            
            'date' : forms.DateInput(attrs={
                "placeholder" : "Date","class" : "worksample-date form-control"}),

        }

class WorkLinkForm(forms.ModelForm):
    class Meta:
        model = models.WorkLink
        exclude = ('employee', )
        widgets = {
            'name' : forms.TextInput(attrs={
                "placeholder" : "Name","class" : "form-control"}),
            
            'url' : forms.TextInput(attrs={
                "placeholder" : "url","class" : "form-control"}),
            
            'description' : forms.TextInput(attrs={
                "placeholder" : "description","class" : "form-control"}),
            
            'title' : forms.TextInput(attrs={
                "placeholder" : "Title","class" : "form-control"}),
            'phone' : forms.TextInput(attrs={
                "placeholder" : "Phone","class" : "form-control"}),
            
            'email' : forms.TextInput(attrs={
                "placeholder" : "Email","class" : "form-control"}),
        }
    


