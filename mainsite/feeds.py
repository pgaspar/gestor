from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from mainsite.models import News
from django.contrib.syndication.feeds import Feed, FeedDoesNotExist

class NewsFeed(Feed):
    title_template = 'news_feed_title.html'
    description_template = "news_feed_description.html"
    
    def title(self):
        return u"jeKnowledge"
        
    def link(self):
        return u"/"

    def description(self):
        return u"Feed das noticias da jeKnowledge"
        
    def author_link(self):
        return u"http://jeknowledge.com/"
        
    def items(self):
        return News.objects.order_by('-date')[:15]
        