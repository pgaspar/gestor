from gestor.models import *

from django.db.models.fields import FieldDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse

#===============================================================================
# HELPERS
#===============================================================================

def generate_structured_response(structure, extension):
	"Generate the HTTP response for the given content and extension"
	
	# Default mimetype
	mimetype = "text/plain"
	
	# Default is XML
	if extension == 'xml' or not extension:
		from xml_generator import generate_xml
		result = generate_xml(structure)
		mimetype = 'application/xml'
	elif extension == 'json':
		from json_generator import generate_json
		result = generate_json(structure)
		mimetype = 'application/json' # from http://jibbering.com/blog/?p=514
	else:
		return generate_error("Invalid extension: '" + extension + "'")
		
	response = HttpResponse(result, mimetype = mimetype)
	return response

def generate_error(error_messsage = 'Unknown error', extension = 'xml'):
	"Generate a response with a given error message"
	error = {'error' : {'message' : error_messsage}}
	return generate_structured_response(error, extension)

def generate_authorization_error(extension = 'xml'):
	"Generate a response with a Not Authorized error."
	error = {'error' : {'message' : 'Not authorized.'}}
	return generate_structured_response(error, extension)

def generate_confirmation(message = 'OK', extension = 'xml'):
	"Generate a response with a confirmation message"
	confirm = {'ok' : {'message' : message}}
	return generate_structured_response(confirm, extension)

def get_arguments(request, extension):
	if request.method == 'POST':
		return request.POST
	elif request.method == 'GET':
		return request.GET
	elif request.method == 'PUT':
		request.method = "POST"
		arguments = request.POST
		request.method = "PUT"
		return arguments
	elif request.method == 'DELETE':
		return request.DELETE
	else:
		return generate_error("Request has to be GET, POST, PUT or DELETE.", extension)

def check_permissions( project, user, extension ):
	if not project.check_user( user ):
		return generate_authorization_error( extension )
	return None

#===============================================================================
# STRUCTURES
#===============================================================================

def generate_action_items_structure(action_items):
	action_item_list = []
	for action_item in action_items:
		fields = action_item.__dict__
		
		project = Project.objects.filter(id=fields["project_id"])
		fields.update( generate_projects_simple_structure(project)[0] )
		del fields["project_id"]
		
		author = User.objects.filter(id = fields["author_id"])
		fields["author"] =	generate_users_simple_structure(author)
		del fields["author_id"]
		
		targets = action_item.targets.all()
		fields["targets"] = generate_users_simple_structure(targets)
		
		action_item_list.append( {"action_item": fields } )

	structure = {"action_items" : action_item_list}
	return structure

def generate_users_simple_structure(users):
	users_list = []
	for user in users:
		user_structure = {}
		user_structure["id"] =		user.id
		user_structure["login"] =	user.username
		user_structure["name"] =	user.get_full_name()
		users_list.append( {"user" : user_structure} )
	return users_list

def generate_projects_simple_structure(projects):
	projects_list = []
	for project in projects:
		project_structure = {}
		project_structure["id"] =	   project.id
		project_structure["name"] =	   project.name
		projects_list.append( {"project" : project_structure} )
	return projects_list

def generate_projects_structure(projects):
	projects_list = []
	for project in projects:
		fields = project.__dict__
	
		manager = User.objects.filter(id = fields["manager_id"])
		fields["manager"] =	 generate_users_simple_structure(manager)
		del fields["manager_id"]
		
		team = project.team.all()
		fields["team"] =  generate_users_simple_structure(team)
	
		action_items = project.actionitem_set.all()
		fields.update( generate_action_items_structure(action_items) )
	
		projects_list.append( {"project" : fields} )
		
	structure = {"projects" : projects_list}
	return structure

#===============================================================================
# MODELS
#===============================================================================

def model_has_field(model, field):	  
	try:
		model._meta.get_field_by_name(field)
		return True
	except FieldDoesNotExist:
		return False

def update_action_item(action_item, arguments, extension):
	
	action_item_targets = []
	
	# Handle given arguments
	for key in arguments.keys():
		
		# Project
		if key == 'project_id':
			project_id =  arguments[key]
			project = Project.objects.filter( id = project_id )
			if project:
				action_item.project = project[0]
			else:
				return generate_error("Unknown project with id '" + project_id + "'", extension)
		
		# Targets	 
		elif key == 'targets':
			user_ids = arguments[key].split(',')
			
			for user_id in user_ids:
				user = User.objects.filter(id = user_id)
				if user:
					action_item_targets.append(user[0])
				else:
					return generate_error("Unknown user with id '" + user_id + "'", extension)
			print action_item_targets
		
		elif key == 'author' or key == 'author_id':
			return generate_error("Can't change an action item author.", extension)
		
		# Other atributes
		elif model_has_field(ActionItem, key):
			try:
				setattr(action_item, key, arguments[key])
			except Exception, exception:
				return generate_error("Invalid value '" + arguments[key] + "' for the attribute '" + key + "'", extension)
			
		else:
			return generate_error("Unknown action item attribute: '" + key + "'", extension)
	
	# Try to save the new action item
	try:
		action_item.save()
		if action_item_targets:
			action_item.targets = action_item_targets
	except Exception, error:
		return generate_error("IntegrityError: " + str(error), extension)

	return None 