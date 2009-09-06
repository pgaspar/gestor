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