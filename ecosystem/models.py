from django.db import models

class Entity(models.Model):
    
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="logos")
    description = models.TextField()
    type = models.IntegerField(default=2, choices=((1, 'Client') ,(2, 'Partner'), (3, 'Supplier'), (4, 'Friend')) )