from django.forms import *
from cvmanager.models import CurriculumVitae
from django.contrib.auth.models import User


class CvForm(ModelForm):
    owner = ModelChoiceField(queryset=User.objects.all(),widget=HiddenInput())
    class Meta:
        model = CurriculumVitae