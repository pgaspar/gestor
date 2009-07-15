from __future__ import division
from datetime import date
from gestor.models import *

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
	try: txt = unicode(txt)
	except: return txt

	new_txt = txt[:int(lim)]

	if len(txt) > int(lim): new_txt += '...'
	return new_txt

def mergeLists(list_a, list_b):
	return list(list_a) + [el for el in list_b if el not in list_a]


def work_together(user, target):
	return len( (set(user.projects_working.all()) | set(user.projects_managed.all())) & (set(target.projects_working.all()) | set(target.projects_managed.all())) ) > 0
	
def get_stats(project = None):
	
	if project:
		q = project.actionitem_set
	else:
		q = ActionItem.objects
	
	faulty_tasks = q.filter(due_date__lt=datetime.today(), done=False)
	open_tasks = q.filter(done=False)
	faulty_users = list()
	
	for task in faulty_tasks:
		for user in task.targets.all(): faulty_users.append(user)
	
	faulty_users_comp = [ [faulty_users.count(user), user] for user in set( faulty_users ) ]
	
	if open_tasks: ratio = len( faulty_tasks ) / len( open_tasks )
	else: ratio = 0
	
	return {'open_tasks': open_tasks,
			'closed_tasks': q.filter(done=True), 
			'faulty_tasks': faulty_tasks,
			'faulty_users': sorted( faulty_users_comp )[::-1],
			'faulty_open_ratio': ratio,
			}