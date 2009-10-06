from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from activitystream.models import Activity

class ProjectManager(models.Manager):
	def get_query_set(self):
		return super(ProjectManager,self).get_query_set().filter(active=True)


class Project(models.Model):
	name = models.CharField(max_length=100, default=None)
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
		permissions = [ ('view_project','Can view Projects'), 
						('view_intern_projects', 'Can view intern Projects'),
						('view_late_projects', 'Can view late Projects'),
						('view_late_users', 'Can view late Users') ]
	
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
			return False
		else: return True
	
	def check_manager(self, user, perm):
		if user != self.manager and not user.has_perm('gestor.' + perm + '_project'):
			return False
		else: return True
	
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
	
	def createActivity(self, action):
		activity = Activity( message_type = Activity.MSG_GESTOR_PROJECT, 
							 action_type = action, 
							 object_id = self.id,
							 message = self.name )
		activity.save()
	
	def save(self):
		new_object = not self.id
		
		super(Project, self).save() # Call the "real" save() method
		
		if new_object:
			action = Activity.ACTION_CREATE
		else:
			action = self.active and Activity.ACTION_EDIT or Activity.ACTION_CLOSE
		self.createActivity(action)
						     
	    
	def delete(self):
		super(Project, self).delete() # Call the "real" delete() method
		self.createActivity(Activity.ACTION_DELETE)

class ActionItem(models.Model):
	project = models.ForeignKey(Project)
	title = models.CharField(max_length=100, default=None)
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
	
	def createActivity(self, action):
		activity = Activity( message_type = Activity.MSG_GESTOR_ACTION_ITEM, 
							 action_type = action, 
							 object_id = self.id,
							 message = self.title )
		activity.save()
	
	def save(self):
		new_object = not self.id
		
		super(ActionItem, self).save() # Call the "real" save() method
		
		if new_object:
			action = Activity.ACTION_CREATE
		else:
			action = not self.done and Activity.ACTION_EDIT or Activity.ACTION_CLOSE
		self.createActivity(action)
						     
	    
	def delete(self):
		super(ActionItem, self).delete() # Call the "real" delete() method
		self.createActivity(Activity.ACTION_DELETE)	
	

class Note(models.Model):
	project = models.ForeignKey(Project)
	title = models.CharField(max_length=100, default=None)
	description = models.TextField(blank=True, null=True)
	author = models.ForeignKey(User)
	set_date = models.DateField(auto_now=True)
	
	class Meta:
		ordering = ["-set_date"]

	def __unicode__(self):
		return u"%s" % self.title
	
	def get_absolute_url(self):
		return "/gestor/note/%s/" % self.id
	
	def createActivity(self, action):
		activity = Activity( message_type = Activity.MSG_GESTOR_NOTE, 
							 action_type = action, 
							 object_id = self.id,
							 message = self.project.name )
		activity.save()
		
	def save(self):
		new_object = not self.id
		
		super(Note, self).save() # Call the "real" save() method
		
		if new_object:
			action = Activity.ACTION_CREATE
		else:
			action = Activity.ACTION_EDIT
		self.createActivity(action)
						     
	def delete(self):
		super(Note, self).delete() # Call the "real" delete() method
		self.createActivity(Activity.ACTION_DELETE)		
			
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

	def createActivity(self, action):
		activity = Activity( message_type = Activity.MSG_GESTOR_ACTION_NOTE, 
							 action_type = action, 
							 object_id = self.id,
							 message = self.actionitem.title )
		activity.save()
		
	def save(self):
		new_object = not self.id
		
		super(ActionNote, self).save() # Call the "real" save() method
		
		if new_object:
			action = Activity.ACTION_CREATE
		else:
			action = Activity.ACTION_EDIT
		self.createActivity(action)
						     
	def delete(self):
		super(ActionNote, self).delete() # Call the "real" delete() method
		self.createActivity(Activity.ACTION_DELETE)		
		