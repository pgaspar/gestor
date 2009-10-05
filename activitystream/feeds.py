from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from gestor.models import Activity
from django.contrib.syndication.feeds import Feed, FeedDoesNotExist

class ActivityStreamFeed(Feed):
    
    title = "jeKnowledge ActivityStream"
    link = "/gestor/stream/"
    description = "jeKnowledge ActivityStream"

    title_template = 'feed_title.html'
    description_template = "feed_description.html"

    def items(self):
        return Activity.objects.all()[:20]