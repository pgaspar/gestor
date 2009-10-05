
from activitystream.models import *
from django.template import Library

register = Library()

@register.filter
def activity_class(activity):
    if activity.message_type == Activity.MSG_GESTOR_PROJECT:
        return "activity-project"
    if activity.message_type == Activity.MSG_GESTOR_ACTION_ITEM:
        return "activity-actionitem"
    if activity.message_type in [Activity.MSG_GESTOR_NOTE, Activity.MSG_GESTOR_ACTION_NOTE]:
        return "activity-note"
    if activity.message_type == Activity.MSG_USER:
        return "activity-user"
    return ""