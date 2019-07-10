from django.core.exceptions import PermissionDenied
from jobs import models

def user_can_acces(function):
    def wrap(request, accesstoken, *args, **kwargs):
        if accesstoken:
            try:
                accesstoken = models.AccessToken.objects.get(value=accesstoken)
                request.user.company = accesstoken.company
                return function(request, accesstoken)
            except Exception as e:
                pass
            
        
        raise PermissionDenied
        
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def can_view_employee(function):
    def wrap(request, applicationID, accesstoken):
        if accesstoken:
            try:
                accesstoken = models.AccessToken.objects.get(value=accesstoken)
                request.user.company = accesstoken.company
                
                return function(request, applicationID, accesstoken, dont_print=True)
            except Exception as e:
                print e
                pass
            
        
        raise PermissionDenied
        
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap