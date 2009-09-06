from django.http import Http404

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
        return generate_error_response("Invalid extension: '" + extension + "'")
        
    response = HttpResponse(result, mimetype="text/plain")
    return response

def generate_error_response(error_messsage, extension = 'xml'):
    "Generate a response with a given error message"
    error = {'error' : {'message' : error_messsage}}
    return generate_structured_response(error, extension)

#===============================================================================
# REQUESTS
#===============================================================================

@logged_in_or_basicauth()
def action_items_todo(request, extension):
    """
    Show all the action items not done
    / action_items / todo    
    """
    # Get todo action item list for the logged in user
    action_items = request.user.actionitem_todo.filter(done=False)
    
    structure = generate_action_items_structure(action_items)
    return generate_structured_response(structure, extension)



