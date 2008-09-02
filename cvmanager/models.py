from django.db import models
from django.contrib.auth.models import User

class CurriculumVitae(models.Model):
    owner = models.OneToOneField(User)
    adress = models.CharField(max_length=100)
    homepage = models.CharField(max_length=40)
    phone = models.CharField(max_length=9)
    
    course = models.CharField(max_length=40)
    coruse_year = models.IntegerField()
    
    complements = models.TextField(max_length=1000)
    foreign_langs = models.TextField(max_length=1000)
    computer_skills = models.TextField(max_length=1000)
    other_skills = models.TextField(max_length=1000)
    interests = models.TextField(max_length=1000)
    proficient_areas = models.TextField(max_length=1000)
    
    set_date = models.DateField(auto_now_add=True)
    
    
    def __unicode__(self):
        return u"%s's Curriculum" % self.owner.get_full_name()
    
    def get_abolute_url(self):
        return "/users/%s/curriculum" % self.owner.username
