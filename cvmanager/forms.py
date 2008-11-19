from django.forms import *
from cvmanager.models import CurriculumVitae
from django.contrib.auth.models import User
from cvmanager.fields import PTPhoneNumberField

class CvForm(ModelForm):
    owner = ModelChoiceField(queryset=User.objects.all(),widget=HiddenInput())
    phone = PTPhoneNumberField()
    complements = CharField(required=False,widget=Textarea(),help_text="<div style='float: right; width: 35%;'><b>Example:</b> Webdesign Workshop given by jeKnowledge in 2008, Robotic course given by DEEC-UC in 2004, etc<br /><b> And supports <a href='http://hobix.com/textile/'>textile</a>. Same for all below.</b></div>")
    class Meta:
        model = CurriculumVitae

class CvFindForm(Form):
	find = CharField(label="Looking for:")