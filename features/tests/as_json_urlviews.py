from django.conf.urls.defaults import patterns, url, handler500, handler404

from features.decorators import as_json


class DictTest:

    @as_json
    def __call__(self, request):
        return {'greeting': u'Hello, JSON!'}


class ListTest:

    @as_json
    def __call__(self, request):
        return [u'Hello, JSON!', 123]


urlpatterns = patterns('',
    url(r'^dict/$', DictTest(), name='test_dict'),
    url(r'^list/$', ListTest(), name='test_list'),
)

