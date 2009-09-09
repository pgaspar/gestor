#-*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from mainsite.models import News
from django.contrib.syndication.feeds import Feed, FeedDoesNotExist

class NewsFeed(Feed):
    description_template = "news_feed_description.html"
    
    categories = (u'júnior','FCTUC','Coimbra','empresa','empreendorismo','engenharia','jeknowledge','startup')
    
    def title(self):
        return u"jeKnowledge"
        
    def link(self):
        return u"/"
    
    def description(self):
        return u"Feed das noticias da jeKnowledge"
        
    def author_link(self):
        return u"http://jeknowledge.com/"
        
    def item_author_name(self, item):
        if item.has_author(): return item.author.get_full_name()
        else: return 'jeKnowledge'
        
    def item_pubdate(self, item):
        return item.date
        
    def items(self):
        return News.objects.filter(is_published=True).order_by('-date')[:15]
        
