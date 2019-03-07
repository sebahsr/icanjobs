from django.forms import ModelForm
from jobs import models 

class CategoryForm(ModelForm):
    class Meta:
        model = models.Category
        exclude=('id',)
class JobForm(ModelForm):
    class Meta:
        model = models.Job
        exclude = ('id', )