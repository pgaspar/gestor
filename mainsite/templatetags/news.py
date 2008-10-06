from django.template import Library
from mainsite.models import News

register = Library()

@register.simple_tag
def latest_news():
	
	latest = News.objects.order_by('-date')[:10]
	
	html = "<ul id='news_list'>\n"
	for obj in latest:
		html += """<li>%s - <a href='%s'>%s</a></li>\n""" %(obj.date.strftime('%d-%m-%Y'), obj.get_absolute_url(), obj.title)
	
	html +="</ul>"
	return html
#register.tag('latest_news', latest_news)

