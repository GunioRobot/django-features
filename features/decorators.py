from django.utils.simplejson import dumps
from django.http import HttpResponse


def as_json(func):
    def wrapper(*args, **kwargs):
        data = func(*args, **kwargs)
        return HttpResponse(dumps(data), mimetype='application/json')
    return wrapper
