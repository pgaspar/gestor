from django_evolution.mutations import *
from django.db import models

MUTATIONS = [
	AddField('News', 'author', models.ForeignKey, initial=None, null=True, related_model='auth.User')
]