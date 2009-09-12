from gestor.models import Project, ActionItem, Note, ActionNote
from cvmanager.models import CurriculumVitae
from accounts.models import UserProfile
from django.contrib.auth.models import User

from django.db.models import Q

# Search utils
	
def search_cv(search_term):
	return set( CurriculumVitae.objects.select_related("owner").filter(
					   Q(owner__first_name__icontains=search_term) \
					 | Q(owner__last_name__icontains=search_term) \
					 | Q(course__icontains=search_term) \
					 | Q(complements__icontains=search_term)    \
					 | Q(proficient_areas__icontains=search_term) \
					 | Q(foreign_langs__icontains=search_term) \
					 | Q(computer_skills__icontains=search_term) \
					 | Q(other_skills__icontains=search_term) \
					 | Q(interests__icontains=search_term) ) )

def search_user(search_term):
	return set( list( User.objects.filter(
							   Q(first_name__icontains=search_term) \
							 | Q(last_name__icontains=search_term) \
							 | Q(username__icontains=search_term) ) ) \
				+ [ p.user for p in UserProfile.objects.filter(
							   Q(organization__icontains=search_term) \
							 | Q(title__icontains=search_term) \
							 | Q(description__icontains=search_term) ) ] )

def search_proj(search_term):
	return set( Project.objects.filter( Q(name__icontains=search_term) \
							 | Q(description__icontains=search_term) ) )
						
def search_actionitem(search_term):
	return set( ActionItem.objects.filter( Q(title__icontains=search_term) \
							 | Q(description__icontains=search_term) ) )
							
def search_actionnote(search_term):
	return set( ActionNote.objects.filter( Q(actionitem__title__icontains=search_term) \
							 | Q(description__icontains=search_term) ) )

def search_note(search_term):
	return set( Note.objects.filter( Q(title__icontains=search_term) \
							 | Q(description__icontains=search_term) ) )


search_types = {'Cv':search_cv,
				'User':search_user,
				'Proj':search_proj,
				'ActionItem':search_actionitem,
				'ActionNote':search_actionnote,
				'Note':search_note}

def search(type, search_term):
	return search_types[type](search_term)