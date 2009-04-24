from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from django.core.exceptions import PermissionDenied

class ProjectManager(models.Manager):
	def get_query_set(self):
		return super(ProjectManager,self).get_query_set().filter(active=True)


class Project(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	active = models.BooleanField(default=True)
	manager = models.ForeignKey(User, related_name='projects_managed')
	team = models.ManyToManyField(User, related_name = 'projects_working')
	start_date = models.DateField()
	end_date = models.DateField()
	
	objects = models.Manager()
	workspace = ProjectManager()
	
	class Meta:
		ordering = ["-start_date"]
		permissions = [ ('view_project','Can view Projects'), ('view_intern_projects', 'Can view intern Projects') ]
	
	def __unicode__(self):
		return u"%s" % self.name
		
	def get_absolute_url(self):
		return "/gestor/project/%d/" % self.id
		
	def has_user(self,user):
		if user in self.team.all() or user == self.manager:
			return True
		return False
		
	def check_user(self,user):
		if not ( user.has_perm('gestor.view_project') or self.has_user(user) or (user.has_perm('gestor.view_intern_projects') and self.isIntern()) ):
			raise PermissionDenied()
	
	def check_manager(self, user, perm):
		if user != self.manager and not user.has_perm('gestor.' + perm + '_project'):
			raise PermissionDenied()
	
	def isIntern(self):
		return self.name.split('-')[0].lower() == 'jk'
	
	def ratio(self):
		done = self.actionitem_set.filter(done=True).count()
		total = self.actionitem_set.all().count()
		if total:
			return float(done) / total
		else:
			return 0
			
	def percentage(self):
		return str(int(round(self.ratio() * 100))) + "%"

class ActionItem(models.Model):
	project = models.ForeignKey(Project)
	title = models.CharField(max_length=100)
	description = models.TextField(blank=True, null=True)
	author = models.ForeignKey(User, related_name='actionitem_set')
	targets = models.ManyToManyField(User, related_name = 'actionitem_todo')
	set_date = models.DateField(auto_now=True)
	due_date = models.DateField(blank=True, null=True)
	done = models.BooleanField(default=False)
	priority = models.IntegerField(default=2, choices=((1, 'High') ,(2, 'Medium'), (3, 'Low')) )

	class Meta:
		ordering = ('done', 'priority', 'due_date')
	
	def __unicode__(self):
		return u"%s" % self.title
	
	def get_absolute_url(self):
		return "/gestor/action/%s/" % self.id 

class Note(models.Model):
	project = models.ForeignKey(Project)
	title = models.CharField(max_length=100)
	description = models.TextField(blank=True, null=True)
	author = models.ForeignKey(User)
	set_date = models.DateField(auto_now=True)
	
	class Meta:
		ordering = ["-set_date"]

	def __unicode__(self):
		return u"%s" % self.title
	
	def get_absolute_url(self):
		return "/gestor/note/%s/" % self.id
		
class ActionNote(models.Model):
	actionitem = models.ForeignKey(ActionItem)
	description = models.TextField(blank=True, null=True)
	author = models.ForeignKey(User)
	set_date = models.DateField(auto_now=True)
	
	class Meta:
		ordering = ["-set_date"]

	def __unicode__(self):
		return u"%s" % self.actionitem

	def get_absolute_url(self):
		return "/gestor/actionnote/%s/" % self.id

class File(models.Model):
	project = models.ForeignKey(Project)
	title = models.CharField(max_length=100)
	content = models.FileField(upload_to="files")
	author = models.ForeignKey(User)
	set_date = models.DateField(auto_now=True)
	
	class Meta:
		ordering = ["-set_date"]

	def __unicode__(self):
		return u"%s" % self.title

	def get_absolute_url(self):
		return "/gestor/file/%s/" % self.id