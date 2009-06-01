from django.template import Library
from mainsite.models import News
from mainsite.utils import translate

register = Library()

@register.simple_tag
def latest_news(number = 5):
	latest = News.objects.order_by('-date')[:number]
	
	html = "<ul>\n"
	for obj in latest:
		html += "<li class='archive'><a href='%s'>%s</a></li>\n" %(obj.get_absolute_url(), obj.title)
	
	html += "</ul>"
	return html

@register.simple_tag
def load_archive(number = 0):
	date_list = News.objects.all().dates('date', 'month')[::-1]
	
	if number: date_list = date_list[:number]
	
	html = "<ul>\n"
	for obj in date_list:
		html += "<li><a href='/noticias/arquivo/%s'>%s</a></li>\n" %(obj.strftime('%Y/%m/'), " ".join( map( translate, obj.strftime('%B %Y').split() ) ))

	html += "</ul>"
	return html

@register.filter
def trans_month(string):
	return " ".join( map( translate, string.split() ) )