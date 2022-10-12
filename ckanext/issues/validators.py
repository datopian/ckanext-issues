import ckan.plugins.toolkit as tk
import ckan.lib.navl.dictization_functions as df
from ckan.common import _
Invalid = df.Invalid
Missing = df.Missing


from ckan.logic.validators  import (
    package_id_exists,
    group_id_exists,
    user_id_exists,
)

object_id_validators = {
    'new package' : package_id_exists,
    'changed package' : package_id_exists,
    'deleted package' : package_id_exists,
    'follow dataset' : package_id_exists,
    'new user' : user_id_exists,
    'changed user' : user_id_exists,
    'follow user' : user_id_exists,
    'new group' : group_id_exists,
    'changed group' : group_id_exists,
    'deleted group' : group_id_exists,
    'new organization' : group_id_exists,
    'changed organization' : group_id_exists,
    'deleted organization' : group_id_exists,
    'follow group' : group_id_exists,
    'changed issue' : package_id_exists,
    'new issue': package_id_exists,
    'issue closed': package_id_exists,
    'issue reopened': package_id_exists,
    'issue deleted': package_id_exists 
    }


def object_id_validator(key, activity_dict, errors, context):
    '''Validate the 'object_id' value of an activity_dict.

    Uses the object_id_validators dict (above) to find and call an 'object_id'
    validator function for the given activity_dict's 'activity_type' value.

    Raises Invalid if the model given in context contains no object of the
    correct type (according to the 'activity_type' value of the activity_dict)
    with the given ID.

    Raises Invalid if there is no object_id_validator for the activity_dict's
    'activity_type' value.

    '''
    activity_type = activity_dict[('activity_type',)]
    if object_id_validators.has_key(activity_type):
        object_id = activity_dict[('object_id',)]
        return object_id_validators[activity_type](object_id, context)
    else:
        raise tk.Invalid('There is no object_id validator for '
            'activity type "%s"' % activity_type)


def activity_type_exists(activity_type):
    '''Raises Invalid if there is no registered activity renderer for the
    given activity_type. Otherwise returns the given activity_type.

    This just uses object_id_validators as a lookup.
    very safe.

    '''
    if activity_type in object_id_validators:
        return activity_type
    else:
        raise Invalid('%s: %s' % (_('Not found'), _('Activity type')))