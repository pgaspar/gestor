from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

from cvmanager.utils import COURSES_CHOICES

class CurriculumVitae(models.Model):
    owner = models.ForeignKey(User, unique=True)
    address = models.TextField()
    phone = models.CharField("PhoneNumber",max_length=100)
    homepage = models.CharField("Webpage",max_length=40,blank=True,null=True)
    
    course = models.CharField(max_length=128,choices=[ (c,c) for c in COURSES_CHOICES ])
    course_year = models.IntegerField(choices=[ (n,str(n)) for n in range(1,7) ] )
    
    complements = models.TextField(blank=True,null=True)
    proficient_areas = models.TextField(blank=True,null=True)
    foreign_langs = models.TextField("Foreign Languages",blank=True,null=True)
    computer_skills = models.TextField("Computer Skills",blank=True,null=True)
    other_skills = models.TextField("Other Skills",blank=True,null=True)
    interests = models.TextField(blank=True,null=True)
    
    set_date = models.DateField(auto_now_add=True)
    
    
    def __unicode__(self):
        return u"%s's Curriculum" % self.owner.get_full_name()
    
    def get_absolute_url(self):
        return "/users/%s/curriculum" % self.owner.username
        
    def get_public_url(self):
        return "/%s/" % self.owner.username
    
    def check_user(self,user):
        if not user is self.owner:
            raise PermissionDenied()

    class Meta:
        permissions = ( ('can_view_cv','Can view CVs'), )