from django.forms import *
from cvmanager.models import CurriculumVitae
from django.contrib.auth.models import User
from cvmanager.fields import PTPhoneNumberField

class CvForm(ModelForm):
    owner = ModelChoiceField(queryset=User.objects.all(),widget=HiddenInput())
    phone = PTPhoneNumberField()
    class Meta:
        model = CurriculumVitae