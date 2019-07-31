from jobs import models 
import datetime

class SimpleMiddleware:
    VISITOR_KEY = 'visitor-key'

    def __init__(self, get_response):
        self.get_response = get_response
 
    def __call__(self, request):
        response = self.get_response(request)

        if request.get_full_path().startswith('/ican/') or request.get_full_path().startswith('/company/'):
            return response

        visitorCookie = request.COOKIES.get(SimpleMiddleware.VISITOR_KEY, None)

        visitCount = models.VisitCount.objects.filter(visitDate=datetime.date.today()).first()
            
        if not visitCount:
            visitCount = models.VisitCount.objects.create(uniqueHitCount=0, totalHitCount=0)
            
        if not visitorCookie:
            visitCount.uniqueHitCount+=1
        
        visitCount.totalHitCount +=1
        visitCount.save()
        print visitCount, "HERE AND THERE", visitCount.totalHitCount

        max_age = 7 * 24 * 60 * 60 
        expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
        response.set_cookie(SimpleMiddleware.VISITOR_KEY, 'dkslfj12312321fsdfs', expires=expires)

        return response