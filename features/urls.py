from django.conf.urls.defaults import *

from views import FeaturesList, SiteFeaturesList, FeatureDetails


urlpatterns = patterns('',
    url(r'^sites/(?P<site_id>\d+)/$', SiteFeaturesList(), name='list_features_for_site'),
    url(r'^(?P<feature_id>\d+)/$', FeatureDetails(), name='show_feature_details'),
    url(r'^$', FeaturesList(), name='list_features'),
)

