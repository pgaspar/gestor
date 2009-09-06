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

def get_arguments(request, extension):
    if request.method == 'POST':
        return request.POST
    elif request.method == 'GET':
        return request.GET
    else:
        return generate_error("Request has to be either GET or POST.", extension)


#===============================================================================
# REQUESTS
#===============================================================================

@basicauth()
def action_items_all(request, extension):
    """
    Show all the action items of the authenticated user
    / action_items / all    
    """
    action_items = request.user.actionitem_todo.all()
    structure = generate_action_items_structure(action_items)
    return generate_structured_response(structure, extension)

@basicauth()
def action_items_todo(request, extension):
    """
    Show all the action items not done of the authenticated user
    / action_items / todo    
    """
    action_items = request.user.actionitem_todo.filter(done = False)
    structure = generate_action_items_structure(action_items)
    return generate_structured_response(structure, extension)

@basicauth()
def action_items_create(request, extension):
    """
    Create a new action item
    / action_items / create    
    """
    arguments = get_arguments(request, extension)
    
    # Create action item
    new_action_item = ActionItem()
    new_action_item.author = request.user
    
    # Fill the action item with the arguments specified
    error = update_action_item(new_action_item, arguments, extension)

    if not error:
        return generate_confirmation("Action item created.", extension)
    else:
        return error
    
@basicauth()
def action_items_update(request, extension):
    """
    Updates an existing action item
    / action_items / update    
    """
    arguments = get_arguments(request, extension)
    
    # Get existing action item, using the given id
    if not arguments.has_key("id"):
        return generate_error("No 'id' was specified.", extension)
    action_item_id = arguments["id"]
    
    action_item = ActionItem.objects.filter( id = action_item_id )
    if not action_item:
        return generate_error("Unknown action item with id '" + action_item_id + "'.", extension)
    action_item = action_item[0] # Get the object from the queryset
    
    # Fill the action item with the arguments specified
    error = update_action_item(action_item, arguments, extension)

    if not error:
        return generate_confirmation("Action item updated.", extension)
    else:
        return error    
    




