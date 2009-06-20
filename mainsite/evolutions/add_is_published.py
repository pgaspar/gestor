from django_evolution.mutations import *
from django.db import models

MUTATIONS = [
	AddField('News', 'is_published', models.BooleanField, initial=True)
]