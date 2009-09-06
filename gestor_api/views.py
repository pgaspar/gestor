from django.http import Http404
from django.db import IntegrityError

from gestor.models  import *
from basic_auth     import *

from views_utils import *

#===============================================================================
# HELPERS
#===============================================================================

def generate_structured_response(structure, extension):
    "Generate the HTTP response for the given content and extension"
    
    # Default is XML
    if extension == 'xml' or not extension:
        from xml_generator import generate_xml
        result = generate_xml(structure)
    else:
        return generate_error("Invalid extension: '" + extension + "'")
        
    response = HttpResponse(result, mimetype="text/plain")
    return response

def generate_error(error_messsage = 'Unknown error', extension = 'xml'):
    "Generate a response with a given error message"
    error = {'error' : {'message' : error_messsage}}
    return generate_structured_response(error, extension)

def generate_confirmation(message = 'OK', extension = 'xml'):
    "Generate a response with a confirmation message"
    confirm = {'ok' : {'message' : message}}
    return generate_structured_response(confirm, extension)


#===============================================================================
# REQUESTS
#===============================================================================

@logged_in_or_basicauth()
def action_items_all(request, extension):
    """
    Show all the action items of the authenticated user
    / action_items / all    
    """
    action_items = request.user.actionitem_todo.all()
    structure = generate_action_items_structure(action_items)
    return generate_structured_response(structure, extension)

@logged_in_or_basicauth()
def action_items_todo(request, extension):
    """
    Show all the action items not done of the authenticated user
    / action_items / todo    
    """
    action_items = request.user.actionitem_todo.filter(done = False)
    structure = generate_action_items_structure(action_items)
    return generate_structured_response(structure, extension)

@logged_in_or_basicauth()
def action_items_create(request, extension):
    """
    Create a new action item
    / action_items / create    
    """
    arguments = request.GET
    
    # Create action item
    new_action_item = ActionItem()
    new_action_item.author = request.user
    action_item_targets = []
    
    # Handle given arguments
    for key in arguments.keys():
        
        # Project
        if key == 'project_id':
            project_id =  arguments[key]
            project = Project.objects.filter( id = project_id )
            if project:
                new_action_item.project = project[0]
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
            
        # Other atributes
        elif model_has_field(ActionItem, key):
            try:
                setattr(new_action_item, key, arguments[key])
            except Exception, exception:
                return generate_error("Invalid value '" + arguments[key] + "' for the attribute '" + key + "'", extension)
            
        else:
            return generate_error("Unknown action item attribute: '" + key + "'", extension)
    
    if not action_item_targets:
        return generate_error("The argument 'targets' is not defined. An action item needs user targets.", extension)
    
    # Try to save the new action item
    try:
        print new_action_item.due_date
        new_action_item.save()
        new_action_item.targets = action_item_targets
    except Exception, error:
        return generate_error("IntegrityError: " + str(error))
    
    return generate_confirmation("Action item created.", extension)
    






