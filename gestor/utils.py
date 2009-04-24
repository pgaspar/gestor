from datetime import date

def color_status(value):
	if value.done:
		return "green"
	if value.due_date > date.today():
		return "yellow"
	return "red"
	
def dist(d):
	dif =  d - date.today()
	return str(dif.days)
	
def truncate(txt, lim):
	new_txt = " ".join( txt.split()[:lim] )
	
	if len(txt.split()) > lim: new_txt += ' ...'
	
	return new_txt
	
def work_together(user, target):
	return len( (set(user.projects_working.all()) | set(user.projects_managed.all())) & (set(target.projects_working.all()) | set(target.projects_managed.all())) ) > 0