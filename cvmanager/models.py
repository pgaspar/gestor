from django.db import models
from django.contrib.auth.models import User
from cvmanager.fields import PTPhoneNumberField

from django.core.exceptions import PermissionDenied

class CurriculumVitae(models.Model):
    owner = models.OneToOneField(User)
    address = models.TextField()
    homepage = models.CharField(max_length=40)
    phone = PTPhoneNumberField()
    
    course = models.CharField(max_length=40)
    course_year = models.IntegerField()
    
    complements = models.TextField()
    foreign_langs = models.TextField()
    computer_skills = models.TextField()
    other_skills = models.TextField()
    interests = models.TextField()
    proficient_areas = models.TextField()
    
    set_date = models.DateField(auto_now_add=True)
    
    
    def __unicode__(self):
        return u"%s's Curriculum" % self.owner.get_full_name()
    
    def get_absolute_url(self):
        return "/users/%s/curriculum" % self.owner.username
    
    def check_user(self,user):
        if not user is self.owner:
            raise PermissionDenied()