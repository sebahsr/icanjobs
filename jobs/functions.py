
def getFileName(instance, fileName):
        import random
        file_extension = fileName.rsplit(".", 1)[-1]
        return "%s_%d.%s" % (fileName, random.randint(1000, 10000000), file_extension )[0:32]

def is_employee(user):
        return hasattr(user, 'employee')

def is_company(user):
        return hasattr(user, 'company')

def create_employee(strategy, details, backend, user=None, *args, **kwargs):
        print details
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