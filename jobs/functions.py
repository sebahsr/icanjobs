
def getFileName(instance, fileName):
        import random
        file_extension = fileName.rsplit(".", 1)[-1]
        return "%s_%d.%s" % (fileName, random.randint(1000, 10000000), file_extension )[0:32]

def is_employee(user):
        return hasattr(user, 'employee')

def is_company(user):
        return hasattr(user, 'company')
def can_access(request, user):
        if is_company:
                return True


def create_employee(strategy, details, backend, user=None, *args, **kwargs):
        from jobs import models
        if user  and not hasattr(user, 'employee') and not hasattr(user, 'company'):
                if strategy.session_get('usertype') == 'jobseeker':
                        user.employee = models.Employee.objects.create(user=user)
                        user.save()
                        return
                elif strategy.session_get('usertype') == 'employer':
                        user.company = models.Company.objects.create(user=user, name='%s' % (details.get('fullname')))
                        user.save()
                        return


def is_staff(user):
        return user.is_staff

from django.template.defaulttags import register
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def calc_emp_percent(employee):
        information_count = 0
        single_fields = ['profile_pic', 'gender', 'age', 'highest_education_level', 'employement_status', 'city', 'region', 'about_me', 'volunteer_experience', 'phone' ]
        multiple_fields = ['job_types', 'services_intersted_in','references','worklinks','worksamples','skills', 'educations','experiences']
        
        for single_field in single_fields:
                if getattr(employee, single_field):
                        information_count +=1
        for multiple_field in multiple_fields:
                if getattr(employee, multiple_field):
                        if getattr(employee, multiple_field).count() > 0:
                                information_count +=1

        total_count = len(single_fields) + len(multiple_fields)
        percent = (float(information_count)/total_count)*100
        return '%.0f' % (percent)

