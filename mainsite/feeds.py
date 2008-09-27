from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from mainsite.models import News
from django.contrib.syndication.feeds import Feed, FeedDoesNotExist

class NewsFeed(Feed):
    title_template = 'news_feed_title.html'
    description_template = "news_feed_description.html"
    
    def get_object(self, bits):
        return news.objects.order_by('-date')[:5]
    
    def title(self, obj):
        return u"jeKnowledge"
    
    def items(self, obj):
        return obj.actionitem_todo.all().order_by('-set_date')[:10]