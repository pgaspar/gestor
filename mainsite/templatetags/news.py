from django.template import Library
from mainsite.models import News

register = Library()

@register.simple_tag
def lastest_news():
	
	latest = News.objects.order_by('-date')[:5]
	
	b = "<ul class='news_block'>"
	for n in latest:
		b+= "<div class='news'></div>"
	
	b+="</ul>"
    return '<a href="mailto:%s">%s</a>' % (email, linktext)
