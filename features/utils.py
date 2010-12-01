def get_name(user):
    return user.get_full_name() or user.username


def get_field(field, feature):
    if hasattr(field, '__iter__'):
        name, func = tuple(field)
    else:
        name, func = field, None

    value = getattr(feature, name)
    
    if hasattr(value, 'get_query_set'):
        value = value.all()
        if func:
            value = map(func, value)
    else:
        if func:
            value = func(value)
    
    return (name, value)


def obj_to_dict(fields):

    def _obj_to_dict(obj):
        return dict((get_field(field, obj) for field in fields))

    return _obj_to_dict
