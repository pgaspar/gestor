from django.template import Library
from mainsite.models import News

register = Library()

@register.simple_tag
def latest_news(number):
	latest = News.objects.order_by('-date')[:number]
	
	html = "<ul>\n"
	for obj in latest:
		html += "<li><a href='%s'>%s</a></li>\n" %(obj.get_absolute_url(), obj.title)
	
	html += "</ul>"
	return html
