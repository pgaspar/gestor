from gestor.models import *
from django.db.models.fields import FieldDoesNotExist

def model_has_field(model, field):    
    try:
        model._meta.get_field_by_name(field)
        return True
    except FieldDoesNotExist:
        return False

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
        fields["author"] =  generate_users_simple_structure(author)
        del fields["author_id"]
        
        targets = action_item.targets.all()
        fields["targets"] = generate_users_simple_structure(targets)
        
        action_item_list.append( {"action_item": fields } )

    structure = {"action_items" : action_item_list}
    return structure

def generate_projects_simple_structure(projects):
    projects_list = []
    for project in projects:
        project_structure = {}
        project_structure["id"] =      project.id
        project_structure["name"] =    project.name
        projects_list.append( {"project" : project_structure} )
    return projects_list

def generate_users_simple_structure(users):
    users_list = []
    for user in users:
        user_structure = {}
        user_structure["id"] =      user.id
        user_structure["login"] =   user.username
        user_structure["name"] =    user.get_full_name()
        users_list.append( {"user" : user_structure} )
    return users_list



#===============================================================================
# MODELS
#===============================================================================

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
        return generate_error("IntegrityError: " + str(error))

    return None 