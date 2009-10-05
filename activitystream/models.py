from django.db import models
from django.conf import settings

from datetime import datetime

from middleware.threadlocals import get_current_user

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
    MSG_GESTOR_ACTION_NOTE = 5    
    MSG_USER = 6
    
    ACTION_CREATE = 0
    ACTION_EDIT = 1
    ACTION_DELETE = 2
    ACTION_CLOSE = 3
	
    class Meta:
        ordering = ["-date"]
    
    def save(self):
    	if not self.id:
    		self.date = datetime.now()
        self.user = get_current_user()
    	super(Activity, self).save()

    
    def generate_text(self):
        "Generate the text to be shown on the interface"
        
        if self.message_type == self.MSG_DROPBOX:
            message = 'Dropbox:' + '<a href="' + self.link + '">' + self.message + '</a>'
        
        elif self.message_type == self.MSG_TWITTER:
            message = 'jeKnowledge Twitter: ' + '<a href="' + self.link + '">' + self.message + '</a>'
            
        elif self.message_type == self.MSG_USER:
            message = ': ' + self.message
        
        elif self.message_type == self.MSG_GESTOR_PROJECT:
            project = self.get_related_object()
            if project:
                project_part = '<a href="' + project.get_absolute_url() + '">' + project.name + '</a>'
                message = self.get_action_string() + ' the project ' + project_part
            else:
                message = self.get_action_string() + ' the project ' + self.message
        
        elif self.message_type == self.MSG_GESTOR_ACTION_ITEM:
            action_item = self.get_related_object()
            if action_item:
                action_item_part = '<a href="' + action_item.get_absolute_url() + '">' + action_item.title  + '</a>'
                project_part = '<a href="' + action_item.project.get_absolute_url() + '">' + action_item.project.name + '</a>'
                message = self.get_action_string() + ' the action item ' + action_item_part + ' on project ' + project_part
            else:
                message = self.get_action_string() + ' the action item ' + self.message
                
        elif self.message_type == self.MSG_GESTOR_NOTE:
            note = self.get_related_object()
            if note:
                project_part = '<a href="' + note.project.get_absolute_url() + '">' + note.project.name + '</a>'
                message = self.get_action_string() + ' a <b>note</b> on project ' + project_part
            else:
                message = self.get_action_string() + ' a <b>note</b> on project ' + self.message
            
        elif self.message_type == self.MSG_GESTOR_ACTION_NOTE:
            note = self.get_related_object()
            if note:
                action_item_part = '<a href="' + note.actionitem.get_absolute_url() + '">' + note.actionitem.title + '</a>'
                project_part = '<a href="' + note.actionitem.project.get_absolute_url() + '">' + note.actionitem.project.name + '</a>'
                message = self.get_action_string() + ' a <b>note</b> on the action item ' + action_item_part + ' of ' + project_part
            else:
                message = self.get_action_string() + ' a <b>note</b> on the action item ' + self.message
                
        return self.get_user_string() + message
    
    def get_related_object(self):
        model = self.get_related_model()
        object = model.objects.filter(id = self.object_id)
        if object: 
            return object[0]
        else: 
            return None
            
    def get_related_model(self):      
        from gestor.models import * 
        if self.message_type == self.MSG_GESTOR_PROJECT:
            model = Project
        elif self.message_type == self.MSG_GESTOR_ACTION_ITEM:
            model = ActionItem
        elif self.message_type == self.MSG_GESTOR_NOTE:
            model = Note
        elif self.message_type == self.MSG_GESTOR_ACTION_NOTE:
            model = ActionNote
        else:
            return None
        return model
        
    def get_user_string(self):    
        if self.user:
            return '<a href="' + self.user.get_absolute_url() + '">' + self.user.get_full_name() + '</a>'
        else:
            return ''
        
    def get_action_string(self):
        if self.action_type == self.ACTION_CREATE:
            str = ' created '
        elif self.action_type == self.ACTION_EDIT:    
            str = ' edited '
        elif self.action_type == self.ACTION_DELETE:
            str = ' deleted '
        elif self.action_type == self.ACTION_CLOSE:
            str = ' closed '
        else:
            str = ''
        return str
            
            
            
            
