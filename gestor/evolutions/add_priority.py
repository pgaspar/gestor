from django_evolution.mutations import *
from django.db import models

MUTATIONS = [
	AddField('ActionItem', 'priority', models.IntegerField, initial=2)
]