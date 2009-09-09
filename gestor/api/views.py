from gestor.models  import *

from gestor.api.lib.basic_auth import *
from gestor.api.lib.views_utils import *

    
#===============================================================================
# REQUESTS
#===============================================================================

# PROJECTS

@basicauth()
def projects(request, extension):
    """
    Show all the projects of the authenticated user
    / projects / all    
    """
    projects = request.user.projects_working.all()
    structure = { 'projects' : generate_projects_simple_structure(projects) }
    return generate_structured_response(structure, extension)

@basicauth()
def projects_show(request, project_id, extension):
    """
    Show the project with the specified ID
    / projects / 123 / show    
    """
    project = request.user.projects_working.filter( id = project_id )
    if not project:
        return generate_error("Unknown project with id '" + project_id + "'", extension)
    
    # Check permissions
    not_authorized = check_permissions( project[0], request.user, extension )
    if not_authorized:
		return not_authorized
    
    structure = generate_projects_structure(project)
    return generate_structured_response(structure, extension)


# ACTION ITEMS

@basicauth()
def action_items(request, extension):
    """
    Show all the action items of the authenticated user
    / action_items / all    
    """

    if request.method == "POST":
        return action_items_create( request, extension)

    action_items = request.user.actionitem_todo.all()
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

    # Check permissions
    if arguments.has_key('project_id'):
        project = Project.objects.filter( id = arguments['project_id'] )
        not_authorized = check_permissions( project[0], request.user, extension )
        if not_authorized: return not_authorized

    # Fill the action item with the arguments specified
    error = update_action_item(new_action_item, arguments, extension)

    if not error:
        return generate_confirmation("Action item created.", extension, status = 201)
    else:
        return error


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
def action_item(request, item_id, extension):
    if request.method == "PUT":
        return action_items_update(request, item_id, extension)
    elif request.method == "DELETE":
        return action_items_delete(request, item_id, extension)
    else:
        return action_items_show(request, item_id, extension)

@basicauth()
def action_items_show(request, item_id, extension):
    """
    Shows an existing action item
    / action_items / 123 / show    
    """
    action_item = ActionItem.objects.filter( id = item_id )
    if not action_item:
        return generate_error("Unknown action item with id '" + item_id + "'.", extension)
    
    # Check permissions
    not_authorized = check_permissions( action_item[0].project, request.user, extension )
    if not_authorized: return not_authorized
    
    structure = generate_action_items_structure(action_item)
    return generate_structured_response(structure, extension)
    
@basicauth()
def action_items_update(request, item_id, extension):
    """
    Updates an existing action item
    / action_items / 123 / update    
    """
    
    action_item = ActionItem.objects.filter( id = item_id )
    if not action_item:
        return generate_error("Unknown action item with id '" + item_id + "'.", extension)
    action_item = action_item[0] # Get the object from the queryset
    
    # Check permissions
    not_authorized = check_permissions( action_item.project, request.user, extension )
    if not_authorized: return not_authorized
    
    # Fill the action item with the arguments specified
    arguments = get_arguments(request, extension)
    error = update_action_item(action_item, arguments, extension)

    if not error:
        return generate_confirmation("Action item updated.", extension)
    else:
        return error    
    
@basicauth()
def action_items_delete(request, item_id, extension):
    """
    Updates an existing action item
    """
    action_item = ActionItem.objects.filter( id = item_id )
    if not action_item:
        return generate_error("Unknown action item with id '" + item_id + "'.", extension)
    action_item = action_item[0] # Get the object from the queryset
    
    # Check permissions
    not_authorized = check_permissions( action_item.project, request.user, extension )
    if not_authorized: return not_authorized
    
    action_item.delete()

    return generate_confirmation("Action item deleted.", extension)
