from django.conf.urls.defaults import patterns, url, handler500, handler404

from features.views import FeaturesList, SiteFeaturesList, FeatureDetails


FIELDS = (
    'title',
    'description',
)


urlpatterns = patterns('',
    url(r'^arg/sites/(?P<site_id>\d+)/$', SiteFeaturesList(FIELDS), name='list_features_for_site_arg'),
    url(r'^arg/(?P<feature_id>\d+)/$', FeatureDetails(FIELDS), name='show_feature_details_arg'),
    url(r'^arg/$', FeaturesList(FIELDS), name='list_features_arg'),

    url(r'^sites/(?P<site_id>\d+)/$', SiteFeaturesList(), name='list_features_for_site'),
    url(r'^(?P<feature_id>\d+)/$', FeatureDetails(), name='show_feature_details'),
    url(r'^$', FeaturesList(), name='list_features'),
)
