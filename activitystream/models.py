from django.db import models
from django.conf import settings

from datetime import datetime

from gestor.models import *

class Activity(models.Model):

    message = models.CharField(max_length = 200, null=True, blank=True, default = None)
    date = models.DateTimeField()
    link = models.URLField(null=True, blank=True, default = None)
    
    user = models.ForeignKey(User, related_name = 'activities', null=True, blank=True, default=None)
    object_id = models.IntegerField(null=True, blank=True, default = None)
    
    message_type = models.IntegerField()
    action_type = models.IntegerField(null=True, blank=True, default = None)
    
    MSG_DROPBOX = 0
    MSG_TWITTER = 1
    MSG_GESTOR_PROJECT = 2
    MSG_GESTOR_ACTION_ITEM = 3
    MSG_GESTOR_NOTE = 4
    
    ACTION_CREATE = 0
    ACTION_DONE = 1
	
	def save(self):
		if not self.id:
			self.date = datetime.datetime.now()
		super(Activity, self).save()
	
    def generate_text(self):
        "Generate the text to be shown on the interface"

        class ObjectNotFoundException(Exception): pass
        
        try:
        
            if self.message_type == self.MSG_DROPBOX:
                return 'Dropbox:' + self.message
            
            elif self.message_type == self.MSG_TWITTER:
                return 'jeKnowledge Twitter: ' + self.message
            
            elif self.message_type == self.MSG_GESTOR_PROJECT:
                project = Project.objects.get(id = self.object_id)
                if project: project = project[0]
                else: raise ObjectNotFoundException
                
                if self.action_type == self.ACTION_CREATE:
                    msg = ' create the project '
                else:
                    msg = ' closed the project '
                
                return user.get_full_name() + msg + self.project.name
            
            elif self.message_type == self.MSG_GESTOR_ACTION_ITEM:
                action_item = ActionItem.objects.get(id = self.object_id)
                if action_item: action_item = action_item[0]
                else: raise ObjectNotFoundException
                
                if self.action_type == self.ACTION_CREATE:
                    msg = ' create the action item '
                else:
                    msg = ' marked the action item '

                return user.get_full_name() + msg + self.action_item.title + ' as done on project ' + self.action_item.project.title
            
        except ObjectNotFoundException:
            pass
        return ""
