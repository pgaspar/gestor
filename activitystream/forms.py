from django.forms import *
from activitystream.models import *

class ActivityMessageForm(Form):
    message = CharField(max_length=140, min_length=1,
                        widget=forms.TextInput(attrs={'size':'100'}))