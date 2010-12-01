from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.conf import settings

from features import get_model
from decorators import as_json
from utils import obj_to_dict, get_name


DEFAULT_API_FIELDS = (
    'id',
    'title',
    'status',
    'description',
    ('site', lambda site: site.id),
    ('people', lambda user: get_name(user)),
    'is_ready',
    'progress',
    'is_launched',
    'is_stopped',
)


class JsonViewMeta(type):

    def __new__(cls, name, bases, attrs):
        new = super(JsonViewMeta, cls).__new__(cls, name, bases, attrs)
        new.__call__ = as_json(new.__call__)
        return new


class JsonView(object):
    __metaclass__ = JsonViewMeta


class FeaturesView(JsonView):
    model = get_model()
    fields = getattr(settings, 'FEATURES_API_FIELDS', DEFAULT_API_FIELDS)

    def __init__(self, fields=None):
        self.fields = fields or self.fields
        self.to_dict = obj_to_dict(self.fields)


class FeaturesList(FeaturesView):

    def __call__(self, request):
        return map(self.to_dict, self.model.objects.all())


class SiteFeaturesList(FeaturesView):
    
    def __call__(self, request, site_id):
        site = get_object_or_404(Site, id=site_id)
        return map(self.to_dict, self.model.objects.filter(site=site))


class FeatureDetails(FeaturesView):

    def __call__(self, request, feature_id):
        return self.to_dict(get_object_or_404(self.model, id=feature_id))
