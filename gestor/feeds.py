from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import User
from gestor.models import ActionItem
from django.contrib.syndication.feeds import Feed, FeedDoesNotExist

class ActionItemFeed(Feed):
    title_template = 'action_feed_title.html'
    description_template = "action_feed_description.html"
    
    def get_object(self, bits):
        if len(bits) < 1:
            raise ObjectDoesNotExist
        return User.objects.get(username__exact=bits[0])
    
    def title(self, obj):
        return "Action Items Feed for %s" % obj.username
    
    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return "/"

    
    def description(self, obj):
        return "Action Items from all %s's projects" % obj.get_full_name()
    
    def items(self, obj):
        return obj.actionitem_todo.all().order_by('due_date')[:10]