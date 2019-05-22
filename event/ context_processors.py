from event.models import MenuLinks
def menulink_processor(request):
    menulinks = MenuLinks.objects.all()            
    return {'menulinks': menulinks}